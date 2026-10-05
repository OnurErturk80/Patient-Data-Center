"""Otomatik yedek ve her gün 14:00'te "Tüm veriler" (v6.216; düzeni v6.248).

Kullanıcının istekleri: "Cryo haritada yapılan her değişiklikten sonra
yedekleme yapsın. Yönetici kısmındaki tüm verileri excele aktar'da her gün
14:00'da cryo haritanın yedeklendiği dosyaya aktarsın." (2026-09-29) ve
"Bütün otomatik yedeklemeleri düzenle. Yani ne ne zaman ve nereye kayıt
oluyor? Biraz karmaşa var düzenleyelim." (2026-10-05).

Program açıkken arka plandaki bir iş parçacığı dakikada bir üç işe bakar.
Üçü de bu bilgisayarın yedek klasörüne yazar (Klasörler ekranı; klasörün
düzeni `yedek.py`'nin belgesinde):

1. **Cryo Haritası değişince yedek** -> `veritabani/`. Harita her
   kurulduğunda içeriğinin bir imzası var (`harita_excel.guncel_imza()`:
   dolu tüpler, Excel kayıtları, yerler, straw'ların yazıları). İmza
   yedeklenen son halinkinden farklıysa yedek alınır -- "Şimdi
   yedekle"nin aynısı (`yedek.yedekle()`: veritabanı, arşivdeki yeni
   fotoğraflar, haritanın Excel'i).
   - **Değişiklikler bitince**: harita bir tur (bir dakika) değişmeden
     kalınca; değişiklik sürüp gidiyorsa ilk değişiklikten en geç
     `EN_GEC_SN` sonra. Bir hastanın dört straw'ı arka arkaya dondurulunca
     dört değil bir yedek.
   - **Yedeklenen imza klasörün durum dosyasında** (`yedek.durum_oku()`):
     program yeniden açılınca değişmemiş harita için yedek alınmaz; program
     kapalıyken değişmişse (terminal aracı, USB ile gelen veritabanı)
     alınır. Başka bir klasör ya da disk kendi dosyasıyla sayılır.
   - Harita kurulamıyorsa (bir hata) veritabanının damgasına bakılır:
     yedek, haritanın hatası yüzünden durmasın.
2. **Her gün 14:00'te yedek** (v6.248) -> `veritabani/`: klasördeki son
   yedek en son geçen 14:00'ten eskiyse (`son_gecen_saat()`) -- 14:00'te
   program kapalıysa açılınca. v6.247'ye kadar Cryo Haritası'nın
   değişmediği günlerde (yalnızca OPU, ICSI, döllenme) hiç yedek
   alınmıyordu; günlük yedek için söylenen Görev Zamanlayıcı da
   kurulmamıştı. Aynı saatte Cryo değişikliğiyle alınmış bir yedek varsa
   ikincisi alınmaz.
3. **Her gün 14:00'te "Tüm veriler"** -> `tum_veriler/`: yönetici
   panelindeki "Tüm veriyi Excel'e aktar"ın dosyası (aynı içerik,
   `disari.tumu_sayfalari()`), `Tum_Veriler_YYYY-AA-GG.xlsx`, son
   `yedek.EXCEL_SAKLA_GUN` gün. v6.247'ye kadar bilgisayarın kendi
   diskindeki Cryo haritası klasörüne yazılıyordu; kullanıcının sözü
   "cryo haritanın yedeklendiği" yerdi, Cryo Haritası'nın yedeği de bu
   klasörde (`cryo_harita/`). Bugünün dosyası varsa yazılmaz; 14:00'te
   program kapalıysa o gün açıldığında yazılır, kaçan günün dosyası
   sonradan yazılmaz (o günün hali yok). **Dosya bütün hasta kayıtlarını
   taşıyor** (indirilen dosyanın aynısı); yedek klasöründe veritabanının
   kendisi de var.

**Yedek klasörü yoksa üçü de bekler** (disk takılı değil), gelince yapılır.
Klasör kendiliğinden OLUŞTURULMAZ (`yedek.hedef_durumu()`); ilk yedeği
"Şimdi yedekle" açar (o klasörü oluşturuyor). Program açılınca eski düzenin
dosyaları yerine taşınır (`yedek.eski_duzeni_tasi()`).

**Ekranın bilgisi bellekten** (`durum()`): iş parçacığı her turda klasörü
okuyor (son yedek, nedeni, yedeklenen imza, son "Tüm veriler"); sayfa
açılırken takılı olmayan bir diske ya da yavaş bir ağ klasörüne sorulmuyor.
Başka bir süreçte alınan yedek (terminalden `yedek.py`) de bir tur sonra
görünüyor.

Hiçbir hata programı durdurmaz: günlüğe (`program.log`, bir kez), ekrana
(Yedekleme ekranı, Yönetici paneli, Cryo Haritası kartı) yazılır,
`HATA_BEKLE_SN` sonra yeniden denenir. `print` yok (CLAUDE.md). Veritabanı
yokken (ilk kurulum ekranı) hiçbir şeye dokunmaz.
"""

