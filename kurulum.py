# -*- coding: utf-8 -*-
"""İlk kurulum: veritabanı olmayan bilgisayar (v6.204).

Kurulum dosyasıyla (installer) yüklenen program, yeni bir bilgisayarda
veritabanı olmadan açılıyor. v6.50'den beri `baslat.py` "önce kurulumu
tamamlayın (sifirdan_kur.py)" deyip duruyordu; kurulum dosyasında terminal
yok. Program artık ilk kurulum ekranıyla açılıyor (`/kurulum`, yalnızca bu
bilgisayardan) ve iki yol sunuyor -- ikisi de bu modülde:

- `yeni_laboratuvar()`: şema, seçim listeleri, varsayılan ayarlar, ilk
  YÖNETİCİ hesabı, göçler. `sifirdan_kur.py` (terminal) de listeleri ve
  ayarları buradan alıyor.
- `veri_al()`: eski bilgisayardan gelen veritabanı -- `tasi.py disari`'nın
  USB klasörü, eski programın kendi klasörü ya da bir yedek dosyası --
  fotoğraf arşivi ve telefonların sertifikası (v6.203'ün kararı: sertifika da
  taşınsın).

İkisi de "ya tam olur ya hiç": veritabanı önce geçici bir dosyada kuruluyor ya
da kopyalanıyor, doğrulanınca tek hamlede yerine konuyor (tasi.py ve
geri_yukle.py'nin deseni). İş sürerken `SURUYOR` işaretli: program gelen
istekleri "kurulum sürüyor" sayfasıyla bekletiyor, yarım veritabanına kimse
girmiyor. Yeni kurulum ağa KAPALI başlıyor (v6.203, kullanıcının kararı).
"""

import shutil
import sqlite3
import threading
from datetime import datetime
from pathlib import Path

import db

_KILIT = threading.Lock()
SURUYOR = threading.Event()

SEMA = db.PROGRAM_KOK / "sema_guncel.sql"
VARSAYILAN_LAB_ADI = "Embriyoloji Laboratuvari"


class KurulumHatasi(Exception):
    """Ekrana yazılacak sebep; kurulum yapılmadı, tekrar denenebilir."""


