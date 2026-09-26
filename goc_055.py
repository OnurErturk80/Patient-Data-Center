"""Göç 055 — ICSI'nin genel bulguları, tedavi başına (v6.200).

Kullanıcının isteği (2026-09-26): "ICSI bölümünde de yumurtaların bulguları
tek tek yazılıyor. ART lab formunda en altta yorum bölümüne yazılıyordu.
Bunu kaldıralım. Onun yerine ICSI bölümüne genel bulgular bölümü olsun,
açılır pencere şeklinde, aynı yumurta bulguları gibi bulgular olsun; bunlara
ek olarak sperm problemleri olsun: Sperm morfolojisi kötü, Baş Boyun
anomalisi var, Sperm motilitesi kötü, diğer elle yazılabilir olsun. Bunlar
ART lab formunun en alt kısmındaki yorum bölümüne eklensin."

- `tedavi_bulgu`: bir tedavinin (bir aşamanın, bugün yalnızca 'icsi') genel
  bulguları. `specimen_bulgu`'nun tedavi hali: örneğe değil tedaviye bağlı,
  küme olarak yazılıyor (sil + ekle). Bir satır ya bir liste değeri
  (`liste_adi` + `bulgu_kodu`) ya da elle yazılan "Diğer" (`metin`).
  `liste_adi` tutuluyor, çünkü seçenekler iki listeden geliyor
  (`bulgu_icsi` yumurta, `bulgu_sperm` sperm) ve etiket listesiyle aranıyor.
- `bulgu_sperm` listesi: kullanıcının yazdığı üç sorun, onun yazımıyla.
  Etiketler `liste_degeri`'nde, laboratuvar değiştirebilir.

`cycle_id`'ye bağlı yeni bir tablo: kalıcı silme (`cycle_tamamen_sil()`) ve
`teshis_silme.py` onu biliyor (tuzak #4).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_055.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

if not b.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                 "AND name='tedavi_bulgu'").fetchone():
    b.execute("""
        CREATE TABLE tedavi_bulgu (
            id           INTEGER PRIMARY KEY,
            cycle_id     INTEGER NOT NULL REFERENCES cycle(id),
            asama        TEXT NOT NULL,
            liste_adi    TEXT,
            bulgu_kodu   TEXT,
            metin        TEXT,
            zaman        TEXT NOT NULL,
            kullanici_id INTEGER NOT NULL REFERENCES kullanici(id),
            CHECK (bulgu_kodu IS NOT NULL OR metin IS NOT NULL)
        )""")
    b.execute("CREATE INDEX idx_tedavi_bulgu_cycle ON tedavi_bulgu(cycle_id, asama)")
    print("tedavi_bulgu tablosu açıldı.")
else:
    print("tedavi_bulgu tablosu zaten var.")

DEGERLER = [
    ("sperm_morfoloji_kotu", "Sperm morfolojisi kötü"),
    ("bas_boyun_anomalisi", "Baş Boyun anomalisi var"),
    ("sperm_motilite_kotu", "Sperm motilitesi kötü"),
]
son_sira = b.execute(
    "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
    "WHERE lab_id=1 AND liste_adi='bulgu_sperm'").fetchone()[0]
for kod, etiket in DEGERLER:
    if b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                 "AND liste_adi='bulgu_sperm' AND kod=?", (kod,)).fetchone():
        continue
    son_sira += 1
    b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'bulgu_sperm',?,?,?)", (kod, etiket, son_sira))
    print(f"  + bulgu_sperm: {kod} ({etiket})")
b.commit()

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 055 tamam.")
