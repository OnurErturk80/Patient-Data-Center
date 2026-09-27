# -*- coding: utf-8 -*-
"""Paketin duman testi (v6.204).

Derlenmiş programı açar, boş bir veri klasöründe ilk kurulumu yapar (sahte
bir laboratuvar, hasta verisi yok), ekranları dener, kapatır. GitHub Actions
her derlemede çalıştırıyor (`.github/workflows/paket.yml`); elle de olur:

    python3 paket/dene.py program <çalıştırılabilir dosya>
        Programı kendisi açar: geçici veri klasörü, portlar 18000/18443,
        `PYTHONPATH` temizlenmiş (paket kaynak klasörüne yaslanmasın). İkinci
        açılışı ("program zaten çalışıyor") ve Mac'te yenilenmiş uygulamanın
        eski derlemeyi kapatıp yerine geçmesini de dener.
    python3 paket/dene.py kurulu [--yeniden]
        Windows: kurulum dosyasıyla kurulmuş, Görev Zamanlayıcı'nın açtığı
        program (portlar 8000/8443). --yeniden: kurulum ikinci kez çalıştı
        (güncelleme); ilk seferin veritabanı yerinde olmalı.
    python3 paket/dene.py oturum <Uygulamalar'daki çalıştırılabilir dosya>
        Mac: çift tıklamayla açılan uygulama oturum açılışı için LaunchAgent
        yazıyor mu.

Yalnızca standart kütüphane: derleme makinesine programın kendi
bağımlılıkları dışında bir şey kurulmasın. Başarısızlıkta programın günlüğü
(`program.log`) basılıyor -- GitHub'ın makinesinde bakılacak başka yer yok.
"""
import http.cookiejar
import json
import os
import plistlib
import re
import shutil
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

KULLANICI = "deneme"
SIFRE = "deneme-1234"
MAC_ETIKETI = "com.patientdatacenter.pdc"      # baslat.MAC_ETIKETI
# Program açılışı bundan uzun sürerse bir şey takılıyor demek (v6.204: Mac'te
# makine adını çözmek 70 sn sürmüş, program o arada hiç açılmamıştı). İlk
# açılışta kök sertifikanın anahtarı üretiliyor, o yüzden pay var.
ACILIS_SINIRI_SN = 45

# Giriş yapmış yöneticinin açabilmesi gereken ekranlar (200).
EKRANLAR = [
    "/", "/hastalar", "/cryo", "/yonetim", "/istatistik", "/bakanlik",
    "/hasta/yeni", "/klasorler", "/yedekleme", "/ag-erisimi", "/baglan",
    "/kullanicilar", "/formlar", "/dil", "/bitenler", "/devam-eden",
    "/yaklasanlar", "/sifre-istekleri", "/manifest.json", "/sw.js",
    "/sertifika", "/static/style.css", "/disari/istatistik",
]


class DenemeHatasi(Exception):
    pass


def ok(kosul, mesaj):
    if not kosul:
        raise DenemeHatasi(mesaj)


class _Yonlendirmesiz(urllib.request.HTTPRedirectHandler):
    """303'ün kendisi görülsün: yönlendirmenin hedefi de denetleniyor."""
    def redirect_request(self, *a, **k):
        return None


class Istemci:
    """Oturum çerezini taşıyan, vekil sunucu kullanmayan, yönlendirmeyi
    izlemeyen tarayıcı yerine geçen."""
    def __init__(self, port):
        self.kok = f"http://127.0.0.1:{port}"
        self.acici = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), _Yonlendirmesiz(),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def iste(self, yol, veri=None):
        govde = None if veri is None else urllib.parse.urlencode(veri).encode()
        try:
            with self.acici.open(self.kok + yol, data=govde, timeout=180) as y:
                return y.status, _basliklar(y.headers), y.read()
        except urllib.error.HTTPError as e:
            return e.code, _basliklar(e.headers), e.read()


