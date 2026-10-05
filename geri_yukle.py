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
(`lab_ONCEKI_<tarih>.db`, yeri `yedek.guvenlik_kopyasi_yolu()`: yedek
klasöründe `veritabani/`) — yanlış yedek seçilirse geri dönülebilsin.

**Yedekler yedek klasöründe `veritabani/`** (v6.248, `yedek.py`'nin belgesi);
eski düzende kalmışlar (klasörün kendisi) da listede.

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
    """Yedek klasöründeki `lab_*.db` dosyaları, yeniden eskiye: `veritabani/`
    (v6.248) ve eski düzende kalmışsa klasörün kendisi; aynı ad iki yerde
    varsa `veritabani/`'ndaki. Her satırın `yol`'u dosyanın kendisi --
    seçilen ad bununla bulunuyor (`yedek_yolu()`), klasöre eklenerek değil.

    `lab_ONCEKI_*.db` (güvenlik kopyaları) da listeye giriyor -- bir önceki
    geri yüklemeden pişman olunursa onlar da seçilebilir olmalı.
    """
    hedef_klasor = Path(hedef_klasor)
    if not hedef_klasor.is_dir():
        return []
    dosyalar, gorulen = [], set()
    for klasor in (yedek.veritabani_klasoru(hedef_klasor), hedef_klasor):
        try:
            adaylar = sorted(klasor.glob("lab_*.db"))
        except OSError:
            continue
        for p in adaylar:
            if p.name not in gorulen and p.is_file():
                gorulen.add(p.name)
                dosyalar.append(p)
    sonuc = []
    for p in dosyalar:
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


def yedek_yolu(hedef_klasor: Path, ad: str):
    """Listedeki adın dosyası ya da None. Seçilen ad yalnızca listeye karşı
    doğrulanıyor: formdan ya da komut satırından gelen metin yola eklenmez
    (`../../lab.db`, tuzak #9'un dosya yolu hali)."""
    for y in yedekleri_listele(hedef_klasor):
        if y["ad"] == ad:
            return y["yol"]
    return None


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
    with yedek.KILIT:
        # Aynı programın otomatik yedeği bu sırada çalışmasın: temizliği ve
        # eski düzenin taşınması seçilen yedeği silmesin, yerinden
        # oynatmasın (v6.248'e kadar `yedek.KILIT`'in yorumu bunu
        # söylüyordu, burada alınmıyordu).
        return _geri_yukle(yedek_dosyasi)


def _geri_yukle(yedek_dosyasi: Path) -> dict:
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
    # Güvenlik kopyası (`lab_ONCEKI_*.db`) yedek klasörüne (`veritabani/`,
    # yoksa veri klasörü; `yedek.guvenlik_kopyasi_yolu()`, v6.248'den beri
    # bütün güvenlik kopyaları için tek yer): başka bir diskte, ve
    # `yedekleri_listele()` orayı taradığı için sonraki bir geri yüklemede
    # seçilebilir. v6.247'ye kadar seçilen yedeğin yanına yazılıyordu --
    # yedek klasöründen seçilince aynı yer.
    onceki_yedek = None
    if db.DB_YOLU.exists():
        onceki_yedek = yedek.guvenlik_kopyasi_yolu()
        _tutarli_kopya(db.DB_YOLU, onceki_yedek)
        yedek.yaz(f"Geri yüklemeden önceki hâl yedeklendi: {onceki_yedek}")

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
            + (f" Önceki hâlin yedeği duruyor: {onceki_yedek}."
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
            # Ad listede aranıyor (`veritabani/` ya da eski düzen, v6.248).
            yol = yedek_yolu(hedef_klasor, dosya)
            if yol is None:
                sys.exit(f"HATA: '{dosya}' yedek klasöründe yok. "
                         "Adları görmek için: python3 geri_yukle.py listele")
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
            print(f"Önceki hâlin yedeği: {sonuc['onceki_yedek']}")
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
