"""Göç 039 — "Yumurta Çözme" tedavi tipi ve çözme notu.

Kullanıcının isteği:
- Daha önce `oosit_cryo` (Yumurta Dondurma) tedavisinde dondurulmuş
  yumurtaların, FET'in embriyo için yaptığı gibi, AYRI bir tedavide
  çözülebilmesi. Yeni tip yalnızca **Çözme** aşamasından oluşuyor —
  ICSI/fertilizasyon vb. gerekiyorsa ayrıca yeni bir tedavi açılır.
- Çözme ekranına (FET, FET (3→5 kültür) ve şimdi Yumurta Çözme'de) tek,
  paylaşılan bir **Not** alanı — taşıyıcıdaki tüm örnekler için ortak.

- `cycle.cycle_tipi` kolonundaki CHECK kısıtı yeni kodu kabul etmiyordu.
  SQLite CHECK kısıtını değiştiremediğinden tablo yeniden oluşturulur
  (goc_016/goc_017/goc_031'deki aynı yöntem). Veri korunur.
- `liste_degeri`'ne `yumurta_cozme` eklenir — dropdown oradan besleniyor.
- `olay.thaw_notu TEXT` — çözme notunun yazıldığı kolon, taşıyıcıdaki her
  örnek için aynı değer tekrarlanır (`thaw_kontrol_zamani` ile aynı desen).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_039.py
"""

import re
import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

# --------------------------------------------------------- CHECK kısıtı
sql = b.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='cycle'"
                ).fetchone()["sql"]

if "yumurta_cozme" in sql:
    print("cycle_tipi kisiti zaten guncel.")
else:
    kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(cycle)")]
    yeni_sql = re.sub(r'CREATE TABLE\s+"?cycle"?', "CREATE TABLE cycle_yeni",
                      sql, count=1)
    yeni_sql = yeni_sql.replace(
        "cycle_tipi IN ('ivf_icsi','fet','fet_kultur','oosit_cryo')",
        "cycle_tipi IN ('ivf_icsi','fet','fet_kultur','oosit_cryo','yumurta_cozme')")
    if "yumurta_cozme" not in yeni_sql:
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
    print("cycle_tipi kisiti genisletildi (+ yumurta_cozme).")

# --------------------------------------------------------- seçim listesi
mevcut = b.execute(
    "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi='cycle_tipi' "
    "AND kod='yumurta_cozme'").fetchone()
if mevcut:
    print("liste_degeri'nde 'yumurta_cozme' zaten var.")
else:
    son_sira = b.execute(
        "SELECT COALESCE(MAX(sira), -1) m FROM liste_degeri "
        "WHERE lab_id=1 AND liste_adi='cycle_tipi'").fetchone()["m"]
    b.execute(
        "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'cycle_tipi','yumurta_cozme',?,?)",
        ("Yumurta Çözme", son_sira + 1))
    b.commit()
    print("  + liste_degeri: yumurta_cozme")

# --------------------------------------------------------- çözme notu
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(olay)")]
if "thaw_notu" not in kolonlar:
    b.execute("ALTER TABLE olay ADD COLUMN thaw_notu TEXT")
    b.commit()
    print("olay.thaw_notu eklendi.")
else:
    print("olay.thaw_notu zaten var.")

print("\nTedavi tipleri:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='cycle_tipi' ORDER BY sira"):
    print(f"  {r['kod']:14s} {r['etiket']}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"\nKirik referans: {len(kirik)}")
b.close()
print("\nGoc 039 tamam.")
