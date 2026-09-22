"""Göç 046 — Çözülen embriyonun yeniden dondurulabilmesi (v6.143).

Kullanıcının isteği (2026-09-22): "Çözülen embriyo aynı FET tedavisinde
yeniden dondurulabilsin ve tüp Cryo Haritası'na girsin." Temmuz 2026'nın
Access kayıtlarında bir FET notu bunu anlatıyordu: "KÜLTÜRE EDİLEN TRANSFER
FAZLASI 1 ADET D5 EMBRİYOSU (1CC) ŞEKLİNDE DONDURULARAK SAKLANDI".

Bugüne kadar program **örnek başına tek dondurma, tek çözme** varsayıyordu:
`olay_kaydet_veya_guncelle()` aynı tipte kayıt varsa onu GÜNCELLİYOR. Yani
yeniden dondurma ilk dondurmanın üzerine yazardı, yeniden dondurulan
embriyo ileride tekrar çözüldüğünde de ikinci çözme ilk FET'in çözme
kaydını sessizce ezerdi. İki kolon bu varsayımı kaldırıyor:

`olay.vit_cycle_id` — **bu dondurma hangi tedavide yapıldı.** Boşsa
örneğin kendi tedavisi (bugüne kadarki bütün dondurmalar). `thaw_cycle_id`
(goc_024) ve `tr_cycle_id`'nin deseni: `olay.cycle_id` her zaman örneğin
KENDİ tedavisi kalıyor, "hangi tedavide yapıldı" ayrı bir alanda
(CLAUDE.md: "Embriyo cycle değiştirmez").

`olay.thaw_tasiyici_id` — **bu çözme hangi tüpü boşalttı.** Bir örnek iki
kez dondurulunca "çözme hangi dondurmayı geri aldı" sorusunun cevabı
kayıtta olmalı; yoksa ikinci tüpün sayfası ilk tüpten yapılan çözmeyi
"bu tüp çözüldü" diye gösterirdi.

Geriye dönük doldurma (yalnızca `thaw_tasiyici_id`): her çözme kaydına,
örneğin o çözmeden ÖNCE açılmış dondurma kaydının tüpü yazılıyor (kimlik
sırasıyla -- saatler elle geri tarihlenebildiği için onlara bakılmıyor).
Bugüne kadar bir örneğin tek etkin dondurması vardı, yani cevap tek.
Dondurması hiç olmayan çözme (program öncesi Access kayıtlarının FET
embriyoları, v6.130) boş kalıyor: tüpü gerçekten bilinmiyor.
`vit_cycle_id` doldurulmuyor: boş = kendi tedavisi, bugüne kadarki
dondurmaların hepsi için doğru olan tam da bu.

Birden fazla kez çalıştırılabilir.

Kullanım:  python3 goc_046.py
"""

import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py
DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")

b = sqlite3.connect(DB, timeout=15)
b.execute("PRAGMA foreign_keys = ON")

kolonlar = {r[1] for r in b.execute("PRAGMA table_info(olay)")}
for kolon, tanim in (("vit_cycle_id", "INTEGER REFERENCES cycle(id)"),
                     ("thaw_tasiyici_id", "INTEGER REFERENCES tasiyici(id)")):
    if kolon in kolonlar:
        print(f"olay.{kolon} zaten var.")
    else:
        b.execute(f"ALTER TABLE olay ADD COLUMN {kolon} {tanim}")
        print(f"olay.{kolon} eklendi.")

b.execute("CREATE INDEX IF NOT EXISTS idx_olay_vit_cycle ON olay(vit_cycle_id)")
b.execute("CREATE INDEX IF NOT EXISTS idx_olay_thaw_tasiyici "
          "ON olay(thaw_tasiyici_id)")

# Çözmenin tüpü, iki adımda: (1) o çözmeden ÖNCE açılmış dondurma (kimlik
# sırası), onlardan etkin olanı, onlardan en yenisi; (2) önceden açılmış hiç
# yoksa -- olağan değil ama eski bir veri düzeltmesinde olabilir -- örneğin
# herhangi bir tüpü. Tek UPDATE'te `ORDER BY (v.id < olay.id)` yazılamıyor:
# SQLite alt sorgunun ORDER BY'ında dıştaki tabloyu görmüyor ("no such
# column: olay.id"); WHERE'de görüyor (goc_024 de öyle yazıyor).
# `rowcount` da işe yaramıyor: alt sorgusu boş dönen satırlar "güncellendi"
# sayılır (NULL üzerine NULL). Önce/sonra sayılıyor.
bos_once = b.execute("SELECT COUNT(*) FROM olay WHERE tip = 'thaw' "
                     "AND thaw_tasiyici_id IS NULL").fetchone()[0]
for oncesi in ("AND v.id < olay.id ", ""):
    b.execute(
        "UPDATE olay SET thaw_tasiyici_id = ("
        "  SELECT v.vit_tasiyici_id FROM olay v "
        "   WHERE v.specimen_id = olay.specimen_id AND v.tip = 'vitrifikasyon' "
        "     AND v.vit_tasiyici_id IS NOT NULL " + oncesi +
        "   ORDER BY v.iptal_mi ASC, v.id DESC LIMIT 1) "
        "WHERE tip = 'thaw' AND thaw_tasiyici_id IS NULL")

bos = b.execute("SELECT COUNT(*) FROM olay WHERE tip = 'thaw' "
                "AND thaw_tasiyici_id IS NULL").fetchone()[0]
doldurulan = bos_once - bos
b.commit()
b.close()
print(f"Cozme kayitlari: {doldurulan} tanesine tupu yazildi"
      + (f", {bos} tanesinin tupu bilinmiyor (dondurmasi programda yok)."
         if bos else "."))
print("\nGoc 046 tamam.")
