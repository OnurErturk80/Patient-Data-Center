"""Cryo Haritası'nın Excel'i -- her değişiklikte kendiliğinden (v6.191).

Kullanıcının isteği (2026-09-25): "Laboratuvarda cryo harita en önemli kayıt
... ben istediğim zaman bu excel cryo haritayı kopyalıyabileyim istiyordum."
Seçimi: "Bugünkü düzen + düz liste" -- her tank ayrı sayfa, kanisterler yan
yana, her goblet kapasitesi kadar satır (boş yerler de görünür); ek olarak
süzülebilir tek bir liste sayfası.

Dosya programın veri klasöründe, `lab.db`'nin yanında durur:
`cryo_harita/Cryo_Haritasi.xlsx`. Her günün son hali ayrıca
`Cryo_Haritasi_YYYY-AA-GG.xlsx` olarak `GUNLUK_SAKLA_GUN` gün saklanır.

- **Türetilmiş, kayıt değil.** Harita her seferinde tank düzeninden, dolu
  tüplerden ve Excel kayıtlarından baştan kuruluyor ("cryo haritası
  türetilmiştir", CLAUDE.md). Dosyada elle yapılan değişiklik programa
  girmez ve bir sonraki yazımda kaybolur -- dosyanın ilk sayfası söylüyor.
- **Ne zaman yazılır.** Program açıkken arka planda bir iş parçacığı
  `KONTROL_SN` saniyede bir veritabanının damgasına bakar
  (`app.veri_damgasi()`, açık ekranları tazeleyen damganın aynısı).
  Damga değiştiyse haritanın İÇERİĞİ kurulur ve içeriğin imzası son
  yazılanla karşılaştırılır; dosya yalnızca harita gerçekten değiştiyse
  yazılır. Bir ICSI kaydı dosyayı yeniden yazdırmaz, bir dondurma yazdırır.
- **Yazım atomik**: önce yanındaki geçici dosyaya, sonra `os.replace` --
  yarım dosya kalmaz. Windows'ta Excel'de açık duran dosya değiştirilemez;
  yazılamazsa sebebi Cryo Haritası'nın kartına düşer, bir sonraki turda
  yeniden denenir.
- **Hiçbir hata programı durdurmaz**: günlüğe (`program.log`, `print`
  değil -- CLAUDE.md) ve karta yazılır.
- Sayfa başlıkları ve hücre yazıları Türkçe, çevrilmiyor: öteki Excel
  çıktılarının kuralı (bekleyen iş 8).
"""

import datetime as _dt
import hashlib
import json
import logging
import os
import re
import threading

import db
import excel
import yerlesim

_gunluk = logging.getLogger("program")

KLASOR_ADI = "cryo_harita"
DOSYA_KOKU = "Cryo_Haritasi"
GUNLUK_SAKLA_GUN = 30
KONTROL_SN = 60
# Program açılır açılmaz değil: göçler ve ilk istekler önce.
ILK_BEKLEME_SN = 5
# Bir bantta yan yana kaç kanister -- laboratuvarın Excel'inde de 5-6.
BANT_KANISTER = 6

EXCEL_KAYDI = "EXCEL KAYDI"
_GUNLUK_AD = re.compile(r"^" + DOSYA_KOKU + r"_(\d{4}-\d{2}-\d{2})\.xlsx$")

# Laboratuvarın Excel'indeki blok: NO SOYAD AD EŞİ TARİH HÜCRE VİAL. Soyad ve
# ad TEK sütun: program adı tek alanda tutuyor (`hasta.ad_soyad`) ve soyadın
# nerede başladığını tahmin etmek (iki soyadlı hasta) yanlış yazabilirdi.
# DOSYA NO eklendi (Excel'de yoktu; tek güvenilir anahtar, v6.125), ETİKET
# tüpün programdaki etiketi.
_BLOK_BASLIK = ["NO", "HASTA", "EŞİ", "DOSYA NO", "TARİH", "HÜCRE", "VİAL", "ETİKET"]
_BLOK_GENISLIK = [8, 26, 18, 11, 11, 24, 18, 16]
_BLOK_ARA = 3                       # bloklar arasındaki boş sütun
_BLOK_ADIM = len(_BLOK_BASLIK) + 1

