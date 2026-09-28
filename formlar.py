"""Resmî formların verisi ve yerleşimi.

Kullanıcının tutmak **zorunda** olduğu iki form var (Akdeniz Üniversitesi
Tıp Fakültesi, Üreme Endokrinolojisi ve YÜT Merkezi):

  - **Embriyoloji Özet Formu** — DH.FR.91, Rev.03, cycle başına bir sayfa
  - **ART Lab. Raporu** — DH.FR.107, Rev.01, cycle başına bir sayfa (yatay)

Formun **kalıbı burada değil**: satır/sütun ölçüleri, kutular ve kâğıtta
basılı yazılar `form_kalip.json`'da duruyor ve orijinal `.xls` dosyalarından
çıkarıldı (bkz. `form_kalip.py`). Bu dosyanın işi **verinin hangi kutuya
gireceği**: `*_verisi()` cycle'ın verisini toplar, `*_dolgu()` onu kalıbın
hücre adreslerine dağıtır. Aynı dolgu iki yere gidiyor — tarayıcıdan
yazdırılan sayfa (`form.html`) ve `.xlsx` — o yüzden ikisi ayrı düşemiyor.

**Form kalıbına dokunma.** Doküman kodu, yayın/revizyon tarihi, alan adları
ve form numarası kurumun kalite sisteminden geliyor; kâğıt aslıyla aynı
görünmek zorunda. Yeni bir alan ekleyeceksen kutunun **içini** doldur,
başlığını değiştirme.

**Programda karşılığı olmayan alan boş bırakılır.** Kimlik no, empty zona,
intakt, tüp no, medium/lot numaraları, seleksiyon, transfer klinisyeni ve
personel sınıflandırması programda tutulmuyor; kutuları boş çıkıyor,
kullanıcı kalemle dolduruyor. Bu alanları **uydurma** — resmî bir forma
yanlış veri yazmak, boş bırakmaktan kötü.
"""

import datetime as _dt
import re
import textwrap

import db
import metinler

# ----------------------------------------------------------- ortak yardımcılar


def _sayi(r, anahtar):
    """Sayısal bir alanın forma basılacak hali; anlamsız ".0" düşürülür.

    Kolonlar SQLite'ta REAL olduğu için 85 değeri "85.0" diye geliyordu ve
    ART Lab'ın "% Motil" kutusuna **sığmıyordu**: kutu 32px, "%  85.0" 40px
    -- fazlası `.kalip td`'nin `overflow: hidden`'ıyla sessizce kesiliyor,
    ekranda "%  85." görünüyordu (v6.37'den beri böyleydi, v6.136'da
    düzeltildi). Tam sayıda ondalık düşüyor ("85"), gerçekten kesirli bir
    değer olduğu gibi kalıyor ("0.8" ml, "85.5") -- yuvarlamak klinik bir
    sayıyı değiştirirdi, bu forma yanlış veri yazmak demek olurdu.
    """
    d = r[anahtar] if r and r[anahtar] is not None else None
    if isinstance(d, float) and d.is_integer():
        return int(d)
    return d


def _zaman_coz(metin):
    """'2026-09-11 08:15[:00]' -> datetime; çözülemezse None.

    Bozuk `0026-09-04` gibi bir değer de None döner: saat hesabına girse
    binlerce saatlik farklar üretirdi (bkz. CLAUDE.md bekleyen iş 6).
    """
    if not metin:
        return None
    try:
        d = _dt.datetime.fromisoformat(str(metin).replace("T", " "))
    except ValueError:
        return None
    return d if d.year >= 1900 else None


def _saat_farki(a, b):
    """b'den a'ya kaç saat geçmiş (bir ondalık). Biri yoksa None."""
    if not a or not b:
        return None
    return round((a - b).total_seconds() / 3600.0, 1)


def _gg_aa_yyyy(tarih):
    """'2026-09-11' -> '11.09.2026'; boş/okunamıyorsa None.

    Ekrandaki `gg_aa_yyyy()` ile aynı gerekçe (CLAUDE.md: "tarih gün.ay.yıl
    sırasıyla basılır") -- resmî formlara aktarılan tarihler de aynı kurala
    uyar. `app.py`'den import edilmiyor (formlar.py ondan bağımsız bir modül,
    döngüsel import olurdu), o yüzden küçük bir kopyası burada duruyor.
    Excel'e giden hücreler zaten kalıbın kendi stilini taşıyor (`bicim !=
    _DUZ`), yani `excel.py`'nin ISO tarih algılaması buraya hiç uygulanmıyor
    -- biçimi değiştirmek Excel çıktısını bozmaz.
    """
    d = _zaman_coz(tarih)
    return d.strftime("%d.%m.%Y") if d else None


def _gg_aa_yyyy_saat(zaman):
    """'2026-09-11 08:15:00' -> '11.09.2026 08:15'; boş/okunamıyorsa None."""
    d = _zaman_coz(zaman)
    return d.strftime("%d.%m.%Y %H:%M") if d else None


def _etiketler() -> dict:
    return {(r["liste_adi"], r["kod"]): r["etiket"] for r in db.sorgu(
        "SELECT liste_adi, kod, etiket FROM liste_degeri WHERE lab_id = ?",
        (db.LAB_ID,))}


def _et(h, liste, kod):
    if kod is None or kod == "":
        return None
    return h.get((liste, str(kod)), str(kod))


def _yapan(cycle_id, asama):
    r = db.tek("SELECT yapan_ad FROM islem_yapan WHERE cycle_id=? AND asama=?",
               (cycle_id, asama))
    return r["yapan_ad"] if r else None


def _iptal_notu(c):
    """Cycle iptal edildiyse seçilen sebebin ekran etiketi, değilse None.

    `c["bitis_sebebi"]` yalnızca `BITIS_DURUMU`'ndaki (app.py) doğrulanmış
    kodlardan biri olabiliyor -- `cycle_bitir()` başka bir değeri reddediyor
    -- o yüzden `metin()` burada doğrudan çağrılabiliyor; adresten gelen
    serbest bir anahtar değil (tuzak #9'daki gibi değil).
    """
    if c["durum"] != "iptal" or not c["bitis_sebebi"]:
        return None
    return metinler.t("bitis_" + c["bitis_sebebi"])


def _yas(dogum, tarih):
    """`tarih` günündeki yaş. Tedavi anındaki yaş istendiği için bugünün
    yaşı değil, OPU günündeki yaş yazılıyor."""
    d, t = _zaman_coz(dogum), _zaman_coz(tarih) or _dt.datetime.now()
    if not d:
        return None
    return t.year - d.year - ((t.month, t.day) < (d.month, d.day))


def _ad_soyad_ayir(tam):
    """Formda SOYADI ve ADI ayrı kutular, programda tek alan (`ad_soyad`).

    **Son kelime soyadı sayılıyor** — Türkçede olağan yazım ve programın
    alan adı da "ad soyad" sırasını söylüyor. Bileşik soyadlarda yanılabilir;
    kullanıcı formda görüp düzeltebilsin diye bilinçli olarak boş bırakmak
    yerine dolduruluyor (resmî formda boş kimlik kutusu daha kötü).
    Hasta kaydında ad ve soyad ayrılırsa burası tek satırla düzelir.
    """
    parcalar = (tam or "").strip().split()
    if len(parcalar) < 2:
        return "", (tam or "").strip()
    return parcalar[-1], " ".join(parcalar[:-1])


def _sutun(alan):
    """Alt sorgunun seçtiği şey: kolon adıysa `x.<ad>`, parantezle başlayan
    bir ifadeyse olduğu gibi (v6.157: birleşmede hücre sayısının yerine
    `db.BIRLESME`, `db.cl_hucre_ifadesi('x')`). İkisi de koddan gelir."""
    return alan if alan.startswith("(") else f"x.{alan}"


def gun_alt(alan, tip, gun, ek=""):
    """Bir örneğin belirli gündeki değerlendirmesinden tek alan (alt sorgu).

    Dış sorguda örnek tablosu `s` diye adlandırılmış olmalı. `disari.py` de
    aynı parçaları kullanıyor — tek yerde dursun diye burada. `ek`:
    `son_alt()`'taki gibi, `AND ...` diye başlayan ek koşul (v6.147).
    `alan` bir kolon adı ya da parantezli bir ifade (`db.cl_hucre_ifadesi()`).
    """
    return (f"(SELECT {_sutun(alan)} FROM olay x WHERE x.specimen_id = s.id "
            f"AND x.tip = '{tip}' AND x.gun = {gun} AND x.iptal_mi = 0 {ek} "
            "ORDER BY x.id DESC LIMIT 1)")


def yumurta_kosulu(c) -> str:
    """Resmî formların ve tedavi Excel'inin yumurta ızgarası hangi örneklerden
    -- SQL koşulu (örnek tablosu `s`), bir `?`: tedavinin kimliği (v6.147).

    Tedavinin kendi örnekleri; Yumurta Çözme'de bu tedavi için çözülen
    yumurtalar (`db.cozulen_yumurta_islenir()`) -- ICSI'leri, döllenmeleri
    bu tedavide. `fet`/`fet_kultur`'un ızgarası değişmedi: çözülen embriyo
    yumurta ızgarasının bir sütunu değil.
    """
    tip = c["cycle_tipi"]
    if db.cozulen_yumurta_islenir(tip):
        return db.tedavi_ornekleri(tip)
    return "s.cycle_id = ?"


def son_alt(alan, tip, sira="x.id DESC", ek=""):
    """Bir örneğin o tipteki son kaydından tek alan (alt sorgu).

    `ek` (v6.143): `AND ...` diye başlayan ek koşul, alt sorgunun olayı `x`.
    Bir örneğin artık birden çok dondurması/çözmesi olabildiği için "son"
    her zaman yeterli değil -- ör. BU tüpten yapılan çözme, BU tedavide
    yapılan dondurma. Koşul metni koddan gelir, adresten değil.
    """
    return (f"(SELECT {_sutun(alan)} FROM olay x WHERE x.specimen_id = s.id "
            f"AND x.tip = '{tip}' AND x.iptal_mi = 0 {ek} "
            f"ORDER BY {sira} LIMIT 1)")


# ------------------------------------------------------------ zaman çizelgesi

# Çizelgede görünecek aşamalar ve zamanın nereden okunacağı. Sıra klinik akış.
# `olay` satırındakiler için o aşamanın **ilk** kaydı alınıyor: laboratuvarın
# o işe başladığı an.
_CIZELGE = [
    ("opu", "asama_opu"),
    ("androloji", "asama_androloji"),
    ("denudasyon", "asama_denudasyon"),
    ("icsi", "asama_icsi"),
    ("fert", "asama_fert"),
    ("gun2", None),
    ("gun3", None),
    ("blast", "asama_blast"),
    ("vitrifikasyon", "asama_vitrifikasyon"),
    ("thaw", "asama_thaw"),
    ("transfer", "asama_transfer"),
]


def _olay_ilk(cycle_id, tip, gun=None):
    """Bu tedavide YAPILAN o tipteki **ilk** olayın zamanı (v6.146).

    v6.146'ya kadar örneğin kendi tedavisine bakıyordu (`specimen.cycle_id`):
    FET'in çizelgesi boş kalıyor, kaynak ICSI'ninkinde FET'te yapılan çözme,
    transfer ve yeniden dondurma görünüyordu -- ICSI'nin resmî formundaki
    İŞLEM saatleri de öyle. Koşul artık `db.tedavide_yapilan()` -- tedavi
    ekranının özet kutusuyla aynı.
    """
    bu_tedavide, p = db.tedavide_yapilan(cycle_id)
    kosul = "AND o.gun = ?" if gun is not None else ""
    r = db.tek(
        f"SELECT MIN(o.zaman) z FROM olay o WHERE o.tip = ? AND o.iptal_mi = 0 "
        f"{kosul} AND {bu_tedavide}",
        [tip] + ([gun] if gun is not None else []) + p)
    return r["z"] if r else None


