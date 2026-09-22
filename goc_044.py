"""Göç 044 — aktarılmış tedavilerin protokol notundaki "oosit" -> "yumurta".

Kullanıcının isteği (2026-09-22): ekranda "oosit" yazan her yer "Yumurta"
olacak. `aktar_access.py` her aktarılan tedavinin protokol notuna şu cümleyi
yazıyordu:

    Program öncesi Access kaydından aktarıldı; oosit kayıtları toplam
    sayılardan üretildi, tek tek gözlem değildir. [Access kaydı #N]

Bu cümle ekranda (tedavi kartı) ve resmî Embriyoloji Özet formunun NOTLAR
kutusunda basılıyor, yani kullanıcının gördüğü bir metin. Betiğin kendisi
düzeltildi; bu göç **daha önce aktarılmış** kayıtları aynı hale getiriyor.

**Yalnızca betiğin kendi ürettiği paragraf değişiyor.** Notun üstündeki
"Tedavi protokolü (kaynak kayıt): ..." ve Access'ten gelen serbest metin
laboratuvarın kendi kaydı -- oraya dokunulmuyor (orada "OOSİT CRYO" gibi
ifadeler var ve onlar kullanıcının yazdığı şey).

Paragraf yeniden üretiliyor, metin içinde arama/değiştirme yapılmıyor:
`textwrap.fill(..., 68)` satırları 68 karakterde sarıyor ve "oosit" ->
"yumurta" iki karakter uzun, düz değiştirme sarmayı bozardı (uzun satır
NOTLAR kutusunda `white-space: pre` yüzünden kesilir, README v6.130).

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_044.py
"""

import re
import sqlite3
import sys
import textwrap

import db as _db          # veritabanının yeri tek yerde: db.py

# Paragrafın başı: buradan sonrası tamamen betiğin ürettiği metin.
BAS = "Program öncesi Access kaydından aktarıldı;"
# `aktar_access.ISARET` ile aynı kalıp; göçler app/araç import etmiyor.
ISARET = re.compile(r"\[Access kaydı #\d+\]")
YENI = ("Program öncesi Access kaydından aktarıldı; yumurta kayıtları "
        "toplam sayılardan üretildi, tek tek gözlem değildir. ")


def paragraf(eski: str) -> str | None:
    """Notun sonundaki üretilmiş paragrafı yeniden kurar; gerekmiyorsa None."""
    yer = eski.find(BAS)
    if yer < 0:
        return None
    kuyruk = eski[yer:]
    if "oosit" not in kuyruk:          # FET metni ya da zaten düzeltilmiş
        return None
    isaret = ISARET.search(kuyruk)
    if not isaret:                     # işareti olmayan not: dokunma
        return None
    return eski[:yer] + textwrap.fill(YENI + isaret.group(0), 68)


def main():
    if not _db.DB_YOLU.exists():
        sys.exit("lab.db bulunamadi.")

    b = sqlite3.connect(_db.DB_YOLU)
    b.row_factory = sqlite3.Row
    n = 0
    for r in b.execute("SELECT id, protokol_notu FROM cycle "
                       "WHERE protokol_notu LIKE '%Access kaydı #%'"):
        yeni = paragraf(r["protokol_notu"])
        if yeni and yeni != r["protokol_notu"]:
            b.execute("UPDATE cycle SET protokol_notu=? WHERE id=?",
                      (yeni, r["id"]))
            n += 1
    b.commit()
    b.close()
    print(f"Goc 044 tamam. {n} tedavinin protokol notu guncellendi.")


main()
