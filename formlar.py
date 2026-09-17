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

import db
import metinler

# ----------------------------------------------------------- ortak yardımcılar


def _sayi(r, anahtar):
    return r[anahtar] if r and r[anahtar] is not None else None


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


def gun_alt(alan, tip, gun):
    """Bir örneğin belirli gündeki değerlendirmesinden tek alan (alt sorgu).

    Dış sorguda örnek tablosu `s` diye adlandırılmış olmalı. `disari.py` de
    aynı parçaları kullanıyor — tek yerde dursun diye burada.
    """
    return (f"(SELECT x.{alan} FROM olay x WHERE x.specimen_id = s.id "
            f"AND x.tip = '{tip}' AND x.gun = {gun} AND x.iptal_mi = 0 "
            "ORDER BY x.id DESC LIMIT 1)")


def son_alt(alan, tip, sira="x.id DESC"):
    """Bir örneğin o tipteki son kaydından tek alan (alt sorgu)."""
    return (f"(SELECT x.{alan} FROM olay x WHERE x.specimen_id = s.id "
            f"AND x.tip = '{tip}' AND x.iptal_mi = 0 ORDER BY {sira} LIMIT 1)")


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
    """Bu cycle'ın örneklerinde o tipteki **ilk** olayın zamanı."""
    kosul = "AND o.gun = ?" if gun is not None else ""
    p = [cycle_id, tip] + ([gun] if gun is not None else [])
    r = db.tek(
        "SELECT MIN(o.zaman) z FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        f"WHERE s.cycle_id=? AND o.tip=? AND o.iptal_mi=0 {kosul}", p)
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


def _oosit_sayilari(cycle_id):
    """Maturasyon kodlarına göre oosit sayıları (mii / mi / gv / …)."""
    return {r["mat_deger"]: r["n"] for r in db.sorgu(
        "SELECT o.mat_deger, COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id = o.specimen_id "
        "WHERE s.cycle_id = ? AND o.tip = 'maturasyon_kontrolu' "
        "AND o.iptal_mi = 0 GROUP BY o.mat_deger", (cycle_id,))}


def _pn_sayilari(cycle_id):
    return {r["fert_pn_sayisi"]: r["n"] for r in db.sorgu(
        "SELECT o.fert_pn_sayisi, COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id = o.specimen_id "
        "WHERE s.cycle_id = ? AND o.tip = 'fertilizasyon_kontrolu' "
        "AND o.iptal_mi = 0 GROUP BY o.fert_pn_sayisi", (cycle_id,))}


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
        "  (SELECT cl.cl_hucre_sayisi FROM olay cl WHERE cl.specimen_id = s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        "   ORDER BY cl.gun DESC LIMIT 1) AS hucre, "
        "  (SELECT cl.cl_skor FROM olay cl WHERE cl.specimen_id = s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        "   ORDER BY cl.gun DESC LIMIT 1) AS cl_skor "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 "
        "  AND COALESCE(o.tr_cycle_id, s.cycle_id) = ? "
        "ORDER BY s.cycle_sira_no", (cycle_id,))


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

    islenen = db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.tip='icsi' AND o.iptal_mi=0", (cycle_id,))["n"]
    dejenere_sonrasi = db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.iptal_mi=0 AND "
        "((o.tip='icsi' AND o.icsi_sonuc='degenere') OR "
        " (o.tip='fertilizasyon_kontrolu' AND o.fert_sonuc='degenere'))",
        (cycle_id,))["n"]

    tr = _transfer_edilenler(cycle_id)
    donan = db.sorgu(
        "SELECT s.id, o.zaman, "
        "  (SELECT b.bl_genisleme FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS genisleme, s.durum "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0",
        (cycle_id,))
    cozulen = db.sorgu(
        "SELECT o.thaw_sagkalim FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "WHERE o.tip='thaw' AND o.iptal_mi=0 "
        "AND COALESCE(o.thaw_cycle_id, s.cycle_id)=?", (cycle_id,))

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
                    or (f"{r['hucre']} hücre" if r["hucre"] else None))
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
        "toplanan_oosit": db.tek(
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
        "transfer_asamasi": _asama_ozeti(tr, "bl_genisleme"),
        "transfer_tarihi": _gg_aa_yyyy(tr[0]["zaman"]) if tr else None,
        "transfer_sayisi": len(tr) or None,
        "transfer_klinisyen": None,              # programda tutulmuyor
        "transfer_embriyolog": _yapan(cycle_id, "transfer"),
        "embriyo1_asama": _emb(0, "asama"),
        "embriyo1_kalite": _emb(0, "kalite"),
        "embriyo2_asama": _emb(1, "asama"),
        "embriyo2_kalite": _emb(1, "kalite"),
        # --- kriyoprezervasyon ---
        "dondurulan_sayi": len(donan) or None,
        "dondurma_asamasi": _asama_ozeti(donan, "genisleme"),
        "cozdurulen_sayi": len(cozulen) or None,
        "cozdurme_viabilite": ", ".join(
            sorted({_et(h, "thaw_sagkalim", r["thaw_sagkalim"]) or ""
                    for r in cozulen} - {""})) or None,
        "notlar": c["protokol_notu"],
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
_OZET_NOTLAR = (70, 2)                      # NOTLAR kutusu (0'dan sayıyor)


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

    ornekler = db.sorgu(
        f"""
        SELECT s.id, s.cycle_sira_no, s.taraf,
               {son_alt('mat_deger', 'maturasyon_kontrolu')} AS mat,
               {son_alt('fert_pn_sayisi', 'fertilizasyon_kontrolu')} AS pn,
               {son_alt('fert_sonuc', 'fertilizasyon_kontrolu')} AS fert,
               {gun_alt('cl_hucre_sayisi', 'cleavage_degerlendirme', 2)} AS g2_hucre,
               {gun_alt('cl_skor', 'cleavage_degerlendirme', 2)} AS g2_skor,
               {gun_alt('cl_hucre_sayisi', 'cleavage_degerlendirme', 3)} AS g3_hucre,
               {gun_alt('cl_skor', 'cleavage_degerlendirme', 3)} AS g3_skor,
               {son_alt('bl_skor', 'blastokist_degerlendirme', 'x.gun DESC')} AS bl,
               {son_alt('zaman', 'transfer')} AS tr_zaman,
               {son_alt('zaman', 'vitrifikasyon')} AS vit_zaman
          FROM specimen s WHERE s.cycle_id = ? ORDER BY s.cycle_sira_no
        """, (cycle_id,))

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
            "yorum": o["bl"] or _et(h, "fert_sonuc", o["fert"]) or "",
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

    donan = db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id WHERE s.cycle_id=? "
        "AND o.tip='vitrifikasyon' AND o.iptal_mi=0", (cycle_id,))["n"]
    cozulen = db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id WHERE o.tip='thaw' "
        "AND o.iptal_mi=0 AND COALESCE(o.thaw_cycle_id, s.cycle_id)=?",
        (cycle_id,))["n"]
    transfer = len(_transfer_edilenler(cycle_id))
    # Kâğıttaki FERTİLİZASYON bloğunun "Dej" sütunu: işlemden **sonra**
    # dejenere olan oosit (ICSI sırasında ya da fert kontrolünde görülen).
    dej_islem = db.tek(
        "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.iptal_mi=0 AND "
        "((o.tip='icsi' AND o.icsi_sonuc='degenere') OR "
        " (o.tip='fertilizasyon_kontrolu' AND o.fert_sonuc='degenere'))",
        (cycle_id,))["n"]

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
        "freeze": donan or None,
        "thaw": cozulen or None,
        "transfer": transfer or None,
    }


