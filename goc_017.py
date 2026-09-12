"""Göç 017 — cycle_tipi kodu 'taze' -> 'ivf_icsi'.

'taze' kodu iki farkli seyi cagristiriyordu: tedavi tipi ve taze transfer.
Taze/donmus transfer ayrimi zaten olay.tr_tipi alaninda tutuluyor.
Bu goc tedavi tipi kodunu netlestirir.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_017.py
"""

import re
import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

sql = b.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='cycle'"
                ).fetchone()["sql"]

if "'ivf_icsi'" in sql:
    print("cycle_tipi kisiti zaten guncel.")
else:
    kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(cycle)")]
    # Tablo adi tirnakli olabilir (onceki RENAME'den): CREATE TABLE "cycle" (...)
    yeni_sql = re.sub(r'CREATE TABLE\s+"?cycle"?', "CREATE TABLE cycle_yeni",
                      sql, count=1)
    for eski, yeni in [
        ("cycle_tipi IN ('taze','fet','oosit_cryo')",
         "cycle_tipi IN ('ivf_icsi','fet','oosit_cryo')"),
        ("cycle_tipi IN ('taze','fet')",
         "cycle_tipi IN ('ivf_icsi','fet','oosit_cryo')"),
    ]:
        yeni_sql = yeni_sql.replace(eski, yeni)
    if "'ivf_icsi'" not in yeni_sql:
        sys.exit("CHECK kisiti beklenen bicimde degil:\n" + sql)

    indeksler = [r["sql"] for r in b.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='cycle' "
        "AND sql IS NOT NULL")]

    b.execute("PRAGMA foreign_keys=OFF")
    b.execute("BEGIN")
    b.execute(yeni_sql)
    k = ", ".join(kolonlar)
    # Kopyalarken kodu cevir; yeni CHECK 'taze' kabul etmiyor
    secim = ", ".join(
        "CASE WHEN cycle_tipi='taze' THEN 'ivf_icsi' ELSE cycle_tipi END"
        if x == "cycle_tipi" else x
        for x in kolonlar)
    b.execute(f"INSERT INTO cycle_yeni ({k}) SELECT {secim} FROM cycle")
    b.execute("DROP TABLE cycle")
    b.execute("ALTER TABLE cycle_yeni RENAME TO cycle")
    for i in indeksler:
        b.execute(i)
    b.execute("COMMIT")
    b.execute("PRAGMA foreign_keys=ON")
    print("cycle_tipi kodu guncellendi: taze -> ivf_icsi")

# Liste degeri
b.execute("UPDATE liste_degeri SET kod='ivf_icsi', etiket='IVF / ICSI cycle''ı' "
          "WHERE lab_id=1 AND liste_adi='cycle_tipi' AND kod='taze'")
b.execute("INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
          "VALUES (1,'cycle_tipi','ivf_icsi','IVF / ICSI cycle''ı',0)")
b.commit()

print("\nTedavi tipleri:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='cycle_tipi' ORDER BY sira"):
    print(f"  {r['kod']:12s} {r['etiket']}")

print("\nCycle dagilimi:")
for r in b.execute("SELECT cycle_tipi, COUNT(*) k FROM cycle GROUP BY cycle_tipi"):
    print(f"  {r['cycle_tipi']:12s} {r['k']}")

print("\nTransfer tipleri (ayri alan, degismedi):")
for r in b.execute("SELECT tr_tipi, COUNT(*) k FROM olay "
                   "WHERE tip='transfer' AND iptal_mi=0 GROUP BY tr_tipi"):
    print(f"  tr_tipi={r['tr_tipi']:10s} {r['k']}")

print(f"\nKirik referans: {len(b.execute('PRAGMA foreign_key_check').fetchall())}")
b.close()
print("Goc 017 tamam.")
