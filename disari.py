"""Excel çıktısı için verinin hazırlanması.

Rotalar `app.py`'de (projenin kuralı: bütün rotalar orada); burada yalnızca
sorgular ve satırların kurulması var — `app.py` zaten 4500 satır.

Dört çıktı:

  - `ay_sayfalari(ay)`       — o ayın cycle'ları, satır başına bir cycle
  - `cycle_sayfalari(id)`    — bir cycle'ın tamamı, satır başına bir örnek
  - `cryo_sayfalari()`       — dolabın dökümü, satır başına bir örnek
  - `tumu_sayfalari()`       — tabloların ham dökümü, tablo başına bir sayfa

Hepsi `excel.kitap()`'ın beklediği `[(ad, başlıklar, satırlar), ...]` biçimini
döndürüyor.

**Kod değil etiket yazılır.** `mii`, `2pn`, `z1` gibi değerler laba özgü ve
yönetici düzenleyebiliyor (`liste_degeri`); ekranda olduğu gibi Excel'de de
etiketleri görünmeli. Etiketler tek sorguda okunup sözlüğe alınıyor — satır
başına sorgu atmak 40 oositlik bir cycle'da 400 sorgu demek olurdu.

**"Tüm veri" dökümünde şifre ve oturum anahtarı yok.** `kullanici` tablosundan
yalnızca kimlik alanları alınıyor (`kullanici_id` kolonlarını okumak için
lazım), `sifre_hash` ve `oturum` tablosu hiç çıkmıyor. Dosya klinik dışına
çıkabilir; bu bilinçli.
"""

import db
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


def _kolon_var(tablo: str, kolon: str) -> bool:
    """Göç çalıştırılmamış olabilir (tuzak #3) — çıktı yine de alınabilmeli."""
    return any(r["name"] == kolon for r in db.sorgu(f"PRAGMA table_info({tablo})"))


# ------------------------------------------------------------------ ay listesi

AY_BASLIK = [
    "Dosya no", "Hasta", "Cycle no", "Hastanın kaçıncı cycle'ı", "Tip",
    "Endikasyon", "Protokol", "Gonadotropin", "Toplam doz", "Stim günü",
    "Trigger", "AMH", "AFC", "Folikül", "Endometrium (mm)",
    "OPU tarihi", "OPU hekimi", "Toplam oosit", "Sağ", "Sol",
    "MII", "ICSI yapılan", "2PN", "Gün 2", "Gün 3", "Blastokist",
    "Donan", "Çözülen", "Transfer", "Durum", "Bitiş sebebi", "Bitiş tarihi",
    "Planlanan tarih", "Hasta durumu",
]


