"""FET / çözme tedavisinin resmî formu neden boş -- teşhis (v6.153).

Kullanım:  python3 teshis_form.py              (çözme tedavilerini listeler)
           python3 teshis_form.py 2026-0123    (o tedaviyi adım adım inceler)

Hiçbir şey değiştirmez, yalnızca okur. Hasta adı basmaz -- çıktı
kopyalanıp paylaşılabilsin diye yalnızca dosya no ve tedavi no.

Formların çözme bilgisi (v6.152) şu kayıtlardan geliyor:
  - çözme olayı, "hangi tedavi için çözüldü" = bu tedavi (`thaw_cycle_id`);
  - transfer olayı, "nerede transfer edildi" = bu tedavi (`tr_cycle_id`).
Çözme ekranı Cryo Haritası'ndan açılınca "hangi tedavi için" seçimi
embriyonun KAYNAK tedavisine düşüyor; değiştirilmeden kaydedilirse çözme
FET'e değil kaynak ICSI'ye yazılır ve FET'in formu boş görünür. Bu araç
bunu ve öteki olası sebepleri tek tek gösterir.
"""

import re
import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py

DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi: " + str(DB))

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row
OLAY = {r[1] for r in b.execute("PRAGMA table_info(olay)")}
FET = tuple(_db.FET_TIPLERI)


def surum():
    """Diskteki programın sürümü -- README'nin son bölümü."""
    try:
        metin = (_db.PROGRAM_KOK / "README.md").read_text(encoding="utf-8")
        s = re.findall(r"^# (v6\.\d+)", metin, re.M)
        return s[-1] if s else "?"
    except OSError:
        return "?"


print(f"Veritabani : {DB}")
print(f"Program    : {surum()} (diskteki kod)")
try:
    import formlar
    yeni = hasattr(formlar, "cozulen_ornekler")
except Exception as h:          # formlar açılamıyorsa bunu da söyle
    yeni = False
    print(f"formlar.py acilamadi: {h}")
print("Form kodu  : " + ("v6.152 ve sonrasi (cozulen embriyolar var)" if yeni
                         else "ESKI -- git pull yapilmamis"))
print("Not: Program acikken 'git pull' yaptiysaniz programi KAPATIP ACIN;\n"
      "    formlar Python kodu, program acikken yenilenmez.\n")

eksik = [k for k in ("thaw_cycle_id", "tr_cycle_id") if k not in OLAY]
if eksik:
    sys.exit("Gocler calismamis, kolon yok: " + ", ".join(eksik))

yer = ",".join("?" * len(FET))

# --------------------------------------------------------------- liste
if len(sys.argv) < 2:
    print("COZME TEDAVILERI (FET, FET 3->5, Yumurta Cozme)\n" + "=" * 66)
    for c in b.execute(
            f"SELECT c.id, c.cycle_no, c.cycle_tipi, h.dosya_no FROM cycle c "
            f"JOIN hasta h ON h.id = c.hasta_id WHERE c.cycle_tipi IN ({yer}) "
            f"ORDER BY c.cycle_no", FET):
        cozme = b.execute(
            "SELECT COUNT(*) FROM olay WHERE tip='thaw' AND iptal_mi=0 "
            "AND thaw_cycle_id=?", (c["id"],)).fetchone()[0]
        tr = b.execute(
            "SELECT COUNT(*) FROM olay WHERE tip='transfer' AND iptal_mi=0 "
            "AND tr_cycle_id=?", (c["id"],)).fetchone()[0]
        isaret = "  <-- FORMDA COZME YOK" if not cozme else ""
        print(f"  {c['cycle_no']}  dosya {c['dosya_no']:>8}  {c['cycle_tipi']:14}"
              f" cozme {cozme:>2}  transfer {tr:>2}{isaret}")
    print("\nAyrinti icin: python3 teshis_form.py <tedavi no>  (orn. 2026-0123)")
    sys.exit()

# --------------------------------------------------------------- tek tedavi
c = b.execute(
    "SELECT c.*, h.dosya_no FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
    "WHERE c.cycle_no = ? OR CAST(c.id AS TEXT) = ?",
    (sys.argv[1], sys.argv[1])).fetchone()
if not c:
    sys.exit(f"Tedavi bulunamadi: {sys.argv[1]}")
