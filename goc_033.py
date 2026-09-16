"""Göç 033 — Sperm Dondurma modülü.

Kullanıcının isteği (2026-09-16): Cryo haritasına "Sperm Dondurma" eklendi,
mevcut "Tank"/Cryo ekranı "Embriyo Dondurma" oldu (bu yalnızca ekran
metni -- README/CLAUDE.md'ye bak, tablo ve rota adları "cryo"/"tasiyici"
kalıyor, v6.79'daki cycle->tedavi deseninin aynısı).

İki değişiklik:
1. `tasiyici.kategori` -- embriyo taşıyıcıları ile sperm taşıyıcıları aynı
   tabloda tutuluyor (ikisi de etiket/renk/konum aynı fikir), ama Embriyo
   Dondurma ekranı yalnızca kendi taşıyıcılarını göstermeli. Yeni kolon
   varsayılan 'embriyo' -- mevcut bütün satırlar zaten embriyo taşıyıcısı.
2. `sperm_dondurma` -- taşıyıcı başına tek kayıt: dondurma öncesi semen
   analizi (hacim/konsantrasyon/motilite, `sperm_analiz` ile aynı kolon
   adlarıyla) + `tasiyici_id` üzerinden taşıyıcı/konum. Çözme/kullanım
   takibi bilerek yok (kullanıcının kararı) -- `olay` tablosuna hiç
   dokunmuyor, kendi başına duran bir kayıt.
   `iptal_mi` deseni `olay`'daki ile aynı: normal silme fiziksel değil,
   işaretleme (CLAUDE.md "Silme = iptal işaretleme").

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_033.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(tasiyici)")]
if "kategori" not in kolonlar:
    b.execute("ALTER TABLE tasiyici ADD COLUMN kategori TEXT NOT NULL DEFAULT 'embriyo'")
    print("tasiyici.kategori eklendi (mevcut satırlar 'embriyo').")
else:
    print("tasiyici.kategori zaten var.")

tablolar = [r[0] for r in b.execute(
    "SELECT name FROM sqlite_master WHERE type='table'")]
if "sperm_dondurma" not in tablolar:
    b.execute("""
        CREATE TABLE sperm_dondurma (
            id                      INTEGER PRIMARY KEY,
            lab_id                  INTEGER NOT NULL REFERENCES lab(id),
            hasta_id                INTEGER NOT NULL REFERENCES hasta(id),
            tasiyici_id             INTEGER NOT NULL REFERENCES tasiyici(id),
            dondurma_zamani         TEXT NOT NULL,
            hacim_ml                REAL,
            konsantrasyon_milyon_ml REAL,
            total_motil_yuzde       REAL,
            notlar                  TEXT,
            kullanici_id            INTEGER REFERENCES kullanici(id),
            iptal_mi                INTEGER NOT NULL DEFAULT 0,
            iptal_kullanici_id      INTEGER REFERENCES kullanici(id),
            iptal_zamani            TEXT,
            iptal_sebep             TEXT,
            olusturma_zamani        TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    print("sperm_dondurma tablosu olusturuldu.")
else:
    print("sperm_dondurma tablosu zaten var.")

b.commit()
b.close()
print("\nGoc 033 tamam.")
