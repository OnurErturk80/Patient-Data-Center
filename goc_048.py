"""Göç 048 — Cleavage'da "Birleşme" (v6.157).

Kullanıcının cevabı (2026-09-23): "BB birleşme başlangıcı demek. Birleşme
olarak yazılsın. Cleavage bölümüne kalitede Birleşme ekle. Birleşme seçilince
hücre sayısı kaybolsun, grade ve fragmantasyon gözüksün. Yani embriyo
kalitesi Birleşme G2 gibi olabilsin."

`olay.cl_birlesme` — bu cleavage değerlendirmesinde embriyo birleşme
(kompaksiyon) başlangıcında: hücre sayısı sayılamıyor, yerine "Birleşme"
yazılıyor. 1 = birleşme, boş = olağan cleavage (hücre sayısıyla).
Kalitenin yazımı `db.cleavage_yazimi()`: "Birleşme G2", "8HG2".

Geriye dönük doldurma: `aktar_access.py` (v6.148) Access notlarındaki
"BB" / "BİRLEŞME" / "BİRLEŞMEG3" öğelerini skoru bilinmeyen embriyo diye
yazıyordu -- hücre sayısı ve grade boş bir cleavage değerlendirmesi, notunda
"Kaynak kayıttaki yazım: BB". Bu göç o değerlendirmeleri birleşme yapıyor;
yazımda grade varsa ("BİRLEŞMEG3") ve değerlendirmede grade boşsa onu da
yazıyor. Yalnızca aktarımın yazdığı, hücre sayısı boş değerlendirmelere
dokunuyor -- ekrandan girilmiş bir kayda değil.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_048.py
"""

import re
import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("PRAGMA foreign_keys = ON")

kolonlar = {r[1] for r in b.execute("PRAGMA table_info(olay)")}
if "cl_birlesme" in kolonlar:
    print("olay.cl_birlesme zaten var.")
else:
    b.execute("ALTER TABLE olay ADD COLUMN cl_birlesme INTEGER")
    print("olay.cl_birlesme eklendi.")

# aktar_access'in notu: "Kaynak kayıttaki yazım: BB" ya da
# "Kaynak kayıttaki yazım (transfer): BİRLEŞMEG3". Türkçe harfler katlanıp
# karşılaştırılıyor (aktar_access._sade()'nin aynısı).
_KATLA = str.maketrans("İIŞĞÜÖÇ", "IISGUOC")
_YAZIM = re.compile(r"^(?:BB|BIRLESME\s*(?:BASLANGICI)?\s*G?\s*([1-4])?)$")

guncellenen = 0
for oid, notlar, skor in b.execute(
        "SELECT id, notlar, cl_skor FROM olay "
        "WHERE tip = 'cleavage_degerlendirme' AND iptal_mi = 0 "
        "AND cl_hucre_sayisi IS NULL AND COALESCE(cl_birlesme, 0) = 0 "
        "AND notlar LIKE 'Kaynak kayıttaki yazım%'").fetchall():
    ham = notlar.split(":", 1)[1] if ":" in notlar else ""
    m = _YAZIM.match(re.sub(r"\s+", " ", ham).strip().upper().translate(_KATLA))
    if not m:
        continue
    grade = f"G{m.group(1)}" if m.group(1) else None
    if grade and not skor:
        b.execute("UPDATE olay SET cl_birlesme = 1, cl_skor = ?, "
                  "cl_skor_kaynagi = 'elle' WHERE id = ?", (grade, oid))
    else:
        b.execute("UPDATE olay SET cl_birlesme = 1 WHERE id = ?", (oid,))
    guncellenen += 1

b.commit()
b.close()
print(f"Aktarılmış 'BB' / 'BİRLEŞME' değerlendirmesi: {guncellenen} tanesi "
      "birleşme olarak işaretlendi.")
