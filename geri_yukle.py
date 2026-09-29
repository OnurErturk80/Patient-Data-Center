"""Yedekten geri yükleme — `/klasorler` panelindeki "Geri yükle" düğmesinin
mantığı (v6.120, kullanıcının isteği: "Yönetici isterse yedekten geri
çağırsın... hastalar tedaviler her şey tekrar yerleşsin").

`tasi.py`'nin USB'den **içeri** alırken kullandığı aynı desen: veritabanını
canlı `lab.db`'nin üzerine değil, önce bir **geçici dosyaya** kopyala (SQLite
backup API ile — düz kopya WAL modunda yarım/boş çıkar, README v6.16), eski
`-wal`/`-shm` yardımcı dosyalarını sil, sonra **atomik `Path.replace()`** ile
takas et. Yarım kalan bir kopya asla canlı veritabanının yerine geçmez —
takas ya tam olur ya hiç olmaz.

**Değiştirmeden önce mevcut veritabanının güvenlik kopyası otomatik alınır**
(`lab_ONCEKI_<tarih>.db`, `tasi.py`'nin aynı adlandırması) — yanlış yedek
seçilirse geri dönülebilsin.

**Takastan hemen sonra eksik veritabanı güncellemeleri uygulanır** (v6.145,
`_gocleri_uygula()`): yedek eski bir sürümden olabilir, program yeniden
açılmayı beklemesin (CLAUDE.md tuzak #15).

Uygulama çalışırken de güvenli **olması beklenir**: `db.baglan()` her
istekte kendi bağlantısını açıp kapatıyor (kalıcı bir bağlantı havuzu yok),
o yüzden takas anında açık bir dosya tutamacı genelde olmaz. Yine de tam o
anda süren bir istek varsa (Windows'ta özellikle) `Path.replace()`
başarısız olabilir — `tasi.py`'deki aynı `OSError` yakalaması burada da var,
hata "programı durdurup tekrar dene" diyor, güvenlik kopyası korunuyor,
canlı veritabanına hiç dokunulmamış oluyor.

**Arşivdeki fotoğraflar geri alınmıyor** — `yedek.arsiv_yedekle()`
hedeften hiçbir şey silmiyor (yalnızca birikimli kopyalıyor), yani "şu
yedeğin arşiv anlık görüntüsü" diye bir şey yok; geri yüklenen eski
veritabanı, aradan silinmiş bir fotoğrafa hâlâ işaret edebilir. Bu bilinçli
bir sınır (README v6.120) — fotoğraf dosyaları kendi başına asla
silinmiyor/üzerine yazılmıyor olduğu için risk yalnızca "bozuk bağlantı",
veri kaybı değil.

Kullanım (terminalden, uygulama olmadan da çalışır — `kullanici.py`'nin
"yönetici de kilitlenirse" felsefesinin aynısı):
    python3 geri_yukle.py listele
    python3 geri_yukle.py geri-yukle <yedek_dosyasi.db>
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import db
import goc
import yedek

DB_ADI = "lab.db"


def yedekleri_listele(hedef_klasor: Path) -> list:
    """`yedek_klasor`'deki `lab_*.db` dosyalarını yeniden eskiye sıralar.

    `lab_ONCEKI_*.db` (güvenlik kopyaları) da listeye giriyor -- bir önceki
    geri yüklemeden pişman olunursa onlar da seçilebilir olmalı.
    """
    if not hedef_klasor.is_dir():
        return []
    sonuc = []
    for p in sorted(hedef_klasor.glob("lab_*.db")):
        ad = p.stem[4:]           # "lab_" sonrası
        tarih = None
        for kalip in ("%Y%m%d_%H%M", "%Y%m%d_%H%M%S"):
            try:
                tarih = datetime.strptime(ad, kalip)
                break
            except ValueError:
                continue
        sonuc.append({
            "ad": p.name, "yol": p,
            "boyut_mb": p.stat().st_size / 1024 / 1024,
            "tarih": tarih,
            "onceki_mi": p.name.startswith("lab_ONCEKI_"),
        })
    sonuc.sort(key=lambda s: s["tarih"] or datetime.min, reverse=True)
    return sonuc


def _tutarli_kopya(kaynak: Path, hedef: Path):
    """SQLite backup API ile kopya — `tasi.py`'nin `tutarli_kopya()`'sının
    aynısı, iki kopya olmasın diye buraya da yazıldı (küçük, tek dosyalı
    modüller arası paylaşım burada bir fonksiyon dosyası kadar değmiyordu)."""
    k = sqlite3.connect(f"file:{kaynak}?mode=ro", uri=True)
    h = sqlite3.connect(hedef)
    with h:
        k.backup(h)
    k.close()
    sonuc = h.execute("PRAGMA integrity_check").fetchone()[0]
    h.close()
    if sonuc != "ok":
        hedef.unlink(missing_ok=True)
        raise RuntimeError(f"Kopya doğrulanamadı ({sonuc}).")


def geri_yukle(yedek_dosyasi: Path) -> dict:
    """Verilen yedeği canlı veritabanının yerine geçirir.

    Dönen sözlük: {"onceki_yedek": Path, "hasta": int, "cycle": int, ...}
    (yeni durumun sayıları — ekrana "şunlar geri geldi" diye basmak için).
    """
    if not yedek_dosyasi.is_file():
        raise RuntimeError(f"Yedek dosyası bulunamadı: {yedek_dosyasi}")

    # Önce yedeğin kendisi bozuk mu diye bak -- bozuk bir dosyayı canlıya
    # taşımadan önce yakala.
    kaynak = sqlite3.connect(f"file:{yedek_dosyasi}?mode=ro", uri=True)
    try:
        sonuc = kaynak.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        kaynak.close()
    if sonuc != "ok":
        raise RuntimeError(f"Seçilen yedek bozuk görünüyor ({sonuc}), "
                           "geri yüklenmedi.")

    kok = db.VERI_KOK
    # Güvenlik kopyası (`lab_ONCEKI_*.db`) `yedek_dosyasi.parent`'a, yani
    # seçilen yedeğin bulunduğu **yedek klasörüne** yazılıyor -- `tasi.py`
    # kendi ONCEKI'sini VERI_KOK'a (canlı veritabanıyla aynı diske) yazıyor,
    # ama orada gerekçe farklı ("bu makinede hemen geri alınacak, USB
    # taşıma hatası"). Buradaki güvenlik kopyası `yedek_klasor`'ün "başka
    # bir diskte olmalı" kuralından (metinler.py `yedek_klasor_ipucu`) aynı
    # şekilde faydalanmalı, ayrıca `yedekleri_listele()`'nin taradığı yer de
    # `yedek_klasor` olduğu için ONCEKI dosyası sonraki bir geri yüklemede
    # de seçilebilir listede görünsün diye buraya yazılıyor.
    onceki_yedek = None
    if db.DB_YOLU.exists():
        onceki_yedek = (yedek_dosyasi.parent
                        / f"lab_ONCEKI_{datetime.now():%Y%m%d_%H%M%S}.db")
        _tutarli_kopya(db.DB_YOLU, onceki_yedek)
        yedek.yaz(f"Geri yüklemeden önceki hâl yedeklendi: {onceki_yedek.name}")

    gecici = kok / (DB_ADI + ".geri-yukleniyor")
    _tutarli_kopya(yedek_dosyasi, gecici)

    # WAL yardımcı dosyaları ESKİ veritabanına ait -- kalırsa yeni dosyanın
    # içeriğiyle uyuşmayan sayfalar yeniden oynatılmaya çalışılır (tasi.py'nin
    # aynı önlemi, README v6.16).
    for uz in ("-wal", "-shm"):
        (kok / (DB_ADI + uz)).unlink(missing_ok=True)

    try:
        gecici.replace(db.DB_YOLU)
    except OSError as e:
        gecici.unlink(missing_ok=True)
        raise RuntimeError(
            f"Veritabanı değiştirilemedi ({e}). Program tam o anda bir "
            "istek işliyor olabilir -- tekrar dene; sürerse programı "
            "durdurup terminalden 'python3 geri_yukle.py geri-yukle "
            f"{yedek_dosyasi.name}' çalıştır."
            + (f" Önceki hâlin yedeği duruyor: {onceki_yedek.name}."
               if onceki_yedek else ""))

    # Yedek eski bir sürümden olabilir: açılışta olanı şimdi yap (v6.145).
    goc_sonucu = _gocleri_uygula()

    b = sqlite3.connect(f"file:{db.DB_YOLU}?mode=ro", uri=True)
    try:
        sayilar = {}
        for tablo in ("hasta", "cycle", "specimen", "goruntu"):
            try:
                sayilar[tablo] = b.execute(
                    f"SELECT COUNT(*) FROM {tablo}").fetchone()[0]
            except sqlite3.Error:
                sayilar[tablo] = None
    finally:
        b.close()

    yedek.yaz(f"Geri yüklendi: {yedek_dosyasi.name} -> {db.DB_YOLU.name}  "
             f"({sayilar.get('hasta')} hasta, {sayilar.get('cycle')} cycle, "
             f"{sayilar.get('specimen')} örnek, {sayilar.get('goruntu')} "
             "fotoğraf)")
    return {"onceki_yedek": onceki_yedek, **sayilar, "goc": goc_sonucu}


def _gocleri_uygula() -> dict:
    """Geri yüklenen veritabanına eksik güncellemeleri uygular (v6.145).

    Kullanıcının isteği: "Geri yüklemeden sonra da kendisi yapsın." Göçler
    yalnızca açılışta çalışıyordu; eski bir yedek geri yüklenince program
    yeniden açılana kadar yeni kolonlara dayanan ekranlar "no such column"
    ile hata veriyordu (denendi: v6.143 öncesi bir yedekte FET'in
    vitrifikasyon ekranı). Çalıştırıcı açılıştakinin aynısı, süreç içinde:
    `goc.calistir()` -- `subprocess` yazma, paketlenmiş programda o satır
    göçü değil programı yeniden başlatır.

    Sonra saklanmış kolon/tablo cevapları unutuluyor (`db.sema_bilgisini_unut`,
    tuzak #15) -- ekrandan geri yükleme programın kendi sürecinde çalışıyor,
    terminalden çalışınca zararsız. Bir göç patlarsa geri yükleme yine tamam
    sayılır (yedek yerinde, önceki hâlin kopyası duruyor); hata sonuçta,
    ekran ve Yönetici paneli onu gösteriyor.
    """
    try:
        sonuc = goc.calistir()
    except Exception as e:                 # geri yükleme yine tamam sayılsın
        sonuc = {"calisti": [], "hatali": [("geri_yukleme", repr(e))],
                 "bekleyen": [], "elle": [], "atlandi": ""}
    db.sema_bilgisini_unut()
    if sonuc.get("calisti"):
        yedek.yaz(f"Geri yüklenen veritabanına {len(sonuc['calisti'])} "
                  f"güncelleme uygulandı: {', '.join(sonuc['calisti'])}")
    for ad, _mesaj in sonuc.get("hatali", []):
        yedek.yaz(f"Geri yüklenen veritabanında güncelleme uygulanamadı: {ad}")
    return sonuc


def main():
    yedek.EKRANA = True           # terminalde yedek.log satırları ekrana da
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    komut = sys.argv[1]
    hedef_klasor = Path(db.ayar("yedek_klasor", "")) if db.ayar(
        "yedek_klasor", "") else None

    if komut == "listele":
        if not hedef_klasor:
            sys.exit("HATA: yedek klasörü tanımlı değil.")
        for y in yedekleri_listele(hedef_klasor):
            print(f"  {y['ad']}  ({y['boyut_mb']:.1f} MB)"
                 f"{'  [önceki hâl yedeği]' if y['onceki_mi'] else ''}")
        return

    if komut == "geri-yukle":
        if len(sys.argv) < 3:
            sys.exit("Kullanım: python3 geri_yukle.py geri-yukle <dosya adı>")
        dosya = sys.argv[2]
        yol = Path(dosya)
        if not yol.is_absolute():
            if not hedef_klasor:
                sys.exit("HATA: yedek klasörü tanımlı değil, tam yol ver.")
            yol = hedef_klasor / dosya
        onay = input(
            f"'{yol.name}' canlı veritabanının ({db.DB_YOLU}) üzerine "
            "yazılacak. Bu geri alınamaz bir işlem (bir güvenlik kopyası "
            "alınacak). Devam etmek için GERİ YÜKLE yaz: ")
        if onay.strip().upper() != "GERİ YÜKLE":
            sys.exit("İptal edildi. Hiçbir şey değişmedi.")
        sonuc = geri_yukle(yol)
        print(f"Tamam. {sonuc['hasta']} hasta, {sonuc['cycle']} cycle, "
             f"{sonuc['specimen']} örnek, {sonuc['goruntu']} fotoğraf.")
        if sonuc["onceki_yedek"]:
            print(f"Önceki hâlin yedeği: {sonuc['onceki_yedek'].name}")
        g = sonuc["goc"]
        if g.get("calisti"):
            print(f"Yedek eski bir sürümdendi: {len(g['calisti'])} veritabanı "
                  f"güncellemesi uygulandı ({', '.join(g['calisti'])}).")
        for ad, mesaj in g.get("hatali", []):
            print(f"UYARI: güncelleme uygulanamadı: {ad}\n{mesaj}")
        return

    sys.exit(__doc__)


if __name__ == "__main__":
    main()
