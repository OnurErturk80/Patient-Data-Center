"""Excel çıktısı için verinin hazırlanması.

Rotalar `app.py`'de (projenin kuralı: bütün rotalar orada); burada yalnızca
sorgular ve satırların kurulması var — `app.py` zaten 4500 satır.

Dört çıktı:

  - `ay_sayfalari(ay)`       — o ayın cycle'ları, satır başına bir cycle
  - `cycle_sayfalari(id)`    — bir cycle'ın tamamı, satır başına bir örnek
  - `cryo_sayfalari()`       — tankların dökümü, satır başına bir örnek
  - `tumu_sayfalari()`       — bütün tedaviler, tedavi türü başına bir sayfa
                               (v6.239; v6.238'e kadar tabloların ham dökümü)

Hepsi `excel.kitap()`'ın beklediği `[(ad, başlıklar, satırlar), ...]` biçimini
döndürüyor.

**Kod değil etiket yazılır.** `mii`, `2pn`, `z1` gibi değerler laba özgü ve
yönetici düzenleyebiliyor (`liste_degeri`); ekranda olduğu gibi Excel'de de
etiketleri görünmeli. Etiketler tek sorguda okunup sözlüğe alınıyor — satır
başına sorgu atmak 40 oositlik bir cycle'da 400 sorgu demek olurdu.

**"Tüm veri" dökümünde şifre, oturum ve Cryo Haritası yok.** v6.239'dan beri
döküm tedavilerin kendisi (tedavi türü başına bir sayfa); kullanıcı tablosu,
oturumlar ve tankların düzeni hiç okunmuyor. Dosya bütün hasta adlarını
içeriyor ve klinik dışına çıkabilir; bu bilinçli.
"""

import db
import formlar
import metinler
# Örnek başına alt sorgu kuran iki parça `formlar.py`'de duruyor: resmî
# formlar da aynı sorguları kuruyor, iki kopya birbirinden ayrı düşerdi.
from formlar import gun_alt as _gun_alt, son_alt as _son_alt

# --------------------------------------------------------------- ortak yardım

def _etiket_haritasi() -> dict:
    """`(liste_adi, kod) -> etiket`. Tek sorgu; satır başına sorgu atılmıyor."""
    return {(r["liste_adi"], r["kod"]): r["etiket"] for r in db.sorgu(
        "SELECT liste_adi, kod, etiket FROM liste_degeri WHERE lab_id = ?",
        (db.LAB_ID,))}


def _et(harita, liste_adi, kod):
    """Kodun etiketi; liste bulunamazsa kodun kendisi (sessizce boş kalmasın)."""
    if kod is None or kod == "":
        return None
    return harita.get((liste_adi, str(kod)), str(kod))


def _tip(kod):
    return metinler.t("tip_" + kod) if kod else None


def _taraf(kod):
    """Toplandığı over — ekranda yazan adıyla."""
    return {"sag": metinler.t("sag_rozet"),
            "sol": metinler.t("sol_rozet")}.get(kod)


def _durum(kod):
    """Cycle durumu. Sütun başlığının altında duracağı için büyük harfle
    başlayan karşılıklar seçildi; `iptal_rozet` cümle içinde kullanıldığı için
    küçük harfle başlıyor, onun yerine `bitis_iptal` alındı."""
    return {"aktif": metinler.t("durum_aktif"),
            "tamamlandi": metinler.t("tamamlandi_rozet"),
            "iptal": metinler.t("bitis_iptal")}.get(kod, kod)


def _ornek_durum(kod):
    """Örneğin durumu (`specimen.durum`) — **olduğu gibi, kodla**.

    Bu kolonun on dörde yakın değeri var: oosit, zigot, immatur, degenere,
    enjekte, gun2, gun3, morula, kavitasyon, blastokist, dondurulmus,
    transfer_edildi, discard, kayip, arrest. Bir kısmının `metinler.py`'de
    karşılığı var, çoğunun yok. Yarısını çevirip yarısını bırakmak sütunu
    tutarsız yapardı ("Dondurulmuş" ile "enjekte" yan yana); eksik olanların
    karşılığını **uydurmak** ise klinik bir varsayım olurdu. Kodlar kısa ve
    embriyoloğun okuyabileceği şeyler; etiket listesi kullanıcıyla
    kararlaştırılınca burası tek satırla çevrilebilir.
    """
    return kod


def _bitis(kod):
    return metinler.t("bitis_" + kod) if kod else None


def _transfer_hekimi(c, transfer_var=True):
    """`cycle.transfer_hekim` (v6.232, goc_061); göç yoksa boş (tuzak #3).
    Ay listesi resmî formun kuralıyla yalnızca transferi olan tedavide basıyor
    (`formlar._transfer_hekimi()`); tedavinin dökümü kaydın kendisini."""
    if not transfer_var or "transfer_hekim" not in c.keys():
        return None
    return c["transfer_hekim"]


def _kolon_var(tablo: str, kolon: str) -> bool:
    """Göç çalıştırılmamış olabilir (tuzak #3) — çıktı yine de alınabilmeli."""
    return any(r["name"] == kolon for r in db.sorgu(f"PRAGMA table_info({tablo})"))


# ------------------------------------------------------------------ ay listesi

AY_BASLIK = [
    "Dosya no", "Hasta", "Cycle no", "Hastanın kaçıncı cycle'ı", "Tip",
    "Endikasyon", "Protokol", "Gonadotropin", "Toplam doz", "Stim günü",
    "Trigger", "AMH", "AFC", "Folikül", "Endometrium (mm)",
    "OPU tarihi", "OPU hekimi", "Toplam yumurta", "Sağ", "Sol",
    "MII", "ICSI yapılan", "2PN", "Gün 2", "Gün 3", "Blastokist",
    "Donan", "Çözülen", "Transfer", "Transfer hekimi", "Durum", "Bitiş sebebi",
    "Bitiş tarihi", "Planlanan tarih", "Hasta durumu",
]


# Tedavi başına aşama sayıları (v6.239'da tek yere alındı): ad -> olayın
# koşulu (olay takma adı `o`). Sayılan, bu tedavide YAPILAN işlem
# (`db.olay_tedavisi()` + `db.tedavi_adayi()`, `tedavide_yapilan()`'ın
# kuralı). Ay listesi de tüm veri dökümü de `tedavi_sayilari()`'nden okuyor.
ASAMA_SAYILARI = (
    ("mii", "o.tip = 'maturasyon_kontrolu' AND o.mat_deger = 'mii'"),
    ("icsi", "o.tip = 'icsi'"),
    ("ikipn", "o.tip = 'fertilizasyon_kontrolu' AND o.fert_pn_sayisi = '2'"),
    ("gun2", "o.tip = 'cleavage_degerlendirme' AND o.gun = 2"),
    ("gun3", "o.tip = 'cleavage_degerlendirme' AND o.gun = 3"),
    ("blast", "o.tip = 'blastokist_degerlendirme'"),
)


def _islem_tedavileri():
    """Dondurma, çözme ve transfer sayıları: `(ad, olay tipi, işlemin
    tedavisi)` -- SQL ifadesi, olay `o`, örnek `s`. Çözme ve transfer
    tedavinin yapıldığı cycle'a (`thaw_cycle_id` / `tr_cycle_id`), dondurma
    yapıldığı tedaviye (`db.vit_tedavisi()`, v6.143). İşlev: göç sorusu her
    çağrıda (tuzak #15)."""
    return (("donan", "vitrifikasyon", db.vit_tedavisi("o")),
            ("cozulen", "thaw", "COALESCE(o.thaw_cycle_id, s.cycle_id)"),
            ("transfer", "transfer", "COALESCE(o.tr_cycle_id, s.cycle_id)"))


def tedavi_sayilari(b) -> dict:
    """Tedavi başına sayılar, bütün tedaviler için tek geçişte (v6.239):
    `{tedavi id: {ad: sayı, ...}}`; listede olmayan sayı sıfır. Çözme ve
    transferin ilk anı da (`cozulen_ilk`, `transfer_ilk`).

    v6.238'e kadar ay listesi her tedaviyi kendi alt sorgularıyla sayıyordu:
    dondurma, çözme ve transfer koşulu (`COALESCE`) dizin kullanamıyor, her
    tedavide olay tablosunun tamamı taranıyordu -- bir ayın listesi deneme
    kopyasında yarım saniye, bütün tedaviler yarım dakika. Tek geçiş bütün
    tedavileri 0,2 sn'de sayıyor; sayılar birebir aynı (denendi: 67 ay, 1.909
    tedavi). `b`: açık bağlantı."""
    sayilar = {}
    secim = ", ".join(f"({kosul}) AS k{i}"
                      for i, (_, kosul) in enumerate(ASAMA_SAYILARI))
    herhangi = " OR ".join(f"({kosul})" for _, kosul in ASAMA_SAYILARI)
    say = ", ".join(f"COUNT(DISTINCT CASE WHEN x.k{i} THEN x.specimen_id END) AS {ad}"
                    for i, (ad, _) in enumerate(ASAMA_SAYILARI))
    for r in b.execute(
            f"SELECT x.tedavi, {say} FROM "
            f"(SELECT o.specimen_id, {db.olay_tedavisi('o')} AS tedavi, {secim} "
            f"   FROM olay o WHERE o.iptal_mi = 0 AND ({herhangi})) x "
            f"WHERE {db.tedavi_adayi('x', 'x.tedavi')} "
            "GROUP BY x.tedavi"):
        sayilar.setdefault(r["tedavi"], {}).update(
            {ad: r[ad] for ad, _ in ASAMA_SAYILARI})
    for ad, tip, ifade in _islem_tedavileri():
        for r in b.execute(
                f"SELECT {ifade} AS tedavi, COUNT(DISTINCT o.specimen_id) AS n, "
                "MIN(o.zaman) AS ilk FROM olay o "
                "JOIN specimen s ON s.id = o.specimen_id "
                "WHERE o.iptal_mi = 0 AND o.tip = ? GROUP BY 1", (tip,)):
            sayilar.setdefault(r["tedavi"], {}).update(
                {ad: r["n"], f"{ad}_ilk": r["ilk"]})
    return sayilar


