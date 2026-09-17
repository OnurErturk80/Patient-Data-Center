"""Göç 036 — hastaya ve eşine telefon numarası alanı.

Kullanıcının isteği: hasta kaydederken hastanın ve eşinin telefon numarası
da tutulsun.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_036.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(hasta)")]

if "telefon" not in kolonlar:
    b.execute("ALTER TABLE hasta ADD COLUMN telefon TEXT")
    print("hasta.telefon eklendi.")
else:
    print("hasta.telefon zaten var.")

if "es_telefon" not in kolonlar:
    b.execute("ALTER TABLE hasta ADD COLUMN es_telefon TEXT")
    print("hasta.es_telefon eklendi.")
else:
    print("hasta.es_telefon zaten var.")

b.commit()
b.close()
print("\nGoc 036 tamam.")