def zaman_cizelgesi(cycle_id: int) -> list:
    """Cycle'ın aşama saatleri ve aralarında geçen süre.

    Kullanıcının isteği (2026-09-11): resmî formdaki "24 saat", "40-45 saat",
    "72 saat" satırlarını **varsayımla** doldurmak yerine program gerçekten
    kaç saat geçtiğini hesaplasın. Ayrı bir kayıt tutulmuyor — bütün saatler
    zaten aşama ekranlarında elle girilebiliyor, çizelge onlardan türüyor.

    Her satır: aşama kodu, ekrandaki adı, zamanı, **bir önceki işlemden**
    geçen saat ve **OPU'dan** bu yana geçen saat. İkisi birden var, çünkü
    "kaç saatte bir baktık" ile "kaçıncı saatteki değerlendirme" iki ayrı
    soru; formun satır başlıkları (24/40-45/72 saat) ikincisini soruyor.

    Zamanı girilmemiş aşama çizelgede **yok** — boş satır koymak "o iş
    yapılmadı" ile "saati girilmedi"yi karıştırırdı.
    """
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return []
    sperm = db.tek("SELECT hazirlama_zamani, alinma_zamani FROM sperm_ornek "
                   "WHERE cycle_id = ? ORDER BY id LIMIT 1", (cycle_id,))

    ham = {
        "opu": c["opu_zamani"],
        "androloji": (sperm["hazirlama_zamani"] or sperm["alinma_zamani"]
                      if sperm else None),
        "denudasyon": c["denudasyon_zamani"],
        "icsi": _olay_ilk(cycle_id, "icsi"),
        "fert": _olay_ilk(cycle_id, "fertilizasyon_kontrolu"),
        "gun2": _olay_ilk(cycle_id, "cleavage_degerlendirme", 2),
        "gun3": _olay_ilk(cycle_id, "cleavage_degerlendirme", 3),
        "blast": _olay_ilk(cycle_id, "blastokist_degerlendirme"),
        "vitrifikasyon": _olay_ilk(cycle_id, "vitrifikasyon"),
        "thaw": _olay_ilk(cycle_id, "thaw"),
        "transfer": _olay_ilk(cycle_id, "transfer"),
    }

    opu = _zaman_coz(ham["opu"])

    # Sıra **zamana göre**, klinik akış sırasına göre değil. "Bir önceki
    # işlemden kaç saat geçti" sorusunun cevabı gerçekten önce yapılan işe
    # bakmalı: aynı gün önce transfer edip sonra kalanı dondurmak olağan ve
    # akış sırası kullanılsaydı o satır eksi saat gösterirdi.
    secilenler = []
    for kod, anahtar in _CIZELGE:
        z = _zaman_coz(ham[kod])
        if not z:
            continue
        ad = (metinler.t(anahtar) if anahtar
              else metinler.t("gun_n_buyuk").format(n=kod[-1]))
        secilenler.append((z, kod, ad))
    secilenler.sort(key=lambda x: x[0])

    cizelge, onceki = [], None
    for z, kod, ad in secilenler:
        cizelge.append({
            "asama": kod,
            "ad": ad,
            "zaman": ham[kod],
            "onceki_saat": _saat_farki(z, onceki),
            "opu_saat": _saat_farki(z, opu) if kod != "opu" else None,
        })
        onceki = z
    return cizelge


def cizelge_saati(cizelge, asama):
    """Çizelgeden bir aşamanın OPU'dan bu yana geçen saati."""
    for s in cizelge:
        if s["asama"] == asama:
            return s["opu_saat"]
    return None


# ------------------------------------------------- embriyoloji özet formu


def _bu_tedavide_say(cycle_id, alan, tip, ek=""):
    """Bu tedavide YAPILAN o tipteki olaylar, bir alanın değerine göre
    sayılmış (DISTINCT örnek) -- `{deger: n}` (v6.147).

    v6.147'ye kadar ölçü örneğin kendi tedavisiydi (`s.cycle_id`): Yumurta
    Çözme'de çözülen yumurtanın ICSI'si, döllenmesi kaynak Yumurta
    Dondurma'nın resmî formuna yazılır, Yumurta Çözme'ninki boş kalırdı.
    Koşul `db.tedavide_yapilan()` -- zaman çizelgesiyle aynı (v6.146).
    """
    kosul, p = db.tedavide_yapilan(cycle_id)
    return {r["d"]: r["n"] for r in db.sorgu(
        f"SELECT o.{alan} d, COUNT(DISTINCT o.specimen_id) n FROM olay o "
        f"WHERE o.tip = ? AND o.iptal_mi = 0 {ek} AND {kosul} "
        f"GROUP BY o.{alan}", [tip] + p)}


def _oosit_sayilari(cycle_id):
    """Maturasyon kodlarına göre oosit sayıları (mii / mi / gv / …)."""
    return _bu_tedavide_say(cycle_id, "mat_deger", "maturasyon_kontrolu")


def _pn_sayilari(cycle_id):
    return _bu_tedavide_say(cycle_id, "fert_pn_sayisi", "fertilizasyon_kontrolu")


def _bu_tedavide_adet(cycle_id, tip_kosulu) -> int:
    """Bu tedavide yapılan, koşulu tutan olayların DISTINCT örnek sayısı."""
    kosul, p = db.tedavide_yapilan(cycle_id)
    return db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        f"WHERE o.iptal_mi = 0 AND ({tip_kosulu}) AND {kosul}", p)["n"]


# İşlemden sonra dejenere olan yumurta: ICSI sırasında ya da fert kontrolünde.
_DEJ_ISLEM = ("(o.tip='icsi' AND o.icsi_sonuc='degenere') OR "
              "(o.tip='fertilizasyon_kontrolu' AND o.fert_sonuc='degenere')")


def _transfer_edilenler(cycle_id):
    """Bu cycle'da transfer edilen embriyolar, aşaması ve skoruyla.

    Ölçü `tr_cycle_id`: FET'te embriyo başka cycle'dan gelir, transferin
    yapıldığı cycle burasıdır (bkz. CLAUDE.md "Embriyo cycle değiştirmez").
    """
    return db.sorgu(
        "SELECT s.id, s.cycle_sira_no, o.zaman, o.tr_tipi, "
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id = s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS bl_skor, "
        "  (SELECT b.bl_genisleme FROM olay b WHERE b.specimen_id = s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS bl_genisleme, "
        f"  (SELECT {db.cl_hucre_ifadesi('cl')} FROM olay cl WHERE cl.specimen_id = s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        "   ORDER BY cl.gun DESC LIMIT 1) AS hucre, "
        "  (SELECT cl.cl_skor FROM olay cl WHERE cl.specimen_id = s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        "   ORDER BY cl.gun DESC LIMIT 1) AS cl_skor, "
        "  (SELECT cl.gun FROM olay cl WHERE cl.specimen_id = s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        "   ORDER BY cl.gun DESC LIMIT 1) AS cl_gun "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 "
        "  AND COALESCE(o.tr_cycle_id, s.cycle_id) = ? "
        "ORDER BY s.cycle_sira_no", (cycle_id,))


# ------------------------------------------------ dondurulan örnekler, tüp tüp
#
# **Bir tüp = bir `tasiyici`** (v6.135, kullanıcının isteği). Vitrifikasyon
# olayı `vit_tasiyici_id` ile taşıyıcıya bağlı; aynı taşıyıcıya yazılmış
# örnekler aynı tüptedir. Kullanıcının kendi yazım geleneği de bu: Access
# notlarında "2 ADET D5 EMBRİYO (3AA) (3AA)" -- **bir parantez bir tüp**
# (aynı kural `aktar_access.py`'de de var, v6.132).
#
# İki form da aynı üç soruyu soruyor: kaç tüp, içinde ne, hangi gün. Cevap
# BURADA tek yerde duruyor -- iki kopya olsaydı Özet'in NOTLAR'ı ile ART
# Lab'ın FREEZE sütunu birbirini tutmazdı.

def dondurma_tupleri(cycle_id: int) -> list:
    """Bu tedavide dondurulan örnekler, tüp tüp.

    "Bu tedavide" = dondurmanın YAPILDIĞI tedavi (v6.143, `db.vit_tedavisi()`),
    örneğin kaynağı değil. FET'te çözülüp yeniden dondurulan embriyonun ikinci
    tüpü FET'in resmî formunda çıkar; kaynak ICSI tedavisinin formuna o
    tedavide dondurulmuş gibi yazılmaz -- resmî forma yanlış bilgi yazmak
    boş bırakmaktan kötü.

    Her öğe: `{"etiket", "ogeler": [kalite|None], "gunler": [int],
    "aktarim": bool, "yumurta": bool}` -- `aktarim`: tüp `aktar_access.py`'nin
    Access notundan yazdığı bir dondurma (v6.159; `db.KAYNAK_DONDURMA_NOTU`);
    `yumurta`: tüpte yumurta mı var (v6.167, `db.dondurulan_yumurta_sql()`,
    tüpün ilk örneğinden -- bir tüp tek tedavinin tek türünü taşıyor).
    `ogeler` tüpteki **her** örnek için bir giriş taşır; kalitesi
    kaydedilmemişse `None` (yumurta dondurmada hiçbirinin skoru olmaz).
    `olgunluk` (v6.169) aynı sırayla her örneğin dondurmadan önceki son
    maturasyonu, kodla (`_yumurta_olgunlugu()`); yumurta tüpünün parantezi
    ondan kuruluyor (`tup_metni()`).
    """
    # Kalite bu tedavinin değerlendirmesinden, yoksa en sonuncudan (v6.148,
    # `db.bu_tedavinin_skoru()`): embriyo sonra bir FET'te yeniden
    # değerlendirildiyse kaynak tedavinin formuna FET'in skoru yazılmasın.
    return _tuplere_topla(_dondurma_satirlari(
        f"{db.vit_tedavisi('o')} = ?", (cycle_id,), str(int(cycle_id))))


def tup_icerikleri(tasiyici_idler) -> dict:
    """Tüplerin içeriği -- `dondurma_tupleri()`'nin tüp tüp hali (v6.189).

    -> {taşıyıcı id: tüp} (öğeleri `dondurma_tupleri()`'ninkiyle aynı). Cryo
    Haritası'nın goblet görünümü ve Excel haritası soruyor; kalite her tüpün
    KENDİ dondurmasının tedavisinden (`db.bu_tedavinin_skoru()`), formlarla
    aynı kural -- iki yerde iki ayrı yazım olmasın.
    """
    sonuc = {}
    idler = [int(x) for x in tasiyici_idler]
    for i in range(0, len(idler), 500):          # SQLite'ın parametre sınırı
        parca = idler[i:i + 500]
        yer = ",".join("?" * len(parca))
        for t in _tuplere_topla(_dondurma_satirlari(
                f"o.vit_tasiyici_id IN ({yer})", tuple(parca), db.vit_tedavisi("o"))):
            sonuc[t["tup"]] = t
    return sonuc


def _dondurma_satirlari(kosul, parametre, tedavi):
    """Dondurma olayları, örnek örnek, kalite ve olgunlukla. `kosul` ve
    `tedavi` (kalitenin tedavisi, SQL ifadesi) koddan gelir."""
    bu = f"AND {db.bu_tedavinin_skoru(tedavi, 'x')}"
    return db.sorgu(
        f"""
        SELECT o.vit_tasiyici_id AS tup, t.etiket, s.cycle_sira_no,
               o.notlar LIKE ? || '%' AS aktarim,
               {db.dondurulan_yumurta_sql('o')} AS yumurta,
               {_olgunluk_sql()} AS mat,
               {son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC', bu)}
                 AS bl_skor,
               {son_alt('gun', 'blastokist_degerlendirme', 'x.gun DESC', bu)}
                 AS bl_gun,
               {son_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme',
                        'x.gun DESC', bu)} AS cl_hucre,
               {son_alt('cl_skor', 'cleavage_degerlendirme', 'x.gun DESC', bu)}
                 AS cl_skor,
               {son_alt('gun', 'cleavage_degerlendirme', 'x.gun DESC', bu)}
                 AS cl_gun
          FROM olay o JOIN specimen s ON s.id = o.specimen_id
          LEFT JOIN tasiyici t ON t.id = o.vit_tasiyici_id
         WHERE {kosul} AND o.tip='vitrifikasyon'
           AND o.iptal_mi = 0
         ORDER BY o.vit_tasiyici_id, s.cycle_sira_no
        """, (db.KAYNAK_DONDURMA_NOTU, *parametre))


def _tuplere_topla(satirlar) -> list:
    tupler, sira = [], {}
    for r in satirlar:
        # Taşıyıcısı olmayan eski bir kayıt tek bir "tüp" sayılır: uydurma
        # bir tüp bölmesi açmaktansa hepsini bir parantezde toplamak dürüst.
        anahtar = r["tup"] or 0
        if anahtar not in sira:
            sira[anahtar] = len(tupler)
            tupler.append({"tup": r["tup"], "etiket": r["etiket"], "ogeler": [],
                           "gunler": [], "olgunluk": [], "aktarim": True,
                           "yumurta": bool(r["yumurta"])})
        t = tupler[sira[anahtar]]
        t["ogeler"].append(_dondurma_kalitesi(r))
        # Olgunluk yalnızca yumurtada: skoru kayıtlı olmayan bir embriyo
        # tüpü "(2*MII)" basmasın -- embriyonun MII'si ICSI'den önceki hali.
        t["olgunluk"].append(r["mat"] if r["yumurta"] else None)
        # Tüp Access notundan mı yazıldı (v6.159): hepsi öyleyse evet.
        t["aktarim"] = t["aktarim"] and bool(r["aktarim"])
        gun = r["bl_gun"] if r["bl_skor"] or r["bl_gun"] else r["cl_gun"]
        if gun and gun not in t["gunler"]:
            t["gunler"].append(gun)
    return tupler