def ay_sayfalari(ay: str, baslik: str):
    """O ay işlem yapılan cycle'lar, satır başına bir cycle.

    Ayın ölçüsü ekrandakiyle aynı: OPU tarihi, yoksa cycle'ın açıldığı tarih
    (FET'te OPU olmuyor — bkz. CLAUDE.md "Hasta kayıtları ay ay").

    Yumurta sayısı (toplanan, sağ/sol) cycle'ın **kendi** örneklerinden;
    çözme ve transfer tedavinin yapıldığı cycle'dan (`thaw_cycle_id` /
    `tr_cycle_id`). Bir FET cycle'ında oosit yoktur ama transfer vardır —
    sayının doğru cycle'da görünmesi böyle sağlanıyor. Dondurma da (v6.143):
    FET'te yeniden dondurulan embriyo o FET'in "Donan"ına yazılır, kaynak
    tedavininkine değil (`db.vit_tedavisi()`). **M2'den blastokiste aşama
    sayıları da v6.147'den beri işlemin yapıldığı tedaviden**
    (`db.tedavide_yapilan_ifade()`, tedavi ekranının özet kutusuyla aynı
    koşul): Yumurta Çözme'de çözülen yumurtanın ICSI'si o satıra yazılır,
    yumurtanın toplandığı Yumurta Dondurma'nınkine değil. Tanımlar
    `ASAMA_SAYILARI` ve `_islem_tedavileri()`'nde (v6.239): tüm veri dökümü
    aynı sayıları bütün tedaviler için sayıyor.
    """
    # FET tiplerinde yumurta toplanmıyor: "Yumurta" sütunu boş (v6.147). Program
    # öncesi aktarılan FET'in embriyoları FET'in kendi altında (v6.130);
    # sayılsaydı çözülen embriyolar toplanan yumurta gibi görünürdü --
    # istatistikteki `fet_dislama`'nın aynı gerekçesi.
    fet = "c.cycle_tipi IN (%s)" % ",".join("'%s'" % t for t in db.FET_TIPLERI)
    h = _etiket_haritasi()
    bitis_var = _kolon_var("cycle", "bitis_sebebi")
    plan_var = _kolon_var("cycle", "planlanan_tarih")
    bitis = ("c.bitis_sebebi, c.bitis_zamani" if bitis_var
             else "NULL AS bitis_sebebi, NULL AS bitis_zamani")
    plan = "c.planlanan_tarih" if plan_var else "NULL AS planlanan_tarih"

    b = db.baglan()
    try:
        satirlar = b.execute(
            f"""
            SELECT c.*, {bitis}, {plan},
                   h.dosya_no, h.ad_soyad, h.durum AS hasta_durum,
                   CASE WHEN {fet} THEN NULL ELSE
                   (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id) END AS oosit,
                   CASE WHEN {fet} THEN NULL ELSE
                   (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id
                     AND s.taraf = 'sag') END AS sag,
                   CASE WHEN {fet} THEN NULL ELSE
                   (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id
                     AND s.taraf = 'sol') END AS sol
              FROM cycle c JOIN hasta h ON h.id = c.hasta_id
             WHERE c.lab_id = ?
               AND strftime('%Y-%m', COALESCE(c.opu_zamani, c.olusturma_zamani)) = ?
             ORDER BY COALESCE(c.opu_zamani, c.olusturma_zamani), h.dosya_no
            """,
            (db.LAB_ID, ay)).fetchall()
        sayilar = tedavi_sayilari(b) if satirlar else {}
    finally:
        b.close()

    cikti = []
    for c in satirlar:
        n = sayilar.get(c["id"], {})
        cikti.append([
            c["dosya_no"], c["ad_soyad"], c["cycle_no"], c["hasta_cycle_no"],
            _tip(c["cycle_tipi"]),
            _et(h, "endikasyon", c["endikasyon"]),
            _et(h, "protokol_tipi", c["protokol_tipi"]),
            c["gonadotropin_tipi"],                  # serbest metin, listesi yok
            c["toplam_doz"], c["stim_gun_sayisi"],
            _et(h, "trigger_tipi", c["trigger_tipi"]),
            c["amh"], c["afc"], c["folikul_sayisi"], c["endometrium_mm"],
            c["opu_zamani"], c["opu_hekim"],
            c["oosit"], c["sag"], c["sol"],
            *(n.get(ad, 0) for ad in ("mii", "icsi", "ikipn", "gun2", "gun3",
                                      "blast", "donan", "cozulen", "transfer")),
            _transfer_hekimi(c, n.get("transfer", 0)),
            _durum(c["durum"]), _bitis(c["bitis_sebebi"]), c["bitis_zamani"],
            c["planlanan_tarih"],
            metinler.t("arsiv") if c["hasta_durum"] == "arsiv" else None,
        ])
    return [(baslik, AY_BASLIK, cikti)]


# --------------------------------------------------------------- cycle detayı

ORNEK_BASLIK = [
    "Örnek kodu", "No", "Over", "Maturasyon", "Maturasyon saati",
    "ICSI", "Geçiş zorluğu", "ICSI saati",
    "Fertilizasyon", "PN", "PN skoru", "Fert. kontrol saati",
    "Gün 2 hücre", "Gün 2 simetri", "Gün 2 frag. (%)", "Gün 2 skor",
    "Gün 3 hücre", "Gün 3 simetri", "Gün 3 frag. (%)", "Gün 3 skor",
    "Blastokist günü", "Genişleme", "ICM", "TE", "Derece", "Blastokist skoru",
    "Vitrifikasyon", "Taşıyıcı", "Konum",
    "Çözme", "Sağkalım", "Re-expansion", "Transfer", "Transfer tipi",
    "Örnek durumu", "Notlar",
]


def cycle_sayfalari(cycle_id: int):
    """Bir cycle'ın tamamı: bilgi sayfası + örnek başına bir satır.

    Hastanın dosyasına konacak/yazdırılacak çıktı. İki sayfa, çünkü cycle'ın
    kendi bilgileri (protokol, OPU, hekim) tek satırlık değil tek sütunluk bir
    liste — 40 oositlik tabloya sıkıştırmak okunmaz hale getirirdi.
    """
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad, h.dogum_tarihi, h.es_adi, "
        "  h.durum AS hasta_durum "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?",
        (cycle_id,))
    if not c:
        return None, None
    h = _etiket_haritasi()

    # --- 1. sayfa: cycle bilgisi (alan / değer) ---
    bilgi = [
        ("Dosya no", c["dosya_no"]),
        ("Hasta", c["ad_soyad"]),
        ("Doğum tarihi", c["dogum_tarihi"]),
        ("Eş", c["es_adi"]),
        ("Cycle no", c["cycle_no"]),
        ("Hastanın kaçıncı cycle'ı", c["hasta_cycle_no"]),
        ("Tip", _tip(c["cycle_tipi"])),
        ("Endikasyon", _et(h, "endikasyon", c["endikasyon"])),
        ("Protokol", _et(h, "protokol_tipi", c["protokol_tipi"])),
        ("Gonadotropin", c["gonadotropin_tipi"]),
        ("Başlangıç doz", c["baslangic_doz"]),
        ("Toplam doz", c["toplam_doz"]),
        ("Stimülasyon günü", c["stim_gun_sayisi"]),
        ("Trigger", _et(h, "trigger_tipi", c["trigger_tipi"])),
        ("hCG saati", c["hcg_zamani"]),
        ("hCG günü E2", c["hcg_gunu_e2"]),
        ("hCG günü P4", c["hcg_gunu_p4"]),
        ("Endometrium (mm)", c["endometrium_mm"]),
        ("Folikül sayısı", c["folikul_sayisi"]),
        ("AMH", c["amh"]),
        ("AFC", c["afc"]),
        ("OPU saati", c["opu_zamani"]),
        ("OPU hekimi", c["opu_hekim"]),
        ("OPU sağ yumurta", c["opu_sag_oosit"]),
        ("OPU sol yumurta", c["opu_sol_oosit"]),
        ("Denüdasyon saati", c["denudasyon_zamani"]),
        ("Transfer hekimi", _transfer_hekimi(c)),
        ("Protokol notu", c["protokol_notu"]),
        ("Durum", _durum(c["durum"])),
    ]
    if _kolon_var("cycle", "bitis_sebebi"):
        bilgi += [("Bitiş sebebi", _bitis(c["bitis_sebebi"])),
                  ("Bitiş tarihi", c["bitis_zamani"])]
    if _kolon_var("cycle", "planlanan_tarih"):
        bilgi.append(("Planlanan tarih", c["planlanan_tarih"]))
    bilgi.append(("Kayıt açılışı", c["olusturma_zamani"]))

    # İşlemi yapanlar: aşama başına tek kişi (`islem_yapan`), ekranda da öyle.
    for r in db.sorgu(
            "SELECT asama, yapan_ad FROM islem_yapan WHERE cycle_id = ? "
            "ORDER BY asama", (cycle_id,)):
        bilgi.append((f"İşlemi yapan — {metinler.t('asama_' + r['asama'])}",
                      r["yapan_ad"]))

    # --- 2. sayfa: örnekler ---
    # Satırlar tedavinin örnekleri; FET tiplerinde bu tedavi için ÇÖZÜLENLER
    # de (v6.147, `db.tedavi_ornekleri()`): Yumurta Çözme'nin yumurtaları ve
    # FET'in embriyoları kaynak tedavinin örnekleri, eskiden FET'in dökümü
    # yalnızca program öncesi aktarılanları gösteriyordu. Hücreler örneğin
    # bütün geçmişi (son kayıt) -- döküm bir geçmiş; resmî formlardan farkı
    # bu, orada yalnızca o tedavide yapılan işlem basılıyor.
    fet = c["cycle_tipi"] in db.FET_TIPLERI
    satir_kosulu = (f"({db.tedavi_ornekleri(c['cycle_tipi'])} OR s.cycle_id = ?)"
                    if fet else "s.cycle_id = ?")
    ornekler = _ornek_satirlari(satir_kosulu,
                                (cycle_id, cycle_id) if fet else (cycle_id,))
    tasiyicilar = _tasiyicilar()

    satirlar = []
    for o in ornekler:
        etiket, konum = tasiyicilar.get(o["vit_tasiyici"], (None, None))
        satirlar.append(_ornek_degerleri(o, f"{c['dosya_no']}-{o['id']}", h,
                                         etiket, konum=konum))

    ad = f"{c['dosya_no']}-{c['cycle_no']}"
    return ad, [("Cycle bilgisi", ["Alan", "Değer"],
                 [[a, d] for a, d in bilgi]),
                ("Örnekler", ORNEK_BASLIK, satirlar)]


def _tasiyicilar() -> dict:
    """Taşıyıcı etiketi ve konumu: örnek başına sorgu atmak yerine tek okuma."""
    return {r["id"]: (r["etiket"], r["tam_yol"]) for r in db.sorgu(
        "SELECT t.id, t.etiket, k.tam_yol FROM tasiyici t "
        "LEFT JOIN konum k ON k.id = t.konum_id WHERE t.lab_id = ?",
        (db.LAB_ID,))}


