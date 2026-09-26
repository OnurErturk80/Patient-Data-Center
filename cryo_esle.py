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
    python3 cryo_esle.py yeni_hasta CRYO_HARITA.xlsx # 2018 öncesi, programda
                                                     # olmayan hastaları açar
                                                     # ("HASTA" onayıyla, v6.179)
    python3 cryo_esle.py sperm CRYO_HARITA.xlsx      # sperm satırlarını açar
                                                     # ("SPERM" onayıyla, v6.180)
    python3 cryo_esle.py eksik CRYO_HARITA.xlsx      # programda dolu, Excel'de
                                                     # olmayan tüpler -- yazmaz
                                                     # (v6.182)
    python3 cryo_esle.py onar CRYO_HARITA.xlsx       # v6.188'e kadarki yanlış
                                                     # okumanın yazdığı konumları
                                                     # ve boş renkleri onarır
                                                     # ("ONAR" onayıyla)
    python3 cryo_esle.py yerlesim CRYO_HARITA.xlsx   # tank düzeni: bütün
                                                     # gobletler + Excel kaydı
                                                     # ("YERLESIM", v6.189)

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

Sperm satırları `liste`/`uygula`'da yalnızca sayılıyor (Access'te sperm
tablosu yoktu, bağlanacak tüp yok); `sperm` kipi onları kayıt olarak açar
(v6.180, aşağıda).

