"""Göç 030 — şifre değişikliği için yönetici onayı.

Kullanıcının kararı (2026-09-12): personel kendi şifresini değiştirebilsin
ama **yönetici onaylayınca** geçerli olsun. Sebebi klinik: ortak kullanılan
telefonlarda şifreyi değiştiren kişi ötekileri farkında olmadan dışarıda
bırakıyor; yönetici haberdar olsun.

Tek tablo:

  `sifre_istegi`
    kullanici_id   şifresini değiştirmek isteyen
    yeni_hash      YENİ şifrenin hash'i — düz metin HİÇBİR YERDE durmuyor
    durum          'bekliyor' | 'onaylandi' | 'reddedildi'
    karar_veren_id onaylayan/reddeden yönetici
    karar_zamani   kararın zamanı

**Neden hash bekletiliyor, şifre onay anında mı sorulsun?** Kullanıcı isteği
gönderirken kimliğini **mevcut şifresiyle** kanıtlıyor (`/sifre` kuralı
değişmedi). Onay anında o kişi orada olmayabilir; yeni şifreyi ikinci kez
sormak "onay" akışını iki kişinin aynı anda orada olmasına bağlardı. Hash
onaylanana kadar hiçbir girişte kullanılmıyor, yani kimlik bilgisi değil.

**Yöneticinin kendi şifresi onay beklemez** — tek yönetici kendi isteğini
onaylamak için giriş yapamaz duruma düşerdi (kilitlenme koruması, README
v6.11'deki kuralın aynısı).

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_030.py      (Mac'te: python3 goc_030.py)
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

var = b.execute("SELECT name FROM sqlite_master WHERE type='table' "
                "AND name='sifre_istegi'").fetchone()
if var:
    print("sifre_istegi zaten var.")
else:
    b.execute("""
        CREATE TABLE sifre_istegi (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id           INTEGER NOT NULL REFERENCES lab(id),
            kullanici_id     INTEGER NOT NULL REFERENCES kullanici(id),
            yeni_hash        TEXT NOT NULL,
            durum            TEXT NOT NULL DEFAULT 'bekliyor',
            karar_veren_id   INTEGER REFERENCES kullanici(id),
            karar_zamani     TEXT,
            olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    b.commit()
    print("  + sifre_istegi")

# Bir kullanicinin AYNI ANDA tek bekleyen istegi olur: ikinci istek birinciyi
# degistiriyor (app.py once bekleyenleri siliyor). Indeks o silmeyi ve onay
# ekranindaki listeyi hizlandiriyor.
b.execute("CREATE INDEX IF NOT EXISTS ix_sifre_istegi "
          "ON sifre_istegi(lab_id, durum, kullanici_id)")
b.commit()
print("  + ix_sifre_istegi")

n = b.execute("SELECT COUNT(*) FROM sifre_istegi WHERE durum='bekliyor'") \
     .fetchone()[0]
print(f"\nBekleyen sifre istegi: {n}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 030 tamam.")
