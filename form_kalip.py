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
import re

_YOL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "form_kalip.json")

# Dosya yoksa program yine calisir, yalnizca gomulu form olmaz. Ticari
# dagitimda bu laboratuvarin kurum formlari depodan cikacak (form_kalip.json
# + static/form_amblem.png silinir); o zaman burada kod degistirmek
# gerekmesin diye eksiklige tahammul ediyor. Her lab kendi formunu yukluyor.
try:
    with open(_YOL, encoding="utf-8") as _d:
        KALIPLAR = json.load(_d)
except (OSError, ValueError):
    KALIPLAR = {}

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


# Kutulara yazılan etiket: {{dosya_no}} (v6.40). Yalnızca küçük harf, rakam
# ve alt çizgi -- yüklenen dosyadan gelen metinle düzenli ifade kuruyoruz,
# dar tutmak hem yazım hatasını hem sürprizi engelliyor.
_ETIKET = re.compile(r"\{\{\s*([a-z0-9_]{1,40})\s*\}\}")


def _kalip_al(kaynak):
    """Kaynak ya gömülü kalıbın adı ya da yüklenmiş bir kalıp sözlüğü."""
    return KALIPLAR[kaynak] if isinstance(kaynak, str) else kaynak


def _sayfa_olcusu(kaynak):
    """(yön, A4'e sığması için hedef yükseklik -- punto)."""
    if isinstance(kaynak, str):
        return _SAYFA.get(kaynak, ("dikey", 780.0))
    y = "yatay" if kaynak.get("yon") == "yatay" else "dikey"
    return (y, 535.0 if y == "yatay" else 780.0)


def yon(kaynak) -> str:
    return _sayfa_olcusu(kaynak)[0]


def olcu(kaynak) -> tuple:
    """(satır sayısı, sütun sayısı) -- kalıbın **dışına** bir şey eklemek
    isteyen kod (v6.104, ART Lab'ın alt kısmındaki iptal notu) nereden
    başlayacağını buradan öğreniyor. Kalıbın kendisine dokunmuyor.
    """
    k = _kalip_al(kaynak)
    return len(k["satirlar"]), len(k["sutun"])


def hucre_adresi(satir: int, sutun: int) -> str:
    """`_adres()`'in dışarıdan da çağrılabilen hali: (0, 0) -> "A1"."""
    return _adres(satir, sutun)


def etiketleri_doldur(metin: str, alan) -> str:
    """`{{dosya_no}}` -> değer. Tanınmayan etiket **olduğu gibi kalır**.

    Bilerek: yazım hatası yapılmış bir etiket ("{{dosyano}}") formda göze
    çarpsın, sessizce boş kutu olarak geçmesin. Yükleme ekranı da dosyadaki
    tanınmayan etiketleri sayıp uyarıyor.
    """
    if not metin or "{{" not in metin:
        return metin

    def degistir(e):
        ad = e.group(1)
        if ad not in alan:
            return e.group(0)
        deger = alan[ad]
        return "" if deger is None else str(deger)

    return _ETIKET.sub(degistir, metin)


def etiketler(kaynak) -> list:
    """Kalıpta geçen bütün `{{...}}` etiketleri, geçiş sırasıyla ve tekrarsız."""
    k = _kalip_al(kaynak)
    bulunan = []
    for satir in k["satirlar"]:
        for _c, _rs, _cs, metin, _stil in satir:
            for ad in _ETIKET.findall(metin or ""):
                if ad not in bulunan:
                    bulunan.append(ad)
    return bulunan


# --------------------------------------------------------------- ızgara kurma
#
# Kalıbı iki yer üretiyor: `formlar_asil/kalip_uret.py` (kâğıt aslındaki .xls'ten,
# tek seferlik) ve `xlsx_oku.py` (yöneticinin yüklediği .xlsx'ten, çalışma
# anında). İkisi de hücreleri okuyup aynı ızgarayı kurmak zorunda — kural burada
# tek kopya duruyor, yoksa yüklenen form ile gömülü form farklı basılırdı.

