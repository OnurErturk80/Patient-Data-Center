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
        kolonlar = {r[1] for r in b.execute("PRAGMA table_info(konum)")}
        if "sira" not in kolonlar:
            return sonuc
        # Yedek goblet (v6.192, goc_053): göç yoksa hiçbiri yedek değil.
        yedek = "yedek" if "yedek" in kolonlar else "NULL AS yedek"
        anahtar_of = {}
        for r in b.execute("SELECT id, seviye1, seviye2, seviye3, kapasite, kategori, "
                           f"sira, tam_yol, {yedek} FROM konum WHERE lab_id=?", (db.LAB_ID,)):
            a = konum_anahtari(r)
            anahtar_of[r["id"]] = a
            if r["sira"] is not None:
                sonuc["gobletler"][a] = {
                    "konum_id": r["id"], "tank": r["seviye1"], "kanister": r["seviye2"],
                    "goblet": r["seviye3"], "tam_yol": r["tam_yol"],
                    "kapasite": r["kapasite"], "kategori": r["kategori"],
                    "sira": r["sira"], "yedek": bool(r["yedek"]),
                    "tupler": [], "excel": [], "dolu": 0}
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
            ust = [g for g in gl if (g["sira"] or 0) >= 1000]
            kanisterler.append({
                "ad": t["kanisterler"][ka]["ad"], "goblet": len(gl), "duzenli": len(duzenli),
                "kapasite": sum(g["kapasite"] for g in duzenli),
                "bos_yuva": sum(bos_yuva(g) for g in duzenli),
                "tup": sum(len(g["tupler"]) for g in gl),
                "excel": sum(len(g["excel"]) for g in gl),
                "yersiz": yersiz[(ta, ka)],
                "ust_kat": bool(ust),
                # Üst katın bütün gobletleri yedek (v6.192): "yer biterse".
                "ust_yedek": bool(ust) and all(g.get("yedek") for g in ust)})
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
            d["pgt"] = []
            sonuc[r["id"]] = d
    # PGT (v6.225): tüpteki biyopsili embriyolar, PGT numarasıyla
    # (`db.tup_pgt()`: örneğin en son biyopsisi) -- goblet satırı, hasta
    # kartı ve taşıma ekranı "PGT 2 · sonuç bekleniyor" basıyor.
    for tid, liste in db.tup_pgt(idler).items():
        if tid in sonuc:
            sonuc[tid]["pgt"] = liste
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


