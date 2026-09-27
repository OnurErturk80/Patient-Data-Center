# -*- coding: utf-8 -*-
"""Programı başlatır — paketlenmiş uygulamanın giriş noktası.

Geliştirmede sunucu şöyle açılıyor:

    python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000

Paketlenmiş uygulamada bu **çalışmaz**: `python` yok, `-m uvicorn` yok, ve
`"app:uygulama"` metniyle modül aramak paketin içinde güvenilir değil. Bu
dosya uvicorn'u kütüphane gibi çağırıp uygulama nesnesini **doğrudan**
veriyor.

Geliştirmede de çalışıyor; ikisi tek yoldan gitsin diye:

    python3 baslat.py

Ayarlar ortam değişkeninden (kurulum dosyası bunları servise yazacak):

    LAB_ADRES   varsayılan 0.0.0.0   -- iç ağdan erişim için
    LAB_PORT    varsayılan 8000
    LAB_VERI    veri klasörü (bkz. db.py "iki kök")
    LAB_HTTPS_PORT  varsayılan 8443 -- güvenli bağlantı (v6.196)
    LAB_HTTPS   "0" ise HTTPS hiç açılmaz, yalnızca düz HTTP

HTTPS (v6.196): program iki kapıdan birden dinliyor -- düz HTTP (8000,
bugünkü adres, eski simgeler ve bilgisayarlar çalışmaya devam etsin; kök
sertifika telefona buradan indiriliyor) ve HTTPS (8443, Android'in
"uygulama gibi" açılışı için). Aynı süreç, aynı uygulama nesnesi: "aynı
kaydı iki kişi düzenliyor" uyarısı (bellekte, v6.55) iki kapıda da ortak.
Sertifika `sertifika.py`'de, her açılışta denetleniyor. Hazırlanamazsa
program yalnızca HTTP ile açılır -- HTTPS yüzünden program açılmaz olmasın.

Günlük **dosyaya** da yazılıyor: servis olarak çalışırken terminal yok,
bir şey ters giderse bakılacak tek yer o dosya olacak.

Aynı bilgisayarda ikinci açılış (v6.204): port doluysa ve onu tutan bu
programsa (`GET /__pdc`, yalnızca 127.0.0.1'e cevap veriyor) ikinci bir sunucu
açılmıyor --

    python3 baslat.py            "program zaten çalışıyor" yazar, çıkar
    kurulum dosyasıyla kurulan   tarayıcıyı açar, çıkar (Windows'ta programa,
                                 Mac'te uygulamaya çift tıklama)
    Mac'te yenilenmiş uygulama   eski derlemeyi kapatır, yerine geçer

Portu başka bir kurulum (başka veri klasörü) ya da başka bir program tutuyorsa
açılmıyor ve söylüyor. Kurulum dosyasıyla kurulan program çift tıklamayla
açılınca sunucu hazır olduğunda tarayıcıyı da açıyor; Mac'te oturum açılışında
başlaması için kendi LaunchAgent'ını yazıyor.

    --servis      tarayıcı açılmaz, pencere gösterilmez: Windows'ta Görev
                  Zamanlayıcı (SYSTEM, masaüstü yok), Mac'te oturum açılışı
    LAB_SESSIZ=1  aynısı, denemeler için (`paket/dene.py`)
"""

import asyncio
import contextlib
import json
import logging
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from logging.handlers import RotatingFileHandler
from pathlib import Path

import db

VARSAYILAN_PORT = 8000
VARSAYILAN_HTTPS_PORT = 8443

# Kurulum dosyasıyla kurulmuş (PyInstaller) program mı, git ile çalışan mı.
PAKETLI = bool(getattr(sys, "frozen", False))
# Mac'te oturum açılışında başlatan LaunchAgent'ın adı; `paket/pdc.spec`'in
# uygulama kimliğiyle aynı.
MAC_ETIKETI = "com.patientdatacenter.pdc"
# Tarayıcı açılabilir, pencere gösterilebilir mi (`main()` kuruyor).
_ARAYUZ = False
# `127.0.0.1`'e giden sorular vekil sunucuya gitmesin: Windows'ta sistemin
# vekil ayarı (hastane ağlarında olağan) urllib'e de uygulanıyor.
_DOGRUDAN = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _akislari_duzelt():
    """Pencereli pakette (Windows'ta konsolsuz program, Mac uygulaması) terminal
    yok, `sys.stdout`/`sys.stderr` None: uvicorn'un günlük biçimi `isatty()`
    çağırıp çöküyor. Boş bir akışa bağla; günlük `program.log`'a yazılıyor."""
    for ad in ("stdout", "stderr"):
        if getattr(sys, ad, None) is None:
            try:
                setattr(sys, ad, open(os.devnull, "w", encoding="utf-8"))
            except OSError:
                pass


