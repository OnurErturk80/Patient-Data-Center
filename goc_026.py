"""Göç 026 — modül bazlı erişim izni.

Yönetici, her kullanıcının hangi ekranlara girebileceğini tek tek belirler.
Yeni tablo:

    yetki(lab_id, kullanici_id, modul)   -- satır varsa izin var

**Mevcut kullanıcılar hiçbir erişim kaybetmez**: bu göç herkese tüm modülleri
verir. Kısıtlama yöneticinin bilinçli olarak kaldırdığı kutulardan doğar,
göçün yan etkisinden değil. Yeni bir modül eklenirse (yeni bir aşama ekranı
gibi) bu göç tekrar çalıştırıldığında onu da herkese verir — kimse sessizce
ekran kaybetmesin diye.

Yöneticiler bu tablodan bağımsız: `rol='yonetici'` her yere girer, satıra
bakılmaz. Yetki kutuları yalnızca embriyologlar için anlamlı.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_026.py      (Windows'ta: python goc_026.py)
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

# app.py'deki MODULLER ile aynı kalmalı. Yeni bir modül eklersen buraya da ekle
# ve göçü tekrar çalıştır — yoksa kimse o ekrana giremez.
MODULLER = [
    "hasta", "opu", "androloji", "denudasyon", "icsi", "fert", "cleavage",
    "blast", "vitrifikasyon", "thaw", "transfer", "gebelik", "cryo", "foto",
    "silme",
]

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

b.execute("""
CREATE TABLE IF NOT EXISTS yetki (
    id           INTEGER PRIMARY KEY,
    lab_id       INTEGER NOT NULL REFERENCES lab(id),
    kullanici_id INTEGER NOT NULL REFERENCES kullanici(id),
    modul        TEXT NOT NULL,
    UNIQUE(kullanici_id, modul)
)""")
b.execute("CREATE INDEX IF NOT EXISTS yetki_kullanici ON yetki(kullanici_id)")
b.commit()

kullanicilar = b.execute("SELECT id, kullanici_adi FROM kullanici").fetchall()
eklenen = 0
for k in kullanicilar:
    for m in MODULLER:
        var = b.execute("SELECT 1 FROM yetki WHERE kullanici_id=? AND modul=?",
                        (k["id"], m)).fetchone()
        if var:
            continue
        b.execute("INSERT INTO yetki (lab_id, kullanici_id, modul) "
                  "VALUES (1,?,?)", (k["id"], m))
        eklenen += 1
b.commit()

if eklenen:
    print(f"  + {eklenen} yetki satiri eklendi "
          f"({len(kullanicilar)} kullanici x {len(MODULLER)} modul)")
else:
    print("Yetkiler zaten guncel.")

print("\nKullanici basina modul sayisi:")
for k in kullanicilar:
    n = b.execute("SELECT COUNT(*) FROM yetki WHERE kullanici_id=?",
                  (k["id"],)).fetchone()[0]
    print(f"  {k['kullanici_adi']:18} {n} / {len(MODULLER)}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"\nKirik referans: {len(kirik)}")
b.close()
print("\nGoc 026 tamam.")
