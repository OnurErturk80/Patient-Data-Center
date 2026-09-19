"""Göç 040 — hasta.ad_soyad ve hasta.es_adi büyük harfe çevrilir.

Kullanıcının isteği: "Bütün hasta ve eş isimleri büyük harf olsun. Nasıl
yazarsam yazayım sonunda büyük harflerle kaydolsun." Kod tarafı (`app.py`
`tr_buyuk()`, `hasta_kaydet()`/`hasta_guncelle()`/
`sperm_dondurma_yeni_hasta_kaydet()`) artık her kayıtta büyük harfe
çeviriyor; bu göç daha önce girilmiş kayıtları aynı kurala getiriyor.

**Python'un `str.upper()`'ı Türkçe 'i' harfini yanlış çeviriyor**
("Turkish I problem"): varsayılan Unicode kuralı küçük 'i'yi noktasız 'I'
yapar, Türkçe kuralı noktalı 'İ' ister. Aşağıdaki `tr_buyuk()` önce 'i'yi
'İ'ye çevirip SONRA `.upper()` çağırıyor — 'ı' zaten doğru çevriliyor
(Unicode'da 'ı'.upper() == 'I'), ç/ğ/ö/ş/ü'de sorun yok. `app.py`'deki
fonksiyonun birebir kopyası — göç betikleri kendi başına çalışan betikler,
`app.py`'yi import etmiyor (diğer göçlerin de yaptığı gibi).

Birden fazla kez çalıştırılabilir (idempotent — zaten büyük harfli
satırlar atlanıyor).

Kullanım:  python3 goc_040.py
"""

import sqlite3
import sys

import db as _db
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")


def tr_buyuk(deger):
    if deger is None:
        return None
    return deger.replace("i", "İ").upper()


b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

satirlar = b.execute("SELECT id, ad_soyad, es_adi FROM hasta").fetchall()
degisen = 0
for r in satirlar:
    yeni_ad = tr_buyuk(r["ad_soyad"])
    yeni_es = tr_buyuk(r["es_adi"])
    if yeni_ad != r["ad_soyad"] or yeni_es != r["es_adi"]:
        b.execute("UPDATE hasta SET ad_soyad=?, es_adi=? WHERE id=?",
                  (yeni_ad, yeni_es, r["id"]))
        degisen += 1

b.commit()
b.close()
print(f"Goc 040 tamam: {len(satirlar)} hasta tarandi, {degisen} satir "
      "buyuk harfe cevrildi.")
