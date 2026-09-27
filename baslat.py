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
"""

import asyncio
import contextlib
import logging
import os
import signal
import socket
import sys
from logging.handlers import RotatingFileHandler

import db

VARSAYILAN_PORT = 8000
VARSAYILAN_HTTPS_PORT = 8443


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


def main():
    _gunluk_kur()
    g = logging.getLogger("baslat")

    adres = os.environ.get("LAB_ADRES") or "0.0.0.0"
    try:
        port = int(os.environ.get("LAB_PORT") or VARSAYILAN_PORT)
    except ValueError:
        port = VARSAYILAN_PORT

    g.info("Program klasoru: %s", db.PROGRAM_KOK)
    g.info("Veri klasoru   : %s", db.VERI_KOK)

    if not db.DB_YOLU.exists():
        # İlk kurulum henüz yapılmamış. Program açılsa da her ekran hata
        # verirdi; sebebini söyleyip durmak daha dürüst.
        g.error("Veritabani yok: %s", db.DB_YOLU)
        g.error("Once kurulumu tamamlayin (sifirdan_kur.py) ya da "
                "mevcut lab.db dosyasini bu klasore koyun.")
        return 2

    try:
        https_port = int(os.environ.get("LAB_HTTPS_PORT") or VARSAYILAN_HTTPS_PORT)
    except ValueError:
        https_port = VARSAYILAN_HTTPS_PORT
    sertifikalar = None
    if os.environ.get("LAB_HTTPS", "1") != "0" and https_port != port:
        try:
            import sertifika
            sertifikalar = sertifika.hazirla()
        except Exception as e:           # HTTPS olmasa da program açılsın
            g.error("HTTPS hazirlanamadi, yalnizca HTTP ile aciliyor: %s", e)

    ip = _yerel_ip()
    if db.ag_erisimi() == db.AG_YEREL:
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

    # `app` burada import ediliyor: veritabanı yoksa yukarıda çıkılmış olsun,
    # ve göçler (app'in açılışında çalışıyor) günlüğe yazabilsin.
    import uvicorn

    import app

    if not sertifikalar:
        try:
            uvicorn.run(app.uygulama, host=adres, port=port, log_level="info",
                        proxy_headers=False)
        except OSError as e:
            g.error("Sunucu acilamadi (%s). Port %d baska bir program tarafindan "
                    "kullaniliyor olabilir.", e, port)
            return 3
        return 0

    app.HTTPS_PORTU = https_port
    app.DUZ_PORTU = port
    return asyncio.run(_iki_kapi(uvicorn, app, adres, port, https_port,
                                 sertifikalar, g))


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
                           proxy_headers=False))
    # Açılış işleri (göçler, harita yazıcısı) yalnızca bir kez: ikinci kapıda
    # `lifespan="off"`.
    guvenli = S(uvicorn.Config(app.uygulama, host=adres, port=https_port,
                               log_level="info", lifespan="off", proxy_headers=False,
                               ssl_certfile=str(sertifikalar[0]),
                               ssl_keyfile=str(sertifikalar[1])))

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
