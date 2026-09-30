"""Göç 059 — Tüpün imha kaydı (v6.227).

Kullanıcının anlatımı (2026-09-29, PGT): genetik incelemede sorunlu çıkan
embriyo "hastaya göre" tankta kalıyor ya da imha ediliyor; imha kaydı
"bütün tüplerde" olsun -- embriyo, yumurta ve sperm tüpü.

Programda tanktan çıkan bir tüp yalnızca çözülmüş (boşaltıldı), kullanılmış
(sperm) ya da başka merkeze taşınmış (v6.182) olabiliyordu. İmha edilen tüp
"dolu" kalınca Cryo Haritası'nda duruyor, boş yer önerisi o yuvayı dolu
sayıyor, formların "Kalan dondurulmuş" satırına giriyordu. Artık
`tasiyici.durum = 'imha'` (kolon serbest metin, CHECK yok) ve üç yeni kolon,
gönderimin (goc_051) karşılığı:

- `imha_zamani`: gün (YYYY-MM-DD) -- "Kalan dondurulmuş" o günün tankını
  söylüyor, form aylar sonra basılsa da (v6.152'nin kuralı).
- `imha_sebep`: `discard_sebep` listesinin kodu (Gelişimsel, Genetik, Hasta
  talebi, Saklama süresi doldu, Diğer); boş olabilir.
- `imha_notu`: serbest açıklama.

Kayıt silinmiyor, örneklerin durumu değişmiyor: imha geri alınabiliyor
(yanlış tüp işaretlendiyse).

`discard_sebep` listesi şemanın ilk sürümünden beri kurulumla geliyor; eski
bir kurulumda eksikse ekleniyor (laboratuvarın düzenlediği etiketlere
dokunulmuyor).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_059.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(tasiyici)")]
for ad in ("imha_zamani", "imha_sebep", "imha_notu"):
    if ad not in kolonlar:
        b.execute(f"ALTER TABLE tasiyici ADD COLUMN {ad} TEXT")
        print(f"tasiyici.{ad} eklendi.")
    else:
        print(f"tasiyici.{ad} zaten var.")

SEBEPLER = [("gelisimsel", "Gelişimsel"), ("genetik", "Genetik"),
            ("hasta_talebi", "Hasta talebi"), ("sure_doldu", "Saklama süresi doldu"),
            ("diger", "Diğer")]
son_sira = b.execute(
    "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
    "WHERE lab_id=1 AND liste_adi='discard_sebep'").fetchone()[0]
for kod, etiket in SEBEPLER:
    if b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                 "AND liste_adi='discard_sebep' AND kod=?", (kod,)).fetchone():
        continue
    son_sira += 1
    b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'discard_sebep',?,?,?)", (kod, etiket, son_sira))
    print(f"  + discard_sebep: {kod} ({etiket})")

b.commit()
b.close()
print("\nGoc 059 tamam.")
