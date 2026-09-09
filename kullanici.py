"""Kullanıcıları görüntüler, ekler, şifre sıfırlar.

Arayüzde kullanıcı yönetimi ekranı yok (bilinçli — bkz. CLAUDE.md bekleyen iş
4). Şifreler scrypt ile karmalanıyor, geri okunamaz; unutulan şifre
kurtarılamaz, ancak **sıfırlanır**. Bu script o işi elle Python yazmadan
yapmak için.

Kullanım:
    python3 kullanici.py                    kullanıcıları listele
    python3 kullanici.py sifre <kullanici>  şifresini değiştir
    python3 kullanici.py yeni               yeni kullanıcı ekle
    python3 kullanici.py aktif <kullanici>  girişe tekrar izin ver
    python3 kullanici.py pasif <kullanici>  girişi kapat (kayıtları durur)

Windows'ta `python kullanici.py`.

Şifre karması hiçbir zaman ekrana yazılmaz.
"""

import getpass
import sys

import db
import guvenlik

MIN_UZUNLUK = 8


def kullanicilar():
    return db.sorgu(
        "SELECT id, kullanici_adi, ad_soyad, kisa_kod, rol, aktif_mi, "
        "olusturma_zamani FROM kullanici WHERE lab_id = ? "
        "ORDER BY aktif_mi DESC, kullanici_adi", (db.LAB_ID,))


def bul(kadi: str):
    """Kullanıcı adı her zaman küçük harf saklanır (`giris_yap` da öyle arar)."""
    return db.tek("SELECT * FROM kullanici WHERE lab_id = ? AND kullanici_adi = ?",
                  (db.LAB_ID, kadi.strip().lower()))


def listele():
    kayitlar = kullanicilar()
    if not kayitlar:
        print("Hic kullanici yok. Eklemek icin:  python3 kullanici.py yeni")
        return
    print(f"{len(kayitlar)} kullanici:\n")
    print(f"  {'kullanici adi':<18}{'ad soyad':<24}{'kod':<6}{'rol':<12}durum")
    print("  " + "-" * 68)
    for k in kayitlar:
        durum = "aktif" if k["aktif_mi"] else "PASIF - giris yapamaz"
        print(f"  {k['kullanici_adi']:<18}{k['ad_soyad']:<24}"
              f"{k['kisa_kod']:<6}{k['rol']:<12}{durum}")
    print("\nGiris yapilamiyorsa sebep ucunden biridir:")
    print("  1. kullanici adi yukaridakilerden biri degil (buyuk/kucuk harf onemsiz)")
    print("  2. kullanici PASIF")
    print("  3. sifre yanlis  ->  python3 kullanici.py sifre <kullanici adi>")


def _sifre_sor() -> str:
    """Şifreyi iki kez sorar. Ekranda görünmez — boş görünmesi normaldir."""
    while True:
        s1 = getpass.getpass(f"  Yeni sifre (en az {MIN_UZUNLUK}): ")
        s2 = getpass.getpass("  Tekrar                  : ")
        if s1 != s2:
            print("  Sifreler ayni degil, tekrar dene.")
        elif len(s1) < MIN_UZUNLUK:
            print(f"  En az {MIN_UZUNLUK} karakter olmali.")
        else:
            return s1


def sifre_degistir(kadi: str):
    k = bul(kadi)
    if not k:
        sys.exit(f"'{kadi}' diye bir kullanici yok. Listelemek icin: "
                 "python3 kullanici.py")
    print(f"{k['ad_soyad']} ({k['kullanici_adi']}) icin yeni sifre:")
    yeni = _sifre_sor()
    db.yaz("UPDATE kullanici SET sifre_hash = ? WHERE id = ?",
           (guvenlik.sifrele(yeni), k["id"]))

    # Eski oturumlar dusurulur: sifre degistiyse acik kalan tarayicilar da
    # kapanmali, yoksa "sifreyi degistirdim" yanilticidir.
    silinen = db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (k["id"],))
    print(f"\nSifre degistirildi: {k['kullanici_adi']}")
    print("Acik oturumlar kapatildi, herkes yeniden giris yapacak.")
    if not k["aktif_mi"]:
        print("\nUYARI: bu kullanici PASIF, sifre dogru olsa da giris yapamaz.")
        print(f"  Acmak icin: python3 kullanici.py aktif {k['kullanici_adi']}")


def yeni_kullanici():
    ad = input("  Ad soyad      : ").strip()
    if not ad:
        sys.exit("Ad soyad bos olamaz.")
    kod = (input("  Kisa kod (ON) : ").strip() or ad[:2]).upper()
    kadi = input("  Kullanici adi : ").strip().lower()
    if not kadi:
        sys.exit("Kullanici adi bos olamaz.")
    if bul(kadi):
        sys.exit(f"'{kadi}' zaten var. Sifresini degistirmek icin: "
                 f"python3 kullanici.py sifre {kadi}")
    rol = input("  Rol (embriyolog) : ").strip() or "embriyolog"
    sifre = _sifre_sor()
    db.yaz("INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, "
           "kullanici_adi, sifre_hash) VALUES (?,?,?,?,?,?)",
           (db.LAB_ID, ad, kod, rol, kadi, guvenlik.sifrele(sifre)))
    print(f"\nKullanici olusturuldu: {kadi}")


def durum_degistir(kadi: str, aktif: bool):
    k = bul(kadi)
    if not k:
        sys.exit(f"'{kadi}' diye bir kullanici yok.")
    db.yaz("UPDATE kullanici SET aktif_mi = ? WHERE id = ?",
           (1 if aktif else 0, k["id"]))
    if not aktif:
        db.yaz("DELETE FROM oturum WHERE kullanici_id = ?", (k["id"],))
        print(f"{k['kullanici_adi']} pasif yapildi, acik oturumlari kapatildi.")
        print("Girdigi kayitlar duruyor - kullanici silinmedi.")
    else:
        print(f"{k['kullanici_adi']} tekrar giris yapabilir.")


def main():
    if not db.DB_YOLU.exists():
        sys.exit(f"lab.db bulunamadi: {db.DB_YOLU}\n"
                 "Bu scripti proje klasorunde calistir.")

    komut = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if not komut:
        listele()
    elif komut == "yeni":
        yeni_kullanici()
    elif komut in ("sifre", "aktif", "pasif"):
        if not arg:
            sys.exit(f"Kullanici adi eksik.  python3 kullanici.py {komut} <kullanici>")
        if komut == "sifre":
            sifre_degistir(arg)
        else:
            durum_degistir(arg, komut == "aktif")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