def ay_sayfalari(ay: str, baslik: str):
    """O ay işlem yapılan cycle'lar, satır başına bir cycle.

    Ayın ölçüsü ekrandakiyle aynı: OPU tarihi, yoksa cycle'ın açıldığı tarih
    (FET'te OPU olmuyor — bkz. CLAUDE.md "Hasta kayıtları ay ay").

    Aşama sayıları cycle'ın **kendi** örneklerinden geliyor; çözme ve transfer
    ise tedavinin yapıldığı cycle'dan (`thaw_cycle_id` / `tr_cycle_id`). Bir
    FET cycle'ında oosit yoktur ama transfer vardır — sayının doğru cycle'da
    görünmesi böyle sağlanıyor.
    """
    h = _etiket_haritasi()
    bitis_var = _kolon_var("cycle", "bitis_sebebi")
    plan_var = _kolon_var("cycle", "planlanan_tarih")
    bitis = ("c.bitis_sebebi, c.bitis_zamani" if bitis_var
             else "NULL AS bitis_sebebi, NULL AS bitis_zamani")
    plan = "c.planlanan_tarih" if plan_var else "NULL AS planlanan_tarih"

    satirlar = db.sorgu(
        f"""
        SELECT c.*, {bitis}, {plan},
               h.dosya_no, h.ad_soyad, h.durum AS hasta_durum,
               (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id) AS oosit,
               (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id
                 AND s.taraf = 'sag') AS sag,
               (SELECT COUNT(*) FROM specimen s WHERE s.cycle_id = c.id
                 AND s.taraf = 'sol') AS sol,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'maturasyon_kontrolu' AND o.mat_deger = 'mii') AS mii,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'icsi') AS icsi,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'fertilizasyon_kontrolu'
                  AND o.fert_pn_sayisi = '2') AS ikipn,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'cleavage_degerlendirme' AND o.gun = 2) AS gun2,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'cleavage_degerlendirme' AND o.gun = 3) AS gun3,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'blastokist_degerlendirme') AS blast,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE s.cycle_id = c.id AND o.iptal_mi = 0
                  AND o.tip = 'vitrifikasyon') AS donan,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE o.iptal_mi = 0 AND o.tip = 'thaw'
                  AND COALESCE(o.thaw_cycle_id, s.cycle_id) = c.id) AS cozulen,
               (SELECT COUNT(DISTINCT o.specimen_id) FROM olay o
                 JOIN specimen s ON s.id = o.specimen_id
                WHERE o.iptal_mi = 0 AND o.tip = 'transfer'
                  AND COALESCE(o.tr_cycle_id, s.cycle_id) = c.id) AS transfer
          FROM cycle c JOIN hasta h ON h.id = c.hasta_id
         WHERE c.lab_id = ?
           AND strftime('%Y-%m', COALESCE(c.opu_zamani, c.olusturma_zamani)) = ?
         ORDER BY COALESCE(c.opu_zamani, c.olusturma_zamani), h.dosya_no
        """,
        (db.LAB_ID, ay))

    cikti = []
    for c in satirlar:
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
            c["mii"], c["icsi"], c["ikipn"], c["gun2"], c["gun3"], c["blast"],
            c["donan"], c["cozulen"], c["transfer"],
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
        ("OPU sağ oosit", c["opu_sag_oosit"]),
        ("OPU sol oosit", c["opu_sol_oosit"]),
        ("Denüdasyon saati", c["denudasyon_zamani"]),
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
    ornekler = db.sorgu(
        f"""
        SELECT s.id, s.cycle_sira_no, s.taraf, s.durum,
               {_son_alt('mat_deger', 'maturasyon_kontrolu')} AS mat,
               {_son_alt('zaman', 'maturasyon_kontrolu')} AS mat_zaman,
               {_son_alt('icsi_sonuc', 'icsi')} AS icsi,
               {_son_alt('icsi_gecis_zorlugu', 'icsi')} AS zorluk,
               {_son_alt('zaman', 'icsi')} AS icsi_zaman,
               {_son_alt('fert_sonuc', 'fertilizasyon_kontrolu')} AS fert,
               {_son_alt('fert_pn_sayisi', 'fertilizasyon_kontrolu')} AS pn,
               {_son_alt('fert_pn_skoru', 'fertilizasyon_kontrolu')} AS pn_skor,
               {_son_alt('zaman', 'fertilizasyon_kontrolu')} AS fert_zaman,
               {_gun_alt('cl_hucre_sayisi', 'cleavage_degerlendirme', 2)} AS g2_hucre,
               {_gun_alt('cl_simetri', 'cleavage_degerlendirme', 2)} AS g2_sim,
               {_gun_alt('cl_fragmentasyon', 'cleavage_degerlendirme', 2)} AS g2_frag,
               {_gun_alt('cl_skor', 'cleavage_degerlendirme', 2)} AS g2_skor,
               {_gun_alt('cl_hucre_sayisi', 'cleavage_degerlendirme', 3)} AS g3_hucre,
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
               {_son_alt('zaman', 'thaw')} AS thaw_zaman,
               {_son_alt('thaw_sagkalim', 'thaw')} AS sagkalim,
               {_son_alt('thaw_re_expansion', 'thaw')} AS re_exp,
               {_son_alt('zaman', 'transfer')} AS tr_zaman,
               {_son_alt('tr_tipi', 'transfer')} AS tr_tipi,
               (SELECT group_concat(x.notlar, ' | ') FROM olay x
                 WHERE x.specimen_id = s.id AND x.iptal_mi = 0
                   AND x.notlar IS NOT NULL AND x.notlar <> '') AS notlar
          FROM specimen s WHERE s.cycle_id = ? ORDER BY s.cycle_sira_no
        """,
        (cycle_id,))

    # Taşıyıcı etiketi ve konumu: örnek başına sorgu atmak yerine tek okuma.
    tasiyicilar = {r["id"]: (r["etiket"], r["tam_yol"]) for r in db.sorgu(
        "SELECT t.id, t.etiket, k.tam_yol FROM tasiyici t "
        "LEFT JOIN konum k ON k.id = t.konum_id WHERE t.lab_id = ?",
        (db.LAB_ID,))}

    satirlar = []
    for o in ornekler:
        etiket, konum = tasiyicilar.get(o["vit_tasiyici"], (None, None))
        satirlar.append([
            f"{c['dosya_no']}-{o['id']}", o["cycle_sira_no"],
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
            o["vit_zaman"], etiket, konum,
            o["thaw_zaman"], _et(h, "thaw_sagkalim", o["sagkalim"]), o["re_exp"],
            o["tr_zaman"], o["tr_tipi"],
            _ornek_durum(o["durum"]), o["notlar"],
        ])

    ad = f"{c['dosya_no']}-{c['cycle_no']}"
    return ad, [("Cycle bilgisi", ["Alan", "Değer"],
                 [[a, d] for a, d in bilgi]),
                ("Örnekler", ORNEK_BASLIK, satirlar)]


