"""Göç 011 — blastokist dışı aşamalar için derece alanı.

Morula, erken morula ve kavitasyon için 1-2-3 derecelendirmesi.
Arrest derecelendirilmez.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_011.py      (Mac'te: python3 goc_011.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(olay)")]
if "bl_derece" not in kolonlar:
    b.execute("ALTER TABLE olay ADD COLUMN bl_derece TEXT")
    print("olay.bl_derece eklendi.")
else:
    print("olay.bl_derece zaten var.")

DERECELER = [
    ("1", "Derece 1"),
    ("2", "Derece 2"),
    ("3", "Derece 3"),
]
for i, (kod, etiket) in enumerate(DERECELER):
    b.execute("INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'bl_derece',?,?,?)", (kod, etiket, i))
b.commit()

print("\nDerece listesi:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='bl_derece' ORDER BY sira"):
    print(f"  {r['kod']}  {r['etiket']}")

b.close()
print("\nGoc 011 tamam.")
