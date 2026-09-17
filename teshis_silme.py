"""Bir hastanın neden silinemediğini adım adım gösterir.

Kullanım:  python3 teshis_silme.py            (hastaları listeler)
           python3 teshis_silme.py 10247      (o hastayı adım adım inceler)

Hiçbir şey silmez — her deneme geri alınır.
"""

import sqlite3
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row
b.execute("PRAGMA foreign_keys = ON")

# --------------------------------------------------------------- liste
if len(sys.argv) < 2:
    print("HASTALAR\n" + "=" * 62)
    for h in b.execute("SELECT id, dosya_no, ad_soyad, durum FROM hasta ORDER BY dosya_no"):
        tr = b.execute(
            "SELECT COUNT(*) k FROM olay o JOIN specimen s ON s.id=o.specimen_id "
            "JOIN cycle c ON c.id=s.cycle_id "
            "WHERE o.tip='transfer' AND o.iptal_mi=0 AND c.hasta_id=?",
            (h["id"],)).fetchone()["k"]
        cy = b.execute("SELECT COUNT(*) k FROM cycle WHERE hasta_id=?",
                       (h["id"],)).fetchone()["k"]
        print(f"  dosya {h['dosya_no']:>8} · {h['ad_soyad'][:22]:22} · {h['durum']:6} "
              f"· {cy} cycle · {tr} transfer"
              f"{'  [SILINEMEZ]' if tr else ''}")
    print("\nAyrinti icin: python3 teshis_silme.py <dosya_no>")
    sys.exit()

dosya_no = sys.argv[1]
h = b.execute("SELECT * FROM hasta WHERE dosya_no=?", (dosya_no,)).fetchone()
if not h:
    sys.exit(f"Dosya no {dosya_no} bulunamadi.")

print(f"HASTA {h['dosya_no']} · {h['ad_soyad']} · id={h['id']} · durum={h['durum']}")
print("=" * 62)

cycles = [r["id"] for r in b.execute("SELECT id FROM cycle WHERE hasta_id=?", (h["id"],))]
print(f"Cycle id'leri: {cycles or 'yok'}")

# --------------------------------------------------------------- referans taramasi
print("\nBU HASTAYA/CYCLE'A REFERANS VEREN KAYITLAR")
print("-" * 62)
bulundu = False
if cycles:
    q = ",".join("?" * len(cycles))
    taramalar = [
        ("specimen.cycle_id", f"SELECT COUNT(*) FROM specimen WHERE cycle_id IN ({q})", cycles),
        ("olay.cycle_id", f"SELECT COUNT(*) FROM olay WHERE cycle_id IN ({q})", cycles),
        ("olay.tr_cycle_id (baska cycle'dan)",
         f"SELECT COUNT(*) FROM olay WHERE tr_cycle_id IN ({q}) AND cycle_id NOT IN ({q})",
         cycles + cycles),
        ("olay.thaw_cycle_id (baska cycle'dan)",
         f"SELECT COUNT(*) FROM olay WHERE thaw_cycle_id IN ({q}) AND cycle_id NOT IN ({q})",
         cycles + cycles),
        ("sperm_dondurma.kullanim_cycle_id (baska hastadan)",
         f"SELECT COUNT(*) FROM sperm_dondurma WHERE kullanim_cycle_id IN ({q}) "
         f"AND hasta_id<>?", cycles + [h["id"]]),
        ("goruntu.cycle_id", f"SELECT COUNT(*) FROM goruntu WHERE cycle_id IN ({q})", cycles),
        ("sperm_ornek.cycle_id", f"SELECT COUNT(*) FROM sperm_ornek WHERE cycle_id IN ({q})", cycles),
        ("gebelik_sonucu.cycle_id", f"SELECT COUNT(*) FROM gebelik_sonucu WHERE cycle_id IN ({q})", cycles),
        ("beta_hcg.cycle_id", f"SELECT COUNT(*) FROM beta_hcg WHERE cycle_id IN ({q})", cycles),
        ("dogan_bebek.cycle_id", f"SELECT COUNT(*) FROM dogan_bebek WHERE cycle_id IN ({q})", cycles),
        ("kaynak_dosya.cycle_id (atlanan kareler)",
         f"SELECT COUNT(*) FROM kaynak_dosya WHERE cycle_id IN ({q})", cycles),
        ("islem_yapan.cycle_id",
         f"SELECT COUNT(*) FROM islem_yapan WHERE cycle_id IN ({q})", cycles),
    ]
    for ad, sql, par in taramalar:
        n = b.execute(sql, par).fetchone()[0]
        if n:
            bulundu = True
            print(f"  {ad:36} {n}")
