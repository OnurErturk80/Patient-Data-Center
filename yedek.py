"""Yedekleme.

**Yedek klasörünün düzeni** (v6.248; kullanıcı: "Bütün otomatik yedeklemeleri
düzenle. Yani ne ne zaman ve nereye kayıt oluyor? Biraz karmaşa var
düzenleyelim."). Bütün yedekler bu bilgisayarın yedek klasöründe (Klasörler
ekranı, başka bir diskte), her biri kendi alt klasöründe:

    <yedek klasörü>/
      veritabani/    lab_YYYYAAGG_SSDD.db: veritabanının yedekleri
                     lab_ONCEKI_*.db: güvenlik kopyaları (`guvenlik_kopyasi_yolu()`)
      arsiv/         fotoğrafların kopyası (birikimli, hiçbiri silinmez)
      cryo_harita/   Cryo Haritası Excel'i: son hali + her günün son hali (30 gün)
      tum_veriler/   her gün 14:00'te "Tüm veriler" Excel'i (30 gün, `oto_yedek.py`)
      BENI_OKU.txt   bunların açıklaması, diske bakan biri için (hasta bilgisi yok)

v6.247'ye kadar veritabanı kopyaları, güvenlik kopyaları ve durum dosyası
klasörün kendisindeydi; Cryo Haritası'nın günlük kopyaları ve "Tüm veriler"
bilgisayarın kendi diskindeki Cryo haritası klasöründe, iki ayrı
`cryo_harita` klasörü vardı. Eski düzenin dosyalarını `eski_duzeni_tasi()`
yerine taşıyor (her yedekte ve program açılınca, taşınacak bir şey yoksa bir
şey yapmaz). Bilgisayarın kendi diskinde yalnızca programın çalışma dosyaları
kalıyor: veritabanı, fotoğraflar, Cryo Haritası Excel'inin son hali.

Bir yedek (`yedekle()`, tek yerde):
  1. Veritabanının tutarlı bir kopyasını alır (SQLite backup API — uygulama
     çalışırken bile güvenli; düz dosya kopyası yarım yazılmış olabilir)
  2. Kopyayı doğrular (integrity_check) — açılmayan yedek yedek değildir
  3. Arşiv klasöründeki yeni fotoğrafları kopyalar
  4. Cryo Haritası'nın Excel'inin son halini ve günün kopyasını alır (v6.191,
     günlük kopya v6.248) -- bilgisayar bozulursa harita programsız da okunsun
  5. Klasörün durum dosyasını yazar: son yedek, neden alındı, yedeklenen
     Cryo Haritası'nın imzası (`oto_yedek.py` ona bakıyor)

Dört yerden çağrılıyor: terminal (`python yedek.py`), Yedekleme ekranının
"Şimdi yedekle"si ve program açıkken `oto_yedek.py` (Cryo Haritası
değişince, her gün 14:00'te). Aynı programın içindeki iki yedek ya da bir
yedek ile geri yükleme aynı anda çalışmasın diye `KILIT`.

**Saklama** (v6.216, `eskileri_temizle()`): son bir günün bütün yedekleri;
14 güne kadar her günün SON yedeği; daha eskide her ayın ilk yedeği kalıcı.
Güvenlik kopyalarına (`lab_ONCEKI_*`) dokunulmuyor.

**"Son yedek" bu klasörden** (`son_yedek()`, v6.248): veritabanına yazılan
`son_yedek` ayarı USB ile öteki bilgisayara, yedekten geri yüklemeyle de
yedeğin alındığı ana gidiyordu -- ekran başka bir bilgisayarın ya da eski bir
günün yedeğini gösteriyordu. Ayar eski sürümler için yazılmaya devam ediyor.

Kullanım:
    python yedek.py                 (hedef: bu makinenin yerel_ayar.json bölümü)
    python yedek.py D:\\lab_yedek    (hedefi elle ver — komut satırı her zaman önce gelir)

Hedef klasörü kalıcı olarak değiştirmek için: Yönetici -> Klasörler
(ya da python yerel_kur.py)
"""

import json
import logging
import os
import re
import shutil
import sqlite3
import sys
import threading
from datetime import date, datetime, timedelta
from pathlib import Path

import db

# Yedeklenen ve yazılan her şey **veri** kökünde (bkz. db.py "iki kök").
KOK = db.VERI_KOK
DB = db.DB_YOLU
LOG = KOK / "yedek.log"

TUMU_SAKLA_SAAT = 24     # son bu kadar saatin bütün yedekleri kalır
GUNLUK_SAKLA = 14        # bu kadar güne kadar her günün son yedeği kalır
AYIN_ILKI_SAKLA = True   # daha eskide her ayın ilk yedeği kalıcı olarak saklanır

