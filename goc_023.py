"""Göç 023 — WAL journal modu (eş zamanlı kullanım).

Varsayılan `delete` modunda biri kayıt yazarken **okuyanlar da bekler**.
Klinikte birkaç telefon aynı anda ekran yenilerken bu gözle görülür yavaşlama
demek. WAL modunda okuyanlar yazana hiç takılmaz.

Ayar veritabanı dosyasında kalıcıdır — bir kez yazılır, öyle kalır. `db.py`
açılışta da garantiler; bu göç yeni bir makinede (Windows mini PC) elle
çalıştırılmasa da kalmasın diye var.

**Ağ sürücüsünde WAL desteklenmez.** SQLite sessizce eski moda döner, hata
vermez. `lab.db` bu yüzden yerel diskte kalmalı (README v6.6).

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_023.py      (Mac'te: python3 goc_023.py)
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)

onceki = b.execute("PRAGMA journal_mode").fetchone()[0]
if onceki.lower() == "wal":
    print("journal_mode zaten WAL.")
else:
    sonra = b.execute("PRAGMA journal_mode = WAL").fetchone()[0]
    if sonra.lower() == "wal":
        print(f"journal_mode: {onceki} -> WAL")
    else:
        print(f"UYARI: WAL'a gecilemedi, mod '{sonra}' olarak kaldi.")
        print("  Veritabani ag surucusunde olabilir — yerel diske alinmali.")

print(f"busy_timeout: {b.execute('PRAGMA busy_timeout').fetchone()[0]} ms "
      f"(uygulama baglantilarinda {15000} ms)")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("Goc 023 tamam.")
