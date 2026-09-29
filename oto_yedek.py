"""Cryo Haritası değişince yedek + her gün 14:00'te "Tüm veriler" (v6.216).

Kullanıcının isteği (2026-09-29): "Cryo haritada yapılan her değişiklikten
sonra yedekleme yapsın. Yönetici kısmındaki tüm verileri excele aktar'da her
gün 14:00'da cryo haritanın yedeklendiği dosyaya aktarsın."

Program açıkken arka plandaki bir iş parçacığı dakikada bir iki işe bakar:

1. **Cryo Haritası değişince yedek.** Harita her kurulduğunda içeriğinin bir
   imzası var (`harita_excel.guncel_imza()`: dolu tüpler, Excel kayıtları,
   yerler, straw'ların yazıları). İmza yedek klasöründe yedeklenmiş son
   halinkinden farklıysa yedek alınır -- "Şimdi yedekle"nin aynısı
   (`yedek.yedekle()`: veritabanı, arşivdeki yeni fotoğraflar, haritanın
   Excel'i).
   - **Değişiklikler bitince**: harita bir tur (bir dakika) değişmeden
     kalınca; değişiklik sürüp gidiyorsa ilk değişiklikten en geç
     `EN_GEC_SN` sonra. Bir hastanın dört straw'ı arka arkaya dondurulunca
     dört değil bir yedek.
   - **Son yedeğin imzası yedek klasöründe** (`DURUM_DOSYASI`): program
     yeniden açılınca değişmemiş harita için yedek alınmaz; program
     kapalıyken değişmişse (terminal aracı, USB ile gelen veritabanı)
     alınır. Başka bir klasör ya da disk kendi dosyasıyla sayılır.
   - **Yedek klasörü yoksa beklenir** (disk takılı değil), gelince alınır.
     Klasör kendiliğinden OLUŞTURULMAZ: takılı olmayan bir diskin yerine
     yanlış yerde klasör açılmasın. İlk yedeği "Şimdi yedekle" açar (o
     klasörü oluşturuyor).
   - Harita kurulamıyorsa (bir hata) veritabanının damgasına bakılır:
     yedek, haritanın hatası yüzünden durmasın.
2. **Her gün 14:00'te "Tüm veriler"**: yönetici panelindeki "Tüm veriyi
   Excel'e aktar"ın dosyası (aynı içerik, `disari.tumu_sayfalari()`) Cryo
   haritası klasörüne (`harita_excel.klasor()`, Klasörler ekranı; Cryo
   haritası Excel'i ve günlük kopyaları da orada):
   `Tum_Veriler_YYYY-AA-GG.xlsx`, son `TUM_VERI_SAKLA_GUN` gün. Bugünün
   dosyası varsa yazılmaz; 14:00'te program kapalıysa açıldığında yazılır.
   **Dosya bütün hasta kayıtlarını taşıyor** (indirilen dosyanın aynısı);
   klasörü yönetici seçiyor, ekranlar bunu söylüyor.

Hiçbir hata programı durdurmaz: günlüğe (`program.log`, bir kez), ekrana
(Yedekleme ve Cryo Haritası kartları) yazılır, `HATA_BEKLE_SN` sonra yeniden
denenir. `print` yok (CLAUDE.md). Veritabanı yokken (ilk kurulum ekranı)
hiçbir şeye dokunmaz.
"""

import datetime as _dt
import json
import logging
import re
import threading
from pathlib import Path

import db
import disari
import excel
import harita_excel
import yedek

_gunluk = logging.getLogger("program")

KONTROL_SN = 60
# Açılışta: harita önce kurulsun (`harita_excel.ILK_BEKLEME_SN` + kurulum).
ILK_BEKLEME_SN = 30
EN_GEC_SN = 10 * 60
HATA_BEKLE_SN = 10 * 60

# Yedek klasöründe: Cryo Haritası'nın o klasöre son yedeklenen halinin imzası.
DURUM_DOSYASI = "cryo_yedek_durumu.json"

