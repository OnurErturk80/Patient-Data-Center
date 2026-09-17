"""Göç 037 — doğumda kaçıncı hafta ve doğan bebeklerin cinsiyet/kilosu.

Kullanıcının isteği: gebelik sonucu doğumla bittiğinde kaçıncı haftada
doğduğu ve her bebeğin (ikiz/üçüz olabilir, `bebek_sayisi` zaten çoğulu
destekliyordu) cinsiyeti ve kilosu girilebilsin.

- `gebelik_sonucu.dogum_haftasi` — tek değer, doğumun kendisine ait
  (ikizde de aynı haftada doğarlar).
- Yeni tablo `dogan_bebek` — her bebek kendi satırında (`sira` ile 1, 2, 3...),
  `beta_hcg` ile aynı desen: doğrudan `cycle_id`'ye bağlı, `gebelik_sonucu`'na
  değil.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_037.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(gebelik_sonucu)")]
if "dogum_haftasi" not in kolonlar:
    b.execute("ALTER TABLE gebelik_sonucu ADD COLUMN dogum_haftasi INTEGER")
    print("gebelik_sonucu.dogum_haftasi eklendi.")
else:
    print("gebelik_sonucu.dogum_haftasi zaten var.")

tablolar = [r[0] for r in b.execute(
    "SELECT name FROM sqlite_master WHERE type='table'")]
if "dogan_bebek" not in tablolar:
    b.execute("""
        CREATE TABLE dogan_bebek (
            id       INTEGER PRIMARY KEY,
            lab_id   INTEGER NOT NULL REFERENCES lab(id),
            cycle_id INTEGER NOT NULL REFERENCES cycle(id),
            sira     INTEGER NOT NULL,
            cinsiyet TEXT,
            kilo_kg  REAL,
            UNIQUE (cycle_id, sira)
        )
    """)
    print("dogan_bebek tablosu oluşturuldu.")
else:
    print("dogan_bebek tablosu zaten var.")

b.commit()
b.close()
print("\nGoc 037 tamam.")
