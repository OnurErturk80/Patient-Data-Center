"""Göç 032 — "Oosit dondurma" tedavi tipi "Yumurta Dondurma" olarak yeniden adlandırılır.

Kullanıcının isteği (2026-09-16): aynı klinik yol (OPU -> Denüdasyon ->
Vitrifikasyon -> Çözme), yalnızca ekrandaki etiket değişiyor -- yeni bir tip
değil. `kod` ("oosit_cryo") ve bütün kod tarafı (TIP_KODLARI, TIP_ASAMALARI,
mevcut cycle kayıtları) aynen duruyor; `liste_degeri.etiket` güncelleniyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_032.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

mevcut = b.execute(
    "SELECT etiket FROM liste_degeri WHERE lab_id=1 AND liste_adi='cycle_tipi' "
    "AND kod='oosit_cryo'").fetchone()

if not mevcut:
    print("liste_degeri'nde 'oosit_cryo' bulunamadi, atlaniyor.")
elif mevcut["etiket"] == "Yumurta Dondurma":
    print("Etiket zaten guncel.")
else:
    b.execute(
        "UPDATE liste_degeri SET etiket='Yumurta Dondurma' "
        "WHERE lab_id=1 AND liste_adi='cycle_tipi' AND kod='oosit_cryo'")
    b.commit()
    print(f"  '{mevcut['etiket']}' -> 'Yumurta Dondurma'")

print("\nTedavi tipleri:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='cycle_tipi' ORDER BY sira"):
    print(f"  {r['kod']:12s} {r['etiket']}")

b.close()
print("\nGoc 032 tamam.")
