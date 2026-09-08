"""Göç 009 — görüntü yollarını göreli hale getirir.

Tam yol saklandığında (C:\\Users\\... veya /Users/...) veritabanı başka bir
makineye taşındığında fotoğraflar bulunamaz. Bu göç mevcut kayıtları
arşiv klasörüne göre göreli yola çevirir: '2026/2026-0417/xxx.jpg'

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_009.py      (Mac'te: python3 goc_009.py)
"""

import sys
from pathlib import Path, PureWindowsPath

import db
import goruntuler

kayitlar = db.sorgu("SELECT id, dosya_yolu FROM goruntu")
if not kayitlar:
    print("Goruntu kaydi yok, yapilacak bir sey yok.")
    sys.exit()

arsiv = goruntuler.arsiv_klasor()
print(f"Arsiv klasoru: {arsiv}")
print(f"{len(kayitlar)} goruntu kaydi inceleniyor...\n")

cevrilen = zaten = bulunamayan = 0

for r in kayitlar:
    kayitli = r["dosya_yolu"]

    # Windows ve POSIX yollarini birlikte tanı
    p = PureWindowsPath(kayitli) if "\\" in kayitli else Path(kayitli)
    mutlak = p.is_absolute()

    if not mutlak:
        zaten += 1
        continue

    parcalar = [x.lower() for x in p.parts]
    if "arsiv" not in parcalar:
        print(f"  ATLANDI (arsiv klasoru yolda gecmiyor): {kayitli}")
        bulunamayan += 1
        continue

    i = len(parcalar) - 1 - parcalar[::-1].index("arsiv")
    goreli = "/".join(p.parts[i + 1:])
    db.yaz("UPDATE goruntu SET dosya_yolu = ? WHERE id = ?", (goreli, r["id"]))
    cevrilen += 1

print(f"\n{cevrilen} kayit goreli yola cevrildi")
print(f"{zaten} kayit zaten goreliydi")
if bulunamayan:
    print(f"{bulunamayan} kayit cevrilemedi (yukarida listelendi)")

# Dosyalar gercekten yerinde mi
eksik = []
for r in db.sorgu("SELECT id, dosya_yolu FROM goruntu"):
    if not goruntuler.tam_yol(r["dosya_yolu"]).is_file():
        eksik.append(r["dosya_yolu"])

print(f"\nDosya kontrolu: {len(kayitlar) - len(eksik)} / {len(kayitlar)} dosya yerinde")
if eksik:
    print("Bulunamayan dosyalar (arsiv klasoru tasinmamis olabilir):")
    for e in eksik[:10]:
        print(f"  {e}")
    if len(eksik) > 10:
        print(f"  ... ve {len(eksik) - 10} tane daha")

print("\nGoc 009 tamam.")
