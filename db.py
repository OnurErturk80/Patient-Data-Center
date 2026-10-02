"""Veritabanı bağlantısı ve yardımcı fonksiyonlar."""

import contextvars
import json
import logging
import os
import platform
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path

# ----------------------------------------------------------------- iki kök
#
# Program paketlenip kurulabilir hale gelecek (PyInstaller). O zaman kodun
# durduğu yer **salt okunur** olur: Mac'te `.app` paketinin içi, Windows'ta
# `Program Files`. Veri oraya yazılamaz; yazılsa bile program güncellenince
# üzerine yazılır ve **veri silinir**.
#
# Bu yüzden iki ayrı kök var ve karıştırılmamalı:
#
#   PROGRAM_KOK  kod, şablonlar, `static/`, `sema_guncel.sql`, göç betikleri
#   VERI_KOK     `lab.db`, `yerel_ayar.json`, `arsiv/`, `snapshot/`, yedek
#
# Veritabanının yerini **kendi başına kuran kod yazma** -- `db.DB_YOLU`
# kullan. Göç betikleri eskiden her biri kendi yolunu kuruyordu; veri
# taşınınca kod klasöründe bomboş yeni bir `lab.db` açarlar ve göç çalıştı
# sanılırdı (tuzak #8'in en pahalı hali).


def _program_kok() -> Path:
    """Kodun yeri. Paketlenmiş çalıştırmada PyInstaller'ın açtığı klasör."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).parent


def _veri_kok() -> Path:
    """Yazılabilir veri klasörü.

    Sıra bilerek böyle:

    1. `LAB_VERI` ortam değişkeni -- kurulum betiği ve testler bunu kullanıyor.
    2. **Kodun yanında `lab.db` varsa orası.** Bugünkü kurulumlar (kullanıcının
       Mac'i ve klinik mini PC'si) böyle çalışıyor; paketlemeye geçerken
       hiçbiri bozulmasın diye veri olduğu yerde bırakılıyor.
    3. Yoksa işletim sisteminin veri klasörü -- yeni (paketlenmiş) kurulumlar.
    """
    ozel = os.environ.get("LAB_VERI")
    if ozel:
        return Path(ozel).expanduser()

    yanindaki = _program_kok() / "lab.db"
    if yanindaki.exists():
        return _program_kok()

    if os.name == "nt":
        taban = Path(os.environ.get("PROGRAMDATA") or Path.home())
    elif sys.platform == "darwin":
        taban = Path.home() / "Library" / "Application Support"
    else:
        taban = Path(os.environ.get("XDG_DATA_HOME")
                     or Path.home() / ".local" / "share")
    return taban / "PatientDataCenter"


PROGRAM_KOK = _program_kok()
VERI_KOK = _veri_kok()


def paket_bilgisi():
    """Kurulum dosyasının derleme bilgisi (v6.204) ya da None.

    `paket/pdc.spec` pakete `paket_bilgisi.json` koyuyor: sürüm ve derlemenin
    kimliği ("v6.204 · abc1234 · 2026-09-27"). Git ile çalışan kurulumda dosya
    yok. Okuyan iki yer: Yönetici panelinin sürüm kartı ve `baslat.py` (Mac'te
    yenilenmiş uygulama eski derlemeyi bununla tanıyıp kapatıyor)."""
    try:
        bilgi = json.loads((PROGRAM_KOK / "paket_bilgisi.json")
                           .read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return bilgi if isinstance(bilgi, dict) else None
try:
    VERI_KOK.mkdir(parents=True, exist_ok=True)
except OSError:
    pass

DB_YOLU = VERI_KOK / "lab.db"
LAB_ID = 1          # v1 tek laboratuvar

# Bu tiplerde dondurulan örnek (embriyo ya da oosit) BAŞKA bir cycle'dan
# gelir, bu cycle'da OPU olmaz -- yumurta toplanmıyor. Tanım burada duruyor
# çünkü `app.py` de (`FET_TIPLERI`, `fet_tipi_mi()`) `disari.py` de
# (istatistikteki oosit sayımı) soruyor; `disari` `app`'i import edemez
# (app zaten disari'yi import ediyor), iki kopya er geç ayrı düşerdi.
# Yeni bir "örneği başka tedaviden gelen" tip eklersen buraya ekle.
FET_TIPLERI = ("fet", "fet_kultur", "yumurta_cozme")

# Yalnızca cleavage embriyosu çözen tipler (v6.156, kullanıcının isteği:
# "FET (3→5)'te sadece cleavage tüplerinin çözülmesine izin ver"). FET (3→5)
# gün 2/3 embriyosunu çözüp gün 5'e kadar kültürlüyor; blastokist tüpü bu
# tiple çözülemez. Tüpün evresi `app.tasiyici_icerigi()`'nin `blastokist`
# kolonunda. Yeni bir "yalnızca cleavage" tipi eklersen buraya ekle.
CLEAVAGE_COZEN_TIPLER = ("fet_kultur",)

# Tedavi tipine göre aşamalar, GÖSTERİM SIRASIYLA (v6.62). v6.147'den beri
# burada: `formlar.py` ve `disari.py` de soruyor ("bu tipte çözülen yumurtaya
# ICSI yapılıyor mu", `cozulen_yumurta_islenir()`) ve `app`'i import edemez --
# `FET_TIPLERI`'nin aynı gerekçesi. `app.TIP_ASAMALARI` bu sözlüğün kendisi.
TIP_ASAMALARI = {
    # Çözme YOK (v6.155, kullanıcının kararı): "ivf/icsi tedavisi içinde
    # çözme bölümü olmamalıydı ... bunu çöz dediğimizde FET tedavisi adı
    # altında yeni bir tedavi başlatması gerekiyor." Bu tedavide dondurulan
    # embriyonun çözülmesi AYRI bir tedavi (FET); burada çözülünce iki
    # tedavinin işleri tek tedavinin formlarına yazılıyordu.
    "ivf_icsi": ["opu", "androloji", "denudasyon", "icsi", "fert", "cleavage",
                 "blast", "vitrifikasyon", "transfer", "gebelik"],
    # FET'te oosit toplanmaz — embriyo baska bir cycle'dan gelir.
    # Vitrifikasyon (v6.143, kullanicinin istegi): cozulup transfer edilmeyen
    # embriyo AYNI tedavide yeniden dondurulabiliyor. Transferden SONRA:
    # dondurulan sey transferin fazlasi. Ekran FET'te bu tedavi icin cozulen
    # embriyolari listeliyor (vit_ekran), dondurma yeni bir kayit oluyor --
    # ilk dondurmanin uzerine yazmiyor (goc_046).
    "fet": ["thaw", "transfer", "vitrifikasyon", "gebelik"],
    # FET (3->5 kultur, v6.62, goc_031): gun 2/3 embriyosu cozulup gun 5'e
    # kadar kulturleniyor, sonra transfer ediliyor -- araya "blast" giriyor.
    # SIRA BURADA thaw'i blast'tan ONCE koyuyor; ivf_icsi'de tam tersi (blast
    # sonra dondurma). Ikisi de ayni ASAMA_SIRASI'ndan besleniyor ama
    # gosterim sirasi buradaki liste sirasindan geliyor (app.cycle_asamalari),
    # yoksa fet_kultur'da blast thaw'dan once cikardi.
    # Yeniden dondurma burada da transferden sonra (v6.143): gun 5'e
    # kulturlenip transfer edilmeyen blastokistin dondurulmasi.
    "fet_kultur": ["thaw", "blast", "transfer", "vitrifikasyon", "gebelik"],
    "oosit_cryo": ["opu", "denudasyon", "vitrifikasyon", "thaw"],
    # Yumurta Çözme (v6.102, goc_039): oosit_cryo'da dondurulmuş bir
    # yumurtanın AYRI bir tedavide çözülmesi. v6.102'de yalnızca çözmeydi;
    # v6.147'de kullanıcı kararını değiştirdi: "yumurta çözme tedavisinde
    # denüdasyon haricinde diğer bütün işlemler IVF/ICSI cycle tedavisi ile
    # aynı olmalıydı". Denüdasyon yok (yumurta dondurulmadan önce soyuldu),
    # OPU da yok (bu tedavide yumurta toplanmıyor -- `fet`'in gerekçesi).
    # Çözme başta: yumurta önce çözülüyor, ICSI ondan sonra.
    "yumurta_cozme": ["thaw", "androloji", "icsi", "fert", "cleavage",
                      "blast", "vitrifikasyon", "transfer", "gebelik"],
}


def cozulen_yumurta_islenir(cycle_tipi) -> bool:
    """Bu tipte ICSI ve sonrası ÇÖZÜLEN yumurtayla mı yapılıyor (v6.147).

    Bugün yalnızca Yumurta Çözme. Aşama ekranları çözülen örnekleri zaten
    `tedavi_ornekleri()` ile buluyor; bu soru resmî formların ve tedavinin
    Excel'inin yumurta ızgarası için: orada `fet`/`fet_kultur`'un çözülen
    embriyoları sütun olarak basılmıyor (yumurta ızgarası onların değil), bu
    tipin çözülen yumurtaları basılıyor -- ICSI'leri, döllenmeleri bu
    tedavide.
    """
    return (cycle_tipi in FET_TIPLERI
            and "icsi" in TIP_ASAMALARI.get(cycle_tipi, ()))


# Cleavage'da birleşme (v6.157, goc_048, kullanıcının cevabı: "BB birleşme
# başlangıcı demek. Birleşme olarak yazılsın ... embriyo kalitesi Birleşme G2
# gibi olabilsin"). Birleşmede hücre sayısı yok; kalitenin yazımında hücre
# sayısının yerinde bu söz duruyor. Resmî formlar hep Türkçe basıldığı için
# (kurum belgesi) sabit burada; `formlar.py` ve `disari.py` de soruyor.
BIRLESME = "Birleşme"

# `aktar_access.py`'nin nottan yazdığı dondurmaların `olay.notlar` başı
# (v6.159). O tüpler Access notunun kendi cümlesinde zaten yazılı; resmî
# formun NOTLAR kutusu onları ikinci kez yazmasın diye `formlar.py` soruyor.
KAYNAK_DONDURMA_NOTU = "Kaynak kayıttaki dondurma notundan aktarıldı"
# Cryo Haritası Excel'inden açılan program öncesi tedavinin protokol notu
# işareti (v6.179, `cryo_esle.py yeni_hasta`). Yalnızca dondurma bilgisi var;
# `/istatistik` bu tedavileri dışlıyor (disari.istatistikler).
CRYO_EXCEL_ISARETI = "[Cryo Excel kaydı]"


def cl_hucre_ifadesi(x: str = "x") -> str:
    """Cleavage değerlendirmesinin "hücre" yeri -- SQL ifadesi (v6.157):
    birleşmede `BIRLESME` sözü, yoksa hücre sayısı. `x`: olay tablosunun
    takma adı. Göç (goc_048) yoksa yalnızca hücre sayısı. Formların ızgarası,
    Excel ve kalite yazımı hücre sayısını buradan okuyor -- birleşme boş
    hücre gibi kaybolmasın."""
    if kolon_var("olay", "cl_birlesme"):
        return (f"(CASE WHEN {x}.cl_birlesme = 1 THEN '{BIRLESME}' "
                f"ELSE {x}.cl_hucre_sayisi END)")
    # Parantezli: `formlar._sutun()` parantezle başlayanı ifade sayıyor, önüne
    # "x." eklemiyor -- göçsüz veritabanında "x.x.cl_hucre_sayisi" olurdu.
    return f"({x}.cl_hucre_sayisi)"


def cleavage_yazimi(hucre, skor):
    """Cleavage kalitesinin laboratuvarın yazımıyla hali: "8HG2", "8H",
    "Birleşme G2", "Birleşme" (v6.157). `hucre`: `cl_hucre_ifadesi()`'nin
    değeri (sayı ya da `BIRLESME`). Değerlendirme yoksa None -- uydurulmuyor.
    Kalite yazan her yer (vitrifikasyon, resmî formlar) bunu çağırsın."""
    if hucre == BIRLESME:
        return f"{BIRLESME} {skor}" if skor else BIRLESME
    if hucre is None:
        return None
    return f"{hucre}H{skor}" if skor else f"{hucre}H"


def cozme_tedavisi_mi(cycle_tipi) -> bool:
    """Bu tipte bir tedavi için çözme yapılabilir mi -- tipin aşamalarında
    çözme var mı (v6.155). IVF/ICSI'de yok: çözme ayrı bir FET tedavisi."""
    return "thaw" in TIP_ASAMALARI.get(cycle_tipi, ())