import datetime as _dt
import logging
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

_DURDUR = threading.Event()
_IS = None
# Bellekte; her turda klasörden tazeleniyor (yukarıdaki belge).
_Y = {}          # yedek: klasör, son yedek, yedeklenen imza, bekleyen değişiklik, hata
_T = {}          # Tüm veriler
_HATALAR = {}    # iş -> günlüğe son yazılan hata (tekrar tekrar yazılmasın)
_TASINDI = set()  # bu açılışta eski düzeni yerine taşınmış klasörler


def _simdi():
    return _dt.datetime.now()


def _iso(t):
    return t.isoformat(" ", "seconds") if t else None


def _hata(is_adi, e) -> None:
    """Hatayı günlüğe bir kez yazar (aynı hata her turda yazılmasın).
    `except` bloğunun içinden çağrılır."""
    if _HATALAR.get(is_adi) != repr(e):
        # Disk / klasör hatası (takılı değil, dolu, izin) tek satır; başka bir
        # hata programın kusuru olabilir, ayrıntısıyla.
        _gunluk.error("OTO YEDEK: %s basarisiz: %s", is_adi, e,
                      exc_info=not isinstance(e, OSError))
    _HATALAR[is_adi] = repr(e)


def hedef():
    """Bu bilgisayarın yedek klasörü kullanılabilir mi -> (yol, engel);
    `yedek.hedef_durumu()`."""
    return yedek.hedef_durumu()


def son_gecen_saat(simdi):
    """En son geçen 14:00 (`yedek.GUNLUK_SAAT`): bugün o saat geçtiyse
    bugünkü, geçmediyse dünkü."""
    saat, dakika = yedek.GUNLUK_SAAT
    esik = simdi.replace(hour=saat, minute=dakika, second=0, microsecond=0)
    return esik if simdi >= esik else esik - _dt.timedelta(days=1)


def tum_veri_dosyasi(klasor, gun: _dt.date) -> Path:
    return (Path(klasor) / yedek.TUM_VERILER
            / yedek.gunluk_ad(yedek.TUM_VERI_KOKU, gun))


def _klasoru_oku(klasor) -> None:
    """Klasörün bugünkü hali belleğe: son yedek (dosya adından), nedeni ve
    yedeklenen haritanın imzası (durum dosyasından), son "Tüm veriler".
    Her turda: başka bir süreçte alınan ya da elle silinen yedek de
    görünsün."""
    klasor = Path(klasor)
    if _Y.get("klasor") != str(klasor):        # başka klasör / disk
        _Y.pop("son_imza", None)
    d = yedek.durum_oku(klasor)
    s = yedek.son_yedek(klasor)
    # Nedeni yalnızca durum dosyası bu yedeği anlatıyorsa (terminalden eski
    # bir sürümle alınmış yedeği anlatmaz) ve bilinen bir kodsa: ekrana
    # `metin()` anahtarı olarak gidiyor (tuzak #9).
    neden = d.get("neden") if s and d.get("dosya") == s["dosya"] else None
    _Y.update(klasor=str(klasor), yedeklenen=d.get("imza"),
              son=s["zaman"] if s else None, dosya=s["dosya"] if s else None,
              neden=neden if neden in yedek.NEDENLER else None)
    _T["son"] = yedek.son_gunluk(klasor / yedek.TUM_VERILER, yedek.TUM_VERI_KOKU)


# ------------------------------------------------------------ yedek

