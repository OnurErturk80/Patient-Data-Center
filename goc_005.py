"""Göç 005 — hastanın kaçıncı tedavi cycle'ı olduğu alanı.

cycle_no laboratuvar kayıt numarasıdır (benzersiz).
hasta_cycle_no hastanın kaçıncı denemesi olduğudur (hasta içinde sıralı).

Mevcut kayıtlar OPU/hCG zamanına göre otomatik numaralandırılır.
Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_005.py
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(cycle)")]
if "hasta_cycle_no" not in kolonlar:
    b.execute("ALTER TABLE cycle ADD COLUMN hasta_cycle_no INTEGER")
    print("cycle.hasta_cycle_no eklendi.")
else:
    print("cycle.hasta_cycle_no zaten var.")

# Bos olanlari zaman sirasina gore doldur
hastalar = [r["id"] for r in b.execute("SELECT id FROM hasta")]
doldurulan = 0
for hid in hastalar:
    cycles = b.execute(
        "SELECT id, hasta_cycle_no FROM cycle WHERE hasta_id = ? "
        "ORDER BY COALESCE(opu_zamani, hcg_zamani, olusturma_zamani), id",
        (hid,),
    ).fetchall()
    for i, c in enumerate(cycles, start=1):
        if c["hasta_cycle_no"] is None:
            b.execute("UPDATE cycle SET hasta_cycle_no = ? WHERE id = ?", (i, c["id"]))
            doldurulan += 1

b.commit()
print(f"{doldurulan} cycle numaralandirildi.")

print("\nOrnek:")
for r in b.execute(
    "SELECT h.dosya_no, c.cycle_no, c.hasta_cycle_no, c.cycle_tipi "
    "FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
    "ORDER BY h.dosya_no, c.hasta_cycle_no LIMIT 10"
):
    print(f"  dosya {r['dosya_no']}  lab no {r['cycle_no']:12s} "
          f"-> {r['hasta_cycle_no']}. cycle ({r['cycle_tipi']})")

b.close()
print("\nGoc 005 tamam.")
