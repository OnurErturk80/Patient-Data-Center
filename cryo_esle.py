"""Cryo haritası Excel'ini programdaki tüplere bağlar (v6.173).

Laboratuvarın kriyo haritası (tank / kanister / goblet başına kimin hangi
embriyosunun durduğu) Excel'de tutuluyor. Access kayıtları `aktar_access.py`
ile aktarılınca o tüpler programda açıldı ama **konumları boş** (Access'te
konum yoktu). Bu araç Excel'in her satırını programdaki tüpe bağlar ve
tüpün konumunu (Tank / Kanister / Goblet), taşıyıcı tipini ve rengini yazar.
Yeni tablo yok: Cryo Haritası ve `/cryo` zaten `tasiyici.konum_id`'den
besleniyor.

Kullanım (proje klasöründe):

    python3 cryo_esle.py liste  CRYO_HARITA.xlsx     # ne olacak, yazmaz
    python3 cryo_esle.py uygula CRYO_HARITA.xlsx     # "ESLE" onayıyla yazar

İkisi de `cryo_esle_rapor.txt` dosyasına satır satır rapor yazar (hasta
adı içerir -- depoya girmez, `.gitignore`). Terminale yalnızca sayılar.

Eşleştirme ölçüsü -- **isim tek başına yetmez**, üçü birden:

1. **Hasta**: Excel'in SOYAD + AD kelime kümesi programdaki `ad_soyad`'ın
   kelime kümesine eşit (sıra önemsiz; Excel'de soyad ve ad ayrı sütun).
   Aynı adlı birden çok hasta varsa eş adı ayırır; ayırmıyorsa belirsiz.
   Dosya numarası Excel'de yok (v6.127'de ölçüldü), ada mecburuz -- ama
   ad yalnızca **aday** veriyor, tüpü tarih ve içerik seçiyor.
2. **Dondurma günü**: Excel'in TARİH'i, tüpün vitrifikasyon günü.
3. **İçerik**: Excel'in HÜCRE'si ("D5 (3AA-4AB)", "OOSİT (3M2-1M1)",
   "3 M2 OOSİT") ile tüpteki örneklerin skoru/olgunluğu -- aynı çoklu küme.
   Yazım `aktar_access._skor_coz()` ile çözülüyor (Access notlarının
   sözlüğü; Excel de aynı elle yazılmış). Karşılaştırma gevşek: "8HG2" ile
   "8G2" aynı, MII ile M2 aynı.

Aynı hastanın aynı günkü Excel satırları ve program tüpleri **birlikte**
dağıtılıyor: birebir aynı içerikli iki tüp ile Excel'de aynı içerikli iki
satır varsa ikisi sırayla eşleşiyor -- programda o iki tüp birbirinden
ayırt edilemez (etiket Access'ten üretilmiş, konum boş), hangisine hangi
goblet yazıldığı fark etmez (v6.148'in "aynı tedavinin birebir aynı tüpleri
fark etmez" kuralı). Ama tüp sayısı satır sayısını aşıyorsa (Excel'de bir
satır, programda iki aynı tüp) belirsizdir: listelenir, yazılmaz.

Yazılmayan, raporda ayrı başlıkla listelenen durumlar: hasta programda yok
(2011-2018 kayıtları hiç aktarılmadı -- Access dosyası yok), aynı adlı
birden çok hasta, o gün tüp yok, içerik hiçbir tüple tutmuyor, tüp
programda zaten boşaltılmış/kullanılmış görünüyor, tüpe daha önce başka bir
konum yazılmış (elle girilmiş olabilir; ezilmiyor), iki Excel satırı aynı
tüpü istiyor. **Sahte tedavi/tüp açılmıyor**: eşleşmeyen satır için kayıt
üretmek istatistikleri bozar (v6.127'nin gerekçesi aynen geçerli).

Sperm sayfaları bu araçta yalnızca sayılıyor: Access'te sperm tablosu
yoktu, programda karşılığı olan sperm dondurma kaydı yok.

İkinci çalıştırma hiçbir şeyi değiştirmez: yazılmış konum "zaten yazılı"
sayılır. Değişiklikler `degisiklik_log`'a düşer (tablo `tasiyici`, alan
`konum`). Program açıkken de çalışır (`yazma_islemi()` kilidi).
"""