def _sar(metin, genislik=68):
    """NOTLAR satırını sarar (`textwrap.fill`, 68 -- kutu `white-space: pre`,
    uzun satır sessizce kesilir, v6.130). Bir kalite ve bir tüp parantezi
    ortasından bölünmez (v6.157): "(Birleşme G3)" iki satıra düşüp
    "(Birleşme" / "G3)" okunuyordu. Bölünmeyecek boşluklar geçici olarak
    bölünmez boşluk oluyor -- textwrap onu kelimenin parçası sayıyor."""
    nb = "\u00a0"
    metin = metin.replace(f"{db.BIRLESME} G", f"{db.BIRLESME}{nb}G")
    metin = re.sub(r"\([^()]*\)", lambda m: m.group(0).replace(" ", nb), metin)
    return textwrap.fill(metin, genislik).replace(nb, " ")


def _dondurma_kalitesi(r):
    """Dondurulan bir örneğin kalitesi -- laboratuvarın kendi yazımıyla.

    Blastokistte `bl_skor` ("3AA", "KAV2"); cleavage'da hücre sayısı + skor
    ("8HG2"; birleşmede "Birleşme G2", v6.157, `db.cleavage_yazimi()`). İkisi de kullanıcının Access notlarında aynen böyle yazılıydı,
    `aktar_access.py` de tam bu kalıbı çözümlüyor -- form da aynı dili
    konuşsun diye. Kaydı yoksa `None`, uydurulmuyor.
    """
    if r["bl_skor"]:
        return r["bl_skor"]
    return db.cleavage_yazimi(r["cl_hucre"], r["cl_skor"])


def tup_metni(tup) -> str:
    """Bir tüpün parantezi: `(4HG2-4HG2-3HG2)`.

    Ayraç **tire**, kullanıcının kendi yazımı: Access notlarında bir tüpteki
    üç embriyo "(4HG2-4HG2-3HG2)", ayrı tüpler ise "(3AA) (3AA)" diye
    yazılıydı. ART Lab'ın FREEZE kutusu dar olduğu için de virgül+boşluktan
    kısa olması işe yarıyor.

    Hiçbir örneğin kalitesi kayıtlı değilse (yumurta dondurma) parantez
    yumurtaların **olgunluğunu** sayısıyla taşır (v6.169, kullanıcının
    isteği: "Sadece rakam yazıyor. Detay yazsın"): `(5*MII)`, karışıksa
    `(4*MII-1*MI)` -- kullanıcının Access'teki kendi yazımı ("(5*M2)"),
    etiket `liste_degeri`'nden. Olgunluğu kayıtlı olmayan yumurta `?`
    (`(2*MII-1*?)`); hiçbirininki yoksa v6.135'teki gibi yalnızca sayı,
    `(4)` -- uydurulacak bir şey yok. Bazısının kalitesi varsa eksik olanlar
    `?` ile görünür: sessizce düşürmek "bu tüpte bir tane var" derdi.
    """
    if all(o is None for o in tup["ogeler"]):
        olg = tup.get("olgunluk") or []
        if any(olg):
            return "(" + _olgunluk_metni(olg) + ")"
        return f"({len(tup['ogeler'])})"
    return "(" + "-".join(o or "?" for o in tup["ogeler"]) + ")"


def _olgunluk_metni(kodlar) -> str:
    """Bir tüpteki yumurtaların olgunluğu: "4*MII-1*MI" (v6.169).

    MII önce, ötekiler ilk göründükleri sırayla, bilinmeyen (`None`) en sonda
    "?" ile. Etiket `liste_degeri`'nden (kodu değil etiketi göster)."""
    h = _etiketler()
    sayim = {}
    for k in kodlar:
        sayim[k] = sayim.get(k, 0) + 1
    sira = sorted(sayim, key=lambda k: (k is None, k != "mii"))
    return "-".join(f"{sayim[k]}*{_et(h, 'maturasyon', k) if k else '?'}"
                    for k in sira)


def _olgunluk_sql(s="s", o="o") -> str:
    """Dondurulan yumurtanın olgunluğu -- alt sorgu (v6.169, v6.171).

    `s`: örnek, `o`: dondurma olayı (dış sorgunun takma adları). Önce
    DONDURMANIN YAPILDIĞI tedavideki maturasyon, giriş sırasına bakmadan
    (`db.olay_tedavisi()`): Yumurta Dondurma'da olgunluk denüdasyon ekranında
    dondurmadan sonra da işaretlenebiliyor. v6.169 yalnızca dondurmadan önce
    girileni okuyordu; kullanıcının 2026-0001 tedavisinde form yalnızca
    sayı basıyordu. O tedavide maturasyon yoksa dondurmadan önceki son
    maturasyon (kimlik sırası, v6.143) -- Yumurta Çözme'de sonradan başka
    tedavide yapılan değerlendirme tüpün içeriği değil."""
    # İki alt sorgu: SQLite iç sorgunun ORDER BY'ında dış kolona izin vermiyor.
    def alt(kosul):
        return (f"(SELECT x.mat_deger FROM olay x WHERE x.specimen_id = {s}.id "
                f"AND x.tip = 'maturasyon_kontrolu' AND x.iptal_mi = 0 "
                f"AND {kosul} ORDER BY x.id DESC LIMIT 1)")
    burada = f"{db.olay_tedavisi('x')} = {db.vit_tedavisi(o)}"
    return (f"COALESCE({alt(burada)}, "
            f"{alt(f'x.id < {o}.id')})")


def _yumurta_olgunlugu(specimen_id, vit_olay_id):
    """Bir dondurmanın yumurtasının olgunluğu, kodla (`_olgunluk_sql()`)."""
    if vit_olay_id is None:
        return None
    r = db.tek(
        f"SELECT {_olgunluk_sql()} AS mat FROM olay o "
        "JOIN specimen s ON s.id = o.specimen_id WHERE o.id = ?",
        (vit_olay_id,))
    return r["mat"] if r else None


def dondurma_gunleri(tupler) -> str | None:
    """Dondurma günü: "5. gün", birden çok gün varsa "5. gün, 6. gün".

    Gün, örneğin **kendi son değerlendirmesinin** günü (blastokist, yoksa
    cleavage) -- programda "kaçıncı günde donduruldu" diye ayrı bir alan
    yok ve uydurulmuyor. Değerlendirmesi olmayan örnek (yumurta dondurma)
    güne hiç katkı vermez, kutu boş kalır.
    """
    gunler = sorted({g for t in tupler for g in t["gunler"]})
    return ", ".join(f"{g}. gün" for g in gunler) or None


# ART Lab'ın FREEZE sütununda kâğıt dört kutu veriyor (satır 28-31).
_ARTLAB_FREEZE_SATIR = (28, 29, 30, 31)
_ARTLAB_FREEZE_SUTUN = 12

# Kâğıdın altındaki "Raporu dolduran ... Yorum:" satırı: tek birleşik hücre,
# sayfanın tamamı kadar geniş. Tedavinin genel bulguları oraya ekleniyor
# (v6.200; ICSI'si olmayan tipte yumurta bulguları, v6.135).
_ARTLAB_YORUM_SATIR = 36

# FREEZE kutusu bir oosit sütunu kadar dar; bir tüpte üç embriyo varsa
# ("(4HG2-4HG2-3HG2)", ağustostaki gerçek kayıt) metin sığmıyordu ve
# `.kalip td`'nin `overflow: hidden`'ı onu **sessizce kesiyordu**.
# Kullanıcının kararı: "Thaw ve onun[ki] alana kadar satırı uzatabilirsin" --
# yani metin sağa, boş komşu kutulara taşsın. Excel zaten böyle davranıyor
# (dolu bir hücrenin yazısı boş komşusuna akar); ekranda aynısını yapmak
# için bu hücrelerin `overflow`'u açılıyor (`.tasabilir`, style.css).
# Kırpmak yerine taşırmak bilinçli: kesilen bir skor yanlış bilgi olurdu.


def _transfer_satirlari(cycle_id, cozulenler) -> list:
    """ART Lab'ın "Uterus grade (x sayı)" kutuları (v6.152).

    Kâğıdın başlığı "grade (x sayı)": aynı kalitede embriyolar tek satırda
    sayılarıyla -- "3AA x2 · %90-%85". Kalite embriyonun transferdeki son
    değerlendirmesi; canlılık oranı bu tedavideki çözmeden (taze transferde
    çözme yok, oran da yok). Kalitesi kayıtlı olmayan embriyo "?" ile, kutu
    boş kalıp "transfer yok" demesin.
    """
    oran = {o["kod"]: o["canlilik"] for o in cozulenler}
    gruplar = {}
    for r in _transfer_edilenler(cycle_id):
        k = _ornek_kalitesi(r["id"]) or "?"
        g = gruplar.setdefault(k, [])
        g.append(oran.get(r["id"]))
    satirlar = []
    for k, oranlar in gruplar.items():
        m = f"{k} x{len(oranlar)}"
        yuzdeler = "-".join(x for x in oranlar if x)
        satirlar.append(f"{m} · {yuzdeler}" if yuzdeler else m)
    return satirlar


def _bulgu_notu(c, h) -> str:
    """Yumurta bulguları, ART Lab'ın alttaki geniş "Yorum:" satırı için.

    v6.200'den beri yalnızca ICSI'si olmayan tipte (Yumurta Dondurma):
    ICSI'li tipte o satıra tedavinin genel bulguları yazılıyor
    (`db.tedavi_bulgu_metni()`, kullanıcının isteği).

    "1: Vakuol, Geniş PVS · 3: Kalın zona" -- hangi yumurtanın bulgusu
    olduğu numarasıyla yazılıyor, çünkü bu satır tek ve bütün tedaviyi
    kapsıyor. Izgaradaki dar "Yorum" kutusuna sığmadığı için buraya kondu
    (v6.135, kullanıcıya soruldu).

    Bulgu iki aşamada da girilebiliyor -- `ivf_icsi`'de ICSI ekranında,
    `oosit_cryo`'da denüdasyonda (v6.96) -- bu yüzden aşama süzülmüyor;
    aynı bulgu iki aşamada da işaretliyse bir kez yazılıyor. Yumurtalar
    ızgaranınkiler (`yumurta_kosulu()`, v6.147): Yumurta Çözme'de çözülen
    yumurtaların bulguları -- dondurmadan önce denüdasyonda işaretlenenler de,
    yumurtanın kendi morfolojisi.
    """
    bulgular = {}
    for r in db.sorgu(
            "SELECT s.cycle_sira_no, sb.bulgu_kodu FROM specimen_bulgu sb "
            "JOIN specimen s ON s.id = sb.specimen_id "
            f"WHERE {yumurta_kosulu(c)} ORDER BY s.cycle_id, s.cycle_sira_no, sb.id",
            (c["id"],)):
        liste = bulgular.setdefault(r["cycle_sira_no"], [])
        e = _et(h, "bulgu_icsi", r["bulgu_kodu"])
        if e and e not in liste:
            liste.append(e)
    return " · ".join(f"{no}: {', '.join(b)}"
                      for no, b in sorted(bulgular.items()) if b)


def dondurma_notu(cycle_id: int, cycle_tipi, tupler) -> str | None:
    """NOTLAR kutusuna giren dondurma satırı (v6.135, kullanıcının isteği).

    "Dondurulan: 2 embriyo, 5. gün, 2 tüp: (3AA) (3AA)" -- kullanıcının
    Access'te kendi yazdığı cümlenin aynısı. Satır 68 karakterde sarılıyor:
    NOTLAR kutusu `white-space: pre`, uzun satır sarmaz, **sessizce kesilir**
    (v6.130'un kuralı). Nota bir şey eklersen formu açıp bak (tuzak #5).
    """
    if not tupler:
        return None
    # Yumurta mı embriyo mu tüpün içeriğinden (v6.167): Access'ten aktarılan
    # IVF/ICSI tedavisinde ICSI'ye alınmayan yumurtalar da dondurulmuş, bir
    # Yumurta Dondurma'da ICSI'den bir blastokist -- tedavinin tipi ikisine
    # de yanlış ad verirdi. Tek türse cümle v6.135'teki gibi; ikisi birden
    # varsa embriyo önce, "; " ile ayrı iki parça.
    parcalar = []
    for yumurta in (False, True):
        grup = [t for t in tupler if t.get("yumurta", False) == yumurta]
        if not grup:
            continue
        adet = sum(len(t["ogeler"]) for t in grup)
        parca = [f"{adet} {'yumurta' if yumurta else 'embriyo'}"]
        gun = dondurma_gunleri(grup)
        if gun:
            parca.append(gun)
        parca.append(f"{len(grup)} tüp")
        parcalar.append(", ".join(parca) + ": "
                        + " ".join(tup_metni(t) for t in grup))
    return _sar("Dondurulan: " + "; ".join(parcalar))


# ------------------------------------------------ çözülen örnekler (v6.152)
#
# Kullanıcının isteği: "FET çözme tedavilerinde formlara işlem geçmiyor."
# İki form da yalnızca çözülen embriyoların SAYISINI basıyordu; hangi
# embriyonun çözüldüğü, canlılığı, transfer mi yeniden dondurma mı olduğu ve
# geriye dondurulmuş embriyo kalıp kalmadığı hiçbir yerde yazmıyordu. Soru
# tek yerde cevaplanıyor -- Özet'in kutuları ve NOTLAR'ı, ART Lab'ın THAW ve
# TRANSFER sütunları buradan okuyor, birbirini tutsunlar diye
# (`dondurma_tupleri()`'nin gerekçesi).


