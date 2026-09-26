# -*- coding: utf-8 -*-
"""Kliniğin kendi HTTPS sertifikası -- kütüphanesiz (v6.196).

Neden: Android telefon programı "uygulama gibi" (adres çubuksuz, kendi
penceresinde) ancak güvenli bağlantıda (HTTPS) açıyor. Program klinikte iç
ağda, internete kapalı çalışıyor; bir sertifika kurumundan sertifika
alınamaz (o kurumlar iç ağ adresine -- 192.168.x.x -- sertifika vermiyor).

Çözüm, kliniğe özel küçük bir sertifika zinciri:

- **Kök sertifika** (`kok.crt`): "bu bilgisayarın imzasına güven" demek.
  Her telefona **bir kez** yüklenir, on yıl geçerli. Özel anahtarı
  (`kok.key`) bu bilgisayardan hiç çıkmaz.
- **Sunucu sertifikası** (`sunucu.crt`): bilgisayarın ağ adresi için, kök
  tarafından imzalı. Program her açılışta bakıyor; adres değiştiyse ya da
  süresi dolmak üzereyse **kendiliğinden yeniler** -- telefonlara yeniden bir
  şey yüklemek gerekmez, çünkü telefon köke güveniyor.

Hepsi veri klasöründe `sertifika/` altında (`db.VERI_KOK`). Depoya girmez
(`.gitignore`): kök anahtarı ele geçen, kliniğin telefonlarına sahte bir
"Patient Data Center" gösterebilir.

Kütüphanesiz, çünkü klinikteki makineye kurulum eklemiyoruz (`excel.py`,
`karekod.py`'nin gerekçesi). Gerekenler küçük: RSA anahtarı üretmek (büyük
asal sayı bulmak), SHA-256 ile imzalamak (PKCS#1 v1.5) ve sertifikayı X.509
kurallarıyla (DER) yazmak. Okuma/doğrulama işini Python'un kendi `ssl`
modülü yapıyor -- yazdığımızı OpenSSL'e okutup sınıyoruz.

Telefonların kuralları (yazarken bunlara göre ayarlandı):
- Apple (iOS 13+): RSA en az 2048 bit, SHA-2 imza, adres "Subject
  Alternative Name"de, "serverAuth" kullanım amacı, sunucu sertifikası en
  çok 825 gün. Burada 397 gün, bitmeden 30 gün önce yenileniyor.
- Chrome (Android): adres SAN'da olmalı (ortak ad -- CN -- yetmiyor).

Kullanım (yalnızca kontrol için; program açılışta kendisi çağırıyor):

    python3 sertifika.py            # durumu göster, gerekirse üret/yenile
"""

import base64
import datetime as _dt
import hashlib
import ipaddress
import json
import logging
import os
import secrets
import socket
from pathlib import Path

import db

KLASOR = db.VERI_KOK / "sertifika"
KOK_ANAHTAR = KLASOR / "kok.key"
KOK_SERTIFIKA = KLASOR / "kok.crt"
SUNUCU_ANAHTAR = KLASOR / "sunucu.key"
SUNUCU_SERTIFIKA = KLASOR / "sunucu.crt"
SUNUCU_BILGI = KLASOR / "sunucu.json"

KOK_GUN = 3650          # kök: on yıl -- telefonlara bir kez yükleniyor
SUNUCU_GUN = 397        # Apple'ın 825 gün sınırının güvenle altında
YENILEME_GUN = 30       # bitmesine bu kadar kala açılışta yenilenir
ANAHTAR_BIT = 2048

_g = logging.getLogger("sertifika")


# ------------------------------------------------------------------- RSA

_KUCUK_ASALLAR = [p for p in range(3, 2000, 2)
                  if all(p % q for q in range(3, int(p ** .5) + 1, 2))]


def _asal_mi(n, tur=40):
    """Miller-Rabin. 40 tur: yanılma olasılığı 4^-40, pratikte sıfır."""
    if n < 2:
        return False
    for p in _KUCUK_ASALLAR:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(tur):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _asal(bit, e):
    while True:
        # En üst iki bit 1: iki asalın çarpımı tam 2048 bit olsun.
        n = secrets.randbits(bit) | (3 << (bit - 2)) | 1
        if (n - 1) % e and _asal_mi(n):
            return n


