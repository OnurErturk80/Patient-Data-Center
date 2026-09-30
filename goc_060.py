"""Göç 060 — Hekim alanının varsayılanı (v6.231).

Kullanıcının isteği (2026-09-30): "Hekim ismi yazılan her yerde sabit Mete
Çağlar olsun. Hep onu göstersin. Farklı birini istersek açılır menüden diğer
seçip elle yazabilelim."

Programda hekim adı yalnızca OPU ekranında giriliyor (`cycle.opu_hekim`,
goc_025); resmî formların "OPU KLİNİSYEN" ve "Hekimler: OPU" kutuları oradan
basılıyor. OPU ekranı artık açılır menüyle açılıyor: varsayılan hekim seçili,
"Diğer" seçilince ad elle yazılıyor (`db.hekim_secimi()`).

Ad laboratuvarın, kodun değil: `ayarlar` tablosunda `varsayilan_hekim`. Bu göç
anahtar YOKSA yazıyor (INSERT OR IGNORE). v6.231'den sonra kurulan veritabanında
anahtar kurulumla boş geliyor (`kurulum.ayarlar()`), bu göç ona dokunmuyor --
başka bir laboratuvarın yeni kurulumuna bu laboratuvarın hekimi girmesin.

Var olan kayıtlara dokunmuyor: eski kayıtların hekim adları (Access'ten
gelenler dahil) olduğu gibi kalıyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_060.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

HEKIM = "Mete Çağlar"

b = sqlite3.connect(DB)
eklendi = b.execute(
    "INSERT OR IGNORE INTO ayarlar (lab_id, anahtar, deger, aciklama) "
    "VALUES (1, 'varsayilan_hekim', ?, ?)",
    (HEKIM, "Hekim alaninin varsayilani (v6.231)")).rowcount
b.commit()
deger = b.execute("SELECT deger FROM ayarlar WHERE lab_id=1 "
                  "AND anahtar='varsayilan_hekim'").fetchone()
b.close()
if eklendi:
    print(f"varsayilan_hekim yazildi: {HEKIM}")
else:
    print(f"varsayilan_hekim zaten var: {deger[0] if deger and deger[0] else '(bos)'}")
