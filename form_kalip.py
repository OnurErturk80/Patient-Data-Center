"""Resmî formların kalıbı — kâğıt aslından çıkarılmış ızgara.

`form_kalip.json` iki formun **birebir** ızgarasını tutuyor: satır yükseklikleri,
sütun genişlikleri, birleşik hücreler, her hücrenin punto/kalınlık/hiza/kenarlık
bilgisi ve kâğıtta basılı olan metinler. Veri `formlar_asil/` altındaki iki
orijinal `.xls` dosyasından `formlar_asil/kalip_uret.py` ile çıkarıldı — elle
yazılmadı, o yüzden kâğıtla arasında fark yok (aslındaki yazım hataları bile
duruyor: "TRANSFES EMBRİYOLOG", "Nukleus durmu", "Labratuvar").

**Kalıba dokunma.** Doküman kodu, revizyon tarihi, alan adları ve form numarası
kurumun kalite sisteminden geliyor. Bir şey değişecekse kâğıt asıl değişir,
sonra `kalip_uret.py` yeniden çalıştırılır.

Aynı ızgara iki yere basılıyor:

  - **ekran/yazdırma**: `satirlar()` -> `form.html` bir HTML tablosu kuruyor
  - **Excel**: `yerlesim()` -> `excel.kitap()`'ın yerleşim sayfası

İkisi tek kaynaktan geldiği için birbirinden ayrı düşemiyor.

Doldurma iki türlü:

  - `deger[(satır, sütun)]`  kâğıtta **boş** olan kutuya yazar
  - `ek[(satır, sütun)]`     kâğıtta basılı yazının **arkasına** ekler
    (kutunun içinde boşluk var; kalemle oraya yazılıyor)

Satır ve sütun numaraları **sıfırdan** başlıyor — Excel'in A1'i (0, 0).

**Amblem** de kalıbın parçası: üniversitenin logosu iki formda da .xls'in
içine gömülüydü, `kalip_uret.py` onu `static/form_amblem.png`'ye çıkardı.
Yeri Excel'in "sabitleyici"sinden (client anchor) geliyor — hangi hücreden
hangi hücreye, hücrenin yüzde kaçından başlayarak. Buradaki hesap onu hem
ekran için yüzde/puntoya hem Excel için EMU'ya çeviriyor.
"""

import json
import os

_YOL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "form_kalip.json")

with open(_YOL, encoding="utf-8") as _d:
    KALIPLAR = json.load(_d)

# Formun kâğıt yönü ve yazdırma alanına sığması için ölçek hesabında
# kullanılan yükseklik (punto). A4: dikey 297mm, yatay 210mm; kenar payı 8mm.
_SAYFA = {"ozet": ("dikey", 780.0), "artlab": ("yatay", 535.0)}

# Kenarlık numaraları kâğıt aslından; CSS sınıfı ve Excel'deki adı aynı
# numaradan türüyor (bkz. excel._CIZGI).
_KENAR_ADI = ("ust", "alt", "sol", "sag")
_HIZA = {1: "hsol", 2: "hort", 3: "hsag"}
_DIKEY = {0: "dust", 1: "dort", 2: "dalt"}


# Excel'in sabitleyicisi hücrenin kesrini kullanıyor: sütunda 1024'te kaç,
# satırda 256'da kaç. Excel'in uzunluk birimi EMU: puntoda 12700, pikselde
# 9525. Sütun genişliği kâğıtta 1/256 karakter; karakter ~7 piksel.
_SUTUN_KESIR, _SATIR_KESIR = 1024.0, 256.0
_EMU_PUNTO, _EMU_PIKSEL = 12700, 9525
_SUTUN_PIKSEL = 7.0 / 256.0


def yon(ad: str) -> str:
    return _SAYFA.get(ad, ("dikey", 780.0))[0]


def _x(k, sutun, kesir):
    """Sabitleyicinin yatay yerini kâğıdın sütun birimiyle verir."""
    gen = k["sutun"]
    once = sum(gen[:sutun])
    bu = gen[sutun] if sutun < len(gen) else 0
    return once + bu * kesir / _SUTUN_KESIR


def _y(k, satir, kesir):
    """Sabitleyicinin dikey yerini punto olarak verir."""
    yuk = k["satir_yuksekligi"]
    once = sum(h or 15.0 for h in yuk[:satir])
    bu = (yuk[satir] if satir < len(yuk) else None) or 15.0
    return once + bu * kesir / _SATIR_KESIR


def _gorsel_kutusu(k, g):
    """(sol, üst, genişlik, yükseklik) -- yatayda sütun birimi, dikeyde punto."""
    s1, dx1, r1, dy1, s2, dx2, r2, dy2 = g["sabit"]
    sol, sag = _x(k, s1, dx1), _x(k, s2, dx2)
    ust, alt = _y(k, r1, dy1), _y(k, r2, dy2)
    return sol, ust, max(0.0, sag - sol), max(0.0, alt - ust)


def _sinif(stil: dict) -> str:
    """Hücrenin CSS sınıfları: punto, kalınlık, hiza ve dört kenar."""
    p = ["p%d" % stil["pt"]]
    if stil["kalin"]:
        p.append("kln")
    if stil["yatay"] in _HIZA:
        p.append(_HIZA[stil["yatay"]])
    p.append(_DIKEY.get(stil["dikey"], "dort"))
    if stil["sar"]:
        p.append("sar")
    for ad, n in zip(_KENAR_ADI, stil["kenar"]):
        if n:
            p.append(f"{ad}{n}")
    return " ".join(p)


