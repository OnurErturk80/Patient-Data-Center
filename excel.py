"""Excel (.xlsx) dosyası üretir — dışarıdan hiçbir kütüphane kurmadan.

Neden elle yazılıyor: `.xlsx` aslında içinde XML dosyaları olan bir ZIP.
Python'un kendi `zipfile` modülü ZIP'i, düz metin de XML'i yazabiliyor. Böylece
klinikteki Windows mini PC'ye `pip install openpyxl` yapmak gerekmiyor —
projenin "ek bağımlılık yok" kuralı bozulmuyor ve kullanıcının iki makinede
ayrı kurulum takip etmesi gerekmiyor.

Ürettiği dosya gerçek bir Excel dosyası: Türkçe karakterler bozulmuyor,
tarihler tarih olarak (sıralanabilir, süzülebilir), sayılar sayı olarak
giriyor. CSV'nin Türkçe Windows'taki ayraç ve kodlama tuzakları yok.

Kullanımı:

    import excel
    veri = excel.kitap([
        ("Hastalar", ["Dosya no", "Ad"], [[527078, "Ayşe Yılmaz"], ...]),
    ])

`veri` bayt dizisi; doğrudan HTTP yanıtı olarak verilebilir.

Hücrenin türü **değerden** anlaşılır:

  - `None`                      -> boş hücre
  - `int` / `float`             -> sayı
  - "2026-09-11"                -> tarih
  - "2026-09-11 08:15[:00]"     -> tarih + saat
  - başka her şey               -> metin

Yılı 1900'den küçük tarihler metin olarak yazılır. Bu bir incelik değil,
gerçek bir kayıt: veritabanında OPU tarihi `0026-09-04` olan bir cycle var
(bkz. CLAUDE.md bekleyen iş 6). Excel'in tarih sayacı 1900'den başlar, böyle
bir değeri tarihe çevirmek dosyayı bozardı.
"""

import datetime as _dt
import re
import zipfile
from io import BytesIO

# Excel'in tarih sayacı: 1 = 1 Ocak 1900. Başlangıcı 1899-12-30 almak
# Excel'in bilinen "1900 artık yıldır" hatasını da hesaba katar.
_SIFIR_GUN = _dt.date(1899, 12, 30)

_TARIH = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_ZAMAN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?$")

# Biçim numaraları styles.xml'deki cellXfs sırasıyla aynı.
_DUZ, _BASLIK, _TARIH_BICIM, _ZAMAN_BICIM = 0, 1, 2, 3

# Yerleşim sayfalarının (resmî formlar) stilleri. Adla çağrılıyor; sıra
# styles.xml'deki cellXfs sırası ve **değiştirilemez** -- araya stil ekleyecek
# olursan sona ekle, ortadan değil (sayılar dosyaya yazılıyor).
STILLER = {
    "duz": 0, "baslik": 1,
    "kurum": 4,      # kurum adı satırları: kalın, ortalı, kenarlıksız
    "formadi": 5,    # formun adı: büyük, kalın, ortalı
    "kunye": 6,      # doküman kodu / revizyon şeridi: küçük, kenarlıklı
    "etiket": 7,     # form alanının adı: kalın, açık dolgulu, kenarlıklı
    "deger": 8,      # programdan gelen değer: kenarlıklı, sola yaslı
    "bolum": 9,      # "OOSİT BİLGİLERİ" gibi bölüm başlığı
    "ortali": 10,    # ızgara hücresi: ortalı, kenarlıklı
    "dipnot": 11,    # form numarası / revizyon: küçük, kenarlıksız
    "ortali_kalin": 12,
}

# Excel sayfa adında kullanılamayan karakterler ve en fazla uzunluk.
_YASAK_AD = re.compile(r"[\[\]:*?/\\]")
_AD_UZUNLUK = 31

# Sütun genişliği: içeriğe göre, ama iki uçta sınırlı. Dar olursa "#####",
# geniş olursa tablo ekrana sığmıyor.
_EN_DAR, _EN_GENIS = 8, 42