# Tank sayfalarının kendi stilleri (`excel._yerlesim_xml`: sıra numarası).
# Gobletin son satırının alt çizgisi kalın -- 4 satırlık gobletler göz
# gezdirirken ayrılsın. Kenar: (üst, alt, sol, sağ); 1 ince, 2 orta.
_S_HUCRE, _S_HUCRE_SON, _S_NO, _S_NO_SON = 0, 1, 2, 3
_STILLER = [
    {"pt": 10, "kenar": (1, 1, 1, 1), "yatay": 1},
    {"pt": 10, "kenar": (1, 2, 1, 1), "yatay": 1},
    {"pt": 10, "kalin": True, "kenar": (1, 1, 1, 1), "yatay": 2},
    {"pt": 10, "kalin": True, "kenar": (1, 2, 1, 1), "yatay": 2},
]

LISTE_BASLIK = ["Tank", "Kanister", "Goblet", "Tür", "Hasta", "Eşi", "Dosya no",
                "Dondurma", "İçerik", "Taşıyıcı", "Renk", "Etiket", "Kaynak", "Yer"]
BOS_BASLIK = ["Tank", "Kanister", "Goblet", "Kapasite", "Dolu", "Boş",
              "Gobletteki renkler"]

_KILIT = threading.Lock()
_DURDUR = threading.Event()
_IS = None
# Son yazımın imzası ve zamanı, son hata. Bellekte: program yeniden açılınca
# ilk tur dosyayı bir kez daha yazar (içerik aynı, zaman yeni) -- zararsız.
_DURUM = {}


def klasor():
    return db.VERI_KOK / KLASOR_ADI


def ana_dosya():
    return klasor() / f"{DOSYA_KOKU}.xlsx"


# ------------------------------------------------------------ içerik

def _gun(iso) -> str:
    """'2026-09-04 ...' -> '04.09.2026' (ekrandaki `gg_aa_yyyy()`). Tank
    sayfası yerleşim sayfası: tarih metin yazılıyor (resmî formlarınki gibi);
    liste sayfasında ISO kalıyor, Excel onu tarih olarak alıyor."""
    if not iso:
        return ""
    e = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(iso))
    return f"{e.group(3)}.{e.group(2)}.{e.group(1)}" if e else str(iso)


def _renk_sirasi(x) -> tuple:
    # Goblet ekranının sırası: straw'lar goblette rengiyle ayırt ediliyor.
    return (x["renk"] is None, x["renk"] or "")


def _hucre_metni(x) -> str:
    """Tüpün içeriği, Excel'in HÜCRE sütunu gibi: "D5 (3AA-4AB)",
    "Yumurta (5*MII)", "Sperm · TESE"."""
    if x["kategori"] == "sperm":
        return "Sperm" + (f" · {x['sperm_sebep']}" if x.get("sperm_sebep") else "")
    if x["yumurta"]:
        return f"Yumurta {x['parantez']}".strip()
    return f"{x['gun']} {x['parantez']}".strip()


def _tur(x) -> str:
    if x["kategori"] == "sperm":
        return "Sperm"
    return "Yumurta" if x["yumurta"] else "Embriyo"


def _excel_adi(e) -> str:
    # Programın sırası (ad soyad), Excel'de iki ayrı sütundu.
    return " ".join(p for p in (e["ad"], e["soyad"]) if p)


def _tup_hucreleri(x, tipler, renkler) -> list:
    vial = " ".join(v for v in (tipler.get(x["tip"], x["tip"]),
                                renkler.get(x["renk"], x["renk"])) if v)
    return [x["ad_soyad"] or "", x["es_adi"] or "", x["dosya_no"],
            _gun(x["vitrifikasyon_zamani"]), _hucre_metni(x), vial, x["etiket"] or ""]


def _excel_hucreleri(e) -> list:
    tarih = _gun(e["tarih"]) if e["tarih"] else (e["tarih_ham"] or "")
    return [_excel_adi(e), e["es_adi"] or "", None, tarih, e["icerik"] or "",
            e["vial"] or "", EXCEL_KAYDI]


