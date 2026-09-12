"""Yılı bozuk tarihleri bulur ve sorarak düzeltir.

Kullanım:
  python3 tarih_duzelt.py           bulur, tek tek sorar, onayladığını düzeltir
  python3 tarih_duzelt.py liste     yalnızca listeler, hiçbir şeye dokunmaz

Neden var: bir cycle'da OPU tarihi `0026-09-04` yazıyordu. `datetime-local`
alanına yıl olarak "26" yazılınca tarayıcı bunu **26. yıl** diye kaydediyor;
değer geçerli bir ISO tarihi olduğu için hiçbir yerde patlamıyor, sessizce
duruyor. Sonucu: o vaka ay listesinde görünmüyor, formda saçma bir tarih
basılıyor, yıl seçicisi iki bin satır olmak istiyor.

Araç **hiçbir şeyi kendiliğinden değiştirmez**. Her kayıt için ne bulduğunu,
kime ait olduğunu ve ne önerdiğini yazar; kararı kullanıcı verir — tarih
klinik veridir, varsayımla düzeltilmez.

Öneri de uydurma değil: kaydın **kendi oluşturma yılından** geliyor. Kayıt
2026'da girildiyse o gün yazılan klinik tarih de 2026'dır. Doğum tarihlerine
öneri yapılmaz (kaydın girildiği yılla doğum yılının ilgisi yok).
"""

import re
import sqlite3
import sys
from datetime import datetime

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)

# Yılı bundan küçükse yazım hatası sayılır. Doğum tarihleri 1900'lerde
# olabilir, o yüzden sınır 2000 değil 1900.
EN_ESKI_YIL = 1900

# Bir tarihin başlangıcı: 0026-09-04, 2026-09-04 08:15:00, 2026-09-04T08:15
TARIH = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")

# Kaydın girildiği yıl bu tarihler için ölçü olmaz.
ONERISIZ = {"dogum_tarihi", "es_dogum_tarihi", "dogum_zamani"}


def _tarih_kolonlari(b):
    """Tarih tutan metin kolonları: adında 'tarih' ya da 'zaman' geçenler.

    Tipe de bakılıyor — `gun`, `stim_gun_sayisi` gibi sayı kolonları adından
    değil tipinden eleniyor.
    """
    for t in [r[0] for r in b.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]:
        kolonlar = [k["name"] for k in b.execute(f"PRAGMA table_info({t})")
                    if ("tarih" in k["name"] or "zaman" in k["name"])
                    and "INT" not in (k["type"] or "").upper()]
        if kolonlar:
            yield t, kolonlar


def _anahtar(b, tablo):
    """Tablonun birincil anahtar kolonu (yoksa rowid)."""
    for k in b.execute(f"PRAGMA table_info({tablo})"):
        if k["pk"]:
            return k["name"]
    return "rowid"


def _kime_ait(b, tablo, satir):
    """Kaydın kime ait olduğunu insan diliyle söyler.

    Ekranda "olay 41" yazsa kullanıcı hangi hastaya dokunduğunu bilemez.
    """
    hasta_id = cycle_id = None
    kolonlar = satir.keys()
    if tablo == "hasta":
        hasta_id = satir["id"]
    elif tablo == "cycle":
        cycle_id = satir["id"]
    elif "cycle_id" in kolonlar:
        cycle_id = satir["cycle_id"]
    elif "hasta_id" in kolonlar:
        hasta_id = satir["hasta_id"]
    elif "specimen_id" in kolonlar:
        s = b.execute("SELECT cycle_id FROM specimen WHERE id=?",
                      (satir["specimen_id"],)).fetchone()
        cycle_id = s["cycle_id"] if s else None

    parca = []
    if cycle_id:
        c = b.execute("SELECT cycle_no, hasta_id FROM cycle WHERE id=?",
                      (cycle_id,)).fetchone()
        if c:
            parca.append(f"cycle {c['cycle_no']}")
            hasta_id = hasta_id or c["hasta_id"]
    if hasta_id:
        h = b.execute("SELECT dosya_no, ad_soyad FROM hasta WHERE id=?",
                      (hasta_id,)).fetchone()
        if h:
            parca.insert(0, f"{h['dosya_no']} {h['ad_soyad']}")
    return " / ".join(parca)