def _kacis(m: str) -> str:
    """XML'e yazılabilir hale getirir.

    Kaçış dışında **denetim karakterlerini de atar**: veritabanındaki serbest
    metin alanlarına (notlar, işlemi yapan) yapıştırma yoluyla girmiş olabilir
    ve Excel böyle bir karakter gördüğünde dosyayı "bozuk" sayıp hiç açmaz.
    """
    m = "".join(k for k in m if k in "\t\n\r" or ord(k) >= 32)
    return (m.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _sutun_adi(n: int) -> str:
    """1 -> A, 26 -> Z, 27 -> AA."""
    ad = ""
    while n > 0:
        n, kalan = divmod(n - 1, 26)
        ad = chr(65 + kalan) + ad
    return ad


def _seri(y, ay, g, sa=0, dk=0, sn=0):
    """Tarihi Excel'in gün sayacına çevirir; çevrilemiyorsa None."""
    try:
        gun = (_dt.date(y, ay, g) - _SIFIR_GUN).days
    except ValueError:                      # 31 Şubat gibi bozuk bir değer
        return None
    if gun <= 0:                            # 1900 öncesi -- Excel sayamaz
        return None
    return gun + (sa * 3600 + dk * 60 + sn) / 86400.0


def _hucre(adres: str, deger, bicim=_DUZ) -> str:
    if deger is None or deger == "":
        return f'<c r="{adres}" s="{bicim}"/>' if bicim else ""

    if isinstance(deger, bool):             # bool int'in alt türü, önce baksın
        deger = "Evet" if deger else "Hayır"

    elif isinstance(deger, (int, float)):
        return f'<c r="{adres}" s="{bicim}"><v>{deger}</v></c>'

    elif isinstance(deger, _dt.datetime):
        s = _seri(deger.year, deger.month, deger.day,
                  deger.hour, deger.minute, deger.second)
        if s is not None:
            return f'<c r="{adres}" s="{_ZAMAN_BICIM}"><v>{s}</v></c>'
        deger = deger.isoformat(" ", "seconds")

    elif isinstance(deger, _dt.date):
        s = _seri(deger.year, deger.month, deger.day)
        if s is not None:
            return f'<c r="{adres}" s="{_TARIH_BICIM}"><v>{s}</v></c>'
        deger = deger.isoformat()

    elif isinstance(deger, str) and bicim == _DUZ:
        e = _ZAMAN.match(deger)
        if e:
            p = [int(x) for x in e.groups(default="0")]
            s = _seri(*p)
            if s is not None:
                return f'<c r="{adres}" s="{_ZAMAN_BICIM}"><v>{s}</v></c>'
        else:
            e = _TARIH.match(deger)
            if e:
                s = _seri(*(int(x) for x in e.groups()))
                if s is not None:
                    return f'<c r="{adres}" s="{_TARIH_BICIM}"><v>{s}</v></c>'

    m = _kacis(str(deger))
    return (f'<c r="{adres}" s="{bicim}" t="inlineStr">'
            f'<is><t xml:space="preserve">{m}</t></is></c>')


def _genislikler(basliklar, satirlar):
    """Sütun genişlikleri: başlık ve ilk 200 satırın en uzun değerine göre."""
    olcu = [len(str(b)) for b in basliklar]
    for satir in satirlar[:200]:
        for i, d in enumerate(satir[:len(olcu)]):
            if d is not None:
                olcu[i] = max(olcu[i], len(str(d)))
    return [min(_EN_GENIS, max(_EN_DAR, u + 2)) for u in olcu]


def _sayfa_xml(basliklar, satirlar) -> str:
    en_son = _sutun_adi(len(basliklar))
    p = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
         '<worksheet xmlns="http://schemas.openxmlformats.org/'
         'spreadsheetml/2006/main">',
         # Başlık satırı kaydırırken ekranda kalsın: 40 oositlik bir tabloda
         # hangi sütunda olduğunu görmenin tek yolu bu.
         '<sheetViews><sheetView workbookViewId="0">'
         '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" '
         'state="frozen"/></sheetView></sheetViews>',
         '<cols>']
    for i, g in enumerate(_genislikler(basliklar, satirlar), start=1):
        p.append(f'<col min="{i}" max="{i}" width="{g}" customWidth="1"/>')
    p.append("</cols><sheetData>")

    p.append('<row r="1">')
    for i, b in enumerate(basliklar, start=1):
        p.append(_hucre(f"{_sutun_adi(i)}1", b, _BASLIK))
    p.append("</row>")

    for n, satir in enumerate(satirlar, start=2):
        p.append(f'<row r="{n}">')
        for i, d in enumerate(satir[:len(basliklar)], start=1):
            p.append(_hucre(f"{_sutun_adi(i)}{n}", d))
        p.append("</row>")

    p.append("</sheetData>")
    # Süzgeç okları: kullanıcı tabloyu Excel'de ayıklayabilsin diye.
    p.append(f'<autoFilter ref="A1:{en_son}{max(1, len(satirlar) + 1)}"/>')
    p.append("</worksheet>")
    return "".join(p)