def _gunluk_kur():
    """Konsola ve veri klasöründeki dosyaya yazar.

    Dosya 1 MB'ı geçince yenileniyor, üç eski kopya saklanıyor -- servis
    aylarca çalışacak, günlüğün diski doldurmaması gerekiyor.
    """
    kok = logging.getLogger()
    if kok.handlers:
        return
    kok.setLevel(logging.INFO)
    bicim = logging.Formatter("%(asctime)s  %(message)s", "%Y-%m-%d %H:%M:%S")

    konsol = logging.StreamHandler()
    konsol.setFormatter(bicim)
    kok.addHandler(konsol)

    try:
        dosya = RotatingFileHandler(db.VERI_KOK / "program.log",
                                    maxBytes=1_000_000, backupCount=3,
                                    encoding="utf-8")
        dosya.setFormatter(bicim)
        kok.addHandler(dosya)
    except OSError as e:                    # günlük yazılamıyorsa program yine açılsın
        kok.warning("Gunluk dosyasi acilamadi: %s", e)


def _yerel_ip():
    """Personelin tarayıcısına yazacağı adres. Dışarıya paket gitmiyor."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return ""
    finally:
        s.close()


def main(argv=None):
    global _ARAYUZ
    argv = sys.argv[1:] if argv is None else list(argv)
    servis = "--servis" in argv
    _ARAYUZ = PAKETLI and not servis and os.environ.get("LAB_SESSIZ") != "1"
    _akislari_duzelt()
    _gunluk_kur()
    g = logging.getLogger("baslat")

    adres = os.environ.get("LAB_ADRES") or "0.0.0.0"
    try:
        port = int(os.environ.get("LAB_PORT") or VARSAYILAN_PORT)
    except ValueError:
        port = VARSAYILAN_PORT
    try:
        https_port = int(os.environ.get("LAB_HTTPS_PORT") or VARSAYILAN_HTTPS_PORT)
    except ValueError:
        https_port = VARSAYILAN_HTTPS_PORT

    g.info("Program klasoru: %s", db.PROGRAM_KOK)
    g.info("Veri klasoru   : %s", db.VERI_KOK)

    # Aynı bilgisayarda program zaten çalışıyor mu (v6.204)?
    cikis = _ikinci_acilis(port, https_port, servis, g)
    if cikis is not None:
        return cikis

    # Veritabanı yoksa ilk kurulum (v6.204): program açılıyor, bütün istekler
    # `/kurulum` ekranına gidiyor ve yalnızca bu bilgisayardan (`app`'in
    # middleware'i). v6.50'den beri burada "önce kurulumu tamamlayın" deyip
    # duruyordu; kurulum dosyasıyla yüklenen programda terminal yok.
    kurulum_kipi = not db.DB_YOLU.exists()
    if kurulum_kipi:
        g.info("Veritabani yok: ilk kurulum ekrani -- bu bilgisayarda "
               "http://localhost:%d/kurulum", port)

    sertifikalar = None
    if os.environ.get("LAB_HTTPS", "1") != "0" and https_port != port:
        try:
            import sertifika
            sertifikalar = sertifika.hazirla()
        except Exception as e:           # HTTPS olmasa da program açılsın
            g.error("HTTPS hazirlanamadi, yalnizca HTTP ile aciliyor: %s", e)

    ip = _yerel_ip()
    if kurulum_kipi:
        pass                                  # yukarıda yazıldı
    elif db.ag_erisimi() == db.AG_YEREL:
        # v6.203: yeni kurulum ağa kapalı başlıyor; yönetici açıyor.
        g.info("Ag erisimi KAPALI: program yalnizca bu bilgisayardan acilir: "
               "http://localhost:%d", port)
        g.info("Telefonlarin baglanmasi icin: Yonetici -> Ag erisimi -> Ic aga acik")
    elif ip and adres == "0.0.0.0":
        g.info("Personel bu adresi kullanacak: http://%s:%d", ip, port)
        if sertifikalar:
            g.info("Guvenli adres (telefona uygulama olarak): https://%s:%d",
                   ip, https_port)
    g.info("Sunucu basliyor: http://%s:%d", adres, port)

    # Kurulum dosyasıyla kurulan program çift tıklamayla açıldıysa: sunucu
    # hazır olunca tarayıcı; Mac'te oturum açılışında başlama.
    if _ARAYUZ:
        _hazir_olunca_ac(port, g)
    if PAKETLI and not servis and sys.platform == "darwin":
        _mac_oturum_acilisi(g)

    # `app` burada import ediliyor: göçler (app'in açılışında çalışıyor)
    # günlüğe yazabilsin; ikinci açılış onu hiç yüklemeden çıkmış olsun.
    import uvicorn

    import app

    if not sertifikalar:
        try:
            uvicorn.run(app.uygulama, host=adres, port=port, log_level="info",
                        proxy_headers=False, **_gunluk_ayari())
        except OSError as e:
            g.error("Sunucu acilamadi (%s). Port %d baska bir program tarafindan "
                    "kullaniliyor olabilir.", e, port)
            return 3
        return 0

    app.HTTPS_PORTU = https_port
    app.DUZ_PORTU = port
    return asyncio.run(_iki_kapi(uvicorn, app, adres, port, https_port,
                                 sertifikalar, g))


def _gunluk_ayari():
    """Pakette uvicorn kendi günlük ayarını kurmasın: iletileri (açılamayan
    kapı, ekranda 500 veren hatanın ayrıntısı) kökteki kayıtçıya, yani
    `program.log`'a düşsün -- terminal yok, bakılacak tek yer o. Her isteğin
    satırı (her ekran beş saniyede bir soruyor, v6.54) günlüğü doldurmasın.
    Git ile çalışırken değişmedi: terminalde bugünkü gibi."""
    return {"log_config": None, "access_log": False} if PAKETLI else {}


def _port_dolu(port):
    """Bu bilgisayarda bu portu dinleyen var mı."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def _calisan_program(port):
    """Portu tutan program (v6.204). None: port boş. {}: dolu ama bu program
    değil ya da `/__pdc`'yi bilmeyen eski bir sürüm (v6.203 ve öncesi).
    Öteki: `app.program_kimligi()` -- sürüm, derleme, süreç, veri klasörü."""
    if not _port_dolu(port):
        return None
    try:
        with _DOGRUDAN.open(f"http://127.0.0.1:{port}/__pdc", timeout=5) as y:
            bilgi = json.loads(y.read().decode("utf-8"))
        if isinstance(bilgi, dict) and bilgi.get("program") == "patient-data-center":
            return bilgi
    except Exception:
        pass
    return {}


