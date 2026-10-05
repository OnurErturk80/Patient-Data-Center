"""Laboratuvarın kendi Cryo Haritası Excel'i, programın bugünkü haliyle (v6.199).

Kullanıcının isteği (2026-09-26): "Tankları Excel'e aktar dediğimde benim
kullandığım orjinal cryo haritaya çıktı alsam. Farklı yapıda excel oluşturma
benim orjinal cryo harita excelimi birebir kullan."

Program laboratuvarın dosyasını bir kez alıyor (Cryo Haritası'nın kartı,
yönetici; `yukle()`), `lab.db`'de saklıyor (goc_054) ve her çıktıda o dosyayı
dolduruyor. Dosyanın kendisine -- sayfalar, Excel tabloları, sütun
genişlikleri, biçimler, başlıklar, NO sütunu -- dokunulmuyor; yalnızca straw
satırlarının değer hücrelerine (SOYAD, AD, EŞİ, TARİH, HÜCRE, VİAL, NOTLAR):

- **Straw hâlâ o gobletteyse satır aynen kalır**, laboratuvarın yazdığı gibi.
  Tek istisna (v6.230): Excel kaydı bir tedavinin tüpüne bağlanmış, içeriği
  tüpünkünden farklı -- HÜCRE tedavinin kaydına göre yazılır
  (`_tedaviye_gore()`).
  Hangi satırın hangi straw olduğu `cryo_esle.py`'nin eşleştirmesiyle (hasta +
  gün + içerik), sperm satırında ad + günle, Excel kayıtlarında içerik
  anahtarıyla bulunuyor -- `cryo_esle.yerlesim_plani()`'nin "temsil" ölçüsü:
  tüp tankta (`durum='dolu'`) ve konumu bu goblet.
- **Straw artık orada değilse** (çözüldü, başka merkeze taşındı, başka yere
  kondu, Excel kaydı "tanktan çıkarıldı") satırın değerleri silinir, NO ve
  hücre biçimi kalır.
- **Programda bu goblete konmuş straw** gobletin boş satırına yazılır: önce
  Excel'de zaten boş olan satırlar, sonra boşalanlar (yazılı straw'lar yer
  değiştirmesin). Başka bir gobletten taşınmışsa eski satırının yazısı
  taşınır; programda dondurulmuşsa laboratuvarın yazımıyla kurulur
  (`_yeni_satirlar()`).
- Yer bulamayan straw (goblet dolu, gobleti dosyada yok) yazılmaz; sayısı ve
  listesi Cryo Haritası'nın kartında (`ozet`). Konumu girilmemiş ya da tank
  düzeninde olmayan tüpler laboratuvarın dosyasında da yoktu, yine yok.

Dosya XML düzeyinde değiştiriliyor (kütüphanesiz, `excel.py`/`xlsx_oku.py`
gibi). Paylaşılan metin tablosu (sharedStrings) baştan kuruluyor: boşalan
satırların adları dosyanın görünmeyen bir köşesinde de kalmasın.
"""

import collections
import datetime as _dt
import hashlib
import html
import io
import re
import threading
import xml.etree.ElementTree as _ET
import zipfile

import cryo_esle
import cryo_excel
import db
import yerlesim

EN_BUYUK_DOSYA = 20 * 1024 * 1024
EN_BUYUK_ACIK = 200 * 1024 * 1024        # açılmış parçaların toplamı (zip bombası)
EN_COK_PARCA = 2000

# Straw satırında yazılan alanlar (`cryo_excel._BASLIKLAR`'ın adları). NO yok:
# gobletin adı, satırın değil.
ALANLAR = ("soyad", "ad", "es", "tarih", "icerik", "vial", "notlar")

_KILIT = threading.Lock()
_ONBELLEK = {}                            # şablonun imzası -> çözümlenmiş hali

_SATIR = re.compile(r"<row\b([^>]*?)(?:/>|>(.*?)</row>)", re.S)
_HUCRE = re.compile(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", re.S)
_OZNITELIK = re.compile(r'([\w:]+)="([^"]*)"')
_METIN_HUCRESI = re.compile(r'(<c\b[^>]*\bt="s"[^>]*>\s*<v>)(\d+)(</v>)')
_ISO_GUN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
# Tarih biçimleri: Excel'in yerleşik numaraları.
_TARIH_BICIMLERI = set(range(14, 23)) | {45, 46, 47}


class Hata(Exception):
    """Dosya kullanılamıyor; mesajı ekranda gösterilecek kadar açık."""


# ------------------------------------------------------------ saklama

def tablo_var() -> bool:
    """goc_054 çalıştı mı (tuzak #3). Cevap `db.tablo_var()`'da saklı,
    geri yüklemeden sonra unutuluyor (tuzak #15)."""
    return db.tablo_var("cryo_sablon")


def bilgi():
    """Kart için yüklü şablon: ad, boyut, zaman, yükleyen -- içerik değil."""
    if not tablo_var():
        return None
    r = db.tek("SELECT s.id, s.dosya_adi, s.boyut, s.imza, s.yukleme_zamani, "
               "  k.ad_soyad AS yukleyen FROM cryo_sablon s "
               "LEFT JOIN kullanici k ON k.id = s.kullanici_id "
               "WHERE s.lab_id = ? ORDER BY s.id DESC LIMIT 1", (db.LAB_ID,))
    return dict(r) if r else None


def _sablon():
    """-> (baytlar, imza) ya da None."""
    if not tablo_var():
        return None
    r = db.tek("SELECT icerik, imza FROM cryo_sablon WHERE lab_id = ? "
               "ORDER BY id DESC LIMIT 1", (db.LAB_ID,))
    return (bytes(r["icerik"]), r["imza"]) if r else None


def var() -> bool:
    return bilgi() is not None


def yukle(dosya_adi: str, baytlar: bytes, kid) -> dict:
    """Laboratuvarın dosyasını denetler ve saklar (öncekinin yerine).

    Reddedilen: `.xlsx` olmayan, okunamayan, goblet tablosu bulunmayan ya da
    gobletlerinden hiçbiri programın tank düzeninde olmayan dosya (yanlış
    dosya). Kabul edilince bugünkü haliyle bir kez doldurulup denenir --
    yazılamayacak bir dosya saklanmasın. -> doldurmanın özeti.
    """
    if not tablo_var():
        raise Hata("Veritabanı güncellemesi (goc_054) henüz uygulanmamış. "
                   "Programı kapatıp yeniden açın.")
    if not (dosya_adi or "").lower().endswith(".xlsx"):
        raise Hata("Yalnızca .xlsx dosyası yüklenebilir. Excel'de "
                   "Farklı Kaydet → Excel Çalışma Kitabı (.xlsx).")
    if len(baytlar) > EN_BUYUK_DOSYA:
        raise Hata("Dosya çok büyük (en çok 20 MB).")
    imza = hashlib.sha256(baytlar).hexdigest()
    p = _cozumle(baytlar, imza)
    harita = yerlesim.doluluk()
    if not harita["gobletler"]:
        raise Hata("Programda tank düzeni kurulmamış: önce "
                   "'python3 cryo_esle.py yerlesim <dosya>' çalıştırılmalı.")
    ortak = sum(1 for g in p["duzen"]["gobletler"]
                if _goblet_anahtari(g) in harita["gobletler"])
    if not ortak:
        raise Hata("Dosyanın gobletlerinden hiçbiri programın tank düzeninde "
                   "yok -- laboratuvarın Cryo Haritası Excel'i mi?")
    plan = kur(baytlar, imza, harita=harita)
    yaz(baytlar, plan["duzenleme"], imza)          # yazılabiliyor mu
    simdi = _dt.datetime.now().isoformat(" ", "seconds")
    with db.yazma_islemi() as b:
        b.execute("DELETE FROM cryo_sablon WHERE lab_id = ?", (db.LAB_ID,))
        cur = b.execute(
            "INSERT INTO cryo_sablon (lab_id, dosya_adi, icerik, boyut, imza, "
            "kullanici_id, yukleme_zamani) VALUES (?,?,?,?,?,?,?)",
            (db.LAB_ID, dosya_adi, baytlar, len(baytlar), imza, kid, simdi))
        b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                  "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
                  (db.LAB_ID, "cryo_sablon", str(cur.lastrowid), "dosya", None,
                   f"{dosya_adi} ({len(baytlar)} bayt)", kid, simdi))
    return {**plan["ozet"], "goblet": len(p["duzen"]["gobletler"]), "ortak": ortak}


