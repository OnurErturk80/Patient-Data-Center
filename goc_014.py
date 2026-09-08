"""Göç 014 — görüntü aşama listesine blastokist günlerini ekler.

Blastokist ekrani gun 4-5-6-7 kaydi tutuyor ama fotograf asama listesinde
karsiliklari yoktu. gun4, gun5, gun6, gun7 eklenir.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_014.py      (Mac'te: python3 goc_014.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

# Tam siralama — gelisim sirasi
SIRA = [
    ("denudasyon", "Denüdasyon"),
    ("icsi", "ICSI"),
    ("fertilizasyon_kontrolu", "Fertilizasyon kontrolü"),
    ("gun2", "Gün 2"),
    ("gun3", "Gün 3"),
    ("gun4", "Gün 4"),
    ("gun5", "Gün 5"),
    ("gun6", "Gün 6"),
    ("gun7", "Gün 7"),
    ("blastokist", "Blastokist (gün belirtilmemiş)"),
    ("vitrifikasyon_oncesi", "Vitrifikasyon öncesi"),
    ("thaw_sonrasi", "Thaw sonrası"),
    ("transfer_oncesi", "Transfer öncesi"),
    ("diger", "Diğer"),
]

for i, (kod, etiket) in enumerate(SIRA):
    var = b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                    "AND liste_adi='goruntu_asama' AND kod=?", (kod,)).fetchone()
    if var:
        b.execute("UPDATE liste_degeri SET etiket=?, sira=? WHERE lab_id=1 "
                  "AND liste_adi='goruntu_asama' AND kod=?", (etiket, i, kod))
    else:
        b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
                  "VALUES (1,'goruntu_asama',?,?,?)", (kod, etiket, i))
b.commit()

print("Goruntu asama listesi:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='goruntu_asama' ORDER BY sira"):
    print(f"  {r['kod']:22s} {r['etiket']}")

n = b.execute("SELECT COUNT(*) FROM goruntu WHERE specimen_id IS NULL").fetchone()[0]
print(f"\nOosite baglanmamis (cycle arsivi) goruntu: {n}")
b.close()
print("\nGoc 014 tamam.")
