"""Yüklenen bir `.xlsx` dosyasından form kalıbı çıkarır — kütüphanesiz.

Neden `.xlsx` ve `.xls` değil: `.xls` (eski Excel) ikili bir belge biçimi,
okumak için `xlrd` gerekiyor ve bu programın kuralı **ek bağımlılık yok**
(klinikteki Windows mini PC'ye kurulum eklemek demek). `.xlsx` ise içinde XML
olan bir ZIP; Python'un kendi `zipfile` ve `xml.etree` modülleri yetiyor.
Laboratuvar formunu Excel'de bir kez "Farklı Kaydet → Excel Çalışma Kitabı
(.xlsx)" ile kaydediyor, gerisi programın işi.

Çıkardığı kalıp `form_kalip.json`'daki ile **aynı biçimde**: satır
yükseklikleri, sütun genişlikleri, birleşik hücreler, her hücrenin
punto/kalınlık/hiza/kenarlık bilgisi, basılı yazılar ve varsa sayfadaki
görseller. Böylece yüklenen form da gömülü iki form da tek yoldan basılıyor.

**Dışarıdan gelen dosya.** Yönetici yüklüyor ama yine de sınırlar var: dosya
boyu, ZIP'teki parça sayısı, açılmış boyut, satır/sütun sayısı ve görsel boyu.
XML'de `<!DOCTYPE`/`<!ENTITY` varsa dosya hiç açılmıyor — "milyar kahkaha"
saldırısı belleği tüketebilir (bkz. Python'un XML güvenlik notları).
"""

import base64
import re
import zipfile
from io import BytesIO
from xml.etree import ElementTree as ET

import form_kalip

# Sınırlar. Bir laboratuvar formu birkaç yüz kilobayt; bunlar rahat ötesi.
EN_BUYUK_DOSYA = 5 * 1024 * 1024
EN_COK_PARCA = 200
EN_BUYUK_ACIK = 20 * 1024 * 1024
EN_COK_SATIR, EN_COK_SUTUN = 500, 200
EN_BUYUK_GORSEL = 2 * 1024 * 1024

_A = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_R = "{http://schemas.openxmlformats.org/package/2006/relationships}"
_RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
_REMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
_XDR = "{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}"
_AML = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# Excel'in çizgi adları -> kalıptaki numaralar (bkz. excel._CIZGI).
_CIZGI = {
    "thin": 1, "medium": 2, "dashed": 3, "dotted": 4, "thick": 5,
    "double": 6, "hair": 7, "mediumDashed": 3, "dashDot": 3,
    "mediumDashDot": 3, "dashDotDot": 4, "mediumDashDotDot": 4,
    "slantDashDot": 3,
}
_YATAY = {"left": 1, "center": 2, "right": 3, "centerContinuous": 2,
          "justify": 1, "distributed": 2}
_DIKEY = {"top": 0, "center": 1, "bottom": 2, "justify": 1, "distributed": 1}

# Excel'in ölçüleri: EMU (puntoda 12700, pikselde 9525); sütun genişliği
# karakter cinsinden, karakter ~7 piksel. Kalıp sütunu 1/256 karakter tutuyor.
_EMU_PUNTO, _EMU_PIKSEL = 12700.0, 9525.0
_KARAKTER_PIKSEL = 7.0
_VARSAYILAN_SUTUN = 8.43
_VARSAYILAN_SATIR = 15.0

_ADRES = re.compile(r"^([A-Z]+)([0-9]+)$")


class Hata(Exception):
    """Dosya okunamadı; mesajı kullanıcıya gösterilecek kadar açık."""


def _sutun_no(harf: str) -> int:
    n = 0
    for k in harf:
        n = n * 26 + (ord(k) - 64)
    return n - 1


def _adres_coz(adres):
    e = _ADRES.match((adres or "").strip().upper())
    if not e:
        return None
    return int(e.group(2)) - 1, _sutun_no(e.group(1))


def _sayi(deger, varsayilan=0.0):
    try:
        return float(deger)
    except (TypeError, ValueError):
        return varsayilan


def _xml(z, ad):
    """ZIP'ten bir XML parçasını güvenle çözer. Yoksa None."""
    try:
        ham = z.read(ad)
    except KeyError:
        return None
    if b"<!DOCTYPE" in ham or b"<!ENTITY" in ham:
        raise Hata("dosyada XML varlık tanımı var")
    try:
        return ET.fromstring(ham)
    except ET.ParseError as e:
        raise Hata(f"XML çözülemedi ({ad}): {e}") from None


