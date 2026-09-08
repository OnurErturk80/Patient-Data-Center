"""Göç 010 — blastokist genişleme listesine 'kavitasyon' ekler.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_010.py      (Mac'te: python3 goc_010.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

var = b.execute(
    "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi='bl_genisleme' "
    "AND kod='kavitasyon'").fetchone()

if var:
    print("kavitasyon zaten listede.")
else:
    # morula'dan hemen sonraya yerlestir
    m = b.execute(
        "SELECT sira FROM liste_degeri WHERE lab_id=1 AND liste_adi='bl_genisleme' "
        "AND kod='morula'").fetchone()
    sira = (m["sira"] + 1) if m else 999
    b.execute(
        "UPDATE liste_degeri SET sira = sira + 1 "
        "WHERE lab_id=1 AND liste_adi='bl_genisleme' AND sira >= ?", (sira,))
    b.execute(
        "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'bl_genisleme','kavitasyon','Kavitasyon',?)", (sira,))
    b.commit()
    print("kavitasyon eklendi.")

# Blastokist disi durumlari gelisim sirasina koy
SIRA = ["1", "2", "3", "4", "5", "6",
        "erken_morula", "morula", "kavitasyon", "arrest"]
for i, kod in enumerate(SIRA):
    b.execute("UPDATE liste_degeri SET sira=? WHERE lab_id=1 "
              "AND liste_adi='bl_genisleme' AND kod=?", (i, kod))
b.commit()

print("\nGenisleme listesi:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='bl_genisleme' ORDER BY sira"):
    print(f"  {r['kod']:14s} {r['etiket']}")

b.close()
print("\nGoc 010 tamam.")
