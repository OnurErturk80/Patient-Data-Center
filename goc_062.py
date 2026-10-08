"""Göç 062 — Transferde yeniden değerlendirme: canlılık oranı (v6.262).

Kullanıcının isteği (2026-10-08): "Transfer menüsünde blastokist aşamasından
veya çözmeden gelen embriyonun yeniden değerlendirmesi olsun. Yani canlılık
oranı girilebilsin."

`olay.tr_canlilik`: transfer kaydının canlılık oranı (%). Çözmenin kendi
`thaw_canlilik`'inden ayrı: taze (çözülmemiş) blastokistin çözme olayı yok,
o oran yazılacak yer olmazdı; çözülen embriyoda da çözmeden sonraki ilk
ölçüm ile transfer öncesi yeniden değerlendirme iki ayrı bilgi.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_062.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(olay)")]
if "tr_canlilik" in kolonlar:
    print("olay.tr_canlilik zaten var.")
else:
    b.execute("ALTER TABLE olay ADD COLUMN tr_canlilik REAL")
    b.commit()
    print("olay.tr_canlilik eklendi.")
b.close()