def _basliklar(h):
    return {k.lower(): v for k, v in h.items()}


def _metin(g):
    return g.decode("utf-8", "replace")


def port_dolu(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def pdc(port):
    """Çalışan programın kendini tanıtması (`GET /__pdc`), yoksa None."""
    acici = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with acici.open(f"http://127.0.0.1:{port}/__pdc", timeout=10) as y:
            return json.loads(y.read().decode("utf-8"))
    except Exception:
        return None


def pdc_bekle(port, sure, surec=None, pid=None):
    """Program cevap verene kadar bekle; `pid` verilirse o süreç olmalı."""
    son = time.time() + sure
    while time.time() < son:
        if surec is not None and surec.poll() is not None:
            raise DenemeHatasi(f"program kapandi (cikis kodu {surec.returncode})")
        bilgi = pdc(port)
        if bilgi and (pid is None or bilgi.get("pid") == pid):
            return bilgi
        time.sleep(0.5)
    raise DenemeHatasi(f"program {sure} sn icinde port {port}'ta cevap vermedi")


def _sure_denetle(ne, t0):
    sure = time.time() - t0
    print(f"  {ne}: {sure:.1f} sn")
    ok(sure <= ACILIS_SINIRI_SN,
       f"{ne} {sure:.0f} sn surdu ({ACILIS_SINIRI_SN} sn'den uzun): acilista bir sey takiliyor")


def ayni_yer(a, b):
    return (os.path.normcase(os.path.realpath(str(a)))
            == os.path.normcase(os.path.realpath(str(b))))


def kapat(surec, beklenen_temiz=True):
    """Programı kapat. POSIX'te SIGTERM (düzgün kapanış: `baslat._iki_kapi`,
    Mac'te eski derlemeyi kapatmak da buna dayanıyor), Windows'ta TerminateProcess."""
    if surec.poll() is not None:
        return
    if os.name == "nt":
        surec.terminate()
        surec.wait(30)
        return
    surec.send_signal(signal.SIGTERM)
    try:
        surec.wait(40)
    except subprocess.TimeoutExpired:
        surec.kill()
        surec.wait(10)
        raise DenemeHatasi("program SIGTERM ile 40 sn icinde kapanmadi")
    if beklenen_temiz:
        ok(surec.returncode == 0, f"SIGTERM'den sonra cikis kodu {surec.returncode}")


# -------------------------------------------------------------------- ekranlar

def ekranlari_dene(port, https_port, ilk=True):
    i = Istemci(port)
    if ilk:
        d, h, _ = i.iste("/")
        ok(d == 303 and h.get("location", "").endswith("/kurulum"),
           f"veritabani yokken / ilk kurulum ekranina gitmeli: {d} {h.get('location')}")
        d, _, g = i.iste("/kurulum")
        ok(d == 200 and "İlk kurulum" in _metin(g), f"/kurulum: {d}")
        d, h, g = i.iste("/kurulum/yeni", {
            "lab_adi": "Deneme Laboratuvarı", "ad_soyad": "Deneme Yönetici",
            "kisa_kod": "DY", "kullanici_adi": KULLANICI,
            "sifre": SIFRE, "sifre2": SIFRE})
        ok(d == 303 and h.get("location", "").endswith("/kurulum/tamam"),
           f"yeni laboratuvar kurulamadi: {d} {h.get('location')} {_metin(g)[:300]}")
        d, _, g = i.iste("/kurulum/tamam")
        ok(d == 200, f"/kurulum/tamam: {d}")
        print("  ilk kurulum: yeni laboratuvar kuruldu")
    d, h, _ = i.iste("/giris", {"kullanici_adi": KULLANICI, "sifre": SIFRE})
    ok(d == 303 and h.get("location") == "/", f"giris yapilamadi: {d} {h.get('location')}")
    for yol in EKRANLAR:
        d, _, g = i.iste(yol)
        ok(d == 200, f"{yol}: {d} {_metin(g)[:200]}")
    print(f"  {len(EKRANLAR)} ekran acildi")

    if ilk:
        d, h, _ = i.iste("/hasta/yeni", {"dosya_no": "900001", "ad_soyad": "deneme hasta"})
        m = re.search(r"/hasta/(\d+)$", h.get("location", ""))
        ok(d == 303 and m, f"hasta kaydedilemedi: {d} {h.get('location')}")
        hid = m.group(1)
        d, _, g = i.iste(f"/hasta/{hid}")
        ok(d == 200 and "DENEME HASTA" in _metin(g), f"hasta karti: {d}")
        d, h, g = i.iste(f"/hasta/{hid}/cycle/yeni", {
            "cycle_no": "2026-9001", "cycle_tipi": "ivf_icsi",
            "opu_zamani": "2026-09-20T09:00"})
        m = re.search(r"/cycle/(\d+)$", h.get("location", ""))
        ok(d == 303 and m, f"tedavi acilamadi: {d} {h.get('location')} {_metin(g)[:300]}")
        cid = m.group(1)
        for yol in (f"/cycle/{cid}", f"/cycle/{cid}/opu", f"/cycle/{cid}/icsi",
                    f"/cycle/{cid}/vitrifikasyon", f"/form/ozet/{cid}",
                    f"/form/artlab/{cid}"):
            d, _, g = i.iste(yol)
            ok(d == 200, f"{yol}: {d} {_metin(g)[:200]}")
        for yol in (f"/disari/cycle/{cid}", f"/disari/form/ozet/{cid}",
                    f"/disari/form/artlab/{cid}", "/disari/ay", "/disari/tumu",
                    "/disari/cryo"):
            d, _, g = i.iste(yol)
            ok(d == 200 and g[:2] == b"PK", f"{yol}: {d} Excel degil")
        print("  hasta, tedavi, resmi formlar ve Excel ciktilari tamam")
    else:
        d, _, g = i.iste("/hastalar")
        ok(d == 200 and "DENEME HASTA" in _metin(g),
           "guncellemeden sonra ilk seferin hastasi yok: veritabani korunmadi")
        print("  veritabani guncellemede korundu")

    if https_port:
        baglam = ssl.create_default_context()
        baglam.check_hostname = False
        baglam.verify_mode = ssl.CERT_NONE
        acici = urllib.request.build_opener(urllib.request.ProxyHandler({}),
                                            urllib.request.HTTPSHandler(context=baglam))
        with acici.open(f"https://127.0.0.1:{https_port}/manifest.json", timeout=30) as y:
            ok(y.status == 200, f"HTTPS: {y.status}")
        print(f"  HTTPS ({https_port}) acik")


def gunlugu_denetle(veri):
    gunluk = Path(veri) / "program.log"
    ok(gunluk.exists(), "program.log yazilmamis")
    metin = gunluk.read_text(encoding="utf-8", errors="replace")
    ok("GOC:" in metin and "goc uygulandi" in metin, "gunlukte goc ozeti yok")
    ok("Traceback" not in metin and "Exception in ASGI" not in metin,
       "gunlukte hata var")
    print("  gunluk temiz (goc ozeti var, hata yok)")


def gunlugu_bas(veri):
    gunluk = Path(veri) / "program.log"
    if gunluk.exists():
        print("---- program.log (son 120 satir) ----")
        print("\n".join(gunluk.read_text(encoding="utf-8", errors="replace")
                        .splitlines()[-120:]))


# ------------------------------------------------------------------------ kipler

def _ortam(veri, port, https_port):
    ortam = dict(os.environ, LAB_VERI=str(veri), LAB_PORT=str(port),
                 LAB_HTTPS_PORT=str(https_port), LAB_SESSIZ="1")
    ortam.pop("PYTHONPATH", None)
    return ortam


def kip_program(exe, port=18000, https_port=18443):
    exe = str(Path(exe).resolve())
    ok(Path(exe).exists(), f"program yok: {exe}")
    ok(not port_dolu(port), f"port {port} dolu, deneme baslayamaz")
    veri = Path(tempfile.mkdtemp(prefix="pdc_dene_"))
    ortam = _ortam(veri, port, https_port)
    print(f"Program: {exe}\nVeri   : {veri}")
    surecler = []
    try:
        t0 = time.time()
        p1 = subprocess.Popen([exe, "--servis"], env=ortam, cwd=str(veri))
        surecler.append(p1)
        bilgi = pdc_bekle(port, 180, surec=p1)
        _sure_denetle("ilk acilis", t0)
        ok(ayni_yer(bilgi.get("veri"), veri), f"veri klasoru yanlis: {bilgi.get('veri')}")
        ok(bilgi.get("paket"), "paket_bilgisi.json pakete girmemis")
        ok(bilgi.get("surum"), "README.md pakete girmemis (surum yok)")
        print(f"  acildi: {bilgi['paket']} (surec {bilgi['pid']})")
        ekranlari_dene(port, https_port, ilk=True)

        # İkinci açılış: yeni sunucu açılmamalı, 0 ile çıkmalı.
        ikinci = subprocess.run([exe], env=ortam, cwd=str(veri), timeout=90)
        ok(ikinci.returncode == 0, f"ikinci acilis cikis kodu {ikinci.returncode}")
        ok((pdc(port) or {}).get("pid") == bilgi["pid"], "ikinci acilis sunucuyu degistirdi")
        ok("Program zaten calisiyor" in (veri / "program.log").read_text(
            encoding="utf-8", errors="replace"), "ikinci acilis gunluge yazmadi")
        print("  ikinci acilis: calisan program taninip cikildi")

        if sys.platform == "darwin" and ".app/Contents/MacOS/" in exe:
            p2 = _devral(exe, ortam, veri, p1, port)
            surecler.append(p2)
            kapat(p2)
        else:
            kapat(p1)
        gunlugu_denetle(veri)
    except BaseException:
        gunlugu_bas(veri)
        raise
    finally:
        for s in surecler:
            if s.poll() is None:
                s.kill()
    shutil.rmtree(veri, ignore_errors=True)


def _devral(exe, ortam, veri, eski, port):
    """Mac: Uygulamalar'daki uygulama yenilendi (farklı derleme kimliği), yeni
    uygulamaya çift tıklandı: eski derleme kapanmalı, yenisi yerine geçmeli."""
    uygulama = Path(exe).parents[2]
    kok = Path(tempfile.mkdtemp(prefix="pdc_yeni_"))
    kopya = kok / uygulama.name
    subprocess.run(["ditto", str(uygulama), str(kopya)], check=True)
    bilgi_yolu = (kopya / "Contents" / "Frameworks" / "paket_bilgisi.json").resolve()
    ok(str(bilgi_yolu).startswith(str(kok.resolve())), f"kopyanin bilgi dosyasi disarida: {bilgi_yolu}")
    b = json.loads(bilgi_yolu.read_text(encoding="utf-8"))
    b["kimlik"] = b["kimlik"] + " (yeni)"
    bilgi_yolu.write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
    # Değişen dosya uygulamanın imzasını bozdu: kopyayı yeniden imzala.
    subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(kopya)], check=True)
    yeni_exe = kopya / "Contents" / "MacOS" / Path(exe).name
    t0 = time.time()
    yeni = subprocess.Popen([str(yeni_exe)], env=ortam, cwd=str(veri))
    try:
        eski.wait(60)
    except subprocess.TimeoutExpired:
        raise DenemeHatasi("yeni derleme eskisini 60 sn icinde kapatmadi")
    ok(eski.returncode == 0, f"eski derlemenin cikis kodu {eski.returncode}")
    bilgi = pdc_bekle(port, 120, surec=yeni, pid=yeni.pid)
    _sure_denetle("yenisinin yerine gecmesi", t0)
    ok(bilgi.get("paket", "").endswith("(yeni)"), f"yerine gecen derleme yanlis: {bilgi.get('paket')}")
    i = Istemci(port)
    d, h, _ = i.iste("/giris", {"kullanici_adi": KULLANICI, "sifre": SIFRE})
    ok(d == 303, "yeni derlemede giris yapilamadi")
    d, _, _ = i.iste("/")
    ok(d == 200, "yeni derlemede ana ekran acilmadi")
    print("  Mac: yenilenmis uygulama eski derlemeyi kapatip yerine gecti")
    return yeni


