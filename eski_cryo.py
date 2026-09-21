"""Programdan önceki cryo haritası — Excel'i çözer, içeri alır, eşleştirir.

Laboratuvarın kendi kriyo haritası program yazılmadan önce Excel'de
tutuluyordu (6 sayfa, ~5.400 satır, 2011-2026). Kullanıcının isteği bu
haritanın Cryo Haritası bölümüne yerleşmesi ve programdaki hastalarla
eşleştirilebilmesi (v6.127).

**Bu satırların hepsi hâlâ tankta duran örnekler** (kullanıcının yanıtı) —
yani tarihsel bir arşiv değil, canlı envanter. Depolama kararlarının
gerekçesi `goc_042.py`'nin başında.

Dosyanın yapısı (kâğıt düzeninden geliyor, elle yazılmadı — çözümlendi):

    TANK 1                                  <- bant, sayfanın içinde
    CANISTER 1        CANISTER 2      ...   <- yan yana bloklar
    NO SOYAD AD EŞİ TARİH HÜCRE VİAL        <- her bloğun başlığı
    1A ....                                 <- veri satırları
    1A ....

- Bloklar **yan yana**; bir sayfada 5-6 blok var, her biri bir kanister.
- Başlık satırı **dikey olarak da tekrarlanıyor** (TANK 4'te 10 kez):
  her tekrar yeni bir kanister demek. Bu yüzden bir bloğun verisi
  "başlıktan sonraki satırdan, aynı sütundaki BİR SONRAKİ başlığa kadar"
  okunuyor — sayfanın sonuna kadar okunursa aynı satırlar defalarca
  sayılır (ilk yazışta tam bu oldu: 595 satırlık sayfa 10.535 kayıt verdi).
- Kanister numarası `NO` başlığının solundaki hücrede (TANK 4: düz "4"),
  ya da bloğun üstündeki `CANISTER n` etiketinde (TANK 1+2+3).
- Tank, bloğun üstündeki `TANK n` bandından; yoksa sayfa adından.

Kategori (embriyo mu sperm mi) **satırın kendi HÜCRE metninden** çıkıyor,
sayfa adından değil: "TANK 4" sayfasında 1.363 embriyo ve 400 sperm satırı
birlikte duruyor.
"""

import datetime as _dt
import re

import db
import xlsx_oku

# Excel'in sayfaları 595 satıra kadar çıkıyor, bloklar 59. sütuna kadar.
EN_COK_SATIR, EN_COK_SUTUN = 5000, 256

# Başlık hücrelerinin tanınan yazılışları. Kâğıttan geldiği için Türkçe
# harfler ve yazım farkları var; hepsi aynı alana bağlanıyor.
_HAM_BASLIKLAR = {
    "NO": "no", "SIRA": "no", "HARF": "no",
    "SOYAD": "soyad", "SOYADI": "soyad",
    "AD": "ad", "ADI": "ad", "İSİM": "ad", "ISIM": "ad",
    "EŞİ": "es", "EŞI": "es", "ESI": "es", "EŞ": "es", "EŞ ADI": "es",
    "TARİH": "tarih", "TARIH": "tarih",
    "HÜCRE": "icerik", "HUCRE": "icerik",
    "VİAL": "vial", "VIAL": "vial",
    "NOTLAR": "notlar", "NOT": "notlar",
}
_BASLIKLAR = {k.replace("İ", "I"): v for k, v in _HAM_BASLIKLAR.items()}

# Bloğun kanonik sütun düzeni: SOYAD'a göre kaçıncı sütunda.
# Başlığı YAZILMAMIŞ alanlar buradan tamamlanıyor -- kâğıttan gelen
# dosyada bir blokta "AD", başkasında "TARİH" başlığı hiç yok ama veri
# satırları o sütunları kullanıyor (YENİ SPERM, 141 kayıt böyle
# kaybolmuştu). Tamamlama yalnızca **boşta olan** sütuna yapılıyor:
# açıkça yazılmış bir başlık hiçbir zaman ezilmiyor.
_KANONIK = {"no": -1, "ad": 1, "es": 2, "tarih": 3, "icerik": 4, "vial": 5}

_ZORUNLU = ("soyad",)

_TANK = re.compile(r"^TANK\s*([0-9]+)\s*$")
# "CANİSTER" (Türkçe İ ile) da yazılmış; `_n()` sonrası I'ya
# çevrilip karşılaştırılıyor.
_KANISTER = re.compile(r"^(?:CANISTER|KANISTER)\s*([0-9]+)\s*$")
_DUZ_SAYI = re.compile(r"^[0-9]{1,3}$")

