"""Göç 006 — otomatik lab kayıt numarası ayarları.

Kullanım:  python goc_006.py
"""

import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

AYARLAR = [
    ("lab_no_onek", str(datetime.now().year),
     "Lab kayit no oneki. Bos birakilirsa yalnizca sira numarasi kullanilir."),
    ("lab_no_basamak", "4", "Sira numarasi kac basamakli olsun (0001 gibi)."),
    ("lab_no_bosluk_doldur", "1",
     "1 = silinen kaydin numarasi yeniden kullanilir. 0 = hep en yuksek + 1."),
    ("lab_no_yillik_sifirla", "1",
     "1 = her yil onek degisir ve sira 1'den baslar."),
]

for anahtar, deger, aciklama in AYARLAR:
    var = b.execute("SELECT 1 FROM ayarlar WHERE lab_id=1 AND anahtar=?",
                    (anahtar,)).fetchone()
    if not var:
        b.execute("INSERT INTO ayarlar (lab_id, anahtar, deger, aciklama) "
                  "VALUES (1,?,?,?)", (anahtar, deger, aciklama))

# cycle.durum zaten var (aktif/iptal icin kullanilacak)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(cycle)")]
print("cycle.durum:", "var" if "durum" in kolonlar else "YOK")

b.commit()

print("\nAyarlar:")
for r in b.execute("SELECT anahtar, deger FROM ayarlar WHERE anahtar LIKE 'lab_no_%'"):
    print(f"  {r['anahtar']:24s} = {r['deger']}")

# Mevcut numaralarin bicimi
onek = b.execute("SELECT deger FROM ayarlar WHERE anahtar='lab_no_onek'").fetchone()[0]
kalip = re.compile(rf"^{re.escape(onek)}-(\d+)$")
mevcut = [r["cycle_no"] for r in b.execute("SELECT cycle_no FROM cycle")]
uyan = [n for n in mevcut if kalip.match(n)]

print(f"\nMevcut {len(mevcut)} cycle numarasindan {len(uyan)} tanesi "
      f"'{onek}-NNNN' bicimine uyuyor.")
if len(uyan) < len(mevcut):
    print("Uymayanlar oldugu gibi kalir; otomatik numaralandirma yalnizca")
    print("yeni kayitlarda calisir ve mevcut numaralarla cakismaz.")

b.close()
print("\nGoc 006 tamam.")