def _yuzde(x):
    """Canlılık oranı: 90.0 -> "%90", 87.5 -> "%87.5". Yuvarlama yok."""
    if x is None or x == "":
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return f"%{x}"
    return f"%{int(f)}" if f.is_integer() else f"%{f:g}"


def _ornek_kalitesi(specimen_id, tedavi_id=None):
    """Bir örneğin kalitesi, `_dondurma_kalitesi()`'nin yazımıyla.

    `tedavi_id` verilirse o tedavinin değerlendirmesi (`db.bu_tedavinin_skoru()`,
    v6.148) -- çözülen embriyonun tüpe konduğu andaki skoru, dondurmanın
    yapıldığı tedaviden. Verilmezse en son değerlendirme.
    """
    bu = (f"AND {db.bu_tedavinin_skoru(str(int(tedavi_id)), 'x')}"
          if tedavi_id is not None else "")
    r = db.tek(
        f"""
        SELECT {son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC', bu)}
                 AS bl_skor,
               {son_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme',
                        'x.gun DESC', bu)} AS cl_hucre,
               {son_alt('cl_skor', 'cleavage_degerlendirme', 'x.gun DESC', bu)}
                 AS cl_skor
          FROM specimen s WHERE s.id = ?
        """, (specimen_id,))
    return _dondurma_kalitesi(r) if r else None


def cozulen_ornekler(cycle_id: int) -> list:
    """Bu tedavi için çözülen örnekler, çözme sırasıyla.

    "Bu tedavi için" = `COALESCE(thaw_cycle_id, specimen.cycle_id)`, Özet'in
    v6.102'den beri kullandığı koşul. Her öğe: örnek kodu (`specimen.id`),
    tüp (çözmenin boşalttığı taşıyıcı, v6.143; yoksa önceki dondurmanınki),
    tüpe konduğu andaki kalite, sağkalım etiketi, canlılık oranı ve bu
    tedavide ne olduğu (transfer / yeniden dondurma).
    """
    tup_kolonu = ("o.thaw_tasiyici_id" if db.cozme_tupu_var() else "NULL")
    satirlar = db.sorgu(
        f"""
        SELECT o.id, o.specimen_id, o.zaman, o.thaw_sagkalim, o.thaw_canlilik,
               {tup_kolonu} AS cozme_tupu, s.cycle_sira_no
          FROM olay o JOIN specimen s ON s.id = o.specimen_id
         WHERE o.tip = 'thaw' AND o.iptal_mi = 0
           AND COALESCE(o.thaw_cycle_id, s.cycle_id) = ?
         ORDER BY o.zaman, o.id
        """, (cycle_id,))
    h = _etiketler()
    vt = db.vit_tedavisi("v")
    sonuc = []
    for r in satirlar:
        # Tüpe konduğu dondurma: bu çözmeden ÖNCEKİ son dondurma (kimlik
        # sırası, v6.143'ün kuralı). Access'ten aktarılan FET'in kendi altına
        # açılan embriyolarının dondurması yok (v6.130) -- tüpsüz, kalite
        # son değerlendirmeden.
        v = db.tek(
            f"SELECT v.id, v.vit_tasiyici_id, {vt} AS vit_cid, t.etiket, "
            f"{db.dondurulan_yumurta_sql('v')} AS yumurta "
            "FROM olay v LEFT JOIN tasiyici t ON t.id = v.vit_tasiyici_id "
            "WHERE v.specimen_id = ? AND v.tip = 'vitrifikasyon' "
            "AND v.iptal_mi = 0 AND v.id < ? ORDER BY v.id DESC LIMIT 1",
            (r["specimen_id"], r["id"]))
        tup = r["cozme_tupu"] or (v["vit_tasiyici_id"] if v else None)
        etiket = v["etiket"] if v and v["vit_tasiyici_id"] == tup else None
        if tup and not etiket:
            t = db.tek("SELECT etiket FROM tasiyici WHERE id = ?", (tup,))
            etiket = t["etiket"] if t else None
        transfer = db.tek(
            "SELECT 1 FROM olay x JOIN specimen s ON s.id = x.specimen_id "
            "WHERE x.specimen_id = ? AND x.tip = 'transfer' AND x.iptal_mi = 0 "
            "AND COALESCE(x.tr_cycle_id, s.cycle_id) = ? AND x.id > ?",
            (r["specimen_id"], cycle_id, r["id"])) is not None
        yeniden = db.tek(
            f"SELECT 1 FROM olay v WHERE v.specimen_id = ? "
            f"AND v.tip = 'vitrifikasyon' AND v.iptal_mi = 0 "
            f"AND {vt} = ? AND v.id > ?",
            (r["specimen_id"], cycle_id, r["id"])) is not None
        sonuc.append({
            "kod": r["specimen_id"],
            "tup": tup,
            "etiket": etiket,
            "kalite": _ornek_kalitesi(r["specimen_id"],
                                      v["vit_cid"] if v else None),
            "olgunluk": (_yumurta_olgunlugu(r["specimen_id"], v["id"])
                         if v and v["yumurta"] else None),
            "sagkalim": _et(h, "thaw_sagkalim", r["thaw_sagkalim"]),
            "canlilik": _yuzde(r["thaw_canlilik"]),
            "transfer": transfer,
            "yeniden": yeniden,
        })
    return sonuc


def cozulen_tupler(cozulenler) -> list:
    """Çözülen örnekler tüp tüp -- `dondurma_tupleri()`'nin biçimiyle, ki
    `tup_metni()` ikisini de aynı parantezle bassın."""
    tupler, sira = [], {}
    for o in cozulenler:
        anahtar = o["tup"] or 0
        if anahtar not in sira:
            sira[anahtar] = len(tupler)
            tupler.append({"etiket": o["etiket"], "ogeler": [], "gunler": [],
                           "olgunluk": []})
        tupler[sira[anahtar]]["ogeler"].append(o["kalite"])
        tupler[sira[anahtar]]["olgunluk"].append(o.get("olgunluk"))
    return tupler


def cozme_viabilitesi(cozulenler) -> str | None:
    """ÇÖZDÜRME SONRASI VİABİLİTE kutusu: "2 Canlı, 1 Dejenere · %90-%80".

    Sağkalım etiketleri sayılarıyla (ekrandaki seçenekler), girilmişse
    canlılık oranları embriyo embriyo, çözme sırasıyla. Ortalama alınmıyor:
    resmî forma programın hesapladığı bir sayı değil, girilen yazılsın.
    """
    sayim = {}
    for o in cozulenler:
        if o["sagkalim"]:
            sayim[o["sagkalim"]] = sayim.get(o["sagkalim"], 0) + 1
    parca = ", ".join(f"{n} {e}" for e, n in sayim.items())
    oranlar = "-".join(o["canlilik"] for o in cozulenler if o["canlilik"])
    return " · ".join(p for p in (parca, oranlar) if p) or None


def _son_islem_ani(cycle_id: int):
    """(hasta id, bu tedavinin son işleminin anı) -- "Kalan dondurulmuş"un
    ölçüsü (v6.152). Tedavide işlem yoksa None."""
    kosul, par = db.tedavide_yapilan(cycle_id)
    son = db.tek(
        f"SELECT MAX(o.zaman) z FROM olay o JOIN specimen s "
        f"ON s.id = o.specimen_id WHERE o.iptal_mi = 0 AND {kosul}", par)
    c = db.tek("SELECT hasta_id FROM cycle WHERE id = ?", (cycle_id,))
    if not son or not son["z"] or not c:
        return None
    return c["hasta_id"], son["z"]


def _gonderim_var() -> bool:
    """`goc_051` (v6.182) çalıştı mı -- yoksa formlar eski haliyle."""
    return db.kolon_var("tasiyici", "gonderim_zamani")


def tasinan_tupler(kosul: str, par) -> list:
    """Başka merkeze taşınan tüpler (v6.182), içindekilerle: `tup_metni()`'nin
    beklediği sözlük + gün, yer, yumurta mı. `kosul` dondurma olayı `v`,
    örnek `s`, tedavi `c`, taşıyıcı `t` üzerinden. v6.205'ten beri tüpün
    kimliği, etiketi ve dondurulduğu tedavi (`tedavi`, `db.vit_tedavisi()`)
    de dönüyor: hasta kartının tedavi satırı aynı tüpleri basıyor."""
    if not _gonderim_var():
        return []
    vt = db.vit_tedavisi("v")
    satirlar = db.sorgu(
        f"""
        SELECT v.id, v.specimen_id, v.vit_tasiyici_id AS tup, {vt} AS vit_cid,
               {db.dondurulan_yumurta_sql('v')} AS yumurta, t.etiket,
               t.gonderim_zamani AS gun, t.gonderim_yeri AS yer
          FROM olay v JOIN specimen s ON s.id = v.specimen_id
          JOIN cycle c ON c.id = s.cycle_id
          JOIN tasiyici t ON t.id = v.vit_tasiyici_id
         WHERE v.tip = 'vitrifikasyon' AND v.iptal_mi = 0
           AND t.durum = 'gonderildi' AND {kosul}
         ORDER BY t.gonderim_zamani, v.zaman, v.id
        """, par)
    tupler = {}
    for r in satirlar:
        tp = tupler.setdefault(r["tup"], {
            "tup": r["tup"], "etiket": r["etiket"], "tedavi": r["vit_cid"],
            "gun": r["gun"], "yer": r["yer"], "yumurta": bool(r["yumurta"]),
            "ogeler": [], "olgunluk": []})
        tp["ogeler"].append(_ornek_kalitesi(r["specimen_id"], r["vit_cid"]))
        tp["olgunluk"].append(_yumurta_olgunlugu(r["specimen_id"], r["id"])
                              if r["yumurta"] else None)
    return list(tupler.values())


def tasinan_notu(tupler) -> str | None:
    """NOTLAR satırı (v6.182, kullanıcının isteği: "1 tüp 12.03.2025
    tarihinde şuraya taşındı şeklinde yazsın"):

        Taşınan: 3 embriyo, 1 tüp: (8HG2-8HG2-6HG2) 12.03.2025 tarihinde
        Memorial Hastanesi'ne taşındı.

    Yer kullanıcının yazdığı gibi (ekiyle: "...Hastanesi'ne"); program ek
    uydurmuyor, yazılmamışsa "başka merkeze". Aynı gün ve yere giden tüpler
    tek cümle. İçerik "Dondurulan:" satırının yazımıyla (`tup_metni()`).
    """
    if not tupler:
        return None
    gruplar = {}
    for tp in tupler:
        gruplar.setdefault((tp["gun"], tp["yer"]), []).append(tp)
    cumleler = []
    for (gun, yer), tuplar in gruplar.items():
        parcalar = []
        for ad, yumurta in (("embriyo", False), ("yumurta", True)):
            bunlar = [tp for tp in tuplar if tp["yumurta"] == yumurta]
            if bunlar:
                adet = sum(len(tp["ogeler"]) for tp in bunlar)
                parcalar.append(f"{adet} {ad}, {len(bunlar)} tüp: "
                                + " ".join(tup_metni(tp) for tp in bunlar))
        cumleler.append("; ".join(parcalar)
                        + f" {_gg_aa_yyyy(gun) or gun} tarihinde "
                        + f"{yer or 'başka merkeze'} taşındı.")
    return _sar("Taşınan: " + " ".join(cumleler))