def _yazi(kalip_metni: str, deger, ekleme) -> str:
    """Kutuya basılacak son metin: kâğıttaki yazı + program verisi."""
    if deger is not None and str(deger) != "":
        return str(deger)
    if ekleme is not None and str(ekleme) != "":
        # Kâğıttaki yazı duruyor, program verisi arkasına yazılıyor.
        return (kalip_metni + "  " + str(ekleme)).strip()
    return kalip_metni


def satirlar(ad: str, deger=None, ek=None) -> dict:
    """Şablonun bastığı ızgara: sütun genişlikleri + satır satır hücreler.

    Ölçek: kâğıdın kendi punto ve satır yükseklikleri A4'e sığmıyor (Excel
    "sayfaya sığdır" ile basıyor). Aynısını tarayıcıda yapmak için bütün
    yükseklikler ve puntolar tek bir katsayıyla küçültülüyor — oranlar
    bozulmadığı için form aynı görünüyor.
    """
    k = KALIPLAR[ad]
    deger, ek = deger or {}, ek or {}

    toplam = sum(h or 15.0 for h in k["satir_yuksekligi"])
    hedef = _SAYFA.get(ad, ("dikey", 780.0))[1]
    olcek = min(1.0, hedef / toplam) if toplam else 1.0

    gen_toplam = sum(k["sutun"]) or 1
    sutunlar = [round(100.0 * g / gen_toplam, 4) for g in k["sutun"]]

    cikti = []
    for r, satir in enumerate(k["satirlar"]):
        hucreler = []
        for c, rs, cs, metin, stil_no in satir:
            stil = k["stiller"][stil_no] if stil_no is not None else None
            hucreler.append({
                "metin": _yazi(metin, deger.get((r, c)), ek.get((r, c))),
                "sinif": _sinif(stil) if stil else "",
                "satir_yayilim": rs,
                "sutun_yayilim": cs,
            })
        yukseklik = (k["satir_yuksekligi"][r] or 15.0) * olcek
        cikti.append({"yukseklik": round(yukseklik, 2), "hucreler": hucreler})

    # Amblem tablonun üstüne konuyor: yatayda kâğıdın yüzdesi, dikeyde
    # satırlarla aynı ölçekte punto -- tabloyla birlikte küçülüyor.
    gorseller = []
    for g in k.get("gorseller", []):
        sol, ust, gen, yuk = _gorsel_kutusu(k, g)
        gorseller.append({
            "dosya": g["dosya"],
            "sol": round(100.0 * sol / gen_toplam, 4),
            "genislik": round(100.0 * gen / gen_toplam, 4),
            "ust": round(ust * olcek, 2),
            "yukseklik": round(yuk * olcek, 2),
        })

    return {"sutunlar": sutunlar, "satirlar": cikti, "gorseller": gorseller,
            "olcek": round(olcek, 4), "yon": yon(ad)}


def yerlesim(ad: str, sayfa_adi: str, deger=None, ek=None) -> dict:
    """Aynı kalıbı `excel.kitap()`'ın yerleşim sayfası olarak kurar."""
    k = KALIPLAR[ad]
    deger, ek = deger or {}, ek or {}

    hucreler, birlesik = {}, []
    for r, satir in enumerate(k["satirlar"]):
        for c, rs, cs, metin, stil_no in satir:
            if stil_no is None:            # yalnızca yer tutan boş hücre
                continue
            adres = _adres(r, c)
            hucreler[adres] = (_yazi(metin, deger.get((r, c)), ek.get((r, c))),
                               stil_no)
            if rs > 1 or cs > 1:
                birlesik.append(f"{adres}:{_adres(r + rs - 1, c + cs - 1)}")

    gorseller = []
    for g in k.get("gorseller", []):
        s1, dx1, r1, dy1, s2, dx2, r2, dy2 = g["sabit"]
        gorseller.append({
            "dosya": g["dosya"],
            "bas": (s1, _emu_x(k, s1, dx1), r1, _emu_y(k, r1, dy1)),
            "bit": (s2, _emu_x(k, s2, dx2), r2, _emu_y(k, r2, dy2)),
        })

    return {
        "ad": sayfa_adi,
        "hucreler": hucreler,
        "birlesik": birlesik,
        "gorseller": gorseller,
        "stiller": k["stiller"],
        # Excel sütun genişliği karakter cinsinden; kâğıttaki 1/256 karakter.
        "genislikler": {c + 1: round(g / 256.0, 2)
                        for c, g in enumerate(k["sutun"])},
        "yukseklikler": {r + 1: h for r, h in
                         enumerate(k["satir_yuksekligi"]) if h},
        "yazdirma": {"yon": yon(ad), "sigdir": True, "kenar": 0.3},
    }


def _adres(r: int, c: int) -> str:
    """(0, 0) -> "A1"."""
    harf, n = "", c + 1
    while n:
        n, kalan = divmod(n - 1, 26)
        harf = chr(65 + kalan) + harf
    return f"{harf}{r + 1}"


def _emu_x(k, sutun, kesir):
    """Sütun içindeki kayma, EMU. Excel hücrenin kendi içinde ölçüyor."""
    gen = k["sutun"][sutun] if sutun < len(k["sutun"]) else 0
    return int(round(gen * _SUTUN_PIKSEL * kesir / _SUTUN_KESIR * _EMU_PIKSEL))


def _emu_y(k, satir, kesir):
    """Satır içindeki kayma, EMU."""
    yuk = k["satir_yuksekligi"]
    h = (yuk[satir] if satir < len(yuk) else None) or 15.0
    return int(round(h * kesir / _SATIR_KESIR * _EMU_PUNTO))
