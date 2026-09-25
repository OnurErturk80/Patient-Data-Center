"""Klasördeki bütün Access CSV'lerini tek komutla, tarih sırasıyla aktarır (v6.172).

Kullanım (proje klasöründe):
    python3 aktar_toplu.py duzelt=tarih_duzeltme_2019_2023.txt dosya=99:801471

Seçenekler:
    duzelt=<dosya>     düzeltme dosyası; klasördeki bütün `tarih_duzeltme*.txt`
                       dosyaları da kendiliğinden eklenir (v6.173)
    dosya=<eski>:<yeni>  önce bu dosya numarasını değiştirir
                       (`dosya_no_degistir.py`); eski numara kayıtlı değilse
                       ya da yeni numara zaten varsa atlar ve söyler
    klasor=<yol>       CSV'lerin klasörü (varsayılan: bulunduğun klasör)

CSV adları `<ay><yıl>.csv` olmalı (`ocak2019.csv`, `agustos2023.csv`);
etiket adından çıkar (`OCAK2019`), sıra tarih sırası. Her dosya için
`aktar_access.py kaynak=... duzelt=... <dosya>` çalıştırılır (aktarım zaten
idempotent: yarıda kalırsa aynı komut yeniden verilir, bitmiş dosyalar
yalnızca kontrol edilip geçilir). Bir dosya hata verirse durur. Bütün çıktı
`aktar_toplu.log`'a yazılır, ekranda dosya başına bir satır özet.

53 dosya bir saat kadar sürer (her dosyadan sonra bütün FET'ler yeniden
bağlanıyor). Önce yedek alın (Yönetici → Yedekleme → Şimdi yedekle).

Başlamadan önce her dosya `liste` kipinden geçer ve ekrana "kaç tedavi
yazılacak" basılır (v6.173); "AKTAR" ondan sonra sorulur. Yazacak bir şeyi
olmayan dosya (zaten aktarılmış) atlanır, yarıda kalmış bir dosyanın yalnızca
eksik satırları yazılır.
"""

import datetime as _dt
import os
import pathlib
import re
import subprocess
import sys
import tempfile

AYLAR = ["ocak", "subat", "mart", "nisan", "mayis", "haziran", "temmuz",
         "agustos", "eylul", "ekim", "kasim", "aralik"]
_AD = re.compile(r"^(" + "|".join(AYLAR) + r")(\d{4})\.csv$", re.I)
PROJE = pathlib.Path(__file__).resolve().parent


def secenekler(argv):
    s = {"duzelt": None, "dosya": None, "klasor": "."}
    for a in argv:
        if "=" not in a or a.split("=", 1)[0] not in s:
            sys.exit(__doc__)
        k, v = a.split("=", 1)
        s[k] = v
    return s


def dosya_no_adimi(deger):
    eski, _, yeni = deger.partition(":")
    if not (eski.isdigit() and yeni.isdigit()):
        sys.exit("dosya=<eski>:<yeni> -- ikisi de rakam olmalı")
    import dosya_no_degistir as d
    eski, yeni = int(eski), int(yeni)
    if not d._hasta(eski):
        print(f"Dosya no {eski} kayıtlı değil -- değiştirme adımı atlandı "
              f"(daha önce yapılmış olabilir).")
        return
    if d._hasta(yeni):
        sys.exit(f"Dosya no {yeni} zaten kayıtlı, {eski} de duruyor: iki kart var. "
                 "Aktarıma başlamadan önce bu çözülmeli.")
    h, klasor = d.ozet(eski, yeni)
    d.uygula(eski, yeni, h, klasor)


