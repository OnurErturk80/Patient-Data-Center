"""Şifre karması ve oturum yönetimi.

Şifreler scrypt ile karmalanır — Python'un standart kütüphanesinde geldiği için
ek paket kurulumu gerekmiyor. Ham şifre hiçbir yerde saklanmaz.
"""

import hashlib
import secrets
from datetime import datetime, timedelta

import db

OTURUM_SURESI_SAAT = 12       # bu süre boyunca işlem yapılmazsa oturum düşer
CEREZ_ADI = "lab_oturum"


# ----------------------------------------------------------------- şifre

def sifrele(sifre: str) -> str:
    """Şifreyi rastgele tuzla karmalar. 'scrypt$tuz$karma' biçiminde döner."""
    tuz = secrets.token_bytes(16)
    karma = hashlib.scrypt(sifre.encode(), salt=tuz, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${tuz.hex()}${karma.hex()}"


def dogrula(sifre: str, kayit: str) -> bool:
    """Girilen şifre kayıtlı karmaya uyuyor mu?"""
    try:
        yontem, tuz_hex, karma_hex = kayit.split("$")
    except (ValueError, AttributeError):
        return False
    if yontem != "scrypt":
        return False
    karma = hashlib.scrypt(
        sifre.encode(), salt=bytes.fromhex(tuz_hex), n=2**14, r=8, p=1, dklen=32
    )
    # secrets.compare_digest zamanlama saldırısına karşı sabit sürede karşılaştırır
    return secrets.compare_digest(karma.hex(), karma_hex)


# ----------------------------------------------------------------- oturum

def giris_yap(kullanici_adi: str, sifre: str):
    """Doğruysa oturum jetonu, yanlışsa None döndürür."""
    k = db.tek(
        "SELECT * FROM kullanici WHERE kullanici_adi = ? AND aktif_mi = 1",
        (kullanici_adi.strip().lower(),),
    )
    if not k or not dogrula(sifre, k["sifre_hash"]):
        return None
    jeton = secrets.token_urlsafe(32)
    simdi = datetime.now().isoformat(" ", "seconds")
    db.yaz(
        "INSERT INTO oturum (jeton, kullanici_id, olusturma, son_erisim) VALUES (?,?,?,?)",
        (jeton, k["id"], simdi, simdi),
    )
    return jeton


def oturumdaki_kullanici(jeton: str):
    """Geçerli oturumsa kullanıcıyı, değilse None döndürür."""
    if not jeton:
        return None
    o = db.tek("SELECT * FROM oturum WHERE jeton = ?", (jeton,))
    if not o:
        return None

    son = datetime.fromisoformat(o["son_erisim"])
    if datetime.now() - son > timedelta(hours=OTURUM_SURESI_SAAT):
        db.yaz("DELETE FROM oturum WHERE jeton = ?", (jeton,))
        return None

    db.yaz(
        "UPDATE oturum SET son_erisim = ? WHERE jeton = ?",
        (datetime.now().isoformat(" ", "seconds"), jeton),
    )
    return db.tek("SELECT * FROM kullanici WHERE id = ?", (o["kullanici_id"],))


def cikis_yap(jeton: str):
    if jeton:
        db.yaz("DELETE FROM oturum WHERE jeton = ?", (jeton,))


# ----------------------------------------------------------------- audit

def degisiklikleri_yaz(tablo, kayit_id, eski, yeni: dict, kullanici_id):
    """Değişen her alan için degisiklik_log'a bir satır yazar.

    eski: veritabanından okunan satır
    yeni: forma girilen değerler
    Değişmeyen alanlar loglanmaz.
    """
    for alan, yeni_deger in yeni.items():
        eski_deger = eski[alan] if alan in eski.keys() else None
        if str(eski_deger or "") == str(yeni_deger or ""):
            continue
        db.yaz(
            "INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
            "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
            (
                db.LAB_ID, tablo, str(kayit_id), alan,
                None if eski_deger is None else str(eski_deger),
                None if yeni_deger is None else str(yeni_deger),
                kullanici_id,
                datetime.now().isoformat(" ", "seconds"),
            ),
        )