# Taşıyıcı markaları — `liste_degeri.tasiyici_tipi` kodlarına eşleniyor
# (Rapid-i ve Vitrifit `goc_042` ile eklendi). Sıra önemli: "CRYOTOP"
# aranmadan önce "CRYOLOCK" denenmeli, ikisi de "CRYO" ile başlıyor.
_TIPLER = (
    ("CRYOLOCK", "cryolock"), ("CRYOTOP", "cryotop"),
    ("RAPID", "rapid_i"), ("RAPİD", "rapid_i"),
    ("VITRIFIT", "vitrifit"), ("VİTRİFİT", "vitrifit"),
    ("STRAW", "straw"), ("VİAL", "vial"), ("VIAL", "vial"),
)
_RENKLER = (
    ("SARI", "sari"), ("MAVİ", "mavi"), ("MAVI", "mavi"),
    ("YEŞİL", "yesil"), ("YESIL", "yesil"), ("TURUNCU", "turuncu"),
    ("KIRMIZI", "kirmizi"), ("BEYAZ", "beyaz"), ("MOR", "mor"),
    ("SİYAH", "siyah"), ("SIYAH", "siyah"),
)

# HÜCRE metninden kategori. Yazım hataları da listede: kâğıttan gelen
# dosyada "EKAKÜLAT", "EJEKÜLAT", "RETROGÜLAT" gibi varyantlar var.
_SPERM_IZI = ("SPERM", "TESE", "EJAK", "EKAK", "EJEK", "TESA", "MESA",
              "RETROG", "EPİDİDİM", "EPIDIDIM")
_EMBRIYO_IZI = ("OOSİT", "OOSIT", "OOCYTE", "M2", "MII", "BLAST", "PN",
                "D2", "D3", "D5", "D6", "D7", "HG", "EMBR")


class Hata(Exception):
    """Dosya okunamadı; mesajı kullanıcıya gösterilecek kadar açık."""


def _n(deger) -> str:
    """Başlık/etiket karşılaştırmaları için sadeleştirilmiş metin.

    Türkçe 'İ' burada 'I'ya indirgeniyor: kâğıttan gelen dosyada aynı
    etiket hem "CANISTER" hem "CANİSTER" diye yazılmış. Bu yalnızca
    **başlık tanıma** içindir; hasta adları `tr_buyuk()` ile işleniyor
    (v6.115), oraya karıştırma.
    """
    m = re.sub(r"\s+", " ", str(deger or "").strip()).upper()
    return m.replace("İ", "I")


# ------------------------------------------------------------------- tarihler

def _iki_haneli_yil(y: int) -> int:
    # "22" -> 2022. Yüzyılı kullanıcıya sordurmamak için: iki haneli yıl
    # bu laboratuvarda hep 2000'li yıllar (en eski kayıt 2011).
    return y + 2000 if y < 100 else y


def tarih_coz(ham) -> tuple:
    """Haritadaki tarihi ISO'ya çevirir. -> (ISO ya da None, not ya da None).

    Dosyada üç biçim birden var: gerçek tarih hücresi (ISO'ya
    `xlsx_oku.izgara()` çeviriyor), `04,11,2019` gibi metin, ve bir avuç
    bozuk kayıt (`110052012`, ` 08.02.2024`, beş haneli gün sayacı).

    Yıl sınırları programın kendi kuralıyla aynı (`yil_kontrol`, v6.51/
    v6.53): 1900'den küçük ya da bu yıl + 5'ten büyük yıl **kaydedilmez**,
    ham metin nota düşer. Böyle bir satır atılmıyor — tankta duran bir
    örneği tarihi bozuk diye dışarıda bırakmak yanlış olur (kullanıcının
    kararı); yalnızca tarihi boş kalıyor.
    """
    metin = str(ham or "").strip()
    if not metin or metin.lower() == "none":
        return None, None
    en_yeni = _dt.date.today().year + 5

    def sonuc(y, a, g):
        try:
            t = _dt.date(y, a, g)
        except ValueError:
            return None, metin
        if not 1900 <= t.year <= en_yeni:
            return None, metin
        return t.isoformat(), None

    e = re.match(r"^(\d{4})-(\d{2})-(\d{2})", metin)
    if e:
        return sonuc(int(e.group(1)), int(e.group(2)), int(e.group(3)))

    parcalar = [p for p in re.split(r"[,./\-\s]+", metin) if p]
    if len(parcalar) == 3 and all(p.isdigit() for p in parcalar):
        g, a, y = (int(p) for p in parcalar)
        return sonuc(_iki_haneli_yil(y), a, g)

    if metin.isdigit():
        # Ayraçsız yazılmış tarih: 11052012 -> 11.05.2012
        if len(metin) == 8:
            return sonuc(_iki_haneli_yil(int(metin[4:])), int(metin[2:4]),
                         int(metin[:2]))
        # Metin olarak kalmış gün sayacı (43922 gibi)
        if 4 <= len(metin) <= 5:
            iso = xlsx_oku._seri_tarih(metin)
            if iso:
                return iso, None
    return None, metin


