"""Göç 056 — `olay(tr_cycle_id)` dizini (v6.201).

Tedavinin günü (`db.tedavi_tarihi()`: OPU, hCG, FET'te çözme ya da transfer,
...) FET'lerde `olay`'a "bu tedavi için yapılan çözme ya da transfer" diye
soruyor: `thaw_cycle_id = c.id OR tr_cycle_id = c.id`. `thaw_cycle_id`'nin
dizini vardı, `tr_cycle_id`'nin yoktu; OR'un bir kolu dizinsiz olunca SQLite
her FET için bütün `olay` tablosunu tarıyor. Ölçüldü: 1.909 tedavinin günü
dizinsiz 5,2 sn, dizinle 0,01 sn. Sağlık Bakanlığı'nın aylık verileri
(SİKLUS SAYISI ve yeni hasta, v6.201) bu işlevden geçiyor; aktarım aracının
ay önbelleği de (`aktar_access._yeni_tedaviler()`, "3.000 tedavide 14 sn").

Yalnızca dizin: hiçbir satır değişmiyor. Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_056.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = {r[1] for r in b.execute("PRAGMA table_info(olay)")}
if "tr_cycle_id" not in kolonlar:
    print("olay.tr_cycle_id yok -- dizin gerekmiyor.")
elif b.execute("SELECT 1 FROM sqlite_master WHERE type='index' "
               "AND name='idx_olay_tr_cycle'").fetchone():
    print("idx_olay_tr_cycle zaten var.")
else:
    b.execute("CREATE INDEX idx_olay_tr_cycle ON olay(tr_cycle_id)")
    print("idx_olay_tr_cycle dizini açıldı.")
b.commit()
b.close()
print("\nGoc 056 tamam.")
