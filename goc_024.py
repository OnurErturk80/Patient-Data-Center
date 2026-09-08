"""Göç 024 — çözmenin hangi cycle için yapıldığı (`olay.thaw_cycle_id`).

Donmuş embriyo doğduğu cycle'a bağlı kalır (`specimen.cycle_id`), FET cycle'ı
ile bağı transfer kaydı kurardı (`olay.tr_cycle_id`). Sorun: **transfere
ulaşmayan çözme** hiçbir yere yazılmıyordu. FET'te iki embriyo çözülüp ikisi de
canlı çıkmazsa o FET cycle'ında tek satır iz kalmıyordu; cycle bazında sağkalım
da hesaplanamıyordu.

Bu kolon "bu çözme hangi tedavi için yapıldı" sorusunu yanıtlar. `tr_cycle_id`
ile aynı mantık, sadece bir aşama önce.

Geriye dönük doldurma:
  1. Embriyo sonradan transfer edilmişse → transferin yapıldığı cycle
  2. Edilmemişse → çözmenin yazıldığı cycle (bugüne kadarki davranış)

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_024.py      (Mac'te: python3 goc_024.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("PRAGMA foreign_keys = ON")

kolonlar = {r[1] for r in b.execute("PRAGMA table_info(olay)")}
if "thaw_cycle_id" in kolonlar:
    print("thaw_cycle_id kolonu zaten var.")
else:
    b.execute("ALTER TABLE olay ADD COLUMN thaw_cycle_id INTEGER REFERENCES cycle(id)")
    print("olay.thaw_cycle_id eklendi.")

b.execute("CREATE INDEX IF NOT EXISTS idx_olay_thaw_cycle ON olay(thaw_cycle_id)")

# 1. Transferi olan çözmeler: transferin yapıldığı cycle
i1 = b.execute(
    "UPDATE olay SET thaw_cycle_id = ("
    "  SELECT t.tr_cycle_id FROM olay t "
    "  WHERE t.specimen_id = olay.specimen_id AND t.tip='transfer' "
    "  AND t.iptal_mi=0 AND t.tr_cycle_id IS NOT NULL "
    "  ORDER BY t.id DESC LIMIT 1) "
    "WHERE tip='thaw' AND thaw_cycle_id IS NULL "
    "AND EXISTS (SELECT 1 FROM olay t WHERE t.specimen_id = olay.specimen_id "
    "            AND t.tip='transfer' AND t.iptal_mi=0 "
    "            AND t.tr_cycle_id IS NOT NULL)").rowcount

# 2. Kalanlar: çözmenin yazıldığı cycle (kaynak cycle)
i2 = b.execute(
    "UPDATE olay SET thaw_cycle_id = cycle_id "
    "WHERE tip='thaw' AND thaw_cycle_id IS NULL").rowcount

b.commit()
print(f"Dolduruldu: {i1} kayit transferden, {i2} kayit kaynak cycle'dan.")

toplam = b.execute("SELECT COUNT(*) FROM olay WHERE tip='thaw'").fetchone()[0]
bos = b.execute("SELECT COUNT(*) FROM olay WHERE tip='thaw' "
                "AND thaw_cycle_id IS NULL").fetchone()[0]
print(f"Toplam cozme kaydi: {toplam}, cycle'i bos kalan: {bos}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("Goc 024 tamam.")