# Yedek klasörünün alt klasörleri (v6.248, yukarıdaki belge). Adlar ASCII ve
# küçük harf: programın veri klasöründekiler gibi (`arsiv`, `cryo_harita`),
# klasör USB ile Mac ile Windows arasında gidip gelse de aynı kalsın.
VERITABANI = "veritabani"
ARSIV = "arsiv"
CRYO = "cryo_harita"
TUM_VERILER = "tum_veriler"
BENI_OKU = "BENI_OKU.txt"
DURUM = "yedek_durumu.json"             # `veritabani/` içinde
ESKI_DURUM = "cryo_yedek_durumu.json"   # v6.216–v6.247: klasörün kendisinde

# Günlük Excel kopyaları: `<kök>_YYYY-AA-GG.xlsx`, `EXCEL_SAKLA_GUN` gün.
TUM_VERI_KOKU = "Tum_Veriler"
EXCEL_SAKLA_GUN = 30

# Her gün bu saatte veritabanı yedeği ve "Tüm veriler" (`oto_yedek.py`).
# 14:00 kullanıcının "Tüm veriler" için seçtiği saat (v6.216); yedek de
# aynı saatte, akılda tek saat kalsın (v6.248).
GUNLUK_SAAT = (14, 0)

# Programın verdiği adlar. Taşıma ve temizlik yalnızca bunlara dokunuyor:
# klasörde elle konmuş bir dosya olabilir.
_YEDEK_AD = re.compile(r"^lab_\d{8}_\d{4}(\d{2})?\.db$")
_ONCEKI_AD = re.compile(r"^lab_ONCEKI_\d{8}_\d{6}\.db$")

# Yedeğin nedeni (durum dosyasında, ekranın "Son yedek"inde -- `metin()`
# anahtarı `yedek_neden_<kod>`).
NEDENLER = ("cryo", "gunluk", "elle", "terminal")

# Aynı programda iki yedek aynı anda çalışmasın (v6.216): Cryo değişince
# alınan yedek ile "Şimdi yedekle" aynı klasöre, aynı dakikanın adına
# yazabilirdi. Geri yükleme de bunu tutuyor (`geri_yukle.geri_yukle()`,
# v6.248'den beri gerçekten -- v6.216'nın bu yorumu söylüyordu, kod
# almıyordu): temizlik ve eski düzenin taşınması seçilen yedeği tam o
# sırada silmesin, yerinden oynatmasın. Terminalden ayrı bir süreçte çalışan
# `yedek.py`'yi kapsamaz; onun için yazım geçici dosyaya
# (`veritabani_yedekle()`).
KILIT = threading.RLock()

# Terminalden çalışınca satırlar ekrana da basılıyor (`main()`); programın
# içinde `print` değil günlük (CLAUDE.md: servis olarak çalışırken konsol yok).
EKRANA = False
_gunluk = logging.getLogger("program")


def yaz(mesaj):
    satir = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {mesaj}"
    if EKRANA:
        print(satir)
    else:
        _gunluk.info("YEDEK: %s", mesaj)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(satir + "\n")
    except OSError:
        pass                     # günlük yazılamadı diye yedek durmasın


def ayar(anahtar, varsayilan=""):
    """Ayar okur — uygulamayla AYNI kaynaktan.

    Eskiden bu dosyanin kendi okuyucusu vardi ve `yerel_ayar.json`'i duz bir
    sozluk saniyordu. Uygulama dosyayi makineye bolumlu bicime
    (`{"makine-adi": {...}}`) cevirdikten sonra `anahtar in d` artik tutmuyor,
    okuyucu sessizce veritabanindaki Windows yoluna dusuyordu: Mac'te calisma
    klasorunun altinda `E:\\yedek` diye bir klasor acilip "Yedekleme tamam"
    yaziliyordu. Tek dogru kaynak `db.ayar()` (README v6.8).
    """
    try:
        return db.ayar(anahtar, varsayilan)
    except sqlite3.Error:
        return varsayilan


def ayar_yaz(anahtar, deger):
    try:
        db.yaz(
            "INSERT INTO ayarlar (lab_id, anahtar, deger) VALUES (?,?,?) "
            "ON CONFLICT(lab_id, anahtar) DO UPDATE SET deger=excluded.deger",
            (db.LAB_ID, anahtar, deger))
    except sqlite3.Error as e:
        yaz(f"UYARI: {anahtar} ayari yazilamadi: {e}")


def bu_makineye_uygun_mu(yol: str) -> bool:
    """Yol bu isletim sisteminde gercekten mutlak bir yol mu?

    `E:\\yedek` Mac'te gecerli bir dosya adidir — hata vermez, calisma
    klasorunun altina o adda bir klasor acar ve yedek alinmis gibi gorunur.
    Yanlis diske yedek almaktansa durup soylemek gerekir.
    """
    surucu_harfi = len(yol) > 1 and yol[1] == ":" and yol[0].isalpha()
    if os.name == "nt":
        return surucu_harfi or yol.startswith("\\\\")   # C:\... veya UNC
    return not surucu_harfi


