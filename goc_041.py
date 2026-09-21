"""Göç 041 — Cleavage skoru artık G1-G4 arasından seçiliyor.

Kullanıcının isteği: "Cleavage bölümünde skor kısmı elle girilebilsin.
G1,G2,G3,G4 şeklinde seçilebilsin." Elle skor girme zaten vardı
(`cl_skor`/`cl_skor_kaynagi`, CLAUDE.md "Otomatik skorlar kaynak
işaretler") ama serbest metin kutusuydu; bu göç `liste_degeri`'ne yeni bir
"cleavage_skor" listesi ekliyor ki ekran (v6.122) bunu kapalı bir seçenek
grubuna (simetri'nin aynı deseni) çevirebilsin.

**Kodlar bilerek "G1".."G4" (büyük harf), lowercase "g1" değil** —
`app.py` `cleavage_kaydet()`'teki `(f.get("cl_skor") or "").strip().upper()`
satırı zaten var ve değiştirilmedi (elle skor eskiden de büyütülüyordu).
Kod lowercase olsaydı `.upper()` onu "G1"e çevirir ama `liste_degeri`'ndeki
gerçek kod "g1" kalırdı — `liste_etiket()` eşleşmeyi bulamaz, ekranda yine
"G1" görünürdü (kodun kendisi düşer) ama laboratuvar etiketi sonradan
değiştirirse (örn. "Grade 1 (mükemmel)") bu sessizce görünmezdi. Kod ve
etiketi aynı tutmak bu riski baştan kapatıyor.

Otomatik hesaplanan A/B/C değerlerine dokunulmadı — `cleavage_skor()`
hâlâ çalışıyor, yalnızca ELLE girilen skorun seçim şekli değişti. İki
skorlama birbirine karışmıyor: `liste_etiket('cleavage_skor', kod)`
bulunamayan bir kodu (A/B/C gibi) olduğu gibi döndürüyor (tuzak yok).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_041.py
"""

import sqlite3
import sys

import db as _db
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

DEGERLER = [("G1", "G1"), ("G2", "G2"), ("G3", "G3"), ("G4", "G4")]

son_sira = b.execute(
    "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
    "WHERE lab_id=1 AND liste_adi='cleavage_skor'").fetchone()[0]
eklenen = 0
for kod, etiket in DEGERLER:
    var = b.execute(
        "SELECT 1 FROM liste_degeri WHERE lab_id=1 AND liste_adi='cleavage_skor' "
        "AND kod=?", (kod,)).fetchone()
    if var:
        continue
    son_sira += 1
    b.execute(
        "INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
        "VALUES (1,'cleavage_skor',?,?,?)", (kod, etiket, son_sira))
    print(f"  + cleavage_skor: {kod} ({etiket})")
    eklenen += 1
b.commit()
if not eklenen:
    print("cleavage_skor listesi zaten guncel.")

kayitlar = b.execute(
    "SELECT etiket FROM liste_degeri WHERE lab_id=1 AND liste_adi='cleavage_skor' "
    "AND aktif_mi=1 ORDER BY sira").fetchall()
print(f"\ncleavage_skor ({len(kayitlar)}): " + ", ".join(r["etiket"] for r in kayitlar))

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 041 tamam.")
