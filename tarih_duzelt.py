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

import sqlite3
import sys
from datetime import datetime

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)

# Yılı bundan küçükse yazım hatası sayılır. Doğum tarihleri 1900'lerde
# olabilir, o yüzden sınır 2000 değil 1900.
EN_ESKI_YIL = 1900

# Üst sınır bu yıldan itibaren beş yıl. `planlanan_tarih` bilerek gelecekte
# olabiliyor (ileri tarihli cycle) ve bebeğin doğum tarihi de dokuz ay ileri;
# beş yıl ikisine de bol bol yeter, `20026` gibi bir yazım hatasını yakalar.
EN_YENI_YIL = datetime.now().year + 5

# Kaydın girildiği yıl bu tarihler için ölçü olmaz.
ONERISIZ = {"dogum_tarihi", "es_dogum_tarihi", "dogum_zamani"}

# Göç defteri taranmıyor. İki sebep: (1) `goc.py` zaten uygulanmış bir göç
# için bilerek `"onceden"` yazıyor -- tarih değil, işaret; (2) o tabloyu
# düzenlemeye davet etmek tehlikeli, göçün yeniden çalışmasına ya da
# atlanmasına yol açar. Klinik veri değil, çalıştırıcının kendi kaydı.
ATLA_TABLO = {"goc_kaydi"}

SEBEP = {
    "yil_kucuk": "yili cok eski",
    "yil_buyuk": "yili cok ileri",
    "okunamadi": "tarih olarak okunamiyor",
}


def _coz(deger):
    """Değeri tarihe çevirir; çevrilemezse None.

    Yalnızca "yılı küçük mü" diye bakmak yetmiyor: `26-09-04` ya da
    `04.09.2026` gibi bir değer o denetimden sessizce geçer. Program böyle
    bir şey yazmaz ama elle düzeltme, göç ya da başka bir araç yazabilir --
    ve buranın işi tam da sessiz duran bozuk veriyi bulmak.
    """
    m = str(deger).strip().replace("T", " ")
    try:
        return datetime.fromisoformat(m)
    except ValueError:
        return None


def _tarih_kolonlari(b):
    """Tarih tutan metin kolonları: adında 'tarih' ya da 'zaman' geçenler.

    Tipe de bakılıyor — `gun`, `stim_gun_sayisi` gibi sayı kolonları adından
    değil tipinden eleniyor.
    """
    for t in [r[0] for r in b.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]:
        if t in ATLA_TABLO:
            continue
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


def _kayit_yili(b, satir):
    """Kaydın girildiği yıl: kendi `olusturma_zamani`'ndan, yoksa cycle'ından."""
    for kaynak in ("olusturma_zamani",):
        if kaynak in satir.keys() and satir[kaynak]:
            d = _coz(satir[kaynak])
            if d and EN_ESKI_YIL <= d.year <= EN_YENI_YIL:
                return d.year
    if "cycle_id" in satir.keys() and satir["cycle_id"]:
        c = b.execute("SELECT olusturma_zamani FROM cycle WHERE id=?",
                      (satir["cycle_id"],)).fetchone()
        if c and c["olusturma_zamani"]:
            d = _coz(c["olusturma_zamani"])
            if d and EN_ESKI_YIL <= d.year <= EN_YENI_YIL:
                return d.year
    return None


def _oneri(b, tablo, satir, kolon, deger, cozulen):
    """Aynı gün ve saat, yılı kaydın oluşturma yılından. Kuramazsa None.

    Öneri **ayrıştırılmış tarihten** kuruluyor, dizginin ilk dört hanesini
    değiştirerek değil: `20026-09-04`'te ilk dört hane yılı vermiyor.
    Okunamayan değere öneri yapılmıyor — gün ve ay da belirsiz.
    """
    if kolon in ONERISIZ or cozulen is None:
        return None
    yil = _kayit_yili(b, satir)
    if yil is None:
        return None
    try:
        y = cozulen.replace(year=yil)
    except ValueError:              # 29 Şubat, hedef yıl artık yıl değil
        return None
    # Saati olmayan tarih (dogum_tarihi, planlanan_tarih) saatsiz kalsın.
    return (y.strftime("%Y-%m-%d") if len(str(deger).strip()) <= 10
            else y.isoformat(" ", "seconds"))


def bulgular(b):
    """Makul olmayan bütün tarihler: yılı çok eski, çok ileri ya da okunamayan."""
    cikti = []
    for tablo, kolonlar in _tarih_kolonlari(b):
        ak = _anahtar(b, tablo)
        kosul = " OR ".join(f"{k} IS NOT NULL" for k in kolonlar)
        for satir in b.execute(f"SELECT rowid, * FROM {tablo} WHERE {kosul}"):
            for kolon in kolonlar:
                deger = satir[kolon]
                if not deger:
                    continue
                d = _coz(deger)
                if d is None:
                    sebep = "okunamadi"
                elif d.year < EN_ESKI_YIL:
                    sebep = "yil_kucuk"
                elif d.year > EN_YENI_YIL:
                    sebep = "yil_buyuk"
                else:
                    continue
                cikti.append({
                    "tablo": tablo, "anahtar": ak,
                    "id": satir[ak] if ak != "rowid" else satir["rowid"],
                    "kolon": kolon, "deger": str(deger), "sebep": sebep,
                    "ait": _kime_ait(b, tablo, satir),
                    "oneri": _oneri(b, tablo, satir, kolon, deger, d),
                })
    return cikti


def _gecerli(metin):
    """Kullanıcının yazdığı tarih kabul edilebilir mi?"""
    d = _coz(metin)
    return d is not None and EN_ESKI_YIL <= d.year <= EN_YENI_YIL


def main():
    yol = _db.DB_YOLU
    if not yol.exists():
        sys.exit(f"lab.db bulunamadi: {yol}")
    b = sqlite3.connect(yol)
    b.row_factory = sqlite3.Row

    print(f"Veritabani: {yol}\n")
    bulunan = bulgular(b)
    if not bulunan:
        print(f"Butun tarihler {EN_ESKI_YIL}-{EN_YENI_YIL} arasinda ve okunabiliyor.")
        print("Duzeltilecek bir sey bulunamadi.")
        return 0

    print(f"{len(bulunan)} bozuk tarih bulundu:\n")
    for i, x in enumerate(bulunan, 1):
        ait = f"  ({x['ait']})" if x["ait"] else ""
        print(f"{i}. {x['tablo']}.{x['kolon']} = {x['deger']}{ait}")
        print(f"   sebep   : {SEBEP[x['sebep']]}")
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
        print(f"\n{x['tablo']}.{x['kolon']} = {x['deger']}{ait}"
              f"  -- {SEBEP[x['sebep']]}")
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
