"""Göç 034 — Sperm dondurmaya sebep ve "hangi tedavide kullanıldı" bağlantısı.

Kullanıcının isteği (2026-09-16): Cryo Harita > Sperm Dondurma'dan açılan yeni
hasta kaydı yalnızca erkek hasta bilgilerini içersin (eş alanları yok) ve
dondurma sebebini de sorsun. Ayrıca: bu hasta ileride evlenip eşi için bir IVF
tedavisi açılırsa, dondurulmuş spermi o tedaviye **bağlayabilmek** lazım —
sperm dondurma hâlâ kendi hastasına (erkeğe) ait kalıyor, yalnızca "hangi
tedavi için kullanıldı" sorusu ayrı bir alanda yanıtlanıyor. Bu,
`olay.thaw_cycle_id`'nin embriyo tarafında yaptığının aynısı: sahiplik
değişmiyor, kullanım amacı ayrı bir FK'de.

İki yeni kolon:
- `sperm_dondurma.sebep`             — serbest metin ("onkoloji tedavisi
  öncesi", "elektif" gibi); sabit bir liste_degeri açılmadı, klinik
  kategorileri kullanıcıyla birlikte belirlemek gerekirdi.
- `sperm_dondurma.kullanim_cycle_id` — NULL'sa hâlâ dolapta/kullanılmamış;
  doluysa o tedavide (androloji ekranından bağlanan) kullanılmış demek.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_034.py
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

if "sebep" not in kolonlar:
    b.execute("ALTER TABLE sperm_dondurma ADD COLUMN sebep TEXT")
    print("sperm_dondurma.sebep eklendi.")
else:
    print("sperm_dondurma.sebep zaten var.")

if "kullanim_cycle_id" not in kolonlar:
    b.execute(
        "ALTER TABLE sperm_dondurma ADD COLUMN kullanim_cycle_id "
        "INTEGER REFERENCES cycle(id)")
    print("sperm_dondurma.kullanim_cycle_id eklendi.")
else:
    print("sperm_dondurma.kullanim_cycle_id zaten var.")

b.commit()
b.close()
print("\nGoc 034 tamam.")
