"""Göç 018 — endikasyon listesindeki serbest metin kopyalarını temizler.

Goc 004 endikasyonu acilir listeye cevirirken, o sirada cycle'larda yazili
olan serbest metinleri kaybolmasin diye listeye tasimisti. Bunlarin bir kismi
zaten listede olan degerlerin kucuk harfli / sapkasiz kopyalari:
  'tubal faktor'  -> tubal_faktor  (Tubal faktör)
  'erkek faktoru' -> erkek_faktoru (Erkek faktörü)

Bu goc eslesenleri birlestirir: cycle'lardaki deger dogru koda cevrilir,
kopya listeden silinir. Eslesmeyen serbest metinlere dokunulmaz.

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_018.py      (Mac'te: python3 goc_018.py)
"""

import sqlite3
import sys
import unicodedata
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")


def sadelestir(metin: str) -> str:
    """Karşılaştırma için: küçük harf, şapkasız, boşluk/tire yerine alt çizgi."""
    m = (metin or "").strip().lower()
    m = m.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
    m = m.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    m = unicodedata.normalize("NFKD", m)
    m = "".join(x for x in m if not unicodedata.combining(x))
    for eski in (" ", "-", "/"):
        m = m.replace(eski, "_")
    while "__" in m:
        m = m.replace("__", "_")
    return m.strip("_")


b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

degerler = b.execute(
    "SELECT * FROM liste_degeri WHERE lab_id=1 AND liste_adi='endikasyon' "
    "ORDER BY sira").fetchall()

# Serbest metinden tasinanlar: kod ile etiket ayni
kopyalar = [d for d in degerler if d["kod"] == d["etiket"]]
resmiler = [d for d in degerler if d["kod"] != d["etiket"]]

if not kopyalar:
    print("Serbest metinden tasinmis deger yok.")
else:
    print(f"{len(kopyalar)} serbest metin degeri inceleniyor:\n")

birlestirilen = kalan = 0
for k in kopyalar:
    anahtar = sadelestir(k["kod"])
    hedef = next((r for r in resmiler
                  if sadelestir(r["kod"]) == anahtar
                  or sadelestir(r["etiket"]) == anahtar), None)
    if not hedef:
        print(f"  KALDI      '{k['kod']}'  (listede karsiligi yok)")
        kalan += 1
        continue

    n = b.execute("SELECT COUNT(*) FROM cycle WHERE endikasyon=?",
                  (k["kod"],)).fetchone()[0]
    b.execute("UPDATE cycle SET endikasyon=? WHERE endikasyon=?",
              (hedef["kod"], k["kod"]))
    b.execute("DELETE FROM liste_degeri WHERE id=?", (k["id"],))
    print(f"  BIRLESTIRILDI  '{k['kod']}' -> {hedef['kod']} ({hedef['etiket']})"
          f"{f'  · {n} cycle guncellendi' if n else ''}")
    birlestirilen += 1

b.commit()

print(f"\n{birlestirilen} birlestirildi, {kalan} dokunulmadi")
if kalan:
    print("Kalanlari elle silmek icin: python liste_duzenle.py endikasyon <kod>")

print("\nGuncel endikasyon listesi:")
for r in b.execute("SELECT kod, etiket FROM liste_degeri WHERE lab_id=1 "
                   "AND liste_adi='endikasyon' ORDER BY sira"):
    n = b.execute("SELECT COUNT(*) FROM cycle WHERE endikasyon=?",
                  (r["kod"],)).fetchone()[0]
    print(f"  {r['kod']:26} {r['etiket'][:24]:24} {n} cycle")

b.close()
print("\nGoc 018 tamam.")
