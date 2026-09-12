"""İki makine arasında veriyi USB ile taşır — üzerine yazmadan önce karşılaştırır.

`lab.db` tek dosyadır; "sadece yeni kayıtları" ayırmanın yolu yok. Taşınan şey
dosyanın tamamıdır ve karşıdakinin **üzerine yazar**. Bu yüzden asıl iş
kopyalamak değil, **yanlış yöne kopyalamayı yakalamak**:

    Mac'te 3 hasta girdin, USB'ye almadın
    Klinikte 5 hasta girdin
    Sonra Mac'ten kliniğe kopyaladın  ->  kliniğin 5 hastası yok oldu

`iceri` komutu bunu yakalar: USB'deki kopyayla bu makinedekini yan yana koyar,
bu makinedeki daha yeniyse durur ve açık onay ister. Ayrıca üzerine yazmadan
önce mevcut veritabanının yedeğini alır.

Kullanım:
    python3 tasi.py durum  /Volumes/USB     sadece karşılaştır, hiçbir şey yapma
    python3 tasi.py disari /Volumes/USB     bu makineden USB'ye
    python3 tasi.py iceri  /Volumes/USB     USB'den bu makineye

Windows'ta `python tasi.py durum E:\\` gibi.

Uygulama çalışırken de güvenli: veritabanı kopyası SQLite backup API ile
alınıyor, düz dosya kopyası değil (README v6.16).
"""

import platform
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import db

# Taşınan her şey veri kökünde: `lab.db`, geçici kopya, `lab_ONCEKI_*.db`
# ve `arsiv/` (bkz. db.py "iki kök").
KOK = db.VERI_KOK
KLASOR_ADI = "lab_tasima"          # USB'de açılacak klasör
DB_ADI = "lab.db"

# Kaydın **girildiği** an. Klinik zamanları (opu_zamani gibi) elle geri
# tarihlenebildiği için "bu veritabanına en son ne zaman yazıldı" sorusuna
# uygun değil; `olusturma_zamani` satırın oluşturulma anıdır.
ETKINLIK = [
    ("hasta", "olusturma_zamani"), ("cycle", "olusturma_zamani"),
    ("specimen", "olusturma_zamani"), ("goruntu", "olusturma_zamani"),
    ("olay", "olusturma_zamani"), ("sperm_ornek", "olusturma_zamani"),
    ("pgt_sonuc", "olusturma_zamani"), ("kullanici", "olusturma_zamani"),
    ("degisiklik_log", "zaman"), ("islem_yapan", "zaman"),
    ("specimen_bulgu", "zaman"), ("sperm_analiz", "zaman"),
    ("beta_hcg", "zaman"), ("kaynak_dosya", "zaman"),
]
SAYILACAK = [("hasta", "hasta"), ("cycle", "cycle"), ("specimen", "örnek"),
             ("goruntu", "fotoğraf"), ("olay", "olay"),
             ("kullanici", "kullanıcı")]


def ozet(yol: Path) -> dict:
    """Bir veritabanı dosyasının kayıt sayıları ve son etkinlik zamanı."""
    b = sqlite3.connect(f"file:{yol}?mode=ro", uri=True)
    sayilar, son = {}, None
    for tablo, ad in SAYILACAK:
        try:
            sayilar[ad] = b.execute(f"SELECT COUNT(*) FROM {tablo}").fetchone()[0]
        except sqlite3.Error:
            sayilar[ad] = None
    for tablo, kolon in ETKINLIK:
        try:
            v = b.execute(f"SELECT MAX({kolon}) FROM {tablo}").fetchone()[0]
        except sqlite3.Error:
            continue
        if v and (son is None or v > son):
            son = v
    b.close()
    return {"sayilar": sayilar, "son_etkinlik": son,
            "boyut_mb": yol.stat().st_size / 1024 / 1024}


def yaz_ozet(baslik: str, o: dict):
    print(f"  {baslik}")
    print("    " + ", ".join(f"{v if v is not None else '?'} {ad}"
                             for ad, v in o["sayilar"].items()))
    print(f"    son kayit : {o['son_etkinlik'] or 'hic kayit yok'}")
    print(f"    dosya     : {o['boyut_mb']:.1f} MB")


def tutarli_kopya(kaynak: Path, hedef: Path):
    """SQLite backup API ile kopya — uygulama çalışırken bile tutarlı.

    Düz dosya kopyası WAL modunda YANILTICIDIR: yeni kayıtlar henüz
    `lab.db-wal` dosyasında olabilir ve kopya bomboş çıkar (README v6.16).
    """
    k = sqlite3.connect(f"file:{kaynak}?mode=ro", uri=True)
    h = sqlite3.connect(hedef)
    with h:
        k.backup(h)
    k.close()
    sonuc = h.execute("PRAGMA integrity_check").fetchone()[0]
    h.close()
    if sonuc != "ok":
        hedef.unlink(missing_ok=True)
        sys.exit(f"HATA: kopya dogrulanamadi ({sonuc}). Tasima yapilmadi.")