def _parcalar(k) -> tuple:
    """Konum satırının üç seviyesi, yazıldığı gibi. Seviyeleri boş, yalnızca
    `tam_yol`u olan eski satır `/` ile bölünüyor (`yerlesim.konum_anahtari`)."""
    if not (k["seviye1"] or k["seviye2"] or k["seviye3"]) and k["tam_yol"]:
        p = [x.strip() for x in k["tam_yol"].split("/")] + ["", "", ""]
        return tuple(p[:3])
    return (k["seviye1"] or "", k["seviye2"] or "", k["seviye3"] or "")


def _kur() -> dict:
    """Haritanın içeriği: tank blokları, liste, boş yerler ve imzası.

    Tank sayfaları tank düzeninden (`yerlesim.doluluk()`); düzen hiç
    kurulmamışsa (`cryo_esle.py yerlesim` çalışmamış) tüplerin yazılı
    konumlarından -- o zaman yalnızca dolu gobletler görünür, boş yuva
    bilinmez. Liste her dolu tüpü ve tankta duran her Excel kaydını taşır,
    yeri bilinmeyenler dahil.
    """
    harita = yerlesim.doluluk()
    etiket = {}
    for r in db.sorgu("SELECT liste_adi, kod, etiket FROM liste_degeri "
                      "WHERE lab_id=? AND liste_adi IN ('tasiyici_tipi','tasiyici_renk')",
                      (db.LAB_ID,)):
        etiket.setdefault(r["liste_adi"], {})[r["kod"]] = r["etiket"]
    tipler, renkler = etiket.get("tasiyici_tipi", {}), etiket.get("tasiyici_renk", {})
    konumlar = {r["id"]: r for r in db.sorgu(
        "SELECT id, seviye1, seviye2, seviye3, tam_yol FROM konum WHERE lab_id=?",
        (db.LAB_ID,))}
    tup_konum = {r["id"]: r["konum_id"] for r in db.sorgu(
        "SELECT id, konum_id FROM tasiyici WHERE lab_id=? AND durum='dolu'", (db.LAB_ID,))}
    tupler = yerlesim.tup_ayrintilari(list(tup_konum))
    ekler = {}
    if yerlesim.excel_kaydi_var():
        ekler = yerlesim.excel_ayrintilari([r["id"] for r in db.sorgu(
            "SELECT id FROM excel_kaydi WHERE lab_id=? AND durum='tankta'", (db.LAB_ID,))])

    gobletler = list(harita["gobletler"].values())
    duzen = bool(gobletler)
    if not duzen:
        # Düzensiz: tüpün yazılı konumu bir goblet sayılır, kapasitesi bilinmez.
        sozde = {}
        for tid, kid in tup_konum.items():
            if kid in konumlar:
                a = yerlesim.konum_anahtari(konumlar[kid])
                t, k, g = _parcalar(konumlar[kid])
                sozde.setdefault(a, {"tank": t, "kanister": k, "goblet": g,
                                     "kapasite": None, "sira": None,
                                     "tupler": [], "excel": []})["tupler"].append({"id": tid})
        for e in ekler.values():
            if e["konum_id"] in konumlar:
                a = yerlesim.konum_anahtari(konumlar[e["konum_id"]])
                t, k, g = _parcalar(konumlar[e["konum_id"]])
                sozde.setdefault(a, {"tank": t, "kanister": k, "goblet": g,
                                     "kapasite": None, "sira": None,
                                     "tupler": [], "excel": []})["excel"].append({"id": e["id"]})
        gobletler = list(sozde.values())

    # Hangi tüp / Excel kaydı hangi gobletde: haritanın kendi hesabı.
    yeri = {}
    for g in gobletler:
        for t in g["tupler"]:
            yeri[("t", t["id"])] = g
        for e in g["excel"]:
            yeri[("e", e["id"])] = g

    def ogeler(g):
        return sorted([{"renk": tupler[t["id"]]["renk"], "tur": "t", "x": tupler[t["id"]]}
                       for t in g["tupler"] if t["id"] in tupler] +
                      [{"renk": ekler[e["id"]]["renk"], "tur": "e", "x": ekler[e["id"]]}
                       for e in g["excel"] if e["id"] in ekler], key=_renk_sirasi)

    def satir(o):
        return (_tup_hucreleri(o["x"], tipler, renkler) if o["tur"] == "t"
                else _excel_hucreleri(o["x"]))

    # Kanisterinde olup hiçbir düzen gobletine düşmeyenler bloğun sonunda
    # "gobleti belirsiz" (goblet ekranının kartı); kanisteri de düzende
    # yoksa yalnızca listede.
    # Düzen yokken bunlar zaten yazılı konumlarının gobletinde (yukarıda).
    belirsiz = {}
    for liste, tur in ((harita["duzen_disi"], "t"), (harita["excel_disi"], "e")):
        for x in liste if duzen else ():
            if x["anahtar"]:
                belirsiz.setdefault(x["anahtar"][:2], []).append((tur, x))

    tanklar = {}
    for g in gobletler:
        a = yerlesim.yer_anahtari(g["tank"], g["kanister"], "")[:2]
        tank = tanklar.setdefault(a[0], {"ad": g["tank"] or "—", "kanisterler": {}})
        tank["kanisterler"].setdefault(a[1], {"ad": g["kanister"] or "", "gl": []})["gl"].append(g)

    sayfa_verisi = []
    bos_satirlari = []
    for ta in sorted(tanklar, key=lambda a: yerlesim._dogal(tanklar[a]["ad"])):
        t = tanklar[ta]
        alt, ust = [], []
        for ka in sorted(t["kanisterler"], key=lambda a: yerlesim._dogal(t["kanisterler"][a]["ad"])):
            kn = t["kanisterler"][ka]
            gl = sorted(kn["gl"], key=lambda g: (g["sira"] or 0, yerlesim._dogal(g["goblet"])))
            for kat, secilen in ((alt, [g for g in gl if (g["sira"] or 0) < 1000]),
                                 (ust, [g for g in gl if (g["sira"] or 0) >= 1000])):
                if not secilen:
                    continue
                satirlar = []
                for g in secilen:
                    o = ogeler(g)
                    n = max(len(o), g["kapasite"] or 1)
                    for i in range(n):
                        satirlar.append([g["goblet"] or "", *(satir(o[i]) if i < len(o)
                                         else [""] * (len(_BLOK_BASLIK) - 1)), i == n - 1])
                    if g["kapasite"] and len(o) < g["kapasite"]:
                        bos_satirlari.append([
                            g["tank"], g["kanister"], g["goblet"], g["kapasite"], len(o),
                            g["kapasite"] - len(o),
                            ", ".join(sorted({renkler.get(x["renk"], x["renk"])
                                              for x in o if x["renk"]}))])
                ek = []
                if kat is alt:
                    for tur, x in belirsiz.get((ta, ka), []):
                        o = {"tur": tur, "renk": None,
                             "x": tupler.get(x["id"]) if tur == "t" else ekler.get(x["id"])}
                        if o["x"] is None:
                            continue
                        k = konumlar.get(o["x"].get("konum_id") if tur == "e"
                                         else tup_konum.get(x["id"]))
                        ek.append([(_parcalar(k)[2] if k else "") or "?", *satir(o), True])
                kat.append({"baslik": f"KANİSTER {kn['ad']}" + (" · ÜST KAT" if kat is ust else ""),
                            "satirlar": satirlar, "belirsiz": ek})
        sayfa_verisi.append({"ad": t["ad"], "alt": alt, "ust": ust})

    # Düz liste: her dolu tüp ve tankta duran her Excel kaydı bir satır.
    liste = []
    for tur, kaynak in (("t", tupler), ("e", ekler)):
        for i, x in kaynak.items():
            g = yeri.get((tur, i))
            kid = tup_konum.get(i) if tur == "t" else x["konum_id"]
            if g is not None:
                yer, parca, sira = "", (g["tank"], g["kanister"], g["goblet"]), g["sira"] or 0
            elif kid in konumlar:
                yer, parca, sira = ("Düzende yok" if duzen else ""), _parcalar(konumlar[kid]), 0
            else:
                yer, parca, sira = "Konum girilmemiş", ("", "", ""), 0
            if tur == "t":
                ic = [_tur(x), x["ad_soyad"], x["es_adi"], x["dosya_no"],
                      (x["vitrifikasyon_zamani"] or "")[:10] or None, _hucre_metni(x),
                      tipler.get(x["tip"], x["tip"]), renkler.get(x["renk"], x["renk"]),
                      x["etiket"], "Program"]
            else:
                ic = ["Sperm" if x["kategori"] == "sperm" else "Embriyo/yumurta",
                      _excel_adi(x), x["es_adi"], None, x["tarih"] or x["tarih_ham"],
                      x["icerik"], x["tip"] and tipler.get(x["tip"], x["tip"]),
                      x["renk"] and renkler.get(x["renk"], x["renk"]), None, "Excel kaydı"]
            liste.append((yer == "Konum girilmemiş",
                          yerlesim._dogal(parca[0]), yerlesim._dogal(parca[1]), sira,
                          yerlesim._dogal(parca[2]), _renk_sirasi(x),
                          [*parca, *ic, yer]))
    liste.sort(key=lambda s: s[:6])
    liste = [s[-1] for s in liste]

    ozet = {"tank": len(sayfa_verisi), "tup": len(tupler), "excel": len(ekler),
            "bos_yuva": sum(s[5] for s in bos_satirlari),
            "belirsiz": sum(1 for s in liste if s[-1]), "duzen": duzen}
    icerik = {"tanklar": sayfa_verisi, "liste": liste, "bos": bos_satirlari, "ozet": ozet}
    imza = hashlib.sha256(json.dumps(icerik, ensure_ascii=False, default=str,
                                     sort_keys=True).encode("utf-8")).hexdigest()
    return {**icerik, "imza": imza}


