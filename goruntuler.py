"""Snapshot klasörünü izler, görüntüleri specimen'lere bağlar ve arşive kopyalar."""

import shutil
import unicodedata
from datetime import datetime
from pathlib import Path

import db

UZANTILAR = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


ayar = db.ayar          # yerel_ayar.json önceliklidir


# --------------------------------------------------------- iki sistemde de güvenli yol

WINDOWS_YASAK = '<>:"/\\|?*'
WINDOWS_AYRILMIS = {"CON", "PRN", "AUX", "NUL",
                    *(f"COM{i}" for i in range(1, 10)),
                    *(f"LPT{i}" for i in range(1, 10))}


def guvenli_ad(metin, varsayilan: str = "bilinmeyen") -> str:
    """Bir klasör/dosya adı parçasını Windows ve macOS'ta güvenli hale getirir.

    Üç ayrı tuzak var:
      - Windows `< > : " / \\ | ? *` karakterlerini ve sondaki nokta/boşluğu
        kabul etmez; `CON`, `NUL`, `COM1`... adları ayrılmıştır.
      - macOS dosya adlarını ayrıştırılmış (NFD), Windows birleştirilmiş (NFC)
        Unicode ile saklar. Klasör USB ile taşınınca 'ü' iki farklı bayt
        dizisi olur ve yol eşleşmez — bu yüzden NFC'ye normalize ediliyor.
      - Boş ad klasör açtırmaz.
    """
    m = unicodedata.normalize("NFC", str(metin or "")).strip()
    m = "".join("_" if (c in WINDOWS_YASAK or ord(c) < 32) else c for c in m)
    m = m.rstrip(". ")
    if m.upper().split(".")[0] in WINDOWS_AYRILMIS:
        m = "_" + m
    return m or varsayilan


def kaynak_klasor() -> Path:
    return Path(ayar("goruntu_kaynak_klasor"))


def arsiv_klasor() -> Path:
    return Path(ayar("goruntu_arsiv_klasor", "arsiv"))


def hasta_klasoru(cycle_id: int) -> str:
    """Arşivde bu cycle'ın hastasına ait klasör adı — hasta dosya numarası.

    Sadece dosya no kullanılır, hasta adı değil: rakam her iki işletim
    sisteminde de sorunsuz, hasta adı değişse bile (evlilik, düzeltme) yol
    bozulmaz. Hangi numaranın kime ait olduğu programdan görünür.
    """
    r = db.tek("SELECT h.dosya_no FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
               "WHERE c.id = ?", (cycle_id,))
    return guvenli_ad(r["dosya_no"] if r else "", f"cycle{cycle_id}")


def ornek_kodu(cycle_id: int, specimen_id, cycle_no: str = "") -> str:
    """Örneğin tam kodu: `<hasta dosya no>-<cycle no>-<sıra>`.

    `specimen_id` zaten `<cycle no>-<sıra>` biçiminde (`2026-0001-03`), başına
    hasta dosya numarası eklenir → `527078-2026-0001-03`. Örneğe bağlı olmayan
    (cycle arşivi) fotoğraflarda `<hasta dosya no>-<cycle no>` olur.

    Kaynak resmin adı kullanılmaz; dosya adı kendi kendini tanımlar.
    """
    return guvenli_ad(f"{hasta_klasoru(cycle_id)}-{specimen_id or cycle_no}")


def hedef_klasor(cycle_id: int, cycle_no: str) -> Path:
    """Bu cycle'ın görüntülerinin yazılacağı arşiv klasörü.

    `arsiv/<hasta dosya no>/<cycle no>/` — v6.4'e kadar `arsiv/<yıl>/<cycle no>/`
    idi; yıl zaten cycle numarasının içinde olduğu için bilgi kaybı yok.
    """
    return arsiv_klasor() / hasta_klasoru(cycle_id) / guvenli_ad(cycle_no)


def goreli_yap(tam: Path) -> str:
    """Arşiv klasörüne göre göreli yol üretir: '527078/2026-0417/xxx.jpg'.

    Tam yol saklanırsa veritabanı başka bir makineye taşındığında
    fotoğraflar bulunamaz. Göreli yol makineden bağımsızdır.
    """
    try:
        return tam.relative_to(arsiv_klasor()).as_posix()
    except ValueError:
        return tam.as_posix()


def tam_yol(kayitli: str) -> Path:
    """Veritabanındaki yolu bu makinedeki gerçek dosyaya çevirir."""
    p = Path(kayitli)
    if p.is_absolute():
        if p.is_file():
            return p                      # eski kayıt, bu makinede duruyor
        # Başka makinede yazılmış tam yol: 'arsiv' sonrasını kurtar
        parcalar = [x.lower() for x in p.parts]
        if "arsiv" in parcalar:
            i = len(parcalar) - 1 - parcalar[::-1].index("arsiv")
            return arsiv_klasor().joinpath(*p.parts[i + 1:])
        return p
    return arsiv_klasor() / p


def imza(p: Path) -> str:
    """Dosyayı benzersiz tanımlar: ad + değiştirilme zamanı + boyut."""
    s = p.stat()
    return f"{p.name}|{int(s.st_mtime)}|{s.st_size}"