def arsiv_kopyala(kaynak: Path, hedef: Path) -> tuple:
    """Yeni veya değişmiş fotoğrafları kopyalar. Hedeften hiçbir şey silinmez."""
    if not kaynak.is_dir():
        return (0, 0)
    yeni = guncel = 0
    for p in kaynak.rglob("*"):
        if not p.is_file():
            continue
        h = hedef / p.relative_to(kaynak)
        if h.exists() and h.stat().st_size == p.stat().st_size:
            guncel += 1
            continue
        h.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, h)
        yeni += 1
    return (yeni, guncel)


def usb_klasoru(usb: str) -> Path:
    return Path(usb) / KLASOR_ADI


def karsilastir(usb: str, sessiz: bool = False):
    """İki tarafın özetini döndürür. Yoksa o taraf None olur.

    Bu makinede `lab.db` olmayabilir: yeni kurulmuş bir bilgisayara ilk kez
    veri alınıyordur. O durumda karşılaştıracak bir şey yok, kaybedilecek bir
    şey de yok (v6.17).
    """
    burasi = ozet(db.DB_YOLU) if db.DB_YOLU.exists() else None
    usb_db = usb_klasoru(usb) / DB_ADI
    oradaki = ozet(usb_db) if usb_db.is_file() else None

    if not sessiz:
        print(f"\nMakine: {db.MAKINE}   ({platform.system()})")
        print("=" * 58)
        if burasi:
            yaz_ozet("BU MAKINEDE", burasi)
        else:
            print(f"  BU MAKINEDE\n    lab.db yok — bu makine henuz bos.")
        print()
        if oradaki:
            yaz_ozet(f"USB'DE ({usb_klasoru(usb)})", oradaki)
        else:
            print(f"  USB'DE\n    {usb_klasoru(usb)} bulunamadi — henuz tasima yok.")
    return burasi, oradaki


def hangisi_yeni(burasi: dict, oradaki: dict) -> str:
    """'usb', 'burasi' veya 'ayni'."""
    a, b = burasi["son_etkinlik"], oradaki["son_etkinlik"]
    if a == b:
        return "ayni"
    if a is None:
        return "usb"
    if b is None:
        return "burasi"
    return "usb" if b > a else "burasi"


def onay_iste(soru: str) -> bool:
    print(f"\n{soru}")
    return input("  Devam etmek icin EVET yaz: ").strip() == "EVET"


# --------------------------------------------------------------------- disari

def disari(usb: str):
    burasi, oradaki = karsilastir(usb)
    if not burasi:
        sys.exit(f"\nBu makinede lab.db yok: {db.DB_YOLU}\n"
                 "Gonderecek veri yok. Once 'iceri' ile veri al ya da "
                 "'sifirdan_kur.py' ile yeni bir veritabani olustur.")
    hedef = usb_klasoru(usb)

    if oradaki:
        yon = hangisi_yeni(burasi, oradaki)
        if yon == "usb":
            print("\n" + "!" * 58)
            print("DIKKAT: USB'deki kopya BU MAKINEDEKINDEN YENI.")
            print("Devam edersen USB'deki daha yeni veri silinir.")
            print("Muhtemelen once 'iceri' yapman gerekiyordu.")
            print("!" * 58)
            if not onay_iste("USB'deki daha yeni veriyi silmek istedigine emin misin?"):
                sys.exit("Iptal edildi. Hicbir sey degismedi.")

    try:
        hedef.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        sys.exit(f"HATA: USB klasoru olusturulamadi: {e}\nUSB takili mi?")

    print(f"\nUSB'ye yaziliyor: {hedef}")
    gecici = hedef / (DB_ADI + ".yeni")
    tutarli_kopya(db.DB_YOLU, gecici)
    gecici.replace(hedef / DB_ADI)          # yarim dosya birakma
    print(f"  veritabani kopyalandi ve dogrulandi")

    arsiv = Path(db.ayar("goruntu_arsiv_klasor", str(KOK / "arsiv")))
    yeni, guncel = arsiv_kopyala(arsiv, hedef / "arsiv")
    print(f"  arsiv: {yeni} yeni dosya, {guncel} zaten guncel")

    (hedef / "TASIMA_BILGI.txt").write_text(
        f"Kaynak makine : {db.MAKINE}\n"
        f"Tasima zamani : {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        f"Son kayit     : {burasi['son_etkinlik']}\n"
        f"Icerik        : " + ", ".join(
            f"{v} {ad}" for ad, v in burasi["sayilar"].items()) + "\n",
        encoding="utf-8")
    print("\nTamam. USB'yi cikarip diger makinede su komutu calistir:")
    print(f"  python3 tasi.py iceri <usb yolu>")


