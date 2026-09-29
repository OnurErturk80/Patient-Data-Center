"""Göç 057 — Tedavide kadının ve erkeğin bulaş hastalığı (v6.219).

Kullanıcının isteği (2026-09-29): "Hastaların tedavi kayıtları sırasında
kadın ve erkeğin bulaş hastalığı olup olmadığı seçeneği olsun. Bu
hastalıkları seçebilelim. Hepatit HİV gibi virütik hastalıklar seçilebilsin.
Seçim tedavi boyunca en üstte adının olduğu yerde fark edilebilecek şekilde
görünsün."

- `cycle.bulas_kadin`, `cycle.bulas_erkek`: tedavinin kaydı, kişi başına bir
  metin. Boş (NULL) = girilmedi, `yok` = bulaş hastalığı yok, başka bir değer
  = seçilen hastalıkların kodları virgülle ("hbv,hiv"), elle yazılan "Diğer"
  varsa `|`'den sonra ("hbv|Sifiliz"). Okuyan ve yazan tek yer
  `db.bulas_oku()` / `db.bulas_yaz()`.
  Tablo değil kolon: tedavinin bir alanı -- tedavi formu yazıyor, değişiklik
  geçmişi formun öteki alanlarıyla birlikte tutuyor, kalıcı silme ve kart
  birleştirme tedaviyle birlikte götürüyor.
- `bulas_hastaligi` listesi: Hepatit B, Hepatit C, HIV (kullanıcının örnekleri:
  "Hepatit HİV gibi virütik hastalıklar"). Etiketler `liste_degeri`'nde.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_057.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(cycle)")]
for kolon in ("bulas_kadin", "bulas_erkek"):
    if kolon not in kolonlar:
        b.execute(f"ALTER TABLE cycle ADD COLUMN {kolon} TEXT")
        print(f"cycle.{kolon} eklendi.")
    else:
        print(f"cycle.{kolon} zaten var.")

DEGERLER = [
    ("hbv", "Hepatit B"),
    ("hcv", "Hepatit C"),
    ("hiv", "HIV"),
]
son_sira = b.execute(
    "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
    "WHERE lab_id=1 AND liste_adi='bulas_hastaligi'").fetchone()[0]
for kod, etiket in DEGERLER:
    if b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                 "AND liste_adi='bulas_hastaligi' AND kod=?", (kod,)).fetchone():
        continue
    son_sira += 1
    b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'bulas_hastaligi',?,?,?)", (kod, etiket, son_sira))
    print(f"  + bulas_hastaligi: {kod} ({etiket})")
b.commit()
b.close()
print("\nGoc 057 tamam.")
