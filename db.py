"""Veritabanı bağlantısı ve yardımcı fonksiyonlar."""

import json
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


def sorgu(sql, parametre=()):
    """Birden çok satır döndüren sorgu."""
    with baglan() as b:
        return b.execute(sql, parametre).fetchall()


def tek(sql, parametre=()):
    """Tek satır döndüren sorgu. Bulunamazsa None."""
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


# ------------------------------------------------- göç çalıştı mı (tuzak #3)

_KOLONLAR = {}


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


def _tedavide_yapilan(o, t, p1) -> tuple:
    adaylar = f"{o}.specimen_id IN (SELECT id FROM specimen WHERE cycle_id = {t})"
    p = list(p1)
    if kolon_var("olay", "thaw_cycle_id"):
        adaylar = (f"({adaylar} OR {o}.specimen_id IN (SELECT tc.specimen_id "
                   "FROM olay tc WHERE tc.tip = 'thaw' AND tc.iptal_mi = 0 "
                   f"AND tc.thaw_cycle_id = {t}))")
        p += p1
    return f"{adaylar} AND {olay_tedavisi(o)} = {t}", p + p1


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


def yeniden_dondurma_var() -> bool:
    """Çözülen embriyo yeniden dondurulabilir mi -- goc_046'nın iki kolonu da
    var mı. Biri yoksa FET'in vitrifikasyon ekranı göç uyarısı basar."""
    return kolon_var("olay", "vit_cycle_id") and cozme_tupu_var()


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
YOL_ANAHTARLARI = ("goruntu_kaynak_klasor", "goruntu_arsiv_klasor", "yedek_klasor")


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
        if anahtar == "yedek_klasor":
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

    Yazan tek yer burası: ayarı iki yerden okumak (ya da yazmak) v6.8'de
    `yedek.py`'de başa geldi, Mac'te `E:\yedek` adında klasör açılmıştı.
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


def ayar(anahtar, varsayilan=""):
    """Ayar değeri. Klasör yolları makineye özgü dosyadan, gerisi veritabanından."""
    if anahtar in YOL_ANAHTARLARI:
        deger = yerel_ayarlar().get(anahtar)
        if deger:
            return deger
    r = tek("SELECT deger FROM ayarlar WHERE lab_id = ? AND anahtar = ?",
            (LAB_ID, anahtar))
    return r["deger"] if r else varsayilan