# ------------------------------------------------------------ klasörün düzeni

def hedef_durumu():
    """Bu bilgisayarın yedek klasörü kullanılabilir mi -> (yol, engel).

    engel None ise yol bir `Path`; değilse "ayarlanmamis", "yanlis_makine"
    (Mac'te `E:\\yedek`) ya da "bulunamadi" (klasör yok: disk takılı değil).
    Klasör burada OLUŞTURULMAZ: takılı olmayan bir diskin yerine (Mac'te
    `/Volumes/...`) iç diskte klasör açılırsa disk takılınca başka adla
    bağlanır, yedek yanlış yerde birikirdi (v6.216). İlk klasörü "Şimdi
    yedekle" açar (`yedekle()`).
    """
    yol = ayar("yedek_klasor", "")
    if not yol:
        return None, "ayarlanmamis"
    if not bu_makineye_uygun_mu(yol):
        return yol, "yanlis_makine"
    if not Path(yol).is_dir():
        return yol, "bulunamadi"
    return Path(yol), None


def veritabani_klasoru(hedef_klasor) -> Path:
    return Path(hedef_klasor) / VERITABANI


def gunluk_ad(kok: str, gun) -> str:
    """Günlük Excel kopyasının adı: `Tum_Veriler_2026-10-05.xlsx`."""
    return f"{kok}_{gun.isoformat()}.xlsx"


def gunluk_gunu(kok: str, ad: str):
    """`<kök>_YYYY-AA-GG.xlsx` -> o gün (`date`); ad kalıba uymuyorsa None."""
    e = re.match(r"^" + re.escape(kok) + r"_(\d{4}-\d{2}-\d{2})\.xlsx$", ad)
    if not e:
        return None
    try:
        return date.fromisoformat(e.group(1))
    except ValueError:
        return None


def gunlukleri_temizle(klasor: Path, kok: str, bugun) -> None:
    """`EXCEL_SAKLA_GUN` günden eski günlük kopyaları siler; adı kalıba
    uymayan dosyaya dokunmaz."""
    sinir = bugun - timedelta(days=EXCEL_SAKLA_GUN)
    try:
        dosyalar = list(klasor.iterdir())
    except OSError:
        return
    for p in dosyalar:
        g = gunluk_gunu(kok, p.name)
        if g is not None and g < sinir:
            try:
                p.unlink()
            except OSError:
                pass
    _yarim_kalanlari_sil(klasor)


def son_gunluk(klasor: Path, kok: str):
    """Klasördeki en yeni günlük kopya: {"gun": date, "dosya": ad} ya da
    None (klasör yoksa da)."""
    en = None
    try:
        dosyalar = list(klasor.iterdir())
    except OSError:
        return None
    for p in dosyalar:
        g = gunluk_gunu(kok, p.name)
        if g is not None and (en is None or g > en[0]):
            en = (g, p.name)
    return {"gun": en[0], "dosya": en[1]} if en else None


def son_yedek(hedef_klasor):
    """Klasördeki en yeni veritabanı yedeği (güvenlik kopyası değil):
    {"zaman": datetime, "dosya": ad} ya da None. Zaman adından (dakikası).

    Ekranın "Son yedek"i bu (v6.248): veritabanına yazılan `son_yedek`
    ayarı USB ile öteki bilgisayara, geri yüklemeyle de yedeğin alındığı ana
    gidiyordu. Eski düzende kalmış (klasörün kendisindeki) yedekler de
    sayılıyor: taşınmadan önce de doğru söylesin.
    """
    en = None
    for klasor in (veritabani_klasoru(hedef_klasor), Path(hedef_klasor)):
        try:
            dosyalar = list(klasor.glob("lab_*.db"))
        except OSError:
            continue
        for p in dosyalar:
            if not _YEDEK_AD.match(p.name):
                continue
            t = yedek_tarihi(p)
            if t is not None and (en is None or t > en[0]):
                en = (t, p.name)
    return {"zaman": en[0], "dosya": en[1]} if en else None


def durum_oku(hedef_klasor) -> dict:
    """Klasörün durum dosyası: son yedeğin zamanı, dosyası, nedeni ve
    yedeklenen Cryo Haritası'nın imzası (`oto_yedek.py`). Yoksa ya da
    okunamıyorsa {}. v6.247'ye kadarki yerinde (klasörün kendisinde) de
    bakıyor."""
    for yol in (veritabani_klasoru(hedef_klasor) / DURUM,
                Path(hedef_klasor) / ESKI_DURUM):
        try:
            d = json.loads(yol.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict):
            return d
    return {}


