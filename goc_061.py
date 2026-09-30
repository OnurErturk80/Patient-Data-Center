"""Göç 061 — Transfer hekimi (v6.232).

Kullanıcının isteği (2026-09-30): "Resmî formların TRANSFER KLİNİSYENi
yazsın. Ekle." Embriyoloji Özet'in "TRANSFER KLİNİSYEN" ve ART Lab'ın
"Hekimler: ... ET" kutusu v6.37'den beri boştu: programda transfer hekimi
tutulmuyordu.

`cycle.transfer_hekim`: transferin YAPILDIĞI tedavinin kaydı (FET'te FET'in,
taze transferde tedavinin kendisi) -- `opu_hekim`'in (goc_025) karşılığı.
Transfer ekranında OPU'nun hekim menüsüyle giriliyor (varsayılan hekim seçili,
"Diğer" elle). Laboratuvar personeli değil, `islem_yapan`'a yazılmaz.

Var olan kayıtlara dokunmuyor. Access'ten aktarılmış tedavilerin transfer
hekimi Access'in "TRANSFER KLİNİSYEN" sütununda; onu
`aktar_access.py transfer_hekim` (ya da `aktar_toplu.py kip=transfer_hekim`)
yalnızca boş olana yazıyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_061.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(cycle)")]
if "transfer_hekim" in kolonlar:
    print("cycle.transfer_hekim zaten var.")
else:
    b.execute("ALTER TABLE cycle ADD COLUMN transfer_hekim TEXT")
    b.commit()
    print("cycle.transfer_hekim eklendi.")
b.close()
