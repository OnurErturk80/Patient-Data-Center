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


def yon(ad: str) -> str:
    return _SAYFA.get(ad, ("dikey", 780.0))[0]


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

    return {"sutunlar": sutunlar, "satirlar": cikti,
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

    return {
        "ad": sayfa_adi,
        "hucreler": hucreler,
        "birlesik": birlesik,
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