def _durum_yaz(hedef_klasor, veri: dict) -> None:
    import harita_excel               # atomik yazım tek yerde
    vt = veritabani_klasoru(hedef_klasor)
    vt.mkdir(parents=True, exist_ok=True)
    veri = {**veri, "not": "Program yazar (Patient Data Center): bu klasordeki son "
                           "yedek ve yedeklenen Cryo Haritasi'nin imzasi. Silinirse "
                           "bir sonraki turda yeniden yedek alinir."}
    harita_excel.atomik_yaz(
        vt / DURUM, json.dumps(veri, ensure_ascii=False, indent=2).encode("utf-8"))
    (Path(hedef_klasor) / ESKI_DURUM).unlink(missing_ok=True)


def guvenlik_kopyasi_yolu() -> Path:
    """`lab_ONCEKI_<zaman>.db`: veritabanını bütünüyle değiştiren bir işten
    hemen önceki halin kopyası nereye (v6.248, tek yerde). Yedekten geri
    yükleme, USB'den alma (`tasi.py iceri`), hasta kartı ve tedavi
    birleştirme bunu çağırıyor.

    Yedek klasörü bu bilgisayarda varsa `veritabani/` (başka disk; geri
    yükleme listesinde "önceki hâlin güvenlik kopyası" diye görünür), yoksa
    veri klasörü. v6.247'ye kadar `tasi.py` hep veri klasörüne, ötekiler
    yedek klasörünün kendisine yazıyordu. Saklama bunlara dokunmaz.
    """
    yol, engel = hedef_durumu()
    ad = f"lab_ONCEKI_{datetime.now():%Y%m%d_%H%M%S}.db"
    if engel is None:
        vt = veritabani_klasoru(yol)
        try:
            vt.mkdir(exist_ok=True)
            return vt / ad
        except OSError:
            pass
    return KOK / ad


def _ayni_yer(a: Path, b: Path) -> bool:
    """İki yol aynı dosya ya da klasör mü (büyük/küçük harf, bağlantı,
    göreli yol farkı sayılmıyor). Biri yoksa False."""
    try:
        return a.samefile(b)
    except OSError:
        return False


def _kopyala(kaynak: Path, hedef: Path) -> None:
    """Kopya önce yanındaki geçici dosyaya, sonra yerine: yarım dosya
    kalmaz (disk çekildi, program kapandı)."""
    gecici = hedef.with_name(hedef.name + ".yaziliyor")
    try:
        shutil.copy2(kaynak, gecici)
        os.replace(gecici, hedef)
    finally:
        gecici.unlink(missing_ok=True)


def _dosya_tasi(kaynak: Path, hedef: Path) -> None:
    """Başka bir klasöre -- başka bir diske de -- taşır: önce kopya
    (`_kopyala()`), sonra kaynak silinir; yarıda kalırsa kaynak yerinde.
    Hedefte aynı adlı dosya varsa o kalır (ikisi de o günün tam bir kopyası,
    hedeftekini yeni düzen yazdı), kaynak silinir. Hata yükselir."""
    if not hedef.exists():
        _kopyala(kaynak, hedef)
    kaynak.unlink()


def _yarim_kalanlari_sil(klasor: Path) -> None:
    """Yarıda kalmış yazımlar (program ya da disk o sırada gitti): bir
    günden eskiyse."""
    sinir = datetime.now().timestamp() - 86400
    try:
        dosyalar = list(klasor.glob("*.yaziliyor"))
    except OSError:
        return
    for p in dosyalar:
        try:
            if p.stat().st_mtime < sinir:
                p.unlink()
        except OSError:
            pass


def _yereldeki_gunlukleri_tasi(hedef_klasor: Path) -> int:
    """Cryo Haritası'nın günlük kopyaları ve "Tüm veriler": v6.247'ye kadar
    bilgisayarın kendi diskindeki Cryo haritası klasörüne yazılıyordu, artık
    yedek klasöründe. Saklama süresi (`EXCEL_SAKLA_GUN`) dolmuşlar taşınmıyor,
    siliniyor -- eski düzende de silinecekti. Cryo haritası klasörü yedekteki
    alt klasörün kendisiyse (Klasörler'de öyle seçilmiş) dokunulmuyor."""
    import harita_excel               # yol tek yerde (tuzak #8)
    yerel = harita_excel.klasor()
    if not yerel.is_dir():
        return 0
    bugun = date.today()
    sinir = bugun - timedelta(days=EXCEL_SAKLA_GUN)
    sayi = 0
    for kok, alt in ((harita_excel.ana_dosya().stem, CRYO),
                     (TUM_VERI_KOKU, TUM_VERILER)):
        hedef = Path(hedef_klasor) / alt
        if _ayni_yer(yerel, hedef):
            continue
        try:
            dosyalar = [p for p in yerel.iterdir() if gunluk_gunu(kok, p.name)]
        except OSError:
            continue
        for p in dosyalar:
            try:
                if gunluk_gunu(kok, p.name) < sinir:
                    p.unlink()
                    continue
                hedef.mkdir(exist_ok=True)
                _dosya_tasi(p, hedef / p.name)
                sayi += 1
            except OSError as e:
                yaz(f"UYARI: {p} {alt}/ klasorune tasinamadi: {e}")
    return sayi