def _iliskiler(z, parca_yolu):
    """Bir parçanın .rels dosyası: {rId: hedef yol}."""
    p = parca_yolu.rsplit("/", 1)
    kok = p[0] if len(p) == 2 else ""
    ad = p[-1]
    rels = _xml(z, f"{kok}/_rels/{ad}.rels" if kok else f"_rels/{ad}.rels")
    if rels is None:
        return {}, kok
    return ({r.get("Id"): r.get("Target") for r in rels.findall(f"{_R}Relationship")},
            kok)


def _birlestir(kok, hedef):
    """Göreli hedefi ("../media/x.png") parça yoluna göre çözer."""
    if hedef.startswith("/"):
        return hedef.lstrip("/")
    parcalar = [p for p in kok.split("/") if p]
    for p in hedef.split("/"):
        if p == "..":
            if parcalar:
                parcalar.pop()
        elif p not in ("", "."):
            parcalar.append(p)
    return "/".join(parcalar)


# ------------------------------------------------------------------ stiller

def _stiller(z):
    """cellXfs sırasına göre [(punto, kalın, yatay, dikey, sar, kenar)]."""
    kok = _xml(z, "xl/styles.xml")
    if kok is None:
        return []

    fontlar = []
    for f in kok.findall(f"{_A}fonts/{_A}font"):
        sz = f.find(f"{_A}sz")
        fontlar.append((_sayi(sz.get("val") if sz is not None else None, 11.0),
                        1 if f.find(f"{_A}b") is not None else 0))

    kenarlar = []
    for b in kok.findall(f"{_A}borders/{_A}border"):
        yan = []
        for ad in ("top", "bottom", "left", "right"):
            e = b.find(f"{_A}{ad}")
            yan.append(_CIZGI.get(e.get("style") if e is not None else None, 0))
        kenarlar.append(tuple(yan))

    cikti = []
    for xf in kok.findall(f"{_A}cellXfs/{_A}xf"):
        fi = int(_sayi(xf.get("fontId"), 0))
        bi = int(_sayi(xf.get("borderId"), 0))
        punto, kalin = fontlar[fi] if fi < len(fontlar) else (11.0, 0)
        kenar = kenarlar[bi] if bi < len(kenarlar) else (0, 0, 0, 0)
        hiz = xf.find(f"{_A}alignment")
        yatay = _YATAY.get(hiz.get("horizontal") if hiz is not None else None, 0)
        # Excel'in varsayılanı **alt**; kalıpta 2 o demek.
        dikey = _DIKEY.get(hiz.get("vertical") if hiz is not None else None, 2)
        sar = 1 if (hiz is not None and hiz.get("wrapText") in ("1", "true")) else 0
        cikti.append((int(round(punto)), kalin, yatay, dikey, sar, kenar))
    return cikti


def _paylasilan(z):
    kok = _xml(z, "xl/sharedStrings.xml")
    if kok is None:
        return []
    out = []
    for si in kok.findall(f"{_A}si"):
        out.append("".join(t.text or "" for t in si.iter(f"{_A}t")))
    return out


# ------------------------------------------------------------------ görseller