def yumurta_mi(cycle_tipi, asama=None) -> bool:
    """Bu tedavide dondurulan/çözülen örnek yumurta mı, embriyo mu?

    Yumurta yalnızca `oosit_cryo`'da dondurulur — `ivf_icsi`'nin
    vitrifikasyon ekranı zaten enjekte edilmiş (embriyo olmuş) örnekleri
    listeliyor (`_ICSI_YAPILMADI` süzgeci). Yumurta donduran yeni bir cycle
    tipi eklersen burayı genişlet.

    **Yumurta Çözme'de cevap aşamaya bağlı** (v6.147): çözülen şey yumurta
    (`asama='thaw'`), ama ICSI'den sonra dondurulan ya da transfer edilen şey
    embriyo. Aşama verilmezse (taşıyıcının içeriği, resmî formdaki dondurma
    notu) soru "bu tedavide dondurulan ne" -- Yumurta Çözme'de embriyo.

    `FET_TIPLERI` ile aynı gerekçeyle burada (v6.135): `app.py` ekranda
    (`ornek_adi()`, `icerik_sayisi()`, v6.133) soruyor, `formlar.py` da
    resmî formda soruyor ("2 embriyo" mu "12 yumurta" mı donduruldu) ve
    `app`'i import edemez — app zaten formlar'ı import ediyor.

    **Bir tüpün içeriği için bu değil, `dondurulan_yumurta_sql()`** (v6.167):
    Access'ten aktarılan IVF/ICSI tedavisinde ICSI'ye alınmayan yumurta da
    dondurulmuş olabiliyor, tipe bakan cevap onlara "embriyo" derdi.
    """
    if cycle_tipi == "oosit_cryo":
        return True
    return asama == "thaw" and cozulen_yumurta_islenir(cycle_tipi)


# Döllenmenin izi (v6.167): bu olaylardan biri dondurmadan önce yazılmışsa
# dondurulan şey embriyodur. `dondurulan_yumurta_sql()`'e bak.
_EMBRIYO_IZI = ("icsi", "fertilizasyon_kontrolu", "cleavage_degerlendirme",
                "blastokist_degerlendirme")


def dondurulan_yumurta_sql(o: str = "o") -> str:
    """Bir dondurma olayının dondurduğu örnek yumurta mı -- SQL ifadesi, 1/0
    (v6.167). `o`: vitrifikasyon olayının sorgudaki takma adı.

    **Tipten değil içerikten**: dondurmadan önce enjekte edilmemiş,
    döllenmemiş ve değerlendirilmemiş örnek yumurtadır. `yumurta_mi(tip)`
    programın kendi akışı için doğru (IVF/ICSI'nin vitrifikasyon ekranı
    yalnızca enjekte edilmiş embriyoyu donduruyor), ama Access'ten aktarılan
    kayıtlarda iki karışık durum var: IVF/ICSI'de ICSI'ye alınmayan MII'ler
    dondurulmuş ("16 ADET OOSİT ... (4*M2)"), Yumurta Dondurma'da birkaç
    yumurtaya ICSI yapılıp blastokisti dondurulmuş. Tipe bakan ölçü ilk tüpe
    "4 embriyo", ikincisine "yumurta" diyordu ve yumurta tüpüne FET
    öneriyordu. Tüpün içindekini söyleyen her yer bunu sorar: Cryo Haritası,
    taşıyıcı sayfası, çözme ekranları ve tüpün hangi tiple çözüleceği
    (`app.icerik_sql()`), resmî formların dondurma satırları, aktarımın tüp
    eşleştirmesi.

    - Dondurmadan SONRAKİ olaya bakılmıyor: Yumurta Dondurma'da dondurulan
      yumurta sonra Yumurta Çözme'de enjekte edilince ilk tüpü yine yumurta.
    - FET ve FET (3→5)'in dondurduğu hep embriyo (çözülen embriyonun yeniden
      dondurulması): aktarılmış FET'in embriyolarının ICSI'si programda yok.
    - Alt sorguların takma adları (`dy_c`, `dy_o`) çağıranınkilerle
      çakışmasın diye özel.
    """
    embriyo_cozen = ", ".join(f"'{t}'" for t in FET_TIPLERI
                              if not cozulen_yumurta_islenir(t)) or "''"
    izler = ", ".join(f"'{t}'" for t in _EMBRIYO_IZI)
    return (f"(CASE WHEN (SELECT dy_c.cycle_tipi FROM cycle dy_c "
            f"WHERE dy_c.id = {vit_tedavisi(o)}) IN ({embriyo_cozen}) THEN 0 "
            f"WHEN EXISTS (SELECT 1 FROM olay dy_o "
            f"WHERE dy_o.specimen_id = {o}.specimen_id AND dy_o.iptal_mi = 0 "
            f"AND dy_o.tip IN ({izler}) AND dy_o.zaman <= {o}.zaman) THEN 0 "
            f"ELSE 1 END)")


def embriyo_izi_sql(s: str = "s") -> str:
    """Örnek embriyo mu -- SQL koşulu (v6.185): enjekte edilmiş, döllenmiş ya
    da cleavage/blastokist değerlendirmesi var (`_EMBRIYO_IZI`). `s`: örnek
    tablosunun takma adı. Dondurma anına bağlı soru için
    `dondurulan_yumurta_sql()`; bu, örneğin bugünkü hali (vitrifikasyon
    ekranının adayları, `app.ornek_kareleri_sql()`)."""
    izler = ", ".join(f"'{t}'" for t in _EMBRIYO_IZI)
    return (f"EXISTS (SELECT 1 FROM olay ez_o WHERE ez_o.specimen_id = {s}.id "
            f"AND ez_o.iptal_mi = 0 AND ez_o.tip IN ({izler}))")

# Kilitli veritabanında ne kadar beklenecek. Klinikte birkaç telefon aynı anda
# kayıt girer; varsayılan 5 sn kısa kalabiliyor.
BEKLEME_SN = 15


def _wal_ac():
    """Süreç başına bir kez: WAL journal modunu garanti eder.

    WAL'da okuyanlar yazana takılmaz — birkaç kişi aynı anda ekran yenilerken
    fark edilir. Ayar veritabanı dosyasında kalıcıdır, her açılışta yazılması
    gerekmez; yine de yeni bir kopyada (sifirdan_kur) unutulmasın diye burada.

    Ağ sürücüsünde WAL desteklenmez; SQLite sessizce eski moda düşer, hata
    vermez. Bu yüzden `lab.db` yerel diskte kalmalı (README v6.6).
    """
    if not DB_YOLU.exists():
        return
    try:
        b = sqlite3.connect(DB_YOLU, timeout=BEKLEME_SN)
        b.execute("PRAGMA journal_mode = WAL")
        b.close()
    except sqlite3.Error:
        pass                          # salt okunur disk vb. — çalışmaya devam et


def baglan(otomatik_islem: bool = True):
    """Yeni bir bağlantı açar. Her istek kendi bağlantısını kullanır.

    `otomatik_islem=False` verilirse Python kendi işlemini başlatmaz; açıkça
    `BEGIN IMMEDIATE` yazabilmek için gerekir (bkz. `yazma_islemi`).
    """
    b = sqlite3.connect(DB_YOLU, timeout=BEKLEME_SN,
                        isolation_level="" if otomatik_islem else None)
    b.row_factory = sqlite3.Row      # sonuçlara kolon adıyla eriş
    b.execute("PRAGMA foreign_keys = ON")
    return b


@contextmanager
def yazma_islemi():
    """Okuma + yazmayı tek atomik işlem yapar.

    "Sıradaki numarayı oku, bir artır, kaydet" gibi yerlerde şart: iki kullanıcı
    aynı anda aynı numarayı hesaplayıp UNIQUE hatası almasın diye. `BEGIN
    IMMEDIATE` yazma kilidini baştan alır, diğer yazar bekler.

    Dosya kopyalama gibi yavaş işleri buraya koyma — kilit boyunca herkes bekler.
    """
    b = baglan(otomatik_islem=False)
    try:
        b.execute("BEGIN IMMEDIATE")
        yield b
        b.execute("COMMIT")
    except BaseException:
        try:
            b.execute("ROLLBACK")
        except sqlite3.Error:
            pass
        raise
    finally:
        b.close()


_wal_ac()


# `ortak_baglanti()` bloğunun bağlantısı (v6.239). ContextVar: istek başına
# (FastAPI her isteği kendi bağlamında çalıştırıyor) ve iş parçacığı başına.
_ORTAK_BAGLANTI = contextvars.ContextVar("pdc_ortak_baglanti", default=None)


@contextmanager
def ortak_baglanti():
    """Bu blokta `sorgu()` ve `tek()` tek bağlantıyı paylaşır (v6.239).

    Her sorgu kendi bağlantısını açıyor (`baglan()`); bedeli sorgu başına
    ~0,6 ms, küçük bir sorgunun kendisinden yüz kat fazla (ölçüldü). Binlerce
    küçük sorgu atan salt okunur toplu işler (tüm veri dökümü,
    `disari.tumu_sayfalari()`) blokta çalışıyor. Yazma (`yaz()`,
    `yazma_islemi()`) etkilenmez, kendi bağlantısını açar. İç içe blok
    dıştakinin bağlantısını kullanır. Döner: bağlantı."""
    var = _ORTAK_BAGLANTI.get()
    if var is not None:
        yield var
        return
    b = baglan()
    jeton = _ORTAK_BAGLANTI.set(b)
    try:
        yield b
    finally:
        _ORTAK_BAGLANTI.reset(jeton)
        b.close()


def sorgu(sql, parametre=()):
    """Birden çok satır döndüren sorgu."""
    ortak = _ORTAK_BAGLANTI.get()
    if ortak is not None:
        return ortak.execute(sql, parametre).fetchall()
    with baglan() as b:
        return b.execute(sql, parametre).fetchall()


def tek(sql, parametre=()):
    """Tek satır döndüren sorgu. Bulunamazsa None."""
    ortak = _ORTAK_BAGLANTI.get()
    if ortak is not None:
        return ortak.execute(sql, parametre).fetchone()
    with baglan() as b:
        return b.execute(sql, parametre).fetchone()


def yaz(sql, parametre=()):
    """INSERT/UPDATE çalıştırır, eklenen kaydın id'sini döndürür."""
    with baglan() as b:
        imlec = b.execute(sql, parametre)
        b.commit()
        return imlec.lastrowid


def liste(liste_adi):
    """Bir seçim listesinin değerlerini döndürür."""
    return sorgu(
        "SELECT kod, etiket FROM liste_degeri "
        "WHERE lab_id = ? AND liste_adi = ? AND aktif_mi = 1 ORDER BY sira",
        (LAB_ID, liste_adi),
    )


# ------------------------------------- tedavinin genel bulguları (v6.200)

# ICSI ekranının "Genel bulgular" penceresindeki listeler, ekrandaki sırayla:
# yumurta bulguları (yumurta yumurta işaretlenenin aynı listesi) ve sperm
# sorunları (goc_055). Form da bu sırayla yazıyor.
GENEL_BULGU_LISTELERI = ("bulgu_icsi", "bulgu_sperm")


