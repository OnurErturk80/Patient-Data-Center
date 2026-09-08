"""Göç 013 — çözme kaydına canlılık oranı ve ikinci kontrol saati.

thaw olayina iki alan ekler:
  thaw_canlilik        canlilik orani (%) — kac blastomer/hucre canli kaldi
  thaw_kontrol_zamani  cozme sonrasi ikinci kontrol saati (re-expansion degerlendirmesi)

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_013.py      (Mac'te: python3 goc_013.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(olay)")]

for ad, tip in (("thaw_canlilik", "REAL"), ("thaw_kontrol_zamani", "TEXT")):
    if ad not in kolonlar:
        b.execute(f"ALTER TABLE olay ADD COLUMN {ad} {tip}")
        print(f"olay.{ad} eklendi.")
    else:
        print(f"olay.{ad} zaten var.")

b.commit()
n = b.execute("SELECT COUNT(*) FROM olay WHERE tip='thaw' AND iptal_mi=0").fetchone()[0]
print(f"\nMevcut thaw kaydi: {n}")
b.close()
print("Goc 013 tamam.")
