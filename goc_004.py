"""Göç 004 — hasta arşiv durumu ve endikasyon seçim listesi.

Mevcut lab.db üzerinde çalışır, veriye dokunmaz.
Birden fazla kez çalıştırılabilir.

Kullanım:  python goc_004.py
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "lab.db"
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)

# --- hasta.durum: aktif / arsiv ---
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(hasta)")]
if "durum" not in kolonlar:
    b.execute("ALTER TABLE hasta ADD COLUMN durum TEXT NOT NULL DEFAULT 'aktif'")
    print("hasta.durum eklendi.")
else:
    print("hasta.durum zaten var.")

# --- endikasyon secim listesi ---
ENDIKASYONLAR = [
    ("erkek_faktoru", "Erkek faktörü"),
    ("siddetli_erkek_faktoru", "Şiddetli erkek faktörü"),
    ("azoospermi", "Azoospermi"),
    ("tubal_faktor", "Tubal faktör"),
    ("endometriozis", "Endometriozis"),
    ("ovulatuar_disfonksiyon", "Ovulatuar disfonksiyon / PCOS"),
    ("azalmis_over_rezervi", "Azalmış over rezervi"),
    ("ileri_anne_yasi", "İleri anne yaşı"),
    ("uterin_faktor", "Uterin faktör"),
    ("aciklanamayan", "Açıklanamayan infertilite"),
    ("tekrarlayan_implantasyon", "Tekrarlayan implantasyon başarısızlığı"),
    ("tekrarlayan_gebelik_kaybi", "Tekrarlayan gebelik kaybı"),
    ("pgt_endikasyonu", "PGT endikasyonu"),
    ("fertilite_koruma", "Fertilite koruma"),
    ("donor_oosit", "Donör oosit"),
    ("donor_sperm", "Donör sperm"),
    ("diger", "Diğer"),
]

sira = 0
for kod, etiket in ENDIKASYONLAR:
    b.execute(
        "INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'endikasyon',?,?,?)", (kod, etiket, sira))
    sira += 1

# --- mevcut serbest metin endikasyonlari kaybetme ---
mevcut = b.execute(
    "SELECT DISTINCT endikasyon FROM cycle "
    "WHERE endikasyon IS NOT NULL AND TRIM(endikasyon) <> ''"
).fetchall()

kodlar = {r[0] for r in b.execute(
    "SELECT kod FROM liste_degeri WHERE lab_id=1 AND liste_adi='endikasyon'")}

eklenen = 0
for (deger,) in mevcut:
    if deger in kodlar:
        continue
    b.execute(
        "INSERT OR IGNORE INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'endikasyon',?,?,?)", (deger, deger, sira))
    sira += 1
    eklenen += 1

b.commit()

n = b.execute(
    "SELECT COUNT(*) FROM liste_degeri WHERE lab_id=1 AND liste_adi='endikasyon'"
).fetchone()[0]
print(f"endikasyon listesi: {n} secenek "
      f"({eklenen} tanesi mevcut kayitlardan tasindi)")

aktif = b.execute("SELECT COUNT(*) FROM hasta WHERE durum='aktif'").fetchone()[0]
arsiv = b.execute("SELECT COUNT(*) FROM hasta WHERE durum='arsiv'").fetchone()[0]
print(f"hasta: {aktif} aktif, {arsiv} arsivde")

b.close()
print("\nGoc 004 tamam.")