# ---------------------------------------------------------------------- iceri

def iceri(usb: str):
    burasi, oradaki = karsilastir(usb)
    if not oradaki:
        sys.exit(f"\nUSB'de tasima klasoru yok: {usb_klasoru(usb)}\n"
                 "Once diger makinede 'python3 tasi.py disari' calistir.")

    print("\n  NOT: uygulama acikken lab.db degistirilemez. Acisksa once "
          "Ctrl+C ile durdur.")

    bilgi = usb_klasoru(usb) / "TASIMA_BILGI.txt"
    if bilgi.is_file():
        print("\n  " + bilgi.read_text(encoding="utf-8").replace("\n", "\n  ").strip())

    print("\n" + "=" * 58)
    if not burasi:
        # Yeni kurulmus makine: karsilastiracak bir sey yok, kaybedilecek de.
        print("Bu makinede lab.db yok — ilk kurulum. Guvenle alinabilir.")
        yon = "usb"
    else:
        yon = hangisi_yeni(burasi, oradaki)
    if not burasi:
        pass
    elif yon == "usb":
        print("USB'deki kopya daha yeni. Guvenle alabilirsin.")
    elif yon == "ayni":
        print("Ikisi de ayni gorunuyor. Almanin zarari yok.")
    else:
        print("!" * 58)
        print("DIKKAT: BU MAKINEDEKI veri USB'dekinden YENI.")
        print(f"  bu makinede son kayit : {burasi['son_etkinlik']}")
        print(f"  USB'de son kayit      : {oradaki['son_etkinlik']}")
        print("\nDevam edersen bu makinede girdigin YENI KAYITLAR SILINIR.")
        print("Muhtemelen once bu makineden 'disari' yapman gerekiyordu.")
        print("!" * 58)
        if not onay_iste("Bu makinedeki daha yeni veriyi silmek istedigine emin misin?"):
            sys.exit("Iptal edildi. Hicbir sey degismedi.")

    # Uzerine yazmadan once mevcut veritabaninin yedegi — yanlislikla
    # yapildiysa geri donulebilsin. Bos makinede yedeklenecek bir sey yok.
    gz = None
    if burasi:
        gz = KOK / f"lab_ONCEKI_{datetime.now():%Y%m%d_%H%M%S}.db"
        tutarli_kopya(db.DB_YOLU, gz)
        print(f"\n  bu makinenin onceki hali yedeklendi: {gz.name}")

    gecici = KOK / (DB_ADI + ".yeni")
    tutarli_kopya(usb_klasoru(usb) / DB_ADI, gecici)
    # WAL yardimci dosyalari eski veritabanina ait — kalirsa yeni dosyayla
    # tutarsiz olur.
    for uz in ("-wal", "-shm"):
        (KOK / (DB_ADI + uz)).unlink(missing_ok=True)
    try:
        gecici.replace(db.DB_YOLU)
    except OSError as e:
        # Windows acik dosyanin uzerine yazdirmaz; uygulama calisiyor demektir.
        gecici.unlink(missing_ok=True)
        sys.exit(f"\nHATA: lab.db degistirilemedi ({e}).\n"
                 "Uygulama calisiyor olabilir — terminalde Ctrl+C ile durdur, "
                 "sonra bu komutu tekrar calistir."
                 + (f"\nOnceki hali duruyor: {gz.name}" if gz else ""))
    print("  veritabani alindi ve dogrulandi")

    arsiv = Path(db.ayar("goruntu_arsiv_klasor", str(KOK / "arsiv")))
    yeni, guncel = arsiv_kopyala(usb_klasoru(usb) / "arsiv", arsiv)
    print(f"  arsiv: {yeni} yeni dosya, {guncel} zaten guncel")

    print("\nTamam. Simdi sirasiyla:")
    komut = "python" if platform.system() == "Windows" else "python3"
    print(f"  {komut} goc_hepsi.py")
    print(f"  {komut} -m uvicorn app:uygulama --host 0.0.0.0 --port 8000")
    if gz:
        print(f"\nHer sey yolundaysa {gz.name} dosyasini silebilirsin.")


def main():
    komut = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    usb = sys.argv[2] if len(sys.argv) > 2 else ""
    if komut not in ("durum", "disari", "iceri") or not usb:
        sys.exit(__doc__)
    if not Path(usb).is_dir():
        sys.exit(f"'{usb}' diye bir klasor yok. USB takili mi?\n"
                 "Mac'te genelde /Volumes/... , Windows'ta E:\\ gibi.")
    if komut == "durum":
        karsilastir(usb)
        print("\n(Sadece bakildi, hicbir sey degismedi.)")
    elif komut == "disari":
        disari(usb)
    else:
        iceri(usb)


if __name__ == "__main__":
    main()