# ----------------------------------------------------------------- listeler
# Seçim listelerinin ilk değerleri. Laboratuvar sonra yönetici ekranından
# değiştiriyor; göçler de yeni listeler ekliyor (bu tablo göçlerin gerisinde
# kalabilir, göçler kurulumun parçası).
LISTELER = {
    "maturasyon": [("mii", "MII"), ("mi", "MI"), ("gv", "GV"),
                   ("degenere", "Dejenere"), ("atretik", "Atretik")],
    "gecis_zorlugu": [("kolay", "Kolay"), ("normal", "Normal"), ("zor", "Zor")],
    "icsi_sonuc": [("basarili", "Başarılı"), ("degenere", "Dejenere")],
    "fert_sonuc": [("normal", "Normal"), ("degenere", "Dejenere"), ("kayip", "Kayıp")],
    "pn_sayisi": [("0", "0PN"), ("1", "1PN"), ("2", "2PN"), ("3", "3PN"),
                  ("4+", "4PN ve üzeri")],
    "pn_skoru": [("z1", "Z1"), ("z2", "Z2"), ("z3", "Z3"), ("z4", "Z4")],
    "simetri": [("esit", "Eşit"), ("hafif_esitsiz", "Hafif eşitsiz"),
                ("esitsiz", "Eşitsiz")],
    "cleavage_skor": [("G1", "G1"), ("G2", "G2"), ("G3", "G3"), ("G4", "G4")],
    "bl_genisleme": [("1", "1 - Erken blastosöl"), ("2", "2 - Blastosöl ≥ yarım"),
                     ("3", "3 - Tam blastokist"), ("4", "4 - Genişlemiş"),
                     ("5", "5 - Hatching"), ("6", "6 - Hatched"),
                     ("erken_morula", "Erken morula"), ("morula", "Morula"),
                     ("kavitasyon", "Kavitasyon"), ("arrest", "Arrest")],
    "bl_derece": [("1", "Derece 1"), ("2", "Derece 2"), ("3", "Derece 3")],
    "bl_icm": [("a", "A"), ("b", "B"), ("c", "C")],
    "bl_te": [("a", "A"), ("b", "B"), ("c", "C")],
    "bulgu_icsi": [
        ("kalin_zona", "Kalın zona"), ("ince_zona", "İnce zona"),
        ("duzensiz_zona", "Düzensiz zona"), ("granullu_sitoplazma", "Granüllü sitoplazma"),
        ("viskoz_sitoplazma", "Viskoz sitoplazma"),
        ("merkezi_granulasyon", "Merkezi granülasyon"), ("vakuol", "Vakuol"),
        ("ser_kumesi", "SER kümesi"), ("refraktil_cisim", "Refraktil cisim"),
        ("koyu_sitoplazma", "Koyu sitoplazma"), ("genis_pvs", "Geniş PVS"),
        ("pvs_debris", "PVS'de debris"), ("fragmente_pb", "Fragmente polar cisim"),
        ("buyuk_pb", "Büyük polar cisim"), ("oval_oosit", "Oval oosit"),
        ("duzensiz_form", "Düzensiz form")],
    "bulgu_fert": [("halo", "Halo"), ("pn_hizasiz", "PN hizasız"),
                   ("sitoplazmik_granulasyon", "Sitoplazmik granülasyon"),
                   ("vakuol", "Vakuol")],
    "bulgu_cleavage": [("multinukleasyon", "Multinükleasyon"),
                       ("duzensiz_bolunme", "Düzensiz bölünme"), ("vakuol", "Vakuol")],
    "sperm_alinma": [("masturbasyon", "Mastürbasyon"), ("tese", "TESE"), ("tesa", "TESA"),
                     ("donor", "Donör"), ("thaw", "Çözülmüş örnek")],
    "sperm_hazirlama": [("swim_up", "Swim-up"), ("gradient", "Gradient"),
                        ("yikama", "Yıkama")],
    "viskozite": [("normal", "Normal"), ("artmis", "Artmış"),
                  ("ileri_artmis", "İleri artmış")],
    "cycle_tipi": [("ivf_icsi", "IVF / ICSI cycle'ı"),
                   ("fet", "FET (donmuş embriyo transferi)"),
                   ("oosit_cryo", "Oosit dondurma")],
    "protokol_tipi": [("antagonist", "Antagonist"), ("long_agonist", "Long agonist"),
                      ("short_agonist", "Short agonist"), ("mild", "Mild"),
                      ("natural", "Natural"), ("ppos", "PPOS")],
    "trigger_tipi": [("hcg", "hCG"), ("gnrh_agonist", "GnRH agonist"),
                     ("dual", "Dual trigger")],
    "thaw_sagkalim": [("canli", "Canlı"), ("degenere", "Dejenere"),
                      ("kismi_hasar", "Kısmi hasar")],
    "discard_sebep": [("gelisimsel", "Gelişimsel"), ("genetik", "Genetik"),
                      ("hasta_talebi", "Hasta talebi"),
                      ("sure_doldu", "Saklama süresi doldu"), ("diger", "Diğer")],
    "pgt_sonuc": [("oploid", "Öploid"), ("anoploid", "Anöploid"), ("mozaik", "Mozaik"),
                  ("sonuc_yok", "Sonuç yok"), ("no_call", "No-call")],
    "sonlanma": [("canli_dogum", "Canlı doğum"), ("abortus", "Abortus"),
                 ("biyokimyasal", "Biyokimyasal gebelik"), ("ektopik", "Ektopik"),
                 ("devam_ediyor", "Devam ediyor"), ("takip_kaybi", "Takip kaybı")],
    "endikasyon": [
        ("erkek_faktoru", "Erkek faktörü"),
        ("siddetli_erkek_faktoru", "Şiddetli erkek faktörü"),
        ("azoospermi", "Azoospermi"), ("tubal_faktor", "Tubal faktör"),
        ("endometriozis", "Endometriozis"),
        ("ovulatuar_disfonksiyon", "Ovulatuar disfonksiyon / PCOS"),
        ("azalmis_over_rezervi", "Azalmış over rezervi"),
        ("ileri_anne_yasi", "İleri anne yaşı"), ("uterin_faktor", "Uterin faktör"),
        ("aciklanamayan", "Açıklanamayan infertilite"),
        ("tekrarlayan_implantasyon", "Tekrarlayan implantasyon başarısızlığı"),
        ("tekrarlayan_gebelik_kaybi", "Tekrarlayan gebelik kaybı"),
        ("pgt_endikasyonu", "PGT endikasyonu"),
        ("fertilite_koruma", "Fertilite koruma"),
        ("donor_oosit", "Donör oosit"), ("donor_sperm", "Donör sperm"),
        ("diger", "Diğer")],
    "goruntu_asama": [
        ("denudasyon", "Denüdasyon"), ("icsi", "ICSI"),
        ("fertilizasyon_kontrolu", "Fertilizasyon kontrolü"),
        ("gun2", "Gün 2"), ("gun3", "Gün 3"), ("blastokist", "Blastokist"),
        ("vitrifikasyon_oncesi", "Vitrifikasyon öncesi"),
        ("thaw_sonrasi", "Thaw sonrası"), ("transfer_oncesi", "Transfer öncesi"),
        ("diger", "Diğer")],
}