def tedavi_bulgulari(cycle_id, asama="icsi"):
    """Tedavinin genel bulguları (v6.200, goc_055): `(seçililer, elle)`.

    `seçililer` ekrandaki sırayla `{"liste", "kod", "etiket"}` -- önce
    listelerin sırası, listede `sira`. Listeden kaldırılmış (pasif) değer de
    etiketiyle geliyor, etiketi hiç yoksa koduyla (tuzak #6: kayıtlı değer
    sessizce kaybolmasın). `elle`: "Diğer" kutusuna yazılan metin ya da None.
    Göç çalışmamışsa ikisi de boş (tuzak #3)."""
    if not tablo_var("tedavi_bulgu"):
        return [], None
    secili, elle = [], None
    for r in sorgu(
            "SELECT tb.id, tb.liste_adi, tb.bulgu_kodu, tb.metin, "
            "       ld.etiket, ld.sira "
            "  FROM tedavi_bulgu tb LEFT JOIN liste_degeri ld "
            "    ON ld.lab_id = ? AND ld.liste_adi = tb.liste_adi "
            "   AND ld.kod = tb.bulgu_kodu "
            " WHERE tb.cycle_id = ? AND tb.asama = ? ORDER BY tb.id",
            (LAB_ID, cycle_id, asama)):
        if r["bulgu_kodu"]:
            secili.append(r)
        elif r["metin"]:
            elle = r["metin"]
    sira = {ad: i for i, ad in enumerate(GENEL_BULGU_LISTELERI)}
    secili.sort(key=lambda r: (sira.get(r["liste_adi"], len(sira)),
                               r["sira"] if r["sira"] is not None else 10**9,
                               r["id"]))
    return ([{"liste": r["liste_adi"], "kod": r["bulgu_kodu"],
              "etiket": r["etiket"] or r["bulgu_kodu"]} for r in secili], elle)


# ------------------------------------------------ bulaş hastalığı (v6.219)

# Tedavinin iki kolonu (goc_057), ekrandaki sırayla: kadın (hastanın kendisi,
# `hasta.ad_soyad`) ve erkek (eşi, `hasta.es_adi`). Kolonun adı
# `bulas_<kişi>`.
BULAS_KISILER = ("kadin", "erkek")
BULAS_LISTESI = "bulas_hastaligi"
BULAS_YOK = "yok"
BULAS_DIGER_EN_COK = 80


def bulas_oku(deger):
    """`cycle.bulas_kadin` / `bulas_erkek` -> `(durum, kodlar, diger)` (v6.219).

    Kolonun biçimi goc_057'de: boş = girilmedi (`durum` None), "yok", ya da
    virgülle `bulas_hastaligi` kodları ve varsa `|`'den sonra elle yazılan
    "Diğer" (`durum` "var"). Kolonu okuyan her yer bundan geçer, ikinci bir
    ayrıştırıcı yazma."""
    metin = deger.strip() if isinstance(deger, str) else ""
    if not metin:
        return None, [], None
    if metin == BULAS_YOK:
        return "yok", [], None
    kod_metni, _, diger = metin.partition("|")
    kodlar = [k for k in (x.strip() for x in kod_metni.split(",")) if k]
    diger = diger.strip() or None
    if not kodlar and not diger:
        return None, [], None
    return "var", kodlar, diger


def bulas_yaz(kodlar, diger, yok):
    """Formun seçimi -> kolonun değeri, `bulas_oku()`'nun tersi (v6.219).

    Hastalık seçildiyse ya da "Diğer" yazıldıysa "Yok" sayılmaz -- ikisi
    birden gelirse hastalık kazanır: bulaş hastalığı sessizce kaybolmasın.
    Hiçbiri yoksa None (girilmedi). Kodların listede olup olmadığına çağıran
    bakar (`app.bulas_formdan()`)."""
    temiz = []
    for k in kodlar:
        k = (k or "").strip()
        if k and k != BULAS_YOK and "," not in k and "|" not in k \
                and k not in temiz:
            temiz.append(k)
    diger = " ".join((diger or "").split())[:BULAS_DIGER_EN_COK] or None
    if temiz or diger:
        return ",".join(temiz) + (f"|{diger}" if diger else "")
    return BULAS_YOK if yok else None


def _bulas_listesi():
    """`bulas_hastaligi` listesinin bütün değerleri (pasif dahil), sırasıyla."""
    return sorgu("SELECT kod, etiket, aktif_mi FROM liste_degeri "
                 "WHERE lab_id = ? AND liste_adi = ? ORDER BY sira, id",
                 (LAB_ID, BULAS_LISTESI))


def bulas_etiketleri(kodlar, diger=None, liste=None):
    """Seçilen hastalıkların ekrandaki adları, listenin sırasıyla; "Diğer"
    en sonda. Listeden kaldırılmış (pasif) değer etiketiyle, listede hiç
    olmayan kod koduyla geliyor (tuzak #6: kayıtlı değer kaybolmasın).
    `liste`: `_bulas_listesi()` bir kez okunduysa (`bulas_isaretle()`)."""
    if liste is None:
        liste = _bulas_listesi() if kodlar else []
    sira = {r["kod"]: i for i, r in enumerate(liste)}
    etiket = {r["kod"]: r["etiket"] for r in liste}
    adlar = [etiket.get(k, k)
             for k in sorted(kodlar, key=lambda k: sira.get(k, len(sira)))]
    return adlar + ([diger] if diger else [])


def bulas_secenekleri(kayitli=()):
    """Tedavi formunun seçenekleri: listenin etkin değerleri + kayıtlı olup
    listeden kaldırılmış (pasif) ya da listede olmayan kodlar, kendi
    etiketleriyle (tuzak #6: seçici kayıtlı değeri sessizce düşürmesin)."""
    liste = _bulas_listesi()
    secenek = [{"kod": r["kod"], "etiket": r["etiket"]} for r in liste
               if r["aktif_mi"] or r["kod"] in kayitli]
    bilinen = {r["kod"] for r in liste}
    return secenek + [{"kod": k, "etiket": k} for k in kayitli if k not in bilinen]


def bulas_durumu(cycle_id):
    """Bir tedavinin bulaş kaydı, kişi başına (v6.219):
    `[{"kisi", "durum", "hastaliklar"}]` -- `durum` None (girilmedi), "yok"
    ya da "var". Göç çalışmamışsa boş liste (tuzak #3)."""
    if not kolon_var("cycle", "bulas_kadin"):
        return []
    c = tek("SELECT bulas_kadin, bulas_erkek FROM cycle WHERE id = ?",
            (cycle_id,))
    if not c:
        return []
    sonuc = []
    for kisi in BULAS_KISILER:
        durum, kodlar, diger = bulas_oku(c[f"bulas_{kisi}"])
        sonuc.append({"kisi": kisi, "durum": durum,
                      "hastaliklar": bulas_etiketleri(kodlar, diger)})
    return sonuc


def son_bulas(hasta_id, haric=None):
    """Hastanın kişi başına EN SON girilmiş bulaş kaydı (v6.219):
    `{kişi: (kolonun değeri, tedavinin lab no'su)}`, girilmemiş kişi yok.

    Tedavilerin sırası `hasta_cycle_no` (tarih sırası, v6.144); silme
    ekranından iptal edilen tedavi (bitiş sebebi yok) sayılmıyor. Yeni tedavi
    bununla açılıyor (form ve çözme ekranının "Yeni tedavi başlat"ı), hasta
    kartının bandı bunu gösteriyor. `haric`: sayılmayacak tedavi."""
    if not kolon_var("cycle", "bulas_kadin"):
        return {}
    sonuc = {}
    for r in sorgu(
            "SELECT id, cycle_no, bulas_kadin, bulas_erkek FROM cycle "
            " WHERE hasta_id = ? AND id <> ? "
            "   AND NOT (durum = 'iptal' AND bitis_sebebi IS NULL) "
            " ORDER BY COALESCE(hasta_cycle_no, 0) DESC, id DESC",
            (hasta_id, haric or 0)):
        for kisi in BULAS_KISILER:
            deger = r[f"bulas_{kisi}"]
            if kisi not in sonuc and bulas_oku(deger)[0] is not None:
                sonuc[kisi] = (deger, r["cycle_no"])
        if len(sonuc) == len(BULAS_KISILER):
            break
    return sonuc


def bulas_uyarilari(cycle_id=None, hasta_id=None):
    """Kimlik bandının uyarısı (v6.219): yalnızca hastalığı OLAN kişiler,
    `[{"kisi", "hastaliklar", "tedavi"}]`.

    `cycle_id`: o tedavinin kendi kaydı (tedavinin bütün ekranları, `tedavi`
    None). `hasta_id`: kişi başına en son girilen (`son_bulas()`; hasta
    kartı, yeni tedavi formu), `tedavi` kaydın geldiği tedavinin lab no'su.
    `base.html` her hasta ekranında çağırıyor: hata ekranı bozmasın, boş
    liste döner."""
    try:
        if cycle_id:
            return [{"kisi": b["kisi"], "hastaliklar": b["hastaliklar"],
                     "tedavi": None}
                    for b in bulas_durumu(int(cycle_id)) if b["durum"] == "var"]
        if hasta_id:
            sonuc = []
            for kisi, (deger, cycle_no) in son_bulas(int(hasta_id)).items():
                durum, kodlar, diger = bulas_oku(deger)
                if durum == "var":
                    sonuc.append({"kisi": kisi, "tedavi": cycle_no,
                                  "hastaliklar": bulas_etiketleri(kodlar, diger)})
            sira = {k: i for i, k in enumerate(BULAS_KISILER)}
            return sorted(sonuc, key=lambda s: sira[s["kisi"]])
    except (sqlite3.Error, ValueError, TypeError):
        logging.getLogger(__name__).exception("Bulaş uyarısı okunamadı")
    return []


def bulas_isaretle(satirlar):
    """Tedavi listesinin satırlarına (sözlük; `bulas_kadin` / `bulas_erkek`
    kolonlarıyla) `bulas` ekler: hastalığı OLAN kişiler, `bulas_uyarilari(
    cycle_id=)` biçiminde (v6.223, ana ekranın listelerinde adın yanındaki
    kırmızı nokta). O işlevin sorgusuz hali -- liste satır başına sorgu
    atmasın; ölçü yine tedavinin kendi kaydı, tedavi ekranının bandı neyi
    gösteriyorsa nokta onu söylüyor. Hastalık listesi yalnızca hastalıklı
    bir satır varsa, bir kez okunuyor. Kolonu olmayan satır (göç yok) boş
    liste alır; hata ana ekranı bozmasın, boş kalır."""
    liste = None
    for s in satirlar:
        s["bulas"] = []
        try:
            for kisi in BULAS_KISILER:
                durum, kodlar, diger = bulas_oku(s.get(f"bulas_{kisi}"))
                if durum != "var":
                    continue
                if liste is None:
                    liste = _bulas_listesi()
                s["bulas"].append({"kisi": kisi, "tedavi": None,
                                   "hastaliklar": bulas_etiketleri(
                                       kodlar, diger, liste)})
        except sqlite3.Error:
            logging.getLogger(__name__).exception("Bulaş işareti okunamadı")
            s["bulas"] = []
    return satirlar


# ------------------------------------------------------- PGT (v6.225)
#
# Kullanıcı: "Tedavinin başında PGT yapılacağına dair laboratuvarda formunun
# üstüne yazıyorum. Tedavi bitene kadar üstünde PGT yapılacağı yazıyor. Bu
# hastanın oluşursa embriyolarından biyopsi yapıyorum ve parçaları genetiğe
# gönderiyorum. Embriyoları numaralandırıp dondurup saklıyorum." Şema
# goc_058'de; ayrıntı README v6.225.
#
# Tedavinin işareti `cycle.pgt_testleri`: `pgt_testi` listesinin kodları
# virgülle, boş = PGT yok. Biyopsi bir olay (`olay.tip='biyopsi'`, şemanın
# ilk sürümünden beri hazırdı): `biy_tup_etiketi` genetiğe giden tüpün
# numarası, yani ekrandaki "PGT 1" (kullanıcının cevabı: biyopsi sırasıyla
# 1'den), `biy_tip` biyopsinin tipi, `biy_sonuc` kullanıcının kararı
# (v6.226). Biyopsinin yapıldığı tedavi `olay_tedavisi()`'nin kuralı:
# değerlendirmeler gibi, işlemden önceki son çözme (FET (3→5)'te çözülüp
# biyopsiye alınan embriyo o tedavinin).