# ------------------------------------------------------- HÜCRE / VİAL çözümü

def kategori_coz(icerik: str, varsayilan: str = "") -> str:
    """HÜCRE metni embriyo/oosit mi, sperm mi? Bilinmiyorsa `varsayilan`."""
    m = _n(icerik)
    if any(k in m for k in _SPERM_IZI):
        return "sperm"
    if any(k in m for k in _EMBRIYO_IZI):
        return "embriyo"
    return varsayilan


def vial_coz(ham: str) -> tuple:
    """VİAL sütunu -> (adet, taşıyıcı tipi kodu, renk kodu). Hepsi None olabilir.

    Örnekler: `1 CRYOLOCKSARI 2` -> (1, cryolock, sari);
    `3 VİAL` -> (3, vial, None); `2(A-B-C)` -> (2, None, None).
    Ham metin her zaman ayrıca saklanıyor (`vial_metni`) — buradaki çıkarım
    bir yorum, aslı kaybolmasın.
    """
    m = _n(ham)
    if not m:
        return None, None, None
    e = re.match(r"^(\d{1,3})", m)
    adet = int(e.group(1)) if e else None
    tip = next((k for a, k in _TIPLER if a in m), None)
    renk = next((k for a, k in _RENKLER if a in m), None)
    return adet, tip, renk


# ---------------------------------------------------------------- çözümleme

def _bloklar(hucreler: dict, sayfa: str) -> list:
    """Bir sayfadaki blokları bulur: [{sutunlar, baslik_satiri, son_satir, ...}]."""
    # 1) Başlık hücreleri: "SOYAD" yazan her hücre bir bloğun başlığı.
    basliklar = sorted((s, c) for (s, c), v in hucreler.items()
                       if _n(v) == "SOYAD")
    if not basliklar:
        return []
    # Aynı sütunda üst üste iki başlık satırı olabiliyor (TANK 1+2+3: 4 ve 5).
    # İkisi de başlık; veri sonuncudan sonra başlıyor.
    sutun_basliklari = {}
    for s, c in basliklar:
        sutun_basliklari.setdefault(c, []).append(s)

    tanklar = sorted((s, c, _TANK.match(_n(v)).group(1))
                     for (s, c), v in hucreler.items() if _TANK.match(_n(v)))
    son_satir = max((s for s, _ in hucreler), default=0)

    bloklar = []
    for sutun, satirlar in sutun_basliklari.items():
        satirlar.sort()
        # Ardışık başlık satırlarını tek başlık say.
        gruplar = []
        for s in satirlar:
            if gruplar and s == gruplar[-1][-1] + 1:
                gruplar[-1].append(s)
            else:
                gruplar.append([s])
        for i, grup in enumerate(gruplar):
            bas = grup[0]
            veri_bas = grup[-1] + 1
            # Veri, aynı sütundaki BİR SONRAKİ başlığa kadar.
            veri_son = (gruplar[i + 1][0] - 1) if i + 1 < len(gruplar) else son_satir
            alanlar = _alan_sutunlari(hucreler, bas, sutun)
            if not all(a in alanlar for a in _ZORUNLU):
                continue
            bloklar.append({
                "sayfa": sayfa,
                "baslik_satiri": bas,
                "veri_bas": veri_bas,
                "veri_son": veri_son,
                "alanlar": alanlar,
                "kanister": _kanister(hucreler, bas, alanlar),
                "tank": _tank(tanklar, bas, alanlar, sayfa),
            })
    return bloklar


