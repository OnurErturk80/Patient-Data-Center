"""Veritabanı bağlantısı ve yardımcı fonksiyonlar."""

import json
import platform
import sqlite3
from pathlib import Path

DB_YOLU = Path(__file__).parent / "lab.db"
LAB_ID = 1          # v1 tek laboratuvar


def baglan():
    """Yeni bir bağlantı açar. Her istek kendi bağlantısını kullanır."""
    b = sqlite3.connect(DB_YOLU)
    b.row_factory = sqlite3.Row      # sonuçlara kolon adıyla eriş
    b.execute("PRAGMA foreign_keys = ON")
    return b


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


def liste(liste_adi):
    """Bir seçim listesinin değerlerini döndürür."""
    return sorgu(
        "SELECT kod, etiket FROM liste_degeri "
        "WHERE lab_id = ? AND liste_adi = ? AND aktif_mi = 1 ORDER BY sira",
        (LAB_ID, liste_adi),
    )


# ----------------------------------------------------------------- yerel ayar

YEREL_DOSYA = Path(__file__).parent / "yerel_ayar.json"
KOK = Path(__file__).parent
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


def ayar(anahtar, varsayilan=""):
    """Ayar değeri. Klasör yolları makineye özgü dosyadan, gerisi veritabanından."""
    if anahtar in YOL_ANAHTARLARI:
        deger = yerel_ayarlar().get(anahtar)
        if deger:
            return deger
    r = tek("SELECT deger FROM ayarlar WHERE lab_id = ? AND anahtar = ?",
            (LAB_ID, anahtar))
    return r["deger"] if r else varsayilan