def _gorseller(z, sayfa_yolu, sutun_genislik, satir_yukseklik):
    """Sayfadaki resimleri kalıbın sabitleyici biçimine çevirir."""
    rels, _ = _iliskiler(z, sayfa_yolu)
    cizim_yolu = None
    for rid, hedef in rels.items():
        if "drawings/" in hedef:
            cizim_yolu = _birlestir(sayfa_yolu.rsplit("/", 1)[0], hedef)
    if not cizim_yolu:
        return []
    cizim = _xml(z, cizim_yolu)
    if cizim is None:
        return []
    crels, _ = _iliskiler(z, cizim_yolu)

    def sutun_px(c):
        gen = sutun_genislik(c)
        return max(1.0, gen * _KARAKTER_PIKSEL)

    def satir_pt(r):
        return max(1.0, satir_yukseklik(r))

    def kesirler(e, etiket):
        c = int(_sayi(e.findtext(f"{_XDR}col"), 0))
        r = int(_sayi(e.findtext(f"{_XDR}row"), 0))
        cx = _sayi(e.findtext(f"{_XDR}colOff"), 0) / _EMU_PIKSEL
        ry = _sayi(e.findtext(f"{_XDR}rowOff"), 0) / _EMU_PUNTO
        return (c, int(round(cx / sutun_px(c) * 1024)),
                r, int(round(ry / satir_pt(r) * 256)))

    def genislikten(c0, kesir0, emu_genislik):
        """oneCellAnchor: başlangıç + genişlikten bitiş hücresini bulur."""
        kalan = emu_genislik / _EMU_PIKSEL
        kalan += kesir0 / 1024.0 * sutun_px(c0)
        c = c0
        while kalan > sutun_px(c) and c < EN_COK_SUTUN:
            kalan -= sutun_px(c)
            c += 1
        return c, int(round(kalan / sutun_px(c) * 1024))

    def yukseklikten(r0, kesir0, emu_yukseklik):
        kalan = emu_yukseklik / _EMU_PUNTO
        kalan += kesir0 / 256.0 * satir_pt(r0)
        r = r0
        while kalan > satir_pt(r) and r < EN_COK_SATIR:
            kalan -= satir_pt(r)
            r += 1
        return r, int(round(kalan / satir_pt(r) * 256))

    cikti = []
    for sabitleyici in list(cizim.findall(f"{_XDR}twoCellAnchor")) + \
            list(cizim.findall(f"{_XDR}oneCellAnchor")):
        blip = sabitleyici.find(f".//{_AML}blip")
        if blip is None:
            continue
        hedef = crels.get(blip.get(_REMBED))
        if not hedef:
            continue
        yol = _birlestir(cizim_yolu.rsplit("/", 1)[0], hedef)
        try:
            veri = z.read(yol)
        except KeyError:
            continue
        if len(veri) > EN_BUYUK_GORSEL:
            continue
        tur = _gorsel_turu(veri)
        if not tur:
            continue

        bas = sabitleyici.find(f"{_XDR}from")
        if bas is None:
            continue
        bc, bdx, br, bdy = kesirler(bas, "from")
        bit = sabitleyici.find(f"{_XDR}to")
        if bit is not None:
            tc, tdx, tr, tdy = kesirler(bit, "to")
        else:
            ext = sabitleyici.find(f"{_XDR}ext")
            if ext is None:
                continue
            tc, tdx = genislikten(bc, bdx, _sayi(ext.get("cx"), 0))
            tr, tdy = yukseklikten(br, bdy, _sayi(ext.get("cy"), 0))

        cikti.append({
            "dosya": yol.rsplit("/", 1)[-1],
            "sabit": [bc, bdx, br, bdy, tc, tdx, tr, tdy],
            "tur": tur,
            "veri": base64.b64encode(veri).decode("ascii"),
        })
    return cikti


def _gorsel_turu(veri: bytes):
    """Baytlardan tür; tanımadığımız bir şeyse None (dosyaya konmuyor)."""
    if veri.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if veri.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if veri.startswith(b"GIF8"):
        return "image/gif"
    return None


# --------------------------------------------------------------------- kalıp

def kalip(baytlar: bytes) -> dict:
    """`.xlsx` baytlarından kalıp sözlüğü. Bozuksa `Hata` atar."""
    if not baytlar:
        raise Hata("dosya boş")
    if len(baytlar) > EN_BUYUK_DOSYA:
        raise Hata("dosya çok büyük")

    try:
        z = zipfile.ZipFile(BytesIO(baytlar))
    except zipfile.BadZipFile:
        raise Hata("bu bir .xlsx dosyası değil") from None

    with z:
        bilgiler = z.infolist()
        if len(bilgiler) > EN_COK_PARCA:
            raise Hata("dosyada çok fazla parça var")
        if sum(b.file_size for b in bilgiler) > EN_BUYUK_ACIK:
            raise Hata("dosya açıldığında çok büyük")

        kitap = _xml(z, "xl/workbook.xml")
        if kitap is None:
            raise Hata("bu bir .xlsx dosyası değil")
        sayfa = kitap.find(f"{_A}sheets/{_A}sheet")
        if sayfa is None:
            raise Hata("dosyada sayfa yok")
        rels, _ = _iliskiler(z, "xl/workbook.xml")
        hedef = rels.get(sayfa.get(_RID)) or "worksheets/sheet1.xml"
        sayfa_yolu = _birlestir("xl", hedef)

        kok = _xml(z, sayfa_yolu)
        if kok is None:
            raise Hata("sayfa okunamadı")

        return _sayfa_kalibi(z, kok, sayfa_yolu, _stiller(z), _paylasilan(z),
                             sayfa.get("name") or "Form")


