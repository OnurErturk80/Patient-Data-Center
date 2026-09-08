"""Göç 016 — tedavi tipine 'oosit cryo' eklenir.

cycle.cycle_tipi kolonundaki CHECK kisiti sadece taze/fet kabul ediyordu.
SQLite CHECK kisitini degistiremediginden tablo yeniden olusturulur.
Veri korunur; referanslar (specimen, olay, goruntu...) ad uzerinden coz-
uldugu icin yeniden adlandirma sonrasi calismaya devam eder.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_016.py
"""

import re
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

sql = b.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='cycle'"
                ).fetchone()["sql"]

if "oosit_cryo" in sql:
    print("cycle_tipi kisiti zaten guncel.")
else:
    kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(cycle)")]
    # Tablo adi tirnakli olabilir (onceki RENAME'den): CREATE TABLE "cycle" (...)
    yeni_sql = re.sub(r'CREATE TABLE\s+"?cycle"?', "CREATE TABLE cycle_yeni",
                      sql, count=1)
    yeni_sql = yeni_sql.replace("cycle_tipi IN ('taze','fet')",
                                "cycle_tipi IN ('ivf_icsi','fet','oosit_cryo')")
    if "oosit_cryo" not in yeni_sql:
        sys.exit("CHECK kisiti beklenen bicimde degil, elle bakilmali:\n" + sql)

    indeksler = [r["sql"] for r in b.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='cycle' "
        "AND sql IS NOT NULL")]

    b.execute("PRAGMA foreign_keys=OFF")
    b.execute("BEGIN")
    b.execute(yeni_sql)
    k = ", ".join(kolonlar)
    b.execute(f"INSERT INTO cycle_yeni ({k}) SELECT {k} FROM cycle")
    b.execute("DROP TABLE cycle")
    b.execute("ALTER TABLE cycle_yeni RENAME TO cycle")
    for i in indeksler:
        b.execute(i)
    b.execute("COMMIT")
    b.execute("PRAGMA foreign_keys=ON")
    print("cycle_tipi kisiti genisletildi (taze / fet / oosit_cryo).")

TIPLER = [("ivf_icsi", "IVF / ICSI cycle'ı"), ("fet", "FET (donmuş embriyo transferi)"),
          ("oosit_cryo", "Oosit dondurma")]
for i, (kod, etiket) in enumerate(TIPLER):
    b.execute("INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'cycle_tipi',?,?,?)", (kod, etiket, i))
b.commit()

print("\nTedavi tipleri:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='cycle_tipi' ORDER BY sira"):
    print(f"  {r['kod']:12s} {r['etiket']}")

print("\nMevcut cycle dagilimi:")
for r in b.execute("SELECT cycle_tipi, COUNT(*) k FROM cycle GROUP BY cycle_tipi"):
    print(f"  {r['cycle_tipi']:12s} {r['k']}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"\nKirik referans: {len(kirik)}")
b.close()
print("Goc 016 tamam.")
