"""Göç 019 — androloji (sperm) modülü: analiz alanları ve seçim listeleri.

`sperm_ornek` / `sperm_analiz` tabloları ve `sperm_alinma` / `sperm_hazirlama`
/ `viskozite` listeleri şemada zaten vardı. Bu göç eksikleri tamamlar:

  - `sperm_analiz` tablosuna geniş WHO parametreleri: total motilite, morfoloji,
    vitalite, yuvarlak hücre, lökosit, aglütinasyon.
  - `sperm_hazirlama` ve `sperm_alinma` listelerine yeni yöntemler.
  - `sperm_aglutinasyon` ve `sperm_gorunum` listeleri.

Listeleri sonradan düzenlemek için: `python liste_duzenle.py sperm_hazirlama`

Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_019.py      (Mac'te: python3 goc_019.py)
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

# ------------------------------------------------------- sperm_analiz kolonlari
YENI_KOLON = [
    ("total_motil_yuzde", "REAL"),
    ("morfoloji_normal_yuzde", "REAL"),
    ("vitalite_yuzde", "REAL"),
    ("yuvarlak_hucre_milyon_ml", "REAL"),
    ("lokosit_milyon_ml", "REAL"),
    ("aglutinasyon", "TEXT"),
]

mevcut = {r["name"] for r in b.execute("PRAGMA table_info(sperm_analiz)")}
eklenen = 0
for ad, tip in YENI_KOLON:
    if ad not in mevcut:
        b.execute(f"ALTER TABLE sperm_analiz ADD COLUMN {ad} {tip}")
        print(f"  + sperm_analiz.{ad}")
        eklenen += 1
b.commit()
if not eklenen:
    print("sperm_analiz kolonlari zaten guncel.")

# --------------------------------------------------------------------- listeler
# Mevcut kodlara dokunulmaz; sadece eksik olanlar eklenir. Sira, o listedeki
# en yuksek siranin bir fazlasindan devam eder.
EKLENECEK = {
    "sperm_hazirlama": [
        ("gradient_swimup", "Gradient + swim-up"),
        ("macs", "MACS"),
        ("picsi", "PICSI"),
        ("mikroakiskan", "Mikroakışkan (ZyMōt)"),
        ("tese_isleme", "TESE örneği işleme"),
    ],
    "sperm_alinma": [
        ("kondom", "Kesintili ilişki (kondom)"),
        ("elektroejakulasyon", "Elektroejakülasyon"),
        ("retrograd", "Retrograd ejakülasyon"),
        ("mikrotese", "mikroTESE"),
        ("pesa", "PESA"),
    ],
    "sperm_aglutinasyon": [
        ("yok", "Yok"),
        ("izole", "İzole"),
        ("hafif", "Hafif"),
        ("orta", "Orta"),
        ("agir", "Ağır"),
    ],
    "sperm_gorunum": [
        ("normal", "Normal (opalesan gri-beyaz)"),
        ("berrak", "Berrak / şeffaf"),
        ("sarimsi", "Sarımsı"),
        ("kirmizi_kahve", "Kırmızı-kahverengi (kanlı)"),
        ("bulanik", "Bulanık"),
    ],
}

eklenen_deger = 0
for liste, degerler in EKLENECEK.items():
    son_sira = b.execute(
        "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
        "WHERE lab_id=1 AND liste_adi=?", (liste,)).fetchone()[0]
    for kod, etiket in degerler:
        var = b.execute(
            "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi=? AND kod=?",
            (liste, kod)).fetchone()
        if var:
            continue
        son_sira += 1
        b.execute(
            "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
            "VALUES (1,?,?,?,?)", (liste, kod, etiket, son_sira))
        print(f"  + {liste}: {kod}  ({etiket})")
        eklenen_deger += 1
b.commit()
if not eklenen_deger:
    print("Secim listeleri zaten guncel.")

# ----------------------------------------------------------------------- ozet
print("\nAndroloji seçim listeleri:")
for liste in ("sperm_alinma", "sperm_hazirlama", "viskozite",
              "sperm_aglutinasyon", "sperm_gorunum"):
    kayitlar = b.execute(
        "SELECT etiket FROM liste_degeri WHERE lab_id=1 AND liste_adi=? "
        "AND aktif_mi=1 ORDER BY sira", (liste,)).fetchall()
    print(f"  {liste} ({len(kayitlar)}): " + ", ".join(r["etiket"] for r in kayitlar))

kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(sperm_analiz)")]
print(f"\nsperm_analiz kolonlari ({len(kolonlar)}): {', '.join(kolonlar)}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 019 tamam.")
