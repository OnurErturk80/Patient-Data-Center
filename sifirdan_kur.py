"""Sıfırdan güncel bir veritabanı kurar.

Yeni bir makinede (veya temiz bir test veritabanı için) tek komutla:
  - şemayı oluşturur ve seçim listeleri ile varsayılan ayarları doldurur
  - bir kullanıcı oluşturur ve şifresini sorar
  - bu makineye uygun klasör ayarlarını yazar
  - **göçleri çalıştırır** — `sema_guncel.sql` göçlerin gerisinde kalabiliyor,
    kuran kişinin `goc_hepsi.py`'yi hatırlamasına güvenilmiyor (README v6.9)

Mevcut lab.db varsa DOKUNMAZ — önce yeniden adlandırman gerekir.

Kullanım:  python sifirdan_kur.py      (Mac'te: python3 sifirdan_kur.py)
"""

import getpass
import json
import platform
import sqlite3
import subprocess
import sys
from pathlib import Path

import db

# Kod ve veri ayrı köklerde (bkz. db.py). Şema dosyası ve göç betikleri
# kodun yanında; veritabanı, ayar dosyası ve arşiv veri klasöründe.
KOK = db.VERI_KOK
PROGRAM = db.PROGRAM_KOK
DB = db.DB_YOLU
SEMA = PROGRAM / "sema_guncel.sql"

if DB.exists():
    sys.exit(
        f"lab.db zaten var: {DB}\n"
        "Uzerine yazmamak icin durduruldu. Yeni bir tane istiyorsan once\n"
        "mevcut dosyayi yeniden adlandir (ornek: lab_eski.db)."
    )
if not SEMA.exists():
    sys.exit(f"sema_guncel.sql bulunamadi: {SEMA}")

# Şema, laboratuvar satırı, seçim listeleri ve varsayılan ayarlar tek yerde
# (v6.204): ilk açılış ekranı (`/kurulum`) da aynısını kuruyor.
import kurulum

b = sqlite3.connect(DB)
kurulum.sema_kur(b)
b.commit()
tablo = b.execute(
    "SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
n = b.execute("SELECT COUNT(*) FROM liste_degeri").fetchone()[0]
b.close()
print(f"Sema olusturuldu: {tablo} tablo")
print(f"Secim listeleri: {n} deger, {len(kurulum.LISTELER)} liste")
print(f"Ayarlar: {len(kurulum.ayarlar())} kayit")

# ------------------------------------------------------------------ kullanici
import db as _db
import guvenlik

print("\nBir kullanici olusturalim.")
ad = input("  Ad soyad      : ").strip() or "Kullanici"
kod = (input("  Kisa kod (ON) : ").strip() or ad[:2]).upper()
kadi = (input("  Kullanici adi : ").strip() or "onur").lower()
while True:
    s1 = getpass.getpass("  Sifre (min 8) : ")
    s2 = getpass.getpass("  Tekrar        : ")
    if s1 != s2:
        print("  Sifreler ayni degil, tekrar dene.")
    elif len(s1) < 8:
        print("  En az 8 karakter olmali.")
    else:
        break

_db.yaz("INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, kullanici_adi, "
        "sifre_hash) VALUES (1,?,?,'embriyolog',?,?)",
        (ad, kod, kadi, guvenlik.sifrele(s1)))
print(f"Kullanici olusturuldu: {kadi}")

# ------------------------------------------------------------------ yerel yol
sistem = platform.system()
ev = Path.home()
if sistem == "Windows":
    yerel = {"goruntu_kaynak_klasor": str(ev / "Desktop" / "snapshot"),
             "goruntu_arsiv_klasor": str(KOK / "arsiv"),
             "yedek_klasor": "D:\\lab_yedek"}
else:
    yerel = {"goruntu_kaynak_klasor": str(ev / "Desktop" / "snapshot"),
             "goruntu_arsiv_klasor": str(KOK / "arsiv"),
             "yedek_klasor": str(ev / "lab_yedek")}

hedef = db.YEREL_DOSYA
if not hedef.exists():
    hedef.write_text(json.dumps(yerel, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nyerel_ayar.json yazildi ({sistem}):")
    for k, v in yerel.items():
        print(f"  {k:24s} = {v}")
    print("Yollar yanlissa dosyayi metin editoruyle duzelt.")

# ------------------------------------------------------------------- gocler
# `sema_guncel.sql` gocler kadar hizli guncellenmiyor: yeni bir kolonu ya da
# secim listesini yalnizca goc dosyasi getiriyor olabilir. Kuran kisinin
# `goc_hepsi.py`'yi ayrica calistirmayi hatirlamasina guvenmek bir kez
# tutmadi -- androloji ekraninda renk ve aglutinasyon secenekleri bos geldi,
# sebebi ekrandan anlasilmiyordu (README v6.9, tuzak #3). Gocler idempotent,
# tekrar calismalarinin zarari yok; bu yuzden kurulumun parcasi.
print("\nGocler calistiriliyor...")
komut = "python" if sistem == "Windows" else "python3"
sonuc = subprocess.run([sys.executable, str(PROGRAM / "goc_hepsi.py")],
                       capture_output=True, text=True)
son_satirlar = [x for x in sonuc.stdout.strip().splitlines() if x.strip()]
for satir in son_satirlar[-6:]:
    print("  " + satir)
if sonuc.returncode != 0:
    print("\n  UYARI: gocler tamamlanamadi. Elle calistir:")
    print(f"    {komut} goc_hepsi.py")
    if sonuc.stderr.strip():
        print("  " + sonuc.stderr.strip().splitlines()[-1])

# Yeni kurulum ağa kapalı başlıyor (v6.203, kullanıcının kararı: "yeni bir
# bilgisayara kurulunca kapalı başlasın, ben açarım"). Ayar bu makineye özel.
if db.ag_erisimi_yaz(db.AG_YEREL):
    print("\nAg erisimi KAPALI: program yalnizca bu bilgisayardan acilir.")
    print("  Telefonlar icin: Yonetici -> Ag erisimi -> Ic aga acik")

print("\nKurulum tamam. Baslatmak icin:")
print(f"  {komut} -m uvicorn app:uygulama --host 0.0.0.0 --port 8000")