def _ayni_klasor(a, b):
    try:
        return (os.path.normcase(os.path.realpath(str(a)))
                == os.path.normcase(os.path.realpath(str(b))))
    except (TypeError, ValueError, OSError):
        return False


def _ikinci_acilis(port, https_port, servis, g):
    """Port doluysa ne yapılacağı: çıkış kodu, ya da None (bu açılış sunucu
    olacak -- port boş ya da eski derleme kapatıldı)."""
    bilgi = _calisan_program(port)
    if bilgi is None:
        return None
    ret = 0 if servis else 3
    if not bilgi:
        _haber_ver(f"Port {port} başka bir program tarafından kullanılıyor, "
                   "Patient Data Center açılamadı. Programın eski bir kurulumu "
                   "(terminalde çalışan python3 baslat.py) açıksa onu kapatıp "
                   "yeniden deneyin.", g)
        return ret
    if not _ayni_klasor(bilgi.get("veri"), db.VERI_KOK):
        _haber_ver("Bu bilgisayarda programın başka bir kurulumu çalışıyor "
                   f"(veri klasörü: {bilgi.get('veri')}). İkisi aynı anda "
                   "çalışamaz: önce onu kapatın.", g)
        return ret
    # Mac'te uygulama yenilenince (yeni DMG'den Uygulamalar'a sürüklendi) eski
    # derleme çalışmaya devam ediyor, dosyaları altından değişmiş halde. Yeni
    # uygulamaya çift tıklamak onu kapatıp yerine geçiyor. Windows'ta bu işi
    # kurulum dosyası yapıyor (eskisini durdurup yenisini başlatıyor).
    benim = (db.paket_bilgisi() or {}).get("kimlik")
    if PAKETLI and not servis and sys.platform == "darwin" \
            and benim and bilgi.get("paket") != benim:
        g.info("Eski derleme calisiyor (%s, surec %s), yenisi yerine geciyor: %s",
               bilgi.get("paket") or bilgi.get("surum"), bilgi.get("pid"), benim)
        if _eskisini_kapat(bilgi.get("pid"), (port, https_port), g):
            return None
        _haber_ver("Programın eski sürümü kapatılamadı. Bilgisayarı yeniden "
                   "başlatıp uygulamayı yeniden açın.", g)
        return ret
    g.info("Program zaten calisiyor (%s): http://localhost:%d",
           bilgi.get("paket") or bilgi.get("surum"), port)
    if _ARAYUZ:
        _tarayiciyi_ac(port, g)
    return 0


