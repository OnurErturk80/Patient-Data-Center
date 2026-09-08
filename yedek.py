"""Günlük yedekleme.

Üç şey yapar:
  1. Veritabanının tutarlı bir kopyasını alır (SQLite backup API — uygulama
     çalışırken bile güvenli; düz dosya kopyası yarım yazılmış olabilir)
  2. Kopyayı doğrular (integrity_check) — açılmayan yedek yedek değildir
  3. Arşiv klasöründeki yeni fotoğrafları hedefe kopyalar

Kullanım:
    python yedek.py                 (hedef: ayarlar tablosundan)
    python yedek.py D:\\lab_yedek    (hedefi elle ver)
"""

import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

KOK = Path(__file__).parent
DB = KOK / "lab.db"
LOG = KOK / "yedek.log"

GUNLUK_SAKLA = 14        # son kaç günlük veritabanı kopyası tutulsun
AYIN_BIRI_SAKLA = True   # her ayın ilk yedeği kalıcı olarak saklanır


def yaz(mesaj):
    satir = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {mesaj}"
    print(satir)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(satir + "\n")


def ayar(anahtar, varsayilan=""):
    yerel = KOK / "yerel_ayar.json"
    if yerel.is_file():
        import json
        try:
            d = json.loads(yerel.read_text(encoding="utf-8"))
            if anahtar in d:
                return str(d[anahtar])
        except Exception:
            pass
    try:
        b = sqlite3.connect(DB)
        r = b.execute("SELECT deger FROM ayarlar WHERE lab_id=1 AND anahtar=?",
                      (anahtar,)).fetchone()
        b.close()
        return r[0] if r else varsayilan
    except sqlite3.Error:
        return varsayilan


def ayar_yaz(anahtar, deger):
    try:
        b = sqlite3.connect(DB)
        b.execute(
            "INSERT INTO ayarlar (lab_id, anahtar, deger) VALUES (1,?,?) "
            "ON CONFLICT(lab_id, anahtar) DO UPDATE SET deger=excluded.deger",
            (anahtar, deger))
        b.commit()
        b.close()
    except sqlite3.Error as e:
        yaz(f"UYARI: son_yedek ayari yazilamadi: {e}")


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


def main():
    if not DB.exists():
        yaz("HATA: lab.db bulunamadi.")
        sys.exit(1)

    hedef = sys.argv[1] if len(sys.argv) > 1 else ayar("yedek_klasor", "")
    if not hedef:
        yaz("HATA: yedek klasoru tanimli degil. "
            "Kullanim: python yedek.py D:\\lab_yedek")
        sys.exit(1)

    hedef_klasor = Path(hedef)
    yaz("=" * 55)
    yaz(f"Yedekleme basladi -> {hedef_klasor}")

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
        ayar_yaz("son_yedek", datetime.now().isoformat(" ", "seconds"))
        yaz("Yedekleme tamam.")
    except Exception as e:
        yaz(f"HATA: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
