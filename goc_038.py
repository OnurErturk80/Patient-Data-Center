"""Göç 038 — sperm dondurmada işlemi yapan ve onam ekleri.

Kullanıcının isteği:
- Sperm dondurma işlemini kimin yaptığı kaydedilsin (aşama ekranlarındaki
  "İşlemi yapan"ın aynı deseni — v6.99'dan beri şifresi olan personelden
  seçiliyor, serbest metin değil).
- Sperm dondurma kaydına "Onamlar" diye bir bölüm eklensin, oraya PDF ve
  fotoğraf kaydedilebilsin.

- `sperm_dondurma.yapan_ad` — serbest metin kolon (aşama ekranlarındaki
  `islem_yapan.yapan_ad` ile aynı isim/tür), ama sperm dondurmanın cycle'ı
  yok, `islem_yapan` tablosu `cycle_id` istiyor (NOT NULL) — o yüzden ayrı
  bir tabloya değil, doğrudan `sperm_dondurma`'ya eklendi (satır başına tek
  değer zaten, `UNIQUE` gerekmiyor).
- Yeni tablo `sperm_dondurma_dosya` — `goruntu`'nun aynısı ama `cycle_id`
  yerine `sperm_dondurma_id`; `goruntu.cycle_id` NOT NULL olduğu için sperm
  dondurmanın (hiç cycle'ı olmayan hastalarda, v6.85) ekleri oraya
  yazılamaz. `id` `AUTOINCREMENT` — `/sperm-onam/{id}` adrese yazılıyor
  (tuzak #13).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_038.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(sperm_dondurma)")]
if "yapan_ad" not in kolonlar:
    b.execute("ALTER TABLE sperm_dondurma ADD COLUMN yapan_ad TEXT")
    print("sperm_dondurma.yapan_ad eklendi.")
else:
    print("sperm_dondurma.yapan_ad zaten var.")

tablolar = [r[0] for r in b.execute(
    "SELECT name FROM sqlite_master WHERE type='table'")]
if "sperm_dondurma_dosya" not in tablolar:
    b.execute("""
        CREATE TABLE sperm_dondurma_dosya (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id             INTEGER NOT NULL REFERENCES lab(id),
            sperm_dondurma_id  INTEGER NOT NULL REFERENCES sperm_dondurma(id),
            dosya_yolu         TEXT NOT NULL,
            orijinal_dosya_adi TEXT,
            kullanici_id       INTEGER REFERENCES kullanici(id),
            olusturma_zamani   TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    print("sperm_dondurma_dosya tablosu oluşturuldu.")
else:
    print("sperm_dondurma_dosya tablosu zaten var.")

b.commit()
b.close()
print("\nGoc 038 tamam.")