def rsa_anahtar(bit=ANAHTAR_BIT):
    """Yeni RSA anahtarı: sözlük (n, e, d, p, q, dp, dq, qinv)."""
    e = 65537
    while True:
        p = _asal(bit // 2, e)
        q = _asal(bit // 2, e)
        if p == q:
            continue
        n = p * q
        if n.bit_length() != bit:
            continue
        d = pow(e, -1, (p - 1) * (q - 1))
        return {"n": n, "e": e, "d": d, "p": p, "q": q,
                "dp": d % (p - 1), "dq": d % (q - 1), "qinv": pow(q, -1, p)}


def _imzala(anahtar, veri):
    """RSASSA-PKCS1-v1_5, SHA-256. Çin kalan teoremiyle (dört kat hızlı)."""
    ozet = hashlib.sha256(veri).digest()
    t = bytes.fromhex("3031300d060960864801650304020105000420") + ozet
    k = (anahtar["n"].bit_length() + 7) // 8
    em = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    m = int.from_bytes(em, "big")
    p, q = anahtar["p"], anahtar["q"]
    s1 = pow(m, anahtar["dp"], p)
    s2 = pow(m, anahtar["dq"], q)
    s = s2 + q * ((anahtar["qinv"] * (s1 - s2)) % p)
    assert pow(s, anahtar["e"], anahtar["n"]) == m    # imza doğru mu
    return s.to_bytes(k, "big")


# ------------------------------------------------------------ DER (ASN.1)

def _uzunluk(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _tlv(etiket, icerik):
    return bytes([etiket]) + _uzunluk(len(icerik)) + icerik


def _int(n):
    b = n.to_bytes(max(1, (n.bit_length() + 7) // 8), "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return _tlv(0x02, b)


def _seq(*ogeler):
    return _tlv(0x30, b"".join(ogeler))


def _set(*ogeler):
    return _tlv(0x31, b"".join(ogeler))


def _oid(metin):
    s = [int(x) for x in metin.split(".")]
    b = bytes([40 * s[0] + s[1]])
    for x in s[2:]:
        parca = [x & 0x7F]
        x >>= 7
        while x:
            parca.insert(0, 0x80 | (x & 0x7F))
            x >>= 7
        b += bytes(parca)
    return _tlv(0x06, b)


def _bit(b, bos=0):
    return _tlv(0x03, bytes([bos]) + b)


def _oktet(b):
    return _tlv(0x04, b)


def _utf8(s):
    return _tlv(0x0C, s.encode("utf-8"))


def _zaman(t):
    # RFC 5280: 2050'den önce UTCTime, sonra GeneralizedTime.
    if t.year < 2050:
        return _tlv(0x17, t.strftime("%y%m%d%H%M%SZ").encode())
    return _tlv(0x18, t.strftime("%Y%m%d%H%M%SZ").encode())


_NULL = b"\x05\x00"
_SHA256_RSA = _seq(_oid("1.2.840.113549.1.1.11"), _NULL)


def _ad(cn):
    return _seq(
        _set(_seq(_oid("2.5.4.10"), _utf8("Patient Data Center"))),
        _set(_seq(_oid("2.5.4.3"), _utf8(cn))),
    )


def _acik_anahtar_bilgisi(a):
    rsa = _seq(_int(a["n"]), _int(a["e"]))
    return _seq(_seq(_oid("1.2.840.113549.1.1.1"), _NULL), _bit(rsa)), rsa


def _uzanti(oid, deger, kritik=False):
    parcalar = [_oid(oid)]
    if kritik:
        parcalar.append(b"\x01\x01\xff")
    parcalar.append(_oktet(deger))
    return _seq(*parcalar)


def _sertifika(konu, konu_anahtar, veren, veren_anahtar, gun, uzantilar):
    simdi = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
    # Bir saat geriye: telefonun saati biraz gerideyse "henüz geçerli değil"
    # demesin.
    bas = simdi - _dt.timedelta(hours=1)
    son = simdi + _dt.timedelta(days=gun)
    spki, _ = _acik_anahtar_bilgisi(konu_anahtar)
    tbs = _seq(
        _tlv(0xA0, _int(2)),                              # v3
        _int(int.from_bytes(secrets.token_bytes(16), "big") >> 1),
        _SHA256_RSA,
        veren,
        _seq(_zaman(bas), _zaman(son)),
        konu,
        spki,
        _tlv(0xA3, _seq(*uzantilar)),
    )
    imza = _imzala(veren_anahtar, tbs)
    return _seq(tbs, _SHA256_RSA, _bit(imza)), son


def _anahtar_kimligi(a):
    _, rsa = _acik_anahtar_bilgisi(a)
    return hashlib.sha1(rsa).digest()


def kok_uret(makine):
    """Kök (CA) anahtarı ve sertifikası."""
    a = rsa_anahtar()
    kimlik = _anahtar_kimligi(a)
    ad = _ad(f"Patient Data Center Yerel Kok ({makine})")
    der, son = _sertifika(ad, a, ad, a, KOK_GUN, [
        _uzanti("2.5.29.19", _seq(b"\x01\x01\xff"), kritik=True),  # CA: evet
        # digitalSignature + keyCertSign + cRLSign
        _uzanti("2.5.29.15", _bit(b"\x86", 1), kritik=True),
        _uzanti("2.5.29.14", _oktet(kimlik)),
    ])
    return a, der


def sunucu_uret(kok_a, kok_der, adlar, ipler, anahtar=None):
    """Sunucu sertifikası: adresler SAN'da. Anahtar verilirse yeniden
    kullanılır (yenilemede yeni asal aramak gerekmiyor)."""
    a = anahtar or rsa_anahtar()
    kok_tbs_konu = _kok_konusu(kok_der)
    san = b"".join(
        [_tlv(0x82, ad.encode("ascii")) for ad in adlar] +
        [_tlv(0x87, ipaddress.ip_address(ip).packed) for ip in ipler])
    cn = ipler[0] if ipler else adlar[0]
    der, son = _sertifika(_ad(cn), a, kok_tbs_konu, kok_a, SUNUCU_GUN, [
        _uzanti("2.5.29.19", _seq(), kritik=True),                 # CA: hayır
        # digitalSignature + keyEncipherment
        _uzanti("2.5.29.15", _bit(b"\xa0", 5), kritik=True),
        _uzanti("2.5.29.37", _seq(_oid("1.3.6.1.5.5.7.3.1"))),   # serverAuth
        _uzanti("2.5.29.17", _seq(san)),
        _uzanti("2.5.29.14", _oktet(_anahtar_kimligi(a))),
        _uzanti("2.5.29.35", _seq(_tlv(0x80, _anahtar_kimligi(kok_a)))),
    ])
    return a, der, son


# --- kökün "konu" alanını kendi DER'inden okumak (veren = kökün konusu,
# birebir aynı bayt olmalı; yeniden kurmak makine adı değişirse tutmazdı).

def _oku(b, i):
    etiket = b[i]
    n = b[i + 1]
    j = i + 2
    if n & 0x80:
        k = n & 0x7F
        n = int.from_bytes(b[j:j + k], "big")
        j += k
    return etiket, j, j + n        # etiket, içeriğin başı, sonu


def _cocuklar(b, bas, son):
    i = bas
    while i < son:
        _, ib, isn = _oku(b, i)
        yield b[i:isn], ib, isn
        i = isn


def _kok_konusu(der):
    _, b, s = _oku(der, 0)                     # Certificate
    tbs, tb, ts = next(_cocuklar(der, b, s))   # TBSCertificate
    parcalar = [p for p, _, _ in _cocuklar(der, tb, ts)]
    # version[0], serial, sigalg, issuer, validity, subject, ...
    return parcalar[5]


# ------------------------------------------------------------ PEM, dosya

def _pem(tur, der):
    b = base64.b64encode(der).decode()
    satirlar = [b[i:i + 64] for i in range(0, len(b), 64)]
    return f"-----BEGIN {tur}-----\n" + "\n".join(satirlar) + f"\n-----END {tur}-----\n"


def _pem_coz(metin):
    govde = "".join(s for s in metin.strip().splitlines() if not s.startswith("-----"))
    return base64.b64decode(govde)


def _anahtar_der(a):
    return _seq(_int(0), _int(a["n"]), _int(a["e"]), _int(a["d"]), _int(a["p"]),
                _int(a["q"]), _int(a["dp"]), _int(a["dq"]), _int(a["qinv"]))


def _anahtar_oku(yol):
    der = _pem_coz(yol.read_text())
    _, b, s = _oku(der, 0)
    sayilar = []
    for _, ib, isn in _cocuklar(der, b, s):
        sayilar.append(int.from_bytes(der[ib:isn], "big"))
    _, n, e, d, p, q, dp, dq, qinv = sayilar
    return {"n": n, "e": e, "d": d, "p": p, "q": q, "dp": dp, "dq": dq, "qinv": qinv}


def _gizli_yaz(yol, metin):
    """Özel anahtar: yalnızca sahibi okuyabilsin (Windows'ta etkisiz)."""
    yol.write_text(metin)
    try:
        os.chmod(yol, 0o600)
    except OSError:
        pass


# --------------------------------------------------------------- adresler

def yerel_ipler():
    """Bu makinenin iç ağ adresleri. Dışarıya paket gitmiyor (UDP soketinde
    `connect` yalnızca "hangi arayüzden çıkardım" sorusu)."""
    ipler = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ipler.append(s.getsockname()[0])
    except OSError:
        pass
    finally:
        s.close()
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip not in ipler and not ip.startswith("127."):
                ipler.append(ip)
    except OSError:
        pass
    ipler.append("127.0.0.1")
    return ipler


def yerel_adlar():
    ad = socket.gethostname().split(".")[0]
    adlar = ["localhost"]
    try:
        ad.encode("ascii")
        if ad and ad != "localhost":
            adlar += [ad, ad + ".local"]
    except UnicodeEncodeError:            # Türkçe harfli makine adı: DNS'e yazılamaz
        pass
    return adlar


# ------------------------------------------------------------- ana işlev

def durum():
    """Ekran için: kök var mı, sunucu sertifikası hangi adresler için, ne
    zamana kadar. Hiçbir şey üretmez."""
    bilgi = {}
    if SUNUCU_BILGI.exists():
        try:
            bilgi = json.loads(SUNUCU_BILGI.read_text())
        except (OSError, ValueError):
            bilgi = {}
    return {"kok": KOK_SERTIFIKA.exists(), **bilgi}


def hazirla(ipler=None, adlar=None):
    """Sertifikaları hazırlar; gerekirse üretir ya da yeniler.

    Döndürür: (sunucu.crt yolu, sunucu.key yolu). Kök yoksa üretir (ilk
    açılış, birkaç saniye). Sunucu sertifikası yoksa, bu makinenin bugünkü
    adresi sertifikada yoksa ya da bitmesine `YENILEME_GUN`'den az kaldıysa
    yeniden imzalanır; anahtarı korunur.
    """
    KLASOR.mkdir(parents=True, exist_ok=True)
    ipler = ipler or yerel_ipler()
    adlar = adlar or yerel_adlar()

    if not (KOK_ANAHTAR.exists() and KOK_SERTIFIKA.exists()):
        _g.info("HTTPS: kok sertifika uretiliyor (ilk acilis, birkac saniye)...")
        kok_a, kok_der = kok_uret(socket.gethostname().split(".")[0] or "PDC")
        _gizli_yaz(KOK_ANAHTAR, _pem("RSA PRIVATE KEY", _anahtar_der(kok_a)))
        KOK_SERTIFIKA.write_text(_pem("CERTIFICATE", kok_der))
        for eski in (SUNUCU_SERTIFIKA, SUNUCU_BILGI):   # eski kökün imzası geçersiz
            if eski.exists():
                eski.unlink()
    kok_a = _anahtar_oku(KOK_ANAHTAR)
    kok_der = _pem_coz(KOK_SERTIFIKA.read_text())

    bilgi = durum()
    gerek = None
    if not (SUNUCU_SERTIFIKA.exists() and SUNUCU_ANAHTAR.exists()):
        gerek = "yok"
    elif not set(ipler) <= set(bilgi.get("ipler", [])):
        gerek = "adres degisti"
    elif not set(adlar) <= set(bilgi.get("adlar", [])):
        gerek = "makine adi degisti"
    else:
        try:
            son = _dt.datetime.fromisoformat(bilgi["bitis"])
            if son - _dt.datetime.now(_dt.timezone.utc) < _dt.timedelta(days=YENILEME_GUN):
                gerek = "suresi doluyor"
        except (KeyError, ValueError):
            gerek = "bilgi okunamadi"

    if gerek:
        _g.info("HTTPS: sunucu sertifikasi hazirlaniyor (%s): %s",
                gerek, ", ".join(ipler + adlar))
        anahtar = _anahtar_oku(SUNUCU_ANAHTAR) if SUNUCU_ANAHTAR.exists() else None
        a, der, son = sunucu_uret(kok_a, kok_der, adlar, ipler, anahtar)
        if anahtar is None:
            _gizli_yaz(SUNUCU_ANAHTAR, _pem("RSA PRIVATE KEY", _anahtar_der(a)))
        # Zincir: önce sunucu, sonra kök -- telefon köke zaten güveniyor ama
        # bazı istemciler zincirin tamamını görmek istiyor.
        SUNUCU_SERTIFIKA.write_text(_pem("CERTIFICATE", der) + _pem("CERTIFICATE", kok_der))
        SUNUCU_BILGI.write_text(json.dumps({
            "ipler": ipler, "adlar": adlar, "bitis": son.isoformat(),
            "uretildi": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        }, ensure_ascii=False, indent=1))
    return SUNUCU_SERTIFIKA, SUNUCU_ANAHTAR


def kok_der():
    """Telefona indirilecek kök sertifika (DER). Yoksa None."""
    if not KOK_SERTIFIKA.exists():
        return None
    return _pem_coz(KOK_SERTIFIKA.read_text())


def kok_parmak_izi():
    """Kök sertifikanın SHA-256 parmak izi -- telefonda görünenle
    karşılaştırıp doğru sertifikayı yüklediğini görmek için."""
    der = kok_der()
    if not der:
        return ""
    h = hashlib.sha256(der).hexdigest().upper()
    return " ".join(h[i:i + 2] for i in range(0, len(h), 2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    crt, key = hazirla()
    d = durum()
    print("Sertifika klasoru:", KLASOR)
    print("Adresler         :", ", ".join(d.get("ipler", []) + d.get("adlar", [])))
    print("Gecerlilik sonu  :", d.get("bitis", "?")[:10])
    print("Kok parmak izi   :", kok_parmak_izi())
