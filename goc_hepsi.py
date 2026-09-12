"""Bekleyen göçleri çalıştırır (terminalden).

Program **açılışta bunu kendisi yapıyor** (v6.49); bu script artık yalnızca
elle kontrol etmek, çıktıyı ayrıntılı görmek ya da sunucuyu başlatmadan
veritabanını güncellemek için.

Çalıştırıcı tek yerde: `goc.calistir()`. Burada ikinci bir kopya yok --
eskiden bu script göçleri `subprocess.run([sys.executable, ...])` ile
çalıştırıyordu, paketlenmiş uygulamada o satır göçü değil **programı**
yeniden başlatırdı (bkz. goc.py).

Kullanım:  python goc_hepsi.py      (Mac'te: python3 goc_hepsi.py)
"""

import sqlite3
import sys

import db
import goc

if not db.DB_YOLU.exists():
    sys.exit(f"lab.db bulunamadi: {db.DB_YOLU}")

print(f"Veritabani: {db.DB_YOLU}")
bekleyen = goc.bekleyenler()
print(f"{len(goc.gocler())} goc var, {len(bekleyen)} tanesi bekliyor.\n")

sonuc = goc.calistir()

if sonuc["atlandi"] == "baska-surec":
    sys.exit("Baska bir surec gocleri calistiriyor. Birkac saniye sonra dene.")

for ad in sonuc["calisti"]:
    print(f"  OK    {ad}")
if not sonuc["calisti"]:
    print("  (uygulanacak yeni goc yok)")

if sonuc["hatali"]:
    print("\nHATALAR")
    print("=" * 60)
    for ad, mesaj in sonuc["hatali"]:
        print(f"\n{ad}:")
        print("  " + "\n  ".join(str(mesaj).splitlines()[-8:]))

if sonuc["elle"]:
    print("\nELLE CALISTIRILMASI GEREKENLER")
    for ad in sonuc["elle"]:
        print(f"  python {ad}.py")

# Son kontrol
b = sqlite3.connect(db.DB_YOLU)
kirik = b.execute("PRAGMA foreign_key_check").fetchall()
tablo = b.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
b.close()
print(f"\nVeritabani: {tablo} tablo, {len(kirik)} kirik referans")

if sonuc["hatali"]:
    sys.exit(1)
