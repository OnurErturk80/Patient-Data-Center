"""Göç 002 — oturum tablosu ekler ve kullanıcı şifresi belirler.

Mevcut lab.db üzerinde çalışır, veriye dokunmaz.
Birden fazla kez çalıştırılabilir.

Kullanım:
    python goc_002.py
"""

import getpass
import sqlite3
import sys
from pathlib import Path

import db
import guvenlik

DB = Path(__file__).parent / "lab.db"

if not DB.exists():
    sys.exit("lab.db bulunamadi. Once kur.py calistirilmali.")

b = sqlite3.connect(DB)

# --- oturum tablosu ---
b.execute("""
CREATE TABLE IF NOT EXISTS oturum (
    jeton        TEXT PRIMARY KEY,
    kullanici_id INTEGER NOT NULL REFERENCES kullanici(id),
    olusturma    TEXT NOT NULL,
    son_erisim   TEXT NOT NULL
)""")
b.execute("CREATE INDEX IF NOT EXISTS idx_oturum_kullanici ON oturum(kullanici_id)")
b.commit()
print("oturum tablosu hazir.")

# --- kullanıcı adlarını küçük harfe çevir (giriş büyük/küçük duyarsız olsun) ---
b.execute("UPDATE kullanici SET kullanici_adi = LOWER(kullanici_adi)")
b.commit()

kullanicilar = b.execute(
    "SELECT id, ad_soyad, kullanici_adi, sifre_hash FROM kullanici ORDER BY id"
).fetchall()
b.close()

print("\nKayitli kullanicilar:")
for k in kullanicilar:
    durum = "sifre YOK" if not k[3].startswith("scrypt$") else "sifre var"
    print(f"  {k[0]}. {k[1]}  (kullanici adi: {k[2]})  — {durum}")

print("\nSifre belirlemek istedigin kullanicinin numarasini yaz (bos birak = cik):")
secim = input("> ").strip()
if not secim:
    sys.exit("Degisiklik yapilmadi.")

kid = int(secim)
s1 = getpass.getpass("Yeni sifre: ")
s2 = getpass.getpass("Tekrar: ")

if s1 != s2:
    sys.exit("Sifreler ayni degil. Degisiklik yapilmadi.")
if len(s1) < 8:
    sys.exit("Sifre en az 8 karakter olmali. Degisiklik yapilmadi.")

db.yaz("UPDATE kullanici SET sifre_hash = ? WHERE id = ?", (guvenlik.sifrele(s1), kid))
db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (kid,))   # eski oturumları düşür
print("Sifre guncellendi. Bu kullanicinin acik oturumlari kapatildi.")