def _kalan_dondurulmus(cycle_id: int, cozulenler) -> str:
    """Bu tedaviden sonra hastanın tankta kalan örnekleri, NOTLAR için.

    Ölçü **bu tedavinin son işleminin anı** -- bugünün tankı değil: form
    aylar sonra basılsa da o gün ne kaldığını söylesin. O ana kadar
    dondurulmuş (bu tedavide yeniden dondurulan dahil) ve o ana kadar
    çözülmemiş örnekler. Tüpü yalnızca çözme boşaltıyor; bir dondurmanın
    çözülüp çözülmediği kimlik sırasıyla (dondurmadan sonraki bir çözme,
    v6.143'ün kuralı), yani yeniden dondurulan embriyonun ilk tüpü sayılmıyor.

    v6.159 (kullanıcının isteği: "Yazı kod yazmasın. Tüp içinde embriyo
    bilgisi parantez ile belirtilsin. Embriyo bilgisi tek sefer yazılsın"):
    - Tüpler etiketle (kodla) değil içindekiyle yazılıyor: "(4AA) (3BB)".
    - **Bu tedavide dondurulan tüpler tekrar edilmiyor** -- "Dondurulan:"
      satırında ya da Access notunda zaten yazılı; "bu tedavide dondurulan
      2 tüp" diye sayılıyor.
    - **Bilinmiyorsa hiç yazılmıyor.** Çözülen bir embriyonun dondurması
      programda yoksa (kaynak tedavisi Access'ten aktarılmamış FET, v6.130)
      hastanın tankı programda eksik: "Kalan dondurulmuş embriyo yok"
      demek yanlış olurdu -- o tedavilerin notu "GERİDE 7 TÜPTE 7 ADET D5
      EMBRİYOSU KALDI" derken form "yok" basıyordu.
    """
    if any(o["tup"] is None for o in cozulenler):
        return ""
    an = _son_islem_ani(cycle_id)
    if not an:
        return ""
    hasta_id, t = an
    vt = db.vit_tedavisi("v")
    # O güne kadar başka merkeze taşınmış tüp tankta değil (v6.182). Gün
    # ölçüsü: taşımadan önceki bir işlemin formunda tüp hâlâ kalan.
    gitmedi, gpar = "", ()
    if _gonderim_var():
        gitmedi = ("AND NOT EXISTS (SELECT 1 FROM tasiyici g WHERE "
                   "g.id = v.vit_tasiyici_id AND g.durum = 'gonderildi' "
                   "AND g.gonderim_zamani <= ?)")
        gpar = (t,)
    satirlar = db.sorgu(
        f"""
        SELECT v.id, v.vit_tasiyici_id AS tup, v.specimen_id, {vt} AS vit_cid,
               {db.dondurulan_yumurta_sql('v')} AS yumurta
          FROM olay v JOIN specimen s ON s.id = v.specimen_id
          JOIN cycle c ON c.id = s.cycle_id
         WHERE c.hasta_id = ? AND v.tip = 'vitrifikasyon' AND v.iptal_mi = 0
           AND v.zaman <= ?
           AND NOT EXISTS (SELECT 1 FROM olay z WHERE z.specimen_id = v.specimen_id
                 AND z.tip = 'thaw' AND z.iptal_mi = 0 AND z.id > v.id
                 AND z.zaman <= ?)
           {gitmedi}
         ORDER BY v.zaman, v.id
        """, (hasta_id, t, t, *gpar))
    # "embriyo"/"yumurta" -> örnek sayısı, bu tedavide dondurulan tüpler,
    # öteki tüpler (tüp -> içindekilerin kalitesi, sırasıyla)
    gruplar = {}
    for r in satirlar:
        # İçerikten (v6.167, `db.dondurulan_yumurta_sql()`), tipten değil
        ad = "yumurta" if r["yumurta"] else "embriyo"
        g = gruplar.setdefault(ad, {"adet": 0, "burada": set(), "oteki": {}})
        g["adet"] += 1
        tup = r["tup"] or ("tupsuz", r["vit_cid"])
        if r["vit_cid"] == cycle_id:
            g["burada"].add(tup)
        else:
            o = g["oteki"].setdefault(tup, {"ogeler": [], "olgunluk": []})
            o["ogeler"].append(_ornek_kalitesi(r["specimen_id"], r["vit_cid"]))
            o["olgunluk"].append(_yumurta_olgunlugu(r["specimen_id"], r["id"])
                                 if r["yumurta"] else None)
    if not gruplar:
        return "Kalan dondurulmuş embriyo yok."
    parcalar = []
    for ad in ("embriyo", "yumurta"):
        g = gruplar.get(ad)
        if not g:
            continue
        tup_sayisi = len(g["burada"]) + len(g["oteki"])
        icerik = []
        if g["burada"]:
            icerik.append(f"bu tedavide dondurulan {len(g['burada'])} tüp")
        if g["oteki"]:
            icerik.append(" ".join(tup_metni(o) for o in g["oteki"].values()))
        parcalar.append(f"{g['adet']} {ad}, {tup_sayisi} tüp: "
                        + ", ".join(icerik))
    return "Kalan dondurulmuş: " + "; ".join(parcalar) + "."


def cozme_notu_satiri(cycle_id: int, cycle_tipi, cozulenler) -> str | None:
    """NOTLAR'a giren çözme satırları (v6.152, kullanıcının isteği: "Hangi
    embriyo çözüldü, geriye dondurulmuş embriyo kaldı mı bilgisi yazsın").

    "Çözülen: 3 embriyo, 1 tüp: (3BB-1CC-KAV3); 1 transfer, 2 yeniden
    donduruldu" ve altında "Kalan dondurulmuş: ...".

    v6.159 (kullanıcının isteği: "Yazı kod yazmasın. Tüp içinde embriyo
    bilgisi parantez ile belirtilsin. Embriyo bilgisi tek sefer yazılsın"):
    v6.152'de her embriyo örnek koduyla yazılıyordu ("2026-0004-01 8HG1
    Canlı, transfer"); kalitesi kayıtlı olmayan embriyoda satırda yalnızca
    kod kalıyordu. Artık tüp tüp parantez (`tup_metni()`, "Dondurulan:"
    satırıyla aynı yazım), ne olduklarıysa yalnızca sayıyla -- kalite
    parantezde bir kez yazılı. Sağkalım ve canlılık oranı ÇÖZDÜRME SONRASI
    VİABİLİTE kutusunda. 68 karakterde sarılı (v6.130'un kuralı).
    """
    if not cozulenler:
        return None
    ad = "yumurta" if db.yumurta_mi(cycle_tipi, "thaw") else "embriyo"
    tupler = cozulen_tupler(cozulenler)
    satir = (f"Çözülen: {len(cozulenler)} {ad}, {len(tupler)} tüp: "
             + " ".join(tup_metni(t) for t in tupler))
    sonuc = [f"{n} {ne}" for n, ne in (
        (sum(1 for o in cozulenler if o["transfer"]), "transfer"),
        (sum(1 for o in cozulenler if o["yeniden"]), "yeniden donduruldu"))
        if n]
    if sonuc:
        satir += "; " + ", ".join(sonuc)
    satirlar = [_sar(satir)]
    kalan = _kalan_dondurulmus(cycle_id, cozulenler)
    if kalan:
        satirlar.append(_sar(kalan))
        # "Kalan"dan çıkan taşınmış tüpler nereye gitti (v6.182). Bu
        # tedavide dondurulanlar değil -- onlar zaten dondurma satırının
        # altında (`ozet_verisi()`).
        an = _son_islem_ani(cycle_id)
        if an and _gonderim_var():
            vt = db.vit_tedavisi("v")
            tasinan = tasinan_notu(tasinan_tupler(
                f"c.hasta_id = ? AND v.zaman <= ? AND t.gonderim_zamani <= ? "
                f"AND {vt} <> ?", (an[0], an[1], an[1], cycle_id)))
            if tasinan:
                satirlar.append(tasinan)
    return "\n".join(satirlar)


def ozet_verisi(cycle_id: int):
    """Embriyoloji Özet Formu'nun (DH.FR.91) bütün kutuları.

    Dönen sözlüğün anahtarları formdaki kutu adları; değeri `None` olan kutu
    boş basılıyor (programda o alan yok ya da o cycle'da girilmemiş).
    """
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad, h.dogum_tarihi, h.es_adi "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?",
        (cycle_id,))
    if not c:
        return None
    h = _etiketler()
    mat = _oosit_sayilari(cycle_id)
    pn = _pn_sayilari(cycle_id)
    soyadi, adi = _ad_soyad_ayir(c["ad_soyad"])

    ornek = db.tek("SELECT * FROM sperm_ornek WHERE cycle_id=? ORDER BY id LIMIT 1",
                   (cycle_id,))
    analiz = {}
    if ornek:
        for r in db.sorgu("SELECT * FROM sperm_analiz WHERE sperm_ornek_id=?",
                          (ornek["id"],)):
            analiz[r["asama"]] = r
    bazal, sonrasi = analiz.get("bazal"), analiz.get("hazirlik_sonrasi")

    # Bu tedavide YAPILAN ICSI (v6.147, `_bu_tedavide_say()`'ın gerekçesi).
    islenen = _bu_tedavide_adet(cycle_id, "o.tip='icsi'")
    dejenere_sonrasi = _bu_tedavide_adet(cycle_id, _DEJ_ISLEM)

    tr = _transfer_edilenler(cycle_id)
    tupler = dondurma_tupleri(cycle_id)
    cozulen = db.sorgu(
        "SELECT o.thaw_sagkalim, o.thaw_notu FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id "
        "WHERE o.tip='thaw' AND o.iptal_mi=0 "
        "AND COALESCE(o.thaw_cycle_id, s.cycle_id)=?", (cycle_id,))
    # Çözülen örnekler tek tek (v6.152): hangisi, canlılığı, ne oldu, geriye
    # ne kaldı. Sayı ve viabilite kutusu da buradan -- NOTLAR'la tutsun diye.
    cozulenler = cozulen_ornekler(cycle_id)
    cozulen_satiri = cozme_notu_satiri(cycle_id, c["cycle_tipi"], cozulenler)
    # Çözme notu (v6.102): taşıyıcıdaki tüm örnekler için aynı değer
    # yazıldığından (thaw.html'in tek, paylaşılan not alanı) ilk dolu olanı
    # yeterli. Protokol notunun altına eklenir, üzerine yazmaz.
    cozme_notu = next((r["thaw_notu"] for r in cozulen if r["thaw_notu"]), None)
    # İptal sebebi de aynı kutuya, en altta eklenir (v6.104, kullanıcının
    # isteği) -- cycle iptal edilmediyse None, kutuya bir şey eklemiyor.
    iptal_notu = _iptal_notu(c)
    # Dondurulan embriyolar da NOTLAR'a (v6.135, kullanıcının isteği).
    # Sıra klinik akış: protokol -> dondurma -> çözme -> iptal sebebi.
    # Çözülen örneklerin satırı (v6.152) çözme notunun hemen önünde.
    # Embriyo bilgisi tek sefer (v6.159, kullanıcının isteği: "bazı
    # tedavilerde embriyo bilgisi iki kere yazılıyor"). Access'ten aktarılan
    # tedavinin protokol notu dondurmayı kendi cümlesiyle zaten anlatıyor
    # ("2 ADET D3 EMBRİYOSU (8HG1-8HG1) ŞEKLİNDE DONDURULARAK SAKLANDI") --
    # o nottan yazılmış tüpler "Dondurulan:" satırında tekrar edilmiyor.
    # Programda dondurulan tüpler yazılıyor. ART Lab'ın FREEZE kutuları
    # bütün tüpleri basmaya devam ediyor (orada not yok).
    # Bu tedavide dondurulup başka merkeze taşınan tüpler (v6.182), dondurma
    # satırının hemen altında.
    tasinan_satiri = tasinan_notu(tasinan_tupler(
        f"{db.vit_tedavisi('v')} = ?", (cycle_id,)))
    access_notu = "[Access kaydı" in (c["protokol_notu"] or "")
    don_notu = dondurma_notu(
        cycle_id, c["cycle_tipi"],
        [t for t in tupler if not (access_notu and t["aktarim"])])

    def _asama_ozeti(satirlar, alan):
        """Dondurma/transfer aşaması: kayıtlardaki farklı aşamalar, virgülle."""
        kodlar = []
        for r in satirlar:
            e = _et(h, "bl_genisleme", r[alan]) if r[alan] else None
            if e and e not in kodlar:
                kodlar.append(e)
        return ", ".join(kodlar) or None

    def _emb(i, alan):
        """Transfer edilen i. embriyonun bir alanı (form iki embriyo soruyor)."""
        if len(tr) <= i:
            return None
        r = tr[i]
        if alan == "asama":
            return (_et(h, "bl_genisleme", r["bl_genisleme"])
                    or (db.BIRLESME if r["hucre"] == db.BIRLESME
                        else f"{r['hucre']} hücre" if r["hucre"] else None))
        return r["bl_skor"] or _et(h, "simetri", r["cl_skor"]) or r["cl_skor"]

    anormal = sum(n for k, n in pn.items() if k and k != "2")
    return {
        # --- kimlik ---
        "kimlik_no": None,                       # programda tutulmuyor
        "dosya_no": c["dosya_no"],
        "soyadi": soyadi,
        "adi": adi,
        "esinin_adi": c["es_adi"],
        "yasi": _yas(c["dogum_tarihi"], c["opu_zamani"]),
        "onceki_tedavi": (c["hasta_cycle_no"] - 1
                          if c["hasta_cycle_no"] else None),
        "tedavi_protokolu": _et(h, "protokol_tipi", c["protokol_tipi"]),
        # --- oosit ---
        "opu_tarihi": _gg_aa_yyyy(c["opu_zamani"]),
        # FET tiplerinde yumurta toplanmıyor (v6.147): program öncesi aktarılan
        # FET'in embriyoları FET'in kendi altına açılıyor (v6.130), sayılsaydı
        # kutu çözülen embriyoları "toplanan yumurta" diye basardı.
        "toplanan_oosit": None if c["cycle_tipi"] in db.FET_TIPLERI else db.tek(
            "SELECT COUNT(*) n FROM specimen WHERE cycle_id=?", (cycle_id,))["n"],
        "matur_mii": mat.get("mii"),
        "immatur": (mat.get("mi") or 0) + (mat.get("gv") or 0) or None,
        "empty_zona": None,                      # programda tutulmuyor
        "dejenere": mat.get("degenere"),
        "atretik": mat.get("atretik"),
        "morfolojik_anomalili": None,            # programda tutulmuyor
        "opu_klinisyen": c["opu_hekim"],
        "opu_embriyolog": _yapan(cycle_id, "opu"),
        # --- sperm ---
        "sperm_kaynagi": _et(h, "sperm_alinma",
                             ornek["alinma_yontemi"] if ornek else None),
        "bazal_volum": _sayi(bazal, "hacim_ml") or (
            ornek["hacim_ml"] if ornek else None),
        "bazal_konsantrasyon": _sayi(bazal, "konsantrasyon_milyon_ml"),
        "bazal_motilite": _sayi(bazal, "total_motil_yuzde"),
        "bazal_progressif": _sayi(bazal, "pr_yuzde"),
        "morfoloji_normal": _sayi(bazal, "morfoloji_normal_yuzde"),
        "lokosit": _sayi(bazal, "lokosit_milyon_ml"),
        "hazirlama_yontemi": _et(h, "sperm_hazirlama",
                                 ornek["hazirlama_yontemi"] if ornek else None),
        "son_volum": _sayi(sonrasi, "hacim_ml"),
        "son_konsantrasyon": _sayi(sonrasi, "konsantrasyon_milyon_ml"),
        "son_motilite": _sayi(sonrasi, "total_motil_yuzde"),
        "son_progressif": _sayi(sonrasi, "pr_yuzde"),
        "hazirlayan_embriyolog": _yapan(cycle_id, "androloji"),
        # --- fertilizasyon ---
        "fertilizasyon_yontemi": metinler.t("tip_" + c["cycle_tipi"])
        if c["cycle_tipi"] else None,
        "islenen_oosit": islenen or None,
        "normal_2pn": pn.get("2"),
        "intakt": None,                          # programda tutulmuyor
        "islem_sonrasi_dejenere": dejenere_sonrasi or None,
        "anormal_fertilizasyon": anormal or None,
        "fert_embriyolog": _yapan(cycle_id, "fert") or _yapan(cycle_id, "icsi"),
        # --- transfer ---
        # Blastokistte evre; cleavage embriyosunda (blastokist kaydı yok) gün
        # -- "3. gün" (v6.154). Önceden 3. gün transferinde kutu boştu.
        "transfer_asamasi": _asama_ozeti(tr, "bl_genisleme") or ", ".join(
            f"{g}. gün" for g in sorted({r["cl_gun"] for r in tr
                                         if r["cl_gun"] and not r["bl_genisleme"]})
        ) or None,
        "transfer_tarihi": _gg_aa_yyyy(tr[0]["zaman"]) if tr else None,
        "transfer_sayisi": len(tr) or None,
        "transfer_klinisyen": None,              # programda tutulmuyor
        "transfer_embriyolog": _yapan(cycle_id, "transfer"),
        "embriyo1_asama": _emb(0, "asama"),
        "embriyo1_kalite": _emb(0, "kalite"),
        "embriyo2_asama": _emb(1, "asama"),
        "embriyo2_kalite": _emb(1, "kalite"),
        # --- kriyoprezervasyon ---
        "dondurulan_sayi": sum(len(t["ogeler"]) for t in tupler) or None,
        # Kâğıtta "EMBRİYO DONDURMA AŞAMASI" yazıyor; kullanıcının isteği
        # (v6.135) buraya **kaçıncı gün** dondurulduğunun yazılması. Önceden
        # blastokist genişleme etiketi ("Tam blastokist") basılıyordu -- o
        # bilgi artık NOTLAR'daki parantezlerde, skoruyla birlikte duruyor.
        "dondurma_asamasi": dondurma_gunleri(tupler),
        "cozdurulen_sayi": len(cozulenler) or None,
        # v6.152: sağkalım etiketleri sayılarıyla + girilmişse canlılık
        # oranları (önceden yalnızca farklı etiketler: "Canlı").
        "cozdurme_viabilite": cozme_viabilitesi(cozulenler),
        "notlar": "\n".join(
            p for p in (c["protokol_notu"], don_notu, tasinan_satiri,
                        cozulen_satiri, cozme_notu, iptal_notu)
            if p) or None,
        # --- başlık / künye ---
        "cycle_no": c["cycle_no"],
        "cycle_id": cycle_id,
        "hasta_adi": c["ad_soyad"],
    }


