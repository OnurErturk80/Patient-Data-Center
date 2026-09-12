# -*- coding: utf-8 -*-
"""Orijinal .xls formlarindan kalibi cikarir -> form_kalip.json

Bu **programin parcasi degil**, tek seferlik bir gelistirme araci. Kagit asil
degisirse (kalite sistemi formu revize ederse) yeni .xls buraya konur ve bu
arac bir kez calistirilir:

    pip install xlrd          # yalnizca bu arac icin; programin bagimliligi degil
    python3 formlar_asil/kalip_uret.py \
        formlar_asil/embriyoloji_ozet_DH.FR.91.xls \
        formlar_asil/art_lab_raporu_DH.FR.107.xls
    mv form_kalip.json ..     # arac calistigi klasore yaziyor

Cikardigi seyler: satir yukseklikleri, sutun genislikleri, birlesik hucreler,
her hucrenin punto/kalinlik/hiza bilgisi, dort kenarinin cizgi tipi ve kagitta
basili olan yazilar. Kagittaki yazim hatalari **duzeltilmez** -- belge o.
"""
import json, os, struct, sys, xlrd

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
import form_kalip                     # izgara kurma kurali orada
from xlrd.compdoc import CompDoc

# --------------------------------------------------------------- amblem
# Formlarin ustunde universitenin ambleminin PNG'si var; .xls icinde
# Escher (MSODRAWINGGROUP) kaydinda duruyor ve CONTINUE kayitlarina
# bolunmus olabiliyor -- dosyada PNG imzasini arayip kesmek bozuk dosya
# veriyor, kayitlari birlestirmek gerekiyor.

def _workbook_akimi(yol):
    c = CompDoc(open(yol, "rb").read(), print, 0)
    for ad in ("Workbook", "Book"):
        s = c.get_named_stream(ad)
        if s:
            return s
    raise SystemExit("Workbook akimi yok: " + yol)


def _kayitlar(s):
    i, out, n = 0, [], len(s)
    while i + 4 <= n:
        rec, boy = struct.unpack("<HH", s[i:i + 4])
        out.append((rec, s[i + 4:i + 4 + boy]))
        i += 4 + boy
    return out


def amblem(yol, hedef):
    """PNG'yi `hedef`e yazar, sayfadaki sabitleyicisini dondurur.

    Sabitleyici (client anchor) sekiz sayi: baslangic sutunu ve sutun
    genisliginin 1024'te kaci, baslangic satiri ve satir yuksekliginin
    256'da kaci, ayni sey bitis icin. Gorselin yeri bundan cikiyor.
    """
    ks = _kayitlar(_workbook_akimi(yol))
    blob, topluyor = bytearray(), False
    for rec, veri in ks:
        if rec == 0x00EB:                      # MSODRAWINGGROUP
            blob += veri
            topluyor = True
        elif rec == 0x003C and topluyor:       # CONTINUE
            blob += veri
        else:
            topluyor = False
    if not blob or b"\x89PNG\r\n\x1a\n" not in bytes(blob):
        return None
    b = bytes(blob)
    bas = b.index(b"\x89PNG\r\n\x1a\n")
    son = b.index(b"IEND", bas) + 8
    with open(hedef, "wb") as f:
        f.write(b[bas:son])

    for rec, veri in ks:
        if rec == 0x00EC:                      # MSODRAWING (sayfadaki sekil)
            j = veri.find(b"\x00\x00\x10\xf0")   # OfficeArtClientAnchor
            if j >= 0 and len(veri) >= j + 26:
                a = struct.unpack("<9H", veri[j + 8:j + 26])
                return {"dosya": os.path.basename(hedef), "sabit": list(a[1:])}
    return None


def kalip(yol):
    b = xlrd.open_workbook(yol, formatting_info=True)
    sh = b.sheet_by_index(0)
    ncol = sh.ncols

    def oku(r, c):
        """(metin, stil) -- izgara_kur'un bekledigi bicimde."""
        cell = sh.cell(r, c)
        xf = b.xf_list[sh.cell_xf_index(r, c)]
        f = b.font_list[xf.font_index]
        br = xf.border
        kenar = (br.top_line_style, br.bottom_line_style,
                 br.left_line_style, br.right_line_style)
        if cell.ctype == 2:                       # sayi
            m = int(cell.value) if cell.value == int(cell.value) else cell.value
            m = str(m)
        elif cell.ctype in (1, 3, 4):
            m = str(cell.value)
        else:
            m = ""
        stil = (f.height // 20, 1 if f.bold else 0,
                xf.alignment.hor_align, xf.alignment.vert_align,
                1 if xf.alignment.text_wrapped else 0, kenar)
        return m, stil

    # Izgarayi kuran kural programla ortak: yuklenen .xlsx de ayni yoldan
    # geciyor (form_kalip.izgara_kur), yoksa iki form farkli basilirdi.
    stiller, satirlar, son = form_kalip.izgara_kur(
        ncol, sh.nrows, list(sh.merged_cells), oku)

    yuk = []
    for r in range(son + 1):
        ri = sh.rowinfo_map.get(r)
        yuk.append(round(ri.height / 20.0, 1) if ri and ri.height else None)

    return {
        "sutun": [sh.computed_column_width(c) for c in range(ncol)],
        "satir_yuksekligi": yuk,
        "stiller": stiller,
        "satirlar": satirlar,
    }


AMBLEM = "form_amblem.png"     # static/ altina yaziliyor

out = {}
for ad, yol in (("ozet", sys.argv[1]), ("artlab", sys.argv[2])):
    out[ad] = kalip(yol)
    k = out[ad]
    g = amblem(yol, os.path.join("static", AMBLEM))
    k["gorseller"] = [g] if g else []
    print(ad, "satir=%d sutun=%d stil=%d hucre=%d gorsel=%d" % (
        len(k["satirlar"]), len(k["sutun"]), len(k["stiller"]),
        sum(len(s) for s in k["satirlar"]), len(k["gorseller"])))
json.dump(out, open("form_kalip.json", "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
