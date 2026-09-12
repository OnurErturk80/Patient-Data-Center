# -*- coding: utf-8 -*-
"""Bekleyen göçleri bulur ve çalıştırır — süreç içinde, alt süreç açmadan.

**Neden süreç içinde:** `goc_hepsi.py` eskiden her göçü
`subprocess.run([sys.executable, "goc_029.py"])` ile çalıştırıyordu.
Paketlenmiş uygulamada (PyInstaller) `sys.executable` **programın kendisi**
olur; o satır göçü çalıştırmaz, programı yeniden başlatır. Üstelik `.py`
dosyaları diskte olmayabilir.

Göç betikleri en üst düzeyde çalışan betikler: `import goc_029` demek onu
çalıştırmak demek. Buradaki çalıştırıcı bunu yapıyor, çıktısını yakalıyor
ve `sys.exit()`'i hata sayıp saymayacağına çıkış koduna bakarak karar
veriyor.

**Hangileri çalıştı:** `goc_kaydi` tablosunda tutuluyor. Tablo bu modül
tarafından açılıyor (göçle değil — kendi kaydını tutan tabloyu bir göçle
kurmak tavuk-yumurta olurdu). Eski kurulumlarda kayıt yok ama göçler
uygulanmış; ilk çalıştırmada hepsi yeniden koşuyor (idempotentler) ve
kaydediliyor, sonrakilerde atlanıyor.

**Eşzamanlılık:** iki süreç aynı anda başlarsa aynı ALTER iki kez
çalışabilir. `BEGIN IMMEDIATE` ile bir işaret konuyor; işareti kapan
çalıştırıyor, öteki atlıyor. Beş dakikadan eski işaret çökmüş bir süreçten
kalmış sayılıp yok sayılıyor.
"""

import importlib
import io
import re
import contextlib
import pkgutil
import sqlite3
import sys
from datetime import datetime, timedelta

import db

# Soru soran göçler kendiliğinden çalıştırılamaz. Değer: o göçün **etkisini**
# arayan bir sorgu -- sonuç dönerse göç zaten uygulanmış demektir ve panelde
# "elle çalıştır" diye durmasına gerek yok. `goc_002` şifre soruyor; etkisi
# `oturum` tablosu.
ELLE = {
    "goc_002": "SELECT 1 FROM sqlite_master WHERE type='table' AND name='oturum'",
}

# Çökmüş bir süreçten kalan işaret bu kadar sonra yok sayılıyor.
ISARET_OMRU = timedelta(minutes=5)

_KALIP = re.compile(r"^goc_(\d+)$")


def _sirala(ad):
    return int(_KALIP.match(ad).group(1))


def gocler():
    """Bütün göç modüllerinin adları, numara sırasıyla.

    Önce dosyalara bakılıyor (geliştirme), bulunamazsa modül listesine
    (paketlenmiş çalıştırma -- orada `.py` diskte olmayabilir).
    """
    adlar = {p.stem for p in db.PROGRAM_KOK.glob("goc_*.py")
             if _KALIP.match(p.stem)}
    if not adlar:
        adlar = {m.name for m in pkgutil.iter_modules() if _KALIP.match(m.name)}
    return sorted(adlar, key=_sirala)


def _baglan():
    return sqlite3.connect(db.DB_YOLU, timeout=db.BEKLEME_SN)


def _tablo(b):
    b.execute("CREATE TABLE IF NOT EXISTS goc_kaydi ("
              "ad TEXT PRIMARY KEY, zaman TEXT)")


def uygulananlar():
    """Kaydı tutulmuş göçlerin adları."""
    if not db.DB_YOLU.exists():
        return set()
    b = _baglan()
    try:
        _tablo(b)
        b.commit()
        return {r[0] for r in b.execute(
            "SELECT ad FROM goc_kaydi WHERE ad NOT LIKE '.%'")}
    finally:
        b.close()


def bekleyenler():
    """Henüz kaydı olmayan ve kendiliğinden çalıştırılabilen göçler."""
    olanlar = uygulananlar()
    return [a for a in gocler() if a not in olanlar and a not in ELLE]


