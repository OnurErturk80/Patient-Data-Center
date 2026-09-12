"""Göç 020 — "işlemi yapan" kaydı.

Her cycle aşaması için (androloji, denüdasyon, ICSI, fertilizasyon, gün 2/3,
blastokist, vitrifikasyon, çözme, transfer, gebelik) o aşamayı **fiilen yapan**
kişinin adı ekranın altından elle girilir. Kaydı giren kullanıcıdan
(`kullanici_id`) ayrıdır — personel işlemi yapan değil, sonradan giren kişi
olabilir. Aşama başına tek satır (`UNIQUE (cycle_id, asama)`).

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_020.py      (Mac'te: python3 goc_020.py)
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)

var = b.execute(
    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='islem_yapan'"
).fetchone()

if var:
    print("islem_yapan tablosu zaten var.")
else:
    b.execute("""
        CREATE TABLE islem_yapan (
            id           INTEGER PRIMARY KEY,
            lab_id       INTEGER NOT NULL REFERENCES lab(id),
            cycle_id     INTEGER NOT NULL REFERENCES cycle(id),
            asama        TEXT NOT NULL,
            yapan_ad     TEXT,
            zaman        TEXT,
            kullanici_id INTEGER REFERENCES kullanici(id),
            UNIQUE (cycle_id, asama)
        )
    """)
    b.execute("CREATE INDEX idx_islem_yapan_cycle ON islem_yapan(cycle_id)")
    b.commit()
    print("islem_yapan tablosu olusturuldu.")

n = b.execute("SELECT COUNT(*) FROM islem_yapan").fetchone()[0]
print(f"islem_yapan satir sayisi: {n}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("Goc 020 tamam.")
