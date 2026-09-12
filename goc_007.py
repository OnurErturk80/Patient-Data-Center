"""Göç 007 — görüntü kaynağı (kamera / elle) ve aşama seçim listesi.

Kullanım:  python goc_007.py
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(goruntu)")]
if "kaynak" not in kolonlar:
    b.execute("ALTER TABLE goruntu ADD COLUMN kaynak TEXT NOT NULL DEFAULT 'kamera'")
    print("goruntu.kaynak eklendi (mevcut kayitlar 'kamera' sayildi).")
else:
    print("goruntu.kaynak zaten var.")

ASAMALAR = [
    ("denudasyon", "Denüdasyon"),
    ("icsi", "ICSI"),
    ("fertilizasyon_kontrolu", "Fertilizasyon kontrolü"),
    ("gun2", "Gün 2"),
    ("gun3", "Gün 3"),
    ("blastokist", "Blastokist"),
    ("vitrifikasyon_oncesi", "Vitrifikasyon öncesi"),
    ("thaw_sonrasi", "Thaw sonrası"),
    ("transfer_oncesi", "Transfer öncesi"),
    ("diger", "Diğer"),
]
for i, (kod, etiket) in enumerate(ASAMALAR):
    b.execute(
        "INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'goruntu_asama',?,?,?)", (kod, etiket, i))

b.commit()

n = b.execute("SELECT COUNT(*) FROM liste_degeri "
              "WHERE lab_id=1 AND liste_adi='goruntu_asama'").fetchone()[0]
print(f"goruntu_asama listesi: {n} secenek")

for r in b.execute("SELECT kaynak, COUNT(*) k FROM goruntu GROUP BY kaynak"):
    print(f"  {r[0]}: {r[1]} goruntu")

b.close()
print("\nGoc 007 tamam.")
