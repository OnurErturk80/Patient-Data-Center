"""Göç 058 — PGT: tedavinin işareti, biyopsi ve genetik sonuçlar (v6.225).

Kullanıcının anlatımı (2026-09-29): "Bazı hastalarda PGT yapılıyor.
Tedavinin başında PGT yapılacağına dair laboratuvarda formunun üstüne
yazıyorum. Tedavi bitene kadar üstünde PGT yapılacağı yazıyor. Bu hastanın
oluşursa embriyolarından biyopsi yapıyorum ve parçaları genetiğe
gönderiyorum. Embriyoları numaralandırıp dondurup saklıyorum. Daha sonra
genetik sonuç gelince sonucu dosyasına koyup hangi embriyolar genetik
incelemede sorunsuz çıkarsa onu belirleyip FET tedavisinde ona bakıp
sorunsuz embriyoları transfer ediyorum." Cevapları: biyopsi blastokistte
(trofektoderm); numara biyopsi sırasıyla 1'den ("PGT 1"); PGT-A, PGT-M,
PGT-SR ve HLA'nın hepsi olabiliyor; "sorunsuz" kararını kendisi işaretliyor.

Şemanın ilk sürümünden beri `olay.tip='biyopsi'` (`biy_tip`,
`biy_tup_etiketi`, `biy_sonuc`) ve `pgt_sonuc` tablosu hazırdı, hiç
kullanılmamıştı. Bu göç yalnızca eksiklerini ekliyor:

- `cycle.pgt_testleri`: PGT yapılacak tedavinin testleri, `pgt_testi`
  listesinin kodları virgülle ("pgt_a,pgt_m"); boş (NULL) = PGT yok.
  `cycle.pgt_notu`: hastalık, translokasyon, genetik laboratuvarı gibi kısa
  not. Okuyan ve yazan tek yer `db.pgt_oku()` / `db.pgt_yaz()`.
- `pgt_sonuc.biyopsi_id`: sonuç hangi biyopsinin. Bir embriyo yeniden
  biyopsiye alınabiliyor (sonuç çıkmadıysa, başka bir tedavide çözülüp);
  her biyopsinin kendi numarası ve sonucu var, örnek kimliği yetmiyor.
- Listeler: `pgt_testi` (PGT-A, PGT-M, PGT-SR, HLA) ve PGT-A dışındaki
  testlerin sonuçları (`pgt_m_sonuc`, `pgt_sr_sonuc`, `hla_sonuc`). PGT-A
  sonuçları şemanın kendi `pgt_sonuc` listesi (Öploid, Anöploid, Mozaik,
  Sonuç yok, No-call); eski kurulumda eksikse ekleniyor.
- `goruntu_asama` listesine "Biyopsi" (blastokistten sonra): biyopsi
  ekranının fotoğrafları.
- `idx_olay_biyopsi`: yalnızca biyopsi satırlarının dizini (kısmi dizin);
  öteki sorguların planına dokunmuyor.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_058.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB)


def kolon_ekle(tablo, kolon, tanim):
    if kolon in [r[1] for r in b.execute(f"PRAGMA table_info({tablo})")]:
        print(f"{tablo}.{kolon} zaten var.")
        return
    b.execute(f"ALTER TABLE {tablo} ADD COLUMN {kolon} {tanim}")
    print(f"{tablo}.{kolon} eklendi.")


kolon_ekle("cycle", "pgt_testleri", "TEXT")
kolon_ekle("cycle", "pgt_notu", "TEXT")
kolon_ekle("pgt_sonuc", "biyopsi_id", "INTEGER REFERENCES olay(id)")

LISTELER = {
    "pgt_testi": [("pgt_a", "PGT-A"), ("pgt_m", "PGT-M"), ("pgt_sr", "PGT-SR"),
                  ("hla", "HLA")],
    "pgt_sonuc": [("oploid", "Öploid"), ("anoploid", "Anöploid"),
                  ("mozaik", "Mozaik"), ("sonuc_yok", "Sonuç yok"),
                  ("no_call", "No-call")],
    "pgt_m_sonuc": [("saglam", "Sağlam"), ("tasiyici", "Taşıyıcı"),
                    ("etkilenmis", "Etkilenmiş"), ("sonuc_yok", "Sonuç yok")],
    "pgt_sr_sonuc": [("dengeli", "Dengeli"), ("dengesiz", "Dengesiz"),
                     ("sonuc_yok", "Sonuç yok")],
    "hla_sonuc": [("uyumlu", "Uyumlu"), ("uyumsuz", "Uyumsuz"),
                  ("sonuc_yok", "Sonuç yok")],
}
for liste, degerler in LISTELER.items():
    son_sira = b.execute(
        "SELECT COALESCE(MAX(sira), -1) FROM liste_degeri "
        "WHERE lab_id=1 AND liste_adi=?", (liste,)).fetchone()[0]
    for kod, etiket in degerler:
        if b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                     "AND liste_adi=? AND kod=?", (liste, kod)).fetchone():
            continue
        son_sira += 1
        b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
                  "VALUES (1,?,?,?,?)", (liste, kod, etiket, son_sira))
        print(f"  + {liste}: {kod} ({etiket})")

# "Biyopsi" fotoğrafı blastokistin arkasında: sonrakiler bir sıra kayıyor.
# Laboratuvarın düzenlediği etiketlere dokunulmuyor (goc_014'ün aksine).
if not b.execute("SELECT 1 FROM liste_degeri WHERE lab_id=1 "
                 "AND liste_adi='goruntu_asama' AND kod='biyopsi'").fetchone():
    r = b.execute("SELECT sira FROM liste_degeri WHERE lab_id=1 "
                  "AND liste_adi='goruntu_asama' AND kod='blastokist'").fetchone()
    if r:
        sira = r[0] + 1
        b.execute("UPDATE liste_degeri SET sira = sira + 1 WHERE lab_id=1 "
                  "AND liste_adi='goruntu_asama' AND sira >= ?", (sira,))
    else:
        sira = b.execute("SELECT COALESCE(MAX(sira), -1) + 1 FROM liste_degeri "
                         "WHERE lab_id=1 AND liste_adi='goruntu_asama'").fetchone()[0]
    b.execute("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
              "VALUES (1,'goruntu_asama','biyopsi','Biyopsi',?)", (sira,))
    print("  + goruntu_asama: biyopsi (Biyopsi)")

if b.execute("SELECT 1 FROM sqlite_master WHERE type='index' "
             "AND name='idx_olay_biyopsi'").fetchone():
    print("idx_olay_biyopsi zaten var.")
else:
    b.execute("CREATE INDEX idx_olay_biyopsi ON olay(specimen_id) "
              "WHERE tip = 'biyopsi'")
    print("idx_olay_biyopsi dizini açıldı.")

b.commit()
b.close()
print("\nGoc 058 tamam.")
