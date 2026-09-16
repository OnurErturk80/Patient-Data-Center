# -*- coding: utf-8 -*-
"""Ana ekran simgelerini üretir -> static/ikon_*.png

Bu **programın parçası değil**, tek seferlik bir geliştirme aracı — tıpkı
`formlar_asil/kalip_uret.py` gibi. Simgeler depoda hazır duruyor; yalnızca
tasarım değişirse (ya da ticari sürümde başka bir marka konacaksa) bir kez
çalıştırılır:

    pip install Pillow          # yalnızca bu araç için; programın bağımlılığı değil
    python3 simge_uret.py

Çizim: koyu zemin üzerinde bir oosit — dışta zona halkası, içinde dört
blastomer. 48 pikselde bile ne olduğu anlaşılsın diye sade tutuldu.

Android'in "maskable" simgesi kenarlardan kırpıyor: içerik merkezin
%40'lık dairesinde kalmalı. Buradaki çizim %32'de bitiyor, o yüzden aynı
dosya hem normal hem maskable olarak kullanılabiliyor.
"""
from PIL import Image, ImageDraw

ZEMIN = (14, 22, 32)         # --zemin (v6.72'de koyu tema kalici oldu)
ZONA = (255, 255, 255)
HUCRE = (224, 53, 111)       # --vurgu
KAT = 4                     # once buyuk ciz, sonra kucult: kenarlar puruzsuz


def ciz(olcu: int) -> Image.Image:
    b = olcu * KAT
    g = Image.new("RGB", (b, b), ZEMIN)
    d = ImageDraw.Draw(g)
    o = b / 2

    zona_r = b * 0.30
    kalinlik = max(1, int(b * 0.045))
    d.ellipse([o - zona_r, o - zona_r, o + zona_r, o + zona_r],
              outline=ZONA, width=kalinlik)

    hucre_r = b * 0.097
    kayma = b * 0.107
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x, y = o + dx * kayma, o + dy * kayma
        d.ellipse([x - hucre_r, y - hucre_r, x + hucre_r, y + hucre_r],
                  fill=HUCRE)

    return g.resize((olcu, olcu), Image.LANCZOS)


for olcu in (180, 192, 512):
    ciz(olcu).save(f"static/ikon_{olcu}.png", optimize=True)
    print(f"static/ikon_{olcu}.png")
