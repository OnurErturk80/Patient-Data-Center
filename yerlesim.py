"""Tank düzeni: gobletler, doluluk, Cryo Haritası'nın ağacı (v6.189).

Kullanıcının isteği (2026-09-25): "Laboratuvarda cryo harita en önemli kayıt
... Bu haritanın kesinlikle bozulmaması gerekiyor. Benim programı yaparken
istediğim bir hastanın embriyolarını dondururken program bana tanklarda boş
yerleri önermesiydi."

Boş yeri bilmek için program tankın DÜZENİNİ tutuyor: her goblet bir `konum`
satırı (Tank / Kanister / Goblet), `kapasite` (kaç straw sığıyor), `kategori`
(embriyo / sperm) ve `sira` (kanister içindeki yeri) ile. Düzen laboratuvarın
Cryo Haritası Excel'inden bir kez kuruluyor (`cryo_esle.py yerlesim`);
sonrasında harita programın kendi kayıtlarından TÜRETİLİYOR, ayrıca
güncellenen bir doluluk tablosu yok ("cryo haritası türetilmiştir",
CLAUDE.md). Gobletin doluluğu = içinde duran dolu tüpler + Excel kaydı
(Excel'de o gobletde duran, programda karşılığı olan tüp bulunamamış satır).

**Yer adları serbest metin** -- dondurma ekranında elle yazılıyordu, "T1",
"Tank 1", "TANK 1" üçü de var olabilir. Bir tüpün hangi gobletde durduğu bu
yüzden `konum_id`'nin kendisiyle değil `yer_anahtari()` ile soruluyor: aynı
yeri söyleyen iki yazım aynı gobletin doluluğuna girer. Anahtar yalnızca
KARŞILAŞTIRMA içindir; ekrana ve veritabanına yazılan her zaman Excel'deki
yazım (`konum` satırının kendisi).
"""

import collections
import re

import cryo_excel
import db
import formlar

_TANK = re.compile(r"^(?:TANK|T)\s*-?\s*0*(\d+)$")
_KANISTER = re.compile(r"^(?:KANISTER|CANISTER|KAN|CAN|K|C)?\s*-?\s*0*(\d+)$")


def yer_anahtari(tank, kanister, goblet) -> tuple:
    """Tank / kanister / goblet -> karşılaştırma anahtarı.

    "T1", "tank 1", "TANK 1" -> "TANK 1"; "K3", "Kanister 3", "3" -> "3";
    goblette büyük/küçük harf ve boşluk farkı yok ("7 Üst" = "7üst",
    "p" = "P"). Gobletin harfi SİLİNMİYOR: "G" (TANK 4'ün A-P gobletlerinden
    biri) bir ön ek değil, gobletin kendisi.
    """
    t = cryo_excel._n(tank)
    e = _TANK.match(t)
    if e:
        t = f"TANK {int(e.group(1))}"
    k = cryo_excel._n(kanister)
    e = _KANISTER.match(k)
    if e:
        k = str(int(e.group(1)))
    g = cryo_excel._n(goblet).replace(" ", "")
    return (t, k, g)


def duzen_var() -> bool:
    """Tank düzeni kurulmuş mu (goc_052 + `cryo_esle.py yerlesim`)."""
    if not db.kolon_var("konum", "sira"):
        return False
    return db.tek("SELECT 1 FROM konum WHERE lab_id=? AND sira IS NOT NULL LIMIT 1",
                  (db.LAB_ID,)) is not None


def excel_kaydi_var() -> bool:
    return db.tablo_var("excel_kaydi")


def _dogal(metin):
    """"2" < "10", "A2" < "A10" (`app._dogal_sira()`'nın aynısı)."""
    return [(0, int(p), "") if p.isdigit() else (1, 0, p)
            for p in re.findall(r"\d+|\D+", str(metin or ""))]


