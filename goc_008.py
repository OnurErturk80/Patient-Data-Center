"""Göç 008 — yedekleme ayarları.

Kullanım:  python goc_008.py
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)

# ayarlar tablosunda UNIQUE(lab_id, anahtar) olmali (ON CONFLICT icin)
AYARLAR = [
    ("yedek_klasor", r"D:\lab_yedek",
     "Yedeklerin yazilacagi klasor. Farkli bir diskte olmali."),
    ("yedek_uyari_gun", "3",
     "Son yedek bu kadar gunden eskiyse ekranda uyari gosterilir."),
]
for anahtar, deger, aciklama in AYARLAR:
    var = b.execute("SELECT 1 FROM ayarlar WHERE lab_id=1 AND anahtar=?",
                    (anahtar,)).fetchone()
    if not var:
        b.execute("INSERT INTO ayarlar (lab_id, anahtar, deger, aciklama) "
                  "VALUES (1,?,?,?)", (anahtar, deger, aciklama))
b.commit()

print("Yedekleme ayarlari:")
for r in b.execute("SELECT anahtar, deger FROM ayarlar "
                   "WHERE anahtar IN ('yedek_klasor','yedek_uyari_gun','son_yedek')"):
    print(f"  {r[0]:18s} = {r[1]}")
b.close()

print("\nHedef klasoru degistirmek icin:")
print(r"""  python -c "import db; db.yaz(\"UPDATE ayarlar SET deger='E:\\yedek' """
      r"""WHERE anahtar='yedek_klasor'\")" """)
print("\nGoc 008 tamam.")