# --------------------------------------------------------------- yerleşim

_ADRES = re.compile(r"^([A-Z]+)(\d+)$")


def _adres_coz(adres: str):
    """"C8" -> (3, 8). Sütun harfi 1'den başlayan sayıya çevrilir."""
    e = _ADRES.match(adres.strip().upper())
    if not e:
        raise ValueError(f"gecersiz hucre adresi: {adres}")
    harf, satir = e.groups()
    n = 0
    for k in harf:
        n = n * 26 + (ord(k) - 64)
    return n, int(satir)


def _yerlesim_xml(y: dict, taban: int = 0) -> str:
    """Serbest yerleşimli sayfa: resmî formların birebir kopyası.

    Tablo sayfasından farkı, hücrelerin **adresle** verilmesi: form kâğıdı
    satır-sütun düzeni değil, belirli kutulara yazılan bir kalıp. Birleşik
    hücre, kenarlık, sütun genişliği ve yazdırma ayarı da buradan geliyor —
    çıktının A4'e formun aslı gibi oturması için hepsi gerekli.

    Beklenen sözlük:
      ad           sayfa adı
      hucreler     {"A1": değer} ya da {"A1": (değer, "stil")}
      birlesik     ["A1:I1", ...]
      genislikler  {sütun no: karakter genişliği}
      yukseklikler {satır no: punto}
      stiller      [{"pt":..,"kalin":..,"kenar":(..)}, ...] -- kalıp stilleri
      yazdirma     {"yon": "dikey"|"yatay", "sigdir": True, "kenar": 0.3}

    Hücrenin stili ya bir ad (`STILLER` sözlüğü) ya da `stiller` listesindeki
    sıra numarasıdır. Sıra numarası `taban` ile kaydırılıyor, çünkü aynı
    dosyadaki her kalıp kendi stillerini styles.xml'in sonuna ekliyor.
    """
    hucreler, birlesik = y.get("hucreler", {}), y.get("birlesik", [])
    yaz = y.get("yazdirma", {})

    # Hücreler satır satır gruplanıyor: sheetData satır sırasına göre yazılır.
    satirlar = {}
    for adres, deger in hucreler.items():
        sutun, satir = _adres_coz(adres)
        satirlar.setdefault(satir, []).append((sutun, adres.upper(), deger))

    p = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
         '<worksheet xmlns="http://schemas.openxmlformats.org/'
         'spreadsheetml/2006/main">']
    if yaz.get("sigdir", True):
        # Tek sayfaya sığdır: form bir sayfa, ikinciye taşarsa dosyaya konmaz.
        p.append('<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>')
    p.append('<sheetViews><sheetView workbookViewId="0" '
             'showGridLines="0"/></sheetViews>')
    p.append('<sheetFormatPr defaultRowHeight="15"/>')

    g = y.get("genislikler", {})
    if g:
        p.append("<cols>")
        for sutun in sorted(g):
            p.append(f'<col min="{sutun}" max="{sutun}" width="{g[sutun]}" '
                     'customWidth="1"/>')
        p.append("</cols>")

    yuk = y.get("yukseklikler", {})
    p.append("<sheetData>")
    for satir in sorted(satirlar):
        h = (f' ht="{yuk[satir]}" customHeight="1"' if satir in yuk else "")
        p.append(f'<row r="{satir}"{h}>')
        for _, adres, deger in sorted(satirlar[satir]):
            if isinstance(deger, tuple):
                deger, stil = deger
            else:
                stil = "duz"
            bicim = (taban + stil if isinstance(stil, int)
                     else STILLER.get(stil, _DUZ))
            p.append(_hucre(adres, deger, bicim))
        p.append("</row>")
    p.append("</sheetData>")

    if birlesik:
        p.append(f'<mergeCells count="{len(birlesik)}">')
        for aralik in birlesik:
            p.append(f'<mergeCell ref="{aralik.upper()}"/>')
        p.append("</mergeCells>")

    kenar = yaz.get("kenar", 0.3)
    p.append(f'<pageMargins left="{kenar}" right="{kenar}" top="{kenar}" '
             f'bottom="{kenar}" header="0" footer="0"/>')
    yon = "landscape" if yaz.get("yon") == "yatay" else "portrait"
    sig = ' fitToWidth="1" fitToHeight="1"' if yaz.get("sigdir", True) else ""
    # paperSize 9 = A4.
    p.append(f'<pageSetup paperSize="9" orientation="{yon}"{sig}/>')
    p.append("</worksheet>")
    return "".join(p)