def _ornek_satirlari(kosul: str, parametre=()):
    """Örnek başına bir satır, her aşamanın son kaydıyla (alt sorgular).

    Tedavinin dökümü (`cycle_sayfalari()`) ve tüm veri dökümünün "Yumurta ve
    embriyolar" sayfası (v6.239) aynı sorgudan -- iki kopya birbirinden ayrı
    düşerdi. `kosul`: örnek tablosu `s` üzerinde, koddan gelir. Dondurmanın,
    çözmenin ve transferin YAPILDIĞI tedavi de (`vit_tedavi`, `thaw_tedavi`,
    `tr_tedavi`): FET'te çözülüp transfer edilen embriyo hangi tedavide.
    """
    vit = "(" + db.vit_tedavisi("x") + ")"
    return db.sorgu(
        f"""
        SELECT s.id, s.cycle_id, s.cycle_sira_no, s.taraf, s.durum,
               {_son_alt('mat_deger', 'maturasyon_kontrolu')} AS mat,
               {_son_alt('zaman', 'maturasyon_kontrolu')} AS mat_zaman,
               {_son_alt('icsi_sonuc', 'icsi')} AS icsi,
               {_son_alt('icsi_gecis_zorlugu', 'icsi')} AS zorluk,
               {_son_alt('zaman', 'icsi')} AS icsi_zaman,
               {_son_alt('fert_sonuc', 'fertilizasyon_kontrolu')} AS fert,
               {_son_alt('fert_pn_sayisi', 'fertilizasyon_kontrolu')} AS pn,
               {_son_alt('fert_pn_skoru', 'fertilizasyon_kontrolu')} AS pn_skor,
               {_son_alt('zaman', 'fertilizasyon_kontrolu')} AS fert_zaman,
               {_gun_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme', 2)} AS g2_hucre,
               {_gun_alt('cl_simetri', 'cleavage_degerlendirme', 2)} AS g2_sim,
               {_gun_alt('cl_fragmentasyon', 'cleavage_degerlendirme', 2)} AS g2_frag,
               {_gun_alt('cl_skor', 'cleavage_degerlendirme', 2)} AS g2_skor,
               {_gun_alt(db.cl_hucre_ifadesi('x'), 'cleavage_degerlendirme', 3)} AS g3_hucre,
               {_gun_alt('cl_simetri', 'cleavage_degerlendirme', 3)} AS g3_sim,
               {_gun_alt('cl_fragmentasyon', 'cleavage_degerlendirme', 3)} AS g3_frag,
               {_gun_alt('cl_skor', 'cleavage_degerlendirme', 3)} AS g3_skor,
               {_son_alt('gun', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_gun,
               {_son_alt('bl_genisleme', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_gen,
               {_son_alt('bl_icm', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_icm,
               {_son_alt('bl_te', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_te,
               {_son_alt('bl_derece', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_der,
               {_son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl_skor,
               {_son_alt('zaman', 'vitrifikasyon')} AS vit_zaman,
               {_son_alt('vit_tasiyici_id', 'vitrifikasyon')} AS vit_tasiyici,
               {_son_alt(vit, 'vitrifikasyon')} AS vit_tedavi,
               {_son_alt('zaman', 'thaw')} AS thaw_zaman,
               {_son_alt('(COALESCE(x.thaw_cycle_id, s.cycle_id))', 'thaw')} AS thaw_tedavi,
               {_son_alt('thaw_sagkalim', 'thaw')} AS sagkalim,
               {_son_alt('thaw_re_expansion', 'thaw')} AS re_exp,
               {_son_alt('zaman', 'transfer')} AS tr_zaman,
               {_son_alt('(COALESCE(x.tr_cycle_id, s.cycle_id))', 'transfer')} AS tr_tedavi,
               {_son_alt('tr_tipi', 'transfer')} AS tr_tipi,
               (SELECT group_concat(x.notlar, ' | ') FROM olay x
                 WHERE x.specimen_id = s.id AND x.iptal_mi = 0
                   AND x.notlar IS NOT NULL AND x.notlar <> '') AS notlar
          FROM specimen s WHERE {kosul}
          ORDER BY s.cycle_id, s.cycle_sira_no
        """, parametre)


def _ornek_degerleri(o, kod, h, etiket, konum=None, tedavi_no=None):
    """Bir örneğin satırı: tedavinin dökümünde `ORNEK_BASLIK`'ın, tüm veri
    dökümünde (`tedavi_no` verilince: {tedavi id: tedavi no}, v6.239)
    `TUM_ORNEK_BASLIK`'ın sırasıyla. Tüm veri dökümünde dondurma, çözme ve
    transferin yapıldığı tedavi de yazılıyor; Konum yok (Cryo Haritası'nın
    bilgisi, dökümde istenmedi)."""
    deger = [
        kod, o["cycle_sira_no"],
        _taraf(o["taraf"]),
        _et(h, "maturasyon", o["mat"]), o["mat_zaman"],
        _et(h, "icsi_sonuc", o["icsi"]),
        _et(h, "gecis_zorlugu", o["zorluk"]), o["icsi_zaman"],
        _et(h, "fert_sonuc", o["fert"]), _et(h, "pn_sayisi", o["pn"]),
        _et(h, "pn_skoru", o["pn_skor"]), o["fert_zaman"],
        o["g2_hucre"], _et(h, "simetri", o["g2_sim"]), o["g2_frag"], o["g2_skor"],
        o["g3_hucre"], _et(h, "simetri", o["g3_sim"]), o["g3_frag"], o["g3_skor"],
        o["bl_gun"], _et(h, "bl_genisleme", o["bl_gen"]),
        _et(h, "bl_icm", o["bl_icm"]), _et(h, "bl_te", o["bl_te"]),
        _et(h, "bl_derece", o["bl_der"]), o["bl_skor"],
    ]
    sagkalim = _et(h, "thaw_sagkalim", o["sagkalim"])
    if tedavi_no is None:
        deger += [o["vit_zaman"], etiket, konum,
                  o["thaw_zaman"], sagkalim, o["re_exp"],
                  o["tr_zaman"], o["tr_tipi"]]
    else:
        deger += [o["vit_zaman"], tedavi_no.get(o["vit_tedavi"]), etiket,
                  o["thaw_zaman"], tedavi_no.get(o["thaw_tedavi"]),
                  sagkalim, o["re_exp"],
                  o["tr_zaman"], tedavi_no.get(o["tr_tedavi"]), o["tr_tipi"]]
    return deger + [_ornek_durum(o["durum"]), o["notlar"]]


# ------------------------------------------------------------------ cryo dökümü

CRYO_BASLIK = [
    "Tankta", "Konum", "Taşıyıcı", "Taşıyıcı tipi", "Renk",
    "Dosya no", "Hasta", "Cycle no", "Tip", "Örnek kodu", "No",
    "Blastokist skoru", "Dondurma", "Çözme", "Sağkalım", "Transfer",
    "Örnek durumu",
]


def cryo_sayfalari():
    """Tanktaki örneklerin dökümü — sayım ve envanter için.

    Çözülmüş örnekler de listede; "Tankta" sütunu ayırıyor. Böylece aynı
    dosya hem bugünkü sayımı hem o taşıyıcının geçmişini veriyor; Excel'in
    süzgeciyle biri ötekinden ayrılıyor.

    Cryo haritası gibi bu da **türetilmiş**: elle güncellenen bir konum
    tablosu yok, liste vitrifikasyon ve çözme kayıtlarından çıkıyor.
    """
    h = _etiket_haritasi()
    # Satır bir DONDURMA; çözme sütunu o dondurmanın tüpünden yapılan çözme
    # (v6.143, `thaw_tasiyici_id`). "Örneğin son çözmesi" yeniden dondurulan
    # bir embriyonun yeni tüpüne eski tüpün çözmesini yazardı ve "Tankta"
    # dolu bir tüp için "Hayır" derdi. Göç yoksa eski ölçü.
    tup = ("AND x.thaw_tasiyici_id = o.vit_tasiyici_id"
           if db.cozme_tupu_var() else "")
    # Cryo Haritası'nda olmayan tüp (v6.233, `db.haritada_yok_sql()`) dökümde
    # yok: straw haritada değil, "Tankta: Evet" yanlış olurdu. Karar tüpün
    # sayfasında; tanktan çıkmış tüpler geçmişleriyle duruyor.
    yok = db.haritada_yok_sql("t")
    satirlar = db.sorgu(
        f"""
        SELECT k.tam_yol, t.etiket, t.tip AS tasiyici_tipi, t.renk,
               t.durum AS tup_durum,
               o.zaman AS dondurma,
               h.dosya_no, h.ad_soyad, c.cycle_no, c.cycle_tipi,
               s.id AS ornek, s.cycle_sira_no, s.durum AS ornek_durum,
               {_son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC')} AS skor,
               {_son_alt('zaman', 'thaw', ek=tup)} AS cozme,
               {_son_alt('thaw_sagkalim', 'thaw', ek=tup)} AS sagkalim,
               {_son_alt('zaman', 'transfer')} AS transfer
          FROM olay o
          JOIN specimen s ON s.id = o.specimen_id
          JOIN cycle c ON c.id = s.cycle_id
          JOIN hasta h ON h.id = c.hasta_id
          LEFT JOIN tasiyici t ON t.id = o.vit_tasiyici_id
          LEFT JOIN konum k ON k.id = t.konum_id
         WHERE o.lab_id = ? AND o.tip = 'vitrifikasyon' AND o.iptal_mi = 0
           AND NOT COALESCE({yok}, 0)
         ORDER BY k.tam_yol, t.etiket, h.dosya_no, s.cycle_sira_no
        """,
        (db.LAB_ID,))

    cikti = []
    for r in satirlar:
        tankta = not r["cozme"] and r["ornek_durum"] == "dondurulmus"
        # Başka merkeze taşınan (v6.182) ya da imha edilen (v6.227) tüp:
        # örnek çözülmedi ama tankta değil.
        if r["tup_durum"] == "gonderildi":
            tank = "Taşındı"
        elif r["tup_durum"] == "imha":
            tank = "İmha edildi"
        else:
            tank = "Evet" if tankta else "Hayır"
        cikti.append([
            tank,
            r["tam_yol"], r["etiket"], _et(h, "tasiyici_tipi", r["tasiyici_tipi"]),
            _et(h, "tasiyici_renk", r["renk"]),
            r["dosya_no"], r["ad_soyad"], r["cycle_no"], _tip(r["cycle_tipi"]),
            f"{r['dosya_no']}-{r['ornek']}", r["cycle_sira_no"],
            r["skor"], r["dondurma"], r["cozme"],
            _et(h, "thaw_sagkalim", r["sagkalim"]), r["transfer"],
            _ornek_durum(r["ornek_durum"]),
        ])
    return [("Cryo dökümü", CRYO_BASLIK, cikti)]


# --------------------------------------------------------------- tüm veri
#
# Yönetici panelinin "Tüm veriyi Excel'e aktar"ı (`/disari/tumu`) ve her gün
# 14:00'te Cryo haritası klasörüne yazılan "Tüm veriler" dosyası
# (`oto_yedek.py`). v6.239'da yeniden kuruldu (kullanıcının isteği: "tüm
# veriyi excel'e aktar butonuna basınca bütün tedavileri excel'e aktarsın;
# FETler, yumurta dondurmalar, ve çözmeler, IVF/ICSI ler. Cryo haritayı içine
# eklemesin"). v6.238'e kadar tabloların ham dökümüydü: tablo başına bir
# sayfa, kodlar, kolon adları; tedaviler yalnızca ham "cycle" sayfasında,
# Cryo Haritası'nın tabloları (taşıyıcı, konum, Excel kayıtları) da içinde.
#
# Bugün tedavi türü başına bir sayfa, satır başına bir tedavi, etiketler
# ekrandaki gibi; sonda örnek başına "Yumurta ve embriyolar". Cryo Haritası
# yok: tüp etiketi var (dondurma kaydının parçası), tankta yeri yok; sperm
# dondurma Cryo Haritası'nın modülü, yok. Şifre ve oturum zaten hiç yok.

# Sayfalar ve hangi tiplerin bir arada durduğu. Burada olmayan bir tip
# (ileride eklenirse) kendi adıyla ayrı sayfaya düşer -- hiçbir tedavi
# dökümden sessizce kaybolmasın.
TUM_SAYFALAR = (
    ("IVF-ICSI", ("ivf_icsi",)),
    ("FET", ("fet", "fet_kultur")),
    ("Yumurta Dondurma", ("oosit_cryo",)),
    ("Yumurta Çözme", ("yumurta_cozme",)),
)


def _asamada(*asamalar):
    """Sütun koşulu: sayfanın tiplerinden birinde bu aşamalardan biri var
    (`db.TIP_ASAMALARI`, tedavi ekranının özet kutusunun ölçüsü). Yeni bir tip
    kendi aşamalarının sütunlarını kendiliğinden alır."""
    return lambda tipler: any(a in db.TIP_ASAMALARI.get(t, ())
                              for t in tipler for a in asamalar)


def _her_zaman(tipler):
    return True


def _embriyo_donduran(tipler):
    """Dondurma günü yalnızca embriyo donduran tipte (yumurtanın günü yok)."""
    return any("vitrifikasyon" in db.TIP_ASAMALARI.get(t, ())
               and not db.yumurta_mi(t) for t in tipler)


