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
