"""Günlük yedekleme.

Üç şey yapar:
  1. Veritabanının tutarlı bir kopyasını alır (SQLite backup API — uygulama
     çalışırken bile güvenli; düz dosya kopyası yarım yazılmış olabilir)
  2. Kopyayı doğrular (integrity_check) — açılmayan yedek yedek değildir
  3. Arşiv klasöründeki yeni fotoğrafları hedefe kopyalar
  4. Cryo Haritası'nın Excel'inin son halini kopyalar (v6.191) --
     bilgisayar bozulursa harita programsız da okunabilsin

Kullanım:
    python yedek.py                 (hedef: bu makinenin yerel_ayar.json bölümü)
    python yedek.py D:\\lab_yedek    (hedefi elle ver — komut satırı her zaman önce gelir)

Hedef klasörü kalıcı olarak değiştirmek için: python yerel_kur.py
"""

import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import db

# Yedeklenen ve yazılan her şey **veri** kökünde (bkz. db.py "iki kök").
KOK = db.VERI_KOK
DB = db.DB_YOLU
LOG = KOK / "yedek.log"

GUNLUK_SAKLA = 14        # son kaç günlük veritabanı kopyası tutulsun
AYIN_BIRI_SAKLA = True   # her ayın ilk yedeği kalıcı olarak saklanır


def yaz(mesaj):
    satir = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {mesaj}"
    print(satir)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(satir + "\n")


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
    """SQLite backup API ile tutarlı kopya alır ve doğrular."""
    hedef_klasor.mkdir(parents=True, exist_ok=True)
    ad = f"lab_{datetime.now():%Y%m%d_%H%M}.db"
    hedef = hedef_klasor / ad

    kaynak = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    kopya = sqlite3.connect(hedef)
    with kopya:
        kaynak.backup(kopya)        # uygulama yazarken bile tutarlı anlık görüntü
    kaynak.close()

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

    if sonuc != "ok":
        hedef.unlink(missing_ok=True)
        raise RuntimeError(f"Yedek dogrulanamadi: {sonuc}")

    mb = hedef.stat().st_size / 1024 / 1024
    yaz(f"Veritabani: {hedef.name}  ({mb:.1f} MB, {tablo} tablo, "
        f"{hasta} hasta, {cycle} cycle, {goruntu} goruntu)")
    return hedef


def eskileri_temizle(hedef_klasor: Path):
    kopyalar = sorted(hedef_klasor.glob("lab_*.db"))
    sinir = datetime.now() - timedelta(days=GUNLUK_SAKLA)
    silinen = 0
    for p in kopyalar[:-1]:                       # en yenisi her zaman kalir
        try:
            tarih = datetime.strptime(p.stem[4:], "%Y%m%d_%H%M")
        except ValueError:
            continue
        if tarih >= sinir:
            continue
        if AYIN_BIRI_SAKLA and tarih.day == 1:
            continue
        p.unlink(missing_ok=True)
        silinen += 1
    if silinen:
        yaz(f"{silinen} eski veritabani kopyasi silindi "
            f"({GUNLUK_SAKLA} gunden eski, ayin 1'i haric)")


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


def main():
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
    yaz("=" * 55)
    yaz(f"Yedekleme basladi -> {hedef_klasor}   (kaynak: {kaynak})")

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
        hedef_klasor.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        yaz(f"HATA: hedef klasor olusturulamadi: {e}")
        sys.exit(1)

    try:
        veritabani_yedekle(hedef_klasor)
        eskileri_temizle(hedef_klasor)
        arsiv_klasor = Path(ayar("goruntu_arsiv_klasor", str(KOK / "arsiv")))
        arsiv_yedekle(arsiv_klasor, hedef_klasor)
        harita_yedekle(hedef_klasor)
        ayar_yaz("son_yedek", datetime.now().isoformat(" ", "seconds"))
        yaz("Yedekleme tamam.")
    except Exception as e:
        yaz(f"HATA: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
