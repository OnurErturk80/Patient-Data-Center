"""IVF Laboratuvar Kayıt Modülü — hasta ve cycle ekranları, giriş ve düzenleme."""

import contextlib
import contextvars
import logging
import json
import os
import socket
import sqlite3
import threading
import time
from pathlib import Path

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import db
import disari
import excel
import form_kalip
import formlar
import goc
import guvenlik
import karekod
import metinler
import xlsx_oku

KOK = db.PROGRAM_KOK          # kod: static/, templates/

# ------------------------------------------------------- açılışta göçler
#
# Göçler eskiden elle çalıştırılıyordu (`python goc_hepsi.py`). Hiçbir klinik
# bunu yapmaz; kurulum dosyasına geçerken bu adımın kalkması şart (v6.49).
# Aynı zamanda tuzak #3'ün ("göç yazdıysan kullanıcının çalıştırdığını
# varsayma") kalıcı çözümü.
#
# Göç patlarsa program **yine açılıyor**: sebebi terminale ve `/yonetim`
# paneline yazılıyor, ekranlar çalışmaya devam ediyor. Açılmayan bir program
# teşhis edilemez.

# Servis olarak çalışırken konsol yok: `print` tamponda kalıp kayboluyor.
# `baslat.py` bu günlüğü hem konsola hem veri klasöründeki dosyaya
# bağlıyor -- bir şey ters giderse bakılacak tek yer orası.
_gunluk = logging.getLogger("program")

GOC_SONUCU = {}


@contextlib.asynccontextmanager
async def _yasam(app):
    global GOC_SONUCU
    try:
        GOC_SONUCU = goc.calistir()
    except Exception as e:                 # beklenmedik bir şey olsa da aç
        GOC_SONUCU = {"calisti": [], "hatali": [("baslangic", repr(e))],
                      "bekleyen": [], "elle": [], "atlandi": ""}
    _goc_ozeti(GOC_SONUCU)
    yield


def _goc_ozeti(s):
    """Terminale tek satırlık özet; hata varsa ayrıntısıyla."""
    if s.get("atlandi") == "veritabani-yok":
        _gunluk.info("GOC: veritabani yok, gocler atlandi.")
        return
    if s.get("atlandi") == "baska-surec":
        _gunluk.info("GOC: baska bir surec gocleri calistiriyor, atlandi.")
        return
    if s.get("calisti"):
        _gunluk.info("GOC: %d goc uygulandi (%s%s).", len(s["calisti"]),
                     ", ".join(s["calisti"][:4]),
                     "..." if len(s["calisti"]) > 4 else "")
    for ad, mesaj in s.get("hatali", []):
        _gunluk.error("GOC HATASI: %s\n  %s", ad,
                      "\n  ".join(str(mesaj).splitlines()[-6:]))
    for ad in s.get("elle", []):
        _gunluk.warning("GOC: %s soru soruyor, elle calistirilmali: "
                        "python %s.py", ad, ad)


uygulama = FastAPI(title="Patient Data Center", lifespan=_yasam)
uygulama.mount("/static", StaticFiles(directory=KOK / "static"), name="static")
sablon = Jinja2Templates(directory=KOK / "templates")

ACIK_YOLLAR = {"/giris", "/sifremi-unuttum", "/sifre",
                "/manifest.json", "/ekle"}

# Başlıklarda kullanılan kısa tedavi tipi gösterimi
TIP_KODLARI = ("ivf_icsi", "fet", "fet_kultur", "oosit_cryo", "yumurta_cozme", "taze")   # taze: eski kod

# Bu tiplerde dondurulan örnek (embriyo ya da oosit) BAŞKA bir cycle'dan
# gelir (OPU bu cycle'da olmaz) -- taşıyıcı/örnek listeleri specimen.cycle_id
# ile değil, çözüldüğü tedaviyi tutan thaw_cycle_id ile aranır (v6.62,
# goc_031). "fet" doğrudan transfer ediyor, "fet_kultur" araya gün 5'e kadar
# kültür + blastokist değerlendirmesi koyuyor. "yumurta_cozme" (v6.102,
# goc_039) yalnızca çözme aşamasından oluşuyor -- oosit_cryo'da dondurulmuş
# bir yumurtanın AYRI bir tedavide çözülmesi, FET'in embriyo için yaptığının
# aynısı. Üçünde de dondurulan örneğin kendi cycle'ı bu cycle DEĞİL.
#
# Liste `db.py`'de duruyor: `disari.py`'nin istatistik sorgusu da aynı ayrımı
# soruyor ve `app`'i import edemiyor. Buradaki ad kalsın -- 20'ye yakın yer
# bunu kullanıyor.
FET_TIPLERI = db.FET_TIPLERI


def tip_kisa(kod):
    """Tedavi tipinin ekranda görünen kısa adı, geçerli dilde."""
    return metinler.t("tip_" + kod) if kod in TIP_KODLARI else (kod or "")


def fet_tipi_mi(cycle_tipi) -> bool:
    """Bu cycle'da embriyo başka bir cycle'dan mı geliyor (OPU yok)."""
    return cycle_tipi in FET_TIPLERI


def asama_adi(kod):
    """Aşamanın ekranda görünen adı, geçerli dilde.

    `ASAMA_SIRASI`'ndaki Türkçe ad kimlik olarak duruyor; ekrana giden ad
    buradan geçiyor, böylece 11 aşama tek noktadan çevriliyor.
    """
    return metinler.t("asama_" + kod)


sablon.env.globals["tip_kisa"] = tip_kisa
sablon.env.globals["fet_tipi_mi"] = fet_tipi_mi
sablon.env.globals["asama_adi"] = asama_adi


def ay_adi(yil, ay) -> str:
    """"Eylül 2026" -- ay adı geçerli dilde (v6.29).

    `strftime("%B")` kullanılmıyor: o işletim sisteminin yerel ayarına bağlı,
    Windows mini PC'de İngilizce çıkabilir. Ay adları `metinler.py`'de.
    """
    return f"{metinler.t('ay_' + str(int(ay)))} {int(yil)}"


sablon.env.globals["ay_adi"] = ay_adi


def takvim_basligi(tarih: str) -> str:
    """'2026-09-14' -> '14 Eylül 2026 Pazartesi' (v6.33).

    Gün adı da ay adı gibi `metinler.py`'de: `strftime("%A")` işletim
    sisteminin yerel ayarına bağlı, Windows mini PC'de İngilizce çıkar.
    """
    try:
        g = _dt.fromisoformat(str(tarih)[:10]).date()
    except (ValueError, TypeError):
        return str(tarih or "")
    return (f"{g.day} {metinler.t('ay_' + str(g.month))} {g.year} "
            f"{metinler.t('gun_' + str(g.isoweekday()))}")


sablon.env.globals["takvim_basligi"] = takvim_basligi


def gg_aa_yyyy(tarih) -> str:
    """'1990-05-12' -> '12.05.1990' (v6.64).

    Doğum tarihi gibi salt gösterim alanları veritabanında ISO (`YYYY-MM-DD`)
    duruyor -- kaydetme, arama ve sıralama ISO'ya güveniyor, o değişmiyor.
    Yalnızca ekrana **gün.ay.yıl** sırasıyla basılıyor (kullanıcının isteği).
    Bozuk/boş değerde olduğu gibi döner — sessizce boş basmak yerine hatayı
    görünür bırakır.
    """
    try:
        g = _dt.fromisoformat(str(tarih)[:10]).date()
    except (ValueError, TypeError):
        return str(tarih or "")
    return g.strftime("%d.%m.%Y")


sablon.env.globals["gg_aa_yyyy"] = gg_aa_yyyy


def gg_aa_yyyy_saat(zaman) -> str:
    """'2026-09-16 08:23:11' -> '16.09.2026 08:23' (v6.67).

    `gg_aa_yyyy()` ile aynı gerekçe, saat de taşıyan kayıt zamanları için
    (işlem geçmişi, şifre isteği, taşıyıcı). Saniye basılmıyor -- dakika
    kullanıcı için yeterli, saniye gösterimi kalabalık ediyor.
    """
    try:
        z = _dt.fromisoformat(str(zaman)[:19])
    except (ValueError, TypeError):
        return str(zaman or "")
    return z.strftime("%d.%m.%Y %H:%M")


sablon.env.globals["gg_aa_yyyy_saat"] = gg_aa_yyyy_saat


def tedavi_yasi(dogum_tarihi, tarih):
    """Hastanın, verilen tedavi tarihinin YILINDA kaç yaşında olduğu.

    Tam yaş değil, yalnızca yıl farkı (`tedavi_yili - dogum_yili`) — ay/gün
    karşılaştırması gerektirseydi doğum günü öncesi/sonrasına göre aynı yıl
    içinde iki farklı sayı çıkardı; kullanıcının sorduğu "o yıl kaçındaydı"
    sorusu bu değil. Tarihlerden biri boşsa ya da okunamıyorsa `None` döner,
    şablon hiçbir şey basmaz.
    """
    if not dogum_tarihi or not tarih:
        return None
    try:
        dogum_yili = _dt.fromisoformat(str(dogum_tarihi)[:10]).year
        tedavi_yili = _dt.fromisoformat(str(tarih)[:10]).year
    except (ValueError, TypeError):
        return None
    return tedavi_yili - dogum_yili


sablon.env.globals["tedavi_yasi"] = tedavi_yasi


def statik_surum() -> str:
    """`style.css`'in son değişim zamanı -- tarayıcı önbelleğini kırmak için (v6.69).

    Dosya adı hep aynı olduğu için tarayıcı sürüm farkını göremiyor, program
    güncellendikten sonra da eski CSS'i göstermeye devam edebiliyor (gerçekten
    başa geldi: kullanıcı v6.68'i çalıştırıyordu ama üç sütun hâlâ eski
    tek-sütun CSS'iyle basılıyordu). Bağlantıya `?v=<mtime>` eklemek her
    değişiklikte adresi değiştirip önbelleği kendiliğinden geçersiz kılıyor --
    kullanıcıdan "sert yenile" istemeye gerek kalmıyor.
    """
    try:
        return str(int((KOK / "static" / "style.css").stat().st_mtime))
    except OSError:
        return "0"


sablon.env.globals["statik_surum"] = statik_surum


def _islem_yapan_ad(cycle_id, asama):
    """Bir cycle aşamasını fiilen yapan kişinin adı (yoksa boş).

    Şablondan `islem_yapan_ad(c.id, "denudasyon")` diye çağrılır; `_islem_yapan`
    kutusu her aşama ekranının altında bunu gösterir.
    """
    r = db.tek("SELECT yapan_ad FROM islem_yapan WHERE cycle_id = ? AND asama = ?",
               (cycle_id, asama))
    return r["yapan_ad"] if r and r["yapan_ad"] else ""


sablon.env.globals["islem_yapan_ad"] = _islem_yapan_ad


def _guncel_kullanici_ad():
    """Şu an giriş yapmış kullanıcının adı (varsa) — şifresiyle giren kişi.

    `_islem_yapan` kutusunun seçicisinde varsayılan seçim için: aşama henüz
    kaydedilmemişse kutu boş durmasın, giriş yapan kişi zaten önceden
    seçili gelsin (v6.99, kullanıcının isteği) — ama değiştirilebilir,
    "Kaydet" hâlâ elle onay ister, otomatik yazmıyor.
    """
    k = _GIRIS_KULLANICI.get()
    return k["ad_soyad"] if k else ""


sablon.env.globals["guncel_kullanici_ad"] = _guncel_kullanici_ad


def _personel_listesi():
    """Şifresi olan (aktif hesabı olan) personelin adları, alfabetik.

    `_islem_yapan` kutusundaki seçiciyi dolduruyor — "işlemi yapan" artık
    serbest metinle yazılmıyor, bu listeden seçiliyor (v6.99).
    """
    return [r["ad_soyad"] for r in db.sorgu(
        "SELECT ad_soyad FROM kullanici WHERE lab_id=? AND aktif_mi=1 "
        "ORDER BY ad_soyad", (db.LAB_ID,))]


sablon.env.globals["personel_listesi"] = _personel_listesi

# Sperm dondurma sebebi — öneri menüsü (v6.101, kullanıcının verdiği liste).
# `sperm_dondurma.sebep` hâlâ serbest metin (v6.86'dan beri bilerek açık,
# kategoriler kesinleşmedi) — bu yalnızca `<datalist>` önerisi, kapalı bir
# liste değil, listede olmayan bir sebep de yazılabilir. Tek yerde dursun
# diye Jinja global: iki form da (`sperm_dondurma_form.html`,
# `sperm_dondurma_yeni_hasta.html`) aynısını kullanıyor.
SPERM_DONDURMA_SEBEPLERI = (
    "Tedavi Öncesi Koruma", "Onkolojik", "TESE", "TESA", "PESA",
)
sablon.env.globals["sperm_dondurma_sebepleri"] = lambda: SPERM_DONDURMA_SEBEPLERI


# ------------------------------------------------------- örnek kodu ve aşama adı

# Aşamaya göre örneğin o anki adı. Oosit → zigot → embriyo aynı örnektir
# (specimen.id değişmez); değişen sadece ekranda yazan isim.
# None olanlar cycle tipine göre belirlenir: oosit cryo'da donan bir oosittir.
# Aşama -> örnek adının sözlük anahtarı. Ad doğrudan yazılmıyor ki dil
# değişince ekrandaki isim de değişsin. None: cycle tipine göre belirlenir.
ASAMA_ORNEK_ADI = {
    "androloji": "ornek_ad",
    "denudasyon": "oosit_ad",
    "icsi": "oosit_ad",
    "fert": "zigot_ad",
    "cleavage": "cleavage_ad",
    "blast": "blastokist_ad",
    "vitrifikasyon": None,
    "thaw": None,
    "transfer": None,
    "gebelik": None,
}


def _yumurta_mi(cycle_tipi, asama=None) -> bool:
    """Bu tedavide dondurulan/çözülen örnek yumurta mı, embriyo mu?

    Tek yerde duruyor çünkü iki soruyu birden yanıtlıyor: aşama ekranında
    örneğe ne deneceği (`ornek_adi()`) ve taşıyıcının içinde ne olduğu
    (`icerik_sayisi()`, v6.133). Yalnızca `oosit_cryo`'da yumurta dondurulur
    — `ivf_icsi`'nin vitrifikasyon ekranı zaten enjekte edilmiş (embriyo
    olmuş) örnekleri listeliyor (`_ICSI_YAPILMADI` süzgeci). Yumurta
    donduran yeni bir cycle tipi eklersen burayı genişlet, ikisi birden
    doğru olur. Yumurta Çözme'de cevap aşamaya bağlı (v6.147): çözülen
    yumurta, ICSI'den sonra dondurulan/transfer edilen embriyo.

    **Kararın kendisi v6.135'ten beri `db.py`'de** — `formlar.py` de aynı
    soruyu soruyor (resmî formda "2 embriyo" mu "12 yumurta" mı donduruldu)
    ve `app`'i import edemez, `FET_TIPLERI`'nin aynı gerekçesi.
    """
    return db.yumurta_mi(cycle_tipi, asama)


def _ornek_adi(asama, cycle_tipi=None):
    """Bu aşamada örneğe ne deniyor: Oosit / Zigot / Cleavage / Blastokist / Embriyo."""
    anahtar = ASAMA_ORNEK_ADI.get(asama, "ornek_ad")
    if anahtar is None:
        anahtar = "oosit_ad" if _yumurta_mi(cycle_tipi, asama) else "embriyo_ad"
    return metinler.t(anahtar)


def _icerik_sayisi(adet, cycle_tipi=None, icerik=None):
    """Taşıyıcının içindekiler: "4 yumurta" / "4 embriyo" (v6.133).

    Kullanıcının isteği: "Yumurta donduruluyorsa Yumurta, Embriyo
    donduruluyorsa Embriyo yazsın." Daha önce her taşıyıcı "n embriyo"
    diyordu; yumurta dondurma kaydı programa ilk kez v6.132'de girince
    ortaya çıktı.

    `icerik` ('yumurta'/'embriyo', `icerik_sql()`) verilirse o kazanır --
    bir tüpün içeriği için hep onu ver (v6.167): tipe bakan cevap, IVF/ICSI'de
    dondurulmuş aktarılmış yumurtaya "embriyo" der. `cycle_tipi` o tipte
    dondurulan şeyi soranlar için kalıyor.
    """
    yumurta = (icerik == "yumurta") if icerik else _yumurta_mi(cycle_tipi)
    return metinler.say("n_yumurta" if yumurta else "n_embriyo", adet)


def _ornek_kodu(specimen_id):
    """Örneğin tam kodu: `<hasta dosya no>-<cycle no>-<sıra>`.

    `specimen.id` zaten `<cycle no>-<sıra>`; başına hasta dosya numarası
    eklenir. Birincil anahtar değişmez — bu yalnızca gösterim ve dosya adı için.
    """
    if not specimen_id:
        return ""
    r = db.tek(
        "SELECT h.dosya_no FROM specimen s "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE s.id = ?", (specimen_id,))
    return f"{r['dosya_no']}-{specimen_id}" if r else str(specimen_id)


def _liste_etiket(liste_adi: str, kod):
    """Bir seçim listesi kodunun ekranda görünen etiketi.

    Bilgi kartları kaydedilmiş **kodu** gösterecek olsa "mii", "2pn" gibi
    ham değerler çıkardı. Listeler laba özgü ve düzenlenebilir (`liste_degeri`),
    o yüzden kod → etiket çevirisi sabit bir sözlükte değil, veritabanında.
    Bulunamayan kod kendi adıyla döner — sessizce boş kalmaz.
    """
    if not kod:
        return ""
    r = db.tek(
        "SELECT etiket FROM liste_degeri WHERE lab_id=? AND liste_adi=? AND kod=?",
        (db.LAB_ID, liste_adi, str(kod)))
    return r["etiket"] if r else str(kod)


sablon.env.globals["liste_etiket"] = _liste_etiket


# Numara şeridindeki kutucuk çok dar (v6.139): "Dejenere"/"Atretik" oraya
# sığmıyor, o yüzden yalnızca bu ikisinin kısaltması var. Ötekiler
# (MII/MI/GV) zaten kısa, kendi `liste_degeri` etiketiyle basılıyor --
# liste laba özgü ve yönetici düzenleyebiliyor (CLAUDE.md "kodu değil
# etiketi göster"), burada sabit bir sözlük yazmak onu bozardı.
_MAT_KISALTMALI = ("degenere", "atretik")


def _mat_kisa(kod):
    """Maturasyon kodunun dar kutucuğa sığan hâli: 'GV', 'MII', 'Dej.'."""
    if not kod:
        return ""
    if kod in _MAT_KISALTMALI:
        return metinler.t(f"mat_kisa_{kod}")
    return _liste_etiket("maturasyon", kod)


sablon.env.globals["mat_kisa"] = _mat_kisa
sablon.env.globals["ornek_adi"] = _ornek_adi
sablon.env.globals["yumurta_mi"] = _yumurta_mi
sablon.env.globals["icerik_sayisi"] = _icerik_sayisi
sablon.env.globals["cozme_tedavisi_mi"] = db.cozme_tedavisi_mi
sablon.env.globals["ornek_kodu"] = _ornek_kodu


def bos_ise_none(deger):
    """Boş form alanlarını NULL olarak kaydet, boş metin olarak değil."""
    if deger is None:
        return None
    deger = deger.strip()
    return deger if deger else None


def _dosya_no_sayi(deger):
    """Form alanından gelen dosya numarasını tamsayıya çevirir (v6.139).

    Eşin dosya numarası **serbest bir referans**: eş henüz kayıtlı olmayabilir
    (numara önce yazılır, kayıt sonra açılır), o yüzden "böyle bir hasta yok"
    diye reddedilmiyor -- yalnızca rakam olmayan bir şey yazılmışsa NULL'a
    düşüyor. "Kayıtlı mı" sorusunu her seferinde `dosya_no_sahibi()` yanıtlıyor
    (türetilmiş, saklanmıyor).
    """
    d = (deger or "").strip()
    return int(d) if d.isdigit() else None


def tr_buyuk(deger):
    """Türkçe büyük harfe çevirir — hasta/eş adları için (v6.115,
    kullanıcının isteği: "nasıl yazarsam yazayım sonunda büyük harflerle
    kaydolsun").

    Python'un `str.upper()`'ı Türkçe 'i' harfini yanlış çeviriyor ("Turkish
    I problem"): varsayılan Unicode kuralı küçük 'i'yi noktasız 'I' yapar,
    Türkçe kuralı noktalı 'İ' ister. Önce 'i'yi 'İ'ye çevirip SONRA
    `.upper()` çağırmak bunu düzeltiyor — 'ı' zaten doğru çevriliyor
    (Unicode'da 'ı'.upper() == 'I'), ç/ğ/ö/ş/ü'de sorun yok.
    """
    if deger is None:
        return None
    return deger.replace("i", "İ").upper()


class FormHatasi(Exception):
    """Kullanıcıya gösterilecek doğrulama hatası."""


def sayi(v, alan="Sayı"):
    """Ondalık sayı. Virgül de nokta gibi kabul edilir (2,1 = 2.1)."""
    v = (v or "").strip().replace(",", ".")
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        raise FormHatasi(f"{alan} alanına sayı yazılmalı. Girilen: {v}")


def tam(v, alan="Sayı"):
    v = (v or "").strip().replace(",", ".")
    if not v:
        return None
    try:
        return int(float(v))
    except ValueError:
        raise FormHatasi(f"{alan} alanına tam sayı yazılmalı. Girilen: {v}")


# Yılı bundan eskiyse yazım hatasıdır. Doğum tarihleri 1900'lerde olabildiği
# için sınır 2000 değil 1900. Üst sınır bu yıldan beş yıl sonrası:
# `planlanan_tarih` bilerek gelecekte olabiliyor ve bebeğin doğumu dokuz ay
# ileri, ama `9999` de `0026` kadar sessiz bir yazım hatası (v6.53).
EN_ESKI_YIL = 1900
EN_YENI_YIL_PAYI = 5


def yil_kontrol(v, alan="Tarih"):
    """Tarihin yılı makul mü? Değilse FormHatasi.

    `date` / `datetime-local` alanına yıl olarak "26" yazılırsa tarayıcı
    **26. yılı** gönderiyor: `0026-09-04`. Değer geçerli bir ISO tarihi
    olduğu için hiçbir katmanda patlamıyor, sessizce kaydediliyor — bir
    cycle'ın OPU tarihi aylarca böyle durdu (bekleyen iş 6). Ekranlarda
    `min` niteliği var ama asıl engel burası: tarayıcıya güvenilmez.

    Üst sınır da var (`9999-01-01` de sessiz bir yazım hatası) ama
    şablonlarda yalnızca `min` niteliği yazılı: `max` her yıl değişen bir
    değer olurdu, sabit yazılsa eskir. Üst sınırı sunucu tutuyor.

    Bulunmuş bozuk kayıtları `tarih_duzelt.py` sorarak düzeltiyor; o araç
    okunamayan biçimleri de (`04.09.2026`, `88-01-05`) buluyor.
    """
    if not v:
        return v
    # Sınır her çağrıda hesaplanıyor: yıl dönünce sabit kalmasın.
    en_yeni = _dt.now().year + EN_YENI_YIL_PAYI
    dort = str(v)[:4]
    if dort.isdigit() and not (EN_ESKI_YIL <= int(dort) <= en_yeni):
        raise FormHatasi(
            f"{alan} yılı hatalı: {v}. Yıl {EN_ESKI_YIL} ile {en_yeni} "
            f"arasında olmalı (örnek: {_dt.now().year}).")
    return v


def zaman(v, alan="Tarih"):
    """datetime-local alanı '2026-04-17T09:45' verir, veritabanı boşluk ister."""
    return yil_kontrol(bos_ise_none((v or "").replace("T", " ")), alan)


def islem_zamani(v):
    """Ekrandan gelen işlem saati. Boş veya geçersizse şu an.

    Yılı bozuk değer de "geçersiz" sayılıyor: aşama ekranlarının POST'unda
    hata gösterecek yer yok, bu yüzden tarih **reddedilip** şu ana düşülüyor.
    Kullanıcı kaydettikten sonra bilgi kartında yazan saati görüyor.
    """
    from datetime import datetime as _d
    try:
        t = zaman(v)
    except FormHatasi:
        return _d.now().isoformat(" ", "seconds")
    if not t:
        return _d.now().isoformat(" ", "seconds")
    try:
        _d.fromisoformat(t)
    except ValueError:
        return _d.now().isoformat(" ", "seconds")
    return t if len(t) > 16 else t + ":00"


# ----------------------------------------------------------------- lab kayıt no

import re
from datetime import datetime as _dt


_ayar = db.ayar         # yerel_ayar.json önceliklidir


def sonraki_lab_no() -> str:
    """Bir sonraki lab kayıt numarasını üretir.

    Boşluk doldurma açıksa, silinen bir kaydın numarası yeniden kullanılır:
    kullanılmayan en küçük sıra numarası seçilir. Kapalıysa en yüksek + 1.
    """
    onek = _ayar("lab_no_onek", str(_dt.now().year))
    if _ayar("lab_no_yillik_sifirla", "1") == "1":
        onek = str(_dt.now().year)
    basamak = int(_ayar("lab_no_basamak", "4") or 4)
    bosluk_doldur = _ayar("lab_no_bosluk_doldur", "1") == "1"

    kalip = re.compile(rf"^{re.escape(onek)}-(\d+)$")
    kullanilan = set()
    for r in db.sorgu("SELECT cycle_no FROM cycle WHERE lab_id = ?", (db.LAB_ID,)):
        m = kalip.match(r["cycle_no"] or "")
        if m:
            kullanilan.add(int(m.group(1)))

    if bosluk_doldur:
        sira = 1
        while sira in kullanilan:
            sira += 1
    else:
        sira = (max(kullanilan) + 1) if kullanilan else 1

    return f"{onek}-{sira:0{basamak}d}"


# ----------------------------------------------------------------- oturum

# --------------------------------------------------------- modül erişim izni

# Yönetici, her kullanıcının hangi ekranlara girebileceğini tek tek belirler
# (v6.14). `goc_026` ile aynı liste olmalı — yeni modül eklersen ikisine de.
MODULLER = [
    ("hasta",         "Hasta ve tedavi kaydı"),
    ("opu",           "OPU"),
    ("androloji",     "Androloji"),
    ("denudasyon",    "Denüdasyon"),
    ("icsi",          "ICSI"),
    ("fert",          "Fertilizasyon"),
    ("cleavage",      "Cleavage"),
    ("blast",         "Blastokist"),
    ("vitrifikasyon", "Vitrifikasyon"),
    ("thaw",          "Çözme"),
    ("transfer",      "Transfer"),
    ("gebelik",       "Gebelik sonucu"),
    ("cryo",          "Cryo haritası (Embriyo / Sperm Dondurma)"),
    ("foto",          "Fotoğraf ekleme / eşleştirme"),
    ("silme",         "Kayıt silme ve iptal"),
]
MODUL_KODLARI = {k for k, _ in MODULLER}
_ASAMA_MODULLERI = {"opu", "androloji", "denudasyon", "icsi", "fert", "cleavage",
                    "blast", "vitrifikasyon", "thaw", "transfer", "gebelik"}

# Bu istekteki kullanıcının izinleri. Kontrolü middleware'de tek noktada
# yapıyoruz: ~50 rotanın her birine kontrol eklemek tuzak #1'in tarifi.
# `asama_gezinme` gibi request almayan fonksiyonlar da buradan okur.
_YETKILER = contextvars.ContextVar("yetkiler", default=None)

# Şu an giriş yapmış kullanıcı — `_guncel_kullanici_ad()` buradan okur
# (`_YETKILER`'in aynı deseni: request almayan Jinja global'lar için).
_GIRIS_KULLANICI = contextvars.ContextVar("giris_kullanici", default=None)


def yol_modulu(yol: str):
    """Bu yol hangi modüle ait? İzin gerekmiyorsa None.

    Görüntüleme ekranları (hasta listesi, hasta detay, cycle özeti) serbest —
    kısıtlanırsa program kullanılamaz hale gelir. İzin, **işlem yapılan**
    ekranlar için.
    """
    p = [x for x in yol.split("/") if x]
    if not p:
        return None
    son = p[-1]
    # Silme ve iptal, hangi ekranda olursa olsun tek modül
    if son == "sil" or son.endswith("-sil") or son == "geri-al":
        return "silme"
    if p[0] == "cryo":
        # /cryo/tasiyici/{id}/thaw gerçek bir çözme işlemi — çözme izni ister
        return "thaw" if son == "thaw" else "cryo"
    if p[0] == "sperm-dondurma":
        # Ayrı bir modül açılmadı — aynı personel grubu, aynı "cryo" izni
        # (goc_026'yı tekrar çalıştırma zorunluluğu doğurmadan).
        return "cryo"
    if p[0] == "disari":
        # Excel çıktısı, ekranda görülebilen veriyi dosyaya yazıyor; izni de
        # ekranınkiyle aynı olmalı. Cryo dökümü cryo haritasına bağlı; ay
        # listesi ve cycle detayı görüntüleme ekranları gibi serbest.
        # `/disari/tumu` bunların dışında: rotanın kendisi yönetici istiyor.
        return "cryo" if len(p) >= 2 and p[1] == "cryo" else None
    if p[0] == "cycle" and len(p) >= 3:
        a = p[2]
        if a in ("foto-ekle", "esle", "doktor-notu-ekle"):
            return "foto"
        if a == "duzenle":
            return "hasta"
        if a == "denudasyon-zaman":
            return "denudasyon"
        if a in _ASAMA_MODULLERI:
            return a
        return None                      # islem-yapan: aşama zaten korumalı
    if p[0] == "hasta":
        if len(p) >= 2 and p[1] == "yeni":
            return "hasta"
        if len(p) >= 3 and (p[2] == "duzenle" or p[2] == "cycle"):
            return "hasta"
        if len(p) >= 3 and p[2] == "sperm-dondurma":
            return "cryo"
        return None                      # /hasta/{id} görüntüleme serbest
    if p[0] == "specimen" and len(p) >= 3:
        if p[2] == "snapshot-al":
            return "foto"
        if p[2] == "taraf":
            return "denudasyon"
    return None


def yetki_tablosu_var() -> bool:
    """`goc_026` çalıştırıldı mı. Çalışmadıysa kimse ekran kaybetmez (tuzak #3).

    Cevap `db.tablo_var()`'da saklanıyor -- geri yüklemeden sonra unutulsun
    diye kendi değişkeninde değil (v6.145, tuzak #15)."""
    return db.tablo_var("yetki")


def kullanici_yetkileri(k) -> set:
    """Bu kullanıcının girebildiği modüller.

    Yönetici her yere girer. Göç çalıştırılmadıysa da herkes her yere girer —
    yarım kurulumda kimse ekran kaybetmesin.
    """
    if not k or k["rol"] == "yonetici" or not yetki_tablosu_var():
        return set(MODUL_KODLARI)
    return {r["modul"] for r in db.sorgu(
        "SELECT modul FROM yetki WHERE kullanici_id = ?", (k["id"],))}


def yetkim(modul: str) -> bool:
    """Şablonlardan çağrılır: bu kullanıcı bu modüle girebiliyor mu?"""
    y = _YETKILER.get()
    return True if y is None else modul in y


sablon.env.globals["yetkim"] = yetkim
sablon.env.globals["metin"] = metinler.t
sablon.env.globals["say"] = metinler.say
sablon.env.globals["yuzde"] = metinler.yuzde
sablon.env.globals["dil"] = metinler.dil


# --------------------------------------------------------------- tazeleme

# Ekranın kendini yenilemesi için "veri değişti mi" sorusunun cevabı (v6.54).
# `oturum` dışarıda: her istekte yazılıyor, sinyal sayarsak sayfa kendi
# sorgusu yüzünden sonsuz yenilenirdi. `goc_kaydi` de klinik veri değil.
# Bu bir **dışlama** listesi: yeni bir tablo eklersen kendiliğinden kapsanır.
DEGISIM_ATLA = {"oturum", "goc_kaydi"}

# Satır sayısı ve en büyük rowid ekleme/silmeyi yakalıyor; **yerinde**
# değişen alanları yakalamıyor. Düzenlemelerin çoğu `degisiklik_log`'a satır
# yazdığı için oradan yakalanıyor, ama iptal işareti yazmıyor: `iptal_mi`
# yerinde 1'e çekiliyor ve günlüğe düşmüyor. İptal klinik bir karar (atılan
# oosit, geri alınan işlem), öteki ekranda görünmesi gerekir -- o yüzden
# ayrıca sayılıyor. Aynı işlem `specimen.durum`'u da değiştiriyor ama onu
# ayrıca saymaya gerek yok: durum değişen her yerde bir `olay` satırı da var.
DEGISIM_EK = {"olay": "COALESCE(SUM(iptal_mi), 0)",
              "sperm_dondurma": "COALESCE(SUM(iptal_mi), 0)"}

_DEGISIM_TABLOLARI = None


def _degisim_tablolari(b):
    """Taranacak tablolar. Bir kez bulunup saklanıyor — şema yalnızca göçle
    değişiyor; yedekten geri yüklemeden sonra `veritabani_yenilendi()`
    listeyi unutturuyor (v6.145)."""
    global _DEGISIM_TABLOLARI
    if _DEGISIM_TABLOLARI is None:
        _DEGISIM_TABLOLARI = [
            r[0] for r in b.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name")
            if r[0] not in DEGISIM_ATLA]
    return _DEGISIM_TABLOLARI


def veri_damgasi() -> str:
    """Klinik verinin o anki imzası. Değiştiyse açık ekranlar yenileniyor.

    Her tablo için `COUNT(*)` ve `MAX(rowid)`: en büyük rowid **eklemeyi**,
    sayı **silmeyi** yakalıyor. İkisi de rowid indeksinden okunuyor.

    Kapsam: her yeni kayıt, her silme, her iptal (`DEGISIM_EK`) ve
    `degisiklik_log`'a satır yazan her düzenleme -- programın ekranlarından
    yapılan düzenlemeler bunu yazıyor, denendi. Kapsam dışı: günlüğe hiç
    yazmayan bir yerinde düzenleme; o ekran bugünkü gibi elle yenilenene
    kadar eski kalır -- gerileme değil, kapsanmayan bir durum.

    Damga hiçbir veri sızdırmaz: yalnızca sayılardan oluşan bir dizgi.
    """
    with db.baglan() as b:
        parcalar = []
        for t in _degisim_tablolari(b):
            ek = DEGISIM_EK.get(t)
            try:
                satir = b.execute(
                    f"SELECT COUNT(*), COALESCE(MAX(rowid), 0)"
                    f"{', ' + ek if ek else ''} FROM {t}").fetchone()
            except sqlite3.Error:        # tablo silinmiş/erişilemiyor
                continue
            parcalar.append(".".join(str(x) for x in satir))
    return "-".join(parcalar)


sablon.env.globals["veri_damgasi"] = veri_damgasi


# ------------------------------------------------- kim neyi düzenliyor

# Aynı kaydı iki kişi aynı anda düzenlerse, ikinci kaydeden birincinin
# yazdığını siler -- kayıt edilirken formun **tamamı** yazılıyor
# (`UPDATE olay SET <bütün alanlar>`), yalnızca dokunduğun alan değil.
# Bu yüzden uyarının birimi "alan" değil **kayıt**: farklı alanları
# düzenlemek de çarpışma (v6.55).
#
# **Uyarı engellemez.** Katı kilit klinikte yanlış olurdu: telefonun pili
# biterse kayıt kilitli kalır, ve acele eden personeli kayıt girmekten
# alıkoymak çarpışmadan pahalıya gelir. Program haber veriyor, kararı
# kullanıcı veriyor.
#
# **Bellekte tutuluyor, `lab.db`'de değil.** İki sebep: (1) bu veri o anki
# sunucu çalışmasına ait, klinik kayıt değil; (2) `lab.db` USB ile
# taşınıyor, bayat "düzenleniyor" satırları da onunla taşınırdı.
# Sunucu tek süreç çalışıyor (`baslat.py`); birden çok işçiyle çalıştırılırsa
# bu sözlük paylaşılmaz, o gün ortak bir yere taşınması gerekir.
DUZENLEME_OMRU = 45.0          # sn -- bu kadar ses vermeyen bırakmış sayılır
DUZENLEME_EN_COK = 500         # sözlük sınırsız büyümesin
ANAHTAR_KALIBI = re.compile(r"^[a-z0-9:_-]{1,60}$")

# {anahtar: {sekme_kimligi: (kisa_kod, son_an)}}
_duzenleyenler = {}
_duzenleme_kilidi = threading.Lock()


def _bayatlari_at(simdi):
    """Ömrü geçenleri ve boşalan anahtarları siler. Kilit tutuluyorken çağır."""
    for anahtar in list(_duzenleyenler):
        kalan = {k: v for k, v in _duzenleyenler[anahtar].items()
                 if simdi - v[1] < DUZENLEME_OMRU}
        if kalan:
            _duzenleyenler[anahtar] = kalan
        else:
            del _duzenleyenler[anahtar]


def duzenleme_bildir(anahtar: str, sekme: str, kisa_kod: str):
    """"Bu kaydı düzenliyorum" haberi. Aynı kaydın öteki düzenleyenlerini döner.

    Kimlik **sekme başına**, kullanıcı başına değil: aynı kişi telefonundan
    ve masaüstünden aynı kaydı açtıysa o da gerçek bir çarpışma.
    """
    simdi = time.monotonic()
    with _duzenleme_kilidi:
        _bayatlari_at(simdi)
        if anahtar not in _duzenleyenler and len(_duzenleyenler) >= DUZENLEME_EN_COK:
            return []                    # sınır aşıldı: haber alınmıyor
        _duzenleyenler.setdefault(anahtar, {})[sekme] = (kisa_kod, simdi)
        return [v[0] for k, v in _duzenleyenler[anahtar].items() if k != sekme]


def duzenleme_birak(anahtar: str, sekme: str):
    """Sayfa kapandı / kaydedildi: haberi geri al."""
    with _duzenleme_kilidi:
        if anahtar in _duzenleyenler:
            _duzenleyenler[anahtar].pop(sekme, None)
            if not _duzenleyenler[anahtar]:
                del _duzenleyenler[anahtar]


def duzenleyenler(anahtar: str, sekme: str):
    """Bu kaydı başka kim düzenliyor? Hiçbir şey yazmaz."""
    simdi = time.monotonic()
    with _duzenleme_kilidi:
        _bayatlari_at(simdi)
        return [v[0] for k, v in _duzenleyenler.get(anahtar, {}).items()
                if k != sekme]


def _anahtar_gecerli(anahtar: str, sekme: str) -> bool:
    """Adresten gelen metin: kalıptan geçmeyen istek hiç işlenmiyor (tuzak #9).

    Ekrana basılan yazı yalnızca **veritabanındaki** `kisa_kod`; istemciden
    gelen metin hiç basılmıyor. Kalıp bellekte çöp birikmesin diye.
    """
    return bool(anahtar and sekme
                and ANAHTAR_KALIBI.match(anahtar) and ANAHTAR_KALIBI.match(sekme))


@uygulama.post("/duzenliyorum")
async def duzenliyorum(request: Request):
    """Form doldurulurken saniyeler içinde bir gelen haber (v6.55)."""
    f = dict(await request.form())
    anahtar = (f.get("anahtar") or "").strip()
    sekme = (f.get("sekme") or "").strip()
    if not _anahtar_gecerli(anahtar, sekme):
        return JSONResponse({"baskalari": []})
    # `request.state.kullanici` bir sqlite3.Row -- `.get()` yok, köşeli parantez.
    k = request.state.kullanici
    kod = ((k["kisa_kod"] or k["kullanici_adi"] or "?"))[:8]
    return JSONResponse({"baskalari": duzenleme_bildir(anahtar, sekme, kod)},
                        headers={"Cache-Control": "no-store"})


@uygulama.post("/duzenlemeyi-biraktim")
async def duzenlemeyi_biraktim(request: Request):
    """Sayfa kapanınca `sendBeacon` ile geliyor; gelmezse haber bayatlıyor."""
    f = dict(await request.form())
    anahtar = (f.get("anahtar") or "").strip()
    sekme = (f.get("sekme") or "").strip()
    if _anahtar_gecerli(anahtar, sekme):
        duzenleme_birak(anahtar, sekme)
    return JSONResponse({"tamam": True})


@uygulama.get("/degisim")
def degisim(anahtar: str = "", sekme: str = ""):
    """Açık ekranların iki sorusu, tek istekte (v6.54, v6.55).

    "Yeni kayıt var mı" (damga) ve "bu kaydı başka kim düzenliyor". İkinci
    bir yoklayıcı eklemek yerine aynı isteğe bindirildi -- klinikte birkaç
    telefon var, istek sayısı iki katına çıkmasın.

    **Hiçbir şey yazmaz**: düzenleme haberi ayrı bir POST ile geliyor, yani
    yalnızca izleyen bir ekran ne veritabanına ne belleğe dokunuyor.

    Middleware'in arkasında: oturumu olmayan bu yolu da göremez.
    `yol_modulu("/degisim")` None dönüyor, yani modül izni istemiyor --
    ekranı görebilen onun tazeliğini de sorabilmeli.
    """
    cevap = {"damga": veri_damgasi(), "baskalari": []}
    if _anahtar_gecerli(anahtar, sekme):
        cevap["baskalari"] = duzenleyenler(anahtar, sekme)
    return JSONResponse(cevap, headers={"Cache-Control": "no-store"})


@uygulama.middleware("http")
async def oturum_kontrolu(request: Request, sonraki):
    yol = request.url.path
    if yol.startswith("/static"):
        return await sonraki(request)

    # Dil lab geneli bir ayardır ve giriş ekranı da çevrilidir — bu yüzden
    # oturum kontrolünden ÖNCE ayarlanır, ACIK_YOLLAR'da da geçerlidir.
    dil_jetonu = metinler.dil_ayarla(db.ayar("dil", metinler.VARSAYILAN))
    try:
        if yol in ACIK_YOLLAR:
            return await sonraki(request)

        # `/degisim` oturumu tazelemez: yoklama kullanıcının işlemi değil.
        kullanici = guvenlik.oturumdaki_kullanici(
            request.cookies.get(guvenlik.CEREZ_ADI),
            dokun=(yol != "/degisim"))
        if not kullanici:
            return RedirectResponse("/giris", status_code=303)

        request.state.kullanici = kullanici
        yetkiler = kullanici_yetkileri(kullanici)
        request.state.yetkiler = yetkiler
        jeton = _YETKILER.set(yetkiler)
        k_jeton = _GIRIS_KULLANICI.set(kullanici)
        try:
            modul = yol_modulu(yol)
            if modul and modul not in yetkiler:
                from urllib.parse import quote
                return RedirectResponse(
                    "/?yetkisiz=" + quote(dict(MODULLER).get(modul, modul)),
                    status_code=303)
            return await sonraki(request)
        finally:
            _YETKILER.reset(jeton)
            _GIRIS_KULLANICI.reset(k_jeton)
    finally:
        metinler.dil_sifirla(dil_jetonu)


@uygulama.get("/giris")
def giris_ekrani(request: Request, hata: str = "", sifre: int = 0):
    return sablon.TemplateResponse(request, "giris.html",
                                   {"hata": hata, "sifre_degisti": sifre})


@uygulama.post("/giris")
def giris(kullanici_adi: str = Form(...), sifre: str = Form(...)):
    jeton = guvenlik.giris_yap(kullanici_adi, sifre)
    if not jeton:
        return RedirectResponse("/giris?hata=1", status_code=303)
    yanit = RedirectResponse("/", status_code=303)
    yanit.set_cookie(
        guvenlik.CEREZ_ADI, jeton,
        httponly=True,          # JavaScript okuyamaz
        samesite="lax",         # baska siteden gelen istekte tasinmaz
        max_age=60 * 60 * guvenlik.OTURUM_SURESI_SAAT,
    )
    return yanit


@uygulama.get("/cikis")
def cikis(request: Request):
    guvenlik.cikis_yap(request.cookies.get(guvenlik.CEREZ_ADI))
    yanit = RedirectResponse("/giris", status_code=303)
    yanit.delete_cookie(guvenlik.CEREZ_ADI)
    return yanit


# ------------------------------------------------------- kullanıcı yönetimi

MIN_SIFRE = 8
ROLLER = ("yonetici", "embriyolog")
ROL_ADI = {"yonetici": "Yönetici", "embriyolog": "Embriyolog"}

# Kullanıcı silmeyi engelleyen tablolar: (tablo, kolon, ekranda görünen ad).
# `oturum` burada yok — o veri değil, açık tarayıcı; silmekle geçmiş bozulmaz.
KULLANICI_KAYITLARI = [
    ("goruntu", "kullanici_id", "fotoğraf"),
    ("olay", "kullanici_id", "olay"),
    ("olay", "iptal_kullanici_id", "iptal ettiği olay"),
    ("specimen_bulgu", "kullanici_id", "bulgu"),
    ("sperm_ornek", "kullanici_id", "sperm örneği"),
    ("sperm_analiz", "kullanici_id", "sperm analizi"),
    ("tasiyici", "kullanici_id", "taşıyıcı"),
    ("sperm_dondurma", "kullanici_id", "sperm dondurma kaydı"),
    ("sperm_dondurma", "iptal_kullanici_id", "iptal ettiği sperm dondurma kaydı"),
    ("islem_yapan", "kullanici_id", "işlemi yapan kaydı"),
    ("pgt_sonuc", "kaydeden_kullanici_id", "PGT sonucu"),
    ("degisiklik_log", "kullanici_id", "değişiklik kaydı"),
    ("lab_formu", "kullanici_id", "yüklediği form kalıbı"),
]


def kullanici_kayitlari(kid: int):
    """Bu kullanıcının girdiği kayıtlar — kalıcı silmeyi engelleyenler.

    11 tablo `kullanici.id`'ye bağlı. Kayıt girmiş bir kullanıcıyı fiziksel
    silmek "bu blastokisti kim değerlendirdi" sorusunu cevapsız bırakır ve
    FOREIGN KEY hatası verir. Projenin kuralı: silme = pasif yapma.
    """
    bulunan = []
    for tablo, kolon, ad in KULLANICI_KAYITLARI:
        try:
            n = db.tek(f"SELECT COUNT(*) n FROM {tablo} WHERE {kolon} = ?",
                       (kid,))["n"]
        except sqlite3.Error:
            continue                      # tablo yoksa (göç çalışmamış) atla
        if n:
            bulunan.append({"ad": ad, "sayi": n})
    return bulunan


def aktif_yonetici_sayisi() -> int:
    return db.tek("SELECT COUNT(*) n FROM kullanici WHERE lab_id = ? "
                  "AND rol = 'yonetici' AND aktif_mi = 1", (db.LAB_ID,))["n"]


def yonetici_mi(k) -> bool:
    return bool(k) and k["rol"] == "yonetici"


def sifre_gecerli(yeni: str, tekrar: str):
    """Hata metni döndürür, sorun yoksa None."""
    if yeni != tekrar:
        return "Yeni şifreler birbirini tutmuyor."
    if len(yeni) < MIN_SIFRE:
        return f"Şifre en az {MIN_SIFRE} karakter olmalı."
    return None


def sifre_istegi_tablosu_var() -> bool:
    """`goc_030` çalıştırıldı mı.

    Çalışmadıysa şifre değiştirme **eski gibi** anında geçer: göçü
    çalıştırmamış bir makinede personelin şifre değiştirmesini tümden
    engellemek, onay akışının çözdüğü sorundan pahalı olurdu (tuzak #3).
    Cevap `db.tablo_var()`'da saklanıyor (v6.145, tuzak #15).
    """
    return db.tablo_var("sifre_istegi")


def bekleyen_sifre_istekleri():
    """Onay bekleyen istekler, eskiden yeniye."""
    if not sifre_istegi_tablosu_var():
        return []
    return db.sorgu(
        "SELECT i.id, i.kullanici_id, i.olusturma_zamani, "
        "       k.kullanici_adi, k.ad_soyad, k.kisa_kod "
        "FROM sifre_istegi i JOIN kullanici k ON k.id = i.kullanici_id "
        "WHERE i.lab_id = ? AND i.durum = 'bekliyor' "
        "ORDER BY i.olusturma_zamani", (db.LAB_ID,))


def sifre_yaz(kid: int, yeni: str, oturum_dusur: bool = True):
    """Şifreyi değiştirir ve o kullanıcının açık oturumlarını kapatır.

    Oturumlar düşmezse "şifreyi değiştirdim" yanıltıcı olur: eski şifreyle
    açılmış bir tarayıcı 12 saat daha çalışmaya devam eder (README v6.11).
    """
    db.yaz("UPDATE kullanici SET sifre_hash = ? WHERE id = ?",
           (guvenlik.sifrele(yeni), kid))
    if oturum_dusur:
        db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (kid,))


@uygulama.get("/sifremi-unuttum")
def sifremi_unuttum(request: Request):
    """Giriş gerektirmez. Hiçbir şey sıfırlamaz — kime başvurulacağını söyler.

    Sistemde e-posta/SMS yok, yani kimliği doğrulayacak ikinci bir kanal yok.
    Doğrulamasız sıfırlama iç ağdaki herkese yönetici şifresini değiştirme
    hakkı verirdi (HTTPS de yok). Bu yüzden sıfırlamayı yönetici yapar.
    Kullanıcı adı listelenmez — giriş yapmamış birine kim olduğunu söylemez.
    """
    return sablon.TemplateResponse(request, "sifremi_unuttum.html", {})


def oturumdaki(request: Request):
    """Açık sayfalarda oturumdaki kullanıcı — yoksa None.

    Middleware `request.state.kullanici`'yi yalnızca korumalı yollarda dolduruyor;
    `/sifre` açık bir yol olduğu için çerezi kendisi okumak zorunda.
    """
    k = getattr(request.state, "kullanici", None)
    if k:
        return k
    return guvenlik.oturumdaki_kullanici(request.cookies.get(guvenlik.CEREZ_ADI))


@uygulama.get("/sifre")
def sifre_ekran(request: Request, hata: str = "", onay: str = ""):
    """Giriş yapılmadan da açılır — giriş ekranından bağlantısı var.

    Güvenliği düşürmez: her iki durumda da **mevcut şifre** isteniyor, yani
    kimlik yine kanıtlanıyor. Giriş yapmışsa kullanıcı adı hazır gelir,
    yapmamışsa kendisi yazar (README v6.12).
    """
    k = oturumdaki(request)
    # Onay kuralı kullanıcıya göre: yönetici anında değiştirir. Giriş
    # yapmamış birine "onay gerekir" demek kimin yönetici olduğunu sızdırırdı
    # — o yüzden yalnızca giriş yapmışa yazılıyor.
    onay_gerekir = bool(k) and not yonetici_mi(k) and sifre_istegi_tablosu_var()
    return sablon.TemplateResponse(
        request, "sifre.html",
        {"kullanici": k, "hata": hata, "onay": bool(onay),
         "onay_gerekir": onay_gerekir})


@uygulama.post("/sifre")
async def sifre_kaydet(request: Request):
    from urllib.parse import quote
    f = dict(await request.form())
    oturum = oturumdaki(request)

    def hata(m):
        return RedirectResponse(f"/sifre?hata={quote(m)}", status_code=303)

    if oturum:
        tam = db.tek("SELECT * FROM kullanici WHERE id = ?", (oturum["id"],))
    else:
        kadi = (f.get("kullanici_adi") or "").strip().lower()
        tam = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND "
                     "kullanici_adi = ? AND aktif_mi = 1", (db.LAB_ID, kadi))

    # Tek ve aynı mesaj: giriş yapmamış birine hangi kullanıcı adının var
    # olduğunu söylemez. Mevcut şifre şart — açık kalmış bir tarayıcıyı bulan
    # biri de hesabı ele geçiremesin.
    if not tam or not guvenlik.dogrula(f.get("mevcut") or "", tam["sifre_hash"]):
        return hata("Kullanıcı adı veya mevcut şifre yanlış.")

    yeni = f.get("yeni") or ""
    m = sifre_gecerli(yeni, f.get("yeni2") or "")
    if m:
        return hata(m)
    if guvenlik.dogrula(yeni, tam["sifre_hash"]):
        return hata("Yeni şifre eskisiyle aynı.")

    # Yöneticinin kendi şifresi onay beklemez (v6.61). Tek yönetici kendi
    # isteğini onaylamak için giriş yapamaz duruma düşerdi — README v6.11'deki
    # kilitlenme korumasının aynısı. Göç çalıştırılmamışsa da eski yol.
    if yonetici_mi(tam) or not sifre_istegi_tablosu_var():
        sifre_yaz(tam["id"], yeni)
        # Oturumlar düştü (varsa kendisininki de) — yeniden giriş yapmalı.
        yanit = RedirectResponse("/giris?sifre=1", status_code=303)
        yanit.delete_cookie(guvenlik.CEREZ_ADI)
        return yanit

    # Bekleyen istek TEK: ikinci istek birincinin yerine geçiyor. Yoksa
    # yönetici hangisinin sonuncusu olduğunu bilemez ve eski bir şifreyi
    # onaylayabilir.
    db.yaz("DELETE FROM sifre_istegi WHERE lab_id = ? AND kullanici_id = ? "
           "AND durum = 'bekliyor'", (db.LAB_ID, tam["id"]))
    db.yaz("INSERT INTO sifre_istegi (lab_id, kullanici_id, yeni_hash) "
           "VALUES (?,?,?)", (db.LAB_ID, tam["id"], guvenlik.sifrele(yeni)))
    _gunluk.info("sifre istegi: %s", tam["kullanici_adi"])
    # Şifre HENÜZ değişmedi: oturumu düşürmek yanıltıcı olurdu.
    return RedirectResponse("/sifre?onay=1", status_code=303)


# --------------------------------------------- yönetici: kullanıcı listesi

def tum_yetkileri_ver(kid: int):
    """Yeni kullanıcıya tüm modülleri verir.

    Göç mevcut kullanıcılara hepsini veriyor; sonradan açılan kullanıcı boş
    kalırsa **hiçbir ekrana giremez** ve sebebi anlaşılmaz. Varsayılan "her şey
    açık", kısıtlama yöneticinin bilinçli olarak kaldırdığı kutulardan doğar
    (v6.14).
    """
    if not yetki_tablosu_var():
        return
    for kod, _ in MODULLER:
        db.yaz("INSERT OR IGNORE INTO yetki (lab_id, kullanici_id, modul) "
               "VALUES (?,?,?)", (db.LAB_ID, kid, kod))


def _kullanici_yetki_haritasi() -> dict:
    """{kullanici_id: {modul, ...}} — yetki ekranındaki kutuları işaretlemek için."""
    if not yetki_tablosu_var():
        return {}
    harita = {}
    for r in db.sorgu("SELECT kullanici_id, modul FROM yetki"):
        harita.setdefault(r["kullanici_id"], set()).add(r["modul"])
    return harita


def yonetici_kontrol(request: Request):
    """Yönetici değilse yönlendirme döndürür, yöneticiyse None.

    `rol` kolonu v6.11'e kadar hiçbir yerde kontrol edilmiyordu — giriş yapan
    herkes her şeyi yapabiliyordu. Kullanıcı silme ekranı bunu zorunlu kıldı:
    yetki kontrolü olmadan herhangi bir personel yöneticiyi silebilirdi.
    """
    if not yonetici_mi(request.state.kullanici):
        return RedirectResponse("/hastalar", status_code=303)
    return None


# --------------------------------------------------- telefonun ana ekranına
#
# Personel adres yazmak yerine karekodu okutuyor, sonra "Ana Ekrana Ekle"
# diyor: program kendi simgesiyle, tam ekran, uygulama gibi açılıyor
# (v6.45, kullanıcının isteği). Mağazaya gerek yok -- mağazadan inen bir
# uygulama da yine bu sunucuya bağlanacaktı.

@uygulama.get("/manifest.json")
def manifest():
    """Ana ekrana eklenen simgenin tanımı.

    `ACIK_YOLLAR`'da: tarayıcı bu dosyayı oturum çerezi göndermeden
    istiyor, korumalı olsaydı giriş ekranına yönlendirilir ve simge
    adsız/ikonsuz eklenirdi. İçinde hasta verisi yok -- program adı ve
    simge yolları.
    """
    return JSONResponse({
        "name": metinler.t("program_adi"),
        "short_name": metinler.t("kisa_ad"),
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#eef2f4",       # sayfa zemini
        "theme_color": "#17222b",            # üst çubuk
        "lang": metinler.dil(),
        "icons": [
            {"src": "/static/ikon_192.png", "sizes": "192x192",
             "type": "image/png", "purpose": "any maskable"},
            {"src": "/static/ikon_512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any maskable"},
        ],
    })


def _yerel_ip():
    """Bu makinenin yerel ağdaki adresi.

    Dışarıya **paket gitmiyor**: UDP soketinde `connect` yalnızca çekirdeğe
    "bu hedefe hangi arayüzden çıkardım" diye soruyor. `gethostbyname` ise
    çoğu makinede 127.0.0.1 döndürüyor, işe yaramıyor.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return ""
    finally:
        s.close()


def _baglanti_adresi(request: Request):
    """Personelin telefonuna yazılacak adres.

    Yönetici zaten ağ üzerinden bağlandıysa **onun kullandığı adres** en
    doğrusu: çalıştığı kanıtlanmış. Sunucunun kendi tarayıcısından
    bakılıyorsa (localhost) yerel ağ adresi bulunuyor.
    """
    ana = request.url.hostname or ""
    if ana in ("localhost", "127.0.0.1", "::1", ""):
        ana = _yerel_ip() or ana
    port = request.url.port or 8000
    return f"http://{ana}:{port}" if port != 80 else f"http://{ana}"


@uygulama.get("/ekle")
def ekle_ekrani(request: Request):
    """Karekodu okutan kişinin telefonunda açılan yönerge.

    **Giriş gerektirmiyor** (`ACIK_YOLLAR`): kişi henüz hesabını açmadı,
    zaten ekranda yalnızca "ana ekrana nasıl eklenir" yazıyor -- hasta
    verisi yok.

    Bir web sayfası kendini ana ekrana **ekleyemez**: iOS'ta böyle bir API
    hiç yok, Android'de `beforeinstallprompt` var ama güvenli bağlantı
    (HTTPS) ve service worker istiyor. Yapılabilecek en yakın şey bu:
    okutan kişi doğrudan yönergeye düşsün, giriş ekranına değil.
    """
    return sablon.TemplateResponse(request, "ekle.html", {})


@uygulama.get("/baglan")
def baglan_ekrani(request: Request):
    """Karekod + "ana ekrana ekle" yönergesi. Duvara asmak için yazdırılabilir."""
    red = yonetici_kontrol(request)
    if red:
        return red
    adres = _baglanti_adresi(request)
    # Karekod **programın kendisine** açılıyor, yani ilk gelen ekran şifre
    # ekranı (v6.48). v6.47'de `/ekle` yönergesine açılıyordu; iPhone "Ana
    # Ekrana Ekle" derken çoğu zaman **o an açık olan adresi** kaydettiği
    # için simge açık bir sayfayı yakalıyor ve şifre hiç sorulmuyordu.
    # Yönergeye giriş ekranındaki bağlantıdan gidiliyor.
    try:
        kare = karekod.svg(adres, kutu=6)
    except karekod.Hata:
        kare = ""
    return sablon.TemplateResponse(request, "baglan.html", {
        "adres": adres, "karekod": kare,
        "makine_adi": socket.gethostname(),
        "kullanici": request.state.kullanici,
    })


@uygulama.get("/dil")
def dil_ekran(request: Request, kaydedildi: int = 0):
    """Lab genelinde dil seçimi — yalnızca yönetici.

    Dil kullanıcı başına değil **lab başına** tektir: yönetici bir kez seçer,
    giriş ekranı dahil bütün program o dile geçer (CLAUDE.md bekleyen iş 8).

    Seçici bilerek giriş ekranında değil: `/dil` açık bir yol olsaydı giriş
    yapmamış herkes labın dilini değiştirebilirdi. Düğmeyi gizlemek yetmez,
    sunucu da reddetmeli — hasta silmedeki kuralın aynısı.
    """
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(request, "dil.html", {
        "diller": metinler.DILLER,
        "secili": metinler.dil(),
        "kaydedildi": kaydedildi,
    })


@uygulama.post("/dil")
def dil_kaydet(request: Request, dil_kodu: str = Form(...)):
    red = yonetici_kontrol(request)
    if red:
        return red
    if dil_kodu not in dict(metinler.DILLER):
        return RedirectResponse("/dil", status_code=303)
    db.yaz("INSERT INTO ayarlar (lab_id, anahtar, deger) VALUES (?, 'dil', ?) "
           "ON CONFLICT (lab_id, anahtar) DO UPDATE SET deger = excluded.deger",
           (db.LAB_ID, dil_kodu))
    return RedirectResponse("/dil?kaydedildi=1", status_code=303)


# ----------------------------------------------------- bu makinenin klasörleri
#
# Kamera klasörünü (mikroskobun snapshot attığı yer) yöneticinin ekrandan
# seçebilmesi için (v6.41, kullanıcının isteği). Önceden tek yol terminaldi:
# `python yerel_kur.py`. Görüntü eşlemesi kuracak bir laboratuvar için bu
# fazla yüksek bir eşik -- kamera klasörü yanlışsa kuyruk hep boş görünür.
#
# **Ayar veritabanında değil `yerel_ayar.json`'da**, makine adına göre
# bölümlenmiş: `lab.db` USB ile taşınıyor, klinik bilgisayarı Mac'in
# yollarını kullanmaya başlamamalı. Yazan tek yer `db.yerel_yaz()`.
#
# `/yonetim` salt okunur kaldı; bu ayrı bir ekran, panelden yalnızca
# bağlantı veriliyor (dil seçiminde olduğu gibi).

KLASOR_ALANLARI = ("goruntu_kaynak_klasor", "goruntu_arsiv_klasor",
                   "yedek_klasor")

# Hata anahtarları adresten geliyor; `metin()` bulamadığını olduğu gibi
# döndürdüğü için beyaz listeden geçiyor (tuzak #9).
KLASOR_HATALARI = {"klasor_hata_kamera", "klasor_hata_arsiv"}


@uygulama.get("/klasorler")
def klasorler_ekran(request: Request, hata: str = "", kaydedildi: int = 0):
    red = yonetici_kontrol(request)
    if red:
        return red
    yollar = []
    for anahtar in KLASOR_ALANLARI:
        yol = db.ayar(anahtar, "")
        yollar.append({"anahtar": anahtar, "yol": yol,
                       "var": bool(yol) and Path(yol).is_dir()})
    return sablon.TemplateResponse(request, "klasorler.html", {
        "yollar": yollar, "makine": db.MAKINE,
        "hata": metinler.t(hata) if hata in KLASOR_HATALARI else "",
        "kaydedildi": kaydedildi,
        "kullanici": request.state.kullanici,
    })


# --------------------------------------------------------------- yedekleme
#
# v6.121, kullanıcının isteği: "Yedekleme bölümünde Yedekleme olsun.
# Klasörlerin altında zor bulunuyor." v6.119/v6.120'de `/klasorler`'in bir
# kartıydı (yedek klasörü ayarının hemen yanı bilerek seçilmişti); kullanıcı
# ayrı bulunması gereken bir ekran olduğunu söyledi. Yedek klasörünün
# **yolu** hâlâ `/klasorler`'de ayarlanıyor (o bir klasör ayarı) -- yalnızca
# eylemler (şimdi yedekle / geri yükle) kendi ekranına taşındı, `/yonetim`
# panelinden Kullanıcılar/Klasörler'in yanına doğrudan bağlantıyla.

@uygulama.get("/yedekleme")
def yedekleme_ekran(request: Request, yhata: str = "", yedeklendi: int = 0,
                    gymesaj: str = ""):
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(request, "yedekleme.html", {
        # `yhata`/`gymesaj` `hata`'nın aksine beyaz listeden geçmiyor:
        # adresten gelen bir anahtar değil, sunucunun ürettiği bitmiş metin
        # (FormHatasi mesajlarının kullandığı desenin aynısı, tuzak #9
        # burada geçerli değil).
        "yhata": yhata,
        "yedeklendi": yedeklendi,
        "gymesaj": gymesaj,
        "son_yedek": _ayar("son_yedek", ""),
        "yedek_uyari": yedek_durumu(),
        "kullanici": request.state.kullanici,
    })


@uygulama.post("/yedekleme/yedekle-simdi")
def yedekleme_yedekle_simdi(request: Request):
    """Elle yedekleme (v6.119, kullanıcının isteği: "Elle yedekleme olsun").

    `yedek.py`'nin fonksiyonlarını **süreç içinde** çağırır -- `goc.py`'nin
    zaten kurduğu desenin aynısı. `subprocess.run([sys.executable, ...])`
    yazılmadı: paketlenmiş uygulamada `sys.executable` **programın kendisi**
    olur, o satır yedeği değil programı yeniden başlatırdı (CLAUDE.md,
    "Çalıştırıcı tek yerde" bölümü, göçler için söylenen aynı tuzak).

    `yedek.main()` çağrılmadı -- o `sys.exit()` kullanıyor, terminalden
    çalıştırıldığında doğru ama bir istek işleyicisinin içinde `SystemExit`
    fırlatmak istenmeyen bir şey. Onun yerine `main()`'in çağırdığı aynı
    fonksiyonlar (`veritabani_yedekle`, `eskileri_temizle`,
    `arsiv_yedekle`) burada elle, normal `try/except` ile çağrılıyor.
    """
    red = yonetici_kontrol(request)
    if red:
        return red
    from urllib.parse import quote
    import yedek as _yedek

    hedef = db.ayar("yedek_klasor", "")
    if not hedef:
        return RedirectResponse(
            "/yedekleme?yhata=" + quote(metinler.t("yedek_klasoru_yok_hata")),
            status_code=303)
    if not _yedek.bu_makineye_uygun_mu(hedef):
        mesaj = metinler.t("yedek_klasoru_yanlis_makine").replace("{yol}", hedef)
        return RedirectResponse("/yedekleme?yhata=" + quote(mesaj), status_code=303)

    hedef_klasor = Path(hedef)
    kullanici_adi = request.state.kullanici["kullanici_adi"]
    try:
        hedef_klasor.mkdir(parents=True, exist_ok=True)
        _yedek.yaz("=" * 55)
        _yedek.yaz(f"Yedekleme basladi -> {hedef_klasor}   "
                   f"(kaynak: /yedekleme, {kullanici_adi})")
        _yedek.veritabani_yedekle(hedef_klasor)
        _yedek.eskileri_temizle(hedef_klasor)
        arsiv_klasor = Path(db.ayar("goruntu_arsiv_klasor", str(db.VERI_KOK / "arsiv")))
        _yedek.arsiv_yedekle(arsiv_klasor, hedef_klasor)
        _yedek.ayar_yaz("son_yedek", _dt.now().isoformat(" ", "seconds"))
        _yedek.yaz("Yedekleme tamam.")
    except Exception as e:
        _yedek.yaz(f"HATA: {e}")
        mesaj = f"{metinler.t('yedekleme_basarisiz')}: {e}"
        return RedirectResponse("/yedekleme?yhata=" + quote(mesaj), status_code=303)
    return RedirectResponse("/yedekleme?yedeklendi=1", status_code=303)


@uygulama.get("/yedekleme/geri-yukle")
def yedekleme_geri_yukle_ekran(request: Request, hata: str = ""):
    """Yedekten geri yükleme onay ekranı (v6.120, kullanıcının isteği:
    "Yönetici isterse yedekten geri çağırsın... Yönetici panelinden hepsini
    yapabilsin"). Rota adı `-sil` ile bitmiyor, `yol_modulu()` bunu "silme"
    modülüne bağlamaz -- bu, silme izninden bağımsız, doğrudan yönetici
    işi: `yonetici_kontrol()` burada elle çağrılıyor (`/yedekleme`'nin kendi
    deseni).
    """
    red = yonetici_kontrol(request)
    if red:
        return red
    import geri_yukle as _gy
    hedef = db.ayar("yedek_klasor", "")
    yedekler = _gy.yedekleri_listele(Path(hedef)) if hedef else []
    return sablon.TemplateResponse(request, "geri_yukle.html", {
        "yedekler": yedekler, "hata": hata,
        "kullanici": request.state.kullanici,
    })


def veritabani_yenilendi(goc_sonucu: dict) -> None:
    """Yedekten geri yüklemeden sonra programın kendi hafızası (v6.145).

    Açılışta olanın geri yüklemedeki karşılığı: göçleri `geri_yukle`
    uyguladı (`_gocleri_uygula()`), burada çalışan programın sakladığı şema
    cevapları unutuluyor -- kolon/tablo cevapları `db.py`'de, tazelemenin
    tablo listesi burada -- ve Yönetici panelinin göç kartı bu sonucu
    gösteriyor. Şema cevabı saklayan yeni bir yer açacaksan `db.kolon_var()`/
    `db.tablo_var()`'ı kullan; kendi değişkenini açarsan onu da burada
    unutturman gerekir (tuzak #15).
    """
    global GOC_SONUCU, _DEGISIM_TABLOLARI
    GOC_SONUCU = {**goc_sonucu, "geri_yukleme": True}
    _goc_ozeti(GOC_SONUCU)
    _DEGISIM_TABLOLARI = None
    db.sema_bilgisini_unut()


@uygulama.post("/yedekleme/geri-yukle")
async def yedekleme_geri_yukle(request: Request):
    """Onay üç kademeli: (1) seçilen yedeğin dosya adını yazmak, (2) "GERİ
    YÜKLE" yazmak, (3) tarayıcının `confirm()`'ü (`geri_yukle.html`). Hasta
    kalıcı silmenin (dosya no + SIL) aynı deseni -- burada daha ağır, çünkü
    tek hasta değil TÜM veritabanını değiştiriyor.

    Asıl iş `geri_yukle.geri_yukle()`'de: mevcut veritabanının güvenlik
    kopyasını alıp SONRA takas ediyor, o yüzden burada yalnızca doğrulama +
    çağrı var.
    """
    red = yonetici_kontrol(request)
    if red:
        return red
    from urllib.parse import quote
    import geri_yukle as _gy
    f = dict(await request.form())

    def hata(m):
        return RedirectResponse(
            "/yedekleme/geri-yukle?hata=" + quote(m), status_code=303)

    hedef = db.ayar("yedek_klasor", "")
    if not hedef:
        return hata(metinler.t("yedek_klasoru_yok_hata"))

    # `dosya` bir form alanı -- adresten gelen bir metnin doğrudan dosya
    # yoluna eklenmesi tuzak #9'un aynısı (whitelisting yok). Beyaz liste
    # burada `yedekleri_listele()`'nin döndürdüğü gerçek dosya adları:
    # `../../lab.db` gibi bir değer bu kümede olmayacağı için elenir,
    # `Path(hedef) / dosya` hiçbir zaman `yedek_klasor`'ün dışına çıkamaz.
    yedekler = _gy.yedekleri_listele(Path(hedef))
    gecerli_adlar = {y["ad"] for y in yedekler}
    dosya = (f.get("dosya") or "").strip()
    if not dosya:
        return hata(metinler.t("geri_yukle_secim_yok"))
    if dosya not in gecerli_adlar:
        return hata(metinler.t("geri_yukle_secim_yok"))
    if (f.get("onay") or "").strip() != dosya:
        return hata(metinler.t("geri_yukle_dosya_yanlis"))
    if (f.get("onay2") or "").strip().upper() != "GERİ YÜKLE":
        return hata(metinler.t("geri_yukle_onay_yanlis"))

    try:
        sonuc = _gy.geri_yukle(Path(hedef) / dosya)
    except Exception as e:
        return hata(f"{metinler.t('geri_yukleme_basarisiz')}: {e}")

    # Yedek eski bir sürümden olabilir: göçler az önce uygulandı, saklanmış
    # şema cevapları şimdi unutuluyor -- programı yeniden açmaya gerek yok.
    g = sonuc.get("goc") or {}
    veritabani_yenilendi(g)

    mesaj = (metinler.t("geri_yuklendi_ozet")
             .replace("{hasta}", str(sonuc.get("hasta")))
             .replace("{cycle}", str(sonuc.get("cycle")))
             .replace("{specimen}", str(sonuc.get("specimen")))
             .replace("{goruntu}", str(sonuc.get("goruntu"))))
    if g.get("calisti"):
        mesaj += " " + metinler.say("geri_yukleme_goc_uygulandi", len(g["calisti"]))
    if g.get("hatali"):
        mesaj += " " + metinler.t("geri_yukleme_goc_hata").replace(
            "{ad}", ", ".join(ad for ad, _ in g["hatali"]))
    return RedirectResponse("/yedekleme?gymesaj=" + quote(mesaj), status_code=303)


# Klasör gezgini (v6.43, kullanıcının isteği: "göz at şeklinde olsa").
#
# Uzun bir yolu elle yazmak zor ve tek harf yanlışsa kamera kuyruğu sessizce
# boş kalıyor. Ama tarayıcı sayfaya **gerçek dosya yolunu vermiyor**
# (`<input type="file">` ile seçilen klasörün tam yolu gizli), yani işletim
# sisteminin kendi "Klasör Seç" penceresi buradan açılamaz.
#
# Karşılığı sunucu tarafında gezinmek: program kendi çalıştığı makinenin
# klasörlerini listeliyor, kullanıcı tıklayarak iniyor. Aranan klasör zaten
# o makinede (mikroskop oraya yazıyor), telefonda değil.
#
# **Yalnızca klasör adları döner** — dosya adları değil, içerik hiç değil.
# Tek sayı geri veriliyor: bulunulan klasördeki fotoğraf sayısı. Kamera
# klasörünü bulmanın en kolay yolu o ("burada 37 fotoğraf var").

# Fotoğraf sayısı `goruntuler.UZANTILAR` ile sayılıyor -- ikinci bir liste
# yazsaydık kuyruğun aldığı dosyalarla gezginin saydığı dosyalar birbirinden
# ayrı düşerdi ("37 fotoğraf var" diyen klasörde kuyrukta 34 kare çıkardı).
EN_COK_KLASOR = 300          # devasa klasörde sayfa kilitlenmesin
EN_COK_SAYIM = 2000          # fotoğraf sayarken bu kadarında dur


def _surucu_kokleri():
    """Windows'ta sürücü harfleri, ötekinde kök. Gezginin en üst basamağı."""
    if os.name == "nt":
        return [f"{h}:\\" for h in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if os.path.isdir(f"{h}:\\")]
    return ["/"]


def _klasor_listesi(yol: Path):
    """(alt klasörler, fotoğraf sayısı). İzin verilmeyen klasörde boş döner."""
    alt, foto, tarandi = [], 0, 0
    try:
        with os.scandir(yol) as gz:
            for g in gz:
                try:
                    if g.name.startswith("."):
                        continue        # gizli klasörler gürültü yapıyor
                    if g.is_dir():
                        if len(alt) < EN_COK_KLASOR:
                            alt.append(g.name)
                    elif tarandi < EN_COK_SAYIM:
                        tarandi += 1
                        if (os.path.splitext(g.name)[1].lower()
                                in goruntuler.UZANTILAR):
                            foto += 1
                except OSError:
                    continue
    except OSError:
        return [], 0
    alt.sort(key=str.lower)
    return alt, foto


@uygulama.get("/klasorler/gozat")
def klasor_gozat(request: Request, yol: str = ""):
    """Bir klasörün alt klasörleri. Yalnızca yönetici."""
    red = yonetici_kontrol(request)
    if red:
        return red

    # Yol boşsa ya da okunamıyorsa makul bir yerden başla: önce kayıtlı
    # kamera klasörü, o da yoksa kullanıcının ev klasörü.
    ham = (yol or "").strip()
    if ham == "*":                       # gezginin en üst basamağı
        return JSONResponse({"yol": "", "ust": None, "kok": True,
                             "klasorler": _surucu_kokleri(), "fotograf": 0})
    try:
        p = Path(ham).expanduser() if ham else Path.home()
        p = p.resolve()
    except (OSError, ValueError, RuntimeError):
        p = Path.home()
    if not p.is_dir():
        p = Path.home()

    alt, foto = _klasor_listesi(p)
    ust = str(p.parent) if p.parent != p else None
    return JSONResponse({"yol": str(p), "ust": ust, "kok": False,
                         "klasorler": alt, "fotograf": foto})


# ---------------------------------------------- işletim sisteminin penceresi
#
# Kullanıcının isteği (v6.44): "gözata basınca işletim sisteminin kendi
# ekranında bulalım". Pencere açılıyor, ama tarayıcı seçilen klasörün
# **nerede olduğunu söylemiyor** -- güvenlik kuralı, `C:\fakepath` diye sahte
# bir yol veriyor; Chrome'un `showDirectoryPicker` API'si de yalnızca adı
# veriyor. Bu bir ayar değil, geçilemiyor.
#
# O yüzden ikinci adım burada: tarayıcı klasörün **adını ve içindeki dosya
# adlarını** gönderiyor, program kendi makinesinde o klasörü arıyor. Ad
# tutması yetmiyor -- içindeki dosyalardan en az biri de yerinde olmalı,
# yoksa aynı adlı başka bir klasör seçilebilirdi.
#
# Bulamazsa ekran listeli gezgine düşüyor; o her yerde çalışıyor.

ARAMA_SURESI = 4.0           # saniye; bulunamazsa listeye düşülüyor
ARAMA_EN_COK_KLASOR = 40000  # gezilecek klasör tavanı
ARAMA_EN_COK_ADAY = 8

# Aramanın girmediği yerler: ya devasa ya da kamera klasörü olamaz.
ARAMA_ATLA = {
    "windows", "program files", "program files (x86)", "programdata",
    "$recycle.bin", "system volume information", "node_modules",
    "__pycache__", "proc", "sys", "dev", "snap",
}


def _arama_kokleri():
    """Aranacak yerler, olasılık sırasıyla: önce ev, sonra sürücüler."""
    kokler, gorulen = [], set()
    surucu = _surucu_kokleri() if os.name == "nt" else []
    for y in [Path.home(), db.VERI_KOK] + [Path(k) for k in surucu] + \
             [Path("/Volumes"), Path("/media"), Path("/mnt")]:
        try:
            if y.is_dir() and str(y) not in gorulen:
                gorulen.add(str(y))
                kokler.append(y)
        except OSError:
            continue
    return kokler


def _klasoru_ara(ad: str, ornekler: list):
    """Adı `ad` olan ve içinde `ornekler`den biri bulunan klasörleri arar."""
    import time
    bitis = time.monotonic() + ARAMA_SURESI
    hedef = ad.lower()
    adaylar, sayac, zaman_doldu = [], 0, False

    for kok in _arama_kokleri():
        for dizin, altlar, _ in os.walk(kok, onerror=lambda e: None):
            sayac += 1
            if sayac > ARAMA_EN_COK_KLASOR or time.monotonic() > bitis:
                zaman_doldu = True
                break
            # Gezilmeyecek dalları listeden çıkarmak `os.walk`'a oraya hiç
            # girmemesini söylüyor -- asıl hızlanma burada.
            altlar[:] = [a for a in altlar
                         if not a.startswith(".") and a.lower() not in ARAMA_ATLA]
            if os.path.basename(dizin).lower() != hedef:
                continue
            if any((Path(dizin) / o).exists() for o in ornekler):
                if dizin not in adaylar:
                    adaylar.append(dizin)
                if len(adaylar) >= ARAMA_EN_COK_ADAY:
                    return adaylar, False
        if zaman_doldu or len(adaylar) >= ARAMA_EN_COK_ADAY:
            break
    return adaylar, zaman_doldu


@uygulama.post("/klasorler/bul")
async def klasor_bul(request: Request):
    """Tarayıcının verdiği klasör adını bu makinede arar. Yalnızca yönetici."""
    red = yonetici_kontrol(request)
    if red:
        return red
    try:
        gelen = await request.json()
    except ValueError:
        return JSONResponse({"adaylar": [], "sebep": "okunamadi"})

    ad = str(gelen.get("ad") or "").strip()
    # Ad tek bir klasör adı olmalı: yol ayıracı gelmiş olamaz.
    if not ad or len(ad) > 120 or "/" in ad or "\\" in ad or ad in (".", ".."):
        return JSONResponse({"adaylar": [], "sebep": "okunamadi"})

    ornekler = []
    for o in (gelen.get("dosyalar") or [])[:5]:
        o = str(o).replace("\\", "/").strip("/")
        if o and ".." not in o.split("/"):
            ornekler.append(o)
    if not ornekler:
        # Boş klasör seçilmiş: tarayıcı hiçbir dosya adı vermiyor, aramanın
        # doğrulayacak bir şeyi yok.
        return JSONResponse({"adaylar": [], "sebep": "bos"})

    adaylar, zaman_doldu = _klasoru_ara(ad, ornekler)
    return JSONResponse({"adaylar": adaylar,
                         "sebep": "" if adaylar else
                                  ("sure" if zaman_doldu else "yok")})


@uygulama.post("/klasorler")
def klasorler_kaydet(request: Request,
                     goruntu_kaynak_klasor: str = Form(""),
                     goruntu_arsiv_klasor: str = Form(""),
                     yedek_klasor: str = Form("")):
    """Üç klasörün üçü de farklı davranıyor, sebepleri farklı.

    - **Kamera klasörünü program yalnızca okur**; oraya kareleri mikroskop
      yazıyor. Var olmayan bir yol kabul edilmiyor: yoksa yazım hatasıdır ve
      kuyruk aylarca boş görünür. Klasörü açmak işe yaramaz, kamera oraya
      yazmıyor olurdu.
    - **Arşive program yazıyor**, o yüzden yoksa oluşturuluyor.
    - **Yedek klasörü olduğu gibi kaydediliyor**, oluşturulmuyor: çoğu zaman
      takılı olmayan bir disk (klinikte `E:`). Mac'te `E:\yedek` adında klasör
      açmak v6.8'de başa geldi; `yedek.py` yolu çalışma anında doğruluyor.
    """
    red = yonetici_kontrol(request)
    if red:
        return red

    kamera = goruntu_kaynak_klasor.strip()
    arsiv = goruntu_arsiv_klasor.strip()
    yedek = yedek_klasor.strip()

    if kamera and not Path(kamera).is_dir():
        return RedirectResponse("/klasorler?hata=klasor_hata_kamera",
                                status_code=303)
    if arsiv:
        try:
            Path(arsiv).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            _gunluk.error("arsiv klasoru olusturulamadi: %s", e)
            return RedirectResponse("/klasorler?hata=klasor_hata_arsiv",
                                    status_code=303)

    db.yerel_yaz({"goruntu_kaynak_klasor": kamera,
                  "goruntu_arsiv_klasor": arsiv,
                  "yedek_klasor": yedek})
    return RedirectResponse("/klasorler?kaydedildi=1", status_code=303)


def kod_surumu():
    """Diskteki programın sürümü: README'deki en büyük "# v6.xxx" başlığı.

    `git pull` yeni kodu diske koyar ama çalışan program eski Python'la devam
    eder (tuzak #5) -- kullanıcı "hâlâ eskisi gibi" der, sebep görünmez
    (v6.162: ART Lab'da "+2 tüp"). Açılışta okunan (`CALISAN_SURUM`) ile şu
    an diskteki farklıysa Yönetici paneli "yeniden başlat" diyor. README
    paketlenmiş kurulumda yoksa None: panel satırı basmıyor.
    """
    try:
        metin_ = (KOK / "README.md").read_text(encoding="utf-8")
    except OSError:
        return None
    surumler = [tuple(int(x) for x in m.groups())
                for m in re.finditer(r"^# v(\d+)\.(\d+)\b", metin_, re.M)]
    return "v%d.%d" % max(surumler) if surumler else None


CALISAN_SURUM = kod_surumu()


@uygulama.get("/yonetim")
def yonetim_ekran(request: Request):
    """Yönetici paneli — sistemin durumu tek ekranda, hepsi salt okunur.

    Buradan hiçbir şey silinmez veya değiştirilmez; ayarlar yine kendi
    ekranlarından/scriptlerinden yapılır. Amaç "her şey yolunda mı" sorusunu
    terminale inmeden yanıtlamak (README v6.12).
    """
    red = yonetici_kontrol(request)
    if red:
        return red

    boyut = None
    try:
        boyut = db.DB_YOLU.stat().st_size / 1024 / 1024
    except OSError:
        pass

    sayilar = []
    for tablo, ad in [("hasta", "Hasta"), ("cycle", "Tedavi"),
                      ("specimen", "Örnek (yumurta/embriyo)"), ("goruntu", "Fotoğraf"),
                      ("olay", "Olay"), ("degisiklik_log", "Değişiklik kaydı")]:
        try:
            sayilar.append({"ad": ad,
                            "n": db.tek(f"SELECT COUNT(*) n FROM {tablo}")["n"]})
        except sqlite3.Error:
            pass

    try:
        kirik = len(db.sorgu("PRAGMA foreign_key_check"))
    except sqlite3.Error:
        kirik = None

    yollar = []
    for anahtar, ad in [("goruntu_kaynak_klasor", "Kamera klasörü (snapshot)"),
                        ("goruntu_arsiv_klasor", "Arşiv"),
                        ("yedek_klasor", "Yedek")]:
        yol = db.ayar(anahtar, "")
        yollar.append({"ad": ad, "yol": yol,
                       "var": bool(yol) and Path(yol).is_dir()})

    kullanicilar = db.sorgu(
        "SELECT rol, aktif_mi, COUNT(*) n FROM kullanici WHERE lab_id = ? "
        "GROUP BY rol, aktif_mi", (db.LAB_ID,))

    return sablon.TemplateResponse(
        request, "yonetim.html",
        {"kullanici": request.state.kullanici,
         "yedek": yedek_durumu(),
         "son_yedek": _ayar("son_yedek", ""),
         "yedek_uyari_gun": _ayar("yedek_uyari_gun", "3"),
         "db_boyut": boyut, "db_yolu": str(db.DB_YOLU),
         # Açılışta çalışan göçlerin sonucu (v6.49). Panel salt okunur:
         # yalnızca gösteriyor, buradan bir şey çalıştırılmıyor.
         "goc": GOC_SONUCU, "goc_bekleyen": goc.bekleyenler(),
         "sayilar": sayilar, "kirik": kirik, "yollar": yollar,
         "makine": db.MAKINE,
         "toplam_kullanici": sum(r["n"] for r in kullanicilar),
         "aktif_kullanici": sum(r["n"] for r in kullanicilar if r["aktif_mi"]),
         "yonetici_sayisi": aktif_yonetici_sayisi(),
         "sifre_istegi": len(bekleyen_sifre_istekleri()),
         "calisan_surum": CALISAN_SURUM, "diskteki_surum": kod_surumu()})


@uygulama.get("/kullanicilar")
def kullanicilar_ekran(request: Request, hata: str = "", bilgi: str = ""):
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(
        request, "kullanicilar.html",
        {"kullanici": request.state.kullanici,
         "liste": db.sorgu(
             "SELECT id, kullanici_adi, ad_soyad, kisa_kod, rol, aktif_mi "
             "FROM kullanici WHERE lab_id = ? ORDER BY aktif_mi DESC, "
             "kullanici_adi", (db.LAB_ID,)),
         "yonetici_sayisi": aktif_yonetici_sayisi(),
         "roller": [(k, ROL_ADI[k]) for k in ROLLER],
         "moduller": MODULLER,
         "yetki_goc_gerekli": not yetki_tablosu_var(),
         "yetkiler": _kullanici_yetki_haritasi(),
         "min_sifre": MIN_SIFRE, "hata": hata, "bilgi": bilgi,
         "sifre_istegi": len(bekleyen_sifre_istekleri())})


# ------------------------------------- yönetici: bekleyen şifre istekleri
#
# Kullanıcının kararı (2026-09-12): personel şifresini kendisi değiştirsin ama
# yönetici onaylayınca geçsin. İstek `/sifre`'de oluşuyor (mevcut şifreyle
# kimlik kanıtlanmış halde), burada yalnızca karar veriliyor.
#
# Rota adlarında `sil` YOK: `yol_modulu()` `sil` ile biten yolu "silme"
# modülüne bağlıyor, o da bu işi silme izni olmayan yöneticiden saklardı.

@uygulama.get("/sifre-istekleri")
def sifre_istekleri_ekran(request: Request, bilgi: str = ""):
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(
        request, "sifre_istekleri.html",
        {"kullanici": request.state.kullanici,
         "liste": bekleyen_sifre_istekleri(),
         "goc_gerekli": not sifre_istegi_tablosu_var(),
         "bilgi": bilgi})


def _bekleyen_istek(iid: int):
    if not sifre_istegi_tablosu_var():
        return None
    return db.tek(
        "SELECT i.*, k.kullanici_adi FROM sifre_istegi i "
        "JOIN kullanici k ON k.id = i.kullanici_id "
        "WHERE i.id = ? AND i.lab_id = ? AND i.durum = 'bekliyor'",
        (iid, db.LAB_ID))


@uygulama.post("/sifre-istekleri/{iid}/onayla")
def sifre_istegi_onayla(request: Request, iid: int):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    istek = _bekleyen_istek(iid)
    if not istek:
        return RedirectResponse("/sifre-istekleri", status_code=303)
    # Hash zaten hazır — düz metin hiçbir yerde durmuyor. `sifre_yaz()`
    # kullanılamaz, o düz metin bekliyor; oturum düşürmeyi burada elle yap
    # (şifre değişince açık oturumlar kapanır, README v6.11).
    db.yaz("UPDATE kullanici SET sifre_hash = ? WHERE id = ?",
           (istek["yeni_hash"], istek["kullanici_id"]))
    db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (istek["kullanici_id"],))
    db.yaz("UPDATE sifre_istegi SET durum = 'onaylandi', karar_veren_id = ?, "
           "karar_zamani = datetime('now') WHERE id = ?",
           (request.state.kullanici["id"], iid))
    _gunluk.info("sifre istegi onaylandi: %s", istek["kullanici_adi"])
    mesaj = metinler.t("sifre_onaylandi").format(kim=istek["kullanici_adi"])
    return RedirectResponse(f"/sifre-istekleri?bilgi={quote(mesaj)}",
                            status_code=303)


@uygulama.post("/sifre-istekleri/{iid}/reddet")
def sifre_istegi_reddet(request: Request, iid: int):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    istek = _bekleyen_istek(iid)
    if not istek:
        return RedirectResponse("/sifre-istekleri", status_code=303)
    db.yaz("UPDATE sifre_istegi SET durum = 'reddedildi', karar_veren_id = ?, "
           "karar_zamani = datetime('now') WHERE id = ?",
           (request.state.kullanici["id"], iid))
    _gunluk.info("sifre istegi reddedildi: %s", istek["kullanici_adi"])
    mesaj = metinler.t("sifre_reddedildi").format(kim=istek["kullanici_adi"])
    return RedirectResponse(f"/sifre-istekleri?bilgi={quote(mesaj)}",
                            status_code=303)


@uygulama.post("/kullanicilar/yeni")
async def kullanici_yeni(request: Request):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())

    def hata(m):
        # Her ret gunluge de dusuyor: "ekleyemiyorum" diyen kullanicinin
        # ekraninda mesaj gorunmediginde tek kanit `program.log` oluyor.
        _gunluk.info("kullanici eklenemedi: %s", m)
        return RedirectResponse(f"/kullanicilar?hata={quote(m)}", status_code=303)

    ad = (f.get("ad_soyad") or "").strip()
    kadi = (f.get("kullanici_adi") or "").strip().lower()
    if not ad:
        return hata("Ad soyad boş olamaz.")
    if not kadi:
        return hata("Kullanıcı adı boş olamaz.")
    if not kadi.isascii() or not kadi.replace(".", "").replace("_", "").isalnum():
        return hata("Kullanıcı adı sadece harf, rakam, nokta ve alt çizgi "
                    "içerebilir (Türkçe karakter kullanma).")
    if db.tek("SELECT 1 FROM kullanici WHERE lab_id = ? AND kullanici_adi = ?",
              (db.LAB_ID, kadi)):
        return hata(f"'{kadi}' zaten kullanılıyor.")

    m = sifre_gecerli(f.get("sifre") or "", f.get("sifre2") or "")
    if m:
        return hata(m)

    rol = "yonetici" if (f.get("rol") or "") == "yonetici" else "embriyolog"
    kod = ((f.get("kisa_kod") or "").strip() or ad[:2]).upper()
    # `kullanici_adi` semada LAB'DAN BAGIMSIZ olarak UNIQUE, yukaridaki
    # kontrol ise `lab_id`'ye gore bakiyor. Iki lab satiri olan bir
    # veritabaninda kontrol gecer, INSERT patlar ve ekran cirilciplak 500
    # verir. Yakala, sebebini yaz (tuzak: sessiz basarisizlik).
    try:
        yeni_id = db.yaz(
            "INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, "
            "kullanici_adi, sifre_hash) VALUES (?,?,?,?,?,?)",
            (db.LAB_ID, ad, kod, rol, kadi, guvenlik.sifrele(f.get("sifre"))))
    except sqlite3.IntegrityError:
        return hata(f"'{kadi}' bu veritabaninda zaten var.")
    except sqlite3.Error as e:
        _gunluk.exception("kullanici INSERT hatasi")
        return hata(f"Kullanici kaydedilemedi: {e}")
    tum_yetkileri_ver(yeni_id)
    _gunluk.info("kullanici eklendi: %s (id=%s, rol=%s)", kadi, yeni_id, rol)
    return RedirectResponse(
        f"/kullanicilar?bilgi={quote(kadi + ' eklendi.')}", status_code=303)


@uygulama.post("/kullanici/{kid}/duzenle")
async def kullanici_duzenle(request: Request, kid: int):
    """Var olan kullanıcının adını ve kullanıcı adını değiştirir (v6.106).

    Doğrulama kuralları `kullanici_yeni()` ile aynı -- ayrı bir kopya değil,
    aynı satırlar burada da geçerli olduğu için tekrarlandı.
    """
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/kullanicilar?hata={quote(m)}", status_code=303)

    ad = (f.get("ad_soyad") or "").strip()
    kadi = (f.get("kullanici_adi") or "").strip().lower()
    if not ad:
        return hata("Ad soyad boş olamaz.")
    if not kadi:
        return hata("Kullanıcı adı boş olamaz.")
    if not kadi.isascii() or not kadi.replace(".", "").replace("_", "").isalnum():
        return hata("Kullanıcı adı sadece harf, rakam, nokta ve alt çizgi "
                    "içerebilir (Türkçe karakter kullanma).")
    if kadi != k["kullanici_adi"] and db.tek(
            "SELECT 1 FROM kullanici WHERE lab_id = ? AND kullanici_adi = ? "
            "AND id != ?", (db.LAB_ID, kadi, kid)):
        return hata(f"'{kadi}' zaten kullanılıyor.")

    eski_ad = k["ad_soyad"]
    try:
        db.yaz("UPDATE kullanici SET ad_soyad = ?, kullanici_adi = ? WHERE id = ?",
               (ad, kadi, kid))
    except sqlite3.IntegrityError:
        # `kullanici_adi` şemada LAB'DAN BAĞIMSIZ UNIQUE (kullanici_yeni()'deki
        # tuzak burada da geçerli) -- yukarıdaki kontrol yalnızca bu lab'a
        # bakıyor, iki lab satırı olan bir veritabanında yine de çarpışabilir.
        return hata(f"'{kadi}' bu veritabanında zaten var.")

    # Ad değiştiyse hasta kayıtlarındaki "İşlemi Yapan" da güncellensin
    # (kullanıcının isteği): `islem_yapan.yapan_ad` ve `sperm_dondurma.
    # yapan_ad` kullaniciyi FK ile değil, o anki adın metin kopyasıyla
    # tutuyor (v6.99/v6.101'in bilinçli kararı) -- ad değişince eski
    # metin kendiliğinden güncellenmez, elle taşınması gerekiyor.
    if ad != eski_ad:
        db.yaz("UPDATE islem_yapan SET yapan_ad = ? WHERE lab_id = ? "
               "AND yapan_ad = ?", (ad, db.LAB_ID, eski_ad))
        db.yaz("UPDATE sperm_dondurma SET yapan_ad = ? WHERE lab_id = ? "
               "AND yapan_ad = ?", (ad, db.LAB_ID, eski_ad))

    _gunluk.info("kullanici duzenlendi: id=%s ad='%s' kadi='%s'", kid, ad, kadi)
    return RedirectResponse(
        f"/kullanicilar?bilgi={quote(kadi + ': ad ve kullanıcı adı güncellendi.')}",
        status_code=303)


@uygulama.post("/kullanici/{kid}/sifre")
async def kullanici_sifre_sifirla(request: Request, kid: int):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/kullanicilar?hata={quote(m)}", status_code=303)

    m = sifre_gecerli(f.get("sifre") or "", f.get("sifre2") or "")
    if m:
        return hata(f"{k['kullanici_adi']}: {m}")

    sifre_yaz(kid, f.get("sifre"))
    mesaj = (f"{k['kullanici_adi']} kullanıcısının şifresi değiştirildi, "
             "açık oturumları kapatıldı.")
    if not k["aktif_mi"]:
        mesaj += " Kullanıcı PASİF olduğu için yine de giriş yapamaz."
    if kid == request.state.kullanici["id"]:
        yanit = RedirectResponse("/giris?sifre=1", status_code=303)
        yanit.delete_cookie(guvenlik.CEREZ_ADI)
        return yanit
    return RedirectResponse(f"/kullanicilar?bilgi={quote(mesaj)}", status_code=303)


@uygulama.post("/kullanici/{kid}/durum")
async def kullanici_durum(request: Request, kid: int):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/kullanicilar?hata={quote(m)}", status_code=303)

    ac = (f.get("eylem") or "") == "aktif"
    if not ac:
        # Kilitlenme koruması: son yöneticiyi kapatan kimse kalmaz.
        if kid == request.state.kullanici["id"]:
            return hata("Kendi hesabını pasif yapamazsın.")
        if k["rol"] == "yonetici" and aktif_yonetici_sayisi() <= 1:
            return hata("Tek yönetici bu — pasif yapılırsa kullanıcı yönetimi "
                        "ekranına kimse giremez. Önce başka bir yönetici ekle.")

    db.yaz("UPDATE kullanici SET aktif_mi = ? WHERE id = ?",
           (1 if ac else 0, kid))
    if not ac:
        db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (kid,))
        mesaj = (f"{k['kullanici_adi']} pasif yapıldı, açık oturumları "
                 "kapatıldı. Girdiği kayıtlar duruyor.")
    else:
        mesaj = f"{k['kullanici_adi']} tekrar giriş yapabilir."
    return RedirectResponse(f"/kullanicilar?bilgi={quote(mesaj)}", status_code=303)


@uygulama.post("/kullanici/{kid}/yetki")
async def kullanici_yetki(request: Request, kid: int):
    """Bir kullanıcının modül izinlerini toptan yazar.

    Form işaretli kutuları gönderir; işaretsizler hiç gelmez. Bu yüzden önce
    hepsi silinip işaretliler yazılıyor — "kaldırılan izin" ayrı bir istek
    olarak gelmiyor (v6.14).
    """
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    if not yetki_tablosu_var():
        return RedirectResponse(
            "/kullanicilar?hata=" + quote("Önce 'python3 goc_026.py' çalıştır."),
            status_code=303)

    f = await request.form()
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    secili = [m for m in f.getlist("modul") if m in MODUL_KODLARI]
    with db.yazma_islemi() as b:
        b.execute("DELETE FROM yetki WHERE kullanici_id = ?", (kid,))
        for m in secili:
            b.execute("INSERT INTO yetki (lab_id, kullanici_id, modul) "
                      "VALUES (?,?,?)", (db.LAB_ID, kid, m))

    mesaj = (f"{k['kullanici_adi']}: {len(secili)} / {len(MODULLER)} modüle "
             "erişebilir.")
    if k["rol"] == "yonetici":
        mesaj += " (Yönetici olduğu için yine her yere girer.)"
    return RedirectResponse(f"/kullanicilar?bilgi={quote(mesaj)}", status_code=303)


@uygulama.post("/kullanici/{kid}/rol")
async def kullanici_rol(request: Request, kid: int):
    """Rolü değiştirir. Son aktif yöneticinin rolü düşürülemez.

    Yönetici olmayan biri bu ekranı göremez; son yönetici de embriyolog
    yapılırsa kimse giremez ve tek çıkış terminaldeki `kullanici.py` olurdu
    (README v6.13).
    """
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/kullanicilar?hata={quote(m)}", status_code=303)

    yeni_rol = (f.get("rol") or "").strip()
    # Değişmemiş rolü önce eleyelim: `rol` serbest metin bir kolon, eski
    # kayıtlarda `androlog` gibi tanımsız değerler olabiliyor. Kullanıcı
    # seçiciye dokunmadan kaydederse bu bir hata değil, hiçbir şey yapmamalı.
    if yeni_rol == k["rol"]:
        return RedirectResponse("/kullanicilar", status_code=303)
    if yeni_rol not in ROLLER:
        return hata("Geçersiz rol.")
    if (k["rol"] == "yonetici" and k["aktif_mi"]
            and aktif_yonetici_sayisi() <= 1):
        return hata("Tek aktif yönetici bu. Rolü düşürülürse yönetim "
                    "ekranlarına kimse giremez. Önce başka bir yönetici yap.")

    db.yaz("UPDATE kullanici SET rol = ? WHERE id = ?", (yeni_rol, kid))
    mesaj = f"{k['kullanici_adi']}: {ROL_ADI.get(yeni_rol, yeni_rol)} yapıldı."
    if kid == request.state.kullanici["id"] and yeni_rol != "yonetici":
        # Kendi yöneticiliğini bıraktı — bu ekrana artık giremez.
        return RedirectResponse("/hastalar", status_code=303)
    return RedirectResponse(f"/kullanicilar?bilgi={quote(mesaj)}", status_code=303)


@uygulama.get("/kullanici/{kid}/sil")
def kullanici_sil_ekran(request: Request, kid: int, hata: str = ""):
    red = yonetici_kontrol(request)
    if red:
        return red
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)
    kayitlar = kullanici_kayitlari(kid)
    return sablon.TemplateResponse(
        request, "kullanici_sil.html",
        {"kullanici": request.state.kullanici, "k": k, "kayitlar": kayitlar,
         "kendisi": kid == request.state.kullanici["id"],
         "son_yonetici": k["rol"] == "yonetici" and aktif_yonetici_sayisi() <= 1,
         "hata": hata})


@uygulama.post("/kullanici/{kid}/sil")
async def kullanici_sil(request: Request, kid: int):
    from urllib.parse import quote
    red = yonetici_kontrol(request)
    if red:
        return red
    f = dict(await request.form())
    k = db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND id = ?",
               (db.LAB_ID, kid))
    if not k:
        return RedirectResponse("/kullanicilar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/kullanici/{kid}/sil?hata={quote(m)}",
                                status_code=303)

    if kid == request.state.kullanici["id"]:
        return hata("Kendi hesabını silemezsin.")
    if k["rol"] == "yonetici" and aktif_yonetici_sayisi() <= 1:
        return hata("Tek yönetici bu — silinirse kullanıcı yönetimine kimse "
                    "giremez. Önce başka bir yönetici ekle.")
    if (f.get("onay") or "").strip().lower() != k["kullanici_adi"]:
        return hata("Kullanıcı adı doğru yazılmadı.")
    if (f.get("onay2") or "").strip().upper() != "SIL":
        return hata("Kalıcı silme için ikinci kutuya SIL yazılmalı.")

    kayitlar = kullanici_kayitlari(kid)
    if kayitlar:
        toplam = sum(x["sayi"] for x in kayitlar)
        return hata(f"Bu kullanıcının {toplam} kaydı var; kalıcı silinemez. "
                    "Pasif yap — kayıtlar kime ait olduğunu kaybetmesin.")

    db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (kid,))
    # `yetki` bir kayıt değil, izin ataması — KULLANICI_KAYITLARI'nda bilerek
    # yok (silmeyi engellemesin), ama FK'sı var: temizlenmezse her yeni
    # kullanıcının `tum_yetkileri_ver()` ile aldığı satırlar yüzünden bu
    # DELETE'in kendisi FOREIGN KEY hatasıyla patlar (v6.100'de bulundu).
    # `goc_026` çalışmamışsa tablo hiç yok (tuzak #3) — o zaman atla.
    if yetki_tablosu_var():
        db.yaz("DELETE FROM yetki WHERE kullanici_id = ?", (kid,))
    db.yaz("DELETE FROM kullanici WHERE id = ?", (kid,))
    return RedirectResponse(
        f"/kullanicilar?bilgi={quote(k['kullanici_adi'] + ' kalıcı olarak silindi.')}",
        status_code=303)


def yedek_durumu():
    """Son yedek eskiyse uyarı metni döndürür, sorun yoksa None."""
    son = _ayar("son_yedek", "")
    sinir = int(_ayar("yedek_uyari_gun", "3") or 3)
    if not son:
        return "Henüz hiç yedek alınmadı. yedek.py çalıştırılmalı."
    try:
        t = _dt.fromisoformat(son)
    except ValueError:
        return None
    gun = (_dt.now() - t).days
    if gun >= sinir:
        return (f"Son yedek {gun} gün önce alındı ({gg_aa_yyyy_saat(son)}). "
                "Yedekleme çalışmıyor olabilir.")
    return None


# ----------------------------------------------------------------- hasta

# Bir cycle'ın nasıl bittiği. Kullanıcının kâğıt klasöründeki üç son:
# embriyolar donduruldu, transfer yapıldı, tedavi iptal oldu (v6.28).
# Dondurma ve transfer `durum='tamamlandi'` yapar; iptal, silme ekranından
# beri var olan `durum='iptal'` değerini kullanır — "Geri al" akışı aynı kalsın.
#
# İptalin altı ayrıntılı sebebi (v6.103, kullanıcının isteği) — hepsi aynı
# şekilde `durum='iptal'` yapıyor, yalnızca hangi aşamada durduğunu
# ayırt ediyor. Genel "İptal" seçeneği **kaldırılmadı**: listede olmayan
# bir sebep için hâlâ kullanılabilir (kullanıcının kararı).
IPTAL_DETAY_SEBEPLERI = (
    "yumurta_cikmadi", "immatur_yumurta", "fert_olmadi",
    "pn_arrest", "cleavage_arrest", "gun5_arrest",
)
BITIS_DURUMU = {"dondurma": "tamamlandi", "transfer": "tamamlandi",
                "iptal": "iptal",
                **{k: "iptal" for k in IPTAL_DETAY_SEBEPLERI}}

# Ana ekrandaki "Yaklaşanlar" kaç gün ileriye baksın (v6.33). İki hafta:
# "haftaya" diye plan yapılıyor, bir hafta dar kalırdı. Ayrı bir "tümünü
# gör" ekranı yok (v6.65'te /takvim kaldırıldı) -- kart kendi penceresini
# gösteriyor.
YAKLASAN_GUN = 14


def _bitis_kolonu_var() -> bool:
    """goc_027 çalıştırıldı mı? (tuzak #3: çalıştırıldığını varsayma)"""
    return any(r["name"] == "bitis_sebebi"
               for r in db.sorgu("PRAGMA table_info(cycle)"))


def _opu_gunu(opu_zamani):
    """OPU'dan bu yana geçen gün (OPU günü = 0). Tarih bozuksa None.

    Bir cycle'da OPU tarihi `0026-09-04` yazıyor (bekleyen iş 6); böyle bir
    değer yüzünden bütün liste patlamasın diye hesap korumalı.
    """
    if not opu_zamani:
        return None
    try:
        gun = _dt.fromisoformat(str(opu_zamani)).date()
        fark = (_dt.now().date() - gun).days
    except (ValueError, TypeError, OverflowError):
        return None
    return fark if 0 <= fark <= 400 else None


def cycle_listesi(bitmis: bool = False, bugun: bool = False, ay: str = "",
                  yaklasan: int = 0, plan_ay: str = "",
                  limit: int = 0, offset: int = 0, sayisi: bool = False):
    """Cycle listesi — bütün liste ekranları bunu kullanıyor.

    - `bitmis=False` laboratuvarda işi süren cycle'lar: ana ekranın
      "Yapılacaklar"ı, kullanıcının kâğıt klasörünün karşılığı (v6.28).
    - `bitmis=True` bitmiş olanlar: `/bitenler` arşivi.
    - `bugun=True` yalnızca **bugün** bitirilenler — ana ekrandaki "Bugün
      bitenler" kartı her gün kendiliğinden boşalsın diye (v6.29). Ölçü
      `date('now','localtime')`; sunucu klinikte, yerel gün doğru olan.
    - `ay="2026-09"` o ayda **işlem yapılan** cycle'lar: hasta kayıtları
      ekranı (v6.29). Ölçü OPU tarihi, yoksa cycle'ın açıldığı tarih —
      FET'te OPU olmuyor.
    - `yaklasan=14` planlanan tarihi **bugünden sonraki** 14 gün içinde olan
      cycle'lar: ana ekranın "Yaklaşanlar" kartı (v6.33).
    - `plan_ay="2026-09"` o ayda **planlanmış** cycle'lar. **Kullanılmıyor**
      (v6.65'te takvim ekranı kaldırıldı) — kod bilerek duruyor, geri
      dönülürse diye; çağıran yok.
    - `limit`/`offset` sayfalama için (v6.88, yalnızca `ay` modunda
      kullanılıyor — `/hastalar`). `limit=0` (varsayılan) sınırsız demek,
      öteki çağıranların hiçbiri bunu vermiyor, davranışları değişmedi.
    - `sayisi=True` satırları değil, **toplam sayıyı** döndürür (sayfa
      sayısını hesaplamak için) — aynı `kosullar` üzerinden, ikinci bir
      sorgu yazmaya gerek kalmadı.

    Arşivlenmiş hastanın cycle'ı ilk üçünde görünmez (hasta arşivi "bu dosya
    kapandı" demek), ama **ay listesinde görünür**: o iş o ay yapıldı, sonra
    dosyanın kapanmış olması onu yapılmamış saymaz.

    Sıra: **hepsinde en yeni üstte**. Yapılacaklar v6.137'ye kadar en eski
    OPU'yu üste alıyordu (v6.28: "unutulan bir cycle dibe düşüp gözden
    kaybolmasın"); kullanıcı tersini istedi ("hastaları yeniden eskiye doğru
    diz") — günlük iş en yeni hastada, her sabah listenin dibine inmek
    istemiyor. Eski gerekçe tümden geçersiz değil: kart 5 satır gösteriyor
    (v6.78), en eskiler artık "Tümü" (`/devam-eden`) sayfasında kalıyor.
    """
    kolon_var = _bitis_kolonu_var()
    plan_var = _planlanan_kolonu_var()
    if bugun and not kolon_var:
        return []                  # goc_027 yok: "bugün" süzgeci kurulamıyor
    if (yaklasan or plan_ay) and not plan_var:
        return []                  # goc_028 yok: takvim kurulamıyor
    planli = bool(yaklasan or plan_ay)
    durumlar = ("tamamlandi", "iptal") if (bitmis or bugun) else ("aktif",)
    kosullar = ["c.lab_id = ?"]
    parametre = [db.LAB_ID]
    if ay:
        kosullar.append(
            "strftime('%Y-%m', COALESCE(c.opu_zamani, c.olusturma_zamani)) = ?")
        parametre.append(ay)
    elif plan_ay:
        kosullar.append("strftime('%Y-%m', c.planlanan_tarih) = ?")
        parametre.append(plan_ay)
    else:
        kosullar.append("h.durum = 'aktif'")
        kosullar.append("c.durum IN (%s)" % ",".join("?" * len(durumlar)))
        parametre += list(durumlar)
    if yaklasan:
        # Bugün **dahil değil**: tarihi gelen cycle zaten Yapılacaklar'da.
        kosullar.append(
            "date(c.planlanan_tarih) > date('now','localtime') AND "
            "date(c.planlanan_tarih) <= date('now','localtime',?)")
        parametre.append(f"+{int(yaklasan)} days")
    if bugun:
        kosullar.append("date(c.bitis_zamani) = date('now','localtime')")
    # Planlanan tarihi gelecekte olan cycle Yapılacaklar'da görünmez: haftaya
    # olacak bir iş bu hafta boyunca her sabah listeyi şişirirdi (v6.33).
    # Tarih gelince kendiliğinden düşüyor.
    if plan_var and not (ay or plan_ay or bitmis or bugun or yaklasan):
        kosullar.append("(c.planlanan_tarih IS NULL OR "
                        "date(c.planlanan_tarih) <= date('now','localtime'))")

    if sayisi:
        satir = db.tek(
            f"SELECT COUNT(*) k FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
            f"WHERE {' AND '.join(kosullar)}", parametre)
        return satir["k"]

    bitis = ("c.bitis_sebebi, c.bitis_zamani" if kolon_var
             else "NULL AS bitis_sebebi, NULL AS bitis_zamani")
    plan = "c.planlanan_tarih" if plan_var else "NULL AS planlanan_tarih"
    if planli:
        sira = "c.planlanan_tarih, h.ad_soyad"   # takvim ileri doğru okunur
    elif ay:
        sira = "COALESCE(c.opu_zamani, c.olusturma_zamani) DESC"
    elif bitmis or bugun:
        sira = "COALESCE(c.bitis_zamani, c.olusturma_zamani) DESC"
    else:
        sira = "COALESCE(c.opu_zamani, c.olusturma_zamani) DESC"
    sinir = ""
    if limit:
        sinir = " LIMIT ? OFFSET ?"
        parametre = parametre + [limit, offset]
    satirlar = db.sorgu(
        f"""SELECT c.id, c.cycle_no, c.cycle_tipi, c.durum, c.opu_zamani,
                   c.olusturma_zamani, {bitis}, {plan},
                   h.id AS hasta_id, h.ad_soyad, h.dosya_no,
                   h.durum AS hasta_durum,
                   (SELECT o.tip FROM olay o
                     WHERE o.cycle_id = c.id AND o.iptal_mi = 0
                     ORDER BY o.zaman DESC, o.id DESC LIMIT 1) AS son_olay
              FROM cycle c JOIN hasta h ON h.id = c.hasta_id
             WHERE {" AND ".join(kosullar)}
             ORDER BY {sira}{sinir}""",
        parametre)
    # sqlite3.Row'a alan eklenemiyor; gün hesabı için sözlüğe çevriliyor
    liste = []
    for r in satirlar:
        d = dict(r)
        d["gun"] = _opu_gunu(d["opu_zamani"])
        liste.append(d)
    return liste


@uygulama.get("/")
def anasayfa(request: Request, yetkisiz: str = ""):
    """Ana ekran: laboratuvarda işi süren cycle'ların listesi.

    v6.18'de bu ekranda hasta adı yoktu (ekrana bakan herkes listeyi
    görüyordu). v6.28'de kullanıcı bu kuralı kendi isteğiyle gevşetti:
    ana ekran artık her sabah bakılan kâğıt klasörün karşılığı, adsız bir
    liste o işi görmüyor.
    """
    aktif_hasta = db.tek(
        "SELECT COUNT(*) k FROM hasta WHERE lab_id=? AND durum='aktif'",
        (db.LAB_ID,))["k"]
    aktif_cycle = db.tek(
        "SELECT COUNT(*) k FROM cycle WHERE lab_id=? AND durum='aktif'",
        (db.LAB_ID,))["k"]
    # Dondurulmuş embriyo sayısı türetilir — /cryo ile aynı ölçü (bkz. CLAUDE.md)
    dondurulmus = db.tek(
        "SELECT COUNT(*) k FROM olay o JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
        "WHERE t.lab_id=? AND t.durum='dolu' AND o.tip='vitrifikasyon' "
        "AND o.iptal_mi=0", (db.LAB_ID,))["k"]
    return sablon.TemplateResponse(
        request, "ana.html",
        {"kullanici": request.state.kullanici,
         "aktif_hasta": aktif_hasta, "aktif_cycle": aktif_cycle,
         "bekleyen": len(goruntuler.bekleyen_dosyalar()),
         "dondurulmus": dondurulmus,
         "liste": cycle_listesi(),
         "bugun_bitenler": cycle_listesi(bugun=True),
         "yaklasanlar": cycle_listesi(yaklasan=YAKLASAN_GUN),
         "yaklasan_gun": YAKLASAN_GUN,
         "goc_gerekli": not _bitis_kolonu_var() or not _planlanan_kolonu_var(),
         "yedek": yedek_durumu(), "yetkisiz": yetkisiz},
    )


def _ay_kaydir(yil: int, ay: int, adim: int) -> tuple:
    """Bir ay ileri / geri. Yıl sınırını kendisi çevirir."""
    n = (yil * 12 + (ay - 1)) + adim
    return n // 12, n % 12 + 1


def _yil_araligi(secili: int) -> list:
    """Yıl seçicide görünecek yıllar (v6.30).

    En eski kayıttan bugüne. `>= 2000` süzgeci bilerek: bir cycle'da OPU
    tarihi `0026-09-04` yazıyor (bekleyen iş 6) ve o değer aralığa girseydi
    seçicide iki bin satır olurdu.

    Seçili yıl listede yoksa yine de eklenir — oklarla aralığın dışına
    çıkılmış olabilir, seçici boş görünmesin.
    """
    tarih = "COALESCE(opu_zamani, olusturma_zamani)"
    r = db.tek(
        f"SELECT MIN(CAST(strftime('%Y', {tarih}) AS INTEGER)) y FROM cycle "
        f"WHERE lab_id = ? AND CAST(strftime('%Y', {tarih}) AS INTEGER) >= 2000",
        (db.LAB_ID,))
    bu = _dt.now().year
    en_eski = min(x for x in ((r and r["y"]) or bu, bu, secili) if x)
    return list(range(int(en_eski), max(bu, secili) + 1))


def ornek_kodu_ara(ara: str) -> list:
    """Örnek kodundan arama: `527078-2026-0001-03` ya da kodun bir parçası.

    Kod tüpün, pipetin ve dosyanın üstünde yazan şey; personelin elinde kod
    var, "bu kim" diye soruyor. `specimen.id` kodun son iki parçası
    (`<cycle no>-<sıra>`), başındaki dosya no hastadan geliyor — o yüzden
    arama ikisini birleştirip arıyor, böylece hem tam kod hem de kodun
    kuyruğu bulunuyor.

    **Hastanın arşivlenmiş olmasına bakmaz.** Dolapta duran bir örneğin
    dosyası kapanmış olabilir; kodu okunabiliyorsa bulunabilmeli.
    """
    k = f"%{ara}%"
    return db.sorgu(
        "SELECT s.id, s.cycle_sira_no, c.id AS cycle_id, c.cycle_no, "
        "  c.cycle_tipi, c.durum AS cycle_durum, "
        "  h.id AS hasta_id, h.dosya_no, h.ad_soyad, h.durum AS hasta_durum "
        "FROM specimen s "
        "JOIN cycle c ON c.id = s.cycle_id "
        "JOIN hasta h ON h.id = c.hasta_id "
        "WHERE s.lab_id = ? "
        "  AND (CAST(h.dosya_no AS TEXT) || '-' || s.id) LIKE ? "
        "ORDER BY h.dosya_no, c.cycle_no, s.cycle_sira_no LIMIT 50",
        (db.LAB_ID, k),
    )


def _sadece_sperm_kosulu(alias: str = "h") -> str:
    """Yalnızca sperm dondurma amacıyla açılmış hasta koşulu (v6.98).

    Hiç cycle'ı olmayan ve en az bir iptal edilmemiş `sperm_dondurma`
    kaydı olan hasta — "Yeni hasta kaydı (Sperm Dondurma)" akışından
    (v6.86) açılmış, IVF tedavisi görmeyen hasta demek. Ayrı bir işaret
    tutulmuyor (v6.38'deki "istatistikler türetilmiştir" gerekçesinin
    aynısı): sonradan kendi cycle'ı açılırsa (nadir ama mümkün) koşul
    kendiliğinden düşer, elle bir şey güncellemeye gerek kalmaz.

    Kullanıcının isteği (2026-09-17): mevcut bir IVF hastasına sperm
    dondurma eklenebilmesi (örn. eşinden alınan sperm) kalsın, ama bu
    şekilde açılan hastalar Tüm Hastalar listesinde IVF hastalarıyla
    karışmasın; arandıklarında ise (arama hedefli bir sorgu, bu listenin
    aksine) bulunabilsinler, yalnızca rozetle ayırt edilsinler.
    """
    return (
        f"(SELECT COUNT(*) FROM cycle WHERE hasta_id = {alias}.id) = 0 "
        f"AND EXISTS (SELECT 1 FROM sperm_dondurma sd "
        f"WHERE sd.hasta_id = {alias}.id AND sd.iptal_mi = 0)"
    )


HASTALAR_SAYFA_BOYU = 50  # /hastalar'daki iki liste de (ay + Tüm Hastalar) bununla sayfalanır


@uygulama.get("/hastalar")
def hastalar(request: Request, ara: str = "", arsiv: int = 0,
             yil: int = 0, ay: int = 0, sayfa: int = 1, aysayfa: int = 1):
    """Hasta kayıtları: ay ay işlem listesi + Tüm Hastalar + arama (v6.63).

    Tek ekran, üç parça — v6.29'dan farklı olarak artık **birlikte**
    görünüyorlar, birbirini değiştirmiyorlar (kullanıcının isteği,
    2026-09-16: "hasta kayıtları ve takvim aynı şey gibi" şikâyetinin
    yanıtı bu ekranı belirginleştirmekti):

    - **Sol sütun — o ayın cycle'ları**, yani "bu ay hangi vakaları yaptık".
      Ölçü OPU tarihi (yoksa cycle'ın açıldığı tarih — FET'te OPU olmuyor).
      Satır cycle başına: aynı hastanın Mart ve Temmuz'daki iki cycle'ı iki
      ayrı satır, çünkü soru "kim kayıtlı" değil "ne zaman ne yapıldı".
      **`ara` ile değişmez** — arama artık ay görünümünü kapatmıyor.
    - **Sağ sütun — Tüm Hastalar**: arama boşken aktif hastaların tamamı,
      alfabetik. Arama doluyken aynı sütun **arama sonucuna** dönüşür (dosya
      no / ad soyad / örnek kodu). Amaç hastayı bulmak; ay bilinseydi zaten
      aranmazdı, o yüzden bu sütun ay süzgecinden bağımsız.
    - **`?arsiv=1`** eskisi gibi ayrı, tam genişlik bir mod: arşivlenmiş
      hastaların listesi, ay/Tüm Hastalar yok.

    **İki liste de sayfalanır** (Tüm Hastalar v6.87'de, ay listesi v6.88'de
    aynı gerekçeyle — kullanıcının isteği: "Tüm Hastalar yanındaki aylık
    tedavilerin olduğu yerde aynı şekilde olsun"). İkisi de `HASTALAR_
    SAYFA_BOYU` (50) kadar geliyor, birbirinden **bağımsız** sayfa
    numaralarıyla: Tüm Hastalar `?sayfa=`, ay listesi `?aysayfa=`. Arama
    sonucu (`kayitlar`/`hastalar`) sayfalanmıyor — zaten süzülmüş, küçük
    bir liste.
    """
    bugun = _dt.now()
    yil = yil or bugun.year
    ay = ay or bugun.month
    if not 1 <= ay <= 12:
        ay = bugun.month
    bu_ay = (yil == bugun.year and ay == bugun.month)

    kayitlar, ornekler = [], []
    # Taşıyıcı etiketi araması (v6.138, kullanıcının isteği: "Ana sayfadaki
    # aramada o da aranabilsin" -- ana ekranın arama kutusu bu ekrana
    # gönderiyor). Hasta durumundan bağımsız: dolaptaki bir tüpün etiketi
    # okunabiliyorsa bulunabilmeli, hastasının dosyası kapanmış olsa da
    # (örnek kodu aramasının gerekçesinin aynısı, v6.35). Arşiv modunda da
    # çalışıyor -- kutu orada da aynı kutu.
    tasiyicilar = etiket_ara(ara)
    durum = "arsiv" if arsiv else ("aktif" if ara.strip() else None)
    if durum:
        ortak = ("SELECT h.*, (SELECT COUNT(*) FROM cycle WHERE hasta_id = h.id) "
                 f"AS cycle_sayisi, ({_sadece_sperm_kosulu()}) AS sperm_hastasi "
                 "FROM hasta h WHERE h.lab_id = ? AND h.durum = ?")
        if ara.strip():
            kayitlar = db.sorgu(
                ortak + " AND (CAST(h.dosya_no AS TEXT) LIKE ? OR h.ad_soyad LIKE ?)"
                        " ORDER BY h.dosya_no",
                # `ad_soyad` her zaman büyük harfle kayıtlı (v6.115); SQLite'ın
                # LIKE'ı yalnızca ASCII'de büyük/küçük harf ayrımı yapmıyor,
                # Türkçe ı/İ/ş/Ş/ğ/Ğ/ö/Ö/ü/Ü/ç/Ç'de yapıyor. Arama terimini de
                # `tr_buyuk()`'ten geçirmezsek küçük harfle Türkçe isim
                # arayan kimse hiçbir sonuç bulamaz (v6.116, kullanıcı bildirdi).
                (db.LAB_ID, durum, f"%{ara.strip()}%", f"%{tr_buyuk(ara.strip())}%"),
            )
            # Örnek kodu araması yalnızca tire içeren metinde çalışır: kod
            # `<dosya no>-<yıl>-<cycle>-<sıra>` biçiminde, tiresiz bir şey
            # kod değildir. Yoksa "3" yazan biri bütün örnekleri listelerdi.
            if "-" in ara:
                ornekler = ornek_kodu_ara(ara.strip())
        else:
            # Yalnızca arsiv=1 ve arama boş: son 50 arşiv kaydı.
            kayitlar = db.sorgu(
                ortak + " ORDER BY h.olusturma_zamani DESC LIMIT 50",
                (db.LAB_ID, durum))

    # Ay listesi ve Tüm Hastalar arşiv modunda basılmıyor, gereksiz sorgu
    # atılmasın diye hesaplanmıyor da. Tüm Hastalar de ara doluyken şablonda
    # hiç gösterilmiyor (o zaman `kayitlar` gösteriliyor) — aynı gerekçeyle
    # onda da hesaplanmıyor.
    liste, tum_hastalar = [], []
    tum_hastalar_sayisi = 0
    tum_hastalar_sayfa_toplam = 1
    ay_sayisi = 0
    ay_sayfa_toplam = 1
    if not arsiv:
        ay_str = f"{yil:04d}-{ay:02d}"
        ay_sayisi = cycle_listesi(ay=ay_str, sayisi=True)
        ay_sayfa_toplam = max(1, -(-ay_sayisi // HASTALAR_SAYFA_BOYU))  # tavana yuvarla
        aysayfa = min(max(aysayfa, 1), ay_sayfa_toplam)
        liste = cycle_listesi(ay=ay_str, limit=HASTALAR_SAYFA_BOYU,
                              offset=(aysayfa - 1) * HASTALAR_SAYFA_BOYU)
        if not ara.strip():
            # Yalnızca sperm dondurma amacıyla açılmış hastalar (v6.98)
            # Tüm Hastalar'dan çıkarılıyor — onlar IVF tedavi hastası değil.
            # Arandıklarında (yukarıdaki `kayitlar`) hâlâ bulunabiliyorlar.
            tum_hastalar_sayisi = db.tek(
                "SELECT COUNT(*) k FROM hasta h WHERE h.lab_id=? AND h.durum='aktif' "
                f"AND NOT ({_sadece_sperm_kosulu()})",
                (db.LAB_ID,))["k"]
            tum_hastalar_sayfa_toplam = max(
                1, -(-tum_hastalar_sayisi // HASTALAR_SAYFA_BOYU))  # tavana yuvarla
            sayfa = min(max(sayfa, 1), tum_hastalar_sayfa_toplam)
            tum_hastalar = db.sorgu(
                "SELECT h.*, (SELECT COUNT(*) FROM cycle WHERE hasta_id = h.id) "
                "AS cycle_sayisi FROM hasta h WHERE h.lab_id = ? AND h.durum = 'aktif' "
                f"AND NOT ({_sadece_sperm_kosulu()}) "
                "ORDER BY h.ad_soyad LIMIT ? OFFSET ?",
                (db.LAB_ID, HASTALAR_SAYFA_BOYU,
                 (sayfa - 1) * HASTALAR_SAYFA_BOYU))

    onceki = _ay_kaydir(yil, ay, -1)
    sonraki = _ay_kaydir(yil, ay, 1)
    arsiv_sayisi = db.tek(
        "SELECT COUNT(*) k FROM hasta WHERE lab_id=? AND durum='arsiv'", (db.LAB_ID,)
    )["k"]
    return sablon.TemplateResponse(
        request, "hastalar.html",
        {"hastalar": kayitlar, "liste": liste, "tum_hastalar": tum_hastalar,
         "ornekler": ornekler, "tasiyicilar": tasiyicilar,
         "ara": ara, "arsiv": arsiv,
         "yil": yil, "ay": ay, "bu_ay": bu_ay,
         "yillar": _yil_araligi(yil),
         "onceki": onceki, "sonraki": sonraki,
         "sayfa": sayfa, "tum_hastalar_sayfa_toplam": tum_hastalar_sayfa_toplam,
         "tum_hastalar_sayisi": tum_hastalar_sayisi,
         "aysayfa": aysayfa, "ay_sayfa_toplam": ay_sayfa_toplam,
         "ay_sayisi": ay_sayisi,
         "arsiv_sayisi": arsiv_sayisi, "kullanici": request.state.kullanici,
         "yedek": yedek_durumu()},
    )


@uygulama.get("/hasta/yeni")
def hasta_yeni(request: Request, dosya_no: str = ""):
    # `v` hata dönüşünde yazılanları taşır; boş formda da tanımlı olmalı.
    return sablon.TemplateResponse(
        request, "hasta_form.html", {"dosya_no": dosya_no, "v": {}})


@uygulama.post("/hasta/yeni")
def hasta_kaydet(
    request: Request,
    dosya_no: str = Form(...),
    ad_soyad: str = Form(...),
    telefon: str = Form(""),
    dogum_tarihi: str = Form(""),
    es_adi: str = Form(""),
    es_telefon: str = Form(""),
    es_dogum_tarihi: str = Form(""),
    es_dosya_no: str = Form(""),
    notlar: str = Form(""),
):
    mevcut = db.tek(
        "SELECT id FROM hasta WHERE lab_id = ? AND dosya_no = ?",
        (db.LAB_ID, int(dosya_no)),
    )
    if mevcut:
        return RedirectResponse(f"/hasta/{mevcut['id']}", status_code=303)

    try:
        dt = zaman(dogum_tarihi, "Doğum tarihi")
        edt = zaman(es_dogum_tarihi, "Eş doğum tarihi")
    except FormHatasi as e:
        # Yazılan doldurulmuş halde geri gelsin (v6.21 kuralı): hata mesajı
        # gösterip formu boşaltmak kullanıcıya ne yazdığını unutturur.
        return sablon.TemplateResponse(
            request, "hasta_form.html",
            {"dosya_no": dosya_no, "hata": str(e),
             "v": {"ad_soyad": ad_soyad, "telefon": telefon,
                   "dogum_tarihi": dogum_tarihi,
                   "es_adi": es_adi, "es_telefon": es_telefon,
                   "es_dogum_tarihi": es_dogum_tarihi,
                   "es_dosya_no": es_dosya_no,
                   "notlar": notlar}},
        )

    # Eşin dosya numarası (v6.139). Göç çalışmamışsa kolon INSERT'ten
    # tümden çıkıyor -- `cycle_alanlari()`'nın koruması (tuzak #3).
    kolonlar = ["lab_id", "dosya_no", "ad_soyad", "telefon", "dogum_tarihi",
                "es_adi", "es_telefon", "es_dogum_tarihi", "notlar"]
    degerler = [db.LAB_ID, int(dosya_no), tr_buyuk(ad_soyad.strip()),
                bos_ise_none(telefon), dt, tr_buyuk(bos_ise_none(es_adi)),
                bos_ise_none(es_telefon), edt, bos_ise_none(notlar)]
    if es_dosya_no_var():
        kolonlar.append("es_dosya_no")
        degerler.append(_dosya_no_sayi(es_dosya_no))
    yeni_id = db.yaz(
        f"INSERT INTO hasta ({', '.join(kolonlar)}) "
        f"VALUES ({', '.join('?' * len(kolonlar))})", tuple(degerler))
    return RedirectResponse(f"/hasta/{yeni_id}", status_code=303)


@uygulama.get("/hasta/kontrol")
def hasta_kontrol(dosya_no: str = ""):
    """Yazılan dosya no zaten kayıtlı mı? Form gönderilmeden önce sorulur.

    İki ekran çağırıyor: yeni hasta (`hasta_form.html`) ve Sperm Dondurma'nın
    yeni-hasta formu. **Tek uç nokta** — sperm tarafına ikinci bir kopya
    yazılmadı, yoksa biri güncellenip öteki unutulurdu.

    **v6.125'te tedavi ve sperm sayısı da dönüyor** (kullanıcının isteği:
    "eğer bu hastanın eşi ile birlikte tüp bebek için hasta kaydı varsa
    uyarı mesajı ver"). Eskiden yalnızca "kayıtlı, adı şu" diyordu;
    sperm dondurmaya gelen erkeğin dosya numarası çiftin tüp bebek
    kaydınınkiyle aynıysa personelin bunu **girerken** bilmesi gerekiyor.
    Eşleştirme tamamen dosya numarası üzerinden: `UNIQUE (lab_id,
    dosya_no)` sayesinde aynı numara = aynı `hasta` satırı, isim
    karşılaştırması yok (bkz. `dosya_no_sahibi`).

    Sunucu tarafındaki engel kalkmadı; bu yalnızca **erken haber**
    (CLAUDE.md: "ekranda göstermek yetmez, sunucu da reddetmeli").
    """
    h = dosya_no_sahibi(dosya_no)
    if not h:
        return {"var": False}
    return {"var": True, "id": h["id"], "ad_soyad": h["ad_soyad"],
            "es_adi": h["es_adi"] or "", "arsiv": h["durum"] == "arsiv",
            "cycle_sayisi": h["cycle_sayisi"], "sperm_sayisi": h["sperm_sayisi"]}


@uygulama.get("/hasta/{hasta_id}")
def hasta_detay(request: Request, hasta_id: int):
    hasta = db.tek(
        f"SELECT h.*, ({_sadece_sperm_kosulu()}) AS sperm_hastasi "
        "FROM hasta h WHERE h.id = ?", (hasta_id,))
    cycles = db.sorgu(
        "SELECT * FROM cycle WHERE hasta_id = ? "
        "ORDER BY hasta_cycle_no DESC, id DESC", (hasta_id,)
    )
    # Bu dosya numarasına ait dondurulmuş sperm kayıtları (v6.125,
    # kullanıcının isteği: "hasta kartında dondurulmuş sperm işlemi varsa
    # dosya numarasından eşle"). Kart şimdiye kadar yalnızca "Yeni Sperm
    # Dondurma" düğmesini gösteriyordu — var olanları göstermiyordu, yani
    # bir tüp bebek çiftinin kartına bakan embriyolog o çiftin dondurulmuş
    # spermi olduğunu göremiyordu. Eşleştirme `hastanin_sperm_kayitlari()`
    # ile: dosya no lab içinde UNIQUE, "aynı dosya no" = "aynı hasta satırı".
    # Eşin KENDİ dosya numarasıyla açılmış kaydı (v6.139, kullanıcının
    # isteği: "Eğer eş erkek olarak sperm dondurma kaydı daha önce
    # yapıldıysa uyarı versin"). v6.125'in bilerek kapsamadığı durum buydu:
    # onkoloji öncesi sperm donduran erkek çiftin dosyasından bağımsız bir
    # numarayla kayıtlıysa dosya no tutmuyor, hiçbir uyarı çıkmıyordu.
    # Artık çiftin kaydı o numarayı taşıyor ve bağ kesinleşiyor.
    es_sahibi = es_sperm = None
    if es_dosya_no_var() and hasta and hasta["es_dosya_no"]:
        es_sahibi = dosya_no_sahibi(hasta["es_dosya_no"])
        # Aynı satırı iki kez listelememek için: eşin dosya numarası yanlışlıkla
        # çiftin kendi numarası yazılmışsa `sperm_kayitlari` zaten onu gösteriyor.
        if es_sahibi and es_sahibi["id"] != hasta_id:
            es_sperm = hastanin_sperm_kayitlari(es_sahibi["id"])
    # Bağlanabilir tedaviler: yalnızca androloji aşaması OLAN tipler
    # (v6.139). Dondurulmuş sperm FET'te kullanılmıyor ve bağlansaydı bağ
    # hiçbir ekranda görünmezdi -- androloji kartı yalnızca `ivf_icsi`'de
    # basılıyor. Koşul `TIP_ASAMALARI`'na bakıyor, cycle tipini elle
    # yazmıyor: yeni bir androlojili tip eklenirse kendiliğinden kapsar.
    baglanabilir = [c for c in cycles
                    if "androloji" in TIP_ASAMALARI.get(c["cycle_tipi"], ())]
    return sablon.TemplateResponse(
        request, "hasta_detay.html",
        {"hasta": hasta, "cycles": cycles,
         "sperm_kayitlari": hastanin_sperm_kayitlari(hasta_id),
         "es_sahibi": es_sahibi, "es_sperm": es_sperm,
         "baglanabilir": baglanabilir,
         "yeniden": hastanin_yeniden_dondurmalari(cycles)}
    )


def hastanin_yeniden_dondurmalari(cycles) -> dict:
    """Hasta kartının tedavi satırları için yeniden dondurmalar (v6.151).

    Kullanıcının isteği: "Hasta kartı bölümünde hastanın bütün tedavileri
    göründüğü gibi eğer refreeze yapıldıysa görünsün." Yeniden dondurma
    v6.143'ten beri kayıtlı; görünmediği yer hasta kartıydı.

    Yeniden dondurma = daha önce çözülmüş bir örneğin dondurması (ölçü kimlik
    sırası, saat değil -- v6.143'ün "önce en son adım" kuralı). Türetilmiş,
    işaret tutulmuyor. **Çözülen şey ile dondurulan şey aynı türde olmalı**:
    Yumurta Çözme'de çözülen yumurtadan gelişip dondurulan embriyo yeniden
    dondurma değil (`db.yumurta_mi()` iki aşamada farklı cevap veriyor).

    Dönen sözlük tedavi kimliğine göre:
    - `dondurulan`: bu tedavide yeniden dondurulan tüpler -- etiket, kaç
      örnek, sonradan hangi tedavi(ler)de çözüldüğü;
    - `cozulen`: bu tedavide çözülen, daha önce yeniden dondurulmuş tüpler --
      hangi tedavide dondurulduğu. İki satır birbirini gösteriyor: FET'ten
      FET'e zincir kartta iki yönden okunur.
    Göç çalışmamışsa boş (tuzak #3).
    """
    if not cycles or not db.yeniden_dondurma_var():
        return {}
    idler = [c["id"] for c in cycles]
    tipler = {c["id"]: c["cycle_tipi"] for c in cycles}
    sira = {c["id"]: c["hasta_cycle_no"] for c in cycles}
    yer = ",".join("?" * len(idler))
    vt = db.vit_tedavisi("v")
    satirlar = db.sorgu(
        f"SELECT {vt} AS vit_cid, v.vit_tasiyici_id AS tid, t.etiket, "
        "v.specimen_id, "
        "(SELECT COALESCE(c.thaw_cycle_id, s.cycle_id) FROM olay c "
        " WHERE c.specimen_id = v.specimen_id AND c.tip = 'thaw' "
        " AND c.iptal_mi = 0 AND c.id < v.id ORDER BY c.id DESC LIMIT 1) "
        "  AS onceki_cozme_cid "
        "FROM olay v JOIN specimen s ON s.id = v.specimen_id "
        "LEFT JOIN tasiyici t ON t.id = v.vit_tasiyici_id "
        f"WHERE v.tip = 'vitrifikasyon' AND v.iptal_mi = 0 AND {vt} IN ({yer}) "
        "ORDER BY v.id", idler)
    tupler = {}   # tid -> {...}; aynı tüpteki örnekler tek satır
    for r in satirlar:
        if r["onceki_cozme_cid"] is None:
            continue  # ilk dondurma
        cozme_tipi = tipler.get(r["onceki_cozme_cid"])
        if cozme_tipi is None:  # başka hastanın tedavisi -- olmamalı
            c = db.tek("SELECT cycle_tipi FROM cycle WHERE id = ?",
                       (r["onceki_cozme_cid"],))
            cozme_tipi = c["cycle_tipi"] if c else None
        if (db.yumurta_mi(cozme_tipi, "thaw")
                != db.yumurta_mi(tipler[r["vit_cid"]], "vitrifikasyon")):
            continue  # yumurta çözüldü, embriyo donduruldu
        anahtar = r["tid"] if r["tid"] is not None else ("yok", r["vit_cid"])
        tup = tupler.setdefault(anahtar, {
            "tid": r["tid"], "etiket": r["etiket"], "vit_cid": r["vit_cid"],
            "ornekler": set(), "cozuldu": []})
        tup["ornekler"].add(r["specimen_id"])
    sonuc = {}
    for tup in tupler.values():
        if tup["tid"] is not None:
            for c in db.sorgu(
                    "SELECT DISTINCT thaw_cycle_id FROM olay "
                    "WHERE thaw_tasiyici_id = ? AND tip = 'thaw' AND iptal_mi = 0 "
                    "AND thaw_cycle_id IS NOT NULL ORDER BY thaw_cycle_id",
                    (tup["tid"],)):
                cid = c["thaw_cycle_id"]
                tup["cozuldu"].append({"cid": cid, "no": sira.get(cid)})
                sonuc.setdefault(cid, {"dondurulan": [], "cozulen": []})[
                    "cozulen"].append({"etiket": tup["etiket"],
                                       "cid": tup["vit_cid"],
                                       "no": sira.get(tup["vit_cid"])})
        tup["adet"] = len(tup["ornekler"])
        sonuc.setdefault(tup["vit_cid"], {"dondurulan": [], "cozulen": []})[
            "dondurulan"].append(tup)
    return sonuc


@uygulama.post("/hasta/{hasta_id}/sperm-dondurma/{sperm_dondurma_id}/bagla")
async def hasta_sperm_bagla(request: Request, hasta_id: int, sperm_dondurma_id: int):
    """Hasta kartından dondurulmuş spermi bu hastanın bir tedavisine bağlar.

    v6.139, kullanıcının isteği: "Hasta kartında tedaviye bağlama opsiyonu
    versin". v6.86'dan beri bağlama yalnızca androloji ekranındaydı ve orada
    **arayarak** bulunuyordu; hasta kartında ise kayıt zaten gözünün önünde
    (kendi kaydı ya da eşin dosya numarasından bulunan kayıt), aradaki tek
    eksik hangi tedaviye bağlanacağıydı.

    Tedavi **bu hastanın** tedavileri arasından seçiliyor: başka bir hastanın
    tedavisine buradan bağlamak yanlış hasta riski taşırdı (CLAUDE.md'nin en
    pahalı hatası), o iş hâlâ androloji ekranının arama akışında.
    """
    f = await request.form()
    cycle_id = (f.get("cycle_id") or "").strip()
    if cycle_id.isdigit() and db.tek(
            "SELECT 1 x FROM cycle WHERE id=? AND hasta_id=?", (int(cycle_id), hasta_id)):
        sperm_tedaviye_bagla(sperm_dondurma_id, int(cycle_id))
    return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)


@uygulama.post("/hasta/{hasta_id}/sperm-dondurma/{sperm_dondurma_id}/baglanti-kaldir")
def hasta_sperm_baglanti_kaldir(request: Request, hasta_id: int, sperm_dondurma_id: int):
    """Bu hastanın bir tedavisine bağlanmış spermin bağını kaldırır.

    Yalnızca bağlı olduğu tedavi BU hastanınsa kaldırılıyor — androloji
    ekranındaki kuralın (yalnızca kendi tedavisinin bağını koparır) hasta
    kartı hali.
    """
    if db.tek(
        "SELECT 1 x FROM sperm_dondurma sd JOIN cycle c ON c.id = sd.kullanim_cycle_id "
        "WHERE sd.id=? AND c.hasta_id=?", (sperm_dondurma_id, hasta_id)):
        sperm_baglanti_kaldir(sperm_dondurma_id)
    return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)


@uygulama.get("/hasta/{hasta_id}/duzenle")
def hasta_duzenle(request: Request, hasta_id: int):
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    return sablon.TemplateResponse(request, "hasta_duzenle.html", {"h": hasta})


@uygulama.post("/hasta/{hasta_id}/duzenle")
def hasta_guncelle(
    request: Request,
    hasta_id: int,
    ad_soyad: str = Form(...),
    telefon: str = Form(""),
    dogum_tarihi: str = Form(""),
    es_adi: str = Form(""),
    es_telefon: str = Form(""),
    es_dogum_tarihi: str = Form(""),
    es_dosya_no: str = Form(""),
    notlar: str = Form(""),
):
    eski = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    try:
        yeni = {
            "ad_soyad": tr_buyuk(ad_soyad.strip()),
            "telefon": bos_ise_none(telefon),
            "dogum_tarihi": zaman(dogum_tarihi, "Doğum tarihi"),
            "es_adi": tr_buyuk(bos_ise_none(es_adi)),
            "es_telefon": bos_ise_none(es_telefon),
            "es_dogum_tarihi": zaman(es_dogum_tarihi, "Eş doğum tarihi"),
            "notlar": bos_ise_none(notlar),
        }
        # Göç çalışmamışsa alan hiç yazılmıyor (tuzak #3) -- sözlüğe
        # eklenmediği için aşağıdaki UPDATE de onu görmüyor.
        if es_dosya_no_var():
            yeni["es_dosya_no"] = _dosya_no_sayi(es_dosya_no)
    except FormHatasi as e:
        # Şablon `h`'ye sözlükle de erişiyor; yazılanlar ekranda kalsın.
        return sablon.TemplateResponse(
            request, "hasta_duzenle.html",
            {"h": {**dict(eski), "ad_soyad": ad_soyad, "telefon": telefon,
                   "dogum_tarihi": dogum_tarihi, "es_adi": es_adi,
                   "es_telefon": es_telefon,
                   "es_dogum_tarihi": es_dogum_tarihi,
                   "es_dosya_no": es_dosya_no, "notlar": notlar},
             "hata": str(e)},
        )
    db.yaz(
        "UPDATE hasta SET " + ", ".join(f"{k}=?" for k in yeni) + " WHERE id=?",
        (*yeni.values(), hasta_id),
    )
    guvenlik.degisiklikleri_yaz(
        "hasta", hasta_id, eski, yeni, request.state.kullanici["id"]
    )
    return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)


# ----------------------------------------------------------------- cycle

CYCLE_ALANLARI = [
    "cycle_no", "hasta_cycle_no", "cycle_tipi", "endikasyon", "protokol_tipi", "gonadotropin_tipi",
    "baslangic_doz", "toplam_doz", "stim_gun_sayisi", "trigger_tipi", "hcg_gunu_e2",
    "endometrium_mm", "folikul_sayisi", "amh", "hcg_zamani", "opu_zamani",
    "denudasyon_zamani", "opu_sag_oosit", "opu_sol_oosit", "protokol_notu",
    "planlanan_tarih",
]


def _planlanan_kolonu_var() -> bool:
    """goc_028 çalıştırıldı mı? (tuzak #3)

    Çalıştırılmadıysa `planlanan_tarih` INSERT/UPDATE'ten **çıkarılıyor** —
    yoksa cycle açmak tümden bozulurdu, ki o çekirdek bir akış.
    """
    return any(r["name"] == "planlanan_tarih"
               for r in db.sorgu("PRAGMA table_info(cycle)"))


def cycle_alanlari() -> list:
    if _planlanan_kolonu_var():
        return CYCLE_ALANLARI
    return [a for a in CYCLE_ALANLARI if a != "planlanan_tarih"]


def _elle_no_kolonu_var() -> bool:
    """goc_047 çalıştırıldı mı -- `cycle.hasta_cycle_no_elle` var mı (v6.144).

    `_planlanan_kolonu_var()` gibi her seferinde soruluyor, `db.kolon_var()`
    gibi saklanmıyor: yedekten geri yüklenen eski bir veritabanında kolon
    yok ve göçler ancak program yeniden açılınca çalışıyor. Saklanmış bir
    "var" cevabı o arada tedavi açmayı "no such column" ile bozardı.
    """
    return any(r["name"] == "hasta_cycle_no_elle"
               for r in db.sorgu("PRAGMA table_info(cycle)"))


def cycle_formu_oku(f: dict) -> dict:
    return {
        "cycle_no": (f.get("cycle_no") or "").strip(),
        "hasta_cycle_no": tam(f.get("hasta_cycle_no"), "Kaçıncı cycle"),
        "cycle_tipi": f.get("cycle_tipi") or "ivf_icsi",
        "endikasyon": bos_ise_none(f.get("endikasyon")),
        "protokol_tipi": bos_ise_none(f.get("protokol_tipi")),
        "gonadotropin_tipi": bos_ise_none(f.get("gonadotropin_tipi")),
        "baslangic_doz": sayi(f.get("baslangic_doz"), "Başlangıç doz"),
        "toplam_doz": sayi(f.get("toplam_doz"), "Toplam doz"),
        "stim_gun_sayisi": tam(f.get("stim_gun_sayisi"), "Stim. gün"),
        "trigger_tipi": bos_ise_none(f.get("trigger_tipi")),
        "hcg_gunu_e2": sayi(f.get("hcg_gunu_e2"), "hCG günü E2"),
        "endometrium_mm": sayi(f.get("endometrium_mm"), "Endometrium"),
        "folikul_sayisi": tam(f.get("folikul_sayisi"), "Folikül sayısı"),
        "amh": sayi(f.get("amh"), "AMH"),
        "hcg_zamani": zaman(f.get("hcg_zamani"), "hCG zamanı"),
        "opu_zamani": zaman(f.get("opu_zamani"), "OPU zamanı"),
        "denudasyon_zamani": zaman(f.get("denudasyon_zamani"), "Denüdasyon zamanı"),
        "opu_sag_oosit": tam(f.get("opu_sag_oosit")),
        "opu_sol_oosit": tam(f.get("opu_sol_oosit")),
        "protokol_notu": bos_ise_none(f.get("protokol_notu")),
        # Planlanan tarih gün bazında: "14/09/2026 FET" -- saat yok.
        "planlanan_tarih": zaman(f.get("planlanan_tarih"), "Planlanan tarih"),
    }


def cycle_listeleri():
    return {
        "tipler": db.liste("cycle_tipi"),
        "protokoller": db.liste("protokol_tipi"),
        "triggerlar": db.liste("trigger_tipi"),
        "endikasyonlar": db.liste("endikasyon"),
    }


def sonraki_hasta_cycle_no(hasta_id: int) -> int:
    """Yeni tedavinin kutuya önerilen numarası — en yüksek numaranın bir fazlası.

    Yalnızca öneri (v6.144): kaydedilince numarayı tarih sırası veriyor
    (`db.tedavileri_sirala()`), eski bir tedavi girildiyse araya yerleşiyor.
    """
    r = db.tek(
        "SELECT MAX(hasta_cycle_no) m FROM cycle WHERE hasta_id = ?", (hasta_id,)
    )
    return (r["m"] or 0) + 1


def tedavi_sirasini_logla(degisen, kullanici_id, haric=None):
    """Kayan numaraları değişiklik geçmişine yazar (v6.144) — "1. tedavi neden
    2. oldu" sorusunun cevabı orada. `haric`: kaydı zaten günlüğe giren tedavi."""
    for cid, _no, eski, yeni in degisen:
        if cid != haric:
            guvenlik.degisiklikleri_yaz("cycle", cid, {"hasta_cycle_no": eski},
                                        {"hasta_cycle_no": yeni}, kullanici_id)


def tedavi_sirasini_duzelt(hasta_id, kullanici_id) -> list:
    """Hastanın tedavilerini tarih sırasıyla yeniden numaralar (v6.144).

    Tedavinin işlem gününü değiştiren yazmalardan sonra çağrılıyor: OPU
    saati, çözme ve transfer (FET'in günü onlardan geliyor), kalıcı silme.
    Tedavi formu bunu kendi işleminin içinde yapıyor (elle yazılan numarayı
    doğrulamak için). Günü değiştiren yeni bir yazma yolu açarsan
    (`db.tedavi_tarihi()`'ne bak) orada da çağır — yoksa numaralar tarih
    sırasından ayrı düşer. Numara türetilmiş bir bilgi: güncellenemezse asıl
    kayıt geri alınmıyor, sebep günlüğe yazılıyor, bir sonraki kayıtta düzelir.
    """
    if not hasta_id:
        return []
    try:
        with db.yazma_islemi() as b:
            degisen = db.tedavileri_sirala(b, hasta_id)
    except sqlite3.Error:
        _gunluk.exception("Tedavi sırası güncellenemedi (hasta %s)", hasta_id)
        return []
    tedavi_sirasini_logla(degisen, kullanici_id)
    return degisen


def _elle_no_dogrula(b, cycle_id, elle):
    """Elle yazılan "Kaçıncı tedavi" tarih sırasıyla bağdaşıyor mu (v6.144).

    Bağdaşmıyorsa `FormHatasi` — çağıran işlemin içinde, yani kayıt geri
    alınıyor ve form yazılanlarla yeniden basılıyor (v6.21). Sıralama elle
    yazılanı yalnızca bir önceki tedavinin numarasından büyükse tutuyor.
    """
    if elle is None:
        return
    etkin = b.execute("SELECT hasta_cycle_no FROM cycle WHERE id = ?",
                      (cycle_id,)).fetchone()[0]
    if etkin != elle:
        raise FormHatasi(
            f"Kaçıncı tedavi {elle} olamaz: tarih sırasına göre bu tedaviden "
            f"önce gelen tedavi hastanın {etkin - 1}. tedavisi. En az {etkin} "
            "yaz ya da kutuyu boş bırak — boş kalırsa numarayı tarih sırası verir.")


@uygulama.get("/hasta/{hasta_id}/cycle/yeni")
def cycle_yeni(request: Request, hasta_id: int):
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    oneri = sonraki_hasta_cycle_no(hasta_id)
    return sablon.TemplateResponse(
        request, "cycle_form.html",
        {"hasta": hasta,
         # Öneri gizli alanda da gidiyor (v6.144): kutu değiştirilmediyse
         # numarayı tarih sırası verir, değiştirildiyse elle yazılmıştır.
         "v": {"hasta_cycle_no": oneri, "hasta_cycle_no_oneri": oneri,
               "cycle_no": sonraki_lab_no()},
         "duzenleme": False, "hata": None,
         "hedef": f"/hasta/{hasta_id}/cycle/yeni", **cycle_listeleri()},
    )


@uygulama.post("/hasta/{hasta_id}/cycle/yeni")
async def cycle_kaydet(request: Request, hasta_id: int):
    f = dict(await request.form())
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))

    def formu_goster(mesaj):
        return sablon.TemplateResponse(
            request, "cycle_form.html",
            {"hasta": hasta, "v": f, "duzenleme": False, "hata": mesaj,
             "hedef": f"/hasta/{hasta_id}/cycle/yeni", **cycle_listeleri()},
        )

    try:
        d = cycle_formu_oku(f)
    except FormHatasi as e:
        return formu_goster(str(e))

    if not d["cycle_no"]:
        return formu_goster("Lab kayıt no boş bırakılamaz.")

    ayni = db.tek(
        "SELECT c.id, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.lab_id = ? AND c.cycle_no = ?",
        (db.LAB_ID, d["cycle_no"]),
    )
    if ayni:
        return formu_goster(
            f"'{d['cycle_no']}' numaralı tedavi zaten var "
            f"(dosya {ayni['dosya_no']}, {ayni['ad_soyad']}). Farklı bir numara gir."
        )
    if d["hasta_cycle_no"] is not None and d["hasta_cycle_no"] < 1:
        return formu_goster("Kaçıncı tedavi en az 1 olabilir.")

    # Kaçıncı tedavi (v6.144): kutuda programın önerisi duruyorsa ya da kutu
    # boşsa numarayı tarih sırası verir; kullanıcı değiştirdiyse elle
    # yazılmıştır ve korunur. Gizli alan yoksa sekme bu sürümden önce açılmış.
    oneri = ((f.get("hasta_cycle_no_oneri") or "").strip()
             or sonraki_hasta_cycle_no(hasta_id))
    elle = (None if d["hasta_cycle_no"] is None
            or str(d["hasta_cycle_no"]) == str(oneri).strip()
            else d["hasta_cycle_no"])
    alanlar = cycle_alanlari()
    degerler = [d[a] for a in alanlar]
    if _elle_no_kolonu_var():
        alanlar = alanlar + ["hasta_cycle_no_elle"]
        degerler.append(elle)
    try:
        # Açmak ve numaralamak tek işlem: elle yazılan numara tarih sırasıyla
        # bağdaşmıyorsa tedavi hiç açılmamış olur.
        with db.yazma_islemi() as b:
            yeni_id = b.execute(
                f"INSERT INTO cycle (lab_id, hasta_id, {', '.join(alanlar)}) "
                f"VALUES (?, ?, {', '.join('?' * len(alanlar))})",
                (db.LAB_ID, hasta_id, *degerler),
            ).lastrowid
            degisen = db.tedavileri_sirala(b, hasta_id)
            _elle_no_dogrula(b, yeni_id, elle)
    except FormHatasi as e:
        return formu_goster(str(e))
    except sqlite3.IntegrityError:
        # Yukarıdaki kontrolle bu INSERT arasında başkası aynı numarayı almış
        # olabilir (iki personel aynı anda cycle açıyor). Yeni numara öner.
        f["cycle_no"] = sonraki_lab_no()
        return formu_goster(
            f"'{d['cycle_no']}' numarasını az önce başka bir kullanıcı aldı. "
            f"Sıradaki boş numara yazıldı: {f['cycle_no']} — kontrol edip kaydet."
        )
    # Eski bir tedavi girildiyse sonrakilerin numarası kaydı: geçmişte görünsün.
    tedavi_sirasini_logla(degisen, request.state.kullanici["id"], haric=yeni_id)
    return RedirectResponse(f"/cycle/{yeni_id}", status_code=303)


@uygulama.get("/cycle/{cycle_id}")
def cycle_detay(request: Request, cycle_id: int, hata: str = ""):
    cycle = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad, h.es_adi, h.dogum_tarihi "
        "FROM cycle c JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    etiketler = {
        r["kod"]: r["etiket"]
        for r in db.sorgu("SELECT kod, etiket FROM liste_degeri WHERE lab_id = ?",
                          (db.LAB_ID,))
    }
    # Örneğe bağlı olmayan görüntüler iki ayrı kart: genel cycle arşivi
    # (embriyoloji fotoğrafları) ve doktor notu ekleri (v6.81) -- ikisi
    # karışmasın diye `asama` ile ayrılıyor.
    arsiv = db.sorgu(
        "SELECT id, asama, zaman, orijinal_dosya_adi FROM goruntu "
        "WHERE cycle_id = ? AND specimen_id IS NULL AND asama != 'doktor_notu' "
        "ORDER BY id", (cycle_id,))
    doktor_notu_satirlari = db.sorgu(
        "SELECT id, zaman, orijinal_dosya_adi FROM goruntu "
        "WHERE cycle_id = ? AND specimen_id IS NULL AND asama = 'doktor_notu' "
        "ORDER BY id", (cycle_id,))
    doktor_notlari = [
        {**dict(r), "pdf_mi": (r["orijinal_dosya_adi"] or "").lower().endswith(".pdf")}
        for r in doktor_notu_satirlari
    ]
    doktor_notu_resim_ids = [d["id"] for d in doktor_notlari if not d["pdf_mi"]]
    return sablon.TemplateResponse(
        request, "cycle_detay.html",
        {"c": cycle, "etiketler": etiketler,
         "arsiv": arsiv,
         "doktor_notlari": doktor_notlari,
         "doktor_notu_resim_ids": doktor_notu_resim_ids,
         "hata": hata,
         # Aşamalar arasında geçen süre (v6.37). Ayrı kayıt yok: aşama
         # ekranlarında elle girilen saatlerden hesaplanıyor.
         "cizelge": formlar.zaman_cizelgesi(cycle_id),
         # Basılabilir formlar: programla gelenler (gizlenmemişler) +
         # laboratuvarın kendi yükledikleri.
         "gomulu_formlar": gomulu_formlar(),
         "lab_formlari": lab_formlari(),
         "bugun": _dt.now().strftime("%Y-%m-%d"),
         "asamalar": (asamalar := cycle_asamalari(cycle["cycle_tipi"])),
         # yan menü aşama ekranlarındakiyle aynı listeden beslensin
         "gezinme": asama_gezinme(cycle_id, ""),
         # Tek özet kutusu (v6.110, v6.112'de tek kutuya birleşti), aynı
         # `asamalar` listesinden (kullanıcının modül izniyle süzülmüş)
         # hangi sayıların bu tedavi tipinde anlamlı olduğunu çıkarıyor.
         "ozet": cycle_ozet(cycle, {a[0] for a in asamalar})},
    )


@uygulama.get("/cycle/{cycle_id}/duzenle")
def cycle_duzenle(request: Request, cycle_id: int):
    cycle = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (cycle["hasta_id"],))
    return sablon.TemplateResponse(
        request, "cycle_form.html",
        {"hasta": hasta, "v": dict(cycle), "duzenleme": True, "hata": None,
         "cycle_id": cycle_id, "hedef": f"/cycle/{cycle_id}/duzenle",
         **cycle_listeleri()},
    )


@uygulama.post("/cycle/{cycle_id}/duzenle")
async def cycle_guncelle(request: Request, cycle_id: int):
    eski = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    f = dict(await request.form())
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (eski["hasta_id"],))

    def formu_goster(mesaj):
        return sablon.TemplateResponse(
            request, "cycle_form.html",
            {"hasta": hasta, "v": f, "duzenleme": True, "hata": mesaj,
             "cycle_id": cycle_id, "hedef": f"/cycle/{cycle_id}/duzenle",
             **cycle_listeleri()},
        )

    try:
        d = cycle_formu_oku(f)
    except FormHatasi as e:
        return formu_goster(str(e))

    if not d["cycle_no"]:
        return formu_goster("Lab kayıt no boş bırakılamaz.")

    ayni = db.tek(
        "SELECT id FROM cycle WHERE lab_id = ? AND cycle_no = ? AND id <> ?",
        (db.LAB_ID, d["cycle_no"], cycle_id),
    )
    if ayni:
        return formu_goster(f"'{d['cycle_no']}' numaralı başka bir tedavi var.")
    if d["hasta_cycle_no"] is not None and d["hasta_cycle_no"] < 1:
        return formu_goster("Kaçıncı tedavi en az 1 olabilir.")

    # Kaçıncı tedavi (v6.144): kutudaki numaraya dokunulmadıysa elle yazılmış
    # olup olmadığı da değişmez; değiştirildiyse o sayı elle yazılmıştır,
    # boşaltıldıysa numarayı tarih sırası verir. OPU tarihi değişince
    # numara kayabilir -- o yüzden kaydetmekle numaralamak tek işlem.
    alanlar = cycle_alanlari()
    degerler = [d[a] for a in alanlar]
    yeni_elle = None
    if _elle_no_kolonu_var():
        if d["hasta_cycle_no"] is None:
            elle = None
        elif d["hasta_cycle_no"] == eski["hasta_cycle_no"]:
            elle = eski["hasta_cycle_no_elle"]
        else:
            elle = yeni_elle = d["hasta_cycle_no"]
        alanlar = alanlar + ["hasta_cycle_no_elle"]
        degerler.append(elle)
    try:
        with db.yazma_islemi() as b:
            b.execute(
                f"UPDATE cycle SET {', '.join(a + '=?' for a in alanlar)} WHERE id=?",
                (*degerler, cycle_id))
            degisen = db.tedavileri_sirala(b, eski["hasta_id"])
            _elle_no_dogrula(b, cycle_id, yeni_elle)
    except FormHatasi as e:
        return formu_goster(str(e))

    kid = request.state.kullanici["id"]
    # Geçmişe numaranın kutudaki değil son hali yazılıyor: OPU tarihi
    # değişip tedavi kaydıysa o da görünsün.
    d["hasta_cycle_no"] = db.tek("SELECT hasta_cycle_no FROM cycle WHERE id = ?",
                                 (cycle_id,))["hasta_cycle_no"]
    guvenlik.degisiklikleri_yaz("cycle", cycle_id, eski, d, kid)
    tedavi_sirasini_logla(degisen, kid, haric=cycle_id)
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


# ----------------------------------------------------------------- geçmiş

@uygulama.get("/gecmis/{tablo}/{kayit_id}")
def gecmis(request: Request, tablo: str, kayit_id: int):
    if tablo not in ("hasta", "cycle"):
        return RedirectResponse("/hastalar", status_code=303)
    kayitlar = db.sorgu(
        "SELECT d.*, k.ad_soyad FROM degisiklik_log d "
        "JOIN kullanici k ON k.id = d.kullanici_id "
        "WHERE d.tablo_adi = ? AND d.kayit_id = ? ORDER BY d.zaman DESC",
        (tablo, str(kayit_id)),
    )
    return sablon.TemplateResponse(
        request, "gecmis.html",
        {"kayitlar": kayitlar, "geri": f"/{tablo}/{kayit_id}", "tablo": tablo},
    )


# ----------------------------------------------------------------- denüdasyon

import goruntuler
from fastapi.responses import FileResponse, Response


# Adresten gelen hata anahtarı doğrudan sözlüğe verilmez: `metin()` bulamadığı
# anahtarı olduğu gibi döndürüyor, yani ?hata=... ile ekrana istenen yazı
# yazdırılabilirdi. Yalnızca bu iki anahtar geçerli.
DENUDASYON_HATALARI = {"kare_zaten_kaydedilmis", "kare_bulunamadi"}


@uygulama.get("/cycle/{cycle_id}/denudasyon")
def denudasyon(request: Request, cycle_id: int, taraf: str = "",
               hata: str = "", duzenle: str = "", oosit: str = ""):
    hata = hata if hata in DENUDASYON_HATALARI else ""
    # Bu ekranda düzenlenebilecek iki ayrı şey var: cycle'ın denüdasyon saati
    # ve seçili oositin over'ı. Hangisi olduğu adreste yazıyor.
    duzenle = duzenle if duzenle in ("saat", "oosit") else ""
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    bekleyen = goruntuler.bekleyen_dosyalar()
    kayitli = db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.taraf, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id) AS kare, "
        "  (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "   ORDER BY g.id LIMIT 1) AS ilk_goruntu, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id = s.id) "
        "  AS goruntu_idler "
        "FROM specimen s WHERE s.cycle_id = ? ORDER BY s.cycle_sira_no", (cycle_id,)
    )
    son = db.tek(
        "SELECT id, specimen_id FROM goruntu WHERE cycle_id = ? AND asama = 'denudasyon' "
        "ORDER BY id DESC LIMIT 1", (cycle_id,)
    )
    # Üstteki numara şeridinden seçilen oosit; istenmemişse **ilki** (v6.35).
    # Kayıttan sonra hangi oositte kalınacağını POST adreste söylüyor; adres
    # bir şey demiyorsa ekran ilk kez açılıyor demektir ve baştan başlanır.
    sp = None
    if kayitli:
        if oosit:
            sp = next((o for o in kayitli if str(o["cycle_sira_no"]) == oosit), None)
        sp = sp or kayitli[0]

    # Yumurta Dondurma'da (oosit_cryo) ICSI aşaması hiç yok, o yüzden
    # maturasyon/bulgu değerlendirmesi burada, dondurmadan önce yapılıyor
    # (kullanıcının isteği). ivf_icsi'de bu ekranda gösterilmiyor -- o
    # değerlendirme zaten ICSI ekranında, iki yerde aynı soruyu sormamak için.
    mat, secili_bulgular = None, set()
    if sp and c["cycle_tipi"] == "oosit_cryo":
        mat = db.tek(
            "SELECT * FROM olay WHERE specimen_id=? AND tip='maturasyon_kontrolu' "
            "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (sp["id"],)
        )
        secili_bulgular = {r["bulgu_kodu"] for r in db.sorgu(
            "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='denudasyon'",
            (sp["id"],)
        )}

    return sablon.TemplateResponse(
        request, "denudasyon.html",
        {
            "c": c,
            "bekleyen": bekleyen,
            "simdiki": bekleyen[0] if bekleyen else None,
            "kayitli": kayitli,
            "sp": sp,
            "kareler": asama_goruntuleri(sp["id"], "denudasyon") if sp else [],
            "sonraki_sira": goruntuler.sonraki_sira(cycle_id),
            "son_goruntu": son,
            "gezinme": asama_gezinme(cycle_id, "denudasyon"),
         "taraf": taraf, "hata": hata,
         "duzenle": duzenle,
         "klasor": str(goruntuler.kaynak_klasor()),
            "klasor_var": goruntuler.kaynak_klasor().is_dir(),
            "bos_dosyalar": goruntuler.bos_dosyalar(),
            "mat": mat, "secili_bulgular": secili_bulgular,
            "maturasyonlar": db.liste("maturasyon"),
            "bulgular": db.liste("bulgu_icsi"),
            "simdi": _dt.now().strftime("%Y-%m-%dT%H:%M"),
        },
    )


def _specimen_sirasi(specimen_id) -> str:
    """Örneğin cycle içindeki sıra numarası (adrese yazmak için metin)."""
    r = db.tek("SELECT cycle_sira_no FROM specimen WHERE id = ?", (specimen_id,))
    return str(r["cycle_sira_no"]) if r else ""


@uygulama.post("/cycle/{cycle_id}/denudasyon")
async def denudasyon_islem(request: Request, cycle_id: int):
    f = dict(await request.form())
    eylem = f.get("eylem")
    im = f.get("imza") or ""
    kid = request.state.kullanici["id"]
    c = db.tek(
        "SELECT id, cycle_no, opu_sag_oosit, opu_sol_oosit FROM cycle WHERE id = ?",
        (cycle_id,),
    )

    taraf = f.get("taraf") or None

    # Kayıttan sonra hangi oosit açık kalacak (v6.35). Ekran artık kendiliğinden
    # sonuncuyu seçmiyor -- seçimi adres söylüyor, o yüzden buradan taşınıyor.
    # Formdan gelen değer adrese yazılacağı için yalnızca rakam kabul ediliyor.
    secili = (f.get("secili") or "").strip()
    secili = secili if secili.isdigit() else ""

    hata = ""

    if eylem == "yeni":
        sid = goruntuler.specimen_olustur(cycle_id, c["cycle_no"], taraf)
        gid = goruntuler.goruntu_bagla(im, cycle_id, c["cycle_no"], sid,
                                       "denudasyon", kid)
        if gid is not None:
            secili = _specimen_sirasi(sid)
        else:
            # Kare bağlanamadı. Eskiden oosit yine de açık kalıyordu: telefonda
            # çift dokunmak "fotoğrafsız" bir hayalet oosit bırakıyor ve oosit
            # sayısını şişiriyordu — hiçbir uyarı da çıkmıyordu. Oosit sayısı
            # klinik bir sayı, yanlış olamaz. Kaydı geri al ve sebebini söyle.
            goruntuler.bos_specimen_sil(sid)
            hata = ("kare_zaten_kaydedilmis" if goruntuler.kare_islenmis(im)
                    else "kare_bulunamadi")

    elif eylem == "ayni":
        son = db.tek(
            "SELECT id FROM specimen WHERE cycle_id=? ORDER BY cycle_sira_no DESC LIMIT 1",
            (cycle_id,),
        )
        if son:
            gid = goruntuler.goruntu_bagla(im, cycle_id, c["cycle_no"], son["id"],
                                           "denudasyon", kid)
            if gid is None:
                hata = ("kare_zaten_kaydedilmis" if goruntuler.kare_islenmis(im)
                        else "kare_bulunamadi")
            else:
                secili = _specimen_sirasi(son["id"])

    elif eylem == "fotografsiz":
        secili = _specimen_sirasi(
            goruntuler.specimen_olustur(cycle_id, c["cycle_no"], taraf))

    elif eylem == "atla":
        goruntuler.atla(im, cycle_id)

    elif eylem == "geri":
        goruntuler.geri_al(int(f.get("goruntu_id")))

    elif eylem == "hepsi":
        # OPU'da toplanan sayı kadar oosit kaydını fotoğrafsız açar
        # (kullanıcının isteği): "Oosit 1", "Oosit 2" ... hazır dursun,
        # fotoğraf her birine sonra tek tek eklensin. Zaten oluşturulmuş
        # olanlar sayılıp yalnızca **eksik** kadarı ekleniyor -- düğmeye
        # ikinci kez basmak fazladan oosit açmaz.
        toplam = (c["opu_sag_oosit"] or 0) + (c["opu_sol_oosit"] or 0)
        mevcut = db.tek(
            "SELECT COUNT(*) n FROM specimen WHERE cycle_id=?", (cycle_id,)
        )["n"]
        for _ in range(max(0, toplam - mevcut)):
            goruntuler.specimen_olustur(cycle_id, c["cycle_no"])

    # Kare eklemek çalışma kipinde yapılıyor; kayıttan sonra orada kal
    # (v6.24). Yoksa her kayıtta özet ekranına düşüp tekrar Düzenle demek
    # gerekirdi -- 20 oositlik bir cycle'da 20 fazladan dokunuş. "Hepsi"
    # kamera akışının parçası değil, fotoğrafsız açılan oositlerin listesini
    # görmek için salt görüntülemeye dönüyor.
    if eylem == "hepsi":
        return RedirectResponse(f"/cycle/{cycle_id}/denudasyon", status_code=303)

    yol = f"/cycle/{cycle_id}/denudasyon?duzenle=oosit"
    if secili:
        yol += f"&oosit={secili}"
    if taraf:
        yol += f"&taraf={taraf}"
    if hata:
        yol += f"&hata={hata}"
    return RedirectResponse(yol, status_code=303)


# ----------------------------------------------------------------- androloji (sperm)

SPERM_ORNEK_KOLON = [
    "alinma_zamani", "alinma_yontemi", "abstinans_gun", "likefaksiyon_zamani",
    "hacim_ml", "renk", "viskozite", "ph", "hazirlama_yontemi",
    "hazirlama_zamani", "notlar",
]

SPERM_ANALIZ_KOLON = [
    "hacim_ml", "konsantrasyon_milyon_ml", "pr_yuzde", "np_yuzde", "im_yuzde",
    "total_motil_yuzde", "toplam_motil_sayi", "morfoloji_normal_yuzde",
    "vitalite_yuzde", "yuvarlak_hucre_milyon_ml", "lokosit_milyon_ml",
    "aglutinasyon", "notlar",
]


def _sperm_ornek_form(f):
    """Form sözlüğünden sperm_ornek alanlarını çıkarır (sayı alanları doğrulanır)."""
    return {
        "alinma_zamani": zaman(f.get("alinma_zamani")),
        "alinma_yontemi": bos_ise_none(f.get("alinma_yontemi")),
        "abstinans_gun": tam(f.get("abstinans_gun"), "Abstinans günü"),
        "likefaksiyon_zamani": zaman(f.get("likefaksiyon_zamani")),
        "hacim_ml": sayi(f.get("hacim_ml"), "Hacim"),
        "renk": bos_ise_none(f.get("renk")),
        "viskozite": bos_ise_none(f.get("viskozite")),
        "ph": sayi(f.get("ph"), "pH"),
        "hazirlama_yontemi": bos_ise_none(f.get("hazirlama_yontemi")),
        "hazirlama_zamani": zaman(f.get("hazirlama_zamani")),
        "notlar": bos_ise_none(f.get("ornek_notlar")),
    }


def _sperm_analiz_form(f, on):
    """`on` = 'bazal_' veya 'sonrasi_'. sperm_analiz alan sözlüğü döndürür."""
    def s(ad, etiket):
        return sayi(f.get(on + ad), etiket)
    return {
        "hacim_ml": s("hacim_ml", "Hacim"),
        "konsantrasyon_milyon_ml": s("konsantrasyon_milyon_ml", "Konsantrasyon"),
        "pr_yuzde": s("pr_yuzde", "İlerleyen (PR) %"),
        "np_yuzde": s("np_yuzde", "İlerlemeyen (NP) %"),
        "im_yuzde": s("im_yuzde", "Hareketsiz (IM) %"),
        "total_motil_yuzde": s("total_motil_yuzde", "Total motilite %"),
        "toplam_motil_sayi": s("toplam_motil_sayi", "TMSC"),
        "morfoloji_normal_yuzde": s("morfoloji_normal_yuzde", "Morfoloji %"),
        "vitalite_yuzde": s("vitalite_yuzde", "Vitalite %"),
        "yuvarlak_hucre_milyon_ml": s("yuvarlak_hucre_milyon_ml", "Yuvarlak hücre"),
        "lokosit_milyon_ml": s("lokosit_milyon_ml", "Lökosit"),
        "aglutinasyon": bos_ise_none(f.get(on + "aglutinasyon")),
        "notlar": bos_ise_none(f.get(on + "notlar")),
    }


@uygulama.get("/cycle/{cycle_id}/androloji")
def androloji(request: Request, cycle_id: int, ornek: str = "",
              hata: str = "", duzenle: int = 0):
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    ornekler = db.sorgu(
        "SELECT * FROM sperm_ornek WHERE cycle_id = ? ORDER BY id", (cycle_id,))

    yeni_mi = ornek == "yeni" or not ornekler
    secili = None
    if not yeni_mi:
        if ornek:
            secili = next((o for o in ornekler if str(o["id"]) == ornek), None)
        secili = secili or (ornekler[0] if ornekler else None)

    analizler = {}
    if secili:
        for r in db.sorgu("SELECT * FROM sperm_analiz WHERE sperm_ornek_id = ?",
                          (secili["id"],)):
            analizler[r["asama"]] = r

    # Bu tedavide kullanılan, başka bir hastaya (eşe) ait dondurulmuş sperm
    # var mı (v6.86) -- taze örnekten (sperm_ornek) tamamen bağımsız, aynı
    # ekranda ayrı bir kart olarak gösteriliyor.
    sd_baglanti = db.tek(
        "SELECT sd.*, t.etiket, h.dosya_no, h.ad_soyad FROM sperm_dondurma sd "
        "JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "JOIN hasta h ON h.id = sd.hasta_id "
        "WHERE sd.kullanim_cycle_id=? AND sd.iptal_mi=0", (cycle_id,))

    # Bu tedavinin hastası (= bu dosya numarası) adına dondurulmuş, henüz
    # hiçbir tedaviye bağlanmamış sperm var mı (v6.125, kullanıcının isteği:
    # "elle eşleme var, bir de dosya numarası üzerinden bu şekilde uyarı
    # ver"). Elle eşleme ekranı (`/androloji/sperm-baglama`) duruyor ve
    # bütün laboratuvarı arıyor — kayıt bilerek başka bir hastaya ait
    # olabildiği için (v6.86). Buradaki fark, aramayı beklemeden haber
    # vermesi: dosya numarası tutuyorsa eşleşme kesindir, personelin
    # arayarak bulmasına gerek yok.
    dosya_sperm = (hastanin_sperm_kayitlari(c["hasta_id"], yalnizca_bagsiz=True)
                   if not sd_baglanti else [])

    return sablon.TemplateResponse(
        request, "androloji.html",
        {
            "c": c,
            "dosya_sperm": dosya_sperm,
            "ornekler": ornekler,
            "secili": secili,
            "yeni_mi": yeni_mi,
            "bazal": analizler.get("bazal"),
            "sonrasi": analizler.get("hazirlik_sonrasi"),
            "alinma": db.liste("sperm_alinma"),
            "hazirlama": db.liste("sperm_hazirlama"),
            "viskoziteler": db.liste("viskozite"),
            "aglutinasyonlar": db.liste("sperm_aglutinasyon"),
            "gorunumler": db.liste("sperm_gorunum"),
            "simdi": _dt.now().strftime("%Y-%m-%dT%H:%M"),
            "hata": hata, "duzenle": duzenle,
            "sd_baglanti": sd_baglanti,
            "gezinme": asama_gezinme(cycle_id, "androloji"),
        },
    )


@uygulama.get("/cycle/{cycle_id}/androloji/sperm-baglama")
def androloji_sperm_baglama_ekran(request: Request, cycle_id: int, ara: str = ""):
    """Başka bir hastaya ait, henüz hiçbir tedavide kullanılmamış dondurulmuş
    sperm kayıtlarını arayıp bu tedaviye bağlama ekranı (v6.86).
    """
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    taban = (
        "SELECT sd.id, sd.dondurma_zamani, sd.sebep, t.etiket, "
        "  h.dosya_no, h.ad_soyad "
        "FROM sperm_dondurma sd JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "JOIN hasta h ON h.id = sd.hasta_id "
        "WHERE sd.lab_id=? AND sd.iptal_mi=0 AND sd.kullanim_cycle_id IS NULL")
    if ara.strip():
        # `h.ad_soyad` her zaman büyük harfle kayıtlı (v6.115) -- SQLite'ın
        # LIKE'ı Türkçe ı/ş/ğ/ö/ü/ç'de büyük/küçük harf eşitlemiyor, arama
        # terimi de `tr_buyuk()`'ten geçmeli (v6.116). `t.etiket` bu kurala
        # tabi değil, kendi yazıldığı gibi aranıyor.
        kayitlar = db.sorgu(
            taban + " AND (t.etiket LIKE ? OR CAST(h.dosya_no AS TEXT) LIKE ? "
            "OR h.ad_soyad LIKE ?) ORDER BY sd.dondurma_zamani DESC",
            (db.LAB_ID, f"%{ara}%", f"%{ara}%", f"%{tr_buyuk(ara)}%"))
    else:
        kayitlar = db.sorgu(
            taban + " ORDER BY sd.dondurma_zamani DESC", (db.LAB_ID,))

    return sablon.TemplateResponse(
        request, "androloji_sperm_baglama.html",
        {"c": c, "ara": ara, "kayitlar": kayitlar})


@uygulama.post("/cycle/{cycle_id}/androloji/sperm-baglama/{sperm_dondurma_id}")
def androloji_sperm_bagla(request: Request, cycle_id: int, sperm_dondurma_id: int):
    # Bağlama mantığı tek yerde (v6.139) -- hasta kartı da aynı işi yapıyor.
    sperm_tedaviye_bagla(sperm_dondurma_id, cycle_id)
    return RedirectResponse(f"/cycle/{cycle_id}/androloji", status_code=303)


@uygulama.post("/cycle/{cycle_id}/androloji/sperm-baglanti-kaldir/{sperm_dondurma_id}")
def androloji_sperm_baglanti_kaldir(request: Request, cycle_id: int, sperm_dondurma_id: int):
    # Yalnızca BU tedaviye bağlıysa kaldır -- başka bir tedavinin bağını
    # bu ekrandan koparmak yanlış olurdu (v6.86'nın davranışı korunuyor).
    if db.tek("SELECT 1 x FROM sperm_dondurma WHERE id=? AND kullanim_cycle_id=?",
              (sperm_dondurma_id, cycle_id)):
        sperm_baglanti_kaldir(sperm_dondurma_id)
    return RedirectResponse(f"/cycle/{cycle_id}/androloji", status_code=303)


@uygulama.post("/cycle/{cycle_id}/androloji")
async def androloji_kaydet(request: Request, cycle_id: int):
    from urllib.parse import quote

    f = dict(await request.form())
    kid = request.state.kullanici["id"]
    c = db.tek("SELECT id FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    ornek_id = (f.get("ornek_id") or "").strip()

    try:
        ornek_d = _sperm_ornek_form(f)
        analiz_d = {
            "bazal": _sperm_analiz_form(f, "bazal_"),
            "hazirlik_sonrasi": _sperm_analiz_form(f, "sonrasi_"),
        }
    except FormHatasi as e:
        # duzenle=1: hata mesaji formun ustunde cikmali, kart modunda degil
        geri = f"/cycle/{cycle_id}/androloji?duzenle=1&hata={quote(str(e))}"
        if ornek_id:
            geri += f"&ornek={ornek_id}"
        return RedirectResponse(geri, status_code=303)

    analiz_dolu = {a: any(v is not None for v in d.values())
                   for a, d in analiz_d.items()}

    if ornek_id:
        eski = db.tek("SELECT * FROM sperm_ornek WHERE id = ?", (ornek_id,))
        if not eski or eski["cycle_id"] != cycle_id:
            return RedirectResponse(f"/cycle/{cycle_id}/androloji", status_code=303)
        oid = int(ornek_id)
        guvenlik.degisiklikleri_yaz("sperm_ornek", oid, eski, ornek_d, kid)
        set_ifade = ", ".join(f"{k} = ?" for k in SPERM_ORNEK_KOLON)
        db.yaz(f"UPDATE sperm_ornek SET {set_ifade} WHERE id = ?",
               (*[ornek_d[k] for k in SPERM_ORNEK_KOLON], oid))
    else:
        # Yeni örnek: hiçbir örnek alanı ve hiçbir analiz dolu değilse kayıt açma
        if not any(v is not None for v in ornek_d.values()) \
                and not any(analiz_dolu.values()):
            return RedirectResponse(f"/cycle/{cycle_id}/androloji", status_code=303)
        kolon = ", ".join(["lab_id", "cycle_id", "kullanici_id"] + SPERM_ORNEK_KOLON)
        isaret = ", ".join(["?"] * (3 + len(SPERM_ORNEK_KOLON)))
        oid = db.yaz(
            f"INSERT INTO sperm_ornek ({kolon}) VALUES ({isaret})",
            (db.LAB_ID, cycle_id, kid, *[ornek_d[k] for k in SPERM_ORNEK_KOLON]))

    for asama, d in analiz_d.items():
        mevcut = db.tek(
            "SELECT * FROM sperm_analiz WHERE sperm_ornek_id = ? AND asama = ?",
            (oid, asama))
        if analiz_dolu[asama]:
            zamani = islem_zamani(
                f.get("bazal_zaman" if asama == "bazal" else "sonrasi_zaman"))
            if mevcut:
                guvenlik.degisiklikleri_yaz("sperm_analiz", mevcut["id"], mevcut,
                                            {**d, "zaman": zamani}, kid)
                set_ifade = ", ".join(f"{k} = ?" for k in SPERM_ANALIZ_KOLON)
                db.yaz(f"UPDATE sperm_analiz SET {set_ifade}, zaman = ?, "
                       "kullanici_id = ? WHERE id = ?",
                       (*[d[k] for k in SPERM_ANALIZ_KOLON], zamani, kid,
                        mevcut["id"]))
            else:
                kolon = ", ".join(["sperm_ornek_id", "asama", "zaman",
                                   "kullanici_id"] + SPERM_ANALIZ_KOLON)
                isaret = ", ".join(["?"] * (4 + len(SPERM_ANALIZ_KOLON)))
                db.yaz(f"INSERT INTO sperm_analiz ({kolon}) VALUES ({isaret})",
                       (oid, asama, zamani, kid, *[d[k] for k in SPERM_ANALIZ_KOLON]))
        elif mevcut:
            db.yaz("DELETE FROM sperm_analiz WHERE id = ?", (mevcut["id"],))

    return RedirectResponse(f"/cycle/{cycle_id}/androloji?ornek={oid}",
                            status_code=303)


# ----------------------------------------------------------------- işlemi yapan

@uygulama.post("/cycle/{cycle_id}/islem-yapan")
async def islem_yapan_kaydet(request: Request, cycle_id: int):
    f = dict(await request.form())
    asama = (f.get("asama") or "").strip()
    yapan = bos_ise_none(f.get("yapan_ad"))
    kid = request.state.kullanici["id"]
    c = db.tek("SELECT id FROM cycle WHERE id = ?", (cycle_id,))
    gecerli_asamalar = {a[0] for a in ASAMA_SIRASI}
    # Ekrana giremeyen kişi oraya ad da yazamamalı. `yol_modulu` form içeriğini
    # göremediği için bu kontrol burada (v6.14).
    if c and asama in gecerli_asamalar and yetkim(asama):
        simdi = _dt.now().isoformat(" ", "seconds")
        mevcut = db.tek(
            "SELECT * FROM islem_yapan WHERE cycle_id = ? AND asama = ?",
            (cycle_id, asama))
        if mevcut:
            guvenlik.degisiklikleri_yaz("islem_yapan", mevcut["id"], mevcut,
                                        {"yapan_ad": yapan}, kid)
            db.yaz("UPDATE islem_yapan SET yapan_ad = ?, zaman = ?, "
                   "kullanici_id = ? WHERE id = ?",
                   (yapan, simdi, kid, mevcut["id"]))
        else:
            db.yaz("INSERT INTO islem_yapan (lab_id, cycle_id, asama, yapan_ad, "
                   "zaman, kullanici_id) VALUES (?,?,?,?,?,?)",
                   (db.LAB_ID, cycle_id, asama, yapan, simdi, kid))
    geri = request.headers.get("referer") or f"/cycle/{cycle_id}"
    return RedirectResponse(geri, status_code=303)


@uygulama.get("/dosya/{goruntu_id}")
def dosya(goruntu_id: int):
    g = db.tek("SELECT dosya_yolu FROM goruntu WHERE id = ?", (goruntu_id,))
    if not g:
        return Response(status_code=404)
    p = goruntuler.tam_yol(g["dosya_yolu"])
    if not p.is_file():
        return Response(status_code=404)
    return FileResponse(p)


@uygulama.get("/onizleme")
def onizleme(imza: str = ""):
    """Kuyruktaki dosyanın önizlemesi. Yol dışarıdan gelmez, imzayla bulunur."""
    p = goruntuler.dosya_bul(imza)
    if not p:
        return Response(status_code=404)
    return FileResponse(p)


# ----------------------------------------------------------------- silme

@uygulama.get("/hasta/{hasta_id}/sil")
def hasta_sil_ekran(request: Request, hasta_id: int, hata: str = ""):
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    if not hasta:
        return RedirectResponse("/hastalar", status_code=303)
    sayilar = db.tek(
        "SELECT (SELECT COUNT(*) FROM cycle WHERE hasta_id=?) AS cycle, "
        "  (SELECT COUNT(*) FROM specimen s JOIN cycle c ON c.id=s.cycle_id "
        "   WHERE c.hasta_id=?) AS oosit, "
        "  (SELECT COUNT(*) FROM goruntu g JOIN cycle c ON c.id=g.cycle_id "
        "   WHERE c.hasta_id=?) AS goruntu, "
        "  (SELECT COUNT(*) FROM olay o JOIN cycle c ON c.id=o.cycle_id "
        "   WHERE c.hasta_id=?) AS olay, "
        "  (SELECT COUNT(*) FROM gebelik_sonucu g JOIN cycle c ON c.id=g.cycle_id "
        "   WHERE c.hasta_id=?) AS gebelik",
        (hasta_id,) * 5,
    )
    transferler = hasta_transfer_kayitlari(hasta_id)
    return sablon.TemplateResponse(
        request, "hasta_sil.html",
        {"h": hasta, "s": sayilar, "hata": hata, "transferler": transferler}
    )


@uygulama.post("/hasta/{hasta_id}/sil")
async def hasta_sil(request: Request, hasta_id: int):
    from urllib.parse import quote
    f = dict(await request.form())
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    if not hasta:
        return RedirectResponse("/hastalar", status_code=303)

    def hata(m):
        return RedirectResponse(
            f"/hasta/{hasta_id}/sil?hata={quote(m)}", status_code=303)

    if (f.get("onay") or "").strip() != str(hasta["dosya_no"]):
        return hata("Dosya numarası doğru yazılmadı.")

    kid = request.state.kullanici["id"]
    eylem = f.get("eylem") or "arsivle"

    if eylem == "sil":
        tr = hasta_transfer_kayitlari(hasta_id)
        if tr:
            return hata(
                f"Bu hastanın {len(tr)} transfer kaydı var. Transfere gitmiş "
                "embriyo içeren kayıtlar kalıcı olarak silinemez; arşivle.")
        if (f.get("onay2") or "").strip().upper() != "SIL":
            return hata("Kalıcı silme için ikinci onay kutusuna SIL yazılmalı.")

        cycles = [r["id"] for r in db.sorgu(
            "SELECT id FROM cycle WHERE hasta_id=?", (hasta_id,))]
        say = db.tek(
            "SELECT (SELECT COUNT(*) FROM specimen s JOIN cycle c ON c.id=s.cycle_id "
            "        WHERE c.hasta_id=?) AS oosit, "
            "  (SELECT COUNT(*) FROM goruntu g JOIN cycle c ON c.id=g.cycle_id "
            "   WHERE c.hasta_id=?) AS goruntu, "
            "  (SELECT COUNT(*) FROM sperm_dondurma WHERE hasta_id=?) AS sperm",
            (hasta_id, hasta_id, hasta_id))
        silme_logla(
            "hasta", hasta_id,
            f"dosya {hasta['dosya_no']} · {hasta['ad_soyad']} · "
            f"{len(cycles)} tedavi · {say['oosit']} oosit · {say['goruntu']} goruntu · "
            f"{say['sperm']} sperm dondurma",
            kid)
        try:
            for cid in cycles:
                cycle_tamamen_sil(cid, kid)
            # Cycle'a değil doğrudan hastaya bağlı: kendi taşıyıcısı hep
            # tek başına (bir kayıt = bir taşıyıcı), "kardeş var mı" kontrolü
            # gerekmiyor -- cycle_tamamen_sil'in 5. adımının basiti.
            sd_tasiyicilar = [r["tasiyici_id"] for r in db.sorgu(
                "SELECT tasiyici_id FROM sperm_dondurma WHERE hasta_id=?", (hasta_id,))]
            # Onam ekleri `sperm_dondurma`'ya FK ile bağlı (v6.101) — önce
            # onlar silinmezse bir sonraki satır FOREIGN KEY hatası verir
            # (tuzak #4'ün aynısı, test edilirken gerçekten böyle patladı).
            for r in db.sorgu(
                "SELECT id FROM sperm_dondurma_dosya WHERE sperm_dondurma_id IN "
                "(SELECT id FROM sperm_dondurma WHERE hasta_id=?)", (hasta_id,)):
                goruntuler.sperm_onam_sil(r["id"])
            db.yaz("DELETE FROM sperm_dondurma WHERE hasta_id=?", (hasta_id,))
            for tid in sd_tasiyicilar:
                t = db.tek("SELECT konum_id FROM tasiyici WHERE id=?", (tid,))
                db.yaz("DELETE FROM tasiyici WHERE id=?", (tid,))
                if t and t["konum_id"]:
                    db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))
            db.yaz("DELETE FROM hasta WHERE id = ?", (hasta_id,))
        except Exception as e:
            return hata(f"Silme sırasında hata: {type(e).__name__}: {e}")
        return RedirectResponse("/hastalar", status_code=303)

    guvenlik.degisiklikleri_yaz("hasta", hasta_id, hasta, {"durum": "arsiv"}, kid)
    db.yaz("UPDATE hasta SET durum = 'arsiv' WHERE id = ?", (hasta_id,))
    return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)


@uygulama.post("/hasta/{hasta_id}/geri-al")
def hasta_geri_al(request: Request, hasta_id: int):
    hasta = db.tek("SELECT * FROM hasta WHERE id = ?", (hasta_id,))
    if hasta:
        guvenlik.degisiklikleri_yaz(
            "hasta", hasta_id, hasta, {"durum": "aktif"},
            request.state.kullanici["id"],
        )
        db.yaz("UPDATE hasta SET durum = 'aktif' WHERE id = ?", (hasta_id,))
    return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)


# ----------------------------------------------------------------- cycle silme

def cycle_bagli_sayilar(cycle_id: int):
    return db.tek(
        "SELECT (SELECT COUNT(*) FROM specimen WHERE cycle_id=?) AS oosit, "
        "       (SELECT COUNT(*) FROM goruntu WHERE cycle_id=?) AS goruntu, "
        "       (SELECT COUNT(*) FROM olay WHERE cycle_id=?) AS olay, "
        "       (SELECT COUNT(*) FROM sperm_ornek WHERE cycle_id=?) AS sperm, "
        "       (SELECT COUNT(*) FROM gebelik_sonucu WHERE cycle_id=?) AS gebelik",
        (cycle_id, cycle_id, cycle_id, cycle_id, cycle_id),
    )


@uygulama.get("/cycle/{cycle_id}/sil")
def cycle_sil_ekran(request: Request, cycle_id: int, hata: str = ""):
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    if not c:
        return RedirectResponse("/hastalar", status_code=303)
    s = cycle_icerik_sayilari(cycle_id)
    bos = all(s[k] == 0 for k in s.keys())
    transferler = cycle_transfer_kayitlari(cycle_id)
    return sablon.TemplateResponse(
        request, "cycle_sil.html",
        {"c": c, "s": s, "bos": bos, "hata": hata, "transferler": transferler}
    )


@uygulama.post("/cycle/{cycle_id}/sil")
async def cycle_sil(request: Request, cycle_id: int):
    from urllib.parse import quote
    f = dict(await request.form())
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    def hata(m):
        return RedirectResponse(
            f"/cycle/{cycle_id}/sil?hata={quote(m)}", status_code=303)

    if (f.get("onay") or "").strip() != str(c["cycle_no"]):
        return hata("Lab kayıt numarası doğru yazılmadı.")

    kid = request.state.kullanici["id"]
    hasta_id = c["hasta_id"]
    eylem = f.get("eylem") or "iptal"

    if eylem == "sil":
        tr = cycle_transfer_kayitlari(cycle_id)
        if tr:
            return hata(
                f"Bu tedavinin {len(tr)} transfer kaydı var. Transfere gitmiş "
                "tedavi kalıcı olarak silinemez; iptal et.")
        if (f.get("onay2") or "").strip().upper() != "SIL":
            return hata("Kalıcı silme için ikinci onay kutusuna SIL yazılmalı.")
        say = cycle_icerik_sayilari(cycle_id)
        silme_logla(
            "cycle", cycle_id,
            f"lab no {c['cycle_no']} · {say['oosit']} oosit · {say['olay']} islem · "
            f"{say['goruntu']} goruntu",
            kid)
        try:
            cycle_tamamen_sil(cycle_id, kid)
        except Exception as e:
            return hata(f"Silme sırasında hata: {type(e).__name__}: {e}")
        # Yanlış açılmış bir tedavi silindi: sonrakiler bir öne kayar (v6.144).
        tedavi_sirasini_duzelt(hasta_id, kid)
        return RedirectResponse(f"/hasta/{hasta_id}", status_code=303)

    guvenlik.degisiklikleri_yaz("cycle", cycle_id, c, {"durum": "iptal"}, kid)
    db.yaz("UPDATE cycle SET durum = 'iptal' WHERE id = ?", (cycle_id,))
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


@uygulama.post("/cycle/{cycle_id}/geri-al")
def cycle_geri_al(request: Request, cycle_id: int):
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if c:
        guvenlik.degisiklikleri_yaz(
            "cycle", cycle_id, c, {"durum": "aktif"}, request.state.kullanici["id"]
        )
        db.yaz("UPDATE cycle SET durum = 'aktif' WHERE id = ?", (cycle_id,))
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


# ------------------------------------------------------------ cycle bitişi

# Adresten gelen anahtar doğrudan `metin()`'e verilmez — beyaz liste (tuzak #9)
BITIS_HATALARI = {"bitis_sebebi_secilmedi", "goc_gerekli_kisa"}


@uygulama.get("/cycle/{cycle_id}/bitir")
def cycle_bitir_ekrani(request: Request, cycle_id: int, hata: str = "",
                       duzenle: int = 0):
    """Laboratuvar işi bitti: cycle yapılacaklar listesinden düşsün.

    Ayrı bir ekran, çünkü sebep ve bitiş saati soruluyor ve yanlışlıkla
    basılmaması gerek. Silme ekranıyla karıştırılmasın: bu bir iptal değil,
    işin olağan sonu.

    `?duzenle=1` bitmiş bir cycle'ın kaydını değiştirmek için: sebep ve saat
    doldurulmuş gelir (v6.31). Cycle listeye geri dönmez — geri almak ayrı
    bir düğme.
    """
    c = db.tek(
        "SELECT c.*, h.ad_soyad, h.dosya_no FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)
    return sablon.TemplateResponse(
        request, "cycle_bitir.html",
        {"kullanici": request.state.kullanici, "c": c, "duzenle": duzenle,
         "simdi": _dt.now().strftime("%Y-%m-%dT%H:%M"),
         "goc_gerekli": not _bitis_kolonu_var(),
         "iptal_detay_sebepleri": IPTAL_DETAY_SEBEPLERI,
         "hata": metinler.t(hata) if hata in BITIS_HATALARI else ""},
    )



@uygulama.post("/cycle/{cycle_id}/bitir")
def cycle_bitir(request: Request, cycle_id: int, sebep: str = Form(""),
                bitis_zamani: str = Form(""), duzenle: int = Form(0)):
    # Hata dönüşü formu kapatmamalı: düzenleme kipinden gelindiyse orada
    # kalınıyor, yoksa normal bitir ekranına (v6.21'deki kural).
    kip = "&duzenle=1" if duzenle else ""
    if not _bitis_kolonu_var():
        return RedirectResponse(
            f"/cycle/{cycle_id}/bitir?hata=goc_gerekli_kisa{kip}",
            status_code=303)
    if sebep not in BITIS_DURUMU:
        return RedirectResponse(
            f"/cycle/{cycle_id}/bitir?hata=bitis_sebebi_secilmedi{kip}",
            status_code=303)
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    # Bitiş saati elle girilebilir; boş ya da bozuksa "şu an" (v6.31).
    # "İşlem saatleri elle girilebilir" kuralı bu ekranda da geçerli:
    # personel işi bitirirken değil, akşam kaydediyor olabilir.
    yeni = {"durum": BITIS_DURUMU[sebep], "bitis_sebebi": sebep,
            "bitis_zamani": islem_zamani(bitis_zamani)}
    guvenlik.degisiklikleri_yaz(
        "cycle", cycle_id, c, yeni, request.state.kullanici["id"])
    db.yaz("UPDATE cycle SET durum = ?, bitis_sebebi = ?, bitis_zamani = ? "
           "WHERE id = ?",
           (yeni["durum"], yeni["bitis_sebebi"], yeni["bitis_zamani"], cycle_id))
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


@uygulama.post("/cycle/{cycle_id}/bitisi-geri-al")
def cycle_bitisi_geri_al(request: Request, cycle_id: int):
    """Yanlışlıkla bitirilen cycle listeye geri döner.

    Silmenin "Geri al"ından ayrı: orası `yetkim("silme")` istiyor, burası
    istemiyor. Bitirmek günlük bir iş, silmek değil.
    """
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if c:
        yeni = {"durum": "aktif", "bitis_sebebi": None, "bitis_zamani": None}
        guvenlik.degisiklikleri_yaz(
            "cycle", cycle_id, c, yeni, request.state.kullanici["id"])
        if _bitis_kolonu_var():
            db.yaz("UPDATE cycle SET durum = 'aktif', bitis_sebebi = NULL, "
                   "bitis_zamani = NULL WHERE id = ?", (cycle_id,))
        else:
            db.yaz("UPDATE cycle SET durum = 'aktif' WHERE id = ?", (cycle_id,))
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


@uygulama.get("/bitenler")
def bitenler(request: Request):
    """Biten cycle'lar — kâğıt düzendeki arşiv klasörü."""
    return sablon.TemplateResponse(
        request, "bitenler.html",
        {"kullanici": request.state.kullanici, "liste": cycle_listesi(True)},
    )


@uygulama.get("/devam-eden")
def devam_eden(request: Request):
    """Devam Eden Tedaviler'in tam listesi — ana ekran ilk 5'i gösterir
    (v6.78, kullanıcının isteği), "Tümü" oraya 5'ten fazlaysa çıkıyor."""
    return sablon.TemplateResponse(
        request, "devam_eden.html",
        {"kullanici": request.state.kullanici, "liste": cycle_listesi()},
    )


@uygulama.get("/yaklasanlar")
def yaklasanlar_tumu(request: Request):
    """Yaklaşan Tedaviler'in tam listesi — ana ekran ilk 5'i gösterir
    (v6.78, kullanıcının isteği), "Tümü" oraya 5'ten fazlaysa çıkıyor."""
    return sablon.TemplateResponse(
        request, "yaklasanlar.html",
        {"kullanici": request.state.kullanici,
         "liste": cycle_listesi(yaklasan=YAKLASAN_GUN),
         "yaklasan_gun": YAKLASAN_GUN},
    )


# ------------------------------------------------------------- Excel çıktısı

# Dosya `.xlsx` olarak **indiriliyor**, tarayıcıda açılmıyor: içinde hasta adı
# var, ekranda açık kalmasın; ayrıca Excel dosyası zaten görüntülenemez.
EXCEL_TURU = ("application/vnd.openxmlformats-officedocument"
              ".spreadsheetml.sheet")


def excel_yaniti(ad_koku: str, sayfalar) -> Response:
    """Sayfalardan .xlsx üretip indirilecek dosya olarak döndürür."""
    return Response(
        excel.kitap(sayfalar),
        media_type=EXCEL_TURU,
        headers={"Content-Disposition":
                 f'attachment; filename="{excel.dosya_adi(ad_koku)}"'},
    )


@uygulama.get("/disari/ay")
def disari_ay(request: Request, yil: int = 0, ay: int = 0):
    """Hasta kayıtlarındaki ay görünümünün Excel hali, satır başına bir cycle.

    "Bu ay kaç vaka yaptık, sonuçları ne" sorusunun cevabı: istatistik ve
    kurum raporu için. Ölçü ekrandakiyle aynı — OPU tarihi, yoksa cycle'ın
    açıldığı tarih.
    """
    bugun = _dt.now()
    yil = yil or bugun.year
    ay = ay if 1 <= ay <= 12 else bugun.month
    baslik = ay_adi(yil, ay)
    return excel_yaniti(
        f"ay_{yil}_{ay:02d}",
        disari.ay_sayfalari(f"{yil:04d}-{ay:02d}", baslik))


@uygulama.get("/disari/cycle/{cycle_id}")
def disari_cycle(request: Request, cycle_id: int):
    """Bir cycle'ın tamamı: bilgi sayfası + örnek başına bir satır.

    Hastanın dosyasına konacak ya da yazdırılacak çıktı.
    """
    ad, sayfalar = disari.cycle_sayfalari(cycle_id)
    if not sayfalar:
        return RedirectResponse("/hastalar", status_code=303)
    return excel_yaniti(f"cycle_{ad}", sayfalar)


@uygulama.get("/disari/cryo")
def disari_cryo(request: Request):
    """Dolabın dökümü — sayım ve envanter için."""
    return excel_yaniti("cryo", disari.cryo_sayfalari())


def _istatistik_donemi(yil: int, ay: int) -> tuple:
    """Adresten gelen yıl/ay'ı makul bir döneme oturtur (v6.123).

    Değer `?yil=`/`?ay=` ile **dışarıdan** geliyor; üç şeyi birden yapması
    gerekiyor:

    - **Sayıya sabitlemek.** `ay_str` buradan çıkıp `disari.istatistikler()`
      içinde SQL metnine giriyor. Orada tırnak da ayıklanıyor ama asıl
      güvence bu: değer iki tamsayıdan kuruluyor, adresten gelen metin
      hiçbir zaman sorguya ulaşmıyor (tuzak #9'un sorgu hali).
    - **Yıl aralığını kapatmak.** `_yil_araligi()` seçili yılı listeye
      zorla ekliyor; `?yil=99999` gelseydi seçicide doksan bin satır
      olurdu. Sınır tarih doğrulamasının kendi sınırı (`EN_ESKI_YIL` ..
      bu yıl + `EN_YENI_YIL_PAYI`) — iki ayrı "makul yıl" tanımı olmasın
      diye aynı sabitler kullanılıyor.
    - **Boş gelince bugüne düşmek**, `/hastalar`'ın ay gezgininde olduğu
      gibi: ekran ilk açıldığında içinde bulunulan ay görünsün.
    """
    bugun = _dt.now()
    yil = min(max(yil or bugun.year, EN_ESKI_YIL),
              bugun.year + EN_YENI_YIL_PAYI)
    ay = ay if 1 <= ay <= 12 else bugun.month
    return yil, ay


@uygulama.get("/istatistik")
def istatistik_ekrani(request: Request, yil: int = 0, ay: int = 0,
                      kayitsayfa: int = 1):
    """Yönetici panelindeki istatistikler — **anlık hesaplanır, saklanmaz**.

    Kullanıcının sorusu "her kayıt anlık kaydedilebilir mi" idi; cevap
    kaydetmeye gerek olmadığı: sayılar zaten kayıtların kendisinden çıkıyor.
    Ayrı bir sayaç aynı bilgiyi iki yere yazmak olurdu ve biri ötekinden ayrı
    düşerdi (bkz. `disari.istatistikler`).

    **Ay seçilebiliyor** (v6.123, kullanıcının isteği: "aylık olarak oranlar
    tutulsun ... yıl ve tarih seçerek bakabileyim"). "Tutulsun" yine ayrı
    bir tabloya yazmak değil: `istatistikler(ay)` zaten aya süzebiliyordu,
    ekranda karşılığı yoktu. Dört oran (M2, 2PN, blastokist, klinik
    gebelik) hem seçilen ay hem laboratuvarın tamamı için yan yana
    basılıyor — bir ayın oranı ancak kendi ortalamasıyla birlikte bir şey
    anlatıyor.

    Ayın ölçüsü **ekranlardakiyle aynı**: OPU tarihi, yoksa tedavinin
    açıldığı tarih (`disari.istatistikler`). `/hastalar`'ın ay listesiyle
    aynı ölçü olsun diye — iki ekran aynı ayda farklı sayıda tedavi
    gösterseydi hangisinin doğru olduğu anlaşılmazdı.

    **"Son kayıtlar" ayrı sayfalanıyor** (`?kayitsayfa=`, v6.124) ve ay
    seçicisinden **bağımsız**: o kart "bu hafta ne yapıldı" penceresi,
    seçilen aya değil bugüne bakıyor. İki sayaç aynı adreste durduğu için
    kartın sayfa bağlantıları `yil`/`ay`'ı taşımak zorunda — yoksa sayfa
    çevirmek seçili ayı bugüne sıfırlardı (`/hastalar`'ın `sayfa`/`aysayfa`
    ikilisinde çözülen sorunun aynısı). Sayfa numarası `son_kayitlar()`
    içinde kendi aralığına sabitleniyor.

    Yalnızca yönetici: ekran laboratuvarın bütün üretimini ve son girilen
    hasta adlarını tek sayfada gösteriyor.
    """
    engel = yonetici_kontrol(request)
    if engel:
        return engel
    yil, ay = _istatistik_donemi(yil, ay)
    return sablon.TemplateResponse(
        request, "istatistik.html",
        {"g": disari.istatistikler(),
         "ga": disari.istatistikler(f"{yil:04d}-{ay:02d}"),
         "aylar": disari.istatistik_aylari(yil),
         "son": disari.son_kayitlar(kayitsayfa),
         "yil": yil, "ay": ay,
         "yillar": _yil_araligi(yil),
         "onceki": _ay_kaydir(yil, ay, -1),
         "sonraki": _ay_kaydir(yil, ay, 1),
         "kullanici": request.state.kullanici},
    )


@uygulama.get("/disari/istatistik")
def disari_istatistik(request: Request, yil: int = 0):
    """İstatistiklerin Excel hali — ekranla aynı izin: yalnızca yönetici.

    `yil` ekrandaki düğmeden geliyor: bakılan yıl insin, kullanıcı dosyayı
    açtığında başka bir yılın tablosunu bulmasın.
    """
    engel = yonetici_kontrol(request)
    if engel:
        return engel
    yil, _ = _istatistik_donemi(yil, 0)
    return excel_yaniti(f"istatistik_{yil}", disari.istatistik_sayfalari(yil))


@uygulama.get("/disari/tumu")
def disari_tumu(request: Request):
    """Bütün tabloların ham dökümü — **yalnızca yönetici**.

    Ötekiler ekranda görülebilen veriyi dosyaya yazıyor; bu, laboratuvarın
    bütün hasta kayıtlarını tek dosyada klinik dışına çıkarabilir. O yüzden
    ekranda düğmeyi gizlemek yetmiyor, sunucu da reddediyor — hasta silmedeki
    kuralın aynısı.
    """
    engel = yonetici_kontrol(request)
    if engel:
        return engel
    return excel_yaniti("tum_veri", disari.tumu_sayfalari())


# ------------------------------------------------------------- resmî formlar

# Kullanıcının tutmak zorunda olduğu formlar. İki çıktı: tarayıcıdan
# yazdırılabilir sayfa (`/form/...`) ve Excel (`/disari/form/...`). İçerik tek
# yerden geliyor -- `formlar.py` -- ki ikisi birbirinden ayrı düşmesin.
# Basılabilir resmî formlar. Her satır: veriyi çeken fonksiyon, kalıba
# yazılacakları hazırlayan fonksiyon, kalıbın adı (`form_kalip.json`), indirilen
# dosyanın kökü ve Excel sayfasının adı.
FORMLAR = {
    ad: satir for ad, satir in (
        ("ozet", (formlar.ozet_verisi, formlar.ozet_dolgu, "ozet",
                  "form_ozet", "Embriyoloji Özet Formu")),
        ("artlab", (formlar.artlab_verisi, formlar.artlab_dolgu, "artlab",
                    "form_artlab", "ART Lab. Raporu")),
    ) if satir[2] in form_kalip.KALIPLAR
}


# Gömülü formlar **bu** laboratuvarın kurum belgeleri: doküman kodu, alan
# adları ve amblem onun kalite sisteminden. Başka bir laboratuvarda ekranda
# durmaları yanlış -- personel yanlışlıkla basarsa ortaya başka bir kurumun
# formunda gerçek hasta verisi çıkar. O yüzden gizlenebiliyorlar (v6.41).
#
# Silinmiyor, gizleniyor: kalıp programın dosyasında, veritabanında değil.
# Ayar `ayarlar` tablosunda, varsayılanı görünür -- bu laboratuvarda hiçbir
# şey değişmiyor.
def gomulu_form_gizli(ad: str) -> bool:
    return db.ayar("form_gizli_" + ad) == "1"


def gomulu_formlar(yalniz_gorunen=True):
    """Programla gelen formlar. Kalıbı olmayan (ticari dağıtımda silinen) yok."""
    return [{"ad": ad, "baslik": metinler.t("form_" + ad),
             "gizli": gomulu_form_gizli(ad)}
            for ad in FORMLAR
            if not (yalniz_gorunen and gomulu_form_gizli(ad))]


@uygulama.get("/form/{ad}/{cycle_id}")
def form_ekrani(request: Request, ad: str, cycle_id: int):
    """Doldurulmuş formun yazdırılabilir hali.

    Adres parçası beyaz listeden geçiyor (`FORMLAR`): şablon adı adresten
    gelen metinle kurulsaydı başka bir dosya istenebilirdi.
    """
    if ad not in FORMLAR:
        return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)
    veri_al, dolgu, kalip, _, _ = FORMLAR[ad]
    v = veri_al(cycle_id)
    if not v:
        return RedirectResponse("/hastalar", status_code=303)
    # Ekranda basılan ızgara ile Excel'e giden ızgara **aynı kalıptan** geliyor.
    # `tasan`: ART Lab'ın dar FREEZE kutusu, yazısı sığmazsa sağdaki boş
    # kutulara akıyor (v6.135, kullanıcının kararı) -- kesilmesindense.
    # `sigdir`: sağı dolu ya da kenardaki kutuda yazı küçülüyor (v6.150).
    # İkisi de sayfanın dolgusuna bakıyor (v6.152): FET'te FREEZE'in yanındaki
    # THAW kutusu da dolu olabiliyor.
    sayfalar = [form_kalip.satirlar(
                    kalip, deger, ek,
                    tasan=formlar.tasan_hucreleri(ad, deger),
                    sigdir=formlar.sigdir_hucreleri(ad, deger))
                for deger, ek in dolgu(v)]
    return sablon.TemplateResponse(
        request, "form.html",
        {"sayfalar": sayfalar, "baslik": metinler.t("form_" + ad),
         "cycle_id": cycle_id, "yon": form_kalip.yon(kalip),
         "excel_yolu": f"/disari/form/{ad}/{cycle_id}",
         # Yalnızca ART Lab'da (v6.104) -- Özet'te aynı bilgi zaten NOTLAR
         # kutusuna karışıyor (bkz. formlar.ozet_verisi), ikinci kez basılmasın.
         "iptal_notu": v.get("iptal_notu") if ad == "artlab" else None,
         "kullanici": request.state.kullanici},
    )


@uygulama.get("/disari/form/{ad}/{cycle_id}")
def form_excel(request: Request, ad: str, cycle_id: int):
    """Aynı formun .xlsx hali — Excel'den basmak ya da üstünde oynamak için."""
    if ad not in FORMLAR:
        return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)
    veri_al, dolgu, kalip, dosya, sayfa_adi = FORMLAR[ad]
    v = veri_al(cycle_id)
    if not v:
        return RedirectResponse("/hastalar", status_code=303)
    parcalar = dolgu(v)
    sayfalar = [
        form_kalip.yerlesim(
            kalip, sayfa_adi if len(parcalar) == 1 else f"{sayfa_adi} {i}",
            deger, ek, sigdir=formlar.sigdir_hucreleri(ad, deger))
        for i, (deger, ek) in enumerate(parcalar, start=1)
    ]
    if ad == "artlab" and v.get("iptal_notu"):
        # Kalıbın hemen altına, tek satır, tam genişlikte, "formadi" (büyük/
        # kalın/ortalı) adlı hazır stille -- kalıbın kendi stil listesine
        # dokunmuyor (v6.104, bkz. form.html'deki .formiptalnotu'nun eşi).
        satir_n, sutun_n = form_kalip.olcu(kalip)
        ilk = form_kalip.hucre_adresi(satir_n, 0)
        son = form_kalip.hucre_adresi(satir_n, sutun_n - 1)
        y = sayfalar[-1]
        y["hucreler"][ilk] = (v["iptal_notu"], "formadi")
        y["birlesik"] = y.get("birlesik", []) + [f"{ilk}:{son}"]
        y["yukseklikler"] = {**y.get("yukseklikler", {}), satir_n + 1: 22}
    return excel_yaniti(f"{dosya}_{v['dosya_no']}-{v['cycle_no']}", sayfalar)


# ------------------------------------------------- laboratuvarın kendi formu
#
# Gömülü iki form bu laboratuvarın; başka bir laboratuvar kendi formunu
# yükleyip programdaki verilerle doldurabilsin diye (v6.40, kullanıcının
# isteği). Yüklenen dosya `.xlsx`; kutuların içine `{{dosya_no}}` gibi
# etiketler yazılıyor ve program onları değerle değiştiriyor.
#
# **Hepsi yönetici işi.** Kalıp laboratuvarın resmî kâğıdı; onu değiştirmek
# ya da silmek personelin günlük işi değil.


def lab_formlari(yalniz_aktif=True):
    """Bu laboratuvarın yüklediği formlar. Kalıbın kendisi gelmiyor (büyük)."""
    kosul = " AND aktif_mi = 1" if yalniz_aktif else ""
    return db.sorgu(
        "SELECT id, ad, dosya_adi, yon, aktif_mi, bilinmeyen, "
        "olusturma_zamani FROM lab_formu "
        f"WHERE lab_id = ?{kosul} ORDER BY ad", (db.LAB_ID,))


def lab_formu_kalibi(form_id: int):
    """(kayıt, kalıp) ya da (None, None). Kalıp JSON metin olarak saklanıyor."""
    r = db.tek("SELECT * FROM lab_formu WHERE id = ? AND lab_id = ?",
               (form_id, db.LAB_ID))
    if not r:
        return None, None
    try:
        return r, json.loads(r["kalip"])
    except ValueError:
        return None, None


@uygulama.get("/formlar")
def lab_formlari_ekrani(request: Request, hata: str = "", eklendi: str = ""):
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(
        request, "lab_formlari.html",
        {"formlar": lab_formlari(yalniz_aktif=False),
         "gomulu": gomulu_formlar(yalniz_gorunen=False),
         "hata": metinler.t(hata) if hata in FORM_HATALARI else "",
         "eklendi": eklendi,
         "kullanici": request.state.kullanici},
    )


# Yükleme hataları adresten geliyor; `metin()` bulamadığı anahtarı olduğu gibi
# döndürdüğü için beyaz listeden geçiyor (tuzak #9).
FORM_HATALARI = {
    "form_hata_dosya", "form_hata_ad", "form_hata_okuma", "form_hata_bos",
}


@uygulama.post("/formlar/yukle")
async def lab_formu_yukle(request: Request):
    red = yonetici_kontrol(request)
    if red:
        return red
    f = await request.form()
    ad = (f.get("ad") or "").strip()[:80]
    dosya = f.get("dosya")
    dosya_adi = getattr(dosya, "filename", "") or ""

    if not dosya_adi.lower().endswith(".xlsx"):
        return RedirectResponse("/formlar?hata=form_hata_dosya", status_code=303)
    icerik = await dosya.read() if dosya else b""

    try:
        kalip = xlsx_oku.kalip(icerik)
    except xlsx_oku.Hata as e:
        # Sebebi kullanıcıya gösteriliyor ama adresten değil: adrese yalnızca
        # beyaz listedeki anahtar yazılıyor, ayrıntı günlüğe.
        _gunluk.error("form yukleme hatasi: %s", e)
        return RedirectResponse("/formlar?hata=form_hata_okuma", status_code=303)

    if not any(s for s in kalip["satirlar"]):
        return RedirectResponse("/formlar?hata=form_hata_bos", status_code=303)

    # Formda geçen ama programda karşılığı olmayan etiketler: yazım hatası
    # olabilir. Silmiyoruz (form olduğu gibi basılsın), listede uyarıyoruz.
    bilinmeyen = [e for e in form_kalip.etiketler(kalip)
                  if e not in formlar.ALAN_ADLARI]

    ad = ad or kalip.get("ad") or dosya_adi.rsplit(".", 1)[0]
    db.yaz(
        "INSERT INTO lab_formu (lab_id, ad, dosya_adi, yon, kalip, "
        "bilinmeyen, kullanici_id, olusturma_zamani) VALUES (?,?,?,?,?,?,?,?)",
        (db.LAB_ID, ad[:80], dosya_adi[:120], kalip.get("yon", "dikey"),
         json.dumps(kalip, ensure_ascii=False),
         ", ".join(bilinmeyen[:20]) or None,
         request.state.kullanici["id"],
         _dt.now().isoformat(" ", "seconds")),
    )
    return RedirectResponse("/formlar?eklendi=" + str(len(kalip["satirlar"])),
                            status_code=303)


@uygulama.post("/formlar/{form_id}/kaldir")
def lab_formu_kaldir(request: Request, form_id: int):
    """Kalıcı siler. Kalıp klinik bir kayıt değil, laboratuvarın kâğıdı —
    yeniden yüklemek bir dosya seçmek kadar. Saklamanın bedeli var: her
    kalıp yüz kilobaytlarca JSON ve `lab.db` USB ile taşınan dosya."""
    red = yonetici_kontrol(request)
    if red:
        return red
    db.yaz("DELETE FROM lab_formu WHERE id = ? AND lab_id = ?",
           (form_id, db.LAB_ID))
    return RedirectResponse("/formlar", status_code=303)


@uygulama.post("/formlar/{form_id}/gizle")
def lab_formu_gizle(request: Request, form_id: int):
    """Cycle ekranında görünmesin, kaydı dursun."""
    red = yonetici_kontrol(request)
    if red:
        return red
    db.yaz("UPDATE lab_formu SET aktif_mi = 1 - aktif_mi "
           "WHERE id = ? AND lab_id = ?", (form_id, db.LAB_ID))
    return RedirectResponse("/formlar", status_code=303)


@uygulama.post("/formlar/gomulu/{ad}/gizle")
def gomulu_form_gizle(request: Request, ad: str):
    """Programla gelen formu cycle ekranından kaldırır/geri getirir.

    Adres parçası `FORMLAR` beyaz listesinden geçiyor: ayar anahtarı adresten
    gelen metinle kurulsaydı `ayarlar` tablosuna istenen satır yazılırdı.
    """
    red = yonetici_kontrol(request)
    if red:
        return red
    if ad in FORMLAR:
        db.yaz("INSERT INTO ayarlar (lab_id, anahtar, deger) VALUES (?,?,?) "
               "ON CONFLICT (lab_id, anahtar) DO UPDATE SET deger = excluded.deger",
               (db.LAB_ID, "form_gizli_" + ad,
                "0" if gomulu_form_gizli(ad) else "1"))
    return RedirectResponse("/formlar", status_code=303)


@uygulama.get("/formlar/etiketler")
def lab_formu_etiketleri(request: Request):
    """Forma yazılabilecek etiketlerin listesi -- kopyala, Excel'e yapıştır."""
    red = yonetici_kontrol(request)
    if red:
        return red
    return sablon.TemplateResponse(
        request, "form_etiketleri.html",
        {"alanlar": formlar.ALAN_ACIKLAMA,
         "kullanici": request.state.kullanici},
    )


@uygulama.get("/form/lab/{form_id}/{cycle_id}")
def lab_formu_ekrani(request: Request, form_id: int, cycle_id: int):
    """Yüklenen formun doldurulmuş, yazdırılabilir hali."""
    kayit, kalip = lab_formu_kalibi(form_id)
    if not kayit:
        return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)
    alan = formlar.alanlar(cycle_id)
    if alan is None:
        return RedirectResponse("/hastalar", status_code=303)
    return sablon.TemplateResponse(
        request, "form.html",
        {"sayfalar": [form_kalip.satirlar(kalip, alan=alan)],
         "baslik": kayit["ad"], "cycle_id": cycle_id,
         "yon": form_kalip.yon(kalip),
         "excel_yolu": f"/disari/form/lab/{form_id}/{cycle_id}",
         "kullanici": request.state.kullanici},
    )


@uygulama.get("/disari/form/lab/{form_id}/{cycle_id}")
def lab_formu_excel(request: Request, form_id: int, cycle_id: int):
    kayit, kalip = lab_formu_kalibi(form_id)
    if not kayit:
        return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)
    alan = formlar.alanlar(cycle_id)
    if alan is None:
        return RedirectResponse("/hastalar", status_code=303)
    return excel_yaniti(
        f"{kayit['ad']}_{alan['dosya_no']}-{alan['cycle_no']}",
        [form_kalip.yerlesim(kalip, kayit["ad"][:31], alan=alan)])


# ----------------------------------------------------------------- görüntü

@uygulama.get("/goruntu/{goruntu_id}/sil")
def goruntu_sil_ekran(request: Request, goruntu_id: int, geri: str = ""):
    g = db.tek(
        "SELECT g.*, c.cycle_no, h.dosya_no, h.ad_soyad, s.cycle_sira_no "
        "FROM goruntu g JOIN cycle c ON c.id = g.cycle_id "
        "JOIN hasta h ON h.id = c.hasta_id "
        "LEFT JOIN specimen s ON s.id = g.specimen_id WHERE g.id = ?",
        (goruntu_id,),
    )
    if not g:
        return RedirectResponse("/hastalar", status_code=303)
    etiketler = {r["kod"]: r["etiket"] for r in db.liste("goruntu_asama")}
    pdf_mi = (g["orijinal_dosya_adi"] or "").lower().endswith(".pdf")
    return sablon.TemplateResponse(
        request, "goruntu_sil.html",
        {"g": g, "asama_etiketi": etiketler.get(g["asama"], g["asama"]),
         "pdf_mi": pdf_mi, "geri": geri or f"/cycle/{g['cycle_id']}"},
    )


@uygulama.post("/goruntu/{goruntu_id}/sil")
async def goruntu_sil(request: Request, goruntu_id: int):
    f = dict(await request.form())
    g = db.tek("SELECT * FROM goruntu WHERE id = ?", (goruntu_id,))
    if not g:
        return RedirectResponse("/hastalar", status_code=303)
    cycle_id = g["cycle_id"]
    geri = f.get("geri") or f"/cycle/{cycle_id}"
    guvenlik.degisiklikleri_yaz(
        "goruntu", goruntu_id, g,
        {"durum": f"SILINDI ({g['asama']}, {g['orijinal_dosya_adi']})"},
        request.state.kullanici["id"],
    )
    goruntuler.goruntu_sil(goruntu_id)
    return RedirectResponse(geri, status_code=303)


@uygulama.get("/cycle/{cycle_id}/foto-ekle")
def foto_ekle_ekran(request: Request, cycle_id: int, hata: str = "",
                    specimen_id: str = "", asama: str = "", geri: str = ""):
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    if not c:
        return RedirectResponse("/hastalar", status_code=303)
    specimenler = db.sorgu(
        "SELECT id, cycle_sira_no FROM specimen WHERE cycle_id = ? "
        "ORDER BY cycle_sira_no", (cycle_id,)
    )
    return sablon.TemplateResponse(
        request, "foto_ekle.html",
        {"c": c, "specimenler": specimenler,
         "asamalar": db.liste("goruntu_asama"), "hata": hata,
         "secili_specimen": specimen_id, "secili_asama": asama or "diger",
         "geri": geri or f"/cycle/{cycle_id}"},
    )


@uygulama.post("/cycle/{cycle_id}/foto-ekle")
async def foto_ekle(request: Request, cycle_id: int):
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    form = await request.form()
    secim = form.get("specimen_id") or ""
    asama = form.get("asama") or "diger"
    geri = form.get("geri") or f"/cycle/{cycle_id}"
    dosyalar = form.getlist("dosyalar")
    kid = request.state.kullanici["id"]

    hatalar, eklenen = [], 0
    for d in dosyalar:
        ad = getattr(d, "filename", "") or ""
        if not ad:
            continue
        icerik = await d.read()

        if secim == "__yeni__":
            # Her dosya kendi oositini alir
            hedef = goruntuler.specimen_olustur(cycle_id, c["cycle_no"])
        else:
            hedef = secim or None

        mesaj = goruntuler.elle_ekle(
            icerik, ad, cycle_id, c["cycle_no"], hedef, asama, kid
        )
        if mesaj:
            hatalar.append(mesaj)
            # Bos kalan oositi geri al
            if secim == "__yeni__":
                bos = db.tek("SELECT COUNT(*) k FROM goruntu WHERE specimen_id=?",
                             (hedef,))["k"]
                if bos == 0:
                    db.yaz("DELETE FROM specimen WHERE id=?", (hedef,))
        else:
            eklenen += 1

    from urllib.parse import quote
    geri_ek = (f"&specimen_id={quote(secim)}&asama={quote(asama)}"
               f"&geri={quote(geri)}")
    if hatalar:
        return RedirectResponse(
            f"/cycle/{cycle_id}/foto-ekle?hata=" + quote(" ".join(hatalar)) + geri_ek,
            status_code=303,
        )
    if eklenen == 0:
        return RedirectResponse(
            f"/cycle/{cycle_id}/foto-ekle?hata=" + quote("Dosya secilmedi.") + geri_ek,
            status_code=303,
        )
    return RedirectResponse(geri, status_code=303)


@uygulama.post("/cycle/{cycle_id}/doktor-notu-ekle")
async def doktor_notu_ekle(request: Request, cycle_id: int):
    """Cycle'a doktor notu eki: fotoğraf veya PDF, oosite bağlanmaz (v6.81).

    `foto-ekle` ile aynı `goruntuler.elle_ekle()`'yi çağırır, yalnızca
    `asama="doktor_notu"` sabit ve izin verilen uzantılar PDF'i de içeriyor.
    """
    c = db.tek("SELECT * FROM cycle WHERE id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    form = await request.form()
    dosyalar = form.getlist("dosyalar")
    kid = request.state.kullanici["id"]

    hatalar, eklenen = [], 0
    for d in dosyalar:
        ad = getattr(d, "filename", "") or ""
        if not ad:
            continue
        icerik = await d.read()
        mesaj = goruntuler.elle_ekle(
            icerik, ad, cycle_id, c["cycle_no"], None, "doktor_notu", kid,
            izin_uzantilari=goruntuler.DOKTOR_NOTU_UZANTILARI,
        )
        if mesaj:
            hatalar.append(mesaj)
        else:
            eklenen += 1

    from urllib.parse import quote
    if hatalar:
        return RedirectResponse(
            f"/cycle/{cycle_id}?hata=" + quote(" ".join(hatalar)) + "#doktor-notu",
            status_code=303,
        )
    if eklenen == 0:
        return RedirectResponse(
            f"/cycle/{cycle_id}?hata=" + quote("Dosya secilmedi.") + "#doktor-notu",
            status_code=303,
        )
    return RedirectResponse(f"/cycle/{cycle_id}#doktor-notu", status_code=303)


# ----------------------------------------------------------------- oosit silme

@uygulama.get("/specimen/{specimen_id}/sil")
def specimen_sil_ekran(request: Request, specimen_id: str):
    sp = db.tek(
        "SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE s.id = ?", (specimen_id,)
    )
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    sayilar = db.tek(
        "SELECT (SELECT COUNT(*) FROM goruntu WHERE specimen_id=?) AS goruntu, "
        "       (SELECT COUNT(*) FROM olay WHERE specimen_id=? AND iptal_mi=0) AS olay, "
        "       (SELECT COUNT(*) FROM specimen_bulgu WHERE specimen_id=?) AS bulgu",
        (specimen_id, specimen_id, specimen_id),
    )
    return sablon.TemplateResponse(
        request, "specimen_sil.html", {"sp": sp, "s": sayilar}
    )


@uygulama.post("/specimen/{specimen_id}/sil")
def specimen_sil(request: Request, specimen_id: str):
    sp = db.tek("SELECT * FROM specimen WHERE id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)

    olay = db.tek(
        "SELECT COUNT(*) k FROM olay WHERE specimen_id=? AND iptal_mi=0", (specimen_id,)
    )["k"]
    if olay:
        return RedirectResponse(f"/specimen/{specimen_id}/sil?hata=1", status_code=303)

    cycle_id = sp["cycle_id"]
    kid = request.state.kullanici["id"]

    guvenlik.degisiklikleri_yaz(
        "specimen", specimen_id, sp,
        {"durum": f"SILINDI (oosit {sp['cycle_sira_no']})"}, kid,
    )

    # Bagli goruntuleri de kaldir (kameradan gelenler kuyruga doner)
    for g in db.sorgu("SELECT id FROM goruntu WHERE specimen_id = ?", (specimen_id,)):
        goruntuler.goruntu_sil(g["id"])

    db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id = ?", (specimen_id,))
    db.yaz("DELETE FROM specimen WHERE id = ?", (specimen_id,))
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)



# ----------------------------------------------------------------- ICSI

# ICSI ekranında "enjekte edilmedi" işaretlenen örnek -- immatür ya da
# dejenere oosit, `icsi_kaydet()`'in "enjekte" kutusu hayır iken yazdığı
# durum (v6.105, kullanıcının isteği). Maturasyon değerlendirildi (ICSI
# ekranı doldurulmuştu, `mat_deger` var) ama aktif bir `icsi` olayı yoksa
# enjekte=hayır seçilmiş demektir. **`specimen.durum == 'degenere'`e
# bakılmıyor** -- enjekte edilip SONRA dejenere olan örnek de aynı durumu
# yazar ama onun kendi `icsi` olayı vardır, bu ikisi karıştırılmamalı: biri
# "denenmedi", öteki "denendi, olmadı". `oosit_cryo`'da maturasyon
# denüdasyonda değerlendirildiği (v6.96) ve ICSI aşaması hiç olmadığı için
# bu koşul orada HER örnek için doğru çıkar -- yalnızca ICSI'nin gerçekten
# var olduğu ekranlarda (fert/cleavage/blast, vitrifikasyon'da yalnızca
# `ivf_icsi` iken) kullan.
_ICSI_YAPILMADI = (
    "EXISTS (SELECT 1 FROM olay m WHERE m.specimen_id = s.id "
    "AND m.tip = 'maturasyon_kontrolu' AND m.iptal_mi = 0) "
    "AND NOT EXISTS (SELECT 1 FROM olay i WHERE i.specimen_id = s.id "
    "AND i.tip = 'icsi' AND i.iptal_mi = 0)"
)

# Dejenere işaretlenmiş örnek (v6.139, kullanıcının isteği: "ICSI veya
# Fertilizasyon ekranında dejenere işaretlenen yumurta ileriki menülerde
# yumurtanın kutucuğunda Dej. kısaltmasıyla gösterilsin ve işlem yapılamasın.
# Yani cleavage ve Blast embriyo yazılamasın").
#
# **`specimen.durum`'a değil OLAY tablosuna bakıyor** -- `_ICSI_YAPILMADI`'nın
# gerekçesinin başka bir yüzü: `durum` her aşamada ÜZERİNE YAZILIYOR
# (`cleavage_kaydet()` `gun2` yazar, `vit_kaydet()` `dondurulmus`), yani
# dejenere bir örneğe bir kez kayıt girilirse `durum` artık 'degenere' demez
# ve süzgeç sessizce susardı. Olay kalıcı: ICSI'de "dejenere oldu" ya da
# fertilizasyonda "dejenere" seçilmiş olması iptal edilene kadar duruyor.
#
# İki kaynağı da kapsıyor çünkü kullanıcı ikisini birlikte söyledi. ICSI'de
# **enjekte edilmeden** dejenere denen örnek (`mat_deger='degenere'`) buraya
# GİRMİYOR -- onu `_ICSI_YAPILMADI` zaten yakalıyor ve o örnek cleavage/
# blastokistte hiç görünmüyor (v6.105, kullanıcı 2026-09-22'de "şu an nasılsa
# öyle kalsın" dedi); fertilizasyon ekranında ise kendi maturasyonuyla
# ("Dej.") görünüyor, aşağıdaki `mat_kisa()`'ya bak.
_DEJENERE = (
    "EXISTS (SELECT 1 FROM olay d WHERE d.specimen_id = s.id AND d.iptal_mi = 0 "
    "AND ((d.tip = 'icsi' AND d.icsi_sonuc = 'degenere') "
    "  OR (d.tip = 'fertilizasyon_kontrolu' AND d.fert_sonuc = 'degenere')))"
)


# ------------------------------------------- aşama ekranlarının ortak parçaları
#
# Yumurta Çözme'de (v6.147) ICSI, fertilizasyon, cleavage ve blastokist
# ekranları BAŞKA bir tedavinin yumurtalarını gösteriyor: bu tedavi için
# çözülenleri (`db.tedavi_ornekleri()`). Buradaki parçalar bunun getirdiği
# üç soruyu tek yerde yanıtlıyor: adresteki örnek hangisi (sıra no tek
# tedavide tekil), bir kayıt BU tedavinin mi, işlem saati çözmeden önce mi.


def _secili_ornek(oositler, oosit):
    """Adresteki `?oosit=` hangi örnek -- yoksa listenin ilki (v6.35).

    Seçim `specimen.id` ile (v6.62'de blastokistte, v6.147'den beri ICSI,
    fertilizasyon ve cleavage'da da): liste birden çok tedavinin
    yumurtalarını taşıyabiliyor ve `cycle_sira_no` yalnızca kendi tedavisinde
    tekil -- iki tedavide de "1." yumurta olabilir, o alanla eşleşmek yanlış
    yumurtayı seçerdi. v6.147'den önceki adres sıra numarası taşıyordu (açık
    kalmış bir sekmenin tazelemesi): liste tek tedavinin örnekleriyse numara
    orada hâlâ tekil, kabul ediliyor.
    """
    if oosit:
        sp = next((o for o in oositler if str(o["id"]) == oosit), None)
        if (sp is None and oosit.isdigit()
                and len({o["cycle_id"] for o in oositler}) == 1):
            sp = next((o for o in oositler if str(o["cycle_sira_no"]) == oosit),
                      None)
        if sp is not None:
            return sp
    return oositler[0]


def _sonraki_ornek(oositler, specimen_id, bos_mu):
    """"Kaydet → sıradaki" (v6.35): listede bu örnekten SONRAKİ ilk boş örnek.

    Listenin kendi sırası izleniyor, sıra no karşılaştırması değil (v6.62'de
    blastokistte, v6.147'den beri dört ekranda) -- liste birden çok tedaviden
    gelebiliyor. `bos_mu(o)`: o örneğe bu ekranda henüz kayıt girilmemiş mi.
    """
    idx = next((i for i, o in enumerate(oositler) if o["id"] == specimen_id),
               None)
    if idx is None:
        return None
    return next((o for o in oositler[idx + 1:] if bos_mu(o)), None)


def _tedavi_ek(cycle_tipi, cycle_id, o="o") -> str:
    """Aşama ekranının olay alt sorgusuna: kayıt BU tedavide mi yapıldı (v6.147).

    Yalnızca FET tiplerinde bir şey ekliyor. Yumurta Çözme'de çözülen
    yumurtanın kaynağında (Yumurta Dondurma'nın denüdasyonunda, v6.96) bir
    maturasyon kaydı var; ICSI ekranı onu kendi kaydı sanıp üzerine yazsaydı
    kaynağın kaydı bozulurdu. Kendi örneğini gösteren tiplerde koşul boş --
    orada her değerlendirme zaten o tedavinin, sorgu eskisiyle aynı kalıyor.
    Ölçü `db.olay_tedavisi()`: işlemden önceki son çözme bu tedavi için mi.
    """
    if cycle_tipi not in FET_TIPLERI:
        return ""
    return f" AND {db.bu_tedavide(cycle_id, o)}"


def _cozme_dejenere_sql(cycle_tipi, cycle_id) -> str:
    """Örnek BU tedavideki çözmede dejenere mi çıktı -- SELECT'e 0/1 ifadesi.

    Yalnızca FET tiplerinde anlamlı; ICSI ekranı böyle bir yumurtayı listede
    tutuyor ama kilitliyor (v6.139'un "gizlemek değil kilitlemek" kuralı):
    ölü yumurtaya maturasyon/enjeksiyon yazılmaz. Başka bir tedavideki çözme
    sayılmıyor: aynı embriyo sonra başka bir tedavide dejenere çıktıysa bu
    tedavinin geçmişi değişmez.
    """
    if cycle_tipi not in FET_TIPLERI:
        return "0"
    return ("CASE WHEN EXISTS (SELECT 1 FROM olay d WHERE d.specimen_id = s.id "
            "AND d.tip = 'thaw' AND d.iptal_mi = 0 AND d.thaw_sagkalim = 'degenere' "
            f"AND d.thaw_cycle_id = {int(cycle_id)}) THEN 1 ELSE 0 END")


def _bu_tedavideki_cozme(specimen_id, cycle_id):
    """Örneğin BU tedavi için yapılan (en son) çözmesi, yoksa None."""
    if not thaw_cycle_var():
        return None
    return db.tek("SELECT * FROM olay WHERE specimen_id=? AND tip='thaw' "
                  "AND iptal_mi=0 AND thaw_cycle_id=? ORDER BY id DESC LIMIT 1",
                  (specimen_id, cycle_id))


def _cozmeden_once(specimen_id, cycle_id, cycle_tipi, zaman) -> bool:
    """FET tiplerinde işlem saati bu tedavideki çözmeden ÖNCE mi (v6.147).

    Kayıt o zaman bu tedavinin sayılmazdı (`db.olay_tedavisi()` saate
    bakıyor): zaman çizelgesi onu kaynağa yazar, ICSI ekranı yazılan
    maturasyonu göremez ve her kayıtta yeni bir tane açardı. Ekran bu yüzden
    reddediyor ve sebebini yazıyor (`hata=cozmeden_once`); saati sessizce
    değiştirmiyor.
    """
    if cycle_tipi not in FET_TIPLERI:
        return False
    cz = _bu_tedavideki_cozme(specimen_id, cycle_id)
    return bool(cz and cz["zaman"] and str(zaman) < str(cz["zaman"]))


# Aşama ekranlarının adresten gelen hata anahtarları (tuzak #9: beyaz liste).
ASAMA_HATALARI = ("cozmeden_once",)


def _asama_hatasi(hata, sp, cycle_id) -> str:
    """Adresteki `?hata=` için ekrana basılacak metin -- tanınmıyorsa boş."""
    if hata not in ASAMA_HATALARI or not sp:
        return ""
    cz = _bu_tedavideki_cozme(sp["id"], cycle_id)
    return metinler.t("hata_cozmeden_once").format(
        z=gg_aa_yyyy_saat(cz["zaman"]) if cz else "")


def _hedef_tedavi(sp, cycle) -> int:
    """Silme ekranının ait olduğu tedavi: adresteki, örnek orada görünüyorsa.

    Yumurta Çözme'de (v6.147) silme bağlantısı örneğin KENDİ tedavisinden
    değil, çözüldüğü tedaviden geliyor -- blastokistin `?cycle=` deseni
    (v6.62). Burada adres yalnızca dönüşü değil hangi kaydın silineceğini de
    belirliyor, o yüzden doğrulanıyor: örnek o tedavi için çözülmüş olmalı.
    Değilse örneğin kendi tedavisi (eski davranış).
    """
    if cycle and cycle != sp["cycle_id"] and _bu_tedavideki_cozme(sp["id"], cycle):
        return cycle
    return sp["cycle_id"]


def _cozme_oncesi_durum(specimen_id, cycle_id) -> str:
    """Bir kayıt geri alınınca örneğin döneceği durum.

    Kendi tedavisinde yumurta 'oosit' durumuna döner (eski davranış).
    Çözüldüğü tedavide ise çözmenin yazdığı duruma: 'cozuldu', 'kismi_hasar'
    (thaw_kaydet()'in kuralı) -- yoksa transfer adayları listesi onu yine
    "dondurulmuş" ya da "yumurta" sanardı.
    """
    cz = _bu_tedavideki_cozme(specimen_id, cycle_id)
    if not cz:
        return "oosit"
    return "cozuldu" if cz["thaw_sagkalim"] == "canli" else (cz["thaw_sagkalim"]
                                                               or "cozuldu")


def asama_goruntuleri(specimen_id, asama):
    """Bir oositin belirli bir aşamadaki tüm kareleri."""
    if not specimen_id:
        return []
    return db.sorgu(
        "SELECT id FROM goruntu WHERE specimen_id=? AND asama=? ORDER BY id",
        (specimen_id, asama))


def icsi_durum(cycle_id: int, cycle_tipi=None):
    """Tedavinin yumurtaları ve ICSI kayıt durumları.

    Yumurta Çözme'de (v6.147) yumurtalar bu tedavi için çözülenler, maturasyon
    ve ICSI de BU tedavininki (`_tedavi_ek()`): çözülen yumurtanın kaynağında
    denüdasyonda yazılmış bir maturasyon var, o "bu yumurta ICSI ekranında
    kaydedildi" demek değil. `cozme_dejenere`: bu tedavideki çözmede dejenere
    çıktı -- listede kalır, kilitli.
    """
    ek = _tedavi_ek(cycle_tipi, cycle_id)
    return db.sorgu(
        "SELECT s.id, s.cycle_id, s.cycle_sira_no, s.durum, s.taraf, "
        "  (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama='icsi' ORDER BY g.id LIMIT 1) AS ilk_goruntu, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama='icsi') AS asama_kare, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id = s.id) "
        "  AS goruntu_idler, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id) AS kare, "
        "  (SELECT o.mat_deger FROM olay o WHERE o.specimen_id = s.id "
        f"   AND o.tip='maturasyon_kontrolu' AND o.iptal_mi=0{ek} "
        "   ORDER BY o.id DESC LIMIT 1) AS mat, "
        "  (SELECT o.icsi_sonuc FROM olay o WHERE o.specimen_id = s.id "
        f"   AND o.tip='icsi' AND o.iptal_mi=0{ek} ORDER BY o.id DESC LIMIT 1) AS icsi, "
        f"  {_cozme_dejenere_sql(cycle_tipi, cycle_id)} AS cozme_dejenere "
        f"FROM specimen s WHERE {db.tedavi_ornekleri(cycle_tipi)} "
        "ORDER BY s.cycle_id, s.cycle_sira_no",
        (cycle_id,),
    )


def olay_kaydet_veya_guncelle(specimen_id, cycle_id, tip, alanlar, kullanici_id,
                              zaman=None, ek_kosul="", ek_deger=()):
    """Aynı tipte kayıt varsa günceller (değişiklikleri loglar), yoksa ekler.

    zaman verilmezse şu an kullanılır. Geriye dönük kayıt için elle verilir.

    `ek_kosul`/`ek_deger` (v6.143): bir örneğin aynı tipte BİRDEN ÇOK kaydı
    olabilen olaylar için hangisinin güncelleneceği. Dondurma ve çözme artık
    öyle -- FET'te çözülüp yeniden dondurulan embriyonun iki dondurması, iki
    kez çözülenin iki çözmesi var; ek koşul verilmeseydi ikincisi birincinin
    üzerine yazardı. Koşul metni KODDAN gelir, hiçbir zaman adresten değil.
    Verilmezse eski davranış: o tipin en son kaydı.
    """
    mevcut = db.tek(
        "SELECT * FROM olay WHERE specimen_id=? AND tip=? AND iptal_mi=0 "
        + (f"AND ({ek_kosul}) " if ek_kosul else "") +
        "ORDER BY id DESC LIMIT 1", (specimen_id, tip, *ek_deger)
    )
    from datetime import datetime as _d
    simdi = zaman or _d.now().isoformat(" ", "seconds")

    if mevcut:
        guvenlik.degisiklikleri_yaz("olay", mevcut["id"], mevcut, alanlar, kullanici_id)
        set_ifade = ", ".join(f"{a}=?" for a in alanlar)
        db.yaz(
            f"UPDATE olay SET {set_ifade}, zaman=?, kullanici_id=? WHERE id=?",
            (*alanlar.values(), simdi, kullanici_id, mevcut["id"]),
        )
        return mevcut["id"]

    kolonlar = ", ".join(alanlar)
    isaret = ", ".join("?" * len(alanlar))
    return db.yaz(
        f"INSERT INTO olay (lab_id, specimen_id, cycle_id, tip, zaman, "
        f"kullanici_id, {kolonlar}) VALUES (?,?,?,?,?,?,{isaret})",
        (db.LAB_ID, specimen_id, cycle_id, tip, simdi, kullanici_id,
         *alanlar.values()),
    )


@uygulama.get("/cycle/{cycle_id}/icsi")
def icsi_ekran(request: Request, cycle_id: int, oosit: str = "",
               duzenle: int = 0, hata: str = ""):
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    oositler = icsi_durum(cycle_id, c["cycle_tipi"])
    if not oositler:
        return sablon.TemplateResponse(
            request, "icsi.html",
            {"c": c, "oositler": [], "sp": None, "kayit": None,
             "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
             "gezinme": asama_gezinme(cycle_id, "icsi"),
             "bekleyen": bekleyen_ozet(),
             "bulgular": [], "secili_bulgular": set(), "kareler": [],
             "maturasyonlar": db.liste("maturasyon"),
             "zorluklar": db.liste("gecis_zorlugu"), "duzenle": duzenle},
        )

    # Hangi oosit gösterilecek: adreste yazan, yoksa **ilki** (v6.35).
    sp = _secili_ornek(oositler, oosit)

    # Maturasyon ve ICSI BU tedavininki (v6.147, `icsi_durum()`'un belgesi).
    ek = _tedavi_ek(c["cycle_tipi"], cycle_id)
    mat = db.tek(
        "SELECT o.* FROM olay o WHERE o.specimen_id=? AND o.tip='maturasyon_kontrolu' "
        f"AND o.iptal_mi=0{ek} ORDER BY o.id DESC LIMIT 1", (sp["id"],)
    )
    ic = db.tek(
        "SELECT o.* FROM olay o WHERE o.specimen_id=? AND o.tip='icsi' "
        f"AND o.iptal_mi=0{ek} ORDER BY o.id DESC LIMIT 1", (sp["id"],)
    )
    secili = {
        r["bulgu_kodu"] for r in db.sorgu(
            "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
            (sp["id"],)
        )
    }
    return sablon.TemplateResponse(
        request, "icsi.html",
        {
            "c": c, "oositler": oositler, "sp": sp,
            "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
            "gezinme": asama_gezinme(cycle_id, "icsi"),
            "kareler": asama_goruntuleri(sp["id"], "icsi"),
            "bekleyen": bekleyen_ozet(),
            "mat": mat, "ic": ic, "secili_bulgular": secili,
            "bulgular": db.liste("bulgu_icsi"),
            "maturasyonlar": db.liste("maturasyon"),
            "zorluklar": db.liste("gecis_zorlugu"), "duzenle": duzenle,
            "hata": _asama_hatasi(hata, sp, cycle_id),
        },
    )


@uygulama.post("/cycle/{cycle_id}/icsi")
async def icsi_kaydet(request: Request, cycle_id: int):
    f = await request.form()
    specimen_id = f.get("specimen_id")
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse(f"/cycle/{cycle_id}/icsi", status_code=303)
    c = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle_id,))
    tip = c["cycle_tipi"] if c else None
    burasi = f"/cycle/{cycle_id}/icsi?oosit={sp['id']}"

    kid = request.state.kullanici["id"]
    mat = f.get("mat_deger") or None
    if not mat:
        return RedirectResponse(burasi, status_code=303)

    # Bu tedavideki çözmede dejenere çıkan yumurtaya kayıt açılmaz (v6.147) --
    # ekran formu basmıyor, asıl engel burada. Var olan kayıt düzeltilebilir
    # (`_dejenere_engel()`'in kuralı).
    ek = _tedavi_ek(tip, cycle_id, "olay")
    if tip in FET_TIPLERI and db.tek(
            "SELECT 1 x FROM specimen s WHERE s.id = ? AND "
            + _cozme_dejenere_sql(tip, cycle_id) + " = 1", (specimen_id,)) \
            and not db.tek("SELECT 1 x FROM olay WHERE specimen_id=? AND "
                           "tip='maturasyon_kontrolu' AND iptal_mi=0" + ek,
                           (specimen_id,)):
        return RedirectResponse(burasi, status_code=303)

    simdi = islem_zamani(f.get("islem_zamani"))
    if _cozmeden_once(specimen_id, cycle_id, tip, simdi):
        return RedirectResponse(burasi + "&duzenle=1&hata=cozmeden_once",
                                status_code=303)
    # olay.cycle_id örneğin KENDİ tedavisi (v6.62 kuralı; Yumurta Çözme'de
    # rotanınki değil). Hangi kaydın güncelleneceği: BU tedavininki (v6.147)
    # -- kaynağın denüdasyon maturasyonu ezilmesin.
    ek_kosul = ek[len(" AND "):] if ek else ""
    olay_kaydet_veya_guncelle(
        specimen_id, sp["cycle_id"], "maturasyon_kontrolu", {"mat_deger": mat},
        kid, simdi, ek_kosul=ek_kosul
    )

    # Bulgular: küme olarak yazılır
    yeni_bulgular = set(f.getlist("bulgu"))
    eski_bulgular = {
        r["bulgu_kodu"] for r in db.sorgu(
            "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
            (specimen_id,))
    }
    if yeni_bulgular != eski_bulgular:
        guvenlik.degisiklikleri_yaz(
            "specimen_bulgu", specimen_id, {"bulgu": ", ".join(sorted(eski_bulgular))},
            {"bulgu": ", ".join(sorted(yeni_bulgular))}, kid,
        )
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
               (specimen_id,))
        for b in sorted(yeni_bulgular):
            db.yaz("INSERT INTO specimen_bulgu (specimen_id, asama, bulgu_kodu, "
                   "zaman, kullanici_id) VALUES (?,'icsi',?,?,?)",
                   (specimen_id, b, simdi, kid))

    # Enjeksiyon
    enjekte = f.get("enjekte") == "evet"
    if enjekte:
        olay_kaydet_veya_guncelle(
            specimen_id, sp["cycle_id"], "icsi",
            {"icsi_gecis_zorlugu": f.get("gecis_zorlugu") or None,
             "icsi_sonuc": f.get("icsi_sonuc") or "basarili"}, kid, simdi,
            ek_kosul=ek_kosul,
        )
        yeni_durum = ("degenere" if f.get("icsi_sonuc") == "degenere" else "enjekte")
    else:
        # Enjekte edilmediyse varsa eski ICSI kaydını iptal et
        eski = db.tek("SELECT id FROM olay WHERE specimen_id=? AND tip='icsi' "
                      "AND iptal_mi=0" + ek, (specimen_id,))
        if eski:
            db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
                   "iptal_sebep='enjekte edilmedi olarak degistirildi' WHERE id=?",
                   (kid, simdi, eski["id"]))
        yeni_durum = "degenere" if mat == "degenere" else "immatur"

    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (yeni_durum, specimen_id))

    # Sıradaki kaydedilmemiş oosite geç -- listenin sırasıyla (v6.147).
    sonraki = _sonraki_ornek(icsi_durum(cycle_id, tip), specimen_id,
                             lambda o: not o["mat"] and not o["cozme_dejenere"])
    hedef = f"/cycle/{cycle_id}/icsi"
    if sonraki:
        hedef += f"?oosit={sonraki['id']}"
    return RedirectResponse(hedef, status_code=303)


@uygulama.get("/specimen/{specimen_id}/icsi-sil")
def icsi_sil_ekran(request: Request, specimen_id: str, cycle: int = 0):
    sp = db.tek(
        "SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE s.id = ?", (specimen_id,)
    )
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    # Yumurta Çözme'de (v6.147) bağlantı çözüldüğü tedaviden geliyor; silinen
    # de o tedavinin kaydı (`_hedef_tedavi()`).
    hedef_cycle = _hedef_tedavi(sp, cycle)
    hc = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (hedef_cycle,))
    # ICSI aşaması olmayan tedavide (Yumurta Dondurma) "ICSI kaydını sil"
    # yok: orada maturasyon denüdasyonda yazıldı (v6.96), bu ekranın silmesi
    # onu da götürürdü. Adressiz eski bir bağlantı çözülen yumurtayı kendi
    # tedavisine düşürdüğünde (v6.147) böyle olur -- tedavi ekranına dön.
    if not hc or "icsi" not in TIP_ASAMALARI.get(hc["cycle_tipi"], ()):
        return RedirectResponse(f"/cycle/{hedef_cycle}", status_code=303)
    ek = _tedavi_ek(hc["cycle_tipi"], hedef_cycle)

    etiketler = {r["kod"]: r["etiket"]
                 for r in db.sorgu("SELECT kod, etiket FROM liste_degeri WHERE lab_id=?",
                                   (db.LAB_ID,))}
    mat = db.tek("SELECT o.* FROM olay o WHERE o.specimen_id=? "
                 f"AND o.tip='maturasyon_kontrolu' AND o.iptal_mi=0{ek} "
                 "ORDER BY o.id DESC LIMIT 1", (specimen_id,))
    ic = db.tek("SELECT o.* FROM olay o WHERE o.specimen_id=? AND o.tip='icsi' "
                f"AND o.iptal_mi=0{ek} ORDER BY o.id DESC LIMIT 1", (specimen_id,))
    bulgular = [etiketler.get(r["bulgu_kodu"], r["bulgu_kodu"]) for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
        (specimen_id,))]
    return sablon.TemplateResponse(
        request, "icsi_sil.html",
        {"sp": sp, "mat": mat, "ic": ic, "bulgular": bulgular, "etiketler": etiketler,
         "hedef_cycle": hedef_cycle},
    )


@uygulama.post("/specimen/{specimen_id}/icsi-sil")
async def icsi_sil(request: Request, specimen_id: str):
    f = dict(await request.form())
    sp = db.tek("SELECT * FROM specimen WHERE id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    try:
        hedef_cycle = _hedef_tedavi(sp, int(f.get("cycle") or 0))
    except ValueError:
        hedef_cycle = sp["cycle_id"]
    hc = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (hedef_cycle,))
    # Ekrandaki engelin aynısı (`icsi_sil_ekran()`): ICSI aşaması olmayan
    # tedavide hiçbir şey iptal edilmez.
    if not hc or "icsi" not in TIP_ASAMALARI.get(hc["cycle_tipi"], ()):
        return RedirectResponse(f"/cycle/{hedef_cycle}", status_code=303)
    ek = _tedavi_ek(hc["cycle_tipi"], hedef_cycle, "olay")

    from datetime import datetime as _d
    simdi = _d.now().isoformat(" ", "seconds")
    kid = request.state.kullanici["id"]

    # Olay kayitlari silinmez, iptal isaretlenir — denetim izi korunur.
    # Yumurta Çözme'de yalnızca BU tedavinin kaydı (v6.147): kaynağın
    # denüdasyonda yazdığı maturasyon yerinde kalır.
    for o in db.sorgu(
        "SELECT id, tip FROM olay WHERE specimen_id=? AND iptal_mi=0 "
        "AND tip IN ('maturasyon_kontrolu','icsi')" + ek, (specimen_id,)
    ):
        db.yaz(
            "UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
            "iptal_sebep='ICSI kaydi temizlendi' WHERE id=?",
            (kid, simdi, o["id"]),
        )

    eski = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
        (specimen_id,))}
    if eski:
        guvenlik.degisiklikleri_yaz(
            "specimen_bulgu", specimen_id, {"bulgu": ", ".join(sorted(eski))},
            {"bulgu": ""}, kid,
        )
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? AND asama='icsi'",
               (specimen_id,))

    # Kendi tedavisinde 'oosit'e, çözüldüğü tedavide (FET tipleri) çözmenin
    # durumuna döner.
    onceki = (_cozme_oncesi_durum(specimen_id, hedef_cycle)
              if hc["cycle_tipi"] in FET_TIPLERI else "oosit")
    guvenlik.degisiklikleri_yaz(
        "specimen", specimen_id, sp, {"durum": onceki}, kid
    )
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (onceki, specimen_id))

    return RedirectResponse(
        f"/cycle/{hedef_cycle}/icsi?oosit={sp['id']}", status_code=303
    )


# ----------------------------------------------------------------- fertilizasyon

def fert_durum(cycle_id: int, cycle_tipi=None):
    """Tedavinin yumurtaları ve fertilizasyon kayıtları. Yumurta Çözme'de
    (v6.147) bu tedavi için çözülenler (`db.tedavi_ornekleri()`)."""
    return db.sorgu(
        "SELECT s.id, s.cycle_id, s.cycle_sira_no, s.durum, s.taraf, "
        "  (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama='fertilizasyon_kontrolu' ORDER BY g.id LIMIT 1) "
        "  AS son_goruntu, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama='fertilizasyon_kontrolu') AS asama_kare, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id) AS kare, "
        "  (SELECT o.mat_deger FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='maturasyon_kontrolu' AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS mat, "
        "  (SELECT o.icsi_sonuc FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='icsi' AND o.iptal_mi=0 ORDER BY o.id DESC LIMIT 1) AS icsi, "
        "  (SELECT o.zaman FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='icsi' AND o.iptal_mi=0 ORDER BY o.id DESC LIMIT 1) AS icsi_zaman, "
        "  (SELECT o.fert_pn_sayisi FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS pn, "
        "  (SELECT o.fert_sonuc FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS fert, "
        f"  CASE WHEN {_ICSI_YAPILMADI} THEN 1 ELSE 0 END AS icsi_yapilmadi, "
        f"  CASE WHEN {_DEJENERE} THEN 1 ELSE 0 END AS dejenere "
        f"FROM specimen s WHERE {db.tedavi_ornekleri(cycle_tipi)} "
        "ORDER BY s.cycle_id, s.cycle_sira_no",
        (cycle_id,),
    )


@uygulama.get("/cycle/{cycle_id}/fert")
def fert_ekran(request: Request, cycle_id: int, oosit: str = "",
               duzenle: int = 0, hata: str = ""):
    c = db.tek(
        "SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
        "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,)
    )
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    oositler = fert_durum(cycle_id, c["cycle_tipi"])
    from datetime import datetime as _d
    ortak = {
        "c": c, "oositler": oositler,
        "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
        "gezinme": asama_gezinme(cycle_id, "fert"),
        "bekleyen": bekleyen_ozet(),
        "duzenle": duzenle,
        "sonuclar": db.liste("fert_sonuc"),
        "pn_sayilari": db.liste("pn_sayisi"),
        "pn_skorlari": db.liste("pn_skoru"),
        "bulgular": db.liste("bulgu_fert"),
        "hedef_saat": db.ayar("fert_kontrol_saat", "17"),
    }
    if not oositler:
        return sablon.TemplateResponse(
            request, "fert.html",
            {**ortak, "sp": None, "kayit": None, "secili_bulgular": set(),
             "gecen": None, "kareler": []},
        )

    sp = _secili_ornek(oositler, oosit)     # v6.35 -- bkz. ICSI ekranı

    kayit = db.tek(
        "SELECT * FROM olay WHERE specimen_id=? AND tip='fertilizasyon_kontrolu' "
        "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (sp["id"],)
    )
    secili = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? "
        "AND asama='fertilizasyon_kontrolu'", (sp["id"],))}

    # ICSI'den bu yana geçen süre
    gecen = None
    if sp["icsi_zaman"]:
        from datetime import datetime as _d
        try:
            gecen = round((_d.now() - _d.fromisoformat(sp["icsi_zaman"]))
                          .total_seconds() / 3600, 1)
        except ValueError:
            gecen = None

    return sablon.TemplateResponse(
        request, "fert.html",
        {**ortak, "sp": sp, "kayit": kayit, "secili_bulgular": secili, "gecen": gecen,
         "hata": _asama_hatasi(hata, sp, cycle_id)},
    )


@uygulama.post("/cycle/{cycle_id}/fert")
async def fert_kaydet(request: Request, cycle_id: int):
    f = await request.form()
    specimen_id = f.get("specimen_id")
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse(f"/cycle/{cycle_id}/fert", status_code=303)
    c = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle_id,))
    tip = c["cycle_tipi"] if c else None
    burasi = f"/cycle/{cycle_id}/fert?oosit={sp['id']}"

    kid = request.state.kullanici["id"]
    sonuc = f.get("fert_sonuc") or None
    if not sonuc:
        return RedirectResponse(burasi, status_code=303)

    pn = f.get("fert_pn_sayisi") or None
    skor = f.get("fert_pn_skoru") or None
    if sonuc != "normal":
        pn = skor = None            # dejenere/kayıpta PN sorulmaz
    if pn != "2":
        skor = None                 # Z sınıflaması yalnız 2PN için tanımlı

    simdi = islem_zamani(f.get("islem_zamani"))
    if _cozmeden_once(specimen_id, cycle_id, tip, simdi):
        return RedirectResponse(burasi + "&duzenle=1&hata=cozmeden_once",
                                status_code=303)
    # olay.cycle_id örneğin KENDİ tedavisi (v6.62; Yumurta Çözme'de, v6.147,
    # rotanınki değil).
    olay_kaydet_veya_guncelle(
        specimen_id, sp["cycle_id"], "fertilizasyon_kontrolu",
        {"fert_sonuc": sonuc, "fert_pn_sayisi": pn, "fert_pn_skoru": skor}, kid, simdi,
    )
    yeni_b = set(f.getlist("bulgu"))
    eski_b = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? "
        "AND asama='fertilizasyon_kontrolu'", (specimen_id,))}
    if yeni_b != eski_b:
        guvenlik.degisiklikleri_yaz(
            "specimen_bulgu", specimen_id,
            {"fert_bulgu": ", ".join(sorted(eski_b))},
            {"fert_bulgu": ", ".join(sorted(yeni_b))}, kid)
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? "
               "AND asama='fertilizasyon_kontrolu'", (specimen_id,))
        for b in sorted(yeni_b):
            db.yaz("INSERT INTO specimen_bulgu (specimen_id, asama, bulgu_kodu, "
                   "zaman, kullanici_id) "
                   "VALUES (?,'fertilizasyon_kontrolu',?,?,?)", (specimen_id, b, simdi, kid))

    if sonuc == "degenere":
        durum = "degenere"
    elif sonuc == "kayip":
        durum = "kayip"
    elif pn == "2":
        durum = "zigot"
    else:
        durum = f"{pn}pn" if pn else "kontrol_edildi"
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (durum, specimen_id))

    sonraki = _sonraki_ornek(fert_durum(cycle_id, tip), specimen_id,
                             lambda o: not o["fert"])
    hedef = f"/cycle/{cycle_id}/fert"
    if sonraki:
        hedef += f"?oosit={sonraki['id']}"
    return RedirectResponse(hedef, status_code=303)


@uygulama.get("/specimen/{specimen_id}/fert-sil")
def fert_sil_ekran(request: Request, specimen_id: str, cycle: int = 0):
    sp = db.tek(
        "SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE s.id = ?", (specimen_id,)
    )
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    kayit = db.tek(
        "SELECT * FROM olay WHERE specimen_id=? AND tip='fertilizasyon_kontrolu' "
        "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (specimen_id,))
    bulgular = [etiketler.get(r["bulgu_kodu"], r["bulgu_kodu"]) for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? "
        "AND asama='fertilizasyon_kontrolu'", (specimen_id,))]
    return sablon.TemplateResponse(
        request, "fert_sil.html",
        {"sp": sp, "kayit": kayit, "bulgular": bulgular, "etiketler": etiketler,
         # Yumurta Çözme'de (v6.147) ekran çözüldüğü tedaviden açılıyor.
         "hedef_cycle": _hedef_tedavi(sp, cycle)},
    )


@uygulama.post("/specimen/{specimen_id}/fert-sil")
async def fert_sil(request: Request, specimen_id: str):
    f = dict(await request.form())
    sp = db.tek("SELECT * FROM specimen WHERE id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    try:
        hedef_cycle = _hedef_tedavi(sp, int(f.get("cycle") or 0))
    except ValueError:
        hedef_cycle = sp["cycle_id"]
    from datetime import datetime as _d
    simdi = _d.now().isoformat(" ", "seconds")
    kid = request.state.kullanici["id"]

    for o in db.sorgu("SELECT id FROM olay WHERE specimen_id=? AND iptal_mi=0 "
                      "AND tip='fertilizasyon_kontrolu'", (specimen_id,)):
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep='Fertilizasyon kaydi temizlendi' WHERE id=?",
               (kid, simdi, o["id"]))

    eski = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? "
        "AND asama='fertilizasyon_kontrolu'", (specimen_id,))}
    if eski:
        guvenlik.degisiklikleri_yaz("specimen_bulgu", specimen_id,
            {"fert_bulgu": ", ".join(sorted(eski))}, {"fert_bulgu": ""}, kid)
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? "
               "AND asama='fertilizasyon_kontrolu'", (specimen_id,))

    hc = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (hedef_cycle,))
    onceki = "enjekte" if db.tek(
        "SELECT id FROM olay WHERE specimen_id=? AND tip='icsi' AND iptal_mi=0",
        (specimen_id,)) else (_cozme_oncesi_durum(specimen_id, hedef_cycle)
                              if hc and hc["cycle_tipi"] in FET_TIPLERI else "oosit")
    guvenlik.degisiklikleri_yaz("specimen", specimen_id, sp, {"durum": onceki}, kid)
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (onceki, specimen_id))

    return RedirectResponse(
        f"/cycle/{hedef_cycle}/fert?oosit={sp['id']}", status_code=303)


# ----------------------------------------------------------------- cleavage

def cleavage_durum(cycle_id: int, gun: int, cycle_tipi=None):
    """Tedavinin embriyoları ve o günün cleavage kayıtları. Yumurta Çözme'de
    (v6.147) bu tedavi için çözülen yumurtalardan gelişenler."""
    return db.sorgu(
        "SELECT s.id, s.cycle_id, s.cycle_sira_no, s.durum, s.taraf, "
        "  (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama = ? ORDER BY g.id LIMIT 1) AS goruntu, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama = ?) AS kare, "
        "  (SELECT o.fert_pn_sayisi FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS pn, "
        # Birleşmede sayı yerine `db.BIRLESME` (v6.157); şerit kısaltıyor.
        f"  (SELECT {db.cl_hucre_ifadesi('o')} FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='cleavage_degerlendirme' AND o.gun = ? AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS hucre, "
        "  (SELECT o.id FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='cleavage_degerlendirme' AND o.gun = ? AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS kayit_id, "
        # Dejenere örnek listeden DÜŞMÜYOR, kilitleniyor (v6.139): kullanıcı
        # "gösterilsin ve işlem yapılamasın" dedi -- gizlemek "hiç yoktu" der
        # gibi olurdu, oysa o yumurta toplandı ve dejenere oldu.
        f"  CASE WHEN {_DEJENERE} THEN 1 ELSE 0 END AS dejenere "
        f"FROM specimen s WHERE {db.tedavi_ornekleri(cycle_tipi)} "
        f"AND NOT ({_ICSI_YAPILMADI}) "
        "ORDER BY s.cycle_id, s.cycle_sira_no",
        (f"gun{gun}", f"gun{gun}", gun, gun, cycle_id),
    )


def _gun_olay(specimen_id, tip, gun):
    return db.tek(
        "SELECT * FROM olay WHERE specimen_id=? AND tip=? AND gun=? AND iptal_mi=0 "
        "ORDER BY id DESC LIMIT 1", (specimen_id, tip, gun)
    )


def _gun_olay_kaydet(specimen_id, cycle_id, tip, gun, alanlar, kid, zaman):
    mevcut = _gun_olay(specimen_id, tip, gun)
    if mevcut:
        guvenlik.degisiklikleri_yaz("olay", mevcut["id"], mevcut, alanlar, kid)
        set_ifade = ", ".join(f"{a}=?" for a in alanlar)
        db.yaz(f"UPDATE olay SET {set_ifade}, zaman=?, kullanici_id=? WHERE id=?",
               (*alanlar.values(), zaman, kid, mevcut["id"]))
        return mevcut["id"]
    kolonlar = ", ".join(alanlar)
    isaret = ", ".join("?" * len(alanlar))
    return db.yaz(
        f"INSERT INTO olay (lab_id, specimen_id, cycle_id, tip, gun, zaman, "
        f"kullanici_id, {kolonlar}) VALUES (?,?,?,?,?,?,?,{isaret})",
        (db.LAB_ID, specimen_id, cycle_id, tip, gun, zaman, kid, *alanlar.values()),
    )


def cleavage_skor(hucre, simetri, frag, gun):
    """Hücre sayısı, simetri ve fragmentasyondan A/B/C skoru türetir.

    Basit ve açık bir kural: her boyut ayrı puanlanır, en kötüsü skoru belirler.
    Lab kendi kuralını benimserse burası değiştirilir.
    """
    if hucre is None or not simetri or frag is None:
        return None
    beklenen = {2: (2, 4), 3: (6, 8)}.get(gun, (6, 8))
    if beklenen[0] <= hucre <= beklenen[1]:
        h = "A"
    elif abs(hucre - beklenen[0]) <= 1 or abs(hucre - beklenen[1]) <= 1:
        h = "B"
    else:
        h = "C"
    sm = {"esit": "A", "hafif_esitsiz": "B", "esitsiz": "C"}.get(simetri, "C")
    f = "A" if frag < 10 else ("B" if frag <= 25 else "C")
    return max(h, sm, f)          # harf sıralamasında en kötü olan


@uygulama.get("/cycle/{cycle_id}/cleavage")
def cleavage_ekran(request: Request, cycle_id: int, gun: int = 3, oosit: str = "",
                   duzenle: int = 0, hata: str = ""):
    if gun not in (2, 3):
        gun = 3
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    oositler = cleavage_durum(cycle_id, gun, c["cycle_tipi"])
    ortak = {
        "c": c, "gun": gun, "oositler": oositler,
        "gezinme": asama_gezinme(cycle_id, "cleavage"),
        "bekleyen": bekleyen_ozet(),
        "duzenle": duzenle,
        "simetriler": db.liste("simetri"),
        "bulgular": db.liste("bulgu_cleavage"),
        # Elle skor artık serbest metin değil, kapalı bir seçim (v6.122,
        # kullanıcının isteği: "G1,G2,G3,G4 şeklinde seçilebilsin") --
        # simetri'nin aynı `liste_degeri` deseni, goc_041.
        "skorlar": db.liste("cleavage_skor"),
        # Birleşme seçeneği (v6.157) göç (goc_048) varken basılıyor.
        "birlesme_var": db.kolon_var("olay", "cl_birlesme"),
        "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
        "hedef_saat": db.ayar("gun3_kontrol_saat", "68") if gun == 3 else None,
    }
    if not oositler:
        return sablon.TemplateResponse(
            request, "cleavage.html",
            {**ortak, "sp": None, "kayit": None, "secili_bulgular": set(), "kareler": []})

    sp = _secili_ornek(oositler, oosit)     # v6.35 -- bkz. ICSI ekranı

    kayit = _gun_olay(sp["id"], "cleavage_degerlendirme", gun)
    secili = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
        (sp["id"], f"gun{gun}"))}
    return sablon.TemplateResponse(
        request, "cleavage.html",
        {**ortak, "sp": sp, "kayit": kayit, "secili_bulgular": secili,
         "kareler": asama_goruntuleri(sp["id"], f"gun{gun}"),
         "hata": _asama_hatasi(hata, sp, cycle_id)})



def _dejenere_mi(specimen_id) -> bool:
    """Bu örnek ICSI ya da fertilizasyonda dejenere işaretlendi mi? (v6.139)

    `_DEJENERE`'nin tek örneklik hali -- POST tarafındaki engel için.
    Aynı SQL'i ikinci kez yazmamak için `s.id` yerine parametre koyuyoruz.
    """
    return bool(db.tek(
        "SELECT 1 x FROM specimen s WHERE s.id = ? AND (" + _DEJENERE + ")",
        (specimen_id,)))


def _dejenere_engel(specimen_id, gun, tip) -> bool:
    """Dejenere örneğe YENİ bir değerlendirme açılıyor mu?

    **Var olan kaydın düzenlenmesi engellenmiyor**: yanlışlıkla girilmiş ya da
    dejenere işaretinden ÖNCE girilmiş bir kaydı düzeltmek/silmek mümkün
    kalmalı, yoksa kullanıcı kendi verisine kilitlenir (v6.105'in "daha önce
    girilmiş bir kayıt varsa normal akış bozulmaz" kuralının aynısı).
    """
    if not _dejenere_mi(specimen_id):
        return False
    return not db.tek(
        "SELECT 1 x FROM olay WHERE specimen_id=? AND tip=? AND gun=? AND iptal_mi=0",
        (specimen_id, tip, gun))


@uygulama.post("/cycle/{cycle_id}/cleavage")
async def cleavage_kaydet(request: Request, cycle_id: int):
    f = await request.form()
    gun = int(f.get("gun") or 3)
    specimen_id = f.get("specimen_id")
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse(f"/cycle/{cycle_id}/cleavage?gun={gun}", status_code=303)
    c = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle_id,))
    tip = c["cycle_tipi"] if c else None
    burasi = f"/cycle/{cycle_id}/cleavage?gun={gun}&oosit={sp['id']}"

    # Dejenere yumurtaya embriyo kaydı yazılamaz (v6.139) -- ekran zaten
    # formu basmıyor, bu sunucu tarafındaki asıl engel.
    if _dejenere_engel(sp["id"], gun, "cleavage_degerlendirme"):
        return RedirectResponse(burasi, status_code=303)

    kid = request.state.kullanici["id"]
    # Birleşme (v6.157, kullanıcının isteği): hücre sayısı sayılamıyor, ekran
    # kutuyu gizliyor; gizli kutuda kalmış bir değer de yazılmıyor. Göç
    # (goc_048) yoksa kutu ekranda yok, alan hiç yazılmıyor (tuzak #3).
    birlesme_var = db.kolon_var("olay", "cl_birlesme")
    birlesme = birlesme_var and f.get("cl_birlesme") == "1"
    try:
        hucre = None if birlesme else tam(f.get("cl_hucre_sayisi"), "Hücre sayısı")
        frag = sayi(f.get("cl_fragmentasyon"), "Fragmentasyon")
    except FormHatasi:
        return RedirectResponse(burasi, status_code=303)
    # Birleşmede simetri de yok (v6.158): ekran gizliyor, gizli kutuda
    # seçili kalmış bir değer de yazılmıyor.
    simetri = None if birlesme else (f.get("cl_simetri") or None)
    if hucre is None and not simetri and frag is None and not birlesme:
        return RedirectResponse(burasi, status_code=303)

    elle_skor = (f.get("cl_skor") or "").strip().upper() or None
    otomatik = cleavage_skor(hucre, simetri, frag, gun)
    skor = elle_skor or otomatik
    kaynak = "elle" if elle_skor else ("otomatik" if otomatik else None)

    simdi = islem_zamani(f.get("islem_zamani"))
    if _cozmeden_once(specimen_id, cycle_id, tip, simdi):
        return RedirectResponse(burasi + "&duzenle=1&hata=cozmeden_once",
                                status_code=303)
    # olay.cycle_id örneğin KENDİ tedavisi (v6.62; Yumurta Çözme'de, v6.147,
    # rotanınki değil).
    alanlar = {"cl_hucre_sayisi": hucre, "cl_simetri": simetri,
               "cl_fragmentasyon": frag, "cl_skor": skor,
               "cl_skor_kaynagi": kaynak}
    if birlesme_var:
        alanlar["cl_birlesme"] = 1 if birlesme else None
    _gun_olay_kaydet(specimen_id, sp["cycle_id"], "cleavage_degerlendirme", gun,
                     alanlar, kid, simdi)

    asama = f"gun{gun}"
    yeni_b = set(f.getlist("bulgu"))
    eski_b = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
        (specimen_id, asama))}
    if yeni_b != eski_b:
        guvenlik.degisiklikleri_yaz("specimen_bulgu", specimen_id,
            {f"{asama}_bulgu": ", ".join(sorted(eski_b))},
            {f"{asama}_bulgu": ", ".join(sorted(yeni_b))}, kid)
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
               (specimen_id, asama))
        for b in sorted(yeni_b):
            db.yaz("INSERT INTO specimen_bulgu (specimen_id, asama, bulgu_kodu, "
                   "zaman, kullanici_id) VALUES (?,?,?,?,?)",
                   (specimen_id, asama, b, simdi, kid))

    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (f"gun{gun}", specimen_id))

    # Sıradaki: listenin sırasıyla (v6.147). v6.147'ye kadar sorgu bütün
    # örneklere bakıyordu, enjekte edilmemiş (listede olmayan) bir yumurtaya
    # da atlayabiliyordu; liste yalnızca ekranda görünenleri taşıyor.
    sonraki = _sonraki_ornek(cleavage_durum(cycle_id, gun, tip), specimen_id,
                             lambda o: not o["kayit_id"] and not o["dejenere"])
    hedef = f"/cycle/{cycle_id}/cleavage?gun={gun}"
    if sonraki:
        hedef += f"&oosit={sonraki['id']}"
    return RedirectResponse(hedef, status_code=303)


@uygulama.get("/specimen/{specimen_id}/cleavage-sil")
def cleavage_sil_ekran(request: Request, specimen_id: str, gun: int = 3,
                       cycle: int = 0):
    sp = db.tek("SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
                "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
                "WHERE s.id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    kayit = _gun_olay(specimen_id, "cleavage_degerlendirme", gun)
    bulgular = [etiketler.get(r["bulgu_kodu"], r["bulgu_kodu"]) for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
        (specimen_id, f"gun{gun}"))]
    return sablon.TemplateResponse(
        request, "cleavage_sil.html",
        {"sp": sp, "gun": gun, "kayit": kayit, "bulgular": bulgular,
         "etiketler": etiketler,
         # Yumurta Çözme'de (v6.147) ekran çözüldüğü tedaviden açılıyor.
         "hedef_cycle": _hedef_tedavi(sp, cycle)})


@uygulama.post("/specimen/{specimen_id}/cleavage-sil")
async def cleavage_sil(request: Request, specimen_id: str):
    f = dict(await request.form())
    gun = int(f.get("gun") or 3)
    sp = db.tek("SELECT * FROM specimen WHERE id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    try:
        hedef_cycle = _hedef_tedavi(sp, int(f.get("cycle") or 0))
    except ValueError:
        hedef_cycle = sp["cycle_id"]
    from datetime import datetime as _d
    simdi = _d.now().isoformat(" ", "seconds")
    kid = request.state.kullanici["id"]

    k = _gun_olay(specimen_id, "cleavage_degerlendirme", gun)
    if k:
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep=? WHERE id=?",
               (kid, simdi, f"Gun {gun} kaydi temizlendi", k["id"]))
    asama = f"gun{gun}"
    eski = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
        (specimen_id, asama))}
    if eski:
        guvenlik.degisiklikleri_yaz("specimen_bulgu", specimen_id,
            {f"{asama}_bulgu": ", ".join(sorted(eski))}, {f"{asama}_bulgu": ""}, kid)
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? AND asama=?",
               (specimen_id, asama))
    return RedirectResponse(
        f"/cycle/{hedef_cycle}/cleavage?gun={gun}&oosit={sp['id']}",
        status_code=303)


# ----------------------------------------------------------------- blastokist

BLAST_GUNLERI = (4, 5, 6, 7)
BLAST_DISI = ("erken_morula", "morula", "kavitasyon", "arrest")
BLAST_DERECELI = ("erken_morula", "morula", "kavitasyon")   # arrest derecelendirilmez
BLAST_KISA = {"erken_morula": "EM", "morula": "M",
              "kavitasyon": "KAV", "arrest": "ARR"}


def blast_durum(cycle_id: int, gun: int, cycle_tipi=None):
    """Blast ekranının embriyoları. fet_kultur'da (v6.62) ve Yumurta Çözme'de
    (v6.147) embriyo ÖNCEKİ bir tedaviden gelir (`specimen.cycle_id` hiç
    değişmez); aranan "hangi örnekler BU tedavi için çözüldü" --
    `db.tedavi_ornekleri()`, `/cycle/{id}/thaw` ekranının aynı mantığı."""
    kosul = db.tedavi_ornekleri(cycle_tipi)
    return db.sorgu(
        "SELECT s.id, s.cycle_id, s.cycle_sira_no, s.durum, s.taraf, "
        "  COALESCE( "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "     AND g.asama = ? ORDER BY g.id LIMIT 1), "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id = s.id "
        "     AND g.asama = 'blastokist' ORDER BY g.id LIMIT 1)) AS goruntu, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id = s.id "
        "   AND g.asama IN (?, 'blastokist')) AS kare, "
        "  (SELECT o.fert_pn_sayisi FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS pn, "
        "  (SELECT o.bl_skor FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='blastokist_degerlendirme' AND o.gun = ? AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS skor, "
        "  (SELECT o.bl_genisleme FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='blastokist_degerlendirme' AND o.gun = ? AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS gen, "
        "  (SELECT o.id FROM olay o WHERE o.specimen_id = s.id "
        "   AND o.tip='blastokist_degerlendirme' AND o.gun = ? AND o.iptal_mi=0 "
        "   ORDER BY o.id DESC LIMIT 1) AS kayit_id, "
        f"  CASE WHEN {_DEJENERE} THEN 1 ELSE 0 END AS dejenere "
        f"FROM specimen s WHERE {kosul} AND NOT ({_ICSI_YAPILMADI}) "
        "ORDER BY s.cycle_id, s.cycle_sira_no",
        (f"gun{gun}", f"gun{gun}", gun, gun, gun, cycle_id),
    )


def blast_skor(genisleme, icm, te, derece=None):
    """Blastokistte genişleme+ICM+TE ('4AA'); dışında kısaltma+derece ('M2')."""
    if not genisleme:
        return None
    if genisleme in BLAST_DISI:
        kisa = BLAST_KISA[genisleme]
        return f"{kisa}{derece}" if derece else kisa
    if not icm or not te:
        return genisleme
    return f"{genisleme}{icm.upper()}{te.upper()}"


@uygulama.get("/cycle/{cycle_id}/blast")
def blast_ekran(request: Request, cycle_id: int, gun: int = 5, oosit: str = "",
                duzenle: int = 0, hata: str = ""):
    if gun not in BLAST_GUNLERI:
        gun = 5
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    oositler = blast_durum(cycle_id, gun, c["cycle_tipi"])

    dereceler = db.liste("bl_derece")
    if not dereceler:                       # göç çalıştırılmamış olabilir
        dereceler = [{"kod": k, "etiket": e} for k, e in
                     (("1", "Derece 1"), ("2", "Derece 2"), ("3", "Derece 3"))]
    kolonlar = [r["name"] for r in db.sorgu("PRAGMA table_info(olay)")]
    eksik_goc = "bl_derece" not in kolonlar

    genislemeler = db.liste("bl_genisleme")
    if not any(g["kod"] == "kavitasyon" for g in genislemeler):
        eksik_goc = True

    ortak = {
        "c": c, "gun": gun, "gunler": BLAST_GUNLERI, "oositler": oositler,
        "gezinme": asama_gezinme(cycle_id, "blast"),
        "bekleyen": bekleyen_ozet(),
        "genislemeler": genislemeler,
        "duzenle": duzenle,
        "icmler": db.liste("bl_icm"),
        "teler": db.liste("bl_te"),
        "dereceler": dereceler,
        "eksik_goc": eksik_goc,
        "blast_disi": BLAST_DISI,
        "blast_dereceli": BLAST_DERECELI,
        "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
    }
    if not oositler:
        return sablon.TemplateResponse(
            request, "blast.html", {**ortak, "sp": None, "kayit": None, "kareler": []})

    # Seçim specimen.id ile -- cycle_sira_no ile DEĞİL (v6.62). Ötekilerde
    # (ICSI/fert/cleavage) o alan tek cycle içinde tekil, ama fet_kultur'da
    # birden çok cycle'ın embriyoları aynı listede olabiliyor; cycle_sira_no
    # yalnız KENDİ cycle'ı içinde tekil (UNIQUE(cycle_id, cycle_sira_no)) --
    # iki cycle'da da "1." embriyo olabilir, o alanla eşleşmek yanlış
    # embriyoyu seçebilirdi (bu işin en pahalı hatası).
    sp = _secili_ornek(oositler, oosit)     # v6.35 -- bkz. ICSI ekranı

    kayit = _gun_olay(sp["id"], "blastokist_degerlendirme", gun)
    return sablon.TemplateResponse(
        request, "blast.html",
        {**ortak, "sp": sp, "kayit": kayit,
         "kareler": asama_goruntuleri(sp["id"], f"gun{gun}"),
         "hata": _asama_hatasi(hata, sp, cycle_id)})


@uygulama.post("/cycle/{cycle_id}/blast")
async def blast_kaydet(request: Request, cycle_id: int):
    f = await request.form()
    gun = int(f.get("gun") or 5)
    if gun not in BLAST_GUNLERI:
        gun = 5
    specimen_id = f.get("specimen_id")
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse(f"/cycle/{cycle_id}/blast?gun={gun}", status_code=303)
    c = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle_id,))

    # Dejenere yumurtaya embriyo kaydı yazılamaz (v6.139), cleavage ile aynı.
    if _dejenere_engel(sp["id"], gun, "blastokist_degerlendirme"):
        return RedirectResponse(
            f"/cycle/{cycle_id}/blast?gun={gun}&oosit={sp['id']}", status_code=303)

    genisleme = f.get("bl_genisleme") or None
    if not genisleme:
        return RedirectResponse(
            f"/cycle/{cycle_id}/blast?gun={gun}&oosit={sp['id']}",
            status_code=303)

    icm = f.get("bl_icm") or None
    te = f.get("bl_te") or None
    derece = f.get("bl_derece") or None
    if genisleme in BLAST_DISI:
        icm = te = None             # morula/kavitasyon/arrest'te ICM ve TE tanımsız
    else:
        derece = None               # blastokistte derece yerine ICM/TE kullanılır
    if genisleme not in BLAST_DERECELI:
        derece = None               # arrest derecelendirilmez

    elle = (f.get("bl_skor") or "").strip().upper() or None
    otomatik = blast_skor(genisleme, icm, te, derece)
    skor = elle or otomatik
    kaynak = "elle" if elle else ("otomatik" if otomatik else None)

    kid = request.state.kullanici["id"]
    simdi = islem_zamani(f.get("islem_zamani"))
    if _cozmeden_once(specimen_id, cycle_id, c["cycle_tipi"] if c else None, simdi):
        return RedirectResponse(
            f"/cycle/{cycle_id}/blast?gun={gun}&oosit={sp['id']}&duzenle=1"
            "&hata=cozmeden_once", status_code=303)
    # olay.cycle_id specimen'in KENDİ cycle'ı (route'un cycle_id'si değil) --
    # thaw ve transfer olaylarının da yaptığı gibi (v6.62): fet_kultur'da bu
    # ekranın cycle'ı ile specimen'in cycle'ı farklı, "hangi tedavi için"
    # sorusunu zaten thaw_cycle_id yanıtlıyor.
    _gun_olay_kaydet(specimen_id, sp["cycle_id"], "blastokist_degerlendirme", gun,
                     {"bl_genisleme": genisleme, "bl_icm": icm, "bl_te": te,
                      "bl_derece": derece, "bl_skor": skor,
                      "bl_skor_kaynagi": kaynak}, kid, simdi)

    if genisleme == "arrest":
        durum = "arrest"
    elif genisleme == "kavitasyon":
        durum = "kavitasyon"
    elif genisleme in ("morula", "erken_morula"):
        durum = "morula"
    else:
        durum = "blastokist"
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (durum, specimen_id))

    # "Kaydet -> sıradaki" burada blast_durum()'un DÖNDÜRDÜĞÜ sırayı izliyor
    # (v6.62) -- cycle_sira_no üzerinden karşılaştırma DEĞİL: fet_kultur'da
    # o alan yalnız kendi cycle'ı içinde tekil, iki cycle'da da "1." embriyo
    # olabilir ve ham karşılaştırma yanlış sırayı/embriyoyu bulabilirdi.
    sonraki = _sonraki_ornek(
        blast_durum(cycle_id, gun, c["cycle_tipi"] if c else None), specimen_id,
        lambda o: not o["kayit_id"])
    hedef = f"/cycle/{cycle_id}/blast?gun={gun}"
    if sonraki:
        hedef += f"&oosit={sonraki['id']}"
    return RedirectResponse(hedef, status_code=303)


@uygulama.get("/specimen/{specimen_id}/blast-sil")
def blast_sil_ekran(request: Request, specimen_id: str, gun: int = 5, cycle: int = 0):
    sp = db.tek("SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
                "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
                "WHERE s.id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    # fet_kultur'da bu ekran embriyonun KENDİ cycle'ından değil, çözüldüğü
    # fet_kultur cycle'ından açılıyor olabilir (specimen.cycle_id hiç
    # değişmez) -- iki yerden gelinen ekranın geri oku sabit olamaz kuralı
    # (taşıyıcı ekranındaki `?cycle=` desenin aynısı, v6.62). Adres bir şey
    # söylemiyorsa specimen'in kendi cycle'ına dönülür (ivf_icsi'de zaten
    # aynı cycle).
    hedef_cycle = cycle or sp["cycle_id"]
    return sablon.TemplateResponse(
        request, "blast_sil.html",
        {"sp": sp, "gun": gun, "hedef_cycle": hedef_cycle,
         "kayit": _gun_olay(specimen_id, "blastokist_degerlendirme", gun),
         "etiketler": etiketler})


@uygulama.post("/specimen/{specimen_id}/blast-sil")
async def blast_sil(request: Request, specimen_id: str):
    f = dict(await request.form())
    gun = int(f.get("gun") or 5)
    sp = db.tek("SELECT * FROM specimen WHERE id = ?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    try:
        hedef_cycle = int(f.get("cycle") or 0) or sp["cycle_id"]
    except ValueError:
        hedef_cycle = sp["cycle_id"]
    from datetime import datetime as _d
    k = _gun_olay(specimen_id, "blastokist_degerlendirme", gun)
    if k:
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep=? WHERE id=?",
               (request.state.kullanici["id"],
                _d.now().isoformat(" ", "seconds"),
                f"Gun {gun} blastokist kaydi temizlendi", k["id"]))
    return RedirectResponse(
        f"/cycle/{hedef_cycle}/blast?gun={gun}&oosit={sp['id']}",
        status_code=303)


# ----------------------------------------------------------------- kriyo

DONMUS_DURUMLAR = ("dondurulmus",)
BITMIS_DURUMLAR = ("transfer_edildi", "discard", "degenere", "kayip", "arrest")


def konum_semasi():
    return db.sorgu(
        "SELECT seviye_sirasi, seviye_adi, deger_tipi FROM konum_semasi "
        "WHERE lab_id = ? ORDER BY seviye_sirasi", (db.LAB_ID,))


def konum_bul_veya_olustur(seviyeler):
    """seviyeler: ['T2','K3','G5','12'] — boş olanlar atlanır."""
    temiz = [(s or "").strip() for s in seviyeler] + ["", "", "", ""]
    temiz = temiz[:4]
    if not any(temiz):
        return None
    tam_yol = " / ".join(x for x in temiz if x)
    mevcut = db.tek("SELECT * FROM konum WHERE lab_id=? AND tam_yol=?",
                    (db.LAB_ID, tam_yol))
    if mevcut:
        return mevcut["id"]
    return db.yaz(
        "INSERT INTO konum (lab_id, seviye1, seviye2, seviye3, seviye4, tam_yol, durum) "
        "VALUES (?,?,?,?,?,?,'dolu')",
        (db.LAB_ID, temiz[0] or None, temiz[1] or None, temiz[2] or None,
         temiz[3] or None, tam_yol))


def icerik_sql() -> str:
    """Taşıyıcının içinde ne olduğu: 'yumurta' ya da 'embriyo' -- alt sorgu,
    sütun adı `icerik` (v6.167; v6.133'ten beri `icerik_tipi` adıyla
    dondurmanın tedavisinin TİPİNİ veriyordu, soran her yer onu
    `yumurta_mi()`'ye soruyordu).

    Bir taşıyıcı tek bir tedavinin örneklerini taşıyor -- hem ekrandaki
    vitrifikasyon kaydı tek seferde tek cycle'dan seçim yapıyor hem de
    `aktar_access.py` tüp başına tek grup yazıyor -- o yüzden ilk satır yeter.
    Taşıyıcı dört sorguda da `t` diye adlandığı için metin olarak paylaşılıyor.

    **Ölçü içerik, tip değil** (`db.dondurulan_yumurta_sql()`): Access'ten
    aktarılan IVF/ICSI tedavisinde ICSI'ye alınmayan yumurtalar dondurulmuş
    olabiliyor -- tipe bakan ölçü o tüpe "4 embriyo" diyor ve çözerken FET
    öneriyordu. v6.147'nin kuralı (dondurmanın YAPILDIĞI tedavi: Yumurta
    Çözme'de çözülen yumurtadan gelişen embriyonun tüpü embriyo) içeriğin
    ölçüsünde zaten var. Fonksiyon, sabit değil: göç çalışmamış (ya da eski
    bir yedekten geri yüklenmiş) veritabanında `vit_cycle_id` yok, cevap her
    istekte soruluyor (tuzak #15).
    """
    return (f"(SELECT CASE {db.dondurulan_yumurta_sql('o9')} WHEN 1 "
            "THEN 'yumurta' ELSE 'embriyo' END FROM olay o9 "
            " WHERE o9.vit_tasiyici_id = t.id AND o9.tip = 'vitrifikasyon' "
            " AND o9.iptal_mi = 0 ORDER BY o9.id LIMIT 1) AS icerik")


def tasiyici_icerigi(tasiyici_id):
    return db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.durum, o.zaman, o.id AS olay_id, "
        "  c.id AS cycle_id, c.cycle_no, c.cycle_tipi, "
        # İçindeki yumurta mı embriyo mu (v6.167, `icerik_sql()`'in
        # gerekçesi): içerikten -- `cycle_tipi` örneğin kendi tedavisi, onun
        # tipi çözülen yumurtadan gelişen embriyoda Yumurta Dondurma der.
        f"  CASE {db.dondurulan_yumurta_sql('o')} WHEN 1 THEN 'yumurta' "
        "  ELSE 'embriyo' END AS icerik, "
        "  h.id AS hasta_id, h.dosya_no, h.ad_soyad, "
        # Skor, dondurmanın YAPILDIĞI tedavideki değerlendirme (v6.148,
        # `db.bu_tedavinin_skoru()`): örnek sonra bir FET'te yeniden
        # değerlendirildiyse bu tüpün içeriği o skorla görünmesin.
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        f"   AND {db.bu_tedavinin_skoru(db.vit_tedavisi('o'), 'b')} "
        "   ORDER BY b.gun DESC LIMIT 1) AS skor, "
        # Tüpe blastokist olarak mı konmuş (v6.156): dondurmanın tedavisinde
        # blastokist değerlendirmesi var -- skorla aynı kural. Skor boş
        # olabilir (kavitasyon evresi), o yüzden ayrı bir soru.
        "  EXISTS (SELECT 1 FROM olay bb WHERE bb.specimen_id=s.id "
        "   AND bb.tip='blastokist_degerlendirme' AND bb.iptal_mi=0 "
        f"   AND {db.bu_tedavinin_skoru(db.vit_tedavisi('o'), 'bb')}) "
        "  AS blastokist, o.vit_tasiyici_id AS tasiyici_id, "
        "  COALESCE( "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     AND g.asama='blastokist' ORDER BY g.id DESC LIMIT 1), "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     ORDER BY g.id DESC LIMIT 1)) AS goruntu, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id=s.id) "
        "  AS goruntu_idler, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id=s.id) AS kare, "
        # Örneğin EN SON dondurmasının tüpü (v6.143): bu tüpten çözülüp başka
        # bir tüpe yeniden dondurulduysa taşıyıcı sayfası onu gösterir --
        # geçmiş iki yönden izlenebilsin.
        "  (SELECT v2.vit_tasiyici_id FROM olay v2 WHERE v2.specimen_id=s.id "
        "   AND v2.tip='vitrifikasyon' AND v2.iptal_mi=0 "
        "   ORDER BY v2.id DESC LIMIT 1) AS son_tasiyici_id, "
        "  (SELECT t2.etiket FROM olay v2 JOIN tasiyici t2 ON t2.id=v2.vit_tasiyici_id "
        "   WHERE v2.specimen_id=s.id AND v2.tip='vitrifikasyon' AND v2.iptal_mi=0 "
        "   ORDER BY v2.id DESC LIMIT 1) AS son_tasiyici_etiket "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "JOIN cycle c ON c.id = s.cycle_id JOIN hasta h ON h.id = c.hasta_id "
        "WHERE o.tip='vitrifikasyon' AND o.iptal_mi=0 AND o.vit_tasiyici_id=? "
        "ORDER BY s.cycle_sira_no", (tasiyici_id,))


# Etiket aramasında hasta iki ayrı yoldan bulunuyor: embriyo taşıyıcısında
# vitrifikasyon olayı üzerinden (olay → specimen → cycle → hasta), sperm
# taşıyıcısında doğrudan `sperm_dondurma.hasta_id` üzerinden. İkisi de `t`yi
# dışarıdan okuyan bağıntılı alt sorgu; JOIN yazılsaydı çok örnekli bir
# taşıyıcı satırı çoğaltırdı. Alan adı iki dalda da aynı (`h8`), o yüzden
# tek bir `{alan}` yetiyor.
_ETIKET_HASTA = (
    "COALESCE("
    " (SELECT {alan} FROM olay o8 JOIN specimen s8 ON s8.id = o8.specimen_id "
    "  JOIN cycle c8 ON c8.id = s8.cycle_id JOIN hasta h8 ON h8.id = c8.hasta_id "
    "  WHERE o8.vit_tasiyici_id = t.id AND o8.tip = 'vitrifikasyon' "
    "  AND o8.iptal_mi = 0 LIMIT 1), "
    " (SELECT {alan} FROM sperm_dondurma sd8 JOIN hasta h8 ON h8.id = sd8.hasta_id "
    "  WHERE sd8.tasiyici_id = t.id AND sd8.iptal_mi = 0 LIMIT 1)) AS {ad} ")


def etiket_ara(ara: str) -> list:
    """Taşıyıcı etiketinden arama: tüpün üstünde yazan kod (v6.138).

    Etiket vitrifikasyon ekranında üretilip (`<tedavi no>-<SSDD>`) ya da elle
    yazılıp tüpün üstüne geçiyor. Personelin elinde tüp var, "bu ne, kimin,
    nerede" diye soruyor — `ornek_kodu_ara()`'nın (v6.35) taşıyıcı hali.
    Kullanıcının isteği (2026-09-22): "Vitrifikasyonda etiket kodu ile arama
    olsun. Ana sayfadaki aramada o da aranabilsin."

    **Taşıyıcının durumuna bakmaz.** `/cryo` haritası `durum='dolu'` süzüyor
    çünkü o bir **envanter** ekranı ("dolapta bugün ne var"); bu ise hedefli
    bir **arama** ("bu etiket kimin"). Boşaltılmış ya da başka bir tedavide
    kullanılmış bir tüpün etiketi arandığında "yok" demek yanlış olurdu —
    örnek kodu aramasının arşivlenmiş hastayı da bulmasıyla aynı gerekçe.

    **Embriyo ve sperm taşıyıcılarını birlikte kapsar.** Etiket lab genelinde
    benzersiz (`vit_kaydet()` mükerrerini reddediyor) ve elde tutulan tüpün
    hangi modüle ait olduğu aranırken bilinmiyor olabilir. Satırın gideceği
    yer (`yol`) kategoriye göre seçiliyor: sperm kaydı kendi detayına,
    embriyo/yumurta taşıyıcısı cryo haritasındaki taşıyıcı sayfasına.

    `tr_buyuk()` **uygulanmaz** — `etiket` büyük harfe sabitlenmiş bir alan
    değil, personelin yazdığı gibi duruyor (v6.116'nın kuralı: yalnızca
    `ad_soyad` karşılaştıran parametre büyütülür).
    """
    if not ara.strip():
        return []
    satirlar = db.sorgu(
        "SELECT t.id, t.etiket, t.tip, t.renk, t.durum, t.kategori, "
        "  t.vitrifikasyon_zamani, k.tam_yol, "
        "  (SELECT COUNT(*) FROM olay o WHERE o.vit_tasiyici_id = t.id "
        "   AND o.tip = 'vitrifikasyon' AND o.iptal_mi = 0) AS adet, "
        + icerik_sql() + ", "
        "  (SELECT sd.id FROM sperm_dondurma sd WHERE sd.tasiyici_id = t.id "
        "   AND sd.iptal_mi = 0 ORDER BY sd.id LIMIT 1) AS sperm_id, "
        + _ETIKET_HASTA.format(alan="h8.dosya_no", ad="dosya_no") + ", "
        + _ETIKET_HASTA.format(alan="h8.ad_soyad", ad="ad_soyad") +
        "FROM tasiyici t LEFT JOIN konum k ON k.id = t.konum_id "
        "WHERE t.lab_id = ? AND t.etiket LIKE ? "
        "ORDER BY t.etiket LIMIT 50",
        (db.LAB_ID, f"%{ara.strip()}%"))

    # sqlite3.Row'a alan eklenemiyor; satır sözlüğe çevrilip `yol` ekleniyor
    # (`cycle_listesi()`/`_vit_satiri()`'nin deseni). Şablon böylece
    # kategoriye göre adres kurmuyor, tek bir `t.yol` basıyor.
    sonuc = []
    for r in satirlar:
        d = dict(r)
        d["yol"] = (f"/sperm-dondurma/{d['sperm_id']}"
                    if d["kategori"] == "sperm" and d["sperm_id"]
                    else f"/cryo/tasiyici/{d['id']}")
        sonuc.append(d)
    return sonuc


# Vitrifikasyon ekranının listesi: bir önceki aşamada (gün 2/3 ya da
# blastokist) kaydı olan örnekler (v6.137, kullanıcının isteği: "bir önceki
# blastokist menüsünde kaydı yapılmamış embriyoyu gösterme"). Kaydı olmayan
# örnek -- döllenmemiş (0PN), zigotta kalmış, immatür -- dondurulacak bir
# embriyo değil; ekranda yalnızca gürültü yapıyordu (gerçek bir tedavide 9
# satırın 7'si böyleydi).
#
# **Cleavage de sayılıyor, yalnızca blastokist değil**: bu laboratuvar gün 3
# embriyosu da donduruyor (ağustos kaydı: "1 TÜPTE 3 ADET D3 EMBRİYOSU
# (4HG2-4HG2-3HG2)"). Yalnızca blastokist aransaydı gün 3'te dondurma
# programda tümden yapılamaz hale gelirdi.
#
# **Vitrifikasyon da sayılıyor**: zaten dondurulmuş bir örnek, değerlendirmesi
# ne olursa olsun listeden DÜŞMEMELİ -- ekranın üst kartı ("dondurulanlar")
# aynı listeden besleniyor, süzgeç var olan bir kaydı görünmez yapardı.
_DEGERLENDIRILMIS = (
    "EXISTS (SELECT 1 FROM olay o WHERE o.specimen_id = s.id "
    "        AND o.iptal_mi = 0 AND o.tip IN ('cleavage_degerlendirme', "
    "            'blastokist_degerlendirme', 'vitrifikasyon'))")


# FET'in vitrifikasyon ekranında listelenen embriyolar (v6.143, kullanıcının
# isteği: "Çözülen embriyo aynı FET tedavisinde yeniden dondurulabilsin").
# `specimen.cycle_id` onların KAYNAK tedavisi, hiç değişmiyor; "bu FET'e ait"
# sorusunu çözme kaydının `thaw_cycle_id`'si yanıtlıyor (`db.tedavi_ornekleri()`'nin
# ve `/cycle/{id}/thaw`'ın aynı mantığı). Liste:
#   * bu tedavi için çözülen ve dejenere çıkmayan -- kısmi hasarlı da
#     listede, çünkü laboratuvar onu transfere de uygun sayıyor
#     (`TRANSFERE_UYGUN`); karar embriyoloğun;
#   * transfer edilmemiş, **ya da** bu tedavide zaten yeniden dondurulmuş
#     (sonradan başka bir FET'te çözülüp transfer edilse bile bu tedavinin
#     "Dondurulmuş" kartından düşmesin -- v6.137'nin "var olan kayıt
#     görünmez olmasın" gerekçesi).
# İki `?`: ikisi de bu tedavinin kimliği. `vit_kaydet()` sunucu tarafında
# aynı koşulu kullanıyor -- ekranda gizlemek yetmez.
_FET_DONDURULABILIR = (
    "s.id IN (SELECT t.specimen_id FROM olay t WHERE t.tip='thaw' "
    "         AND t.iptal_mi=0 AND t.thaw_cycle_id=? "
    "         AND COALESCE(t.thaw_sagkalim, '') <> 'degenere') "
    "AND (NOT EXISTS (SELECT 1 FROM olay tr WHERE tr.specimen_id=s.id "
    "                 AND tr.tip='transfer' AND tr.iptal_mi=0) "
    "     OR EXISTS (SELECT 1 FROM olay v WHERE v.specimen_id=s.id "
    "                AND v.tip='vitrifikasyon' AND v.iptal_mi=0 "
    "                AND v.vit_cycle_id=?))")


def _degerlendirilmis_burada(cycle_id) -> str:
    """`_DEGERLENDIRILMIS`'in Yumurta Çözme hali (v6.147): dondurma kaydı BU
    tedavininki olmalı. Çözülen yumurtanın kaynağında (Yumurta Dondurma) bir
    vitrifikasyon kaydı zaten var; genel süzgeç onu görüp enjekte edilmiş ama
    hiç değerlendirilmemiş yumurtayı da listeye alırdı."""
    return ("EXISTS (SELECT 1 FROM olay o WHERE o.specimen_id = s.id "
            "AND o.iptal_mi = 0 AND (o.tip IN ('cleavage_degerlendirme', "
            "'blastokist_degerlendirme') OR (o.tip = 'vitrifikasyon' AND "
            f"{db.vit_tedavisi('o')} = {int(cycle_id)})))")


def _vit_adaylari(c) -> tuple:
    """Vitrifikasyon ekranında listelenen örnekler -- `(SQL koşulu, parametreler)`.

    Ekran ve kayıt (`vit_kaydet()`) aynı koşulu kullanıyor: ekranda gizlemek
    yetmez, eski bir sekmedeki form da reddedilmeli (v6.143).
    - Kendi örneği olan tipler: tedavinin örnekleri; ICSI aşaması varsa
      enjekte edilmemiş örnek hiç görünmüyor (v6.105), embriyo aşaması varsa
      hiç değerlendirilmemiş örnek de (v6.137). İkisi de `oosit_cryo`'da
      uygulanmıyor -- orada ICSI de cleavage/blastokist de yok, her yumurta
      elenir ve ekran bomboş kalırdı (`_ICSI_YAPILMADI`'nın belgesi).
    - FET tipleri: bu tedavi için çözülüp transfer edilmeyenler
      (`_FET_DONDURULABILIR`, v6.143). FET'te öteki iki süzgeç anlamsız:
      çözülen embriyo zaten bir kez dondurulmuştu, program öncesi aktarılan
      FET embriyolarının hiç değerlendirmesi yok (v6.130). **Yumurta
      Çözme'de ikisi de geçerli** (v6.147): çözülen yumurtaydı, dondurulan
      ise ICSI'den sonra gelişen embriyo -- `ivf_icsi`'nin kuralı, yalnızca
      dondurma kaydı bu tedavininki olmalı (`_degerlendirilmis_burada()`).
    Aşama soruları tip adıyla değil `TIP_ASAMALARI` ile soruluyor.
    """
    tip, cid = c["cycle_tipi"], c["id"]
    asamalar = TIP_ASAMALARI.get(tip, ())
    if fet_tipi_mi(tip):
        kosul, par = _FET_DONDURULABILIR, (cid, cid)
        if "icsi" in asamalar:
            kosul += (" AND NOT (" + _ICSI_YAPILMADI + ") AND ("
                      + _degerlendirilmis_burada(cid) + ")")
        return kosul, par
    kosul = "s.cycle_id=?"
    if "icsi" in asamalar:
        kosul += " AND NOT (" + _ICSI_YAPILMADI + ")"
    if "blast" in asamalar:
        kosul += " AND (" + _DEGERLENDIRILMIS + ")"
    return kosul, (cid,)


def _vit_satiri(e: dict) -> dict:
    """Vitrifikasyon listesinde bir satırın kalitesi ve günü.

    Blastokist skoru varsa o; yoksa gün 2/3 kaydından hücre sayısı + skor
    ("4HG2"; birleşmede "Birleşme G2", v6.157, `db.cleavage_yazimi()`). Kaydı hiç olmayan örnek zaten listeye girmiyor (v6.137), ama
    `oosit_cryo`'da süzgeç uygulanmadığı için orada ikisi de boş kalabilir --
    şablon o zaman "değerlendirilmemiş" basıyor, doğru olan da o.
    """
    if e.get("skor"):
        e["kalite"], e["kalite_gun"] = e["skor"], e.get("gun")
    elif e.get("cl_hucre") is not None:
        e["kalite"] = db.cleavage_yazimi(e["cl_hucre"], e.get("cl_skor"))
        e["kalite_gun"] = e.get("cl_gun")
    else:
        e["kalite"], e["kalite_gun"] = None, None
    return e


@uygulama.get("/cycle/{cycle_id}/vitrifikasyon")
def vit_ekran(request: Request, cycle_id: int, hata: str = "",
              ara: str = ""):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    fet = fet_tipi_mi(c["cycle_tipi"])
    # FET'te yeniden dondurma goc_046'yı istiyor (iki kolon); çalışmamışsa
    # ekran açılır ama liste boş ve üstte göç uyarısı (tuzak #3).
    goc_gerekli = fet and not db.yeniden_dondurma_var()
    # Listenin koşulu tek yerde, `vit_kaydet()` de aynısını soruyor.
    kosul, par = ("0", ()) if goc_gerekli else _vit_adaylari(c)
    # Satırın tüpü: BU tedavide yapılan dondurma (v6.143). Yeniden dondurulan
    # bir embriyonun ilk tüpü kaynak tedavinin ekranında, ikincisi FET'inkinde
    # görünür. `cycle_id` rotadan tamsayı geliyor, metne gömmek güvenli.
    bu_vit = f"AND {db.vit_tedavisi('o')} = {int(cycle_id)} "
    # Skor bu tedavinin değerlendirmesinden, yoksa en sonuncudan (v6.148,
    # `db.bu_tedavinin_skoru()`): kaynak tedavinin ekranı, embriyo sonra bir
    # FET'te yeniden değerlendirilince FET'in skorunu basmasın.
    bu_b = f"AND {db.bu_tedavinin_skoru(str(int(cycle_id)), 'b')} "
    bu_cl = f"AND {db.bu_tedavinin_skoru(str(int(cycle_id)), 'cl')} "
    embriyolar = db.sorgu(
        "SELECT s.id, s.cycle_id, s.cycle_sira_no, s.durum, s.taraf, "
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        f"   {bu_b}ORDER BY b.gun DESC LIMIT 1) AS skor, "
        "  (SELECT b.gun FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        f"   {bu_b}ORDER BY b.gun DESC LIMIT 1) AS gun, "
        # Gün 2/3'te dondurulan embriyonun blastokist skoru yok; kendi
        # cleavage kaydı gösterilsin diye (v6.137) -- yoksa listedeki her
        # gün 3 embriyosu "değerlendirilmemiş" yazardı, oysa kaydı var.
        f"  (SELECT {db.cl_hucre_ifadesi('cl')} FROM olay cl WHERE cl.specimen_id=s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        f"   {bu_cl}ORDER BY cl.gun DESC LIMIT 1) AS cl_hucre, "
        "  (SELECT cl.cl_skor FROM olay cl WHERE cl.specimen_id=s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        f"   {bu_cl}ORDER BY cl.gun DESC LIMIT 1) AS cl_skor, "
        "  (SELECT cl.gun FROM olay cl WHERE cl.specimen_id=s.id "
        "   AND cl.tip='cleavage_degerlendirme' AND cl.iptal_mi=0 "
        f"   {bu_cl}ORDER BY cl.gun DESC LIMIT 1) AS cl_gun, "
        "  (SELECT o.vit_tasiyici_id FROM olay o WHERE o.specimen_id=s.id "
        "   AND o.tip='vitrifikasyon' AND o.iptal_mi=0 " + bu_vit +
        "   ORDER BY o.id DESC LIMIT 1) AS tasiyici_id, "
        "  (SELECT t.etiket FROM olay o JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
        "   WHERE o.specimen_id=s.id AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
        + bu_vit + "ORDER BY o.id DESC LIMIT 1) AS tasiyici_etiket, "
        "  (SELECT k.tam_yol FROM olay o JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
        "   JOIN konum k ON k.id=t.konum_id WHERE o.specimen_id=s.id "
        "   AND o.tip='vitrifikasyon' AND o.iptal_mi=0 " + bu_vit +
        "   ORDER BY o.id DESC LIMIT 1) AS konum, "
        # FET'te liste birden çok kaynak tedaviden gelebilir ve `cycle_sira_no`
        # yalnızca kendi tedavisinde tekil (v6.62) -- satırda kaynağı da yaz.
        "  (SELECT kc.cycle_no FROM cycle kc WHERE kc.id=s.cycle_id) "
        "  AS kaynak_cycle_no, "
        "  COALESCE( "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     AND g.asama='blastokist' ORDER BY g.id DESC LIMIT 1), "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     ORDER BY g.id DESC LIMIT 1)) AS goruntu, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id=s.id) "
        "  AS goruntu_idler, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id=s.id) AS kare "
        f"FROM specimen s WHERE {kosul} ORDER BY s.cycle_id, s.cycle_sira_no",
        par)

    # Satırda gösterilecek kalite: blastokist skoru, yoksa cleavage'ın kendi
    # yazımı ("4HG2" -- laboratuvarın kendi notasyonu, v6.135'te resmî
    # formlarda da bu kullanılıyor). sqlite3.Row'a alan eklenemiyor, sözlüğe
    # çevriliyor (`cycle_listesi()`'nin deseni).
    embriyolar = [_vit_satiri(dict(e)) for e in embriyolar]

    return sablon.TemplateResponse(
        request, "vitrifikasyon.html",
        {"c": c, "embriyolar": embriyolar, "sema": konum_semasi(),
         "gezinme": asama_gezinme(cycle_id, "vitrifikasyon"),
         "tipler": db.liste("tasiyici_tipi"), "renkler": db.liste("tasiyici_renk"),
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"), "hata": hata,
         "fet": fet, "goc_gerekli": goc_gerekli,
         # Yumurta Çözme (v6.147): dondurulan, çözülen yumurtadan gelişen
         # embriyo -- FET'in "yeniden dondurma" metinleri ona uymuyor.
         "yumurtadan": db.cozulen_yumurta_islenir(c["cycle_tipi"]),
         # Etiket araması (v6.138, kullanıcının isteği): elde tutulan tüpün
         # etiketi bu ekranda da aranabiliyor. Bu cycle'la sınırlı DEĞİL --
         # aranan tüp çoğu zaman başka bir tedaviye ait, soru zaten "bu
         # etiket kimin". Aynı sorgu `/hastalar`'ın aramasını da besliyor.
         "ara": ara, "etiket_sonuc": etiket_ara(ara),
         "onerilen": f"{c['cycle_no']}-{_d.now().strftime('%H%M')}"})


@uygulama.post("/cycle/{cycle_id}/vitrifikasyon")
async def vit_kaydet(request: Request, cycle_id: int):
    from urllib.parse import quote
    f = await request.form()
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    def hata(m):
        return RedirectResponse(
            f"/cycle/{cycle_id}/vitrifikasyon?hata={quote(m)}", status_code=303)

    fet = fet_tipi_mi(c["cycle_tipi"])
    if fet and not db.yeniden_dondurma_var():
        return hata("Çözülen embriyonun yeniden dondurulması için veritabanı "
                    "güncellemesi (goc_046) henüz uygulanmamış. Programı "
                    "kapatıp yeniden aç.")

    secilen = f.getlist("embriyo")
    if not secilen:
        return hata("Hiç embriyo seçilmedi.")

    # Seçilenler ÖNCE doğrulanıyor, taşıyıcı SONRA açılıyor (v6.143): hiçbiri
    # uygun değilse -- eski bir sekmedeki form, bu arada transfer edilmiş bir
    # embriyo -- Cryo Haritası'nda içi boş bir "dolu" tüp kalmasın. Koşul
    # ekrandakinin aynısı (`_vit_adaylari()`); gizlemek yetmez.
    # Güncellenecek kayıt BU tedavide yapılan dondurma (v6.143): örnek bu
    # tedavide zaten dondurulduysa o kayıt güncellenir (başka tüpe taşıma,
    # eski davranış); başka bir tedavideki dondurması -- FET'te yeniden
    # dondurulan embriyonun ilk tüpü -- hiç ellenmez, yeni kayıt açılır.
    bu_vit = f"{db.vit_tedavisi('olay')} = ?"
    uygunlar = []
    kosul, par = _vit_adaylari(c)
    for sid in secilen:
        sp = db.tek("SELECT s.* FROM specimen s WHERE s.id=? AND (" + kosul + ")",
                    (sid, *par))
        # Çözülmüş bir tüpün dondurma kaydı TAŞINAMAZ (v6.143): eski bir
        # sekmedeki form, bu arada dondurulup çözülen bir örneği gönderirse
        # kayıt yeni tüpe taşınır, çözmenin tüpü içeriksiz kalırdı -- geçmiş
        # yeniden yazılırdı. Geri almadaki kuralın aynısı
        # (`_vit_geri_alma_engeli()`).
        if sp:
            mevcut = db.tek("SELECT specimen_id, vit_tasiyici_id FROM olay "
                            "WHERE specimen_id=? AND tip='vitrifikasyon' "
                            f"AND iptal_mi=0 AND {bu_vit} "
                            "ORDER BY id DESC LIMIT 1", (sid, cycle_id))
            if _vit_geri_alma_engeli(mevcut):
                sp = None
        if sp:
            uygunlar.append(sp)
    if not uygunlar:
        return hata("Seçilenlerin hiçbiri bu tedavide dondurulamıyor.")

    etiket = (f.get("etiket") or "").strip()
    if not etiket:
        return hata("Taşıyıcı etiketi boş bırakılamaz.")
    if db.tek("SELECT id FROM tasiyici WHERE lab_id=? AND etiket=?", (db.LAB_ID, etiket)):
        return hata(f"'{etiket}' etiketli bir taşıyıcı zaten var.")

    seviyeler = [f.get(f"seviye{i}") for i in (1, 2, 3, 4)]
    konum_id = konum_bul_veya_olustur(seviyeler)

    kid = request.state.kullanici["id"]
    simdi = islem_zamani(f.get("islem_zamani"))

    tid = db.yaz(
        "INSERT INTO tasiyici (lab_id, tip, etiket, renk, konum_id, "
        "vitrifikasyon_zamani, kullanici_id, durum) VALUES (?,?,?,?,?,?,?,'dolu')",
        (db.LAB_ID, f.get("tip") or "cryotop", etiket, f.get("renk") or None,
         konum_id, simdi, kid))
    if konum_id:
        db.yaz("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))

    # `olay.cycle_id` örneğin KENDİ tedavisi (CLAUDE.md), FET'in kimliği
    # `vit_cycle_id`'de.
    eski_tasiyicilar = set()
    for sp in uygunlar:
        sid = sp["id"]
        onceki = db.tek(
            "SELECT vit_tasiyici_id FROM olay WHERE specimen_id=? "
            f"AND tip='vitrifikasyon' AND iptal_mi=0 AND {bu_vit} "
            "ORDER BY id DESC LIMIT 1", (sid, cycle_id))
        if onceki and onceki["vit_tasiyici_id"] and onceki["vit_tasiyici_id"] != tid:
            eski_tasiyicilar.add(onceki["vit_tasiyici_id"])
        alanlar = {"vit_tasiyici_id": tid}
        if fet:
            alanlar["vit_cycle_id"] = cycle_id
        olay_kaydet_veya_guncelle(sid, sp["cycle_id"], "vitrifikasyon", alanlar,
                                  kid, simdi, ek_kosul=bu_vit,
                                  ek_deger=(cycle_id,))
        db.yaz("UPDATE specimen SET durum='dondurulmus' WHERE id=?", (sid,))

    # Boşalan eski taşıyıcıları ve konumlarını serbest bırak
    for et in eski_tasiyicilar:
        kalan = db.tek("SELECT COUNT(*) k FROM olay WHERE vit_tasiyici_id=? "
                       "AND tip='vitrifikasyon' AND iptal_mi=0", (et,))["k"]
        if kalan == 0:
            e = db.tek("SELECT konum_id FROM tasiyici WHERE id=?", (et,))
            db.yaz("UPDATE tasiyici SET durum='bosaltildi' WHERE id=?", (et,))
            if e and e["konum_id"]:
                db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (e["konum_id"],))

    return RedirectResponse(f"/cryo/tasiyici/{tid}", status_code=303)


@uygulama.get("/cryo")
def cryo_harita(request: Request, ara: str = ""):
    if ara.strip():
        tasiyicilar = db.sorgu(
            "SELECT DISTINCT t.id, t.etiket, t.tip, t.renk, t.durum, "
            "  k.tam_yol, t.vitrifikasyon_zamani, "
            "  (SELECT COUNT(*) FROM olay o WHERE o.vit_tasiyici_id=t.id "
            "   AND o.tip='vitrifikasyon' AND o.iptal_mi=0) AS adet, "
            + icerik_sql() +
            " FROM tasiyici t LEFT JOIN konum k ON k.id=t.konum_id "
            "LEFT JOIN olay o ON o.vit_tasiyici_id=t.id AND o.iptal_mi=0 "
            "LEFT JOIN specimen s ON s.id=o.specimen_id "
            "LEFT JOIN cycle c ON c.id=s.cycle_id "
            "LEFT JOIN hasta h ON h.id=c.hasta_id "
            "WHERE t.lab_id=? AND t.durum='dolu' AND t.kategori='embriyo' AND ("
            "  t.etiket LIKE ? OR k.tam_yol LIKE ? "
            "  OR CAST(h.dosya_no AS TEXT) LIKE ? OR h.ad_soyad LIKE ? "
            # Tüpün üstünde yazan örnek kodu (v6.35). Cryo haritasında aranan
            # şey çoğu zaman elde tutulan kodun kendisidir.
            "  OR (CAST(h.dosya_no AS TEXT) || '-' || s.id) LIKE ?) "
            "ORDER BY k.tam_yol, t.etiket",
            # `h.ad_soyad` her zaman büyük harfle kayıtlı (v6.115) -- arama
            # terimi Türkçe ı/ş/ğ/ö/ü/ç için `tr_buyuk()`'ten geçmeli
            # (v6.116), yoksa küçük harfle Türkçe isim aranınca sonuç çıkmaz.
            (db.LAB_ID, f"%{ara}%", f"%{ara}%", f"%{ara}%", f"%{tr_buyuk(ara)}%",
             f"%{ara}%"))
    else:
        tasiyicilar = db.sorgu(
            "SELECT t.id, t.etiket, t.tip, t.renk, t.durum, k.tam_yol, "
            "  t.vitrifikasyon_zamani, "
            "  (SELECT COUNT(*) FROM olay o WHERE o.vit_tasiyici_id=t.id "
            "   AND o.tip='vitrifikasyon' AND o.iptal_mi=0) AS adet, "
            + icerik_sql() +
            " FROM tasiyici t LEFT JOIN konum k ON k.id=t.konum_id "
            "WHERE t.lab_id=? AND t.durum='dolu' AND t.kategori='embriyo' "
            "ORDER BY k.tam_yol, t.etiket",
            (db.LAB_ID,))

    # Tank satırında embriyo ve yumurta AYRI sayılıyor: bir tankta ikisi de
    # olabilir, tek bir "n embriyo" ikisini de embriyo gösterirdi (v6.133).
    # Ölçü içerik (v6.167, `icerik_sql()`'in gerekçesi): v6.133'ten beri
    # örneğin kendi tedavisinin tipiydi.
    def tank_sayim(yumurta, ad):
        return (
            "  (SELECT COUNT(*) FROM olay o JOIN tasiyici t2 ON t2.id=o.vit_tasiyici_id "
            "   JOIN konum k2 ON k2.id=t2.konum_id "
            "   WHERE o.tip='vitrifikasyon' AND o.iptal_mi=0 AND t2.durum='dolu' "
            f"   AND k2.seviye1 = k.seviye1 AND {db.dondurulan_yumurta_sql('o')} = {yumurta}) "
            f"AS {ad} ")
    tanklar = db.sorgu(
        "SELECT k.seviye1 AS tank, COUNT(DISTINCT t.id) AS tasiyici, "
        + tank_sayim(0, "embriyo") + ", "
        + tank_sayim(1, "yumurta") + 
        "FROM konum k JOIN tasiyici t ON t.konum_id=k.id AND t.durum='dolu' "
        "  AND t.kategori='embriyo' "
        "WHERE k.lab_id=? AND k.seviye1 IS NOT NULL "
        "GROUP BY k.seviye1 ORDER BY k.seviye1", (db.LAB_ID,))

    # ----------------------------------------------------------- sperm dondurma
    #
    # Embriyo Dondurma ile aynı taşıyıcı/konum altyapısını paylaşıyor
    # (`tasiyici`, `konum`, `tasiyici_tipi`/`tasiyici_renk` liste_degeri) ama
    # `kategori='sperm'` ile işaretleniyor, kendi tablosu `sperm_dondurma`
    # (dondurma öncesi semen analizi -- çözme/kullanım takibi bilerek yok).
    # v6.85'ten beri bu ekranın **içinde**, ayrı bir sayfa değil (kullanıcının
    # isteği: "Cryo Harita başlığı altına toplansın, ikisinin modülü yan yana
    # olsun") -- arama kutusu tek, aynı `ara` her iki modülü de süzüyor.
    sperm_taban = (
        "SELECT sd.id, sd.dondurma_zamani, sd.hacim_ml, sd.sebep, "
        "  sd.konsantrasyon_milyon_ml, sd.total_motil_yuzde, "
        "  t.etiket, t.tip, t.renk, k.tam_yol, "
        "  h.id AS hasta_id, h.dosya_no, h.ad_soyad, "
        # Bu dondurma başka bir hastanın (eşin) tedavisinde kullanıldıysa
        # (v6.86, androloji ekranından bağlanıyor) burada da görünsün.
        "  uh.dosya_no AS kul_dosya_no, uh.ad_soyad AS kul_ad_soyad, "
        "  uc.cycle_no AS kul_cycle_no, uc.id AS kul_cycle_id "
        "FROM sperm_dondurma sd "
        "JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "LEFT JOIN konum k ON k.id = t.konum_id "
        "JOIN hasta h ON h.id = sd.hasta_id "
        "LEFT JOIN cycle uc ON uc.id = sd.kullanim_cycle_id "
        "LEFT JOIN hasta uh ON uh.id = uc.hasta_id "
        "WHERE sd.lab_id=? AND sd.iptal_mi=0")
    if ara.strip():
        # `h.ad_soyad` her zaman büyük harfle kayıtlı (v6.115) -- arama
        # terimi Türkçe ı/ş/ğ/ö/ü/ç için `tr_buyuk()`'ten geçmeli (v6.116).
        sperm_kayitlari = db.sorgu(
            sperm_taban + " AND (t.etiket LIKE ? OR k.tam_yol LIKE ? "
            "OR CAST(h.dosya_no AS TEXT) LIKE ? OR h.ad_soyad LIKE ?) "
            "ORDER BY k.tam_yol, t.etiket",
            (db.LAB_ID, f"%{ara}%", f"%{ara}%", f"%{ara}%", f"%{tr_buyuk(ara)}%"))
    else:
        sperm_kayitlari = db.sorgu(
            sperm_taban + " ORDER BY k.tam_yol, t.etiket", (db.LAB_ID,))

    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    return sablon.TemplateResponse(
        request, "cryo.html",
        {"tasiyicilar": tasiyicilar, "tanklar": tanklar, "ara": ara,
         "sperm_kayitlari": sperm_kayitlari,
         "etiketler": etiketler, "kullanici": request.state.kullanici})


@uygulama.get("/sperm-dondurma")
def sperm_dondurma_harita_eski(request: Request, ara: str = ""):
    # v6.85: ayrı ekran kaldırıldı, Sperm Dondurma artık /cryo'nun içinde
    # (yan yana iki modülden biri). Eski bağlantılar/yer imleri için yönlendirme.
    from urllib.parse import urlencode
    return RedirectResponse(
        "/cryo" + (f"?{urlencode({'ara': ara})}" if ara else ""), status_code=303)


def dosya_no_sahibi(dosya_no) -> dict | None:
    """Bu dosya numarası kimin? Tedavi ve sperm dondurma sayısıyla birlikte.

    **Dosya numarası bu programda tek eşleştirme anahtarı** (v6.125,
    kullanıcının isteği: "dondurma işlemi yapılan erkek hastanın dosya
    numarası giriliyor ... eşi ile birlikte tüp bebek için hasta kaydı
    varsa uyarı mesajı ver ... dosya numarasından eşle").

    Bunu yapabilmemizin sebebi şemadaki `UNIQUE (lab_id, dosya_no)`:
    **"aynı dosya no" ile "aynı `hasta` satırı" aynı şey.** Yani tüp bebek
    çiftinin kaydı ile o çiftteki erkeğin sperm dondurması aynı satıra
    bağlanıyor, `sperm_dondurma.hasta_id` üzerinden — ayrı bir eşleştirme
    tablosuna da, isim karşılaştırmasına da gerek yok. İsimle eşleştirme
    **bilerek yazılmadı**: "yanlış hasta bu işin en pahalı hatası"
    (CLAUDE.md) ve ad benzerliği o riski taşır; dosya numarası kesin.

    Dönen `None` "böyle bir dosya no yok" demek; sözlük dönerse içinde
    `cycle_sayisi` (tüp bebek tedavisi var mı) ve `sperm_sayisi` var.
    """
    if not str(dosya_no).strip().isdigit():
        return None
    r = db.tek(
        "SELECT h.id, h.dosya_no, h.ad_soyad, h.es_adi, h.durum, "
        "  (SELECT COUNT(*) FROM cycle WHERE hasta_id = h.id) AS cycle_sayisi, "
        "  (SELECT COUNT(*) FROM sperm_dondurma WHERE hasta_id = h.id "
        "     AND iptal_mi = 0) AS sperm_sayisi "
        "FROM hasta h WHERE h.lab_id = ? AND h.dosya_no = ?",
        (db.LAB_ID, int(str(dosya_no).strip())))
    return dict(r) if r else None


def es_dosya_no_var() -> bool:
    """`goc_045` çalıştırıldı mı (v6.139).

    Çalışmadıysa hasta kaydetmek/güncellemek **eskisi gibi** çalışır, yalnızca
    eşin dosya numarası alanı yok sayılır. `cycle_alanlari()`'nın (v6.33)
    aynı koruması: göçü çalıştırmamış bir makinede hasta açmayı tümden
    bozmak, alanın kendisinden çok daha pahalı olurdu (tuzak #3). Cevap
    `db.kolon_var()`'da saklanıyor (v6.145, tuzak #15).
    """
    return db.kolon_var("hasta", "es_dosya_no")


def sperm_tedaviye_bagla(sperm_dondurma_id: int, cycle_id: int) -> bool:
    """Dondurulmuş spermi bir tedaviye bağlar (v6.86; v6.139'da paylaşıldı).

    İki ekran çağırıyor: androloji (`/cycle/{id}/androloji/sperm-baglama`) ve
    hasta kartı (v6.139, kullanıcının isteği: "Hasta kartında tedaviye
    bağlama opsiyonu versin"). Sahiplik değişmiyor -- `sperm_dondurma.
    hasta_id` dondurmayı yaptıran erkekte kalır, yalnızca "hangi tedavi için
    kullanıldı" yazılır.

    Yalnızca **henüz bağlanmamış** bir kayıt bağlanır; zaten bağlıysa sessizce
    hiçbir şey yapmaz (False döner) -- iki ekrandan aynı anda basılırsa
    ikincisi birincinin bağını başka bir tedaviye çevirmesin.
    """
    c = db.tek("SELECT id FROM cycle WHERE id=? AND lab_id=?", (cycle_id, db.LAB_ID))
    sd = db.tek(
        "SELECT tasiyici_id FROM sperm_dondurma WHERE id=? AND lab_id=? "
        "AND iptal_mi=0 AND kullanim_cycle_id IS NULL",
        (sperm_dondurma_id, db.LAB_ID))
    if not (c and sd):
        return False
    db.yaz("UPDATE sperm_dondurma SET kullanim_cycle_id=? WHERE id=?",
           (cycle_id, sperm_dondurma_id))
    db.yaz("UPDATE tasiyici SET durum='kullanildi' WHERE id=?", (sd["tasiyici_id"],))
    return True


def sperm_baglanti_kaldir(sperm_dondurma_id: int) -> bool:
    """Bağlantıyı kaldırır; taşıyıcı `'dolu'`ya döner (v6.86)."""
    sd = db.tek(
        "SELECT tasiyici_id FROM sperm_dondurma WHERE id=? AND lab_id=? "
        "AND kullanim_cycle_id IS NOT NULL", (sperm_dondurma_id, db.LAB_ID))
    if not sd:
        return False
    db.yaz("UPDATE sperm_dondurma SET kullanim_cycle_id=NULL WHERE id=?",
           (sperm_dondurma_id,))
    db.yaz("UPDATE tasiyici SET durum='dolu' WHERE id=?", (sd["tasiyici_id"],))
    return True


def hastanin_sperm_kayitlari(hasta_id: int, yalnizca_bagsiz: bool = False) -> list:
    """Bir hastanın (= bir dosya numarasının) dondurulmuş sperm kayıtları.

    `dosya_no_sahibi()`'nin açıkladığı aynı gerekçeyle doğrudan
    `sperm_dondurma.hasta_id` üzerinden okunuyor. `yalnizca_bagsiz` henüz
    hiçbir tedaviye bağlanmamış (`kullanim_cycle_id IS NULL`) olanları
    süzüyor — androloji ekranındaki "bağlanmayı bekleyen kayıt var"
    uyarısı için; hasta kartı ise hepsini gösteriyor, bağlananın hangi
    tedavide kullanıldığını da yazarak.
    """
    ek = " AND sd.kullanim_cycle_id IS NULL" if yalnizca_bagsiz else ""
    return db.sorgu(
        "SELECT sd.id, sd.dondurma_zamani, sd.sebep, sd.kullanim_cycle_id, "
        "  t.etiket, t.durum AS tasiyici_durum, k.tam_yol, "
        "  uc.cycle_no AS kul_cycle_no, uh.dosya_no AS kul_dosya_no, "
        "  uh.ad_soyad AS kul_ad_soyad "
        "FROM sperm_dondurma sd JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "LEFT JOIN konum k ON k.id = t.konum_id "
        "LEFT JOIN cycle uc ON uc.id = sd.kullanim_cycle_id "
        "LEFT JOIN hasta uh ON uh.id = uc.hasta_id "
        f"WHERE sd.hasta_id = ? AND sd.lab_id = ? AND sd.iptal_mi = 0{ek} "
        "ORDER BY sd.dondurma_zamani DESC, sd.id DESC",
        (hasta_id, db.LAB_ID))


def _sperm_dondurma_olustur(hasta_id, f, kid):
    """Taşıyıcı + `sperm_dondurma` satırını birlikte yazar.

    Hem mevcut hastanın kendi "Yeni Sperm Dondurma"sında hem yeni-hasta
    (`/sperm-dondurma/yeni-hasta`) akışında kullanılıyor — iki kopya
    olsaydı biri güncellenip öteki unutulurdu. Doğrulama **yazmadan önce**
    bitiyor: yeni-hasta akışı hata durumunda az önce açtığı boş hasta
    kaydını geri alabilsin diye (CLAUDE.md "kayıt açıp doldurma" kuralı).
    """
    etiket = (f.get("etiket") or "").strip()
    if not etiket:
        raise FormHatasi("Taşıyıcı etiketi boş bırakılamaz.")
    if db.tek("SELECT id FROM tasiyici WHERE lab_id=? AND etiket=?", (db.LAB_ID, etiket)):
        raise FormHatasi(f"'{etiket}' etiketli bir taşıyıcı zaten var.")

    hacim = sayi(f.get("hacim_ml"), "Hacim")
    konsantrasyon = sayi(f.get("konsantrasyon"), "Konsantrasyon")
    motilite = sayi(f.get("total_motilite"), "Total motilite")

    seviyeler = [f.get(f"seviye{i}") for i in (1, 2, 3, 4)]
    konum_id = konum_bul_veya_olustur(seviyeler)
    simdi = islem_zamani(f.get("islem_zamani"))

    tid = db.yaz(
        "INSERT INTO tasiyici (lab_id, tip, etiket, renk, konum_id, "
        "vitrifikasyon_zamani, kullanici_id, durum, kategori) "
        "VALUES (?,?,?,?,?,?,?,'dolu','sperm')",
        (db.LAB_ID, f.get("tip") or "straw", etiket, f.get("renk") or None,
         konum_id, simdi, kid))
    if konum_id:
        db.yaz("UPDATE konum SET durum='dolu' WHERE id=?", (konum_id,))

    return db.yaz(
        "INSERT INTO sperm_dondurma (lab_id, hasta_id, tasiyici_id, "
        "dondurma_zamani, hacim_ml, konsantrasyon_milyon_ml, total_motil_yuzde, "
        "sebep, notlar, kullanici_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (db.LAB_ID, hasta_id, tid, simdi, hacim, konsantrasyon, motilite,
         bos_ise_none(f.get("sebep")), bos_ise_none(f.get("notlar")), kid))


@uygulama.get("/hasta/{hasta_id}/sperm-dondurma/yeni")
def sperm_dondurma_form(request: Request, hasta_id: int, hata: str = ""):
    h = db.tek("SELECT * FROM hasta WHERE id=?", (hasta_id,))
    if not h:
        return RedirectResponse("/hastalar", status_code=303)
    from datetime import datetime as _d
    return sablon.TemplateResponse(
        request, "sperm_dondurma_form.html",
        {"h": h, "sema": konum_semasi(),
         "tipler": db.liste("tasiyici_tipi"), "renkler": db.liste("tasiyici_renk"),
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"), "hata": hata,
         "onerilen": f"{h['dosya_no']}-SP-{_d.now().strftime('%H%M')}"})


@uygulama.post("/hasta/{hasta_id}/sperm-dondurma/yeni")
async def sperm_dondurma_kaydet(request: Request, hasta_id: int):
    from urllib.parse import quote
    f = await request.form()
    h = db.tek("SELECT * FROM hasta WHERE id=?", (hasta_id,))
    if not h:
        return RedirectResponse("/hastalar", status_code=303)

    kid = request.state.kullanici["id"]
    try:
        _sperm_dondurma_olustur(hasta_id, f, kid)
    except FormHatasi as e:
        return RedirectResponse(
            f"/hasta/{hasta_id}/sperm-dondurma/yeni?hata=" + quote(str(e)),
            status_code=303)

    return RedirectResponse("/cryo", status_code=303)


@uygulama.get("/sperm-dondurma/yeni-hasta")
def sperm_dondurma_yeni_hasta_form(request: Request, hata: str = ""):
    """Cryo Haritası > Sperm Dondurma'dan tek ekranda yeni erkek hasta +
    dondurma kaydı (v6.86). `hasta_form.html`'in eş alanları burada yok —
    bu hasta tüp bebek tedavisi görmüyor olabilir (örn. onkoloji öncesi).
    """
    from datetime import datetime as _d
    return sablon.TemplateResponse(
        request, "sperm_dondurma_yeni_hasta.html",
        {"v": {}, "hata": hata, "eslesen": None, "sema": konum_semasi(),
         "tipler": db.liste("tasiyici_tipi"), "renkler": db.liste("tasiyici_renk"),
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M")})


@uygulama.post("/sperm-dondurma/yeni-hasta")
async def sperm_dondurma_yeni_hasta_kaydet(request: Request):
    f = await request.form()

    def yeniden(m, eslesen=None):
        # Hata formu kapatmaz, yazılanlarla yeniden basılır (v6.21 kuralı) —
        # bu form uzun olduğu için (hasta + taşıyıcı + konum + semen analizi)
        # kaybı özellikle can sıkıcı olurdu.
        # `eslesen` doluysa şablon düz bir hata satırı yerine, o hastaya
        # gidecek bağlantıyı taşıyan bir uyarı kutusu basıyor (v6.125).
        return sablon.TemplateResponse(
            request, "sperm_dondurma_yeni_hasta.html",
            {"v": dict(f), "hata": m, "eslesen": eslesen, "sema": konum_semasi(),
             "tipler": db.liste("tasiyici_tipi"), "renkler": db.liste("tasiyici_renk"),
             "simdi": f.get("islem_zamani") or _dt.now().strftime("%Y-%m-%dT%H:%M")})

    dosya_no = (f.get("dosya_no") or "").strip()
    ad_soyad = (f.get("ad_soyad") or "").strip()
    if not dosya_no or not ad_soyad:
        return yeniden("Dosya no ve ad soyad boş bırakılamaz.")
    if not dosya_no.isdigit():
        return yeniden("Dosya no sayı olmalı.")
    # Dosya no zaten kayıtlıysa: eskiden düz bir metin dönüyordu, artık
    # hastayı adıyla tanıtan ve oraya götüren bir kutu (v6.125). Engel aynı
    # (`UNIQUE (lab_id, dosya_no)` zaten izin vermezdi) — değişen, çıkmaz
    # sokak yerine yolu göstermesi: çift zaten kayıtlıysa doğru davranış
    # yeni bir hasta açmak değil, o kayda sperm dondurma eklemek.
    eslesen = dosya_no_sahibi(dosya_no)
    if eslesen:
        return yeniden("", eslesen)

    try:
        dt = zaman(f.get("dogum_tarihi"), "Doğum tarihi")
    except FormHatasi as e:
        return yeniden(str(e))

    kid = request.state.kullanici["id"]
    hasta_id = db.yaz(
        "INSERT INTO hasta (lab_id, dosya_no, ad_soyad, telefon, dogum_tarihi) "
        "VALUES (?,?,?,?,?)",
        (db.LAB_ID, int(dosya_no), tr_buyuk(ad_soyad), bos_ise_none(f.get("telefon")), dt))

    try:
        sd_id = _sperm_dondurma_olustur(hasta_id, f, kid)
    except FormHatasi as e:
        # Dolduramadik: boş kalan hasta kaydı geri alınıyor (specimen'i
        # geri alan `bos_specimen_sil()` ile aynı gerekçe) — yoksa lab
        # boş, ıssız hasta dosyalarıyla dolar.
        db.yaz("DELETE FROM hasta WHERE id=?", (hasta_id,))
        return yeniden(str(e))

    return RedirectResponse(f"/sperm-dondurma/{sd_id}", status_code=303)


@uygulama.get("/sperm-dondurma/{sperm_dondurma_id}")
def sperm_dondurma_detay(request: Request, sperm_dondurma_id: int, hata: str = ""):
    sd = db.tek(
        "SELECT sd.*, t.etiket, t.tip, t.renk, t.durum AS tasiyici_durum, "
        "  k.tam_yol, h.id AS hasta_id, h.dosya_no, h.ad_soyad, "
        "  uh.dosya_no AS kul_dosya_no, uh.ad_soyad AS kul_ad_soyad, "
        "  uc.cycle_no AS kul_cycle_no "
        "FROM sperm_dondurma sd "
        "JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "LEFT JOIN konum k ON k.id = t.konum_id "
        "JOIN hasta h ON h.id = sd.hasta_id "
        "LEFT JOIN cycle uc ON uc.id = sd.kullanim_cycle_id "
        "LEFT JOIN hasta uh ON uh.id = uc.hasta_id "
        "WHERE sd.id=? AND sd.lab_id=?", (sperm_dondurma_id, db.LAB_ID))
    if not sd or sd["iptal_mi"]:
        return RedirectResponse("/cryo", status_code=303)
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    onamlar = [
        {**dict(r), "pdf_mi": (r["orijinal_dosya_adi"] or "").lower().endswith(".pdf")}
        for r in db.sorgu(
            "SELECT * FROM sperm_dondurma_dosya WHERE sperm_dondurma_id=? "
            "ORDER BY id", (sperm_dondurma_id,))
    ]
    onam_resim_ids = [o["id"] for o in onamlar if not o["pdf_mi"]]
    return sablon.TemplateResponse(
        request, "sperm_dondurma_detay.html",
        {"sd": sd, "etiketler": etiketler, "onamlar": onamlar,
         "onam_resim_ids": onam_resim_ids, "hata": hata})


@uygulama.post("/sperm-dondurma/{sperm_dondurma_id}/islem-yapan")
async def sperm_dondurma_islem_yapan_kaydet(request: Request, sperm_dondurma_id: int):
    """Sperm dondurmayı fiilen yapan kişi — aşama ekranlarındaki İşlemi
    Yapan kutusunun aynı deseni (v6.99), ama `islem_yapan` tablosu `cycle_id`
    istediği için sperm dondurmada doğrudan `sperm_dondurma.yapan_ad`'a yazılıyor.
    """
    f = dict(await request.form())
    yapan = bos_ise_none(f.get("yapan_ad"))
    sd = db.tek("SELECT id FROM sperm_dondurma WHERE id=? AND lab_id=?",
                (sperm_dondurma_id, db.LAB_ID))
    if sd:
        db.yaz("UPDATE sperm_dondurma SET yapan_ad=? WHERE id=?",
               (yapan, sperm_dondurma_id))
    return RedirectResponse(f"/sperm-dondurma/{sperm_dondurma_id}", status_code=303)


@uygulama.post("/sperm-dondurma/{sperm_dondurma_id}/onam-ekle")
async def sperm_dondurma_onam_ekle(request: Request, sperm_dondurma_id: int):
    """Onamlar: sperm dondurma kaydına PDF/fotoğraf eki (v6.101).

    `doktor_notu_ekle()` ile aynı desen, `goruntuler.sperm_onam_ekle()`
    çağırıyor — `goruntu` tablosuna değil, `sperm_dondurma_dosya`'ya yazıyor
    (sperm dondurmanın cycle'ı olmayabilir, `goruntu.cycle_id` NOT NULL).
    """
    from urllib.parse import quote
    sd = db.tek("SELECT hasta_id FROM sperm_dondurma WHERE id=? AND lab_id=?",
                (sperm_dondurma_id, db.LAB_ID))
    if not sd:
        return RedirectResponse("/cryo", status_code=303)

    form = await request.form()
    dosyalar = form.getlist("dosyalar")
    kid = request.state.kullanici["id"]

    hatalar = 0
    for d in dosyalar:
        ad = getattr(d, "filename", "") or ""
        if not ad:
            continue
        icerik = await d.read()
        mesaj = goruntuler.sperm_onam_ekle(
            icerik, ad, sd["hasta_id"], sperm_dondurma_id, kid)
        if mesaj:
            hatalar += 1

    if hatalar:
        return RedirectResponse(
            f"/sperm-dondurma/{sperm_dondurma_id}?hata="
            + quote("Bazı dosyalar eklenemedi (desteklenmeyen tür ya da boyut)."),
            status_code=303)
    return RedirectResponse(f"/sperm-dondurma/{sperm_dondurma_id}", status_code=303)


@uygulama.get("/sperm-onam/{dosya_id}")
def sperm_onam_dosya(dosya_id: int):
    d = db.tek("SELECT dosya_yolu FROM sperm_dondurma_dosya WHERE id = ?", (dosya_id,))
    if not d:
        return Response(status_code=404)
    p = goruntuler.tam_yol(d["dosya_yolu"])
    if not p.is_file():
        return Response(status_code=404)
    return FileResponse(p)


@uygulama.get("/sperm-onam/{dosya_id}/sil")
def sperm_onam_sil_ekran(request: Request, dosya_id: int):
    d = db.tek(
        "SELECT sd.*, h.dosya_no, h.ad_soyad "
        "FROM sperm_dondurma_dosya sd "
        "JOIN sperm_dondurma s ON s.id = sd.sperm_dondurma_id "
        "JOIN hasta h ON h.id = s.hasta_id "
        "WHERE sd.id=?", (dosya_id,))
    if not d:
        return RedirectResponse("/cryo", status_code=303)
    pdf_mi = (d["orijinal_dosya_adi"] or "").lower().endswith(".pdf")
    return sablon.TemplateResponse(
        request, "sperm_onam_sil.html", {"d": d, "pdf_mi": pdf_mi})


@uygulama.post("/sperm-onam/{dosya_id}/sil")
def sperm_onam_dosya_sil(request: Request, dosya_id: int):
    d = db.tek("SELECT sperm_dondurma_id FROM sperm_dondurma_dosya WHERE id=?",
               (dosya_id,))
    if not d:
        return RedirectResponse("/cryo", status_code=303)
    goruntuler.sperm_onam_sil(dosya_id)
    return RedirectResponse(f"/sperm-dondurma/{d['sperm_dondurma_id']}", status_code=303)


@uygulama.get("/sperm-dondurma/{sperm_dondurma_id}/sil")
def sperm_dondurma_sil_ekran(request: Request, sperm_dondurma_id: int):
    sd = db.tek(
        "SELECT sd.*, t.etiket, k.tam_yol, h.dosya_no, h.ad_soyad "
        "FROM sperm_dondurma sd JOIN tasiyici t ON t.id = sd.tasiyici_id "
        "LEFT JOIN konum k ON k.id = t.konum_id "
        "JOIN hasta h ON h.id = sd.hasta_id "
        "WHERE sd.id=? AND sd.lab_id=? AND sd.iptal_mi=0",
        (sperm_dondurma_id, db.LAB_ID))
    if not sd:
        return RedirectResponse("/cryo", status_code=303)
    return sablon.TemplateResponse(request, "sperm_dondurma_sil.html", {"sd": sd})


@uygulama.post("/sperm-dondurma/{sperm_dondurma_id}/sil")
def sperm_dondurma_sil(request: Request, sperm_dondurma_id: int):
    from datetime import datetime as _d
    sd = db.tek("SELECT * FROM sperm_dondurma WHERE id=? AND lab_id=?",
               (sperm_dondurma_id, db.LAB_ID))
    if not sd:
        return RedirectResponse("/cryo", status_code=303)
    kid = request.state.kullanici["id"]
    simdi = _d.now().isoformat(" ", "seconds")
    db.yaz("UPDATE sperm_dondurma SET iptal_mi=1, iptal_kullanici_id=?, "
           "iptal_zamani=?, iptal_sebep='Sperm dondurma kaydi silindi' WHERE id=?",
           (kid, simdi, sperm_dondurma_id))
    t = db.tek("SELECT konum_id FROM tasiyici WHERE id=?", (sd["tasiyici_id"],))
    db.yaz("UPDATE tasiyici SET durum='bosaltildi' WHERE id=?", (sd["tasiyici_id"],))
    if t and t["konum_id"]:
        db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))
    return RedirectResponse("/cryo", status_code=303)


@uygulama.get("/cryo/tasiyici/{tasiyici_id}")
def tasiyici_detay(request: Request, tasiyici_id: int, cycle: int = 0):
    """Taşıyıcının içeriği.

    `?cycle=N` çözme ekranından gelindiğini söyler; geri oku cryo haritasına
    değil o cycle'ın çözme ekranına döner (v6.32). Adresten gelen değer
    **sayı** ve var olan bir cycle'a bakılarak doğrulanıyor — `geri=<yol>`
    biçiminde serbest bir adres almıyoruz, `href`'e yazılacak.
    """
    t = db.tek("SELECT t.*, k.tam_yol FROM tasiyici t "
               "LEFT JOIN konum k ON k.id=t.konum_id WHERE t.id=?", (tasiyici_id,))
    if not t:
        return RedirectResponse("/cryo", status_code=303)
    gecerli = cycle and db.tek("SELECT 1 FROM cycle WHERE id=? AND lab_id=?",
                               (cycle, db.LAB_ID))
    geri = f"/cycle/{cycle}/thaw" if gecerli else "/cryo"
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    icerik = tasiyici_icerigi(tasiyici_id)
    # Çözme özeti: BU tüpten yapılan çözmeler (v6.143). Eski ölçü ("bu tüpte
    # dondurulmuş örneklerin herhangi bir çözmesi") yeniden dondurulan bir
    # embriyoda ikinci tüpe ilk tüpün çözmesini yazardı -- dolu bir tüp
    # "çözüldü" görünürdü. Göç yoksa eski ölçü.
    if db.cozme_tupu_var():
        thawlar = db.sorgu(
            "SELECT o.thaw_sagkalim, o.thaw_canlilik FROM olay o "
            "WHERE o.tip='thaw' AND o.iptal_mi=0 AND o.thaw_tasiyici_id=?",
            (tasiyici_id,))
    else:
        thawlar = db.sorgu(
            "SELECT o.thaw_sagkalim, o.thaw_canlilik FROM olay o "
            "JOIN specimen s ON s.id=o.specimen_id "
            "JOIN olay v ON v.specimen_id=s.id AND v.tip='vitrifikasyon' AND v.iptal_mi=0 "
            "WHERE o.tip='thaw' AND o.iptal_mi=0 AND v.vit_tasiyici_id=?", (tasiyici_id,))
    ozet = None
    if thawlar:
        canli = sum(1 for r in thawlar if r["thaw_sagkalim"] == "canli")
        oranlar = [r["thaw_canlilik"] for r in thawlar if r["thaw_canlilik"] is not None]
        ozet = {"toplam": len(thawlar), "canli": canli,
                "oran": round(100 * canli / len(thawlar)),
                "ortalama_canlilik": round(sum(oranlar) / len(oranlar), 1) if oranlar else None}
    return sablon.TemplateResponse(
        request, "tasiyici.html",
        {"t": t, "icerik": icerik, "etiketler": etiketler, "ozet": ozet,
         "geri": geri, "geri_cycle": cycle if gecerli else 0})


def _vit_kaydi(specimen_id, cycle: int = 0):
    """Geri alınacak dondurma kaydı (v6.143).

    Bir örneğin artık birden çok dondurması olabiliyor (FET'te yeniden
    dondurma). `cycle` verilirse O tedavide yapılan dondurma -- "Kaydı geri
    al" bağlantısı hangi ekrandan basıldıysa onun tedavisini taşıyor; yoksa
    en son dondurma (eski davranış, adressiz bağlantılar için).
    """
    kosul, par = "", (specimen_id,)
    if cycle:
        kosul, par = f"AND {db.vit_tedavisi('o')} = ? ", (specimen_id, cycle)
    return db.tek(
        "SELECT o.*, t.etiket, k.tam_yol FROM olay o "
        "LEFT JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
        "LEFT JOIN konum k ON k.id=t.konum_id "
        "WHERE o.specimen_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
        + kosul + "ORDER BY o.id DESC LIMIT 1", par)


def _vit_geri_alma_engeli(kayit):
    """Bu dondurma geri alınamıyorsa sebebinin metin anahtarı, alınabiliyorsa
    None (v6.143).

    **Önce en son adım geri alınır.** Tüp çözülmüşse dondurmayı silmek
    "hiç dondurulmadı" demek olurdu, ama çözme kaydı -- ve belki ondan sonra
    yapılan yeniden dondurma -- duruyor: geçmiş kendi içinde çelişirdi.
    Önce çözme geri alınmalı. Göç (goc_046) çalışmamışsa eski davranış:
    engel yok.
    """
    if not (kayit and kayit["vit_tasiyici_id"] and db.cozme_tupu_var()):
        return None
    cozme = db.tek("SELECT 1 FROM olay WHERE specimen_id=? AND tip='thaw' "
                   "AND iptal_mi=0 AND thaw_tasiyici_id=?",
                   (kayit["specimen_id"], kayit["vit_tasiyici_id"]))
    return "vit_geri_alma_cozulmus" if cozme else None


def _vit_yapildigi_tedavi(kayit, varsayilan):
    """Dondurmanın YAPILDIĞI tedavi: FET'te yeniden dondurmada o FET, yoksa
    örneğin kendi tedavisi (`db.vit_tedavisi()`'nin Python hali)."""
    if not kayit:
        return varsayilan
    if "vit_cycle_id" in kayit.keys() and kayit["vit_cycle_id"]:
        return kayit["vit_cycle_id"]
    return kayit["cycle_id"]


def _dondurma_oncesi_cozme(kayit):
    """Bu dondurmadan ÖNCE açılmış etkin çözme -- varsa bu bir yeniden
    dondurmadır ve geri alınınca örnek o çözülmüş hâline döner.

    Ölçü kimlik sırası, saat değil: saatler elle geri tarihlenebiliyor.
    "Kaynak tedaviden farklı bir FET mi" diye bakılmıyor, çünkü program
    öncesi aktarılan FET embriyolarının kendi tedavisi zaten o FET (v6.130).
    """
    if not kayit:
        return None
    return db.tek("SELECT thaw_sagkalim FROM olay WHERE specimen_id=? "
                  "AND tip='thaw' AND iptal_mi=0 AND id < ? "
                  "ORDER BY id DESC LIMIT 1", (kayit["specimen_id"], kayit["id"]))


@uygulama.get("/specimen/{specimen_id}/vit-sil")
def vit_sil_ekran(request: Request, specimen_id: str, cycle: int = 0):
    sp = db.tek("SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
                "JOIN cycle c ON c.id=s.cycle_id JOIN hasta h ON h.id=c.hasta_id "
                "WHERE s.id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    kayit = _vit_kaydi(specimen_id, cycle)
    kardes = 0
    if kayit and kayit["vit_tasiyici_id"]:
        kardes = db.tek("SELECT COUNT(*) k FROM olay WHERE vit_tasiyici_id=? "
                        "AND tip='vitrifikasyon' AND iptal_mi=0",
                        (kayit["vit_tasiyici_id"],))["k"]
    # Geri ok ve Vazgeç, dondurmanın YAPILDIĞI tedavinin ekranına döner --
    # FET'te yeniden dondurmada o FET, kaynak tedavi değil.
    hedef = _vit_yapildigi_tedavi(kayit, sp["cycle_id"])
    return sablon.TemplateResponse(
        request, "vit_sil.html",
        {"sp": sp, "kayit": kayit, "kardes": kardes, "hedef_cycle": hedef,
         "adres_cycle": cycle, "engel": _vit_geri_alma_engeli(kayit)})


@uygulama.post("/specimen/{specimen_id}/vit-sil")
async def vit_sil(request: Request, specimen_id: str):
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    f = await request.form()
    # Adrese yazılacak bir değer: yalnızca rakam (denüdasyonun `secili`
    # alanının kuralı, v6.35).
    cycle_metin = (f.get("cycle") or "").strip()
    cycle = int(cycle_metin) if cycle_metin.isdigit() else 0
    from datetime import datetime as _d
    kid = request.state.kullanici["id"]
    simdi = _d.now().isoformat(" ", "seconds")

    k = _vit_kaydi(specimen_id, cycle)
    # Sunucu da reddediyor -- ekranda düğmeyi gizlemek yetmez.
    if _vit_geri_alma_engeli(k):
        return RedirectResponse(
            f"/specimen/{specimen_id}/vit-sil" + (f"?cycle={cycle}" if cycle else ""),
            status_code=303)
    cozme = _dondurma_oncesi_cozme(k)
    hedef = _vit_yapildigi_tedavi(k, sp["cycle_id"])
    if k:
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep='Vitrifikasyon kaydi temizlendi' WHERE id=?",
               (kid, simdi, k["id"]))
        tid = k["vit_tasiyici_id"]
        if tid:
            kalan = db.tek("SELECT COUNT(*) k FROM olay WHERE vit_tasiyici_id=? "
                           "AND tip='vitrifikasyon' AND iptal_mi=0", (tid,))["k"]
            if kalan == 0:
                t = db.tek("SELECT konum_id FROM tasiyici WHERE id=?", (tid,))
                db.yaz("UPDATE tasiyici SET durum='bosaltildi' WHERE id=?", (tid,))
                if t and t["konum_id"]:
                    db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))

    # Önceki duruma dön. FET'te yeniden dondurma geri alındıysa embriyo o
    # tedavide çözülmüş hâline döner (transfere de, tekrar dondurmaya da
    # aday) -- `transfer_sil()`'in çözme kuralının aynısı. Aksi hâlde eski
    # davranış.
    onceki = "blastokist"
    if cozme:
        onceki = ("cozuldu" if cozme["thaw_sagkalim"] == "canli"
                  else cozme["thaw_sagkalim"] or "cozuldu")
    guvenlik.degisiklikleri_yaz("specimen", specimen_id, sp,
                                {"durum": onceki}, kid)
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (onceki, specimen_id))
    return RedirectResponse(f"/cycle/{hedef}/vitrifikasyon", status_code=303)


# ----------------------------------------------------------------- thaw

def thaw_cycle_var() -> bool:
    """`goc_024` çalıştırıldı mı — `olay.thaw_cycle_id` kolonu var mı.

    Göç çalıştırılmadan ekranlar 500 vermesin diye (tuzak #3). Bir kez
    bakılıp `db.kolon_var()`'da saklanıyor; yedekten geri yüklemeden sonra
    unutuluyor (v6.145, tuzak #15).
    """
    return db.kolon_var("olay", "thaw_cycle_id")


def _tup_yumurta_mi(icerik) -> bool:
    """Taşıyıcıda yumurta mı var, embriyo mu -- içerikten (`icerik`,
    v6.167, `icerik_sql()`'in gerekçesi). Bir tüp tek tedavinin."""
    return bool(icerik) and icerik[0]["icerik"] == "yumurta"


def thaw_tedavi_tipleri(icerik) -> list:
    """Bu tüpün çözülebileceği tedavi tipleri (v6.155).

    Çözmesi olan tipler (`db.cozme_tedavisi_mi()`: IVF/ICSI değil) ve
    tüpün içeriğiyle aynı türü çözenler: embriyo tüpü FET / FET (3→5),
    yumurta tüpü Yumurta Çözme (ve Yumurta Dondurma'nın kendi çözmesi).
    Sıra `TIP_ASAMALARI`'nın sırası -- ilki "yeni tedavi aç" düğmesinin ilki.
    """
    yumurta = _tup_yumurta_mi(icerik)
    blast = tup_cleavage_tipine_kapali(icerik)
    return [t for t in TIP_ASAMALARI
            if db.cozme_tedavisi_mi(t) and db.yumurta_mi(t, "thaw") == yumurta
            and not (blast and t in db.CLEAVAGE_COZEN_TIPLER)]


def tup_cleavage_tipine_kapali(icerik) -> bool:
    """Bu tüp FET (3→5)'te çözülemez mi (v6.156, kullanıcının isteği:
    "FET (3→5)'te sadece cleavage tüplerinin çözülmesine izin ver").

    Tüpte blastokist olarak dondurulmuş bir örnek varsa kapalı. Evresi
    bilinmeyen tüp (hiç değerlendirmesi yok -- skoru okunamamış eski bir
    kayıt) kapalı değil: blastokist olduğu gösterilemiyor. Var olan kayıt
    dokunulmaz (v6.139'un kuralı): bu tüpten bir FET (3→5) için zaten
    çözme yazılmışsa o çözme düzeltilebilsin diye kapı açık kalıyor.
    """
    if not icerik or not any(r["blastokist"] for r in icerik):
        return False
    if db.cozme_tupu_var():
        yer = ",".join("?" * len(db.CLEAVAGE_COZEN_TIPLER))
        var = db.tek(
            "SELECT 1 FROM olay z JOIN cycle cz ON cz.id = z.thaw_cycle_id "
            "WHERE z.tip='thaw' AND z.iptal_mi=0 AND z.thaw_tasiyici_id=? "
            f"AND cz.cycle_tipi IN ({yer}) LIMIT 1",
            (icerik[0]["tasiyici_id"], *db.CLEAVAGE_COZEN_TIPLER))
        if var:
            return False
    return True


def thaw_cycle_secenekleri(icerik):
    """Bu taşıyıcı hangi tedaviler için çözülebilir (v6.155).

    v6.155'e kadar hastanın BÜTÜN tedavileri sunuluyor, seçim yoksa embriyonun
    kaynak tedavisi seçili geliyordu. Kullanıcının bildirdiği: IVF/ICSI'de
    dondurulan embriyo oradan çözülünce FET'in işi ICSI'nin kaydına ve
    resmî formlarına yazılıyordu, iki tedavi birleşiyordu. Artık yalnızca
    çözmesi olan, tüpün içeriğine uygun tipteki tedaviler
    (`thaw_tedavi_tipleri()`). Hiçbiri yoksa liste boş; ekran yeni bir FET
    açmayı önerir.

    Taşıyıcı tek bir vitrifikasyon ekranından doldurulur, yani tek hastaya
    aittir. Karışık bir taşıyıcıda (elle veri düzeltmesi vb.) seçim yok.
    """
    hastalar = {r["hasta_id"] for r in icerik}
    if len(hastalar) != 1:
        return []
    tipler = thaw_tedavi_tipleri(icerik)
    if not tipler:
        return []
    return db.sorgu(
        "SELECT id, cycle_no, cycle_tipi, hasta_cycle_no, durum FROM cycle "
        f"WHERE hasta_id=? AND cycle_tipi IN ({','.join('?' * len(tipler))}) "
        "ORDER BY hasta_cycle_no DESC, id DESC",
        (hastalar.pop(), *tipler))


@uygulama.get("/cryo/tasiyici/{tasiyici_id}/thaw")
def thaw_ekran(request: Request, tasiyici_id: int, hata: str = "", cycle: int = 0):
    t = db.tek("SELECT t.*, k.tam_yol FROM tasiyici t "
               "LEFT JOIN konum k ON k.id=t.konum_id WHERE t.id=?", (tasiyici_id,))
    if not t:
        return RedirectResponse("/cryo", status_code=303)

    from datetime import datetime as _d
    icerik = tasiyici_icerigi(tasiyici_id)
    mevcut, fotolar = {}, {}
    # Mevcut çözme: BU tüpten yapılan (v6.143). Yeniden dondurulan bir
    # embriyonun ikinci tüpü açıldığında ilk tüpten yapılan çözme "zaten
    # çözüldü" diye görünmemeli. Göç yoksa eski ölçü: örneğin son çözmesi.
    tup_kosul = "AND thaw_tasiyici_id=? " if db.cozme_tupu_var() else ""
    tup_deger = (tasiyici_id,) if db.cozme_tupu_var() else ()
    for e in icerik:
        k = db.tek("SELECT * FROM olay WHERE specimen_id=? AND tip='thaw' "
                   "AND iptal_mi=0 " + tup_kosul + "ORDER BY id DESC LIMIT 1",
                   (e["id"], *tup_deger))
        if k:
            mevcut[e["id"]] = k
        fotolar[e["id"]] = {}
        for asama in ("thaw_sonrasi", "transfer_oncesi"):
            fotolar[e["id"]][asama] = db.sorgu(
                "SELECT id FROM goruntu WHERE specimen_id=? AND asama=? ORDER BY id",
                (e["id"], asama))

    # Çözme hangi tedavi için yapılıyor. Geldiğimiz tedavi varsayılan; yoksa
    # daha önce kaydedilmiş değer; o da yoksa tek bir açık (aktif) uygun
    # tedavi. v6.155'e kadar son çare embriyonun KAYNAK tedavisiydi -- FET'in
    # işi ICSI'ye yazılıyordu. Artık seçim yoksa personel seçer ya da yeni
    # FET açar; sunucu da seçimsiz kaydı reddediyor.
    secenekler = thaw_cycle_secenekleri(icerik) if thaw_cycle_var() else []
    gecerli = {r["id"] for r in secenekler}
    secili = cycle if cycle in gecerli else 0
    if not secili and mevcut and secenekler:
        ilk = next(iter(mevcut.values()))
        secili = ilk["thaw_cycle_id"] if ilk["thaw_cycle_id"] in gecerli else 0
    if not secili:
        aktif = [r["id"] for r in secenekler if r["durum"] == "aktif"]
        secili = aktif[0] if len(aktif) == 1 else 0
    # FET (3→5)'in ekranından blastokist tüpüne gelindiyse o tedavi listede
    # yok (v6.156); sebebi yazılmazsa personel neden seçemediğini anlamaz.
    if cycle and cycle not in gecerli and not hata:
        gelinen = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle,))
        if gelinen and gelinen["cycle_tipi"] in db.CLEAVAGE_COZEN_TIPLER \
                and tup_cleavage_tipine_kapali(icerik):
            hata = metinler.t("fet_kultur_yalniz_cleavage")

    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    return sablon.TemplateResponse(
        request, "thaw.html",
        {"t": t, "icerik": icerik, "mevcut": mevcut, "fotolar": fotolar,
         "hata": hata, "cycle_secenekleri": secenekler, "secili_cycle": secili,
         "geri_cycle": cycle if cycle in gecerli else 0,
         # Yeni tedavi açma düğmeleri (v6.155): göç yoksa (thaw_cycle_id
         # kolonu yok) eski davranış, düğme de yok.
         "yeni_tipler": (thaw_tedavi_tipleri(icerik)
                         if thaw_cycle_var() and icerik else []),
         "sagkalimlar": db.liste("thaw_sagkalim"), "etiketler": etiketler,
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M")})


@uygulama.post("/cryo/tasiyici/{tasiyici_id}/thaw")
async def thaw_kaydet(request: Request, tasiyici_id: int):
    from urllib.parse import quote
    f = await request.form()
    t = db.tek("SELECT * FROM tasiyici WHERE id=?", (tasiyici_id,))
    if not t:
        return RedirectResponse("/cryo", status_code=303)

    icerik = tasiyici_icerigi(tasiyici_id)
    if not icerik:
        return RedirectResponse(f"/cryo/tasiyici/{tasiyici_id}", status_code=303)

    kid = request.state.kullanici["id"]
    simdi = islem_zamani(f.get("islem_zamani"))

    eksik = [e for e in icerik if not f.get(f"sagkalim_{e['id']}")]
    if eksik:
        return RedirectResponse(
            f"/cryo/tasiyici/{tasiyici_id}/thaw?hata=" +
            quote("Her embriyo için sağkalım seçilmeli. "
                  "Taşıyıcı çözüldüğünde içindekilerin hepsi etkilenir."),
            status_code=303)

    kontrol_zamani = zaman(f.get("kontrol_zamani"))
    thaw_notu = bos_ise_none(f.get("thaw_notu"))

    # Çözme hangi tedavi için yapıldı. Formdaki değer aynı hastanın çözmesi
    # olan bir tedavisi olmalı (v6.155). Önceden geçersiz seçim embriyonun
    # kendi tedavisine düşüyordu -- IVF/ICSI'ye; artık reddediliyor.
    gecerli = ({r["id"] for r in thaw_cycle_secenekleri(icerik)}
               if thaw_cycle_var() else set())
    try:
        secili_cycle = int(f.get("thaw_cycle") or 0)
    except ValueError:
        secili_cycle = 0
    if secili_cycle not in gecerli:
        secili_cycle = 0
    if thaw_cycle_var() and not secili_cycle:
        geri = f.get("geri_cycle") or ""
        return RedirectResponse(
            f"/cryo/tasiyici/{tasiyici_id}/thaw?hata="
            + quote(metinler.t("cozme_tedavisi_sec"))
            + (f"&cycle={int(geri)}" if geri.isdigit() else ""),
            status_code=303)

    def yuzde(v, ad):
        try:
            x = sayi(v, ad)
        except FormHatasi:
            return None
        return None if x is None else max(0.0, min(100.0, x))

    for e in icerik:
        sagkalim = f.get(f"sagkalim_{e['id']}")
        re_exp = yuzde(f.get(f"reexp_{e['id']}"), "Re-expansion")
        canlilik = yuzde(f.get(f"canlilik_{e['id']}"), "Canlılık oranı")

        alanlar = {"thaw_sagkalim": sagkalim, "thaw_canlilik": canlilik,
                   "thaw_re_expansion": re_exp,
                   "thaw_kontrol_zamani": kontrol_zamani,
                   "thaw_notu": thaw_notu}
        if thaw_cycle_var():
            alanlar["thaw_cycle_id"] = secili_cycle or e["cycle_id"]
        # Tüp başına bir çözme (v6.143): aynı tüpün formu yeniden
        # kaydedilirse o çözme güncellenir (düzeltme, eski davranış); başka
        # bir tüpten -- yeniden dondurulan embriyonun ikinci tüpü -- yeni
        # kayıt açılır, ilk FET'in çözmesi ezilmez.
        ek_kosul, ek_deger = "", ()
        if db.cozme_tupu_var():
            alanlar["thaw_tasiyici_id"] = tasiyici_id
            ek_kosul, ek_deger = "thaw_tasiyici_id = ?", (tasiyici_id,)
        thaw_id = olay_kaydet_veya_guncelle(e["id"], e["cycle_id"], "thaw",
                                            alanlar, kid, simdi,
                                            ek_kosul=ek_kosul, ek_deger=ek_deger)
        # Bu çözmeden SONRA yeniden dondurulduysa (eski bir tüpün çözme
        # bilgisi sonradan düzeltiliyor) durum "çözüldü"ye çekilmez: embriyo
        # şu an başka bir tüpte donmuş duruyor.
        sonra_donduruldu = db.tek(
            "SELECT 1 FROM olay WHERE specimen_id=? AND tip='vitrifikasyon' "
            "AND iptal_mi=0 AND id > ?", (e["id"], thaw_id))
        if not sonra_donduruldu:
            db.yaz("UPDATE specimen SET durum=? WHERE id=?",
                   ("cozuldu" if sagkalim == "canli" else sagkalim, e["id"]))

    # Taşıyıcı boşaldı, konumu serbest kaldı
    db.yaz("UPDATE tasiyici SET durum='bosaltildi' WHERE id=?", (tasiyici_id,))
    if t["konum_id"]:
        db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))

    # FET'in günü çözme günü (v6.144): geriye tarihli bir çözme tedaviyi
    # hastanın öteki tedavilerinin önüne alabilir.
    for hid in {e["hasta_id"] for e in icerik}:
        tedavi_sirasini_duzelt(hid, kid)

    # Bir cycle ekranından gelindiyse oraya dön — sonuç orada listelenir
    if f.get("geri_cycle") and secili_cycle:
        return RedirectResponse(f"/cycle/{secili_cycle}/thaw", status_code=303)
    return RedirectResponse(f"/cryo/tasiyici/{tasiyici_id}", status_code=303)


def _cozme_tupu(kayit, specimen_id):
    """Bu çözmenin boşalttığı tüp: `{vit_tasiyici_id, etiket}` ya da None.

    v6.143'ten beri çözme tüpünü kendisi biliyor (`thaw_tasiyici_id`,
    goc_046). Bilmiyorsa (göç yok ya da tüpü programda olmayan program öncesi
    bir kayıt) eski ölçü: örneğin son dondurmasının tüpü.
    """
    if kayit and db.cozme_tupu_var() and kayit["thaw_tasiyici_id"]:
        return db.tek("SELECT id AS vit_tasiyici_id, etiket FROM tasiyici "
                      "WHERE id=?", (kayit["thaw_tasiyici_id"],))
    return db.tek("SELECT o.vit_tasiyici_id, t.etiket FROM olay o "
                  "LEFT JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
                  "WHERE o.specimen_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
                  "ORDER BY o.id DESC LIMIT 1", (specimen_id,))


def _cozme_geri_alma_engeli(kayit):
    """Bu çözme geri alınamıyorsa sebebinin metin anahtarı (v6.143).

    Önce en son adım geri alınır: çözmeden SONRA açılmış bir dondurma varsa
    (FET'te yeniden dondurma) çözmeyi silmek "hiç çözülmedi" demek olurdu ama
    embriyo o arada başka bir tüpe girmiş. Kimlik sırası, saat değil.

    v6.147'den beri çözmeden sonra açılmış HER kayıt engel: Yumurta Çözme'de
    çözülen yumurtanın ICSI'si, döllenmesi, değerlendirmesi, transferi.
    Çözme gidince örnek o tedavinin ekranlarından düşer, kayıtları sahipsiz
    kalır -- zaman çizelgesi onları kaynak tedaviye yazardı
    (`db.olay_tedavisi()`).
    """
    if not kayit:
        return None
    if db.cozme_tupu_var() and db.tek(
            "SELECT 1 FROM olay WHERE specimen_id=? AND tip='vitrifikasyon' "
            "AND iptal_mi=0 AND id > ?", (kayit["specimen_id"], kayit["id"])):
        return "thaw_geri_alma_yeniden_dondurulmus"
    sonra = db.tek("SELECT 1 FROM olay WHERE specimen_id=? AND tip <> 'thaw' "
                   "AND iptal_mi=0 AND id > ?", (kayit["specimen_id"], kayit["id"]))
    return "thaw_geri_alma_sonraki_kayit" if sonra else None


@uygulama.post("/cryo/tasiyici/{tasiyici_id}/yeni-tedavi")
async def thaw_yeni_tedavi(request: Request, tasiyici_id: int):
    """Çözme ekranından yeni bir FET / Yumurta Çözme tedavisi açar (v6.155).

    Kullanıcının isteği: "ivf/icsi tedavisinde çözme menüsünden dondurulmuş
    embriyoyu görüp bunu çöz dediğimizde FET tedavisi adı altında yeni bir
    tedavi başlatması gerekiyor." Tedavi formu (`/hasta/{id}/cycle/yeni`)
    atlanıyor: FET'in formda doldurulacak alanı yok denecek kadar az
    (endikasyon, protokol sonradan tedavi ekranından girilir). Lab kayıt no
    ve "kaçıncı tedavi" programın verdiği; numara tarih sırasıyla (v6.144)
    -- FET'in günü çözme kaydedilince gelir, ondan sonra yeniden numaralanır.

    Tip beyaz listeden (`thaw_tedavi_tipleri()`): adresten gelen metin cycle
    tipine yazılmıyor. Sonra çözme ekranına bu tedavi seçili dönülüyor.
    """
    from urllib.parse import quote
    f = await request.form()
    icerik = tasiyici_icerigi(tasiyici_id)
    hastalar = {r["hasta_id"] for r in icerik}
    tip = f.get("tip") or ""
    if not icerik or len(hastalar) != 1 or not thaw_cycle_var() \
            or tip not in thaw_tedavi_tipleri(icerik):
        return RedirectResponse(f"/cryo/tasiyici/{tasiyici_id}/thaw",
                                status_code=303)
    hasta_id = hastalar.pop()
    kid = request.state.kullanici["id"]
    for _ in range(3):
        # İki personel aynı anda tedavi açarsa aynı numarayı alabilir; UNIQUE
        # hatasında sıradaki numarayla tekrar dene (cycle_kaydet'in gerekçesi).
        try:
            with db.yazma_islemi() as b:
                yeni_id = b.execute(
                    "INSERT INTO cycle (lab_id, hasta_id, cycle_no, cycle_tipi) "
                    "VALUES (?, ?, ?, ?)",
                    (db.LAB_ID, hasta_id, sonraki_lab_no(), tip)).lastrowid
                degisen = db.tedavileri_sirala(b, hasta_id)
            break
        except sqlite3.IntegrityError:
            continue
    else:
        return RedirectResponse(
            f"/cryo/tasiyici/{tasiyici_id}/thaw?hata="
            + quote(metinler.t("yeni_tedavi_acilamadi")), status_code=303)
    tedavi_sirasini_logla(degisen, kid, haric=yeni_id)
    return RedirectResponse(f"/cryo/tasiyici/{tasiyici_id}/thaw?cycle={yeni_id}",
                            status_code=303)


@uygulama.get("/specimen/{specimen_id}/thaw-sil")
def thaw_sil_ekran(request: Request, specimen_id: str):
    sp = db.tek("SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
                "JOIN cycle c ON c.id=s.cycle_id JOIN hasta h ON h.id=c.hasta_id "
                "WHERE s.id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    kayit = db.tek("SELECT * FROM olay WHERE specimen_id=? AND tip='thaw' "
                   "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (specimen_id,))
    vit = _cozme_tupu(kayit, specimen_id)
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    return sablon.TemplateResponse(
        request, "thaw_sil.html",
        {"sp": sp, "kayit": kayit, "vit": vit, "etiketler": etiketler,
         "engel": _cozme_geri_alma_engeli(kayit)})


@uygulama.post("/specimen/{specimen_id}/thaw-sil")
def thaw_sil(request: Request, specimen_id: str):
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    from datetime import datetime as _d
    kid = request.state.kullanici["id"]
    k = db.tek("SELECT * FROM olay WHERE specimen_id=? AND tip='thaw' AND iptal_mi=0 "
               "ORDER BY id DESC LIMIT 1", (specimen_id,))
    # Sunucu da reddediyor -- ekranda düğmeyi gizlemek yetmez.
    if _cozme_geri_alma_engeli(k):
        return RedirectResponse(f"/specimen/{specimen_id}/thaw-sil", status_code=303)
    vit = _cozme_tupu(k, specimen_id)
    if k:
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep='Thaw kaydi temizlendi' WHERE id=?",
               (kid, _d.now().isoformat(" ", "seconds"), k["id"]))
    db.yaz("UPDATE specimen SET durum='dondurulmus' WHERE id=?", (specimen_id,))
    # Çözme gidince FET'in günü değişebilir (v6.144).
    h = db.tek("SELECT hasta_id FROM cycle WHERE id=?", (sp["cycle_id"],))
    tedavi_sirasini_duzelt(h and h["hasta_id"], kid)

    hedef = f"/cryo/tasiyici/{vit['vit_tasiyici_id']}" if vit and vit["vit_tasiyici_id"] else "/cryo"
    return RedirectResponse(hedef, status_code=303)


@uygulama.get("/cycle/{cycle_id}/thaw")
def cycle_thaw_listesi(request: Request, cycle_id: int):
    """Bu cycle'ın embriyolarını içeren taşıyıcılar — çözme girişi."""
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)
    # Çözmesi olmayan tip (v6.155: IVF/ICSI): eski bir bağlantı ya da yer imi
    # buraya düşerse tedavi ekranına dön -- çözme ayrı bir FET tedavisinde.
    if not db.cozme_tedavisi_mi(c["cycle_tipi"]):
        return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)

    # FET cycle'inda hastanin tum cycle'larindaki tasiyicilar listelenir;
    # dondurulan embriyo baska bir cycle'dan gelir. fet_kultur'da da ayni
    # (gun 5'e kadar kulturlenecek embriyo da baska bir cycle'dan geliyor).
    if fet_tipi_mi(c["cycle_tipi"]):
        kosul = "c2.hasta_id = ?"
        par = (c["hasta_id"],)
    else:
        kosul = "s.cycle_id = ?"
        par = (cycle_id,)

    # v6.143: bir tüpten yapılan çözme o tüpün kendi kaydı (`thaw_tasiyici_id`).
    # Eski ölçü ("bu tüpte dondurulmuş örneğin herhangi bir çözmesi")
    # yeniden dondurulan bir embriyoda ikinci tüpe ilk tüpün çözmesini
    # sayardı. Göç yoksa eski ölçü.
    tup_yeni = db.cozme_tupu_var()
    cozulen_alt = (
        "  (SELECT COUNT(*) FROM olay o3 WHERE o3.tip='thaw' AND o3.iptal_mi=0 "
        "   AND o3.thaw_tasiyici_id=t.id) AS cozulen, " if tup_yeni else
        "  (SELECT COUNT(*) FROM olay o3 JOIN olay v3 ON v3.specimen_id=o3.specimen_id "
        "   AND v3.tip='vitrifikasyon' AND v3.iptal_mi=0 AND v3.vit_tasiyici_id=t.id "
        "   WHERE o3.tip='thaw' AND o3.iptal_mi=0) AS cozulen, ")
    tasiyicilar = db.sorgu(
        "SELECT DISTINCT t.id, t.etiket, t.tip, t.renk, t.durum, k.tam_yol, "
        "  t.vitrifikasyon_zamani, "
        "  (SELECT COUNT(*) FROM olay o2 WHERE o2.vit_tasiyici_id=t.id "
        "   AND o2.tip='vitrifikasyon' AND o2.iptal_mi=0) AS adet, "
        + cozulen_alt +
        "  (SELECT group_concat(DISTINCT c3.cycle_no) FROM olay o4 "
        "   JOIN specimen s4 ON s4.id=o4.specimen_id "
        "   JOIN cycle c3 ON c3.id=s4.cycle_id "
        "   WHERE o4.vit_tasiyici_id=t.id AND o4.tip='vitrifikasyon' "
        "   AND o4.iptal_mi=0) AS kaynak_cycle, "
        + icerik_sql() +
        " FROM tasiyici t "
        "JOIN olay o ON o.vit_tasiyici_id=t.id AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
        "JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c2 ON c2.id = s.cycle_id "
        "LEFT JOIN konum k ON k.id=t.konum_id "
        f"WHERE {kosul} ORDER BY t.durum DESC, t.etiket", par)

    # FET (3→5)'te blastokist tüpü çözülemez (v6.156): "Çöz" yerine sebebi.
    # Liste kısa (hastanın tüpleri), tüp başına içerik sorgusu sorun değil.
    if c["cycle_tipi"] in db.CLEAVAGE_COZEN_TIPLER:
        tasiyicilar = [
            {**dict(t), "cleavage_kapali": t["durum"] == "dolu"
             and tup_cleavage_tipine_kapali(tasiyici_icerigi(t["id"]))}
            for t in tasiyicilar]

    # Bu cycle için yapılmış çözmeler. Transfere ulaşmayan (canlı çıkmayan)
    # embriyo da burada görünür — FET'in kaydı budur (README v6.7).
    # Satırın tüpü çözmenin KENDİ tüpü (v6.143). Eski birleştirme (örneğin
    # dondurma kayıtları üzerinden) yeniden dondurulan bir embriyoyu iki
    # dondurmasıyla iki satır yapardı. Transfer de yalnızca BU tedavideki:
    # başka bir FET'te sonradan transfer edilen embriyo burada "transfer
    # edildi" görünmesin.
    if tup_yeni:
        tup_birlesimi = "LEFT JOIN tasiyici t ON t.id=o.thaw_tasiyici_id "
        tr_kosul = "AND COALESCE(tr.tr_cycle_id, tr.cycle_id) = o.thaw_cycle_id"
    else:
        tup_birlesimi = ("LEFT JOIN olay v ON v.specimen_id=s.id "
                         "  AND v.tip='vitrifikasyon' AND v.iptal_mi=0 "
                         "LEFT JOIN tasiyici t ON t.id=v.vit_tasiyici_id ")
        tr_kosul = ""
    cozulenler = [] if not thaw_cycle_var() else db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.cycle_id, c2.cycle_no AS kaynak_cycle_no, "
        "  c2.hasta_cycle_no AS kaynak_hasta_cycle_no, "
        "  o.zaman, o.thaw_sagkalim, o.thaw_canlilik, o.thaw_re_expansion, "
        "  t.etiket AS tasiyici_etiket, "
        "  (SELECT tr.id FROM olay tr WHERE tr.specimen_id=s.id "
        f"   AND tr.tip='transfer' AND tr.iptal_mi=0 {tr_kosul}) AS transfer_id "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c2 ON c2.id=s.cycle_id "
        + tup_birlesimi +
        "WHERE o.tip='thaw' AND o.iptal_mi=0 AND o.thaw_cycle_id=? "
        "ORDER BY o.zaman, s.cycle_sira_no", (cycle_id,))
    ozet = None
    if cozulenler:
        canli = sum(1 for r in cozulenler if r["thaw_sagkalim"] == "canli")
        ozet = {"toplam": len(cozulenler), "canli": canli,
                "oran": round(100 * canli / len(cozulenler)),
                "transfer": sum(1 for r in cozulenler if r["transfer_id"])}

    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    return sablon.TemplateResponse(
        request, "cycle_thaw.html",
        {"c": c, "tasiyicilar": tasiyicilar, "etiketler": etiketler,
         "cozulenler": cozulenler, "ozet": ozet, "goc_gerekli": not thaw_cycle_var(),
         # Vitrifikasyon ekranına bağlantı, tipin o aşaması varsa (v6.143:
         # FET'e de geldi). Tip adını elle yazma, `TIP_ASAMALARI`'na bak.
         "vit_var": "vitrifikasyon" in TIP_ASAMALARI.get(c["cycle_tipi"], ()),
         "gezinme": asama_gezinme(cycle_id, "thaw")})


# ----------------------------------------------------------------- transfer

TRANSFERE_UYGUN = ("blastokist", "morula", "kavitasyon", "cozuldu", "kismi_hasar",
                   "zigot", "gun2", "gun3")


def transfer_adaylari(hasta_id: int, cycle=None):
    """Bu hastanın transfer edilebilir embriyoları — taze ve çözülmüş.

    **Tedaviye göre süzülür** (v6.155, `cycle` verilirse). Çözme ayrı bir
    tedavi olunca transfer de öyle: FET tiplerinde yalnızca BU tedavi için
    çözülenler (`db.tedavi_ornekleri()`), öteki tiplerde (IVF/ICSI) yalnızca
    tedavinin kendi, hiç çözülmemiş embriyoları. Önceden hastanın bütün
    embriyoları listeleniyordu: IVF/ICSI'nin transfer ekranında FET'te
    çözülen embriyo seçilebiliyor, iki tedavi yine birleşiyordu. Göç
    (goc_024) yoksa eski davranış.

    **Yumurta transfer adayı değil** (v6.147). Yumurta Dondurma'da
    dondurulan yumurta çözülünce 'cozuldu' durumuna geçiyor -- embriyonunkiyle
    aynı değer -- ve Yumurta Çözme'nin transfer aşaması gelince listede
    görünmeye başlıyordu. Ölçü: yumurta donduran bir tedavinin örneği
    (`db.yumurta_mi()`) ve hiç ICSI'si yok. ICSI'den sonra embriyo olur,
    döllenince (zigot, gün 2/3, blastokist) aday.
    """
    yumurta_tipleri = ", ".join(
        f"'{t}'" for t in TIP_ASAMALARI if db.yumurta_mi(t)) or "''"
    tedavi_kosulu, tedavi_par = "", ()
    if cycle is not None and thaw_cycle_var():
        if cycle["cycle_tipi"] in FET_TIPLERI:
            tedavi_kosulu = "AND " + db.tedavi_ornekleri(cycle["cycle_tipi"], "s")
        else:
            tedavi_kosulu = ("AND s.cycle_id = ? AND NOT EXISTS (SELECT 1 "
                             "FROM olay z WHERE z.specimen_id=s.id "
                             "AND z.tip='thaw' AND z.iptal_mi=0)")
        tedavi_par = (cycle["id"],)
    return db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.durum, s.cycle_id, c.cycle_no, "
        "  c.hasta_cycle_no, "
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS skor, "
        "  (SELECT o.thaw_sagkalim FROM olay o WHERE o.specimen_id=s.id "
        "   AND o.tip='thaw' AND o.iptal_mi=0 ORDER BY o.id DESC LIMIT 1) AS thaw, "
        "  COALESCE( "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     AND g.asama IN ('transfer_oncesi','blastokist') ORDER BY g.id DESC LIMIT 1), "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     ORDER BY g.id DESC LIMIT 1)) AS goruntu, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id=s.id) "
        "  AS goruntu_idler, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id=s.id) AS kare "
        "FROM specimen s JOIN cycle c ON c.id=s.cycle_id "
        "WHERE c.hasta_id=? AND s.durum IN "
        "  ('blastokist','morula','kavitasyon','cozuldu','kismi_hasar', "
        "   'zigot','gun2','gun3') "
        "AND NOT EXISTS (SELECT 1 FROM olay o WHERE o.specimen_id=s.id "
        "                AND o.tip='transfer' AND o.iptal_mi=0) "
        f"AND NOT (c.cycle_tipi IN ({yumurta_tipleri}) "
        "         AND NOT EXISTS (SELECT 1 FROM olay i WHERE i.specimen_id=s.id "
        "                         AND i.tip='icsi' AND i.iptal_mi=0)) "
        f"{tedavi_kosulu} "
        "ORDER BY c.hasta_cycle_no, s.cycle_sira_no", (hasta_id, *tedavi_par))


@uygulama.get("/cycle/{cycle_id}/transfer")
def transfer_ekran(request: Request, cycle_id: int, hata: str = ""):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad, h.id AS hasta_id FROM cycle c "
               "JOIN hasta h ON h.id = c.hasta_id WHERE c.id = ?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    adaylar = transfer_adaylari(c["hasta_id"], c)
    edilen = db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.cycle_id, c2.cycle_no, c2.hasta_cycle_no, "
        "  o.zaman, o.tr_tipi, o.id AS olay_id, "
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS skor, "
        "  COALESCE( "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     AND g.asama IN ('transfer_oncesi','blastokist') ORDER BY g.id DESC LIMIT 1), "
        "    (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id "
        "     ORDER BY g.id DESC LIMIT 1)) AS goruntu, "
        "  (SELECT group_concat(g.id) FROM goruntu g WHERE g.specimen_id=s.id) "
        "  AS goruntu_idler, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id=s.id) AS kare "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c2 ON c2.id=s.cycle_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 AND o.tr_cycle_id=? "
        "ORDER BY s.cycle_sira_no", (cycle_id,))

    return sablon.TemplateResponse(
        request, "transfer.html",
        {"c": c, "adaylar": adaylar, "edilen": edilen, "hata": hata,
         "gezinme": asama_gezinme(cycle_id, "transfer"),
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M")})


@uygulama.post("/cycle/{cycle_id}/transfer")
async def transfer_kaydet(request: Request, cycle_id: int):
    from urllib.parse import quote
    f = await request.form()
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    secilen = f.getlist("embriyo")
    if not secilen:
        return RedirectResponse(
            f"/cycle/{cycle_id}/transfer?hata=" + quote("Hiç embriyo seçilmedi."),
            status_code=303)

    kid = request.state.kullanici["id"]
    simdi = islem_zamani(f.get("islem_zamani"))
    # Ekranın gösterdiği adaylardan olmalı (v6.155): eski bir sekmeden ya da
    # elle kurulmuş bir istekten başka tedavinin embriyosu gelirse yazılmaz.
    uygun = {r["id"] for r in transfer_adaylari(c["hasta_id"], c)}

    for sid in secilen:
        if sid not in uygun:
            continue
        sp = db.tek("SELECT * FROM specimen WHERE id=?", (sid,))
        if not sp:
            continue
        # Çözülmüşse donmuş, değilse taze
        cozuldu = db.tek("SELECT id FROM olay WHERE specimen_id=? AND tip='thaw' "
                         "AND iptal_mi=0", (sid,))
        olay_kaydet_veya_guncelle(
            sid, sp["cycle_id"], "transfer",
            {"tr_cycle_id": cycle_id, "tr_tipi": "donmus" if cozuldu else "taze"},
            kid, simdi)
        db.yaz("UPDATE specimen SET durum='transfer_edildi' WHERE id=?", (sid,))

    # FET'in günü transfer günü de olabilir (v6.144, `db.tedavi_tarihi()`).
    tedavi_sirasini_duzelt(c["hasta_id"], kid)
    return RedirectResponse(f"/cycle/{cycle_id}/transfer", status_code=303)


@uygulama.get("/specimen/{specimen_id}/transfer-sil")
def transfer_sil_ekran(request: Request, specimen_id: str):
    sp = db.tek("SELECT s.*, c.cycle_no, h.dosya_no, h.ad_soyad FROM specimen s "
                "JOIN cycle c ON c.id=s.cycle_id JOIN hasta h ON h.id=c.hasta_id "
                "WHERE s.id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    kayit = db.tek("SELECT o.*, c.cycle_no AS tr_cycle_no FROM olay o "
                   "LEFT JOIN cycle c ON c.id=o.tr_cycle_id "
                   "WHERE o.specimen_id=? AND o.tip='transfer' AND o.iptal_mi=0 "
                   "ORDER BY o.id DESC LIMIT 1", (specimen_id,))
    return sablon.TemplateResponse(
        request, "transfer_sil.html", {"sp": sp, "kayit": kayit})


@uygulama.post("/specimen/{specimen_id}/transfer-sil")
def transfer_sil(request: Request, specimen_id: str):
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    from datetime import datetime as _d
    kid = request.state.kullanici["id"]
    k = db.tek("SELECT * FROM olay WHERE specimen_id=? AND tip='transfer' "
               "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (specimen_id,))
    hedef_cycle = k["tr_cycle_id"] if k else sp["cycle_id"]
    if k:
        db.yaz("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
               "iptal_sebep='Transfer kaydi temizlendi' WHERE id=?",
               (kid, _d.now().isoformat(" ", "seconds"), k["id"]))

    # Önceki duruma dön
    thaw = db.tek("SELECT thaw_sagkalim FROM olay WHERE specimen_id=? AND tip='thaw' "
                  "AND iptal_mi=0 ORDER BY id DESC LIMIT 1", (specimen_id,))
    if thaw:
        onceki = "cozuldu" if thaw["thaw_sagkalim"] == "canli" else thaw["thaw_sagkalim"]
    else:
        bl = db.tek("SELECT bl_genisleme FROM olay WHERE specimen_id=? "
                    "AND tip='blastokist_degerlendirme' AND iptal_mi=0 "
                    "ORDER BY gun DESC LIMIT 1", (specimen_id,))
        if bl:
            onceki = ("arrest" if bl["bl_genisleme"] == "arrest"
                      else "kavitasyon" if bl["bl_genisleme"] == "kavitasyon"
                      else "morula" if bl["bl_genisleme"] in ("morula", "erken_morula")
                      else "blastokist")
        else:
            onceki = "gun3"
    db.yaz("UPDATE specimen SET durum=? WHERE id=?", (onceki, specimen_id))
    # Transfer gidince FET'in günü değişebilir (v6.144).
    h = db.tek("SELECT hasta_id FROM cycle WHERE id=?", (hedef_cycle,))
    tedavi_sirasini_duzelt(h and h["hasta_id"], kid)
    return RedirectResponse(f"/cycle/{hedef_cycle}/transfer", status_code=303)


# ----------------------------------------------------------------- snapshot alma

def bekleyen_ozet():
    """Snapshot klasöründe bekleyen kareler — en yenisi başta."""
    b = goruntuler.bekleyen_dosyalar()
    return {"adet": len(b), "son": b[-1] if b else None}


@uygulama.post("/specimen/{specimen_id}/snapshot-al")
async def snapshot_al(request: Request, specimen_id: str):
    f = dict(await request.form())
    asama = f.get("asama") or "diger"
    geri = f.get("geri") or "/hastalar"
    hepsi = f.get("hepsi") == "1"

    sp = db.tek("SELECT s.*, c.cycle_no FROM specimen s "
                "JOIN cycle c ON c.id=s.cycle_id WHERE s.id=?", (specimen_id,))
    if not sp:
        return RedirectResponse(geri, status_code=303)

    kid = request.state.kullanici["id"]
    bekleyen = goruntuler.bekleyen_dosyalar()
    if not bekleyen:
        return RedirectResponse(geri, status_code=303)

    alinacak = bekleyen if hepsi else [bekleyen[-1]]
    for d in alinacak:
        goruntuler.goruntu_bagla(d["imza"], sp["cycle_id"], sp["cycle_no"],
                                 specimen_id, asama, kid)
    return RedirectResponse(geri, status_code=303)


@uygulama.get("/cycle/{cycle_id}/arsiv-sil")
def arsiv_sil_ekran(request: Request, cycle_id: int):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id=c.hasta_id WHERE c.id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)
    arsiv = db.sorgu(
        "SELECT id, asama, zaman, orijinal_dosya_adi, kaynak FROM goruntu "
        "WHERE cycle_id=? AND specimen_id IS NULL ORDER BY id", (cycle_id,))
    etiketler = {r["kod"]: r["etiket"] for r in db.sorgu(
        "SELECT kod, etiket FROM liste_degeri WHERE lab_id=?", (db.LAB_ID,))}
    return sablon.TemplateResponse(
        request, "arsiv_sil.html",
        {"c": c, "arsiv": arsiv, "etiketler": etiketler})


@uygulama.post("/cycle/{cycle_id}/arsiv-sil")
async def arsiv_sil(request: Request, cycle_id: int):
    f = dict(await request.form())
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    arsiv = db.sorgu("SELECT id FROM goruntu WHERE cycle_id=? AND specimen_id IS NULL",
                     (cycle_id,))
    if (f.get("onay") or "").strip() != str(len(arsiv)):
        return RedirectResponse(f"/cycle/{cycle_id}/arsiv-sil?hata=1", status_code=303)

    kid = request.state.kullanici["id"]
    for g in arsiv:
        tam = db.tek("SELECT * FROM goruntu WHERE id=?", (g["id"],))
        guvenlik.degisiklikleri_yaz(
            "goruntu", g["id"], tam,
            {"durum": f"SILINDI (cycle arsivi, {tam['orijinal_dosya_adi']})"}, kid)
        goruntuler.goruntu_sil(g["id"])
    return RedirectResponse(f"/cycle/{cycle_id}", status_code=303)


# ----------------------------------------------------------------- kalıcı silme

def cycle_transfer_kayitlari(cycle_id: int):
    """Bu cycle'ı transfere bağlayan kayıtlar.

    İki yönü var: bu cycle'ın embriyoları transfer edilmiş olabilir, ya da
    bu cycle bir FET olarak başka cycle'ın embriyolarının transfer edildiği
    cycle olabilir. İkisi de silmeyi engeller.
    """
    return db.sorgu(
        "SELECT o.id, o.zaman, o.tr_tipi, s.cycle_sira_no, s.cycle_id, "
        "  c.cycle_no AS kaynak_cycle, tc.cycle_no AS transfer_cycle "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c ON c.id=s.cycle_id "
        "LEFT JOIN cycle tc ON tc.id=o.tr_cycle_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 "
        "AND (s.cycle_id=? OR o.tr_cycle_id=?) "
        "ORDER BY o.zaman", (cycle_id, cycle_id))


def hasta_transfer_kayitlari(hasta_id: int):
    return db.sorgu(
        "SELECT o.id, o.zaman, s.cycle_sira_no, c.cycle_no AS kaynak_cycle, "
        "  tc.cycle_no AS transfer_cycle "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c ON c.id=s.cycle_id "
        "LEFT JOIN cycle tc ON tc.id=o.tr_cycle_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 AND c.hasta_id=? "
        "ORDER BY o.zaman", (hasta_id,))


def cycle_icerik_sayilari(cycle_id: int):
    return db.tek(
        "SELECT (SELECT COUNT(*) FROM specimen WHERE cycle_id=?) AS oosit, "
        "  (SELECT COUNT(*) FROM olay WHERE cycle_id=?) AS olay, "
        "  (SELECT COUNT(*) FROM goruntu WHERE cycle_id=?) AS goruntu, "
        "  (SELECT COUNT(*) FROM specimen_bulgu WHERE specimen_id IN "
        "     (SELECT id FROM specimen WHERE cycle_id=?)) AS bulgu, "
        "  (SELECT COUNT(*) FROM sperm_ornek WHERE cycle_id=?) AS sperm, "
        "  (SELECT COUNT(*) FROM gebelik_sonucu WHERE cycle_id=?) AS gebelik, "
        "  (SELECT COUNT(*) FROM pgt_sonuc WHERE specimen_id IN "
        "     (SELECT id FROM specimen WHERE cycle_id=?)) AS pgt, "
        "  (SELECT COUNT(DISTINCT o.vit_tasiyici_id) FROM olay o "
        "     JOIN specimen s ON s.id=o.specimen_id "
        "     WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.vit_tasiyici_id IS NOT NULL) "
        "   AS tasiyici",
        (cycle_id,) * 8)


def cycle_tamamen_sil(cycle_id: int, kullanici_id: int):
    """Cycle'ı ve ona bağlı her şeyi kalıcı olarak siler."""
    specimenler = [r["id"] for r in db.sorgu(
        "SELECT id FROM specimen WHERE cycle_id=?", (cycle_id,))]

    # 1. Görüntüler (arşiv dosyaları dahil)
    for g in db.sorgu("SELECT id FROM goruntu WHERE cycle_id=?", (cycle_id,)):
        goruntuler.goruntu_sil(g["id"])
    for sid in specimenler:
        for g in db.sorgu("SELECT id FROM goruntu WHERE specimen_id=?", (sid,)):
            goruntuler.goruntu_sil(g["id"])

    # 2. Başka cycle'lardan bu cycle'a yapılmış transferleri serbest bırak
    db.yaz("UPDATE olay SET tr_cycle_id=NULL, iptal_mi=1, "
           "iptal_sebep='Transfer tedavisi silindi' "
           "WHERE tr_cycle_id=? AND cycle_id<>?", (cycle_id, cycle_id))
    # Aynısı çözme için: bu cycle'a yapılmış ama embriyosu başka cycle'dan olan
    # çözmelerin bağı kopar (kayıt kalır, hangi tedavi için olduğu bilinmez)
    db.yaz("UPDATE olay SET thaw_cycle_id=NULL "
           "WHERE thaw_cycle_id=? AND cycle_id<>?", (cycle_id, cycle_id))
    # Aynısı yeniden dondurma için (v6.143, tuzak #4): bu FET'te yeniden
    # dondurulan başka bir tedavinin embriyosu. Kayıt kalır -- tüp tankta
    # duruyor, silmek onu haritadan düşürürdü -- yalnızca hangi tedavide
    # dondurulduğu bilinmez olur (boş = kendi tedavisi).
    if db.kolon_var("olay", "vit_cycle_id"):
        db.yaz("UPDATE olay SET vit_cycle_id=NULL "
               "WHERE vit_cycle_id=? AND cycle_id<>?", (cycle_id, cycle_id))

    # Başka bir hastaya (eşe) ait, bu tedaviye bağlanmış dondurulmuş sperm
    # varsa bağı kopar (v6.86, tuzak #4'ün aynısı: yeni bir cycle_id alanı
    # eklendi, kalıcı silmede temizlenmesi şart) -- kayıt kalır, taşıyıcı
    # tekrar 'dolu' olur, sahibi hastanın dolabında kalmaya devam eder.
    for r in db.sorgu(
            "SELECT id, tasiyici_id FROM sperm_dondurma WHERE kullanim_cycle_id=?",
            (cycle_id,)):
        db.yaz("UPDATE sperm_dondurma SET kullanim_cycle_id=NULL WHERE id=?",
               (r["id"],))
        db.yaz("UPDATE tasiyici SET durum='dolu' WHERE id=?", (r["tasiyici_id"],))

    # 3. Bu cycle'ın embriyolarının kullandığı taşıyıcılar
    tasiyicilar = [r["vit_tasiyici_id"] for r in db.sorgu(
        "SELECT DISTINCT o.vit_tasiyici_id FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' "
        "AND o.vit_tasiyici_id IS NOT NULL", (cycle_id,))]

    # 4. Bağlı kayıtlar
    if specimenler:
        isaret = ",".join("?" * len(specimenler))
        db.yaz(f"DELETE FROM specimen_bulgu WHERE specimen_id IN ({isaret})", specimenler)
        db.yaz(f"DELETE FROM pgt_sonuc WHERE specimen_id IN ({isaret})", specimenler)
        db.yaz(f"DELETE FROM olay WHERE specimen_id IN ({isaret})", specimenler)
    db.yaz("DELETE FROM olay WHERE cycle_id=?", (cycle_id,))
    # Kuyruk isaretleri: "atla" denen kareler goruntuye bagli degil, cycle'a bagli
    db.yaz("DELETE FROM kaynak_dosya WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM beta_hcg WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM dogan_bebek WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM gebelik_sonucu WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM sperm_analiz WHERE sperm_ornek_id IN "
           "(SELECT id FROM sperm_ornek WHERE cycle_id=?)", (cycle_id,))
    db.yaz("DELETE FROM sperm_ornek WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM islem_yapan WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM specimen WHERE cycle_id=?", (cycle_id,))
    db.yaz("DELETE FROM cycle WHERE id=?", (cycle_id,))

    # 5. Boşalan taşıyıcıları ve konumları serbest bırak
    for tid in tasiyicilar:
        kalan = db.tek("SELECT COUNT(*) k FROM olay WHERE vit_tasiyici_id=?",
                       (tid,))["k"]
        if kalan == 0:
            t = db.tek("SELECT konum_id FROM tasiyici WHERE id=?", (tid,))
            # Çözme kaydı tüpü `thaw_tasiyici_id` ile gösteriyor (v6.143,
            # FK). O çözmeler aynı örneğin kayıtları ve 4. adımda silindi;
            # yine de tüpe işaret eden kalırsa silme FOREIGN KEY ile patlardı.
            if db.cozme_tupu_var():
                db.yaz("UPDATE olay SET thaw_tasiyici_id=NULL "
                       "WHERE thaw_tasiyici_id=?", (tid,))
            db.yaz("DELETE FROM tasiyici WHERE id=?", (tid,))
            if t and t["konum_id"]:
                db.yaz("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))


def silme_logla(tablo, kayit_id, ozet, kullanici_id):
    from datetime import datetime as _d
    db.yaz("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
           "eski_deger, yeni_deger, kullanici_id, zaman) "
           "VALUES (?,?,?,'KALICI_SILME',?,'silindi',?,?)",
           (db.LAB_ID, tablo, str(kayit_id), ozet, kullanici_id,
            _d.now().isoformat(" ", "seconds")))


@uygulama.post("/cycle/{cycle_id}/denudasyon-zaman")
async def denudasyon_zaman(request: Request, cycle_id: int):
    f = dict(await request.form())
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if c:
        yeni = zaman(f.get("denudasyon_zamani"))
        guvenlik.degisiklikleri_yaz("cycle", cycle_id, c,
                                    {"denudasyon_zamani": yeni},
                                    request.state.kullanici["id"])
        db.yaz("UPDATE cycle SET denudasyon_zamani=? WHERE id=?", (yeni, cycle_id))
    return RedirectResponse(f"/cycle/{cycle_id}/denudasyon", status_code=303)


# ----------------------------------------------------------------------- OPU

def opu_hekim_var() -> bool:
    """`goc_025` çalıştırıldı mı — `cycle.opu_hekim` kolonu var mı.

    Göç çalıştırılmadan ekran 500 vermesin diye (tuzak #3). Bir kez
    bakılıp `db.kolon_var()`'da saklanıyor; yedekten geri yüklemeden sonra
    unutuluyor (v6.145, tuzak #15).
    """
    return db.kolon_var("cycle", "opu_hekim")


@uygulama.get("/cycle/{cycle_id}/opu")
def opu_ekran(request: Request, cycle_id: int, hata: str = "",
              duzenle: int = 0):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id=c.hasta_id WHERE c.id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    return sablon.TemplateResponse(
        request, "opu.html",
        {"c": c, "hata": hata, "duzenle": duzenle,
         "goc_gerekli": not opu_hekim_var(),
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
         "gezinme": asama_gezinme(cycle_id, "opu")})


@uygulama.post("/cycle/{cycle_id}/opu")
async def opu_kaydet(request: Request, cycle_id: int):
    from urllib.parse import quote
    f = dict(await request.form())
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    try:
        yeni = {
            "opu_zamani": zaman(f.get("opu_zamani"), "OPU zamanı"),
            "opu_sag_oosit": tam(f.get("opu_sag_oosit"), "Sağ over yumurta sayısı"),
            "opu_sol_oosit": tam(f.get("opu_sol_oosit"), "Sol over yumurta sayısı"),
        }
    except FormHatasi as e:
        return RedirectResponse(
            f"/cycle/{cycle_id}/opu?duzenle=1&hata={quote(str(e))}",
            status_code=303)

    # Hekim adı yalnızca göç çalıştıysa yazılır; yoksa ekranda uyarı görünür.
    if opu_hekim_var():
        yeni["opu_hekim"] = bos_ise_none(f.get("opu_hekim"))

    guvenlik.degisiklikleri_yaz("cycle", cycle_id, c, yeni,
                                request.state.kullanici["id"])
    kolonlar = ", ".join(f"{k}=?" for k in yeni)
    db.yaz(f"UPDATE cycle SET {kolonlar} WHERE id=?",
           (*yeni.values(), cycle_id))
    # OPU günü tedavinin günü: eski bir tedavinin OPU'su girildiyse numara
    # tarih sırasına göre kayar (v6.144).
    tedavi_sirasini_duzelt(c["hasta_id"], request.state.kullanici["id"])
    return RedirectResponse(f"/cycle/{cycle_id}/opu", status_code=303)


# ----------------------------------------------------------------- aşama gezinme

ASAMA_SIRASI = [
    ("opu", "OPU", "/cycle/{id}/opu"),
    ("androloji", "Androloji", "/cycle/{id}/androloji"),
    ("denudasyon", "Denüdasyon", "/cycle/{id}/denudasyon"),
    ("icsi", "ICSI", "/cycle/{id}/icsi"),
    ("fert", "Fertilizasyon", "/cycle/{id}/fert"),
    ("cleavage", "Cleavage", "/cycle/{id}/cleavage?gun=2"),
    ("blast", "Blastokist", "/cycle/{id}/blast?gun=5"),
    ("vitrifikasyon", "Vitrifikasyon", "/cycle/{id}/vitrifikasyon"),
    ("thaw", "Çözme", "/cycle/{id}/thaw"),
    ("transfer", "Transfer", "/cycle/{id}/transfer"),
    ("gebelik", "Gebelik sonucu", "/cycle/{id}/gebelik"),
]


# Tedavi tipine göre aşamalar, gösterim sırasıyla. Sözlük v6.147'den beri
# `db.py`'de (`formlar.py` ve `disari.py` de soruyor, `app`'i import
# edemezler -- `FET_TIPLERI`'nin aynı gerekçesi); her tipin gerekçesi orada.
TIP_ASAMALARI = db.TIP_ASAMALARI


def cycle_asamalari(cycle_tipi: str):
    """Bu tedavi tipinde **ve bu kullanıcının izninde** olan aşamalar.

    Gezinme çubuğu ve cycle detaydaki düğmeler buradan besleniyor; süzme tek
    yerde olunca ikisi birden doğru davranıyor. İzni olmayan bir aşama listeden
    çıkar, "3/8" sayacı da kullanıcının kendi adımlarını sayar (v6.14).

    Gösterim sırası **buradaki listenin kendi sırası** (v6.62) —
    `ASAMA_SIRASI`'nın sırası değil. İkisi ivf_icsi/fet/oosit_cryo'da zaten
    aynıydı; fet_kultur'da farklı: thaw blast'tan ÖNCE gelmeli (embriyo
    ÖNCE çözülüyor, SONRA gün 5'e kültürleniyor), ama ASAMA_SIRASI'nda blast
    dondurmadan önce durur (ivf_icsi akışında blast önce, sonra dondurma).
    """
    kodlar = TIP_ASAMALARI.get(cycle_tipi, TIP_ASAMALARI["ivf_icsi"])
    sozluk = {a[0]: a for a in ASAMA_SIRASI}
    return [sozluk[k] for k in kodlar if k in sozluk and yetkim(k)]


def cycle_ozet(cycle: dict, kodlar: set) -> list:
    """Tedavi ekranının en üstündeki tek özet kutusu — türetilmiş, saklanmaz
    (v6.110, kullanıcının isteği: "Oositler listesini kaldır, kısa bir
    özet olsun: kaç yumurta, M2, döllenen, cleavage, blastokist"; v6.112'de
    genişletildi — kullanıcı eskiden ayrı duran Folikül/Toplanan kutusuyla
    bu özeti **tek** kutuda istedi: "Folikül Sayısı, Toplanan Yumurta
    Sayısı, M2 (Olgun) Yumurta Sayısı, Döllenen Yumurta (2PN) Sayısı,
    Cleavage Sayısı, Blastokist Sayısı").

    `disari.istatistikler()`'deki lab-geneli `_olay()` sayımının tek-cycle
    hali — aynı "sayaç tutma, ekrana her açılışta türet" gerekçesi (v6.38):
    ayrı bir sayı sütunu tutmak, bir kayıt silinince ya da düzeltilince
    özetin gerçek veriden ayrı düşmesi demek olurdu. `kodlar` çağıranın
    zaten hesapladığı `cycle_asamalari()` sonucudur (kullanıcının modül
    izniyle de süzülmüş) — burada tekrar hesaplanmıyor.

    **Toplanan yumurta OPU'da elle girilen sayıdır** (`opu_sag_oosit` +
    `opu_sol_oosit`), specimen kaydı sayısı değil — v6.110'da yanlışlıkla
    specimen `COUNT(*)`'ı kullanılmıştı (eskiden ayrı duran "Kayıtlı"
    kutusunun sayısıyla aynı şeydi, üstteki kutunun "Toplanan Oosit"'inden
    FARKLI bir anlam taşıyordu — iki kutu birleşince bu tutarsızlık ortaya
    çıkardı). Tek kutuda tek "Toplanan" olacağı için OPU'nun kendi sayısı
    kazandı: klinik olarak "kaç yumurta alındı" sorusunun cevabı o, oositin
    ne zaman ayrı bir kayda (specimen) döküldüğünden bağımsız.

    Yalnızca bu cycle tipinde **gerçekten var olan** aşamalar için bir satır
    döner (Folikül hariç — o her tipte cycle seviyesinde girilebiliyor,
    `opu.html`'de de koşulsuz basılıyor): `fet` gibi OPU/ICSI'siz bir tipte
    "0 M2" basmak yanlış bilgi verir (hiç ölçülmedi, sıfır değil) — bu
    yüzden "0" değil, satır hiç yok.
    """
    # Bu tedavide YAPILAN işlemler (v6.146): FET (3→5 kültür)'te çözülen
    # embriyonun blastokisti FET'in sayısı, kaynak ICSI'ninki değil -- aynı
    # sayfadaki zaman çizelgesiyle aynı koşul (`db.tedavide_yapilan()`).
    bu_tedavide, p = db.tedavide_yapilan(cycle["id"])

    def _olay(tip, ek=""):
        return db.tek(
            "SELECT COUNT(DISTINCT o.specimen_id) n FROM olay o "
            f"WHERE o.tip = ? AND o.iptal_mi = 0 {ek} AND {bu_tedavide}",
            (tip, *p),
        )["n"]

    satirlar = [{
        "anahtar": "ozet_folikul",
        "sayi": cycle["folikul_sayisi"] if cycle["folikul_sayisi"] is not None else "—",
    }]
    if "opu" in kodlar:
        sag, sol = cycle["opu_sag_oosit"], cycle["opu_sol_oosit"]
        satir = {"anahtar": "ozet_toplanan", "sayi": (sag or 0) + (sol or 0)}
        if sag is not None or sol is not None:
            satir["kirilim"] = (
                f'{metinler.t("sag")} {sag or 0} · {metinler.t("sol")} {sol or 0}'
            )
        satirlar.append(satir)
    # Yumurta Çözme (v6.147): yumurta toplanmıyor, çözülüyor -- "Toplanan"ın
    # yerinde çözülen yumurta sayısı, kırılımında kaçının canlı çıktığı.
    if db.cozulen_yumurta_islenir(cycle["cycle_tipi"]) and "thaw" in kodlar:
        cozulen = db.sorgu(
            "SELECT o.specimen_id, MAX(CASE WHEN o.thaw_sagkalim = 'canli' "
            "THEN 1 ELSE 0 END) canli FROM olay o WHERE o.tip = 'thaw' "
            "AND o.iptal_mi = 0 AND o.thaw_cycle_id = ? GROUP BY o.specimen_id",
            (cycle["id"],)) if thaw_cycle_var() else []
        satirlar.append({
            "anahtar": "ozet_cozulen", "sayi": len(cozulen),
            "kirilim": f'{metinler.t("canli")} {sum(r["canli"] for r in cozulen)}'
            if cozulen else None})
    # oosit_cryo'da maturasyon denüdasyonda, ivf_icsi'de ICSI ekranında
    # soruluyor (v6.96) ama ikisi de aynı olay.tip='maturasyon_kontrolu'yu
    # yazıyor — "denudasyon" aşaması ikisinde de var. Yumurta Çözme'de
    # denüdasyon yok, ICSI ekranı var (v6.147); sayılan yine BU tedavide
    # yapılan maturasyon (`bu_tedavide`), kaynağın denüdasyonundaki değil.
    if "denudasyon" in kodlar or "icsi" in kodlar:
        satirlar.append({
            "anahtar": "ozet_m2",
            "sayi": _olay("maturasyon_kontrolu", "AND o.mat_deger='mii'"),
        })
    if "fert" in kodlar:
        satirlar.append({
            "anahtar": "ozet_dollenen",
            "sayi": _olay("fertilizasyon_kontrolu", "AND o.fert_pn_sayisi='2'"),
        })
    if "cleavage" in kodlar:
        satirlar.append({"anahtar": "ozet_cleavage", "sayi": _olay("cleavage_degerlendirme")})
    if "blast" in kodlar:
        satirlar.append({"anahtar": "ozet_blastokist", "sayi": _olay("blastokist_degerlendirme")})
    return satirlar


def asama_gezinme(cycle_id: int, anahtar: str):
    """Bir aşama ekranının gezinme verisi: önceki/sonraki **ve tüm liste**.

    `liste` yan menüyü besliyor (geniş ekranda solda duran aşama menüsü).
    Aynı yerden geldiği için menü de, alttaki çubuk da tedavi tipine ve
    kullanıcının modül izinlerine göre süzülmüş oluyor.
    """
    c = db.tek("SELECT cycle_tipi FROM cycle WHERE id=?", (cycle_id,))
    liste = cycle_asamalari(c["cycle_tipi"] if c else "ivf_icsi")
    kodlar = [a[0] for a in liste]
    tumu = [{"kod": k, "ad": asama_adi(k), "yol": yol.format(id=cycle_id),
             "aktif": k == anahtar}
            for k, _ad, yol in liste]
    if anahtar not in kodlar:
        return {"onceki": None, "sonraki": None, "sira": None,
                "toplam": len(kodlar), "liste": tumu}
    i = kodlar.index(anahtar)
    def yap(j):
        if 0 <= j < len(liste):
            k, ad, yol = liste[j]
            return {"ad": asama_adi(k), "yol": yol.format(id=cycle_id)}
        return None
    return {"onceki": yap(i - 1), "sonraki": yap(i + 1),
            "sira": i + 1, "toplam": len(liste), "liste": tumu}


# ----------------------------------------------------------------- toplu eşleştirme

@uygulama.get("/cycle/{cycle_id}/esle")
def esle_ekran(request: Request, cycle_id: int, asama: str = "icsi", hedef: str = ""):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id=c.hasta_id WHERE c.id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    oositler = db.sorgu(
        "SELECT s.id, s.cycle_sira_no, s.taraf, "
        "  (SELECT COUNT(*) FROM goruntu g WHERE g.specimen_id=s.id AND g.asama=?) "
        "  AS asama_kare, "
        "  (SELECT g.id FROM goruntu g WHERE g.specimen_id=s.id AND g.asama=? "
        "   ORDER BY g.id DESC LIMIT 1) AS goruntu "
        "FROM specimen s WHERE s.cycle_id=? ORDER BY s.cycle_sira_no",
        (asama, asama, cycle_id))

    bekleyen = goruntuler.bekleyen_dosyalar()
    asamalar = db.liste("goruntu_asama")
    etiket = next((a["etiket"] for a in asamalar if a["kod"] == asama), asama)

    # Hedef oosit: istenen, yoksa bu aşamada fotoğrafı olmayan ilk oosit
    sp = None
    if hedef:
        sp = next((o for o in oositler if str(o["cycle_sira_no"]) == hedef), None)
    if sp is None:
        sp = next((o for o in oositler if o["asama_kare"] == 0), None)
    if sp is None and oositler:
        sp = oositler[0]

    return sablon.TemplateResponse(
        request, "esle.html",
        {"c": c, "asama": asama, "asama_etiket": etiket, "asamalar": asamalar,
         "oositler": oositler, "sp": sp,
         "simdiki": bekleyen[0] if bekleyen else None,
         "bekleyen_adet": len(bekleyen),
         "gezinme": None})


@uygulama.post("/cycle/{cycle_id}/esle")
async def esle_islem(request: Request, cycle_id: int):
    f = dict(await request.form())
    asama = f.get("asama") or "icsi"
    eylem = f.get("eylem")
    im = f.get("imza") or ""
    kid = request.state.kullanici["id"]
    c = db.tek("SELECT id, cycle_no FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    hedef_sira = ""
    if eylem == "ata":
        sid = f.get("specimen_id")
        sp = db.tek("SELECT * FROM specimen WHERE id=? AND cycle_id=?", (sid, cycle_id))
        if sp:
            goruntuler.goruntu_bagla(im, cycle_id, c["cycle_no"], sid, asama, kid)
            sonraki = db.tek(
                "SELECT cycle_sira_no n FROM specimen WHERE cycle_id=? "
                "AND cycle_sira_no > ? ORDER BY cycle_sira_no LIMIT 1",
                (cycle_id, sp["cycle_sira_no"]))
            hedef_sira = str(sonraki["n"]) if sonraki else str(sp["cycle_sira_no"])
    elif eylem == "atla":
        goruntuler.atla(im, cycle_id)
        hedef_sira = f.get("hedef") or ""

    yol = f"/cycle/{cycle_id}/esle?asama={asama}"
    if hedef_sira:
        yol += f"&hedef={hedef_sira}"
    return RedirectResponse(yol, status_code=303)


@uygulama.post("/specimen/{specimen_id}/taraf")
async def specimen_taraf(request: Request, specimen_id: str):
    f = dict(await request.form())
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)
    yeni = f.get("taraf") or None
    if yeni not in ("sag", "sol", None):
        yeni = None
    guvenlik.degisiklikleri_yaz("specimen", specimen_id, sp, {"taraf": yeni},
                                request.state.kullanici["id"])
    db.yaz("UPDATE specimen SET taraf=? WHERE id=?", (yeni, specimen_id))
    return RedirectResponse(f.get("geri") or f"/cycle/{sp['cycle_id']}", status_code=303)


@uygulama.post("/specimen/{specimen_id}/oosit-degerlendirme")
async def oosit_degerlendirme_kaydet(request: Request, specimen_id: str):
    """Yumurta Dondurma'da (oosit_cryo) dondurmadan önce maturasyon/bulgu.

    ICSI ekranındaki `maturasyon_kontrolu` olayı ve `specimen_bulgu` ile
    aynı mekanizma -- yalnızca `asama='denudasyon'` ile ayrılıyor ki ICSI'nin
    kendi bulgularıyla karışmasın (bu ekran zaten yalnızca oosit_cryo'da
    kullanılıyor, ivf_icsi'de aynı soru ICSI ekranında soruluyor).
    """
    f = await request.form()
    sp = db.tek("SELECT * FROM specimen WHERE id=?", (specimen_id,))
    if not sp:
        return RedirectResponse("/hastalar", status_code=303)

    kid = request.state.kullanici["id"]
    simdi = islem_zamani(f.get("islem_zamani"))

    mat = f.get("mat_deger") or None
    if mat:
        olay_kaydet_veya_guncelle(
            specimen_id, sp["cycle_id"], "maturasyon_kontrolu",
            {"mat_deger": mat}, kid, simdi,
        )

    yeni_bulgular = set(f.getlist("bulgu"))
    eski_bulgular = {r["bulgu_kodu"] for r in db.sorgu(
        "SELECT bulgu_kodu FROM specimen_bulgu WHERE specimen_id=? AND asama='denudasyon'",
        (specimen_id,))}
    if yeni_bulgular != eski_bulgular:
        guvenlik.degisiklikleri_yaz(
            "specimen_bulgu", specimen_id,
            {"bulgu": ", ".join(sorted(eski_bulgular))},
            {"bulgu": ", ".join(sorted(yeni_bulgular))}, kid,
        )
        db.yaz("DELETE FROM specimen_bulgu WHERE specimen_id=? AND asama='denudasyon'",
               (specimen_id,))
        for b in sorted(yeni_bulgular):
            db.yaz("INSERT INTO specimen_bulgu (specimen_id, asama, bulgu_kodu, "
                   "zaman, kullanici_id) VALUES (?,'denudasyon',?,?,?)",
                   (specimen_id, b, simdi, kid))

    return RedirectResponse(f.get("geri") or f"/cycle/{sp['cycle_id']}/denudasyon",
                            status_code=303)


# ----------------------------------------------------------------- gebelik sonucu

@uygulama.get("/cycle/{cycle_id}/gebelik")
def gebelik_ekran(request: Request, cycle_id: int, hata: str = ""):
    c = db.tek("SELECT c.*, h.dosya_no, h.ad_soyad FROM cycle c "
               "JOIN hasta h ON h.id=c.hasta_id WHERE c.id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    from datetime import datetime as _d
    kayit = db.tek("SELECT * FROM gebelik_sonucu WHERE cycle_id=?", (cycle_id,))
    betalar = db.sorgu("SELECT * FROM beta_hcg WHERE cycle_id=? ORDER BY zaman, id",
                       (cycle_id,))
    bebekler = db.sorgu("SELECT * FROM dogan_bebek WHERE cycle_id=? ORDER BY sira",
                        (cycle_id,))
    bebek_kayitli = {b["sira"]: b for b in bebekler}
    # Bebek sayısı henüz girilmemişse bile en az 1 satır gösterilsin --
    # çoğu doğum tekil, kullanıcı önce "Bebek sayısı"nı doldurmak zorunda kalmasın.
    bebek_siralari = range(1, max(kayit["bebek_sayisi"] if kayit and kayit["bebek_sayisi"] else 1,
                                  max(bebek_kayitli, default=0)) + 1)

    transferler = db.sorgu(
        "SELECT s.cycle_sira_no, s.id, o.zaman, o.tr_tipi, c2.cycle_no AS kaynak, "
        "  (SELECT b.bl_skor FROM olay b WHERE b.specimen_id=s.id "
        "   AND b.tip='blastokist_degerlendirme' AND b.iptal_mi=0 "
        "   ORDER BY b.gun DESC LIMIT 1) AS skor "
        "FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "JOIN cycle c2 ON c2.id=s.cycle_id "
        "WHERE o.tip='transfer' AND o.iptal_mi=0 AND o.tr_cycle_id=? "
        "ORDER BY s.cycle_sira_no", (cycle_id,))

    # Beta artış hızı (ardışık ikisi arası)
    artis = []
    for i in range(1, len(betalar)):
        onceki, simdi = betalar[i - 1], betalar[i]
        try:
            t1 = _d.fromisoformat(onceki["zaman"])
            t2 = _d.fromisoformat(simdi["zaman"])
            saat = (t2 - t1).total_seconds() / 3600
            if saat > 0 and onceki["deger"] > 0:
                kat = simdi["deger"] / onceki["deger"]
                artis.append({"i": i, "saat": round(saat, 1), "kat": round(kat, 2)})
        except (ValueError, TypeError, ZeroDivisionError):
            pass

    return sablon.TemplateResponse(
        request, "gebelik.html",
        {"c": c, "k": kayit, "betalar": betalar, "artis": artis,
         "transferler": transferler, "hata": hata,
         "sonlanmalar": db.liste("sonlanma"),
         "bebek_siralari": bebek_siralari, "bebek_kayitli": bebek_kayitli,
         "simdi": _d.now().strftime("%Y-%m-%dT%H:%M"),
         "gezinme": asama_gezinme(cycle_id, "gebelik")})


@uygulama.post("/cycle/{cycle_id}/gebelik")
async def gebelik_kaydet(request: Request, cycle_id: int):
    from urllib.parse import quote
    f = dict(await request.form())
    c = db.tek("SELECT * FROM cycle WHERE id=?", (cycle_id,))
    if not c:
        return RedirectResponse("/hastalar", status_code=303)

    def hata(m):
        return RedirectResponse(f"/cycle/{cycle_id}/gebelik?hata={quote(m)}",
                                status_code=303)

    kid = request.state.kullanici["id"]
    from datetime import datetime as _d

    # --- beta hCG ekleme / silme ---
    if f.get("eylem") == "beta_ekle":
        try:
            deger = sayi(f.get("beta_deger"), "Beta hCG")
        except FormHatasi as e:
            return hata(str(e))
        if deger is None:
            return hata("Beta hCG değeri girilmeli.")
        z = zaman(f.get("beta_zaman")) or _d.now().isoformat(" ", "seconds")
        db.yaz("INSERT INTO beta_hcg (cycle_id, zaman, deger) VALUES (?,?,?)",
               (cycle_id, z, deger))
        return RedirectResponse(f"/cycle/{cycle_id}/gebelik", status_code=303)

    if f.get("eylem") == "beta_sil":
        db.yaz("DELETE FROM beta_hcg WHERE id=? AND cycle_id=?",
               (f.get("beta_id"), cycle_id))
        return RedirectResponse(f"/cycle/{cycle_id}/gebelik", status_code=303)

    # --- ana sonuç ---
    try:
        kese = tam(f.get("gebelik_kesesi_sayisi"), "Gebelik kesesi sayısı")
        bebek = tam(f.get("bebek_sayisi"), "Bebek sayısı")
        hafta = tam(f.get("dogum_haftasi"), "Doğum haftası")
    except FormHatasi as e:
        return hata(str(e))

    yeni = {
        "klinik_gebelik": bos_ise_none(f.get("klinik_gebelik")),
        "gebelik_kesesi_sayisi": kese,
        "fk_pozitif": bos_ise_none(f.get("fk_pozitif")),
        "fk_kontrol_zamani": zaman(f.get("fk_kontrol_zamani")),
        "sonlanma": bos_ise_none(f.get("sonlanma")),
        "dogum_zamani": zaman(f.get("dogum_zamani")),
        "bebek_sayisi": bebek,
        "dogum_haftasi": hafta,
        "guncelleme_zamani": _d.now().isoformat(" ", "seconds"),
    }

    mevcut = db.tek("SELECT * FROM gebelik_sonucu WHERE cycle_id=?", (cycle_id,))
    if mevcut:
        guvenlik.degisiklikleri_yaz("gebelik_sonucu", mevcut["id"], mevcut, yeni, kid)
        db.yaz("UPDATE gebelik_sonucu SET " +
               ", ".join(f"{a}=?" for a in yeni) + " WHERE cycle_id=?",
               (*yeni.values(), cycle_id))
    else:
        db.yaz("INSERT INTO gebelik_sonucu (lab_id, cycle_id, " +
               ", ".join(yeni) + ") VALUES (?,?," +
               ", ".join("?" * len(yeni)) + ")",
               (db.LAB_ID, cycle_id, *yeni.values()))
    return RedirectResponse(f"/cycle/{cycle_id}/gebelik", status_code=303)


@uygulama.post("/cycle/{cycle_id}/gebelik/bebek")
async def gebelik_bebek_kaydet(request: Request, cycle_id: int):
    """Doğan bebeklerden birinin cinsiyeti/kilosu — bebek sayısı kadar,
    ayrı satır (kullanıcının isteği: ikiz/üçüzde her bebek kendi kaydı).
    `beta_hcg` gibi doğrudan cycle_id'ye bağlı, `gebelik_sonucu`'na değil.
    """
    from urllib.parse import quote
    f = await request.form()

    def hata(m):
        return RedirectResponse(f"/cycle/{cycle_id}/gebelik?hata={quote(m)}",
                                status_code=303)

    try:
        sira = tam(f.get("sira"), "Sıra")
        kilo = sayi(f.get("kilo_kg"), "Kilo")
    except FormHatasi as e:
        return hata(str(e))
    if not sira:
        return RedirectResponse(f"/cycle/{cycle_id}/gebelik", status_code=303)

    cinsiyet = f.get("cinsiyet") or None
    if cinsiyet not in ("kiz", "erkek", None):
        cinsiyet = None

    mevcut = db.tek("SELECT id FROM dogan_bebek WHERE cycle_id=? AND sira=?",
                    (cycle_id, sira))
    if mevcut:
        db.yaz("UPDATE dogan_bebek SET cinsiyet=?, kilo_kg=? WHERE id=?",
               (cinsiyet, kilo, mevcut["id"]))
    else:
        db.yaz("INSERT INTO dogan_bebek (lab_id, cycle_id, sira, cinsiyet, kilo_kg) "
               "VALUES (?,?,?,?,?)", (db.LAB_ID, cycle_id, sira, cinsiyet, kilo))
    return RedirectResponse(f"/cycle/{cycle_id}/gebelik", status_code=303)
