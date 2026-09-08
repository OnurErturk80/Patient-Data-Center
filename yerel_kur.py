"""Bu makinenin klasör ayarlarını gösterir ve gerekirse değiştirir.

Normalde çalıştırmana gerek yok: uygulama bu makine için bir bölüm bulamazsa
kendi varsayılanlarını (uygulama klasörünün altındaki snapshot/ ve arsiv/)
oluşturur. Bu script yalnızca yolları başka bir yere almak istediğinde gerekir.

yerel_ayar.json makine adına göre bölümlenir; klasörün tamamı iki bilgisayar
arasında taşınsa bile her makine kendi bölümünü kullanır.

Kullanım:  python yerel_kur.py      (Mac'te: python3 yerel_kur.py)
"""

import json
import platform
import sys
from pathlib import Path

import db

KOK = Path(__file__).parent
HEDEF = KOK / "yerel_ayar.json"

print(f"Makine: {db.MAKINE}   ({platform.system()})")
print("=" * 58)

mevcut = db.yerel_ayarlar()          # yoksa oluşturur, eksikleri tamamlar
print("\nBu makinenin ayarlari:")
for k in db.YOL_ANAHTARLARI:
    yol = Path(mevcut.get(k, ""))
    isaret = "var" if yol.exists() else "yok"
    print(f"  {k:24} {mevcut.get(k)}   [{isaret}]")

try:
    tum = json.loads(HEDEF.read_text(encoding="utf-8"))
except Exception:
    tum = {}
digerleri = [m for m in tum if m != db.MAKINE]
if digerleri:
    print(f"\nDosyada baska makineler de var: {', '.join(digerleri)}")
    print("Onlara dokunulmaz.")

print("\nDegistirmek istedigin var mi? (e/h) ", end="")
if input().strip().lower() not in ("e", "evet"):
    sys.exit("Degisiklik yapilmadi.")

bolum = dict(mevcut)
for k in db.YOL_ANAHTARLARI:
    print(f"\n{k}")
    print(f"  su an: {bolum.get(k)}")
    yeni = input("  yeni deger (bos = degistirme): ").strip()
    if yeni:
        bolum[k] = yeni

tum[db.MAKINE] = bolum
HEDEF.write_text(json.dumps(tum, indent=2, ensure_ascii=False), encoding="utf-8")

for k in ("goruntu_kaynak_klasor", "goruntu_arsiv_klasor"):
    try:
        Path(bolum[k]).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"  UYARI: {bolum[k]} olusturulamadi: {e}")

print(f"\n{HEDEF.name} guncellendi:")
for k in db.YOL_ANAHTARLARI:
    print(f"  {k:24} {bolum[k]}")