def _sayfa_adi_of(sayfa):
    """Sayfa hem demet hem sözlük olabilir; adı ikisinden de okur."""
    return sayfa.get("ad", "") if isinstance(sayfa, dict) else sayfa[0]


def _sayfa_adlari(sayfalar):
    """Excel'in sayfa adı kuralları: 31 karakter, bazı işaretler yasak, tekrar yok."""
    adlar, kullanilan = [], set()
    for i, sayfa in enumerate(sayfalar, start=1):
        ad = _sayfa_adi_of(sayfa)
        temiz = _YASAK_AD.sub(" ", str(ad)).strip()[:_AD_UZUNLUK] or f"Sayfa{i}"
        kok, n = temiz, 2
        while temiz.lower() in kullanilan:
            ek = f" {n}"
            temiz = kok[:_AD_UZUNLUK - len(ek)] + ek
            n += 1
        kullanilan.add(temiz.lower())
        adlar.append(temiz)
    return adlar


# styles.xml parça parça kuruluyor: tablo sayfalarının stilleri sabit, form
# kalıplarınınki **dosyaya özel** (kâğıt aslındaki punto ve kenarlıklar
# formdan forma değişiyor). Taban listelerin sırası dosyaya sayı olarak
# yazılıyor -- araya ekleme, sona ekle.

_NUMFMT = ('<numFmts count="2">'
           '<numFmt numFmtId="164" formatCode="yyyy\\-mm\\-dd"/>'
           '<numFmt numFmtId="165" formatCode="yyyy\\-mm\\-dd\\ hh:mm"/>'
           "</numFmts>")

# 0-1 tablo yazıları, 2-7 form yazıları (punto ve kalınlık).
_TABAN_FONT = [
    '<font><sz val="11"/><name val="Calibri"/></font>',
    '<font><b/><sz val="11"/><name val="Calibri"/></font>',
    '<font><b/><sz val="12"/><name val="Calibri"/></font>',
    '<font><b/><sz val="14"/><name val="Calibri"/></font>',
    '<font><sz val="8"/><name val="Calibri"/></font>',
    '<font><b/><sz val="9"/><name val="Calibri"/></font>',
    '<font><sz val="10"/><name val="Calibri"/></font>',
    '<font><b/><sz val="10"/><name val="Calibri"/></font>',
]

# İlk iki dolgu Excel'in şartı: sırayla "none" ve "gray125" olmak zorunda.
_FILL = ('<fills count="5">'
         '<fill><patternFill patternType="none"/></fill>'
         '<fill><patternFill patternType="gray125"/></fill>'
         '<fill><patternFill patternType="solid">'
         '<fgColor rgb="FFE8EDF0"/><bgColor indexed="64"/></patternFill></fill>'
         '<fill><patternFill patternType="solid">'
         '<fgColor rgb="FFF2F2F2"/><bgColor indexed="64"/></patternFill></fill>'
         '<fill><patternFill patternType="solid">'
         '<fgColor rgb="FFD9D9D9"/><bgColor indexed="64"/></patternFill></fill>'
         "</fills>")

# 0: kenarlıksız, 1: dört yanı ince çizgi (form kutuları).
_TABAN_KENAR = [
    "<border><left/><right/><top/><bottom/><diagonal/></border>",
    '<border><left style="thin"><color indexed="64"/></left>'
    '<right style="thin"><color indexed="64"/></right>'
    '<top style="thin"><color indexed="64"/></top>'
    '<bottom style="thin"><color indexed="64"/></bottom>'
    "<diagonal/></border>",
]