if not bulundu:
    print("  (hicbiri — temiz gorunuyor)")

# --------------------------------------------------------------- adim adim deneme
print("\nSILME DENEMESI (adim adim, geri alinir)")
print("-" * 62)

ADIMLAR = []
for cid in cycles:
    ADIMLAR += [
        (f"cycle {cid}: transfer baglarini kopar",
         "UPDATE olay SET tr_cycle_id=NULL, iptal_mi=1 WHERE tr_cycle_id=? AND cycle_id<>?",
         (cid, cid)),
        (f"cycle {cid}: cozme baglarini kopar",
         "UPDATE olay SET thaw_cycle_id=NULL WHERE thaw_cycle_id=? AND cycle_id<>?",
         (cid, cid)),
        (f"cycle {cid}: sperm_dondurma baglarini kopar",
         "UPDATE sperm_dondurma SET kullanim_cycle_id=NULL WHERE kullanim_cycle_id=?",
         (cid,)),
        (f"cycle {cid}: kaynak_dosya (cycle goruntuleri)",
         "DELETE FROM kaynak_dosya WHERE goruntu_id IN "
         "(SELECT id FROM goruntu WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: kaynak_dosya (oosit goruntuleri)",
         "DELETE FROM kaynak_dosya WHERE goruntu_id IN (SELECT id FROM goruntu "
         "WHERE specimen_id IN (SELECT id FROM specimen WHERE cycle_id=?))", (cid,)),
        (f"cycle {cid}: goruntu (oosit)",
         "DELETE FROM goruntu WHERE specimen_id IN "
         "(SELECT id FROM specimen WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: goruntu (cycle)", "DELETE FROM goruntu WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: specimen_bulgu",
         "DELETE FROM specimen_bulgu WHERE specimen_id IN "
         "(SELECT id FROM specimen WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: pgt_sonuc",
         "DELETE FROM pgt_sonuc WHERE specimen_id IN "
         "(SELECT id FROM specimen WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: olay (oosit)",
         "DELETE FROM olay WHERE specimen_id IN "
         "(SELECT id FROM specimen WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: olay (cycle)", "DELETE FROM olay WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: kaynak_dosya (cycle)",
         "DELETE FROM kaynak_dosya WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: beta_hcg", "DELETE FROM beta_hcg WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: dogan_bebek", "DELETE FROM dogan_bebek WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: gebelik_sonucu", "DELETE FROM gebelik_sonucu WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: sperm_analiz",
         "DELETE FROM sperm_analiz WHERE sperm_ornek_id IN "
         "(SELECT id FROM sperm_ornek WHERE cycle_id=?)", (cid,)),
        (f"cycle {cid}: sperm_ornek", "DELETE FROM sperm_ornek WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: islem_yapan", "DELETE FROM islem_yapan WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: specimen", "DELETE FROM specimen WHERE cycle_id=?", (cid,)),
        (f"cycle {cid}: CYCLE", "DELETE FROM cycle WHERE id=?", (cid,)),
    ]
ADIMLAR.append(("HASTA", "DELETE FROM hasta WHERE id=?", (h["id"],)))

hatali = None
b.execute("BEGIN")
for ad, sql, par in ADIMLAR:
    try:
        imlec = b.execute(sql, par)
        if imlec.rowcount > 0:
            print(f"  ok   {ad}  ({imlec.rowcount} satir)")
    except sqlite3.Error as e:
        print(f"  HATA {ad}")
        print(f"       -> {e}")
        hatali = (ad, sql, e)
        break

if not hatali:
    print("\n  Tum adimlar gecti — silme calisir.")
    kalan = b.execute("PRAGMA foreign_key_check").fetchall()
    if kalan:
        print("\n  ANCAK kirik referanslar var:")
        for r in kalan[:10]:
            print(f"    tablo={r[0]} rowid={r[1]} -> {r[2]}")
b.execute("ROLLBACK")
print("\n  (deneme geri alindi, hicbir sey silinmedi)")

# --------------------------------------------------------------- genel saglik
print("\nVERITABANI GENEL KONTROL")
print("-" * 62)
kirik = b.execute("PRAGMA foreign_key_check").fetchall()
if kirik:
    print(f"  {len(kirik)} kirik referans var:")
    gruplu = {}
    for r in kirik:
        gruplu[(r[0], r[2])] = gruplu.get((r[0], r[2]), 0) + 1
    for (tablo, hedef), n in gruplu.items():
        print(f"    {tablo} -> {hedef}: {n} satir")
    print("\n  Bu kayitlar var olmayan bir satira isaret ediyor.")
    print("  Silme islemi bu yuzden basarisiz olabilir.")
else:
    print("  Kirik referans yok.")

b.close()