def bekleyen_dosyalar():
    """Kaynak klasörde henüz işlenmemiş görüntüler, çekim sırasına göre."""
    klasor = kaynak_klasor()
    if not klasor.is_dir():
        return []

    islenmis = {r["imza"] for r in db.sorgu("SELECT imza FROM kaynak_dosya")}

    bulunan = []
    for p in klasor.iterdir():
        if not p.is_file() or p.suffix.lower() not in UZANTILAR:
            continue
        try:
            bilgi = p.stat()
        except OSError:
            continue
        if bilgi.st_size == 0:
            continue                    # boş dosya (yarım kopyalanmış olabilir)
        im = f"{p.name}|{int(bilgi.st_mtime)}|{bilgi.st_size}"
        if im in islenmis:
            continue
        bulunan.append({"yol": p, "imza": im, "ad": p.name,
                        "zaman": bilgi.st_mtime, "boyut": bilgi.st_size})

    bulunan.sort(key=lambda d: (d["zaman"], d["ad"]))
    return bulunan


def bos_dosyalar():
    """Klasördeki 0 baytlık görüntü dosyaları — kullanıcıya bildirilir."""
    klasor = kaynak_klasor()
    if not klasor.is_dir():
        return []
    bos = []
    for p in klasor.iterdir():
        if not p.is_file() or p.suffix.lower() not in UZANTILAR:
            continue
        try:
            if p.stat().st_size == 0:
                bos.append(p.name)
        except OSError:
            continue
    return sorted(bos)


def dosya_bul(im: str):
    """İmzadan dosyayı bulur. Yol dışarıdan gelmediği için güvenli.

    İmza dosya adı + değiştirilme zamanı + boyuttan üretilir. Dosya
    kopyalandıktan sonra (USB, bulut senkronizasyonu) bu değerler değişebilir;
    o durumda dosya adına göre eşleştirmeye düşülür.
    """
    bekleyenler = bekleyen_dosyalar()
    for d in bekleyenler:
        if d["imza"] == im:
            return d["yol"]

    ad = im.split("|")[0] if "|" in im else im
    for d in bekleyenler:
        if d["ad"] == ad:
            return d["yol"]

    # Kuyrukta yok ama klasörde duruyor olabilir (imza değişmiş ve
    # kaynak_dosya'da kayıtlı) — önizleme için yine de göster.
    klasor = kaynak_klasor()
    if klasor.is_dir():
        aday = klasor / ad
        if aday.is_file() and aday.parent == klasor and aday.suffix.lower() in UZANTILAR:
            return aday
    return None


# ----------------------------------------------------------------- kayıt

def sonraki_sira(cycle_id: int) -> int:
    r = db.tek("SELECT MAX(cycle_sira_no) m FROM specimen WHERE cycle_id=?", (cycle_id,))
    return (r["m"] or 0) + 1


def specimen_olustur(cycle_id: int, cycle_no: str, taraf=None) -> str:
    sira = sonraki_sira(cycle_id)
    sid = f"{cycle_no}-{sira:02d}"
    db.yaz(
        "INSERT INTO specimen (id, lab_id, cycle_id, cycle_sira_no, durum, taraf) "
        "VALUES (?,?,?,?,?,?)",
        (sid, db.LAB_ID, cycle_id, sira, "oosit", taraf or None),
    )
    # Cycle'ın denüdasyon zamanı boşsa ilk oositle birlikte doldur
    c = db.tek("SELECT denudasyon_zamani FROM cycle WHERE id=?", (cycle_id,))
    if not c["denudasyon_zamani"]:
        db.yaz("UPDATE cycle SET denudasyon_zamani=? WHERE id=?",
               (datetime.now().isoformat(" ", "seconds"), cycle_id))
    return sid


def goruntu_bagla(im: str, cycle_id: int, cycle_no: str, specimen_id: str,
                  asama: str, kullanici_id: int):
    """Kaynak dosyayı arşive kopyalar ve veritabanına bağlar.

    Kaynak dosyaya dokunulmaz — kamera klasörü temizlense bile arşiv kalır.
    """
    kaynak = dosya_bul(im)
    if not kaynak:
        return None

    ts = datetime.now()
    klasor = hedef_klasor(cycle_id, cycle_no)
    klasor.mkdir(parents=True, exist_ok=True)

    uzanti = kaynak.suffix.lower()
    kod = ornek_kodu(cycle_id, specimen_id, cycle_no)
    ad = guvenli_ad(f"{kod}_{asama}_{ts.strftime('%Y%m%d-%H%M%S')}") + uzanti
    hedef = klasor / ad
    sayac = 1
    while hedef.exists():                       # aynı saniyede ikinci kare
        hedef = klasor / f"{hedef.stem}-{sayac}{uzanti}"
        sayac += 1

    shutil.copy2(kaynak, hedef)

    gid = db.yaz(
        "INSERT INTO goruntu (lab_id, cycle_id, specimen_id, asama, zaman, "
        "dosya_yolu, orijinal_dosya_adi, kullanici_id, kaynak_imza) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (db.LAB_ID, cycle_id, specimen_id, asama,
         ts.isoformat(" ", "seconds"), goreli_yap(hedef), kaynak.name,
         kullanici_id, im),
    )
    db.yaz(
        "INSERT INTO kaynak_dosya (imza, dosya_adi, cycle_id, goruntu_id, durum, zaman) "
        "VALUES (?,?,?,?,?,?)",
        (im, kaynak.name, cycle_id, gid, "eslesti", ts.isoformat(" ", "seconds")),
    )
    return gid