def duzeltmeleri_birlestir(klasor, verilen):
    """Klasördeki bütün `tarih_duzeltme*.txt` + `duzelt=` ile verilen dosya ->
    tek geçici dosyanın yolu (ya da None) ve kullanılan dosyaların adları.

    **Neden hepsi** (v6.173, kliniğin makinesinde): her yılın düzeltmeleri
    ayrı dosyada (`tarih_duzeltme_2023.txt`, `..._2024b.txt`, ...). Araç
    klasördeki her CSV'yi yalnızca verilen TEK dosyayla kontrol ediyordu;
    haziran 2023'ün yer tutucu dosya numarası ("41") 2023'ün dosyasında
    gerçek numarasına çevriliyor, o dosya verilmeyince satır "başka hastanın
    kaydını buluyor" diye çakışma sayıldı ve bütün iş durdu. Birleştirmek
    güvenli: her satır kendi etiketini taşıyor (`HAZIRAN2023#41 ...`),
    `aktar_access.py` yalnızca o dosyanın etiketindeki satırları uyguluyor.
    Aynı satır iki dosyada varsa bir kez yazılıyor; aynı kayda iki dosyada
    FARKLI düzeltme varsa hangisinin doğru olduğu bilinmiyor -- durur.
    """
    yollar = sorted(pathlib.Path(klasor).glob("tarih_duzeltme*.txt"))
    if verilen:
        v = pathlib.Path(verilen)
        if not v.exists():
            sys.exit(f"Düzeltme dosyası yok: {verilen}")
        if v.resolve() not in {y.resolve() for y in yollar}:
            yollar.append(v)
    if not yollar:
        return None, []
    satirlar, anahtarlar = [], {}
    for y in yollar:
        for ham in y.read_text(encoding="utf-8-sig").splitlines():
            satir = ham.strip()
            if not satir or satir.startswith("#"):
                continue
            parca = satir.split()
            anahtar = (parca[0].upper(), parca[1].upper() if len(parca) > 1 else "")
            normal = " ".join(parca)
            if anahtar in anahtarlar:
                onceki, onceki_dosya = anahtarlar[anahtar]
                if onceki != normal:
                    sys.exit(f"{parca[0]} için iki düzeltme dosyasında farklı satır var:\n"
                             f"  {onceki_dosya.name}: {onceki}\n  {y.name}: {normal}\n"
                             "Doğru olmayanı silip komutu yeniden verin.")
                continue
            anahtarlar[anahtar] = (normal, y)
            satirlar.append(normal)
    dosya = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt",
                                        prefix="aktar_toplu_duzeltme_", delete=False)
    with dosya:
        dosya.write("\n".join(satirlar) + "\n")
    return dosya.name, [y.name for y in yollar]


def _calistir(etiket, p, duzelt, liste=False):
    """`aktar_access.py`'yi alt süreçte çalıştırır. -> CompletedProcess.

    **Alt sürecin çıktısı UTF-8'e sabitleniyor** (v6.173). Windows'ta bir
    Python süreci boruya (pipe) konsolun değil sistemin kod sayfasıyla
    yazıyor -- Türkçe Windows'ta cp1254: "ı" 0xFD, "İ" 0xDD. Bu betik UTF-8
    okuyordu ve kliniğin makinesinde ilk dosyada çöktü ("'utf-8' codec can't
    decode byte 0xfd"); Mac'te boru zaten UTF-8 olduğu için görülmemişti.
    Üstelik cp1254'te "→" yok: alt süreç kendisi de o karakteri basarken
    patlayabilirdi. `PYTHONIOENCODING` iki tarafı da UTF-8 yapıyor;
    `errors="replace"` bir baytın özetin okunmasını bir daha durdurmasın diye.
    """
    komut = [sys.executable, str(PROJE / "aktar_access.py")]
    if liste:
        komut.append("liste")
    komut.append(f"kaynak={etiket}")
    if duzelt:
        komut.append(f"duzelt={duzelt}")
    komut.append(str(p.resolve()))
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(komut, input=None if liste else "AKTAR\n",
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=str(PROJE), env=ortam)


def main():
    s = secenekler(sys.argv[1:])
    klasor = pathlib.Path(s["klasor"])
    dosyalar = []
    for p in klasor.iterdir():
        m = _AD.match(p.name)
        if m and int(m.group(2)) >= 2026:
            # 2026'nın ayları yılsız etiketle aktarıldı (`kaynak=MAYIS`);
            # burada MAYIS2026 diye yeniden aktarılsaydı hepsi ikinci kez
            # açılırdı. O dosyalar elle, kendi etiketiyle.
            print(f"{p.name} atlandı: 2026 dosyaları bu araçla aktarılmaz.")
        elif m:
            dosyalar.append((int(m.group(2)), AYLAR.index(m.group(1).lower()), p))
    if not dosyalar:
        sys.exit(f"{klasor.resolve()} içinde <ay><yıl>.csv adında dosya yok.")
    dosyalar.sort()
    duzelt, kullanilan = duzeltmeleri_birlestir(klasor, s["duzelt"])
    try:
        _aktar(s, dosyalar, duzelt, kullanilan)
    finally:
        if duzelt:
            os.unlink(duzelt)