def yedekle(klasor, kaynak: str, imza=None, otomatik: bool = False,
            neden: str = "elle", esik=None):
    """`yedek.yedekle()` + bellekteki durum. "Şimdi yedekle" de bunu
    çağırıyor: elle alınan yedekten sonra aynı harita için bir daha
    otomatik yedek alınmasın.

    `imza`: yedeklenen haritanın imzası (verilmezse şu anki). Kilit
    alındıktan sonra o arada başka bir yedeğin aynı işi yapıp yapmadığına
    yeniden bakılıyor -- yaptıysa ikinci kez alınmıyor (None döner):
    `otomatik` ise klasörün durum dosyasındaki imza, `esik` verilmişse
    (günlük yedek) o andan sonra alınmış bir yedek. Hata yükselir.
    -> yazılan veritabanı kopyasının yolu.
    """
    if imza is None:
        imza = harita_excel.guncel_imza()
    with yedek.KILIT:
        if otomatik and imza and yedek.durum_oku(klasor).get("imza") == imza:
            _klasoru_oku(klasor)
            return None
        if esik is not None:
            s = yedek.son_yedek(klasor)
            if s and s["zaman"] >= esik:
                _klasoru_oku(klasor)
                return None
        yol = yedek.yedekle(Path(klasor), kaynak, imza=imza, neden=neden)
        _klasoru_oku(klasor)
        # Durum dosyası yazılamadıysa da bu açılışta aynı hal için yeniden
        # yedek alınmasın (her turda bir yedek olurdu).
        _Y["son_imza"] = imza
        return yol


def _yedek_al(klasor, simdi, neden, kaynak, imza, otomatik=False, esik=None) -> None:
    if _Y.get("sonraki_deneme") and simdi < _Y["sonraki_deneme"]:
        return
    try:
        yedekle(klasor, kaynak, imza=imza, otomatik=otomatik, neden=neden, esik=esik)
    except Exception as e:
        _hata("yedek", e)
        _Y.update(hata=str(e), hata_zamani=_iso(simdi),
                  sonraki_deneme=simdi + _dt.timedelta(seconds=HATA_BEKLE_SN))
        return
    _HATALAR.pop("yedek", None)
    _Y.update(bekliyor=None, hata=None, hata_zamani=None, sonraki_deneme=None)


def _cryo_turu(simdi, damga, klasor) -> None:
    imza = harita_excel.guncel_imza()
    if imza is None:
        if not harita_excel.kurulamadi():
            return                          # harita henüz kurulmadı
        imza = "damga:" + str(damga())
    if imza in (_Y.get("yedeklenen"), _Y.get("son_imza")):
        _Y.update(bekliyor=None, onceki=imza)
        return
    if not _Y.get("bekliyor"):
        _Y["bekliyor"] = simdi
    sakin = imza == _Y.get("onceki")
    _Y["onceki"] = imza
    if not sakin and (simdi - _Y["bekliyor"]).total_seconds() < EN_GEC_SN:
        return                              # değişiklik sürüyor
    _yedek_al(klasor, simdi, "cryo", "Cryo Haritasi degisti", imza, otomatik=True)


def _gunluk_turu(simdi, klasor) -> None:
    esik = son_gecen_saat(simdi)
    if _Y.get("son") is not None and _Y["son"] >= esik:
        return
    # Haritanın imzası da yazılsın: hemen ardından aynı hal için Cryo
    # yedeği alınmasın.
    _yedek_al(klasor, simdi, "gunluk", "Her gun %02d:%02d" % yedek.GUNLUK_SAAT,
              harita_excel.guncel_imza(), esik=esik)


# ------------------------------------------------------------ tüm veriler

def _tum_veri_turu(simdi, klasor) -> None:
    if (simdi.hour, simdi.minute) < yedek.GUNLUK_SAAT:
        return
    if _T.get("sonraki_deneme") and simdi < _T["sonraki_deneme"]:
        return
    yol = tum_veri_dosyasi(klasor, simdi.date())
    if yol.exists():
        return
    try:
        # Önce klasör: yazılamayacaksa döküm hiç kurulmasın (her denemede
        # bütün veritabanını okumak boşa olurdu). Yedek klasörü var (engel
        # yok), içindeki alt klasörü açmak güvenli.
        yol.parent.mkdir(exist_ok=True)
        veri = excel.kitap(disari.tumu_sayfalari())
        harita_excel.atomik_yaz(yol, veri)
    except Exception as e:
        _hata("tum_veri", e)
        _T.update(hata=str(e), hata_zamani=_iso(simdi),
                  sonraki_deneme=simdi + _dt.timedelta(seconds=HATA_BEKLE_SN))
        return
    _HATALAR.pop("tum_veri", None)
    _T.update(hata=None, hata_zamani=None, sonraki_deneme=None,
              son={"gun": simdi.date(), "dosya": yol.name})
    _gunluk.info("TUM VERI: %s yazildi (%.1f MB).", yol, len(veri) / 1024 / 1024)
    yedek.gunlukleri_temizle(yol.parent, yedek.TUM_VERI_KOKU, simdi.date())