PGT_TEST_LISTESI = "pgt_testi"
# Her testin sonuç listesi (`liste_degeri`, goc_058). PGT-A'nınki şemanın
# kendi `pgt_sonuc` listesi.
PGT_SONUC_LISTELERI = {"pgt_a": "pgt_sonuc", "pgt_m": "pgt_m_sonuc",
                       "pgt_sr": "pgt_sr_sonuc", "hla": "hla_sonuc"}
PGT_NOTU_EN_COK = 120
# Laboratuvar trofektoderm biyopsisi yapıyor (kullanıcının cevabı,
# 2026-09-29: "Blastokist (TE)"); ekranda seçici yok, kayıt tipini taşıyor.
BIYOPSI_TIPI = "te"
# Bir tedavide PGT numarası en çok (ekranın kutusu, sunucu da tutuyor).
PGT_NO_EN_COK = 99
# Genetik sonuçtan sonra embriyonun durumu (v6.226, `olay.biy_sonuc`): kararı
# KULLANICI işaretliyor (cevabı: "Ben işaretlerim") -- program sonuçtan karar
# çıkarmıyor. Boş = karar verilmedi (sonuç bekleniyor).
PGT_KARARLARI = ("sorunsuz", "sorunlu")
# Genetik raporu tedavinin belge eki (`goruntu.asama`, Doktor Notu gibi):
# örneğe bağlı değil, embriyoloji fotoğrafı değil. Tedavinin "arşivi"
# (örneğe bağlanmamış kareler) bunları saymamalı, temizlememeli.
PGT_RAPOR_ASAMASI = "pgt_rapor"
BELGE_ASAMALARI = ("doktor_notu", PGT_RAPOR_ASAMASI)


def pgt_acik() -> bool:
    """goc_058 çalıştırıldı mı (tedavi formunun PGT kartı, bant)."""
    return kolon_var("cycle", "pgt_testleri")


def pgt_oku(deger) -> list:
    """`cycle.pgt_testleri` -> test kodları. Kolonu okuyan her yer bundan
    geçer (`bulas_oku()`'nun kuralı)."""
    metin = deger.strip() if isinstance(deger, str) else ""
    return [k for k in (x.strip() for x in metin.split(",")) if k]


def pgt_yaz(kodlar):
    """Formun seçimi -> kolonun değeri, `pgt_oku()`'nun tersi; hiçbiri
    seçilmediyse None (PGT yok). Kodların listede olup olmadığına çağıran
    bakar (`app.pgt_formdan()`)."""
    temiz = []
    for k in kodlar:
        k = (k or "").strip()
        if k and "," not in k and k not in temiz:
            temiz.append(k)
    return ",".join(temiz) or None


def _pgt_test_listesi():
    """`pgt_testi` listesinin bütün değerleri (pasif dahil), sırasıyla."""
    return sorgu("SELECT kod, etiket, aktif_mi FROM liste_degeri "
                 "WHERE lab_id = ? AND liste_adi = ? ORDER BY sira, id",
                 (LAB_ID, PGT_TEST_LISTESI))


def pgt_etiketleri(kodlar, liste=None) -> list:
    """Testlerin ekrandaki adları, listenin sırasıyla. Listeden kaldırılmış
    değer etiketiyle, listede olmayan kod koduyla (tuzak #6)."""
    if liste is None:
        liste = _pgt_test_listesi() if kodlar else []
    sira = {r["kod"]: i for i, r in enumerate(liste)}
    etiket = {r["kod"]: r["etiket"] for r in liste}
    return [etiket.get(k, k)
            for k in sorted(kodlar, key=lambda k: sira.get(k, len(sira)))]


def pgt_secenekleri(kayitli=()) -> list:
    """Tedavi formunun seçenekleri: etkin testler + kayıtlı olup listeden
    kaldırılmış ya da listede olmayanlar (`bulas_secenekleri()`'nin kuralı)."""
    liste = _pgt_test_listesi()
    secenek = [{"kod": r["kod"], "etiket": r["etiket"]} for r in liste
               if r["aktif_mi"] or r["kod"] in kayitli]
    bilinen = {r["kod"] for r in liste}
    return secenek + [{"kod": k, "etiket": k} for k in kayitli if k not in bilinen]


def pgt_durumu(cycle_id):
    """Tedavinin PGT işareti: `{"kodlar", "testler", "not"}` ya da None (PGT
    yok ya da göç çalışmamış)."""
    if not pgt_acik():
        return None
    c = tek("SELECT pgt_testleri, pgt_notu FROM cycle WHERE id = ?", (cycle_id,))
    kodlar = pgt_oku(c["pgt_testleri"]) if c else []
    if not kodlar:
        return None
    return {"kodlar": kodlar, "testler": pgt_etiketleri(kodlar),
            "not": c["pgt_notu"]}


def tedavinin_biyopsileri(cycle_id, cycle_tipi=None, b=None) -> list:
    """Bu tedavide YAPILAN biyopsiler, PGT numarası sırasıyla:
    `[{"id", "specimen_id", "no", "zaman", "gun", "karar", ...}]`.

    Adaylar tedavinin aşama ekranlarının örnekleri (`tedavi_ornekleri()`:
    FET tiplerinde bu tedavi için çözülenler), karar `bu_tedavide()`: aynı
    embriyonun başka bir tedavideki biyopsisi (yeniden biyopsi) sayılmaz.
    `b`: açık bağlantı -- numarayı `yazma_islemi()` içinde okuyan biyopsi
    kaydı."""
    if cycle_tipi is None:
        c = tek("SELECT cycle_tipi FROM cycle WHERE id = ?", (cycle_id,))
        cycle_tipi = c["cycle_tipi"] if c else None
    sql = ("SELECT o.id, o.specimen_id, o.biy_tup_etiketi, o.biy_tip, o.biy_sonuc, "
           "  o.zaman, o.gun, o.notlar, o.cycle_id, s.cycle_sira_no "
           "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
           f"WHERE o.tip = 'biyopsi' AND o.iptal_mi = 0 AND {tedavi_ornekleri(cycle_tipi)} "
           f"AND {bu_tedavide(int(cycle_id), 'o')}")
    satirlar = (b.execute(sql, (cycle_id,)).fetchall() if b is not None
                else sorgu(sql, (cycle_id,)))
    sonuc = [_biyopsi_satiri(r) for r in satirlar]
    sonuc.sort(key=lambda b: (b["no"] is None, b["no"] or 0, b["zaman"] or ""))
    return sonuc


def _pgt_no(deger):
    """`biy_tup_etiketi` -> PGT numarası (tamsayı) ya da None."""
    metin = str(deger or "").strip()
    return int(metin) if metin.isdigit() else None


def _biyopsi_satiri(r) -> dict:
    d = dict(r)
    d["no"] = _pgt_no(d.get("biy_tup_etiketi"))
    # Yalnızca bilinen iki karar; kolondaki başka bir değer "karar yok".
    d["karar"] = d.get("biy_sonuc") if d.get("biy_sonuc") in PGT_KARARLARI else None
    d.setdefault("sonuc_metni", "")
    return d


def pgt_uyarisi(b) -> bool:
    """Biyopsili embriyo çözülür / transfer edilirken sorulmalı mı (v6.226):
    kararı "sorunsuz" değil -- sorunlu ya da sonuç (karar) henüz girilmemiş.
    Biyopsisi olmayan embriyo PGT'nin dışında, sorulmaz."""
    return bool(b) and b.get("karar") != "sorunsuz"


def _pgt_etiket_sozlugu() -> dict:
    """Test ve sonuç listelerinin etiketleri: `{(liste, kod): etiket}`."""
    listeler = (PGT_TEST_LISTESI, *PGT_SONUC_LISTELERI.values())
    return {(r["liste_adi"], r["kod"]): r["etiket"] for r in sorgu(
        "SELECT liste_adi, kod, etiket FROM liste_degeri WHERE lab_id = ? "
        f"AND liste_adi IN ({','.join('?' * len(listeler))})",
        (LAB_ID, *listeler))}


def pgt_sonuclari(biyopsi_idleri) -> dict:
    """Biyopsilerin genetik sonuçları (v6.226, `pgt_sonuc`, goc_058):
    `{biyopsi_id: {test_kodu: satır}}`. Göç yoksa boş."""
    idler = [i for i in dict.fromkeys(biyopsi_idleri or ()) if i]
    if not idler or not kolon_var("pgt_sonuc", "biyopsi_id"):
        return {}
    sonuc = {}
    for i in range(0, len(idler), 500):
        parca = idler[i:i + 500]
        for r in sorgu(f"SELECT * FROM pgt_sonuc WHERE biyopsi_id IN "
                       f"({','.join('?' * len(parca))}) ORDER BY id", parca):
            sonuc.setdefault(r["biyopsi_id"], {})[r["test_tipi"]] = dict(r)
    return sonuc


def pgt_sonuc_metni(satirlar, etiketler=None) -> str:
    """Bir biyopsinin sonuçları tek satır: "PGT-A: Mozaik %30 (+16) ·
    PGT-M: Taşıyıcı". Sonucu boş test yazılmaz. Etiket listeden (kodu değil
    etiketi göster); listede olmayan kod koduyla."""
    if not satirlar:
        return ""
    if etiketler is None:
        etiketler = _pgt_etiket_sozlugu()
    parcalar = []
    for test in sorted(satirlar, key=lambda k: list(PGT_SONUC_LISTELERI).index(k)
                       if k in PGT_SONUC_LISTELERI else 99):
        r = satirlar[test]
        if not r.get("sonuc") and not r.get("detay"):
            continue
        ad = etiketler.get((PGT_TEST_LISTESI, test), test)
        liste = PGT_SONUC_LISTELERI.get(test, "")
        metin = etiketler.get((liste, r.get("sonuc")), r.get("sonuc") or "")
        if r.get("mozaik_yuzde") is not None:
            y = r["mozaik_yuzde"]
            metin += f" %{int(y) if float(y).is_integer() else y}"
        if r.get("detay"):
            metin = f"{metin} ({r['detay']})" if metin else r["detay"]
        parcalar.append(f"{ad}: {metin}")
    return " · ".join(parcalar)


def biyopsi_bilgisi(specimen_idleri) -> dict:
    """Örneklerin EN SON biyopsisi (v6.225): `{specimen_id: {"id", "no",
    "karar", "tedavi", "zaman", "sonuc_metni"}}` -- biyopsisi olmayan örnek
    sözlükte yok. `sonuc_metni` genetik sonuçlar (v6.226, `pgt_sonuc_metni()`).

    Tüpün satırları (Cryo Haritası, taşıyıcı sayfası, çözme ve dondurma
    ekranları, hasta kartı) "bu embriyo PGT'nin kaçıncısı, sonucu ne"
    sorusunu buradan soruyor. Embriyo yeniden biyopsiye alındıysa (sonuç
    çıkmadı, başka bir tedavide çözüldü) sonuncusu geçerli; ölçü saat, sonra
    kimlik. `tedavi`: biyopsinin yapıldığı tedavi (`olay_tedavisi()`).
    Hata ekranı bozmasın: boş döner."""
    idler = [s for s in dict.fromkeys(specimen_idleri or ()) if s]
    if not idler:
        return {}
    sonuc = {}
    try:
        for i in range(0, len(idler), 500):
            parca = idler[i:i + 500]
            for r in sorgu(
                    "SELECT o.id, o.specimen_id, o.biy_tup_etiketi, o.biy_sonuc, "
                    f"  o.zaman, {olay_tedavisi('o')} AS tedavi "
                    "FROM olay o WHERE o.tip = 'biyopsi' AND o.iptal_mi = 0 "
                    f"AND o.specimen_id IN ({','.join('?' * len(parca))}) "
                    "ORDER BY o.zaman, o.id", parca):
                sonuc[r["specimen_id"]] = _biyopsi_satiri(r)
        sonuclar = pgt_sonuclari([b["id"] for b in sonuc.values()])
        etiketler = _pgt_etiket_sozlugu() if sonuclar else {}
        for b in sonuc.values():
            b["sonuc_metni"] = pgt_sonuc_metni(sonuclar.get(b["id"]), etiketler)
    except sqlite3.Error:
        logging.getLogger(__name__).exception("Biyopsi bilgisi okunamadı")
        return {}
    return sonuc


