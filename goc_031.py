"""Göç 031 — tedavi tipine 'FET (3->5 kültür)' eklenir.

Kullanıcının isteği (2026-09-12): bazı FET'lerde gün 2/3 embriyosu çözülüp
aynı gün transfer ediliyor (mevcut "fet" tipi bunu karşılıyor); bazı
FET'lerde ise gün 2/3 embriyosu çözülüp gün 5'e kadar kültürlenip öyle
transfer ediliyor. İkincisi ayrı bir tedavi tipi: "fet_kultur" -- seçilince
sol menüde Çözme, Blastokist, Transfer, Gebelik sonucu görünür (araya
blastokist değerlendirmesi giriyor).

`cycle.cycle_tipi` kolonundaki CHECK kısıtı yeni kodu kabul etmiyordu.
SQLite CHECK kısıtını değiştiremediğinden tablo yeniden oluşturulur (goc_016
ve goc_017'deki aynı yöntem). Veri korunur; referanslar (specimen, olay,
goruntu...) ad üzerinden çözüldüğü için yeniden adlandırma sonrası çalışmaya
devam eder.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_031.py
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

if "fet_kultur" in sql:
    print("cycle_tipi kisiti zaten guncel.")
else:
    kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(cycle)")]
    # Tablo adi tirnakli olabilir (onceki RENAME'den): CREATE TABLE "cycle" (...)
    yeni_sql = re.sub(r'CREATE TABLE\s+"?cycle"?', "CREATE TABLE cycle_yeni",
                      sql, count=1)
    yeni_sql = yeni_sql.replace(
        "cycle_tipi IN ('ivf_icsi','fet','oosit_cryo')",
        "cycle_tipi IN ('ivf_icsi','fet','fet_kultur','oosit_cryo')")
    if "fet_kultur" not in yeni_sql:
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
    print("cycle_tipi kisiti genisletildi (+ fet_kultur).")

# Secim listesine ekleniyor -- dropdown db.liste("cycle_tipi")'den besleniyor,
# koddan degil. Sira mevcut en yuksek siranin bir fazlasi: listede zaten olan
# secimlerin sirasini bozmamak icin (elle yeniden siralanmis olabilir).
mevcut = b.execute(
    "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi='cycle_tipi' "
    "AND kod='fet_kultur'").fetchone()
if mevcut:
    print("liste_degeri'nde 'fet_kultur' zaten var.")
else:
    son_sira = b.execute(
        "SELECT COALESCE(MAX(sira), -1) m FROM liste_degeri "
        "WHERE lab_id=1 AND liste_adi='cycle_tipi'").fetchone()["m"]
    b.execute(
        "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'cycle_tipi','fet_kultur',?,?)",
        ("FET (3→5 kültür)", son_sira + 1))
    b.commit()
    print("  + liste_degeri: fet_kultur")

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
print("\nGoc 031 tamam.")