# ------------------------------------------------------------ dosyayı okuma

def _yol(hedef: str) -> str:
    """İlişki dosyasındaki hedef -> zip içindeki yol."""
    return hedef.lstrip("/") if hedef.startswith("/") else "xl/" + hedef


def _kitap(baytlar: bytes) -> dict:
    """Zip'in parçaları, sayfa adı -> parça, paylaşılan metinler, biçimler.

    Dışarıdan gelen dosya: `xlsx_oku.py`'nin korumaları burada da --
    parça/boyut sınırı, DOCTYPE/ENTITY taşıyan XML hiç açılmıyor."""
    try:
        z = zipfile.ZipFile(io.BytesIO(baytlar))
        bilgiler = z.infolist()
        if len(bilgiler) > EN_COK_PARCA or sum(i.file_size for i in bilgiler) > EN_BUYUK_ACIK:
            raise Hata("Dosya beklenenden çok büyük.")
        parcalar = [(i, z.read(i.filename)) for i in bilgiler]
    except (zipfile.BadZipFile, OSError, RuntimeError) as e:
        raise Hata(f"Dosya açılamadı: {e}") from None
    ham = {i.filename: v for i, v in parcalar}
    for ad, v in ham.items():
        if ad.endswith((".xml", ".rels")) and (b"<!DOCTYPE" in v or b"<!ENTITY" in v):
            raise Hata("Dosyada izin verilmeyen XML tanımı var.")
    try:
        wb = ham["xl/workbook.xml"].decode("utf-8")
        rels = ham["xl/_rels/workbook.xml.rels"].decode("utf-8")
        sst = ham["xl/sharedStrings.xml"].decode("utf-8")
        stiller = ham["xl/styles.xml"].decode("utf-8")
    except KeyError as e:
        raise Hata(f"Dosyada beklenen parça yok: {e.args[0]}") from None
    hedef = {}
    for m in re.finditer(r"<Relationship\b([^>]*)>", rels):
        at = dict(_OZNITELIK.findall(m.group(1)))
        hedef[at.get("Id")] = at.get("Target", "")
    sayfalar = {}
    for m in re.finditer(r"<sheet\b([^>]*)>", wb):
        at = dict(_OZNITELIK.findall(m.group(1)))
        yol = _yol(hedef.get(at.get("r:id"), ""))
        if yol in ham:
            sayfalar[html.unescape(at.get("name", ""))] = yol
    # Paylaşılan metinler: her <si> ham haliyle (zengin metin de) korunuyor.
    bas = re.search(r"<sst\b[^>]*>", sst)
    if not bas:
        raise Hata("Paylaşılan metin tablosu okunamadı.")
    si = re.findall(r"<si\b[^>]*?(?:/>|>.*?</si>)", sst[bas.end():], re.S)
    # Hücre biçimleri: hangisi tarih.
    xfs = re.search(r"<cellXfs\b[^>]*>(.*?)</cellXfs>", stiller, re.S)
    ozel = {int(n): k for n, k in re.findall(r'<numFmt\b[^>]*numFmtId="(\d+)"[^>]*'
                                              r'formatCode="([^"]*)"', stiller)}
    tarih_stil = set()
    for i, x in enumerate(re.findall(r"<xf\b[^>]*?(?:/>|>.*?</xf>)",
                                     xfs.group(1) if xfs else "", re.S)):
        n = re.search(r'numFmtId="(\d+)"', x)
        n = int(n.group(1)) if n else 0
        kod = re.sub(r'"[^"]*"|\[[^\]]*\]', "", html.unescape(ozel.get(n, ""))).lower()
        if n in _TARIH_BICIMLERI or (n in ozel and re.search(r"[dmy]", kod)):
            tarih_stil.add(i)
    return {"parcalar": parcalar, "ham": ham, "sayfalar": sayfalar,
            "sst_bas": bas.group(0), "sst_on": sst[:bas.start()], "si": si,
            "tarih_stil": tarih_stil}