import collections
import datetime as _dt
import re
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)
import cryo_excel
import aktar_access       # `_skor_coz()`: skor yazımının tek sözlüğü

RAPOR = Path("cryo_esle_rapor.txt")

# Taşıyıcı tipleri: Excel'in VİAL sütunundan çıkan kod `liste_degeri`'nde
# yoksa ekleniyor (goc_042'nin v6.129'da geri alınan iki satırı).
TIP_ETIKETLERI = {"rapid_i": "Rapid-i", "vitrifit": "Vitrifit"}


# ------------------------------------------------------------------ içerik

def _norm(skor: str) -> str:
    """Skor yazımını karşılaştırılabilir hale getirir: "8HG2" -> "8G2",
    "MII" -> "M2", "MI" -> "M1"."""
    s = (skor or "").upper().replace("MII", "M2").replace("MI", "M1")
    s = re.sub(r"^(\d+)H", r"\1", s)
    return s


def _tup_skoru(b, sid: int) -> str:
    """Tüpteki bir örneğin kalitesi: blastokist skoru, yoksa cleavage yazımı,
    yoksa olgunluk. Aktarılmış tüplerde örnek başına tek değerlendirme var."""
    r = b.execute(
        "SELECT bl_skor FROM olay WHERE specimen_id=? AND tip='blastokist_degerlendirme' "
        "AND iptal_mi=0 AND bl_skor IS NOT NULL ORDER BY id DESC LIMIT 1", (sid,)).fetchone()
    if r:
        return r[0]
    r = b.execute(
        f"SELECT {_db.cl_hucre_ifadesi('x')} || COALESCE(x.cl_skor,'') FROM olay x "
        "WHERE x.specimen_id=? AND x.tip='cleavage_degerlendirme' AND x.iptal_mi=0 "
        "ORDER BY x.id DESC LIMIT 1", (sid,)).fetchone()
    if r and r[0]:
        return r[0]
    r = b.execute(
        "SELECT mat_deger FROM olay WHERE specimen_id=? AND tip='maturasyon_kontrolu' "
        "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (sid,)).fetchone()
    return (r[0] if r and r[0] else "") or "?"


_GRUP = re.compile(r"\(([^()]*)\)")
_YUMURTA_SAYI = re.compile(r"(\d+)\s*(?:ADET\s+)?(?:\*|X)?\s*(MII|MI|M2|M1|GV|MA)?\b")
_OLGUNLUK = {"MII": "M2", "M2": "M2", "MI": "M1", "M1": "M1", "GV": "GV"}


def _parantezsiz_yumurta(ic: str):
    """"3 M2 OOSİT", "2 M1 2 M2 OOSİT", "1 GV OOSİT", "3 OOSİT", "OOSİT 4MII"
    -> tek tüp; olgunluğu yazmayan yumurta "?" (sayı yine tutuyor)."""
    out = []
    for adet, mat in _YUMURTA_SAYI.findall(ic):
        out += [_OLGUNLUK.get(mat, "?")] * int(adet)
    return [sorted(out)] if out else None


def _uyar(istek, tup) -> bool:
    """Excel içeriği tüple tutuyor mu? "?" (okunamayan/olgunluğu yazılmamış
    öğe) her şeyi tutar; sayı ve bilinen öğeler birebir."""
    if len(istek) != len(tup):
        return False
    bilinen = collections.Counter(x for x in istek if x != "?")
    return not (bilinen - collections.Counter(tup))


# Excel'in kendi yazım alışkanlıkları (v6.176, haritanın 2019-2023 satırları):
# evre ile derece arasında boşluk ("MORULA G2", "KAV G3", "BİRLEŞME G1" --
# boşluktan bölününce iki "?" oluyordu), iki embriyo arasında yıldız
# ("3BB*3BB"; "3*KAVG3" ise sayı, dokunulmuyor), blastokist skoruna bitişik
# evre ("2CCKAVG3" -- `_skor_coz()` baştaki 2CC'yi okuyup KAVG3'ü atıyordu).
_EVRE_DERECE = re.compile(r"\b(MORULA|MOR|KAVİTASYON|KAV|BİRLEŞME|BİR)\s+(G\d)\b")
_YILDIZ_ARASI = re.compile(r"(?<=[A-Z])\*+(?=\d)")
_BITISIK_EVRE = re.compile(r"(\d[ABC]{2})(?=KAV|MOR|BİR)")


def _yazimi_duzelt(ic: str) -> str:
    ic = _EVRE_DERECE.sub(r"\1\2", ic)
    ic = _YILDIZ_ARASI.sub(" ", ic)
    return _BITISIK_EVRE.sub(r"\1 ", ic)


def excel_icerik(icerik: str):
    """HÜCRE metni -> [tüp içeriği, ...]; her tüp sıralı skor listesi, okunamayan
    parça "?" olur. Hiç okunamıyorsa None.

    Bir parantez = bir tüp (Access notlarıyla aynı yazım, v6.132). Parantezsiz
    "3 M2 OOSİT" tek tüp, üç MII yumurta. Morfoloji nitelemesi (HATCHİNG,
    OVAL, COLLAPSED -- `aktar_access._NITELIK`) ayrı embriyo değil, atlanıyor;
    "10HG2*" yıldızı da (v6.172'nin okumaları).
    """
    ic = _yazimi_duzelt((icerik or "").upper())
    yumurta = "OOS" in ic or "M2" in ic or "MII" in ic
    if not yumurta:
        ic = re.sub(r"\b(\d+)\s*ADET\s+", r"\1*", ic)     # "3 ADET MORULA G2"
    gruplar = _GRUP.findall(ic)
    if not gruplar:
        return _parantezsiz_yumurta(ic) if yumurta else None
    tupler = []
    for g in gruplar:
        parcalar = re.split(r"[\s,\-/]+", g.strip())
        out = []
        for p in parcalar:
            p = p.strip("*")
            if not p or aktar_access._NITELIK.match(aktar_access._sade(p)):
                continue
            # "3*KAVG3", "2X8HG1": aynı skordan N embriyo (Access okuyucusunun
            # kuralı, v6.173). Yumurtada "3*M2"yi `_skor_coz()` kendisi sayıyor.
            carpan = None if yumurta else re.match(r"^(\d+)[X*](\S+)$", p)
            z = aktar_access._skor_coz(carpan.group(2), yumurta=False) if carpan else None
            if z and z["tur"] in ("blast", "cleavage"):
                tek = (_norm(f'{z["hucre"]}{z["skor"]}') if z["tur"] == "cleavage"
                       else _norm(z["skor"]))
                out += [tek] * int(carpan.group(1))
                continue
            z = aktar_access._skor_coz(p, yumurta=yumurta)
            if not z:
                y = aktar_access._yuva_coz(p)
                if y:
                    out.append(_norm(_db.BIRLESME + (y.get("skor") or "")))
                    continue
                out.append("?")
                continue
            if z["tur"] == "oosit":
                mat = z["mat"]
                out += [_norm("M2" if mat == "mii" else "GV" if mat == "gv"
                              else "M1" if mat == "mi" else "?")] * z["adet"]
            elif z["tur"] == "cleavage":
                out.append(_norm(f'{z["hucre"]}{z["skor"]}'))
            else:
                out.append(_norm(z["skor"]))
        if out:
            tupler.append(sorted(out))
    return tupler or None


# -------------------------------------------------------------- veritabanı

def hastalar(b) -> dict:
    """{ad kelime kümesi: [(hasta id, eş kelime kümesi, dosya no), ...]}"""
    idx = collections.defaultdict(list)
    for r in b.execute("SELECT id, ad_soyad, es_adi, dosya_no FROM hasta WHERE lab_id=?",
                       (_db.LAB_ID,)):
        idx[cryo_excel.kelimeler(r["ad_soyad"])].append(
            (r["id"], cryo_excel.kelimeler(r["es_adi"]), r["dosya_no"], r["es_adi"] or ""))
    return idx


def tupler(b) -> dict:
    """{hasta id: [tüp sözlüğü, ...]} -- embriyo/yumurta tüpleri, dondurma
    günü ve içerikleriyle. Sperm tüplerinin `olay` satırı yok, gelmiyorlar."""
    sonuc = collections.defaultdict(list)
    q = ("SELECT h.id hid, t.id tid, t.etiket, t.durum, t.tip, t.renk, t.konum_id, "
         "k.tam_yol, substr(MIN(o.zaman),1,10) gun, GROUP_CONCAT(s.id) ornekler, "
         "substr(MIN(vc.opu_zamani),1,10) opu "
         "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
         "JOIN cycle c ON c.id=s.cycle_id JOIN hasta h ON h.id=c.hasta_id "
         f"LEFT JOIN cycle vc ON vc.id={_db.vit_tedavisi('o')} "
         "JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
         "LEFT JOIN konum k ON k.id=t.konum_id "
         "WHERE o.tip='vitrifikasyon' AND o.iptal_mi=0 AND h.lab_id=? "
         "GROUP BY t.id")
    for r in b.execute(q, (_db.LAB_ID,)):
        skorlar = sorted(_norm(_tup_skoru(b, sid)) for sid in r["ornekler"].split(","))
        sonuc[r["hid"]].append({
            "tid": r["tid"], "etiket": r["etiket"], "durum": r["durum"],
            "tip": r["tip"], "renk": r["renk"], "konum_id": r["konum_id"],
            "tam_yol": r["tam_yol"], "gun": r["gun"], "opu": r["opu"],
            "skorlar": skorlar})
    return sonuc


# ------------------------------------------------------------- eşleştirme

# Sınıflar: raporun başlıkları bu sırayla. `yazilir` olanlar `uygula`'da
# konum alır.
SINIFLAR = [
    ("eslesti", "Eşleşti -- konum yazılacak", True),
    ("zaten", "Zaten bu konum yazılı (ikinci çalıştırma)", False),
    ("ayni_dagitildi", "Aynı içerikli tüpler goblete sırayla dağıtıldı "
                       "(tüpler birbirinden ayırt edilemez, sıra fark etmez)", True),
    ("sayiyla", "İçerik tam okunamadı, sayı ve okunan kısmı tutuyor", True),
    ("ad_cok_gun_ayirdi", "Aynı adlı birden çok hasta; o gün tüpü olan tek -- o alındı", True),
    ("farkli_konum", "Tüpe daha önce BAŞKA bir konum yazılmış -- ezilmedi", False),
    ("bosaltilmis", "Tüp programda boşaltılmış/kullanılmış görünüyor -- Excel tankta diyor", False),
    ("es_tutmuyor", "Ad tutuyor, eş adı tutmuyor -- yazılmadı (tüp bulunduysa yazılı)", False),
    ("tutmuyor", "O gün tüp var ama içerik tutmuyor (ya da Excel'de tüpten çok satır)", False),
    ("cakisma", "İki Excel satırı aynı tüpü istiyor", False),
    ("opu_gunu", "Tarih programdakinden farklı; Excel'in günü OPU'dan sayılınca "
                 "(D5 = OPU + 5) aynı tedavi, içerik tutuyor", True),
    ("gun_yok", "Hasta programda var, o gün dondurma tüpü yok", False),
    ("tup_yok", "Hasta programda var, hiç dondurma tüpü yok", False),
    ("hasta_cok", "Aynı adlı birden çok hasta, eş adı ve tarih ayırmıyor", False),
    ("hasta_yok", "Hasta programda yok", False),
    ("tarihsiz", "Excel'de tarih yok/okunamadı", False),
]
YAZILIR = {k for k, _, y in SINIFLAR if y}


def _benzer(ad, idx):
    """Programda yok -- en az iki kelimesi ortak TEK bir hasta varsa ipucu."""
    yakin = [(k, v) for k, v in idx.items() if len(k & ad) >= 2 and k != ad]
    if len(yakin) == 1:
        (k, v), = yakin
        return f"benzer ad programda: {' '.join(sorted(k))} (dosya {v[0][2]})"
    return ""


def _hasta_bul(satir, idx, tup):
    """-> (hasta id, dosya no, bayrak|None, not). Bayrak: 'hasta_yok' /
    'hasta_cok' (kesin karar yok), 'es_tutmuyor' / 'ad_cok_gun_ayirdi'
    (hasta seçildi, sınıf raporda bunu söyleyecek)."""
    ad = cryo_excel.kelimeler((satir["soyad"] or "") + " " + (satir["ad"] or ""))
    adaylar = idx.get(ad, [])
    if not adaylar:
        return None, None, "hasta_yok", _benzer(ad, idx)
    es = cryo_excel.kelimeler(satir["es_adi"])
    bayrak = None
    if len(adaylar) > 1:
        daralt = [a for a in adaylar if es and a[1] and (es & a[1])]
        if len(daralt) == 1:
            adaylar = daralt
        else:
            # Eş adı ayırmadı: o gün tüpü olan tek aday varsa tarih ayırır.
            gun = satir["tarih"]
            gunlu = [a for a in adaylar
                     if gun and any(t["gun"] == gun for t in tup.get(a[0], []))]
            if len(gunlu) != 1:
                return None, None, "hasta_cok", f"{len(adaylar)} aynı adlı hasta"
            adaylar, bayrak = gunlu, "ad_cok_gun_ayirdi"
    hid, hes, dosya, hes_metni = adaylar[0]
    if es and hes and not (es & hes):
        bayrak = "es_tutmuyor"
        return hid, dosya, bayrak, f"programdaki eş adı: {hes_metni}"
    return hid, dosya, bayrak, ""


def _dagit(istekler, adaylar):
    """Aynı hasta + aynı günün Excel istekleri (satır, tüp içeriği) ile program
    tüplerini eşler. -> [(istek, tüp, sınıf)]; eşleşmeyen istek tüpsüz döner.

    Sıra: içeriği tek bir tüple tutan istekler; sonra aynı içerikli istekler,
    tutan tüp sayısı yettiği sürece sırayla (birebir aynı tüpler arasında
    seçim yapmak bilgi kaybetmez); sonra okunamayan içerik, kalan tek tüp.
    Kalan istekler "tutmuyor".
    """
    kalan = _sirala(adaylar)
    sonuc, acik = [], []
    for istek in istekler:
        ic = istek[1]
        if ic is None:
            acik.append(istek)
            continue
        uyan = [t for t in kalan if _uyar(ic, t["skorlar"])]
        if len(uyan) == 1:
            kalan.remove(uyan[0])
            sonuc.append((istek, uyan[0], "sayiyla" if "?" in ic else "eslesti"))
        else:
            acik.append(istek)
    gruplar = collections.defaultdict(list)
    for istek in acik:
        gruplar[tuple(istek[1]) if istek[1] is not None else None].append(istek)
    for ic, grup in gruplar.items():
        if ic is None:
            continue
        uyan = [t for t in kalan if _uyar(list(ic), t["skorlar"])]
        for istek in grup:
            if uyan:
                t = uyan.pop(0)
                kalan.remove(t)
                sonuc.append((istek, t, "sayiyla" if "?" in ic else "ayni_dagitildi"))
            else:
                sonuc.append((istek, None, "tutmuyor"))
    okunamayan = gruplar.get(None, [])
    if len(okunamayan) == 1 and len(kalan) == 1:
        sonuc.append((okunamayan[0], kalan.pop(), "sayiyla"))
    else:
        for istek in okunamayan:
            sonuc.append((istek, None, "tutmuyor"))
    return sonuc


def _sirala(adaylar):
    """Dolu tüpler önce (Excel tankta diyor; boşaltılmış ikizini seçmek yanlış
    uyarı üretir), sonra etiket sırası -- dağıtım kararlı olsun (aynı
    çalıştırma aynı sonucu versin)."""
    return sorted(adaylar, key=lambda t: (t["durum"] != "dolu", t["etiket"], t["tid"]))


_EXCEL_GUN = re.compile(r"^\s*D\s*(\d)\b")


def _excel_opu(s):
    """Excel satırının OPU günü (v6.177, kullanıcının cevabı, 2026-09-25:
    "Excel'de dondurma günü yazıyor. 5. gün dondurma ise OPU gününden 5 gün
    sonra"). HÜCRE "D5 (...)" -> TARİH − 5; yumurta OPU günü dondurulur ->
    TARİH. Günü yazmayan embriyo satırında None."""
    m = _EXCEL_GUN.match(s["icerik"] or "")
    ic = (s["icerik"] or "").upper()
    if m:
        gun = int(m.group(1))
    elif "OOS" in ic or "M2" in ic or "MII" in ic:
        gun = 0
    else:
        return None
    try:
        return (_dt.date.fromisoformat(s["tarih"]) - _dt.timedelta(days=gun)).isoformat()
    except (TypeError, ValueError):
        return None


def esle(satirlar, idx, tup) -> list:
    """Excel satırları -> [(satır, sınıf, tüp|None, ek not)]"""
    sonuc = []
    gunluk = collections.defaultdict(list)     # (hasta, gün) -> istekler
    bayraklar = {}
    for s in satirlar:
        if s["kategori"] == "sperm":
            continue
        hid, dosya, bayrak, ek = _hasta_bul(s, idx, tup)
        s["dosya_no"] = dosya
        if hid is None:
            sonuc.append((s, bayrak, None, ek))
            continue
        bayraklar[id(s)] = (bayrak, ek)
        if not s["tarih"]:
            sonuc.append((s, "tarihsiz", None, s.get("tarih_notu") or ""))
            continue
        hastanin = tup.get(hid, [])
        es_notu = f"; {ek}" if bayrak == "es_tutmuyor" else ""
        if not hastanin:
            sonuc.append((s, "tup_yok", None, es_notu.strip("; ")))
            continue
        anahtar = (hid, "gun", s["tarih"])
        if not any(t["gun"] == s["tarih"] for t in hastanin):
            # Tarih tutmuyor: programdaki dondurma günü Access notundan
            # (OPU + nottaki gün) kurulmuştu, gün yanlış okunmuş olabilir.
            # Excel'in kendi günüyle OPU'ya dönüp aynı tedaviyi ara (v6.177).
            opu = _excel_opu(s)
            if opu and any(t["opu"] == opu for t in hastanin):
                anahtar = (hid, "opu", opu)
            else:
                gunler = sorted({t["gun"] for t in hastanin})
                sonuc.append((s, "gun_yok", None,
                              "programdaki dondurma günleri: " + ", ".join(gunler) + es_notu))
                continue
        icerik = excel_icerik(s["icerik"])
        if icerik:
            for tek in icerik:
                gunluk[anahtar].append((s, tek))
        else:
            gunluk[anahtar].append((s, None))
    kullanilan = {}
    # Önce günü tutanlar: OPU'dan bulunan satır, günü tutan satırın tüpünü
    # almasın.
    for (hid, olcu, deger), istekler in sorted(gunluk.items(), key=lambda x: x[0][1] != "gun"):
        if olcu == "gun":
            adaylar = [t for t in tup[hid] if t["gun"] == deger]
        else:
            adaylar = [t for t in tup[hid] if t["opu"] == deger and t["tid"] not in kullanilan]
        for (s, ic), t, sinif in _dagit(istekler, adaylar):
            if t is not None and olcu == "opu":
                sinif = "opu_gunu"
            bayrak, ek = bayraklar.get(id(s), (None, ""))
            if t is None:
                sonuc.append((s, "es_tutmuyor" if bayrak == "es_tutmuyor" else sinif, None,
                              "tüpler: " + "; ".join(
                                  f'{a["etiket"]} [{"-".join(a["skorlar"])}]' for a in adaylar)))
                continue
            if t["tid"] in kullanilan:
                sonuc.append((s, "cakisma", t, f"aynı tüpü isteyen: {kullanilan[t['tid']]}"))
                continue
            kullanilan[t["tid"]] = _yer(s)
            if bayrak == "es_tutmuyor":
                sonuc.append((s, "es_tutmuyor", t, f"{ek}; eşleşme sınıfı: {sinif}"))
            elif t["durum"] != "dolu":
                sonuc.append((s, "bosaltilmis", t, f"program: {t['durum']}"))
            elif t["tam_yol"] and t["tam_yol"] == _tam_yol(s):
                sonuc.append((s, "zaten", t, ""))
            elif t["tam_yol"]:
                sonuc.append((s, "farkli_konum", t, f"programdaki konum: {t['tam_yol']}"))
            elif bayrak == "ad_cok_gun_ayirdi":
                sonuc.append((s, "ad_cok_gun_ayirdi", t, f"eşleşme sınıfı: {sinif}"))
            else:
                sonuc.append((s, sinif, t, ""))
    return sonuc


def _seviyeler(s):
    return [s["tank"] or "", s["kanister"] or "", s["goblet"] or "", ""]


def _tam_yol(s):
    return " / ".join(x for x in _seviyeler(s) if x)


def _yer(s):
    return f'{s["sayfa"]} satır {s["satir"]} ({_tam_yol(s)})'


# ------------------------------------------------------------------- rapor

def _satir_metni(s, t, ek):
    ad = f'{s["soyad"]} {s["ad"]}'.strip()
    es = f' (eşi {s["es_adi"]})' if s["es_adi"] else ""
    dosya = f' dosya {s["dosya_no"]}' if s.get("dosya_no") else ""
    tup = (f' -> tüp {t["etiket"]} [{"-".join(t["skorlar"])}]' if t else "")
    ek = f"  | {ek}" if ek else ""
    return (f'{_yer(s):40} | {ad}{es}{dosya} | {s["tarih"] or "tarih?"} | '
            f'{s["icerik"]} | {s["vial_metni"]}{tup}{ek}')


def rapor_yaz(sonuc, satirlar, uyarilar, kip):
    sayac = collections.Counter(sinif for _, sinif, _, _ in sonuc)
    sperm = sum(1 for s in satirlar if s["kategori"] == "sperm")
    satirlar_c = [f"CRYO HARİTASI EŞLEŞTİRME RAPORU -- {kip} -- "
                  f"{_dt.datetime.now().isoformat(' ', 'seconds')}",
                  f"Excel: {len(satirlar)} satır ({len(satirlar) - sperm} embriyo/yumurta, "
                  f"{sperm} sperm -- sperm bu araçta eşleştirilmiyor)", ""]
    for u in uyarilar:
        satirlar_c.append(f"UYARI (Excel): {u}")
    satirlar_c.append("")
    for kod, baslik, yazilir in SINIFLAR:
        n = sayac.get(kod, 0)
        satirlar_c.append(f"== {baslik}: {n}" + ("  [yazılır]" if yazilir else ""))
        if not n:
            continue
        yillar = collections.Counter((s["tarih"] or "????")[:4] for s, k, _, _ in sonuc if k == kod)
        satirlar_c.append("   yıl: " + ", ".join(f"{y}: {c}" for y, c in sorted(yillar.items())))
        for s, k, t, ek in sonuc:
            if k == kod:
                satirlar_c.append("   " + _satir_metni(s, t, ek))
        satirlar_c.append("")
    RAPOR.write_text("\n".join(satirlar_c) + "\n", encoding="utf-8")
    return sayac, sperm


def ozet_bas(sayac, sperm, toplam):
    print(f"Excel: {toplam} satır, {sperm} sperm (eşleştirilmiyor), "
          f"{toplam - sperm} embriyo/yumurta.")
    for kod, baslik, yazilir in SINIFLAR:
        n = sayac.get(kod, 0)
        if n:
            print(f"  {n:5}  {baslik}" + ("  [yazılır]" if yazilir else ""))
    yazilacak = sum(sayac.get(k, 0) for k in YAZILIR)
    print(f"Yazılacak: {yazilacak} tüp. Ayrıntı: {RAPOR}")
    return yazilacak


# ------------------------------------------------------------------ yazma

def _kullanici_id(b):
    for kosul in ("AND rol='yonetici'", ""):
        r = b.execute(f"SELECT id FROM kullanici WHERE lab_id=? AND aktif_mi=1 "
                      f"{kosul} ORDER BY id LIMIT 1", (_db.LAB_ID,)).fetchone()
        if r:
            return r[0]
    sys.exit("Aktif kullanici yok -- once bir kullanici ac (kullanici.py).")


def _liste_kodu_ekle(b, liste, kod, etiket):
    if b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=? AND liste_adi=? AND kod=?",
                 (_db.LAB_ID, liste, kod)).fetchone():
        return False
    sira = b.execute("SELECT COALESCE(MAX(sira),0)+1 FROM liste_degeri "
                     "WHERE lab_id=? AND liste_adi=?", (_db.LAB_ID, liste)).fetchone()[0]
    b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (?,?,?,?,?)", (_db.LAB_ID, liste, kod, etiket, sira))
    return True