# ------------------------------------------------------------ sayfalar

def _blok_yaz(hucreler, birlesik, blok, r0, c0) -> int:
    """Bir kanister bloğunu `r0` satırı, `c0` sütunundan yazar; yüksekliği."""
    son = c0 + len(_BLOK_BASLIK) - 1
    adr = lambda c, r: f"{excel._sutun_adi(c)}{r}"
    hucreler[adr(c0, r0)] = (blok["baslik"], "bolum")
    birlesik.append(f"{adr(c0, r0)}:{adr(son, r0)}")
    for j, b in enumerate(_BLOK_BASLIK):
        hucreler[adr(c0 + j, r0 + 1)] = (b, "etiket")
    r = r0 + 2
    for s in blok["satirlar"]:
        *degerler, son_mu = s
        for j, d in enumerate(degerler):
            stil = ((_S_NO_SON if son_mu else _S_NO) if j == 0
                    else (_S_HUCRE_SON if son_mu else _S_HUCRE))
            hucreler[adr(c0 + j, r)] = (d, stil)
        r += 1
    if blok["belirsiz"]:
        hucreler[adr(c0, r)] = ("GOBLETİ BELİRSİZ (yazılan goblet düzende yok)", "etiket")
        birlesik.append(f"{adr(c0, r)}:{adr(son, r)}")
        r += 1
        for s in blok["belirsiz"]:
            *degerler, _ = s
            for j, d in enumerate(degerler):
                hucreler[adr(c0 + j, r)] = (d, _S_NO_SON if j == 0 else _S_HUCRE_SON)
            r += 1
    return r - r0


