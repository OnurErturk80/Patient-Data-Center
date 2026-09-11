"""Resmî formların verisi ve yerleşimi.

Kullanıcının tutmak **zorunda** olduğu iki form var (Akdeniz Üniversitesi
Tıp Fakültesi, Üreme Endokrinolojisi ve YÜT Merkezi):

  - **Embriyoloji Özet Formu** — DH.FR.91, Rev.03, cycle başına bir sayfa
  - **ART Lab. Raporu** — DH.FR.107, Rev.01, cycle başına bir sayfa (yatay)

İkisi de iki biçimde çıkıyor: tarayıcıdan yazdırılabilir sayfa (şablonlar
`form_ozet.html` / `form_artlab.html`) ve `.xlsx` (buradaki `*_yerlesimi`
fonksiyonları). İçerik tek yerden — `*_verisi()` — geliyor ki iki çıktı
birbirinden ayrı düşmesin.

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
        "opu_tarihi": (c["opu_zamani"] or "")[:10] or None,
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
        "transfer_tarihi": (tr[0]["zaman"] or "")[:10] if tr else None,
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


# --------------------------------------- embriyoloji özet formu: yerleşim

# Formun künyesi — kâğıt aslından birebir. Değiştirme.
OZET_KUNYE = {
    "kurum": ["AKDENİZ ÜNİVERSİTESİ TIP FAKÜLTESİ",
              "KADIN HASTALIKLARI VE DOĞUM ANABİLİM DALI",
              "ÜREME ENDOKRİNOLOJİSİ VE YARDIMCI ÜREME TEKNİKLERİ MERKEZİ"],
    "ad": "EMBRİYOLOJİ ÖZET FORMU",
    "serit": ["Doküman Kodu:DH.FR.91", "Yayın Tarihi:27.03.2007",
              "Revizyon Tarihi:24.04.2019", "Revizyon No:03",
              "Sayfa No Sayısı:1/1"],
    "dipnot": "Form - 70 01 26 02 03",
    "rev": "Rev.No: 03",
}

# Formun gövdesi: (satır, sol etiket, sol anahtar, sağ etiket, sağ anahtar).
# Satır numaraları kâğıt aslındaki satırlar — kutuların yeri birebir aynı
# olsun diye korunuyor. Sağ tarafı olmayan satırda sağ etiket boş.
# "#" ile başlayan satır bölüm başlığı.
OZET_GOVDE = [
    (8,  "KİMLİK NO", "kimlik_no", "EŞİNİN ADI", "esinin_adi"),
    (10, "DOSYA NO", "dosya_no", "YAŞI", "yasi"),
    (12, "SOYADI", "soyadi", "ÖNCEKİ TEDAVİ SAYISI", "onceki_tedavi"),
    (14, "ADI", "adi", "TEDAVİ PROTOKOLÜ", "tedavi_protokolu"),
    (16, "#OOSİT BİLGİLERİ", None, None, None),
    (18, "OPU TARİHİ", "opu_tarihi", "DEJENERE", "dejenere"),
    (20, "TOPLANAN OOSİT", "toplanan_oosit", "ATRETİK", "atretik"),
    (22, "MATÜR (MII)", "matur_mii", "MORFOLOJİK ANOMALİLİ", "morfolojik_anomalili"),
    (24, "İMMATÜR (MI+GV)", "immatur", "OPU KLİNİSYEN", "opu_klinisyen"),
    (26, "EMPTY ZONA", "empty_zona", "OPU EMBRİYOLOG", "opu_embriyolog"),
    (28, "#SPERM BİLGİLERİ", None, None, None),
    (30, "SPERM KAYNAĞI", "sperm_kaynagi", "HAZIRLAMA YÖNTEMİ", "hazirlama_yontemi"),
    (32, "BAZAL VOLÜM (ML)", "bazal_volum", "VOLÜM (ML)", "son_volum"),
    (34, "KONSANTRASYON (x106/ML)", "bazal_konsantrasyon",
         "KONSANTRASYON (x106/ML)", "son_konsantrasyon"),
    (36, "BAZAL MOTİLİTE (%)", "bazal_motilite", "MOTİLİTE (%)", "son_motilite"),
    (38, "BAZAL PROGRESSİF (%)", "bazal_progressif",
         "PROGRESSİF (%)", "son_progressif"),
    (40, "MORFOLOJİ (% NORMAL)", "morfoloji_normal",
         "HAZIRLAYAN EMBRİYOLOG", "hazirlayan_embriyolog"),
    (42, "LÖKOSİT (x106/ML)", "lokosit", None, None),
    (44, "#FERTİLİZASYON BİLGİLERİ", None, None, None),
    (46, "FERTİLİZASYON YÖNTEMİ", "fertilizasyon_yontemi", "INTAKT", "intakt"),
    (48, "İŞLEME ALINAN OOSİT SAYISI", "islenen_oosit",
         "İŞLEM SONRASI DEJENERE", "islem_sonrasi_dejenere"),
    (50, "NORMAL FERTİLİZASYON 2PN", "normal_2pn",
         "ANORMAL FERTİLİZASYON", "anormal_fertilizasyon"),
    (52, None, None, "EMBRİYOLOG", "fert_embriyolog"),
    (54, "#EMBRİYO TRANSFERİ BİLGİLERİ", None, None, None),
    (56, "EMBRİYO TRANSFER AŞAMASI", "transfer_asamasi",
         "EMBRİYO1 HÜCRE/AŞAMA", "embriyo1_asama"),
    (58, "TRANSFER TARİHİ", "transfer_tarihi", "EMBRİYO1 KALİTE", "embriyo1_kalite"),
    (60, "TRANSFER EMBRİYO SAYISI", "transfer_sayisi",
         "EMBRİYO2 HÜCRE/AŞAMA", "embriyo2_asama"),
    (62, "TRANSFER KLİNİSYEN", "transfer_klinisyen",
         "EMBRİYO2 KALİTE", "embriyo2_kalite"),
    (64, "TRANSFER EMBRİYOLOG", "transfer_embriyolog", None, None),
    (66, "#KRİYOPREZERVASYON BİLGİLERİ", None, None, None),
    (68, "DONDURULAN EMBRİYO SAYISI", "dondurulan_sayi",
         "ÇÖZDÜRÜLEN EMBRİYO SAYISI", "cozdurulen_sayi"),
    (70, "EMBRİYO DONDURMA AŞAMASI", "dondurma_asamasi",
         "ÇÖZDÜRME SONRASI VİABİLİTE", "cozdurme_viabilite"),
]


def _yaz(v):
    """Kutuya basılacak metin. None ve boş, boş kutu olarak çıkar."""
    return "" if v is None else str(v)


def ozet_yerlesimi(v: dict) -> dict:
    """Özet formunu `excel.kitap()`'ın yerleşim sayfası olarak kurar.

    Satır numaraları, sütun genişlikleri ve birleşik hücreler kâğıt aslından
    alındı; çıktı Excel'den basıldığında formun aslıyla aynı yere oturuyor.
    """
    hucreler, birlesik = {}, []

    for i, metin in enumerate(OZET_KUNYE["kurum"], start=1):
        hucreler[f"A{i}"] = (metin, "kurum")
        birlesik.append(f"A{i}:I{i}")
    hucreler["A5"] = (OZET_KUNYE["ad"], "formadi")
    birlesik.append("A5:I5")

    serit = OZET_KUNYE["serit"]
    for adres, aralik, metin in (("A6", "A6:B6", serit[0]),
                                 ("C6", "C6:D6", serit[1]),
                                 ("E6", "E6:F6", serit[2]),
                                 ("G6", None, serit[3]),
                                 ("H6", "H6:I6", serit[4])):
        hucreler[adres] = (metin, "kunye")
        if aralik:
            birlesik.append(aralik)

    for satir, sol, sol_k, sag, sag_k in OZET_GOVDE:
        if sol and sol.startswith("#"):
            hucreler[f"A{satir}"] = (sol[1:], "bolum")
            birlesik.append(f"A{satir}:I{satir}")
            continue
        # Etiket iki satır yüksekliğinde; aralarındaki ince satır kâğıtta
        # kutuları ayıran boşluk. Tek satırlık olanlar aslında da öyle.
        cift = satir not in (14, 26, 42, 52, 64, 70)
        if sol:
            hucreler[f"A{satir}"] = (sol, "etiket")
            birlesik.append(f"A{satir}:B{satir + 1}" if cift
                            else f"A{satir}:B{satir}")
            hucreler[f"C{satir}"] = (_yaz(v.get(sol_k)), "deger")
            birlesik.append(f"C{satir}:D{satir}")
        if sag:
            hucreler[f"F{satir}"] = (sag, "etiket")
            birlesik.append(f"F{satir}:G{satir + 1}" if cift
                            else f"F{satir}:G{satir}")
            hucreler[f"H{satir}"] = (_yaz(v.get(sag_k)), "deger")
            birlesik.append(f"H{satir}:I{satir}")

    hucreler["A72"] = ("NOTLAR", "etiket")
    birlesik.append("A72:B73")
    hucreler["C72"] = (_yaz(v.get("notlar")), "deger")
    birlesik.append("C72:I73")
    hucreler["A74"] = (OZET_KUNYE["dipnot"], "dipnot")
    hucreler["I74"] = (OZET_KUNYE["rev"], "dipnot")

    # Kâğıt aslındaki satır yükseklikleri: 16 punto kutu satırı, 5 punto
    # ayırıcı. Bunlar olmadan form A4'e oturmuyor.
    yukseklikler = {1: 22, 2: 15, 3: 16, 5: 18, 6: 13, 7: 15, 74: 12}
    for satir, sol, _, _, _ in OZET_GOVDE:
        yukseklikler[satir] = 16
        if sol and sol.startswith("#"):
            yukseklikler[satir + 1] = 10
        else:
            yukseklikler[satir + 1] = 5
    yukseklikler[72] = 17
    yukseklikler[73] = 17

    return {
        "ad": "Embriyoloji Özet",
        "hucreler": hucreler,
        "birlesik": birlesik,
        "genislikler": {1: 10, 2: 20, 3: 11, 4: 11, 5: 8,
                        6: 10, 7: 20, 8: 11, 9: 11},
        "yukseklikler": yukseklikler,
        "yazdirma": {"yon": "dikey", "sigdir": True, "kenar": 0.3},
    }


# ------------------------------------------------------------ ART lab raporu

ARTLAB_KUNYE = {
    "kurum": ["AKDENİZ ÜNİVERSİTESİ TIP FAKÜLTESİ",
              "KADIN HASTALIKLARI VE DOĞUM A.B.D.",
              "ÜREME ENDOKRİNOLOJİSİ VE YARDIMCI ÜREME TEKNİKLERİ MERKEZİ"],
    "ad": "ART LAB. RAPORU",
    "serit": ["Doküman Kodu:DH.FR.107", "Yayın Tarihi:16.01.2017",
              "Yayın Tarihi:14.09.2012", "Revizyon No:01",
              "Sayfa No Sayısı:1/1"],
    "dipnot": "Form - 70 01 26 02 39",
    "rev": "Rev.No: 01",
}

# Formdaki oosit ızgarası 13 sütunluk. Daha çok oosit varsa fazlası ikinci
# tabloya taşıyor (kâğıtta ikinci sayfa demek) -- kırpmak klinik bir sayıyı
# gizlerdi.
ARTLAB_SUTUN = 13

# Izgaranın satırları: (etiket, anahtar). Anahtarı None olan satır programda
# tutulmuyor, boş çıkıyor -- kalemle dolduruluyor.
ARTLAB_SATIRLAR = [
    ("Over (R / L)", "taraf"),
    ("Tüp (folikül)", None),             # programda tutulmuyor
    ("Nukleus durumu", "mat"),
    ("Fertilizasyon : PN", "pn"),
    ("Fertilizasyon sonucu", "fert"),
    ("Gün 2 : hücre", "g2_hucre"),
    ("             grade", "g2_skor"),
    ("Gün 3 : hücre", "g3_hucre"),
    ("             grade", "g3_skor"),
    ("Blastokist", "bl"),
    ("Transfer", "transfer"),
    ("Yorum", "yorum"),
]


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
            "yorum": "",
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
        "satirlar": ARTLAB_SATIRLAR,
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
        "oosit_mi_gv": (mat.get("mi") or 0) + (mat.get("gv") or 0) or None,
        "oosit_dej": mat.get("degenere"),
        "oosit_atretik": mat.get("atretik"),
        "pn0": pn.get("0"), "pn1": pn.get("1"), "pn2": pn.get("2"),
        "pn3": pn.get("3"), "pn4": pn.get("4+"),
        "freeze": donan or None,
        "thaw": cozulen or None,
        "transfer": transfer or None,
    }


def artlab_yerlesimi(v: dict) -> dict:
    """ART Lab. Raporu'nu `excel.kitap()`'ın yerleşim sayfası olarak kurar.

    Yatay basılıyor: 13 oositlik ızgara dikey A4'e sığmıyor. Yerleşim kâğıt
    aslının blok düzenini izliyor (kimlik → ızgara → özet → işlem saatleri →
    medium/lot), ama satır numaraları birebir değil: ızgaranın boyu oosit
    sayısına göre değişiyor, sabit satıra oturtmak fazlasını kırpardı.
    """
    hucreler, birlesik = {}, []
    sutun_sayisi = max(2, len(v["sutunlar"]) + 1)
    son = sutun_sayisi

    def _harf(n):
        ad = ""
        while n > 0:
            n, k = divmod(n - 1, 26)
            ad = chr(65 + k) + ad
        return ad

    satir = 1
    for metin in ARTLAB_KUNYE["kurum"]:
        hucreler[f"A{satir}"] = (metin, "kurum")
        birlesik.append(f"A{satir}:{_harf(son)}{satir}")
        satir += 1
    hucreler[f"A{satir}"] = (ARTLAB_KUNYE["ad"], "formadi")
    birlesik.append(f"A{satir}:{_harf(son)}{satir}")
    satir += 1
    for i, parca in enumerate(ARTLAB_KUNYE["serit"]):
        hucreler[f"{_harf(1 + i)}{satir}"] = (parca, "kunye")
    satir += 2

    def _blok(basliklar, degerler_listesi):
        """Etiket + değer satırlarından bir blok basar, sonraki satırı döndürür."""
        nonlocal satir
        for i, b in enumerate(basliklar, start=1):
            hucreler[f"{_harf(i)}{satir}"] = (b, "etiket")
        satir += 1
        for degerler in degerler_listesi:
            for i, d in enumerate(degerler, start=1):
                hucreler[f"{_harf(i)}{satir}"] = (_yaz(d), "ortali")
            satir += 1
        satir += 1

    # --- kimlik ---
    _blok(["Dosya No", "Adı", "Yaş", "Eşinin Adı", "İşlem", "Sperm",
           "Hekimler", "Laboratuvar"],
          [[v["dosya_no"], v["adi"], v["yasi"], v["esinin_adi"],
            v["islem"], v["sperm_kaynagi"], v["hekim"], v["laboratuvar"]]])

    # --- oosit ızgarası ---
    hucreler[f"A{satir}"] = ("OOSİT VE EMBRYO", "bolum")
    birlesik.append(f"A{satir}:{_harf(son)}{satir}")
    satir += 1
    hucreler[f"A{satir}"] = ("Oosit", "etiket")
    for i, s in enumerate(v["sutunlar"], start=2):
        hucreler[f"{_harf(i)}{satir}"] = (s["no"], "ortali_kalin")
    satir += 1
    for etiket, anahtar in ARTLAB_SATIRLAR:
        hucreler[f"A{satir}"] = (etiket, "etiket")
        for i, s in enumerate(v["sutunlar"], start=2):
            hucreler[f"{_harf(i)}{satir}"] = (
                _yaz(s[anahtar]) if anahtar else "", "ortali")
        satir += 1
    satir += 1

    # --- özet ---
    hucreler[f"A{satir}"] = ("ÖZET", "bolum")
    birlesik.append(f"A{satir}:{_harf(son)}{satir}")
    satir += 1
    _blok(["SEMEN", "M/ml", "% Motil", "% Normal"],
          [["Bazal", v["bazal_kons"], v["bazal_motil"], v["bazal_normal"]],
           ["İşlem", v["son_kons"], v["son_motil"], v["son_normal"]]])
    _blok(["OPU", "Toplam", "MII", "MI+GV", "Dejenere", "Atretik"],
          [["Oosit tipi", v["oosit_toplam"], v["oosit_mii"], v["oosit_mi_gv"],
            v["oosit_dej"], v["oosit_atretik"]]])
    _blok(["FERTİLİZASYON", "0PN", "1PN", "2PN", "3PN", "4+PN",
           "FREEZE", "THAW", "TRANSFER"],
          [["", v["pn0"], v["pn1"], v["pn2"], v["pn3"], v["pn4"],
            v["freeze"], v["thaw"], v["transfer"]]])

    # --- işlem saatleri (zaman çizelgesinden) ---
    hucreler[f"A{satir}"] = ("İŞLEM", "bolum")
    birlesik.append(f"A{satir}:{_harf(son)}{satir}")
    satir += 1
    _blok(["İşlem", "Tarih", "Önceki işlemden (sa)", "OPU'dan bu yana (sa)"],
          [[z["ad"], z["zaman"][:16], z["onceki_saat"], z["opu_saat"]]
           for z in v["cizelge"]] or [["", "", "", ""]])

    # --- programda tutulmayanlar: kalemle doldurulacak boş kutular ---
    _blok(["Medium / Lot", "IVF", "Sperm Prep", "PVP", "Hyalurinidase",
           "Freezing pack", "Thawing pack"], [["Lot", "", "", "", "", "", ""]])
    _blok(["Raporu dolduran", "Tarih", "Seleksiyon", "Yorum"],
          [["", "", "", ""]])

    hucreler[f"A{satir}"] = (ARTLAB_KUNYE["dipnot"], "dipnot")
    hucreler[f"{_harf(son)}{satir}"] = (ARTLAB_KUNYE["rev"], "dipnot")

    genislikler = {1: 22}
    for i in range(2, son + 1):
        genislikler[i] = 8
    return {
        "ad": "ART Lab Raporu",
        "hucreler": hucreler,
        "birlesik": birlesik,
        "genislikler": genislikler,
        "yazdirma": {"yon": "yatay", "sigdir": True, "kenar": 0.3},
    }