# (başlık, `_tedavi_degerleri()`'nin anahtarı, koşul). Sıra klinik akış:
# kimlik, stimülasyon, OPU, çözme, androloji, laboratuvar, dondurma, transfer,
# gebelik; sonda PGT, bulaş, işlemi yapanlar ve durum.
TUM_SUTUNLAR = [
    ("Dosya no", "dosya_no", _her_zaman),
    ("Hasta", "ad_soyad", _her_zaman),
    ("Doğum tarihi", "dogum_tarihi", _her_zaman),
    ("Eşi", "es_adi", _her_zaman),
    ("Tedavi no", "cycle_no", _her_zaman),
    ("Kaçıncı tedavi", "hasta_cycle_no", _her_zaman),
    ("Tip", "tip", _her_zaman),
    ("Tedavi tarihi", "tedavi_gunu", _her_zaman),
    ("Yaş", "yas", _her_zaman),
    ("Endikasyon", "endikasyon", _her_zaman),
    ("Protokol", "protokol", _asamada("opu")),
    ("Gonadotropin", "gonadotropin_tipi", _asamada("opu")),
    ("Başlangıç doz", "baslangic_doz", _asamada("opu")),
    ("Toplam doz", "toplam_doz", _asamada("opu")),
    ("Stim günü", "stim_gun_sayisi", _asamada("opu")),
    ("Trigger", "trigger", _asamada("opu")),
    ("hCG zamanı", "hcg_zamani", _asamada("opu")),
    ("hCG günü E2", "hcg_gunu_e2", _asamada("opu")),
    ("hCG günü P4", "hcg_gunu_p4", _asamada("opu")),
    ("AMH", "amh", _asamada("opu")),
    ("AFC", "afc", _asamada("opu")),
    ("Folikül", "folikul_sayisi", _asamada("opu")),
    ("Endometrium (mm)", "endometrium_mm", _asamada("transfer")),
    ("OPU zamanı", "opu_zamani", _asamada("opu")),
    ("OPU hekimi", "opu_hekim", _asamada("opu")),
    # İki ayrı sayı, iki ayrı ad (v6.112): OPU ekranında girilen sayı ve
    # programda açılmış yumurta kaydı.
    ("Toplanan yumurta (OPU)", "toplanan", _asamada("opu")),
    ("Kayıtlı yumurta", "kayitli", _asamada("opu")),
    ("Çözme zamanı", "cozulen_ilk", _asamada("thaw")),
    ("Çözülen", "cozulen", _asamada("thaw")),
    ("Çözülen tüpler", "cozulen_tupler", _asamada("thaw")),
    ("Sağkalım", "sagkalim", _asamada("thaw")),
    ("Kaynak tedavi", "kaynak", _asamada("thaw")),
    ("Sperm alınma yöntemi", "sperm_alinma", _asamada("androloji")),
    ("Sperm hazırlama", "sperm_hazirlama", _asamada("androloji")),
    ("Bazal konsantrasyon (milyon/ml)", "bazal_kons", _asamada("androloji")),
    ("Bazal total motil (%)", "bazal_motil", _asamada("androloji")),
    ("Hazırlık sonrası konsantrasyon (milyon/ml)", "son_kons", _asamada("androloji")),
    ("Hazırlık sonrası total motil (%)", "son_motil", _asamada("androloji")),
    ("MII", "mii", _asamada("denudasyon", "icsi")),
    ("ICSI", "icsi", _asamada("icsi")),
    ("2PN", "ikipn", _asamada("fert")),
    ("Gün 2", "gun2", _asamada("cleavage")),
    ("Gün 3", "gun3", _asamada("cleavage")),
    ("Blastokist", "blast", _asamada("blast")),
    ("Genel bulgular", "genel_bulgu", _asamada("icsi")),
    ("Dondurulan", "donan", _asamada("vitrifikasyon")),
    ("Dondurulan tüp", "donan_tup", _asamada("vitrifikasyon")),
    ("Dondurulan tüpler", "donan_tupler", _asamada("vitrifikasyon")),
    ("Dondurma günü", "dondurma_gunu", _embriyo_donduran),
    ("Transfer", "transfer", _asamada("transfer")),
    ("Transfer zamanı", "transfer_ilk", _asamada("transfer")),
    ("Transfer edilen", "transfer_edilen", _asamada("transfer")),
    ("Transfer hekimi", "transfer_hekimi", _asamada("transfer")),
    ("Beta hCG", "beta", _asamada("gebelik")),
    # v6.241: beta hCG'den türetilen sonuç (`db.gebelik_testi()`).
    ("Gebelik testi (beta hCG)", "gebelik_testi", _asamada("gebelik")),
    ("Klinik gebelik", "klinik_gebelik", _asamada("gebelik")),
    ("Gebelik kesesi sayısı", "gebelik_kesesi_sayisi", _asamada("gebelik")),
    ("Fetal kalp atımı", "fk", _asamada("gebelik")),
    ("FK kontrol zamanı", "fk_kontrol_zamani", _asamada("gebelik")),
    ("Sonlanma", "sonlanma", _asamada("gebelik")),
    ("Doğum zamanı", "dogum_zamani", _asamada("gebelik")),
    ("Doğum haftası", "dogum_haftasi", _asamada("gebelik")),
    ("Bebek sayısı", "bebek_sayisi", _asamada("gebelik")),
    ("Bebekler", "bebekler", _asamada("gebelik")),
    ("PGT", "pgt", _asamada("blast", "transfer")),
    ("Bulaş (kadın)", "bulas_kadin", _her_zaman),
    ("Bulaş (erkek)", "bulas_erkek", _her_zaman),
    ("İşlemi yapanlar", "yapanlar", _her_zaman),
    ("Durum", "durum", _her_zaman),
    ("Bitiş sebebi", "bitis", _her_zaman),
    ("Bitiş tarihi", "bitis_zamani", _her_zaman),
    ("Planlanan tarih", "planlanan_tarih", _her_zaman),
    ("Protokol notu", "protokol_notu", _her_zaman),
    ("Hasta durumu", "hasta_durumu", _her_zaman),
]

# "Yumurta ve embriyolar" sayfası: tedavinin dökümünün örnek satırı
# (`ORNEK_BASLIK`), önünde hastası ve tedavisi; dondurma, çözme ve transferin
# yapıldığı tedavi de yazılı (FET'te çözülen embriyo kaynağının satırında).
# Konum yok -- Cryo Haritası'nın bilgisi.
TUM_ORNEK_BASLIK = [
    "Dosya no", "Hasta", "Tedavi no", "Tip",
    "Örnek kodu", "No", "Over", "Maturasyon", "Maturasyon saati",
    "ICSI", "Geçiş zorluğu", "ICSI saati",
    "Fertilizasyon", "PN", "PN skoru", "Fert. kontrol saati",
    "Gün 2 hücre", "Gün 2 simetri", "Gün 2 frag. (%)", "Gün 2 skor",
    "Gün 3 hücre", "Gün 3 simetri", "Gün 3 frag. (%)", "Gün 3 skor",
    "Blastokist günü", "Genişleme", "ICM", "TE", "Derece", "Blastokist skoru",
    "Vitrifikasyon", "Dondurulduğu tedavi", "Taşıyıcı",
    "Çözme", "Çözüldüğü tedavi", "Sağkalım", "Re-expansion",
    "Transfer", "Transfer edildiği tedavi", "Transfer tipi",
    "Örnek durumu", "Notlar",
]


def _sayi_metni(x):
    """Bir ölçümün yazısı: 85.0 -> "85", 2.45 -> "2,45" (yuvarlama yok)."""
    if isinstance(x, float):
        x = int(x) if x.is_integer() else x
    return str(x).replace(".", ",")


def _evet_hayir(kod, evet, hayir):
    """Gebelik ekranının üç seçeneği (`evet` / `hayir` / `bilinmiyor`); ilk
    kayıtlarda `1` / `0` (`db.klinik_gebelik_sql()`'in gerekçesi)."""
    if kod in ("evet", "1", 1):
        return metinler.t(evet)
    if kod in ("hayir", "0", 0):
        return metinler.t(hayir)
    if kod == "bilinmiyor":
        return metinler.t("bilinmiyor")
    return kod or None


def _bulas_yazisi(deger):
    """Bulaş kaydı (`db.bulas_oku()`): girilmedi boş, "Yok", ya da hastalıklar."""
    durum, kodlar, diger = db.bulas_oku(deger)
    if durum is None:
        return None
    if durum == "yok":
        return metinler.t("yok")
    return ", ".join(db.bulas_etiketleri(kodlar, diger))


def _tek_satir(metin):
    """Resmî formun NOTLAR satırı 68'de sarılı (`formlar._sar()`); hücrede
    tek satır."""
    return " ".join(metin.split()) if metin else None