# ------------------------------------ embriyoloji özet formu: kalıba yerleşim

# Formun kutuları: (kâğıttaki satır no, sol kutunun anahtarı, sağ kutununki).
# Satır numaraları kâğıt aslındaki satırlar. Kutuların **adları burada değil**
# -- onlar kalıptan geliyor (`form_kalip.json`, kâğıttan çıkarıldı); burada
# yalnızca hangi verinin hangi kutuya yazıldığı duruyor. Satır sonundaki
# yorumlar kâğıtta ne yazdığını hatırlatmak için.
OZET_KUTULARI = [
    (8,  "kimlik_no", "esinin_adi"),        # KİMLİK NO / EŞİNİN ADI
    (10, "dosya_no", "yasi"),               # DOSYA NO / YAŞI
    (12, "soyadi", "onceki_tedavi"),        # SOYADI / ÖNCEKİ TEDAVİ SAYISI
    (14, "adi", "tedavi_protokolu"),        # ADI / TEDAVİ PROTOKOLÜ
    (18, "opu_tarihi", "dejenere"),         # OPU TARİHİ / DEJENERE
    (20, "toplanan_oosit", "atretik"),      # TOPLANAN OOSİT / ATRETİK
    (22, "matur_mii", "morfolojik_anomalili"),
    (24, "immatur", "opu_klinisyen"),       # İMMATÜR (MI+GV) / OPU KLİNİSYEN
    (26, "empty_zona", "opu_embriyolog"),   # EMPTY ZONA / OPU EMBRİYOLOG
    (30, "sperm_kaynagi", "hazirlama_yontemi"),
    (32, "bazal_volum", "son_volum"),       # BAZAL VOLÜM / VOLÜM
    (34, "bazal_konsantrasyon", "son_konsantrasyon"),
    (36, "bazal_motilite", "son_motilite"),
    (38, "bazal_progressif", "son_progressif"),
    (40, "morfoloji_normal", "hazirlayan_embriyolog"),
    (42, "lokosit", None),                  # LÖKOSİT (x106/ML)
    (46, "fertilizasyon_yontemi", "intakt"),
    (48, "islenen_oosit", "islem_sonrasi_dejenere"),
    (50, "normal_2pn", "anormal_fertilizasyon"),
    (52, None, "fert_embriyolog"),          # EMBRİYOLOG
    (56, "transfer_asamasi", "embriyo1_asama"),
    (58, "transfer_tarihi", "embriyo1_kalite"),
    (60, "transfer_sayisi", "embriyo2_asama"),
    (62, "transfer_klinisyen", "embriyo2_kalite"),
    (64, "transfer_embriyolog", None),      # TRANSFES EMBRİYOLOG (kâğıttaki
                                            # yazım hatası; kalıp öyle basıyor)
    (68, "dondurulan_sayi", "cozdurulen_sayi"),
    (70, "dondurma_asamasi", "cozdurme_viabilite"),
]

# Sol kutu C sütununda, sağ kutu H sütununda (kâğıttaki birleşik hücreler).
_OZET_SOL, _OZET_SAG = 2, 7
# NOTLAR kutusu (0'dan sayıyor). v6.102'de bulundu: (70, 2) yazıyordu ama
# kalıpta satır 70 boş (`form_kalip.json`'da `satirlar[70] == []`) -- "NOTLAR"
# etiketi ve değer kutusu gerçekte satır 71'de (`[[0,2,2,'NOTLAR ',12],
# [2,1,7,'',14]]`). Bu yüzden protokol notu hiçbir zaman basılmıyordu; kalıba
# dokunulmadı, yalnızca bu satır numarası düzeltildi.
_OZET_NOTLAR = (71, 2)

# Hasta kimliği kutuları: uzun bir ad kutuya sığmazsa kesilmesin, **küçülsün**
# (v6.150). Özet'in EŞİNİN ADI kutusu formun sağ kenarında -- sağa taşırmak
# (`.tasabilir`, v6.135) yazıyı kâğıdın dışına çıkarırdı; kâğıda elle
# yazarken de sığmayan ad küçük yazılır. Ekranda form.html'in betiği puntoyu
# düşürüyor, Excel'de hücre "sığacak şekilde küçült" alıyor.
OZET_SIGDIR_HUCRELER = {
    (satir - 1, sutun)
    for satir, sol, sag in OZET_KUTULARI
    for anahtar, sutun in ((sol, _OZET_SOL), (sag, _OZET_SAG))
    # ÇÖZDÜRME SONRASI VİABİLİTE de sağ kenarda (v6.152): "2 Canlı,
    # 1 Dejenere · %90-%85" uzayabiliyor.
    if anahtar in ("soyadi", "adi", "esinin_adi", "cozdurme_viabilite")
}


def _yaz(v):
    """Kutuya basılacak metin. None ve boş, boş kutu olarak çıkar."""
    return "" if v is None else str(v)


def ozet_dolgu(v: dict) -> list:
    """Özet formunun kalıbına yazılacaklar: [(değer, ek)] -- tek sayfa.

    `değer` kâğıtta **boş** olan kutulara yazıyor; bu formda hepsi öyle, o
    yüzden `ek` boş. Programda karşılığı olmayan kutular (kimlik no, empty
    zona, intakt, transfer klinisyen) None geliyor ve boş basılıyor.
    """
    d = {}
    for satir, sol, sag in OZET_KUTULARI:
        if sol:
            d[(satir - 1, _OZET_SOL)] = _yaz(v.get(sol))
        if sag:
            d[(satir - 1, _OZET_SAG)] = _yaz(v.get(sag))
    d[_OZET_NOTLAR] = _yaz(v.get("notlar"))
    return [(d, {})]


# ------------------------------------------------------------ ART lab raporu

# Kâğıttaki oosit ızgarası **13 sütunluk**. Daha çok oosit varsa fazlası
# ikinci sayfaya geçiyor (kâğıtta ikinci form demek) -- kırpmak klinik bir
# sayıyı gizlerdi, sütun eklemek kalıbı bozardı.
ARTLAB_SUTUN = 13

# Izgaranın kâğıttaki satırları (0'dan sayıyor) ve o satıra hangi verinin
# yazıldığı. Anahtarı None olan satır programda tutulmuyor, boş kalıyor.
ARTLAB_IZGARA = [
    (11, "taraf"),      # Over (R / L)
    (12, None),         # Tüp (folikül) -- programda yok
    (13, "no"),         # Oosit: kâğıtta 1..13 basılı, örneğin kendi numarası
    (14, "mat"),        # Nukleus durmu
    (15, "pn"),         # PM durumu (18 sa)
    (16, None),         # 24 saat : hücre -- programda 24. saat kaydı yok
    (17, "g2_hucre"),   # 40-45 saat : hücre
    (18, "g2_skor"),    #              grade
    (19, "g3_hucre"),   # 72   saat : hücre
    (20, "g3_skor"),    #              grade
    (21, "transfer"),   # Transfer
    (22, "yorum"),      # Yorum
]

# İlk oositin sütunu; kâğıtta her oosit iki sütun geniş.
_IZGARA_SUTUN0, _IZGARA_ADIM = 3, 2