def excel_kaydini_bagla(b, e, t, kid, simdi, ezilebilir=()) -> list:
    """Excel kaydını programdaki tüpe bağlar: tüp Excel kaydının gobletine
    geçer (konumu yazılır, eski konumu kayda saklanır), rengi/tipi boşsa
    Excel'inki yazılır, Excel kaydı 'baglandi' olur -- straw artık tüpün
    kendisiyle sayılıyor, iki kez değil.

    İki yol aynı yazımı kullanıyor (v6.207): Excel kaydının sayfasındaki
    "tüpe bağla" (`app.excel_kaydi_bagla`, v6.189) ve aktarımın sonunda
    kendiliğinden bağlama (`cryo_esle.excel_kayitlarini_bagla()`). Bağı çözen
    yol (`/bagi-coz`) `islem_notu`'na ("doldurulan: renk,tip=cryotop" --
    üzerine yazılan alanın eski değeriyle, v6.214) ve
    `onceki_konum_id`'ye güveniyor -- yazımı bir yerde değiştirirsen ikisi
    birlikte değişir.

    `b` yazma işleminin bağlantısı, `e` Excel kaydı satırı, `t` tüp satırı
    (`tam_yol` ile). Denetim (tüp dolu mu, türü tutuyor mu) çağıranın işi.
    `ezilebilir`: dolu olsa da Excel'inkiyle değişecek alanlar -- aktarımın
    açtığı tüpün tipi ("cryotop" varsayılan, kaynakta yok; Excel'in VİAL'i
    gerçeği söylüyor, `uygula` da öyle yazıyor). Bağ çözülünce doldurulan
    alanlar boşalıyor. -> doldurulan alanlar.
    """
    def logla(tablo, kayit, alan, eski, yeni):
        b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                  "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                  (db.LAB_ID, tablo, str(kayit), alan, eski, yeni, kid, simdi))

    if e["konum_id"] and e["konum_id"] != t["konum_id"]:
        yeni_yol = b.execute("SELECT tam_yol FROM konum WHERE id=?",
                             (e["konum_id"],)).fetchone()[0]
        b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?", (e["konum_id"], t["id"]))
        logla("tasiyici", t["id"], "konum", t["tam_yol"], yeni_yol)
    doldurulan, notu = [], []
    for alan in ("renk", "tip"):
        if e[alan] and (not t[alan] or (alan in ezilebilir and t[alan] != e[alan])):
            b.execute(f"UPDATE tasiyici SET {alan}=? WHERE id=?", (e[alan], t["id"]))
            logla("tasiyici", t["id"], alan, t[alan], e[alan])
            doldurulan.append(alan)
            # Üzerine yazılan değer notta ("tip=cryotop", v6.214): bağ
            # çözülünce o geri konuyor. `tip` boş olamaz (NOT NULL) --
            # boşaltmaya çalışan geri alma patlıyordu.
            notu.append(f"{alan}={t[alan]}" if t[alan] else alan)
    # Hangi alanın bağlarken doldurulduğu `islem_notu`nda (bağlı kayıtta
    # başka bir not yok): bağ çözülünce yalnızca onlar geri alınıyor.
    b.execute("UPDATE excel_kaydi SET durum='baglandi', tasiyici_id=?, "
              "onceki_konum_id=?, islem_zamani=?, islem_notu=?, islem_kullanici_id=? "
              "WHERE id=?",
              (t["id"], t["konum_id"], simdi[:10],
               ("doldurulan: " + ",".join(notu)) if notu else None,
               kid, e["id"]))
    logla("excel_kaydi", e["id"], "durum", "tankta", f"baglandi: {t['etiket']}")
    return doldurulan


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
# Önerinin uzunluğu (v6.202, kullanıcı: "boş yer önerisi sabit,
# değiştirilebilsin ... tank belirterek de öneri versin. Hem otomatik öneri
# versin hem de ben sorgulayabileyim"). Ekran her listede EN_COK_ONERI satır
# gösteriyor, gerisi "daha fazla göster"in arkasında. Otomatik öneride 12
# aday; tank / kanister sorgusunda o yerin bütün adayları (bugünkü düzende
# bir kanisterin kapasitesi bilinen gobleti en çok 60).
OTOMATIK_EN_COK = 12
SORGU_EN_COK = 60


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


def _aday(g, palet):
    """Goblet önerilebilir mi -> (boş yuva, gobletteki renkler, serbest palet
    renkleri) ya da None. Embriyo gobleti, kapasitesi biliniyor, boş yuvası
    var ve paletin en az bir rengi gobletde yok (yoksa aynı renk ikinci kez
    girerdi). `oneriler()` ile sorgunun sayıları (`oneri_yerleri()`) aynı
    ölçüyü kullansın diye tek yerde."""
    if g["kategori"] != "embriyo" or not g["kapasite"]:
        return None
    bos = bos_yuva(g)
    if bos < 1:
        return None
    kullanilan = set(gobletin_renkleri(g))
    serbest = [r for r in palet if r not in kullanilan]
    if palet and not serbest:
        return None
    return bos, kullanilan, serbest


def _yer_suzgeci(tank, kanister):
    """Sorgunun yeri -> gobletin `yer_anahtari()` önekiyle karşılaştırılacak
    anahtar; tank yoksa None (bütün tanklar). Kanister tanksız anlamsız."""
    if not tank:
        return None
    a = yer_anahtari(tank, kanister or "", "")
    return a[:2] if kanister else a[:1]


def oneri_yerleri(harita, palet) -> list:
    """Öneri sorgusunun seçicisi (v6.202): embriyo gobleti olan tanklar ve
    kanisterleri, önerilebilir boş yuva sayısıyla -- `oneriler()`'in
    adaylarıyla aynı ölçü (`_aday()`); yedek gobletlerin yuvası ayrı sayılıyor
    (`yedek_bos`), olağan yer biterse diye hazırlandılar.

    -> [{"tank", "bos", "yedek_bos", "kanisterler": [{"kanister", "bos",
        "yedek_bos"}]}], düzen sırasıyla. Adlar Excel'in yazımı (seçicinin
    değeri de o; sunucu anahtarla karşılaştırıyor)."""
    tanklar = {}
    for g in sorted(harita["gobletler"].values(), key=_duzen_sirasi):
        if g["kategori"] != "embriyo" or not g["kapasite"]:
            continue
        a = yer_anahtari(g["tank"], g["kanister"], "")
        t = tanklar.setdefault(a[0], {"tank": g["tank"], "bos": 0, "yedek_bos": 0,
                                      "kanisterler": {}})
        k = t["kanisterler"].setdefault(a[1], {"kanister": g["kanister"] or "",
                                               "bos": 0, "yedek_bos": 0})
        aday = _aday(g, palet)
        if aday:
            alan = "yedek_bos" if g.get("yedek") else "bos"
            t[alan] += aday[0]
            k[alan] += aday[0]
    return [{**t, "kanisterler": list(t["kanisterler"].values())}
            for t in tanklar.values()]