def _tank_sayfasi(t, zaman) -> dict:
    hucreler, birlesik = {}, []
    en_cok = min(BANT_KANISTER, max(len(t["alt"]), len(t["ust"]), 1))
    son = excel._sutun_adi(en_cok * _BLOK_ADIM - 1)
    hucreler["A1"] = (t["ad"], "formadi")
    birlesik.append(f"A1:{son}1")
    hucreler["A2"] = (f"Program tarafından {zaman} tarihinde üretildi. Elle "
                      "değişiklik yapmayın: dosya her güncellemede yeniden yazılır.", "dipnot")
    birlesik.append(f"A2:{son}2")
    r = 4
    for kat_adi, bloklar in (("", t["alt"]), ("ÜST KAT", t["ust"])):
        if not bloklar:
            continue
        if kat_adi:
            hucreler[f"A{r}"] = (kat_adi, "kurum")
            birlesik.append(f"A{r}:{son}{r}")
            r += 2
        for i in range(0, len(bloklar), BANT_KANISTER):
            yukseklik = 0
            for j, blok in enumerate(bloklar[i:i + BANT_KANISTER]):
                yukseklik = max(yukseklik, _blok_yaz(hucreler, birlesik, blok, r,
                                                     1 + j * _BLOK_ADIM))
            r += yukseklik + 1
    genislikler = {}
    for j in range(en_cok):
        c0 = 1 + j * _BLOK_ADIM
        for k, g in enumerate(_BLOK_GENISLIK):
            genislikler[c0 + k] = g
        genislikler[c0 + len(_BLOK_BASLIK)] = _BLOK_ARA
    return {"ad": t["ad"], "hucreler": hucreler, "birlesik": birlesik,
            "genislikler": genislikler, "stiller": _STILLER,
            "yazdirma": {"sigdir": False, "yon": "yatay"}}


