"""Göç 042 — programdan önceki cryo haritası (eski kayıtlar).

Kullanıcının isteği: "Bu excelde laboratuvarımdaki cryo harita kayıtları
var. Bu haritayı programa yerleştirmek istiyorum. Cryo haritası bölümüne
yerleştirmek istiyorum. Bu harita programdan önce oluşturuldu."

Kullanıcı dört soruyu da yanıtladı (2026-09-21):
  1. Haritadaki her satır **hâlâ tankta duran** bir örnek -- kullanılmış /
     çözülmüş kayıt listesi değil, canlı envanter.
  2. Hepsi girecek; yıl sınırı yok (2011-2026, ~5.400 satır).
  3. Embriyo listesinde eşi geçmeyen erkeklere (onkoloji gibi) kendi hasta
     kayıtları açılacak.
  4. Tarihi olmayan satırlar "tarih girilmemiş" diye gösterilecek.

Neden yeni bir tablo:

- **Sahte `cycle`/`specimen`/`olay` satırı açılmıyor.** `/cryo` ve
  `/istatistik` türetilmiş ekranlar (CLAUDE.md "Cryo haritası
  türetilmiştir", "İstatistikler türetilmiştir"); 15 yıllık, klinik
  ayrıntısı olmayan envanteri `olay` tablosuna sahte vitrifikasyon diye
  yazmak M2/fertilizasyon/blastokist oranlarını geri dönülmez biçimde
  bozardı ve hangi sayının gerçek olduğu bir daha ayrılamazdı.

- **`konum` tablosu PAYLAŞILIYOR** (`eski_cryo.konum_id`). Bu şart:
  program "bu goblet dolu mu" sorusunu `konum`dan yanıtlıyor. Eski
  kayıtlar ayrı bir konum kavramı kullansaydı program 2019'dan kalma bir
  embriyonun durduğu gobleti boş gösterir, oraya yeni bir vitrifikasyon
  yerleştirilmesine izin verirdi.

- **`tasiyici` tablosu paylaşılmıyor**, bilerek. Her eski satır için bir
  `tasiyici` satırı açmak `/cryo`'nun mevcut Embriyo Dondurma listesini
  (`WHERE t.durum='dolu' AND t.kategori='embriyo'`) 3.884 tane içeriği
  görünmeyen taşıyıcıyla doldururdu -- o liste `olay` üzerinden sayıyor,
  eski kayıtların `olay` satırı yok. Taşıyıcının bilgisi (tip/renk/adet)
  bu yüzden `eski_cryo`'nun kendi kolonlarında; `tasiyici` "programın
  kendi açtığı taşıyıcı" anlamını koruyor.

- `id` **`AUTOINCREMENT`**: kimlik adrese yazılıyor (`/eski-cryo/{id}/...`),
  tuzak #13.

- `UNIQUE (lab_id, kaynak_sayfa, kaynak_satir, kaynak_sutun)`: içeri alma
  **idempotent**. Kullanıcı Excel'i düzeltip yeniden yüklerse aynı hücre
  ikinci bir kayıt açmıyor, mevcut satır güncelleniyor.

- `hasta_id` **NULL olabilir** ve öyle başlıyor: eşleştirme sonradan, elle
  onaylanarak yapılıyor (dosyada hasta dosya numarası yok, yalnızca isim
  var -- CLAUDE.md "isimle eşleştirme yok" kuralı bu yüzden gevşetilmedi,
  isim yalnızca **öneri** üretiyor, bağlamayı insan onaylıyor).

Ayrıca `tasiyici_tipi` listesine Rapid-i ve Vitrifit ekleniyor: eski
haritada geçen iki taşıyıcı markası (Cryolock/Cryotop/Straw/Vial zaten
vardı).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_042.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

tablolar = [r[0] for r in b.execute(
    "SELECT name FROM sqlite_master WHERE type='table'")]

if "eski_cryo" not in tablolar:
    b.execute("""
        CREATE TABLE eski_cryo (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id               INTEGER NOT NULL REFERENCES lab(id),
            konum_id             INTEGER REFERENCES konum(id),
            kategori             TEXT NOT NULL DEFAULT 'embriyo',
            soyad                TEXT,
            ad                   TEXT,
            es_adi               TEXT,
            tarih                TEXT,
            tarih_notu           TEXT,
            icerik               TEXT,
            vial_metni           TEXT,
            tip                  TEXT,
            renk                 TEXT,
            adet                 INTEGER,
            durum                TEXT NOT NULL DEFAULT 'dolu',
            kaynak_sayfa         TEXT NOT NULL,
            kaynak_satir         INTEGER NOT NULL,
            kaynak_sutun         INTEGER NOT NULL,
            hasta_id             INTEGER REFERENCES hasta(id),
            eslesme_zamani       TEXT,
            eslesme_kullanici_id INTEGER REFERENCES kullanici(id),
            notlar               TEXT,
            olusturma_zamani     TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE (lab_id, kaynak_sayfa, kaynak_satir, kaynak_sutun)
        )
    """)
    print("eski_cryo tablosu olusturuldu.")
else:
    print("eski_cryo tablosu zaten var.")

for ad, sut in (("eski_cryo_hasta", "hasta_id"),
                ("eski_cryo_konum", "konum_id"),
                ("eski_cryo_durum", "durum")):
    b.execute(f"CREATE INDEX IF NOT EXISTS {ad} ON eski_cryo({sut})")
print("eski_cryo dizinleri hazir.")

# ------------------------------------------------- eski haritadaki taşıyıcılar
DEGERLER = [("rapid_i", "Rapid-i"), ("vitrifit", "Vitrifit")]

son_sira = b.execute(
    "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
    "WHERE lab_id=1 AND liste_adi='tasiyici_tipi'").fetchone()[0]
eklenen = 0
for kod, etiket in DEGERLER:
    var = b.execute(
        "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi='tasiyici_tipi' "
        "AND kod=?", (kod,)).fetchone()
    if var:
        continue
    son_sira += 1
    b.execute(
        "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'tasiyici_tipi',?,?,?)", (kod, etiket, son_sira))
    print(f"  + tasiyici_tipi: {kod} ({etiket})")
    eklenen += 1
if not eklenen:
    print("tasiyici_tipi listesi zaten guncel.")

b.commit()

kayitlar = b.execute(
    "SELECT etiket FROM liste_degeri WHERE lab_id=1 AND liste_adi='tasiyici_tipi' "
    "AND aktif_mi=1 ORDER BY sira").fetchall()
print(f"\ntasiyici_tipi ({len(kayitlar)}): " + ", ".join(r["etiket"] for r in kayitlar))
print("eski_cryo satiri:", b.execute("SELECT COUNT(*) FROM eski_cryo").fetchone()[0])

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 042 tamam.")