def artlab_verisi(cycle_id: int):
    """ART Lab. Raporu'nun (DH.FR.107) verisi.

    Üç parça: kimlik, oosit ızgarası (örnek başına bir sütun) ve özet bloğu.

    **Saat satırları.** Kâğıt aslında "24 saat", "40-45 saat", "72 saat" diye
    sabit başlıklar var. Kullanıcının kararı (2026-09-11): bu başlıkları
    varsayımla eşlemek yerine program **gerçekten kaç saat geçtiğini**
    hesaplasın. Satırlar bu yüzden programın kendi aşama adlarını taşıyor
    (fertilizasyon kontrolü, gün 2, gün 3) ve her birinin yanında OPU'dan bu
    yana geçen gerçek saat yazıyor. Formun "İŞLEM / Tarih / Sa." bloğu da
    zaman çizelgesinden doluyor.
    """
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad, h.dogum_tarihi, h.es_adi "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?",
        (cycle_id,))
    if not c:
        return None
    h = _etiketler()
    cizelge = zaman_cizelgesi(cycle_id)

    # Her hücre BU tedavide yapılan işlemden (v6.147): Yumurta Çözme'de
    # yumurtanın kaynağındaki maturasyon değil ICSI ekranındaki; kaynak
    # tedavinin formunda da sonradan başka bir tedavide yapılan ICSI,
    # transfer, yeniden dondurma yok. Kendi tedavisinde her şeyi yapılan
    # örnekte sonuç eskisiyle aynı.
    bu = f"AND {db.bu_tedavide(cycle_id, 'x')}"
    ornekler = db.sorgu(
        f"""
        SELECT s.id, s.cycle_sira_no, s.taraf,
               {son_alt('mat_deger', 'maturasyon_kontrolu', ek=bu)} AS mat,
               {son_alt('fert_pn_sayisi', 'fertilizasyon_kontrolu', ek=bu)} AS pn,
               {son_alt('fert_sonuc', 'fertilizasyon_kontrolu', ek=bu)} AS fert,
               {gun_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme', 2, bu)} AS g2_hucre,
               {gun_alt('cl_skor', 'cleavage_degerlendirme', 2, bu)} AS g2_skor,
               {gun_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme', 3, bu)} AS g3_hucre,
               {gun_alt('cl_skor', 'cleavage_degerlendirme', 3, bu)} AS g3_skor,
               {son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC', ek=bu)} AS bl,
               {son_alt('zaman', 'transfer', ek=bu)} AS tr_zaman,
               {son_alt('zaman', 'vitrifikasyon', ek=bu)} AS vit_zaman
          FROM specimen s WHERE {yumurta_kosulu(c)}
          ORDER BY s.cycle_id, s.cycle_sira_no
        """, (cycle_id,))

    # Kâğıdın altındaki "Yorum:" satırı (v6.200, kullanıcının isteği): ICSI'si
    # olan tipte tedavinin GENEL bulguları (ICSI ekranı, `tedavi_bulgu`);
    # yumurta yumurta bulgular artık oraya yazılmıyor. ICSI'si olmayan tipte
    # (Yumurta Dondurma) genel bulgu bölümü yok, orada denüdasyonda
    # işaretlenen yumurta bulguları eskisi gibi (v6.135).
    if "icsi" in db.TIP_ASAMALARI.get(c["cycle_tipi"], ()):
        bulgu_notu = db.tedavi_bulgu_metni(cycle_id)
    else:
        bulgu_notu = _bulgu_notu(c, h)

    sutunlar = []
    for o in ornekler:
        sutunlar.append({
            "no": o["cycle_sira_no"],
            "taraf": {"sag": "R", "sol": "L"}.get(o["taraf"], ""),
            "mat": _et(h, "maturasyon", o["mat"]) or "",
            "pn": _et(h, "pn_sayisi", o["pn"]) or "",
            "fert": _et(h, "fert_sonuc", o["fert"]) or "",
            "g2_hucre": o["g2_hucre"] if o["g2_hucre"] is not None else "",
            "g2_skor": o["g2_skor"] or "",
            "g3_hucre": o["g3_hucre"] if o["g3_hucre"] is not None else "",
            "g3_skor": o["g3_skor"] or "",
            "bl": o["bl"] or "",
            "transfer": "✓" if o["tr_zaman"] else ("F" if o["vit_zaman"] else ""),
            # Kâğıtta blastokist satırı yok (form gün 3'te bitiyor); blastokist
            # skoru "Yorum" satırına yazılıyor -- orası serbest metin.
            # Yumurta bulguları buraya DEĞİL, kâğıdın altındaki geniş
            # "Yorum:" satırına yazılıyor (v6.135, kullanıcıya soruldu):
            # bu kutu bir oosit genişliğinde, "3AA, Vakuol, Geniş PVS" 52px
            # taşıp kesiliyordu.
            # Skor yoksa fertilizasyon sonucu, ama "Normal" DEĞİL (v6.187,
            # kullanıcının kararı): o kontrolün sonucu, embriyo hakkında bir
            # yorum değil; aynı sütunun PN satırı zaten 2PN yazıyor. Dejenere
            # ve Kayıp kalıyor -- neden cleavage olmadığını açıklıyorlar.
            # Kodla karşılaştırılıyor, etiket laboratuvarın düzenleyebildiği.
            "yorum": o["bl"] or (_et(h, "fert_sonuc", o["fert"])
                                 if o["fert"] != "normal" else None) or "",
        })

    mat = _oosit_sayilari(cycle_id)
    pn = _pn_sayilari(cycle_id)
    ornek = db.tek("SELECT * FROM sperm_ornek WHERE cycle_id=? ORDER BY id LIMIT 1",
                   (cycle_id,))
    analiz = {}
    if ornek:
        for r in db.sorgu("SELECT * FROM sperm_analiz WHERE sperm_ornek_id=?",
                          (ornek["id"],)):
            analiz[r["asama"]] = r
    bazal, sonrasi = analiz.get("bazal"), analiz.get("hazirlik_sonrasi")

    tupler = dondurma_tupleri(cycle_id)
    cozulenler = cozulen_ornekler(cycle_id)
    # Kâğıttaki FERTİLİZASYON bloğunun "Dej" sütunu: işlemden **sonra**
    # dejenere olan oosit (ICSI sırasında ya da fert kontrolünde görülen).
    dej_islem = _bu_tedavide_adet(cycle_id, _DEJ_ISLEM)

    return {
        "cycle_id": cycle_id,
        "cycle_no": c["cycle_no"],
        "dosya_no": c["dosya_no"],
        "adi": c["ad_soyad"],
        "yasi": _yas(c["dogum_tarihi"], c["opu_zamani"]),
        "esinin_adi": c["es_adi"],
        "islem": metinler.t("tip_" + c["cycle_tipi"]) if c["cycle_tipi"] else "",
        "sperm_kaynagi": _et(h, "sperm_alinma",
                             ornek["alinma_yontemi"] if ornek else None) or "",
        "hekim": c["opu_hekim"] or "",
        "laboratuvar": _yapan(cycle_id, "opu") or "",
        "sutunlar": sutunlar,
        "cizelge": cizelge,
        # --- özet bloğu ---
        "bazal_kons": _sayi(bazal, "konsantrasyon_milyon_ml"),
        "bazal_motil": _sayi(bazal, "total_motil_yuzde"),
        "bazal_normal": _sayi(bazal, "morfoloji_normal_yuzde"),
        "son_kons": _sayi(sonrasi, "konsantrasyon_milyon_ml"),
        "son_motil": _sayi(sonrasi, "total_motil_yuzde"),
        "son_normal": _sayi(sonrasi, "morfoloji_normal_yuzde"),
        "oosit_toplam": len(ornekler),
        "oosit_mii": mat.get("mii"),
        "oosit_mi": mat.get("mi"),
        "oosit_gv": mat.get("gv"),
        "oosit_mi_gv": (mat.get("mi") or 0) + (mat.get("gv") or 0) or None,
        "oosit_dej": mat.get("degenere"),
        "oosit_dej_islem": dej_islem or None,
        "oosit_atretik": mat.get("atretik"),
        "pn0": pn.get("0"), "pn1": pn.get("1"), "pn2": pn.get("2"),
        "pn3": pn.get("3"), "pn4": pn.get("4+"),
        # FREEZE sütunu artık sayı değil, **tüp tüp parantezler** (v6.135,
        # kullanıcının isteği: "Parantezler içine embriyoları yaz, birden çok
        # tüp varsa alt satırlarına"). Kâğıtta bu sütunda dört kutu var
        # (28-31); dördü aşan tüpler İKİNCİ KÂĞIDIN aynı kutularında devam
        # ediyor (v6.161, kullanıcının isteği -- önce son kutu "+2 tüp"
        # diyordu), `artlab_dolgu()`. Liste burada kırpılmıyor.
        "freeze_satirlari": [tup_metni(t) for t in tupler],
        # Kâğıdın altındaki geniş "Yorum:" satırına eklenir (v6.135; v6.200'den
        # beri ICSI'li tipte genel bulgular).
        "bulgu_notu": bulgu_notu,
        # THAW ve TRANSFER sütunları da dört kutu (v6.152, kullanıcının
        # isteği): önceden ikisi de yalnızca bir sayıydı. THAW'da çözülen
        # tüpler FREEZE'in parantezleriyle; TRANSFER'in "Uterus grade (x
        # sayı)" kutularında transfer edilen embriyoların kalitesi, sayısı ve
        # çözmedeki canlılık oranı.
        "thaw_satirlari": [tup_metni(t) for t in cozulen_tupler(cozulenler)],
        "transfer_satirlari": _transfer_satirlari(cycle_id, cozulenler),
        # ART Lab'da NOTLAR gibi bir kutu yok; iptal sebebi kalıbın dışına,
        # en alta ayrı bir şerit olarak ekleniyor (v6.104) -- bkz. app.py
        # form_ekrani()/form_excel(), form_kalip.olcu()/hucre_adresi().
        "iptal_notu": _iptal_notu(c),
    }


# Özet bloğunun kutuları: (satır, sütun, anahtar). Kâğıt aslındaki yerler.
_ARTLAB_OZET = [
    (28, 0, "bazal_kons"), (28, 2, "son_kons"),          # M/ml
    (28, 5, "oosit_mii"), (29, 5, "oosit_mi"), (30, 5, "oosit_gv"),
    (31, 5, "oosit_dej"),                                 # Mll / Ml / Pl / Dej
    (28, 6, "oosit_dej_islem"),                           # Dej (fertilizasyon)
    (28, 8, "pn0"), (28, 9, "pn1"), (28, 10, "pn2"), (28, 11, "pn3"),
    # FREEZE, THAW ve TRANSFER ayrı: dört kutu, `_ARTLAB_DORT_KUTU` (v6.152).
]

# Dört kutulu sütunlar: (sütun, verinin anahtarı). Satırlar 28-31.
_ARTLAB_THAW_SUTUN, _ARTLAB_TRANSFER_SUTUN = 14, 16
_ARTLAB_DORT_KUTU = [
    (_ARTLAB_FREEZE_SUTUN, "freeze_satirlari"),
    (_ARTLAB_THAW_SUTUN, "thaw_satirlari"),
    (_ARTLAB_TRANSFER_SUTUN, "transfer_satirlari"),
]

# "% Motil" ve "% Normal" kutularında kâğıtta zaten yazı var; sayı onun
# arkasına yazılıyor -- kalemle de öyle yapılıyor.
_ARTLAB_OZET_EK = [
    (29, 0, "bazal_motil"), (30, 0, "bazal_normal"),
    (29, 2, "son_motil"), (30, 2, "son_normal"),
]

# ART Lab'ın ad kutuları (Adı, Eşinin adı) yedi sütun genişliğinde, bugün
# sığıyor; kural iki formda aynı olsun diye yine de işaretli (v6.150).
# Alttaki "Yorum:" satırı da (v6.200): kâğıdın basılı yazısı satırın ~%80'ini
# kaplıyor, "Yorum:"dan sonra tam puntoda ~35 harf sığıyor (ölçüldü). Satır
# sayfanın sağ kenarında bitiyor -- taşma olmaz, genel bulgular uzunsa satır
# küçülüyor. Bulgu yokken basılı yazı zaten sığıyor, punto değişmiyor.
ARTLAB_SIGDIR_HUCRELER = {(6, 2), (8, 2), (_ARTLAB_YORUM_SATIR, 0)}


def sigdir_hucreleri(ad: str, deger=None) -> set:
    """Formun, sığmayan yazısı küçülen hücreleri (v6.150).

    `deger`: sayfanın dolgusu (`*_dolgu()`'nun `d`'si). ART Lab'ın dört
    kutulu sütunlarında karar veriye bağlı (v6.152): sağındaki kutu doluysa
    taşmak onun yazısının üstüne binerdi -- küçülür; boşsa taşar
    (`tasan_hucreleri()`). Karar sırası v6.150'nin: taşır, olmazsa küçült,
    asla kesme.
    """
    if ad == "artlab":
        deger = deger or {}
        return (ARTLAB_SIGDIR_HUCRELER
                | {(r, _ARTLAB_THAW_SUTUN) for r in _ARTLAB_FREEZE_SATIR}
                | {(r, _ARTLAB_FREEZE_SUTUN) for r in _ARTLAB_FREEZE_SATIR
                   if deger.get((r, _ARTLAB_THAW_SUTUN))})
    return {"ozet": OZET_SIGDIR_HUCRELER}.get(ad, set())


def tasan_hucreleri(ad: str, deger=None) -> set:
    """Sığmayan yazısı sağdaki BOŞ kutuya taşan hücreler (v6.135, v6.152).

    FREEZE yalnızca yanındaki THAW kutusu boşsa taşar (FET'te ikisi birden
    dolu olabiliyor); TRANSFER'in sağındaki "Deselect grade" programda
    tutulmuyor, hep boş -- taşar. THAW'ın sağı TRANSFER, taşmaz, küçülür.
    """
    if ad != "artlab":
        return set()
    deger = deger or {}
    return (ARTLAB_TASAN_HUCRELER
            | {(r, _ARTLAB_FREEZE_SUTUN) for r in _ARTLAB_FREEZE_SATIR
               if not deger.get((r, _ARTLAB_THAW_SUTUN))}
            | {(r, _ARTLAB_TRANSFER_SUTUN) for r in _ARTLAB_FREEZE_SATIR})