# Özet bloğunun kutuları: (satır, sütun, anahtar). Kâğıt aslındaki yerler.
_ARTLAB_OZET = [
    (28, 0, "bazal_kons"), (28, 2, "son_kons"),          # M/ml
    (28, 5, "oosit_mii"), (29, 5, "oosit_mi"), (30, 5, "oosit_gv"),
    (31, 5, "oosit_dej"),                                 # Mll / Ml / Pl / Dej
    (28, 6, "oosit_dej_islem"),                           # Dej (fertilizasyon)
    (28, 8, "pn0"), (28, 9, "pn1"), (28, 10, "pn2"), (28, 11, "pn3"),
    (28, 12, "freeze"), (28, 14, "thaw"), (28, 16, "transfer"),
]

# "% Motil" ve "% Normal" kutularında kâğıtta zaten yazı var; sayı onun
# arkasına yazılıyor -- kalemle de öyle yapılıyor.
_ARTLAB_OZET_EK = [
    (29, 0, "bazal_motil"), (30, 0, "bazal_normal"),
    (29, 2, "son_motil"), (30, 2, "son_normal"),
]

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
    """
    sutunlar = v["sutunlar"]
    sayfa_sayisi = max(1, -(-len(sutunlar) // ARTLAB_SUTUN))
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
    ("fertilizasyon_yontemi", "Tedavi tipi (IVF/ICSI, FET, oosit cryo)"),
    ("onceki_tedavi", "Önceki tedavi sayısı"),
    ("notlar", "Cycle'ın protokol notu"),
    ("bugun", "Formun basıldığı tarih"),
    ("laboratuvar", "Laboratuvarın adı"),
    ("— OPU ve oosit —", None),
    ("opu_tarihi", "OPU tarihi"),
    ("toplanan_oosit", "Toplanan oosit sayısı"),
    ("matur_mii", "MII (matür) sayısı"),
    ("immatur", "MI + GV sayısı"),
    ("dejenere", "Dejenere oosit sayısı"),
    ("atretik", "Atretik oosit sayısı"),
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
    ("islenen_oosit", "İşleme alınan oosit sayısı"),
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
ALAN_ADLARI = [a for a, aciklama in ALAN_ACIKLAMA if aciklama]


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
    return v