TUM_VERI_SAATI = (14, 0)
TUM_VERI_KOKU = "Tum_Veriler"
TUM_VERI_SAKLA_GUN = 30
_TUM_VERI_AD = re.compile(r"^" + TUM_VERI_KOKU + r"_(\d{4}-\d{2}-\d{2})\.xlsx$")

_DURDUR = threading.Event()
_IS = None
# Bellekte: program yeniden açılınca yedeğin durumu klasördeki dosyadan,
# "Tüm veriler"inki klasördeki dosyalardan okunuyor.
_Y = {}          # Cryo değişince yedek
_T = {}          # Tüm veriler
_HATALAR = {}    # iş -> günlüğe son yazılan hata (tekrar tekrar yazılmasın)


def _simdi():
    return _dt.datetime.now()


def _hata(is_adi, e) -> None:
    """Hatayı günlüğe bir kez yazar (aynı hata her turda yazılmasın).
    `except` bloğunun içinden çağrılır."""
    if _HATALAR.get(is_adi) != repr(e):
        # Disk / klasör hatası (takılı değil, dolu, izin) tek satır; başka bir
        # hata programın kusuru olabilir, ayrıntısıyla.
        _gunluk.error("OTO YEDEK: %s basarisiz: %s", is_adi, e,
                      exc_info=not isinstance(e, OSError))
    _HATALAR[is_adi] = repr(e)


# ------------------------------------------------------------ yedek

def hedef():
    """Bu bilgisayarın yedek klasörü otomatik yedek için kullanılabilir mi.
    -> (yol, engel): engel None ise yol bir `Path`; değilse "ayarlanmamis",
    "yanlis_makine" (Mac'te `E:\\yedek`) ya da "bulunamadi" (klasör yok)."""
    yol = db.ayar("yedek_klasor", "")
    if not yol:
        return None, "ayarlanmamis"
    if not yedek.bu_makineye_uygun_mu(yol):
        return yol, "yanlis_makine"
    if not Path(yol).is_dir():
        return yol, "bulunamadi"
    return Path(yol), None