def _oneri(b, tablo, satir, kolon, deger):
    """Aynı gün ve saat, yılı kaydın oluşturma yılından. Bulunamazsa None."""
    if kolon in ONERISIZ:
        return None
    yil = None
    for kaynak in ("olusturma_zamani",):
        if kaynak in satir.keys() and satir[kaynak]:
            e = TARIH.match(str(satir[kaynak]))
            if e and int(e.group(1)) >= EN_ESKI_YIL:
                yil = e.group(1)
    if yil is None and "cycle_id" in satir.keys() and satir["cycle_id"]:
        c = b.execute("SELECT olusturma_zamani FROM cycle WHERE id=?",
                      (satir["cycle_id"],)).fetchone()
        if c and c["olusturma_zamani"]:
            e = TARIH.match(str(c["olusturma_zamani"]))
            if e and int(e.group(1)) >= EN_ESKI_YIL:
                yil = e.group(1)
    return yil + str(deger)[4:] if yil else None


def bulgular(b):
    """Yılı EN_ESKI_YIL'den küçük bütün tarihler."""
    cikti = []
    for tablo, kolonlar in _tarih_kolonlari(b):
        ak = _anahtar(b, tablo)
        kosul = " OR ".join(f"{k} IS NOT NULL" for k in kolonlar)
        for satir in b.execute(f"SELECT rowid, * FROM {tablo} WHERE {kosul}"):
            for kolon in kolonlar:
                deger = satir[kolon]
                if not deger:
                    continue
                e = TARIH.match(str(deger))
                if e and int(e.group(1)) < EN_ESKI_YIL:
                    cikti.append({
                        "tablo": tablo, "anahtar": ak,
                        "id": satir[ak] if ak != "rowid" else satir["rowid"],
                        "kolon": kolon, "deger": str(deger),
                        "ait": _kime_ait(b, tablo, satir),
                        "oneri": _oneri(b, tablo, satir, kolon, deger),
                    })
    return cikti


def _gecerli(metin):
    """Kullanıcının yazdığı tarih kabul edilebilir mi?"""
    e = TARIH.match(metin)
    if not e or int(e.group(1)) < EN_ESKI_YIL:
        return False
    try:
        datetime.fromisoformat(metin.replace("T", " "))
    except ValueError:
        return False
    return True


def main():
    yol = _db.DB_YOLU
    if not yol.exists():
        sys.exit(f"lab.db bulunamadi: {yol}")
    b = sqlite3.connect(yol)
    b.row_factory = sqlite3.Row

    print(f"Veritabani: {yol}\n")
    bulunan = bulgular(b)
    if not bulunan:
        print(f"Yili {EN_ESKI_YIL}'den kucuk tarih yok. Duzeltilecek bir sey bulunamadi.")
        return 0

    print(f"{len(bulunan)} bozuk tarih bulundu:\n")
    for i, x in enumerate(bulunan, 1):
        ait = f"  ({x['ait']})" if x["ait"] else ""
        print(f"{i}. {x['tablo']}.{x['kolon']} = {x['deger']}{ait}")
        if x["oneri"]:
            print(f"   onerilen: {x['oneri']}")
        else:
            print("   onerilemiyor - dogru tarihi kendin yazman gerekiyor")
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "liste":
        print("Liste kipi: hicbir sey degistirilmedi.")
        return 0

    if not sys.stdin.isatty():
        print("Terminalden calistirilmadi, soru sorulamiyor. Hicbir sey degismedi.")
        return 0

    degisen = 0
    for x in bulunan:
        ait = f" ({x['ait']})" if x["ait"] else ""
        print(f"\n{x['tablo']}.{x['kolon']} = {x['deger']}{ait}")
        varsayilan = x["oneri"]
        if varsayilan:
            soru = f"  Enter = {varsayilan} yaz | baska tarih yaz | a = atla | q = cik: "
        else:
            soru = "  Dogru tarihi yaz (YYYY-AA-GG) | a = atla | q = cik: "
        cevap = input(soru).strip()
        if cevap.lower() == "q":
            break
        if cevap.lower() == "a" or (not cevap and not varsayilan):
            print("  atlandi")
            continue
        yeni = cevap or varsayilan
        if not _gecerli(yeni):
            print(f"  '{yeni}' gecerli bir tarih degil, atlandi")
            continue
        with _db.baglan() as k:
            k.execute(f"UPDATE {x['tablo']} SET {x['kolon']}=? "
                      f"WHERE {x['anahtar']}=?", (yeni, x["id"]))
        print(f"  yazildi: {yeni}")
        degisen += 1

    print(f"\n{degisen} kayit duzeltildi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