def _tum_veri(b):
    """Tüm veri dökümünün tedavileri: `[(cycle_tipi, değerler sözlüğü)]`,
    tedavinin günü sırasıyla, ve {tedavi id: tedavi no}.

    Bütün tedavilerin her bilgisi tablo başına bir sorguyla okunuyor
    (`tedavi_sayilari()`, `formlar.tedavilerin_*()`); tedavi tedavi sormak
    bin tedavide dakikalar sürerdi. Ekranlar ve resmî formlarla aynı kural:
    sayılar ay listesinin (`tedavi_sayilari()`), tüpler ve çözülenler resmî
    formların (`dondurma_tupleri()`, `cozulen_ornekler()`), transfer edilenin
    kalitesi ART Lab'ın "Uterus grade"i (`_transfer_satirlari()`).
    """
    h = _etiket_haritasi()
    gun = db.tedavi_tarihi(b, "c")
    cycleler = [dict(r) for r in b.execute(
        f"SELECT c.*, h.dosya_no, h.ad_soyad, h.dogum_tarihi, h.es_adi, "
        f"  h.durum AS hasta_durum, {gun} AS tedavi_gunu "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id WHERE c.lab_id = ? "
        "ORDER BY tedavi_gunu, h.dosya_no, c.cycle_no", (db.LAB_ID,))]
    tedavi_no = {c["id"]: c["cycle_no"] for c in cycleler}

    sayilar = tedavi_sayilari(b)
    kayitli = {r[0]: r[1] for r in b.execute(
        "SELECT cycle_id, COUNT(*) FROM specimen GROUP BY cycle_id")}
    kaynaklar = {}
    for r in b.execute(
            "SELECT DISTINCT COALESCE(o.thaw_cycle_id, s.cycle_id) AS tedavi, "
            "  s.cycle_id AS kaynak FROM olay o "
            "JOIN specimen s ON s.id = o.specimen_id "
            "WHERE o.tip = 'thaw' AND o.iptal_mi = 0"):
        if r["kaynak"] != r["tedavi"]:
            kaynaklar.setdefault(r["tedavi"], set()).add(r["kaynak"])

    # Androloji: tedavinin ilk örneği ve iki analizi (resmî formların okuması).
    sperm = {}
    for r in b.execute("SELECT * FROM sperm_ornek ORDER BY id"):
        sperm.setdefault(r["cycle_id"], {"ornek": r})
    ornek_tedavisi = {v["ornek"]["id"]: cid for cid, v in sperm.items()}
    for r in b.execute("SELECT * FROM sperm_analiz ORDER BY id"):
        cid = ornek_tedavisi.get(r["sperm_ornek_id"])
        if cid is not None:
            sperm[cid][r["asama"]] = r

    gebelik = {r["cycle_id"]: r for r in b.execute(
        "SELECT * FROM gebelik_sonucu WHERE lab_id = ? ORDER BY id",
        (db.LAB_ID,))}
    beta, beta_deger = {}, {}
    for r in b.execute("SELECT cycle_id, zaman, deger FROM beta_hcg "
                       "ORDER BY cycle_id, zaman, id"):
        if r["deger"] is not None:
            tarih = formlar._gg_aa_yyyy(r["zaman"])
            beta.setdefault(r["cycle_id"], []).append(
                f"{_sayi_metni(r['deger'])} ({tarih})" if tarih
                else _sayi_metni(r["deger"]))
            beta_deger.setdefault(r["cycle_id"], []).append(r["deger"])
    bebek = {}
    for r in (b.execute("SELECT cycle_id, cinsiyet, kilo_kg FROM dogan_bebek "
                        "WHERE lab_id = ? ORDER BY cycle_id, sira, id",
                        (db.LAB_ID,)) if db.tablo_var("dogan_bebek") else ()):
        parca = [metinler.t(r["cinsiyet"])] if r["cinsiyet"] in ("kiz", "erkek") else []
        if r["kilo_kg"] is not None:
            parca.append(f"{_sayi_metni(r['kilo_kg'])} kg")
        bebek.setdefault(r["cycle_id"], []).append(" ".join(parca) or "?")
    yapanlar = {}
    for r in b.execute("SELECT cycle_id, asama, yapan_ad FROM islem_yapan "
                       "WHERE lab_id = ? AND yapan_ad IS NOT NULL "
                       "AND yapan_ad <> ''", (db.LAB_ID,)):
        yapanlar.setdefault(r["cycle_id"], {})[r["asama"]] = r["yapan_ad"]
    bulgulu = ({r[0] for r in b.execute(
        "SELECT DISTINCT cycle_id FROM tedavi_bulgu WHERE asama = 'icsi'")}
        if db.tablo_var("tedavi_bulgu") else set())
    biyopsi_var = b.execute(
        "SELECT 1 FROM olay WHERE tip = 'biyopsi' AND iptal_mi = 0 LIMIT 1"
    ).fetchone() is not None

    tupler = formlar.tedavilerin_dondurma_tupleri()
    cozulenler = formlar.tedavilerin_cozulenleri()
    transferler = formlar.tedavilerin_transfer_edilenleri()
    # Tedavide kullanılan dondurulmuş spermin yöntemi (v6.247): resmî formların
    # "Sperm kaynağı"nın aynısı -- çözülen TESE "TESE".
    sperm_yontem = formlar.tedavilerin_sperm_yontemleri()

    sonuc = []
    for c in cycleler:
        cid, tip = c["id"], c["cycle_tipi"]
        asamalar = db.TIP_ASAMALARI.get(tip, ())
        n = sayilar.get(cid, {})
        tup = tupler.get(cid, [])
        coz = cozulenler.get(cid, [])
        sp = sperm.get(cid, {})
        g = gebelik.get(cid)
        yapan = yapanlar.get(cid, {})
        sira = list(asamalar) + sorted(a for a in yapan if a not in asamalar)
        sag, sol = c.get("opu_sag_oosit"), c.get("opu_sol_oosit")

        pgt = []
        if db.pgt_oku(c.get("pgt_testleri")):
            pgt.append(formlar.pgt_notu(cid))
        if coz and biyopsi_var and tip in db.FET_TIPLERI:
            pgt.append(formlar.pgt_cozulen_notu(cid, coz))
        analiz = {a: sp.get(a) for a in ("bazal", "hazirlik_sonrasi")}
        test = db.gebelik_testi(beta_deger.get(cid, ()))     # v6.241

        def olcu(asama, alan):
            r = analiz.get(asama)
            return r[alan] if r is not None and alan in r.keys() else None

        d = {
            **c,
            "tip": _tip(tip),
            "yas": formlar._yas(c["dogum_tarihi"], c["tedavi_gunu"]),
            "endikasyon": _et(h, "endikasyon", c.get("endikasyon")),
            "protokol": _et(h, "protokol_tipi", c.get("protokol_tipi")),
            "trigger": _et(h, "trigger_tipi", c.get("trigger_tipi")),
            "toplanan": (None if sag is None and sol is None
                         else (sag or 0) + (sol or 0)),
            "kayitli": kayitli.get(cid, 0),
            "cozulen_ilk": n.get("cozulen_ilk"),
            "cozulen": n.get("cozulen", 0),
            "cozulen_tupler": " ".join(
                formlar.tup_metni(t) for t in formlar.cozulen_tupler(coz)) or None,
            "sagkalim": formlar.cozme_viabilitesi(coz),
            "kaynak": ", ".join(sorted(
                tedavi_no.get(k, str(k)) for k in kaynaklar.get(cid, ()))) or None,
            "sperm_alinma": formlar.sperm_kaynagi_metni(
                h, sp["ornek"]["alinma_yontemi"] if sp else None, sperm_yontem.get(cid, [])),
            "sperm_hazirlama": _et(h, "sperm_hazirlama",
                                   sp["ornek"]["hazirlama_yontemi"] if sp else None),
            "bazal_kons": olcu("bazal", "konsantrasyon_milyon_ml"),
            "bazal_motil": olcu("bazal", "total_motil_yuzde"),
            "son_kons": olcu("hazirlik_sonrasi", "konsantrasyon_milyon_ml"),
            "son_motil": olcu("hazirlik_sonrasi", "total_motil_yuzde"),
            **{ad: n.get(ad, 0) for ad, _ in ASAMA_SAYILARI},
            "genel_bulgu": (db.tedavi_bulgu_metni(cid)
                            if cid in bulgulu and "icsi" in asamalar else None),
            "donan": n.get("donan", 0),
            "donan_tup": len(tup),
            "donan_tupler": " ".join(formlar.tup_metni(t) for t in tup) or None,
            "dondurma_gunu": formlar.dondurma_gunleri(tup),
            "transfer": n.get("transfer", 0),
            "transfer_ilk": n.get("transfer_ilk"),
            "transfer_edilen": "; ".join(formlar._transfer_satirlari(
                cid, coz, transferler.get(cid, []))) or None,
            "transfer_hekimi": _transfer_hekimi(c, n.get("transfer", 0)),
            "beta": " → ".join(beta.get(cid, [])) or None,
            "gebelik_testi": metinler.t(test) if test else None,
            "klinik_gebelik": _evet_hayir(g["klinik_gebelik"], "var", "yok") if g else None,
            "gebelik_kesesi_sayisi": g["gebelik_kesesi_sayisi"] if g else None,
            "fk": _evet_hayir(g["fk_pozitif"], "pozitif", "negatif") if g else None,
            "fk_kontrol_zamani": g["fk_kontrol_zamani"] if g else None,
            "sonlanma": _et(h, "sonlanma", g["sonlanma"]) if g else None,
            "dogum_zamani": g["dogum_zamani"] if g else None,
            "dogum_haftasi": (g["dogum_haftasi"]
                              if g and "dogum_haftasi" in g.keys() else None),
            "bebek_sayisi": g["bebek_sayisi"] if g else None,
            "bebekler": " · ".join(bebek.get(cid, [])) or None,
            "pgt": " · ".join(_tek_satir(p) for p in pgt if p) or None,
            "bulas_kadin": _bulas_yazisi(c.get("bulas_kadin")),
            "bulas_erkek": _bulas_yazisi(c.get("bulas_erkek")),
            "yapanlar": " · ".join(
                f"{metinler.t('asama_' + a)}: {yapan[a]}"
                for a in sira if a in yapan) or None,
            "durum": _durum(c["durum"]),
            "bitis": _bitis(c.get("bitis_sebebi")),
            "bitis_zamani": c.get("bitis_zamani"),
            "planlanan_tarih": c.get("planlanan_tarih"),
            "hasta_durumu": (metinler.t("arsiv") if c["hasta_durum"] == "arsiv"
                             else None),
        }
        sonuc.append((tip, d))
    return sonuc, tedavi_no


def tumu_sayfalari():
    """Bütün tedaviler, tedavi türü başına bir sayfa (`TUM_SAYFALAR`), satır
    başına bir tedavi; sonda "Yumurta ve embriyolar", örnek başına (v6.239).

    Bir sayfanın sütunları tiplerinin aşamalarından (`TUM_SUTUNLAR`): FET'te
    OPU ve stimülasyon yok, Yumurta Dondurma'da transfer ve gebelik yok.
    Tedavisi olmayan sayfa da basılıyor (yalnızca başlık) -- "bu türden hiç
    tedavi yok" demek. Her tedavi bir kez, tipinin sayfasında.
    """
    # Tek bağlantı (`db.ortak_baglanti()`): döküm binlerce küçük sorgu atıyor
    # (çözülen her embriyonun tüpü, kalitesi), her biri bağlantı açsa deneme
    # kopyasında 4 sn yalnızca bağlantı açmaya giderdi.
    with db.ortak_baglanti() as b:
        tedaviler, tedavi_no = _tum_veri(b)
        sayfalar = _tum_sayfalar(tedaviler, tedavi_no)
    return sayfalar


def _tum_sayfalar(tedaviler, tedavi_no):
    """`tumu_sayfalari()`'nın sayfaları: tedaviler tiplerinin sayfasına,
    sonda örnekler."""
    tip_sayfasi = {t: ad for ad, tipler in TUM_SAYFALAR for t in tipler}
    sayfalar = [(ad, tipler) for ad, tipler in TUM_SAYFALAR]
    for tip in dict.fromkeys(t for t, _ in tedaviler):
        if tip not in tip_sayfasi:
            tip_sayfasi[tip] = _tip(tip) or str(tip)
            sayfalar.append((tip_sayfasi[tip], (tip,)))

    cikti = []
    for ad, tipler in sayfalar:
        sutunlar = [(baslik, anahtar, kosul) for baslik, anahtar, kosul
                    in TUM_SUTUNLAR if kosul(tipler)]
        # Hücre satırın KENDİ tipine göre: FET sayfasının Blastokist'i FET
        # (3→5) için var, düz FET'in satırında boş -- tedavi ekranının özet
        # kutusu gibi (`cycle_ozet()`), aşaması olmayan tipte "0" ölçülmemişi
        # ölçülmüş gösterirdi. (Aktarılan FET'te transfer günü değerlendirmesi
        # bir sayı verirdi; kalitesi "Transfer edilen"de.)
        satirlar = [[d.get(anahtar) if kosul((tip,)) else None
                     for _, anahtar, kosul in sutunlar]
                    for tip, d in tedaviler if tip_sayfasi[tip] == ad]
        cikti.append((ad, [baslik for baslik, _, _ in sutunlar], satirlar))

    # Örnekler: tedavisinin sırasıyla (tedavi sayfalarınınki), içinde numara.
    h = _etiket_haritasi()
    sira = {d["id"]: i for i, (_, d) in enumerate(tedaviler)}
    bilgi = {d["id"]: d for _, d in tedaviler}
    tasiyicilar = _tasiyicilar()
    ornekler = sorted(_ornek_satirlari("1 = 1"),
                      key=lambda o: (sira.get(o["cycle_id"], len(sira)),
                                     o["cycle_sira_no"] or 0, o["id"]))
    satirlar = []
    for o in ornekler:
        c = bilgi.get(o["cycle_id"])
        if c is None:
            continue                     # başka laboratuvarın tedavisi
        etiket, _konum = tasiyicilar.get(o["vit_tasiyici"], (None, None))
        satirlar.append([c["dosya_no"], c["ad_soyad"], c["cycle_no"], c["tip"]]
                        + _ornek_degerleri(o, f"{c['dosya_no']}-{o['id']}", h,
                                           etiket, tedavi_no=tedavi_no))
    cikti.append(("Yumurta ve embriyolar", TUM_ORNEK_BASLIK, satirlar))
    return cikti


