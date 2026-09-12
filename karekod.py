# -*- coding: utf-8 -*-
"""Karekod (QR) üretir — kütüphanesiz, çıktı SVG.

Personel telefonuna programın adresini yazmak yerine karekodu okutuyor.
Kütüphane eklemedik: `excel.py` `.xlsx`'i nasıl kendi yazıyorsa bu da
karekodu kendi çiziyor. Sebep aynı -- klinikteki mini PC'ye kurulum
adımı eklememek (CLAUDE.md "ek bağımlılık yok").

Çıktı **SVG**: resim kütüphanesi gerekmiyor, her boyutta keskin çıkıyor ve
duvara asmak için yazdırılınca da düzgün basılıyor.

Kapsam bilerek dar: **bayt kipi, M düzeltme düzeyi, sürüm 1-10**. Bu 213
karaktere kadar yetiyor; bizim yazdığımız şey `http://klinik-pc:8000`
gibi kısa bir adres. Daha uzunu istenirse `SURUMLER` tablosuna satır
eklenir, kodun gerisi değişmez.

Karekodun nasıl kurulduğu ISO/IEC 18004'te yazılı; buradaki adımlar:
veriyi bitlere çevir -> Reed-Solomon ile düzeltme kodu ekle -> blokları
harmanla -> ızgaraya sabit desenleri koy -> veriyi zikzak yerleştir ->
sekiz maskeden en iyisini seç -> biçim bilgisini yaz.
"""

# --------------------------------------------------------------- tablolar
# Sürüm başına: (düzeltme kodu sayısı, grup1 (blok, veri), grup2 (blok, veri)).
# M düzeyi. Toplam kod sözcüğü = bloklar * (veri + düzeltme).
SURUMLER = {
    1:  (10, (1, 16), None),
    2:  (16, (1, 28), None),
    3:  (26, (1, 44), None),
    4:  (18, (2, 32), None),
    5:  (24, (2, 43), None),
    6:  (16, (4, 27), None),
    7:  (18, (4, 31), None),
    8:  (22, (2, 38), (2, 39)),
    9:  (22, (3, 36), (2, 37)),
    10: (26, (4, 43), (1, 44)),
}

# Hizalama desenlerinin merkezleri (sürüm 1'de yok).
HIZALAMA = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46],
    10: [6, 28, 50],
}


class Hata(Exception):
    pass


# ------------------------------------------------------- Galois alanı (256)
# Reed-Solomon GF(256) üzerinde çalışıyor; çarpma logaritma tablosuyla
# yapılıyor. İlkel polinom 0x11D (standart).
_LOG = [0] * 256
_US = [0] * 512
_x = 1
for _i in range(255):
    _US[_i] = _x
    _LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    _US[_i] = _US[_i - 255]


def _carp(a, b):
    if a == 0 or b == 0:
        return 0
    return _US[_LOG[a] + _LOG[b]]


def _uretec(n):
    """Reed-Solomon üreteç polinomu: (x-a^0)(x-a^1)...(x-a^(n-1))."""
    p = [1]
    for i in range(n):
        yeni = [0] * (len(p) + 1)
        for j, k in enumerate(p):
            yeni[j] ^= _carp(k, 1)
            yeni[j + 1] ^= _carp(k, _US[i])
        p = yeni
    return p


def _duzeltme(veri, n):
    """Veri kod sözcüklerinin düzeltme kodu (n adet)."""
    g = _uretec(n)
    kalan = list(veri) + [0] * n
    for i in range(len(veri)):
        k = kalan[i]
        if k:
            for j, gj in enumerate(g):
                kalan[i + j] ^= _carp(gj, k)
    return kalan[len(veri):]


# ------------------------------------------------------------- veriyi kur
def _surum_sec(uzunluk):
    for s in range(1, 11):
        ec, g1, g2 = SURUMLER[s]
        veri_cw = g1[0] * g1[1] + (g2[0] * g2[1] if g2 else 0)
        sayac_biti = 8 if s < 10 else 16
        if veri_cw * 8 >= 4 + sayac_biti + uzunluk * 8:
            return s
    raise Hata("metin karekoda sığmıyor (en çok 213 karakter)")


