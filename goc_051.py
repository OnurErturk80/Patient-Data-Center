"""Göç 051 — Başka merkeze taşınan tüp (v6.182).

Kullanıcının bilgisi (2026-09-25): "Tedavide embriyosu var gözüküp ama cryo
haritada embriyo gözükmüyorsa bazen hastalar embriyolarını başka tüp bebek
ünitesine taşıma yapabiliyor." İsteği: taşıyıcı sayfasından işaretlensin,
notlara "1 tüp 12.03.2025 tarihinde şuraya taşındı" diye yazılsın.

Programda bir tüp yalnızca dolu / boşaltıldı (çözüldü) / kullanıldı (sperm)
olabiliyordu. Başka merkeze giden tüp "dolu" kalıyor, Cryo Haritası'nda
konumsuz görünüyor ve sonraki formların "Kalan dondurulmuş" satırına
giriyordu. Artık `tasiyici.durum = 'gonderildi'` (kolon serbest metin, CHECK
yok) ve üç yeni kolon:

- `gonderim_zamani`: gün (YYYY-MM-DD) -- "Kalan dondurulmuş" o günün
  tankını söylüyor, form aylar sonra basılsa da (v6.152'nin kuralı).
- `gonderim_yeri`: nereye, kullanıcının yazdığı gibi ("Memorial
  Hastanesi'ne"); nota olduğu gibi giriyor, program ek uydurmuyor.
- `gonderim_notu`: serbest açıklama.

Kayıt silinmiyor, örneklerin durumu değişmiyor: gönderim geri alınabiliyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_051.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(tasiyici)")]
for ad in ("gonderim_zamani", "gonderim_yeri", "gonderim_notu"):
    if ad not in kolonlar:
        b.execute(f"ALTER TABLE tasiyici ADD COLUMN {ad} TEXT")
        print(f"tasiyici.{ad} eklendi.")
    else:
        print(f"tasiyici.{ad} zaten var.")
b.commit()
b.close()
print("\nGoc 051 tamam.")
