"""Tüm göç scriptlerini sırayla çalıştırır.

Göçler birden fazla kez çalıştırılabilir olacak şekilde yazıldı; zaten
uygulanmış olanlar "zaten var" deyip geçer. Bu yüzden kod güncellendiğinde
veya başka bir makineden veritabanı getirildiğinde bunu çalıştırmak
en güvenli yoldur.

Kullanım:  python goc_hepsi.py      (Mac'te: python3 goc_hepsi.py)
"""

import re
import subprocess
import sys
from pathlib import Path

import db as _db

# Göç betikleri kodun yanında, `lab.db` veri klasöründe -- ikisi ayrı
# (bkz. db.py "iki kök"). Aynı sanılırsa paketlenmiş kurulumda kod
# klasöründe bomboş bir veritabanı açılırdı.
KOK = _db.PROGRAM_KOK
if not _db.DB_YOLU.exists():
    sys.exit("lab.db bulunamadi. Bu scripti app klasorunde calistir.")

gocler = sorted(
    (p for p in KOK.glob("goc_*.py") if re.match(r"goc_\d+\.py$", p.name)),
    key=lambda p: int(re.search(r"\d+", p.name).group()))

if not gocler:
    sys.exit("Goc scripti bulunamadi.")

print(f"{len(gocler)} goc scripti bulundu.\n")
basarili, hatali, atlanan = [], [], []

for g in gocler:
    metin = g.read_text(encoding="utf-8", errors="ignore")
    if "input(" in metin:
        atlanan.append(g.name)
        print(f"  ATLANDI  {g.name}  (soru soruyor, elle calistirilmali)")
        continue

    sonuc = subprocess.run([sys.executable, str(g)], cwd=KOK,
                           capture_output=True, text=True)
    if sonuc.returncode == 0:
        basarili.append(g.name)
        son = [x for x in sonuc.stdout.strip().splitlines() if x.strip()]
        ozet = son[-1] if son else ""
        print(f"  OK       {g.name}  {ozet[:48]}")
    else:
        hatali.append((g.name, (sonuc.stderr or sonuc.stdout).strip()))
        print(f"  HATA     {g.name}")

print(f"\n{len(basarili)} basarili, {len(hatali)} hatali, {len(atlanan)} atlandi")

if hatali:
    print("\nHATALAR")
    print("=" * 60)
    for ad, mesaj in hatali:
        print(f"\n{ad}:")
        print("  " + "\n  ".join(mesaj.splitlines()[-6:]))

if atlanan:
    print("\nELLE CALISTIRILMASI GEREKENLER")
    for ad in atlanan:
        print(f"  python goc_{ad.split('_')[1]}")

# Son kontrol
import sqlite3
b = sqlite3.connect(_db.DB_YOLU)
kirik = b.execute("PRAGMA foreign_key_check").fetchall()
tablo = b.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
print(f"\nVeritabani: {tablo} tablo, {len(kirik)} kirik referans")
b.close()
