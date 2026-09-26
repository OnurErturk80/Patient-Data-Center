"""Göç 054 — Laboratuvarın kendi Cryo Haritası Excel'i, şablon olarak (v6.199).

Kullanıcı (2026-09-26): "Tankları Excel'e aktar dediğimde benim kullandığım
orjinal cryo haritaya çıktı alsam. Farklı yapıda excel oluşturma benim
orjinal cryo harita excelimi birebir kullan." Program o dosyayı saklayıp her
çıktıda onu dolduruyor (`cryo_sablon.py`): sayfalar, tablolar, sütunlar ve
biçim aynen; yalnızca straw satırlarının değerleri programın bugünkü haliyle.

- `cryo_sablon`: yüklenen dosyanın kendisi (`icerik`, BLOB). `lab.db`'de,
  diskte değil: `lab.db` USB ile taşınan tek dosya (`tasi.py`), şablon ayrı
  dursaydı öteki makinede olmazdı (`lab_formu.kalip`'ın gerekçesi). Dosyada
  hasta adları var, ama `lab.db`'de zaten hepsi var. Tam dökümüne
  (`disari.TUM_TABLOLAR`) girmiyor: klinik kayıt değil, tek hücreye sığmaz.
- Laboratuvar başına tek şablon: yenisi yüklenince eskisi siliniyor.
- `yukleme_zamani` ekranda gösterilen yerel saat; `olusturma_zamani`
  şemanın UTC damgası (elle yazılmıyor, `tasi.py` ona bakıyor).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_054.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
if not b.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                 "AND name='cryo_sablon'").fetchone():
    b.execute("""
        CREATE TABLE cryo_sablon (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id           INTEGER NOT NULL REFERENCES lab(id),
            dosya_adi        TEXT NOT NULL,
            icerik           BLOB NOT NULL,
            boyut            INTEGER NOT NULL,
            imza             TEXT NOT NULL,
            kullanici_id     INTEGER REFERENCES kullanici(id),
            yukleme_zamani   TEXT,
            olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now'))
        )""")
    print("cryo_sablon tablosu açıldı.")
else:
    print("cryo_sablon tablosu zaten var.")
b.commit()
b.close()
print("\nGoc 054 tamam.")
