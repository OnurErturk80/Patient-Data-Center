"""Göç 045 — Hastaya eşin dosya numarası alanı.

Kullanıcının isteği (2026-09-22): "Hasta kartında Eşin dosya numarasının
girilebileceği yer olsun. Eğer Eş erkek olarak sperm dondurma kaydı daha önce
yapıldıysa uyarı versin."

Bu, v6.125'in bilerek açık bıraktığı boşluğu kapatıyor. Orada eşleştirme
**yalnızca dosya numarasıyla** yapılıyordu ve şu durum kapsam dışıydı:
erkek hasta kendi AYRI dosya numarasıyla kayıtlıysa (onkoloji öncesi sperm
dondurma gibi, çiftin dosyasından bağımsız) hiçbir uyarı çıkmıyordu. Artık
çiftin kaydına erkeğin dosya numarası yazılabiliyor ve bağ kesinleşiyor.

`es_dosya_no` **FK DEĞİL, düz bir sayı**: eş henüz kayıtlı olmayabilir
(numara önce yazılır, hasta sonra açılır) ve `hasta.dosya_no` üzerinde
FK kurulabilecek bir UNIQUE indeks lab_id ile birlikte tanımlı
(`UNIQUE (lab_id, dosya_no)`), tek kolona FK verilemezdi. Okuma her zaman
`dosya_no_sahibi()` üzerinden, yani "kayıtlı mı" sorusu her seferinde
yeniden soruluyor -- CLAUDE.md'nin "türetilmiş, sayaç tutma" gerekçesinin
aynısı.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_045.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(hasta)")]

if "es_dosya_no" not in kolonlar:
    b.execute("ALTER TABLE hasta ADD COLUMN es_dosya_no INTEGER")
    print("hasta.es_dosya_no eklendi.")
else:
    print("hasta.es_dosya_no zaten var.")

b.commit()
b.close()
print("\nGoc 045 tamam.")
