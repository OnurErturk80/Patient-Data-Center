"""Göç 050 — Aktarılmış FET çözmelerinin kayıt sırası (v6.175).

Program "bir örneğin önce dondurulup sonra mı çözüldüğü"nü kayıt kimliğinin
sırasıyla soruyor, saatle değil (saatler elle geri tarihlenebilir, v6.143):
hasta kartının "yeniden dondurma" rozeti, resmî formun "Kalan dondurulmuş"
satırı, çözmeyi / dondurmayı geri alma engelleri.

Access ayları karışık sırayla aktarıldı (2026 önce 2025 sonra, 2019 önce 2018
sonra). Bir FET'in çözmesi yazıldıktan SONRA çözülen tüpün dondurması
aktarıldı ve `aktar_access.py` ikisini aynı embriyoya bağladı: çözmenin
kimliği dondurmanınkinden küçük kaldı. Sonuç: hasta kartı 2018'de dondurulup
2019'da çözülen tüpü "Yeniden donduruldu" diye gösteriyordu, FET'in formu
çözülmüş tüpü tankta sayıyordu. Test veritabanında 342 FET'in 555 çözmesi.

Bu göç o örneklerin çözmeden sonraki olaylarını, saat sırasıyla, yeni
kimlikle yeniden yazıyor (`db.olay_sirasini_duzelt()`); içerik değişmiyor.
Yalnızca aktarımın kendi kayıtları: çözme [Access kaydı] işaretli bir FET'in,
dondurma aktarımın notunu taşıyor. Programdan girilmiş kayda dokunmuyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_050.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("PRAGMA foreign_keys = ON")
try:
    b.execute("BEGIN IMMEDIATE")
    n = _db.olay_sirasini_duzelt(b)
    b.commit()
finally:
    b.close()
print(f"{n} örneğin çözme kaydı sırası düzeltildi.")