def _surec_var(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True


def _eskisini_kapat(pid, portlar, g):
    """Eski derlemeye "kapan" de (SIGTERM: `_iki_kapi`'nın düzgün kapanışı,
    ikincisi hemen), kapılar boşalana kadar bekle. Süreç kapılarını kapatıp
    kapanışını bitiriyorsa (ya da onu toplayan olmadığı için "zombi" kaldıysa)
    kapılar boşaldıktan en çok 3 sn sonra devam."""
    if not isinstance(pid, int) or pid <= 1 or pid == os.getpid():
        return False
    for _ in range(2):
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except OSError as e:
            g.warning("Eski surec kapatilamadi: %s", e)
            return False
        bosaldi = None
        for _ in range(150):                          # 15 sn
            if any(_port_dolu(p) for p in portlar):
                bosaldi = None
            elif not _surec_var(pid):
                return True
            elif bosaldi is None:
                bosaldi = time.monotonic()
            elif time.monotonic() - bosaldi > 3:
                return True
            time.sleep(0.1)
    return not any(_port_dolu(p) for p in portlar)


def _haber_ver(metin, g):
    """Günlüğe yaz; terminali olmayan programda (çift tıklamayla açılan paket)
    kullanıcıya pencereyle de söyle -- Mac'te `osascript`, Windows'ta ileti
    kutusu. `--servis` iken pencere yok: Görev Zamanlayıcı'nın SYSTEM
    oturumunda görünmeyen bir pencere programı sonsuza dek bekletirdi."""
    g.warning("%s", metin)
    if not _ARAYUZ:
        return
    baslik = "Patient Data Center"
    try:
        if sys.platform == "darwin":
            betik = "display alert %s message %s" % (
                json.dumps(baslik, ensure_ascii=False),
                json.dumps(metin, ensure_ascii=False))
            subprocess.run(["osascript", "-e", betik], timeout=600, check=False)
        elif os.name == "nt":
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, metin, baslik, 0x30)
    except Exception as e:                            # pencere yoksa günlük yeter
        g.warning("Pencere gosterilemedi: %s", e)


def _tarayiciyi_ac(port, g):
    adres = f"http://localhost:{port}/"
    try:
        webbrowser.open(adres)
    except Exception as e:
        g.warning("Tarayici acilamadi (%s): %s", adres, e)


def _hazir_olunca_ac(port, g):
    """Sunucu dinlemeye başlayınca tarayıcıyı aç. uvicorn açılış işlerini
    (göçler) portu açmadan önce yapıyor: port açıksa ekran hazır. En çok beş
    dakika bekler (büyük bir veritabanında göçler)."""
    def bekle():
        for _ in range(3000):
            if _port_dolu(port):
                _tarayiciyi_ac(port, g)
                return
            time.sleep(0.1)
    threading.Thread(target=bekle, name="tarayici", daemon=True).start()


