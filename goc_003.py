"""Göç 003 — görüntü kuyruğu tablosu ve klasör ayarları.

Mevcut lab.db üzerinde çalışır, veriye dokunmaz.
Birden fazla kez çalıştırılabilir.

Kullanım:
    python goc_003.py
"""

import sqlite3
import sys
from pathlib import Path

KOK = Path(__file__).parent
DB = KOK / "lab.db"

if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)

# Kaynak klasördeki hangi dosyanın işlendiğini takip eder.
# İmza = dosya adı + değiştirilme zamanı + boyut. Aynı isimli farklı dosya
# (kamera sayacı sıfırlanırsa) yeni dosya sayılır.
b.execute("""
CREATE TABLE IF NOT EXISTS kaynak_dosya (
    imza       TEXT PRIMARY KEY,
    dosya_adi  TEXT NOT NULL,
    cycle_id   INTEGER REFERENCES cycle(id),
    goruntu_id INTEGER REFERENCES goruntu(id),
    durum      TEXT NOT NULL,          -- eslesti / atlandi
    zaman      TEXT NOT NULL
)""")

# goruntu tablosuna imza kolonu (geriye izleme icin)
kolonlar = [r[1] for r in b.execute("PRAGMA table_info(goruntu)")]
if "kaynak_imza" not in kolonlar:
    b.execute("ALTER TABLE goruntu ADD COLUMN kaynak_imza TEXT")
    print("goruntu.kaynak_imza eklendi.")

b.commit()

# Klasor ayarlari
VARSAYILAN = {
    "goruntu_kaynak_klasor": r"C:\Users\Genel\Desktop\Patient Data Center\snapshot",
    "goruntu_arsiv_klasor": str(KOK / "arsiv"),
}
for anahtar, deger in VARSAYILAN.items():
    var = b.execute(
        "SELECT deger FROM ayarlar WHERE lab_id=1 AND anahtar=?", (anahtar,)
    ).fetchone()
    if var:
        b.execute("UPDATE ayarlar SET deger=? WHERE lab_id=1 AND anahtar=?",
                  (deger, anahtar))
    else:
        b.execute("INSERT INTO ayarlar (lab_id, anahtar, deger) VALUES (1,?,?)",
                  (anahtar, deger))

b.commit()

print("\nKlasor ayarlari:")
for r in b.execute("SELECT anahtar, deger FROM ayarlar WHERE anahtar LIKE 'goruntu_%'"):
    yol = Path(r[1])
    print(f"  {r[0]}\n    {r[1]}   [{'var' if yol.exists() else 'YOK — olusturulacak'}]")

b.close()

(KOK / "arsiv").mkdir(exist_ok=True)
print("\nGoc 003 tamam.")
