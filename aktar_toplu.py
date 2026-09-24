"""Klasördeki bütün Access CSV'lerini tek komutla, tarih sırasıyla aktarır (v6.172).

Kullanım (proje klasöründe):
    python3 aktar_toplu.py duzelt=tarih_duzeltme_2019_2023.txt dosya=99:801471

Seçenekler:
    duzelt=<dosya>     düzeltme dosyası, her CSV'ye verilir (yoksa verilmez)
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
"""

import datetime as _dt
import pathlib
import re
import subprocess
import sys

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
    duzelt = s["duzelt"]
    if duzelt:
        if not pathlib.Path(duzelt).exists():
            sys.exit(f"Düzeltme dosyası yok: {duzelt}")
        duzelt = str(pathlib.Path(duzelt).resolve())   # alt süreç proje klasöründe çalışıyor
    print(f"{len(dosyalar)} dosya, {dosyalar[0][2].name} → {dosyalar[-1][2].name}"
          + (f", düzeltme: {duzelt}" if duzelt else ", düzeltme dosyası YOK"))
    if input('Başlamak için "AKTAR" yazın: ').strip() != "AKTAR":
        sys.exit("Vazgeçildi.")
    if s["dosya"]:
        dosya_no_adimi(s["dosya"])

    gunluk = open("aktar_toplu.log", "a", encoding="utf-8")
    gunluk.write(f"\n===== {_dt.datetime.now():%Y-%m-%d %H:%M} — {len(dosyalar)} dosya\n")
    for i, (yil, ay, p) in enumerate(dosyalar, 1):
        etiket = f"{AYLAR[ay].upper()}{yil}"
        komut = [sys.executable, str(PROJE / "aktar_access.py"), f"kaynak={etiket}"]
        if duzelt:
            komut.append(f"duzelt={duzelt}")
        komut.append(str(p.resolve()))
        bas = _dt.datetime.now()
        sonuc = subprocess.run(komut, input="AKTAR\n", capture_output=True,
                               text=True, encoding="utf-8", cwd=str(PROJE))
        gunluk.write(f"\n--- {etiket} ({p.name})\n{sonuc.stdout}{sonuc.stderr}\n")
        gunluk.flush()
        ozet = re.search(r"(\d+) tedavi aktarıldı, (\d+) atlandı, (\d+) hata", sonuc.stdout)
        uyari = sonuc.stdout.count("UYARI")
        sure = (_dt.datetime.now() - bas).seconds
        if sonuc.returncode != 0 or not ozet:
            print(f"[{i}/{len(dosyalar)}] {etiket}: HATA -- aktar_toplu.log'un sonuna bak. "
                  "Durduruldu; sorun giderilince aynı komut yeniden verilir.")
            print((sonuc.stderr or sonuc.stdout)[-1500:])
            sys.exit(1)
        print(f"[{i}/{len(dosyalar)}] {etiket}: {ozet.group(1)} aktarıldı, "
              f"{ozet.group(2)} atlandı, {uyari} uyarı, {sure} sn")
    print("Bitti. Uyarıların ayrıntısı aktar_toplu.log'da (UYARI diye ara).")


if __name__ == "__main__":
    main()
