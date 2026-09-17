"""Göç 035 — goruntu.id ROWID tekrar kullanımını kapatır (AUTOINCREMENT).

Gerçek başa gelen hata: denüdasyon/ICSI'de bir fotoğraf silinip yerine
yenisi eklendiğinde, silinen kayıt tablodaki EN BÜYÜK id ise, SQLite
yeni satıra **aynı id'yi** yeniden veriyor (`INTEGER PRIMARY KEY`
`AUTOINCREMENT` olmadan SQLite'ın standart davranışı budur -- "bir sonraki
id = mevcut en büyük id + 1", en büyüğü silinince o numara boşa çıkar).
`/dosya/{id}` id'yi doğrudan URL'e yazıyor; tarayıcı o id'yi bir kez
gördüyse (o fotoğrafa bakılmışsa) önbelleğe alabiliyor. id yeniden
kullanılınca tarayıcı **eski, silinmiş fotoğrafı** gösterebiliyor --
kullanıcının bildirdiği "yüklediğim resim dışında başka bir resim
yükleniyor" tam olarak bu: 2./3. oosit gibi üzerinde en son çalışılan,
dolayısıyla silinip yeniden eklenmesi en olası kayıtlarda ortaya çıkıyor.

Çözüm `id INTEGER PRIMARY KEY AUTOINCREMENT` -- SQLite bu durumda ayrı bir
sayaç (`sqlite_sequence`) tutuyor ve bir id'yi sildikten sonra asla
yeniden vermiyor. SQLite CHECK/AUTOINCREMENT kısıtı sonradan ALTER ile
eklenemediği için tablo yeniden oluşturuluyor (goc_016/017/031'deki aynı
yöntem). Veri korunur, id'ler AYNEN kalır -- yalnızca bundan sonraki
id üretimi artık geri dönüşsüz.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_035.py
"""

import re
import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)
b.row_factory = sqlite3.Row

sql = b.execute(
    "SELECT sql FROM sqlite_master WHERE type='table' AND name='goruntu'"
).fetchone()["sql"]

if "AUTOINCREMENT" in sql:
    print("goruntu.id zaten AUTOINCREMENT.")
else:
    kolonlar = [r["name"] for r in b.execute("PRAGMA table_info(goruntu)")]
    # Tablo adi tirnakli olabilir (onceki RENAME'den): CREATE TABLE "goruntu" (...)
    yeni_sql = re.sub(r'CREATE TABLE\s+"?goruntu"?', "CREATE TABLE goruntu_yeni",
                      sql, count=1)
    yeni_sql, n = re.subn(
        r"id\s+INTEGER PRIMARY KEY", "id INTEGER PRIMARY KEY AUTOINCREMENT",
        yeni_sql, count=1)
    if n != 1 or "AUTOINCREMENT" not in yeni_sql:
        sys.exit("id kolonu beklenen bicimde degil, elle bakilmali:\n" + sql)

    indeksler = [r["sql"] for r in b.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='goruntu' "
        "AND sql IS NOT NULL")]

    b.execute("PRAGMA foreign_keys=OFF")
    b.execute("BEGIN")
    b.execute(yeni_sql)
    k = ", ".join(kolonlar)
    b.execute(f"INSERT INTO goruntu_yeni ({k}) SELECT {k} FROM goruntu")
    b.execute("DROP TABLE goruntu")
    b.execute("ALTER TABLE goruntu_yeni RENAME TO goruntu")
    for i in indeksler:
        b.execute(i)
    b.execute("COMMIT")
    b.execute("PRAGMA foreign_keys=ON")
    print("goruntu.id artik AUTOINCREMENT -- id'ler bir daha yeniden kullanilmayacak.")

toplam = b.execute("SELECT COUNT(*) FROM goruntu").fetchone()[0]
en_buyuk = b.execute("SELECT COALESCE(MAX(id), 0) FROM goruntu").fetchone()[0]
print(f"\nToplam goruntu: {toplam}, en buyuk id: {en_buyuk}")

kirik = b.execute("PRAGMA foreign_key_check").fetchall()
print(f"Kirik referans: {len(kirik)}")
b.close()
print("\nGoc 035 tamam.")