def eski_duzeni_tasi(hedef_klasor) -> int:
    """v6.247'ye kadarki düzenin dosyalarını yerine taşır (v6.248):

    - klasörün kendisindeki veritabanı yedekleri ve güvenlik kopyaları ->
      `veritabani/` (aynı disk, yalnızca yer değiştiriyor);
    - veri klasöründeki güvenlik kopyaları -> `veritabani/` (başka disk:
      önce kopya, sonra silinir);
    - eski durum dosyası (`cryo_yedek_durumu.json`) -> `veritabani/yedek_durumu.json`;
    - bilgisayarın kendi diskindeki Cryo haritası klasöründen Cryo
      Haritası'nın günlük kopyaları -> `cryo_harita/`, "Tüm veriler" ->
      `tum_veriler/`.

    Yalnızca programın verdiği adlar; elle konmuş dosyaya dokunulmaz. Her
    yedekte ve program açılınca çağrılıyor; taşınacak bir şey yoksa bir şey
    yapmaz. Hata yükselmez: taşınamayan dosya yerinde kalır, günlüğe yazılır,
    bir sonrakinde yeniden denenir. -> taşınan dosya sayısı.
    """
    hedef_klasor = Path(hedef_klasor)
    sayi = 0
    with KILIT:
        vt = veritabani_klasoru(hedef_klasor)
        try:
            eskiler = [p for p in hedef_klasor.glob("lab_*.db")
                       if _YEDEK_AD.match(p.name) or _ONCEKI_AD.match(p.name)]
        except OSError:
            eskiler = []
        for p in eskiler:
            if (vt / p.name).exists():
                continue
            try:
                vt.mkdir(exist_ok=True)
                os.replace(p, vt / p.name)
                sayi += 1
            except OSError as e:
                yaz(f"UYARI: {p.name} {VERITABANI}/ klasorune tasinamadi: {e}")
        _yarim_kalanlari_sil(hedef_klasor)

        # Veri klasöründe kalmış güvenlik kopyaları (v6.247'ye kadar
        # `tasi.py` hep oraya, ötekiler yedek klasörü yokken oraya yazıyordu):
        # başka diske, geri yükleme listesine.
        if not _ayni_yer(KOK, hedef_klasor):
            try:
                yereldekiler = [p for p in KOK.glob("lab_ONCEKI_*.db")
                                if _ONCEKI_AD.match(p.name)]
            except OSError:
                yereldekiler = []
            for p in yereldekiler:
                try:
                    vt.mkdir(exist_ok=True)
                    _dosya_tasi(p, vt / p.name)
                    sayi += 1
                except OSError as e:
                    yaz(f"UYARI: {p.name} {VERITABANI}/ klasorune tasinamadi: {e}")

        eski = hedef_klasor / ESKI_DURUM
        if eski.is_file():
            try:
                if not (vt / DURUM).exists():
                    d = json.loads(eski.read_text(encoding="utf-8"))
                    if isinstance(d, dict):
                        _durum_yaz(hedef_klasor, d)        # eskisini de siler
                eski.unlink(missing_ok=True)
            except (OSError, ValueError) as e:
                yaz(f"UYARI: {ESKI_DURUM} tasinamadi: {e}")

        try:
            sayi += _yereldeki_gunlukleri_tasi(hedef_klasor)
        except Exception as e:            # yedeği durdurmasın (belgedeki söz)
            yaz(f"UYARI: Cryo haritasi klasorundeki eski kopyalar tasinamadi: {e}")
    if sayi:
        yaz(f"Yedek klasorunun yeni duzeni: {sayi} dosya yerine tasindi "
            f"({VERITABANI}/, {CRYO}/, {TUM_VERILER}/).")
    return sayi


_BENI_OKU_METNI = """\
PATIENT DATA CENTER -- YEDEK KLASÖRÜ

Bu klasördeki her şeyi program yazar. Kopyalayabilirsiniz; dosyaları
taşımayın, adlarını değiştirmeyin: program eskileri kendi kuralıyla siler.

{veritabani}/
    Veritabanının yedekleri: lab_YYYYAAGG_SSDD.db
    (örnek: lab_20261005_1400.db = 05.10.2026 saat 14:00).
    Ne zaman: Cryo Haritası'nda her değişiklikten birkaç dakika sonra
    (dondurma, çözme, taşıma, yer), her gün {saat}'te (program o saatte
    kapalıysa açılınca) ve Yedekleme ekranında "Şimdi yedekle"ye basılınca.
    Saklanan: son {tumu} saatin hepsi, {gunluk} güne kadar her günün
    sonuncusu, daha eskide her ayın ilki.
    lab_ONCEKI_...db: güvenlik kopyası -- yedekten geri yüklemeden, USB'den
    veri almadan, iki hasta kartını ya da iki tedaviyi birleştirmeden
    hemen önceki hal. Program bunları silmez; gerekmediğinden eminseniz
    elle silebilirsiniz.

{arsiv}/
    Fotoğrafların kopyası. Her yedekte yalnızca yeni fotoğraflar eklenir,
    hiçbiri silinmez.

{cryo}/
    Cryo Haritası Excel'i: Cryo_Haritasi.xlsx (son yedekteki hali) ve her
    günün son hali (Cryo_Haritasi_YYYY-AA-GG.xlsx, son {excel} gün).
    Program çalışmasa da Excel'de açılabilir.

{tum}/
    Her gün {saat}'te "Tüm veriler" Excel'i (Tum_Veriler_YYYY-AA-GG.xlsx,
    son {excel} gün): bütün tedaviler, yumurta ve embriyolar. Bütün hasta
    kayıtlarını taşır.

Geri yüklemek için: programda Yönetici -> Yedekleme -> Yedekten geri yükle.
Bu klasörün yeri: Yönetici -> Klasörler -> Yedek klasörü.
"""


