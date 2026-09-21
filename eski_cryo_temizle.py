"""Eski cryo haritası içeri alma özelliğinden kalanları temizler.

Bu özellik (v6.127/v6.128) kullanıcının isteğiyle **geri alındı**. Kodu
geri almak veritabanını geri almıyor: `eski_cryo` tablosu, içeri alınan
kayıtlar ve o kayıtların açtığı `konum` satırları yerinde kalıyor.

Neden sadece durmalarına izin verilmiyor: `eski_cryo.hasta_id` `hasta(id)`
ye yabancı anahtarla bağlı. Kodun geri alınmış hali bu bağı temizlemeyi
bilmiyor, o yüzden **bağ kurulmuş bir hastayı kalıcı silmek FOREIGN KEY
hatası verir** ve `teshis_silme.py` de sebebini söyleyemez (o da geri
alındı). Ölçüldü, gerçekten böyle patlıyor.

**Kaynak Excel dosyana dokunulmuyor.** Silinen şey onun programa alınmış
kopyası; asıl harita hâlâ sende. Kaybolan tek şey, eski kayıtlarla hastalar
arasında elle kurduğun bağlar.

Kullanım:  python3 eski_cryo_temizle.py
           python3 eski_cryo_temizle.py liste     (yalnızca gösterir)
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)

DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

YALNIZCA_LISTE = len(sys.argv) > 1 and sys.argv[1] == "liste"

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row
b.execute("PRAGMA foreign_keys = ON")


def sayi(sql, par=()):
    try:
        return b.execute(sql, par).fetchone()[0]
    except sqlite3.OperationalError:
        return None


var = b.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                "AND name='eski_cryo'").fetchone()

print("=" * 62)
print("ESKI CRYO HARITASI - KALANLARIN TEMIZLENMESI")
print("=" * 62)
print(f"Veritabani: {DB}")

if not var:
    print("\n'eski_cryo' tablosu yok - temizlenecek bir sey bulunamadi.")
    b.close()
    sys.exit(0)

kayit = sayi("SELECT COUNT(*) FROM eski_cryo")
bagli = sayi("SELECT COUNT(*) FROM eski_cryo WHERE hasta_id IS NOT NULL")
# Yalnizca eski kayitlarin actigi, baska hicbir seyin kullanmadigi konumlar.
oksuz = sayi(
    "SELECT COUNT(*) FROM konum k WHERE k.lab_id=? "
    "AND NOT EXISTS (SELECT 1 FROM tasiyici t WHERE t.konum_id=k.id)",
    (_db.LAB_ID,))
goc = sayi("SELECT COUNT(*) FROM goc_kaydi WHERE ad='goc_042'")
# Iceri alma ile eklenen iki tasiyici tipi - yalnizca HIC KULLANILMAMISSA.
tipler = [r["kod"] for r in b.execute(
    "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_tipi' "
    "AND kod IN ('rapid_i','vitrifit')", (_db.LAB_ID,))]
tipler = [k for k in tipler if not b.execute(
    "SELECT 1 FROM tasiyici WHERE lab_id=? AND tip=?", (_db.LAB_ID, k)).fetchone()]

print(f"\nSilinecek:")
print(f"  eski_cryo kaydi           : {kayit}  (bunlarin {bagli} tanesi bir hastaya bagli)")
print(f"  taşiyicisi olmayan konum  : {oksuz}")
print(f"  goc_kaydi'ndaki goc_042   : {goc}")
print(f"  kullanilmamis tasiyici tipi: {', '.join(tipler) or 'yok'}")
print("\nKaynak Excel dosyana DOKUNULMUYOR. Kaybolan tek sey, eski")
print("kayitlarla hastalar arasinda elle kurdugun baglar.")

if YALNIZCA_LISTE:
    print("\n(liste kipi - hicbir sey degistirilmedi)")
    b.close()
    sys.exit(0)

print()
if input('Silmek icin SIL yazin: ').strip() != "SIL":
    print("Vazgecildi, hicbir sey degistirilmedi.")
    b.close()
    sys.exit(0)

try:
    b.execute("BEGIN IMMEDIATE")
    b.execute("DELETE FROM eski_cryo")
    b.execute("DROP TABLE eski_cryo")
    b.execute(
        "DELETE FROM konum WHERE lab_id=? "
        "AND NOT EXISTS (SELECT 1 FROM tasiyici t WHERE t.konum_id=konum.id)",
        (_db.LAB_ID,))
    b.execute("DELETE FROM goc_kaydi WHERE ad='goc_042'")
    for k in tipler:
        b.execute("DELETE FROM liste_degeri WHERE lab_id=? "
                  "AND liste_adi='tasiyici_tipi' AND kod=?", (_db.LAB_ID, k))
    b.execute("COMMIT")
except Exception as e:
    b.execute("ROLLBACK")
    sys.exit(f"HATA: {type(e).__name__}: {e}\nHicbir sey degistirilmedi.")

print("\nTemizlendi.")
print("  kalan konum :", sayi("SELECT COUNT(*) FROM konum WHERE lab_id=?", (_db.LAB_ID,)))
print("  eski_cryo   :", "yok" if not b.execute(
    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='eski_cryo'"
).fetchone() else "HALA VAR")
kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print("  kirik referans:", len(kirik))
b.close()