def kip_kurulu(yeniden=False):
    """Windows'ta kurulum dosyasının kurduğu program: Görev Zamanlayıcı
    (SYSTEM) açmış olmalı, veri `C:\\ProgramData\\PatientDataCenter`'da."""
    port, https_port = 8000, 8443
    veri = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "PatientDataCenter"
    pid_dosyasi = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "pdc_pid.txt"
    try:
        bilgi = pdc_bekle(port, 240)
        ok(ayni_yer(bilgi.get("veri"), veri), f"veri klasoru yanlis: {bilgi.get('veri')}")
        print(f"  calisiyor: {bilgi.get('paket')} (surec {bilgi['pid']}), veri {bilgi['veri']}")
        if yeniden:
            eski = pid_dosyasi.read_text().strip()
            ok(str(bilgi["pid"]) != eski, "guncellemeden sonra program yeniden baslamadi")
        pid_dosyasi.write_text(str(bilgi["pid"]))
        ekranlari_dene(port, https_port, ilk=not yeniden)
        gunlugu_denetle(veri)
    except BaseException:
        gunlugu_bas(veri)
        raise


def kip_oturum(exe, port=18000, https_port=18443):
    """Mac: Uygulamalar'dan çift tıklamayla açılan program LaunchAgent yazmalı."""
    exe = str(Path(exe).resolve())
    plist = Path.home() / "Library" / "LaunchAgents" / f"{MAC_ETIKETI}.plist"
    if plist.exists():
        plist.unlink()
    veri = Path(tempfile.mkdtemp(prefix="pdc_oturum_"))
    t0 = time.time()
    p = subprocess.Popen([exe], env=_ortam(veri, port, https_port), cwd=str(veri))
    try:
        pdc_bekle(port, 180, surec=p)
        _sure_denetle("Uygulamalar'dan acilis", t0)
        ok(plist.exists(), f"LaunchAgent yazilmadi: {plist}")
        with open(plist, "rb") as f:
            icerik = plistlib.load(f)
        ok(icerik.get("ProgramArguments") == [exe, "--servis"],
           f"LaunchAgent'in programi yanlis: {icerik.get('ProgramArguments')}")
        ok(icerik.get("RunAtLoad") is True and icerik.get("Label") == MAC_ETIKETI,
           "LaunchAgent eksik")
        print(f"  LaunchAgent yazildi: {plist}")
        kapat(p)
    except BaseException:
        gunlugu_bas(veri)
        raise
    finally:
        if p.poll() is None:
            p.kill()
        if plist.exists():
            plist.unlink()
    shutil.rmtree(veri, ignore_errors=True)


def main(arg):
    if len(arg) >= 2 and arg[0] == "program":
        kip_program(arg[1])
    elif arg and arg[0] == "kurulu":
        kip_kurulu(yeniden="--yeniden" in arg)
    elif len(arg) >= 2 and arg[0] == "oturum":
        kip_oturum(arg[1])
    else:
        print(__doc__)
        return 2
    print("TAMAM")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except DenemeHatasi as e:
        print(f"BASARISIZ: {e}")
        sys.exit(1)