def ayarlar() -> list:
    """Varsayılan ayarlar: (anahtar, değer, açıklama). Lab kayıt no öneki bu yıl."""
    return [
        ("fert_kontrol_saat", "17", "ICSI sonrasi hedef fertilizasyon kontrolu (saat)"),
        ("gun3_kontrol_saat", "68", "ICSI sonrasi gun 3 kontrolu (saat)"),
        ("blast_kontrol_saat", "116", "ICSI sonrasi gun 5 kontrolu (saat)"),
        ("lab_no_onek", str(datetime.now().year), "Lab kayit no oneki"),
        ("lab_no_basamak", "4", "Sira kac basamakli"),
        ("lab_no_bosluk_doldur", "1", "1 = bosalan numara yeniden kullanilir"),
        ("lab_no_yillik_sifirla", "1", "1 = her yil sira 1'den baslar"),
        ("yedek_uyari_gun", "3", "Son yedek bu kadar gunden eskiyse uyar"),
        # Hekim alanının varsayılanı (v6.231): yeni laboratuvar boş başlıyor.
        # goc_060 anahtar yoksa bu laboratuvarın hekimini yazıyor (INSERT OR
        # IGNORE) -- boş satır, başka bir laboratuvarın yeni kurulumuna o adın
        # girmemesi için.
        ("varsayilan_hekim", "", "Hekim alaninin varsayilani (bos = yok)"),
    ]


def sema_kur(b: sqlite3.Connection, lab_adi: str = VARSAYILAN_LAB_ADI) -> None:
    """Açık (boş) bağlantıya şemayı, laboratuvar satırını, seçim listelerini ve
    varsayılan ayarları yazar. Commit çağıranın işi."""
    if not SEMA.exists():
        raise KurulumHatasi(f"sema_guncel.sql bulunamadi: {SEMA}")
    b.executescript(SEMA.read_text(encoding="utf-8"))
    b.execute("INSERT INTO lab (id, ad) VALUES (1, ?)", (lab_adi or VARSAYILAN_LAB_ADI,))
    sira = 0
    for liste, degerler in LISTELER.items():
        for kod, etiket in degerler:
            b.execute("INSERT OR IGNORE INTO liste_degeri "
                      "(lab_id, liste_adi, kod, etiket, sira) VALUES (1,?,?,?,?)",
                      (liste, kod, etiket, sira))
            sira += 1
    for anahtar, deger, aciklama in ayarlar():
        b.execute("INSERT OR IGNORE INTO ayarlar (lab_id, anahtar, deger, aciklama) "
                  "VALUES (1,?,?,?)", (anahtar, deger, aciklama))


# ------------------------------------------------------------------ yardımcı

def _yardimcilari_sil():
    for uz in ("-wal", "-shm", "-journal"):
        Path(str(db.DB_YOLU) + uz).unlink(missing_ok=True)


def _gecici_sil(gecici: Path) -> None:
    for uz in ("", "-wal", "-shm", "-journal"):
        Path(str(gecici) + uz).unlink(missing_ok=True)


def _yerine_koy(gecici: Path) -> None:
    """Geçici veritabanını tek hamlede yerine koyar (aynı klasörde,
    `Path.replace` atomik). Eski WAL yardımcı dosyaları kalırsa yeni içerikle
    uyuşmaz (README v6.16)."""
    _yardimcilari_sil()
    gecici.replace(db.DB_YOLU)
    db.sema_bilgisini_unut()


def _gocler() -> dict:
    """Göçler süreç içinde (`goc.calistir()`, açılıştakinin aynısı). Patlayan
    göç kurulumu geri almaz: program açılışta olduğu gibi açılır, hata
    Yönetici panelinde (v6.49)."""
    import goc
    try:
        sonuc = goc.calistir()
    except Exception as e:
        sonuc = {"calisti": [], "hatali": [("kurulum", repr(e))],
                 "bekleyen": [], "elle": [], "atlandi": ""}
    db.sema_bilgisini_unut()
    return sonuc