def uygula(sonuc) -> dict:
    yazilanlar = [(s, t) for s, k, t, _ in sonuc if k in YAZILIR and t]
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        kid = _kullanici_id(b)
        simdi = _dt.datetime.now().isoformat(" ", "seconds")
        renkler = {r[0] for r in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_renk'",
            (_db.LAB_ID,))}
        tipler = {r[0] for r in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_tipi'",
            (_db.LAB_ID,))}
        for kod, etiket in TIP_ETIKETLERI.items():
            if any(s["tip"] == kod for s, _ in yazilanlar) and \
                    _liste_kodu_ekle(b, "tasiyici_tipi", kod, etiket):
                tipler.add(kod)
                sayac["tip_kodu_eklendi"] += 1

        def logla(tid, alan, eski, yeni):
            b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                      "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                      (_db.LAB_ID, "tasiyici", str(tid), alan, eski, yeni, kid, simdi))

        for s, t in yazilanlar:
            konum_id = _db.konum_bul_veya_olustur(_seviyeler(s), b)
            b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?", (konum_id, t["tid"]))
            b.execute("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))
            logla(t["tid"], "konum", t["tam_yol"], _tam_yol(s))
            sayac["konum"] += 1
            if s["tip"] and s["tip"] in tipler and s["tip"] != t["tip"]:
                b.execute("UPDATE tasiyici SET tip=? WHERE id=?", (s["tip"], t["tid"]))
                logla(t["tid"], "tip", t["tip"], s["tip"])
                sayac["tip"] += 1
            if s["renk"] and s["renk"] in renkler and s["renk"] != t["renk"]:
                b.execute("UPDATE tasiyici SET renk=? WHERE id=?", (s["renk"], t["tid"]))
                logla(t["tid"], "renk", t["renk"], s["renk"])
                sayac["renk"] += 1
    return sayac


# ------------------------------------------------------------------- main

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("liste", "uygula"):
        sys.exit(__doc__)
    kip, dosya = sys.argv[1], Path(sys.argv[2])
    if not dosya.is_file():
        sys.exit(f"{dosya} bulunamadı.")
    if not _db.DB_YOLU.exists():
        sys.exit("lab.db bulunamadi.")
    print(f"Veritabanı: {_db.DB_YOLU}")
    try:
        cozum = cryo_excel.coz(dosya.read_bytes())
    except cryo_excel.Hata as e:
        sys.exit(f"Excel okunamadı: {e}")
    with _db.baglan() as b:
        idx = hastalar(b)
        tup = tupler(b)
    print(f"Program: {sum(len(v) for v in idx.values())} hasta, "
          f"{sum(len(v) for v in tup.values())} dondurma tüpü.")
    sonuc = esle(cozum["satirlar"], idx, tup)
    sayac, sperm = rapor_yaz(sonuc, cozum["satirlar"], cozum["uyarilar"], kip)
    yazilacak = ozet_bas(sayac, sperm, len(cozum["satirlar"]))
    if kip == "liste":
        return
    if not yazilacak:
        print("Yazılacak bir şey yok.")
        return
    print(f"\n{yazilacak} tüpe konum yazılacak. Devam için ESLE yazın:")
    if input("> ").strip() != "ESLE":
        print("Vazgeçildi, hiçbir şey yazılmadı.")
        return
    y = uygula(sonuc)
    print(f"Yazıldı: {y['konum']} tüpe konum, {y['tip']} tüpe taşıyıcı tipi, "
          f"{y['renk']} tüpe renk"
          + (f"; {y['tip_kodu_eklendi']} yeni taşıyıcı tipi listeye eklendi"
             if y["tip_kodu_eklendi"] else "") + ".")


if __name__ == "__main__":
    main()
