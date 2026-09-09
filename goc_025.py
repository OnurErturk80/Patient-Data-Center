"""Göç 025 — OPU aşaması: işlemi yapan hekim.

OPU artık kendi ekranı olan bir aşama. İki kişi kaydediliyor:

  - **Hekim** — oositleri aspire eden kişi. Laboratuvar personeli olmadığı
    için `islem_yapan` tablosuna değil, cycle'ın kendi verisine yazılır;
    `opu_zamani` / `opu_sag_oosit` ile aynı satırda durur.
  - **Embriyolog** — folikül sıvısını tarayıp oositleri bulan kişi. Diğer tüm
    aşamalarla aynı yoldan, `islem_yapan` tablosuna `asama='opu'` olarak
    yazılır (v6.3). Bu yüzden burada ayrı bir kolon açılmıyor.

Bu göç yalnızca `cycle.opu_hekim` kolonunu ekler. `islem_yapan` tarafı için
şema değişikliği gerekmiyor — tablo zaten aşama adına göre çalışıyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_025.py      (Mac'te: python3 goc_025.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

mevcut = {r["name"] for r in b.execute("PRAGMA table_info(cycle)")}
if "opu_hekim" in mevcut:
    print("cycle.opu_hekim zaten var.")
else:
    b.execute("ALTER TABLE cycle ADD COLUMN opu_hekim TEXT")
    b.commit()
    print("  + cycle.opu_hekim")

# ----------------------------------------------------------------------- ozet
n = b.execute("SELECT COUNT(*) FROM cycle WHERE opu_hekim IS NOT NULL").fetchone()[0]
toplam = b.execute("SELECT COUNT(*) FROM cycle").fetchone()[0]
print(f"\nOPU hekimi girilmis cycle: {n} / {toplam}")

iy = b.execute("SELECT COUNT(*) FROM islem_yapan WHERE asama='opu'").fetchone()[0]
print(f"OPU embriyologu girilmis cycle: {iy} / {toplam}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 025 tamam.")