def beni_oku_yaz(hedef_klasor) -> None:
    """Klasöre bakan biri için açıklama (v6.248; hasta bilgisi yok).
    Windows'un eski Not Defteri de Türkçe okusun diye BOM'lu UTF-8 ve CRLF.
    İçerik aynıysa yazılmaz."""
    metin = _BENI_OKU_METNI.format(
        veritabani=VERITABANI, arsiv=ARSIV, cryo=CRYO, tum=TUM_VERILER,
        saat="%02d:%02d" % GUNLUK_SAAT, tumu=TUMU_SAKLA_SAAT,
        gunluk=GUNLUK_SAKLA, excel=EXCEL_SAKLA_GUN)
    bayt = metin.replace("\n", "\r\n").encode("utf-8-sig")
    yol = Path(hedef_klasor) / BENI_OKU
    try:
        if yol.read_bytes() == bayt:
            return
    except OSError:
        pass
    import harita_excel               # atomik yazım tek yerde
    harita_excel.atomik_yaz(yol, bayt)


# ------------------------------------------------------------ yedek

def veritabani_yedekle(hedef_klasor: Path) -> Path:
    """SQLite backup API ile tutarlı kopya alır ve doğrular.

    Kopya önce yanındaki geçici dosyaya yazılıyor, doğrulanınca adını alıyor
    (v6.216): yazım yarıda kalırsa (disk çekildi, program kapandı) geri
    yükleme listesinde yarım bir `lab_*.db` durmasın; aynı dakikada ikinci
    bir yedek de öncekinin yazılmakta olan dosyasına yazmasın.
    """
    hedef_klasor.mkdir(parents=True, exist_ok=True)
    ad = f"lab_{datetime.now():%Y%m%d_%H%M}.db"
    hedef = hedef_klasor / ad
    gecici = hedef_klasor / f"{ad}.{os.getpid()}.yaziliyor"

    kaynak = kopya = None
    try:
        kaynak = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        kopya = sqlite3.connect(gecici)
        with kopya:
            kaynak.backup(kopya)    # uygulama yazarken bile tutarlı anlık görüntü
        kaynak.close()
        kaynak = None

        # Dogrulama
        sonuc = kopya.execute("PRAGMA integrity_check").fetchone()[0]
        tablo = kopya.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
        try:
            hasta = kopya.execute("SELECT COUNT(*) FROM hasta").fetchone()[0]
            cycle = kopya.execute("SELECT COUNT(*) FROM cycle").fetchone()[0]
            goruntu = kopya.execute("SELECT COUNT(*) FROM goruntu").fetchone()[0]
        except sqlite3.Error:
            hasta = cycle = goruntu = -1
        kopya.close()
        kopya = None

        if sonuc != "ok":
            raise RuntimeError(f"Yedek dogrulanamadi: {sonuc}")
        os.replace(gecici, hedef)
    finally:
        # Yarıda kalınca bağlantılar açık kalmasın: Windows açık dosyayı
        # silemez, asıl hatanın yerine silme hatası yükselirdi.
        for b in (kaynak, kopya):
            if b is not None:
                try:
                    b.close()
                except sqlite3.Error:
                    pass
        try:
            gecici.unlink(missing_ok=True)
        except OSError:
            pass

    mb = hedef.stat().st_size / 1024 / 1024
    yaz(f"Veritabani: {hedef.name}  ({mb:.1f} MB, {tablo} tablo, "
        f"{hasta} hasta, {cycle} cycle, {goruntu} goruntu)")
    return hedef


def yedek_tarihi(p: Path):
    """`lab_20260929_1403.db` -> o an; yedek adı değilse (`lab_ONCEKI_*`,
    elle konmuş bir dosya) None -- temizlik ona hiç dokunmaz."""
    for kalip in ("%Y%m%d_%H%M", "%Y%m%d_%H%M%S"):
        try:
            return datetime.strptime(p.stem[4:], kalip)
        except ValueError:
            continue
    return None