def _etkisi_var(b, sorgu):
    """Elle çalıştırılan bir göç zaten uygulanmış mı?"""
    try:
        return b.execute(sorgu).fetchone() is not None
    except sqlite3.Error:
        return False


def _isareti_kap(b):
    """Başka bir süreç göç çalıştırmıyorsa işareti kapar. True/False."""
    simdi = datetime.now()
    b.isolation_level = None
    b.execute("BEGIN IMMEDIATE")
    try:
        r = b.execute("SELECT zaman FROM goc_kaydi WHERE ad = '.calisiyor'"
                      ).fetchone()
        if r:
            try:
                if simdi - datetime.fromisoformat(r[0]) < ISARET_OMRU:
                    b.execute("ROLLBACK")
                    return False
            except ValueError:
                pass                       # bozuk işaret: yok say
        b.execute("INSERT OR REPLACE INTO goc_kaydi (ad, zaman) "
                  "VALUES ('.calisiyor', ?)", (simdi.isoformat(" ", "seconds"),))
        b.execute("COMMIT")
        return True
    except sqlite3.Error:
        b.execute("ROLLBACK")
        return False


def _isareti_birak(b):
    b.execute("DELETE FROM goc_kaydi WHERE ad = '.calisiyor'")


def _tek_goc(ad):
    """Bir göçü çalıştırır. (başarılı mı, çıktı) döndürür.

    `import` etmek göçü çalıştırmak demek. Göçler `print` ediyor ve bazıları
    `sys.exit()` çağırıyor -- çıkış kodu 0 ise bu "yapacak bir şey yok"
    demektir, hata değil.
    """
    tampon = io.StringIO()
    try:
        with contextlib.redirect_stdout(tampon):
            if ad in sys.modules:
                importlib.reload(sys.modules[ad])
            else:
                importlib.import_module(ad)
    except SystemExit as e:
        kod = e.code
        if kod not in (None, 0):
            return False, (tampon.getvalue() + "\n" + str(kod)).strip()
    except Exception as e:                 # göç patlarsa program yine açılsın
        return False, (tampon.getvalue() + "\n" + repr(e)).strip()
    return True, tampon.getvalue().strip()


def calistir():
    """Bekleyen göçleri sırayla çalıştırır.

    Döndürdüğü sözlük `/yonetim` panelinde ve terminalde aynı şekilde
    kullanılıyor: {"calisti": [...], "hatali": [(ad, mesaj)], "bekleyen": [...],
    "elle": [...], "atlandi": sebep}
    """
    sonuc = {"calisti": [], "hatali": [], "bekleyen": [], "elle": [],
             "atlandi": ""}
    if not db.DB_YOLU.exists():
        sonuc["atlandi"] = "veritabani-yok"
        return sonuc

    b = _baglan()
    try:
        _tablo(b)
        b.commit()
        if not _isareti_kap(b):
            sonuc["atlandi"] = "baska-surec"
            return sonuc

        try:
            olanlar = {r[0] for r in b.execute("SELECT ad FROM goc_kaydi")}
            for ad in gocler():
                if ad in ELLE:
                    if ad in olanlar:
                        continue
                    if _etkisi_var(b, ELLE[ad]):
                        b.execute("INSERT OR REPLACE INTO goc_kaydi "
                                  "(ad, zaman) VALUES (?, ?)",
                                  (ad, "onceden"))
                    else:
                        sonuc["elle"].append(ad)
                    continue
                if ad in olanlar:
                    continue
                tamam, cikti = _tek_goc(ad)
                if tamam:
                    b.execute("INSERT OR REPLACE INTO goc_kaydi (ad, zaman) "
                              "VALUES (?, ?)",
                              (ad, datetime.now().isoformat(" ", "seconds")))
                    sonuc["calisti"].append(ad)
                else:
                    sonuc["hatali"].append((ad, cikti))
                    break                  # sıradakiler buna dayanıyor olabilir
        finally:
            _isareti_birak(b)
    finally:
        b.close()

    sonuc["bekleyen"] = bekleyenler()
    return sonuc
