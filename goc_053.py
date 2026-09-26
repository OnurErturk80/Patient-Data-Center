"""Göç 053 — Yedek goblet (v6.192).

Kullanıcı (2026-09-26): "Tank 5'in 2-6 üst katları yer biterse diye
hazırlandı, ihtiyaç olursa oralara da hasta konulacak." Excel'de o katların
tabloları var ama gobletleri numaralanmamış; `cryo_esle.py yerlesim` onları
açıyor (`cryo_excel._hazir_kat_gobletleri()`). Yer bitmeden kullanılmasınlar
diye YEDEK işaretleniyorlar:

- `konum.yedek`: 1 = yedek goblet (hazırlanmış, yer biterse kullanılacak),
  boş = olağan. Öneri (`yerlesim.oneriler()`) yedeği ancak olağan yerler
  hastanın bugünkü straw'larını alamadığında sunuyor; haritada ve Excel'de
  "yedek" yazıyor. Yedek bir goblete straw konabilir -- yazılan yer düzende,
  dondurma ekranı uyarmaz.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_053.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
if "yedek" not in [r[1] for r in b.execute("PRAGMA table_info(konum)")]:
    b.execute("ALTER TABLE konum ADD COLUMN yedek INTEGER")
    print("konum.yedek eklendi.")
else:
    print("konum.yedek zaten var.")
b.commit()
b.close()
print("\nGoc 053 tamam.")