def _bilgi_sayfasi(v, zaman) -> dict:
    o = v["ozet"]
    satirlar = [("Üretildi", zaman),
                ("Programdaki dolu tüp", o["tup"]),
                ("Excel kaydı (tankta)", o["excel"]),
                ("Boş yuva", o["bos_yuva"] if o["duzen"] else "tank düzeni kurulmamış"),
                ("Yeri belirsiz", o["belirsiz"])]
    notlar = [
        "Bu dosyayı program yazar: Cryo Haritası'nda bir şey değişince (dondurma, "
        "çözme, taşıma, Excel kaydı) kendiliğinden yeniden üretilir. Dosyada yapılan "
        "değişiklik programa girmez ve bir sonraki güncellemede silinir.",
        "Tank sayfaları laboratuvarın Cryo Haritası düzeninde: kanisterler yan yana, "
        "her goblet kapasitesi kadar satır; boş satır boş yuvadır. Liste sayfası her "
        "straw'ı tek satırda verir, Excel'in süzgeciyle ayıklanabilir.",
        f"{EXCEL_KAYDI}: eski Cryo Haritası Excel'inde bu yerde duran, programda "
        "tüpü bulunamamış straw. Programda Cryo Haritası'ndan bir tüpe bağlanabilir.",
        "Dosyayı Excel'de açmadan önce bir kopyasını alın: açık duran dosya "
        "güncellenemez (program bir sonraki denemede yeniden yazar).",
    ]
    if not o["duzen"]:
        notlar.insert(2, "Tank düzeni kurulmamış (cryo_esle.py yerlesim): tank "
                         "sayfalarında yalnızca tüpü olan yerler var, boş yuva bilinmiyor.")
    hucreler = {"A1": ("CRYO HARİTASI", "formadi")}
    r = 3
    for ad, deger in satirlar:
        hucreler[f"A{r}"] = (ad, "etiket")
        hucreler[f"B{r}"] = (deger, "deger")
        r += 1
    r += 1
    birlesik, yukseklik = ["A1:B1"], {}
    for n in notlar:
        hucreler[f"A{r}"] = (n, "deger")
        birlesik.append(f"A{r}:B{r}")
        yukseklik[r] = 42
        r += 1
    return {"ad": "Bilgi", "hucreler": hucreler, "birlesik": birlesik,
            "genislikler": {1: 26, 2: 90}, "yukseklikler": yukseklik,
            "yazdirma": {"sigdir": True, "yon": "dikey"}}


def _sayfalar(v, simdi) -> list:
    zaman = simdi.strftime("%d.%m.%Y %H:%M")
    sayfalar = [_bilgi_sayfasi(v, zaman)]
    sayfalar += [_tank_sayfasi(t, zaman) for t in v["tanklar"]]
    sayfalar.append(("Liste", LISTE_BASLIK, v["liste"]))
    if v["ozet"]["duzen"]:
        sayfalar.append(("Boş yerler", BOS_BASLIK, v["bos"]))
    return sayfalar


# ------------------------------------------------------------ yazma

def _yaz(yol, veri: bytes) -> None:
    """Atomik: yanındaki geçici dosyaya, sonra yerine. Yarım dosya kalmaz."""
    gecici = yol.with_name(yol.name + ".yaziliyor")
    try:
        gecici.write_bytes(veri)
        os.replace(gecici, yol)
    finally:
        if gecici.exists():
            try:
                gecici.unlink()
            except OSError:
                pass