_TABAN_XF = [
    # 0-3: tablo sayfaları (düz, başlık, tarih, tarih+saat)
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>',
    '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" '
    'applyFont="1" applyFill="1"/>',
    '<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" '
    'applyNumberFormat="1"/>',
    '<xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" '
    'applyNumberFormat="1"/>',
    # 4-12: eski form stilleri (adla çağrılıyor, bkz. STILLER)
    '<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" '
    'applyFont="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center"/></xf>',
    '<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" '
    'applyFont="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center"/></xf>',
    '<xf numFmtId="0" fontId="4" fillId="0" borderId="1" xfId="0" '
    'applyFont="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center" wrapText="1"/></xf>',
    '<xf numFmtId="0" fontId="5" fillId="3" borderId="1" xfId="0" '
    'applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="left" vertical="center" wrapText="1"/></xf>',
    '<xf numFmtId="0" fontId="6" fillId="0" borderId="1" xfId="0" '
    'applyFont="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="left" vertical="center" wrapText="1"/></xf>',
    '<xf numFmtId="0" fontId="7" fillId="4" borderId="1" xfId="0" '
    'applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center"/></xf>',
    '<xf numFmtId="0" fontId="4" fillId="0" borderId="1" xfId="0" '
    'applyFont="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center" wrapText="1"/></xf>',
    '<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" '
    'applyFont="1" applyAlignment="1">'
    '<alignment horizontal="left" vertical="center"/></xf>',
    '<xf numFmtId="0" fontId="5" fillId="0" borderId="1" xfId="0" '
    'applyFont="1" applyBorder="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center" wrapText="1"/></xf>',
]

# Kalıp stilleri kâğıt aslından geliyor; sayılar orada ne ise o.
_CIZGI = {1: "thin", 2: "medium", 3: "dashed", 4: "dotted", 5: "thick",
          6: "double", 7: "hair"}
_YATAY = {1: "left", 2: "center", 3: "right"}
_DIKEY = {0: "top", 1: "center", 2: "bottom"}


def _kenar_xml(kenar) -> str:
    """(üst, alt, sol, sağ) çizgi numaralarından border parçası."""
    ust, alt, sol, sag = kenar

    def yan(ad, n):
        if not n:
            return f"<{ad}/>"
        return (f'<{ad} style="{_CIZGI.get(n, "thin")}">'
                f'<color indexed="64"/></{ad}>')

    return ("<border>" + yan("left", sol) + yan("right", sag) +
            yan("top", ust) + yan("bottom", alt) + "<diagonal/></border>")


def _kalip_xf(stil: dict, fontlar: list, kenarlar: list) -> str:
    """Kalıptan gelen bir stili cellXfs satırına çevirir.

    Gereken font ve kenarlık listede yoksa sona ekleniyor; aynısı ikinci kez
    istendiğinde var olan kullanılıyor.
    """
    punto = stil.get("pt", 10)
    kalin = "<b/>" if stil.get("kalin") else ""
    font = f'<font>{kalin}<sz val="{punto}"/><name val="Arial"/></font>'
    if font not in fontlar:
        fontlar.append(font)
    fid = fontlar.index(font)

    kenar = _kenar_xml(stil.get("kenar", (0, 0, 0, 0)))
    if kenar not in kenarlar:
        kenarlar.append(kenar)
    kid = kenarlar.index(kenar)

    hiza = []
    y = _YATAY.get(stil.get("yatay", 0))
    if y:
        hiza.append(f'horizontal="{y}"')
    hiza.append('vertical="%s"' % _DIKEY.get(stil.get("dikey", 1), "center"))
    if stil.get("sar"):
        hiza.append('wrapText="1"')
    return (f'<xf numFmtId="0" fontId="{fid}" fillId="0" borderId="{kid}" '
            'xfId="0" applyFont="1" applyBorder="1" applyAlignment="1">'
            f'<alignment {" ".join(hiza)}/></xf>')


def _stil_xml(fontlar, kenarlar, xfler) -> str:
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/'
            'spreadsheetml/2006/main">' + _NUMFMT +
            f'<fonts count="{len(fontlar)}">' + "".join(fontlar) + "</fonts>" +
            _FILL +
            f'<borders count="{len(kenarlar)}">' + "".join(kenarlar) +
            "</borders>"
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" '
            'borderId="0"/></cellStyleXfs>'
            f'<cellXfs count="{len(xfler)}">' + "".join(xfler) + "</cellXfs>"
            # Adlandırılmış "Normal" stili: Excel onsuz da açıyor ama bazı
            # okuyucular (openpyxl) "varsayılan stil yok" diye uyarıyor.
            '<cellStyles count="1">'
            '<cellStyle name="Normal" xfId="0" builtinId="0"/>'
            "</cellStyles></styleSheet>")