def _alan_sutunlari(hucreler: dict, satir: int, soyad_sutunu: int) -> dict:
    """Başlık satırını okuyup {alan adı: sütun} çıkarır.

    Sütun kaymalarına dayanıklı olsun diye sabit offset **kullanılmıyor**:
    başlık satırındaki gerçek yazılar okunuyor. YENİ SPERM sayfasında bir
    blokta "AD" başlığı hiç yok, o blok yalnızca bulunan alanlarla çalışır.
    """
    alanlar = {}
    for c in range(soyad_sutunu - 2, soyad_sutunu + 8):
        ad = _BASLIKLAR.get(_n(hucreler.get((satir, c))))
        if ad and ad not in alanlar:
            alanlar[ad] = c
    alanlar["soyad"] = soyad_sutunu
    dolu = set(alanlar.values())
    for ad, kayma in _KANONIK.items():
        if ad in alanlar:
            continue
        c = soyad_sutunu + kayma
        if c > 0 and c not in dolu:
            alanlar[ad] = c
            dolu.add(c)
    return alanlar


def _kanister(hucreler: dict, baslik_satiri: int, alanlar: dict):
    """Bloğun kanister numarası: `NO` başlığının solundaki ya da üstündeki."""
    no_sutunu = alanlar.get("no", alanlar["soyad"] - 1)
    for sutun in (no_sutunu - 1, no_sutunu):
        for satir in range(baslik_satiri, max(0, baslik_satiri - 4), -1):
            m = _n(hucreler.get((satir, sutun)))
            if not m:
                continue
            e = _KANISTER.match(m)
            if e:
                return e.group(1)
            if _DUZ_SAYI.match(m):
                return m
    return None


def _tank(tanklar: list, baslik_satiri: int, alanlar: dict, sayfa: str):
    """Bloğun tankı: üstündeki en yakın `TANK n` bandı.

    Bant seçimi **sütuna da bakıyor**, yalnızca satıra değil: TANK 1+2+3
    sayfasında 53. sütundaki blok için (2, 53)'te ayrı bir "TANK 3" bandı
    var; yalnızca "en yakın üstteki bant" denseydi 1. sütundaki bloklar da
    onu alırdı.
    """
    no_sutunu = alanlar.get("no", alanlar["soyad"] - 1)
    son = alanlar.get("vial", alanlar["soyad"] + 5)
    icinde = [t for t in tanklar
              if t[0] <= baslik_satiri and no_sutunu - 1 <= t[1] <= son]
    if icinde:
        return "TANK " + max(icinde)[2]
    ustunde = [t for t in tanklar if t[0] <= baslik_satiri and t[1] <= no_sutunu]
    if ustunde:
        return "TANK " + max(ustunde)[2]
    # Sayfa adı olduğu gibi (büyük harfe çevrilmiş) kalır: `_n()`
    # burada kullanılamaz, o "İ"yi "I"ya indiriyor (başlık tanıma
    # için) ve tank adı "YENİ SPERM" -> "YENI SPERM" olurdu.
    return re.sub(r"\s+", " ", str(sayfa or "").strip()).replace("i", "İ").upper()


