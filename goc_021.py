"""Göç 021 — arşiv klasörü hasta dosya numarasına göre yeniden düzenlenir.

Eski yapı:  arsiv/<yıl>/<cycle no>/<dosya>
Yeni yapı:  arsiv/<hasta dosya no>/<cycle no>/<dosya>

Yıl zaten cycle numarasının içinde (`2026-0001`), bilgi kaybı yok. Böylece
Finder / Dosya Gezgini'nde bir hastanın bütün görüntüleri tek klasörde
toplanır.

Hasta **adı** klasör adına konmadı — bilerek: macOS Unicode'u ayrıştırılmış
(NFD), Windows birleştirilmiş (NFC) saklar, klasör USB ile taşınınca Türkçe
harfli yollar eşleşmeyebilir; ayrıca hasta adı değişebilir. Dosya no saf
rakam, iki sistemde de güvenli.

Dosyaları taşır **ve** veritabanındaki yolları günceller. Dosya bulunamazsa
kayda dokunmaz, sadece bildirir.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_021.py      (Mac'te: python3 goc_021.py)
"""

import shutil
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

import db                       # noqa: E402  (lab.db kontrolunden sonra)
import goruntuler               # noqa: E402

ARSIV = goruntuler.arsiv_klasor()
print(f"Arsiv klasoru: {ARSIV}")

kayitlar = db.sorgu(
    "SELECT g.id, g.cycle_id, g.dosya_yolu, c.cycle_no "
    "FROM goruntu g JOIN cycle c ON c.id = g.cycle_id ORDER BY g.id")

tasinan = zaten = eksik = 0
eksik_liste = []

for g in kayitlar:
    yeni_goreli = "/".join([
        goruntuler.hasta_klasoru(g["cycle_id"]),
        goruntuler.guvenli_ad(g["cycle_no"]),
        Path(g["dosya_yolu"]).name,
    ])

    if g["dosya_yolu"] == yeni_goreli:
        zaten += 1
        continue

    simdiki = goruntuler.tam_yol(g["dosya_yolu"])
    hedef = ARSIV / yeni_goreli

    if not simdiki.is_file():
        if hedef.is_file():
            # Dosya yeni yerinde ama kayit eski yolu gosteriyor — yolu duzelt
            db.yaz("UPDATE goruntu SET dosya_yolu = ? WHERE id = ?",
                   (yeni_goreli, g["id"]))
            tasinan += 1
            print(f"  YOL DUZELTILDI  goruntu {g['id']}: {yeni_goreli}")
        else:
            eksik += 1
            eksik_liste.append((g["id"], g["dosya_yolu"]))
        continue

    hedef.parent.mkdir(parents=True, exist_ok=True)
    if hedef.exists():                       # ayni adli baska dosya
        sayac = 1
        while hedef.exists():
            hedef = hedef.parent / f"{hedef.stem}-{sayac}{hedef.suffix}"
            sayac += 1
        yeni_goreli = goruntuler.goreli_yap(hedef)

    shutil.move(str(simdiki), str(hedef))
    db.yaz("UPDATE goruntu SET dosya_yolu = ? WHERE id = ?",
           (yeni_goreli, g["id"]))
    tasinan += 1
    print(f"  TASINDI  {g['dosya_yolu']}  ->  {yeni_goreli}")

# Bosalan eski klasorleri temizle (icinde dosya kalmayanlar)
silinen_klasor = 0
if ARSIV.is_dir():
    for p in sorted(ARSIV.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            try:
                p.rmdir()
                silinen_klasor += 1
            except OSError:
                pass

print(f"\n{tasinan} tasindi, {zaten} zaten dogru yerde, {eksik} dosya bulunamadi")
if silinen_klasor:
    print(f"{silinen_klasor} bos klasor kaldirildi")

if eksik_liste:
    print("\nDOSYASI BULUNAMAYAN KAYITLAR (veritabani kaydina dokunulmadi):")
    for gid, yol in eksik_liste:
        print(f"  goruntu {gid}: {yol}")
    print("Bu dosyalar arsivden silinmis olabilir; yedekten geri alinabilir.")

print("\nGuncel arsiv yapisi:")
if ARSIV.is_dir():
    for hasta in sorted(p for p in ARSIV.iterdir() if p.is_dir()):
        adet = sum(1 for _ in hasta.rglob("*") if _.is_file())
        cycleler = sorted(p.name for p in hasta.iterdir() if p.is_dir())
        print(f"  {hasta.name}/  {adet} dosya  ({', '.join(cycleler)})")

print("\nGoc 021 tamam.")