def tup_pgt(tasiyici_idleri) -> dict:
    """Tüplerdeki biyopsili embriyolar (v6.225'te `yerlesim.tup_ayrintilari()`
    içindeydi, v6.226'da çözme listesi de soruyor): `{tüp id: [biyopsi_bilgisi
    satırı, ...]}`, PGT numarası sırasıyla. Biyopsisi olmayan tüp sözlükte yok."""
    idler = [i for i in dict.fromkeys(tasiyici_idleri or ()) if i]
    ornekler = {}
    for i in range(0, len(idler), 500):
        parca = idler[i:i + 500]
        for r in sorgu("SELECT vit_tasiyici_id, specimen_id FROM olay "
                       "WHERE tip='vitrifikasyon' AND iptal_mi=0 AND vit_tasiyici_id "
                       f"IN ({','.join('?' * len(parca))})", parca):
            ornekler.setdefault(r["vit_tasiyici_id"], []).append(r["specimen_id"])
    biy = biyopsi_bilgisi([s for liste in ornekler.values() for s in liste])
    sonuc = {}
    for tid, liste in ornekler.items():
        satirlar = sorted((biy[s] for s in dict.fromkeys(liste) if s in biy),
                          key=lambda b: (b["no"] is None, b["no"] or 0))
        if satirlar:
            sonuc[tid] = satirlar
    return sonuc


def pgt_tup_sirasi(pgt) -> int:
    """Tüpün PGT durumunun sırası (v6.226, FET'in çözme listesi "sorunsuz"u
    öne alıyor): 0 biyopsili embriyolarının hepsi sorunsuz, 1 PGT yok, 2
    sonucu (kararı) beklenen var, 3 sorunlu var."""
    if not pgt:
        return 1
    kararlar = {b.get("karar") for b in pgt}
    if "sorunlu" in kararlar:
        return 3
    return 0 if kararlar == {"sorunsuz"} else 2


def pgt_nolar_yazisi(nolar) -> str:
    """PGT numaraları: "PGT 1–3, 5" (ardışık olanlar aralık). "PGT" iki
    dilde aynı; resmî formun NOTLAR'ı da bant da bunu basıyor."""
    nolar = sorted({int(n) for n in nolar if n is not None})
    if not nolar:
        return ""
    parcalar, bas = [], nolar[0]
    for onceki, n in zip(nolar, nolar[1:] + [None]):
        if n is not None and n == onceki + 1:
            continue
        parcalar.append(f"{bas}–{onceki}" if onceki != bas else str(bas))
        bas = n
    return "PGT " + ", ".join(parcalar)


def pgt_bandi(cycle_id):
    """Kimlik bandının altındaki PGT kutusu (v6.225, `_pgt_bandi.html`):
    tedavinin testleri, notu, bu tedavide yapılan biyopsiler. PGT'siz
    tedavide None. `base.html` her tedavi ekranında çağırıyor: hata ekranı
    bozmasın, None döner."""
    try:
        d = pgt_durumu(int(cycle_id))
        if not d:
            return None
        biyopsiler = tedavinin_biyopsileri(int(cycle_id))
        d["biyopsi"] = len(biyopsiler)
        d["nolar"] = pgt_nolar_yazisi(b["no"] for b in biyopsiler)
        # Kararlar (v6.226): "Sorunsuz: PGT 1, 3 · Sorunlu: PGT 2" -- bu
        # tedavinin her ekranında. Hiç karar yoksa boş (bant "biyopsi" der).
        d["kararlar"] = [] if all(b["karar"] is None for b in biyopsiler) else [
            (karar, yazi) for karar, yazi in (
                (k, pgt_nolar_yazisi(b["no"] for b in biyopsiler if b["karar"] == k))
                for k in (*PGT_KARARLARI, None)) if yazi]
        return d
    except (sqlite3.Error, ValueError, TypeError):
        logging.getLogger(__name__).exception("PGT bandı okunamadı")
        return None


def pgt_isaretle(satirlar):
    """Tedavi listesinin satırlarına (`pgt_testleri` kolonuyla) `pgt` ekler:
    testlerin adları, PGT'siz tedavide boş liste (v6.225, adın yanındaki
    "PGT" rozeti). `bulas_isaretle()` gibi sorgusuz: test listesi yalnızca
    PGT'li bir satır varsa, bir kez okunuyor."""
    liste = None
    for s in satirlar:
        kodlar = pgt_oku(s.get("pgt_testleri"))
        if not kodlar:
            s["pgt"] = []
            continue
        try:
            if liste is None:
                liste = _pgt_test_listesi()
            s["pgt"] = pgt_etiketleri(kodlar, liste)
        except sqlite3.Error:
            logging.getLogger(__name__).exception("PGT işareti okunamadı")
            s["pgt"] = []
    return satirlar


def klinik_gebelik_sql(g: str = "g") -> str:
    """Gebelik sonucunda klinik gebelik var mı -- SQL koşulu (v6.201).

    Gebelik ekranı `evet` / `hayir` / `bilinmiyor` yazıyor; ilk kayıtlarda
    (programın ilk tedavileri) `1` / `0` duruyor. `/istatistik`'in gebelik
    oranı v6.201'e kadar yalnızca `1`'i sayıyordu, yani ekrandan girilen
    klinik gebeliklerin hiçbirini görmüyordu. Klinik gebeliği soran her yer
    bunu kullanır: istatistik ve Sağlık Bakanlığı'nın aylık verileri
    (`disari.bakanlik_verileri()`). `g`: `gebelik_sonucu`'nun takma adı."""
    return f"{g}.klinik_gebelik IN ('evet', '1')"


# Gebelik testi (beta hCG, v6.241). Kullanıcının isteği: "Beta hCG değeri
# girince gebelik pozitif olarak kayıtlara geç." Cevapları (2026-10-02):
# ayrı bir bilgi -- klinik gebelik (kese) ayrı kalır, elle işaretlenir --
# ve eşik "10 ve üstü" (mIU/mL). Sonuç TÜRETİLMİŞ, saklanmıyor: beta
# değerlerinden her soruşta hesaplanıyor, beta silinince sonuç da değişiyor
# (istatistiklerin sayaç tutmama kuralı, v6.38). Eşiği değiştirmek klinik
# bir karar: kullanıcıya sormadan değiştirme.
BETA_POZITIF_ESIK = 10


def gebelik_testi(degerler):
    """Beta hCG değerlerinden gebelik testi (v6.241): `"pozitif"` (bir değer
    eşikte ya da üstünde), `"negatif"` (değer var, hepsi altında), None
    (değer girilmemiş). SQL hali `beta_pozitif_sql()` -- ikisi aynı kural."""
    sayilar = []
    for d in degerler:
        try:
            sayilar.append(float(d))
        except (TypeError, ValueError):
            continue
    if not sayilar:
        return None
    return "pozitif" if max(sayilar) >= BETA_POZITIF_ESIK else "negatif"


def beta_pozitif_sql(cycle: str = "c.id") -> str:
    """Tedavinin gebelik testi pozitif mi -- SQL koşulu, `gebelik_testi()`'nin
    "pozitif"i (v6.241). `cycle`: dış sorgudaki tedavi kimliği, koddan gelir."""
    return ("EXISTS (SELECT 1 FROM beta_hcg bh WHERE bh.cycle_id = "
            f"{cycle} AND bh.deger >= {BETA_POZITIF_ESIK})")


def tedavi_bulgu_metni(cycle_id, asama="icsi"):
    """Genel bulguların tek satırı: "Kalın zona, Sperm motilitesi kötü, ...".

    ICSI ekranındaki özet ve ART Lab formunun alttaki "Yorum:" satırı
    (`formlar.artlab_verisi()`) aynı metni basıyor. Bulgu yoksa None."""
    secili, elle = tedavi_bulgulari(cycle_id, asama)
    return ", ".join([s["etiket"] for s in secili] + ([elle] if elle else [])) \
        or None


# ------------------------------------------------- göç çalıştı mı (tuzak #3)

_KOLONLAR = {}



def konum_bul_veya_olustur(seviyeler, b=None):
    """Tank/kanister/goblet/pozisyon -> `konum.id`; yoksa açar.

    `seviyeler`: ['T2','K3','G5','12'] -- boş olanlar atlanır, hepsi boşsa
    None. Konumun kimliği `tam_yol` (" / " ile birleşik), `UNIQUE (lab_id,
    tam_yol)`: aynı yol ikinci kez açılmaz. Vitrifikasyon ve sperm dondurma
    ekranları (app.py) ile `cryo_esle.py` aynı kuralı kullanıyor -- v6.173'e
    kadar app.py'deydi.

    `b`: açık bir bağlantı (`yazma_islemi()` içinden çağrılırken); yoksa
    kendi bağlantısını açar.
    """
    temiz = [(s or "").strip() for s in seviyeler] + ["", "", "", ""]
    temiz = temiz[:4]
    if not any(temiz):
        return None
    tam_yol = " / ".join(x for x in temiz if x)
    sql_bul = "SELECT id FROM konum WHERE lab_id=? AND tam_yol=?"
    sql_ac = ("INSERT INTO konum (lab_id, seviye1, seviye2, seviye3, seviye4, "
              "tam_yol, durum) VALUES (?,?,?,?,?,?,'dolu')")
    par = (LAB_ID, temiz[0] or None, temiz[1] or None, temiz[2] or None,
           temiz[3] or None, tam_yol)
    if b is not None:
        mevcut = b.execute(sql_bul, (LAB_ID, tam_yol)).fetchone()
        if mevcut:
            return mevcut[0]
        return b.execute(sql_ac, par).lastrowid
    mevcut = tek(sql_bul, (LAB_ID, tam_yol))
    if mevcut:
        return mevcut["id"]
    return yaz(sql_ac, par)

def kolon_var(tablo: str, kolon: str) -> bool:
    """`tablo.kolon` var mı -- göçü çalışmamış makinede ekran 500 vermesin.

    Bir kez bakılıp saklanıyor. Göçler açılışta ilk istekten ÖNCE çalışıyor
    (v6.49), ilk bakış onlardan sonraya düşer -- bu yüzden modül yüklenirken
    ÇAĞIRMA, "yok" cevabı saklanırdı. Yedekten geri yüklemeden sonra
    `sema_bilgisini_unut()` bunu unutturuyor (v6.145). Tablo ve kolon adı her
    zaman koddan gelir, adresten değil (PRAGMA parametre almaz).
    """
    if (tablo, kolon) not in _KOLONLAR:
        _KOLONLAR[(tablo, kolon)] = any(
            r["name"] == kolon for r in sorgu(f"PRAGMA table_info({tablo})"))
    return _KOLONLAR[(tablo, kolon)]


def tablo_var(tablo: str) -> bool:
    """`tablo` var mı -- `kolon_var()`'ın tablo hali (v6.145).

    Aynı yerde saklanıyor, yani geri yüklemeden sonra onunla birlikte
    unutuluyor. `yetki` (goc_026) ve `sifre_istegi` (goc_030) soruluyor.
    """
    anahtar = (tablo, None)
    if anahtar not in _KOLONLAR:
        _KOLONLAR[anahtar] = tek(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            (tablo,)) is not None
    return _KOLONLAR[anahtar]


