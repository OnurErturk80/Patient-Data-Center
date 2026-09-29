"""Yedekleme.

Dört şey yapar (`yedekle()`, tek yerde):
  1. Veritabanının tutarlı bir kopyasını alır (SQLite backup API — uygulama
     çalışırken bile güvenli; düz dosya kopyası yarım yazılmış olabilir)
  2. Kopyayı doğrular (integrity_check) — açılmayan yedek yedek değildir
  3. Arşiv klasöründeki yeni fotoğrafları hedefe kopyalar
  4. Cryo Haritası'nın Excel'inin son halini kopyalar (v6.191) --
     bilgisayar bozulursa harita programsız da okunabilsin

Üç yerden çağrılıyor: terminal (`python yedek.py`), Yedekleme ekranının
"Şimdi yedekle"si ve v6.216'dan beri program açıkken Cryo Haritası her
değiştiğinde (`oto_yedek.py`). Aynı programın içindeki iki yedek aynı anda
çalışmasın diye `KILIT`.

**Saklama** (v6.216, `eskileri_temizle()`): son bir günün bütün yedekleri;
14 güne kadar her günün SON yedeği; daha eskide her ayın ilk yedeği kalıcı.
Cryo değişince alınan yedekler günde birkaç tane olabiliyor; ertesi gün
yalnızca o günün son hali kalıyor. Güvenlik kopyalarına (`lab_ONCEKI_*`)
dokunulmuyor.

Kullanım:
    python yedek.py                 (hedef: bu makinenin yerel_ayar.json bölümü)
    python yedek.py D:\\lab_yedek    (hedefi elle ver — komut satırı her zaman önce gelir)

Hedef klasörü kalıcı olarak değiştirmek için: python yerel_kur.py
"""

import logging
import os
import shutil
import sqlite3
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path

import db

# Yedeklenen ve yazılan her şey **veri** kökünde (bkz. db.py "iki kök").
KOK = db.VERI_KOK
DB = db.DB_YOLU
LOG = KOK / "yedek.log"

TUMU_SAKLA_SAAT = 24     # son bu kadar saatin bütün yedekleri kalır
GUNLUK_SAKLA = 14        # bu kadar güne kadar her günün son yedeği kalır
AYIN_ILKI_SAKLA = True   # daha eskide her ayın ilk yedeği kalıcı olarak saklanır

# Aynı programda iki yedek aynı anda çalışmasın (v6.216): Cryo değişince
# alınan yedek ile "Şimdi yedekle" aynı klasöre, aynı dakikanın adına
# yazabilirdi. Geri yükleme de bunu tutuyor (`geri_yukle.geri_yukle()`):
# temizlik, seçilen yedeği tam o sırada silmesin. Terminalden ayrı bir
# süreçte çalışan `yedek.py`'yi kapsamaz; onun için yazım geçici dosyaya
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
    # Yarıda kalmış yazımlar (program o sırada kapandı): bir günden eskiyse.
    sinir = datetime.now().timestamp() - 86400
    for p in hedef_klasor.glob("lab_*.yaziliyor"):
        try:
            if p.stat().st_mtime < sinir:
                p.unlink()
        except OSError:
            pass
    if silinen:
        yaz(f"{silinen} eski veritabani kopyasi silindi (son {TUMU_SAKLA_SAAT} "
            f"saatin hepsi, {GUNLUK_SAKLA} gune kadar her gunun sonuncusu, "
            "daha eskide her ayin ilki kalir)")


def arsiv_yedekle(arsiv: Path, hedef_klasor: Path):
    """Yeni veya degismis fotograflari kopyalar. Hedeften hicbir sey silinmez."""
    if not arsiv.is_dir():
        yaz(f"Arsiv klasoru yok, atlandi: {arsiv}")
        return
    hedef = hedef_klasor / "arsiv"
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
    """Cryo Haritası'nın Excel'ini (`harita_excel.py`, v6.191) hedefe kopyalar:
    yalnızca son hali, eskisinin üzerine. Program kendi kopyasını veri
    klasöründe tutuyor; bu, bilgisayar bozulursa haritanın programsız
    okunabilmesi için. Kopyalanamazsa yedeklemeyi durdurmaz -- asıl yedek
    veritabanı, harita ondan yeniden üretilebilir."""
    import harita_excel               # yol tek yerde (tuzak #8)
    kaynak = harita_excel.ana_dosya()
    if not kaynak.is_file():
        yaz("Cryo haritasi Excel'i yok, atlandi (program acildiginda yazilir).")
        return
    try:
        hedef = hedef_klasor / harita_excel.KLASOR_ADI
        hedef.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kaynak, hedef / kaynak.name)
        yaz(f"Cryo haritasi Excel'i kopyalandi: {hedef / kaynak.name}")
    except OSError as e:
        yaz(f"UYARI: Cryo haritasi Excel'i kopyalanamadi: {e}")


def yedekle(hedef_klasor: Path, kaynak: str) -> Path:
    """Bütün yedekleme, tek yerden: veritabanı, eski kopyaların temizliği,
    arşivdeki yeni fotoğraflar, Cryo Haritası'nın Excel'i, "son yedek" ayarı.

    Terminal (`main()`), "Şimdi yedekle" ve Cryo değişince alınan yedek
    (`oto_yedek.py`) bunu çağırıyor -- v6.215'e kadar ilk ikisi adımları ayrı
    ayrı yazıyordu. Hata yükselir (`yaz()` önce günlüğe yazar); hedef klasör
    yoksa oluşturulur, kullanılabilir olup olmadığına çağıran karar verir.
    Yazılan veritabanı kopyasının yolunu döndürür.
    """
    with KILIT:
        yaz("=" * 55)
        yaz(f"Yedekleme basladi -> {hedef_klasor}   (kaynak: {kaynak})")
        try:
            hedef_klasor.mkdir(parents=True, exist_ok=True)
            yol = veritabani_yedekle(hedef_klasor)
            eskileri_temizle(hedef_klasor)
            arsiv_klasor = Path(ayar("goruntu_arsiv_klasor", str(KOK / "arsiv")))
            arsiv_yedekle(arsiv_klasor, hedef_klasor)
            harita_yedekle(hedef_klasor)
            ayar_yaz("son_yedek", datetime.now().isoformat(" ", "seconds"))
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
        yedekle(hedef_klasor, kaynak)
    except Exception:
        sys.exit(1)                 # sebebi yedekle() yazdı


if __name__ == "__main__":
    main()
