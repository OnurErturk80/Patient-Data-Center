"""Göç 049 — `olay.vit_tasiyici_id` dizini (v6.173).

Cryo Haritası (`/cryo`) her dolu tüp için "kaç örnek var" ve "yumurta mı
embriyo mu" alt sorgularını `olay.vit_tasiyici_id` üzerinden soruyor
(`app.icerik_sql()`). Kolonun dizini yoktu: tüp başına bütün `olay` tablosu
taranıyordu. Programın kendi girdiği birkaç yüz tüpte fark edilmiyordu;
2019-2026 Access kayıtları aktarılınca (5.000'den fazla tüp, 137.000 olay
satırı) ekran test veritabanında bir dakikada açılmadı, dizinle 0,04 sn
(ölçüldü, v6.173). Çözmenin tüpü (`thaw_tasiyici_id`) goc_046'dan beri
dizinli, dondurmanın tüpü unutulmuştu.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_049.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("CREATE INDEX IF NOT EXISTS idx_olay_vit_tasiyici ON olay(vit_tasiyici_id)")
b.commit()
b.close()
print("olay(vit_tasiyici_id) dizini hazır.")
