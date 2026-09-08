"""Göç 012 — kriyoprezervasyon: konum şeması ve taşıyıcı tipleri.

Laboratuvarın tank hiyerarşisini tanımlar. Varsayılan dört seviye:
Tank / Kanister / Goblet / Pozisyon

Farklı çalışıyorsan (Tank/Rack/Box/Slot gibi) asagidaki SEVIYELER
listesini duzenleyip scripti yeniden calistir.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_012.py      (Mac'te: python3 goc_012.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

# (sira, ekranda gorunen ad, deger tipi: sayi / harf / serbest)
SEVIYELER = [
    (1, "Tank", "serbest"),
    (2, "Kanister", "serbest"),
    (3, "Goblet", "serbest"),
    (4, "Pozisyon", "serbest"),
]

TASIYICI_TIPLERI = [
    ("cryotop", "Cryotop"),
    ("straw", "Straw"),
    ("vial", "Vial"),
    ("cryolock", "Cryolock"),
    ("diger", "Diğer"),
]

TASIYICI_RENKLERI = [
    ("beyaz", "Beyaz"), ("sari", "Sarı"), ("mavi", "Mavi"),
    ("kirmizi", "Kırmızı"), ("yesil", "Yeşil"), ("turuncu", "Turuncu"),
    ("mor", "Mor"), ("siyah", "Siyah"),
]

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

var = b.execute("SELECT COUNT(*) k FROM konum_semasi WHERE lab_id=1").fetchone()["k"]
if var:
    print(f"Konum semasi zaten tanimli ({var} seviye). Guncelleniyor...")
    b.execute("DELETE FROM konum_semasi WHERE lab_id=1")

for sira, ad, tip in SEVIYELER:
    b.execute("INSERT INTO konum_semasi (lab_id, seviye_sirasi, seviye_adi, deger_tipi) "
              "VALUES (1,?,?,?)", (sira, ad, tip))

for liste, degerler in (("tasiyici_tipi", TASIYICI_TIPLERI),
                        ("tasiyici_renk", TASIYICI_RENKLERI)):
    for i, (kod, etiket) in enumerate(degerler):
        b.execute("INSERT OR IGNORE INTO liste_degeri "
                  "(lab_id, liste_adi, kod, etiket, sira) VALUES (1,?,?,?,?)",
                  (liste, kod, etiket, i))
b.commit()

print("\nKonum semasi:")
for r in b.execute("SELECT seviye_sirasi, seviye_adi FROM konum_semasi "
                   "WHERE lab_id=1 ORDER BY seviye_sirasi"):
    print(f"  {r['seviye_sirasi']}. {r['seviye_adi']}")

n = b.execute("SELECT COUNT(*) FROM liste_degeri WHERE liste_adi='tasiyici_tipi'").fetchone()[0]
r = b.execute("SELECT COUNT(*) FROM liste_degeri WHERE liste_adi='tasiyici_renk'").fetchone()[0]
print(f"\nTasiyici tipleri: {n}, renkler: {r}")

k = b.execute("SELECT COUNT(*) FROM konum WHERE lab_id=1").fetchone()[0]
t = b.execute("SELECT COUNT(*) FROM tasiyici WHERE lab_id=1").fetchone()[0]
print(f"Kayitli konum: {k}, tasiyici: {t}")

b.close()
print("\nGoc 012 tamam.")
