"""Seçim listelerini görüntüle ve temizle.

Kullanım:
  python3 liste_duzenle.py                    tüm listeleri özetler
  python3 liste_duzenle.py endikasyon         o listenin değerlerini gösterir
  python3 liste_duzenle.py endikasyon fefewf  o değeri siler (kullanımı varsa sorar)
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

# Hangi kolonlar hangi listeyi kullaniyor
KULLANIM = {
    "endikasyon": [("cycle", "endikasyon")],
    "protokol_tipi": [("cycle", "protokol_tipi")],
    "trigger_tipi": [("cycle", "trigger_tipi")],
    "cycle_tipi": [("cycle", "cycle_tipi")],
    "maturasyon": [("olay", "mat_deger")],
    "gecis_zorlugu": [("olay", "icsi_gecis_zorlugu")],
    "icsi_sonuc": [("olay", "icsi_sonuc")],
    "fert_sonuc": [("olay", "fert_sonuc")],
    "pn_sayisi": [("olay", "fert_pn_sayisi")],
    "pn_skoru": [("olay", "fert_pn_skoru")],
    "simetri": [("olay", "cl_simetri")],
    "bl_genisleme": [("olay", "bl_genisleme")],
    "bl_icm": [("olay", "bl_icm")],
    "bl_te": [("olay", "bl_te")],
    "bl_derece": [("olay", "bl_derece")],
    "thaw_sagkalim": [("olay", "thaw_sagkalim")],
    "discard_sebep": [("olay", "dis_sebep")],
    "goruntu_asama": [("goruntu", "asama")],
    "taraf": [("specimen", "taraf")],
    "tasiyici_tipi": [("tasiyici", "tip")],
    "tasiyici_renk": [("tasiyici", "renk")],
    "sperm_alinma": [("sperm_ornek", "alinma_yontemi")],
    "sperm_hazirlama": [("sperm_ornek", "hazirlama_yontemi")],
    "viskozite": [("sperm_ornek", "viskozite")],
    "sonlanma": [("gebelik_sonucu", "sonlanma")],
    "pgt_sonuc": [("pgt_sonuc", "sonuc")],
}


def kullanim_sayisi(liste_adi, kod):
    toplam = 0
    for tablo, kolon in KULLANIM.get(liste_adi, []):
        try:
            toplam += b.execute(
                f"SELECT COUNT(*) FROM {tablo} WHERE {kolon}=?", (kod,)).fetchone()[0]
        except sqlite3.Error:
            pass
    return toplam


if len(sys.argv) < 2:
    print("LISTELER\n" + "=" * 50)
    for r in b.execute("SELECT liste_adi, COUNT(*) k FROM liste_degeri "
                       "WHERE lab_id=1 GROUP BY liste_adi ORDER BY liste_adi"):
        print(f"  {r['liste_adi']:22} {r['k']:3} deger")
    print("\nAyrinti: python3 liste_duzenle.py <liste_adi>")
    sys.exit()

liste = sys.argv[1]
degerler = b.execute("SELECT * FROM liste_degeri WHERE lab_id=1 AND liste_adi=? "
                     "ORDER BY sira", (liste,)).fetchall()
if not degerler:
    sys.exit(f"'{liste}' diye bir liste yok.")

if len(sys.argv) == 2:
    print(f"LISTE: {liste}\n" + "=" * 62)
    for d in degerler:
        n = kullanim_sayisi(liste, d["kod"])
        not_ = ""
        if d["kod"] == d["etiket"]:
            not_ = "  <- serbest metinden tasinmis"
        print(f"  {d['kod']:28} {d['etiket'][:20]:20} {n:3} kayitta{not_}")
    print("\nSilmek icin: python3 liste_duzenle.py " + liste + " <kod>")
    sys.exit()

kod = sys.argv[2]
d = next((x for x in degerler if x["kod"] == kod), None)
if not d:
    sys.exit(f"'{kod}' bu listede yok.")

n = kullanim_sayisi(liste, kod)
print(f"Silinecek: {liste} / {kod} ('{d['etiket']}')")
print(f"Kullanildigi kayit sayisi: {n}")

if n:
    print("\nBu deger kayitlarda kullaniliyor. Silersen o kayitlarda kod")
    print("goruntulenir ama veri kaybolmaz. Devam edilsin mi? (e/h) ", end="")
    if input().strip().lower() not in ("e", "evet"):
        sys.exit("Iptal edildi.")
    print("Kayitlardaki degeri de temizlemek ister misin? (e/h) ", end="")
    if input().strip().lower() in ("e", "evet"):
        for tablo, kolon in KULLANIM.get(liste, []):
            b.execute(f"UPDATE {tablo} SET {kolon}=NULL WHERE {kolon}=?", (kod,))
        print("Kayitlardaki deger temizlendi.")

b.execute("DELETE FROM liste_degeri WHERE lab_id=1 AND liste_adi=? AND kod=?",
          (liste, kod))
b.commit()
print(f"'{kod}' listeden silindi.")
b.close()