# FREEZE/THAW/TRANSFER'in taşma kararı veriye bağlı, `tasan_hucreleri()`.
ARTLAB_TASAN_HUCRELER = (
    # "% Motil" / "% Normal" kutuları da dar (32px): kâğıttaki "%" ile
    # değerin ikisi birden aynı hücreye giriyor. `_sayi()` ".0"ı düşürdüğü
    # için iki haneli değer tam sığıyor ("%  85" = 32px); %100 ya da gerçekten
    # kesirli bir değer 5px taşıyor ve komşunun 2px dolgusuna akıyor --
    # kesilmesindense (v6.136).
    {(r, c) for r, c, _ in _ARTLAB_OZET_EK})

# "İŞLEM / Tarih / Sa." bloğu: kâğıttaki beş satır ve çizelgedeki karşılığı.
_ARTLAB_ISLEM = [
    (27, "opu"), (28, "icsi"), (29, "vitrifikasyon"),
    (30, "thaw"), (31, "transfer"),
]
_ISLEM_TARIH, _ISLEM_SAAT = 25, 27


def _cizelge_zamani(cizelge, asama):
    for s in cizelge:
        if s["asama"] == asama:
            return s["zaman"] or ""
    return ""


def artlab_dolgu(v: dict) -> list:
    """ART Lab. Raporu'nun kalıbına yazılacaklar: sayfa başına (değer, ek).

    Kâğıtta 13 oosit sütunu var; daha çoksa aynı kalıp ikinci kez basılıyor ve
    kalan oositler oraya yazılıyor. Özet ve işlem saatleri **yalnızca ilk
    sayfada**: aynı toplamı iki kere basmak hangisinin doğru olduğunu
    sorduruyor.

    FREEZE, THAW ve TRANSFER'in dört kutusu ise sayfadan sayfaya **devam
    ediyor** (v6.161, kullanıcının isteği: "ikinci kâğıt var, orada freeze
    bölümünde devam etsin"): 5. tüp ikinci kâğıdın ilk FREEZE kutusunda.
    Oosit 13'ü geçmese de dördü aşan tüp varsa ikinci kâğıt basılıyor --
    kâğıtta da öyle doldurulurdu.
    """
    sutunlar = v["sutunlar"]
    kutu = len(_ARTLAB_FREEZE_SATIR)
    en_uzun = max([len(v.get(a) or []) for _s, a in _ARTLAB_DORT_KUTU] + [0])
    sayfa_sayisi = max(1, -(-len(sutunlar) // ARTLAB_SUTUN),
                       -(-en_uzun // kutu))
    cizelge = v.get("cizelge") or []
    sayfalar = []

    for sayfa in range(sayfa_sayisi):
        d, ek = {}, {}

        # --- kimlik: kâğıtta "Dosya No : ......" tek açık alan, ":" hücresine
        #     yazılıyor ki kalıptaki iki nokta yerinde kalsın.
        ek[(5, 2)] = v["dosya_no"]
        ek[(6, 2)] = v["adi"]
        ek[(7, 2)] = v["yasi"]
        ek[(8, 2)] = v["esinin_adi"]
        # İşlem ve sperm kutularında seçenekler basılı ("IVF , ICSI");
        # kâğıtta doğru olan daire içine alınıyor. Program daire çizemediği
        # için seçenekleri olduğu gibi bırakıp cevabı okla arkasına yazıyor --
        # yoksa "IVF , ICSI IVF/ICSI" diye üç seçenek gibi okunuyor.
        ek[(6, 9)] = "→ " + v["islem"] if v["islem"] else None
        ek[(8, 9)] = ("→ " + v["sperm_kaynagi"]) if v["sperm_kaynagi"] else None
        ek[(6, 21)] = v["hekim"]              # Hekimler: OPU
        ek[(7, 17)] = v["laboratuvar"]        # Labratuvar
        # Kâğıdın altındaki tek satırlık "... Yorum:" alanı (tüm sayfa
        # genişliğinde tek birleşik hücre). Bulgular oraya, basılı yazının
        # arkasına ekleniyor -- `ek`'in tam işi (v6.135, v6.200).
        if sayfa == 0 and v.get("bulgu_notu"):
            ek[(_ARTLAB_YORUM_SATIR, 0)] = " " + v["bulgu_notu"]

        # --- oosit ızgarası
        dilim = sutunlar[sayfa * ARTLAB_SUTUN:(sayfa + 1) * ARTLAB_SUTUN]
        for i, o in enumerate(dilim):
            c = _IZGARA_SUTUN0 + i * _IZGARA_ADIM
            for satir, anahtar in ARTLAB_IZGARA:
                if anahtar:
                    d[(satir, c)] = _yaz(o.get(anahtar))

        if sayfa == 0:
            for satir, c, anahtar in _ARTLAB_OZET:
                d[(satir, c)] = _yaz(v.get(anahtar))
            for satir, c, anahtar in _ARTLAB_OZET_EK:
                ek[(satir, c)] = v.get(anahtar)
            for satir, asama in _ARTLAB_ISLEM:
                z = _cizelge_zamani(cizelge, asama)
                if z:
                    d[(satir, _ISLEM_TARIH)] = _gg_aa_yyyy(z)
                    d[(satir, _ISLEM_SAAT)] = z[11:16]

        # Dört kutulu sütunlar: bu sayfanın payı (ilk sayfa 1-4, ikinci 5-8).
        for sutun, anahtar in _ARTLAB_DORT_KUTU:
            pay = (v.get(anahtar) or [])[sayfa * kutu:(sayfa + 1) * kutu]
            for satir, metin in zip(_ARTLAB_FREEZE_SATIR, pay):
                d[(satir, sutun)] = metin

        sayfalar.append((d, {k: x for k, x in ek.items()
                             if x is not None and str(x) != ""}))
    return sayfalar


# ----------------------------------------------- yüklenen formların alanları
#
# Laboratuvarın kendi yüklediği `.xlsx` formunda kutuların içine `{{dosya_no}}`
# gibi bir etiket yazılıyor; program onu değerle değiştiriyor (v6.40).
# Etiketlerin listesi burada **tek yerde** duruyor: hem doldurma hem yönetici
# alanındaki "hangi etiketi yazabilirim" ekranı bunu okuyor, yoksa ekrandaki
# liste ile gerçekte çalışan etiketler birbirinden ayrı düşerdi.
#
# Değerlerin çoğu `ozet_verisi()`'nden geliyor -- resmî özet formunun kutuları
# zaten bir laboratuvarın bir cycle için isteyeceği şeylerin listesi.

ALAN_ACIKLAMA = [
    ("— Hasta —", None),
    ("hasta_adi", "Hastanın adı soyadı"),
    ("adi", "Adı (son kelime soyadı sayılıyor)"),
    ("soyadi", "Soyadı"),
    ("dosya_no", "Dosya numarası"),
    ("yasi", "OPU günündeki yaşı"),
    ("esinin_adi", "Eşinin adı"),
    ("kimlik_no", "Kimlik no — programda tutulmuyor, boş çıkar"),
    ("— Cycle —", None),
    ("cycle_no", "Cycle numarası (2026-0001)"),
    ("ornek_kodu", "Cycle'ın örnek kodu kökü (527078-2026-0001)"),
    ("tedavi_protokolu", "Tedavi protokolü"),
    ("fertilizasyon_yontemi", "Tedavi tipi (IVF/ICSI, FET, yumurta dondurma)"),
    ("onceki_tedavi", "Önceki tedavi sayısı"),
    ("notlar", "Cycle'ın protokol notu"),
    ("bugun", "Formun basıldığı tarih"),
    ("laboratuvar", "Laboratuvarın adı"),
    ("— OPU ve yumurta —", None),
    ("opu_tarihi", "OPU tarihi"),
    ("toplanan_yumurta", "Toplanan yumurta sayısı"),
    ("matur_mii", "MII (matür) sayısı"),
    ("immatur", "MI + GV sayısı"),
    ("dejenere", "Dejenere yumurta sayısı"),
    ("atretik", "Atretik yumurta sayısı"),
    ("opu_klinisyen", "OPU hekimi"),
    ("opu_embriyolog", "OPU embriyoloğu"),
    ("— Sperm —", None),
    ("sperm_kaynagi", "Sperm kaynağı (ejakülat, TESE...)"),
    ("hazirlama_yontemi", "Hazırlama yöntemi"),
    ("bazal_volum", "Bazal volüm (ml)"),
    ("bazal_konsantrasyon", "Bazal konsantrasyon (x10⁶/ml)"),
    ("bazal_motilite", "Bazal total motilite (%)"),
    ("bazal_progressif", "Bazal progressif motilite (%)"),
    ("morfoloji_normal", "Normal morfoloji (%)"),
    ("lokosit", "Lökosit (x10⁶/ml)"),
    ("son_volum", "Hazırlık sonrası volüm (ml)"),
    ("son_konsantrasyon", "Hazırlık sonrası konsantrasyon"),
    ("son_motilite", "Hazırlık sonrası motilite (%)"),
    ("son_progressif", "Hazırlık sonrası progressif (%)"),
    ("hazirlayan_embriyolog", "Spermi hazırlayan embriyolog"),
    ("— Fertilizasyon —", None),
    ("islenen_yumurta", "İşleme alınan yumurta sayısı"),
    ("normal_2pn", "2PN sayısı"),
    ("anormal_fertilizasyon", "Anormal fertilizasyon (0/1/3PN)"),
    ("islem_sonrasi_dejenere", "İşlem sonrası dejenere"),
    ("fert_embriyolog", "Fertilizasyonu değerlendiren embriyolog"),
    ("— Transfer —", None),
    ("transfer_tarihi", "Transfer tarihi"),
    ("transfer_sayisi", "Transfer edilen embriyo sayısı"),
    ("transfer_asamasi", "Transfer aşaması"),
    ("transfer_embriyolog", "Transfer embriyoloğu"),
    ("embriyo1_asama", "1. embriyonun hücre/aşaması"),
    ("embriyo1_kalite", "1. embriyonun kalitesi"),
    ("embriyo2_asama", "2. embriyonun hücre/aşaması"),
    ("embriyo2_kalite", "2. embriyonun kalitesi"),
    ("— Dondurma / çözme —", None),
    ("dondurulan_sayi", "Dondurulan embriyo sayısı"),
    ("dondurma_asamasi", "Dondurma aşaması"),
    ("cozdurulen_sayi", "Çözdürülen embriyo sayısı"),
    ("cozdurme_viabilite", "Çözdürme sonrası viabilite"),
    ("— İşlem saatleri —", None),
    ("saat_opu", "OPU tarihi ve saati"),
    ("saat_denudasyon", "Denüdasyon tarihi ve saati"),
    ("saat_icsi", "Mikroenjeksiyon tarihi ve saati"),
    ("saat_fert", "Fertilizasyon kontrolü tarihi ve saati"),
    ("saat_vitrifikasyon", "Vitrifikasyon tarihi ve saati"),
    ("saat_thaw", "Çözme tarihi ve saati"),
    ("saat_transfer", "Transfer tarihi ve saati"),
]

# Başlık satırları (`— Hasta —`) yalnızca ekranda; etiket değil.
# Etiketin ekranda yazan adı değişti ama laboratuvar formunu çoktan
# yüklemiş olabilir (v6.40): eski ad da kabul ediliyor ve aynı değeri
# basıyor. Anahtarın kendisi (`ozet_verisi()`'nin sözlüğü, hücre eşlemeleri)
# değişmedi -- yalnızca etiketin adı.
ESKI_ALAN_ADI = {"toplanan_yumurta": "toplanan_oosit",
                 "islenen_yumurta": "islenen_oosit"}

ALAN_ADLARI = ([a for a, aciklama in ALAN_ACIKLAMA if aciklama]
               + list(ESKI_ALAN_ADI.values()))


def alanlar(cycle_id: int):
    """Yüklenen formun etiketlerine karşılık gelen değerler.

    `{{dosya_no}}` gibi etiketlerin sözlüğü. Değeri `None` olan etiket boş
    basılıyor -- "girilmedi" ile "sıfır" aynı görünmesin diye kutuyu doldurmuyor.
    """
    v = ozet_verisi(cycle_id)
    if not v:
        return None

    c = db.tek("SELECT c.cycle_no, h.dosya_no FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    cizelge = {s["asama"]: s["zaman"] for s in zaman_cizelgesi(cycle_id)}

    lab = db.tek("SELECT ad FROM lab WHERE id = ?", (db.LAB_ID,))

    v = dict(v)
    v.pop("cycle_id", None)        # iç numara; forma basılacak bir şey değil
    v["ornek_kodu"] = f"{c['dosya_no']}-{c['cycle_no']}" if c else None
    v["bugun"] = _dt.date.today().strftime("%d.%m.%Y")
    v["laboratuvar"] = (lab["ad"] if lab else None) or None
    for asama in ("opu", "denudasyon", "icsi", "fert", "vitrifikasyon",
                  "thaw", "transfer"):
        z = cizelge.get(asama)
        v["saat_" + asama] = _gg_aa_yyyy_saat(z)
    for yeni, eski in ESKI_ALAN_ADI.items():
        v[yeni] = v.get(eski)
    return v
