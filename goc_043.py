"""Göç 043 — seçim listelerindeki "oosit" etiketleri "yumurta" olur.

Kullanıcının isteği (2026-09-22): "oosit yazan her yeri Yumurta ile
değiştir." Ekran metinlerinin çoğu `metinler.py`'de, ama iki tanesi
**veritabanında** (`liste_degeri.etiket`) çünkü laboratuvar onları kendi
düzenleyebiliyor:

    bulgu_icsi  / oval_oosit   "Oval oosit"  -> "Oval yumurta"
    endikasyon  / donor_oosit  "Donör oosit" -> "Donör yumurta"

**`kod` değişmiyor** (`oval_oosit`, `donor_oosit`) — kayıtlı `specimen_bulgu`
ve `cycle.endikasyon` satırları o kodu tutuyor; `goc_032`'nin "Yumurta
Dondurma" için yaptığının aynısı, yalnızca etiket.

**Yalnızca eski etiketi taşıyan satır güncellenir.** Yönetici o etiketi
kendisi değiştirmişse dokunulmuyor — göç kullanıcının yazdığını ezmemeli.

Numara 042 değil 043: `goc_042` geri alınmış cryo-harita özelliğinindi
(v6.127/v6.129) ve kullanıcının `goc_kaydi` tablosunda "uygulandı" olarak
durabiliyor; aynı adı kullanan yeni bir göç sessizce atlanırdı.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_043.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

DEGISENLER = (
    ("bulgu_icsi", "oval_oosit", "Oval oosit", "Oval yumurta"),
    ("endikasyon", "donor_oosit", "Donör oosit", "Donör yumurta"),
)

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

for liste, kod, eski, yeni in DEGISENLER:
    r = b.execute("SELECT etiket FROM liste_degeri WHERE lab_id=? "
                  "AND liste_adi=? AND kod=?", (_db.LAB_ID, liste, kod)).fetchone()
    if not r:
        print(f"  {liste}/{kod}: liste_degeri'nde yok, atlandi")
    elif r["etiket"] == yeni:
        print(f"  {liste}/{kod}: zaten '{yeni}'")
    elif r["etiket"] != eski:
        print(f"  {liste}/{kod}: elle degistirilmis ('{r['etiket']}'), dokunulmadi")
    else:
        b.execute("UPDATE liste_degeri SET etiket=? WHERE lab_id=? "
                  "AND liste_adi=? AND kod=?", (yeni, _db.LAB_ID, liste, kod))
        b.commit()
        print(f"  {liste}/{kod}: '{eski}' -> '{yeni}'")

b.close()
print("\nGoc 043 tamam.")