İkinci çalıştırma hiçbir şeyi değiştirmez: yazılmış konum "zaten yazılı"
sayılır. Değişiklikler `degisiklik_log`'a düşer (tablo `tasiyici`, alan
`konum`). Program açıkken de çalışır (`yazma_islemi()` kilidi).
"""

import collections
import datetime as _dt
import hashlib
import re
import sys
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)
import cryo_excel
import aktar_access       # `_skor_coz()`: skor yazımının tek sözlüğü
import yerlesim as _yerlesim   # yer adlarının karşılaştırma anahtarı (v6.189)

RAPOR = Path("cryo_esle_rapor.txt")

# Taşıyıcı tipleri: Excel'in VİAL sütunundan çıkan kod `liste_degeri`'nde
# yoksa ekleniyor (goc_042'nin v6.129'da geri alınan iki satırı).
TIP_ETIKETLERI = {"rapid_i": "Rapid-i", "vitrifit": "Vitrifit"}
# Renkler de öyle (v6.188): laboratuvar pembe straw kullanıyor, programın
# renk listesinde yoktu.
RENK_ETIKETLERI = {"pembe": "Pembe"}


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


_MAT_KODU = {"MII": "mii", "M2": "mii", "MI": "mi", "M1": "mi", "GV": "gv"}


def _parantezsiz_yumurta(ic: str):
    """"3 M2 OOSİT", "2 M1 2 M2 OOSİT", "1 GV OOSİT", "3 OOSİT", "OOSİT 4MII"
    -> tek tüp; olgunluğu yazmayan yumurta olgunluksuz (sayı yine tutuyor)."""
    out = []
    for adet, mat in _YUMURTA_SAYI.findall(ic):
        out += [{"tur": "oosit", "mat": _MAT_KODU.get(mat)} for _ in range(int(adet))]
    return [out] if out else None


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
# 2011-2017'nin yazımı (v6.179, kullanıcının cevapları, 2026-09-25):
# "4H G1" hücre ile derece arasında boşluk; "2G1" = iki G1 embriyo (hücre
# sayısı yazılmamış -- "2 hücreli" DEĞİL); "10H" / "10H%5" = 10 hücreli, %5
# fragmantasyon; "UE" = uneven, önündeki embriyonun niteliği; "KAVKAV" = iki
# kavitasyon; "7OOSİT" = yedi yumurta.
_HUCRE_DERECE = re.compile(r"(\d+H)\s+(G\d)\b")
_ADETLI_DERECE = re.compile(r"^(\d*)G(\d)$")
_HUCRE_FRAG = re.compile(r"^(\d+)H(?:%(\d+))?$")
_KAV_TEKRAR = re.compile(r"^(?:KAV){2,}$")
_ADETLI_OOSIT = re.compile(r"^(\d+)OOS")
_ADET_BOSLUK = re.compile(r"(?<![\dH.,])(\d+)\s+(G\d)\b")      # "2 G1"
_ADETLI_EVRE = re.compile(r"^(\d+)(MORULA|MOR|KAV)(G\d)?$")        # "2MOR"
# Parantezsiz embriyo satırında tüpün öğesi olmayan sözler: "D3 1G3",
# "5.GÜN 4AA 4AA BİRARADA", "G1 BLAST".
_PARANTEZSIZ_ATLA = re.compile(r"\bD\d\b|\d+\s*[.,]\s*GÜN|\bBİRARADA\b|\bBLAST\b")


def _yazimi_duzelt(ic: str) -> str:
    ic = _EVRE_DERECE.sub(r"\1\2", ic)
    ic = re.sub(r"GRD(\d)", r"G\1", ic)                       # "4H GRD1"
    ic = _HUCRE_DERECE.sub(r"\1\2", ic)
    ic = _ADET_BOSLUK.sub(r"\1\2", ic)
    ic = _YILDIZ_ARASI.sub(" ", ic)
    return _BITISIK_EVRE.sub(r"\1 ", ic)


def excel_ogeleri(icerik: str):
    """HÜCRE metni -> [tüp, ...]; her tüp öğe listesi, öğe `aktar_access`
    yazımında (`_skor_coz()`/`_yuva_coz()`'ün sözlüğü; yumurtada tek tek
    `{"tur": "oosit", "mat": ...}`; okunamayan parça `{"tur": "taninmadi"}`).
    Hiç okunamıyorsa None. `excel_icerik()` karşılaştırma için bunu metne
    çeviriyor, `yeni_hasta` kipi (v6.179) aynı öğelerden tüp açıyor -- iki
    ayrı okuyucu olsaydı açılan tüp eşleştirmenin okuduğunu tutmayabilirdi.

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
    if not gruplar and yumurta:
        return _parantezsiz_yumurta(ic)
    parantezsiz = not gruplar
    if parantezsiz:
        # Parantezsiz embriyo (v6.179): bütün hücre bir tüp -- ama yalnızca
        # en az bir öğesi tanınıyorsa ("EJAKÜLAT", "PGT", "D3ÜST3" tüp değil).
        kalan = _PARANTEZSIZ_ATLA.sub(" ", ic).strip()
        if not kalan or cryo_excel.kategori_coz(ic) == "sperm":
            return None
        gruplar = [kalan]
    tupler = []
    for g in gruplar:
        parcalar = re.split(r"[\s,\-/]+", g.strip())
        out = []
        for p in parcalar:
            p = p.strip("*")
            if not p or aktar_access._NITELIK.match(aktar_access._sade(p)):
                continue
            if p == "UE":
                if out and out[-1]["tur"] == "cleavage":
                    out[-1]["simetri"] = "esitsiz"
                    out[-1]["ham"] += " UE"
                continue
            m = _ADETLI_DERECE.match(p) if not yumurta else None
            if m:
                out += [{"tur": "embriyo", "skor": f"G{m.group(2)}", "ham": p}
                        for _ in range(int(m.group(1) or 1))]
                continue
            m = _HUCRE_FRAG.match(p) if not yumurta else None
            if m:
                out.append({"tur": "cleavage", "hucre": int(m.group(1)), "skor": None,
                            "frag": int(m.group(2)) if m.group(2) else None, "ham": p})
                continue
            m = _ADETLI_EVRE.match(p) if not yumurta else None
            if m and aktar_access._skor_coz(m.group(2) + (m.group(3) or "")):
                z = aktar_access._skor_coz(m.group(2) + (m.group(3) or ""))
                out += [dict(z, ham=p) for _ in range(int(m.group(1)))]
                continue
            if not yumurta and _KAV_TEKRAR.match(p):
                out += [dict(aktar_access._skor_coz("KAV"), ham=p)
                        for _ in range(len(p) // 3)]
                continue
            m = _ADETLI_OOSIT.match(p) if yumurta else None
            if m:
                out += [{"tur": "oosit", "mat": None} for _ in range(int(m.group(1)))]
                continue
            # "3*KAVG3", "2X8HG1": aynı skordan N embriyo (Access okuyucusunun
            # kuralı, v6.173). Yumurtada "3*M2"yi `_skor_coz()` kendisi sayıyor.
            carpan = None if yumurta else re.match(r"^(\d+)[X*](\S+)$", p)
            if carpan and re.match(r"^G\d$", carpan.group(2)):      # "2XG1"
                out += [{"tur": "embriyo", "skor": carpan.group(2), "ham": p}
                        for _ in range(int(carpan.group(1)))]
                continue
            z = aktar_access._skor_coz(carpan.group(2), yumurta=False) if carpan else None
            if z and z["tur"] in ("blast", "cleavage"):
                out += [dict(z) for _ in range(int(carpan.group(1)))]
                continue
            z = aktar_access._skor_coz(p, yumurta=yumurta)
            if not z:
                y = aktar_access._yuva_coz(p)
                out.append(dict(y) if y else {"tur": "taninmadi", "ham": p})
                continue
            if z["tur"] == "oosit":
                out += [{"tur": "oosit", "mat": z["mat"]} for _ in range(z["adet"])]
            else:
                out.append(z)
        if out:
            tupler.append(out)
    if parantezsiz and all(o["tur"] == "taninmadi" for t in tupler for o in t):
        return None
    return tupler or None


def _oge_metni(o) -> str:
    """Öğenin karşılaştırma yazımı -- tüpteki örneğin `_tup_skoru()`'yla aynı."""
    if o["tur"] == "oosit":
        return {"mii": "M2", "mi": "M1", "gv": "GV"}.get(o["mat"], "?")
    if o["tur"] == "cleavage":
        return _norm(f'{o["hucre"]}{o["skor"] or ""}')
    if o["tur"] == "blast":
        return _norm(o["skor"])
    if o["tur"] == "embriyo" and o.get("birlesme"):
        return _norm(_db.BIRLESME + (o.get("skor") or ""))
    return "?"


def excel_icerik(icerik: str):
    """HÜCRE metni -> [tüp içeriği, ...]; her tüp sıralı skor listesi, okunamayan
    parça "?" olur. Hiç okunamıyorsa None."""
    tupler = excel_ogeleri(icerik)
    return [sorted(_oge_metni(o) for o in t) for t in tupler] if tupler else None


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
         "substr(MIN(vc.opu_zamani),1,10) opu, MIN(vc.cycle_tipi) vit_tipi "
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
            "fet": r["vit_tipi"] in _db.FET_TIPLERI,
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
    ("bosaltilmis", "Tüp programda boşaltılmış/kullanılmış/başka merkeze taşınmış "
                    "görünüyor -- Excel tankta diyor", False),
    ("es_tutmuyor", "Ad tutuyor, eş adı tutmuyor -- yazılmadı (tüp bulunduysa yazılı)", False),
    ("tutmuyor", "O gün tüp var ama içerik tutmuyor (ya da Excel'de tüpten çok satır)", False),
    ("cakisma", "İki Excel satırı aynı tüpü istiyor", False),
    ("opu_gunu", "Tarih programdakinden farklı; Excel'in günü OPU'dan sayılınca "
                 "(D5 = OPU + 5) aynı tedavi, içerik tutuyor", True),
    ("yumurta_bir_gun", "Yumurta: Excel ile programın günü bir gün farklı (tek OPU, "
                        "yumurta OPU günü dondurulur), içerik tutuyor", True),
    ("refreeze_gunu", "FET'te yeniden dondurma: Excel'in günü çözmeden 1-3 gün sonra "
                      "(kültür / transfer artığı), içerik tutuyor", True),
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


def _gun_farki(a, b) -> int:
    return (_dt.date.fromisoformat(a) - _dt.date.fromisoformat(b)).days


# Tarih tutmayan Excel satırı için sırayla denenen ölçüler (v6.177,
# kullanıcının cevapları, 2026-09-25). Hepsinde hasta aynı, içerik birebir.
# (ad, satırdan değer, tüp bu değere uyuyor mu)
def _yumurta_satiri(s) -> bool:
    ic = (s["icerik"] or "").upper()
    return not _EXCEL_GUN.match(ic) and ("OOS" in ic or "M2" in ic or "MII" in ic)


_TARIH_OLCULERI = [
    # Excel'in günü OPU'dan: "D5" = OPU + 5.
    ("opu", _excel_opu, lambda t, d: t["opu"] == d),
    # Yumurta OPU günü dondurulur ("yumurta dondurma opu günü yapılıyor"),
    # bir tedavide tek OPU var: yumurta tüpü (dondurma günü = OPU) ile bir
    # gün kayık yumurta satırı aynı dondurma.
    ("yumurta_bir_gun", lambda s: s["tarih"] if _yumurta_satiri(s) else None,
     lambda t, d: t["opu"] and t["gun"] == t["opu"] and abs(_gun_farki(d, t["gun"])) == 1),
    # FET'te yeniden dondurma çözme günü, kültürden sonra (3->5, 4->5) ya da
    # transfer artığı olarak: program çözme gününü yazıyor, Excel 1-3 gün
    # sonrasını.
    ("refreeze_gunu", lambda s: s["tarih"],
     lambda t, d: t["fet"] and 1 <= _gun_farki(d, t["gun"]) <= 3),
]


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
        s["hid"] = hid                  # `eksik` kipi için (v6.182)
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
            for ad, deger_al, uyar in _TARIH_OLCULERI:
                d = deger_al(s)
                if d and any(uyar(t, d) for t in hastanin):
                    anahtar = (hid, ad, d)
                    break
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
    sira = ["gun"] + [ad for ad, _, _ in _TARIH_OLCULERI]
    uyarlar = {ad: u for ad, _, u in _TARIH_OLCULERI}
    for (hid, olcu, deger), istekler in sorted(gunluk.items(), key=lambda x: sira.index(x[0][1])):
        if olcu == "gun":
            adaylar = [t for t in tup[hid] if t["gun"] == deger]
        else:
            adaylar = [t for t in tup[hid]
                       if uyarlar[olcu](t, deger) and t["tid"] not in kullanilan]
        for (s, ic), t, sinif in _dagit(istekler, adaylar):
            if t is not None and olcu != "gun":
                sinif = "opu_gunu" if olcu == "opu" else olcu
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
    print(f"Excel: {toplam} satır, {sperm} sperm (bu kipte eşleştirilmiyor -- sperm kipi açar), "
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


def _renk_kodlari(b, gerekenler) -> tuple:
    """Listedeki renk kodları -> (kodlar, eklenen sayısı). Excel'de geçen ama
    listede olmayan `RENK_ETIKETLERI` rengi önce ekleniyor (v6.188)."""
    eklenen = 0
    for kod in sorted(set(gerekenler) & set(RENK_ETIKETLERI)):
        eklenen += _liste_kodu_ekle(b, "tasiyici_renk", kod, RENK_ETIKETLERI[kod])
    kodlar = {r[0] for r in b.execute(
        "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_renk'",
        (_db.LAB_ID,))}
    return kodlar, eklenen


def uygula(sonuc) -> dict:
    yazilanlar = [(s, t) for s, k, t, _ in sonuc if k in YAZILIR and t]
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        kid = _kullanici_id(b)
        simdi = _dt.datetime.now().isoformat(" ", "seconds")
        renkler, sayac["renk_kodu_eklendi"] = _renk_kodlari(
            b, {s["renk"] for s, _ in yazilanlar if s["renk"]})
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


# ------------------------------------------------------------ onar (v6.188)
#
# v6.188'e kadar Excel üç yerde yanlış okunuyordu ve `uygula` o okumayı
# kullanıcının veritabanına yazdı (2026-09-25):
#   - TANK 3'ün 2-5. kanisterleri tek sütunda alt alta, araya "CANİSTER 2"
#     satırları konarak yazılmış; hepsi 1. kanister sayıldı.
#   - "Tank 1-5 üst" sayfası kanisterlerin üst katı; gobletleri alttakilerle
#     aynı adı aldı (TANK 5'te 1-30 iki katta da var, tek yer sayıldı).
#     Artık "7 Üst" (kullanıcının seçtiği yazım).
#   - "YEŞİL" hiç tanınmıyordu, pembe listede yoktu: straw'lar renksiz kaldı.
# `onar` YALNIZCA o okumanın yazdığını düzeltir. Tüpün bugünkü konumu
# satırın eski okumadaki yeriyle aynıysa yeni yer yazılır; başka bir konum
# varsa (elle girilmiş, taşınmış) dokunulmaz, raporda listelenir. Renk
# yalnızca boşsa yazılır. İkinci çalıştırma hiçbir şeyi değiştirmez.

ONAR_RAPOR = Path("cryo_esle_rapor_onar.txt")


def _eski_yol(s):
    return " / ".join(x for x in s["eski_yer"] if x)


def onar_plani(sonuc) -> tuple:
    """-> (konumu düzeltilecek, rengi yazılacak, dokunulmayan) [(satır, tüp)]"""
    konum, renk, dokunulmadi = [], [], []
    for s, sinif, t, _ek in sonuc:
        if t is None or t["durum"] != "dolu":
            continue
        yeni, eski = _tam_yol(s), _eski_yol(s)
        tasinacak = False
        if sinif == "farkli_konum" and yeni != eski:
            if t["tam_yol"] == eski:
                konum.append((s, t))
                tasinacak = True
            else:
                dokunulmadi.append((s, t))
        if (sinif == "zaten" or tasinacak) and not t["renk"] and s["renk"]:
            renk.append((s, t))
    return konum, renk, dokunulmadi


def onar_yaz(konum, renk) -> dict:
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        kid = _kullanici_id(b)
        simdi = _dt.datetime.now().isoformat(" ", "seconds")
        renkler, sayac["renk_kodu_eklendi"] = _renk_kodlari(b, {s["renk"] for s, _ in renk})

        def logla(tid, alan, eski, yeni):
            b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                      "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                      (_db.LAB_ID, "tasiyici", str(tid), alan, eski, yeni, kid, simdi))

        def simdiki(tid):
            return b.execute("SELECT k.tam_yol, t.renk FROM tasiyici t "
                             "LEFT JOIN konum k ON k.id=t.konum_id WHERE t.id=?",
                             (tid,)).fetchone()

        for s, t in konum:
            # Program açıkken biri bu arada tüpü taşımış olabilir: kilidin
            # içinde yeniden bak, değişmişse dokunma.
            r = simdiki(t["tid"])
            if not r or r[0] != t["tam_yol"]:
                sayac["degismis"] += 1
                continue
            konum_id = _db.konum_bul_veya_olustur(_seviyeler(s), b)
            b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?", (konum_id, t["tid"]))
            b.execute("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))
            logla(t["tid"], "konum", t["tam_yol"], _tam_yol(s))
            sayac["konum"] += 1
        for s, t in renk:
            if s["renk"] not in renkler:
                sayac["renk_listede_yok"] += 1
                continue
            r = simdiki(t["tid"])
            if not r or r[1]:
                sayac["degismis"] += 1
                continue
            b.execute("UPDATE tasiyici SET renk=? WHERE id=?", (s["renk"], t["tid"]))
            logla(t["tid"], "renk", None, s["renk"])
            sayac["renk"] += 1
    return sayac


def onar_raporu(konum, renk, dokunulmadi):
    with ONAR_RAPOR.open("w", encoding="utf-8") as f:
        f.write(f"Cryo haritası onarımı (v6.188) -- {_dt.datetime.now():%d.%m.%Y %H:%M}\n")
        f.write("Hasta adı içerir: bu dosyayı paylaşma, depoya koyma.\n")
        for baslik, liste, metin in (
                ("Konumu düzeltilecek (eski okumanın yazdığı yer -> doğru yer)", konum,
                 lambda s, t: f'{t["tam_yol"]}  ->  {_tam_yol(s)}'),
                ("Rengi yazılacak (tüpün rengi boş)", renk,
                 lambda s, t: f'renk: {s["renk"]}'),
                ("DOKUNULMADI -- tüpün konumu eski okumadan da farklı "
                 "(elle girilmiş ya da taşınmış olabilir, bakılmalı)", dokunulmadi,
                 lambda s, t: f'programda: {t["tam_yol"]}  | Excel: {_tam_yol(s)}')):
            f.write(f"\n== {baslik}: {len(liste)}\n")
            for s, t in liste:
                f.write(f"  {_satir_metni(s, t, metin(s, t))}\n")


def _onar_kipi(sonuc):
    konum, renk, dokunulmadi = onar_plani(sonuc)
    onar_raporu(konum, renk, dokunulmadi)
    tank = collections.Counter(
        s["tank"] + (f" {cryo_excel.UST_KAT}" if s["goblet"].endswith(cryo_excel.UST_KAT)
                     else f" kanister {s['kanister']}") for s, _ in konum)
    print(f"Konumu düzeltilecek tüp: {len(konum)}"
          + (" (" + ", ".join(f"{k}: {n}" for k, n in sorted(tank.items())) + ")"
             if tank else ""))
    print(f"Rengi yazılacak tüp: {len(renk)} ("
          + ", ".join(f"{k}: {n}" for k, n in sorted(
              collections.Counter(s["renk"] for s, _ in renk).items())) + ")"
          if renk else "Rengi yazılacak tüp: 0")
    if dokunulmadi:
        print(f"Dokunulmayacak: {len(dokunulmadi)} tüpün konumu eski okumadan da "
              "farklı (elle girilmiş olabilir) -- raporda.")
    print(f"Ayrıntı: {ONAR_RAPOR}")
    if not (konum or renk):
        print("Onarılacak bir şey yok.")
        return
    print("\nDevam için ONAR yazın:")
    if input("> ").strip() != "ONAR":
        print("Vazgeçildi, hiçbir şey yazılmadı.")
        return
    y = onar_yaz(konum, renk)
    print(f"Yazıldı: {y['konum']} tüpün konumu, {y['renk']} tüpün rengi"
          + (f"; {y['renk_kodu_eklendi']} renk listeye eklendi" if y["renk_kodu_eklendi"] else "")
          + (f"; {y['degismis']} tüp bu arada değişmiş, dokunulmadı" if y["degismis"] else "")
          + ".")


# --------------------------------------------------- yerleşim (v6.189)
#
# Kullanıcının isteği (2026-09-25): "Laboratuvarda cryo harita en önemli
# kayıt ... Bu haritanın kesinlikle bozulmaması gerekiyor. ... dondururken
# program bana tanklarda boş yerleri önermesi." Program boş gobleti hiç
# bilmiyordu: `konum` yalnızca bir tüpe yazılmış yerdi. `yerlesim` Excel'in
# BÜTÜN gobletlerini (boşlar dahil) programa açar ve Excel'de duran ama
# programda karşılığı olan bir tüp bulunamayan her satırı gobletinde bir
# "Excel kaydı" olarak bırakır (kullanıcının seçimi: "Gobletinde 'Excel
# kaydı' olarak dursun") -- yuvası dolu sayılsın, haritadan hiçbir straw
# kaybolmasın.
#
# ÖNCE öteki kipler: bekleyen `uygula` / `onar` / `yeni_hasta` / `sperm`
# yazısı varsa hiçbir şey yazmadan durur. Yoksa aynı straw hem Excel kaydı
# olarak açılır hem de sonradan tüpüne konum yazılırdı -- goblet iki kez
# dolu görünürdü.
#
# Bir satır "programda temsil ediliyor" = eşleştiği tüp dolu ve o gobletde
# (`yerlesim.yer_anahtari()` ile: "p" = "P"). Temsil edilmeyen her dolu satır
# -- hasta yok, içerik tutmuyor, tüp programda boşaltılmış, tüp başka konumda,
# yalnızca adı yazılı satır -- Excel kaydı olur, sebebiyle. Sahte tüp
# açılmıyor (v6.127'nin gerekçesi aynen geçerli).
#
# İkinci çalıştırma hiçbir şeyi değiştirmez (goblet zaten düzende, Excel
# kaydı içerik anahtarıyla zaten var). Excel'e sonradan satır eklenmiş olsa
# da anahtar tutar (sayfa/satır numarasına değil içeriğe bakıyor); Excel'den
# silinmiş bir satırın Excel kaydı ise KENDİLİĞİNDEN kaldırılmaz, raporda
# listelenir -- straw'ın tanktan çıktığını söyleyecek olan kullanıcı.

YERLESIM_RAPOR = Path("cryo_esle_rapor_yerlesim.txt")

# Excel kaydının "neden programdaki bir tüp değil" sebebi: eşleştirmenin
# sınıfı, yoksa bunlar.
_BILGISIZ = "bilgisiz"          # yalnızca ad yazılı, tarih/hücre/VİAL yok
_GOBLETSIZ = "gobletsiz"        # NO sütunu boş


def _satir_kimligi(s):
    return (s["sayfa"], s["satir"], s["sutun"])


def _duzen_yolu(g):
    return [g["tank"] or "", g["kanister"] or "", g["goblet"] or "", ""]


def _anahtarlar(satirlar):
    """Excel kaydının içerik anahtarı: yer + ad + tarih + hücre + VİAL, aynı
    içerikteki kaçıncı satır olduğuyla. Sayfa/satır numarası YOK: Excel'e
    satır eklenince kayar, aynı straw ikinci kez açılırdı."""
    sayac = collections.Counter()
    sonuc = {}
    for s in satirlar:
        yer = _yerlesim.yer_anahtari(s["tank"], s["kanister"], s["goblet"])
        ic = "\x1f".join([*yer, s["soyad"], s["ad"], s["tarih_ham"],
                          s["icerik"], s["vial_metni"]])
        ozet = hashlib.sha1(ic.encode("utf-8")).hexdigest()
        sayac[ozet] += 1
        sonuc[_satir_kimligi(s)] = f"{ozet}:{sayac[ozet]}"
    return sonuc


def yerlesim_bekleyenler(sonuc, satirlar, b) -> list:
    """Önce çalıştırılması gereken kipler: [(kip, kaç kayıt, açıklama)]."""
    bekleyen = []
    n = sum(1 for _s, k, t, _e in sonuc if k in YAZILIR and t)
    if n:
        bekleyen.append(("uygula", n, "tüpe konum yazılacak"))
    konum, _renk, _dok = onar_plani(sonuc)
    if konum:
        bekleyen.append(("onar", len(konum), "tüpün konumu düzeltilecek"))
    plan, _atlanan = yeni_hasta_plani(sonuc)
    if plan:
        bekleyen.append(("yeni_hasta", len(plan), "2018 öncesi hasta açılacak"))
    sp, _kisiler = sperm_plani(satirlar, b)
    n = sum(1 for _s, k, _e in sp if k in ("yeni", "konum_yaz", "sebep_yaz"))
    if n:
        bekleyen.append(("sperm", n, "sperm satırı yazılacak"))
    return bekleyen


def yerlesim_plani(duzen, sonuc, satirlar, b) -> dict:
    """Excel'in düzeni + eşleştirme -> ne yazılacak (hiçbir şey yazmaz)."""
    konumlar = {}
    anahtar_of = {}
    for r in b.execute("SELECT id, seviye1, seviye2, seviye3, tam_yol, kapasite, "
                       "kategori, sira FROM konum WHERE lab_id=?", (_db.LAB_ID,)):
        konumlar[r["tam_yol"]] = r
        anahtar_of[r["id"]] = _yerlesim.konum_anahtari(r)
    # 1) Gobletler. "Sayfa1"in tankı yok (v6.180): gobletleri düzene girmiyor.
    gobletler = []
    for g in duzen["gobletler"]:
        if _KONUMSUZ_SAYFA.match(cryo_excel._n(g["tank"])):
            continue
        yol = " / ".join(x for x in _duzen_yolu(g) if x)
        k = konumlar.get(yol)
        istenen = (g["kapasite"], g["kategori"], g["sira"])
        if k is None:
            gobletler.append((g, "yeni"))
        elif (k["kapasite"], k["kategori"], k["sira"]) != istenen:
            gobletler.append((g, "degisecek" if k["sira"] is not None else "duzene"))
        else:
            gobletler.append((g, "zaten"))
    # 2) Excel'in dolu satırları: programda temsil ediliyor mu?
    temsil = set()
    sebep = {}
    for s, k, t, ek in sonuc:
        kim = _satir_kimligi(s)
        yer = _yerlesim.yer_anahtari(s["tank"], s["kanister"], s["goblet"])
        if (k != "cakisma" and t and t["durum"] == "dolu" and t["konum_id"]
                and anahtar_of.get(t["konum_id"]) == yer):
            temsil.add(kim)
            continue
        not_ = ek or ""
        if t:
            not_ = (not_ + "; " if not_ else "") + f"tüp {t['etiket']}"
        sebep[kim] = (k, not_)
    sp, _kisiler = sperm_plani(satirlar, b)
    for s, k, ek in sp:
        kim = _satir_kimligi(s)
        if k == "zaten":
            temsil.add(kim)
        else:
            sebep[kim] = (f"sperm_{k}", ek if isinstance(ek, str) else "")
    # Satırın kategorisi `coz()`'unki (eşleştirmenin baktığı); yalnızca adı
    # yazılı satır orada yok, düzeninki. Excel kaydı gobletin Excel'deki
    # yazımına açılıyor ("p" satırı da "P" gobletine).
    coz_kat = {_satir_kimligi(s): s["kategori"] for s in satirlar}
    yolu = {}
    dolu = []
    for g in duzen["gobletler"]:
        for r in g["satirlar"]:
            if r["dolu"]:
                dolu.append(r)
                yolu[_satir_kimligi(r)] = _duzen_yolu(g)
    for r in duzen["gobletsiz"]:
        dolu.append(r)
        yolu[_satir_kimligi(r)] = [r["tank"] or "", r["kanister"] or "", "", ""]
    anahtarlar = _anahtarlar(dolu)
    mevcut = {r["anahtar"]: r for r in b.execute(
        "SELECT id, anahtar, durum FROM excel_kaydi WHERE lab_id=?", (_db.LAB_ID,))}
    yeni, zaten = [], 0
    for r in dolu:
        kim = _satir_kimligi(r)
        if kim in temsil:
            continue
        if anahtarlar[kim] in mevcut:
            zaten += 1
            continue
        k, not_ = sebep.get(kim, (_BILGISIZ if r["no"] else _GOBLETSIZ, ""))
        if not r["no"] and k != _GOBLETSIZ:
            not_ = (not_ + "; " if not_ else "") + "Excel'de NO (goblet) yazmıyor"
        yol = ([] if _KONUMSUZ_SAYFA.match(cryo_excel._n(r["tank"])) else yolu[kim])
        yeni.append((r, anahtarlar[kim], k, not_, coz_kat.get(kim, r["kategori"]), yol))
    bu_dosyada = set(anahtarlar.values())
    excel_yok = [r for a, r in mevcut.items()
                 if r["durum"] == "tankta" and a not in bu_dosyada]
    return {"gobletler": gobletler, "yeni": yeni, "zaten": zaten,
            "temsil": len(temsil), "excel_yok": excel_yok, "notlar": duzen["notlar"]}


def yerlesim_yaz(baytlar) -> dict:
    """Düzeni ve Excel kayıtlarını yazar -- kilidin içinde her şeyi yeniden
    hesaplayarak (program açıkken biri bu arada dondurma yapmış olabilir)."""
    cozum = cryo_excel.coz(baytlar)
    duzen = cryo_excel.duzen(baytlar)
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        idx, tup = hastalar(b), tupler(b)
        sonuc = esle(cozum["satirlar"], idx, tup)
        if yerlesim_bekleyenler(sonuc, cozum["satirlar"], b):
            raise RuntimeError("bu arada eşleştirilecek yeni kayıt çıktı -- "
                               "önce öteki kipleri çalıştırın")
        plan = yerlesim_plani(duzen, sonuc, cozum["satirlar"], b)
        kid = _kullanici_id(b)
        simdi = _dt.datetime.now().isoformat(" ", "seconds")
        renkler, _ = _renk_kodlari(b, {cryo_excel.vial_coz(r["vial_metni"])[2]
                                       for r, *_x in plan["yeni"]} - {None})
        tipler = {x[0] for x in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_tipi'",
            (_db.LAB_ID,))}
        for g, durum in plan["gobletler"]:
            if durum == "zaten":
                continue
            konum_id = _db.konum_bul_veya_olustur(_duzen_yolu(g), b)
            b.execute("UPDATE konum SET kapasite=?, kategori=?, sira=? WHERE id=?",
                      (g["kapasite"], g["kategori"], g["sira"], konum_id))
            sayac["goblet_" + durum] += 1
        for r, anahtar, sebep, not_, kategori, yol in plan["yeni"]:
            konum_id = _db.konum_bul_veya_olustur(yol, b) if yol else None
            tarih, tarih_notu = cryo_excel.tarih_coz(r["tarih_ham"])
            _adet, tip, renk = cryo_excel.vial_coz(r["vial_metni"])
            b.execute(
                "INSERT INTO excel_kaydi (lab_id, anahtar, konum_id, kategori, soyad, ad, "
                "es_adi, tarih, tarih_ham, icerik, vial, notlar, tip, renk, "
                "eslesmeme_sebebi, eslesmeme_notu, kaynak_sayfa, kaynak_satir, "
                "durum, kullanici_id, olusturma_zamani) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'tankta',?,?)",
                (_db.LAB_ID, anahtar, konum_id, kategori or "embriyo",
                 r["soyad"] or None, r["ad"] or None, r["es_adi"] or None, tarih,
                 r["tarih_ham"] or None, r["icerik"] or None, r["vial_metni"] or None,
                 r["notlar"] or None, tip if tip in tipler else None,
                 renk if renk in renkler else None, sebep, not_ or None,
                 r["sayfa"], r["satir"], kid, simdi))
            sayac["excel_" + (kategori or "embriyo")] += 1
        b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                  "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                  (_db.LAB_ID, "konum", "*", "duzen", None,
                   f"Cryo Excel'inden tank düzeni: {sum(1 for _ in plan['gobletler'])} "
                   f"goblet; {sayac['excel_embriyo'] + sayac['excel_sperm']} yeni "
                   "Excel kaydı", kid, simdi))
    return sayac


def yerlesim_raporu(plan, bekleyen):
    with YERLESIM_RAPOR.open("w", encoding="utf-8") as f:
        f.write(f"Cryo haritası -- tank düzeni (v6.189) -- "
                f"{_dt.datetime.now():%d.%m.%Y %H:%M}\n")
        f.write("Hasta adı içerir: bu dosyayı paylaşma, depoya koyma.\n")
        if bekleyen:
            f.write("\nÖNCE ÇALIŞTIRILMALI (hiçbir şey yazılmadı):\n")
            for kip, n, ne in bekleyen:
                f.write(f"  python3 cryo_esle.py {kip} ...  -- {n} {ne}\n")
            return
        durum = collections.Counter(d for _g, d in plan["gobletler"])
        f.write(f"\nGobletler: {len(plan['gobletler'])} ({dict(durum)})\n")
        f.write("Kapasitesi bilinmeyen embriyo yerleri (önerilmez):\n")
        for g, _d in plan["gobletler"]:
            if g["kategori"] == "embriyo" and not g["kapasite"]:
                f.write(f"  {' / '.join(x for x in _duzen_yolu(g) if x)}  "
                        f"({len(g['satirlar'])} satır)\n")
        f.write(f"\n== Yeni Excel kaydı: {len(plan['yeni'])}\n")
        sira = collections.defaultdict(list)
        for r, _a, sebep, not_, _k, _y in plan["yeni"]:
            sira[sebep].append((r, not_))
        for sebep in sorted(sira):
            f.write(f"\n-- {sebep}: {len(sira[sebep])}\n")
            for r, not_ in sira[sebep]:
                yer = " / ".join(x for x in (r["tank"], r["kanister"], r["goblet"]) if x)
                f.write(f'  {r["sayfa"]} satır {r["satir"]} ({yer}) | {r["soyad"]} '
                        f'{r["ad"]} | {r["tarih_ham"] or "tarih?"} | {r["icerik"]} | '
                        f'{r["vial_metni"]}' + (f"  | {not_}" if not_ else "") + "\n")
        f.write(f"\n== Excel'de artık olmayan Excel kaydı (dokunulmadı): "
                f"{len(plan['excel_yok'])}\n")
        for r in plan["excel_yok"]:
            f.write(f"  /cryo/excel-kaydi/{r['id']}\n")
        f.write(f"\n== Not satırları (NO sütununa yazılmış; programa geçmiyor): "
                f"{len(plan['notlar'])}\n")
        for r in plan["notlar"]:
            f.write(f'  {r["sayfa"]} satır {r["satir"]} ({r["tank"]} / {r["kanister"]}): '
                    f'{r["no"]}\n')


def _yerlesim_kipi(dosya, cozum, sonuc):
    if not _db.kolon_var("konum", "sira") or not _db.tablo_var("excel_kaydi"):
        sys.exit("Veritabanında tank düzeninin yeri yok (göç 052). Programı bir kez "
                 "açıp kapatın, sonra tekrar çalıştırın.")
    baytlar = dosya.read_bytes()
    duzen = cryo_excel.duzen(baytlar)
    with _db.baglan() as b:
        bekleyen = yerlesim_bekleyenler(sonuc, cozum["satirlar"], b)
        plan = None if bekleyen else yerlesim_plani(duzen, sonuc, cozum["satirlar"], b)
    yerlesim_raporu(plan, bekleyen)
    if bekleyen:
        print("Önce şunlar çalıştırılmalı (tank düzeni hiçbir şey yazmadı):")
        for kip, n, ne in bekleyen:
            print(f"  python3 cryo_esle.py {kip} {dosya}   -- {n} {ne}")
        return
    g = duzen["gobletler"]
    emb = [x for x in g if x["kategori"] == "embriyo"]
    print(f"Tank düzeni (Excel): {len(g)} goblet -- {len(emb)} embriyo "
          f"({sum(1 for x in emb if x['kapasite'])} tanesi {cryo_excel.GOBLET_KAPASITESI} "
          f"yuvalı), {len(g) - len(emb)} sperm.")
    durum = collections.Counter(d for _g, d in plan["gobletler"])
    print(f"  Programda: {durum.get('zaten', 0)} goblet zaten düzende; açılacak "
          f"{durum.get('yeni', 0)}, düzene alınacak {durum.get('duzene', 0)}, "
          f"değişecek {durum.get('degisecek', 0)}.")
    kat = collections.Counter(k or "embriyo" for _r, _a, _s, _n, k, _y in plan["yeni"])
    print(f"Excel'in dolu satırı: {plan['temsil']} tanesi programdaki tüpte (gobletinde); "
          f"yeni Excel kaydı {len(plan['yeni'])} (embriyo {kat.get('embriyo', 0)}, "
          f"sperm {kat.get('sperm', 0)}); zaten açılmış {plan['zaten']}.")
    sebep = collections.Counter(s for _r, _a, s, _n, _k, _y in plan["yeni"])
    if sebep:
        print("  Excel kaydı olma sebebi: " + ", ".join(
            f"{k} {n}" for k, n in sebep.most_common()))
    if plan["excel_yok"]:
        print(f"Excel'de artık olmayan Excel kaydı: {len(plan['excel_yok'])} "
              "(dokunulmadı -- raporda).")
    print(f"Not satırı (programa geçmiyor): {len(plan['notlar'])}.")
    print(f"Ayrıntı: {YERLESIM_RAPOR}")
    if not (plan["yeni"] or any(d != "zaten" for _g, d in plan["gobletler"])):
        print("Yazılacak bir şey yok.")
        return
    print("\nDevam için YERLESIM yazın:")
    if input("> ").strip() != "YERLESIM":
        print("Vazgeçildi, hiçbir şey yazılmadı.")
        return
    try:
        y = yerlesim_yaz(baytlar)
    except RuntimeError as e:
        sys.exit(f"Yazılmadı: {e}.")
    print(f"Yazıldı: {y['goblet_yeni']} goblet açıldı, "
          f"{y['goblet_duzene'] + y['goblet_degisecek']} goblet düzene alındı; "
          f"{y['excel_embriyo']} embriyo ve {y['excel_sperm']} sperm Excel kaydı.")


# ------------------------------------------------------ yeni hasta (v6.179)
#
# Kullanıcının isteği (2026-09-25): "390: hastanın programda kaydı yok. Büyük
# kısmı 2011–2017'den. Bunları programa ekle." Kararları (aynı gün soruldu):
# yalnızca 2011–2017 satırları -- o yılların Access dosyası yok; 2018 ve
# sonrasında "hasta yok" satırlarının çoğunun benzer adlı bir hastası var
# (bir harf, eksik bir soyad), yeni kart aynı kişiyi iki kez açardı -- ve
# geçici dosya numarası, gerçeği sonra `dosya_no_degistir.py` ile.
#
# v6.127'nin "sahte tedavi/tüp açılmaz" gerekçesi (istatistikleri bozar)
# burada da geçerli; o yüzden bu tedaviler protokol notlarındaki işaretle
# (`db.CRYO_EXCEL_ISARETI`) `/istatistik`'ten dışlanıyor: yalnızca dondurma
# bilgisi var, OPU/ICSI/döllenme yok -- oranlara girseler 2011–2017 aylarında
# "%0 MII" gibi ölçülmemişi ölçülmüş gösteren sayılar çıkardı.

YENI_HASTA_SON = "2018"                 # bu yıldan ÖNCEKİ satırlar
GECICI_DOSYA_TABANI = 9_000_000_000     # gerçek numaralar 9 haneyi aşmıyor
YENI_RAPOR = Path("cryo_esle_rapor_yeni_hasta.txt")
_YENI_VIT_NOTU = "Cryo Haritası Excel'inden açıldı (program öncesi kayıt)"
_YENI_YAZIM = "Cryo Haritası Excel'indeki yazım"


def _tup_yumurta_mu(tup) -> bool:
    return all(o["tur"] == "oosit" for o in tup)


def _excel_gunu(s):
    m = _EXCEL_GUN.match(s["icerik"] or "")
    return int(m.group(1)) if m else None


def yeni_hasta_plani(sonuc):
    """"Hasta programda yok" ve TARİH'i 2018'den önce olan satırlar ->
    ([(ad kelimeleri, eş adı, [satır, ...]), ...], [(satır, sebep), ...]).

    Hasta ad kelime kümesiyle gruplanıyor (eşleştirmenin kendi ölçüsü,
    `cryo_excel.kelimeler()`); aynı adın iki farklı eşi varsa iki kişi, eşi
    yazılmamış satırı hangisinin bilinmiyor -- atlanıyor, uydurulmuyor."""
    adaylar = [s for s, k, _t, _e in sonuc
               if k == "hasta_yok" and s["tarih"] and s["tarih"] < YENI_HASTA_SON]
    gruplar = collections.defaultdict(list)
    for s in adaylar:
        gruplar[cryo_excel.kelimeler(f'{s["soyad"]} {s["ad"]}')].append(s)
    plan, atlanan = [], []
    for kel, satirlar in gruplar.items():
        okunan = []
        for s in satirlar:
            if excel_ogeleri(s["icerik"]):
                okunan.append(s)
            else:
                atlanan.append((s, "HÜCRE okunamadı -- tüp içeriği bilinmiyor"))
        if not okunan:
            continue
        esler = sorted({cryo_excel.buyuk(s["es_adi"]) for s in okunan if s["es_adi"].strip()})
        if len(esler) <= 1:
            plan.append((kel, esler[0] if esler else None, okunan))
            continue
        for es in esler:
            plan.append((kel, es, [s for s in okunan if cryo_excel.buyuk(s["es_adi"]) == es]))
        for s in okunan:
            if not s["es_adi"].strip():
                atlanan.append((s, "aynı adla iki farklı eş var, bu satırda eş yazmıyor"))
    return plan, atlanan


def _tedavileri(satirlar):
    """Bir hastanın satırları -> {tedavi anahtarı: [satır, ...]}. Anahtar OPU
    günü (`_excel_opu()`: "D5" = TARİH − 5, yumurta TARİH); günü yazmayan
    embriyo satırında OPU bilinmiyor, anahtar TARİH (OPU boş kalır)."""
    t = collections.defaultdict(list)
    for s in satirlar:
        opu = _excel_opu(s)
        t[("opu", opu) if opu else ("tarih", s["tarih"])].append(s)
    return t


def _yeni_ad(s) -> str:
    return cryo_excel.buyuk(f'{s["ad"]} {s["soyad"]}'.strip())


def yeni_hasta_yaz(plan) -> dict:
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        kid = _kullanici_id(b)
        renkler, _ = _renk_kodlari(
            b, {s["renk"] for _k, _e, g in plan for s in g if s["renk"]})
        tipler = {r[0] for r in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_tipi'",
            (_db.LAB_ID,))}
        dosya = max(GECICI_DOSYA_TABANI, b.execute(
            "SELECT COALESCE(MAX(dosya_no),0) FROM hasta WHERE lab_id=?",
            (_db.LAB_ID,)).fetchone()[0])
        for _kel, es, satirlar in plan:
            dosya += 1
            ilk = min(s["tarih"] for s in satirlar)
            b.execute(
                "INSERT INTO hasta (lab_id, dosya_no, ad_soyad, es_adi, notlar, durum, "
                "olusturma_zamani) VALUES (?,?,?,?,?,'aktif',?)",
                (_db.LAB_ID, dosya, _yeni_ad(satirlar[0]), es,
                 "Cryo Haritası Excel'inden açıldı (v6.179). GEÇİCİ dosya numarası -- "
                 "gerçek numara dosya_no_degistir.py ile yazılmalı.",
                 f"{ilk} 08:00:00"))
            hid = b.execute("SELECT last_insert_rowid()").fetchone()[0]
            sayac["hasta"] += 1
            for (olcu, gun), grup in sorted(_tedavileri(satirlar).items(),
                                            key=lambda x: x[0][1]):
                # Excel'in kendi sırasıyla (`esle()`'nin istek sırası): aynı gün
                # birebir aynı içerikli iki tüp ikinci çalıştırmada `_dagit()`
                # ile etiket sırasına dağıtılıyor -- başka sırayla açılsalar
                # çapraz eşleşip "başka konum yazılmış" derlerdi.
                tuplar = [(s, tup) for s in grup for tup in excel_ogeleri(s["icerik"])]
                tip = "oosit_cryo" if all(_tup_yumurta_mu(t) for _s, t in tuplar) else "ivf_icsi"
                cycle_no = aktar_access._lab_no(b, gun[:4])
                son = max(s["tarih"] for s in grup)
                yerler = "; ".join(sorted({f'{s["sayfa"]} satır {s["satir"]}' for s in grup}))
                notu = ("Program öncesi kayıt: yalnızca Cryo Haritası Excel'indeki dondurma "
                        f"bilgisi ({yerler}). OPU, ICSI ve döllenme kaydı yok.\n"
                        + _db.CRYO_EXCEL_ISARETI)
                sira_no = (b.execute("SELECT COALESCE(MAX(hasta_cycle_no),0)+1 FROM cycle "
                                     "WHERE hasta_id=?", (hid,)).fetchone()[0])
                b.execute(
                    "INSERT INTO cycle (lab_id, hasta_id, cycle_no, hasta_cycle_no, cycle_tipi, "
                    "protokol_notu, opu_zamani, durum, bitis_sebebi, bitis_zamani, "
                    "olusturma_zamani) VALUES (?,?,?,?,?,?,?,'tamamlandi','dondurma',?,?)",
                    (_db.LAB_ID, hid, cycle_no, sira_no, tip, notu,
                     f"{gun} 09:00:00" if olcu == "opu" else None,
                     f"{son} 16:00:00", f"{gun} 08:30:00"))
                cid = b.execute("SELECT last_insert_rowid()").fetchone()[0]
                sayac["tedavi"] += 1
                sira = 0
                for i, (s, tup) in enumerate(tuplar):
                    an = f'{s["tarih"]} {12 + i // 60:02d}:{i % 60:02d}:00'
                    tid, _etiket, an = aktar_access._tasiyici_ac(b, kid, cycle_no, an)
                    konum_id = _db.konum_bul_veya_olustur(_seviyeler(s), b)
                    b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?", (konum_id, tid))
                    b.execute("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))
                    if s["tip"] and s["tip"] not in tipler and s["tip"] in TIP_ETIKETLERI:
                        _liste_kodu_ekle(b, "tasiyici_tipi", s["tip"], TIP_ETIKETLERI[s["tip"]])
                        tipler.add(s["tip"])
                    if s["tip"] in tipler:
                        b.execute("UPDATE tasiyici SET tip=? WHERE id=?", (s["tip"], tid))
                    if s["renk"] in renkler:
                        b.execute("UPDATE tasiyici SET renk=? WHERE id=?", (s["renk"], tid))
                    sayac["tup"] += 1
                    egun = _excel_gunu(s)
                    for o in tup:
                        sira += 1
                        sid = aktar_access._specimen_ac(b, cid, cycle_no, sira, "dondurulmus",
                                                        f"{gun} 08:30:00")
                        sayac["ornek"] += 1
                        if o["tur"] == "oosit":
                            if o["mat"]:
                                aktar_access._olay(b, kid, sid, cid, "maturasyon_kontrolu",
                                                   f"{s['tarih']} 11:30:00", mat_deger=o["mat"],
                                                   notlar=_YENI_VIT_NOTU)
                        else:
                            if o["tur"] == "taninmadi":
                                sayac["skorsuz"] += 1
                                sayac.setdefault("okunamayan", []).append(o["ham"])
                            g = egun or (5 if o["tur"] == "blast" else 3)
                            alan = aktar_access._oge_alanlari(o, g)
                            if alan and o["tur"] == "cleavage":
                                if not o.get("skor"):
                                    alan[1]["cl_skor_kaynagi"] = None
                                if o.get("frag") is not None:
                                    alan[1]["cl_fragmentasyon"] = o["frag"]
                                if o.get("simetri"):
                                    alan[1]["cl_simetri"] = o["simetri"]
                            if alan:
                                aktar_access._degerlendirme_yaz(
                                    b, kid, sid, cid, alan[0],
                                    max(g, 4) if o["tur"] == "blast" else min(g, 3),
                                    f"{s['tarih']} 09:00:00", alan[1], o.get("ham", ""),
                                    onek=_YENI_YAZIM)
                        aktar_access._olay(b, kid, sid, cid, "vitrifikasyon", an,
                                           vit_tasiyici_id=tid, notlar=_YENI_VIT_NOTU)
            _db.tedavileri_sirala(b, hid)
    return sayac


def yeni_hasta_raporu(plan, atlanan):
    satirlar = [f"CRYO EXCEL -- YENİ HASTA ({YENI_HASTA_SON} öncesi) -- "
                f"{_dt.datetime.now():%Y-%m-%d %H:%M:%S}", ""]
    for kel, es, grup in plan:
        satirlar.append(f'{_yeni_ad(grup[0])}' + (f" (eşi {es})" if es else ""))
        for (olcu, gun), g in sorted(_tedavileri(grup).items(), key=lambda x: x[0][1]):
            satirlar.append(f"   tedavi {'OPU ' + gun if olcu == 'opu' else 'OPU bilinmiyor, ' + gun}")
            for s in g:
                n = sum(len(t) for t in excel_ogeleri(s["icerik"]))
                satirlar.append(f"      {_yer(s)} | {s['tarih']} | {s['icerik']} | "
                                f"{s['vial_metni']} -> {n} örnek")
    if atlanan:
        satirlar += ["", f"== Açılmayan satırlar: {len(atlanan)}"]
        for s, sebep in atlanan:
            satirlar.append(f"   {_yer(s)} | {s['soyad']} {s['ad']} | {s['tarih']} | "
                            f"{s['icerik']} -- {sebep}")
    YENI_RAPOR.write_text("\n".join(satirlar) + "\n", encoding="utf-8")



# ----------------------------------------------------------- sperm (v6.180)
#
# Kullanıcının isteği (2026-09-25): "Excel'deki sperm sayfaları da programa
# alınsın. Cryo Haritalar bölümünde Sperm Dondurma diye bir bölüm olsun oraya
# harita eklensin. Tedavi hastalarına bağlama seçeneği olsun." Kararları:
# - **erkek için kayıt açılır** ("Eşinin adı olan kadın hasta olabilir,
#   karışıklık olur") -- satır EŞİ adından çiftin kaydına bağlanmıyor;
# - **otomatik bağ yok**: eski dondurmalarda dosya numarası yazmıyordu,
#   eşleştirmeyi kullanıcı elle yapıyor (hasta kartı, v6.180);
# - **her satır bir tüp** ("tek hastanın 3 tüp spermi dondurulduysa cryo
#   haritada 3 satır işgal ediyor"): aynı adın satırları TEK hasta kaydında
#   toplanıyor, her satır o kaydın altında bir `sperm_dondurma` + bir taşıyıcı
#   (programın kuralı: bir sperm dondurma kaydı = bir taşıyıcı, v6.84).
#
# Hasta: aynı ad kelime kümesinde yalnızca-sperm (tedavisi olmayan) TEK bir
# kayıt varsa onun altına ekleniyor -- programda daha önce açılmış erkek ya da
# bu aracın önceki çalıştırması. Çift kaydına (kadının adı) hiç bakılmıyor.
# Yoksa geçici dosya numarasıyla (v6.179'un tabanı) yeni kayıt.
#
# Tüp zaten programdaysa (aynı ad, aynı gün, aynı konum) "zaten"; programda
# o gün kaydı olup konumu boşsa konum yazılıyor (elle girilmiş dondurma);
# konumu farklıysa dokunulmuyor. İkinci çalıştırma hiçbir şeyi değiştirmez.
#
# Dondurma sebebi: HÜCRE'de "CA" geçiyorsa (EJAKÜLAT-CA, CA-SPERM, TESE-CA)
# "Onkolojik" -- kullanıcının cevabı (2026-09-25): "CA kanser"; yoksa TESE/
# TESA ("TESE/TESA yazılsın"). Değerler programın sebep önerisinden
# (`app.SPERM_DONDURMA_SEBEPLERI`). Başka sebep uydurulmuyor. Uydurulmayanlar: hacim/konsantrasyon/motilite ("9 MİLYON %35" ml başına mı toplam mı belli
# değil) -- HÜCRE ve VİAL metni olduğu gibi nota yazılıyor. Tarihi olmayan ya
# da ileri tarihli (2027/2028 yazım hatası) satır açılmıyor: dondurma zamanı
# zorunlu alan, tarih uydurulmuyor; raporda, kullanıcı elle girer.

SPERM_RAPOR = Path("cryo_esle_rapor_sperm.txt")
ONKOLOJIK = "Onkolojik"              # app.SPERM_DONDURMA_SEBEPLERI'nin değeri
_CA = re.compile(r"(?<![A-ZÇĞİÖŞÜ])CA(?![A-ZÇĞİÖŞÜ])")
_TESE_TESA = re.compile(r"(?<![A-ZÇĞİÖŞÜ])(TESE|TESA)(?![A-ZÇĞİÖŞÜ])")
_SPERM_SAAT = 10                     # dondurma saati bilinmiyor
_KONUMSUZ_SAYFA = re.compile(r"^(?:SAYFA|SHEET)\s*\d*$")

SPERM_SINIFLARI = [
    ("yeni", "yeni tüp açılacak", True),
    ("konum_yaz", "programda o gün kaydı var, konumu boş -- konum yazılacak", True),
    ("sebep_yaz", "zaten programda, dondurma sebebi yazılacak", True),
    ("zaten", "zaten programda (aynı ad, gün ve konum)", False),
    ("baska_konum", "programda o gün kaydı var, konumu FARKLI -- dokunulmadı", False),
    ("tarih_yok", "tarih yok ya da okunamadı -- açılmadı, elle girilmeli", False),
    ("tarih_ileri", "tarih bugünden ileri (yazım hatası) -- açılmadı", False),
    ("ayni_ad", "aynı adla birden çok yalnızca-sperm hasta kaydı -- açılmadı", False),
    ("es_belirsiz", "aynı adla iki farklı eş var, bu satırda eş yazmıyor -- açılmadı",
     False),
]


def _sperm_yolu(s):
    """Excel satırının konum yolu; sayfanın tankı bilinmiyorsa None.
    "Sayfa1"in bandı yok, tank adı sayfa adından geliyordu ("SAYFA1") --
    haritada uydurma bir tank açmaktansa konum boş kalıyor, nota yazılıyor."""
    if _KONUMSUZ_SAYFA.match(cryo_excel._n(s["tank"])):
        return None
    return " / ".join(x.strip() for x in _seviyeler(s) if x and x.strip()) or None


def _sperm_sebebi(s):
    """HÜCRE'den dondurma sebebi; yoksa None. "CA" (kanser) -> "Onkolojik",
    yoksa "TESE"/"TESA" (kullanıcı, 2026-09-25: "TESE/TESA yazılsın") --
    ikisi de `app.SPERM_DONDURMA_SEBEPLERI`'nin değeri. Alan tek: "TESE-CA"da
    sebep kanser, TESE yöntem; Onkolojik kazanıyor, HÜCRE'nin tamamı notta."""
    m = cryo_excel.buyuk(s["icerik"])
    if _CA.search(m):
        return ONKOLOJIK
    t = _TESE_TESA.search(m)
    return t.group(1) if t else None


def _sperm_programda(b):
    """{(ad kelimeleri, gün): [kayıt]} -- programdaki iptal edilmemiş dondurmalar."""
    d = collections.defaultdict(list)
    for r in b.execute(
            "SELECT sd.id, sd.hasta_id, h.ad_soyad, date(sd.dondurma_zamani) AS gun, "
            "  t.id AS tid, t.konum_id, k.tam_yol, sd.sebep, sd.notlar "
            "FROM sperm_dondurma sd JOIN hasta h ON h.id = sd.hasta_id "
            "JOIN tasiyici t ON t.id = sd.tasiyici_id "
            "LEFT JOIN konum k ON k.id = t.konum_id "
            "WHERE sd.lab_id = ? AND sd.iptal_mi = 0 ORDER BY sd.id", (_db.LAB_ID,)):
        d[(cryo_excel.kelimeler(r[2]), r[3])].append(
            {"sid": r[0], "hid": r[1], "tid": r[4], "konum_id": r[5], "tam_yol": r[6],
             "sebep": r[7],
             # Bu aracın açtığı kayıt: sebebi sonradan yazılabilir (v6.180'in
             # ilk hali sebep yazmıyordu). Ekrandan girilmişe dokunulmuyor.
             "excel": _db.CRYO_EXCEL_ISARETI in (r[8] or "")})
    return d


def _sperm_hastalari(b):
    """{ad kelimeleri: [(id, es_adi)]} -- tedavisi olmayan, sperm kaydı olan."""
    d = collections.defaultdict(list)
    for hid, ad, es in b.execute(
            "SELECT h.id, h.ad_soyad, h.es_adi FROM hasta h WHERE h.lab_id = ? "
            "AND NOT EXISTS (SELECT 1 FROM cycle c WHERE c.hasta_id = h.id) "
            "AND EXISTS (SELECT 1 FROM sperm_dondurma sd WHERE sd.hasta_id = h.id "
            "            AND sd.iptal_mi = 0)", (_db.LAB_ID,)):
        d[cryo_excel.kelimeler(ad)].append((hid, cryo_excel.buyuk(es) if es else ""))
    return d


def _ad(s):
    return cryo_excel.kelimeler(f'{s["soyad"]} {s["ad"]}')


def sperm_plani(satirlar, b):
    """Excel'in sperm satırları -> [(satır, sınıf, ek)] ve hasta planı.

    Dönen `sonuc` satır satır; `yeni` satırlar ayrıca `kisi` anahtarı taşıyor:
    ("var", hasta_id) ya da ("yeni", grup no). Grup = açılacak bir hasta."""
    bugun = _dt.date.today().isoformat()
    programda = _sperm_programda(b)
    hastalar_ = _sperm_hastalari(b)
    sonuc = []
    adaylar = []
    gruplar = collections.defaultdict(list)          # (ad, gün) -> satırlar
    for s in satirlar:
        if s["kategori"] != "sperm":
            continue
        if not s["tarih"]:
            sonuc.append([s, "tarih_yok", s["tarih_notu"] or ""])
        elif s["tarih"] > bugun:
            sonuc.append([s, "tarih_ileri", ""])
        else:
            gruplar[(_ad(s), s["tarih"])].append(s)
    for anahtar, grup in gruplar.items():
        mevcut = list(programda.get(anahtar, []))
        kalan = []
        for s in grup:                               # önce aynı konum
            yol = _sperm_yolu(s)
            k = next((m for m in mevcut if m["tam_yol"] == yol), None)
            if k is None and yol is None and mevcut:
                k = mevcut[0]                        # konumsuz satır bilgi eklemiyor
            if k:
                mevcut.remove(k)
                if k["excel"] and not k["sebep"] and _sperm_sebebi(s):
                    sonuc.append([s, "sebep_yaz", k])
                else:
                    sonuc.append([s, "zaten", f"sperm kaydı {k['sid']}"])
            else:
                kalan.append(s)
        for s in kalan:
            bos = next((m for m in mevcut if m["konum_id"] is None), None)
            if bos and _sperm_yolu(s):
                mevcut.remove(bos)
                sonuc.append([s, "konum_yaz", bos])
            elif mevcut:
                sonuc.append([s, "baska_konum",
                              f"programdaki konum: {mevcut[0]['tam_yol'] or '-'}"])
            else:
                adaylar.append(s)
    # Yeni satırların hastası: ada göre topla, eşe göre ayır.
    ada_gore = collections.defaultdict(list)
    for s in adaylar:
        ada_gore[_ad(s)].append(s)
    kisiler = []                                     # [(ad, eş, [satır])]
    for kel, grup in ada_gore.items():
        esler = sorted({cryo_excel.buyuk(s["es_adi"]) for s in grup if s["es_adi"].strip()})
        parcalar = ([(esler[0] if esler else "", grup)] if len(esler) <= 1 else
                    [(es, [s for s in grup if cryo_excel.buyuk(s["es_adi"]) == es])
                     for es in esler])
        if len(esler) > 1:
            for s in grup:
                if not s["es_adi"].strip():
                    sonuc.append([s, "es_belirsiz", ""])
        for es, satirlar_ in parcalar:
            uygun = [h for h, hes in hastalar_.get(kel, []) if not es or not hes or hes == es]
            if len(uygun) > 1:
                for s in satirlar_:
                    sonuc.append([s, "ayni_ad", f"{len(uygun)} kayıt"])
                continue
            if uygun:
                kisi = ("var", uygun[0])
            else:
                kisi = ("yeni", len(kisiler))
                kisiler.append((kel, es, satirlar_))
            for s in satirlar_:
                sonuc.append([s, "yeni", kisi])
    return sonuc, kisiler


def _sperm_notu(s, yol):
    parca = [f'Örnek: {s["icerik"] or "-"}', f'VİAL: {s["vial_metni"] or "-"}']
    if not yol:
        parca.append(f'Excel\'deki yer: {_tam_yol(s)} (tankı yazmıyor)')
    return (" · ".join(parca) + f'\nCryo Haritası Excel\'i: {s["sayfa"]} satır {s["satir"]}\n'
            + _db.CRYO_EXCEL_ISARETI)


def _sperm_etiketi(b, dosya_no, gun, dakika):
    """Programın sperm formunun kalıbı: `<dosya no>-SP-<SSDD>` (v6.84). Saat
    bilinmiyor; aynı hastanın aynı gün birden çok tüpü dakika dakika ilerliyor
    (`aktar_access._tasiyici_ac()`'nin embriyo tüpleri için yaptığı gibi)."""
    while True:
        s, d = divmod(_SPERM_SAAT * 60 + dakika, 60)
        etiket = f"{dosya_no}-SP-{s:02d}{d:02d}"
        if not b.execute("SELECT 1 FROM tasiyici WHERE lab_id=? AND etiket=?",
                         (_db.LAB_ID, etiket)).fetchone():
            return etiket, f"{gun} {s:02d}:{d:02d}:00", dakika
        dakika += 1


def sperm_yaz(satirlar) -> dict:
    sayac = collections.Counter()
    with _db.yazma_islemi() as b:
        sonuc, kisiler = sperm_plani(satirlar, b)   # kilit içinde yeniden
        kid = _kullanici_id(b)
        simdi = _dt.datetime.now().isoformat(" ", "seconds")
        tipler = {r[0] for r in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_tipi'",
            (_db.LAB_ID,))}
        renkler, _ = _renk_kodlari(b, {s["renk"] for s in satirlar if s["renk"]})
        dosya = max(GECICI_DOSYA_TABANI, b.execute(
            "SELECT COALESCE(MAX(dosya_no),0) FROM hasta WHERE lab_id=?",
            (_db.LAB_ID,)).fetchone()[0])
        hasta_id = {}
        for i, (_kel, es, grup) in enumerate(kisiler):
            dosya += 1
            b.execute(
                "INSERT INTO hasta (lab_id, dosya_no, ad_soyad, es_adi, notlar, durum, "
                "olusturma_zamani) VALUES (?,?,?,?,?,'aktif',?)",
                (_db.LAB_ID, dosya, _yeni_ad(grup[0]), es or None,
                 "Cryo Haritası Excel'inden açıldı (v6.180, sperm dondurma). GEÇİCİ "
                 "dosya numarası -- gerçek numara dosya_no_degistir.py ile yazılmalı.",
                 f"{min(s['tarih'] for s in grup)} 08:00:00"))
            hasta_id[i] = b.execute("SELECT last_insert_rowid()").fetchone()[0]
            sayac["hasta"] += 1
        dakikalar = collections.Counter()
        for s, sinif, ek in sonuc:
            if sinif == "sebep_yaz":
                b.execute("UPDATE sperm_dondurma SET sebep=? WHERE id=? AND sebep IS NULL",
                          (_sperm_sebebi(s), ek["sid"]))
                b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                          "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                          (_db.LAB_ID, "sperm_dondurma", str(ek["sid"]), "sebep", None,
                           _sperm_sebebi(s), kid, simdi))
                sayac["sebep"] += 1
                continue
            if sinif == "konum_yaz":
                yol = _sperm_yolu(s)
                konum_id = _db.konum_bul_veya_olustur(_seviyeler(s), b)
                b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?", (konum_id, ek["tid"]))
                b.execute("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))
                b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                          "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                          (_db.LAB_ID, "tasiyici", str(ek["tid"]), "konum", None, yol,
                           kid, simdi))
                sayac["konum"] += 1
                continue
            if sinif != "yeni":
                continue
            tur, deger = ek
            hid = deger if tur == "var" else hasta_id[deger]
            dno = b.execute("SELECT dosya_no FROM hasta WHERE id=?", (hid,)).fetchone()[0]
            yol = _sperm_yolu(s)
            konum_id = _db.konum_bul_veya_olustur(_seviyeler(s), b) if yol else None
            etiket, an, dk = _sperm_etiketi(b, dno, s["tarih"], dakikalar[(hid, s["tarih"])])
            dakikalar[(hid, s["tarih"])] = dk + 1
            # Tip: Excel'in sütunu "VİAL" ve STRAW yalnızca dış merkezden gelen
            # birkaç satırda ayrıca yazılmış -- yazmayan satır vial.
            tip = s["tip"] if s["tip"] in tipler else "vial"
            b.execute(
                "INSERT INTO tasiyici (lab_id, tip, etiket, renk, konum_id, "
                "vitrifikasyon_zamani, kullanici_id, durum, kategori) "
                "VALUES (?,?,?,?,?,?,?,'dolu','sperm')",
                (_db.LAB_ID, tip, etiket, s["renk"] if s["renk"] in renkler else None,
                 konum_id, an, kid))
            tid = b.execute("SELECT last_insert_rowid()").fetchone()[0]
            if konum_id:
                b.execute("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))
            b.execute(
                "INSERT INTO sperm_dondurma (lab_id, hasta_id, tasiyici_id, dondurma_zamani, "
                "sebep, notlar, kullanici_id, olusturma_zamani) VALUES (?,?,?,?,?,?,?,?)",
                (_db.LAB_ID, hid, tid, an, _sperm_sebebi(s), _sperm_notu(s, yol), kid, an))
            sayac["tup"] += 1
            if _sperm_sebebi(s):
                sayac["sebep"] += 1
            if tur == "var":
                sayac["mevcut_hastaya"] += 1
    return sayac


def sperm_raporu(sonuc, kisiler, b):
    adlar = {hid: ad for hid, ad in b.execute(
        "SELECT id, dosya_no || ' ' || ad_soyad FROM hasta WHERE lab_id=?", (_db.LAB_ID,))}
    sayac = collections.Counter(k for _s, k, _e in sonuc)
    c = [f"CRYO EXCEL -- SPERM DONDURMA -- {_dt.datetime.now():%Y-%m-%d %H:%M:%S}", ""]
    for kod, baslik, yazilir in SPERM_SINIFLARI:
        n = sayac.get(kod, 0)
        c.append(f"== {baslik}: {n}" + ("  [yazılır]" if yazilir else ""))
        for s, k, ek in sonuc:
            if k != kod:
                continue
            if kod == "yeni":
                tur, deger = ek
                ek = (f"mevcut kayda: {adlar.get(deger, deger)}" if tur == "var"
                      else f"yeni hasta #{deger + 1}")
            elif kod in ("konum_yaz", "sebep_yaz"):
                ek = f"sperm kaydı {ek['sid']}"
            es = f' (eşi {s["es_adi"]})' if s["es_adi"] else ""
            c.append(f'   {_yer(s):40} | {s["soyad"]} {s["ad"]}{es} | '
                     f'{s["tarih"] or s["tarih_notu"] or "tarih?"} | {s["icerik"]} | '
                     f'{s["vial_metni"]}' + (f"  | {ek}" if ek else ""))
        c.append("")
    SPERM_RAPOR.write_text("\n".join(c) + "\n", encoding="utf-8")
    return sayac


# ------------------------------------------- programda dolu, Excel'de yok

EKSIK_RAPOR = Path("cryo_esle_rapor_eksik.txt")
EKSIK_SINIFLARI = [
    ("ad_farkli", "Excel'de aynı gün, aynı içerikli ama adı programdakiyle tutmayan "
                  "satır var -- büyük olasılıkla ad farklı yazılmış, tüp tankta"),
    ("excel_yok", "Hastanın Excel'de HİÇ satırı yok -- başka merkeze taşınmış, "
                  "çözülmüş ama programa yazılmamış ya da Excel'de eksik olabilir"),
    ("ayni_ad", "Excel'de aynı adlı birden çok hasta var, satır hastaya atanamadı"),
    ("satiri_var", "Hastanın Excel'de satırı var ama bu tüple eşleşmedi "
                   "(tarih/içerik tutmuyor olabilir -- önce Excel satırına bakın)"),
]


def _bagsiz_fetler(b) -> dict:
    """{hasta id: [çözme günü, ...]} -- aktarılmış ama tüpüne bağlanmamış FET
    (embriyoları FET'in kendi altında duruyor, v6.130). Böyle bir hastanın
    'dolu' tüpü aslında çözülmüş olabilir."""
    sonuc = collections.defaultdict(list)
    yer = ",".join("?" * len(_db.FET_TIPLERI))
    for r in b.execute(
            "SELECT c.hasta_id, (SELECT substr(MIN(o.zaman),1,10) FROM olay o "
            "JOIN specimen s ON s.id=o.specimen_id WHERE s.cycle_id=c.id "
            "AND o.iptal_mi=0 AND o.tip IN ('thaw','transfer')) gun FROM cycle c "
            f"WHERE c.lab_id=? AND c.cycle_tipi IN ({yer}) "
            "AND c.protokol_notu LIKE '%[Access kaydı%' "
            "AND EXISTS (SELECT 1 FROM specimen s WHERE s.cycle_id=c.id)",
            (_db.LAB_ID, *_db.FET_TIPLERI)):
        sonuc[r["hasta_id"]].append(r["gun"] or "?")
    return sonuc


def eksik_plani(sonuc, satirlar, idx, tup, b):
    """Programda DOLU olup Excel'in hiçbir satırının almadığı embriyo/yumurta
    tüpleri (v6.182, kullanıcının bilgisi: hastalar embriyolarını bazen başka
    bir tüp bebek ünitesine taşıtıyor). **Hiçbir şey yazmaz**: liste
    kullanıcının incelemesi için; taşınanı tüpün sayfasından kendisi
    işaretler. Excel'in son tarihinden sonra dondurulan tüpler sayılıyor,
    listelenmiyor (Excel o günü henüz görmedi).

    -> (sınıf -> [(hasta id, tüp, ek not)], Excel'den yeni tüp sayısı, son gün)
    """
    alinan = {t["tid"] for _s, _k, t, _e in sonuc if t}
    gunler = [s["tarih"] for s in satirlar if s["kategori"] != "sperm" and s["tarih"]]
    excel_son = max(gunler) if gunler else "9999"
    hasta_satiri = collections.defaultdict(list)
    for s_, k, t, _e in sonuc:
        if s_.get("hid"):
            hasta_satiri[s_["hid"]].append((s_, k))
    belirsiz = set()
    for s_, k, _t, _e in sonuc:
        if k == "hasta_cok":
            ad = cryo_excel.kelimeler((s_["soyad"] or "") + " " + (s_["ad"] or ""))
            belirsiz.update(a[0] for a in idx.get(ad, []))
    # Hastaya atanamayan Excel satırları, güne göre: adı farklı yazılmış
    # olabilir -- aynı gün aynı içerik güçlü bir iz.
    sahipsiz = collections.defaultdict(list)
    for s_, k, _t, _e in sonuc:
        if k in ("hasta_yok", "hasta_cok") and s_["tarih"]:
            sahipsiz[s_["tarih"]].append(s_)
    fet = _bagsiz_fetler(b)
    plan = collections.defaultdict(list)
    yeni = 0
    for hid, tuplar in tup.items():
        for t in tuplar:
            if t["durum"] != "dolu" or t["tid"] in alinan:
                continue
            if (t["gun"] or "") > excel_son:
                yeni += 1
                continue
            notlar = []
            if fet.get(hid):
                notlar.append("tüpüne bağlanmamış aktarılmış FET: "
                              + ", ".join(sorted(fet[hid])))
            benzer = [x for x in sahipsiz.get(t["gun"], [])
                      if any(_uyar(ic, t["skorlar"])
                             for ic in (excel_icerik(x["icerik"]) or []))]
            if benzer and not hasta_satiri.get(hid):
                notlar.insert(0, "Excel: " + " ; ".join(
                    f'{x["soyad"] or ""} {x["ad"] or ""} (eşi {x["es_adi"] or "?"}) '
                    f'{_yer(x)} {x["icerik"]}' for x in benzer))
                plan["ad_farkli"].append((hid, t, " | ".join(notlar)))
                continue
            if hasta_satiri.get(hid):
                es = [f'{_yer(x)} {x["tarih"] or "tarih?"} {x["icerik"]} [{k}]'
                      for x, k in hasta_satiri[hid] if k not in YAZILIR | {"zaten"}]
                if es:
                    notlar.append("eşleşmeyen Excel satırları: " + " ; ".join(es))
                plan["satiri_var"].append((hid, t, " | ".join(notlar)))
            elif hid in belirsiz:
                plan["ayni_ad"].append((hid, t, " | ".join(notlar)))
            else:
                plan["excel_yok"].append((hid, t, " | ".join(notlar)))
    return plan, yeni, excel_son


def eksik_raporu(plan, yeni, excel_son, b):
    kim = {r["id"]: r for r in b.execute(
        "SELECT id, dosya_no, ad_soyad FROM hasta WHERE lab_id=?", (_db.LAB_ID,))}
    satirlar = [f"PROGRAMDA DOLU, CRYO EXCEL'İNDE KARŞILIĞI OLMAYAN TÜPLER -- "
                f"{_dt.datetime.now().isoformat(' ', 'seconds')}",
                "Bu liste hiçbir şeyi değiştirmez. Başka merkeze taşınan tüpü "
                "programda tüpün sayfasından işaretleyin",
                "(arama kutusuna tüp etiketini yazın -> tüp -> \"Başka merkeze "
                "taşındı olarak işaretle\").",
                f"Excel'in son tarihi {excel_son}; ondan sonra dondurulan {yeni} "
                "tüp listelenmedi.", ""]
    for kod, baslik in EKSIK_SINIFLARI:
        liste = sorted(plan.get(kod, []), key=lambda x: (x[1]["gun"] or "", x[1]["etiket"]))
        satirlar.append(f"== {baslik}: {len(liste)}")
        for hid, t, ek in liste:
            h = kim.get(hid)
            konum = t["tam_yol"] or "konum yok"
            satirlar.append(
                f'   {h["dosya_no"] if h else "?"} | {h["ad_soyad"] if h else "?"} | '
                f'tüp {t["etiket"]} | {t["gun"]} | [{"-".join(t["skorlar"])}] | {konum}'
                + (f"  | {ek}" if ek else ""))
        satirlar.append("")
    EKSIK_RAPOR.write_text("\n".join(satirlar) + "\n", encoding="utf-8")


def _eksik_kipi(sonuc, satirlar, idx, tup):
    with _db.baglan() as b:
        plan, yeni, excel_son = eksik_plani(sonuc, satirlar, idx, tup, b)
        eksik_raporu(plan, yeni, excel_son, b)
    print("Programda dolu, Excel'de karşılığı olmayan tüpler (hiçbir şey yazılmadı):")
    for kod, baslik in EKSIK_SINIFLARI:
        print(f"  {len(plan.get(kod, [])):5}  {baslik}")
    print(f"  {yeni:5}  Excel'in son tarihinden ({excel_son}) sonra dondurulmuş -- "
          "listelenmedi")
    print(f"Ayrıntı: {EKSIK_RAPOR}")


def _sperm_kipi(satirlar):
    with _db.baglan() as b:
        sonuc, kisiler = sperm_plani(satirlar, b)
        sayac = sperm_raporu(sonuc, kisiler, b)
    toplam = sum(1 for s in satirlar if s["kategori"] == "sperm")
    print(f"Excel: {toplam} sperm satırı (her satır bir tüp).")
    for kod, baslik, yazilir in SPERM_SINIFLARI:
        if sayac.get(kod):
            print(f"  {sayac[kod]:5}  {baslik}" + ("  [yazılır]" if yazilir else ""))
    mevcut = sum(1 for _s, k, e in sonuc if k == "yeni" and e[0] == "var")
    print(f"Yeni hasta kaydı: {len(kisiler)} (geçici dosya numarasıyla); "
          f"programdaki erkek kayıtlarına eklenecek tüp: {mevcut}.")
    print(f"Ayrıntı: {SPERM_RAPOR}")
    sebepler = collections.Counter(_sperm_sebebi(s) for s, k, _e in sonuc
                                   if k == "yeni" and _sperm_sebebi(s))
    if sebepler:
        print("Yeni tüplerin dondurma sebebi (HÜCRE'den): "
              + ", ".join(f"{a} {n}" for a, n in sebepler.most_common()) + ".")
    if not (sayac.get("yeni") or sayac.get("konum_yaz") or sayac.get("sebep_yaz")):
        print("Yazılacak bir şey yok.")
        return
    print("\nDevam için SPERM yazın:")
    if input("> ").strip() != "SPERM":
        print("Vazgeçildi, hiçbir şey yazılmadı.")
        return
    y = sperm_yaz(satirlar)
    print(f"Yazıldı: {y['hasta']} yeni hasta, {y['tup']} tüp"
          + (f" (programdaki kayıtlara eklenen: {y['mevcut_hastaya']})" if y["mevcut_hastaya"] else "")
          + f", {y['konum']} tüpe konum, {y['sebep']} kayda dondurma sebebi.")


# ------------------------------------------------------------------- main

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("liste", "uygula", "yeni_hasta", "sperm",
                                                 "eksik", "onar", "yerlesim"):
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
    if kip == "sperm":
        return _sperm_kipi(cozum["satirlar"])
    with _db.baglan() as b:
        idx = hastalar(b)
        tup = tupler(b)
    print(f"Program: {sum(len(v) for v in idx.values())} hasta, "
          f"{sum(len(v) for v in tup.values())} dondurma tüpü.")
    sonuc = esle(cozum["satirlar"], idx, tup)
    if kip == "yeni_hasta":
        return _yeni_hasta_kipi(sonuc)
    if kip == "eksik":
        return _eksik_kipi(sonuc, cozum["satirlar"], idx, tup)
    if kip == "onar":
        return _onar_kipi(sonuc)
    if kip == "yerlesim":
        return _yerlesim_kipi(dosya, cozum, sonuc)
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
             if y["tip_kodu_eklendi"] else "")
          + (f"; {y['renk_kodu_eklendi']} renk listeye eklendi"
             if y["renk_kodu_eklendi"] else "") + ".")