# ------------------------------------------------------------------ cryo dökümü

CRYO_BASLIK = [
    "Dolapta", "Konum", "Taşıyıcı", "Taşıyıcı tipi", "Renk",
    "Dosya no", "Hasta", "Cycle no", "Tip", "Örnek kodu", "No",
    "Blastokist skoru", "Dondurma", "Çözme", "Sağkalım", "Transfer",
    "Örnek durumu",
]


def cryo_sayfalari():
    """Tanktaki örneklerin dökümü — sayım ve envanter için.

    Çözülmüş örnekler de listede; "Dolapta" sütunu ayırıyor. Böylece aynı
    dosya hem bugünkü sayımı hem o taşıyıcının geçmişini veriyor; Excel'in
    süzgeciyle biri ötekinden ayrılıyor.

    Cryo haritası gibi bu da **türetilmiş**: elle güncellenen bir konum
    tablosu yok, liste vitrifikasyon ve çözme kayıtlarından çıkıyor.
    """
    h = _etiket_haritasi()
    satirlar = db.sorgu(
        f"""
        SELECT k.tam_yol, t.etiket, t.tip AS tasiyici_tipi, t.renk,
               o.zaman AS dondurma,
               h.dosya_no, h.ad_soyad, c.cycle_no, c.cycle_tipi,
               s.id AS ornek, s.cycle_sira_no, s.durum AS ornek_durum,
               {_son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC')} AS skor,
               {_son_alt('zaman', 'thaw')} AS cozme,
               {_son_alt('thaw_sagkalim', 'thaw')} AS sagkalim,
               {_son_alt('zaman', 'transfer')} AS transfer
          FROM olay o
          JOIN specimen s ON s.id = o.specimen_id
          JOIN cycle c ON c.id = s.cycle_id
          JOIN hasta h ON h.id = c.hasta_id
          LEFT JOIN tasiyici t ON t.id = o.vit_tasiyici_id
          LEFT JOIN konum k ON k.id = t.konum_id
         WHERE o.lab_id = ? AND o.tip = 'vitrifikasyon' AND o.iptal_mi = 0
         ORDER BY k.tam_yol, t.etiket, h.dosya_no, s.cycle_sira_no
        """,
        (db.LAB_ID,))

    cikti = []
    for r in satirlar:
        dolapta = not r["cozme"] and r["ornek_durum"] == "dondurulmus"
        cikti.append([
            "Evet" if dolapta else "Hayır",
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

# Hangi tablolar dökülüyor. Sıra okunma sırası: önce kimlik, sonra işlem.
# **`oturum` ve `yetki` burada yok**, `kullanici` da tam değil (aşağıya bak):
# bu dosya klinik dışına çıkabilir, şifre özeti ve oturum anahtarı çıkmamalı.
TUM_TABLOLAR = [
    "hasta", "cycle", "specimen", "olay", "goruntu", "specimen_bulgu",
    "sperm_ornek", "sperm_analiz", "sperm_dondurma", "sperm_dondurma_dosya",
    "islem_yapan", "gebelik_sonucu",
    "beta_hcg", "dogan_bebek", "pgt_sonuc", "tasiyici", "konum", "konum_semasi",
    "liste_degeri", "degisiklik_log",
]

# Kullanıcı tablosundan yalnızca bunlar: `kullanici_id` kolonlarının kimi
# gösterdiği okunabilsin diye var, kimlik doğrulama verisi için değil.
KULLANICI_KOLONLARI = ["id", "ad_soyad", "kisa_kod", "rol", "kullanici_adi",
                       "aktif_mi", "olusturma_zamani"]


def tumu_sayfalari():
    """Bütün tabloların ham dökümü, tablo başına bir sayfa.

    Ham: kodlar etikete çevrilmiyor, kolon adları veritabanındaki adlar.
    Amaç okumak değil **aktarmak** — başka bir programa vermek ya da veriyi
    elde tutmak. Okunacak çıktı ay listesi ve cycle detayı.
    """
    sayfalar = []
    for tablo in TUM_TABLOLAR:
        kolonlar = [r["name"] for r in db.sorgu(f"PRAGMA table_info({tablo})")]
        if not kolonlar:
            continue                        # tablo bu veritabanında yok
        secim = ", ".join(f'"{k}"' for k in kolonlar)
        nerede = " WHERE lab_id = ?" if "lab_id" in kolonlar else ""
        p = (db.LAB_ID,) if nerede else ()
        satirlar = [[r[k] for k in kolonlar]
                    for r in db.sorgu(f"SELECT {secim} FROM {tablo}{nerede}", p)]
        sayfalar.append((tablo, kolonlar, satirlar))

    mevcut = {r["name"] for r in db.sorgu("PRAGMA table_info(kullanici)")}
    kolonlar = [k for k in KULLANICI_KOLONLARI if k in mevcut]
    if kolonlar:
        secim = ", ".join(f'"{k}"' for k in kolonlar)
        satirlar = [[r[k] for k in kolonlar] for r in db.sorgu(
            f"SELECT {secim} FROM kullanici WHERE lab_id = ?", (db.LAB_ID,))]
        sayfalar.append(("kullanici", kolonlar, satirlar))
    return sayfalar


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

    cycle_kosul = f"c.lab_id = ? {cs}"
    ornek_kosul = ("s.cycle_id IN (SELECT c.id FROM cycle c "
                   f"WHERE {cycle_kosul})")

    def _olay(tip, ek=""):
        return _tek(
            "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
            f"JOIN specimen s ON s.id = o.specimen_id WHERE {ornek_kosul} "
            f"AND o.tip = ? AND o.iptal_mi = 0 {ek}", (db.LAB_ID, tip))

    oosit = _tek(f"SELECT COUNT(*) n FROM specimen s WHERE {ornek_kosul}",
                 (db.LAB_ID,))
    mii = _olay("maturasyon_kontrolu", "AND o.mat_deger = 'mii'")
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
    gebelik = _tek(
        "SELECT COUNT(*) n FROM gebelik_sonucu g WHERE g.klinik_gebelik = 1 "
        f"AND g.cycle_id IN (SELECT c.id FROM cycle c WHERE {cycle_kosul})",
        (db.LAB_ID,)) if gebelik_var else 0

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
        "foto": _tek("SELECT COUNT(*) n FROM goruntu g WHERE g.cycle_id IN "
                     f"(SELECT c.id FROM cycle c WHERE {cycle_kosul})",
                     (db.LAB_ID,)),
        # Oranlar: payda sıfırsa None -- "%0" yazmak yanıltıcı olurdu.
        "oran_mii": _oran(mii, oosit),
        "oran_fert": _oran(ikipn, icsi),
        "oran_blast": _oran(blast, ikipn),
        "oran_gebelik": _oran(gebelik, transfer_cycle),
    }


def _oran(pay, payda):
    """Yüzde, bir ondalık. Payda sıfırsa None — "%0" yanıltıcı olurdu."""
    if not payda:
        return None
    return round(pay * 100.0 / payda, 1)


def istatistik_aylari(yil: int = 0, n: int = ISTATISTIK_AY) -> list:
    """Ay ay kırılım: sayılar **ve dört oran** (v6.123, kullanıcının isteği).

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
                "gebelik": i["gebelik"],
                "oran_mii": i["oran_mii"], "oran_fert": i["oran_fert"],
                "oran_blast": i["oran_blast"], "oran_gebelik": i["oran_gebelik"],
            })
    return satirlar


def son_kayitlar(n: int = 10) -> list:
    """En son girilen kayıtlar — hasta, cycle ve laboratuvar işlemleri.

    Kullanıcının "yapılan her kayıt ... anlık" isteğinin ikinci yarısı:
    sayıların yanında **ne olduğu** da görünsün. Üç tablodan okunup zamana
    göre birleştiriliyor; ayrı bir günlük tablosu tutulmuyor (bkz.
    `istatistikler`).

    Varsayılan **on satır**: bu bir kayıt defteri değil, "en son ne yapıldı"
    penceresi. Uzun tutulunca ekranın yarısını kaplıyor ve yanındaki ay
    kırılımını eziyordu. Tam döküm zaten `/disari/tumu`'da.
    """
    hasta = db.sorgu(
        "SELECT olusturma_zamani AS z, 'hasta' AS tur, dosya_no, ad_soyad, "
        "  NULL AS cycle_id, NULL AS cycle_no, NULL AS tip "
        "FROM hasta WHERE lab_id = ? ORDER BY olusturma_zamani DESC LIMIT ?",
        (db.LAB_ID, n))
    cycle = db.sorgu(
        "SELECT c.olusturma_zamani AS z, 'cycle' AS tur, h.dosya_no, h.ad_soyad, "
        "  c.id AS cycle_id, c.cycle_no, c.cycle_tipi AS tip "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
        "WHERE c.lab_id = ? ORDER BY c.olusturma_zamani DESC LIMIT ?",
        (db.LAB_ID, n))
    olay = db.sorgu(
        "SELECT o.olusturma_zamani AS z, 'olay' AS tur, h.dosya_no, h.ad_soyad, "
        "  c.id AS cycle_id, c.cycle_no, o.tip "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE o.lab_id = ? AND o.iptal_mi = 0 "
        "ORDER BY o.olusturma_zamani DESC LIMIT ?", (db.LAB_ID, n))

    hepsi = [dict(r) for r in list(hasta) + list(cycle) + list(olay)]
    hepsi.sort(key=lambda r: r["z"] or "", reverse=True)
    for r in hepsi:
        if r["tur"] == "cycle":
            r["ad"] = _tip(r["tip"]) or r["tip"]
        elif r["tur"] == "olay":
            r["ad"] = metinler.t("olay_" + r["tip"]) if r["tip"] else ""
        else:
            r["ad"] = ""
    return hepsi[:n]


ISTATISTIK_BASLIK = ["Ay", "Cycle", "Oosit", "MII", "ICSI yapılan", "2PN",
                     "Blastokist", "Transfer edilen cycle", "Klinik gebelik",
                     "M2 oranı (%)", "Fertilizasyon oranı (%)",
                     "Blastokist oranı (%)", "Klinik gebelik oranı (%)"]


def istatistik_sayfalari(yil: int = 0):
    """İstatistiklerin Excel hali: ay ay kırılım + genel toplam.

    `yil` ekrandan geliyor (v6.123) — düğmeye basıldığında bakılan yıl
    insin diye. Ekranda oranların yanında **payı ve paydası** da yazıyor;
    burada da öyle: yalnızca yüzdeyi vermek "%100" ile "1/1"i ayırt
    edilemez yapardı.
    """
    aylar = [[s["ay"], s["cycle"], s["oosit"], s["mii"], s["icsi"],
              s["ikipn"], s["blast"], s["transfer"], s["gebelik"],
              s["oran_mii"], s["oran_fert"], s["oran_blast"],
              s["oran_gebelik"]] for s in istatistik_aylari(yil)]
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
        ["Klinik gebelik", g["gebelik"]],
        ["Fotoğraf", g["foto"]],
        ["M2 oranı (%)", g["oran_mii"]],
        ["Fertilizasyon oranı (%)", g["oran_fert"]],
        ["Blastokist oranı (%)", g["oran_blast"]],
        ["Klinik gebelik oranı (%)", g["oran_gebelik"]],
    ]
    return [(f"{yil} aylara göre" if yil else "Aylara göre",
             ISTATISTIK_BASLIK, aylar),
            ("Genel", ["Ölçü", "Değer"], genel)]