# ------------------------------------------------------------ ekran

def durum() -> dict:
    """Yedekleme ekranı, Yönetici paneli, Cryo Haritası kartı ve "son yedek
    eski" uyarısı için. Hiçbir şey yazmaz, yedek klasörüne sormaz (bellekten,
    yukarıdaki belge)."""
    simdi = _simdi()
    imza = harita_excel.guncel_imza()
    son = _Y.get("son")
    engel = _Y.get("engel")
    saat = "%02d:%02d" % yedek.GUNLUK_SAAT
    # Sıradaki günlük yedek: son yedek en son geçen 14:00'ten eskiyse
    # birazdan (`_gunluk_turu()`), değilse bugün ya da yarın 14:00'te.
    esik = son_gecen_saat(simdi)
    if son is None or son < esik:
        sonraki = "simdi"
    else:
        sonraki = "yarin" if esik.date() == simdi.date() else "bugun"
    y = {"bakildi": bool(_Y.get("bakildi")), "engel": engel, "yol": _Y.get("yol"),
         "hata": _Y.get("hata"), "hata_zamani": _Y.get("hata_zamani"),
         "bekliyor": bool(_Y.get("bekliyor")),
         "son": _iso(son), "dosya": _Y.get("dosya"), "neden": _Y.get("neden"),
         "gun_once": (simdi - son).days if son else None, "sonraki": sonraki,
         "yedekli": bool(imza) and imza in (_Y.get("yedeklenen"), _Y.get("son_imza")),
         "calisiyor": bool(_IS is not None and _IS.is_alive()),
         "tekrar_dk": HATA_BEKLE_SN // 60, "saat": saat}
    ts = _T.get("son")
    t = {"saat": saat, "gun": yedek.EXCEL_SAKLA_GUN, "engel": engel,
         "hata": _T.get("hata"), "hata_zamani": _T.get("hata_zamani"),
         "son": ({"gun": ts["gun"].isoformat(), "dosya": ts["dosya"]} if ts else None),
         "bugun": bool(ts) and ts["gun"] == simdi.date()}
    return {"yedek": y, "tum_veri": t}


# ------------------------------------------------------------ arka plan

def _tur(simdi, damga) -> None:
    yol, engel = hedef()
    if engel and _Y.get("klasor") and _Y["klasor"] != (str(Path(yol)) if yol else None):
        # Klasör ayarı değişti, yenisine ulaşılamıyor: eski klasörün son
        # yedeği "son yedek" diye görünmesin. Aynı klasörse (disk çekildi)
        # bilinen son yedek kalır -- uyarının ölçüsü o.
        for a in ("klasor", "son", "dosya", "neden", "yedeklenen", "son_imza"):
            _Y.pop(a, None)
        _T.pop("son", None)
    _Y.update(engel=engel, yol=str(yol) if yol else None, bakildi=True)
    if engel:
        return
    if str(yol) not in _TASINDI:      # açılışta ya da başka klasör / disk
        _TASINDI.add(str(yol))
        try:
            yedek.eski_duzeni_tasi(yol)
        except Exception as e:          # yedekler dursun diye değil: her yedek yeniden dener
            _hata("tasima", e)
    _klasoru_oku(yol)
    for ad, is_ in (("yedek", lambda: _cryo_turu(simdi, damga, yol)),
                    ("yedek", lambda: _gunluk_turu(simdi, yol)),
                    ("tum_veri", lambda: _tum_veri_turu(simdi, yol))):
        try:
            is_()
        except Exception as e:          # hiçbir hata programı durdurmasın
            _hata(ad, e)


def _dongu(damga) -> None:
    if _DURDUR.wait(ILK_BEKLEME_SN):
        return
    while True:
        # İlk kurulum ekranında veritabanı yok: hiçbir şeye dokunma
        # (`sqlite3.connect` boş bir lab.db yaratırdı).
        if db.DB_YOLU.exists():
            try:
                _tur(_simdi(), damga)
            except Exception as e:      # hiçbir hata programı durdurmasın
                _hata("yedek", e)
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