def _sutun_no(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n


def _sutun_adi(n: int) -> str:
    ad = ""
    while n:
        n, k = divmod(n - 1, 26)
        ad = chr(65 + k) + ad
    return ad


def _hucre_stilleri(kitap) -> dict:
    """{parça: {"metin": {sütun: s}, "tarih": {sütun: s}}, "_tarih": s} -- yeni
    açılan hücreye verilecek biçim: o sütunda en sık görülen. TARİH'e hep bir
    tarih biçimi (yoksa gün sayısı "46290" diye görünürdü)."""
    sonuc, genel = {}, collections.Counter()
    for yol in kitap["sayfalar"].values():
        metin, tarih = collections.defaultdict(collections.Counter), \
            collections.defaultdict(collections.Counter)
        for m in _HUCRE.finditer(kitap["ham"][yol].decode("utf-8")):
            at = dict(_OZNITELIK.findall(m.group(1)))
            if "r" not in at or not m.group(2) or "<v>" not in m.group(2):
                continue
            s = int(at.get("s", 0))
            c = _sutun_no(at["r"])
            if at.get("t") == "s":
                metin[c][s] += 1
            elif "t" not in at and s in kitap["tarih_stil"]:
                tarih[c][s] += 1
                genel[s] += 1
        sonuc[yol] = {"metin": {c: n.most_common(1)[0][0] for c, n in metin.items()},
                      "tarih": {c: n.most_common(1)[0][0] for c, n in tarih.items()}}
    sonuc["_tarih"] = (genel.most_common(1)[0][0] if genel
                       else min(kitap["tarih_stil"]) if kitap["tarih_stil"] else None)
    return sonuc


def _goblet_anahtari(g) -> tuple:
    return yerlesim.yer_anahtari(g["tank"], g["kanister"], g["goblet"])


def _satir_anahtari(r) -> tuple:
    return yerlesim.yer_anahtari(r["tank"], r["kanister"], r["goblet"])


def _kimlik(r) -> tuple:
    return (r["sayfa"], r["satir"], r["sutun"])


def _cozumle(baytlar: bytes, imza: str) -> dict:
    """Şablonun programın anladığı hali -- imzasıyla bellekte (dosya nadiren
    değişiyor, her çıktıda yeniden okumak 2 sn)."""
    with _KILIT:
        p = _ONBELLEK.get(imza)
    if p:
        return p
    try:
        cozum = cryo_excel.coz(baytlar)
        duzen = cryo_excel.duzen(baytlar)
    except cryo_excel.Hata as e:
        raise Hata(f"Excel okunamadı: {e}") from None
    kitap = _kitap(baytlar)
    eksik = {r["sayfa"] for g in duzen["gobletler"] for r in g["satirlar"]} - set(kitap["sayfalar"])
    if eksik:
        raise Hata("Sayfa bulunamadı: " + ", ".join(sorted(eksik)))
    # Excel kaydının anahtarı `cryo_esle.yerlesim_plani()`'ndeki sırayla:
    # gobletlerin dolu satırları, sonra gobletsizler (aynı içerikteki kaçıncı
    # satır olduğu anahtarın parçası).
    dolu = [r for g in duzen["gobletler"] for r in g["satirlar"] if r["dolu"]]
    dolu += list(duzen["gobletsiz"])
    # Hastanın Excel'deki yazımı (kullanıcının kararı, 2026-09-26): yeni
    # straw'ının SOYAD/AD'ı, varsa önceki satırındaki gibi.
    yazim = {}
    for r in dolu:
        k = cryo_excel.kelimeler(f"{r['soyad']} {r['ad']}")
        gun = cryo_excel.tarih_coz(r["tarih_ham"])[0] or ""
        if k and (k not in yazim or gun >= yazim[k][2]):
            yazim[k] = (r["soyad"], r["ad"], gun)
    p = {"cozum": cozum, "duzen": duzen, "kitap": kitap,
         "stiller": _hucre_stilleri(kitap),
         "anahtar": cryo_esle._anahtarlar(dolu),
         "satirlar": {_kimlik(r): r for g in duzen["gobletler"] for r in g["satirlar"]}
         | {_kimlik(r): r for r in duzen["gobletsiz"]},
         "yazim": yazim}
    with _KILIT:
        _ONBELLEK.clear()
        _ONBELLEK[imza] = p
    return p


# ------------------------------------------------------------ eşleme

def _sperm_kayitlari(b, konum) -> tuple:
    """-> ({(ad kelimeleri, gün): [tüp id]}, {(goblet anahtarı, gün): [tüp
    id]}). Birincisi `cryo_esle._sperm_programda()`'nın ölçüsü (Excel'in sperm
    satırı hastanın adı + dondurma günüyle açıldı); ikincisi ad tutmadığında
    (v6.247): kart sonradan düzeltildi ya da birleştirildi -- aynı goblet aynı
    gün aynı straw (sperm yerinde tek vial).

    **Silinen kayıt da** (v6.247): satır programın bildiği bir straw'ı
    anlatıyor, kayıt silinince program o yeri boş gösteriyor -- Excel de
    göstermesin. v6.246'ya kadar silinen kayıt eşleşmede yoktu, satır "programın
    bilmediği" sayılıp aynen kalıyordu: harita boş, Excel dolu. Tüpler
    önce silinmemişler gelecek şekilde sıralı (`kur()`: önce yerindeki)."""
    adla, yerle = collections.defaultdict(list), collections.defaultdict(list)
    for r in b.execute(
            "SELECT t.id AS tid, t.konum_id, h.ad_soyad, date(sd.dondurma_zamani) AS gun "
            "FROM sperm_dondurma sd JOIN hasta h ON h.id = sd.hasta_id "
            "JOIN tasiyici t ON t.id = sd.tasiyici_id "
            "WHERE sd.lab_id = ? ORDER BY sd.iptal_mi, sd.id", (db.LAB_ID,)):
        adla[(cryo_excel.kelimeler(r["ad_soyad"]), r["gun"])].append(r["tid"])
        if r["konum_id"] in konum:
            yerle[(konum[r["konum_id"]], r["gun"])].append(r["tid"])
    return adla, yerle


def _konumsuz_sayfa(r) -> bool:
    """"Sayfa1" (v6.180): tankı yok, tüpleri konumsuz açıldı."""
    return bool(cryo_esle._KONUMSUZ_SAYFA.match(cryo_excel._n(r["tank"])))


def kur(baytlar=None, imza=None, harita=None) -> dict:
    """Şablonun bugünkü haliyle doldurulması: hangi hücreye ne yazılacak.

    -> {"duzenleme": {(sayfa, satır, sütun): değer}, "ozet": {...},
        "imza": ...} ya da şablon yoksa None. Değer: None (sil),
    ("s", metin), ("d", ISO gün). Hiçbir şey yazmaz.
    """
    if baytlar is None:
        s = _sablon()
        if not s:
            return None
        baytlar, imza = s
    p = _cozumle(baytlar, imza)
    if harita is None:
        harita = yerlesim.doluluk()
    with db.baglan() as b:
        idx, tup = cryo_esle.hastalar(b), cryo_esle.tupler(b)
        sonuc = cryo_esle.esle(p["cozum"]["satirlar"], idx, tup)
        tupler = {r["id"]: dict(r) for r in b.execute(
            "SELECT id, durum, konum_id, vitrifikasyon_zamani FROM tasiyici "
            "WHERE lab_id = ?", (db.LAB_ID,))}
        konum = {r["id"]: yerlesim.konum_anahtari(r) for r in b.execute(
            "SELECT id, seviye1, seviye2, seviye3, tam_yol FROM konum "
            "WHERE lab_id = ?", (db.LAB_ID,))}
        sperm, sperm_yeri = _sperm_kayitlari(b, konum)
        tup_hasta = {t["tid"]: hid for hid, liste in tup.items() for t in liste}
        excel = {}
        if yerlesim.excel_kaydi_var():
            excel = {r["anahtar"]: dict(r) for r in b.execute(
                "SELECT id, anahtar, durum, tasiyici_id FROM excel_kaydi "
                "WHERE lab_id = ?", (db.LAB_ID,))}

    def yerinde(tid, r) -> bool:
        """Tüp tankta ve bu satırın gobletinde (Sayfa1'de: konumsuz)."""
        t = tupler.get(tid)
        if not t or t["durum"] != "dolu":
            return False
        if _konumsuz_sayfa(r):
            return t["konum_id"] is None
        return konum.get(t["konum_id"]) == _satir_anahtari(r)

    temsil = {}          # satır kimliği -> ("t", tüp) | ("e", Excel kaydı)
    asil_satir = {}      # tüp -> onu anlatan şablon satırı (taşınırsa yazısı)
    atanan = set()
    # Programın bir kaydıyla (hangi durumda olursa olsun) eşleşen satırlar.
    # Hiçbiriyle eşleşmeyen satır -- dosya tank düzeni kurulduktan sonra
    # Excel'de elle değiştirilmiş -- boşaltılmaz, olduğu gibi kalır: program
    # hakkında hiçbir şey bilmediği bir straw'ı "gitti" sayamaz.
    bilinen = set()

    def ata(kim, sakin):
        if sakin not in atanan:
            temsil[kim] = sakin
            atanan.add(sakin)

    # 1) Embriyo/yumurta satırları: cryo_esle'nin eşleştirmesi.
    for s, k, t, _ek in sonuc:
        if not t or k == "cakisma":
            continue
        kim = _kimlik(s)
        bilinen.add(kim)
        asil_satir.setdefault(t["tid"], kim)
        if yerinde(t["tid"], s):
            ata(kim, ("t", t["tid"]))
    # 2) Sperm satırları: ad + gün, önce aynı yerdeki tüp. Silinen kayıt da
    #    sayılıyor (v6.247, `_sperm_kayitlari()`).
    kullanilan = set()
    for s in p["cozum"]["satirlar"]:
        if s["kategori"] != "sperm" or not s.get("tarih"):
            continue
        adaylar = [tid for tid in sperm.get((cryo_excel.kelimeler(f"{s['soyad']} {s['ad']}"),
                                             s["tarih"]), []) if tid not in kullanilan]
        tid = next((t for t in adaylar if yerinde(t, s)), None) or (adaylar[0] if adaylar else None)
        if tid is None:
            continue
        kullanilan.add(tid)
        kim = _kimlik(s)
        bilinen.add(kim)
        asil_satir.setdefault(tid, kim)
        if yerinde(tid, s):
            ata(kim, ("t", tid))
    # 3) Excel kayıtları: içerik anahtarıyla.
    bagli_satirlar = []
    for kim, anahtar in p["anahtar"].items():
        if kim in temsil:
            continue
        e = excel.get(anahtar)
        if not e:
            continue
        bilinen.add(kim)
        if e["durum"] == "tankta":
            ata(kim, ("e", e["id"]))
        elif e["durum"] == "baglandi" and e["tasiyici_id"]:
            asil_satir.setdefault(e["tasiyici_id"], kim)
            if yerinde(e["tasiyici_id"], p["satirlar"][kim]):
                ata(kim, ("t", e["tasiyici_id"]))
                bagli_satirlar.append((kim, e["tasiyici_id"]))
    # 4) Adı tutmayan sperm satırları (v6.247): aynı goblet + aynı gün, henüz
    #    hiçbir satıra gitmemiş tüp. Excel kaydı olan satır 3'te kaldı -- bu adım
    #    onu başka bir hastanın aynı gün aynı goblete konmuş tüpüne yapıştırmasın.
    for s in p["cozum"]["satirlar"]:
        if s["kategori"] != "sperm" or not s.get("tarih") or _konumsuz_sayfa(s):
            continue
        kim = _kimlik(s)
        if kim in bilinen:
            continue
        adaylar = [tid for tid in sperm_yeri.get((_satir_anahtari(s), s["tarih"]), [])
                   if tid not in kullanilan and ("t", tid) not in atanan]
        tid = next((t for t in adaylar if yerinde(t, s)), None) or (adaylar[0] if adaylar else None)
        if tid is None:
            continue
        kullanilan.add(tid)
        bilinen.add(kim)
        asil_satir.setdefault(tid, kim)
        if yerinde(tid, s):
            ata(kim, ("t", tid))
    duzeltilecek = _tedaviye_gore(bagli_satirlar, temsil, tup, p)

    duzenleme = {}
    ozet = collections.Counter()
    sigmayan = []

    def bosalt(r):
        for alan in ALANLAR:
            c = r["alanlar"].get(alan)
            if c:
                duzenleme[(r["sayfa"], r["satir"], c)] = None

    yazilacak = []       # (satır, sakin)
    sablondaki = set()
    for g in p["duzen"]["gobletler"]:
        a = _goblet_anahtari(g)
        sablondaki.add(a)
        pg = harita["gobletler"].get(a)
        bos, bosalan = [], []
        for r in g["satirlar"]:
            if not r["dolu"]:
                bos.append(r)
            elif _kimlik(r) in temsil:
                ozet["korunan"] += 1
            elif _kimlik(r) not in bilinen:
                ozet["bilinmeyen"] += 1
            else:
                bosalan.append(r)
                bosalt(r)
                ozet["bosalan"] += 1
        if pg is None:
            continue
        sakinler = ([("e", e["id"]) for e in pg["excel"]] +
                    sorted((("t", t["id"]) for t in pg["tupler"]),
                           key=lambda x: (tupler.get(x[1], {}).get("vitrifikasyon_zamani") or "", x[1])))
        yeniler = [x for x in sakinler if x not in atanan]
        yeniler = _birlikte_yazilanlar(yeniler, g, temsil, tupler, tup_hasta)
        serbest = bos + bosalan
        for sakin, r in zip(yeniler, serbest):
            yazilacak.append((r, sakin))
        for sakin in yeniler[len(serbest):]:
            sigmayan.append((sakin, g))
    # Programın düzeninde olup dosyada olmayan gobletlerin straw'ları.
    for a, pg in harita["gobletler"].items():
        if a in sablondaki:
            continue
        for x in [("e", e["id"]) for e in pg["excel"]] + [("t", t["id"]) for t in pg["tupler"]]:
            if x not in atanan:
                sigmayan.append((x, pg))
    # Gobletsiz satırlar (NO boş): yalnızca korunur ya da boşalır.
    for r in p["duzen"]["gobletsiz"]:
        if _kimlik(r) in temsil:
            ozet["korunan"] += 1
        elif _kimlik(r) not in bilinen:
            ozet["bilinmeyen"] += 1
        else:
            bosalt(r)
            ozet["bosalan"] += 1

    # Tedaviye göre düzeltilen satırlar (v6.230): yalnızca HÜCRE, satırın geri
    # kalanı laboratuvarın yazdığı gibi.
    if duzeltilecek:
        yazilar = _program_satirlari(sorted(set(duzeltilecek.values())), p)
        for kim, tid in duzeltilecek.items():
            r = p["satirlar"][kim]
            c = r["alanlar"].get("icerik")
            hucre = (yazilar.get(("t", tid)) or {}).get("icerik")
            # Yazımda skoru bilinmeyen örnek ("?") varsa laboratuvarın yazısı kalır.
            if c and hucre and "?" not in hucre:
                duzenleme[(r["sayfa"], r["satir"], c)] = _deger("icerik", hucre)
                ozet["duzeltilen"] += 1
                ozet["korunan"] -= 1
    metinler = _yeni_satirlar([s for _r, s in yazilacak], asil_satir, p)
    for r, sakin in yazilacak:
        degerler = metinler.get(sakin)
        if not degerler:                  # yazısı kurulamadı: sessizce düşmesin
            sigmayan.append((sakin, r))
            continue
        for alan in ALANLAR:
            c = r["alanlar"].get(alan)
            if c:
                duzenleme[(r["sayfa"], r["satir"], c)] = _deger(alan, degerler.get(alan))
        ozet["yeni"] += 1
        if sakin[0] == "t" and sakin[1] in asil_satir:
            ozet["tasinan"] += 1
    ozet["sigmayan"] = len(sigmayan)
    ozet["yersiz"] = len(harita["duzen_disi"]) + len(harita["excel_disi"])
    ozet["konumsuz"] = harita["konumsuz"]
    ozet_d = dict(ozet)
    ozet_d["sigmayanlar"] = _sigmayan_listesi(sigmayan)
    ic = sorted((f"{k[0]}\x1f{k[1]}\x1f{k[2]}", repr(v)) for k, v in duzenleme.items())
    imza_ = hashlib.sha256((imza + repr(ic)).encode("utf-8")).hexdigest()
    return {"duzenleme": duzenleme, "ozet": ozet_d, "imza": imza_,
            "baytlar": baytlar, "sablon_imza": imza}


def _tedaviye_gore(bagli_satirlar, temsil, tup, p) -> dict:
    """Excel kaydı bir tüpe bağlanmış satırlardan HÜCRE'si tedavinin yazımıyla
    yazılacaklar -> {satır kimliği: tüp} (v6.230; kullanıcı, 2026-09-30:
    "Ben tedaviye göre cryo harita içeriğini değiştirmek istiyorum").

    Bağlamayı kullanıcı yaptı ("Tüpe bağla", "Haritadan yer tamamla") ya da
    program birebir içerikle: straw o tüp, tedavinin kaydı esas. Yalnızca
    içerik farklıysa (`cryo_esle._uyar()`; "8HG2" / "8G2" gibi yazım farkı
    aynı sayılır, satıra dokunulmaz) ve tüpün içeriği eksiksizse: skoru
    bilinmeyen örneği olan tüpte laboratuvarın yazısı daha çok şey söylüyor,
    kalıyor. Sperm tüpü `cryo_esle.tupler()`'de yok, satırı değişmez."""
    tup_tid = {t["tid"]: t for liste in tup.values() for t in liste}
    sonuc = {}
    for kim, tid in bagli_satirlar:
        t = tup_tid.get(tid)
        if temsil.get(kim) != ("t", tid) or not t or not t["skorlar"] \
                or any(x in ("?", "") for x in t["skorlar"]):
            continue
        ic = cryo_esle.excel_icerik(p["satirlar"][kim]["icerik"] or "")
        if ic and any(cryo_esle._uyar(x, t["skorlar"]) for x in ic):
            continue
        sonuc[kim] = tid
    return sonuc


def cikti(plan) -> bytes:
    """`kur()`'un planından dosyanın baytları."""
    return yaz(plan["baytlar"], plan["duzenleme"], plan["sablon_imza"])


# Son yüklemenin sonucu, ekranda bir kez gösterilmek için (bellekte; adrese
# yalnızca "gösterilecek sonuç var" işareti yazılıyor -- tuzak #9).
SON_YUKLEME = {}


def _birlikte_yazilanlar(yeniler, g, temsil, tupler, tup_hasta) -> list:
    """"2 CRYOLOCK" gibi birden çok straw'ı TEK satırda anlatan Excel satırı
    (v6.189'da 6 goblet böyleydi): aynı hastanın aynı gün dondurulmuş öteki
    tüpleri o satırda sayılıyor, ayrıca yazılmıyor. Satırın VİAL'indeki sayı
    kadar."""
    kalan = list(yeniler)
    for r in g["satirlar"]:
        sakin = temsil.get(_kimlik(r))
        if not r["dolu"] or not sakin or sakin[0] != "t":
            continue
        adet = cryo_excel.vial_coz(r["vial_metni"])[0] or 1
        hasta = tup_hasta.get(sakin[1])
        gun = (tupler.get(sakin[1], {}).get("vitrifikasyon_zamani") or "")[:10]
        if adet < 2 or hasta is None or not gun:
            continue
        for x in list(kalan):
            if adet < 2:
                break
            if (x[0] == "t" and tup_hasta.get(x[1]) == hasta and
                    (tupler.get(x[1], {}).get("vitrifikasyon_zamani") or "")[:10] == gun):
                kalan.remove(x)
                adet -= 1
    return kalan


def _sigmayan_listesi(sigmayan) -> list:
    """Kart için: yer bulamayan straw'lar -- tüp etiketi / Excel kaydı ve yeri."""
    tids = [x[1] for x, _g in sigmayan if x[0] == "t"]
    etiket = {}
    for i in range(0, len(tids), 500):
        parca = tids[i:i + 500]
        for r in db.sorgu(f"SELECT id, etiket FROM tasiyici WHERE id IN "
                          f"({','.join('?' * len(parca))})", tuple(parca)):
            etiket[r["id"]] = r["etiket"]
    return [{"tur": x[0], "id": x[1], "etiket": etiket.get(x[1]) if x[0] == "t" else None,
             "yer": " / ".join(str(v) for v in (g.get("tank"), g.get("kanister"), g.get("goblet")) if v)}
            for x, g in sigmayan]


def _deger(alan, v):
    if v is None or str(v).strip() == "":
        return None
    v = str(v).strip()
    if alan == "tarih" and _ISO_GUN.match(v):
        return ("d", v[:10])
    return ("s", v)


# ------------------------------------------------------------ yeni satırın yazısı

def _buyuk(metin) -> str:
    """Türkçe büyük harf (`app.tr_buyuk()`'ün aynısı; app burada import
    edilemiyor)."""
    return (metin or "").replace("i", "İ").upper()


def _ad_bol(ad_soyad, p) -> tuple:
    """Programın tek alanı -> (SOYAD, AD). Hastanın Excel'de satırı varsa
    oradaki yazım; yoksa son kelime soyad (kullanıcının kararı, 2026-09-26:
    programdaki adlar "AD SOYAD" sırasında)."""
    k = cryo_excel.kelimeler(ad_soyad or "")
    if k in p["yazim"]:
        return p["yazim"][k][:2]
    kelimeler = _buyuk(ad_soyad).split()
    if not kelimeler:
        return "", ""
    return kelimeler[-1], " ".join(kelimeler[:-1])


def _yumurta_parantezi(parantez: str) -> str:
    """Resmî formun yazımı -> laboratuvarın Excel'i: "(4*MII-1*MI)" ->
    "(4M2-1M1)" (Excel'deki "OOSİT (4M2-1M1)")."""
    m = re.sub(r"(\d+)\*MII\b", r"\1M2", parantez or "")
    m = re.sub(r"(\d+)\*MI\b", r"\1M1", m)
    return re.sub(r"(\d+)\*", r"\1", m)


def _sperm_hucresi(sebep) -> str:
    """Laboratuvarın sperm yazımı: "EJAKÜLAT", kanserde "EJAKÜLAT-CA"
    (v6.180'in okumasının tersi: "CA" -> Onkolojik), "TESE"/"TESA"."""
    m = _buyuk(sebep)
    for yontem in ("TESE", "TESA", "MESA", "PESA"):
        if yontem in m:
            return yontem
    if "ONKOLOJ" in m or "KANSER" in m:
        return "EJAKÜLAT-CA"
    return "EJAKÜLAT"


def _yeni_satirlar(sakinler, asil_satir, p) -> dict:
    """Boş satıra yazılacak straw'ların yazısı -> {sakin: {alan: değer}}.

    - Excel kaydı: Excel'deki kendi yazısı (dosya değişmiş, satırı bulunamadı).
    - Başka gobletten taşınmış tüp: şablondaki eski satırının yazısı.
    - Programda dondurulmuş tüp: laboratuvarın son yıllardaki yazımıyla --
      HÜCRE "D5 (3BA-1BB)", yumurtada "OOSİT (4M2-1M1)", FET'te yeniden
      dondurulan "... REFREEZE"; VİAL "1 CRYOLOCKMAVİ 2" (sondaki sayı aynı
      dondurmanın kaçıncı straw'ı, tek straw'da yok); sperm "EJAKÜLAT" / "1".
    """
    sonuc = {}
    eids = [x[1] for x in sakinler if x[0] == "e"]
    if eids:
        for i, e in yerlesim.excel_ayrintilari(eids).items():
            sonuc[("e", i)] = {"soyad": e["soyad"], "ad": e["ad"], "es": e["es_adi"],
                               "tarih": e["tarih"] or e["tarih_ham"], "icerik": e["icerik"],
                               "vial": e["vial"], "notlar": e["notlar"]}
    yeni = []
    for x in sakinler:
        if x[0] != "t":
            continue
        kim = asil_satir.get(x[1])
        r = p["satirlar"].get(kim) if kim else None
        if r is None:
            r = next((s for s in p["cozum"]["satirlar"] if _kimlik(s) == kim), None) if kim else None
        if r is not None:
            tarih = cryo_excel.tarih_coz(r["tarih_ham"])[0] or r["tarih_ham"]
            sonuc[x] = {"soyad": r["soyad"], "ad": r["ad"], "es": r["es_adi"], "tarih": tarih,
                        "icerik": r["icerik"], "vial": r["vial_metni"], "notlar": r["notlar"]}
        else:
            yeni.append(x[1])
    if yeni:
        sonuc.update(_program_satirlari(yeni, p))
    return sonuc


def _program_satirlari(yeni, p) -> dict:
    """Programdaki tüplerin laboratuvar yazımıyla satırı -> {("t", tüp): {alan:
    değer}} (`_yeni_satirlar()`'ın yeni straw'ı; v6.230'dan beri tedaviye göre
    düzeltilen satırın HÜCRE'si de buradan)."""
    sonuc = {}
    ayrinti = yerlesim.tup_ayrintilari(yeni)
    etiket = {}
    for r in db.sorgu("SELECT liste_adi, kod, etiket FROM liste_degeri WHERE lab_id = ? "
                      "AND liste_adi IN ('tasiyici_tipi', 'tasiyici_renk')", (db.LAB_ID,)):
        etiket[(r["liste_adi"], r["kod"])] = r["etiket"]
    yer = ",".join("?" * len(yeni))
    tedavi = {r["tid"]: r["vc"] for r in db.sorgu(
        f"SELECT o.vit_tasiyici_id AS tid, MIN({db.vit_tedavisi('o')}) AS vc FROM olay o "
        f"WHERE o.tip = 'vitrifikasyon' AND o.iptal_mi = 0 AND o.vit_tasiyici_id IN ({yer}) "
        "GROUP BY o.vit_tasiyici_id", tuple(yeni))}
    # Straw'ın numarası: aynı tedavide AYNI GÜN dondurulanlar arasındaki sırası
    # (laboratuvarın Excel'i: iki ayrı günde straw'ı olan 78 hastanın 50'sinde
    # ikinci günün numarası 1'den başlıyor; kalanların ilk straw'ları çözülmüş
    # olabilir). Bugün tankta olmayanlar da sayılıyor: numara dondururken verildi.
    oturum, tipi = {}, {}
    for vc in set(tedavi.values()):
        for r in db.sorgu(
                "SELECT o.vit_tasiyici_id AS tid, MIN(t.vitrifikasyon_zamani) AS z FROM olay o "
                "JOIN tasiyici t ON t.id = o.vit_tasiyici_id WHERE o.tip = 'vitrifikasyon' "
                f"AND o.iptal_mi = 0 AND {db.vit_tedavisi('o')} = ? "
                "GROUP BY o.vit_tasiyici_id ORDER BY z, tid", (vc,)):
            oturum.setdefault((vc, (r["z"] or "")[:10]), []).append(r["tid"])
        c = db.tek("SELECT cycle_tipi FROM cycle WHERE id = ?", (vc,))
        tipi[vc] = c["cycle_tipi"] if c else None
    sperm = {r["tid"]: dict(r) for r in db.sorgu(
        "SELECT sd.tasiyici_id AS tid, sd.sebep, date(sd.dondurma_zamani) AS gun, "
        "  h.ad_soyad, h.es_adi, "
        "  EXISTS (SELECT 1 FROM cycle c WHERE c.hasta_id = h.id) AS cift "
        "FROM sperm_dondurma sd JOIN hasta h ON h.id = sd.hasta_id "
        f"WHERE sd.iptal_mi = 0 AND sd.tasiyici_id IN ({yer})", tuple(yeni))}
    for tid in yeni:
        x = ayrinti.get(tid)
        if not x:
            continue
        gun = (x["vitrifikasyon_zamani"] or "")[:10]
        if x["kategori"] == "sperm":
            sp = sperm.get(tid, {})
            # Çiftin kaydındaki sperm eşindir (`ad_soyad` kadın, `es_adi` erkek);
            # yalnızca sperm için açılmış kayıtta adı hastanın kendisi.
            if sp.get("cift") and sp.get("es_adi"):
                kisi, es = sp["es_adi"], sp["ad_soyad"]
            else:
                kisi, es = x["ad_soyad"], x["es_adi"]
            soyad, ad = _ad_bol(kisi, p)
            sonuc[("t", tid)] = {"soyad": soyad, "ad": ad, "es": es,
                                 "tarih": gun or sp.get("gun"),
                                 "icerik": _sperm_hucresi(sp.get("sebep")), "vial": "1"}
            continue
        soyad, ad = _ad_bol(x["ad_soyad"], p)
        if x["yumurta"]:
            hucre = f"OOSİT {_yumurta_parantezi(x['parantez'])}".strip()
        else:
            hucre = " ".join(v for v in (x["gun"], x["parantez"]) if v)
            if tipi.get(tedavi.get(tid)) in ("fet", "fet_kultur"):
                hucre = f"{hucre} REFREEZE".strip()
        tip = _buyuk(etiket.get(("tasiyici_tipi", x["tip"]), x["tip"] or ""))
        renk = _buyuk(etiket.get(("tasiyici_renk", x["renk"]), x["renk"] or ""))
        vial = f"1 {tip}{renk}".strip()
        sira = oturum.get((tedavi.get(tid), gun), [])
        if len(sira) > 1 and tid in sira:
            vial += f" {sira.index(tid) + 1}"
        sonuc[("t", tid)] = {"soyad": soyad, "ad": ad, "es": x["es_adi"], "tarih": gun,
                             "icerik": hucre, "vial": vial}
    return sonuc


# ------------------------------------------------------------ dosyayı yazma

def _xml_metni(v: str) -> str:
    v = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", v)
    return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _si_metni(si: str):
    """Düz bir <si>'nin metni (zengin metinse None) -- aynı metin ikinci kez
    eklenmesin diye."""
    m = re.fullmatch(r'<si>\s*<t(?: xml:space="preserve")?>(.*?)</t>\s*</si>', si, re.S)
    return html.unescape(m.group(1)) if m else None


def _gun_sayisi(iso: str) -> int:
    return (_dt.date.fromisoformat(iso) - _dt.date(1899, 12, 30)).days


def _satir_parcala(govde: str) -> list:
    """sheetData'nın satırları: [[satır no, öznitelikler, hücreler]]; hücre
    [sütun, ham XML]. Satırların dışında bir şey varsa (beklenmiyor) dosyaya
    dokunulmaz."""
    satirlar, son = [], 0
    for m in _SATIR.finditer(govde):
        if govde[son:m.start()].strip():
            raise Hata("Sayfanın satırları beklenen biçimde değil.")
        son = m.end()
        at = m.group(1)
        r = re.search(r'\br="(\d+)"', at)
        if not r:
            raise Hata("Numarası yazılmamış satır var.")
        hucreler, hs = [], 0
        ic = m.group(2) or ""
        for h in _HUCRE.finditer(ic):
            if ic[hs:h.start()].strip():
                raise Hata("Satırın hücreleri beklenen biçimde değil.")
            hs = h.end()
            ra = re.search(r'\br="([A-Z]+)\d+"', h.group(1))
            if not ra:
                raise Hata("Adressiz hücre var.")
            hucreler.append([_sutun_no(ra.group(1)), h.group(0)])
        if ic[hs:].strip():
            raise Hata("Satırın hücreleri beklenen biçimde değil.")
        satirlar.append([int(r.group(1)), at, hucreler, False, m.group(0)])
    if govde[son:].strip():
        raise Hata("Sayfanın satırları beklenen biçimde değil.")
    return satirlar


def _sayfa_duzenle(xml: str, duzen: dict, metin_no, stil: dict, tarih_stil: set,
                   genel_tarih) -> str:
    """Bir sayfanın XML'inde yalnızca verilen hücreleri değiştirir."""
    bas = re.search(r"<sheetData\b[^>]*>", xml)
    if not bas:
        raise Hata("Sayfada veri bölümü yok.")
    kapanis = xml.index("</sheetData>", bas.end())
    satirlar = _satir_parcala(xml[bas.end():kapanis])
    sira = {s[0]: s for s in satirlar}
    for (r, c), v in sorted(duzen.items()):
        satir = sira.get(r)
        if satir is None:
            if v is None:
                continue
            satir = [r, f' r="{r}"', [], True, ""]
            sira[r] = satir
            satirlar.append(satir)
            satirlar.sort(key=lambda s: s[0])
        hucreler = satir[2]
        i = next((j for j, h in enumerate(hucreler) if h[0] == c), None)
        eski = hucreler[i][1] if i is not None else None
        s = None
        if eski is not None:
            m = re.search(r'\bs="(\d+)"', eski.split(">", 1)[0])
            s = int(m.group(1)) if m else None
        ref = f"{_sutun_adi(c)}{r}"
        if v is None:
            if eski is None or ("<v>" not in eski and "<is>" not in eski):
                continue
            yeni = f'<c r="{ref}"' + (f' s="{s}"' if s else "") + "/>"
        elif v[0] == "d":
            if s not in tarih_stil:
                s = stil["tarih"].get(c, genel_tarih)
            if s is None:                      # dosyada hiç tarih biçimi yok
                v = ("s", ".".join(reversed(v[1].split("-"))))
            else:
                yeni = f'<c r="{ref}" s="{s}"><v>{_gun_sayisi(v[1])}</v></c>'
        if v is not None and v[0] == "s":
            if eski is None:
                s = stil["metin"].get(c)
            yeni = (f'<c r="{ref}"' + (f' s="{s}"' if s else "") +
                    f' t="s"><v>{metin_no(v[1])}</v></c>')
        if i is None:
            hucreler.append([c, yeni])
            hucreler.sort(key=lambda h: h[0])
        else:
            hucreler[i][1] = yeni
        satir[3] = True
    parca = []
    for no, at, hucreler, degisti, ham in satirlar:
        if not degisti:
            parca.append(ham)
            continue
        m = re.search(r'\bspans="(\d+):(\d+)"', at)
        if m and hucreler:
            a, b = int(m.group(1)), int(m.group(2))
            a2, b2 = min(a, hucreler[0][0]), max(b, hucreler[-1][0])
            if (a2, b2) != (a, b):
                at = at.replace(m.group(0), f'spans="{a2}:{b2}"')
        parca.append(f"<row{at}>" + "".join(h[1] for h in hucreler) + "</row>"
                     if hucreler else f"<row{at}/>")
    return xml[:bas.end()] + "".join(parca) + xml[kapanis:]


def yaz(baytlar: bytes, duzenleme: dict, imza: str = None) -> bytes:
    """Şablon + düzenlemeler -> yeni .xlsx baytları.

    Değişen yalnızca düzenlenen hücreler ve paylaşılan metin tablosu; öteki
    parçalar (tablolar, biçimler, yazıcı ayarları) bayt bayt aynı."""
    p = _cozumle(baytlar, imza or hashlib.sha256(baytlar).hexdigest())
    k = p["kitap"]
    si = list(k["si"])
    duz_metin = {}
    for i, x in enumerate(si):
        t = _si_metni(x)
        if t is not None:
            duz_metin.setdefault(t, i)

    def metin_no(metin):
        if metin not in duz_metin:
            bosluk = ' xml:space="preserve"' if metin != metin.strip() else ""
            si.append(f"<si><t{bosluk}>{_xml_metni(metin)}</t></si>")
            duz_metin[metin] = len(si) - 1
        return duz_metin[metin]

    sayfa_duzen = collections.defaultdict(dict)
    for (sayfa, r, c), v in duzenleme.items():
        yol = k["sayfalar"].get(sayfa)
        if yol:
            sayfa_duzen[yol][(r, c)] = v
    sayfalar = {}
    for yol in k["sayfalar"].values():
        xml = k["ham"][yol].decode("utf-8")
        if yol in sayfa_duzen:
            xml = _sayfa_duzenle(xml, sayfa_duzen[yol], metin_no, p["stiller"][yol],
                                 k["tarih_stil"], p["stiller"]["_tarih"])
        sayfalar[yol] = xml
    # Paylaşılan metinler baştan: yalnızca bir hücrenin gösterdiği metin kalır.
    kullanilan = sorted({int(n) for xml in sayfalar.values()
                         for _a, n, _b in _METIN_HUCRESI.findall(xml)})
    yeni_no = {eski: i for i, eski in enumerate(kullanilan)}
    toplam = 0
    for yol, xml in sayfalar.items():
        toplam += len(_METIN_HUCRESI.findall(xml))
        sayfalar[yol] = _METIN_HUCRESI.sub(
            lambda m: f"{m.group(1)}{yeni_no[int(m.group(2))]}{m.group(3)}", xml)
    bas = re.sub(r'\s(?:count|uniqueCount)="\d+"', "", k["sst_bas"])
    bas = bas[:-1].rstrip("/") + f' count="{toplam}" uniqueCount="{len(kullanilan)}">'
    sst = k["sst_on"] + bas + "".join(si[i] for i in kullanilan) + "</sst>"
    yeni = {"xl/sharedStrings.xml": sst.encode("utf-8")}
    yeni.update({yol: xml.encode("utf-8") for yol, xml in sayfalar.items()})
    for yol, veri in yeni.items():            # bozuk XML yazılmasın
        try:
            _ET.fromstring(veri)
        except _ET.ParseError as e:
            raise Hata(f"Dosya kurulamadı ({yol}): {e}") from None
    cikti = io.BytesIO()
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        for bilgi_, veri in k["parcalar"]:
            zi = zipfile.ZipInfo(bilgi_.filename, date_time=bilgi_.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = bilgi_.external_attr
            z.writestr(zi, yeni.get(bilgi_.filename, veri))
    return cikti.getvalue()