def _durum_oku(klasor: Path) -> dict:
    try:
        d = json.loads((klasor / DURUM_DOSYASI).read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _durum_yaz(klasor: Path, imza: str, dosya: str, zaman: str) -> None:
    veri = {"imza": imza, "zaman": zaman, "dosya": dosya,
            "not": "Program yazar (Patient Data Center, v6.216): Cryo "
                   "Haritasi'nin bu klasore son yedeklenen halinin imzasi. "
                   "Silinirse bir sonraki turda yeniden yedek alinir."}
    harita_excel.atomik_yaz(klasor / DURUM_DOSYASI,
                            json.dumps(veri, ensure_ascii=False, indent=2).encode("utf-8"))


def yedekle(klasor: Path, kaynak: str, imza=None, otomatik: bool = False):
    """`yedek.yedekle()` + klasörün durum dosyası. "Şimdi yedekle" de bunu
    çağırıyor: elle alınan yedekten sonra aynı harita için bir daha
    otomatik yedek alınmasın.

    `imza`: yedeklenen haritanın imzası (verilmezse şu anki). `otomatik`:
    kilit alındıktan sonra klasörün dosyası yeniden okunuyor -- o arada
    "Şimdi yedekle" aynı hali yedeklediyse ikinci kez alınmıyor (None döner).
    Hata yükselir. -> yazılan veritabanı kopyasının yolu.
    """
    if imza is None:
        imza = harita_excel.guncel_imza()
    with yedek.KILIT:
        if otomatik and imza and _durum_oku(klasor).get("imza") == imza:
            _Y.update(klasor=str(klasor), yedeklenen=imza)
            return None
        yol = yedek.yedekle(klasor, kaynak)
        zaman = _simdi().isoformat(" ", "seconds")
        if imza:
            try:
                _durum_yaz(klasor, imza, yol.name, zaman)
            except OSError as e:          # yedek alındı; bir sonraki tur tekrarlar
                _gunluk.warning("OTO YEDEK: %s yazilamadi: %s", DURUM_DOSYASI, e)
                imza = None
        _Y.update(klasor=str(klasor) if imza else None, yedeklenen=imza,
                  son=zaman, dosya=yol.name)
        return yol


def _cryo_turu(simdi, damga) -> None:
    yol, engel = hedef()
    _Y.update(engel=engel, yol=str(yol) if yol else None)
    if engel:
        _Y["klasor"] = None             # disk gelince durum dosyası yeniden okunsun
        return
    imza = harita_excel.guncel_imza()
    if imza is None:
        if not harita_excel.kurulamadi():
            return                          # harita henüz kurulmadı
        imza = "damga:" + str(damga())
    if _Y.get("klasor") != str(yol):        # açılış ya da başka klasör / disk
        d = _durum_oku(yol)
        _Y.update(klasor=str(yol), yedeklenen=d.get("imza"),
                  son=d.get("zaman"), dosya=d.get("dosya"))
    if imza == _Y.get("yedeklenen"):
        _Y.update(bekliyor=None, onceki=imza)
        return
    if not _Y.get("bekliyor"):
        _Y["bekliyor"] = simdi
    sakin = imza == _Y.get("onceki")
    _Y["onceki"] = imza
    if not sakin and (simdi - _Y["bekliyor"]).total_seconds() < EN_GEC_SN:
        return                              # değişiklik sürüyor
    if _Y.get("sonraki_deneme") and simdi < _Y["sonraki_deneme"]:
        return
    try:
        yedekle(yol, "Cryo Haritasi degisti", imza=imza, otomatik=True)
    except Exception as e:
        _hata("yedek", e)
        _Y.update(hata=str(e), hata_zamani=simdi.isoformat(" ", "seconds"),
                  sonraki_deneme=simdi + _dt.timedelta(seconds=HATA_BEKLE_SN))
        return
    _HATALAR.pop("yedek", None)
    _Y.update(bekliyor=None, hata=None, hata_zamani=None, sonraki_deneme=None)


# ------------------------------------------------------------ tüm veriler

def tum_veri_dosyasi(gun: _dt.date) -> Path:
    return harita_excel.klasor() / f"{TUM_VERI_KOKU}_{gun.isoformat()}.xlsx"


def _tum_veri_temizle(klasor: Path, bugun: _dt.date) -> None:
    """`TUM_VERI_SAKLA_GUN` günden eski dökümleri siler; ad kalıbı
    tutmayan dosyaya dokunmaz (klasörde haritanın kendi dosyaları da var)."""
    sinir = bugun - _dt.timedelta(days=TUM_VERI_SAKLA_GUN)
    for p in klasor.iterdir():
        e = _TUM_VERI_AD.match(p.name)
        if not e:
            continue
        try:
            if _dt.date.fromisoformat(e.group(1)) < sinir:
                p.unlink()
        except (ValueError, OSError):
            pass


def _tum_veri_turu(simdi) -> None:
    if (simdi.hour, simdi.minute) < TUM_VERI_SAATI:
        return
    if _T.get("sonraki_deneme") and simdi < _T["sonraki_deneme"]:
        return
    yol = tum_veri_dosyasi(simdi.date())
    if yol.exists():
        return
    try:
        # Önce klasör: yazılamayacaksa döküm hiç kurulmasın (her denemede
        # bütün veritabanını okumak boşa olurdu).
        yol.parent.mkdir(parents=True, exist_ok=True)
        veri = excel.kitap(disari.tumu_sayfalari())
        harita_excel.atomik_yaz(yol, veri)
    except Exception as e:
        _hata("tum_veri", e)
        _T.update(hata=str(e), hata_zamani=simdi.isoformat(" ", "seconds"),
                  sonraki_deneme=simdi + _dt.timedelta(seconds=HATA_BEKLE_SN))
        return
    _HATALAR.pop("tum_veri", None)
    _T.update(hata=None, hata_zamani=None, sonraki_deneme=None)
    _gunluk.info("TUM VERI: %s yazildi (%.1f MB).", yol, len(veri) / 1024 / 1024)
    try:
        _tum_veri_temizle(yol.parent, simdi.date())
    except OSError:
        pass


def _son_tum_veri():
    """Klasördeki en yeni döküm: (gün, dosya adı, değişme zamanı) ya da None."""
    adlar = []
    try:
        for p in harita_excel.klasor().iterdir():
            e = _TUM_VERI_AD.match(p.name)
            if e:
                adlar.append((e.group(1), p))
    except OSError:
        return None
    if not adlar:
        return None
    gun, p = max(adlar)
    try:
        zaman = _dt.datetime.fromtimestamp(p.stat().st_mtime).isoformat(" ", "seconds")
    except OSError:
        zaman = None
    return {"gun": gun, "ad": p.name, "zaman": zaman}


# ------------------------------------------------------------ ekran

def durum() -> dict:
    """Yedekleme, Yönetici ve Cryo Haritası kartları için. Hiçbir şey yazmaz.

    Yedeğin durumu bellekten (iş parçacığı dakikada bir tazeliyor): ekran
    takılı olmayan bir diske ya da yavaş bir ağ klasörüne hiç sormasın.
    "Tüm veriler"inki Cryo haritası klasöründen (haritanın kartı zaten oraya
    bakıyor)."""
    imza = harita_excel.guncel_imza()
    y = {"bakildi": "engel" in _Y, "engel": _Y.get("engel"), "yol": _Y.get("yol"),
         "hata": _Y.get("hata"), "hata_zamani": _Y.get("hata_zamani"),
         "bekliyor": bool(_Y.get("bekliyor")),
         "son": _Y.get("son"), "dosya": _Y.get("dosya"),
         "yedekli": bool(imza) and _Y.get("yedeklenen") == imza,
         "calisiyor": bool(_IS is not None and _IS.is_alive()),
         "tekrar_dk": HATA_BEKLE_SN // 60}
    # Sıradaki yazım: bugünkü yazıldıysa yarın, değilse bugün (saat geçtiyse
    # bir dakika içinde).
    t = {"saat": "%02d:%02d" % TUM_VERI_SAATI, "klasor": str(harita_excel.klasor()),
         "gun": TUM_VERI_SAKLA_GUN, "hata": _T.get("hata"),
         "hata_zamani": _T.get("hata_zamani"), "son": _son_tum_veri(),
         "yarin": tum_veri_dosyasi(_simdi().date()).exists()}
    return {"yedek": y, "tum_veri": t}


# ------------------------------------------------------------ arka plan

def _dongu(damga) -> None:
    if _DURDUR.wait(ILK_BEKLEME_SN):
        return
    while True:
        simdi = _simdi()
        # İlk kurulum ekranında veritabanı yok: hiçbir şeye dokunma
        # (`sqlite3.connect` boş bir lab.db yaratırdı).
        if db.DB_YOLU.exists():
            for ad, is_ in (("yedek", lambda: _cryo_turu(simdi, damga)),
                            ("tum_veri", lambda: _tum_veri_turu(simdi))):
                try:
                    is_()
                except Exception as e:      # hiçbir hata programı durdurmasın
                    _hata(ad, e)
        if _DURDUR.wait(KONTROL_SN):
            return


def baslat(damga) -> None:
    """Arka plandaki iş parçacığını başlatır (programın açılışında, göçlerden
    ve haritanın iş parçacığından sonra). `damga`: veritabanının damgasını
    veren işlev (harita kurulamıyorsa değişikliği o söylüyor). Zaten
    çalışıyorsa bir şey yapmaz."""
    global _IS
    if _IS is not None and _IS.is_alive():
        return
    _DURDUR.clear()
    _IS = threading.Thread(target=_dongu, args=(damga,), name="oto-yedek",
                           daemon=True)
    _IS.start()


def durdur() -> None:
    _DURDUR.set()