def _hucre_metni(c, paylasilan):
    tip = c.get("t")
    if tip == "inlineStr":
        return "".join(t.text or "" for t in c.iter(f"{_A}t"))
    v = c.find(f"{_A}v")
    if v is None or v.text is None:
        return ""
    ham = v.text
    if tip == "s":
        try:
            return paylasilan[int(ham)]
        except (ValueError, IndexError):
            return ""
    if tip == "b":
        return "Evet" if ham == "1" else "Hayır"
    if tip in (None, "n"):
        # Sayı: tam sayıysa ondalık basma ("13.0" değil "13").
        try:
            f = float(ham)
        except ValueError:
            return ham
        return str(int(f)) if f == int(f) else str(f)
    return ham


def _sayfa_kalibi(z, kok, sayfa_yolu, stiller_tablosu, paylasilan, ad):
    bicim = kok.find(f"{_A}sheetFormatPr")
    vars_sutun = _sayi(bicim.get("defaultColWidth") if bicim is not None else None,
                       _VARSAYILAN_SUTUN) or _VARSAYILAN_SUTUN
    vars_satir = _sayi(bicim.get("defaultRowHeight") if bicim is not None else None,
                       _VARSAYILAN_SATIR) or _VARSAYILAN_SATIR

    genislikler = {}
    for col in kok.findall(f"{_A}cols/{_A}col"):
        gen = _sayi(col.get("width"), vars_sutun)
        for c in range(int(_sayi(col.get("min"), 1)) - 1,
                       min(int(_sayi(col.get("max"), 1)), EN_COK_SUTUN)):
            genislikler[c] = gen

    hucreler, yukseklikler = {}, {}
    en_sag, en_alt = -1, -1
    for row in kok.findall(f"{_A}sheetData/{_A}row"):
        r = int(_sayi(row.get("r"), 0)) - 1
        if r < 0 or r >= EN_COK_SATIR:
            continue
        if row.get("ht") is not None:
            yukseklikler[r] = round(_sayi(row.get("ht"), vars_satir), 1)
        for c in row.findall(f"{_A}c"):
            yer = _adres_coz(c.get("r"))
            if yer is None or yer[1] >= EN_COK_SUTUN:
                continue
            _, sutun = yer
            hucreler[(r, sutun)] = (_hucre_metni(c, paylasilan),
                                    int(_sayi(c.get("s"), 0)))
            en_sag, en_alt = max(en_sag, sutun), max(en_alt, r)

    birlesmeler = []
    for m in kok.findall(f"{_A}mergeCells/{_A}mergeCell"):
        aralik = (m.get("ref") or "").split(":")
        if len(aralik) != 2:
            continue
        bas, bit = _adres_coz(aralik[0]), _adres_coz(aralik[1])
        if not bas or not bit:
            continue
        if bit[0] >= EN_COK_SATIR or bit[1] >= EN_COK_SUTUN:
            continue
        birlesmeler.append((bas[0], bit[0] + 1, bas[1], bit[1] + 1))
        en_sag, en_alt = max(en_sag, bit[1]), max(en_alt, bit[0])

    ncol = max(en_sag + 1, max(genislikler, default=-1) + 1, 1)
    nsatir = en_alt + 1
    if nsatir < 1:
        raise Hata("sayfa boş")

    bos_stil = (11, 0, 0, 2, 0, (0, 0, 0, 0))

    def oku(r, c):
        metin, si = hucreler.get((r, c), ("", None))
        if si is None:
            return "", bos_stil
        stil = (stiller_tablosu[si] if si < len(stiller_tablosu) else bos_stil)
        return metin, stil

    stiller, satirlar, son = form_kalip.izgara_kur(ncol, nsatir, birlesmeler, oku)

    def sutun_gen(c):
        return genislikler.get(c, vars_sutun)

    def satir_yuk(r):
        return yukseklikler.get(r, vars_satir)

    yazdirma = kok.find(f"{_A}pageSetup")
    yon = "yatay" if (yazdirma is not None
                      and yazdirma.get("orientation") == "landscape") else "dikey"

    return {
        "ad": ad,
        "yon": yon,
        "sutun": [int(round(sutun_gen(c) * 256)) for c in range(ncol)],
        "satir_yuksekligi": [yukseklikler.get(r) for r in range(son + 1)],
        "stiller": stiller,
        "satirlar": satirlar,
        "gorseller": _gorseller(z, sayfa_yolu, sutun_gen, satir_yuk),
    }