def _katilir(onceki_stil, stil, metin, rs, cs) -> bool:
    """Bu boş hücre soldaki hücreye katılabilir mi?

    Excel'de bir hücrenin yazısı, yanındaki hücre boşsa ve aralarında dikey
    çizgi yoksa oraya taşar; kâğıtta `Dosya No : ......` tek bir açık alan gibi
    görünür, aslında altı ayrı hücredir. HTML tablosunda taşma yok, yazı
    kırpılır — o yüzden aralarında çizgi olmayan boş hücreler soldakine
    katılıyor (colspan). Üst/alt çizgileri farklıysa katılmıyor: birleştirmek
    kâğıttaki çizgiyi bozardı.
    """
    if metin.strip() or rs != 1 or cs != 1:
        return False
    if onceki_stil is None:
        return False
    ok, yk = onceki_stil[5], stil[5]
    return (ok[3] == 0 and yk[2] == 0          # aralarında dikey çizgi yok
            and ok[0] == yk[0] and ok[1] == yk[1])   # üst/alt aynı


def izgara_kur(ncol: int, nsatir: int, birlesmeler, oku):
    """Hücrelerden kalıbın ızgarasını kurar.

    `birlesmeler`  [(r1, r2, c1, c2)] -- üst sınır dışta (Excel'in kendi kuralı)
    `oku(r, c)`    -> (metin, stil) ; stil altı parçalı bir demet:
                      (punto, kalın, yatay, dikey, sar, (üst, alt, sol, sağ))

    Döner: (stiller, satirlar, son_satir). `satirlar` her satır için
    [sütun, satır yayılımı, sütun yayılımı, metin, stil no] listesi; stil no
    None ise yalnızca yer tutan boş hücre (Excel'e hiç yazılmıyor).
    """
    kapali, yayilim = {}, {}
    for (r1, r2, c1, c2) in birlesmeler:
        yayilim[(r1, c1)] = (r2 - r1, c2 - c1)
        for r in range(r1, r2):
            for c in range(c1, c2):
                if (r, c) != (r1, c1):
                    kapali[(r, c)] = True

    def dolu_mu(metin, stil):
        return bool(metin.strip()) or any(stil[5])

    son = 0
    for r in range(nsatir):
        for c in range(ncol):
            if (r, c) in kapali:
                continue
            if dolu_mu(*oku(r, c)):
                son = r
    for (r1, r2, c1, c2) in birlesmeler:
        son = max(son, r2 - 1)

    stiller, stil_no = [], {}

    def no(stil):
        if stil not in stil_no:
            stil_no[stil] = len(stiller)
            stiller.append({"pt": stil[0], "kalin": stil[1], "yatay": stil[2],
                            "dikey": stil[3], "sar": stil[4],
                            "kenar": list(stil[5])})
        return stil_no[stil]

    satirlar = []
    for r in range(son + 1):
        hucreler, satir_stilleri, bos = [], [], 0
        for c in range(ncol):
            if (r, c) in kapali:
                continue
            rs, cs = yayilim.get((r, c), (1, 1))
            metin, stil = oku(r, c)
            if rs > 1 or cs > 1:
                # Birleşmiş kutunun sağ/alt kenarı ANCHOR'da değil, kutunun
                # en sağ/en alt hücresinin KENDİ kenarlığında duruyor --
                # Excel birleşmiş hücrelerde bile her hücrenin kendi
                # kenarlığını tutuyor, birleştirme onu devretmiyor. `kapali`
                # bu hücreleri atladığı için bilgi hiç okunmuyordu (v6.77'de
                # kullanıcının Excel çıktısıyla bulundu: kutuların sağ
                # tarafı kesikti). Aynı fikir aşağıdaki colspan-katılma
                # dalında zaten vardı (bkz. `_katilir`), gerçek birleşmeler
                # için de uygulanıyor.
                _, sag_stil = oku(r, c + cs - 1)
                _, alt_stil = oku(r + rs - 1, c)
                ust, alt, sol, sag = stil[5]
                stil = stil[:5] + ((ust, alt_stil[5][1], sol, sag_stil[5][3]),)

            onceki = hucreler[-1] if hucreler and not bos else None
            onc_stil = satir_stilleri[-1] if onceki else None
            if (onceki and onceki[1] == 1
                    and _katilir(onc_stil, stil, metin, rs, cs)):
                onceki[2] += 1                        # colspan
                k = onc_stil[5]
                yeni = onc_stil[:5] + ((k[0], k[1], k[2], stil[5][3]),)
                satir_stilleri[-1] = yeni
                onceki[4] = no(yeni)
                continue

            if not dolu_mu(metin, stil) and rs == 1 and cs == 1:
                bos += 1
                continue
            if bos:
                hucreler.append([c - bos, 1, bos, "", None])
                satir_stilleri.append(None)
                bos = 0
            hucreler.append([c, rs, cs, metin, no(stil)])
            satir_stilleri.append(stil)
        satirlar.append(hucreler)      # kuyruktaki boş hücreler atılıyor

    return stiller, satirlar, son


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