def coz(baytlar: bytes) -> dict:
    """Yüklenen `.xlsx`'i çözer.

    -> {"satirlar": [...], "sayfalar": {...}, "uyarilar": [...]}

    Hiçbir şey veritabanına yazılmaz; yazma `iceri_al()`'de.
    """
    try:
        izgara = xlsx_oku.izgara(baytlar, EN_COK_SATIR, EN_COK_SUTUN)
    except xlsx_oku.Hata as e:
        raise Hata(str(e)) from None
    if not izgara:
        raise Hata("dosyada sayfa yok")

    satirlar, uyarilar = [], []
    sayfa_ozeti = {}
    for sayfa, hucreler in izgara.items():
        bloklar = _bloklar(hucreler, sayfa)
        if not bloklar:
            uyarilar.append(f"{sayfa}: başlık satırı (NO/SOYAD/AD/…) bulunamadı, "
                            "sayfa atlandı")
            continue
        sayfa_satirlari = []
        eksik = 0
        for blok in bloklar:
            a = blok["alanlar"]
            for satir in range(blok["veri_bas"], blok["veri_son"] + 1):
                def al(ad):
                    return str(hucreler.get((satir, a[ad]), "")).strip() if ad in a else ""
                soyad, ad_, es = al("soyad"), al("ad"), al("es")
                tarih_ham, icerik, vial = al("tarih"), al("icerik"), al("vial")
                no, not_ = al("no"), al("notlar")
                if _n(soyad) in _BASLIKLAR or _n(ad_) in _BASLIKLAR:
                    continue                      # tekrarlanan başlık satırı
                if not (soyad or ad_):
                    continue
                if not (tarih_ham or icerik or vial):
                    # Adı var ama örnek bilgisi hiç yok: kayıt saymıyoruz,
                    # ama sessizce yutmuyoruz da.
                    eksik += 1
                    continue
                tarih, tarih_notu = tarih_coz(tarih_ham)
                adet, tip, renk = vial_coz(vial)
                sayfa_satirlari.append({
                    "sayfa": sayfa, "satir": satir, "sutun": a["soyad"],
                    "tank": blok["tank"], "kanister": blok["kanister"],
                    "goblet": no,
                    "soyad": soyad, "ad": ad_, "es_adi": es,
                    "tarih": tarih, "tarih_notu": tarih_notu,
                    "icerik": icerik, "vial_metni": vial,
                    "adet": adet, "tip": tip, "renk": renk, "notlar": not_,
                    "kategori": kategori_coz(icerik),
                })
        # Kategorisi metinden anlaşılmayan satırlar sayfanın baskın
        # kategorisine düşer (YENİ SPERM'de HÜCRE'si boş 74 satır gibi).
        baskin = _baskin_kategori(sayfa_satirlari)
        for s in sayfa_satirlari:
            if not s["kategori"]:
                s["kategori"] = baskin
        satirlar.extend(sayfa_satirlari)
        sayfa_ozeti[sayfa] = {
            "kayit": len(sayfa_satirlari), "blok": len(bloklar), "eksik": eksik}
        if eksik:
            uyarilar.append(f"{sayfa}: {eksik} satırda isim var ama tarih/hücre/"
                            "vial yok — kayıt sayılmadı")
    if not satirlar:
        raise Hata("dosyada okunabilir kayıt bulunamadı")
    return {"satirlar": satirlar, "sayfalar": sayfa_ozeti, "uyarilar": uyarilar}


def _baskin_kategori(satirlar: list) -> str:
    sperm = sum(1 for s in satirlar if s["kategori"] == "sperm")
    embriyo = sum(1 for s in satirlar if s["kategori"] == "embriyo")
    return "sperm" if sperm > embriyo else "embriyo"


# ------------------------------------------------------------------ içeri alma

