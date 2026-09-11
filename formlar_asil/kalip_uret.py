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

    kapali = {}          # (r,c) -> True  (birlesmenin icinde, basilmaz)
    yayilim = {}         # (r,c) -> (rowspan, colspan)
    for (r1, r2, c1, c2) in sh.merged_cells:
        yayilim[(r1, c1)] = (r2 - r1, c2 - c1)
        for r in range(r1, r2):
            for c in range(c1, c2):
                if (r, c) != (r1, c1):
                    kapali[(r, c)] = True

    def bilgi(r, c):
        """(metin, stil_tuple, dolu_mu)"""
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
        return m, stil, bool(m.strip()) or any(kenar)

    # son dolu satir
    son = 0
    for r in range(sh.nrows):
        for c in range(ncol):
            if (r, c) in kapali:
                continue
            _, _, dolu = bilgi(r, c)
            if dolu:
                son = r
    for (r1, r2, c1, c2) in sh.merged_cells:
        son = max(son, r2 - 1)

    stiller, stil_no = [], {}
    def no(stil):
        if stil not in stil_no:
            stil_no[stil] = len(stiller)
            stiller.append({"pt": stil[0], "kalin": stil[1], "yatay": stil[2],
                            "dikey": stil[3], "sar": stil[4],
                            "kenar": list(stil[5])})
        return stil_no[stil]

    # Excel'de bir hucrenin yazisi, yanindaki hucre bossa ve aralarinda dikey
    # cizgi yoksa oraya tasar. HTML tablosunda tasma yok; ayni gorunumu vermek
    # icin bos hucre soldaki hucreye katiliyor (colspan). Ayni sey degerin
    # yazilacagi kutular icin de gecerli: kagitta "Dosya No : ......" tek bir
    # acik alan, 6 ayri hucre degil.
    def katilir(onceki_stil, stil, metin, rs, cs):
        if metin.strip() or rs != 1 or cs != 1:
            return False
        if onceki_stil is None:
            return False
        ok, yk = onceki_stil[5], stil[5]
        return (ok[3] == 0 and yk[2] == 0        # aralarinda dikey cizgi yok
                and ok[0] == yk[0] and ok[1] == yk[1])   # ust/alt ayni

    satirlar = []
    for r in range(son + 1):
        hucreler, stiller_satir, bos = [], [], 0
        for c in range(ncol):
            if (r, c) in kapali:
                continue
            rs, cs = yayilim.get((r, c), (1, 1))
            m, stil, dolu = bilgi(r, c)

            onceki = hucreler[-1] if hucreler and not bos else None
            onc_stil = stiller_satir[-1] if onceki else None
            if (onceki and onceki[1] == 1
                    and katilir(onc_stil, stil, m, rs, cs)):
                onceki[2] += 1                       # colspan
                yeni_stil = onc_stil[:5] + ((onc_stil[5][0], onc_stil[5][1],
                                             onc_stil[5][2], stil[5][3]),)
                stiller_satir[-1] = yeni_stil
                onceki[4] = no(yeni_stil)
                continue

            if not dolu and rs == 1 and cs == 1:
                bos += 1
                continue
            if bos:
                hucreler.append([c - bos, 1, bos, "", None])
                stiller_satir.append(None)
                bos = 0
            hucreler.append([c, rs, cs, m, no(stil)])
            stiller_satir.append(stil)
        satirlar.append(hucreler)          # kuyruktaki bos hucreler atiliyor

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
