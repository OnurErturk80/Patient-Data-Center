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


def yumurta_mi(cycle_tipi) -> bool:
    """Bu tedavide dondurulan/çözülen örnek yumurta mı, embriyo mu?

    Yalnızca `oosit_cryo`'da yumurta dondurulur — `ivf_icsi`'nin
    vitrifikasyon ekranı zaten enjekte edilmiş (embriyo olmuş) örnekleri
    listeliyor (`_ICSI_YAPILMADI` süzgeci). Yumurta donduran yeni bir cycle
    tipi eklersen burayı genişlet.

    `FET_TIPLERI` ile aynı gerekçeyle burada (v6.135): `app.py` ekranda
    (`ornek_adi()`, `icerik_sayisi()`, v6.133) soruyor, `formlar.py` da
    resmî formda soruyor ("2 embriyo" mu "12 yumurta" mı donduruldu) ve
    `app`'i import edemez — app zaten formlar'ı import ediyor.
    """
    return cycle_tipi == "oosit_cryo"

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

    Bir kez bakılıp saklanıyor (`thaw_cycle_var()`'ın deseni). Göçler açılışta
    ilk istekten ÖNCE çalışıyor (v6.49), ilk bakış onlardan sonraya düşer --
    bu yüzden modül yüklenirken ÇAĞIRMA, "yok" cevabı saklanırdı. Tablo ve
    kolon adı her zaman koddan gelir, adresten değil (PRAGMA parametre almaz).
    """
    if (tablo, kolon) not in _KOLONLAR:
        _KOLONLAR[(tablo, kolon)] = any(
            r["name"] == kolon for r in sorgu(f"PRAGMA table_info({tablo})"))
    return _KOLONLAR[(tablo, kolon)]


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
