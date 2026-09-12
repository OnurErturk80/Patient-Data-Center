"""Göç 022 — arşiv dosya adlarına hasta dosya numarası eklenir.

Eski ad:  2026-0001-03_gun5_20260906-224440.jpg
Yeni ad:  527078-2026-0001-03_gun5_20260906-224440.jpg
          └ hasta dosya no

Böylece dosya adı tek başına kendini tanımlar: hangi hasta, hangi cycle, kaçıncı
örnek, hangi aşama, ne zaman. Dosya klasöründen çıkarılıp bir yere kopyalansa
bile kimliği kaybolmaz. Kaynak resmin adı (`oocyte2.jpg`) hiçbir yerde
kullanılmıyor — o yalnızca `goruntu.orijinal_dosya_adi` alanında iz olarak
duruyor.

Örneğe bağlı olmayan (cycle arşivi) fotoğraflarda kök `cycle1` yerine
`527078-2026-0001` olur.

Dosyaları yeniden adlandırır **ve** veritabanındaki yolları günceller.
Dosya bulunamazsa kayda dokunmaz, bildirir. Birden fazla çalıştırılabilir.

Kullanım:  python goc_022.py      (Mac'te: python3 goc_022.py)
"""

import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

import db                       # noqa: E402  (lab.db kontrolunden sonra)
import goruntuler               # noqa: E402

kayitlar = db.sorgu(
    "SELECT g.id, g.cycle_id, g.specimen_id, g.dosya_yolu, c.cycle_no "
    "FROM goruntu g JOIN cycle c ON c.id = g.cycle_id ORDER BY g.id")

degisen = zaten = eksik = atlanan = 0
eksik_liste = []

for g in kayitlar:
    eski_yol = Path(g["dosya_yolu"])
    ad = eski_yol.name
    kok, ayrac, kalan = ad.partition("_")
    if not ayrac:
        atlanan += 1
        print(f"  ATLANDI  goruntu {g['id']}: beklenmedik ad bicimi '{ad}'")
        continue

    yeni_kok = goruntuler.ornek_kodu(
        g["cycle_id"], g["specimen_id"], g["cycle_no"])

    if kok == yeni_kok:
        zaten += 1
        continue

    simdiki = goruntuler.tam_yol(g["dosya_yolu"])
    yeni_ad = f"{yeni_kok}_{kalan}"
    hedef = simdiki.parent / yeni_ad

    if not simdiki.is_file():
        if hedef.is_file():
            db.yaz("UPDATE goruntu SET dosya_yolu = ? WHERE id = ?",
                   (goruntuler.goreli_yap(hedef), g["id"]))
            degisen += 1
            print(f"  YOL DUZELTILDI  goruntu {g['id']}: {yeni_ad}")
        else:
            eksik += 1
            eksik_liste.append((g["id"], g["dosya_yolu"]))
        continue

    if hedef.exists():                       # ayni adli baska dosya
        sayac = 1
        while hedef.exists():
            hedef = simdiki.parent / f"{yeni_kok}_{Path(kalan).stem}-{sayac}{simdiki.suffix}"
            sayac += 1

    simdiki.rename(hedef)
    db.yaz("UPDATE goruntu SET dosya_yolu = ? WHERE id = ?",
           (goruntuler.goreli_yap(hedef), g["id"]))
    degisen += 1
    print(f"  {ad}  ->  {hedef.name}")

print(f"\n{degisen} yeniden adlandirildi, {zaten} zaten dogru, "
      f"{eksik} dosya bulunamadi, {atlanan} atlandi")

if eksik_liste:
    print("\nDOSYASI BULUNAMAYAN KAYITLAR (veritabani kaydina dokunulmadi):")
    for gid, yol in eksik_liste:
        print(f"  goruntu {gid}: {yol}")

print("\nGuncel arsiv:")
ARSIV = goruntuler.arsiv_klasor()
if ARSIV.is_dir():
    for p in sorted(ARSIV.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(ARSIV).as_posix()}")

print("\nGoc 022 tamam.")