def _kullanici_gecerli(ad_soyad, kullanici_adi, sifre, sifre2):
    """`/kullanicilar/yeni`'nin kuralları (app.kullanici_yeni): ad boş olamaz,
    kullanıcı adı ASCII harf/rakam/nokta/alt çizgi, şifre en az 8 ve tekrarı
    aynı. Hata metni ya da None."""
    if not (ad_soyad or "").strip():
        return "Ad soyad boş olamaz."
    k = (kullanici_adi or "").strip().lower()
    if not k:
        return "Kullanıcı adı boş olamaz."
    if not k.isascii() or not k.replace(".", "").replace("_", "").isalnum():
        return ("Kullanıcı adı sadece harf, rakam, nokta ve alt çizgi içerebilir "
                "(Türkçe karakter kullanma).")
    if len(sifre or "") < 8:
        return "Şifre en az 8 karakter olmalı."
    if sifre != sifre2:
        return "Şifreler aynı değil."
    return None


# ---------------------------------------------------------- yeni laboratuvar

def yeni_laboratuvar(lab_adi, ad_soyad, kisa_kod, kullanici_adi, sifre, sifre2) -> dict:
    """Boş bilgisayarda yeni veritabanı + ilk yönetici. -> {"kullanici_id",
    "gocler"}. Hata: `KurulumHatasi` (hiçbir şey yazılmadı).

    Kullanıcı göçlerden ÖNCE yazılıyor: izin tablosunu göç (goc_026) kuruyor ve
    o an var olan kullanıcılara bütün modülleri veriyor. Göç patlasa bile
    yönetici girip Yönetici panelinde hatayı görebiliyor."""
    import guvenlik
    hata = _kullanici_gecerli(ad_soyad, kullanici_adi, sifre, sifre2)
    if hata:
        raise KurulumHatasi(hata)
    ad = ad_soyad.strip()
    kadi = kullanici_adi.strip().lower()
    kod = ((kisa_kod or "").strip() or ad[:2]).upper()
    with _KILIT:
        if db.DB_YOLU.exists():
            raise KurulumHatasi("Bu bilgisayarda zaten bir veritabanı var.")
        SURUYOR.set()
        gecici = db.VERI_KOK / "lab.db.kurulum"
        try:
            _gecici_sil(gecici)
            b = sqlite3.connect(gecici)
            try:
                sema_kur(b, (lab_adi or "").strip() or VARSAYILAN_LAB_ADI)
                kid = b.execute(
                    "INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, "
                    "kullanici_adi, sifre_hash) VALUES (1,?,?,'yonetici',?,?)",
                    (ad, kod, kadi, guvenlik.sifrele(sifre))).lastrowid
                b.commit()
                sonuc = b.execute("PRAGMA integrity_check").fetchone()[0]
            finally:
                b.close()
            if sonuc != "ok":
                raise KurulumHatasi(f"Yeni veritabanı doğrulanamadı ({sonuc}).")
            _yerine_koy(gecici)
            gocler = _gocler()
            db.ag_erisimi_yaz(db.AG_YEREL)
            return {"kullanici_id": kid, "gocler": gocler}
        except KurulumHatasi:
            raise
        except (sqlite3.Error, OSError) as e:
            raise KurulumHatasi(f"Veritabanı kurulamadı: {e}")
        finally:
            _gecici_sil(gecici)
            SURUYOR.clear()


# ------------------------------------------------------------ eski bilgisayar

def adaylar(klasor: Path) -> list:
    """Seçilen klasörde alınabilecek veritabanları, en yeni önce.

    `lab.db` (tasi.py'nin USB klasörü ya da eski programın kendi klasörü) ve
    yedek dosyaları (`lab_*.db`, yedek.py). Her biri için kayıt sayıları ve son
    kayıt (`tasi.ozet()`, salt okunur). Açılamayan ya da programın veritabanı
    olmayan (hasta tablosu yok) dosya listeye girmiyor."""
    import tasi
    sonuc = []
    try:
        dosyalar = [p for p in klasor.iterdir() if p.is_file() and p.suffix == ".db"]
    except OSError:
        return []
    for p in sorted(dosyalar, key=lambda x: x.stat().st_mtime, reverse=True)[:30]:
        try:
            o = tasi.ozet(p)
        except sqlite3.Error:
            continue
        if o["sayilar"].get("hasta") is None:
            continue
        sonuc.append({"ad": p.name, "yol": p, **o})
    return sonuc


def arsiv_klasoru(klasor: Path):
    a = klasor / "arsiv"
    return a if a.is_dir() else None


def sertifika_klasoru(klasor: Path):
    s = klasor / "sertifika"
    return s if (s / "kok.key").is_file() else None