cid = c["id"]
print(f"Tedavi {c['cycle_no']} (kimlik {cid}) · dosya {c['dosya_no']} · "
      f"tip {c['cycle_tipi']} · {c['hasta_cycle_no']}. tedavi\n")

print("1) Bu tedavi ICIN kaydedilmis cozmeler:")
cozmeler = b.execute(
    "SELECT o.specimen_id, o.zaman, o.thaw_sagkalim, o.thaw_canlilik "
    "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
    "WHERE o.tip='thaw' AND o.iptal_mi=0 "
    "AND COALESCE(o.thaw_cycle_id, s.cycle_id) = ? ORDER BY o.zaman",
    (cid,)).fetchall()
for r in cozmeler:
    print(f"   {r['specimen_id']}  {r['zaman']}  sagkalim={r['thaw_sagkalim']}"
          f"  canlilik={r['thaw_canlilik']}")
if not cozmeler:
    print("   YOK -- formda cozulen embriyo bu yuzden bos.")

print("\n2) Bu tedavide transfer edilenler:")
trler = b.execute(
    "SELECT o.id, o.specimen_id, o.zaman FROM olay o JOIN specimen s "
    "ON s.id = o.specimen_id WHERE o.tip='transfer' AND o.iptal_mi=0 "
    "AND COALESCE(o.tr_cycle_id, s.cycle_id) = ? ORDER BY o.zaman",
    (cid,)).fetchall()
for r in trler:
    print(f"   {r['specimen_id']}  {r['zaman']}")
if not trler:
    print("   YOK")

print("\n3) Bu hastanin BASKA tedaviye yazilmis cozmeleri:")
# Transferden hemen önceki çözme (kimlik sırası): transfer edilen embriyo
# bu çözmeyle çıktı. O çözme başka tedaviye yazılmışsa sebep bu.
onceki_cozme = set()
for t in trler:
    z = b.execute("SELECT id FROM olay WHERE specimen_id=? AND tip='thaw' "
                  "AND iptal_mi=0 AND id < ? ORDER BY id DESC LIMIT 1",
                  (t["specimen_id"], t["id"])).fetchone()
    if z:
        onceki_cozme.add(z["id"])
baska = b.execute(
    "SELECT o.id, o.specimen_id, o.zaman, "
    "  COALESCE(o.thaw_cycle_id, s.cycle_id) AS yazildigi, cc.cycle_no, "
    "  cc.cycle_tipi "
    "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
    "JOIN cycle kaynak ON kaynak.id = s.cycle_id "
    "JOIN cycle cc ON cc.id = COALESCE(o.thaw_cycle_id, s.cycle_id) "
    "WHERE o.tip='thaw' AND o.iptal_mi=0 AND kaynak.hasta_id = ? "
    "AND COALESCE(o.thaw_cycle_id, s.cycle_id) <> ? ORDER BY o.zaman",
    (c["hasta_id"], cid)).fetchall()
for r in baska:
    tr_burada = r["id"] in onceki_cozme
    not_ = ("  <-- BU TEDAVIDE TRANSFER EDILMIS ama cozmesi "
            f"{r['cycle_no']} ({r['cycle_tipi']}) tedavisine yazilmis"
            if tr_burada else "")
    print(f"   {r['specimen_id']}  {r['zaman']}  -> {r['cycle_no']} "
          f"({r['cycle_tipi']}){not_}")
if not baska:
    print("   YOK")
if any(not _db.cozme_tedavisi_mi(r["cycle_tipi"]) for r in baska):
    print("   Cozme asamasi olmayan tedaviye (IVF/ICSI) yazilmis cozme var.\n"
          "   v6.155'ten beri bu ayri bir FET tedavisi: python3 cozme_ayir.py")

if yeni:
    print("\n4) Formun gorecegi degerler (su anki kodla):")
    v = formlar.ozet_verisi(cid)
    a = formlar.artlab_verisi(cid)
    print(f"   Ozet  cozdurulen sayi : {v.get('cozdurulen_sayi')}")
    print(f"   Ozet  viabilite       : {v.get('cozdurme_viabilite')}")
    print(f"   ART   THAW            : {a.get('thaw_satirlari')}")
    print(f"   ART   TRANSFER        : {a.get('transfer_satirlari')}")
    print("   Ozet  NOTLAR:")
    for s in (v.get("notlar") or "(bos)").splitlines():
        print("     " + s)

print("\nBu ciktinin tamamini kopyalayip gonderin.")