def _bit_dizisi(baytlar, surum):
    ec, g1, g2 = SURUMLER[surum]
    veri_cw = g1[0] * g1[1] + (g2[0] * g2[1] if g2 else 0)
    sayac_biti = 8 if surum < 10 else 16

    bitler = "0100"                                   # bayt kipi
    bitler += format(len(baytlar), "0%db" % sayac_biti)
    for b in baytlar:
        bitler += format(b, "08b")

    bitler += "0" * min(4, veri_cw * 8 - len(bitler))  # sonlandırıcı
    bitler += "0" * ((8 - len(bitler) % 8) % 8)        # bayta tamamla

    dolgu = ("11101100", "00010001")                   # 0xEC, 0x11
    i = 0
    while len(bitler) < veri_cw * 8:
        bitler += dolgu[i % 2]
        i += 1
    return [int(bitler[j:j + 8], 2) for j in range(0, len(bitler), 8)]


def _harmanla(kodlar, surum):
    """Blokları böl, her birine düzeltme kodu üret, sonra harmanla."""
    ec, g1, g2 = SURUMLER[surum]
    bloklar, i = [], 0
    for adet, boy in [g1] + ([g2] if g2 else []):
        for _ in range(adet):
            bloklar.append(kodlar[i:i + boy])
            i += boy
    ecler = [_duzeltme(b, ec) for b in bloklar]

    cikti = []
    for j in range(max(len(b) for b in bloklar)):
        for b in bloklar:
            if j < len(b):
                cikti.append(b[j])
    for j in range(ec):
        for e in ecler:
            cikti.append(e[j])
    return cikti


# ------------------------------------------------------------ ızgara kurma
def _bos_izgara(surum):
    n = surum * 4 + 17
    return [[None] * n for _ in range(n)], n


def _sabit_desenler(m, n, surum):
    """Köşe kareleri, zamanlama çizgileri, hizalama desenleri, koyu nokta."""
    def kare(r, c):
        for i in range(-1, 8):
            for j in range(-1, 8):
                if 0 <= r + i < n and 0 <= c + j < n:
                    kenar = i in (0, 6) and 0 <= j <= 6
                    kenar = kenar or (j in (0, 6) and 0 <= i <= 6)
                    ic = 2 <= i <= 4 and 2 <= j <= 4
                    m[r + i][c + j] = 1 if (kenar or ic) else 0

    kare(0, 0); kare(0, n - 7); kare(n - 7, 0)

    for i in range(8, n - 8):                      # zamanlama
        m[6][i] = m[i][6] = 1 if i % 2 == 0 else 0

    merkezler = HIZALAMA[surum]
    for r in merkezler:
        for c in merkezler:
            if (r, c) in ((6, 6), (6, n - 7), (n - 7, 6)):
                continue                            # köşe karelerine girmesin
            for i in range(-2, 3):
                for j in range(-2, 3):
                    kenar = max(abs(i), abs(j))
                    m[r + i][c + j] = 1 if kenar != 1 else 0

    m[n - 8][8] = 0        # her zaman koyu olacak; `_bilgi_yaz` yazıyor

    for i in range(9):                              # biçim bilgisinin yeri
        if m[8][i] is None:
            m[8][i] = 0
        if m[i][8] is None:
            m[i][8] = 0
    for i in range(8):
        if m[8][n - 1 - i] is None:
            m[8][n - 1 - i] = 0
        if m[n - 1 - i][8] is None:
            m[n - 1 - i][8] = 0
    if surum >= 7:                                  # sürüm bilgisinin yeri
        for i in range(6):
            for j in range(3):
                m[n - 11 + j][i] = 0
                m[i][n - 11 + j] = 0


def _yerlestir(m, n, kodlar):
    """Veriyi sağ alttan başlayarak iki sütunluk zikzakla yerleştirir."""
    bitler = "".join(format(k, "08b") for k in kodlar)
    i, yukari, sutun = 0, True, n - 1
    while sutun > 0:
        if sutun == 6:
            sutun -= 1                              # zamanlama sütunu atlanır
        satirlar = range(n - 1, -1, -1) if yukari else range(n)
        for satir in satirlar:
            for d in (0, 1):
                c = sutun - d
                if m[satir][c] is None:
                    m[satir][c] = int(bitler[i]) if i < len(bitler) else 0
                    i += 1
        yukari = not yukari
        sutun -= 2


_MASKELER = (
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
)


