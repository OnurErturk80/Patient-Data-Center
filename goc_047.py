"""Göç 047 — hastanın tedavileri tarih sırasıyla numaralanıyor (v6.144).

Kullanıcının isteği (2026-09-23): "sonradan eklenen hasta kayıtlarında işlem
tarihi yeni olan son tedavi olarak eklensin. Bir daha aynı hastaya eski
tedavi kaydı eklenirse tarih sırasına göre en eski tedavi 1. tedavi olarak
eklensin. Bu daha sonra hep uygulansın."

"Kaçıncı tedavi" (`hasta_cycle_no`) tedavi açılırken "hastanın en yüksek
numarası + 1" diye veriliyordu -- yeni açılan tedavinin hep en yenisi olduğu
varsayımı. Program öncesi Access kayıtları bu varsayımı bozdu: temmuz dosyası
ağustostan SONRA aktarıldı (v6.141), iki ayda da tedavisi olan hastanın
temmuz tedavisi "2.", ağustos tedavisi "1." oldu.

Numara artık tedavinin işlem gününden hesaplanıyor: `db.tedavileri_sirala()`,
programın kendisinin her kayıtta çağırdığı işlev -- ikinci bir kopya yok.

`cycle.hasta_cycle_no_elle` -- **elle yazılan numara**. Hasta başka merkezde
de tedavi gördüyse embriyolog gerçek deneme sayısını yazabiliyor (README
v0.8); tarih sırası onu ezmemeli. Bu göçten önce elle yazılanla programın
verdiği ayırt edilmiyordu. Bulmanın yolu: program numarayı açılışta "o ana
kadarki en yüksek + 1" diye öneriyordu, yani bir hastanın tedavileri açılış
sırasıyla (kimlik) dizildiğinde bu kurala uymayan numara elle yazılmıştır.
Kural yalnızca kolon İLK eklendiğinde uygulanıyor: sonraki çalıştırmalarda
numaralar artık tarih sırasında, açılış sırasına bakmak onları elle yazılmış
sanardı. Kalıcı silinmiş bir tedavinin bıraktığı boşluk da bu kurala uymaz;
o numara bugünkü haliyle kalır -- bu göçten önce de öyleydi.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_047.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("PRAGMA foreign_keys = ON")

kolonlar = {r[1] for r in b.execute("PRAGMA table_info(cycle)")}
if "hasta_cycle_no_elle" in kolonlar:
    print("cycle.hasta_cycle_no_elle zaten var.")
else:
    b.execute("ALTER TABLE cycle ADD COLUMN hasta_cycle_no_elle INTEGER")
    print("cycle.hasta_cycle_no_elle eklendi.")
    en_yuksek, elle = {}, 0
    for cid, hid, no in b.execute(
            "SELECT id, hasta_id, hasta_cycle_no FROM cycle "
            "ORDER BY hasta_id, id").fetchall():
        m = en_yuksek.get(hid, 0)
        if no is not None and no != m + 1:
            b.execute("UPDATE cycle SET hasta_cycle_no_elle = ? WHERE id = ?",
                      (no, cid))
            elle += 1
        en_yuksek[hid] = max(m, no or 0)
    print(f"{elle} tedavinin numarasi elle yazilmis sayildi, korunuyor.")

hasta = tedavi = 0
for (hid,) in b.execute("SELECT DISTINCT hasta_id FROM cycle").fetchall():
    degisen = _db.tedavileri_sirala(b, hid)
    if degisen:
        hasta += 1
        tedavi += len(degisen)
b.commit()
b.close()
print(f"{hasta} hastanin {tedavi} tedavisi tarih sirasina gore "
      "yeniden numaralandi.")
print("\nGoc 047 tamam.")