def satirlar(kaynak, deger=None, ek=None, alan=None) -> dict:
    """Şablonun bastığı ızgara: sütun genişlikleri + satır satır hücreler.

    Ölçek: kâğıdın kendi punto ve satır yükseklikleri A4'e sığmıyor (Excel
    "sayfaya sığdır" ile basıyor). Aynısını tarayıcıda yapmak için bütün
    yükseklikler ve puntolar tek bir katsayıyla küçültülüyor — oranlar
    bozulmadığı için form aynı görünüyor.
    """
    k = _kalip_al(kaynak)
    deger, ek, alan = deger or {}, ek or {}, alan or {}

    toplam = sum(h or 15.0 for h in k["satir_yuksekligi"])
    sayfa_yon, hedef = _sayfa_olcusu(kaynak)
    olcek = min(1.0, hedef / toplam) if toplam else 1.0

    gen_toplam = sum(k["sutun"]) or 1
    sutunlar = [round(100.0 * g / gen_toplam, 4) for g in k["sutun"]]

    cikti = []
    for r, satir in enumerate(k["satirlar"]):
        hucreler = []
        for c, rs, cs, metin, stil_no in satir:
            stil = k["stiller"][stil_no] if stil_no is not None else None
            hucreler.append({
                "metin": etiketleri_doldur(
                    _yazi(metin, deger.get((r, c)), ek.get((r, c))), alan),
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
            # Gömülü formun amblemi `static/` altında; yüklenen formunki
            # kalıbın içinde base64 -- veritabanıyla birlikte taşınsın diye.
            "kaynak": (f"data:{g['tur']};base64,{g['veri']}" if g.get("veri")
                       else "/static/" + g["dosya"]),
            "sol": round(100.0 * sol / gen_toplam, 4),
            "genislik": round(100.0 * gen / gen_toplam, 4),
            "ust": round(ust * olcek, 2),
            "yukseklik": round(yuk * olcek, 2),
        })

    return {"sutunlar": sutunlar, "satirlar": cikti, "gorseller": gorseller,
            "olcek": round(olcek, 4), "yon": sayfa_yon}


def yerlesim(kaynak, sayfa_adi: str, deger=None, ek=None, alan=None) -> dict:
    """Aynı kalıbı `excel.kitap()`'ın yerleşim sayfası olarak kurar."""
    k = _kalip_al(kaynak)
    deger, ek, alan = deger or {}, ek or {}, alan or {}

    hucreler, birlesik = {}, []
    for r, satir in enumerate(k["satirlar"]):
        for c, rs, cs, metin, stil_no in satir:
            if stil_no is None:            # yalnızca yer tutan boş hücre
                continue
            adres = _adres(r, c)
            hucreler[adres] = (
                etiketleri_doldur(
                    _yazi(metin, deger.get((r, c)), ek.get((r, c))), alan),
                stil_no)
            if rs > 1 or cs > 1:
                birlesik.append(f"{adres}:{_adres(r + rs - 1, c + cs - 1)}")
                # Excel kenarlığı HÜCRE bazında çiziyor, birleştirme onu
                # devretmiyor -- yalnızca sol üstteki (anchor) hücreye stil
                # verilince kutunun sağ ve alt kenarı hiç çizilmiyordu
                # (v6.77'de kullanıcının ekran görüntüsüyle bulundu: "hücreler
                # sağ tarafları kesik"). Kapladığı hücrelerin hepsine aynı
                # stili ver -- metin boş kalsın, anchor zaten yazıyı taşıyor.
                # İç kenarlar merge içinde görünmez, tekrar çizilmeleri zararsız.
                for rr in range(r, r + rs):
                    for cc in range(c, c + cs):
                        if rr == r and cc == c:
                            continue
                        hucreler[_adres(rr, cc)] = ("", stil_no)

    gorseller = []
    for g in k.get("gorseller", []):
        s1, dx1, r1, dy1, s2, dx2, r2, dy2 = g["sabit"]
        gorseller.append({
            "dosya": g["dosya"],
            "tur": g.get("tur"),
            "veri": g.get("veri"),
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
        "yazdirma": {"yon": yon(kaynak), "sigdir": True, "kenar": 0.3},
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