def atla(im: str, cycle_id: int):
    """Görüntüyü kuyruktan çıkarır, hiçbir oosite bağlamaz."""
    kaynak = dosya_bul(im)
    db.yaz(
        "INSERT OR IGNORE INTO kaynak_dosya (imza, dosya_adi, cycle_id, durum, zaman) "
        "VALUES (?,?,?,?,?)",
        (im, kaynak.name if kaynak else "?", cycle_id, "atlandi",
         datetime.now().isoformat(" ", "seconds")),
    )


def geri_al(goruntu_id: int):
    """Son eşleştirmeyi bozar: arşiv dosyasını siler, kaydı ve kuyruk işaretini kaldırır."""
    g = db.tek("SELECT * FROM goruntu WHERE id=?", (goruntu_id,))
    if not g:
        return
    try:
        tam_yol(g["dosya_yolu"]).unlink(missing_ok=True)
    except OSError:
        pass
    db.yaz("DELETE FROM kaynak_dosya WHERE goruntu_id=?", (goruntu_id,))
    db.yaz("DELETE FROM goruntu WHERE id=?", (goruntu_id,))

    # Bu specimen'in başka görüntüsü yoksa ve hiç olayı yoksa specimen'i de kaldır
    sid = g["specimen_id"]
    if sid:
        kalan = db.tek("SELECT COUNT(*) k FROM goruntu WHERE specimen_id=?", (sid,))["k"]
        olay = db.tek("SELECT COUNT(*) k FROM olay WHERE specimen_id=?", (sid,))["k"]
        if kalan == 0 and olay == 0:
            db.yaz("DELETE FROM specimen WHERE id=?", (sid,))


# ----------------------------------------------------------------- elle yükleme

MAKS_BOYUT = 25 * 1024 * 1024      # 25 MB


def elle_ekle(icerik: bytes, orijinal_ad: str, cycle_id: int, cycle_no: str,
              specimen_id, asama: str, kullanici_id: int):
    """Dışarıdan yüklenen bir görüntüyü arşive yazar ve kaydeder.

    specimen_id None ise görüntü cycle'a bağlı kalır (oosite bağlanmaz).
    Hata durumunda açıklama metni döndürür, başarılıysa None.
    """
    uzanti = Path(orijinal_ad).suffix.lower()
    if uzanti not in UZANTILAR:
        return (f"'{orijinal_ad}' desteklenmeyen bir dosya türü. "
                f"İzin verilenler: {', '.join(sorted(UZANTILAR))}")
    if len(icerik) > MAKS_BOYUT:
        return f"'{orijinal_ad}' çok büyük (en fazla {MAKS_BOYUT // 1024 // 1024} MB)."
    if not icerik:
        return f"'{orijinal_ad}' boş."

    ts = datetime.now()
    klasor = hedef_klasor(cycle_id, cycle_no)
    klasor.mkdir(parents=True, exist_ok=True)

    kod = ornek_kodu(cycle_id, specimen_id, cycle_no)
    ad = guvenli_ad(f"{kod}_{asama}_{ts.strftime('%Y%m%d-%H%M%S')}") + uzanti
    hedef = klasor / ad
    sayac = 1
    while hedef.exists():
        hedef = klasor / f"{hedef.stem}-{sayac}{uzanti}"
        sayac += 1

    hedef.write_bytes(icerik)

    db.yaz(
        "INSERT INTO goruntu (lab_id, cycle_id, specimen_id, asama, zaman, "
        "dosya_yolu, orijinal_dosya_adi, kullanici_id, kaynak) "
        "VALUES (?,?,?,?,?,?,?,?,'elle')",
        (db.LAB_ID, cycle_id, specimen_id, asama,
         ts.isoformat(" ", "seconds"), goreli_yap(hedef), orijinal_ad, kullanici_id),
    )
    return None


def goruntu_sil(goruntu_id: int):
    """Görüntüyü siler. Oosit kaydına dokunmaz.

    Kameradan gelmişse kuyruk işareti de kaldırılır, dosya tekrar
    eşleştirilebilir hale gelir. Arşivdeki kopya silinir.
    """
    g = db.tek("SELECT * FROM goruntu WHERE id=?", (goruntu_id,))
    if not g:
        return None
    try:
        tam_yol(g["dosya_yolu"]).unlink(missing_ok=True)
    except OSError:
        pass
    db.yaz("DELETE FROM kaynak_dosya WHERE goruntu_id=?", (goruntu_id,))
    db.yaz("DELETE FROM goruntu WHERE id=?", (goruntu_id,))
    return g