def _yeni_hasta_kipi(sonuc):
    plan, atlanan = yeni_hasta_plani(sonuc)
    yeni_hasta_raporu(plan, atlanan)
    tedavi = sum(len(_tedavileri(g)) for _k, _e, g in plan)
    tup = sum(len(excel_ogeleri(s["icerik"])) for _k, _e, g in plan for s in g)
    ornek = sum(len(t) for _k, _e, g in plan for s in g for t in excel_ogeleri(s["icerik"]))
    print(f"{YENI_HASTA_SON} öncesi, programda olmayan hasta: {len(plan)} hasta, "
          f"{tedavi} tedavi, {tup} tüp, {ornek} örnek açılacak.")
    if atlanan:
        print(f"Açılmayacak satır: {len(atlanan)} (sebepleri raporda).")
    print(f"Ayrıntı: {YENI_RAPOR}")
    if not plan:
        return
    print("\nHastalar GEÇİCİ dosya numarasıyla açılacak. Devam için HASTA yazın:")
    if input("> ").strip() != "HASTA":
        print("Vazgeçildi, hiçbir şey yazılmadı.")
        return
    y = yeni_hasta_yaz(plan)
    print(f"Açıldı: {y['hasta']} hasta, {y['tedavi']} tedavi, {y['tup']} tüp, "
          f"{y['ornek']} örnek" + (f" ({y['skorsuz']} embriyonun skoru okunamadı, "
                                   "skorsuz)" if y["skorsuz"] else "") + ".")


if __name__ == "__main__":
    main()