def _mac_oturum_acilisi(g):
    """Mac: oturum açılınca program kendiliğinden başlasın (v6.204).

    `~/Library/LaunchAgents/<etiket>.plist`: uygulamanın kendi dosyası
    `--servis` ile, oturum açılışında. Çökerse launchd yeniden başlatıyor;
    temiz çıkışta (ikinci açılış, başka kurulum portu tutuyor) değil, döngüye
    girmesin. Yalnızca uygulama Uygulamalar klasöründeyse: DMG'den ya da
    İndirilenler'den açılmışsa macOS onu geçici bir yerden çalıştırıyor, yol
    sonra kaybolur. Kapatmak: Sistem Ayarları -> Genel -> Oturum Açma Öğeleri."""
    import plistlib
    exe = Path(sys.executable).resolve()
    if not str(exe).startswith(("/Applications/",
                                str(Path.home() / "Applications") + "/")):
        g.info("Uygulama Uygulamalar klasorunde degil (%s): oturum acilisinda "
               "baslatma ayarlanmadi.", exe)
        return
    icerik = plistlib.dumps({
        "Label": MAC_ETIKETI,
        "ProgramArguments": [str(exe), "--servis"],
        "RunAtLoad": True,
        "KeepAlive": {"SuccessfulExit": False},
        "ThrottleInterval": 30,
        "ProcessType": "Standard",
        # Oturum Açma Öğeleri'nde uygulamanın adı ve simgesiyle görünsün.
        "AssociatedBundleIdentifiers": [MAC_ETIKETI],
    })
    hedef = Path.home() / "Library" / "LaunchAgents" / f"{MAC_ETIKETI}.plist"
    try:
        if hedef.exists() and hedef.read_bytes() == icerik:
            return
        hedef.parent.mkdir(parents=True, exist_ok=True)
        gecici = hedef.with_name(hedef.name + ".yeni")
        gecici.write_bytes(icerik)
        os.replace(gecici, hedef)
        g.info("Oturum acilisinda baslatma ayarlandi: %s", hedef)
    except OSError as e:
        g.warning("Oturum acilisinda baslatma ayarlanamadi: %s", e)


def _sessiz_sunucu(uvicorn):
    """uvicorn.Server'ın sinyal yakalamayan hali. İki sunucu aynı süreçte
    kendi Ctrl+C işleyicisini kurarsa sonraki öncekini eziyor, biri hiç
    durmuyordu. Sinyali `_iki_kapi` tutuyor, ikisine birden "dur" diyor."""
    class S(uvicorn.Server):
        def install_signal_handlers(self):          # eski uvicorn
            pass

        @contextlib.contextmanager
        def capture_signals(self):                  # yeni uvicorn
            yield
    return S


async def _iki_kapi(uvicorn, app, adres, port, https_port, sertifikalar, g):
    S = _sessiz_sunucu(uvicorn)
    # `proxy_headers=False` (v6.203): istemcinin adresi bağlantının kendisinden,
    # `X-Forwarded-For` başlığından değil -- ağ erişimi kapalıyken "bu
    # bilgisayardan mı" sorusu (`app._bu_bilgisayardan()`) buna dayanıyor.
    duz = S(uvicorn.Config(app.uygulama, host=adres, port=port, log_level="info",
                           proxy_headers=False, **_gunluk_ayari()))
    # Açılış işleri (göçler, harita yazıcısı) yalnızca bir kez: ikinci kapıda
    # `lifespan="off"`.
    guvenli = S(uvicorn.Config(app.uygulama, host=adres, port=https_port,
                               log_level="info", lifespan="off", proxy_headers=False,
                               ssl_certfile=str(sertifikalar[0]),
                               ssl_keyfile=str(sertifikalar[1]), **_gunluk_ayari()))

    def dur(*_):
        for s in (duz, guvenli):
            if s.should_exit:                         # ikinci Ctrl+C: hemen
                s.force_exit = True
            s.should_exit = True
    for sinyal in (signal.SIGINT, getattr(signal, "SIGTERM", None)):
        if sinyal is not None:
            try:
                signal.signal(sinyal, dur)
            except (ValueError, OSError):
                pass

    async def izle(s, ad, p, oteki):
        if s is guvenli:
            # Güvenli kapı, düz kapının açılış işleri (göçler) bitince açılsın:
            # göç bitmeden gelen bir istek eski şemaya çarpmasın.
            while not duz.started and not duz.should_exit:
                await asyncio.sleep(0.1)
            if duz.should_exit:
                return
        try:
            await s.serve()
        except (OSError, SystemExit) as e:
            g.error("%s kapisi acilamadi (port %d): %s", ad, p, e)
        if ad == "HTTP":                              # ana kapı kapandıysa hepsi
            oteki.should_exit = True

    await asyncio.gather(izle(duz, "HTTP", port, guvenli),
                         izle(guvenli, "HTTPS", https_port, duz))
    return 0


if __name__ == "__main__":
    sys.exit(main())