def sema_bilgisini_unut() -> None:
    """Saklanmış kolon ve tablo cevaplarını unutur (v6.145, tuzak #15).

    Çalışan programın altındaki veritabanı değiştiğinde çağrılıyor: yedekten
    geri yükleme eski bir sürümün veritabanını koyuyor, göçler onu
    güncelliyor, sonra buradaki "var/yok" cevaplarının hepsi yeniden
    soruluyor. Şema cevabı saklayan yeni bir yer açacaksan kendi değişkenini
    açma, `kolon_var()`/`tablo_var()`'ı kullan: geri yükleme yalnızca
    buradakini unutturuyor.
    """
    _KOLONLAR.clear()


def vit_tedavisi(o: str = "o") -> str:
    """Bir dondurma olayının YAPILDIĞI tedavi -- SQL ifadesi (v6.143, goc_046).

    `olay.cycle_id` her zaman örneğin KENDİ tedavisi (CLAUDE.md: "Embriyo
    cycle değiştirmez"). FET'te çözülüp yeniden dondurulan embriyonun ikinci
    dondurması ise o FET'te yapıldı; bu `vit_cycle_id`'de yazıyor. Boşsa
    kendi tedavisi -- `COALESCE(thaw_cycle_id, ...)` deseninin aynısı, bugüne
    kadarki bütün dondurmalar için doğru olan da bu.

    `formlar.py` (resmî formdaki dondurulan tüpler) ve `disari.py` (ay
    listesi) de soruyor ve `app`'i import edemiyor -- `FET_TIPLERI` ile aynı
    gerekçeyle burada. `o`: sorgudaki olay tablosunun takma adı. Göç
    çalışmamışsa eski ölçü: örneğin kendi tedavisi.
    """
    if kolon_var("olay", "vit_cycle_id"):
        return f"COALESCE({o}.vit_cycle_id, {o}.cycle_id)"
    return f"{o}.cycle_id"


def olay_tedavisi(o: str = "o") -> str:
    """Bir olayın YAPILDIĞI tedavi -- SQL ifadesi (v6.146).

    Kullanıcının isteği: "Zaman çizelgesini de işlemin yapıldığı tedaviye
    bağla." `olay.cycle_id` her zaman örneğin KENDİ tedavisi (CLAUDE.md:
    "Embriyo cycle değiştirmez"); "hangi tedavide yapıldı":
    - çözme `thaw_cycle_id`'de, transfer `tr_cycle_id`'de, dondurma
      `vit_cycle_id`'de (`vit_tedavisi()`) -- boşsa kendi tedavisi;
    - öteki işlemlerde (değerlendirmeler) alan yok: ölçü embriyonun o andaki
      tedavisi, yani işlemden ÖNCEKİ son çözme hangi tedavi içinse o. FET
      (3→5 kültür)'te çözülen embriyonun blastokist değerlendirmesi FET'in
      işi. Çözülmemişse kendi tedavisi. Ölçü saat: değerlendirme kaydı
      güncellenince yerinde kalıyor (kimliği eskiyebilir), saati güncelleniyor.

    `o`: sorgudaki olay tablosunun takma adı; alt sorgunun kendi takma adı
    `t`, dış sorguda `t` kullanma. Göç çalışmamışsa (goc_024) çözme bilinmiyor:
    her şey kendi tedavisi, eski davranış.
    """
    if not kolon_var("olay", "thaw_cycle_id"):
        return f"{o}.cycle_id"
    sonra = ("COALESCE((SELECT COALESCE(t.thaw_cycle_id, t.cycle_id) FROM olay t "
             f"WHERE t.specimen_id = {o}.specimen_id AND t.tip = 'thaw' "
             f"AND t.iptal_mi = 0 AND t.zaman <= {o}.zaman "
             f"ORDER BY t.zaman DESC, t.id DESC LIMIT 1), {o}.cycle_id)")
    return (f"CASE WHEN {o}.tip = 'thaw' THEN COALESCE({o}.thaw_cycle_id, {o}.cycle_id) "
            f"WHEN {o}.tip = 'transfer' THEN COALESCE({o}.tr_cycle_id, {o}.cycle_id) "
            f"WHEN {o}.tip = 'vitrifikasyon' THEN {vit_tedavisi(o)} "
            f"ELSE {sonra} END")


def tedavide_yapilan(cycle_id, o: str = "o") -> tuple:
    """Bu tedavide YAPILAN olaylar -- `(SQL koşulu, parametreler)` (v6.146).

    Adaylar tedavinin kendi örnekleri ile bu tedavi için çözülenler (bu
    tedavide yapılmış bir işlem ancak onlardan birinin olabilir), karar
    `olay_tedavisi()`. Zaman çizelgesi (`formlar._olay_ilk()`) ve tedavi
    ekranının özet kutusu (`app.cycle_ozet()`) soruyor -- ikisi aynı sayfada,
    biri öbürüyle çelişmesin diye koşul tek yerde. Kullanım:
    `kosul, p = db.tedavide_yapilan(cid)` → `... WHERE {kosul} ...`, `p` o
    sırada parametrelere eklenir.
    """
    return _tedavide_yapilan(o, "?", [cycle_id])


def tedavide_yapilan_ifade(tedavi: str, o: str = "o") -> str:
    """`tedavide_yapilan()`'ın bağıntılı alt sorgu hali (v6.147): tedavinin
    kimliği parametre değil, dış sorgudaki bir ifade (ay listesinde `c.id`).
    İfade her zaman koddan gelir."""
    return _tedavide_yapilan(o, tedavi, [])[0]


def tedavi_adayi(o: str, t: str) -> str:
    """Olayın örneği `t` tedavisinin bir örneği mi -- `tedavide_yapilan()`'ın
    aday süzgeci, SQL koşulu (v6.239'da ayrıldı): tedavinin kendi örnekleri ile
    bu tedavi için çözülenler. `t` koddan gelen bir ifade (`?` ya da bir kolon);
    göç çalışmamışsa yalnızca kendi örnekleri. Tüm veri dökümü
    (`disari.tedavi_sayilari()`) bütün tedavileri tek geçişte sayarken soruyor --
    kural tek yerde kalsın diye."""
    adaylar = f"{o}.specimen_id IN (SELECT id FROM specimen WHERE cycle_id = {t})"
    if kolon_var("olay", "thaw_cycle_id"):
        adaylar = (f"({adaylar} OR {o}.specimen_id IN (SELECT tc.specimen_id "
                   "FROM olay tc WHERE tc.tip = 'thaw' AND tc.iptal_mi = 0 "
                   f"AND tc.thaw_cycle_id = {t}))")
    return adaylar


def _tedavide_yapilan(o, t, p1) -> tuple:
    # `t` aday süzgecinde iki kez (göç yoksa bir kez), karşılaştırmada bir kez
    # geçiyor; `?` ise her biri için bir parametre.
    n = 3 if kolon_var("olay", "thaw_cycle_id") else 2
    return (f"{tedavi_adayi(o, t)} AND {olay_tedavisi(o)} = {t}",
            list(p1) * n)


def bu_tedavide(cycle_id: int, o: str = "o") -> str:
    """Bu olay BU tedavide mi yapıldı -- örneği zaten bilinen bir alt sorgu
    için kısa koşul (v6.147). `tedavide_yapilan()`'ın aday süzgeci olmadan:
    örnek dış sorgudan geliyor. Tedavinin kimliği tamsayıya çevrilip metne
    gömülüyor (rotadan `int` geliyor); böylece çok alt sorgulu bir SELECT'te
    parametre sırası karışmıyor."""
    return f"{olay_tedavisi(o)} = {int(cycle_id)}"


def bu_tedavinin_skoru(tedavi: str, o: str = "o") -> str:
    """WHERE parçası: değerlendirme bu tedavide yapılmış -- ya da örneğin bu
    tedavide hiç değerlendirmesi yok (v6.148).

    Bir tüpün ya da bir tedavinin dondurduğu örneğin skorunu soran yerler
    (vitrifikasyon ekranı, taşıyıcı sayfası, resmî formların dondurma
    satırı) "örneğin en son değerlendirmesi"ni alıyordu. Örnek sonra bir
    FET (3→5 kültür)'de çözülüp yeniden değerlendirilince kaynak tedavinin
    ekranı FET'in 5. gün skorunu basıyordu: 4. gün morula olarak dondurulan
    embriyo "3AC · gün 5" görünüyordu (aktarılan kayıtlarda dört örnekte).
    Sıralamayla çözülmüyor: tüpün tedavisinde yalnızca cleavage, FET'te
    blastokist kaydı varsa blastokist skorunu soran alt sorgu yine FET'inkini
    bulurdu. Kural bu yüzden iki tipi birlikte soruyor: bu tedavide herhangi
    bir değerlendirme varsa yalnızca onlar; hiç yoksa (düz FET'te yeniden
    dondurulan embriyonun FET'te skoru olmaz) hepsi, eski davranış.
    `tedavi`: SQL ifadesi -- tamsayı ya da dış sorgudaki bir kolon
    (`vit_tedavisi('o')` gibi), her zaman koddan gelir. İç alt sorgu `y`.
    """
    return (f"({olay_tedavisi(o)} = {tedavi} OR NOT EXISTS (SELECT 1 FROM olay y "
            f"WHERE y.specimen_id = {o}.specimen_id AND y.iptal_mi = 0 "
            "AND y.tip IN ('cleavage_degerlendirme', 'blastokist_degerlendirme') "
            f"AND {olay_tedavisi('y')} = {tedavi}))")


def tedavi_ornekleri(cycle_tipi, s: str = "s") -> str:
    """Bu tedavinin aşama ekranlarında görünen örnekler -- SQL koşulu, bir `?`
    (tedavinin kimliği).

    Kendi örneği olan tiplerde `s.cycle_id = ?`. `FET_TIPLERI`'nde örnek
    başka bir tedaviden geliyor (`specimen.cycle_id` hiç değişmez): bu
    tedavi için çözülenler, `thaw_cycle_id` ile. v6.62'de blastokist ekranı
    için yazılmıştı (`_blast_kosul`); v6.147'den beri Yumurta Çözme'nin ICSI,
    fertilizasyon ve cleavage ekranları da, resmî formların ve Excel'in
    yumurta ızgarası da (`cozulen_yumurta_islenir()`) buradan okuyor.
    """
    if cycle_tipi in FET_TIPLERI:
        return (f"{s}.id IN (SELECT tz.specimen_id FROM olay tz "
                "WHERE tz.tip = 'thaw' AND tz.iptal_mi = 0 AND tz.thaw_cycle_id = ?)")
    return f"{s}.cycle_id = ?"


def cozme_tupu_var() -> bool:
    """Çözme kaydı hangi tüpü boşalttığını biliyor mu (`olay.thaw_tasiyici_id`,
    goc_046). Bilmiyorsa bir örneğin tek dondurması, tek çözmesi var sayılır
    -- v6.143'ten önceki davranış."""
    return kolon_var("olay", "thaw_tasiyici_id")