def oneriler(harita, hasta_tupleri, gun, palet, tank="", kanister="",
             en_cok=EN_COK_ONERI) -> dict:
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

    Yedek goblet (v6.192, `konum.yedek`; kullanıcı: "yer biterse diye
    hazırlandı, ihtiyaç olursa oralara da hasta konulacak"): hastanın kendi
    gobleti değilse (1)-(2) değil, yakınlık üstünlüğü de almıyor -- (4)'te,
    bugünkü straw'ları alabilen bütün olağan gobletlerden sonra, ama
    alamayanlardan ÖNCE: olağan yer hastanın straw'larını alamadığında bir
    hastanın straw'ları dağılmasın.

    Tank / kanister (v6.202, embriyoloğun sorgusu): adaylar yalnızca o yerin
    gobletleri, sıra aynı kural -- hastanın o yerdeki straw'ları yine önce.
    Boşsa bütün tanklar (otomatik öneri). `en_cok`: liste başına aday.
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
    suzgec = _yer_suzgeci(tank, kanister)
    adaylar = []
    for g in harita["gobletler"].values():
        aday = _aday(g, palet)
        if aday is None:
            continue
        if suzgec and yer_anahtari(g["tank"], g["kanister"], "")[:len(suzgec)] != suzgec:
            continue
        bos, kullanilan, serbest = aday
        serbest.sort(key=lambda r: r in bugun_renk)
        yer = yer_anahtari(g["tank"], g["kanister"], "")[:2]
        yedek = bool(g.get("yedek"))
        if id(g) in bugun_g:
            grup, ince = 0, 0
        elif id(g) in hasta_g:
            grup, ince = 1, 0
        elif yer in yakinlar and not yedek:
            grup, ince = 2, min(abs((g["sira"] or 0) - s) for s in yakinlar[yer])
        else:
            grup, ince = 3, 0
        # Rengi yazılmamış straw: önerilen renk onunla çakışabilir -- ekranda
        # söyleniyor, eşitlikte bu goblet sona.
        renksiz = sum(1 for x in g["tupler"] + g["excel"] if not x["renk"])
        adaylar.append({"g": g, "bos": bos, "renkler": sorted(kullanilan),
                        "renk": serbest[0] if serbest else None, "grup": grup,
                        "ince": ince, "renksiz": renksiz, "yedek": yedek})
    sebep = {0: "bugun", 1: "hasta", 2: "yakin", 3: "yer"}
    listeler = {}
    for kac in (1, 2, 3, 4):
        def anahtar(a):
            sigar = a["bos"] >= kac
            # Sığan olağan < sığan yedek < sığmayan olağan < sığmayan yedek.
            sinif = (0 if sigar else 2) + (1 if a["yedek"] and a["grup"] >= 2 else 0)
            return (a["grup"], a["ince"], sinif,
                    a["bos"] if sigar else -a["bos"], a["renksiz"] > 0,
                    _duzen_sirasi(a["g"]))
        secilen = sorted(adaylar, key=anahtar)[:en_cok]
        listeler[kac] = [{
            "tank": a["g"]["tank"], "kanister": a["g"]["kanister"],
            "goblet": a["g"]["goblet"], "kapasite": a["g"]["kapasite"],
            "bos": a["bos"], "renkler": a["renkler"], "renk": a["renk"],
            "renksiz": a["renksiz"], "sebep": sebep[a["grup"]],
            "yedek": a["yedek"]} for a in secilen]
    return {"bugun": bool(bugunku), "listeler": listeler,
            "tank": tank if suzgec else "", "kanister": kanister if suzgec else ""}
