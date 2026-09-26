"""Göç 052 — Tank düzeni ve Excel kaydı (v6.189).

Kullanıcının isteği (2026-09-25): "Laboratuvarda cryo harita en önemli kayıt
... Bu haritanın kesinlikle bozulmaması gerekiyor. ... hastanın embriyolarını
dondururken program bana tanklarda boş yerleri önermesi." Boş yer
önerebilmek için program tankların DÜZENİNİ bilmeli: hangi gobletler var,
her birine kaç straw sığıyor, hangisinde ne duruyor. Bugüne kadar `konum`
yalnızca bir tüpe yazılan yerdi (dondurma ekranında elle yazılıyordu);
boş goblet programda hiç yoktu.

Düzen laboratuvarın Cryo Haritası Excel'inden geliyor (`cryo_esle.py
yerlesim`). Bu göç yalnızca yerini açar:

- `konum.kapasite`: gobletin kaç straw aldığı. Kullanıcı: "Her goblete 4
  straw/Cryotop konuyor". Boş (NULL) = bilinmiyor (eski "cane" yerleri,
  sperm yerleri, elle yazılmış konum) -- öyle bir yer hiç önerilmez.
- `konum.kategori`: 'embriyo' / 'sperm' -- Excel'de gobletin içeriğinden.
- `konum.sira`: gobletin kanister içindeki sırası (Excel'deki sıra; üst kat
  alttakilerden sonra). "Yakın goblet" bu sırayla ölçülüyor.
- `excel_kaydi`: Excel'de bir gobletde duran ama programda karşılığı olan
  tüp bulunamayan satır (kullanıcının seçimi, 2026-09-25: "Gobletinde
  'Excel kaydı' olarak dursun"). Excel'deki ad, tarih, içerik ve VİAL
  yazısıyla gobletinde durur, yuvası dolu sayılır; sonra bir tüpe
  bağlanabilir ya da tanktan çıkarıldı diye işaretlenebilir. Kayıt
  silinmiyor: `durum` 'tankta' / 'baglandi' / 'kaldirildi'.
  - `anahtar`: satırın içerik anahtarı (tank, kanister, goblet, ad, tarih,
    içerik, VİAL + aynı içerikteki sırası). Araç ikinci kez çalışınca aynı
    satırı ikinci kez açmasın diye; Excel'e satır eklenmiş olsa da tutar
    (sayfa/satır numarası kayar, içerik kaymaz).
  - `id` AUTOINCREMENT: kimlik adrese yazılıyor (`/cryo/excel-kaydi/{id}`,
    tuzak #13).
  - `tasiyici_id` / `onceki_konum_id`: bağlandığı tüp ve tüpün bağlamadan
    önceki konumu (yanlış bağlama geri alınınca tüp oraya dönüyor).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_052.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(konum)")]
for ad, tip in (("kapasite", "INTEGER"), ("kategori", "TEXT"), ("sira", "INTEGER")):
    if ad not in kolonlar:
        b.execute(f"ALTER TABLE konum ADD COLUMN {ad} {tip}")
        print(f"konum.{ad} eklendi.")
    else:
        print(f"konum.{ad} zaten var.")

if not b.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                 "AND name='excel_kaydi'").fetchone():
    b.execute("""
        CREATE TABLE excel_kaydi (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id             INTEGER NOT NULL REFERENCES lab(id),
            anahtar            TEXT NOT NULL,
            konum_id           INTEGER REFERENCES konum(id),
            kategori           TEXT NOT NULL,
            soyad              TEXT,
            ad                 TEXT,
            es_adi             TEXT,
            tarih              TEXT,
            tarih_ham          TEXT,
            icerik             TEXT,
            vial               TEXT,
            notlar             TEXT,
            tip                TEXT,
            renk               TEXT,
            eslesmeme_sebebi   TEXT,
            eslesmeme_notu     TEXT,
            kaynak_sayfa       TEXT,
            kaynak_satir       INTEGER,
            durum              TEXT NOT NULL DEFAULT 'tankta',
            tasiyici_id        INTEGER REFERENCES tasiyici(id),
            onceki_konum_id    INTEGER REFERENCES konum(id),
            islem_zamani       TEXT,
            islem_notu         TEXT,
            islem_kullanici_id INTEGER REFERENCES kullanici(id),
            kullanici_id       INTEGER REFERENCES kullanici(id),
            olusturma_zamani   TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE (lab_id, anahtar)
        )""")
    print("excel_kaydi tablosu açıldı.")
else:
    print("excel_kaydi tablosu zaten var.")
    # Bağlanan tüpün bağlamadan önceki konumu: yanlış bağlama geri alınınca
    # tüp oraya dönüyor.
    if "onceki_konum_id" not in [r[1] for r in b.execute("PRAGMA table_info(excel_kaydi)")]:
        b.execute("ALTER TABLE excel_kaydi ADD COLUMN onceki_konum_id "
                  "INTEGER REFERENCES konum(id)")
        print("excel_kaydi.onceki_konum_id eklendi.")
b.execute("CREATE INDEX IF NOT EXISTS idx_excel_kaydi_konum ON excel_kaydi(konum_id)")
b.execute("CREATE INDEX IF NOT EXISTS idx_excel_kaydi_tasiyici ON excel_kaydi(tasiyici_id)")
b.commit()
b.close()
print("\nGoc 052 tamam.")