_KOK_REL = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
    'relationships"><Relationship Id="rId1" Type="http://schemas.'
    'openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="xl/workbook.xml"/></Relationships>'
)


def kitap(sayfalar) -> bytes:
    """Sayfalardan bir .xlsx dosyası üretir ve baytlarını döndürür.

    Sayfa iki biçimde verilebilir:

      - **Tablo**: `(ad, [başlık, ...], [[hücre, ...], ...])` — başlık satırı,
        donmuş bölme, süzgeç, içeriğe göre sütun genişliği.
      - **Yerleşim**: `{"ad":..., "hucreler": {...}, "birlesik": [...], ...}`
        — resmî formların birebir kopyası; bkz. `_yerlesim_xml`.

    En az bir sayfa olmalı; boş sayfa (yalnızca başlık satırı) geçerlidir.
    """
    if not sayfalar:
        sayfalar = [("Boş", ["Kayıt yok"], [])]
    adlar = _sayfa_adlari(sayfalar)
    n = len(sayfalar)

    # Kalıp stilleri styles.xml'in sonuna ekleniyor; her sayfa kendi
    # başlangıç numarasını (taban) öğreniyor.
    fontlar, kenarlar = list(_TABAN_FONT), list(_TABAN_KENAR)
    xfler, tabanlar = list(_TABAN_XF), {}
    for i, sayfa in enumerate(sayfalar):
        if isinstance(sayfa, dict) and sayfa.get("stiller"):
            tabanlar[i] = len(xfler)
            for stil in sayfa["stiller"]:
                xfler.append(_kalip_xf(stil, fontlar, kenarlar))

    tipler = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
              'content-types">',
              '<Default Extension="rels" ContentType="application/vnd.'
              'openxmlformats-package.relationships+xml"/>',
              '<Default Extension="xml" ContentType="application/xml"/>',
              '<Override PartName="/xl/workbook.xml" ContentType="application/'
              'vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
              '<Override PartName="/xl/styles.xml" ContentType="application/vnd.'
              'openxmlformats-officedocument.spreadsheetml.styles+xml"/>']

    kitap_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<workbook xmlns="http://schemas.openxmlformats.org/'
                 'spreadsheetml/2006/main" xmlns:r="http://schemas.'
                 'openxmlformats.org/officeDocument/2006/relationships"><sheets>']

    relq = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            '2006/relationships">']

    for i, ad in enumerate(adlar, start=1):
        tipler.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.worksheet+xml"/>')
        kitap_xml.append(
            f'<sheet name="{_kacis(ad)}" sheetId="{i}" r:id="rId{i}"/>')
        relq.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i}.xml"/>')

    tipler.append("</Types>")
    kitap_xml.append("</sheets></workbook>")
    relq.append(
        f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>")

    kova = BytesIO()
    with zipfile.ZipFile(kova, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(tipler))
        z.writestr("_rels/.rels", _KOK_REL)
        z.writestr("xl/workbook.xml", "".join(kitap_xml))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(relq))
        z.writestr("xl/styles.xml", _stil_xml(fontlar, kenarlar, xfler))
        for i, sayfa in enumerate(sayfalar, start=1):
            icerik = (_yerlesim_xml(sayfa, tabanlar.get(i - 1, 0))
                      if isinstance(sayfa, dict)
                      else _sayfa_xml(sayfa[1], sayfa[2]))
            z.writestr(f"xl/worksheets/sheet{i}.xml", icerik)
    return kova.getvalue()


def dosya_adi(kok: str) -> str:
    """`kok` + bugünün tarihi + .xlsx — indirilen dosyalar karışmasın diye.

    Türkçe harfler ve boşluk ayıklanır: dosya adı tarayıcıdan geçip Windows'a
    iniyor, orada bozulmasın.
    """
    cevir = str.maketrans("çğıöşüÇĞİÖŞÜ ", "cgiosuCGIOSU_")
    temiz = re.sub(r"[^A-Za-z0-9_.-]", "", str(kok).translate(cevir))
    return f"{temiz or 'disari'}_{_dt.date.today().isoformat()}.xlsx"
