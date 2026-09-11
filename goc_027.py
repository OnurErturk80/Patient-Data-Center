"""Göç 027 — cycle'ın bitişi: "işlem bitti" kaydı.

Kullanıcının kâğıt üzerindeki düzeni: laboratuvarda işi bitmemiş hastaların
formları bir klasörde durur, her sabah ona bakılır. İş bitince (embriyolar
donduruldu, transfer yapıldı ya da iptal oldu) form arşive kaldırılır.

Program bugüne kadar bunu ayırt edemiyordu: `cycle.durum` yalnızca `aktif`
ve `iptal` alıyordu ve `iptal`i yazan tek yer **silme ekranıydı**. Yani
"normal bitti" demek için cycle'ı iptal etmek gerekiyordu — oysa dondurma
ve transfer bir iptal değil, işin olağan sonu.

Bu göç iki kolon ekliyor:

  - `bitis_sebebi` — 'dondurma' | 'transfer' | 'iptal'. Cycle'ın nasıl
    bittiği. `durum` ile ikisi birlikte okunur: dondurma ve transfer
    `durum='tamamlandi'` yapar, iptal `durum='iptal'` (var olan değer,
    "Geri al" akışı aynen duruyor).
  - `bitis_zamani` — ne zaman bitirildiği. Klinik bir zaman değil, kaydın
    kapatıldığı an; bu yüzden elle girilmiyor.

`durum` kolonuna CHECK yok, yeni `tamamlandi` değeri için şema değişikliği
gerekmiyor. Eski kayıtlar `aktif` kalır — kimse geriye dönük bitmiş
sayılmaz, kullanıcı klasörü kendisi boşaltır.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_027.py      (Mac'te: python3 goc_027.py)
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
for kolon in ("bitis_sebebi", "bitis_zamani"):
    if kolon in mevcut:
        print(f"cycle.{kolon} zaten var.")
    else:
        b.execute(f"ALTER TABLE cycle ADD COLUMN {kolon} TEXT")
        b.commit()
        print(f"  + cycle.{kolon}")

# Yapilacaklar listesi her acilista "durum='aktif'" cycle'lari tariyor.
# Kayit sayisi buyudukce bu tarama uzar; indeks onu kisa tutar.
b.execute("CREATE INDEX IF NOT EXISTS ix_cycle_durum ON cycle(lab_id, durum)")
b.commit()
print("  + ix_cycle_durum")

# ----------------------------------------------------------------------- ozet
print()
for satir in b.execute("SELECT durum, COUNT(*) n FROM cycle GROUP BY durum"):
    print(f"  {satir['durum']:14} {satir['n']}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"\nKirik referans: {len(kirik)}")
b.close()
print("\nGoc 027 tamam.")
