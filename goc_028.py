"""Göç 028 — cycle'ın planlanan tarihi (takvim).

Kullanıcı ileri tarihli işler için kayıt açabilmek istiyor: "haftaya
14/09/2026 Pazartesi FET olacak". Karar (2026-09-11): planlanan iş **ayrı bir
randevu kaydı değil, cycle'ın kendisi**. Cycle bugün açılıyor, planlanan
tarihi giriliyor.

Tek kolon ekleniyor:

  - `planlanan_tarih` — 'YYYY-MM-DD'. Saat yok; plan gün bazında yapılıyor.

Davranış (app.py `cycle_listesi`):
  - Tarihi **gelecekte** olan cycle ana ekranın "Yapılacaklar"ında görünmez;
    yoksa haftaya olacak bir iş bu hafta boyunca her sabah listeyi şişirirdi.
    Takvimde ve ana ekrandaki "Yaklaşanlar" kartında görünür.
  - Tarih gelince (`<= bugün`) cycle kendiliğinden Yapılacaklar'a düşer.
  - `planlanan_tarih` boş olan cycle eskisi gibi davranır — eski kayıtların
    hiçbiri etkilenmiyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_028.py      (Mac'te: python3 goc_028.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

mevcut = {r["name"] for r in b.execute("PRAGMA table_info(cycle)")}
if "planlanan_tarih" in mevcut:
    print("cycle.planlanan_tarih zaten var.")
else:
    b.execute("ALTER TABLE cycle ADD COLUMN planlanan_tarih TEXT")
    b.commit()
    print("  + cycle.planlanan_tarih")

# Takvim ve "Yaklasanlar" her acilista bu kolona gore suzuyor.
b.execute("CREATE INDEX IF NOT EXISTS ix_cycle_planlanan "
          "ON cycle(lab_id, planlanan_tarih)")
b.commit()
print("  + ix_cycle_planlanan")

# ----------------------------------------------------------------------- ozet
n = b.execute("SELECT COUNT(*) FROM cycle WHERE planlanan_tarih IS NOT NULL").fetchone()[0]
toplam = b.execute("SELECT COUNT(*) FROM cycle").fetchone()[0]
print(f"\nPlanlanan tarihi girilmis cycle: {n} / {toplam}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 028 tamam.")