def olay_sirasini_duzelt(b, ornekler=None) -> int:
    """Aktarılmış bir FET'in çözmesi, çözülen tüpün dondurmasından DAHA KÜÇÜK
    kimlikliyse o örneğin çözmeden sonraki olaylarını yeni kimlikle yeniden
    yazar (v6.175). Döner: düzeltilen örnek sayısı.

    Program "önce hangisi" sorusunu kimlik sırasıyla soruyor, saatle değil
    (saatler elle geri tarihlenebilir, v6.143): hasta kartının "yeniden
    dondurma" rozeti, resmî formun "Kalan dondurulmuş"u, geri alma engelleri.
    Access aylarını karışık sırayla aktarınca (2026 önce, 2025 sonra; 2019
    önce, 2018 sonra) FET'in çözmesi yazıldıktan SONRA tüpünün dondurması
    yazıldı, sonra `aktar_access._kaynaga_bagla()` ikisini aynı örneğe
    bağladı: çözme dondurmadan "önce" görünüyor. Kart 2018'in tüpünü "yeniden
    donduruldu" diye gösteriyordu, form çözülmüş tüpü tankta sayıyordu.

    Yalnızca aktarımın kendi kayıtları: çözme aktarılmış bir FET'in
    ([Access kaydı] işaretli) ve dondurma aktarımın notunu taşıyor, aynı tüp.
    Programdan girilmiş bir kayda dokunulmuyor -- orada kimlik sırası
    gerçekten giriş sırası. Taşınan olaylar örneğin çözmeden sonraki BÜTÜN
    olayları, saat sırasıyla (aralarındaki sıra korunuyor); olay kimliğine
    bağlı tablo yok, değişiklik geçmişinin olay satırları yeni kimliğe
    çevriliyor. `b` açık bağlantı; işlem çağıranın. İkinci çalıştırma hiçbir
    şey değiştirmez."""
    kolonlar = [r[1] for r in b.execute("PRAGMA table_info(olay)")]
    if "thaw_tasiyici_id" not in kolonlar or "thaw_cycle_id" not in kolonlar:
        return 0
    suz = ""
    par = [KAYNAK_DONDURMA_NOTU + "%"]
    if ornekler is not None:
        ornekler = list(ornekler)
        if not ornekler:
            return 0
        suz = f"AND z.specimen_id IN ({','.join('?' * len(ornekler))}) "
        par += ornekler
    bozuk = b.execute(
        "SELECT z.specimen_id, MIN(z.zaman) "
        "FROM olay z JOIN olay v ON v.specimen_id = z.specimen_id "
        "AND v.tip = 'vitrifikasyon' AND v.iptal_mi = 0 "
        "AND v.vit_tasiyici_id = z.thaw_tasiyici_id "
        "AND v.id > z.id AND v.zaman <= z.zaman AND v.notlar LIKE ? "
        "JOIN cycle f ON f.id = z.thaw_cycle_id "
        "WHERE z.tip = 'thaw' AND z.iptal_mi = 0 "
        "AND f.protokol_notu LIKE '%[Access kayd%' "
        f"{suz}GROUP BY z.specimen_id", par).fetchall()
    if not bozuk:
        return 0
    alanlar = [k for k in kolonlar if k != "id"]
    liste = ",".join(alanlar)
    log = b.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                    "AND name='degisiklik_log'").fetchone()
    for sid, t0 in bozuk:
        # Çözmeden önceki olaylar (tüpün dondurması dahil) yerinde kalıyor,
        # sonrakiler (aynı FET'teki yeniden dondurma da) saat sırasıyla.
        idler = [r[0] for r in b.execute(
            "SELECT id FROM olay WHERE specimen_id = ? AND zaman >= ? "
            "ORDER BY zaman, id", (sid, t0)).fetchall()]
        for eski in idler:
            yeni = b.execute(f"INSERT INTO olay ({liste}) SELECT {liste} FROM olay "
                             "WHERE id = ?", (eski,)).lastrowid
            b.execute("DELETE FROM olay WHERE id = ?", (eski,))
            if log:
                b.execute("UPDATE degisiklik_log SET kayit_id = ? WHERE "
                          "tablo_adi = 'olay' AND kayit_id = ?", (str(yeni), str(eski)))
    return len(bozuk)


def yeniden_dondurma_var() -> bool:
    """Çözülen embriyo yeniden dondurulabilir mi -- goc_046'nın iki kolonu da
    var mı. Biri yoksa FET'in vitrifikasyon ekranı göç uyarısı basar."""
    return kolon_var("olay", "vit_cycle_id") and cozme_tupu_var()


# ------------------------------------------ tanktan çıkan tüp (v6.182, v6.227)

# Tanktan çıkmış ama kaydı ve örnekleri duran tüpün durumları: başka merkeze
# taşındı (v6.182) ve imha edildi (v6.227). İkisi de geri alınabilen bir
# işaret -- tüp çözülemez, tedaviye bağlanamaz, dondurma kaydı geri alınamaz
# ya da başka tüpe taşınamaz (önce işaret kaldırılır). "Tankta mı" sorusu
# `durum = 'dolu'` (embriyo tüpü); sperm listesi kullanılmış tüpü de bilerek
# gösterdiği için orada `durum NOT IN TANKTAN_CIKAN_SQL`.
TANKTAN_CIKAN = ("gonderildi", "imha")
TANKTAN_CIKAN_SQL = "(" + ", ".join(f"'{d}'" for d in TANKTAN_CIKAN) + ")"


def imha_var() -> bool:
    """`goc_059` (v6.227) çalıştı mı: tüpün imha günü, sebebi, notu. Göç
    yoksa imha formu basılmıyor, ekranlar ve formlar eski haliyle (tuzak #3);
    cevap `kolon_var()`'da saklanıyor, geri yüklemeden sonra unutuluyor."""
    return kolon_var("tasiyici", "imha_zamani")


# ------------------------------------ Cryo Haritası'nda olmayan tüp (v6.233)

def tank_duzeni_var() -> bool:
    """Tank düzeni kurulmuş mu (goc_052 + `cryo_esle.py yerlesim`, v6.189): en
    az bir konum satırı düzenin gobleti. `yerlesim.duzen_var()` bunu soruyor.
    Cevap saklanmıyor, her çağrıda tek satırlık sorgu: geri yüklenen eski bir
    yedekte düzen olmayabilir (tuzak #15)."""
    if not kolon_var("konum", "sira"):
        return False
    return tek("SELECT 1 FROM konum WHERE lab_id=? AND sira IS NOT NULL LIMIT 1",
               (LAB_ID,)) is not None


def haritada_yok_sql(t: str = "t") -> str:
    """Cryo Haritası'nda olmayan tüp -- SQL koşulu; `t` taşıyıcının takma adı
    (koddan gelir).

    Kullanıcının isteği (2026-09-30): "Cryo harita için Excelde dondurma tüpü
    yoksa programda gösterme ... cryo haritada kaydı olmayanları hiç bir
    şekilde programda görünmesin." Laboratuvarın haritası tank düzeni
    (v6.189); tankta duran (dolu) embriyo / yumurta tüpünün yeri yoksa straw
    haritada değil. Access kayıtlarından açılıp haritadaki bir straw'la
    eşleşemeyen tüpler böyle (deneme kopyasında 514 tüp, hepsi aktarımın).
    Bu tüpler Cryo Haritası'nda, hasta kartında, çözme listelerinde, taşıma
    ekranında, Excel çıktılarında ve formların "Kalan dondurulmuş"unda yok;
    yalnızca dondurulduğu tedavinin vitrifikasyon ekranında ve tüpün kendi
    sayfasında "Cryo Haritası'nda yok" diye görünüyor -- kararı (tankta
    şurada, haritadaki straw'ı bu, taşındı, imha edildi) kullanıcı orada
    veriyor. Çözülemez.

    Kurallar:
    - Tank düzeni yoksa (düzeni kurulmamış bir laboratuvar) harita programın
      kendi kayıtları, koşul hiçbir tüpü tutmaz ("0").
    - Yalnızca embriyo / yumurta tüpü: sperm tüplerinin konumsuzları
      laboratuvarın Excel'inin "Sayfa1"inden (tankı yazılmamış), haritada
      duruyorlar.
    - Yeri yazılı ama düzende olmayan tüp (elle yazılmış bilinmeyen bir yer)
      haritada: "Haritada yeri belirsiz"de yazılan yeriyle görünüyor.
    - Tanktan çıkmış (çözülmüş, taşınmış, imha edilmiş) tüp bu koşulda değil:
      kaydı geçmiş, olduğu gibi görünüyor.
    Python hali `haritada_yok()`."""
    if not tank_duzeni_var():
        return "0"
    return (f"({t}.kategori = 'embriyo' AND {t}.durum = 'dolu' "
            f"AND {t}.konum_id IS NULL)")


def haritada_yok(t) -> bool:
    """`haritada_yok_sql()`'in Python hali: taşıyıcı satırı (kategori, durum,
    konum_id)."""
    return bool(t) and (t["kategori"] == "embriyo" and t["durum"] == "dolu"
                        and not t["konum_id"] and tank_duzeni_var())


# ------------------------------------------------- hastanın tedavi sırası

def _kolonlari(b, tablo: str) -> set:
    """Tablonun kolonları, VERİLEN bağlantıyla ve saklamadan.

    `kolon_var()` cevabı saklıyor; bir göçün içinden çağrılsaydı sonraki bir
    göçün ekleyeceği kolon için "yok" saklanırdı (goc_047 bu işlevleri
    kullanıyor). Tablo adı her zaman koddan gelir.
    """
    return {r[1] for r in b.execute(f"PRAGMA table_info({tablo})")}


def tedavi_tarihi(b, c: str = "c") -> str:
    """Bir tedavinin işlem günü -- SQL ifadesi (v6.144).

    Hastanın tedavileri bu sırayla numaralanıyor (`tedavileri_sirala()`).
    Yumurta toplanan tedavide OPU, yoksa hCG; FET'te çözme ya da transfer --
    `olay.cycle_id` örneğin KENDİ tedavisi, "hangi tedavide yapıldı"
    `thaw_cycle_id`/`tr_cycle_id`'de; hiçbiri girilmemişse planlanan tarih, o
    da yoksa kaydın açıldığı an (aktarılan eski kayıtlarda o an zaten
    tedavinin tarihine çekili, aktar_access). Yalnızca gün karşılaştırılıyor:
    saatler farklı biçimlerde yazılmış olabilir, aynı gün iki tedavi olmaz.
    `date()` okuyamadığı değeri NULL yapar, sıradaki alana düşülür.

    `b`: bağlantı (kolonlar ona sorulur), `c`: sorgudaki cycle takma adı.
    """
    parca = [f"date({c}.opu_zamani)", f"date({c}.hcg_zamani)"]
    bag = [f"o.{k} = {c}.id" for k in ("thaw_cycle_id", "tr_cycle_id")
           if k in _kolonlari(b, "olay")]
    if bag:
        parca.append("(SELECT date(MIN(o.zaman)) FROM olay o "
                     "WHERE o.iptal_mi = 0 AND (" + " OR ".join(bag) + "))")
    if "planlanan_tarih" in _kolonlari(b, "cycle"):
        parca.append(f"date({c}.planlanan_tarih)")
    parca.append(f"date({c}.olusturma_zamani)")
    return "COALESCE(" + ", ".join(parca) + ")"


def tedavi_gunu(cycle_id):
    """Bir tedavinin işlem günü ('YYYY-MM-DD'), `tedavi_tarihi()`'nin
    kuralıyla, tek tedavi için. Resmî formların YAŞI bu günden (v6.243): OPU'su
    olmayan tedavide (FET, Yumurta Çözme) çözme / transfer günü. Tedavi
    yoksa None."""
    with ortak_baglanti() as b:
        r = b.execute(f"SELECT {tedavi_tarihi(b, 'c')} FROM cycle c "
                      "WHERE c.id = ?", (cycle_id,)).fetchone()
    return r[0] if r else None


