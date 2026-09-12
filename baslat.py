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

Günlük **dosyaya** da yazılıyor: servis olarak çalışırken terminal yok,
bir şey ters giderse bakılacak tek yer o dosya olacak.
"""

import logging
import os
import socket
import sys
from logging.handlers import RotatingFileHandler

import db

VARSAYILAN_PORT = 8000


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

    ip = _yerel_ip()
    if ip and adres == "0.0.0.0":
        g.info("Personel bu adresi kullanacak: http://%s:%d", ip, port)
    g.info("Sunucu basliyor: http://%s:%d", adres, port)

    # `app` burada import ediliyor: veritabanı yoksa yukarıda çıkılmış olsun,
    # ve göçler (app'in açılışında çalışıyor) günlüğe yazabilsin.
    import uvicorn

    import app

    try:
        uvicorn.run(app.uygulama, host=adres, port=port, log_level="info")
    except OSError as e:
        g.error("Sunucu acilamadi (%s). Port %d baska bir program tarafindan "
                "kullaniliyor olabilir.", e, port)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
