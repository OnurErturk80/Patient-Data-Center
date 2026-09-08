"""Snapshot klasörü neden okunmuyor — teşhis.

Kullanım:  python teshis.py
"""

import sqlite3
from pathlib import Path

KOK = Path(__file__).parent
DB = KOK / "lab.db"

print("=" * 60)
print("1. DOSYALAR")
print("=" * 60)
for ad in ["app.py", "db.py", "guvenlik.py", "goruntuler.py",
           "goc_002.py", "goc_003.py", "lab.db"]:
    print(f"   {'VAR ' if (KOK / ad).exists() else 'YOK!'}  {ad}")
for ad in ["templates", "static"]:
    print(f"   {'VAR ' if (KOK / ad).is_dir() else 'YOK!'}  {ad}/")
print(f"   templates/denudasyon.html: "
      f"{'VAR' if (KOK / 'templates' / 'denudasyon.html').exists() else 'YOK!'}")

if not DB.exists():
    raise SystemExit("\nlab.db bulunamadi — bu klasorde calistirilmali.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

print()
print("=" * 60)
print("2. VERITABANI")
print("=" * 60)
tablolar = [r[0] for r in b.execute(
    "SELECT name FROM sqlite_master WHERE type='table'")]
for t in ["kaynak_dosya", "oturum"]:
    print(f"   {'VAR ' if t in tablolar else 'YOK!'}  tablo: {t}")
if "kaynak_dosya" not in tablolar:
    print("   -> goc_003.py calistirilmamis. Once onu calistir.")

kolonlar = [r[1] for r in b.execute("PRAGMA table_info(goruntu)")]
print(f"   {'VAR ' if 'kaynak_imza' in kolonlar else 'YOK!'}  goruntu.kaynak_imza")

print()
print("=" * 60)
print("3. KLASOR AYARI")
print("=" * 60)
r = b.execute("SELECT deger FROM ayarlar WHERE anahtar='goruntu_kaynak_klasor'").fetchone()
if not r:
    raise SystemExit("   Ayar yok. goc_003.py calistirilmali.")

yol = Path(r["deger"])
print(f"   Ayarli yol : {r['deger']}")
print(f"   Klasor var mi: {'EVET' if yol.is_dir() else 'HAYIR — yol yanlis!'}")

if not yol.is_dir():
    raise SystemExit(
        "\n   Bu klasor bulunamadi. Windows Gezgini'nde snapshot klasorunu ac,\n"
        "   adres cubugundaki yolu kopyala ve goc_003.py icindeki\n"
        "   goruntu_kaynak_klasor degerini duzelt, sonra goc_003.py'yi calistir."
    )

UZANTILAR = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
tum = [p for p in yol.iterdir() if p.is_file()]
gecerli = [p for p in tum if p.suffix.lower() in UZANTILAR]
gecersiz = [p for p in tum if p.suffix.lower() not in UZANTILAR]

print(f"   Klasordeki dosya sayisi : {len(tum)}")
print(f"   Gorunta olarak tanindi  : {len(gecerli)}")
if gecersiz:
    print(f"   TANINMAYAN uzantilar    : {len(gecersiz)}")
    for p in gecersiz[:5]:
        print(f"      {p.name}  (uzanti: {p.suffix or 'yok'})")
    print("   -> Desteklenen: .jpg .jpeg .png .tif .tiff .bmp .webp")

print()
print("=" * 60)
print("4. KUYRUK")
print("=" * 60)
islenmis = {r["imza"] for r in b.execute("SELECT imza FROM kaynak_dosya")}
bekleyen = []
for p in gecerli:
    s = p.stat()
    im = f"{p.name}|{int(s.st_mtime)}|{s.st_size}"
    if im not in islenmis:
        bekleyen.append(p)

print(f"   Daha once islenmis : {len(islenmis)}")
print(f"   BEKLEYEN           : {len(bekleyen)}")
for p in sorted(bekleyen, key=lambda x: x.stat().st_mtime)[:10]:
    print(f"      {p.name}")

if gecerli and not bekleyen:
    print("\n   Tum goruntuler daha once islenmis gorunuyor.")
    print("   Kuyrugu sifirlamak icin (DIKKAT: eslesmeler de silinir):")
    print("      python -c \"import db; db.yaz('DELETE FROM kaynak_dosya')\"")

print()
print("=" * 60)
print("5. SONUC")
print("=" * 60)
if bekleyen:
    print(f"   {len(bekleyen)} goruntu hazir. Denudasyon ekranini acip")
    print("   sayfayi YENILE — ekran kendiliginden guncellenmez.")
else:
    print("   Bekleyen goruntu yok. Yukaridaki adimlara bak.")

b.close()