def _aktar(s, dosyalar, duzelt, kullanilan):
    print(f"{len(dosyalar)} dosya, {dosyalar[0][2].name} → {dosyalar[-1][2].name}")
    print("Düzeltme dosyaları: " + (", ".join(kullanilan) if kullanilan else "YOK"))

    # Önce her dosyada ne yazılacağına bak (v6.173). v6.172 hepsini baştan
    # çalıştırıyordu (bitmiş dosya dakikalar sürüyor); v6.173'ün ilk hali
    # "o etiketle tek tedavi varsa bitmiş" sayıyordu -- yarıda kalmış bir
    # dosyanın kalan satırlarını hiç aktarmazdı. Ölçü aracın kendi `liste`'si:
    # "0 tedavi yazılacak" diyen dosya bitmiş.
    print("Dosyalar kontrol ediliyor (dosya başına birkaç saniye)...")
    yapilacak, sorunlu = [], []
    for yil, ay, p in dosyalar:
        etiket = f"{AYLAR[ay].upper()}{yil}"
        sonuc = _calistir(etiket, p, duzelt, liste=True)
        m = re.search(r"(\d+) tedavi yazılacak", sonuc.stdout or "")
        if sonuc.returncode != 0 or not m:
            # Bu dosya aktarılmıyor ama öteki dosyalar durmasın (v6.173):
            # aracın kendi "DUR" mesajı hiçbir şey yazmadığını söylüyor.
            sorunlu.append((etiket, ((sonuc.stdout or "") + (sonuc.stderr or "")).strip()))
            print(f"  {etiket:14} KONTROL EDİLEMEDİ -- aktarılmayacak (aşağıda)")
            continue
        n = int(m.group(1))
        if n:
            yapilacak.append((etiket, p, n))
            print(f"  {etiket:14} {n} tedavi yazılacak")
    atlanan = len(dosyalar) - len(yapilacak) - len(sorunlu)
    if atlanan:
        print(f"  ({atlanan} dosya zaten aktarılmış, atlanacak)")
    for etiket, cikti in sorunlu:
        print(f"\n{etiket} kontrol edilemedi, aktarılmayacak. Aracın mesajı:")
        print(cikti[-1200:])
    if not yapilacak:
        print("Yazılacak bir şey yok, bütün dosyalar zaten aktarılmış.")
        return
    print(f"{len(yapilacak)} dosyada {sum(n for _e, _p, n in yapilacak)} tedavi aktarılacak.")
    if input('Başlamak için "AKTAR" yazın: ').strip() != "AKTAR":
        sys.exit("Vazgeçildi.")
    if s["dosya"]:
        dosya_no_adimi(s["dosya"])

    gunluk = open("aktar_toplu.log", "a", encoding="utf-8")
    gunluk.write(f"\n===== {_dt.datetime.now():%Y-%m-%d %H:%M} — {len(yapilacak)} dosya\n")
    for i, (etiket, p, _n) in enumerate(yapilacak, 1):
        bas = _dt.datetime.now()
        sonuc = _calistir(etiket, p, duzelt)
        cikti, hata = sonuc.stdout or "", sonuc.stderr or ""
        gunluk.write(f"\n--- {etiket} ({p.name})\n{cikti}{hata}\n")
        gunluk.flush()
        ozet = re.search(r"(\d+) tedavi aktarıldı, (\d+) atlandı, (\d+) hata", cikti)
        uyari = cikti.count("UYARI")
        sure = (_dt.datetime.now() - bas).seconds
        if sonuc.returncode != 0 or not ozet:
            print(f"[{i}/{len(yapilacak)}] {etiket}: HATA -- aktar_toplu.log'un sonuna bak. "
                  "Durduruldu; sorun giderilince aynı komut yeniden verilir.")
            print((hata or cikti)[-1500:])
            sys.exit(1)
        print(f"[{i}/{len(yapilacak)}] {etiket}: {ozet.group(1)} aktarıldı, "
              f"{ozet.group(2)} atlandı, {uyari} uyarı, {sure} sn")
    print("Bitti. Uyarıların ayrıntısı aktar_toplu.log'da (UYARI diye ara).")


if __name__ == "__main__":
    main()