def silinecek_yedekler(hedef_klasor: Path, simdi=None) -> list:
    """Saklama kuralının dışında kalan yedekler (v6.216; yukarıdaki belge).

    v6.215'e kadar kural "14 günün hepsi + ayın 1'inde alınanlar"dı; günde
    bir yedekle aynı sonucu veriyor. Cryo Haritası değişince alınan
    yedeklerle günde birkaç kopya birikiyor: 24 saatten eskisinin yalnızca
    o günün sonuncusu kalıyor. Aylık kalıcı kopya "ayın ilk yedeği" (ayın
    1'inde birden çok yedek olabiliyor, ayın 1'inde hiç yedek alınmamış
    olabiliyor).
    """
    simdi = simdi or datetime.now()
    yedekler = []
    for p in hedef_klasor.glob("lab_*.db"):
        t = yedek_tarihi(p)
        if t is not None:
            yedekler.append((t, p))
    yedekler.sort()
    if not yedekler:
        return []
    gunun_sonu, ayin_ilki = {}, {}
    for t, p in yedekler:
        gunun_sonu[t.date()] = p                        # sıralı: sonuncu kalır
        ayin_ilki.setdefault((t.year, t.month), p)      # sıralı: ilki kalır
    kalacak = {yedekler[-1][1]}                         # en yenisi her zaman
    for t, p in yedekler:
        yas = simdi - t
        if yas < timedelta(hours=TUMU_SAKLA_SAAT):
            kalacak.add(p)
        elif yas < timedelta(days=GUNLUK_SAKLA) and gunun_sonu[t.date()] == p:
            kalacak.add(p)
        elif AYIN_ILKI_SAKLA and ayin_ilki[(t.year, t.month)] == p:
            kalacak.add(p)
    return [p for _, p in yedekler if p not in kalacak]


def eskileri_temizle(hedef_klasor: Path):
    silinen = 0
    for p in silinecek_yedekler(hedef_klasor):
        p.unlink(missing_ok=True)
        silinen += 1
    _yarim_kalanlari_sil(hedef_klasor)
    if silinen:
        yaz(f"{silinen} eski veritabani kopyasi silindi (son {TUMU_SAKLA_SAAT} "
            f"saatin hepsi, {GUNLUK_SAKLA} gune kadar her gunun sonuncusu, "
            "daha eskide her ayin ilki kalir)")


def arsiv_yedekle(arsiv: Path, hedef_klasor: Path):
    """Yeni veya degismis fotograflari kopyalar. Hedeften hicbir sey silinmez."""
    if not arsiv.is_dir():
        yaz(f"Arsiv klasoru yok, atlandi: {arsiv}")
        return
    hedef = hedef_klasor / ARSIV
    yeni = guncel = 0
    for kaynak in arsiv.rglob("*"):
        if not kaynak.is_file():
            continue
        h = hedef / kaynak.relative_to(arsiv)
        if h.exists() and h.stat().st_size == kaynak.stat().st_size:
            guncel += 1
            continue
        h.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kaynak, h)
        yeni += 1
    yaz(f"Arsiv: {yeni} yeni dosya kopyalandi, {guncel} dosya zaten guncel")


def harita_yedekle(hedef_klasor: Path):
    """Cryo Haritası'nın Excel'i (`harita_excel.py`, v6.191) yedek klasörüne:
    son hali (`cryo_harita/Cryo_Haritasi.xlsx`) ve günün kopyası
    (`Cryo_Haritasi_YYYY-AA-GG.xlsx`, `EXCEL_SAKLA_GUN` gün; günün sonraki
    yedeği üzerine yazar, kalan o günün son hali). Bilgisayar bozulursa
    harita programsız da okunabilsin. v6.248'e kadar günlük kopyalar
    bilgisayarın kendi diskindeki Cryo haritası klasöründe, yedekte yalnızca
    son hali vardı. Kopyalanamazsa yedeklemeyi durdurmaz -- asıl yedek
    veritabanı, harita ondan yeniden üretilebilir."""
    import harita_excel               # yol tek yerde (tuzak #8)
    kaynak = harita_excel.ana_dosya()
    if not kaynak.is_file():
        yaz("Cryo haritasi Excel'i yok, atlandi (program acildiginda yazilir).")
        return
    hedef = Path(hedef_klasor) / CRYO
    bugun = date.today()
    try:
        hedef.mkdir(parents=True, exist_ok=True)
        # Cryo haritası klasörü Klasörler'de bu alt klasör seçilmişse son
        # hali zaten burada; yalnızca günün kopyası.
        if not _ayni_yer(kaynak, hedef / kaynak.name):
            _kopyala(kaynak, hedef / kaynak.name)
        _kopyala(kaynak, hedef / gunluk_ad(kaynak.stem, bugun))
        gunlukleri_temizle(hedef, kaynak.stem, bugun)
        yaz(f"Cryo haritasi Excel'i kopyalandi: {hedef}")
    except OSError as e:
        yaz(f"UYARI: Cryo haritasi Excel'i kopyalanamadi: {e}")


