"""Göç 015 — oosit bazında over tarafı (sağ / sol).

specimen tablosuna taraf alani ekler. Cycle duzeyindeki
opu_sag_oosit / opu_sol_oosit sayilari yerinde kalir.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_015.py
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(specimen)")]
if "taraf" not in kolonlar:
    b.execute("ALTER TABLE specimen ADD COLUMN taraf TEXT")
    print("specimen.taraf eklendi.")
else:
    print("specimen.taraf zaten var.")

for i, (kod, etiket) in enumerate([("sag", "Sağ"), ("sol", "Sol")]):
    b.execute("INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'taraf',?,?,?)", (kod, etiket, i))
b.commit()

n = b.execute("SELECT COUNT(*) FROM specimen").fetchone()[0]
d = b.execute("SELECT COUNT(*) FROM specimen WHERE taraf IS NOT NULL").fetchone()[0]
print(f"\n{n} oositten {d} tanesinde taraf bilgisi var.")
b.close()
print("Goc 015 tamam.")
