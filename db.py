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


_TABLO_VAR = {}


def tablo_var(ad: str) -> bool:
    """Bu tablo var mı — yani o göç çalıştırılmış mı?

    Göçü çalıştırmamış makinede program yine açılmalı, yalnızca o özellik
    susmalı (tuzak #3). `app.sifre_istegi_tablosu_var()` aynı işi kendi
    tablosu için yapıyordu; yenisini yazarken kopyalamak yerine bunu çağır.
    Sonuç önbelleğe alınıyor: tablo bir sürecin ömründe ortadan kalkmaz,
    göç açılışta çalışır.
    """
    if ad not in _TABLO_VAR:
        _TABLO_VAR[ad] = bool(tek(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (ad,)))
    return _TABLO_VAR[ad]


def liste(liste_adi):
    """Bir seçim listesinin değerlerini döndürür."""
    return sorgu(
        "SELECT kod, etiket FROM liste_degeri "
        "WHERE lab_id = ? AND liste_adi = ? AND aktif_mi = 1 ORDER BY sira",
        (LAB_ID, liste_adi),
    )


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