def _ceza(m, n):
    """Standardın dört ceza kuralı; en düşük cezalı maske seçiliyor."""
    p = 0
    for dizi in [m, list(zip(*m))]:                 # kural 1: aynı renk dizisi
        for satir in dizi:
            uzunluk, onceki = 1, satir[0]
            for h in list(satir)[1:]:
                if h == onceki:
                    uzunluk += 1
                else:
                    if uzunluk >= 5:
                        p += 3 + uzunluk - 5
                    uzunluk, onceki = 1, h
            if uzunluk >= 5:
                p += 3 + uzunluk - 5

    for r in range(n - 1):                          # kural 2: 2x2 blok
        for c in range(n - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                p += 3

    desen1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]      # kural 3: köşe kare taklidi
    desen2 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    for dizi in [m, [list(s) for s in zip(*m)]]:
        for satir in dizi:
            s = list(satir)
            for i in range(n - 10):
                if s[i:i + 11] in (desen1, desen2):
                    p += 40

    koyu = sum(sum(s) for s in m)                   # kural 4: koyu oranı
    oran = koyu * 100.0 / (n * n)
    p += int(abs(oran - 50) / 5) * 10
    return p


def _bicim_bitleri(maske):
    """5 bit veri (M düzeyi = 00 + maske) + 10 bit BCH, sonra 0x5412 ile XOR."""
    veri = (0 << 3) | maske                          # M düzeyi kodu 00
    d = veri << 10
    for i in range(4, -1, -1):
        if d & (1 << (i + 10)):
            d ^= 0x537 << i
    return ((veri << 10) | d) ^ 0x5412


def _surum_bitleri(surum):
    d = surum << 12
    for i in range(5, -1, -1):
        if d & (1 << (i + 12)):
            d ^= 0x1F25 << i
    return (surum << 12) | d


def _bilgi_yaz(m, n, surum, maske):
    b = _bicim_bitleri(maske)
    for i in range(15):
        bit = (b >> i) & 1
        if i < 6:                      # birinci kopya
            m[i][8] = bit
        elif i == 6:
            m[7][8] = bit
        elif i == 7:
            m[8][8] = bit
        elif i == 8:
            m[8][7] = bit
        else:
            m[8][14 - i] = bit
        if i < 8:                      # ikinci kopya
            m[8][n - 1 - i] = bit
        else:
            m[n - 15 + i][8] = bit
    m[n - 8][8] = 1

    if surum >= 7:
        v = _surum_bitleri(surum)
        for i in range(18):
            bit = (v >> i) & 1
            m[i // 3][n - 11 + i % 3] = bit
            m[n - 11 + i % 3][i // 3] = bit


def izgara(metin: str):
    """Karekodun kendisi: 0/1'lerden kare bir liste."""
    baytlar = metin.encode("utf-8")
    surum = _surum_sec(len(baytlar))
    kodlar = _harmanla(_bit_dizisi(baytlar, surum), surum)

    m, n = _bos_izgara(surum)
    _sabit_desenler(m, n, surum)
    sabit = [[h is not None for h in satir] for satir in m]
    _yerlestir(m, n, kodlar)

    # Ceza **biçim bilgisi yazılmadan** hesaplanıyor: o modüller maskeye göre
    # değişmediği için puanı da değiştirmemeli. Yaygın uygulamalar böyle
    # yapıyor; buradaki seçim onlarla birebir aynı maskeyi buluyor.
    en_iyi, en_iyi_maske, en_iyi_p = None, 0, None
    for maske in range(8):
        aday = [satir[:] for satir in m]
        for r in range(n):
            for c in range(n):
                if not sabit[r][c] and _MASKELER[maske](r, c):
                    aday[r][c] ^= 1
        p = _ceza(aday, n)
        if en_iyi_p is None or p < en_iyi_p:
            en_iyi, en_iyi_maske, en_iyi_p = aday, maske, p
    _bilgi_yaz(en_iyi, n, surum, en_iyi_maske)
    return en_iyi


def svg(metin: str, kenar: int = 4, kutu: int = 8) -> str:
    """Karekodun SVG'si. `kenar` sessiz bölge (en az 4 olmalı, standart)."""
    m = izgara(metin)
    n = len(m)
    olcu = (n + kenar * 2) * kutu
    parcalar = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" shape-rendering="crispEdges" role="img">'
        % (olcu, olcu, olcu, olcu),
        '<rect width="%d" height="%d" fill="#fff"/>' % (olcu, olcu),
    ]
    # Yan yana koyu kareleri tek dikdörtgende birleştirmek SVG'yi kısaltıyor.
    for r in range(n):
        c = 0
        while c < n:
            if m[r][c]:
                bas = c
                while c < n and m[r][c]:
                    c += 1
                parcalar.append(
                    '<rect x="%d" y="%d" width="%d" height="%d" fill="#000"/>'
                    % ((bas + kenar) * kutu, (r + kenar) * kutu,
                       (c - bas) * kutu, kutu))
            else:
                c += 1
    parcalar.append("</svg>")
    return "".join(parcalar)