# --------------------------------------------------------------- istatistikler

# İstatistik penceresi: kaç aylık geçmişe bakılacağı. Ay ay kırılım bundan
# çıkıyor; daha uzunu ekranı şişiriyor, Excel çıktısı zaten tam veriyi veriyor.
ISTATISTIK_AY = 12


def _tek(sql, p=()):
    r = db.tek(sql, p)
    return (r["n"] if r and r["n"] is not None else 0)


def istatistikler(ay: str = "") -> dict:
    """Yönetici panelindeki sayılar — **anlık hesaplanır, saklanmaz**.

    Kullanıcının sorusu: "yapılan her kayıt hasta olsun cycle olsun opu olsun
    yönetici bölümünde yer alan bir istatistikler bölümüne anlık kaydedilebilir
    mi?" Cevap: kaydedilmesine gerek yok, zaten kayıtlı. Sayılar her açılışta
    `hasta`, `cycle`, `specimen` ve `olay` tablolarından hesaplanıyor.

    **Ayrı bir sayaç tutulmuyor, bilinçli.** Sayaç tutmak aynı bilgiyi iki
    yere yazmak demek; biri ötekinden ayrı düşer (bir kayıt silinir, bir göç
    araya girer, bir işlem yarım kalır) ve hangisinin doğru olduğu
    anlaşılmaz. Türetilmiş sayı her zaman doğrudur — cryo haritasının
    türetilmiş olmasıyla aynı gerekçe.

    `ay="2026-09"` verilirse sayılar o aya süzülür; boşsa laboratuvarın
    tamamı. Ayın ölçüsü ekranlardakiyle aynı: OPU tarihi, yoksa cycle'ın
    açıldığı tarih.
    """
    if ay:
        cs = ("AND strftime('%Y-%m', COALESCE(c.opu_zamani, c.olusturma_zamani)) "
              "= '" + ay.replace("'", "") + "'")
    else:
        cs = ""

    # Cryo Haritası Excel'inden açılan program öncesi tedaviler (v6.179)
    # dışarıda: yalnızca dondurma bilgisi var, OPU/ICSI/döllenme yok --
    # oranlara girseler ölçülmemişi ölçülmüş gösterirlerdi ("%0 MII").
    cycle_kosul = (f"c.lab_id = ? {cs} AND COALESCE(c.protokol_notu, '') "
                   f"NOT LIKE '%{db.CRYO_EXCEL_ISARETI}%'")
    ornek_kosul = ("s.cycle_id IN (SELECT c.id FROM cycle c "
                   f"WHERE {cycle_kosul})")

    def _olay(tip, ek=""):
        return _tek(
            "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
            f"JOIN specimen s ON s.id = o.specimen_id WHERE {ornek_kosul} "
            f"AND o.tip = ? AND o.iptal_mi = 0 {ek}", (db.LAB_ID, tip))

    # "Kayıtlı oosit" yalnızca yumurta TOPLANAN tedavilerden sayılır. FET
    # tipi tedavilerde (`db.FET_TIPLERI`) OPU yok; oradaki örnek çözülmüş bir
    # embriyo/yumurtadır, toplanmış bir oosit değil -- MII oranının paydasına
    # girerse oran olduğundan düşük çıkar. Program bugün FET'e specimen
    # yazmıyor ama program öncesi kayıtlar aktarıldığında (transferi görünür
    # kılmak için FET'in embriyoları kendi altına açılıyor) bu satırlar
    # gerçekten oluşuyor.
    fet_dislama = " AND c2.cycle_tipi NOT IN (%s)" % ",".join(
        "'%s'" % t for t in db.FET_TIPLERI)
    oosit = _tek(f"SELECT COUNT(*) n FROM specimen s "
                 f"JOIN cycle c2 ON c2.id = s.cycle_id "
                 f"WHERE {ornek_kosul}{fet_dislama}", (db.LAB_ID,))
    # MII de yalnızca TOPLANAN yumurtalardan (v6.147): oranın paydası
    # "kayıtlı oosit" FET tiplerini dışlıyor, pay dışlamasaydı Yumurta
    # Çözme'nin program öncesi aktarılan (kendi altına açılan) yumurtaları
    # oranı %100'ün üstüne bile çıkarabilirdi. Programda çözülen yumurta
    # Yumurta Dondurma'nın örneği, zaten orada bir kez sayılıyor (DISTINCT).
    mii = _olay("maturasyon_kontrolu", "AND o.mat_deger = 'mii' AND s.cycle_id IN "
                "(SELECT c2.id FROM cycle c2 WHERE 1=1" + fet_dislama + ")")
    icsi = _olay("icsi")
    ikipn = _olay("fertilizasyon_kontrolu", "AND o.fert_pn_sayisi = '2'")
    blast = _olay("blastokist_degerlendirme")
    donan = _olay("vitrifikasyon")
    cozulen = _olay("thaw")

    # Transfer ve gebelik cycle'a bağlı: transfer edilen embriyo başka
    # cycle'dan gelmiş olabilir (FET), ölçü tedavinin yapıldığı cycle.
    transfer_cycle = _tek(
        "SELECT COUNT(DISTINCT COALESCE(o.tr_cycle_id, s.cycle_id)) n "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 "
        "AND COALESCE(o.tr_cycle_id, s.cycle_id) IN "
        f"(SELECT c.id FROM cycle c WHERE {cycle_kosul})", (db.LAB_ID,))
    transfer_embriyo = _tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 "
        "AND COALESCE(o.tr_cycle_id, s.cycle_id) IN "
        f"(SELECT c.id FROM cycle c WHERE {cycle_kosul})", (db.LAB_ID,))

    gebelik_var = _kolon_var("gebelik_sonucu", "klinik_gebelik")
    # `evet` (gebelik ekranı) ya da `1` (ilk kayıtlar): v6.201'e kadar
    # yalnızca `1` sayılıyordu (`db.klinik_gebelik_sql()`).
    gebelik = _tek(
        f"SELECT COUNT(*) n FROM gebelik_sonucu g WHERE {db.klinik_gebelik_sql('g')} "
        f"AND g.cycle_id IN (SELECT c.id FROM cycle c WHERE {cycle_kosul})",
        (db.LAB_ID,)) if gebelik_var else 0

    # Gebelik testi pozitif (v6.241): beta hCG'si eşiği geçen tedavi
    # (`db.beta_pozitif_sql()`); klinik gebelikten ayrı sayı, payda aynı
    # (transfer yapılan tedavi).
    beta_var = db.tablo_var("beta_hcg")
    beta = _tek(
        f"SELECT COUNT(*) n FROM cycle c WHERE {cycle_kosul} "
        f"AND {db.beta_pozitif_sql('c.id')}", (db.LAB_ID,)) if beta_var else 0

    cycle_sayisi = _tek(
        f"SELECT COUNT(*) n FROM cycle c WHERE {cycle_kosul}", (db.LAB_ID,))
    tipler = db.sorgu(
        "SELECT c.cycle_tipi, COUNT(*) n FROM cycle c "
        f"WHERE {cycle_kosul} GROUP BY c.cycle_tipi ORDER BY n DESC",
        (db.LAB_ID,))
    durumlar = db.sorgu(
        "SELECT c.durum, COUNT(*) n FROM cycle c "
        f"WHERE {cycle_kosul} GROUP BY c.durum", (db.LAB_ID,))

    return {
        "ay": ay,
        "hasta": _tek("SELECT COUNT(*) n FROM hasta WHERE lab_id = ?",
                      (db.LAB_ID,)) if not ay else None,
        "hasta_aktif": _tek(
            "SELECT COUNT(*) n FROM hasta WHERE lab_id=? AND durum='aktif'",
            (db.LAB_ID,)) if not ay else None,
        "cycle": cycle_sayisi,
        "tipler": [(_tip(r["cycle_tipi"]) or r["cycle_tipi"], r["n"])
                   for r in tipler],
        "durumlar": [(_durum(r["durum"]), r["n"]) for r in durumlar],
        "opu": _tek("SELECT COUNT(*) n FROM cycle c "
                    f"WHERE {cycle_kosul} AND c.opu_zamani IS NOT NULL",
                    (db.LAB_ID,)),
        "oosit": oosit,
        "mii": mii,
        "icsi": icsi,
        "ikipn": ikipn,
        "blast": blast,
        "donan": donan,
        "cozulen": cozulen,
        "transfer_cycle": transfer_cycle,
        "transfer_embriyo": transfer_embriyo,
        "gebelik": gebelik,
        "gebelik_var": gebelik_var,
        "beta": beta,
        "beta_var": beta_var,
        "foto": _tek("SELECT COUNT(*) n FROM goruntu g WHERE g.cycle_id IN "
                     f"(SELECT c.id FROM cycle c WHERE {cycle_kosul})",
                     (db.LAB_ID,)),
        # Oranlar: payda sıfırsa None -- "%0" yazmak yanıltıcı olurdu.
        "oran_mii": _oran(mii, oosit),
        "oran_fert": _oran(ikipn, icsi),
        "oran_blast": _oran(blast, ikipn),
        "oran_gebelik": _oran(gebelik, transfer_cycle),
        "oran_beta": _oran(beta, transfer_cycle),
    }


def _oran(pay, payda):
    """Yüzde, bir ondalık. Payda sıfırsa None — "%0" yanıltıcı olurdu."""
    if not payda:
        return None
    return round(pay * 100.0 / payda, 1)


def istatistik_aylari(yil: int = 0, n: int = ISTATISTIK_AY) -> list:
    """Ay ay kırılım: sayılar **ve oranlar** (v6.123, kullanıcının isteği;
    v6.241'den beri beşinci oran gebelik testi).

    `yil` verilirse o yılın on iki ayı, verilmezse bugünden geriye `n` ay
    (eski davranış). Ekran yıl seçicisiyle çalıştığı için hep yıl veriyor;
    Excel çıktısı da ekrandaki yılı taşıyor, böylece düğmeye basınca
    bakılan yıl iniyor.

    **Oranlar burada hesaplanmıyor, `istatistikler(ay)` hesaplıyor** —
    ekranın üstündeki kart ile bu tablo aynı tanımı kullansın diye. İki
    ayrı formül yazılsaydı biri düzeltilip öteki unutulurdu; sayaç
    tutmama gerekçesinin (v6.38) formül hali.

    Kaydı olmayan ay listeye girmez: "o ay iş yapılmadı" bilgisi satırın
    yokluğundan okunuyor, on iki satır tire tabloyu uzatmaktan başka bir
    şey yapmazdı.
    """
    from datetime import date
    if yil:
        aylar = [f"{yil:04d}-{a:02d}" for a in range(1, 13)]
    else:
        bugun = date.today()
        aylar, y, a = [], bugun.year, bugun.month
        for _ in range(n):
            aylar.append(f"{y:04d}-{a:02d}")
            a -= 1
            if a == 0:
                y, a = y - 1, 12
        aylar.reverse()
    satirlar = []
    for a in aylar:
        i = istatistikler(a)
        if i["cycle"]:
            satirlar.append({
                "ay": a, "cycle": i["cycle"], "oosit": i["oosit"],
                "mii": i["mii"], "icsi": i["icsi"], "ikipn": i["ikipn"],
                "blast": i["blast"], "transfer": i["transfer_cycle"],
                "gebelik": i["gebelik"], "beta": i["beta"],
                "oran_mii": i["oran_mii"], "oran_fert": i["oran_fert"],
                "oran_blast": i["oran_blast"], "oran_gebelik": i["oran_gebelik"],
                "oran_beta": i["oran_beta"],
            })
    return satirlar