def yedekle(hedef_klasor: Path, kaynak: str, imza=None, neden=None) -> Path:
    """Bütün yedekleme, tek yerden: eski düzenin taşınması, veritabanı, eski
    kopyaların temizliği, arşivdeki yeni fotoğraflar, Cryo Haritası'nın
    Excel'i, `BENI_OKU.txt`, klasörün durum dosyası, "son yedek" ayarı.

    Terminal (`main()`), "Şimdi yedekle" ve otomatik yedek (`oto_yedek.py`)
    bunu çağırıyor. `kaynak`: günlüğe yazılan açıklama; `neden`: `NEDENLER`'den
    biri (ekranın "Son yedek"i); `imza`: yedeklenen Cryo Haritası'nın imzası
    (`oto_yedek.py`; verilmezse durum dosyasındaki eski imza kalır -- terminal
    haritayı bilmiyor). Hata yükselir (`yaz()` önce günlüğe yazar); hedef
    klasör yoksa oluşturulur, kullanılabilir olup olmadığına çağıran karar
    verir. Yazılan veritabanı kopyasının yolunu döndürür.
    """
    hedef_klasor = Path(hedef_klasor)
    with KILIT:
        yaz("=" * 55)
        yaz(f"Yedekleme basladi -> {hedef_klasor}   (kaynak: {kaynak})")
        try:
            hedef_klasor.mkdir(parents=True, exist_ok=True)
            eski_duzeni_tasi(hedef_klasor)
            vt = veritabani_klasoru(hedef_klasor)
            yol = veritabani_yedekle(vt)
            eskileri_temizle(vt)
            arsiv_klasor = Path(ayar("goruntu_arsiv_klasor", str(KOK / "arsiv")))
            arsiv_yedekle(arsiv_klasor, hedef_klasor)
            harita_yedekle(hedef_klasor)
            try:
                beni_oku_yaz(hedef_klasor)
            except OSError as e:
                yaz(f"UYARI: {BENI_OKU} yazilamadi: {e}")
            zaman = datetime.now().isoformat(" ", "seconds")
            try:
                eski = durum_oku(hedef_klasor)
                _durum_yaz(hedef_klasor, {
                    "zaman": zaman, "dosya": yol.name,
                    "neden": neden if neden in NEDENLER else None,
                    "imza": imza if imza is not None else eski.get("imza")})
            except OSError as e:          # yedek alındı; otomatik yedek bir kez daha alır
                yaz(f"UYARI: {DURUM} yazilamadi: {e}")
            ayar_yaz("son_yedek", zaman)  # eski sürümler okuyor; ekran klasörden
        except Exception as e:
            yaz(f"HATA: {e}")
            raise
        yaz("Yedekleme tamam.")
        return yol


def main():
    global EKRANA
    EKRANA = True
    if not DB.exists():
        yaz("HATA: lab.db bulunamadi.")
        sys.exit(1)

    if len(sys.argv) > 1:
        hedef, kaynak = sys.argv[1], "komut satiri"
    else:
        hedef, kaynak = ayar("yedek_klasor", ""), f"{db.MAKINE} ayari"
    if not hedef:
        yaz("HATA: yedek klasoru tanimli degil. "
            "Once 'python yerel_kur.py' calistir ya da hedefi elle ver: "
            "python yedek.py D:\\lab_yedek")
        sys.exit(1)

    if not bu_makineye_uygun_mu(hedef):
        yaz(f"HATA: '{hedef}' bu isletim sisteminin yolu degil ({kaynak}).")
        yaz("      Yedek alinmadi. Bu makinenin hedefini 'python yerel_kur.py' "
            "ile ayarla.")
        sys.exit(1)

    hedef_klasor = Path(hedef)

    # Veritabanindaki eski deger baska bir makineye ait olabilir. Yol ayarlari
    # artik makineye ozgu dosyadan okunuyor; fark varsa sessiz kalma.
    try:
        r = db.tek("SELECT deger FROM ayarlar WHERE lab_id = ? AND anahtar = ?",
                   (db.LAB_ID, "yedek_klasor"))
        db_deger = (r["deger"] or "") if r else ""
    except sqlite3.Error:
        db_deger = ""            # sadece bilgi notu — yedeklemeyi engellemesin
    if db_deger and db_deger != hedef:
        yaz(f"NOT: veritabanindaki yedek_klasor ({db_deger}) baska bir makineye "
            "ait, kullanilmadi.")

    try:
        yedekle(hedef_klasor, kaynak, neden="terminal")
    except Exception:
        sys.exit(1)                 # sebebi yedekle() yazdı


if __name__ == "__main__":
    main()