def iceri_al(satirlar: list, konum_bul, kullanici_id=None) -> dict:
    """Çözülmüş satırları `eski_cryo`'ya yazar. -> sayaçlar.

    **Idempotent**: kaynak hücre koordinatı (`sayfa`, `satır`, `sütun`)
    tekil anahtar. Kullanıcı Excel'i düzeltip yeniden yüklerse aynı satır
    ikinci bir kayıt açmıyor, mevcut kayıt güncelleniyor — ve **elle
    kurulmuş `hasta_id` eşleşmesi korunuyor** (UPDATE o kolona dokunmuyor).

    `konum_bul`: `app.konum_bul_veya_olustur`. Dışarıdan veriliyor çünkü
    konum yolunu kuran kural tek yerde durmalı ve `app` bu modülü import
    ettiği için buradan `app`'i import etmek döngü olurdu.

    **İki aşama, bilerek.** Önce konumlar çözülüyor (`konum_bul` kendi
    bağlantısını açıyor), SONRA 5.400 satır tek `yazma_islemi()` içinde
    yazılıyor. Karıştırılamaz: `BEGIN IMMEDIATE` yazma kilidini tuttuğu
    sürece `konum_bul`'un ayrı bağlantısı kilidi bekler ve iş asılır.
    Satır başına ayrı bağlantı açmak ise ilk denemede 5.400 kayıt için
    14 saniye sürmüştü — tek işlemde saniyenin altına iniyor.
    """
    # 1) Konumlar. Var olanlar tek sorguyla belleğe alınıyor; yalnızca
    #    gerçekten yeni olan yol için `konum_bul` çağrılıyor.
    mevcut_konum = {r["tam_yol"]: r["id"] for r in db.sorgu(
        "SELECT id, tam_yol FROM konum WHERE lab_id=?", (db.LAB_ID,))}
    konumlar, yeni_konum = {}, 0
    for s in satirlar:
        anahtar = (s["tank"], s["kanister"], s["goblet"])
        if anahtar in konumlar:
            continue
        seviyeler = [s["tank"] or "",
                     f"Kanister {s['kanister']}" if s["kanister"] else "",
                     s["goblet"] or "", ""]
        tam_yol = " / ".join(x for x in seviyeler if x)
        if tam_yol in mevcut_konum:
            konumlar[anahtar] = mevcut_konum[tam_yol]
        elif tam_yol:
            konumlar[anahtar] = konum_bul(seviyeler)
            mevcut_konum[tam_yol] = konumlar[anahtar]
            yeni_konum += 1
        else:
            konumlar[anahtar] = None

    # 2) Kayıtlar — tek işlemde.
    eklenen = guncellenen = 0
    with db.yazma_islemi() as b:
        var = {(r["kaynak_sayfa"], r["kaynak_satir"], r["kaynak_sutun"]): r["id"]
               for r in b.execute(
                   "SELECT id, kaynak_sayfa, kaynak_satir, kaynak_sutun "
                   "FROM eski_cryo WHERE lab_id=?", (db.LAB_ID,))}
        for s in satirlar:
            konum_id = konumlar[(s["tank"], s["kanister"], s["goblet"])]
            alanlar = (konum_id, s["kategori"], s["soyad"], s["ad"], s["es_adi"],
                       s["tarih"], s["tarih_notu"], s["icerik"], s["vial_metni"],
                       s["tip"], s["renk"], s["adet"], s.get("notlar") or None)
            kimlik = var.get((s["sayfa"], s["satir"], s["sutun"]))
            if kimlik:
                b.execute(
                    "UPDATE eski_cryo SET konum_id=?, kategori=?, soyad=?, ad=?, "
                    "  es_adi=?, tarih=?, tarih_notu=?, icerik=?, vial_metni=?, "
                    "  tip=?, renk=?, adet=?, notlar=? WHERE id=?",
                    alanlar + (kimlik,))
                guncellenen += 1
            else:
                b.execute(
                    "INSERT INTO eski_cryo (lab_id, konum_id, kategori, soyad, "
                    "  ad, es_adi, tarih, tarih_notu, icerik, vial_metni, tip, "
                    "  renk, adet, notlar, kaynak_sayfa, kaynak_satir, "
                    "  kaynak_sutun) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (db.LAB_ID,) + alanlar
                    + (s["sayfa"], s["satir"], s["sutun"]))
                eklenen += 1
    return {"eklenen": eklenen, "guncellenen": guncellenen,
            "konum": len(konumlar), "yeni_konum": yeni_konum}


# ---------------------------------------------------------------- eşleştirme
#
# Eski haritada **hasta dosya numarası yok**, yalnızca isim var. Programın
# tek güvendiği kimlik ise `dosya_no` (`UNIQUE (lab_id, dosya_no)`, v6.125)
# ve CLAUDE.md'nin kuralı açık: "isimle eşleştirme yok ... yanlış hasta bu
# işin en pahalı hatası".
#
# Bu kural burada **gevşetilmiyor**: isim yalnızca ADAY öneriyor, bağlamayı
# her zaman insan onaylıyor (`bagla()` bir kullanıcı eylemi). Ölçüldü —
# ad+soyad ikilisi 3.884 embriyo satırında 1.997 kişiye denk geliyor, eş
# adı bunun üstüne 26 ayrım daha koyuyor ve 17 kişide aynı ad-soyad farklı
# eş adı taşıyor (13'ü gerçekten farklı isim). Yani eş adı ana anahtar
# değil, **hakem**: ad-soyad çakıştığında ayıran şey o.

# Eşleşmenin gücü. Ekranda kova adı olarak da kullanılıyor.
TAM = "tam"            # ad+soyad birebir VE eş adı da tutuyor
ISIM = "isim"          # ad+soyad birebir, eş adı iki tarafta da yok/boş
CELISKILI = "celiskili"  # ad+soyad birebir ama eş adı TUTMUYOR
KISMI = "kismi"        # yalnızca kısmen benziyor
_SIRA = {TAM: 3, ISIM: 2, CELISKILI: 1, KISMI: 0}


def _kelimeler(metin) -> set:
    """İsmi kelime kümesine çevirir — sıra önemsiz olsun diye.

    Excel'de soyad ve ad AYRI sütunlarda, programda tek bir "Ad soyad"
    kutusu var ve personel hangi sırayla yazarsa öyle duruyor. Düz metin
    eşitliği bu yüzden çalışmaz: "<soyad> <ad>" ile "<ad> <soyad>"
    aynı kişi.
    """
    from app import tr_buyuk   # döngüsel import olmasın diye çağrı anında
    m = tr_buyuk(str(metin or "").strip())
    return {k for k in re.split(r"[^\wİIŞĞÜÖÇ]+", m or "") if k}