def tasima_klasoru_mu(klasor: Path) -> bool:
    """`tasi.py disari`'nın USB klasörü mü (`lab_tasima`, TASIMA_BILGI.txt).
    Oradaki sertifika alındıktan sonra siliniyor; eski programın kendi
    klasöründekine dokunulmuyor (o program hâlâ çalışıyor olabilir)."""
    return (klasor / "TASIMA_BILGI.txt").is_file()


def dosya_say(klasor: Path) -> int:
    """Arşivdeki dosya sayısı -- ekran "N fotoğraf da gelecek" desin diye."""
    n = 0
    for p in klasor.rglob("*"):
        if p.is_file():
            n += 1
    return n


def veri_al(kaynak: Path, arsiv_al: bool = True, sertifika_al: bool = True) -> dict:
    """Eski bilgisayarın veritabanını (ve varsa arşivini, sertifikasını) bu
    bilgisayara alır. `kaynak`: `adaylar()`'dan seçilen dosya.

    -> {"ozet", "arsiv": (yeni, güncel) ya da None, "sertifika": bool,
        "gocler"}. Veritabanı kopyası SQLite backup API ile (açık bir
    programın veritabanı da tutarlı kopyalanır, README v6.16), bütünlüğü
    doğrulanıyor. Arşiv birikimli kopyalanıyor, hedeften bir şey silinmiyor
    (tasi.arsiv_kopyala)."""
    import tasi
    kaynak = Path(kaynak)
    klasor = kaynak.parent
    with _KILIT:
        if db.DB_YOLU.exists():
            raise KurulumHatasi("Bu bilgisayarda zaten bir veritabanı var.")
        SURUYOR.set()
        gecici = db.VERI_KOK / "lab.db.kurulum"
        try:
            _gecici_sil(gecici)
            k = h = None
            try:
                k = sqlite3.connect(f"file:{kaynak}?mode=ro", uri=True)
                h = sqlite3.connect(gecici)
                k.backup(h)
                sonuc = h.execute("PRAGMA integrity_check").fetchone()[0]
            except sqlite3.Error as e:
                raise KurulumHatasi(f"Veritabanı okunamadı: {e}")
            finally:
                for x in (k, h):          # Windows açık dosyayı silmez
                    if x is not None:
                        x.close()
            if sonuc != "ok":
                raise KurulumHatasi(f"Veritabanı doğrulanamadı ({sonuc}).")
            _yerine_koy(gecici)
            # Özet yerine konmuş dosyadan: geçici kopyayı salt okunur açmak
            # onun boş -wal/-shm dosyalarını klasörde bırakıyordu.
            ozet = tasi.ozet(db.DB_YOLU)
        except KurulumHatasi:
            _gecici_sil(gecici)
            SURUYOR.clear()
            raise
        except (sqlite3.Error, OSError) as e:
            _gecici_sil(gecici)
            SURUYOR.clear()
            raise KurulumHatasi(f"Veri alınamadı: {e}")

        # Veritabanı yerinde: kurulum oldu. Arşiv ve sertifika ondan sonra;
        # biri yapılamazsa kurulum geri alınmıyor, sebebi `uyarilar`da (arşiv
        # sonradan `tasi.py iceri` ile de alınabilir).
        uyarilar, arsiv, sertifika_alindi = [], None, False
        try:
            a = arsiv_klasoru(klasor) if arsiv_al else None
            if a is not None:
                try:
                    hedef = Path(db.ayar("goruntu_arsiv_klasor",
                                         str(db.VERI_KOK / "arsiv")))
                    arsiv = tasi.arsiv_kopyala(a, hedef)
                except OSError as e:
                    uyarilar.append(f"Fotoğraf arşivi kopyalanamadı: {e}")
            s = sertifika_klasoru(klasor) if sertifika_al else None
            if s is not None:
                try:
                    import sertifika
                    if sertifika.KLASOR.exists():
                        eski = sertifika.KLASOR.parent / (
                            f"sertifika_ONCEKI_{datetime.now():%Y%m%d_%H%M%S}")
                        sertifika.KLASOR.rename(eski)
                    shutil.copytree(s, sertifika.KLASOR)
                    sertifika_alindi = True
                    if tasima_klasoru_mu(klasor):
                        shutil.rmtree(s, ignore_errors=True)
                except OSError as e:
                    uyarilar.append(f"Sertifika alınamadı: {e}")
            gocler = _gocler()
            db.ag_erisimi_yaz(db.AG_YEREL)
        finally:
            SURUYOR.clear()
        return {"ozet": ozet, "arsiv": arsiv, "sertifika": sertifika_alindi,
                "gocler": gocler, "uyarilar": uyarilar}