# "Son kayıtlar" penceresi (v6.124, kullanıcının isteği: "son kayıtları
# sayfada çok gösterme haftalık tut ... beş sayfada göster ki çok uzun liste
# olmasın"). Üçü birlikte kartın boyunu sabitliyor: en çok 5x5 = 25 satır ve
# hepsi son bir haftadan. Sayfa boyu **5**, ana ekranın üç kartındaki
# "en fazla 5 satır" ölçüsüyle (v6.78) aynı — kullanıcının zaten seçtiği boy.
SON_KAYIT_GUN = 7            # kaç günlük geçmişe bakılıyor
SON_KAYIT_SAYFA_BOYU = 5     # bir sayfada kaç satır
SON_KAYIT_EN_COK_SAYFA = 5   # en çok kaç sayfa


def son_kayitlar(sayfa: int = 1) -> dict:
    """Son bir haftada girilen kayıtlar — hasta, cycle ve laboratuvar işlemleri.

    Kullanıcının "yapılan her kayıt ... anlık" isteğinin ikinci yarısı:
    sayıların yanında **ne olduğu** da görünsün. Üç tablodan okunup zamana
    göre birleştiriliyor; ayrı bir günlük tablosu tutulmuyor (bkz.
    `istatistikler`).

    **Pencere bir hafta, liste sayfalı** (v6.124). Önce sabit on satırdı;
    kullanıcı hem listenin kısalmasını hem de geçmişin haftayla sınırlanmasını
    istedi. Bu hâlâ bir kayıt defteri değil, "bu hafta ne yapıldı" penceresi —
    tam döküm `/disari/tumu`'da. Sınırı aşan kayıt **gizlenmiyor, yok**:
    kart en çok `SON_KAYIT_EN_COK_SAYFA` sayfa gösteriyor ve ekranda kaç
    kayıt olduğunu yazıyor, böylece "hepsi bu" sanılmıyor.

    **Ölçü `olusturma_zamani`, ve o şemanın `datetime('now')` varsayılanıyla
    yazılıyor — yani UTC.** Süzgeç de bu yüzden `datetime('now', '-7 days')`
    kullanıyor, `'localtime'` DEĞİL: iki tarafın aynı saate göre olması
    gerekiyor. Klinik tarih alanlarındaki (`bitis_zamani`, `planlanan_tarih`)
    `date('now','localtime')` deseniyle karıştırma — onlar personelin elle
    girdiği yerel zamanlar, bu ise veritabanının kendi damgası.
    """
    # Her tablodan en çok gösterilebilecek kadar çekip birleştiriyoruz:
    # birleşik listenin ilk N'i, her tablonun kendi ilk N'inin içindedir.
    en_cok = SON_KAYIT_SAYFA_BOYU * SON_KAYIT_EN_COK_SAYFA
    pencere = f"-{SON_KAYIT_GUN} days"

    hasta = db.sorgu(
        "SELECT olusturma_zamani AS z, 'hasta' AS tur, dosya_no, ad_soyad, "
        "  NULL AS cycle_id, NULL AS cycle_no, NULL AS tip "
        "FROM hasta WHERE lab_id = ? AND olusturma_zamani >= datetime('now', ?) "
        "ORDER BY olusturma_zamani DESC LIMIT ?",
        (db.LAB_ID, pencere, en_cok))
    cycle = db.sorgu(
        "SELECT c.olusturma_zamani AS z, 'cycle' AS tur, h.dosya_no, h.ad_soyad, "
        "  c.id AS cycle_id, c.cycle_no, c.cycle_tipi AS tip "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
        "WHERE c.lab_id = ? AND c.olusturma_zamani >= datetime('now', ?) "
        "ORDER BY c.olusturma_zamani DESC LIMIT ?",
        (db.LAB_ID, pencere, en_cok))
    olay = db.sorgu(
        "SELECT o.olusturma_zamani AS z, 'olay' AS tur, h.dosya_no, h.ad_soyad, "
        "  c.id AS cycle_id, c.cycle_no, o.tip "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE o.lab_id = ? AND o.iptal_mi = 0 "
        "  AND o.olusturma_zamani >= datetime('now', ?) "
        "ORDER BY o.olusturma_zamani DESC LIMIT ?", (db.LAB_ID, pencere, en_cok))

    hepsi = [dict(r) for r in list(hasta) + list(cycle) + list(olay)]
    hepsi.sort(key=lambda r: r["z"] or "", reverse=True)
    sinirli = len(hepsi) > en_cok          # haftada bundan fazlası var
    hepsi = hepsi[:en_cok]
    for r in hepsi:
        if r["tur"] == "cycle":
            r["ad"] = _tip(r["tip"]) or r["tip"]
        elif r["tur"] == "olay":
            r["ad"] = metinler.t("olay_" + r["tip"]) if r["tip"] else ""
        else:
            r["ad"] = ""

    # Sayfa sunucuda kendi aralığına sabitleniyor: aralık dışı bir değer
    # hataya değil son sayfaya düşer (/hastalar'daki kuralın aynısı).
    sayfa_toplam = max(1, -(-len(hepsi) // SON_KAYIT_SAYFA_BOYU))  # tavana yuvarla
    sayfa = min(max(sayfa, 1), sayfa_toplam)
    bas = (sayfa - 1) * SON_KAYIT_SAYFA_BOYU
    return {
        "satirlar": hepsi[bas:bas + SON_KAYIT_SAYFA_BOYU],
        "sayfa": sayfa, "sayfa_toplam": sayfa_toplam,
        "toplam": len(hepsi), "gun": SON_KAYIT_GUN, "sinirli": sinirli,
    }


ISTATISTIK_BASLIK = ["Ay", "Cycle", "Yumurta", "MII", "ICSI yapılan", "2PN",
                     "Blastokist", "Transfer edilen cycle",
                     "Beta hCG pozitif", "Klinik gebelik",
                     "M2 oranı (%)", "Fertilizasyon oranı (%)",
                     "Blastokist oranı (%)",
                     "Beta hCG pozitif oranı (%)",
                     "Klinik gebelik oranı (%)"]


def istatistik_sayfalari(yil: int = 0):
    """İstatistiklerin Excel hali: ay ay kırılım + genel toplam.

    `yil` ekrandan geliyor (v6.123) — düğmeye basıldığında bakılan yıl
    insin diye. Ekranda oranların yanında **payı ve paydası** da yazıyor;
    burada da öyle: yalnızca yüzdeyi vermek "%100" ile "1/1"i ayırt
    edilemez yapardı.
    """
    aylar = [[s["ay"], s["cycle"], s["oosit"], s["mii"], s["icsi"],
              s["ikipn"], s["blast"], s["transfer"], s["beta"], s["gebelik"],
              s["oran_mii"], s["oran_fert"], s["oran_blast"],
              s["oran_beta"], s["oran_gebelik"]] for s in istatistik_aylari(yil)]
    g = istatistikler()
    genel = [
        ["Hasta (toplam)", g["hasta"]],
        ["Hasta (aktif)", g["hasta_aktif"]],
        ["Cycle", g["cycle"]],
        ["OPU yapılan cycle", g["opu"]],
        ["Oosit", g["oosit"]],
        ["MII", g["mii"]],
        ["ICSI yapılan", g["icsi"]],
        ["2PN", g["ikipn"]],
        ["Blastokist", g["blast"]],
        ["Dondurulan", g["donan"]],
        ["Çözülen", g["cozulen"]],
        ["Transfer edilen cycle", g["transfer_cycle"]],
        ["Transfer edilen embriyo", g["transfer_embriyo"]],
        [f"Beta hCG pozitif (≥ {db.BETA_POZITIF_ESIK} mIU/mL)", g["beta"]],
        ["Klinik gebelik", g["gebelik"]],
        ["Fotoğraf", g["foto"]],
        ["M2 oranı (%)", g["oran_mii"]],
        ["Fertilizasyon oranı (%)", g["oran_fert"]],
        ["Blastokist oranı (%)", g["oran_blast"]],
        ["Beta hCG pozitif oranı (%)", g["oran_beta"]],
        ["Klinik gebelik oranı (%)", g["oran_gebelik"]],
    ]
    return [(f"{yil} aylara göre" if yil else "Aylara göre",
             ISTATISTIK_BASLIK, aylar),
            ("Genel", ["Ölçü", "Değer"], genel)]


# --------------------------------------------------- Sağlık Bakanlığı (v6.201)

# Bakanlığın ünite olarak her ay istediği sayılar, onun sütun adları ve
# sırasıyla (kullanıcının gösterdiği form). IUI SAYISI ile EMBRİYO İMHA
# SAYISI bilerek yok, kullanıcının isteği ("IUI sayısı ve İmha Sayısı
# hariç"): v6.201'de programda tutulmuyorlardı. İmha v6.227'den beri tüpte
# kaydediliyor (`tasiyici.imha_zamani`); sütunu eklemek kullanıcıya soruldu,
# cevabı gelmeden ekleme. Adlar bakanlığın formunun yazısı --
# ekrandaki "tedavi"/"yumurta" kuralının (v6.79, v6.134) dışında, resmî
# formların kâğıt kalıbı gibi olduğu gibi duruyor ("SİKLUS", "OOSİT").
BAKANLIK_SUTUNLARI = [
    ("opu", "OPU SAYISI"),
    ("oosit", "DONDURULMUŞ OOSİT SAYISI"),
    ("tese", "TESE SAYISI"),
    ("sperm", "DONDURULMUŞ SPERM SAYISI"),
    ("siklus", "SİKLUS SAYISI"),
    ("transfer", "EMBRİYO TRANSFER SAYISI"),
    ("gebelik", "GEBELİK SAYISI"),
    ("dogum", "CANLI DOĞUM SAYISI"),
    ("hasta", "TOTAL HASTA SAYISI"),
]

# Kullanıcı: "2026 yılından öncesi olmasın". Program öncesi kayıtlar 2018'e
# kadar aktarıldı; bakanlığa verilen sayılar 2026'dan başlıyor.
BAKANLIK_ILK_YIL = 2026

# TESE SAYISI "bütün cerrahi alımlar" (kullanıcının seçimi): androlojide
# alınma yönteminin kodu, sperm dondurmada serbest metin sebep (öneri
# listesinde TESE, TESA, PESA var; "mikroTESE" de TESE'yi içeriyor).
CERRAHI_ALIM_KODLARI = ("tese", "mikrotese", "tesa", "pesa", "mesa")
CERRAHI_ALIM_SOZLERI = ("TESE", "TESA", "PESA", "MESA")


def bakanlik_verileri(yil: int) -> dict:
    """Sağlık Bakanlığı'nın aylık istediği sayılar, `yil`in ayları (v6.201).

    Her açılışta kayıtlardan türetiliyor, saklanmıyor ("istatistikler
    türetilmiştir", v6.38): sonradan düzeltilen bir kayıt geçmiş ayın
    sayısını da düzeltir. Tanımlar kullanıcının cevapları (2026-09-26):

    - OPU: OPU'su yapılan tedavi, OPU gününün ayına.
    - DONDURULMUŞ OOSİT: yumurta dondurma İŞLEMİ -- o ay yumurtası
      dondurulan tedavi (adet değil). Yumurta mı embriyo mu içerikten
      (`db.dondurulan_yumurta_sql()`), dondurmanın yapıldığı tedavi
      `db.vit_tedavisi()`.
    - TESE: bütün cerrahi alımlar (TESE, mikroTESE, TESA, PESA, MESA);
      androlojinin alınma yöntemi ve sperm dondurmanın sebebi, aynı kişi
      aynı gün bir kez.
    - DONDURULMUŞ SPERM: dondurma İŞLEMİ -- aynı kişinin aynı gün
      dondurulan tüpleri bir.
    - SİKLUS: bütün tedaviler (tipi ne olursa olsun, iptal edilen de),
      tedavinin günüyle (`db.tedavi_tarihi()`: OPU, hCG, FET'te çözme ya da
      transfer, planlanan tarih, açılış).
    - EMBRİYO TRANSFER: transfer işlemi -- tedavi ve gün başına bir (taze ve
      donmuş), transfer edilen embriyo sayısı değil.
    - GEBELİK: klinik gebelik (`db.klinik_gebelik_sql()`), gebelik
      ekranındaki kontrol zamanının ayına; kontrol zamanı yoksa sayılmıyor
      (`eksik_gebelik` o tedavileri listeliyor).
    - CANLI DOĞUM: sonucu canlı doğum olan gebelik, doğum zamanının ayına;
      ikiz doğum bir (`eksik_dogum`: doğum zamanı girilmemiş olanlar).
    - TOTAL HASTA: o ay yeni kaydedilen hasta. Ölçü hastanın İLK kaydı:
      kartın açılışı, ilk tedavisi, ilk sperm dondurması -- hangisi önceyse.
      Access'ten aktarılan hasta bu yüzden ilk tedavisinin ayında sayılıyor:
      aylar karışık sırayla aktarıldığı için kartın açılış tarihi, sonradan
      eklenen eski bir tedavinin gerisinde kalabiliyor (aktarım var olan
      kartın tarihine dokunmuyor).

    "Aynı kişi": erkeğin kendi kartı bir çiftin `es_dosya_no`'suyla o çifte
    bağlıysa ikisi bir sayılıyor (dosya numarası tek eşleştirme anahtarı,
    v6.125) -- aynı gün hem ICSI'de kullanılıp hem dondurulan TESE ikinci kez
    sayılmasın diye. Cryo Haritası Excel'inden açılan program öncesi
    tedaviler (`db.CRYO_EXCEL_ISARETI`) dışarıda, istatistiğin kuralı.
    """
    from collections import Counter
    from datetime import date as _date

    bas, son = f"{yil:04d}-01-01", f"{yil + 1:04d}-01-01"
    cryo = (f"COALESCE(c.protokol_notu, '') "
            f"NOT LIKE '%{db.CRYO_EXCEL_ISARETI}%'")
    kg = db.klinik_gebelik_sql("g")
    vt = db.vit_tedavisi("o")
    sayilar = {}

    b = db.baglan()
    try:
        def ay_say(sql, par):
            return {r[0]: r[1] for r in b.execute(sql, par) if r[0]}

        # Zamanlar ISO metin ("2026-03-04 10:15:00" ya da "...T10:15"): ay
        # ilk yedi harf, aralık metin karşılaştırması -- dizin kullanılabilsin.
        sayilar["opu"] = ay_say(
            "SELECT substr(c.opu_zamani, 1, 7), COUNT(*) FROM cycle c "
            f"WHERE c.lab_id = ? AND {cryo} AND c.opu_zamani >= ? "
            "AND c.opu_zamani < ? GROUP BY 1", (db.LAB_ID, bas, son))

        sayilar["oosit"] = ay_say(
            f"SELECT substr(o.zaman, 1, 7), COUNT(DISTINCT {vt}) FROM olay o "
            f"JOIN cycle c ON c.id = {vt} "
            "WHERE o.lab_id = ? AND o.tip = 'vitrifikasyon' AND o.iptal_mi = 0 "
            f"AND o.zaman >= ? AND o.zaman < ? AND {cryo} "
            f"AND {db.dondurulan_yumurta_sql('o')} = 1 GROUP BY 1",
            (db.LAB_ID, bas, son))

        # Erkeğin kartı -> bağlı olduğu çiftin kartı (`es_dosya_no`).
        es_cift = {}
        if db.kolon_var("hasta", "es_dosya_no"):
            es_cift = {r[0]: r[1] for r in b.execute(
                "SELECT e.id, MIN(h.id) FROM hasta h JOIN hasta e "
                "ON e.lab_id = h.lab_id AND e.dosya_no = h.es_dosya_no "
                "WHERE h.lab_id = ? GROUP BY e.id", (db.LAB_ID,))}
        tese, sperm = set(), set()          # (ay, kişi, gün)
        isaret = ",".join("?" * len(CERRAHI_ALIM_KODLARI))
        for gun, hid in b.execute(
                "SELECT substr(COALESCE(so.alinma_zamani, c.opu_zamani), 1, 10), "
                "c.hasta_id FROM sperm_ornek so JOIN cycle c ON c.id = so.cycle_id "
                f"WHERE c.lab_id = ? AND {cryo} AND so.alinma_yontemi IN ({isaret}) "
                "AND COALESCE(so.alinma_zamani, c.opu_zamani) >= ? "
                "AND COALESCE(so.alinma_zamani, c.opu_zamani) < ?",
                (db.LAB_ID, *CERRAHI_ALIM_KODLARI, bas, son)):
            tese.add((gun[:7], es_cift.get(hid, hid), gun))
        for gun, hid, sebep in b.execute(
                "SELECT substr(dondurma_zamani, 1, 10), hasta_id, sebep "
                "FROM sperm_dondurma WHERE lab_id = ? AND iptal_mi = 0 "
                "AND dondurma_zamani >= ? AND dondurma_zamani < ?",
                (db.LAB_ID, bas, son)):
            anahtar = (gun[:7], es_cift.get(hid, hid), gun)
            sperm.add(anahtar)
            if any(s in (sebep or "").upper() for s in CERRAHI_ALIM_SOZLERI):
                tese.add(anahtar)
        sayilar["tese"] = Counter(a for a, _k, _g in tese)
        sayilar["sperm"] = Counter(a for a, _k, _g in sperm)

        gun = db.tedavi_tarihi(b, "c")
        sayilar["siklus"] = ay_say(
            f"SELECT substr(t.g, 1, 7), COUNT(*) FROM (SELECT {gun} AS g "
            f"FROM cycle c WHERE c.lab_id = ? AND {cryo}) t "
            "WHERE t.g >= ? AND t.g < ? GROUP BY 1", (db.LAB_ID, bas, son))

        sayilar["transfer"] = ay_say(
            "SELECT substr(o.zaman, 1, 7), COUNT(DISTINCT "
            "COALESCE(o.tr_cycle_id, s.cycle_id) || ' ' || substr(o.zaman, 1, 10)) "
            "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
            "JOIN cycle c ON c.id = COALESCE(o.tr_cycle_id, s.cycle_id) "
            f"WHERE o.lab_id = ? AND o.tip = 'transfer' AND o.iptal_mi = 0 "
            f"AND {cryo} AND o.zaman >= ? AND o.zaman < ? GROUP BY 1",
            (db.LAB_ID, bas, son))

        sayilar["gebelik"] = ay_say(
            "SELECT substr(g.fk_kontrol_zamani, 1, 7), COUNT(*) "
            f"FROM gebelik_sonucu g WHERE g.lab_id = ? AND {kg} "
            "AND g.fk_kontrol_zamani >= ? AND g.fk_kontrol_zamani < ? GROUP BY 1",
            (db.LAB_ID, bas, son))
        sayilar["dogum"] = ay_say(
            "SELECT substr(g.dogum_zamani, 1, 7), COUNT(*) FROM gebelik_sonucu g "
            "WHERE g.lab_id = ? AND g.sonlanma = 'canli_dogum' "
            "AND g.dogum_zamani >= ? AND g.dogum_zamani < ? GROUP BY 1",
            (db.LAB_ID, bas, son))

        # Hastanın ilk kaydı. Kartın açılışı `olusturma_zamani`: programda
        # açılan kartta şemanın UTC damgası, aktarılanda tedavinin yerel
        # günü (08:00) -- `localtime` ikincisini aynı günde bırakıyor.
        ilk = {}

        def ilk_yaz(rows):
            for hid, z in rows:
                if z and (hid not in ilk or z < ilk[hid]):
                    ilk[hid] = z
        ilk_yaz(b.execute("SELECT id, date(olusturma_zamani, 'localtime') "
                          "FROM hasta WHERE lab_id = ?", (db.LAB_ID,)))
        ilk_yaz(b.execute(f"SELECT c.hasta_id, MIN({gun}) FROM cycle c "
                          "WHERE c.lab_id = ? GROUP BY c.hasta_id", (db.LAB_ID,)))
        ilk_yaz(b.execute("SELECT hasta_id, MIN(substr(dondurma_zamani, 1, 10)) "
                          "FROM sperm_dondurma WHERE lab_id = ? AND iptal_mi = 0 "
                          "GROUP BY hasta_id", (db.LAB_ID,)))
        sayilar["hasta"] = Counter(z[:7] for z in ilk.values() if bas <= z < son)

        # Tarihi girilmemiş için sayılmayanlar: bu ayların birine düşebilecek
        # olanlar (tedavisi bir önceki yıldan bu yana).
        esik = f"{BAKANLIK_ILK_YIL - 1}-01-01"

        def eksik(kosul):
            return b.execute(
                f"SELECT c.id, c.cycle_no, h.dosya_no, h.ad_soyad, {gun} AS gun "
                "FROM gebelik_sonucu g JOIN cycle c ON c.id = g.cycle_id "
                "JOIN hasta h ON h.id = c.hasta_id "
                f"WHERE g.lab_id = ? AND {kosul} AND {gun} >= ? ORDER BY gun, c.id",
                (db.LAB_ID, esik)).fetchall()
        eksik_gebelik = eksik(f"{kg} AND COALESCE(g.fk_kontrol_zamani, '') = ''")
        eksik_dogum = eksik("g.sonlanma = 'canli_dogum' "
                            "AND COALESCE(g.dogum_zamani, '') = ''")
    finally:
        b.close()

    bugun = _date.today()
    son_ay = 12 if yil < bugun.year else bugun.month
    aylar = []
    for m in range(1, son_ay + 1):
        ay = f"{yil:04d}-{m:02d}"
        satir = {"ay": ay, "no": m,
                 "suruyor": (yil, m) == (bugun.year, bugun.month)}
        for a, _ad in BAKANLIK_SUTUNLARI:
            satir[a] = sayilar[a].get(ay, 0)
        aylar.append(satir)
    return {
        "yil": yil,
        "aylar": aylar,
        "toplam": {a: sum(s[a] for s in aylar) for a, _ad in BAKANLIK_SUTUNLARI},
        "eksik_gebelik": eksik_gebelik,
        "eksik_dogum": eksik_dogum,
    }


def bakanlik_sayfalari(yil: int):
    """Bakanlık verilerinin Excel hali: ekrandaki tablonun aynısı, bakanlığın
    sütun adlarıyla. Süren ay yıldızlı ("Eylül 2026 *"): ay bitmedi."""
    v = bakanlik_verileri(yil)
    satirlar = []
    for s in v["aylar"]:
        ad = f"{metinler.t('ay_' + str(s['no']))} {yil}"
        satirlar.append([ad + (" *" if s["suruyor"] else "")]
                        + [s[a] for a, _ad in BAKANLIK_SUTUNLARI])
    satirlar.append([metinler.t("toplam")]
                    + [v["toplam"][a] for a, _ad in BAKANLIK_SUTUNLARI])
    return [(f"Bakanlık {yil}",
             ["AY"] + [ad for _a, ad in BAKANLIK_SUTUNLARI], satirlar)]