def _guc(kayit_ad: set, kayit_es: set, hasta_ad: set, hasta_es: set) -> str:
    if kayit_ad != hasta_ad:
        return KISMI
    if not kayit_es or not hasta_es:
        return ISIM
    return TAM if kayit_es & hasta_es else CELISKILI


def aday_hastalar(kayit, en_cok: int = 8) -> list:
    """Bu eski kayıt programdaki hangi hastalar olabilir?

    Dönen her satır hastanın kendi alanları + `guc` (TAM/ISIM/CELISKILI/
    KISMI). **Hiçbiri kendiliğinden bağlanmaz**; ekran bunları gösterir,
    bağlamayı kullanıcı yapar.
    """
    from app import tr_buyuk
    soyad = (kayit["soyad"] or "").strip()
    ad = (kayit["ad"] or "").strip()
    if not (soyad or ad):
        return []
    # `hasta.ad_soyad` v6.115'ten beri hep büyük harfle kayıtlı; arama
    # terimi de `tr_buyuk()`'ten geçmeli, yoksa Türkçe harfli isimler
    # SQLite'ın ASCII-only LIKE'ında eşleşmez (v6.116).
    kosul, parametre = ["h.lab_id = ?"], [db.LAB_ID]
    for parca in (soyad, ad):
        if parca:
            kosul.append("h.ad_soyad LIKE ?")
            parametre.append(f"%{tr_buyuk(parca)}%")
    satirlar = db.sorgu(
        "SELECT h.id, h.dosya_no, h.ad_soyad, h.es_adi, h.durum, "
        "  (SELECT COUNT(*) FROM cycle WHERE hasta_id = h.id) AS cycle_sayisi "
        "FROM hasta h WHERE " + " AND ".join(kosul)
        + " ORDER BY h.ad_soyad LIMIT 50", tuple(parametre))
    kayit_ad = _kelimeler(f"{soyad} {ad}")
    kayit_es = _kelimeler(kayit["es_adi"])
    cikti = []
    for r in satirlar:
        d = dict(r)
        d["guc"] = _guc(kayit_ad, kayit_es,
                        _kelimeler(r["ad_soyad"]), _kelimeler(r["es_adi"]))
        cikti.append(d)
    cikti.sort(key=lambda d: (-_SIRA[d["guc"]], d["ad_soyad"]))
    return cikti[:en_cok]


def bagla(eski_id: int, hasta_id, kullanici_id=None) -> None:
    """Eski kaydı bir hastaya bağlar (ya da `hasta_id=None` ile bağı koparır)."""
    db.yaz(
        "UPDATE eski_cryo SET hasta_id=?, eslesme_zamani=?, "
        "  eslesme_kullanici_id=? WHERE lab_id=? AND id=?",
        (hasta_id,
         _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if hasta_id else None,
         kullanici_id if hasta_id else None, db.LAB_ID, eski_id))


def durum_yaz(eski_id: int, durum: str) -> None:
    """Örneğin tanktaki durumu: 'dolu' ya da 'cikarildi'.

    Kullanıcının yanıtına göre haritadaki her satır **hâlâ tankta duran**
    bir örnek; ileride çözülen/çıkarılan olursa harita Excel gibi bayatlamasın
    diye işaretlenebiliyor. Kayıt silinmiyor (programın "silme = iptal
    işaretleme" kuralı).
    """
    db.yaz("UPDATE eski_cryo SET durum=? WHERE lab_id=? AND id=?",
           (durum, db.LAB_ID, eski_id))


def ozet() -> dict:
    """Ekranın üst kartı: kaç kayıt, kaçı eşleşmiş, kaçı duruyor."""
    r = db.tek(
        "SELECT COUNT(*) AS toplam, "
        "  SUM(CASE WHEN hasta_id IS NOT NULL THEN 1 ELSE 0 END) AS eslesen, "
        "  SUM(CASE WHEN durum='dolu' THEN 1 ELSE 0 END) AS duran, "
        "  SUM(CASE WHEN kategori='embriyo' THEN 1 ELSE 0 END) AS embriyo, "
        "  SUM(CASE WHEN kategori='sperm' THEN 1 ELSE 0 END) AS sperm "
        "FROM eski_cryo WHERE lab_id=?", (db.LAB_ID,))
    d = {k: (r[k] or 0) for k in
         ("toplam", "eslesen", "duran", "embriyo", "sperm")}
    d["eslesmeyen"] = d["toplam"] - d["eslesen"]
    return d