def _temizle(bugun) -> None:
    """`GUNLUK_SAKLA_GUN` günden eski günlük kopyaları siler; başka dosyaya
    dokunmaz (ad kalıbı tutmuyorsa)."""
    sinir = bugun - _dt.timedelta(days=GUNLUK_SAKLA_GUN)
    for yol in klasor().iterdir():
        e = _GUNLUK_AD.match(yol.name)
        if not e:
            continue
        try:
            if _dt.date.fromisoformat(e.group(1)) < sinir:
                yol.unlink()
        except (ValueError, OSError):
            pass


def guncelle(bayt_iste: bool = False) -> dict:
    """Haritayı kurar; içeriği son yazılandan farklıysa (ya da dosya yoksa)
    ana dosyayı ve bugünün kopyasını yazar.

    -> {"yazildi": bool, "veri": .xlsx baytları ya da None}. `bayt_iste`:
    indirme için -- içerik değişmemiş olsa da baytlar üretilir. Veritabanı
    hatası yükselir; dosya yazılamazsa yükselmez, `durum()`'a düşer.
    """
    with _KILIT:
        v = _kur()
        simdi = _dt.datetime.now()
        degisti = v["imza"] != _DURUM.get("imza") or not ana_dosya().exists()
        veri = excel.kitap(_sayfalar(v, simdi)) if (degisti or bayt_iste) else None
        if not degisti:
            _DURUM.pop("kurulamadi", None)
            return {"yazildi": False, "veri": veri}
        try:
            klasor().mkdir(parents=True, exist_ok=True)
            _yaz(ana_dosya(), veri)
        except OSError as e:
            if _DURUM.get("hata") != str(e):
                _gunluk.warning("CRYO EXCEL: %s yazilamadi: %s", ana_dosya(), e)
            _DURUM.update(hata=str(e), kurulamadi=None)
            return {"yazildi": False, "veri": veri}
        try:
            _yaz(klasor() / f"{DOSYA_KOKU}_{simdi.date().isoformat()}.xlsx", veri)
            _temizle(simdi.date())
        except OSError as e:           # ana dosya yazıldı; kopya bir sonrakinde
            _gunluk.warning("CRYO EXCEL: gunluk kopya yazilamadi: %s", e)
        _DURUM.update(imza=v["imza"], zaman=simdi.isoformat(" ", "seconds"),
                      hata=None, kurulamadi=None, ozet=v["ozet"])
        _gunluk.info("CRYO EXCEL: harita yazildi (%d tup, %d Excel kaydi).",
                     v["ozet"]["tup"], v["ozet"]["excel"])
        return {"yazildi": True, "veri": veri}


def durum() -> dict:
    """Cryo Haritası'nın kartı için: son yazım zamanı, yol, varsa hata."""
    d = dict(_DURUM)
    yol = ana_dosya()
    if not d.get("zaman") and yol.exists():
        d["zaman"] = _dt.datetime.fromtimestamp(yol.stat().st_mtime).isoformat(" ", "seconds")
    d["yol"] = str(yol)
    d["klasor"] = str(klasor())
    return d


# ------------------------------------------------------------ arka plan

def _dongu(damga) -> None:
    son = None
    if _DURDUR.wait(ILK_BEKLEME_SN):
        return
    while True:
        try:
            if db.DB_YOLU.exists():
                d = damga()
                if d != son:
                    guncelle()
                    if not _DURUM.get("hata"):
                        son = d
        except Exception as e:           # hiçbir hata programı durdurmasın
            if _DURUM.get("kurulamadi") != repr(e):
                _gunluk.exception("CRYO EXCEL: harita kurulamadi")
            _DURUM["kurulamadi"] = repr(e)
        if _DURDUR.wait(KONTROL_SN):
            return


def baslat(damga) -> None:
    """Arka plandaki iş parçacığını başlatır (programın açılışında, göçlerden
    sonra). `damga`: veritabanının damgasını veren işlev -- değişmediyse
    harita hiç kurulmaz. Zaten çalışıyorsa bir şey yapmaz."""
    global _IS
    if _IS is not None and _IS.is_alive():
        return
    _DURDUR.clear()
    _IS = threading.Thread(target=_dongu, args=(damga,), name="cryo-harita-excel",
                           daemon=True)
    _IS.start()


def durdur() -> None:
    _DURDUR.set()