def konum_anahtari(r) -> tuple:
    """Bir `konum` satırının anahtarı. Seviyeleri boş, yalnızca `tam_yol`u
    yazılı eski satırlar da var (test veritabanında bir sperm tüpü): yol
    " / " ile bölünüp okunuyor."""
    if not (r["seviye1"] or r["seviye2"] or r["seviye3"]) and r["tam_yol"]:
        parca = [x.strip() for x in r["tam_yol"].split("/")] + ["", "", ""]
        return yer_anahtari(*parca[:3])
    return yer_anahtari(r["seviye1"], r["seviye2"], r["seviye3"])


def doluluk(b=None) -> dict:
    """Bütün tank düzeni, doluluğuyla.

    -> {"gobletler": {anahtar: goblet}, "duzen_disi": [tüp], "excel_disi":
        [Excel kaydı], "konumsuz": n}

    goblet: {"konum_id", "tank", "kanister", "goblet", "kapasite", "kategori",
    "sira", "tupler": [...], "excel": [...], "dolu": n}. Tüp ve Excel kaydı
    yalnızca kimlik, renk ve tip taşıyor -- ayrıntı ekranın kendi sorgusunda.
    `duzen_disi` / `excel_disi`: konumu var ama anahtarı hiçbir düzen
    gobletine düşmeyen dolu tüpler ve Excel kayıtları (elle yazılmış
    bilinmeyen bir yer; Excel'de NO'su boş satır) -- `anahtar`larıyla, haritada
    kanisterlerinin altında görünsünler diye. Göç (052) çalışmamışsa boş döner.
    """
    kapat = b is None
    if b is None:
        b = db.baglan()
    try:
        sonuc = {"gobletler": {}, "duzen_disi": [], "excel_disi": [], "konumsuz": 0}
        if not any(r[1] == "sira" for r in b.execute("PRAGMA table_info(konum)")):
            return sonuc
        anahtar_of = {}
        for r in b.execute("SELECT id, seviye1, seviye2, seviye3, kapasite, kategori, "
                           "sira, tam_yol FROM konum WHERE lab_id=?", (db.LAB_ID,)):
            a = konum_anahtari(r)
            anahtar_of[r["id"]] = a
            if r["sira"] is not None:
                sonuc["gobletler"][a] = {
                    "konum_id": r["id"], "tank": r["seviye1"], "kanister": r["seviye2"],
                    "goblet": r["seviye3"], "tam_yol": r["tam_yol"],
                    "kapasite": r["kapasite"], "kategori": r["kategori"],
                    "sira": r["sira"], "tupler": [], "excel": [], "dolu": 0}
        gob = sonuc["gobletler"]
        for r in b.execute("SELECT id, etiket, tip, renk, konum_id, kategori, "
                           "vitrifikasyon_zamani FROM tasiyici WHERE lab_id=? "
                           "AND durum='dolu'", (db.LAB_ID,)):
            if r["konum_id"] is None:
                sonuc["konumsuz"] += 1
                continue
            g = gob.get(anahtar_of.get(r["konum_id"]))
            if g is None:
                sonuc["duzen_disi"].append({**dict(r), "anahtar": anahtar_of.get(r["konum_id"])})
                continue
            g["tupler"].append(dict(r))
            g["dolu"] += 1
        if any(r[0] == "excel_kaydi" for r in b.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")):
            for r in b.execute("SELECT id, konum_id, kategori, tip, renk FROM excel_kaydi "
                               "WHERE lab_id=? AND durum='tankta'", (db.LAB_ID,)):
                g = gob.get(anahtar_of.get(r["konum_id"]))
                if g is None:
                    sonuc["excel_disi"].append({**dict(r), "anahtar": anahtar_of.get(r["konum_id"])})
                    continue
                g["excel"].append(dict(r))
                g["dolu"] += 1
        return sonuc
    finally:
        if kapat:
            b.close()


def bos_yuva(g) -> int:
    """Gobletin boş yuva sayısı; kapasitesi bilinmiyorsa 0 (önerilmez)."""
    if not g["kapasite"]:
        return 0
    return max(0, g["kapasite"] - g["dolu"])


def agac(harita, kategori="embriyo") -> dict:
    """Cryo Haritası'nın ağacı: tank -> kanister, sayılarıyla.

    -> {"tanklar": [...], "yersiz_tup": [...], "yersiz_excel": [...]}

    Bir kategorinin ağacına o kategorinin gobletleri girer; öteki kategorinin
    gobletinde duran bir tüp de (sperm gobletinde embriyo tüpü gibi) o
    gobletle birlikte gelir, kaybolmasın diye. Düzen gobletine düşmeyen tüp ve
    Excel kaydı kanisteri düzende varsa o kanisterin `yersiz` sayısına,
    yoksa ağacın dışındaki `yersiz_*` listelerine.
    """
    tanklar = {}
    for g in harita["gobletler"].values():
        kendi = g["kategori"] == kategori
        tupu_var = any(t["kategori"] == kategori for t in g["tupler"]) or \
            any(e["kategori"] == kategori for e in g["excel"])
        if not (kendi or tupu_var):
            continue
        a = yer_anahtari(g["tank"], g["kanister"], "")
        tank = tanklar.setdefault(a[0], {"ad": g["tank"] or "—", "kanisterler": {}})
        tank["kanisterler"].setdefault(a[1], {"ad": g["kanister"] or "", "gl": []})["gl"].append(g)
    yersiz_tup, yersiz_excel = [], []
    yersiz = collections.Counter()
    for liste, hedef in ((harita["duzen_disi"], yersiz_tup),
                         (harita["excel_disi"], yersiz_excel)):
        for x in liste:
            if x["kategori"] != kategori:
                continue
            a = x["anahtar"] or ("", "", "")
            if a[0] in tanklar and a[1] in tanklar[a[0]]["kanisterler"]:
                yersiz[a[:2]] += 1
            else:
                hedef.append(x)
    sonuc = []
    for ta in sorted(tanklar, key=lambda a: _dogal(tanklar[a]["ad"])):
        t = tanklar[ta]
        kanisterler = []
        for ka in sorted(t["kanisterler"], key=lambda a: _dogal(t["kanisterler"][a]["ad"])):
            gl = t["kanisterler"][ka]["gl"]
            duzenli = [g for g in gl if g["kapasite"]]
            kanisterler.append({
                "ad": t["kanisterler"][ka]["ad"], "goblet": len(gl), "duzenli": len(duzenli),
                "kapasite": sum(g["kapasite"] for g in duzenli),
                "bos_yuva": sum(bos_yuva(g) for g in duzenli),
                "tup": sum(len(g["tupler"]) for g in gl),
                "excel": sum(len(g["excel"]) for g in gl),
                "yersiz": yersiz[(ta, ka)],
                "ust_kat": any((g["sira"] or 0) >= 1000 for g in gl)})
        sonuc.append({"ad": t["ad"], "kanisterler": kanisterler,
                      "tup": sum(k["tup"] for k in kanisterler),
                      "excel": sum(k["excel"] for k in kanisterler),
                      "bos_yuva": sum(k["bos_yuva"] for k in kanisterler)})
    return {"tanklar": sonuc, "yersiz_tup": yersiz_tup, "yersiz_excel": yersiz_excel}


def tup_ayrintilari(idler) -> dict:
    """Gobletteki tüplerin ayrıntısı: hasta, içerik, sayı -> {tüp id: satır}.

    Goblet ekranı (`/cryo/yer`), yeri belirsizler ve Excel haritası
    (`harita_excel.py`, v6.191) aynı satırları basıyor -- tek sorgu. Hasta
    embriyo tüpünde örneğin tedavisinden, sperm tüpünde dondurma kaydından.
    `parantez` resmî formların tüp yazımı (`formlar.tup_metni()`: "(3AA-4AB)",
    yumurtada "(5*MII)"), `gun` "D5" (birden çok günse "D3/D5")."""
    if not idler:
        return {}
    sonuc = {}
    idler = list(idler)
    icerik = formlar.tup_icerikleri(idler)
    hasta = ("(SELECT h.{a} FROM olay o JOIN specimen s ON s.id=o.specimen_id "
             "JOIN cycle c ON c.id=s.cycle_id JOIN hasta h ON h.id=c.hasta_id "
             "WHERE o.vit_tasiyici_id=t.id AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
             "ORDER BY o.id LIMIT 1)")
    sperm = ("(SELECT h.{a} FROM sperm_dondurma sd JOIN hasta h ON h.id=sd.hasta_id "
             "WHERE sd.tasiyici_id=t.id AND sd.iptal_mi=0 LIMIT 1)")
    for i in range(0, len(idler), 500):
        parca = idler[i:i + 500]
        yer = ",".join("?" * len(parca))
        for r in db.sorgu(
                "SELECT t.id, t.etiket, t.tip, t.renk, t.kategori, t.vitrifikasyon_zamani, "
                "  (SELECT COUNT(*) FROM olay o WHERE o.vit_tasiyici_id=t.id "
                "   AND o.tip='vitrifikasyon' AND o.iptal_mi=0) AS adet, "
                f"  COALESCE({hasta.format(a='dosya_no')}, {sperm.format(a='dosya_no')}) AS dosya_no, "
                f"  COALESCE({hasta.format(a='ad_soyad')}, {sperm.format(a='ad_soyad')}) AS ad_soyad, "
                f"  COALESCE({hasta.format(a='es_adi')}, {sperm.format(a='es_adi')}) AS es_adi, "
                "  (SELECT sd.id FROM sperm_dondurma sd WHERE sd.tasiyici_id=t.id "
                "   AND sd.iptal_mi=0 LIMIT 1) AS sperm_id, "
                "  (SELECT sd.sebep FROM sperm_dondurma sd WHERE sd.tasiyici_id=t.id "
                "   AND sd.iptal_mi=0 LIMIT 1) AS sperm_sebep "
                f"FROM tasiyici t WHERE t.id IN ({yer})", tuple(parca)):
            d = dict(r)
            ic = icerik.get(r["id"])
            d["yumurta"] = bool(ic and ic["yumurta"])
            d["parantez"] = formlar.tup_metni(ic) if ic else ""
            d["gun"] = "/".join(f"D{g}" for g in sorted(ic["gunler"])) if ic else ""
            sonuc[r["id"]] = d
    return sonuc


def excel_ayrintilari(idler) -> dict:
    """Excel kayıtlarının bütün alanları -> {id: satır}."""
    if not idler:
        return {}
    sonuc = {}
    idler = list(idler)
    for i in range(0, len(idler), 500):
        parca = idler[i:i + 500]
        yer = ",".join("?" * len(parca))
        for r in db.sorgu(f"SELECT * FROM excel_kaydi WHERE id IN ({yer})", tuple(parca)):
            sonuc[r["id"]] = dict(r)
    return sonuc


def kanister_gobletleri(harita, tank, kanister) -> dict:
    """Bir kanisterin gobletleri, Excel'deki sırasıyla (alt kat, üst kat),
    ve kanisterde olup hiçbir düzen gobletine düşmeyen tüp/Excel kaydı.

    -> {"alt": [goblet], "ust": [goblet], "yersiz_tup": [...],
        "yersiz_excel": [...]} -- kanister düzende yoksa None.
    """
    a = yer_anahtari(tank, kanister, "")[:2]
    gl = sorted((g for k, g in harita["gobletler"].items() if k[:2] == a),
                key=lambda g: (g["sira"] or 0, _dogal(g["goblet"])))
    if not gl:
        return None
    return {"alt": [g for g in gl if (g["sira"] or 0) < 1000],
            "ust": [g for g in gl if (g["sira"] or 0) >= 1000],
            "yersiz_tup": [x for x in harita["duzen_disi"]
                           if x["anahtar"] and x["anahtar"][:2] == a],
            "yersiz_excel": [x for x in harita["excel_disi"]
                             if x["anahtar"] and x["anahtar"][:2] == a]}


# ------------------------------------------------ boş yer önerisi (v6.190)
#
# Kullanıcının kuralı (2026-09-25): "Bir hastanın birden fazla strawu varsa
# renkleri farklı olsun. Mümkünse birbirine yakın olsun. Kondukları goblette
# aynı renklerin olmadığına dikkat edilsin." Excel'de de böyle: aynı günün
# straw'ları çoğunlukla aynı gobletde (2 straw'da 452'ye 36), dolunca yanındaki
# gobletde devam ediyor; bir gobletin straw'ları renkle ayırt ediliyor.
#
# Öneri bir SIRA, karar değil: ilk aday ekrandaki kutulara yazılıyor,
# embriyolog başkasını seçebilir ya da elle yazabilir. Kapasitesi bilinmeyen
# yer (eski "cane" yerleri, sperm yerleri) hiç önerilmez.

# Son bir yılın dondurmalarında bu paydan az görülen renk palete girmez:
# listede beyaz/kırmızı/mor/siyah da var ama laboratuvar 2022'den beri dört
# renk kullanıyor (Excel: mavi, sarı, turuncu, yeşil). Listenin tamamı
# kullanılsaydı üç straw'lı bir gobletin boş rengi "beyaz" önerilirdi.
PALET_EN_AZ_PAY = 0.05
PALET_GUN = 365
EN_COK_ONERI = 6


def renk_paleti(b=None) -> list:
    """Laboratuvarın bugün kullandığı straw renkleri, renk listesinin
    sırasıyla (yönetici listeden sıralıyor). Veriden: son bir yılın embriyo/
    yumurta tüplerinde payı %5'ten çok olan renkler. Hiç renkli tüp yoksa
    boş -- renk önerilmez, uydurulmaz."""
    kapat = b is None
    if b is None:
        b = db.baglan()
    try:
        sayim = {r[0]: r[1] for r in b.execute(
            "SELECT renk, COUNT(*) FROM tasiyici WHERE lab_id=? AND kategori='embriyo' "
            "AND renk IS NOT NULL AND vitrifikasyon_zamani >= date('now', ?) "
            "GROUP BY renk", (db.LAB_ID, f"-{PALET_GUN} days"))}
        toplam = sum(sayim.values())
        if not toplam:
            return []
        sira = [r[0] for r in b.execute(
            "SELECT kod FROM liste_degeri WHERE lab_id=? AND liste_adi='tasiyici_renk' "
            "AND aktif_mi=1 ORDER BY sira", (db.LAB_ID,))]
        return [k for k in sira if sayim.get(k, 0) / toplam >= PALET_EN_AZ_PAY]
    finally:
        if kapat:
            b.close()


def goblet_bul(harita, tank, kanister, goblet):
    """Yazılan yerin düzen gobleti (anahtarla), yoksa None."""
    if not (tank or kanister or goblet):
        return None
    return harita["gobletler"].get(yer_anahtari(tank, kanister, goblet))


def gobletin_renkleri(g) -> list:
    """Gobletteki straw'ların renkleri (tüpler + Excel kayıtları); rengi
    yazılmamış straw sayılmıyor."""
    return [x["renk"] for x in g["tupler"] + g["excel"] if x["renk"]]


def yer_uyarilari(harita, tank, kanister, goblet, renk) -> list:
    """Dondurmadan önce seçilen yerin sorunları: [(kod, parametreler)].

    Kodlar: `duzende_yok` (yazılan goblet tank düzeninde yok -- yazım hatası
    ya da yeni bir yer), `kapasite_yok` (kaç straw aldığı bilinmiyor),
    `dolu` (boş yuva yok), `renk_var` (bu renkte straw zaten gobletde).
    Uyarı engel değil: ekran ve sunucu "yine de kaydet" onayı istiyor.
    """
    if not (tank or kanister or goblet):
        return []
    g = goblet_bul(harita, tank, kanister, goblet)
    if g is None:
        return [("duzende_yok", {})]
    uyari = []
    if not g["kapasite"]:
        uyari.append(("kapasite_yok", {}))
    elif g["dolu"] >= g["kapasite"]:
        uyari.append(("dolu", {"dolu": g["dolu"], "kapasite": g["kapasite"]}))
    if renk and renk in gobletin_renkleri(g):
        uyari.append(("renk_var", {"renk": renk}))
    return uyari


def _duzen_sirasi(g):
    return (_dogal(g["tank"]), _dogal(g["kanister"]), g["sira"] or 0)


def oneriler(harita, hasta_tupleri, gun, palet) -> dict:
    """Bu hastanın sıradaki straw'ı için boş yer adayları, en iyisi önce.

    `hasta_tupleri`: hastanın dolu embriyo/yumurta tüpleri [{id, gun}].
    -> {"bugun": hastanın bugün dondurulmuş straw'ı var mı (varsa sıradaki
        onun gobletine ya da yanına; "kaç straw" sorusu anlamsız), "listeler":
        {kaç straw: [aday, ...]}}

    Sıra: (1) bu hastanın BUGÜNKÜ straw'ının gobleti, (2) başka straw'larının
    gobleti, (3) aynı kanisterde onlara en yakın goblet, (4) geri kalanlar --
    bugün kaç straw dondurulacağına göre "en iyi sığan": o kadar boş yuvası
    olan gobletlerin en azı dolu olanı (boş gobletleri çok straw'lı hastaya
    saklar), eşitse düzen sırası. Renk: gobletteki renkler dışında kalan
    palet rengi, hastanın bugünkü straw'larının renkleri sona.
    """
    tup_goblet = {}
    for g in harita["gobletler"].values():
        for t in g["tupler"]:
            tup_goblet[t["id"]] = g
    bugunku = [t for t in hasta_tupleri if t["gun"] == gun and t["id"] in tup_goblet]
    bugun_g = {id(tup_goblet[t["id"]]) for t in bugunku}
    hasta_g = {id(tup_goblet[t["id"]]) for t in hasta_tupleri if t["id"] in tup_goblet}
    bugun_renk = {r["renk"] for g in harita["gobletler"].values() for r in g["tupler"]
                  if r["id"] in {t["id"] for t in bugunku} and r["renk"]}
    yakinlar = {}                                   # (tank, kanister) -> [sira]
    for g in harita["gobletler"].values():
        if id(g) in hasta_g:
            yakinlar.setdefault(yer_anahtari(g["tank"], g["kanister"], "")[:2],
                                []).append(g["sira"] or 0)
    adaylar = []
    for g in harita["gobletler"].values():
        if g["kategori"] != "embriyo" or not g["kapasite"]:
            continue
        bos = bos_yuva(g)
        if bos < 1:
            continue
        kullanilan = set(gobletin_renkleri(g))
        serbest = [r for r in palet if r not in kullanilan]
        if palet and not serbest:
            continue                    # renkleri dolu: aynı renk ikinci kez girerdi
        serbest.sort(key=lambda r: r in bugun_renk)
        yer = yer_anahtari(g["tank"], g["kanister"], "")[:2]
        if id(g) in bugun_g:
            grup, ince = 0, 0
        elif id(g) in hasta_g:
            grup, ince = 1, 0
        elif yer in yakinlar:
            grup, ince = 2, min(abs((g["sira"] or 0) - s) for s in yakinlar[yer])
        else:
            grup, ince = 3, 0
        # Rengi yazılmamış straw: önerilen renk onunla çakışabilir -- ekranda
        # söyleniyor, eşitlikte bu goblet sona.
        renksiz = sum(1 for x in g["tupler"] + g["excel"] if not x["renk"])
        adaylar.append({"g": g, "bos": bos, "renkler": sorted(kullanilan),
                        "renk": serbest[0] if serbest else None, "grup": grup,
                        "ince": ince, "renksiz": renksiz})
    sebep = {0: "bugun", 1: "hasta", 2: "yakin", 3: "yer"}
    listeler = {}
    for kac in (1, 2, 3, 4):
        def anahtar(a):
            sigar = a["bos"] >= kac
            return (a["grup"], a["ince"], 0 if sigar else 1,
                    a["bos"] if sigar else -a["bos"], a["renksiz"] > 0,
                    _duzen_sirasi(a["g"]))
        secilen = sorted(adaylar, key=anahtar)[:EN_COK_ONERI]
        listeler[kac] = [{
            "tank": a["g"]["tank"], "kanister": a["g"]["kanister"],
            "goblet": a["g"]["goblet"], "kapasite": a["g"]["kapasite"],
            "bos": a["bos"], "renkler": a["renkler"], "renk": a["renk"],
            "renksiz": a["renksiz"], "sebep": sebep[a["grup"]]} for a in secilen]
    return {"bugun": bool(bugunku), "listeler": listeler}