_TABAN = (
    "SELECT e.*, k.tam_yol, k.seviye1 AS tank, "
    "  h.dosya_no, h.ad_soyad AS hasta_adi "
    "FROM eski_cryo e LEFT JOIN konum k ON k.id = e.konum_id "
    "LEFT JOIN hasta h ON h.id = e.hasta_id "
    "WHERE e.lab_id = ?")


def kayitlar(ara: str = "", kategori: str = "", yalnizca_eslesmeyen: bool = False,
             hasta_id=None, limit: int = 100, offset: int = 0) -> list:
    """Eski harita kayıtları — `/cryo` kartı ve eşleştirme ekranı için."""
    from app import tr_buyuk
    kosul, p = [], [db.LAB_ID]
    if kategori:
        kosul.append("e.kategori = ?")
        p.append(kategori)
    if yalnizca_eslesmeyen:
        kosul.append("e.hasta_id IS NULL")
    if hasta_id is not None:
        kosul.append("e.hasta_id = ?")
        p.append(hasta_id)
    if ara.strip():
        # İsim sütunları eski haritadan geldiği gibi (büyük harf) duruyor;
        # arama terimi `tr_buyuk()`'ten geçiyor (v6.116). Konum yolu ve
        # içerik metni büyük harfe sabitlenmiş DEĞİL — onlara ham terim.
        kosul.append("(e.soyad LIKE ? OR e.ad LIKE ? OR e.es_adi LIKE ? "
                     "OR k.tam_yol LIKE ? OR e.icerik LIKE ?)")
        p += [f"%{tr_buyuk(ara)}%"] * 3 + [f"%{ara}%"] * 2
    sql = _TABAN + ("".join(" AND " + k for k in kosul))
    sql += " ORDER BY k.tam_yol, e.soyad, e.ad LIMIT ? OFFSET ?"
    return db.sorgu(sql, tuple(p) + (limit, offset))


def sayisi(ara: str = "", kategori: str = "",
           yalnizca_eslesmeyen: bool = False) -> int:
    """`kayitlar()` ile aynı süzgeç, yalnızca sayı (sayfalama için)."""
    from app import tr_buyuk
    kosul, p = [], [db.LAB_ID]
    if kategori:
        kosul.append("e.kategori = ?")
        p.append(kategori)
    if yalnizca_eslesmeyen:
        kosul.append("e.hasta_id IS NULL")
    if ara.strip():
        kosul.append("(e.soyad LIKE ? OR e.ad LIKE ? OR e.es_adi LIKE ? "
                     "OR k.tam_yol LIKE ? OR e.icerik LIKE ?)")
        p += [f"%{tr_buyuk(ara)}%"] * 3 + [f"%{ara}%"] * 2
    sql = ("SELECT COUNT(*) AS n FROM eski_cryo e "
           "LEFT JOIN konum k ON k.id = e.konum_id WHERE e.lab_id = ?"
           + "".join(" AND " + k for k in kosul))
    return db.tek(sql, tuple(p))["n"]


def tek_kayit(eski_id: int):
    return db.tek(_TABAN + " AND e.id = ?", (db.LAB_ID, eski_id))


def hastanin_kayitlari(hasta_id: int) -> list:
    """Bir hastaya bağlanmış eski harita kayıtları — hasta kartı için."""
    return kayitlar(hasta_id=hasta_id, limit=200)


def tank_ozeti() -> list:
    """Tank tank kaç eski kayıt duruyor — `/cryo`'nun tank kartı için."""
    return db.sorgu(
        "SELECT k.seviye1 AS tank, COUNT(*) AS adet, "
        "  SUM(CASE WHEN e.kategori='embriyo' THEN 1 ELSE 0 END) AS embriyo, "
        "  SUM(CASE WHEN e.kategori='sperm' THEN 1 ELSE 0 END) AS sperm "
        "FROM eski_cryo e JOIN konum k ON k.id = e.konum_id "
        "WHERE e.lab_id=? AND e.durum='dolu' AND k.seviye1 IS NOT NULL "
        "GROUP BY k.seviye1 ORDER BY k.seviye1", (db.LAB_ID,))
