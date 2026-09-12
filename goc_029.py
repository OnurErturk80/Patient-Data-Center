"""Göç 029 — laboratuvarın kendi form kalıpları (yüklenen .xlsx).

Programın içinde iki resmî form gömülü (`form_kalip.json`): Embriyoloji Özet
ve ART Lab. Raporu. Bunlar **bu laboratuvarın** formları. Kullanıcının kararı
(2026-09-11): başka bir laboratuvar kendi formunu yükleyip programdaki
verilerle doldurup çıktı alabilsin.

Tek tablo:

  `lab_formu`
    ad             ekranda görünen ad ("Embriyoloji Raporu")
    dosya_adi      yüklenen dosyanın adı — nereden geldiği belli olsun diye
    yon            'dikey' | 'yatay' (kalıptan okundu, elle değiştirilebilir)
    kalip          kalıbın tamamı, JSON metin olarak
    aktif_mi       0 yapılan form cycle ekranında görünmez, kaydı durur
    kullanici_id   yükleyen

**Kalıp neden veritabanında, dosyada değil?** `lab.db` `tasi.py` ile USB'de
taşınan tek dosya. Kalıp diskte ayrı bir klasörde dursaydı taşınırken unutulur,
program karşı makinede "form yok" derdi. Formun içindeki görsel (logo) de aynı
sebeple kalıbın içinde, base64 olarak duruyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_029.py      (Mac'te: python3 goc_029.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

var = b.execute("SELECT name FROM sqlite_master WHERE type='table' "
                "AND name='lab_formu'").fetchone()
if var:
    print("lab_formu zaten var.")
else:
    b.execute("""
        CREATE TABLE lab_formu (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id           INTEGER NOT NULL REFERENCES lab(id),
            ad               TEXT NOT NULL,
            dosya_adi        TEXT,
            yon              TEXT NOT NULL DEFAULT 'dikey',
            kalip            TEXT NOT NULL,
            aktif_mi         INTEGER NOT NULL DEFAULT 1,
            bilinmeyen       TEXT,
            kullanici_id     INTEGER REFERENCES kullanici(id),
            olusturma_zamani TEXT
        )
    """)
    b.commit()
    print("  + lab_formu")

# Formda gecen ama programda karsiligi olmayan etiketler ("{{dosyano}}" gibi
# yazim hatalari) yuklemede bulunup buraya yaziliyor; liste ekraninda uyari
# olarak gorunuyor. Tabloyu daha once kurmus bir kurulum icin ayrica ekleniyor.
mevcut = {r["name"] for r in b.execute("PRAGMA table_info(lab_formu)")}
if "bilinmeyen" not in mevcut:
    b.execute("ALTER TABLE lab_formu ADD COLUMN bilinmeyen TEXT")
    b.commit()
    print("  + lab_formu.bilinmeyen")

b.execute("CREATE INDEX IF NOT EXISTS ix_lab_formu "
          "ON lab_formu(lab_id, aktif_mi)")
b.commit()
print("  + ix_lab_formu")

n = b.execute("SELECT COUNT(*) FROM lab_formu").fetchone()[0]
print(f"\nYuklenmis form: {n}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 029 tamam.")