def tedavileri_sirala(b, hasta_id) -> list:
    """Hastanın tedavilerini işlem günlerine göre numaralar (v6.144, goc_047).

    Kullanıcının isteği (2026-09-23): "Bir daha aynı hastaya eski tedavi
    kaydı eklenirse tarih sırasına göre en eski tedavi 1. tedavi olarak
    eklensin. Bu daha sonra hep uygulansın." Numara eskiden açılışta
    "en yüksek + 1" veriliyordu; temmuzun Access kayıtları ağustostan SONRA
    aktarılınca temmuz tedavisi 2., ağustos 1. oldu.

    Programın verdiği numara bir önceki tedavininkinin bir fazlası (ilk
    tedavi 1). **Elle yazılan numara korunur** (`hasta_cycle_no_elle`:
    hasta başka merkezde de tedavi gördüyse gerçek deneme sayısı, README
    v0.8) -- bir önceki tedavinin numarasından büyük olduğu sürece; değilse
    tarih sırası kazanır ve numara bir öncekinin bir fazlası olur. Elle
    yazılan değer silinmiyor: çakışma kalkınca (önceki tedavinin tarihi
    düzeltildi, yanlış açılan tedavi silindi) numara ona döner.

    Tedavinin tarihini değiştiren her yazmadan sonra çağrılmalı. `b` yazma
    işleminin bağlantısı, commit çağıranın işi. Döner: değişenler,
    `[(cycle_id, cycle_no, eski, yeni), ...]`.

    goc_047 çalışmamışsa hiçbir şeye dokunmaz (tuzak #3): elle yazılan
    numarayı ayırt edemeden sıralamak onu ezerdi. Numara o zaman eskisi
    gibi açılıştaki öneride kalır.
    """
    if "hasta_cycle_no_elle" not in _kolonlari(b, "cycle"):
        return []
    satirlar = b.execute(
        "SELECT c.id, c.cycle_no, c.hasta_cycle_no, c.hasta_cycle_no_elle "
        "FROM cycle c WHERE c.hasta_id = ? "
        f"ORDER BY {tedavi_tarihi(b, 'c')}, c.id", (hasta_id,)).fetchall()
    degisen, onceki = [], 0
    for cid, cycle_no, eski, yazilan in satirlar:
        yeni = yazilan if yazilan is not None and yazilan > onceki else onceki + 1
        if eski != yeni:
            b.execute("UPDATE cycle SET hasta_cycle_no = ? WHERE id = ?",
                      (yeni, cid))
            degisen.append((cid, cycle_no, eski, yeni))
        onceki = yeni
    return degisen


# ----------------------------------------------------------------- yerel ayar

YEREL_DOSYA = VERI_KOK / "yerel_ayar.json"
KOK = VERI_KOK          # `snapshot/` ve `arsiv/` varsayılanları buna göre
MAKINE = platform.node() or "bilinmeyen"

# Bu anahtarlar makineye özgüdür: her bilgisayarda kendi değeri olur
YOL_ANAHTARLARI = ("goruntu_kaynak_klasor", "goruntu_arsiv_klasor", "yedek_klasor",
                   "cryo_harita_klasor")


def _varsayilan_yollar() -> dict:
    """Bu makine için makul varsayılanlar. Klasörle birlikte taşınır."""
    ev = Path.home()
    if platform.system() == "Windows":
        yedek = "D:\\lab_yedek"
    else:
        yedek = str(ev / "lab_yedek")
    return {
        "goruntu_kaynak_klasor": str(KOK / "snapshot"),
        "goruntu_arsiv_klasor": str(KOK / "arsiv"),
        "yedek_klasor": yedek,
        # Cryo Haritası'nın Excel'i (v6.191; klasörü v6.203'ten beri seçilebilir).
        "cryo_harita_klasor": str(KOK / "cryo_harita"),
    }


def _dosyayi_oku() -> dict:
    if not YEREL_DOSYA.is_file():
        return {}
    try:
        return json.loads(YEREL_DOSYA.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _dosyaya_yaz(veri: dict) -> None:
    try:
        YEREL_DOSYA.write_text(json.dumps(veri, indent=2, ensure_ascii=False),
                               encoding="utf-8")
    except OSError:
        pass


def yerel_ayarlar() -> dict:
    """Bu makinenin klasör ayarları.

    Dosya makine adına göre bölümlenir, böylece klasörün tamamı iki bilgisayar
    arasında taşınsa bile her makine kendi yollarını kullanır. Kayıtlı bir yol
    bu makinede yoksa uygulama klasörüne göreli varsayılana düşülür ve dosya
    sessizce güncellenir.
    """
    veri = _dosyayi_oku()

    # Eski düz biçim: {"goruntu_kaynak_klasor": "..."} -> makine bölümüne taşı
    if veri and not any(isinstance(v, dict) for v in veri.values()):
        veri = {MAKINE: veri}
        _dosyaya_yaz(veri)

    bolum = dict(veri.get(MAKINE) or {})
    varsayilan = _varsayilan_yollar()
    degisti = False

    for anahtar in YOL_ANAHTARLARI:
        deger = bolum.get(anahtar)
        # Yedek ve Cryo haritası: yazılanı olduğu gibi tut, yoksa diye
        # varsayılana dönme -- takılı olmayan bir disk olabilir; yazılamazsa
        # yedek ve harita bunu kendi ekranlarında söylüyor (v6.203).
        if anahtar in ("yedek_klasor", "cryo_harita_klasor"):
            if not deger:
                bolum[anahtar] = varsayilan[anahtar]
                degisti = True
            continue
        # Görüntü klasörleri: yoksa veya bu makinede bulunamıyorsa varsayılana dön
        if not deger or not Path(deger).is_dir():
            if deger and Path(deger).is_dir():
                continue
            bolum[anahtar] = varsayilan[anahtar]
            degisti = True

    # Klasörleri oluştur — taşınan kurulumda elle iş kalmasın
    for anahtar in ("goruntu_kaynak_klasor", "goruntu_arsiv_klasor"):
        try:
            Path(bolum[anahtar]).mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    if degisti:
        veri[MAKINE] = bolum
        _dosyaya_yaz(veri)
    return bolum


def yerel_yaz(degerler: dict) -> dict:
    """Bu makinenin yol ayarlarını günceller, yeni bölümü döndürür.

    Dosyada başka makinelerin bölümleri varsa onlara **dokunulmaz** — klasörün
    tamamı USB ile taşındığında klinik bilgisayarı Mac'in yollarını kullanmaya
    başlamasın diye. `YOL_ANAHTARLARI` dışındaki anahtarlar yok sayılır.

    Dosyaya yazanlar yalnızca bu modülde (bu ve `ag_erisimi_yaz()`): ayarı
    iki yerden okumak (ya da yazmak) v6.8'de `yedek.py`'de başa geldi, Mac'te
    `E:\yedek` adında klasör açılmıştı.
    """
    veri = _dosyayi_oku()
    bolum = dict(veri.get(MAKINE) or {})
    for anahtar_ in YOL_ANAHTARLARI:
        deger = (degerler.get(anahtar_) or "").strip()
        if deger:
            bolum[anahtar_] = deger
    veri[MAKINE] = bolum
    _dosyaya_yaz(veri)
    return bolum


# ------------------------------------------------------------ ağ erişimi

# Program iç ağa açık mı, yalnızca bu bilgisayardan mı kullanılıyor (v6.203).
# Kullanıcının isteği: "Program sadece olduğu PC'de çalışsın ... önce yerelde
# açıp daha sonra ağdan yaysak"; kararı: "yeni bir bilgisayara kurulunca
# kapalı başlasın, ben açarım".
# - Makineye özel (`yerel_ayar.json`): `lab.db` USB ile taşınıyor, ayar
#   veritabanında olsaydı Mac'in "açık"ı yeni bilgisayara da giderdi.
# - Yazılmamışsa AÇIK: bugünkü Mac ve klinik kurulumu değişmesin. "Yalnızca bu
#   bilgisayar"ı yeni kurulum yazıyor -- ilk veritabanı bu bilgisayarda
#   açıldığı an (`sifirdan_kur.py`, boş makineye `tasi.py iceri`, ilk açılış
#   ekranı). Makine adına bakıp "bölüm yoksa yeni kurulum" demek güvenilir
#   değil: Mac'in adı ağa göre değişebiliyor, telefonlar sessizce düşerdi.
AG_YEREL = "yerel"
AG_ACIK = "acik"
_AG_ONBELLEK = {"damga": None, "deger": AG_ACIK}


def ag_erisimi() -> str:
    """`AG_YEREL` ya da `AG_ACIK`. Her istekte soruluyor (middleware): dosya
    yalnızca değiştiyse yeniden okunuyor (değişme zamanı + boyut)."""
    try:
        st = YEREL_DOSYA.stat()
        damga = (st.st_mtime_ns, st.st_size)
    except OSError:
        return AG_ACIK
    if _AG_ONBELLEK["damga"] != damga:
        bolum = _dosyayi_oku().get(MAKINE)
        deger = bolum.get("ag_erisimi") if isinstance(bolum, dict) else None
        _AG_ONBELLEK["deger"] = AG_YEREL if deger == AG_YEREL else AG_ACIK
        _AG_ONBELLEK["damga"] = damga
    return _AG_ONBELLEK["deger"]


def ag_erisimi_yaz(deger: str) -> bool:
    """Bu makinenin ağ erişimini yazar; öteki makinelerin bölümüne dokunmaz
    (`yerel_yaz()` gibi). Yazılamadıysa (disk salt okunur, izin yok) False --
    ekran bunu söylüyor, sessizce "kaydedildi" demiyor."""
    if deger not in (AG_YEREL, AG_ACIK):
        raise ValueError(deger)
    veri = _dosyayi_oku()
    bolum = dict(veri.get(MAKINE) or {})
    bolum["ag_erisimi"] = deger
    veri[MAKINE] = bolum
    _dosyaya_yaz(veri)
    _AG_ONBELLEK["damga"] = None
    bolum = _dosyayi_oku().get(MAKINE)
    return isinstance(bolum, dict) and bolum.get("ag_erisimi") == deger


def ayar(anahtar, varsayilan=""):
    """Ayar değeri. Klasör yolları makineye özgü dosyadan, gerisi veritabanından."""
    if anahtar in YOL_ANAHTARLARI:
        deger = yerel_ayarlar().get(anahtar)
        if deger:
            return deger
    r = tek("SELECT deger FROM ayarlar WHERE lab_id = ? AND anahtar = ?",
            (LAB_ID, anahtar))
    return r["deger"] if r else varsayilan


# ------------------------------------------------------------------ hekim

def varsayilan_hekim() -> str:
    """Hekim alanının varsayılan adı (v6.231; `ayarlar.varsayilan_hekim`).

    Kullanıcı: "Hekim ismi yazılan her yerde sabit Mete Çağlar olsun. Hep onu
    göstersin. Farklı birini istersek açılır menüden diğer seçip elle
    yazabilelim." Ad laboratuvarın, kodun değil: `goc_060` bu laboratuvarın
    veritabanına yazıyor, yeni kurulum (`kurulum.ayarlar()`) anahtarı boş
    açıyor. Boşsa (ya da göç çalışmamışsa) '' -- alan eskisi gibi düz yazı
    kutusu. Her hasta ekranında çağrılabilir, hata vermez.
    """
    try:
        return (ayar("varsayilan_hekim", "") or "").strip()
    except sqlite3.Error:
        return ""


def _hekim_anahtari(ad) -> str:
    """Karşılaştırma için: Türkçe büyük harf (`app.tr_buyuk()`'ün kuralı),
    fazla boşluk yok. Yazılan ad değişmiyor, yalnızca karşılaştırılıyor."""
    return " ".join((ad or "").replace("i", "İ").upper().split())


def hekim_secimi(kayitli):
    """Hekim seçicisinin hali (v6.231): {'varsayilan', 'diger', 'deger'}.

    Kayıt boşsa ya da varsayılanın kendisiyse (büyük/küçük harf ve boşluk farkı
    sayılmıyor) seçici varsayılanda, yazı kutusu varsayılanı taşıyor: kaydedilen
    ekranda görünen (`islem_yapani_doldur()`'un kuralı, v6.208). Başka bir ad
    "Diğer", kutuda olduğu gibi -- eski kayıtların kısaltmaları ("M ÇAĞLAR")
    dahil: program kısaltmanın kim olduğunu tahmin edip kaydı değiştirmez.
    Varsayılan hekim yoksa None (alan düz yazı kutusu).
    """
    vh = varsayilan_hekim()
    if not vh:
        return None
    ad = (kayitli or "").strip()
    diger = bool(ad) and _hekim_anahtari(ad) != _hekim_anahtari(vh)
    return {"varsayilan": vh, "diger": diger, "deger": ad if diger else vh}
