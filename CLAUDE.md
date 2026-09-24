# Patient Data Center — proje belleği

Bu dosyayı her oturumda oku. Tasarım kararlarının **gerekçeleri** `README.md`
içinde, sürüm sürüm yazılmış. Bir davranışı değiştirmeden önce oradaki ilgili
bölümü oku — çoğu "tuhaf" görünen karar bilinçli.

---

## Proje nedir

IVF laboratuvarı için hasta / cycle / oosit kayıt sistemi. Klinikte bir mini PC
üzerinde yerel sunucu olarak çalışır, personel iç ağdan telefonla girer.
Mikroskop kamerası bir klasöre snapshot atar, program o kareleri oositlere
bağlar ve arşivler.

**Kullanıcı:** 22 yıllık embriyolog, Python'a yeni başlamış. Kod açıklamaları ve
arayüz Türkçe; klinik terimler İngilizce kalır (blastocyst, ICSI, PN, ICM, TE,
re-expansion, FET). Kullanıcı klinik doğruluk konusunda uzman, kod konusunda
öğrenci — teknik kararları açıklayarak ver, klinik kararlarda ona sor.

**Durum:** çalışır halde. **Gerçek hasta verisi var** — program öncesi
Access kayıtları (temmuz ve ağustos 2026) `aktar_access.py` ile aktarıldı
(v6.130, v6.141). Ocak–haziran 2026 v6.148'de, mayıs 2026 v6.149'da
(`kaynak=MAYIS`) aktarıma hazırlandı; kullanıcı kendi makinesinde
çalıştırıyor — sonraki bir işte veri sayısına güvenmeden önce çalıştırıp
çalıştırmadığını sor. v6.148 kullanıcının veritabanının bir kopyasında
denendi; v6.149'da o kopya yoktu, mayıs yalnızca test veritabanında denendi —
FET'in tüpe bağlanması (önceki aylar gerekiyor) ancak kullanıcının
makinesinde çalışıyor. **Ocak–mayıs 2025** v6.160'ta hazırlandı
(`kaynak=OCAK2025` … `MAYIS2025` — 2026'nın etiketleri çakışırdı), ardından
2026'nın ayları `bagla` ile geçiriliyor; yine kullanıcı çalıştırıyor.
Kullanıcı 2026-09-23'te ocak–mayıs 2025'i aktardığını söyledi. **Haziran–ekim
2025** v6.164'te hazırlandı (`kaynak=HAZIRAN2025` … `EKIM2025`); **kasım–aralık
2025 ve ocak–mart 2024** v6.165'te (`kaynak=KASIM2025`, `ARALIK2025`,
`OCAK2024`, `SUBAT2024`, `MART2024`), ardından da şubat 2026'nın bir tüpü
`dondurma` kipiyle onarılıyor. **Nisan–ağustos 2024** v6.167'de
(`kaynak=NISAN2024` … `AGUSTOS2024`; mayısın aynı gün iki kez girilmiş bir
kaydı kullanıcının seçimini bekliyor, `ATLA`). **Eylül–aralık 2024 ve ocak
2023** v6.168'de (`kaynak=EYLUL2024` … `ARALIK2024`, `OCAK2023` — o dosyanın
tarihleri 2023). **Şubat–aralık 2023 yok** (kullanıcı 2026-09-24'te
onları da aktaracağını söyledi; etiketler `SUBAT2023` … `ARALIK2023`): ocak
2023 tüplerini çözen FET'lerin bağlanması erteleniyor (aşağıda "aktarılmamış ay"). Göç, kalıcı silme, geri yükleme gibi veriye dokunan her
işte bunu hesaba kat.

---

## Çalıştırma

Ara sıra lazım olan bütün komutlar tek sayfada: **`KOMUTLAR.md`**
(veri taşıma, yedek, göçler, kullanıcı, git, sık sorunlar).

Komutlar proje klasörünün kökünde çalışır (v6.1'de `app/` alt klasörü
kaldırıldı — README v6.1 bölümü):

```bash
python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Mac
python  -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Windows
```

Bağımlılıklar: `fastapi uvicorn jinja2 python-multipart`. Python 3.10+.

**Program kurulabilir paket olarak dağıtılacak** (v6.50, `PAKETLEME.md`).
Giriş noktası `baslat.py`; `python -m uvicorn app:uygulama` pakette çalışmaz
(`python` yok, `-m` yok). Uvicorn kütüphane gibi çağrılıp uygulama nesnesi
doğrudan veriliyor. Geliştirmede de aynı yol: `python3 baslat.py`.
- **Şablonlar ve `static/` tarifte veri olarak ekleniyor.** PyInstaller
  yalnızca `import` edilenleri toplar; eksik kalırsa program açılır ama her
  ekran hata verir.
- **Göç betikleri `hiddenimports`'ta** — adıyla çağrıldıkları için görünmezler.
  Tarif dosya adına bakıp kendiliğinden buluyor, yeni göç eklerken bir şey
  yapmana gerek yok.
- **`print` kullanma, `logging` kullan.** Servis olarak çalışırken konsol yok
  ve `print` tamponda kalıp kayboluyor -- paketlenmiş denemede göç özeti
  günlüğe hiç düşmedi. `baslat.py` günlüğü konsola **ve** veri klasöründeki
  `program.log`'a bağlıyor.
- Paket denendi: kaynak klasörünün dışında, `PYTHONPATH` temizlenmiş halde
  27 göç uygulandı ve 22 adres 200 verdi.

**Göçler açılışta kendiliğinden çalışır** (v6.49) — yedekten geri
yüklemeden hemen sonra da (v6.145, tuzak #15). Elle bir şey yapmak
gerekmiyor; `python3 goc_hepsi.py` yalnızca terminalden kontrol etmek için.
- **Çalıştırıcı tek yerde: `goc.py`.** Göçler **süreç içinde** çalışıyor
  (`import goc_029` demek onu çalıştırmak demek). `subprocess.run([sys.executable,
  ...])` yazma — paketlenmiş uygulamada `sys.executable` **programın kendisi**
  olur, o satır göçü değil programı yeniden başlatır.
- Uygulananlar `goc_kaydi` tablosunda. Tabloyu **çalıştırıcı açıyor**, göçle
  değil (kendi kaydını tutan tabloyu göçle kurmak tavuk-yumurta olurdu).
- Soru soran göçler `goc.ELLE` sözlüğünde; değer o göçün **etkisini** arayan
  bir sorgu. Etki varsa göç uygulanmış sayılır ve panel susar. Yeni bir soru
  soran göç yazarsan oraya etkisini de yaz.
- **Göç patlarsa program yine açılır**: hata terminale ve `/yonetim` paneline
  yazılır, sıradaki göçler çalıştırılmaz. Açılmayan program teşhis edilemez.
- İki süreç aynı anda başlarsa `BEGIN IMMEDIATE` işaretini kapan çalıştırır.

---

## Mimari

**Kod ve veri iki ayrı kökte** (v6.46, paketlemenin ön şartı). `db.py`:

- `PROGRAM_KOK` — kod, `templates/`, `static/`, `sema_guncel.sql`, göçler.
  Paketlenmiş kurulumda **salt okunur** (Mac'te `.app` içi, Windows'ta
  `Program Files`) ve program güncellenince üzerine yazılır.
- `VERI_KOK` — `lab.db`, `yerel_ayar.json`, `arsiv/`, `snapshot/`, `yedek.log`.

Veri kökü sırayla: `LAB_VERI` ortam değişkeni → **kodun yanında `lab.db` varsa
orası** (bugünkü iki kurulum böyle, veri yerinde kalıyor) → işletim sisteminin
veri klasörü.

**Veritabanının yerini kendi başına kuran kod yazma** — `db.DB_YOLU` kullan.
28 betik (`goc_002`…`goc_029`, `goc_hepsi`, `teshis`, `teshis_silme`,
`liste_duzenle`) eskiden her biri kendi yolunu kuruyordu; veri taşınınca kod
klasöründe **bomboş yeni bir veritabanı** açarlar, "27 başarılı" derler ve
gerçek veriye hiç dokunmazlardı. Tuzak #8'in sessiz ve en pahalı hali.

SQLite + FastAPI + Jinja2. Framework yok, ORM yok, build adımı yok. Mobil
öncelikli responsive HTML.

Tüm dosyalar proje klasörünün kökünde (v6.1'e kadar bir `app/` alt
klasöründeydi):

```
Patient Data Center/
  app.py            ~3300 satır — TÜM rotalar burada
  db.py             bağlantı, yardımcılar, PROGRAM_KOK / VERI_KOK
  guvenlik.py       oturum / kullanıcı
  goruntuler.py     snapshot kuyruğu, arşivleme, dosya yolları
  excel.py          .xlsx üretir — kütüphanesiz, yalnızca zipfile + XML
  disari.py         Excel çıktılarının sorguları (rotalar app.py'de)
  formlar.py        resmî formların verisi + zaman çizelgesi
  form_kalip.py     form ızgarası: kalıbı kuran/basan ortak kurallar
  form_kalip.json   kâğıt aslından çıkarılmış ızgara — ELLE DÜZENLEME
  xlsx_oku.py       yüklenen .xlsx'ten kalıp çıkarır — kütüphanesiz
  karekod.py        karekod (QR) üretir — kütüphanesiz, çıktı SVG
  simge_uret.py     ana ekran simgelerini üretir (araç, Pillow ister)
  formlar_asil/     orijinal .xls formlar + kalip_uret.py (kalıbı üreten araç)
  static/form_amblem.png  formların üstündeki üniversite amblemi (kâğıttan çıktı)
  templates/        ~42 Jinja2 şablonu
  static/style.css  tüm görsel tasarım
  goc_002..048.py   veritabanı göçleri (sırayla)
  baslat.py         programı başlatır — paketlenmiş uygulamanın giriş noktası
  paket/pdc.spec    PyInstaller tarifi; pdc_kurulum.iss Windows kurulumu
  goc.py            bekleyen göçleri bulur ve çalıştırır (süreç içinde)
  goc_hepsi.py      aynı çalıştırıcının terminal yüzü
  teshis.py         genel sorun teşhisi
  tarih_duzelt.py   yılı bozuk tarihleri bulur, sorarak düzeltir
  teshis_silme.py   bir hasta neden silinemiyor — hiçbir şey silmez
  teshis_form.py    FET formunda çözme neden görünmüyor — yalnızca okur
  cozme_ayir.py     IVF/ICSI'ye yazılmış çözmeleri FET'e taşır (v6.155)
  liste_duzenle.py  seçim listelerini görüntüle / temizle
  kullanici.py      kullanıcı listesi / şifre sıfırlama / yeni kullanıcı
  tasi.py           iki makine arasında USB ile veri taşıma
  aktar_access.py   program öncesi Access kayıtlarını içeri alır (araç)
  yerel_kur.py      bu makinenin klasör yollarını ayarlar
  sifirdan_kur.py   boş veritabanı
  yedek.py          yedekleme (Windows'ta zamanlama kurulmadı)
  sema_guncel.sql   şema referansı — GÜNCEL DEĞİL, bkz. bekleyen iş 7
```

---

## Klinik akış

`OPU → Androloji → Denüdasyon → ICSI → Fertilizasyon → Gün 2/3 → Blastokist
(gün 4-7) → Vitrifikasyon → Çözme → Transfer → Gebelik sonucu`

Tedavi tipine göre hangi aşamaların görüneceği değişir:
- `ivf_icsi` → **çözme hariç** 10 aşama (OPU ve androloji dahil).
  **Çözme yok** (v6.155, kullanıcının kararı: "ivf/icsi tedavisi içinde
  çözme bölümü olmamalıydı"): bu tedavide dondurulan embriyonun çözülmesi
  AYRI bir FET tedavisidir. v6.155'e kadar çözme ekranı seçim yoksa
  kaynak tedaviyi seçiyordu, FET'in işi ICSI'nin formuna yazılıyordu.
  Bugün: `db.cozme_tedavisi_mi(tip)` (tipin aşamalarında çözme var mı);
  çözme ekranı yalnızca `thaw_tedavi_tipleri()`'nin tiplerini sunar, seçim
  yoksa kaynağa düşmez, sunucu seçimsiz kaydı reddeder; ekrandaki "Yeni
  tedavi başlat: FET" `POST /cryo/tasiyici/{id}/yeni-tedavi` ile tedavi
  açar; transfer ekranı `transfer_adaylari(hasta, tedavi)` ile süzülür
  (FET: bu tedavi için çözülenler, IVF/ICSI: kendi çözülmemişleri). Eski
  kayıtları `cozme_ayir.py` ayırır (README v6.155). Yeni bir yerde "bu
  tedavi için çözme yapılabilir mi" diye soracaksan tip adı yazma,
  `cozme_tedavisi_mi()`'ye sor. **Yumurta Dondurma'nın kendi çözmesi
  KALIYOR** (kullanıcının kararı, 2026-09-23: "Yumurta dondurmada çözme
  kalkmasın") — ayrım yalnızca IVF/ICSI için; oraya uygulama.
- `fet` → çözme, transfer, **vitrifikasyon**, gebelik (**OPU yok** — oosit
  toplanmaz, embriyo başka bir cycle'dan gelir, aynı gün transfer edilir).
  Vitrifikasyon v6.143'ten beri (kullanıcının isteği): çözülüp transfer
  edilmeyen embriyo aynı tedavide yeniden dondurulabiliyor — aşağıdaki
  "Bir örneğin birden çok dondurması ve çözmesi olabilir" bölümüne bak.
- `fet_kultur` → çözme, **blastokist**, transfer, vitrifikasyon, gebelik
  (v6.62, `goc_031`; vitrifikasyon v6.143).
  "FET (3→5 kültür)" — gün 2/3 embriyosu çözülüp gün 5'e kadar kültürlenip
  öyle transfer ediliyor. **Yalnızca cleavage tüpü çözülür** (v6.156,
  kullanıcının isteği): blastokist tüpü (dondurmanın tedavisinde blastokist
  değerlendirmesi olan örnek, `tasiyici_icerigi()`'nin `blastokist`
  kolonu) `thaw_tedavi_tipleri()`'nde bu tipe kapanıyor — seçici, yeni
  tedavi düğmesi ve sunucu aynı listeden. Tip listesi
  `db.CLEAVAGE_COZEN_TIPLER`. Evresi bilinmeyen tüp açık; bu tüpten zaten
  yazılmış bir FET (3→5) çözmesi varsa kapı açık (var olan kayıt
  dokunulmaz, `tup_cleavage_tipine_kapali()`); `fet`'ten farkı yalnızca araya giren blastokist
  değerlendirmesi. **Sıra `ivf_icsi`'nin tersi**: orada blastokist
  dondurmadan (vitrifikasyon) önce gelir, burada çözme blastokistten önce
  gelir — embriyo zaten dondurulmuş halde geliyor.
- `oosit_cryo` → OPU, denüdasyon, vitrifikasyon, çözme
- `yumurta_cozme` → **çözme, androloji, ICSI, fertilizasyon, cleavage,
  blastokist, vitrifikasyon, transfer, gebelik** (v6.147; v6.102'de,
  `goc_039`, yalnızca çözmeydi). `oosit_cryo`'da dondurulmuş bir yumurtanın,
  FET'in embriyo için yaptığı gibi, AYRI bir tedavide çözülmesi — **OPU yok,
  çözülen örnek bu tedavide toplanmadı**; denüdasyon da yok (yumurta
  dondurulmadan önce soyuldu). Kullanıcının v6.147'deki sözü: "yumurta
  çözme tedavisinde denüdasyon haricinde diğer bütün işlemler IVF/ICSI cycle
  tedavisi ile aynı olmalıydı" — v6.102'nin "ICSI gerekiyorsa ayrı bir
  tedavi açılır" kararını kendisi değiştirdi. `FET_TIPLERI`'nde (aşağıya
  bak): örnekler `specimen.cycle_id` ile değil `olay.thaw_cycle_id` ile
  aranıyor. Aşama ekranlarının bundan çıkan kuralları aşağıdaki "Yumurta
  Çözme'de ICSI ve sonrası" bölümünde.

`ASAMA_SIRASI` `app.py`'de; tip-aşama eşlemesi `TIP_ASAMALARI` v6.147'den
beri `db.py`'de (`app.TIP_ASAMALARI` aynı sözlük) — `formlar.py` ve
`disari.py` de soruyor, `app`'i import edemezler (`FET_TIPLERI`'nin
gerekçesi). Androloji (`sperm_ornek` + iki `sperm_analiz`: bazal /
hazırlık sonrası) `ivf_icsi`'de ve Yumurta Çözme'de. Şema/listeler: README
v6.2, `goc_019`.

**ICSI'de "enjekte edilmedi" işaretlenen oosit sonraki aşamalara sızmaz**
(v6.105, kullanıcının isteği). ICSI ekranının "Enjekte edildi mi?" kutusu
hayır iken (`icsi_kaydet()`) hiçbir `icsi` olayı yazılmıyor, `specimen.durum`
`immatur`/`degenere` oluyor — `app.py`'deki `_ICSI_YAPILMADI` SQL parçası bu
durumu **`specimen.durum`'a değil `olay` tablosuna bakarak** yakalıyor:
maturasyon değerlendirildi (ICSI ekranı dolduruldu) AMA aktif bir `icsi`
olayı yok. Bu ayrım şart — enjekte edilip **sonra** dejenere olan oositin
`durum`'u da `degenere` yazar ama onun kendi `icsi` olayı vardır, ikisi aynı
`durum` değerini paylaşır.
- **Fertilizasyon ekranında hâlâ görünür, ama salt "yapılmadı" bilgisiyle** —
  `fert_durum()`'a eklenen `icsi_yapilmadi` bayrağı doğruysa (ve o oosite
  daha önce girilmiş bir kayıt yoksa) form hiç basılmıyor, `metin(
  "icsi_yapilmadi_fert_form_yok")` ile salt bilgi kartı çıkıyor — embriyolog
  hiç denenmemiş bir işlem için fertilizasyon sonucu uydurmuyor.
- **Cleavage, blastokist ve vitrifikasyonda hiç görünmez.** `cleavage_durum()`
  ve `blast_durum()`'un `WHERE`'ine `AND NOT (_ICSI_YAPILMADI)` eklendi;
  ikisi de zaten yalnızca `ivf_icsi`'de (ya da `fet_kultur` gibi ondan gelen
  embriyolarla) çalışıyor, güvenli.
**Dejenere işaretlenen yumurta sonraki aşamalarda GÖRÜNÜR ama KİLİTLİDİR**
(v6.139, kullanıcının isteği: "dejenere işaretlenen yumurta ileriki menülerde
yumurtanın kutucuğunda Dej. kısaltmasıyla gösterilsin ve işlem yapılamasın.
Yani cleavage ve Blast embriyo yazılamasın"). Süzgeç `_DEJENERE`.
- **`specimen.durum`'a DEĞİL `olay` tablosuna bakıyor** — `_ICSI_YAPILMADI`'nın
  gerekçesinin başka bir yüzü, ama sebebi farklı: `durum` her aşamada
  **üzerine yazılıyor** (`cleavage_kaydet()` `gun2`, `vit_kaydet()`
  `dondurulmus`), yani dejenere bir örneğe bir kez kayıt girilse süzgeç
  sessizce susardı. Olay kalıcı: `icsi_sonuc='degenere'` ya da
  `fert_sonuc='degenere'`. Yeni bir "şu durumda mı" süzgeci yazarken hep sor:
  bu alanın üzerine sonradan yazılıyor mu?
- **Gizlemek DEĞİL kilitlemek**: numara şeridinde `10-Dej.` yazar (kutu `deg`
  sınıfını alır), üstte uyarı çıkar, form yerine bilgi kartı basılır
  (`metin("dejenere_form_yok")`). Gizlemek "o yumurta hiç yoktu" derdi.
- **Var olan kayıt dokunulmaz**: koşul `{% elif sp.dejenere and not kayit %}` —
  v6.105'in fertilizasyondaki deseninin aynısı. Yoksa yanlışlıkla dejenere
  işaretlenen bir embriyonun kaydı bir daha düzeltilemezdi.
- **Asıl engel sunucuda**: `_dejenere_engel()` yalnızca **yeni** kayıt
  açılmasını reddeder, var olanın güncellenmesini değil.
- **`_ICSI_YAPILMADI` ile karıştırma**: enjekte edilmeden dejenere denen
  yumurta buraya girmiyor, onu zaten o süzgeç yakalıyor ve cleavage/
  blastokistte hiç göstermiyor (kullanıcı 2026-09-22'de "şu an nasılsa öyle
  kalsın" dedi — v6.105 gevşetilmedi).
- **Vitrifikasyona ayrı bir şey eklenmedi**: `_DEGERLENDIRILMIS` (v6.137)
  zaten kaydı olmayanı eliyor, dejenere yumurtaya kayıt açılamadığı için
  oraya hiç ulaşamıyor.

**Enjekte edilmeyen yumurta fertilizasyon şeridinde kendi maturasyonunu
yazar** (v6.139, kullanıcının seçimi). Önceden hepsi `∅` idi, hangisi olduğu
görünmüyordu; artık GV / MI / Dej. / Atr. Jinja global `mat_kisa(kod)`:
yalnızca uzun iki etiketin (`degenere`, `atretik`) kısaltması
`metinler.py`'de (`mat_kisa_<kod>`), MII/MI/GV kendi `liste_degeri`
etiketiyle basılıyor — "kodu değil etiketi göster" kuralı. Şeritte `|upper`
kullanma, bu fonksiyonu çağır. **Bu kısaltmalar yalnızca ICSI ve
fertilizasyonda**: enjekte edilmeyen yumurta cleavage/blastokistte zaten
görünmüyor.

- **Aynı ekranda ikinci bir süzgeç var: `_DEGERLENDIRILMIS`** (v6.137,
  kullanıcının isteği: "bir önceki blastokist menüsünde kaydı yapılmamış
  embriyoyu gösterme"). Örneğin iptal edilmemiş bir cleavage/blastokist
  değerlendirmesi ya da zaten bir vitrifikasyon kaydı olmalı. **Cleavage de
  sayılıyor**: bu lab gün 3 embriyosu da donduruyor, yalnızca blastokist
  aransaydı gün 3'te dondurma programda tümden yapılamazdı. **Dondurulmuş
  örnek her koşulda kalır** — ekranın üst kartı aynı listeden besleniyor.
  Koşul `TIP_ASAMALARI`'na bakıyor (`"blast" in ...`), cycle tipini elle
  yazmıyor. Satırdaki kalite `_vit_satiri()`'nden: blastokist skoru → yoksa
  cleavage yazımı ("4HG2") → yoksa "değerlendirilmemiş".
- **Vitrifikasyon ekranı `oosit_cryo` ile de paylaşılıyor — orada bu süzgeç
  UYGULANMAZ.** `oosit_cryo`'da maturasyon denüdasyonda değerlendiriliyor
  (aşağıdaki madde) ve ICSI aşaması hiç yok; `_ICSI_YAPILMADI` orada **her**
  oosit için doğru çıkardı (hiçbirinin `icsi` olayı olamaz) ve ekranı
  bomboş bırakırdı. `_vit_adaylari()` bu yüzden süzgeci yalnızca tipin
  ICSI aşaması varken ekliyor (`"icsi" in TIP_ASAMALARI[...]`: `ivf_icsi`
  ve v6.147'den beri Yumurta Çözme). Yeni bir yerde `_ICSI_YAPILMADI`
  kullanırsan aynı soruyu sor: bu ekranı ICSI'siz bir tip de paylaşıyor mu?

**`oosit_cryo`'da maturasyon/bulgu değerlendirmesi denüdasyon ekranında
yapılır** (v6.96, kullanıcının isteği). `ivf_icsi`'de bu soru ICSI
ekranında soruluyor; `oosit_cryo`'da ICSI aşaması hiç yok, dondurmadan
önce sorulacak başka yer olmadığı için denüdasyona kondu — kullanıcıya
soruldu, "denüdasyon ekranı" dedi. Aynı mekanizma: `olay.tip=
'maturasyon_kontrolu'` + `specimen_bulgu` (`bulgu_icsi` listesi, ICSI'ye
özel değil — oositin kendi morfolojisi), yalnızca
`specimen_bulgu.asama='denudasyon'` ile ICSI'ninkinden (`asama='icsi'`)
ayrılıyor. Denüdasyon ekranı bu bölümü yalnızca `c.cycle_tipi ==
'oosit_cryo'` iken basıyor — `ivf_icsi`'de aynı soru iki yerde
sorulmasın diye. Yeni bir `FET_TIPLERI` dışı cycle tipi eklersen ve o
tipte de ICSI aşaması yoksa aynı ihtiyaç doğar, aynı deseni kullan.

**`fet`, `fet_kultur` ve `yumurta_cozme`'de dondurulan örnek BU cycle'dan
gelmez** — `FET_TIPLERI` sabiti ve Jinja global `fet_tipi_mi(cycle_tipi)`
bunu tek yerden kontrol ediyor (v6.62, `yumurta_cozme` v6.102'de eklendi).
**Sabitin kendisi v6.130'dan beri `db.py`'de**, `app.FET_TIPLERI` oradan
besleniyor: `disari.py`'nin istatistik sorgusu da aynı ayrımı soruyor ve
`app`'i import edemiyor (app zaten disari'yi import ediyor). Yeni bir üye
eklersen `db.py`'ye ekle, `app.py`'deki ad kendiliğinden kapsar.
Taşıyıcı/örnek listeleri `specimen.cycle_id` ile değil, `olay.thaw_cycle_id`
("hangi tedavi için çözüldü") ile aranıyor — `specimen.cycle_id` örneğin
**ilk** (OPU/ICSI) cycle'ı, hiç değişmez (README v6.7). `FET_TIPLERI` adı
"embriyo" diyor ama mekanizma tamamen genel: `cycle_thaw_listesi()`'nin
taşıyıcı sorgusu embriyo/oosit ayrımı yapmıyor, `yumurta_cozme` eklenirken
hiç değişmedi. Yeni bir `FET_TIPLERI` üyesi eklersen `cycle_thaw_listesi()`,
`db.tedavi_ornekleri()` (v6.147'ye kadar `_blast_kosul()`) ve
`_vit_adaylari()`'nın FET dalı (`_FET_DONDURULABILIR`) otomatik kapsar — `fet_tipi_mi()` kullanmayan yeni bir `== "fet"` kontrolü
yazma. `cycle_thaw.html`'deki vitrifikasyon bağlantısı v6.143'ten beri
`fet_tipi_mi()`'ye değil **tipin aşamalarına** bakıyor (`vit_var`,
`TIP_ASAMALARI`): FET'te de vitrifikasyon var.

**Aşama ekranlarında seçim `specimen.id` ile, `cycle_sira_no` ile DEĞİL**
(v6.62'de blastokistte; v6.147'den beri ICSI, fertilizasyon ve cleavage'da
da). `fet_kultur`'da ve Yumurta Çözme'de birden çok tedavinin örnekleri aynı
listede olabiliyor ve `cycle_sira_no` yalnızca **kendi** tedavisinde tekil
(`UNIQUE(cycle_id, cycle_sira_no)`) — iki tedavide de "1. yumurta" olabilir.
Seçimi `_secili_ornek()` yapıyor: v6.147'den önceki adres (`?oosit=3`)
liste tek tedavinin örnekleriyse hâlâ kabul ediliyor (açık kalmış bir
sekmenin tazelemesi). "Kaydet → sıradaki" listenin kendi sırasını izliyor
(`_sonraki_ornek()`), sıra no karşılaştırmasını değil. Denüdasyon kendi
örneklerini gösterdiği için `?oosit=<cycle_sira_no>` ile kaldı.

**`olay.cycle_id` her zaman specimen'in KENDİ cycle'ı, ekranın cycle'ı
değil** — `thaw` ve `transfer` olaylarının zaten yaptığı şey
(`e["cycle_id"]` / `sp["cycle_id"]`), `blastokist_degerlendirme` de artık
aynısını yapıyor. "Hangi tedavi için" sorusu ayrı bir alanda (`thaw_cycle_id`,
`tr_cycle_id`) yanıtlanıyor. Fotoğraf ekleme de aynı kuralı izliyor:
embriyonun **kendi** cycle'ının arşiv klasörüne gidiyor
(`/cycle/{{ sp.cycle_id }}/foto-ekle`, `thaw.html`'in zaten yaptığı gibi),
görüntülenen ekranın cycle'ına değil — iki klasöre bölünmüş bir embriyo
geçmişi olmasın diye. v6.147'den beri ICSI, fertilizasyon ve cleavage
POST'ları da öyle (önce rotanın `cycle_id`'sini yazıyorlardı; `ivf_icsi`'de
ikisi aynı değerdi).

**Yumurta Çözme'de ICSI ve sonrası: çözülen yumurta başka tedavinin örneği**
(v6.147, kullanıcının isteği; README v6.147). Yumurtanın `specimen.cycle_id`'si
Yumurta Dondurma; ekranlar onu `db.tedavi_ornekleri()` ile buluyor.
- **Maturasyon iki kez soruluyor, iki ayrı kayıt.** Denüdasyonda (Yumurta
  Dondurma, v6.96) ve çözmeden sonra ICSI ekranında. ICSI ekranı yalnızca
  BU tedavinin maturasyonunu okuyor ve güncelliyor (`_tedavi_ek()`,
  `db.olay_tedavisi()` üzerinden); kaynağınki ezilmiyor, kaynağın özeti ve
  formu değişmiyor. FET tipinde kaynağında da bulunabilen bir olay tipini
  okuyan/yazan yeni bir ekran yazarsan aynı süzgeci kullan.
- **İşlem saati bu tedavideki çözmeden önce olamaz** (`_cozmeden_once()`,
  FET tiplerinin dört aşama POST'unda). Reddedilir, ekrana sebebi ve çözme
  saati yazılır (`?hata=cozmeden_once`, `ASAMA_HATALARI` beyaz listesi —
  tuzak #9). Sessizce değiştirmek yerine reddediliyor; gerekçe:
  `olay_tedavisi()` saate bakıyor, kayıt kaynağın sayılırdı ve ICSI ekranı
  yazılanı göremeyip her kayıtta yeni bir maturasyon açardı. Bilinen sınır:
  yazılan değerler forma geri gelmiyor, kayıtlı değerler basılıyor.
- **Çözmede dejenere çıkan yumurta** ICSI şeridinde "Dej." ile kalıyor,
  formu açılmıyor, sunucu da yeni kayıt açmıyor (`_cozme_dejenere_sql()`,
  v6.139'un "gizlemek değil kilitlemek" kuralı). Yalnızca BU tedavinin
  çözmesi sayılıyor. Enjekte edilmediği için cleavage/blastokistte hiç
  görünmüyor (`_ICSI_YAPILMADI`).
- **Silme ekranları `?cycle=` taşıyor** ve `_hedef_tedavi()` doğruluyor:
  örnek o tedavi için çözülmüş olmalı. Adres yalnızca dönüşü değil hangi
  kaydın silineceğini de belirliyor. ICSI silmesi ICSI aşaması olmayan bir
  tedaviye düşerse (adressiz eski bağlantı, Yumurta Dondurma) hiçbir şey
  iptal etmiyor — orada maturasyon denüdasyonda yazıldı. Geri alınınca
  yumurta çözmenin durumuna dönüyor (`_cozme_oncesi_durum()`), `oosit`'e
  değil.
- **Vitrifikasyon adayları** `_vit_adaylari()`'nda, ekran ve kayıt aynı
  koşulu soruyor: FET'in koşulu (bu tedavi için çözülüp transfer edilmeyen)
  + enjekte edilmiş (v6.105) + değerlendirilmiş (v6.137), dondurma kaydı BU
  tedavininki olmalı (`_degerlendirilmis_burada()`: kaynağın yumurta
  dondurması sayılmıyor). Dondurmanın `vit_cycle_id`'si bu tedavi (goc_046).
- **Yumurta transfer adayı değil** (`transfer_adaylari()`): yumurta donduran
  bir tipin örneği ve hiç ICSI'si yok. Önce çözülen yumurta 'cozuldu'
  durumuyla hastanın bütün transfer ekranlarında listeleniyordu.
- **Yumurta mı embriyo mu: `db.yumurta_mi(tip, asama)`** — Yumurta Çözme'de
  çözülen yumurta (`asama='thaw'`), dondurulan/transfer edilen embriyo.
- **Çözmeyi geri almak**: çözmeden sonra girilmiş HER kayıt engel (ICSI,
  değerlendirme, transfer), yalnızca yeniden dondurma değil
  (`_cozme_geri_alma_engeli()`). Önce en son adım.
- Formlar, Excel ve istatistik: aşağıdaki "Bir olayın yapıldığı tedavi"
  maddesi.
- v6.146'daki soru (FET (3→5)'te aynı gün değerlendirmesi kaynağın
  üzerine yazılıyor) kapandı: FET (3→5)'te cleavage embriyosu çözülüyor
  (kullanıcı, 2026-09-23). Yumurta Çözme'de de doğmuyor: çözülen yumurtanın
  kaynakta cleavage/blastokist kaydı yok.

Freeze-all ayrı bir tip **değil** — veriden çıkar (vitrifikasyon var, transfer yok).

---

## Değişmeyen kurallar

**Hasta kimliği her ekranda görünür.** Yanlış hasta bu işin en pahalı hatası.
Üst çubuk sticky, kimlik koyu bantta: **ad üstte ve büyük, dosya no altında**
(v6.23; öncesinde tersiydi). Bandın sırası 31 şablonda aynı HTML'le basılıyor
ve **CSS'te** çevriliyor (`.kimlik` flex + `order`) — sırayı değiştireceksen
şablonlara dokunma, tuzak #1. Hasta adı olmayan ekranlar (taşıyıcı, çözme)
`kimlik tekli` sınıfını alır.

**Örnek kodu ana fotoğrafın altında yazar.** `527078-2026-0001-03` kodu
oosit → zigot → embriyo boyunca değişmediği için aynı kod her aşama ekranında
aynı yerde çıkar; soyağacı ekrandan okunur. Yeni bir aşama ekranı yazarsan
fotoğrafın altına `<div class="dosyaadi">{{ ornek_kodu(sp.id) }}</div>` koy.

**Aşama ekranı ilk kareyi gösterir, sonuncuyu değil** (v6.23). Ana fotoğrafı
seçen sorgu `ORDER BY g.id LIMIT 1` olmalı; `DESC` yazma.

**Aşama ekranı adressiz açıldığında ilk örneği seçer** (v6.35). Denüdasyon,
ICSI, fertilizasyon, gün 2/3 ve blastokistte varsayılan `oositler[0]` —
"sonuncu" ya da "ilk kaydedilmemiş" değil. Kullanıcının isteği: aşamalar
arasında geçerken ekran baştan başlasın. Toplu giriş bundan etkilenmiyor,
çünkü **seçim adreste yazıyor**: "kaydet → sıradaki oosit" akışı
`?oosit=<sıradaki>` ile geçiyor, varsayılan yalnızca adres bir şey
söylemediğinde devreye giriyor. Yeni bir aşama ekranı yazarsan aynısını
yap ve POST'unda seçimi **adrese yaz** — varsayılana güvenme.
Denüdasyonun POST'u bunu `secili` gizli alanıyla taşıyor (atla / geri al);
alan adrese yazıldığı için yalnızca rakam kabul ediliyor.

**Fotoğrafsız örnek boş bir alan bırakmaz** (v6.35). `_kareler.html`
`yer(ad, sp, ekle_yolu)` makrosu fotoğrafın yerini tutar ve içine örneğin
**o aşamadaki adını** yazar -- ekranın başlığında ne yazıyorsa o: Yumurta,
Zigot, Cleavage, Blastokist. Beşi de `ornek_adi(asama, cycle_tipi)`'den
geliyor; adı makroya sabit yazma, çağıran ekrandan geçir — dil değişince
isim de değişmeli. Yeni bir aşama ekranında "fotoğraf yok" diye boş kart basma,
bu makroyu çağır.

**Ekran düzeni her aşamada aynı: üstte örnekler, altta bilgi kartı.** Bir
örneğe basınca altında salt okunur bilgi kartı açılır; değiştirmek "Düzenle"
ile (`?duzenle=1`). Kaydı olmayan örnekte form doğrudan açılır — "kaydet →
sonraki oosit" toplu giriş akışı bozulmasın diye (v6.20). Yeni bir aşama
ekranı yazarsan formu hep açık bırakma, bu düzene uy. İki parça var
(v6.20–v6.22):
- `_bilgikart.html` `kart(baslik, satirlar, duzenle_yolu=None, rozet=None)` —
  form yerine gösterilen salt okunur kart. **Aşama ekranlarının hepsi**:
  OPU, androloji, denüdasyon, ICSI, fert, gün 2/3, blastokist. Bu ekranlarda
  üstte numara şeridi var ve seçim **adresten** yapılır (`?oosit=N`), tıklanan
  kareden değil. `duzenle_yolu` verilmezse düğme basılmaz (androlojideki gibi
  bölüm kartları için); vurgulu kenarlık yalnızca `rozet` verilen kartta.
- `_ornekkart.html` `izgara(...)` + `baglama()` — kayıt listesi ızgarası,
  kartları **sunucu** basar (`{% call(e) %}` ile satırları çağıran verir).
  Vitrifikasyon, çözme, transfer: orada bir örneğin tek kaydı var, kareye
  basınca altında kartı açılır.

**Bir ekranda birden çok düzenlenebilir şey varsa adreste adıyla söyle.**
Denüdasyonda `?duzenle=saat` (cycle'ın denüdasyon saati) ve `?duzenle=oosit`
(oositlerin çalışma kipi) — `duzenle=1`/`duzenle=2` okunmuyor (v6.22).

**Denüdasyonun bilgi ekranı fert/blastokistin aynısıdır** (v6.25): numara
şeridi → seçilenin fotoğrafı → altında örnek kodu → kare şeridi → bilgi
kartı. `?duzenle=oosit` çalışma kipinde **yalnızca** oosit ekleme (kamera
kuyruğu, fotoğrafsız ekleme, elle fotoğraf, son kaydı geri al), over
değiştirme ve kamera uyarıları var. **Şeridi ve fotoğrafı çalışma kipine
saklama** — v6.24'te bu yapıldı, kullanıcı geri istedi: tasarım bütünlüğü
aşama ekranlarının hepsinde aynı görünmekten geliyor. Kare kaydettikten
sonra çalışma kipinde **kalınır**, yoksa her kayıtta tekrar Düzenle demek
gerekir.

**Form doğrulama hatası formu kapatmamalı.** Kart modu geldikten sonra
`?hata=...` ile geri dönmek "mesajı göster, formu gizle" demek — kullanıcı
yazdığını göremez. Hata dönüşü `?duzenle=1&hata=...` olmalı (v6.21, OPU).

**Geniş ekranda kartlar iki sütuna ayrılır** (v6.42). Telefon öncelikli
tasarım geniş ekranda içeriği ortada 640px'lik bir şeride sıkıştırıyordu; iki
yanda ~400'er piksel boş kalıyor, sayfa boşuna uzuyordu. `/cycle/{id}` ve
`/yonetim` şimdi `.sutunlar` > iki `.sutun` kullanıyor.
- **Sütunlar şablonda ayrılır, `column-count` ile değil.** CSS'in çok sütunu
  kartları yüksekliğe göre böler; "İşlemi bitir" düğmesi verinin üstüne
  düşebilir. Hangi kartın nerede duracağı anlamla ilgili bir karar.
- **Bölme noktası kaynak sırasında olmalı** — araya `</div><div class="sutun">`
  girer, sıra değişmez. Böylece sütunlar alt alta dizildiğinde (telefon) sıra
  bire bir aynı kalır. Kart taşıyacaksan sırayı bozmadan taşı.
- **Medya sorgusu yok, sarma var**: `flex: 1 1 380px` + `flex-wrap`. Sütun
  380px'in altına düşecekse kendiliğinden alt alta diziliyor, yani kural her
  genişlikte doğru. Sabit kırılma noktası yazma.
- **İçerik sütununun genişliği tek yerde**: `--genis-sutun`. Hem `.kap.genis`
  hem kimlik bandının hizası onu kullanıyor — iki ayrı formül olsaydı band ile
  kartlar birbirinden kayardı. Bandın hangi ölçüyü kullanacağını
  `body.genissayfa` söylüyor (`base.html`'deki `{% block govde %}`); bant
  `.kap`'ın kardeşi olduğu için `:has()` gerekirdi, o da eski Safari'de yok.
- **`.kap.genis` yan menü payını (`100vw - 500px`) içerir.** Yan menüsü olmayan
  ekranda `.kap.genis.yanmenusuz` payı kaldırıyor. Sınıf bilerek opt-in:
  unutulursa sayfa dar kalır, menünün altına **girmez**.
- **İki sütun her ekranın çözümü değil** (v6.52). Ölçü: ekranda birbirinden
  bağımsız kartlar mı var, yoksa genişliğe ihtiyacı olan tek bir şey mi?
  İki sütun: `/yonetim`, `/cycle/{id}`, `/kullanicilar`, `/istatistik`,
  `/formlar`, `/hastalar` (v6.63 — ay listesi ile Tüm Hastalar birbirinden
  bağımsız iki kart), `/cryo` (v6.85 — Embriyo Dondurma ve Sperm Dondurma
  birbirinden bağımsız iki modül). Yalnızca genişleyen (`kap genis`,
  v6.65'ten beri `yanmenusuz` DEĞİL — menü artık orada da var):
  `/klasorler`, `/hasta/{id}`, `/bitenler` — liste ekranlarını bölme,
  `_cyclesatir` satırları soldan sağa okunan tek bir akış.
  `/hastalar`'ın arşiv modu (`?arsiv=1`) bu kategoride kaldı: orada tek liste
  var, bölünecek ikinci bir kart yok.
  Bilerek dar kalanlar: `/cycle/{id}/bitir` (onay ekranı — dar olması
  yanlışlıkla basmayı zorlaştırıyor), `/dil` ve form ekranları (alan
  genişledikçe etiketle değer birbirinden uzaklaşır).
- **Bölme noktası `{% if %}`'in içine düşmemeli.** `/formlar`'da ilk yazışta
  `{% if gomulu %}`'nin içine düştü; gömülü form olmayan kurulumda (ticari
  dağıtım, v6.41) `</div>` hiç basılmayacaktı. Sütun sınırı her zaman
  basılan bir yerde olmalı.
- **Aşama ekranları iki sütuna BÖLÜNMEZ** — iki kez denendi, kullanıcı iki
  kez beğenmedi, v6.59'da geri alındı. Tekrar denemeden önce README v6.57–59'u
  oku. Sebep ölçülü: kartların boyu çok farklı (androlojide 586/235/877/563px)
  ve **sırayı bozmadan** (v6.42) yapılabilecek üç bölmenin verdiği farklar
  1089/619/1135px — yani en iyi bölme bile ~600px ragged bırakıyor. Üstelik
  fotoğraf geldiğinde sol sütun ~500px büyüyüp denge **tersine** dönüyor:
  bir duruma göre dengelenen düzen ötekinde bozuluyor. Kullanıcının sözü:
  "bölümler çok asimetrik, düzensiz görünüyor".
  - Tek geniş sütun (940px) da denendi ve gösterildi: simetrik ve fotoğraf
    608 → 908px, **ama sayfa boyu hiç kısalmıyor** (formlar zaten `.alan ikili`
    ile iki sütunlu satır kullanıyor). Kullanıcı onu da istemedi.
  - Bugün bu ekranlar 640px'lik tek sütunda. Büyük monitörde iki yanda geniş
    boşluk kalıyor; kullanıcı "daha sonra bir şeyler düşünürüz" dedi
    (2026-09-12). Ona sormadan yeniden bölme.
- **Kimlik bandı + geniş + yan menüsüz üçlüsü ayrı ölçü ister**
  (`--genis-sutun-menusuz`, v6.52). Şablon ikisini birlikte verir:
  `{% block kapsinif %} genis yanmenusuz{% endblock %}` **ve**
  `{% block govde %}genissayfa menusuzsayfa{% endblock %}`. Yalnız birini
  verirsen bant ile kartlar 1100-1440 arasında ~120px kayar.

**Ekranda "cycle" değil "tedavi" denir** (v6.79, kullanıcının isteği). Kod
tarafı (tablo adı `cycle`, kolonlar `cycle_id`/`cycle_no`/`cycle_tipi`/...,
rotalar `/cycle/{id}`, Python değişkenleri, şablon dosya adları
`cycle_detay.html` gibi, `metin()` **anahtarları**) değişmedi — yalnızca
kullanıcının gördüğü Türkçe metin. Yeni bir ekranda "cycle" yazmak
gerekiyorsa `metin("cycle")`/`metin("cycleler")` kullan (zaten "Tedavi"/
"Tedaviler" basıyor) ya da aynı çekim mantığıyla elle yaz — "cycle'ı" değil
"tedaviyi", "cycle'da" değil "tedavide". İngilizce ("en") değerlerine
dokunulmadı: o çeviri zaten yarım ve askıda (bekleyen iş 8), ayrıca "cycle"
İngilizce IVF literatüründe zaten kullanılan bir terim.

**Hasta kartında tedaviler `hasta_cycle_no DESC` ile sıralanır, klinik tarih
alanıyla DEĞİL** (v6.80). `hasta_detay()` önce `COALESCE(opu_zamani,
hcg_zamani) DESC` kullanıyordu; `fet`/`fet_kultur` tiplerinde OPU hiç
yapılmadığı için bu iki alan da hep NULL, SQLite `DESC`'te NULL'ları en sona
attığı için en son açılan tedavi FET ise listenin dibine düşüyordu (kullanıcı
fark etti). `hasta_cycle_no` ("Kaçıncı tedavi") tedavi tipinden bağımsız her
zaman atanıyor — yeni bir hasta-tedavi listesi sıralaması yazarsan klinik
tarih alanına değil, bu artan sıra numarasına güven (aynı desen
`/cycle/{id}/vitrifikasyon`'un kaynak tedavi seçicisinde de var).
v6.144'ten beri numaranın kendisi tarih sırasından geliyor (aşağıdaki
madde), yani bu sıralama zaten tarih sırası — NULL sorunu olmadan.

**Hastanın tedavileri tarih sırasıyla numaralanır** (v6.144, `goc_047`,
kullanıcının isteği: "eski tedavi kaydı eklenirse tarih sırasına göre en
eski tedavi 1. tedavi olarak eklensin. Bu daha sonra hep uygulansın").
Numara eskiden açılışta "en yüksek + 1"di; temmuzun Access kayıtları
ağustostan sonra aktarılınca temmuz tedavisi 2., ağustos 1. oldu.
- **Kural tek yerde: `db.tedavileri_sirala(b, hasta_id)`**, tedavinin günü
  `db.tedavi_tarihi(b, c)`: OPU, yoksa hCG; FET'te çözme ya da transfer
  (`thaw_cycle_id`/`tr_cycle_id`); yoksa planlanan tarih; yoksa açılış anı.
  Program, `aktar_access.py` ve göç aynı işlevi çağırıyor, ikinci bir kopya
  yazma. Programın verdiği numara bir öncekinin bir fazlası (ilk 1).
- **Elle yazılan numara korunur** (`cycle.hasta_cycle_no_elle`, README
  v0.8: başka merkezdeki denemeler). Bir önceki tedavinin numarasından
  büyükse tutuluyor, değilse tarih sırası kazanıyor; değer silinmiyor.
  "Hep 1'den" ya da "ilk numarayı koru" gibi tek bir taban YAZMA: ilki
  başka merkezdeki denemeleri siler, ikincisi Access kayıtlarını zaten
  sayan bir elle numarayı aktarımdan sonra iki kez sayar (README v6.144).
- **Tedavinin gününü değiştiren her yazmadan sonra numarala.** Bugün:
  tedavi formu (kaydetme ile numaralama tek işlem, elle numara
  `_elle_no_dogrula()` ile reddedilebiliyor), OPU ekranı, çözme ve transfer
  (kayıt + geri alma), kalıcı tedavi silme (`tedavi_sirasini_duzelt()`),
  aktarım aracı (`_tedavi_sirasi()`). `db.tedavi_tarihi()`'ne yeni bir alan
  eklersen o alanı yazan yola da çağrıyı ekle — yoksa numaralar tarih
  sırasından sessizce ayrı düşer. Kayan numaralar değişiklik geçmişine
  yazılıyor (`tedavi_sirasini_logla()`).
- **Formda "elle mi"**: yeni tedavide kutu programın önerisinden (gizli
  `hasta_cycle_no_oneri`) farklıysa, düzenlemede bugünkü numaradan
  farklıysa. Boş kutu = tarih sırası.
- **Göç yoksa hiçbir şeye dokunmaz** (tuzak #3); formdaki kolon kontrolü
  (`_elle_no_kolonu_var()`) **saklanmıyor** — tuzak #15.
- **Lab kayıt no (`cycle_no`, 2026-0xxx) asla yeniden numaralanmaz**: tüp
  etiketinde, örnek kodunda (`specimen.id`) ve arşiv klasöründe yazıyor.

**Cycle ekranı klinik özettir, fotoğraf yoktur** (v6.20). Fotoğraflar aşama
ekranlarında, tek tek ve büyük bakılacak yerde. Cycle ekranına küçük resim
ekleme. **İstisna: Doktor Notu** (v6.81, kullanıcının isteği) — bu kural
embriyoloji/oosit fotoğrafları içindir; Doktor Notu bir **belge eki** (rapor,
konsültasyon yazısı — foto ya da PDF), embriyo fotoğrafı değil, klinik özetin
parçası. `cycle_detay.html`'de protokol notu kartının hemen altında küçük
önizlemeyle duruyor. Yeni bir "belge eki" kavramı daha eklersen aynı ayrımı
yap: embriyoloji fotoğrafı → asama ekranı, klinik belge → cycle ekranı.
- Depolama: yeni tablo yok, mevcut `goruntu` mekanizması (`elle_ekle()`,
  `specimen_id IS NULL`) yeni bir `asama="doktor_notu"` değeriyle yeniden
  kullanıldı. `goruntu.asama` serbest metin (CHECK yok) olduğu için göç
  gerekmedi. **`goruntu_asama` liste_degeri'ne EKLENMEDİ** — o liste
  `/cycle/{id}/foto-ekle`'nin embriyoloji-aşaması seçicisi, Doktor Notu oradan
  seçilebilir bir şey değil, sabit kod.
- **PDF yalnızca Doktor Notu'nda kabul edilir.** `goruntuler.elle_ekle()`'ye
  `izin_uzantilari` parametresi eklendi (varsayılan hâlâ görüntü-only
  `UZANTILAR`); `DOKTOR_NOTU_UZANTILARI = UZANTILAR | {".pdf"}` yalnızca
  `/cycle/{id}/doktor-notu-ekle` rotasından geçiyor. Genel "Fotoğraf ekle"
  (`/cycle/{id}/foto-ekle`) hâlâ PDF reddediyor — oosit/embriyo fotoğrafında
  PDF anlamsız, bu ayrımı bozma.
- **PDF'in "tam ekranı" `_buyutec.html` değil, yeni sekme.** `_buyutec`
  yalnızca `<img>` basıyor, PDF'i gösteremez. PDF kutusu `<a target="_blank"
  href="/dosya/{id}">` — tarayıcının kendi PDF görüntüleyicisi zaten neredeyse
  tam ekran, `excel.py`/`karekod.py`'deki "kütüphanesiz" gerekçenin aynısı
  (PDF.js gibi bir kütüphane eklemeye gerek yok). `/goruntu/{id}/sil` onay
  ekranında da aynı ayrım: PDF için `<embed type="application/pdf">`, görüntü
  için `<img>` (`goruntu_sil_ekran()`'da hesaplanan `pdf_mi` bayrağıyla).
- **`_buyutec.html` include eden her ekran kendi tıklama betiğini yazar**
  (paylaşılan bir global yok) — `cycle_detay.html`'e yeni eklenirken bu ilk
  kez oraya girdi, `.notfoto` sınıfı ve kablolaması diğer ekranlardaki
  `.stripkare`/`.arsivfoto` desenlerinin birebir kopyası.
- Silme ayrı bir rota istemedi: `/goruntu/{id}/sil` zaten genel
  (`yol_modulu()`'nda `son == "sil"` → `silme` modülü, asama'dan bağımsız).

**Cycle ekranında "Oositler" numara şeridi ve genel "Fotoğraf ekle" düğmesi
yerini türetilmiş bir embriyoloji özetine bıraktı** (v6.110, kullanıcının
isteği: "Oositler ve Fotoğraf ekleyi kaldır, kısa bir özet olsun: kaç
yumurta, M2, döllenen, cleavage, blastokist"). `app.py` `cycle_ozet()` —
`disari.istatistikler()`'deki lab-geneli `_olay()` sayımının **tek-cycle**
hali, aynı "sayaç tutma, her açılışta türet" gerekçesi (v6.38): oosit
toplanan sayısı `specimen` tablosundan, M2 `olay.tip='maturasyon_kontrolu'
AND mat_deger='mii'`den, döllenen `olay.tip='fertilizasyon_kontrolu' AND
fert_pn_sayisi='2'`den, cleavage/blastokist ise ilgili
`*_degerlendirme` olaylarının **DISTINCT specimen_id** sayısından geliyor
(bir örnek gün 2 VE gün 3'te değerlendirilmişse iki kez sayılmasın diye).
Ayrı bir sayaç sütunu yok — aşama ekranlarından biri düzeltilir/iptal
edilirse özet otomatik doğru kalır, cryo haritası ve istatistik
ekranındaki "türetilmiş sayı" gerekçesinin aynısı. **v6.146'dan beri
sayılan, bu tedavide YAPILAN işlemler** (`db.tedavide_yapilan()`, aynı
sayfadaki zaman çizelgesiyle aynı koşul): FET (3→5 kültür)'te çözülen
embriyonun blastokisti FET'in kutusunda, kaynak ICSI'ninkinde değil. Var
olan 120 tedavinin 480 sayısı değişmedi (denendi).
- **Hangi satırın gösterileceği cycle tipine göre değişir.** `cycle_ozet()`
  çağırana `cycle_asamalari()`'nin zaten hesapladığı kod kümesini alıyor
  (kendi başına tekrar hesaplamıyor) — "Toplanan" yalnızca `opu` aşaması
  varsa, "M2" `denudasyon` ya da `icsi` varsa (ICSI ekranında mı yoksa
  `oosit_cryo`'da denüdasyon ekranında mı sorulduğu fark etmez, ikisi de
  aynı `olay.tip` yazıyor — v6.96), "Döllenen" yalnızca `fert`, "Cleavage"
  yalnızca `cleavage`, "Blastokist" yalnızca `blast` aşaması varsa. Yumurta
  Çözme'de "Toplanan"ın yerinde "Çözülen yumurta sayısı" (kırılımında
  canlı, v6.147, `db.cozulen_yumurta_islenir()`). `fet` gibi bu
  aşamaların HİÇBİRİ olmayan bir tipte özet listesi
  tamamen boş döner ve kart hiç basılmaz — "0 M2" yazmak "ölçülmedi"
  ile "sıfır çıktı"yı karıştırırdı, bu yanlış bilgi olurdu. Yeni bir cycle
  tipi eklersen (bkz. "Embriyo Dondurma ve Sperm Dondurma" bölümündeki dört
  adım) bu koşulları elden geçirmene gerek yok — `TIP_ASAMALARI`'na
  eklediğin kod kümesi otomatik doğru satırları seçer.
- **Fotoğraf eklemek kaldırılmadı, yalnızca cycle ekranındaki genel giriş
  noktası kaldırıldı.** `/cycle/{id}/foto-ekle` rotası aynen duruyor — her
  aşama ekranının kendi "Fotoğraf ekle" düğmesi (`specimen_id` ve `asama`
  parametreleriyle, v6.20'nin zaten söylediği yerden) hâlâ oraya gidiyor.
  Kaldırılan yalnızca `cycle_detay.html`'deki **parametresiz** bağlantıydı —
  o zaten "cycle ekranında fotoğraf olmaz" kuralının (v6.20) sessiz bir
  istisnasıydı, hemen üstündeki yorum bile bunu söylüyordu.
- **v6.112'de bu özet, sayfanın en üstündeki eski Folikül/Toplanan/Kayıtlı
  kutusuyla BİRLEŞTİ — tek kutu.** Kullanıcının isteği: "Bu ikisi
  birleşsin, sayfanın en üstünde Folikül Sayısı, Toplanan Yumurta Sayısı,
  M2 (Olgun) Yumurta Sayısı, Döllenen Yumurta (2PN) Sayısı, Cleavage
  Sayısı, Blastokist Sayısı şeklinde bilgilendirme alanı olsun." `cycle_
  ozet(cycle, kodlar)` artık `cycle_id` değil **`cycle` satırının tamamını**
  alıyor (Folikül ve OPU sağ/sol sayıları için) — sol sütunun ilk kartı
  oldu, sağ sütundaki ayrı kart kaldırıldı.
  - **"Kayıtlı" (specimen kaydı sayısı) bilerek düşürüldü** — kullanıcının
    verdiği liste yalnızca altı kalem, "Kayıtlı" onda yok. Örnekler hâlâ
    aşama ekranlarından erişilebiliyor, yalnızca bu özet kutusunda ayrı
    bir satırı kalmadı.
  - **"Toplanan" artık specimen `COUNT(*)` değil, OPU'da elle girilen sayı**
    (`opu_sag_oosit` + `opu_sol_oosit`) — v6.110'da yanlışlıkla specimen
    sayısı kullanılmıştı ve bu, üstteki (o zaman ayrı duran) kutunun aynı
    adı taşıyan ama **farklı bir şey ölçen** "Toplanan Oosit"'iyle
    çakışıyordu (biri OPU'nun kendi girdisi, öbürü sonradan açılan kayıt
    sayısı). İki kutu birleşince bu çakışma görünür hale geldi ve
    düzeltildi: tek "Toplanan" kaldı, OPU'nun kendi sayısı kazandı —
    "kaç yumurta alındı" sorusunun klinik cevabı o, oositin ne zaman ayrı
    bir specimen kaydına döküldüğünden bağımsız. **Yeni bir "toplanan"
    türü sayı eklersen bu ayrımı hatırla**: OPU girdisi mi, yoksa
    sonradan oluşan kayıt sayısı mı — ikisi aynı şey değil, aynı adı
    paylaşmamalı.
  - **Folikül tek satır, koşulsuz** (diğer beşi gibi `kodlar`'a bakmıyor)
    — cycle seviyesinde bir alan, `opu.html`'de de koşulsuz basılıyor;
    `fet` gibi hiçbir embriyoloji aşaması olmayan bir tipte bile tek
    başına gösteriliyor (değeri girilmemişse `—`).
  - Yeni metin anahtarları: `ozet_folikul`, `ozet_toplanan`,
    `ozet_cleavage`, `ozet_blastokist` (`cleavage_ad`/`blastokist_ad`
    **bilerek kullanılmadı** — onlar `cleavage_sil.html`/`blast_sil.html`
    gibi başka ekranlarda "aşama adı" olarak geçiyor, metnini "Cleavage
    Sayısı" yaparsan oralardaki cümle bozulur). `toplanan_oosit`/`folikul`/
    `kayitli` eski anahtarları **dokunulmadan** kaldı — `opu.html`'in kendi
    salt okunur kartı hâlâ onları kullanıyor, cycle_detay'in bu özetle
    ilgisi yok.
  - `specimenler`/`taraf` context değişkenleri `cycle_detay()` rotasından
    kaldırıldı — o kartın kaldırılmasıyla birlikte hem şablonda hem
    sorguda **hiçbir yerde** kullanılmıyorlardı (üç alt sorgulu `specimen`
    sorgusu dahil), gereksiz sorgu koşusun diye tutmaya gerek yoktu.

**Kodu değil etiketi göster.** `mii`, `2pn`, `z1` gibi değerler
`liste_degeri`'nde ve laba özgü — yönetici düzenleyebiliyor. Ekranda
`liste_etiket(liste_adi, kod)` (Jinja global) kullan, sabit sözlük yazma.

**Kategoriler kesinleşmemişse: "öneri menüsü + serbest yazı" (`<datalist>`),
kapalı `<select>` değil** (v6.100'de doğum kilosuyla denendi, kullanıcı
istemedi — v6.101'de sperm dondurma sebebine uygulandı, orada kaldı).
`<input list="...">` + `<datalist id="...">` sık kullanılan değerleri
dropdown gibi önerir ama kutuya elle **başka bir şey de yazılabilir** —
kategorisi henüz netleşmemiş serbest metin bir alanda (`sperm_dondurma.
sebep` gibi, v6.86'dan beri bilerek açık) kapalı bir liste kullanıcının
aklında olmayan bir sebebi yazmasını engeller. **Sayısal alanlarda
(kilo gibi) denenmedi kalmalı** — v6.100'de gebelik'teki doğum kilosuna
uygulandı (0,50–5,00 kg arası öneri), kullanıcı v6.101'de "eskiye çevir,
beğenmedim" dedi; sebep sorulmadı, düz `<input type="text" inputmode=
"decimal">`'e geri dönüldü. Tekrar denemeden önce kullanıcıya sor. `liste_
degeri` + `liste_etiket()` deseni hâlâ geçerli — **yalnızca** liste laba
özgü ama sabit/kapalı olması gereken yerlerde (mii, 2pn, z1 gibi, yönetici
düzenler ama ekrandaki kişi listenin dışına çıkamaz). Yeni bir alan
yazarken kendine sor: "listede olmayan bir değer girilmesi gerekebilir
mi?" — evetse datalist, hayırsa `liste_degeri`/`<select>`.

**Ekranda tarih gün.ay.yıl sırasıyla basılır, ISO değil** (v6.64, v6.67'de
tüm ekranlara genişledi). Veritabanı ISO (`YYYY-MM-DD[ HH:MM:SS]`) tutmaya
devam ediyor — kaydetme, arama, sıralama, karşılaştırma (`cycle_detay.html`
`planlanan_tarih[:10] > bugun` gibi) hep ISO'ya güveniyor, bu değişmedi.
Yalnızca **ekrana basarken** iki Jinja global var: **`gg_aa_yyyy(tarih)`**
saat taşımayan alanlar için (`'2026-09-04'` → `'04.09.2026'`), **
`gg_aa_yyyy_saat(zaman)`** saat de taşıyan kayıtlar için
(`'2026-09-04 08:15:00'` → `'04.09.2026 08:15'`). `[:10]`'u elle dilimleyip
ekrana basma — yeni bir tarih/zaman alanı ekranda görünecekse bu ikisinden
birini çağır. (`type="date"`/`type="datetime-local"` form alanları istisna:
tarayıcı değeri kendi yerel biçiminde gösteriyor, `value` ISO kalmalı.)
`takvim_basligi(tarih)` ayrı kalıyor — gün adı + ay adını yazıyor
("16 Eylül 2026 Çarşamba"), planlanan tarih gibi zaten günün önemli olduğu
yerlerde kullanılıyor.

**Ana ekran yapılacaklar listesidir** (v6.28). Kullanıcının kâğıt düzeni:
laboratuvarda işi bitmemiş hastaların formları bir klasörde durur, her sabah
ona bakılır, iş bitince form arşive kaldırılır. `/` tam bunun karşılığı —
`durum='aktif'` cycle'lar, hasta adı, dosya no, cycle no, OPU günü ve son
işlem. Altında **"Bugün bitenler"** (v6.29) — ölçü
`date(bitis_zamani) = date('now','localtime')`, yani kart her gece
kendiliğinden boşalıyor; saklanan bir "bugünün listesi" yok, olmasın da.
Sonra sayı özeti, en altta menü.

Düzen (v6.34'te iki kart, v6.67'de kullanıcının isteğiyle üçe çıktı):
**Devam Eden Tedaviler, Bugün Biten Tedaviler ve Yaklaşan Tedaviler üçü de
yan yana.** `.ucsutun` **medya sorgusu kullanmıyor** — her kart `flex: 1 1
190px` istiyor, sığan kadarı aynı satırda duruyor, gerisi sarıp alt satıra
iniyor (aşama ekranlarındaki "sabit kırılma noktası yerine sarma" deseninin
aynısı, aşağıdaki "İki sütun her ekranın çözümü değil" bölümüne bak). Sıra
HTML sırasıyla aynı, telefonda kendiliğinden tek sütuna düşüyor. **Basis
190px, 260 değil** (v6.68'de düşürüldü) — `--genis-sutun` yan menüye pay
ayırdığı için 640px'e kadar daralabiliyor, 260'ta taban ihtiyaç
(3×260+2×16=812px) 640-1350px arası viewport'ların hiçbirine sığmıyordu;
kullanıcı 24" ekranında kartların yan yana durmadığını bildirdi. 190'da
taban ihtiyaç (602px) garantili en dar `--genis-sutun`'un (640px) bile
içinde — **her** genişlikte (≥1100px) üçü yan yana kalıyor. Ana ekran
`kap genis` sınıfını alıyor, sütunu 940px'e kadar genişliyor ama yan
menüyle çarpışmasın diye `calc(100vw - 500px)` ile sınırlı. Yeni bir kart
eklersen bu üç sütunu şişirme, altına koy; kart basisini büyütürsen aynı
sığma hesabını (3×basis + 2×16 ≤ 640) tekrar yap.

**Devam Eden Tedaviler en yeniden eskiye sıralanır** (v6.137, kullanıcının
isteği). v6.28'de bilerek tersiydi ("unutulan bir cycle dibe düşmesin");
kullanıcı değiştirdi — günlük iş en yeni hastada. `cycle_listesi()`'nin
yalnızca **yapılacaklar** dalı `DESC` oldu, öteki listeler (`/bitenler`,
ay listesi, Yaklaşanlar) kendi sıralarını koruyor. Kart 5 satır gösterdiği
için (v6.78) en eskiler artık `/devam-eden`'de kalıyor.

**Üç kart da en fazla 5 satır gösterir, fazlası "Tümü" ile ayrı ekrana
gider** (v6.78, kullanıcının isteği). `ana.html` her listeyi `liste[:5]`
diye kırpıyor ama **rozet sayısı kırpılmıyor** — `liste|length` hep gerçek
toplamı gösterir, "Tümü" bağlantısı da `liste|length > 5` iken basılır.
Hedefler: Bugün Biten Tedaviler → `/bitenler` (v6.29'dan beri var, sadece
görünürlük koşulu eklendi), Devam Eden Tedaviler → yeni `/devam-eden`,
Yaklaşan Tedaviler → yeni `/yaklasanlar` (`cycle_listesi(yaklasan=
YAKLASAN_GUN)`'ın kırpılmamış hali, aynı 14 günlük pencere). İkisi de
`bitenler.html`'in kopyaladığı kalıp: `_cyclesatir.html` `satir()` makrosu,
`yol_modulu()`'nda özel kural yok (görüntüleme ekranı, middleware
varsayılanı kapsıyor). **Bu, kaldırılmış `/takvim`'in geri gelmesi değil**
(v6.65) — ay ızgarası yok, düz liste; "aynı şey gibi görünme" gerekçesi
burada geçerli değil çünkü kart zaten var, yalnızca taşan kısmı ayrı sayfaya
alıyor.

> v6.18'de bu ekranda **hasta adı yoktu** (ekrana bakan herkes listeyi
> görüyordu). Kuralı v6.28'de **kullanıcı kendi isteğiyle gevşetti**: adsız
> bir liste her sabah bakılan klasörün işini görmüyor. Kendiliğinden geri
> alma — bu bilinçli bir denge, ona sormadan değiştirme.

**Cycle'ın bitişi silme değildir** (v6.28, `goc_027`). Üç son var ve ikisi
olağan: `bitis_sebebi` ∈ `dondurma` | `transfer` | `iptal`. İlk ikisi
`durum='tamamlandi'`, üçüncüsü silme ekranından beri var olan
`durum='iptal'` yapar. Eşleme `BITIS_DURUMU`'nda, listeyi `cycle_listesi()`
kuruyor. Düğme **üç ekranda**: cycle, vitrifikasyon, transfer — işin gerçekten
bittiği yer çoğu zaman son iki aşama (v6.29). Üçü de `_bitir.html`
`dugme(c)` makrosunu çağırıyor; koşul ve yazı tek yerde dursun diye
şablona elle yazma. → `/cycle/{id}/bitir`.
- **Geri al ekranda hep tek.** "Bitir" ekranından kapatılan cycle
  `/cycle/{id}/bitisi-geri-al` ile döner; silme ekranından iptal edilmiş eski
  kayıtlar `/cycle/{id}/geri-al` ile. İkincisi `not c.bitis_sebebi` ile
  susturuluyor, yoksa yan yana iki geri al çıkar.
- **Bitirmek `yetkim("silme")` istemez**, geri alması da. Günlük bir iş;
  `yol_modulu()` bu yolları bilerek modülsüz bırakıyor. Rotayı
  `geri-al` diye adlandırma — o ad "silme" modülüne düşer.
- **Bitiş saati elle girilebilir** (v6.31) — "işlem saatleri elle girilebilir"
  kuralı burada da geçerli, v6.28'de atlanmıştı. Geriye tarihlenen bitiş
  "Bugün bitenler"de görünmez; bu doğru davranış.
- **Düzenle ile Listeye geri al ayrı iki düğme.** `?duzenle=1` sebebi ve
  saati değiştirir, cycle'ı listeye **döndürmez**; geri almak ayrı. İkisini
  birleştirme.
- Biten cycle'lar `/bitenler`'de; kayıt silinmiyor, hasta ekranında da
  rozetiyle duruyor.
- **İptalin altı ayrıntılı sebebi var** (v6.103, kullanıcının isteği):
  Yumurta Çıkmadı, İmmatür Yumurta, Fertilizasyon Olmadı, PN Arrest,
  Cleavage Arrest, 5. Gün Arrest — `IPTAL_DETAY_SEBEPLERI`, hepsi
  `BITIS_DURUMU`'nda `"iptal"`e eşleniyor (`durum='iptal'`, genel İptal'le
  aynı). **Genel "İptal" düğmesi kaldırılmadı** — kullanıcının kararı:
  listede olmayan bir sebep için hâlâ kullanılabiliyor. `cycle_bitir.html`
  bu altısını genel üç seçeneğin altında ayrı bir grupta gösteriyor; `metin()`
  anahtarı yine `"bitis_" ~ kod` deseninde (`_cyclesatir.html` ve
  `cycle_detay.html`'in `bitis_sebebi` gösterimiyle aynı kalsın diye) —
  yeni bir ayrıntılı sebep eklersen kodu `IPTAL_DETAY_SEBEPLERI`'na ekle,
  `metinler.py`'ye `bitis_<kod>` anahtarını yaz, `BITIS_DURUMU` kendiliğinden
  kapsar (`**{k: "iptal" for k in IPTAL_DETAY_SEBEPLERI}` ile kuruluyor).
  Şema değişmedi — `bitis_sebebi` zaten CHECK'siz serbest metin.
- **Seçilen iptal sebebi resmî formlara da yansır** (v6.104, kullanıcının
  isteği). `formlar._iptal_notu(c)`: `c["durum"]=="iptal"` ise seçilen
  sebebin ekran etiketini döndürür (`metin("bitis_"+bitis_sebebi)`) — bu
  çağrı `metin()`'e adresten gelen bir anahtar vermiyor, `bitis_sebebi`
  zaten `cycle_bitir()`'in `BITIS_DURUMU` ile doğruladığı bir kod (tuzak #9
  burada geçerli değil). **Embriyoloji Özet'te** mevcut NOTLAR kutusuna,
  protokol notu ve çözme notunun (v6.102) altına üçüncü satır olarak
  eklenir — kutunun kendi puntosunu kullanır, ayrı bir vurgu yok.
  **ART Lab'da NOTLAR gibi bir kutu yoktur** — kullanıcının isteği "alt
  kısmında tam ortada, büyük punto" olduğu için kalıbın **dışına**, son
  sayfanın hemen altına yeni bir şerit ekleniyor:
  - Ekranda `form.html`'de `{% if iptal_notu and loop.last %}` ile
    `.formiptalnotu` (`static/style.css`) — sabit siyah/beyaz (kâğıt aslı
    gibi), `.kalip`'in p7..p14 ölçeğinden bağımsız sabit 15pt kalın ortalı.
  - Excel'de `app.py` `form_excel()`, `ad=="artlab"` iken son sayfanın
    `hucreler`/`birlesik`/`yukseklikler` sözlüklerine elle bir satır ekliyor
    — `form_kalip.olcu(kalip)` kalıbın satır/sütun sayısını, `hucre_adresi()`
    Excel adresini veriyor (`_adres()`'in genel hali). Stil hazır adlı
    `"formadi"` (`excel.STILLER`, 14pt kalın ortalı) — kalıbın **kendi**
    stil listesine (`k["stiller"]`, paylaşılan/önbellekli) dokunmadan,
    `excel._yerlesim_xml()` string stil adını doğrudan `STILLER`'den
    çözüyor. **`form_kalip.py`'nin kendisi (kalıp/JSON) değişmedi** — "kalıba
    dokunma" kuralı bu satır için de geçerli, o yüzden ekleme kalıbın
    ürettiği ızgaranın bittiği yerden, tamamen dışarıdan yapılıyor.
  - Yalnızca `ad=="artlab"` iken devreye giriyor — Özet zaten NOTLAR'a
    yazıyor, ikinci kez basılmasın diye `iptal_notu` context'i Özet'e hiç
    verilmiyor.

**İleri tarihli iş cycle'ın kendisidir** (v6.33, `goc_028`). Ayrı bir randevu
tablosu yok: cycle bugün açılıyor, `planlanan_tarih` (gün, saat yok)
giriliyor. Kullanıcının kararı — ayrı kayıt aynı hastayı iki kez girdirirdi.
- **Tarihi gelecekte olan cycle Yapılacaklar'da görünmez.** Takvimde ve ana
  ekranın "Yaklaşanlar" kartında durur, tarih gelince kendiliğinden listeye
  düşer. Bu kuralı gevşetme: haftaya olacak bir iş bu hafta boyunca her sabah
  listeyi şişirirdi.
- "Yaklaşanlar" **bugünü içermez** (`> bugün`), penceresi `YAKLASAN_GUN` = 14.
- `/takvim` **gün gün liste**, ay ızgarası değil — telefonda okunaklı, işi
  olmayan gün yer kaplamıyor. Ay seçici hasta kayıtlarınınkiyle aynı.
- Gün adları `metinler.py`'de (`gun_1`…`gun_7`, ISO sırası), ekrana
  `takvim_basligi(tarih)` basıyor. `strftime("%A")` **kullanma**.
- **`cycle_alanlari()`** göç çalıştırılmamışsa `planlanan_tarih`'i
  INSERT/UPDATE'ten çıkarıyor. `CYCLE_ALANLARI`'na yeni bir kolon eklersen
  aynısını yap — yoksa göçü çalıştırmamış makinede **cycle açmak tümden
  bozulur** (tuzak #3'ün en pahalı hali).

**Excel çıktısı kütüphanesiz üretilir** (v6.36). `.xlsx` içinde XML olan bir
ZIP; `excel.py` onu `zipfile` ile yazıyor. **Buraya `openpyxl` sokma** —
klinikteki Windows mini PC'ye kurulum eklemek demek, projenin "ek bağımlılık
yok" kuralı bunun için var. `excel.kitap([(ad, başlıklar, satırlar), ...])`
bayt döndürür; hücrenin türü değerden anlaşılır (ISO metin tarih olur).
Yılı 1900'den küçük tarih **metin** yazılır: bozuk `0026-09-04` kaydı
(bekleyen iş 6) dosyayı bozmasın diye.
- **Bu ISO-tarih algılaması yalnızca `_DUZ` (varsayılan) biçimli hücrelerde
  çalışır** (v6.94'te doğrulandı). Resmî formların "yerleşim" sayfasında
  (`form_kalip.yerlesim()` → `excel._yerlesim_xml()`) her hücre kalıbın
  kendi stilini taşıyor, hiçbir zaman `_DUZ` değil — o yüzden oradaki
  tarihler zaten hep düz metin (`inlineStr`) yazılıyor, ISO biçimine
  bağlı değil. `formlar.py`'deki tarih alanlarını (`opu_tarihi`,
  `saat_<asama>` gibi) gün.ay.yıl'a çevirmek bu yüzden Excel çıktısını
  bozmadı (v6.94, `_gg_aa_yyyy()`/`_gg_aa_yyyy_saat()`). Bu ayrımı
  karıştırma: **tablo sayfalarındaki** (ay listesi, `/disari/tumu` gibi)
  tarihler hâlâ ISO kalmalı, resmî formların yerleşim hücreleri artık
  gün.ay.yıl.

**Excel çıktısının izni ekranın iznidir** (v6.36). Dört çıktı var:
`/disari/ay`, `/disari/cycle/{id}` (ikisi görüntüleme gibi serbest),
`/disari/cryo` (`yol_modulu` onu `cryo`'ya bağlıyor) ve `/disari/tumu`.
- **`/disari/tumu` yalnızca yönetici** — rota `yonetici_kontrol(request)` ile
  başlıyor. Ötekiler ekrandaki veriyi verir, bu laboratuvarın tamamını tek
  dosyada klinik dışına çıkarabilir. Bu kuralı gevşetme.
- **Dökümde şifre ve oturum anahtarı yok.** `oturum`/`yetki` hiç çıkmıyor,
  `kullanici`'dan yalnızca `KULLANICI_KOLONLARI`. Yeni bir tabloya gizli bir
  alan eklersen `disari.TUM_TABLOLAR`'ı gözden geçir.
- Yeni bir çıktı eklersen sorguyu `disari.py`'ye yaz, rotayı `app.py`'ye:
  bütün rotalar orada duruyor.
- Ay listesinde **çözme ve transfer tedavinin yapıldığı cycle'a** yazılır
  (`thaw_cycle_id` / `tr_cycle_id`), örneğin geldiği cycle'a değil — FET'te
  oosit yok ama transfer var.
- `specimen.durum` **kodla** yazılır; on dörde yakın değerinin çoğunun
  karşılığı yok, yarısını çevirmek sütunu tutarsız yapar. Etiket listesini
  kullanıcıya sormadan uydurma.

**Resmî formlar kâğıt aslının kalıbıyla basılır** (v6.37, v6.39'da birebir
oldu). İki form, ikisi de kullanıcının tutmak **zorunda** olduğu kurum
formları: Embriyoloji Özet (DH.FR.91, dikey) ve ART Lab. Raporu (DH.FR.107,
yatay). Her biri iki çıktı veriyor — yazdırılabilir sayfa
(`/form/{ad}/{id}`, Ctrl+P) ve Excel (`/disari/form/{ad}/{id}`) — ve **tek
kalıptan**: `form_kalip.json`.
- **Ekrana sığma, A4'e sığmadan AYRI bir sorun** (v6.107, v6.108,
  kullanıcının isteği — "formlar sığmıyor", sonra "kesik gözüküyor").
  `.kalipkap` kâğıdın **doğal** boyutunda kalmak zorunda (660x1040 dikey/
  Özet, 980x713 yatay/ART Lab — `static/style.css`'teki min-width, amblemin
  yüzdeyle hesaplanan yeri buna göre, bkz. yukarıdaki yorum); dar bir
  telefon ekranında yatay kaydırma gerekiyordu (v6.107), geniş bir
  masaüstü/mini PC ekranında genişlik zaten sığdığı için hiç
  ölçeklenmiyordu ama dikey Özet formu (1040px doğal boy) ekran
  yüksekliğinden taşıp kesik görünüyordu — kullanıcı v6.108'de bunu
  bildirdi. Çözüm `form.html`'de `.kalipolcek` sarmalayıcı + küçük bir betik
  (`formlariSigdir()`): `.kalipkap`'ı **bütün olarak**
  (`transform: scale(oran)`) hem mevcut genişliğe HEM YÜKSEKLİĞE
  (`window.innerHeight` eksi sarmalayıcının üstteki başlangıç konumu)
  sığdırıyor, **ikisinden küçük olan** oranı kullanıyor — tıpkı bir yazıcı
  önizlemesi gibi kâğıdın tamamı tek ekranda görünüyor. Punto, sütun, amblem
  hepsi birlikte küçülür, oranlar bozulmaz, kâğıdın kendisi
  (`form_kalip.json`, "kalıba dokunma" kuralı) hiç değişmez. `resize` ve
  `orientationchange`'de yeniden hesaplanıyor; `<img class="kalipgorsel">`
  (**v6.158: çok sayfalı formda bütün sayfalar AYNI oranla, kullanılabilir
  yükseklik ilk kâğıdın belge içindeki tepesinden** — her sayfa kendi
  tepesinden ölçülünce ikinci sayfa ilkinin altında küçücük kalıyordu,
  kullanıcı bildirdi)
  (amblem) geç yüklenip doğal boyu değiştirebildiği için `load` olayında da
  tekrar çalışıyor. **Yükseklik hesabı `getBoundingClientRect().top`'a
  dayanıyor** — bu, sarmalayıcının SAYFA YÜKLENDİĞİNDEKİ konumu; kaydırma
  pozisyonuna göre yeniden hesaplanmıyor (yalnızca `resize`/
  `orientationchange`'de tetikleniyor), yoksa kullanıcı sayfayı kaydırdıkça
  ölçek anlamsızca değişirdi. **Yazdırmaya karışmaz**: `@media print` bu
  ölçeği `!important` ile `transform: none` yapıp iptal ediyor (satır içi
  `style` ile yazıldığı için normal öncelik yetmez) — çıktı her zaman
  kâğıdın gerçek boyutunda, A4'e sığdırma (`s.olcek`, server-side, ayrı bir
  mekanizma) hiç etkilenmiyor. Playwright ile dört ekran boyutunda
  (375x812, 390x844, 1280x900, 1920x1080) doğrulandı: `.kalipolcek` artık
  hiçbirinde ne yatay ne dikey taşıyor (`scrollWidth == clientWidth` VE
  `getBoundingClientRect().bottom <= innerHeight`), yazdırma çıktısı (PDF)
  öncesi/sonrası birebir aynı boyutta kaldı.
  - **`transform-origin: top left` ŞART, yoksa küçültme ORTAYA doğru büzülür**
    (v6.109). v6.107/v6.108'in ölçeği doğru hesaplıyordu ama `.kalipkap`'a
    `transform-origin` hiç yazılmamıştı — CSS varsayılanı `center center`.
    `.kalipolcek` sarmalayıcının yüksekliği betikte küçültülmüş boy kadar
    (sol-üstten sayarak) ayrılıyordu; `.kalipkap` ortadan küçülünce içeriğin
    yarısı sarmalayıcının **üstüne** taşıyordu (kırpılmıyordu, `overflow:
    hidden` onu görünmez yaptı) ve alt yarısı da sarmalayıcının dışına, aşağı
    taşıp yine kırpılıyordu — ekranda kalan tek şey ortadaki dar bir şerit.
    Kullanıcı ekran görüntüsüyle bildirdi: kartın üst yarısı bomboştu, form
    yalnızca en altta yarım görünüyordu ("Mobilde böyle gözüküyor. Masaüstünde
    de kesik tam ekran değil"). Düzeltme tek satır: `.kalipkap { transform-
    origin: top left; }` — artık küçültme sol-üst köşeden başlıyor, sarmalayıcının
    ayırdığı alanla birebir örtüşüyor. **Bu hata v6.107/v6.108'in Playwright
    testlerinde yakalanamadı** çünkü testler yalnızca `.kalipolcek`
    sarmalayıcının **kendi** `getBoundingClientRect()`'ine bakıyordu —
    sarmalayıcının boyutu içindeki `.kalipkap`'ın nereye render edildiğinden
    bağımsız, hep doğru çıkıyordu. Gerçek hatayı yalnızca ekran görüntüsü (ya
    da içerideki `.kalip` tablosunun sarmalayıcıya göre konumunu ölçmek)
    ortaya çıkardı. **Ders**: `transform: scale()` kullanan her yeni yerde
    `transform-origin`'i açıkça yaz, varsayılana güvenme; test yazarken de
    yalnızca dış kabın ölçüsüne değil, içindeki asıl içeriğin göründüğü yere
    bak (bir ekran görüntüsü, sarmalayıcı geometrisinin kaçırdığı hatayı
    yakalar).
- **Kalıp elle yazılmadı, kâğıttan çıkarıldı.** `formlar_asil/` altındaki iki
  orijinal `.xls` dosyası `kalip_uret.py` ile okundu; satır yükseklikleri,
  sütun genişlikleri, birleşik hücreler, puntolar ve dört kenarın çizgi tipi
  oradan geliyor. **`form_kalip.json`'ı elle düzenleme** — kâğıt asıl
  değişirse onu değiştir, sonra aracı tekrar çalıştır (araç `xlrd` istiyor;
  programın bağımlılığı değil, tek seferlik geliştirme aracı).
- **Kalıba dokunma.** Doküman kodu, revizyon tarihi, alan adları ve form
  numarası kalite sisteminden geliyor. Kâğıttaki **yazım hataları da öyle**:
  "TRANSFES EMBRİYOLOG", "Nukleus durmu", "Labratuvar", "Oasit tipi" —
  düzeltme, belge o.
- `formlar.py` kalıbı kurmuyor, **dolduruyor**: `*_verisi()` veriyi toplar,
  `*_dolgu()` hücre adreslerine dağıtır. İki tür dolgu var: `deger` kâğıtta
  boş olan kutuya yazar, `ek` kâğıtta basılı yazının arkasına ekler
  (`"Dosya No :"` + numara).
- **Programda karşılığı olmayan alan boş kalır** (kimlik no, empty zona,
  intakt, tüp no, medium/lot, seleksiyon, transfer klinisyeni, 24. saat
  hücre sayısı). Uydurma — resmî forma yanlış veri yazmak boş bırakmaktan
  kötü. Kullanıcı hangilerinin programa gireceğine sonra karar verecek.
- **ART raporunda gün 2 "40-45 saat", gün 3 "72 saat" satırına yazılır.**
  Eşleme olduğu için kullanıcıya soruldu, **"kalsın" dedi** (2026-09-11).
  Boşaltma. "24 saat : hücre" satırı boş — programda o kayıt yok.
- **Oosit 13'ü geçerse kalıp ikinci kez basılır** (kâğıtta ikinci form).
  Sütun ekleme, kırpma da yapma; özet bloğu yalnızca ilk sayfada.
- **Amblem de kalıptan** (v6.39): üniversitenin logosu iki `.xls`'in içine
  gömülüydü, `kalip_uret.py` `static/form_amblem.png`'ye çıkardı. Yeri
  kâğıttaki **sabitleyiciden** (Excel client anchor) hesaplanıyor — ekranda
  mutlak konumlu `<img>`, Excel'de `twoCellAnchor` çizim parçası. Amblemi
  başka bir yere taşıma, boyunu elle verme: iki hücre arasına oturduğu için
  "sayfaya sığdır" ile birlikte küçülüyor.
- Ekranda ve Excel'de aynı ızgara: `form_kalip.satirlar()` ve
  `form_kalip.yerlesim()`. Şablon tek: `form.html`.
- Form adı adresten geliyor; `FORMLAR` **beyaz listesinden** geçiyor. Şablon
  adını adresteki metinle kurma.
- `excel.py`'nin **yerleşim sayfası** bunun için var. Taban stillerin sırası
  dosyaya sayı olarak yazılıyor — `_TABAN_XF`/`STILLER`'e **araya değil sona**
  ekle. Kalıbın kendi stilleri `styles.xml`'in sonuna, sayfa başına ekleniyor.
- **`worksheet` içindeki etiket sırası OOXML şemasında sabit** (v6.76).
  `<drawing>` (amblem) `<pageMargins>`/`<pageSetup>`'tan **önce** yazılmıştı
  — şema bunun tam tersini istiyor (`mergeCells → ... → pageMargins →
  pageSetup → ... → drawing`). Excel dosyayı "bir kısmı onarılmalı" diye
  açıyor, amblemi düşürüyordu. `excel.py`'de `_sayfa_xml()`'e yeni bir
  `<...>` eklersen sırayı ECMA-376 `CT_Worksheet` sırasıyla karşılaştır,
  tahminle ekleme — `openpyxl`'in istisna vermemesi yetmez (o sırayı sıkı
  denetlemiyor), gerçek Excel'de açıp dener gibi düşün.
- **Birleşmiş bir kutunun sağ/alt kenarlığı ANCHOR'da değil, kutunun en
  sağ/en alt hücresinin KENDİ kenarlığında** (v6.77). Excel birleştirmede
  her hücrenin kendi sınırını korur, devretmez — `form_kalip.izgara_kur()`
  birleşmenin kapladığı hücreleri (anchor hariç) atlıyordu, bu yüzden Excel
  çıktısında kutuların sağ tarafı kesik görünüyordu (kullanıcı fark etti).
  Düzeltme `izgara_kur()`'da, hem `kalip_uret.py` hem `xlsx_oku.py`'yi
  kapsıyor — ayrı bir kopya yazma. **`form_kalip.json` türetilmiş bir
  dosya**: kenarlık/ızgara mantığında yeni bir hata bulursan `izgara_kur()`'u
  düzelt, sonra `python3 formlar_asil/kalip_uret.py <ozet.xls> <artlab.xls>`
  ile kalıbı yeniden üret — JSON'ı elle düzenleme, bu "kalıba dokunma"
  kuralını çiğnemez çünkü değişen kâğıt değil, aracın kendi hatası.
- Form **iki dilde de Türkçe** basılır: kurum belgesi, arayüz metni değil.
- **Dondurulan örnekler iki forma da tek yerden yazılıyor** (v6.135,
  kullanıcının isteği). `formlar.dondurma_tupleri(cycle_id)` — `olay.
  vit_tasiyici_id`'ye göre gruplanmış tüpler, her tüpte örneklerin kalitesi
  ve günü. **Bir tüp = bir taşıyıcı, bir parantez = bir tüp**; kullanıcının
  Access'teki kendi yazımı da bu ("(3AA) (3AA)" ayrı tüpler,
  "(4HG2-4HG2-3HG2)" bir tüpte üç embriyo — `aktar_access.py` v6.132 aynı
  kuralı okuyor). Yeni bir yerde "hangi tüpte ne var" diye soracaksan bu
  fonksiyonu çağır, ikinci bir sorgu yazma: Özet'in NOTLAR'ı ile ART Lab'ın
  FREEZE sütunu birbirini tutmak zorunda.
  - **Kalite** `bl_skor`, cleavage'da hücre+skor ("8HG2") — Cryo
    Haritası'nın gösterdiği alanın aynısı. **Gün** örneğin kendi son
    değerlendirmesinin günü; "kaçıncı günde donduruldu" diye bir alan yok
    ve uydurulmuyor, değerlendirmesi olmayan örnek güne katkı vermiyor.
  - Özet'te: "EMBRİYO DONDURMA AŞAMASI" kutusu **gün** basıyor (v6.135'e
    kadar blastokist genişleme etiketiydi), NOTLAR'a
    `Dondurulan: 2 embriyo, 5. gün, 2 tüp: (3AA) (3AA)` satırı ekleniyor.
    Satır `textwrap.fill(..., 68)` ile sarılı — kutu `white-space: pre`,
    uzun satır sarmaz, **sessizce kesilir** (v6.130'un kuralı). NOTLAR
    sırası: protokol → dondurma → çözme → iptal sebebi.
  - ART Lab'da FREEZE sütununun **dört kutusu** (satır 28-31) tüp tüp
    doluyor; dördü aşan tüpler **ikinci kâğıdın** aynı kutularında devam
    ediyor (v6.161, kullanıcının isteği; v6.160'a kadar son kutu "+3 tüp"
    diyordu). THAW ve TRANSFER de aynı. Oosit 13'ü geçmese de dördü aşan
    tüp ikinci kâğıdı açıyor (`artlab_dolgu()`'nun sayfa sayısı).
- **Çözülen örnekler de iki forma tek yerden** (v6.152, kullanıcının
  isteği: "FET çözme tedavilerinde formlara işlem geçmiyor").
  `formlar.cozulen_ornekler(cycle_id)` — her çözülen örnek: kodu
  (`specimen.id`), tüpü, tüpe konduğu andaki kalitesi (önceki dondurmanın
  tedavisinden, `bu_tedavinin_skoru()`), sağkalımı, canlılık oranı
  (`thaw_canlilik`), bu tedavide transfer mi yeniden dondurma mı.
  - Özet: ÇÖZDÜRÜLEN sayısı; VİABİLİTE `cozme_viabilitesi()` ("2 Canlı,
    1 Dejenere · %90-%85" — ortalama alınmıyor); NOTLAR'a dondurma
    satırından sonra "Çözülen: ..." ve "Kalan dondurulmuş: ..."
    (`_kalan_dondurulmus()`: bu tedavinin **son işleminin anındaki** tank,
    bugünkü değil — form aylar sonra basılsa da o günü söylesin).
  - **NOTLAR'da kod yok, embriyo bilgisi bir kez** (v6.159, kullanıcının
    isteği: "Yazı kod yazmasın. Tüp içinde embriyo bilgisi parantez ile
    belirtilsin. Embriyo bilgisi tek sefer yazılsın"). "Çözülen: 2
    embriyo, 1 tüp: (8HG1-7HG2); 2 transfer" — örnek kodu yok, ne olduğu
    sayıyla. "Kalan dondurulmuş" tüpleri etiketle değil içindekiyle yazıyor,
    bu tedavide dondurulanları tekrar etmiyor ("bu tedavide dondurulan 1
    tüp"), çözülen embriyonun dondurması programda yoksa (aktarılmış FET)
    **hiç yazılmıyor** — "yok" demek yanlış olurdu. Access'ten aktarılan
    tedavide notun kendi dondurma cümlesi ile aynı tüpler "Dondurulan:"
    satırına girmiyor (`dondurma_tupleri()`'nin `aktarim` bayrağı,
    `db.KAYNAK_DONDURMA_NOTU`: aktarımın dondurma olayına yazdığı not).
    ART Lab'ın kutuları değişmedi.
  - ART Lab: THAW ve TRANSFER da FREEZE gibi dört kutu (`_ARTLAB_DORT_KUTU`).
    THAW tüp tüp parantez (`tup_metni()`), TRANSFER'in "Uterus grade (x
    sayı)"sı "3AA x2 · %90-%85" (`_transfer_satirlari()`).
  - Izgaranın "Transfer" satırındaki **F = Freeze** (o embriyo transfer
    edilmedi, donduruldu), ✓ = transfer. Kullanıcı sordu, anlamı ekranda
    yazmıyor.
- **"Formda görünmüyor" derse önce `teshis_form.py`** (v6.153). Bilinen
  iki sebep: program `git pull`'dan sonra yeniden başlatılmamış (tuzak #5)
  ya da çözme FET'e değil kaynak ICSI'ye yazılmış — v6.155'e kadar çözme
  ekranının "hangi tedavi için" seçimi embriyonun kaynak tedavisine
  düşüyordu (bugün düşmüyor, eski kayıtları `cozme_ayir.py` ayırır). Araç
  ikisini de ve
  "bu tedavide transfer edilmiş ama çözmesi başka tedaviye yazılmış"
  embriyoyu gösteriyor; hasta adı basmıyor.
- **Taşma/küçülme kararı sayfanın verisine bağlı** (v6.152):
  `formlar.tasan_hucreleri(ad, deger)` / `sigdir_hucreleri(ad, deger)`,
  app ikisini de sayfa sayfa çağırıyor. FREEZE yanındaki THAW boşsa taşar,
  doluysa küçülür; THAW hep küçülür (sağı TRANSFER); TRANSFER taşar
  (sağındaki Deselect grade programda yok). Yeni bir dolu komşu eklersen
  bu iki işlevi güncelle, sabit kümeye güvenme.
- **Yazdırırken form tek A4'e sığdırılıyor** (v6.152, `form.html`
  `baskiyaSigdir()`). Kâğıdın NOTLAR kutusu iki satır boyunda; 3 satırı
  aşan not satırları uzatıp formu **ikinci sayfaya** taşıyordu (ölçüldü:
  4 satırda 2 sayfa — Access'ten gelen protokol notları zaten aşıyordu).
  `beforeprint`'te `.kalipkap` kalıbın kendi boyuna (`data-yukseklik`)
  `zoom` ile küçülüyor, `afterprint`'te geri. Kesme yok, Excel'in "sayfaya
  sığdır"ının aynısı. Test ederken Playwright `pdf()` `beforeprint`'i
  kendisi atmıyor — olayı elle gönder.
- **Sayıyı forma basmadan önce `_sayi()`'den geçir** (v6.136). Yüzde/hacim
  kolonları SQLite'ta REAL; 85 değeri "85.0" diye geliyordu ve ART Lab'ın
  "% Motil" kutusuna (32px) "%  85.0" (40px) sığmayıp **sessizce
  kesiliyordu**. `_sayi()` tam sayıda ondalığı düşürüyor ("85"), gerçekten
  kesirli değeri koruyor ("0.8") -- yuvarlama yok, resmî forma yanlış sayı
  yazmak boş bırakmaktan kötü. Yeni bir sayısal form alanı eklersen ham
  kolonu değil bu fonksiyonu kullan.
- **Sığmayan yazıyı kesme, sağa taşır** (v6.135, kullanıcının kararı:
  "Thaw ve onun[ki] alana kadar satırı uzatabilirsin"). `.kalip td`
  varsayılan olarak `overflow: hidden` — ART Lab'ın dar FREEZE kutusunda
  "(4HG2-4HG2-3HG2)" **sessizce kesiliyordu**. `form_kalip.satirlar()`'ın
  `tasan` parametresi (koordinat kümesi) o hücrelere `.tasabilir`
  (`overflow: visible`) veriyor, yazı sağdaki boş kutulara akıyor —
  **Excel'in kendi davranışı da bu**, o yüzden Excel tarafında bir şey
  yapmak gerekmedi. `tasan` `deger`/`ek` gibi **doldurma tarafından**
  geliyor, kalıp değişmiyor. Yeni bir dar kutuya uzun bir değer yazarsan
  önce ölç (`scrollWidth > clientWidth`), sonra taşıt.
- **Kenardaki kutuda taşırma olmaz, küçült** (v6.150, kullanıcının
  isteği). Özet'in EŞİNİN ADI kutusu formun sağ kenarında: 19 harflik bir
  ad 3px taşıp son harfi kesiliyordu, `.tasabilir` yazıyı kâğıdın dışına
  çıkarırdı. Kimlik kutuları (`formlar.sigdir_hucreleri(ad)`: Özet'in
  SOYADI/ADI/EŞİNİN ADI, ART Lab'ın Adı/Eşinin adı) `.sigdir` alıyor:
  `form.html`'in `adlariSigdir()`'i puntoyu kutuya sığana kadar düşürüyor
  (en çok yarısına, ~40 harf), `beforeprint`/`afterprint`'te yeniden
  ölçüyor (çıktıda kutu daha geniş). Excel'de aynı hücreler stilin bir
  **kopyasıyla** `shrinkToFit` alıyor (`form_kalip.yerlesim(sigdir=)`,
  `excel._kalip_xf`) — kalıbın stil listesi önbellekte paylaşılıyor,
  kendisine ekleme. Karar sırası: sağında boş kutu varsa taşır, yoksa
  küçült, **asla kesme** — kimlik bilgisi kesik basılmaz.
- **ART Lab'ın "Yorum"u iki ayrı yer** — karıştırma. Izgaranın en alt
  satırı **oosit başına** ve çok dar (blastokist skoru orada, v6.37);
  kâğıdın altındaki "Raporu dolduran … Yorum:" satırı ise sayfa
  genişliğinde tek hücre. **Yumurta bulguları alttakine** yazılıyor
  (v6.135, kullanıcıya soruldu, o seçti): ızgaraya konduğunda
  "3AA, Vakuol, Geniş PVS" kutudan 52px taşıyordu. Bulgular oosit
  numarasıyla (`1: Vakuol, Geniş PVS · 3: Kalın zona`), basılı yazının
  arkasına `ek` ile ekleniyor. Bulgu iki aşamada da girilebildiği için
  (ICSI / denüdasyon, v6.96) aşama süzülmüyor, tekrar eden bulgu bir kez
  yazılıyor.
- **`formlar.py`'deki bir hücre koordinatı kalıptaki gerçek satırla eşleşmeyebilir
  — kalıba değil, o sabite bak.** `_OZET_NOTLAR = (70, 2)` NOTLAR kutusunu hiç
  bulamıyordu (v6.102'de bulundu): kalıpta satır 70 (0'dan sayarak) boş,
  "NOTLAR" etiketi ve değer kutusu gerçekte satır 71'de. Yani **protokol notu
  hiçbir zaman basılmamıştı**, kimse fark etmemişti çünkü kutu sessizce boş
  kalıyordu (hatasız, sayfa yine düzgün görünüyordu). Düzeltme `(71, 2)`,
  yalnızca Python sabiti — kalıba dokunulmadı. `OZET_KUTULARI`/`ARTLAB_IZGARA`
  gibi listelerde yeni bir satır numarası kullanırsan `form_kalip.json`'daki
  gerçek `satirlar[N]` içeriğiyle karşılaştır (`python3 -c "import json;
  print(json.load(open('form_kalip.json'))['ozet']['satirlar'][N])"` gibi),
  yorum satırındaki kâğıt numarasına güvenme.

**Çözme notu Embriyoloji Özet'in NOTLAR kutusuna eklenir** (v6.102,
kullanıcının isteği). `thaw.html`'deki tek, paylaşılan `thaw_notu` alanı
(taşıyıcıdaki tüm örnekler için aynı değer, `thaw_kontrol_zamani` ile aynı
desen) `olay.thaw_notu`'na yazılıyor. `formlar.ozet_verisi()` bu cycle'a ait
(`COALESCE(thaw_cycle_id, specimen.cycle_id) = cycle_id`) bir çözme notu
bulursa, protokol notunun **altına** ekliyor (`"\n".join`, üzerine yazmıyor)
— kutunun kendisi zaten `white-space: pre` (`.kalip td`), newline satır
atlıyor, ek bir CSS gerekmedi. Cycle tipinden bağımsız: `ivf_icsi`/
`oosit_cryo`'nun kendi thaw'ında not yazılırsa o da aynı şekilde eklenir,
ayrı bir `fet_tipi_mi()` süzgeci yok — sorgu zaten yalnızca **bu cycle'a
ait** çözmeleri buluyor.

**Laboratuvar kendi formunu yükleyebilir** (v6.40, `goc_029`). Gömülü iki form
bu laboratuvarın; başka bir laboratuvar `/formlar`'dan kendi `.xlsx` formunu
yükleyip programdaki verilerle doldurup basıyor.
- **Yalnızca `.xlsx` kabul edilir.** `.xls` okumak `xlrd` isterdi; o
  `formlar_asil/` altındaki **geliştirme aracının** bağımlılığı, programın
  değil. `.xlsx` içinde XML olan bir ZIP — `zipfile` + `xml.etree` yetiyor.
  Bu kuralı gevşetip çalışma anına kütüphane sokma.
  Yükleme kutusunun altında `.xls`'i çevirmenin beş adımı yazılı
  (`form_xls_*`, açılır); kütüphane eklemek yerine yönerge yazıldı.
- **Izgarayı kuran kural tek yerde**: `form_kalip.izgara_kur()`. Hem
  `kalip_uret.py` (kâğıt aslından) hem `xlsx_oku.py` (yüklenen dosyadan) onu
  çağırıyor — iki kopya olsaydı yüklenen form ile gömülü form farklı basılırdı.
- **Doldurma etiketle**: kutunun içine `{{dosya_no}}` yazılıyor. Etiketlerin
  listesi `formlar.ALAN_ACIKLAMA`'da, **tek yerde**; hem doldurma hem
  `/formlar/etiketler` ekranı oradan okuyor. Yeni alan eklersen oraya ekle.
- **Tanınmayan etiket olduğu gibi basılır** — yazım hatası gözden kaçmasın
  diye; yükleme listesi de ayrıca uyarıyor. Boş basma.
- **Kalıp veritabanında** (`lab_formu.kalip`, JSON metin), logosu da içinde
  base64. `lab.db` USB ile taşınan tek dosya; kalıp diskte ayrı dursaydı
  taşınırken unutulurdu. Aynı sebeple `/disari/tumu` dökümüne **girmiyor** —
  `TUM_TABLOLAR`'a `lab_formu` ekleme: klinik kayıt değil ve tek Excel
  hücresine sığmaz (sınır 32767 karakter).
- **Yükleme/gizleme/silme yalnızca yönetici** (`yonetici_kontrol`); **basmak
  serbest**, gömülü formlarla aynı. Rotalar `kaldir`/`gizle` diye adlandırıldı:
  `sil` adı "silme" modülüne düşerdi.
- **Dışarıdan gelen dosya.** Boyut/parça/satır/sütun/görsel sınırları
  `xlsx_oku.py`'de; XML'de `<!DOCTYPE`/`<!ENTITY` varsa dosya hiç açılmıyor.
  Bu korumaları kaldırma.
- Bu sürümde **oosit ızgarası yok** (kullanıcının kararı): bir kutu = bir
  değer. Izgara desteği eklenirse etiket yazımı ve ekran birlikte düşünülmeli.

**Gömülü formlar gizlenebilir, ticari sürümde hiç olmayacak** (v6.41).
Gömülü iki form **bu** laboratuvarın kurum belgesi: doküman kodu, revizyon
tarihi ve üniversite ambleminin sahibi o. Başka bir laboratuvarda ekranda
durmaları yanlış — yanlışlıkla basılırsa ortaya ait olmadığı kurumun
belgesinde gerçek hasta verisi çıkar.
- `/formlar`'da Gizle/Göster var; ayar `ayarlar` tablosunda
  (`form_gizli_<ad>`), **varsayılanı görünür** — bu labda bir şey değişmiyor.
- Adres parçası `FORMLAR` **beyaz listesinden** geçiyor: ayar anahtarını
  adresten gelen metinle kurma, `ayarlar`'a istenen satır yazılırdı.
- Gizli form adresten hâlâ basılıyor; gizleme ekran düzeni, yetki sınırı
  değil (yüklenen formlarda da öyle). Yetki `yonetici_kontrol()`'de.
- **Ticari dağıtımda gömülü form olmayacak** (kullanıcının kararı,
  2026-09-12): `form_kalip.json` + `static/form_amblem.png` silinir, her lab
  kendi formunu yükler. O gün **kod değişmemeli** — bugün hazırlandı:
  `form_kalip.py` dosya yoksa `KALIPLAR = {}` ile devam ediyor, `FORMLAR`
  yalnızca kalıbı olanlardan kuruluyor, `gomulu_formlar()` boş dönüyor.
  Bu toleransı kaldırma, `form_kalip.json`'ın varlığına güvenen kod yazma.

**Zaman çizelgesi türetilmiştir, kayıt değil** (v6.37). `formlar.zaman_cizelgesi()`
cycle'ın aşama saatlerini toplayıp iki süre veriyor: önceki işlemden ve
OPU'dan bu yana. Kullanıcının isteği — formdaki "24 saat / 40-45 saat /
72 saat" satırlarını varsayımla eşlemek yerine program gerçek saati hesaplasın.
- **Ayrı tablo yok.** Saatler zaten aşama ekranlarında elle giriliyor; ikinci
  bir yere yazmak veriyi ikiye ayırırdı.
- **Sıra zamana göre**, klinik akış sırasına göre değil: aynı gün önce
  transfer edip sonra dondurmak olağan, akış sırası eksi saat gösterirdi.
- Zamanı girilmemiş aşama çizelgede yok.
- **Saatler işlemin yapıldığı tedaviden** (v6.146, `db.tedavide_yapilan()`).
  FET'in çizelgesinde kendi çözme/transferi/yeniden dondurması var. Kaynak
  ICSI'ninkinde FET'in işleri yok; ICSI'nin resmî formundaki İŞLEM saatleri
  de öyle.
- **`.cizelge` dört-beş sütun + `nowrap` hücreler (tarih/saat gibi geniş
  değerler) yüzünden tek `.sutun`un genişliğinde kolayca taşıyor** — taşan
  kısım kartın dışında **sessizce kesik** kalıyordu (v6.113, kullanıcı
  ekran görüntüsüyle bildirdi: "tablo kesik, tam görünmüyor"). Tablonun
  kendisi hâlâ `nowrap` (README v6.37, sayılar okunaklı kalsın diye
  bilinçli) — sütunları daraltmak çözüm değil.
  - **`/istatistik`'in iki `.cizelge` tablosu**: sarmalayıcı
    `<div class="cizelgekap">` (CSS'te `overflow-x: auto`) hâlâ duruyor —
    `form.html`'in `.kalipolcek`'inin (v6.107) aynı deseni, tabloya değil
    onu saran `<div>`'e uygulanıyor (`<table>`'ın kendisinde `overflow-x`
    güvenilir çalışmıyor). Yeni bir çok-sütunlu `.cizelge` tablosu
    eklersen aynı sarmalayıcıyı kullan.
  - **Cycle ekranının zaman çizelgesi farklı — kaydırma DEĞİL, genişletme
    + küçültme.** v6.114'te kullanıcının isteği "yatay kaydırma yerine
    sadece zaman çizelgesini uzat, başka hiçbir yeri uzatma — ne işlemi
    bitir butonunu ne de embriyoloji özet formu butonunu" idi.
    `cycle_detay.html`'de bu kart `.sutunlar`'ın **dışında**, iki sütunun
    ikisini birden kapsayan tam genişlikte duruyor (`.kap.genis`'in kendi
    `--genis-sutun` genişliği, ~940px'e kadar) — `İşlemi bitir`/
    `Embriyoloji Özet Formu` gibi düğmeler hâlâ kendi `.sutun`larının
    içinde, genişlikleri değişmedi. **Ama bu genişletme yalnızca gerçek
    iki-sütunlu (geniş masaüstü, `--genis-sutun` ≳ 800px) görünümde ek
    genişlik veriyor**: `.sutunlar` iki 380px'lik sütunu + 16px boşluğu
    (776px) sığdıramadığı her genişlikte (dar telefon dahil, iki sütun
    zaten tek sütuna dizilmiş oluyor) kart sığdığı tek sütunla **aynı
    genişlikte** kalıyor.
    v6.114'te bu durumda kaydırma da kaldırılmış olduğu için (v6.113'ün
    `.cizelgekap`'ı geri alınmıştı) taşma hiç kırpılmıyor, **sayfanın
    kendisi** yatay kaydırılabilir hale geliyordu — v6.117'de kullanıcı
    tam bunu bildirdi: "mobilde tam gözükmüyor, kaydırmalı görünüyor —
    ilk bakışta görünsün, ekranı kaydırarak değil". **v6.117'nin çözümü**:
    `<table class="cizelge">` artık `<div class="cizelgeolcek">` içinde;
    `form.html`'in `.kalipolcek`/`formlariSigdir()` deseninin (v6.107,
    v6.109) birebir aynısı — `cizelgeSigdir()` betiği tabloyu kırpmak/
    kaydırmak yerine BÜTÜN olarak `transform: scale()` ile mevcut
    genişliğe küçültüyor (`transform-origin: top left` burada da v6.109'un
    dersiyle şart). Geniş ekranda oran zaten ~1 (v6.114'ün kazancı
    korunuyor), dar telefonda tablo görsel olarak küçülüp **her zaman**
    tam sığıyor — sayfa hiçbir genişlikte yatay kaymıyor. Bu, v6.114'ün
    "gerçekten dar bir telefonda dördüncü sütun kesik görünebilir" bilinen
    sınırını kapatıyor. Yeni bir yerde aynı "sabit-doğal-genişlikte içerik
    hiçbir kaydırmaya/kesilmeye izin vermeden bir kaba sığmalı" ihtiyacı
    doğarsa (form.html'in kâğıt kalıbı, buradaki zaman çizelgesi) bu
    `transform: scale()` + `transform-origin: top left` deseni üçüncü
    yerde de geçerli — kaydırma çözüm değilse ilk seçenek bu olsun.

**`gun_alt()` / `son_alt()` `formlar.py`'de durur**, `disari.py` oradan alır.
Örnek başına alt sorgu kuran iki küçük parça; iki kopya birbirinden ayrı
düşerdi.

**İstatistikler türetilmiştir, sayaç yoktur** (v6.38). `/istatistik` her
açılışta sayıları `hasta`, `cycle`, `specimen` ve `olay`'dan hesaplıyor.
**Sayaç tutma** — aynı bilgiyi iki yere yazmak olur ve ikisi er geç ayrı
düşer; cryo haritasının türetilmiş olmasıyla aynı gerekçe. Kullanıcı "anlık
kaydedilebilir mi" diye sordu, cevap "kaydetmeye gerek yok, zaten kayıtlı".
- **Yalnızca yönetici**: hem `/istatistik` hem `/disari/istatistik`
  `yonetici_kontrol(request)` ile başlıyor. Ekran bütün üretimi ve son
  girilen hasta adlarını tek sayfada gösteriyor.
- **Paydası sıfır olan oran basılmaz** — "%0" ölçülmemişi ölçülmüş gösterir.
- **"Kayıtlı oosit" yalnızca yumurta TOPLANAN tedavilerden sayılır**
  (v6.130): `db.FET_TIPLERI` dışındaki cycle'lar. FET'teki bir örnek
  çözülmüş bir embriyo/yumurtadır, toplanmış oosit değil — M2 oranının
  paydasına girerse oran olduğundan düşük çıkar (ölçüldü: 105/%63.8,
  doğrusu 94/%71.3). Program normal akışta FET'e specimen yazmıyor, ama
  `aktar_access.py` yazıyor (aşağıya bak).
- Transfer ve gebelik **tedavinin yapıldığı cycle'a** yazılır
  (`COALESCE(o.tr_cycle_id, s.cycle_id)`), ay listesindeki kuralın aynısı.
- **"Son kayıtlar" haftalık ve sayfalı** (v6.124, kullanıcının isteği:
  "son kayıtları sayfada çok gösterme haftalık tut ... beş sayfada göster
  ki çok uzun liste olmasın"). Pencere `SON_KAYIT_GUN` = 7 gün, sayfa boyu
  `SON_KAYIT_SAYFA_BOYU` = 5, en çok `SON_KAYIT_EN_COK_SAYFA` = 5 sayfa
  → 25 kayıt. Kayıt defteri değil, **"bu hafta ne yapıldı"** penceresi;
  tam döküm hâlâ `/disari/tumu`'da.
  - **Sayfa boyu 5, çünkü ana ekranın üç kartı da `liste[:5]`** (v6.78).
    Aynı programda "kısa liste" ölçüsü iki farklı sayı olmasın.
  - **Tavanı aşan kayıt gizlenmiyor, sayısı yazılıyor** — kart
    "Son 7 gün · en yeni 25 kayıt" basıyor. Sessizce kesmek "bu hafta 25
    iş yapıldı" der gibi görünürdü.
  - **Haftalık süzgeç `localtime` KULLANMAZ**: `olusturma_zamani` hiçbir
    yerde elle yazılmıyor, şemanın `DEFAULT (datetime('now'))` değerine
    düşüyor ve o **UTC**. Süzgeç de `datetime('now','-7 days')`. Klinik
    tarih alanlarının deseniyle (`date(bitis_zamani) =
    date('now','localtime')`, v6.29) karıştırma — orada karşılaştırılan
    şey personelin elle girdiği yerel zaman, burada veritabanının kendi
    damgası. Yeni bir `olusturma_zamani` süzgeci yazarsan `localtime`
    ekleme.
  - **Kart ay seçicisinden bağımsız ama sayfa bağlantıları `yil`/`ay`'ı
    taşır** — yoksa son kayıtlarda sayfa çevirmek seçili ayı bugüne
    sıfırlardı (`/hastalar`'ın `sayfa`/`aysayfa` ikilisindeki sorunun
    aynısı). Aynı adreste iki bağımsız sayfa sayacı varsa her biri
    ötekinin durumunu taşımak zorunda.
  - `son_kayitlar()` **sözlük** döndürüyor (`satirlar`, `sayfa`,
    `sayfa_toplam`, `toplam`, `gun`, `sinirli`), liste değil. Havuz için
    tablo başına 25 çekiliyor: birleşik listenin ilk 25'i her tablonun
    kendi ilk 25'inin içinde, ayrı bir `COUNT(*)` gerekmiyor.
- **Ay/yıl seçilebilir** (v6.123, kullanıcının isteği: "aylık olarak
  oranlar tutulsun ... yıl ve tarih seçerek bakabileyim"). "Tutulsun"
  burada da ayrı bir aylık özet tablosu **değil**: `istatistikler(ay)`
  zaten aya süzebiliyordu, eksik olan ekrandaki karşılığıydı. Seçici
  `/hastalar`'ın `.aygezgin`'inin birebir kopyası — aynı işi yapan iki
  ekran aynı görünsün diye; yeni bir seçici deseni yazma.
  - **Dört oranın tanımı v6.38'den beri aynı**, yeniden yazılmadı:
    `oran_mii` = MII / kayıtlı oosit (specimen sayısı — OPU'da elle
    girilen "toplanan" sayısı **değil**, v6.112'nin ayrımı burada da
    geçerli), `oran_fert` = 2PN / ICSI, `oran_blast` = blastokist / 2PN,
    `oran_gebelik` = klinik gebelik / transfer edilen tedavi.
  - **Ay kırılımı oranı kendi hesaplamıyor**, her ay için
    `istatistikler(ay)` çağırıp ondan alıyor — ekranın üstündeki kart ile
    altındaki tablo iki ayrı formül kullansaydı biri düzeltilip öteki
    unutulurdu. Sayaç tutmama gerekçesinin formül hali. Yeni bir yerde
    aynı oranı göstereceksen sen de `istatistikler()`'den al.
  - **"Genel toplam" ve "Son kayıtlar" seçiciden etkilenmez**, bilerek:
    ikisi de laboratuvarın tamamı. `istatistikler(ay)` ay verildiğinde
    `hasta`/`hasta_aktif`'i `None` döndürüyor — hasta kaydı bir aya ait
    değil. Aya bağlı yeni bir sayı eklersen bu ayrımı hatırla.
  - **Kaydı olmayan ay tabloya girmez**; oranı `None` (ekranda `—`).
    Boş bir ayda "%0 blastokist" yazmak "ölçüldü, sıfır çıktı" demek
    olurdu — "paydası sıfır olan oran basılmaz" kuralının aylık hali.
  - **Adresten gelen `?yil=`/`?ay=` `_istatistik_donemi()`'nden geçer**:
    iki tamsayıya sabitlenir (SQL'e giden `ay_str` oradan kuruluyor,
    tuzak #9) ve yıl `EN_ESKI_YIL` .. bu yıl + `EN_YENI_YIL_PAYI`
    aralığına sıkıştırılır — `_yil_araligi()` seçili yılı listeye zorla
    eklediği için `?yil=99999` seçiciye doksan bin satır koyardı.
  - **`.cizelge`nin `nowrap`i SAYILAR için, etiket sütunu sarabilir.**
    Oran tablosu dört sütunla `.sutun`u aşınca taşan "Tüm zamanlar"
    sütunu kartın dışında kaldı: ekran görüntüsünde başlık "Tüm zam"
    diye kesikti, hücrelerde yalnızca "%" görünüyordu — `.cizelgekap`
    teknik olarak kaydırılabilir yapmıştı ama kimse karşılaştırmak için
    tabloyu kaydırmaz. Çözüm `.cizelge.oran td.ad { white-space: normal }`
    (yalnızca o tabloya). v6.109'un dersi bir kez daha: dış kabın ölçüsü
    doğru çıkabilir, içeriğin göründüğü yere ayrıca bak — bir ekran
    görüntüsü geometrinin kaçırdığını yakalar.

**Örnek kodu aranabilir** (v6.35). Kod (`527078-2026-0001-03`) tüpün ve
formun üstünde yazan şey; `<hasta dosya no>-<specimen.id>` olarak
birleştirilip aranıyor, yani tam kod da kuyruğu da (`0001-03`) buluyor.
İki yerde: `/hastalar` (sonuç kartı hasta satırlarının üstünde, satır
**cycle'a** gider) ve `/cryo?ara=`. İki kural:
- Arama **yalnızca tire içeren** metinde örnek arar — tiresiz metin kod
  değildir, yoksa "3" yazan bütün örnekleri listeler.
- Örnek araması **hastanın arşivlenmiş olmasına bakmaz**; dolaptaki bir
  örneğin dosyası kapanmış olabilir. (Hasta araması eskisi gibi süzer.)

**Taşıyıcı etiketi de aranabilir** (v6.138, kullanıcının isteği:
"Vitrifikasyonda etiket kodu ile arama olsun. Ana sayfadaki aramada o da
aranabilsin"). Sorgu tek yerde: `app.etiket_ara(ara)` — `ornek_kodu_ara()`'nın
taşıyıcı hali. Satır da tek yerde: `templates/_etiketsonuc.html`'in
`sonuc()` makrosu. İki ekran çağırıyor: vitrifikasyon (`?ara=`, ekranın en
üstünde) ve `/hastalar` (ana ekranın arama kutusu oraya gönderiyor; örnek
kodu kartının altında, hasta satırlarının üstünde). Üçüncü bir yerde aynı
soruyu soracaksan bu ikisini çağır, yeni sorgu/satır yazma.
- **`durum` süzülmez** — boşaltılmış ve kullanılmış taşıyıcı da bulunur.
  `/cryo` `durum='dolu'` süzüyor çünkü o bir **envanter** ekranı; bu hedefli
  bir **arama**, "bu etiket kimin". Durum rozetle söyleniyor ve `bosaltildi`
  ile `kullanildi` **ayrı yazıyor** (v6.86: kullanılan tüp boşalmadı).
- **Tire kapısı YOK** (örnek kodunda var). Örnek kodu birleştirilmiş bir
  değer, etiket ise gerçek bir kolon — "1400" yazan gerçekten onu arıyor.
  `/cryo`'nun etiket araması da kapısız. Sınır `LIMIT 50`.
- **Embriyo ve sperm taşıyıcılarını birlikte kapsar**; hasta iki ayrı
  bağıntılı alt sorgudan geliyor (`_ETIKET_HASTA`) — JOIN çok örnekli
  taşıyıcı satırını çoğaltırdı. Satırın gideceği yer (`yol`) **sunucuda**
  kuruluyor, şablon kategoriye göre adres kurmuyor.
- **`tr_buyuk()` uygulanmaz** — `etiket` büyük harfe sabitlenmiş bir alan
  değil (v6.116'nın kuralı).
- **Vitrifikasyondaki kutu dondurma formunun İÇİNDE değil**: içinde olsaydı
  arama kutusunda Enter'a basmak vitrifikasyonu kaydederdi. Bir ekrana yeni
  bir arama kutusu koyarken hep sor — o ekranda zaten bir POST formu var mı?

**Hasta kayıtları ay ay + Tüm Hastalar, birlikte** (v6.29, v6.63'te
genişledi). `/hastalar` **iki sütun**: solda o ayın cycle'ları (satır cycle
başına), sağda **Tüm Hastalar** — arama boşken aktif hastaların tamamı
alfabetik, doluyken arama sonucu. **v6.63'e kadar arama ay görünümünün
YERİNE geçiyordu** (iki ayrı mod, hiç birlikte görünmezlerdi); kullanıcının
isteğiyle (2026-09-16, "hasta kayıtları ve takvim aynı şey gibi"
gözleminin yanıtı) artık **ikisi aynı anda** ekranda. Yeni bir davranış
eklersen bu ayrımın kaldırıldığını unutma — `ara` artık `liste`'yi
etkilemiyor.
- **Ayın ölçüsü OPU tarihi**, yoksa cycle'ın açıldığı tarih (FET'te OPU
  olmuyor). Kullanıcının kararı: soru "kim kayıtlı" değil, "bu ay kaç vaka
  yaptık". Bunu hasta kaydının tarihine çevirme.
- Arşivlenmiş hastanın cycle'ı **ay listesinde görünür** (o iş o ay yapıldı),
  yapılacaklarda görünmez. Satırda "Arşiv" rozeti var.
- Satırın sağındaki **"Hasta kartı"** düğmesi (v6.63'te "Hasta kaydı"ndan
  yeniden adlandırıldı — sayfanın adı zaten "hasta kaydı", düğmede aynı
  kelime neyin nereye gittiğini belirsizleştiriyordu) hastanın tüm geçmişine
  gider, satırın kendisi o ayki cycle'a (v6.31). İç içe `<a>` olamayacağı
  için ikisi kardeş, `.satirikili` yan yana diziyor — satıra bir bağlantı
  daha eklersen aynı yolu izle. Metin anahtarı hâlâ `hasta_kaydi` — yalnızca
  görünen metin değişti, anahtarı değiştirme.
- **Tüm Hastalar** (`durum='aktif'`, `ORDER BY ad_soyad`) aynı satır
  tasarımını kullanıyor, isme tıklamak `/hasta/{id}`'yi (aynı ekran) açıyor.
- **İki liste de sayfalanır** (Tüm Hastalar v6.87'de, ay listesi v6.88'de
  aynı gerekçeyle — kullanıcının isteği: "Tüm Hastalar yanındaki aylık
  tedavilerin olduğu yerde aynı şekilde olsun"), ikisi de `HASTALAR_
  SAYFA_BOYU` (50) kadar, birbirinden **bağımsız** sayfa numarasıyla: Tüm
  Hastalar `?sayfa=`, ay listesi `?aysayfa=`. Hasta/tedavi sayısı bini
  geçince telefonun tek seferde binlerce satır basması yavaşlığa yol
  açardı. İkisi de sunucuda kendi `[1, toplam_sayfa]` aralığına
  sabitleniyor, aralık dışı bir değer hataya değil son sayfaya düşer.
  Sayfa gezginleri `.aygezgin`'in (ay/yıl seçicisiyle aynı) kutusunu
  yeniden kullanıyor, ortada seçici yerine düz "Sayfa 3 / 42" metni
  (`.sayfabilgi`). **Arama sonucu sayfalanmıyor** — zaten süzülmüş küçük
  bir liste; arama doluyken Tüm Hastalar sorgusu hiç çalışmıyor bile
  (gereksiz sorgu atılmasın diye, arşiv modundaki gerekçenin aynısı). Ay
  listesi araması etkilemiyor zaten (`ara` ay görünümünü değiştirmiyor).
  `cycle_listesi()`'ye bu yüzden `limit`/`offset`/`sayisi` eklendi —
  **yalnızca `ay` çağıranı** (`/hastalar`) bunları veriyor, ötekiler
  (ana ekran, `/bitenler`, `/yaklasanlar`) vermediği için davranışları
  değişmedi. Yeni bir `cycle_listesi()` kipini de sayfalamak istersen aynı
  üç parametreyi kullan, ayrı bir sorgu yazma.
- **Ay ile arama birbirini silmiyor**: `aygezgin` formu gizli `ara` alanı,
  arama formu gizli `yil`/`ay` alanları taşıyor. Biri değişirken öteki
  sıfırlanmasın diye.
- **Arşiv hâlâ ayrı, tam genişlik bir mod** — iki sütuna girmiyor: "bu
  dosya kapandı" demek, günlük ay/Tüm Hastalar akışının parçası değil.
- `/hastalar` artık **iki sütun** kategorisinde (aşağıdaki "İki sütun her
  ekranın çözümü değil" listesine bak) — ay listesi ile Tüm Hastalar
  birbirinden bağımsız iki kart, `_cyclesatir` satırlarını bölmüyor.
- Ay adları `metinler.py`'de (`ay_1`…`ay_12`), ekrana `ay_adi(yil, ay)`
  basıyor. `strftime("%B")` **kullanma** — işletim sisteminin yerel ayarına
  bağlı, Windows mini PC'de İngilizce çıkar.
- Yıl ve ay **açılır seçici**, yanlarında `‹ ›` okları (v6.30). Yıl aralığı
  veriden geliyor (`_yil_araligi`) ve `>= 2000` süzgeci **şart**: bozuk
  `0026-09-04` tarihi seçiciye iki bin satır koyardı.

**Bütün cycle listeleri tek fonksiyon, tek satır makrosu** (v6.29–v6.33).
Yapılacaklar, bugün bitenler, `/bitenler` arşivi, ay listesi, "Yaklaşanlar"
ve takvim: sorgu `cycle_listesi()` (`bitmis` / `bugun` / `ay` / `yaklasan` /
`plan_ay`), satır `_cyclesatir.html` `satir(s, kip)` (`yapilacak` / `bitmis` /
`ay` / `plan` / `plangun`). Yeni bir liste ekranı yazarsan ayrı bir sorgu
yazma, buraya bir kip ekle — hepsi aynı görünsün diye böyle.

**Geri oku gerçekten bir önceki ekrana gider** (v6.126, kullanıcının
bildirdiği sorun: "bir önceki menüye geçmesi gerekirken farklı menülere
geçiyor"). `base.html`'in sonundaki küçük betik geri okuna tıklamayı
yakalayıp `history.back()` çalıştırıyor — **tek yerde**, 55 şablonun
okuna tek tek dokunmak tuzak #1'in tarifiydi.
- **Şablonlardaki `{% block geri %}` adresi KALDIRILMADI** ve kaldırma:
  o hâlâ ekranın "bir üst seviyesi" ve JS kapalıyken, doğrudan adresle/
  yer iminden girildiğinde, karekoddan ya da ana ekran simgesinden
  açıldığında tek davranış o. Yeni ekranda yine yaz.
- **Betiğin karışmadığı dört durum, hepsi bilerek**: (1) referrer yok ya
  da başka bir site — `history.back()` kullanıcıyı programın dışına
  atardı; (2) gelinen sayfanın **yolu aynı**, yalnızca sorgusu farklı
  (`?oosit=`, `?duzenle=`, `?gun=`, `?asama=`) — bu bir önceki ekran
  değil, aynı ekranın başka hali; ICSI'nin "kaydet → sıradaki oosit"
  akışında (v6.35) geri ok tedavi ekranına dönmeli, oositleri tek tek
  geri yürümemeli; (3) sayfaya **yönlendirmeyle** gelinmiş
  (`performance`'ın `redirectCount`'u > 0) — bu programda neredeyse her
  zaman POST → 303, yani az önce kaydedilen form, ona dönmemeli;
  (4) ekranda geri oku yok. Bu dördünü gevşetme.
- **`?geri=<yol>` hâlâ yasak** — adresten gelen metin `href`'e yazılırsa
  `javascript:` sokulabilir. Referrer burada yalnızca **karar vermek**
  için okunuyor (aynı köken mi, aynı yol mu), hiçbir yere yazılmıyor.
- **Yedek adresi yanlış olan iki ekran düzeltildi**: `/cryo` ve
  `/yonetim` ana menü öğesi (`_gezinme.html` + `ana.html`), `/hastalar`'ın
  altında değiller — `/hastalar` → `/`. Yeni bir ekranın adresini
  yazarken "bu ekran hangi menünün altında" diye sor; "buraya kaç yoldan
  geliniyor" sorusunu artık betik yanıtlıyor.
- Betik `{% block tazeleme %}`'nin **dışında** — o blok yazdırma
  ekranlarında (`form.html`, `/baglan`) boşaltılıyor, içine konsaydı
  oralarda geri ok çalışmazdı.

**Üst çubukta iki dönüş var, ikisi farklı şey.** Geri oku (`‹`) **bir
önceki** ekrana gider ve şablon başına ayrı yazılır; ev simgesi (`.anaya`)
**ana menüye** gider ve `base.html`'de tek yerde durur, 42 şablonun hepsine
oradan iner (v6.27). Yeni ekran yazarken ev simgesini eklemene gerek yok,
kendiliğinden gelir — `{% block geri %}`'yi doldurman yeter. Ana ekranda ve
giriş yapılmamış ekranlarda basılmaz; koşul `(kullanici or
request.state.kullanici)` çünkü middleware `request.state`'i açık yollarda
(`/sifre`) doldurmuyor.

**Ana menü artık `base.html`'de global, cycle ekranları hariç her ekranda
solda** (v6.65, kullanıcının isteği — önceden yalnızca `/` çağırıyordu).
`{% block yanmenu %}` `.ust` bandının hemen altında, varsayılanı
`gz.yan_ana(_yk, _aktif_menu)`. **Cycle ekranları** (OPU, androloji,
denüdasyon, ICSI, fert, cleavage, blast, vitrifikasyon, çözme, transfer,
gebelik, `cycle_detay`) bu bloğu **boş bırakıyor**
(`{% block yanmenu %}{% endblock %}`) — onlar zaten kendi aşama menülerini
(`gez.cubuk`/`gez.yan`) gösteriyor, ikisi üst üste binmesin diye. **Yeni bir
cycle ekranı yazarsan bu boş override'ı eklemeyi unutma** — unutursan iki
`.yanmenu` aynı `position:fixed` konumunda çakışır.

Geniş ekranda `.yanmenu` (aşama menüsüyle aynı görünüm), telefonda
`.anadugmeler` düğme yığını (**yalnızca ana ekranda**, `ana.html`) — CSS
1100px'te birini gizleyip ötekini gösteriyor. Ana menüye madde eklersen
**ikisine birden ekle ve aynı yazıyı kullan** — aynı düğmeyi iki isimle
öğretmek personeli yanıltır. Sıra: Hasta kayıtları → Cryo haritası →
Yönetici, altında ayrı grupta işlemler (Yeni hasta, Şifre değiştir).
Menüdeki izin kontrolü yalnızca bağlantıyı gizler; asıl engel middleware ve
`yonetici_kontrol()`.

**Menü artık her yerde olduğu için genişleyen ekranlar `yanmenusuz` değil
`genis` kullanmalı** (`.kap.genis.yanmenusuz` → `.kap.genis`, `--genis-sutun`
menü payını içeriyor). Yeni bir genişleyen (`kap genis`) ekran yazarsan
`yanmenusuz` ekleme — o artık yalnızca gerçekten menüsüz kalan bir ekran
için (bugün öyle bir ekran yok, sınıf CSS'te duruyor ama kullanılmıyor).

**Takvim kaldırıldı** (v6.65). `/takvim` rotası ve `takvim.html` silindi;
sebep, hasta kayıtları ekranıyla "aynı şey gibi" görünmesiydi (v6.63'ün ilk
denemesi bunu çözmeye çalışmıştı, kullanıcı sonunda ekranı tamamen
kaldırmayı seçti). Ana ekrandaki **"Yaklaşanlar" kartı kalıyor** — yalnızca
artık gitmediği "Tümü" bağlantısı kaldırıldı. `cycle_listesi(plan_ay=...)`
kod yolu bilerek dokunulmadan bırakıldı (çağıran yok, ama `yaklasan` moduyla
iç içe geçmiş, ayıklaması riskli) — yeni bir kullanım yazmadan önce hâlâ
çalıştığını doğrula. `takvim_basligi()` **kalıyor**, `/takvim`'e özel
değildi — `cycle_detay.html` planlanan tarihi göstermek için kullanıyor.

**Kayıt açıp sonra doldurma varsa, dolduramazsan açtığını geri al.**
Denüdasyonda `specimen_olustur()` önce, `goruntu_bagla()` sonra çalışıyor;
ikincisi başarısızsa **oosit geri alınmalı**, yoksa oosit sayısı şişer — o
klinik bir sayı (v6.19). Geri alma `goruntuler.bos_specimen_sil()` ile:
yalnızca hiç görüntüsü ve olayı olmayan oosit silinir. Başarısızlık **sessiz
olmasın**, sebebini ekrana yaz.

**Tarihin yılı 1900'den küçükse kaydedilmez** (v6.51). `datetime-local`
alanına yıl olarak "26" yazılınca tarayıcı `0026-09-04` gönderiyor; değer
geçerli bir ISO tarihi olduğu için hiçbir katman itiraz etmiyor ve kayıt
sessizce yanlış duruyor (bir cycle'ın OPU tarihi aylarca böyleydi). Kontrol
`yil_kontrol()`'de, `zaman()` onu çağırıyor — yeni bir tarih alanı yazarsan
`bos_ise_none` değil **`zaman(v, "Alan adı")`** kullan.
- **Sınır 2000 değil 1900** — doğum tarihleri 1900'lerde olabilir.
- Hata dönüşü formu kapatmaz: yazılan değerlerle yeniden basılır (v6.21).
- `islem_zamani()` ayrı: aşama POST'unda hata gösterecek yer olmadığı için
  bozuk yıl **şu ana** düşer, fonksiyonun belgelenmiş davranışı.
- Şablonlarda `min="1900-01-01"` var ama asıl engel sunucuda; tarayıcıya
  güvenme.
- **Üst sınır da var** (v6.53): `bu yıl + 5`. `9999-01-01` de `0026-09-04`
  kadar sessiz bir hata. Şablonlarda `max` **yok** — her yıl değişen bir değer
  şablona sabit yazılamaz; üst sınırı sunucu tutuyor.
- Bulunmuş bozuk kayıtları **`tarih_duzelt.py`** sorarak düzeltir; hiçbir
  şeyi kendiliğinden değiştirmez, doğum tarihlerine öneri yapmaz. `teshis.py`
  de bozuk tarih varsa söyler.
- Araç **"bozuk olanı tanımıyor, makul olanı geçiriyor"** (v6.53): değeri
  tarihe çevirmeye çalışıp üç şey bildiriyor — yılı çok eski, çok ileri, hiç
  okunamıyor. v6.51 yalnızca dört haneli küçük yılı arıyordu ve
  `20026-09-02`, `04.09.2026`, `88-01-05` elinden kaçıyordu. Denetimi
  daraltma.
- **`goc_kaydi` taranmaz** (`ATLA_TABLO`). `goc.py` zaten uygulanmış göç için
  bilerek `"onceden"` yazıyor — tarih değil, işaret; ayrıca o tabloyu
  düzenlemek göçün yeniden çalışmasına ya da atlanmasına yol açar.

**`style.css` sürüm numarasıyla bağlanır** (v6.69). `base.html`'deki bağlantı
`/static/style.css?v={{ statik_surum() }}` — `statik_surum()` dosyanın
`st_mtime`'ını döndürüyor. Gerçekten başa geldi: kullanıcı doğru commit'i
çalıştırıyordu ama tarayıcı `style.css`'i eski haliyle önbellekten okumaya
devam ediyordu (HTML güncel, CSS değil — `view-source` ile HTML'de yeni
sınıf görünüyordu, `/static/style.css`'i doğrudan açınca görünmüyordu).
Adres sabit kaldığı sürece tarayıcının yeniden indirmesi için sebep yok;
kullanıcıdan her güncellemede "sert yenile" hatırlamasını istemek kırılgan.
**Yeni bir statik dosya (ikinci bir `.css`/`.js`) eklersen aynı deseni kullan**
— sabit adresle bağlama, tuzak listesine eklenecek kadar ucuz bir hata.

**Tasarım koyu tema, tek tema** (v6.71'de sistem tercihine bağlı bir deneme
olarak başladı, v6.72'de kullanıcının kararıyla kalıcı ve tek tema oldu —
gerekçe README v6.71–72). Açık tema artık **yok**; `:root`'taki renkler
doğrudan koyu değerler, ayrıca bir `@media (prefers-color-scheme)` bloğu da
yok.
- **Bütün tasarım CSS değişkenleri üzerinden kurulu** (`--ink`, `--yuzey`,
  `--vurgu`, ...) — yeni bir bileşen yazarken renk sabit yazma, hep bu
  değişkenleri kullan. Sabit yazılan her renk koyu temada iki türlü patlar:
  ya kendisi yanlış görünür ya da bir komşu değişkenle (`var(--ink)` gibi)
  eşleşmesi gereken bir varsayımı sessizce kırar.
- **`--ink` metin rengi, `--ust-bg` kasa rengi — ikisini karıştırma.** Üst
  bant, kimlik bandı, aktif sekme gibi öğeler hep koyu kalması gereken
  "kasa" — onlar `var(--ust-bg)` kullanıyor. `--ink` **metin** için: koyu
  temada açık renk. Yeni bir "hep koyu duracak" öge yazarsan `--ink` değil
  `--ust-bg` kullan, yoksa metin rengiyle aynı değişkeni paylaşınca öge
  temayla birlikte (yanlışlıkla) rengini değiştirir.
- **Zemin sabit bir renkse (`background: #fff` gibi, `.tazelekutu a` veya
  `.kagit` — resmî form kâğıdı bilerek beyaz kalıyor), üzerindeki yazı rengi
  de sabit olmalı, `var(--ink)` OLMAMALI.** v6.72'de tam bunun tersi
  bulundu: `.tazelekutu a` zemini sabit beyazdı ama yazısı `var(--ink)`
  kullanıyordu — koyu tema gelince yazı da açık renge dönüp beyaz zemin
  üzerinde okunmaz oldu. Yeni bir bileşen yazarken zemin sabitse yazı da
  sabit olsun.
- **Amblem (üst banttaki halka + dört nokta) PNG değil, satır içi SVG**
  (`base.html`, `.ust` içinde) — dört nokta `fill="var(--vurgu)"` kullanıyor,
  ayrı bir dosya üretmeye gerek yok. `simge_uret.py`'nin çizdiği favicon/PWA
  ikonları (`static/ikon_*.png`) PNG olduğu için tema değişemiyor — onlar
  koyu zeminle sabitlendi, tasarım değişirse ikisini birlikte güncelle.
- **Resmî form ekranı (`/form/...`) dışarıda** — kâğıt aslı hep beyaz
  basılacak, `.kagit` sınıfı sabit `#fff`/`#000` kullanıyor, koyu temadan
  etkilenmiyor. Yeni bir yazdırma ekranı yazarsan aynı şekilde sabit tut.
- **Arka planda köşe görseli var** (v6.75, kullanıcının isteği):
  `static/desen.svg` (sağ üst) + `desen2.svg` (aynısının 180° çevrilmişi,
  sol alt) — amblemle aynı motif ailesi (dört hücreli embriyo, zona
  pellucida halkası, bölünen/tek hücreler), `body`'de iki `background`
  katmanı olarak `vw` tabanlı boyutla bağlı. Kartlar opak olduğu için
  metnin önüne geçmiyor. **SVG yorumlarında `--` (çift tire) kullanma** —
  XML'de geçersiz, tarayıcı dosyayı hiç render etmiyor (sessizce boş arka
  plan kalıyordu, v6.75'te böyle bulundu). `@media print`'teki
  `body { background: #fff }` bunu da temizliyor, yazdırma etkilenmiyor.
- **`--ink-2` / `--ink-3` yalnızca METİN için güvenli, zemin/kenarlık için
  değil** (v6.74). İkisi de koyu temada açık renk (ikincil/üçüncül metin).
  `.rozet` (İptal/Arşiv/Tamamlandı etiketi) zemini `var(--ink-2)`
  kullanıyordu — v6.72'de bu satır atlandı çünkü tarama yalnızca eskiden
  sabit-hex-yazılmış renkleri arıyordu, *anlamı temayla tersine dönen* bir
  değişken kullanımını yakalamadı. Sonuç: beyaz yazı artık açık gri zemine
  biniyordu, neredeyse okunmuyordu (kullanıcı "bazı yazılar okunmuyor" dedi).
  Zemin/kenarlık olarak `--ink-2`/`--ink-3` kullanan yeni bir satır yazma —
  gerekiyorsa sabit bir koyu ton seç (`.rozet` `#3d4f63` kullanıyor).
- **`html { color-scheme: dark; }` şart** (v6.74). Tarayıcının kendi çizdiği
  kontroller (`<select>` açılır listesi, tarih/saat seçici, kaydırma çubuğu)
  CSS'ten değil, sayfanın `color-scheme`'inden renk alıyor. `prefers-color-
  scheme` ile otomatikken (v6.71) tarayıcı zaten biliyordu; v6.72'de tek
  temaya geçilince bu satır unutulmuş, tarayıcı hâlâ "açık" sanıp `<select>`
  listesini kendi açık renkleriyle çiziyordu — bizim CSS'imiz yalnızca
  kapalı kutuya koyu-tema yazı rengi vermişti, bazı tarayıcılarda liste
  okunmuyordu. Bu satırı kaldırma.
- **Kart başlıkları (`.kart h2`) büyük, kalın ve kendi rengi `--baslik`**
  (v6.82: 13px + `var(--ink-2)` → 16px + `font-weight:700`; v6.83: rengi de
  `var(--ink)`'ten `var(--baslik)`'e — kullanıcı "başka bir renk, ama
  okunabilir" istedi). **Tek kural, uygulamadaki her `<div class="kart">
  <h2>` bundan besleniyor**, ayrı ayrı büyütmeye/renklendirmeye gerek yok.
  `.bilgikart h2` (aşama ekranlarının salt okunur kartı) kendi küçük
  override'ını taşıyordu, kaldırıldı — `.bilgikart` her zaman `.kart` ile
  birlikte kullanıldığı için (`class="kart bilgikart"`) yeni değerleri
  miras alıyor.
  - **`--baslik` (#e76491) `--vurgu`'nun (#e0356f) AÇIK tonu, aynısı değil.**
    Düz `--vurgu` kart zemini `--yuzey` üzerinde yalnızca ~3.75:1 kontrast
    veriyor — WCAG'in normal metin için istediği 4.5:1'in altında.
    `--vurgu`'nun HSL açıklığını (~54%→65%) yükseltip hue/doygunluğu
    (~340°/73%) koruyarak `--baslik` (~5:1 kontrast) türetildi — hem
    markanın pembesiyle aynı aile hem WCAG AA'yı geçiyor. **Yeni bir vurgu
    rengi gerekiyorsa böyle türet** (hue sabit, açıklığı `--yuzey`/`--zemin`
    kontrastına göre ayarla), rastgele bir hex yazma.
  - Yeni bir kart başlığı için ayrı font-size/color yazma, bu paylaşılan
    kuralı boz olarak bırak; yalnızca gerçekten farklı bir vurgu gerekiyorsa
    (`.snapkart h2`'nin düz `var(--vurgu)` rengi gibi — kendi bilinçli
    vurgusu, dokunulmadı) küçük bir override ekle.

**Ekran kendini tazeler** (v6.54). Klinikte birkaç telefon aynı anda kayıt
giriyor; masaüstünde açık duran sayfa elle yenilenene kadar eski kalıyordu.
Veri hep anında kaydoluyordu — eski olan sayfaydı. `base.html`'deki
`{% block tazeleme %}` beş saniyede bir `/degisim`'e soruyor.
- **Yazdığın asla silinmez.** Sayfa "kirli" ise (bir alanın değeri
  varsayılanından farklı ya da imleç bir alanın içinde) **kendiliğinden
  yenilenmiyor**; altta şerit çıkıyor, karar kullanıcının. Bu korumayı
  kaldırma — form doldururken yenilemek, çözdüğü sorundan pahalı bir hata.
- Şerit **altta** durur: üstteki kimlik bandını kapatmamalı.
- **Damga `veri_damgasi()`'nde**: her tablo için `COUNT(*)` + `MAX(rowid)`
  (+ `DEGISIM_EK` ile `olay.iptal_mi` toplamı, çünkü iptal yerinde yazılıyor
  ve günlüğe düşmüyor). `DEGISIM_ATLA` bir **dışlama** listesi — yeni tablo
  kendiliğinden kapsanır. `oturum` dışarıda: her istekte yazıldığı için
  sinyal sayılsa sayfa kendi sorusu yüzünden sonsuz yenilenirdi.
- **Yerinde düzenleme günlük sayesinde yakalanıyor**: `degisiklikleri_yaz`
  satır yazıyor, o satır damgayı değiştiriyor. Günlüğe yazmayan bir düzenleme
  yolu yazarsan o değişiklik öteki ekranda görünmez.
- **`PRAGMA data_version` ve dosya damgası denendi, ikisi de olmaz** —
  birincisi bağlantı başına, ikincisi oturum yazısını da sinyal sayıyor
  (README v6.54).
- **Yazdırma ekranları dışarıda**: `form.html` ve `/baglan`
  `{% block tazeleme %}{% endblock %}` yazıyor. Yeni bir yazdırma ekranında
  aynısını yap — Ctrl+P açıkken sayfa altından değişirse çıktı bozulur.
- **Yoklama oturumu tazelemez** (`dokun=False`). Olmasa ekranı açık
  bırakılmış telefon hiç düşmez, 12 saatlik sınır işlevsiz kalırdı.
  `son_erisim` de artık her istekte değil, bir dakikadan eskiyse yazılıyor.

**Aynı kaydı iki kişi düzenlerse uyarı çıkar** (v6.55). Klinikte birkaç
telefon aynı anda kayıt giriyor; ikinci kaydeden birincinin yazdığını siliyor.
- **Birim "alan" değil KAYIT.** Kaydederken formun **tamamı** yazılıyor
  (`UPDATE olay SET <bütün alanlar>`), yalnızca dokunduğun alan değil — yani
  farklı alanları düzenlemek de çarpışma. Alan bazında uyarmak **yanlış
  güven** verirdi; bu birimi daraltma.
- **Uyarı engellemez.** Katı kilit klinikte yanlış: pili biten telefon kaydı
  kilitli bırakır, acele eden personeli engellemek çarpışmadan pahalı.
  Program haber verir, kararı kullanıcı verir. Bunu kilide çevirme.
- **Bellekte tutulur, `lab.db`'de değil** (`_duzenleyenler` + `threading.Lock`).
  İki sebep: o anki sunucu çalışmasına ait, klinik kayıt değil; ve `lab.db`
  USB ile taşınıyor, bayat "düzenleniyor" satırları da onunla giderdi. Bunu
  tabloya taşıma. **Sunucu tek süreç** çalışıyor (`baslat.py`) — birden çok
  işçiyle çalıştırılırsa sözlük paylaşılmaz ve uyarı çalışmaz.
- **Kimlik sekme başına**, kullanıcı başına değil: aynı kişinin telefonu ve
  masaüstü de gerçek bir çarpışma.
- **`GET /degisim` hiçbir şey yazmaz**, haber ayrı bir `POST /duzenliyorum`
  ile gelir ve yalnızca gerçekten düzenleyen gönderir. Sadece izleyen ekran
  ne veritabanına ne belleğe dokunur — bu ayrımı bozma.
- **Anahtarı şablon söyler**: `{% block kayitanahtari %}`. Adresten türetme —
  aşama ekranı adressiz açıldığında ilk örneği seçiyor (v6.35), o yüzden
  `/cycle/1/icsi` ile `?oosit=1` aynı kaydı farklı anahtarla gösterir ve uyarı
  kaçar. Anahtar sunucuda `ANAHTAR_KALIBI`'ndan geçer (tuzak #9); ekrana
  yalnızca veritabanındaki `kisa_kod` basılır.
- **Kapsam dışı: vitrifikasyon, çözme, transfer** — tek ekranda birden çok
  örneğin kartı var, ekran bazında anahtar farklı embriyolarda çalışan iki
  kişiyi de uyarırdı. Yanlış alarm uyarıya olan güveni bitirir.
- **Uyarı kaybı engellemiyor**: iki kişi yine de kaydederse ikincisi üzerine
  yazar. Asıl güvenlik ağı (forma gömülü imza + kaydederken reddetme)
  kullanıcıya sorulacak, README v6.55 sonu.

**İşlem saatleri elle girilebilir.** Her aşamada varsayılan "şu an", ama
değiştirilebilir — personel işlemi yaparken değil sonra kaydediyor olabilir.
Bu özelliği asla kaldırma.

**Boş alan NULL kaydedilir**, boş metin değil. "Girilmedi" ile "sıfır/yok"
ayırt edilebilsin diye.

**Hasta ve eş adı her zaman büyük harfle kaydedilir** (v6.115, kullanıcının
isteği: "nasıl yazarsam yazayım sonunda büyük harflerle kaydolsun").
`app.py` `tr_buyuk()` — `hasta_kaydet()`, `hasta_guncelle()` ve
`sperm_dondurma_yeni_hasta_kaydet()` (üçü de `hasta.ad_soyad`/`es_adi`
yazan tek yerler) yazmadan önce çağırıyor.
- **`str.upper()` tek başına yeterli değil — "Turkish I problem".**
  Python'un varsayılan Unicode kuralı küçük 'i'yi noktasız 'I' yapar,
  Türkçe kuralı noktalı 'İ' ister ("ışık" → yanlışlıkla "ISIK" değil
  "IŞIK" olmalı, ama "iyi" → "IYI" değil "İYİ" olmalı). `tr_buyuk()` önce
  'i'yi 'İ'ye çevirip SONRA `.upper()` çağırıyor — 'ı' zaten doğru
  çevriliyor (Unicode'da 'ı'.upper() == 'I'), ç/ğ/ö/ş/ü'de hiç sorun yok.
  Hasta/eş adı için yeni bir yazma yolu açarsan (ya da başka bir kişi adı
  alanı eklersen) `str.upper()` değil bu fonksiyonu kullan.
- **Hata dönüşünde büyütülmüş değil, kullanıcının yazdığı gösterilir**
  (v6.21 kuralı) — form doğrulaması patlarsa (`FormHatasi`) şablona
  ham `ad_soyad`/`es_adi` geçiyor, `tr_buyuk()` yalnızca gerçek yazma
  anında (INSERT/UPDATE'ten hemen önce) çağrılıyor.
- **`goc_040`** daha önce girilmiş kayıtları aynı kurala getirdi (tek
  seferlik, idempotent) — `tr_buyuk()`'ün birebir kopyası göçün içinde,
  göç betikleri `app.py`'yi import etmiyor (diğer göçlerin deseni).
  Kullanıcı adı (`kullanici.ad_soyad`, personel) bu kuralın **dışında** —
  yalnızca hasta/eş isimleri için, personel isimleri kendi yazdığı gibi
  kalıyor.
- **`h.ad_soyad LIKE` arayan her sorgu arama terimini de `tr_buyuk()`'ten
  geçirmek ZORUNDA** (v6.116, kullanıcı bildirdi: "küçük harf ile arama
  yaparsam hasta çıkmıyor"). `ad_soyad` her zaman büyük harfle kayıtlı
  olduğu için sorgu `h.ad_soyad LIKE '%terim%'` şeklinde kalıyor ama SQLite'ın
  `LIKE`'ı büyük/küçük harf eşitlemeyi **yalnızca ASCII'de** yapıyor
  (`'ali' LIKE '%ALI%'` eşleşir) — Türkçe ı/İ/ş/Ş/ğ/Ğ/ö/Ö/ü/Ü/ç/Ç'de
  yapmıyor (`'ışık' LIKE '%IŞIK%'` **eşleşmez**, farklı Unicode karakterler).
  v6.115 hasta adlarını büyük harfe sabitleyince bu susmuş bir hata haline
  geldi: Türkçe harf içeren hemen her isim için küçük harfle arama sıfır
  sonuç veriyordu. Düzeltme dört yerde (`/hastalar`, `/cycle/{id}/androloji/
  sperm-baglama`, `/cryo`'nun embriyo VE sperm dondurma aramaları) aynı:
  `ad_soyad` karşılaştıran `?` parametresine `f"%{tr_buyuk(ara)}%"`,
  **diğer** alanlara (dosya no, `t.etiket`, `k.tam_yol`, örnek kodu) hâlâ
  ham `ara` — onlar büyük harfe sabitlenmiş değil, `tr_buyuk()` onlara
  uygulanırsa küçük harfli bir etiket/yol araması bozulurdu. **Yeni bir
  `ad_soyad`/`es_adi` arama sorgusu yazarsan bu deseni kopyala** — yalnızca
  isim karşılaştıran parametreye `tr_buyuk()` uygula, aynı sorgudaki diğer
  `LIKE` parametrelerine dokunma.

**Silme = iptal işaretleme.** Normal akışta fiziksel silme yok. Kalıcı silme
ayrı, bilinçli bir yol: dosya no yaz → `SIL` yaz → tarayıcı onayı.
**Transfer kaydı olan hasta/cycle kalıcı silinemez** — ekranda seçenek
görünmez, sunucu da reddeder. Bu kuralı gevşetme.

**Yedekten geri yükleme, uygulamadaki en yıkıcı işlem — kalıcı silmeden
bile ağır** (v6.120, kullanıcının isteği: "Yönetici isterse yedekten geri
çağırsın... Yönetici panelinden hepsini yapabilsin"). Kalıcı silme tek bir
hastayı etkiliyor; geri yükleme **tüm** veritabanını seçilen yedeğin
alındığı andaki hâline döndürüyor, aradan girilmiş her şey kayboluyor.
`/yedekleme/geri-yukle` (v6.121'e kadar `/klasorler/geri-yukle`'ydi, bkz.
"Bekleyen işler" madde 2), `geri_yukle.py`.
- **Üç kademeli onay** — hasta kalıcı silmenin (dosya no + SIL) daha
  ağırı: (1) seçilen yedeğin dosya adını yazmak, (2) "GERİ YÜKLE" yazmak
  (iki dilde de **sabit, çevrilmeyen** aynı metin — sunucu kontrolü dilden
  bağımsız aynı stringi arıyor, ekrandaki yönerge de öyle söylemeli), (3)
  tarayıcının `confirm()`'ü. Yeni bir "tüm veritabanını etkileyen" işlem
  eklersen bu üçünü de koy, ikisi yetmez.
- **Değiştirmeden önce mevcut veritabanının güvenlik kopyası otomatik
  alınır** (`lab_ONCEKI_<tarih>.db`) — yanlış yedek seçilirse geri
  dönülebilsin. **`tasi.py`'nin kendi ONCEKI'sinden farklı olarak bu kopya
  `VERI_KOK`'a değil, seçilen yedeğin bulunduğu `yedek_klasor`'e yazılır**
  (`yedek_dosyasi.parent`) — geliştirme sırasında tam tersi yazılmıştı,
  test bunu yakaladı: `yedekleri_listele()` yalnızca `yedek_klasor`'ü
  taradığı için `VERI_KOK`'a yazılan bir ONCEKI hiçbir zaman geri yükleme
  listesinde görünmüyordu. `tasi.py`'ninki `VERI_KOK`'ta kalmaya devam
  ediyor — onun bağlamı "bu makinede hemen geri alınacak bir USB taşıma
  hatası", ayrı diske ihtiyacı yok. Yeni bir "değiştirmeden önce yedekle"
  akışı yazarsan bu kopyanın SONRADAN nereden bulunacağını/seçileceğini
  düşün, öyle karar ver.
- **Değiştirme mekaniği `tasi.py`'nin USB'den içeri alma deseninin
  birebir aynısı** — elle taklit edilmedi, aynı üç adım kopyalandı: SQLite
  backup API ile bir **geçici dosyaya** kopyala (`VERI_KOK`'ta —
  `Path.replace()`'in atomik kalması için hedefle aynı dosya sisteminde
  olmalı, `yedek_klasor` ayrı diskte olabileceği için oraya yazılamaz),
  eski `-wal`/`-shm` yardımcı dosyalarını sil (kalırsa yeni içerikle
  uyuşmayan sayfalar yeniden oynatılmaya çalışılır, README v6.16), sonra
  `Path.replace()` ile **atomik** takas — ya tam olur ya hiç olmaz.
  Düz dosya kopyası (`shutil.copy2`) burada da yasak (README v6.16'nın
  WAL gerekçesi).
- **Güvenlik: seçilen dosya adı whitelist'ten geçiyor.** Formdan gelen
  `dosya` alanını doğrudan `Path(hedef) / dosya`'ya eklemek yol aşımına
  (`../../lab.db`) açık olurdu (tuzak #9'un dosya-yolu hali). Sunucu önce
  `yedekleri_listele()`'nin döndürdüğü **gerçek** dosya adlarının kümesini
  kuruyor, `dosya` o kümede değilse reddediyor. Yeni bir "kullanıcının
  seçtiği dosya adını yola ekleyen" rota yazarsan aynı deseni kullan —
  yolun kendisini değil, önceden bilinen bir listeye karşı doğrula.
- **Arşivdeki fotoğraflar geri yüklenmiyor, bilinçli bir sınır.**
  `yedek.arsiv_yedekle()` hedeften hiçbir şey silmiyor (yalnızca birikimli
  kopyalıyor) — "şu yedeğin arşiv anlık görüntüsü" diye bir kavram yok.
  Risk yalnızca "eski DB, aradan silinmiş bir fotoğrafa işaret ediyor"
  (kırık bağlantı), veri kaybı değil — fotoğraf dosyaları kendi başına
  asla silinmiyor/üzerine yazılmıyor.
- **Geri yükleme sonrası oturumlar geçersiz olabilir** — eski bir yedeğe
  dönülünce o yedekten sonra açılmış `oturum` satırları artık yok, geri
  yükleyen yönetici dahil herkes bir sonraki istekte `/giris`'e düşebilir.
  Beklenen davranış, ayrı bir işlem gerektirmiyor.
- **Geri yükleme eski yedeğin eksik güncellemelerini hemen uygular**
  (v6.145, kullanıcının isteği: "Geri yüklemeden sonra da kendisi
  yapsın"). Program yeniden açılmadan: göçler, saklanmış şema cevaplarını
  unutma, Yönetici panelinin göç kartı ("Son geri yüklemede N güncelleme
  uygulandı"). Ekran mesajı ve `yedek.log` kaç güncelleme uygulandığını
  söylüyor. Bir göç patlarsa geri yükleme yine tamam: yedek yerinde,
  önceki hâlin kopyası duruyor, hata panelde. Terminaldeki
  `geri_yukle.py` de aynı işlevden geçiyor. Ayrıntı tuzak #15.

**İki yerden gelinen ekranın geri oku sabit olamaz.** Taşıyıcı ekranına hem
cryo haritasından hem çözme ekranından giriliyor; `?cycle=N` ile hangisinden
gelindiği söyleniyor ve geri adresi **sunucuda** kuruluyor (v6.32). Aynı
şey tek ekranın iki durumu için de geçerli: hasta kayıtlarında geri oku
arama/arşiv sonucundayken `/hastalar`'a, ay görünümündeyken `/`'a gider
(v6.34). Yeni bir ekranda `{% block geri %}` yazarken "buraya kaç yoldan
geliniyor" diye sor.
`?geri=<yol>` kalıbını yeni yerlerde kullanma — adresten gelen metin doğrudan
`href`'e yazılıyor, `javascript:` girilebilir. Sayı al, doğrula, yolu kendin
kur.

**Cryo haritası türetilmiştir.** `/cryo` ekranı vitrifikasyon ve çözme
kayıtlarından hesaplanır; elle güncellenen bir konum tablosu yok.

**Taşıyıcının içeriği "yumurta" mı "embriyo" mu — v6.167'den beri
İÇERİKTEN: `db.dondurulan_yumurta_sql(o)`** (v6.133'te kullanıcının isteği:
"Yumurta donduruluyorsa Yumurta, Embriyo donduruluyorsa Embriyo yazsın").
Dondurmadan önce enjekte edilmemiş, döllenmemiş ve değerlendirilmemiş örnek
yumurtadır; FET ve FET (3→5)'in dondurduğu hep embriyo; dondurmadan SONRAKİ
olaya bakılmıyor (Yumurta Çözme'de enjekte edilen yumurtanın ilk tüpü yine
yumurta). v6.166'ya kadar ölçü dondurmanın tedavisinin TİPİYDİ
(`db.yumurta_mi(tip)`): Access'ten aktarılan IVF/ICSI tedavisinde ICSI'ye
alınmayan yumurtalar da dondurulmuş, tipe bakan ölçü o tüplere "4 embriyo"
diyor, çözerken FET öneriyordu; bir Yumurta Dondurma'nın blastokist tüpüne de
"yumurta" diyordu. `db.py`'de çünkü `formlar.py` ve `aktar_access.py` de
soruyor (`FET_TIPLERI`'nin gerekçesi). Ekranda Jinja global
`icerik_sayisi(adet, icerik=t.icerik)` ("4 yumurta"/"4 embriyo") —
`say("n_embriyo", ...)` yazma, altı yerde aynı etiket var (cryo haritası
tank+taşıyıcı satırı, çözme ekranının iki listesi, taşıyıcı detayının üç
yeri) ve biri unutulursa ekranlar birbirini tutmaz.
- Taşıyıcının içeriğini `app.icerik_sql()` alt sorgusu veriyor (v6.166'ya
  kadar `icerik_tipi_sql()`, dört sorguda paylaşılıyor, taşıyıcı hepsinde
  `t`), sütun `icerik` = `'yumurta'`/`'embriyo'`; taşıyıcı sayfası ve çözme
  ekranı `tasiyici_icerigi()`'nin `icerik`'ine, çözme tipi seçimi
  `_tup_yumurta_mi()`'ye bakıyor. **İlk satır yeter**: bir taşıyıcı tek bir
  tedavinin tek türünü taşıyor. Sabit değil fonksiyon: `vit_cycle_id` eski bir
  yedekte yok, cevap her istekte soruluyor (tuzak #15).
- **Bir tüpün içeriğini soran yeni bir yer yazarsan `yumurta_mi(tip)`'e değil
  `dondurulan_yumurta_sql()`'e sor.** `yumurta_mi(tip)` "bu tipte dondurulan
  ne" sorusu için kalıyor: vitrifikasyon ekranının başlığı ve örnek adları
  (`ornek_adi()`), aktarımın notu okurken bağlamı. Bilinen sınır: IVF/ICSI
  tedavisinin vitrifikasyon ekranı aktarılmış dondurulmuş yumurtayı "Embriyo
  N" diye listeliyor (ızgaranın adı tedavinin tipinden) ve
  `transfer_adaylari()` yumurtayı tipe bakarak eliyor.
- Resmî formların "Dondurulan:" satırı tüp tüp içerikten
  (`formlar.dondurma_tupleri()`'nin `yumurta`'sı); ikisi birden varsa
  "Dondurulan: 1 embriyo, 5. gün, 1 tüp: (1CB); 16 yumurta, 3 tüp: (6) (5)
  (5)". "Kalan dondurulmuş" da (`_kalan_dondurulmus()`).
- **`yumurta_mi(tip, asama)`**: Yumurta Çözme'de aşamaya bağlı (v6.147) —
  çözülen yumurta, ICSI'den sonra dondurulan/transfer edilen embriyo.
  Aşama verilmezse soru "bu tedavide dondurulan ne".
- **Tank satırı ikisini ayrı sayıyor** — bir tankta ikisi birden olabilir,
  orada tek kelime seçilemez; sıfır olmayan basılıyor.
- `oosit_ad` metni v6.133'te dokunulmadan bırakılmıştı; v6.134'te
  kullanıcı "her yer" dedi ve o da "Yumurta" oldu (aşağıya bak).

**Ekranda "oosit" değil "yumurta" denir** (v6.134, kullanıcının isteği:
"oosit yazan her yeri Yumurta ile değiştir"). v6.79'un ("cycle" → "tedavi")
kuralının aynısı: **yalnızca kullanıcının gördüğü Türkçe metin** değişti —
`metinler.py`'nin `tr` değerleri, `app.py`'nin ekrana basılan etiketleri,
`disari.py`'nin Excel başlıkları, `formlar.ALAN_ACIKLAMA` açıklamaları,
`liste_degeri.etiket` (`goc_043`).
- **Kod tarafı aynen duruyor**: `specimen.durum='oosit'`, `opu_sag_oosit`/
  `opu_sol_oosit`, `?oosit=N` adres parametresi, `oosit_cryo` tedavi kodu,
  `metin()` **anahtarları** (`oosit_ad`, `oosit_n`, `henuz_oosit_yok_icsi`),
  Jinja değişkenleri (`oositler`), fonksiyon adları (`_oositleri_ac`).
  Yeni ekranda `metin("oosit_ad")`/`ornek_adi()` kullan — anahtarın adına
  bakıp "Oosit" basacağını sanma, o artık "Yumurta" döndürüyor.
- **Türkçe eki düz değiştirmeyle tutmaz**: "oosit" ünsüzle, "yumurta"
  ünlüyle bitiyor — "oosite"→"yumurtaya", "oositin"→"yumurtanın",
  "oositi"→"yumurtayı". Tuzak #1 burada dilin kendisinden de geliyor;
  `sed s/oosit/yumurta/g` yazma, metni tek tek oku.
- **Resmî formun kâğıt kalıbı dışarıda** — "OOSİT BİLGİLERİ", "TOPLANAN
  OOSİT" kalite sisteminin kendi yazısı ("kalıba dokunma", v6.37).
  Access'ten gelen serbest metin de öyle (laboratuvarın ağustos kaydının
  aslı), `degisiklik_log`'un silme özeti de (denetim izi, ekran değil).
- **Yüklenen form etiketlerinin adı değişirse eskisi de kabul edilmeli**:
  `{{toplanan_oosit}}`/`{{islenen_oosit}}` → `{{toplanan_yumurta}}`/
  `{{islenen_yumurta}}`, eskiler `formlar.ESKI_ALAN_ADI` üzerinden hâlâ
  çalışıyor (`ALAN_ADLARI` ikisini de içeriyor, `alanlar()` yeni adları
  sözlüğe ekliyor). Etiket hem ekran metni hem başka bir laboratuvarın
  çoktan yüklediği `.xlsx` ile sözleşme — sessizce kaldırırsan o form
  hata vermeden **boş** basar. `ozet_verisi()`'nin anahtarları ve hücre
  eşlemeleri (`OZET_KUTULARI`/`ARTLAB_IZGARA`) değişmedi.
- **`goc_044`** `aktar_access.py`'nin daha önce yazdığı protokol notlarını
  düzeltti. Not `textwrap.fill(..., 68)` ile sarılı ve "yumurta" iki
  karakter uzun — göç metin içinde değiştirme yapmıyor, üretilmiş
  **paragrafı baştan kuruyor**; düz değiştirme satırı 68'in üstüne
  çıkarır, NOTLAR kutusu `white-space: pre` olduğu için sessizce keserdi.
  Aynı nota yeni bir satır eklersen bu hesabı tekrar yap.

> **Eski cryo haritasını Excel'den içeri alma denendi ve GERİ ALINDI**
> (v6.127/v6.128 yazıldı, v6.129'da revert edildi). Kullanıcının kararı:
> "Cryo Harita istediğim gibi olmadı." Özellik hatalı olduğu için değil,
> **istenmediği için** kaldırıldı — kendiliğinden yeniden yazma. Yeniden
> gündeme gelirse önce git geçmişindeki v6.127/v6.128 bölümlerini oku
> (`3dfd58a`…`51efd53`): ölçülen sayılar ve üç somut tuzak orada.
> Kullanıcının veritabanında kalanları `eski_cryo_temizle.py` siliyor —
> kod geri alındı ama `eski_cryo` tablosu ve `konum` satırları kalıyor ve
> bağ kurulmuş bir hastanın kalıcı silinmesi FOREIGN KEY hatası veriyor.
>
> **Yeniden gündemde (kullanıcı, 2026-09-24):** "cryo haritamı excel olarak
> vericem. Bütün hasta kayıtlarını aktardıktan sonra onunla eşleştirme yapıp
> cryo haritalar bölümünü baştan yaratacağız." Sıra: önce bütün Access
> ayları, sonra Excel. Bu sefer eşleşecek şey yalnızca isim değil,
> **aktarılmış tüp**: hasta (dosya no, programda) + dondurma tarihi +
> içerik. Excel'de dosya no yoktu (v6.127). Başlamadan önce: v6.127/v6.128'i
> oku, kullanıcıya geçen sefer neyin istediği gibi olmadığını sor,
> `eski_cryo_temizle.py`'yi çalıştırıp çalıştırmadığını sor.

**Program öncesi kayıtlar `aktar_access.py` ile giriyor** (v6.130,
kullanıcının isteği). Ağustos 2026 tedavileri Access'te tutuluyordu;
betik Access'ten CSV'ye aktarılmış dosyayı okuyup `hasta`/`cycle`/
`specimen`/`olay`/`sperm_*`/`islem_yapan` yazıyor. **Programın parçası
değil, araç** — `.accdb` okunmuyor ("ek bağımlılık yok").
- **Eşleştirme yalnızca dosya numarasıyla**, isimle değil (v6.125'in
  kuralı). Var olan hastanın adı üzerine yazılmıyor, boş alanlar
  dolduruluyor.
- **İşaret protokol notunda**: `[Access kaydı #19]`. Aynı satır iki kez
  girmesin diye; betik yeniden çalıştırılabilir. Yeni bir içeri alma
  yazarsan aynı deseni kullan — ayrı bir "aktarıldı" tablosu açma.
  - **İkinci bir Access dosyası aktarılırken `kaynak=` ŞART** (v6.141).
    Her dosya kendi kayıtlarını 1'den numaralandırıyor: ağustosun #1..#20'si
    dururken temmuz dosyası etiketsiz aktarılsaydı temmuzun ilk 20 satırı
    "zaten aktarılmış" sanılıp **sessizce** atlanırdı.
    `python3 aktar_access.py kaynak=TEMMUZ temmuz.csv` → işaret
    `[Access kaydı TEMMUZ#5]`. **Ağustos etiketsiz kaldı, öyle kalmalı** —
    `KAYNAK` boşken işaret v6.130'daki haliyle basılıyor, etiket verilirse
    o satırlar yeniden aktarılır. Unutulursa betik duruyor: işaretin bulduğu
    tedavi **başka** hastanınsa (dosya no tutmuyorsa) bu yeniden çalıştırma
    değil çakışmadır, hiçbir şey yazmadan çıkıyor.
  - **İşaret kendi satırında durur, cümlenin sonunda değil** (v6.141).
    Not `textwrap.fill(..., 68)` ile sarılıyor ve cümleye eklenen işaret
    ortasından bölünüyordu (`[Access kaydı\nTEMMUZ#9]`) — `_zaten_var()`in
    `LIKE` deseni tutmuyor, yani aktarım idempotent olmaktan çıkıyor. 86
    satırın 60'ında oldu; ağustosta olmaması şanstı (işaret altı karakter
    kısa). `_zaten_var()` ayrıca satır sonlarını boşluğa katlıyor
    (`REPLACE(...char(10), ' ')`), zaten yazılmış bölünmüş işaretleri de
    buluyor. **Genel kural**: üretilmiş bir metnin içine gömdüğün, sonra
    makineyle arayacağın bir işareti sarma/biçimleme bozabilir — ayrı
    satıra koy, arayan sorguyu da boşluk farklarına dayanıklı yaz.
- **Toplam sayılar oosit oosit açılıyor** çünkü program sayıları
  `specimen`/`olay`'dan türetiyor ("istatistikler türetilmiştir"). Bu
  bilgi protokol notunda, yani ekranda ve resmî formda yazılı.
- **FET'in embriyoları FET'in kendi altına açılıyor** — kaynak (dondurma)
  tedavisi programda yok. `specimen.cycle_id`'nin "kendi cycle'ı" kuralının
  bilinçli istisnası; gerekçe README v6.130'da (ağustosun bütün
  transferleri FET, yoksa program "hiç transfer yok" derdi). Bunun tek yan
  etkisi istatistikteki oosit sayımıydı, o da düzeltildi (yukarı bak).
- **Serbest metinden klinik karar iki kademeli çıkarılıyor**: önce kaynak
  açıkça "iptal edildi"/"dondurularak saklandı" demeli, ancak ondan sonra
  hangi ayrıntılı sebep olduğuna bakılıyor; tanınmazsa genel "iptal"
  kalıyor. `liste` kipi yazmadan önce her satır için ne seçildiğini
  basıyor. Yeni bir metin kalıbı eklersen **ASCII yaz** — `_sade()` bütün
  Türkçe harfleri katlıyor (GUN, ASAMA, COZME).
- **Protokol notu kısa kalmalı**: resmî formun NOTLAR kutusuna basılıyor,
  kutu `white-space: pre` — uzun satır sarmıyor, kesiliyor. Satırlar 68
  karakterde sarılı. Nota yeni satır eklersen formu açıp bak (tuzak #5).
- **Dondurulan embriyonun skoru serbest nottan çözümlenip aşama ekranına
  yazılıyor** (v6.131, kullanıcının isteği: "4BB blastokist dondurulmuş
  yazıyor ise blastokist bölümüne fotoğrafsız 4BB embriyo kaydet").
  `3AA`→`bl_genisleme/icm/te`, `KAVG2`→`kavitasyon`+derece,
  `4HG2`→`cl_hucre_sayisi`+`cl_skor`. Yapılabilmesinin sebebi yazımın
  `app.blast_skor()`'un ürettiğiyle birebir aynı olması; tanınmayan parça
  atılmıyor, olayın notuna ham haliyle giriyor. `bl_skor_kaynagi='elle'`
  — skor bir insanın notu, otomatik hesap ezmemeli.
- **Dondurma taşıyıcısıyla birlikte yazılıyor** (v6.132 — v6.131 taşıyıcı
  açmıyordu, kullanıcı düzeltti: "Vitrifikasyon bölümünde etiket kodu
  üretiyor, onu kullansan"). Etiket `vit_ekran()`'in kendi önerisiyle aynı
  kalıpta: `<tedavi no>-<SSDD>`, aynı tedavide birden çok tüp varsa dakika
  ilerliyor. **Konum boş kalıyor** (kaynakta yok, ekran da boşa izin
  veriyor) — Cryo Haritası o tüpleri "konum girilmemiş" diye işaretliyor.
  Tüp dağılımı nottaki **parantez gruplarından**: bir grup = bir tüp,
  yazılı "N TÜPTE" olan üç satırın üçünde de tutuyor.
  - **Ders**: bir alanın "elle girilen gerçek ad" mı yoksa "programın
    ürettiği kod" mu olduğunu, o alanı kullanan ekranın **kendi
    varsayılanına** bakarak belirle. v6.131 bunu yapmadan "uydurulamaz"
    deyip kullanıcıya gereksiz iş çıkardı.
  - **Taşıyıcıya bağlı vitrifikasyon varsa dokunulmuyor**
    (`_vitrifikasyon_var()`): kullanıcı konumu elle girmiş olabilir.
- **Yumurta mı embriyo mu: önce tedavinin tipi, sonra not** (v6.142).
  `_dondurma_coz()` yalnızca nottaki "OOSİT"/"YUMURTA" kelimesine
  bakıyordu; bir temmuz notu kelimeyi atlamış ("2 TÜPTE 10 ADET (5*M2)
  (5*M2)"), araç embriyo sandı ve 10 yumurtayı **hiç yazmadı** — Cryo
  Haritası o iki tüpü göstermiyordu. Artık üç işaretten biri yeter:
  `db.yumurta_mi(tip)`, nottaki kelime, her öğenin `N*M2` yazımı.
  **Serbest metinden bir klinik kategori çıkaracaksan önce yapılandırılmış
  veriye sor** — `db.yumurta_mi()`'nin var olma sebebi tam bu soru.
- **FET'te çözme sonrası yeniden dondurma yazılıyor** (v6.143; v6.142'de
  yalnızca uyarıyordu, kullanıcı "programa ekleyelim" dedi). Hedef bu
  FET'te çözülüp transfer edilmeyen embriyolar, dondurmanın `vit_cycle_id`'si
  bu FET — programın kendi FET vitrifikasyon ekranının yazdığıyla aynı.
  Tarih transfer günü (kaynakta kültürün kaçıncı güne sürdüğü yok). **Araç
  göçü kendisi çalıştırmıyor**: goc_046 yoksa hiçbir şey yazmadan duruyor.
  Skor parantezi olmayan bir dondurma cümlesi de uyarıyor (v6.142'ye kadar
  sessizce dönülüyordu). **Kural: dondurulmuş bir örneği yazamıyorsan
  söyle** — tankta duran ama Cryo Haritası'nda görünmeyen bir tüp bu işin
  en sinsi kayıplarından.
- **Aktarılan tedavi tarih sırasına yerleşir** (v6.144): her satırın
  sonunda `db.tedavileri_sirala()`, rapor "hastanın N. tedavisi — tarih
  sırasına göre kayanlar: …" diyor. Araç goc_047 yoksa da duruyor. Aynı
  dosyanın satırları zaten tarih sırasıyla yazılıyor (`main()` sıralıyor);
  sorun ayrı dosyaların sırasıydı (ağustos önce, temmuz sonra).
- **"UYARI: notta N örnek ... M uygun kayıt var" iki ayrı sebebi taşıyor**:
  kaynağın kendi tutarsızlığı (2PN'den çok dondurulan embriyo) ya da
  aracın notu yanlış okuması. v6.141 ikisini karıştırıp aracın hatasını
  "kaynak tutmuyor" diye raporladı. Uyarıya sonuç bağlamadan önce notun
  kendisine bak.
- **`tamamla` kipi**: aktarılmış tedavileri baştan almadan günceller
  (`python3 aktar_access.py tamamla <dosya.csv>`). `_dondurma_kayitlari()`
  idempotent — var olan değerlendirmeyi `UPDATE` ediyor, ikinci satır
  açmıyor. Betiğe nottan okunan yeni bir alan eklersen aynı işlevin içine
  koy, yoksa daha önce aktarmış kullanıcı ona ulaşamaz.
  - **Aracın bir hatası düzeltildiyse onarım yolu budur** (v6.142'de
    #33'ün eksik tüpleri böyle eklendi) — ama **hemen** çalıştırılmalı:
    değerlendirme nottaki değerle güncelleniyor, yani kullanıcı aktarılan
    bir skoru ekranda elle düzelttiyse `tamamla` o düzeltmeyi ezer.
    Onarımı önermeden önce hatalı aktarımın kopyasında dene ve **her
    tabloyu satır satır** karşılaştır — v6.142'de yalnızca beklenen
    satırların değiştiği böyle gösterildi.
- **FET'in çözdüğü embriyo, tüpü programdaysa o tüpe bağlanıyor**
  (v6.148, `_kaynaga_bagla()`, kullanıcının kararı: "Bağla, belirsizi
  listele"). Embriyolar yine önce FET'in altında açılıyor (v6.130), sonra
  hastanın dolu tüpleri arasında tek bir eşleşme varsa bütün olayları o
  tüpün örneklerine taşınıyor, FET'in kendi örnekleri siliniyor, tüp
  boşaltılıyor — programın kendi çözmesiyle aynı veri. Eşleşme: toplam
  örnek = çözülen sayı, transferin yazımı kümedeki bir örnekle tutmalı
  (aynı evrede aynı skor; erken evredeki tüp kültürde ilerlemiş olabilir,
  ileri evredeki tutmaz), birebir tutan küme önce. **Farklı tedavilerin aynı
  skorlu tüpleri belirsiz sayılır** — soyağacını değiştirir; aynı tedavinin
  birebir aynı tüpleri fark etmez, ilki. Belirsiz ya da tutmayan
  bağlanmıyor, rapor kayıt numarasıyla söylüyor. Bu yüzden **dosyalar tarih
  sırasıyla aktarılmalı**: tüpün ayı önce.
- **`tamamla` her kuralın onarım yolu, ikinci çalıştırma hiçbir şeyi
  değiştirmez** (v6.148'de yedi dosyada satır satır denendi): dondurma →
  taze transfer → geçersiz canlılık → çözmeye yanlış yazılmış tüp →
  kaynağa bağlama → iptal sebebi (v6.150).
- **Dar onarım kipleri de var: `iptal`** (v6.150). `tamamla` dondurma
  değerlendirmesini nottaki değerle yeniden yazıyor — aylar önce aktarılmış
  bir tedavide elle düzeltilmiş skoru ezer. Yalnızca bir alanı onarman
  gerekiyorsa (iptal sebebi gibi) bütün `tamamla`'yı önerme; o adımı tek
  başına çalıştıran bir kip yaz. `iptal` yalnızca `bitis_sebebi` hâlâ
  genel `'iptal'` iken ayrıntılı sebebi yazıyor (kullanıcının ekrandan
  seçtiğine dokunmuyor), `degisiklik_log`'a düşüyor. Log satırı `b` ile
  yazılıyor: `guvenlik.degisiklikleri_yaz()` kendi bağlantısını açar,
  `yazma_islemi()`'nin kilidi içinde bekler. Öteki dar kipler:
  `transfer` (v6.154), `bagla` (v6.160: yalnızca kaynağa bağlama; v6.163'ten
  beri dosyasız, bütün veritabanı) ve `tip` (v6.167: ICSI'siz, yalnızca
  yumurta donduran IVF/ICSI tedavisini Yumurta Dondurma yapar; dosyasız).
- **Her aktarımın sonunda bütün aktarılmış FET'ler yeniden deneniyor**
  (v6.163, kullanıcının isteği: "her yeni aktarım yaptığımda eski
  kayıtlardan bağlantılı hasta varsa tedavileri bağla"):
  `butun_fetleri_bagla()`, CSV'siz — FET'in bilgisi veritabanından
  (`_vt_satiri()`: transfer notundaki "Embriyo: 3AA"), çözme tarihi
  sırasıyla (aynı tüpü isteyebilecek iki FET'ten önce çözen önce alır).
  Bağlanınca FET'in transfer günü değerlendirmesi kaynağın aynı tip+gün
  kaydıyla çakışıyorsa iptal (v6.154'ün kuralı, sonradan bağlanana da).
  v6.163'ün bilinen sınırı (FET o gün tek tutan tüpe bağlanıyor, sonradan
  gelen ikinci tüp bağı geri almıyor) **kullanıcının asıl durumuydu**: 2026
  aktarılmışken 2025 ay ay geliyor. v6.164'ten beri iki kural:
  - **Aktarılmamış ay varsa ertele**: tutan tüp ile çözme arasında en az 10
    tedavisi olmayan bir ay varsa bağlanmıyor, "ertelendi" (ay gelince her
    aktarımın sonunda kendiliğinden yeniden). Ölçü `db.tedavi_tarihi()`,
    olay günü DEĞİL (ekimin 5. gün dondurmaları kasıma düşer); eşik bir iki
    başıboş tedavinin boş bir ayı dolu göstermemesi için. "Tüpler tutmuyor"
    da arada boş ay varsa "elle bak" değil "ertelendi".
  - **Bağlı olanı yeniden sına, çözme**: `_baglantilari_yeniden_sina()`
    bağlı FET'lere bugünkü tüplerle bakıyor; başka tüp de tutuyorsa "Bağlı
    ama artık kesin değil" listesi. Bağ çözülmüyor (FET'in örnekleri silindi,
    konum elle girilmiş olabilir). Aday araması tek yerde,
    `_bag_siniflari()`: bağlama ile sınama aynı kural.
- **Etiket her dosyada tekil, yıllar arasında da** (v6.160): 2026'nın ayları
  `OCAK`…`TEMMUZ` ile aktarıldı, 2025'inkiler `OCAK2025`…, 2024'ünküler
  `OCAK2024`… (nisan–ağustos: `NISAN2024`, `MAYIS2024`, `HAZIRAN2024`,
  `TEMMUZ2024`, `AGUSTOS2024`; v6.168'de `EYLUL2024`…`ARALIK2024` ve
  `OCAK2023`). Aynı etiketi başka yılın dosyasına verme.
- **Dondurma notunun yazım hataları** (v6.168, `_skor_metni()`): "KACG1"
  kavitasyon (C, V'nin yanında; yalnızca arkasından derece geliyorsa),
  "KAVVİTASYON". Notta birden çok dondurma fiili varsa **parantezi olan ilk
  cümle** okunuyor ("... REFREEZE YAPILDI. ... 1 TÜPTE(4*M2) ... DONDURULARAK
  SAKLANDI"); "(%80 VİABİLİTE)" tüp değil. Not M1, kutu MII diyorsa da not
  kazanıyor (`olgunlugu_nottan_duzelt()`, v6.161'in ters yönü;
  kullanıcı doğruladı, 2026-09-24: "M1 kararı doğru").
- **Parantezsiz ama tek tüplü dondurma yazılıyor** (v6.160): "5 ADET M2
  OOSİT 1 TÜPTE" — dağılım belli. **Yumurtada tüp sayısı hiç yazmıyorsa
  da tek tüp** (v6.161, kullanıcının cevabı: "2 ADET M2 OOSİT DONDURULARAK
  SAKLANDI tek tüptür"); embriyoda bu varsayılmıyor. "2 TÜPTE 4 ADET" gibi
  dağılımı yazmayan çok tüp ve olgunluğu karışık olan ("M1 M2", sayısız)
  hâlâ yazılmıyor, uyarı çıkıyor. Dar onarım kipi `dondurma`: hiç tüpü
  olmayan tedaviye dondurmayı yazar; v6.165'ten beri tüpü olan tedavide
  yalnızca EKSİK örneği ekler (`yalnizca_ekle`), tüpteki örneğe, skoruna ve
  durumuna dokunmaz, hiçbir şeyi çıkarmaz. Bir okuma kuralı düzelince
  aktarılmış tüpü onarmanın `tamamla`'sız yolu bu. Son satırı kaç aktarılmış
  tedaviye baktığını söylüyor (v6.166; 0 = etiket tutmuyor), UYARI veren
  tedaviyi hiçbir şey yazmasa da basıyor. Kullanıcı "0 tedaviye" derse önce
  aracın sürümünü sor (`git log --oneline -1`): eski araç aynı çıktıyı verir.
- **Olgunluğu kaynakta hiç sayılmamış yumurta dondurulabiliyor** (v6.160,
  havuzun `olcusuz`'u): MII/immatür kutuları boş, not "1 ADET OOSİT
  DONDURULARAK SAKLANDI". Yalnızca kaynağın sayılarının ÖTESİNDEKİ
  yumurtalar — empty zona da maturasyon kaydı olmadan açılıyor, içinde
  yumurta yok.
- **Dondurma notu MII sayısıyla çelişirse not kazanır** (v6.161,
  kullanıcının cevabı: "yanlış yazılmıştır, en son yazılanı kullan"):
  `olgunlugu_nottan_duzelt()`, notun M2 sayısı MII'den çoksa fark
  immatürden MII'ye geçer, not "Access'te MII 4 ... yazıyordu" der. Aktarım
  anında çalışıyor (yumurtalar o an açılıyor); daha önce aktarılmış
  tedavinin maturasyon kayıtlarına dokunmuyor. MI yazılmış yumurta yine M2
  yerine konmuyor — sayı baştan doğru açılıyor.
- **İptal kalıpları** (`_IPTAL_AYRINTI`): fertilizasyon olmadı, cleavage
  arrest, 5. gün arrest, v6.149'dan beri "OOSİT ÇIKMADI" → Yumurta Çıkmadı,
  "İNMATÜR OOSİT SEBEBİYLE" → İmmatür Yumurta. Programdaki sebebin adıyla
  **birebir aynı söz** olmalı, yorum değil; empty zone ve 3PN'in listede
  karşılığı yok, genel iptal kalıyor. Dondurma onarımı var olan tüpü notun grubuyla eşleştiriyor
  (tüpteki örnek kendi skorundan / olgunluğundan tanınıyor), eksik yeri
  tamamlıyor, notta olmayanı çıkarıyor; **tüp silinmez, etiketi ve konumu
  değişmez**. Yeni bir kural eklersen `tamamla`'nın adımlarına da ekle ve
  aynı "ikinci çalıştırma" karşılaştırmasını yap.
- **FET'te transfer edilen embriyonun kalitesi yazılıyor** (v6.154,
  `_fet_transfer_kalitesi()`; kullanıcı: "FET tedavileri hâlâ formlara
  işlenmiyor"). Kaynağın EMBRİYO1/2 kutuları FET'te yalnızca transfer
  notuna gidiyordu — değerlendirme yoktu, Özet'in EMBRİYO1/2 ve TRANSFER
  AŞAMASI kutuları, ART Lab'ın "Uterus grade"i boş basılıyordu. Kaynağa
  bağlamadan SONRA çalışıyor; bu tedavide o tipte değerlendirmesi olana ve
  kaynak tedavisinde aynı günün kaydı olana dokunmuyor (v6.146'nın örnek+gün
  çakışması). Dar kip: `transfer` (elle düzeltilmiş skoru ezmez).
- **Taze transfer yazılıyor** (v6.148; araç yalnızca FET transferini
  yazıyordu, IVF/ICSI tedavisi "transfer ile bitti" deyip transfer ekranı boş
  kalıyordu). Dondurmadan SONRA: ikisi de 2PN'lerden seçiyor.
- **Kaynağın sayıları tutmayabilir, önce hangisinin korunacağına karar ver:**
  ICSI toplamı tutmuyorsa 2PN korunuyor (dondurulan/transfer edilen embriyo
  ona dayanıyor), dejenere kısılıyor; 2PN 0 ama embriyo dondurulmuşsa
  embriyo döllenme kaydı olmayan enjekte yumurtaya yazılıyor — tanktaki tüp
  görünmeli (v6.142). Döllenme ya da ICSI **uydurulmuyor**: ICSI sayısı hiç
  yoksa transfer yazılmıyor, uyarı çıkıyor.
- **Satırın tipi sayılardan da çıkıyor**: "OOSİT ÇÖZME" Yumurta Çözme
  (yumurtalar çözme olayıyla, `thaw_cycle_id`); OPU'su yok, ÇÖZDÜRÜLEN dolu
  bir satır FET (3→5 kültür) (`_satir_tipi()`, PGT kültürü).
- **Tarihsiz satır** bir önceki kaydın tarihini alır, not "yaklaşık" der,
  OPU/transfer alanı boş kalır; **yazım hatalı tarih** `duzelt=` dosyasıyla
  düzeltilir, not eski değeri söyler. Düzeltme dosyası hasta kaydına bağlı,
  **depoya girmez**. Aynı hastanın aynı günkü dolu satırının boş ikizi atlanır.
- **"BB" = birleşme başlangıcı** (kullanıcının cevabı, v6.157): "BB",
  "BİRLEŞME G1", "BİRLEŞMEG3" hücre sayısı boş, `cl_birlesme=1` bir cleavage
  değerlendirmesi olarak yazılıyor, grade yazılıysa o da. v6.148–v6.156
  arası skorsuz embriyo diye yazılmıştı, goc_048 onları düzeltti.
  Tüp eşleştirmesinde anahtarı hâlâ "bilinmiyor" (`_degerlendirme_anahtari()`).
- **Dondurma notunun v6.164 okumaları** (haziran–ekim 2025, yedisi de
  sessizdi -- tüp eksik ya da fazla yazılıyordu, uyarısız):
  - "REFREEZ YAPILARAK / YAPILAN" niteleme, fiil değil (`_DONDURMA_FIILI`);
    "GERİYE ... REFREEZ ... DONDURULDU" (bitmiş fiil) stok değil, yeniden
    dondurma.
  - Bir notta iki gün ("D3 (..) D5 (..)"): grubun günü önündeki son işaret
    (`_son_gun()`, `grup_gunleri`); saat ve değerlendirme günü grup grup.
  - Aynı tüp iki kez yazılmışsa (notun ADET'i = DONDURULAN < grup toplamı ve
    tekrarı çıkarınca tam tutuyor) tekrar düşüyor, not söylüyor. Yalnızca
    embriyoda; aynı içerikli iki tüp olağan, sayılar tutuyorsa dokunulmuyor.
  - Yumurtada "4-M2", "1*1", "1M*1" okunuyor; rakamla başlayan okunamayan
    embriyo yazımı ("8HGT1") skorsuz embriyo (sayı tutsun, skor
    uydurulmasın). Başka tanınmayan parça UYARI ile atılıyor -- **tanınmayan
    öğeyi sessizce atma**, tüpe eksik yazılıyor demek.
  - ICSI sayısı boş ama döllenme sonuçları dolu: ICSI = 2PN + intakt +
    anormal + işlem sonrası dejenere (`icsi_sayisini_tamamla()`), not
    söylüyor. Sonuç da yoksa ICSI yazılmıyor.
  - "4BA TA": skor okunuyor, "TA" notta; anlamı kullanıcıya soruldu.
- **v6.165 okumaları** (kasım–aralık 2025, ocak–mart 2024):
  - Ayırıcısız skorlar ("10HG28HG2", "8HG2 8HG2 8HG2 6HG3"):
    `_bitisik_ayir()`. `_skor_coz()`'ün regex'i sona bağlı değil ("8HG1BB",
    "4BA TA" niteleme) -- arkada kalan metin rakamla başlıyorsa bak, o bir
    embriyo daha olabilir. Şubat 2026'da bir tüpe bu yüzden 4 yerine 1
    embriyo girdi.
  - "BBG1", "BİRG1": birleşme + grade (`_YUVA`); "BİR" yalnızca grade'iyle.
    Kullanıcı doğruladı (2026-09-24): "BİRG1" = Birleşme G1.
  - Eksik parantez: "(3BB (3BC)" iki tüp, "4AA-3AA)" bir tüp -- dışarıda
    kalan parçanın bütün öğeleri tanınıyorsa. "TÜPTE84*M2)" -> "(" (shift'siz
    "8").
  - **Kaynağın sayısı (ADET/DONDURULAN) tüplerden çoksa UYARI** (`eksik_not`):
    eksik yazılmıyor ama söyleniyor. "İLE TOPLAM ... KALDI" stok, durak.
  - Yeni bir okuma kuralı eklerken bütün CSV'lerin okumasını eski ve yeni
    araçla karşılaştır; değişen eski satır varsa kullanıcının veritabanında
    da yanlış demektir, onarım yolunu (`dondurma`) söyle.
- **v6.167 okumaları** (nisan–ağustos 2024):
  - Tip: protokolde yazım hatası ("OOSİT CRTYO", "CRRYO") da Yumurta
    Dondurma; ICSI, 2PN, transfer ve DONDURULAN boş, notun bütün tüpleri
    yumurta olan IVF/ICSI satırı Yumurta Dondurma (`tipi_veriden_duzelt()`).
    Aktarılmış olanlar için dar kip **`tip`** (CSV'siz, bütün veritabanı;
    tedavinin kendi kayıtlarına bakıyor, satırın kuralının aynısı). Kısmi
    ICSI'li satır (birkaç yumurtaya ICSI, kalanı dondurulmuş) Access'teki
    tipinde kalıyor -- programın kendi akışında böyle bir tedavinin yeri yok,
    kullanıcıya soruldu.
  - Bir notta yumurta ve embriyo tüpü birlikte ("1 ADET 5,GÜN EMBRİYOSU
    (1CB) ... 16 ADET OOSİT (6*M2) ..."): grup grup tür (`grup_yumurta`),
    zaman grup grup (`_grup_zamanlari()`), var olan tüp türünün içinde
    sırasıyla eşleşiyor. Aynı tüpte ikisi birden yazılmışsa UYARI.
  - Embriyoda beklenen sayı önce DONDURULAN, boşsa ADET (v6.165'te büyüğü).
  - ICSI yumurta sayısından fazlaysa yazım hatası: boş sayılıp döllenme
    sonuçlarından (v6.164'ün kuralı), not Access'teki değeri söylüyor.
    Doğrusu biliniyorsa düzeltme dosyasında `KAYNAK#KAYIT  ICSI  eski  yeni`.
  - Açılan yumurta: TOPLANAN, olgunluk sayılarının toplamı ve ICSI'nin
    büyüğü (`_yumurta_sayisi()`, Yumurta Çözme'de zaten böyleydi). "Toplanan"
    kutusu Access'teki değeri tutuyor, not farkı söylüyor.
  - **Aynı hastanın aynı günkü aynı tipte iki dolu kaydı**
    (`ikizleri_ayikla()`): birebir aynıysa ikincisi atlanıyor; farklıysa İKİSİ
    DE atlanıyor, kullanıcı doğru olmayanı düzeltme dosyasına
    `KAYNAK#KAYIT  ATLA` yazıp dosyayı yeniden aktarıyor. Karar kullanıcının --
    hangisinin doğru olduğunu tahmin etme. Yalnızca `liste`/aktarımda; onarım
    kipleri aktarılmış tedavilere işaretleriyle ulaşıyor.
- **Access'teki ad programdakinden farklıysa** eşleşme yine dosya
  numarasıyla, rapor "DİKKAT" diyor (ad rapora yazılmıyor).
- **Kaynak dosya ve ondan üretilen CSV depoya girmez** — gerçek hasta
  verisi. README/CLAUDE.md'ye hasta adı/dosya numarası yazma.

**Embriyo cycle değiştirmez; her alan tek bir soruyu yanıtlar.**
`specimen.cycle_id` nereden geldiği (OPU/ICSI cycle'ı, değişmez),
`olay.thaw_cycle_id` hangi tedavi için çözüldüğü, `olay.tr_cycle_id` nerede
transfer edildiği, **`olay.vit_cycle_id` hangi tedavide dondurulduğu**
(v6.143; boş = kendi tedavisi). FET böyle bağlanır — embriyo kopyalanmaz,
taşınmaz. Transfere ulaşmayan çözme de FET'in kaydıdır, görünmesi gerekir
(README v6.7). Bu üç alan **başka bir cycle'a** işaret edebildiği için kalıcı
silmede `NULL`'a çekilmeleri şart (bkz. tuzak #4) — `cycle_tamamen_sil()` ve
`teshis_silme.py` üçünü de biliyor.

**Bir örneğin birden çok dondurması ve çözmesi olabilir** (v6.143, `goc_046`,
kullanıcının isteği: "Çözülen embriyo aynı FET tedavisinde yeniden
dondurulabilsin ve tüp Cryo Haritası'na girsin"). Geçmiş bir dizi: dondur A →
çöz A → dondur B → çöz B. v6.143'e kadar program örnek başına tek dondurma,
tek çözme varsayıyordu (`olay_kaydet_veya_guncelle()` aynı tipin son kaydını
**güncelliyor**); yeniden dondurma ilk dondurmanın üzerine yazar, ikinci
çözme ilk FET'in çözmesini ezerdi. README v6.143'te bu varsayımın kırdığı
yedi yer tek tek yazılı.
- **Dondurmayı "hangisi" diye sor, "son" diye değil.** Bir tedavinin
  dondurması `db.vit_tedavisi(o) = <tedavi>` (`COALESCE(vit_cycle_id,
  cycle_id)`) — vitrifikasyon ekranı, resmî formların `dondurma_tupleri()`'i,
  ART Lab'ın dondurma saati, ay listesinin "Donan"ı hep böyle. Yeni bir
  yerde bir örneğin dondurmasını okuyacaksan `LIMIT 1` yazıp geçme: hangi
  tedavinin dondurması? Bir tüpün içeriği ise zaten `vit_tasiyici_id` ile
  soruluyor, değişmedi.
- **Çözme tüpüne bağlı: `olay.thaw_tasiyici_id`.** Bir tüpün "çözüldü mü /
  kaç çözme" sorusu `thaw_tasiyici_id = <tüp>`; "örneğin herhangi bir
  çözmesi" bir embriyonun ikinci tüpüne ilkinin çözmesini yazar. Çözme ekranı
  tüp başına bir çözme yazıyor (`ek_kosul`), Cryo Excel'inin çözme sütunu,
  taşıyıcı sayfasının özeti, tedavinin çözme listesi hep tüpe bakıyor.
- **`olay_kaydet_veya_guncelle(..., ek_kosul, ek_deger)`**: aynı tipte birden
  çok kaydı olabilen bir olay yazıyorsan hangisinin güncelleneceğini söyle.
  Verilmezse eski davranış (son kayıt) — yalnızca gerçekten tek olan
  olaylarda (ICSI, fertilizasyon, transfer) böyle bırak.
- **Önce en son adım geri alınır.** Çözülmüş bir tüpün dondurması geri
  alınamaz (`_vit_geri_alma_engeli()`), çözmeden sonra yeniden dondurma
  varsa çözme geri alınamaz (`_cozme_geri_alma_engeli()`); ölçü kimlik
  sırası, saat değil (saatler elle geri tarihlenebilir). Aynı kural kayıt
  tarafında: çözülmüş bir tüpün dondurma kaydı başka tüpe **taşınamaz**
  (eski sekmedeki form). Engel ekranda yazar, sunucu da reddeder.
- **Geri alma bağlantısı ekranın tedavisini taşır**:
  `/specimen/{id}/vit-sil?cycle=N`. Adressiz eski bağlantı son dondurmayı
  bulur (eski davranış).
- **Çözmeyi geri almak tüpü haritaya geri koymaz** — bu sürümden önceki
  bilinçli bir karar, `thaw_sil.html` söylüyor; değiştirme.
- **FET'in vitrifikasyon listesi `_FET_DONDURULABILIR`**: bu tedavi için
  çözülüp dejenere çıkmayan, transfer edilmemiş (ya da bu tedavide zaten
  yeniden dondurulmuş) embriyolar. ivf_icsi'nin iki süzgeci
  (`_ICSI_YAPILMADI`, `_DEGERLENDIRILMIS`) FET'e uygulanmaz.
- **Göç çalışmamışsa eski davranış** (`db.kolon_var()`,
  `db.cozme_tupu_var()`, `db.yeniden_dondurma_var()`); FET'in vitrifikasyon
  ekranı göç uyarısı basar.
- **Hasta kartının tedavi satırı yeniden dondurmayı söylüyor** (v6.151,
  `app.hastanin_yeniden_dondurmalari()`): dondurulan tedavide rozet + tüp +
  "→ N. tedavide çözüldü", çözen tedavide "N. tedaviden". Ölçü türetilmiş:
  aynı örneğin daha önce (kimlik sırası) bir çözmesi var. Yumurta Çözme'nin
  embriyo dondurması sayılmıyor (`db.yumurta_mi()` çözmede ve dondurmada
  farklı cevap veriyor). Yeni bir yerde "bu yeniden dondurma mı" diye
  soracaksan bu işlevin koşulunu kullan.
- **Zaman çizelgesi ve tedavi ekranının özet kutusu da işlemin yapıldığı
  tedaviye bakıyor** (v6.146, kullanıcının isteği). v6.143'te kapsam
  dışıydı. Kural `db.olay_tedavisi()`/`db.tedavide_yapilan()`'da, aşağıdaki
  "Bir olayın yapıldığı tedavi" maddesine bak.

**Bir olayın yapıldığı tedavi: `db.olay_tedavisi(o)`** (v6.146).
- Çözme `thaw_cycle_id`'den, transfer `tr_cycle_id`'den, dondurma
  `vit_cycle_id`'den (`vit_tedavisi()`) alınıyor; boşsa kendi tedavisi.
- Öteki işlemlerin (değerlendirmelerin) "hangi tedavide" alanı yok. Ölçü
  embriyonun o andaki tedavisi: işlemden ÖNCEKİ son çözme hangi tedavi
  içinse o, çözülmemişse kendi tedavisi. FET (3→5 kültür)'te çözülen
  embriyonun blastokist değerlendirmesi FET'in işi.
- Ölçü **saat**, kimlik değil: değerlendirme kaydı güncellenince kimliği
  eski kalıyor, saati güncelleniyor.
- "Bu tedavide yapılan olaylar" koşulu `db.tedavide_yapilan(cid)` →
  `(kosul, parametreler)`. Adaylar tedavinin kendi örnekleri ile bu tedavi
  için çözülenler.
- Zaman çizelgesi (ART Lab'ın İŞLEM saatleri ve yüklenen formların
  `{{saat_*}}` etiketleri de oradan) ve özet kutusu bu koşulu kullanıyor.
  Tedavi başına bir işlemi soran yeni bir sayım/saat yazarsan `s.cycle_id`
  değil bu koşul — yoksa FET'in işi kaynak ICSI'ye yazılır.
- **v6.147'den beri resmî formlar ve ay listesi de** (Yumurta Çözme'nin
  ICSI'si yoksa kaynak Yumurta Dondurma'ya yazılırdı):
  - resmî formların sayımları (`formlar._bu_tedavide_say()`/`_adet()`) ve
    yumurta ızgarasının her hücresi (`db.bu_tedavide(cid, 'x')` —
    örneği dış sorgudan gelen alt sorgu için kısa koşul). Izgaranın
    satırları `formlar.yumurta_kosulu()`: kendi örnekleri, Yumurta Çözme'de
    çözülen yumurtalar (`db.cozulen_yumurta_islenir()`); `fet`/`fet_kultur`'un
    ızgarası değişmedi. Özet formunun "Toplanan"ı FET tiplerinde boş.
  - ay listesinin M2'den blastokiste sayıları (`db.tedavide_yapilan_ifade("c.id")`,
    bağıntılı alt sorgu hali); FET tiplerinde "Toplam yumurta/Sağ/Sol" boş.
  - **Tedavinin Excel dökümü bilerek değil**: bir geçmiş, hücreleri örneğin
    son kaydı; FET tiplerinde yalnızca satırlara bu tedavi için çözülenler
    eklendi. İstatistik ekranı da örneğin kendi tedavisinin ayına yazıyor
    (MII artık yalnızca toplanan yumurtalardan, paydayla aynı süzgeç).
  - Denendi: var olan 120 tedavide ART Lab ızgaraları, Excel dökümleri ve
    istatistik eski kodla birebir aynı; tek fark FET'lerin "Toplanan"ı.
- **Dondurulan örneğin skoru dondurmanın tedavisinden:
  `db.bu_tedavinin_skoru(tedavi, o)`** (v6.148). Vitrifikasyon ekranı,
  taşıyıcı sayfası ve resmî formların dondurma satırı "en son
  değerlendirme"yi basıyordu; embriyo sonra bir FET (3→5 kültür)'de yeniden
  değerlendirilince kaynağın ekranı FET'in 5. gün skorunu gösteriyordu. Kural:
  o tedavide herhangi bir değerlendirme varsa yalnızca onlar, hiç yoksa
  hepsi (düz FET'te yeniden dondurulan embriyonun FET'te skoru olmaz).
  **Sıralamayla yazma** (`ORDER BY (bu tedavi) DESC`): tüpün tedavisinde
  yalnızca cleavage, FET'te blastokist varsa blastokist skorunu soran alt
  sorgu yine FET'inkini bulur. Bir tüpün/tedavinin dondurduğu örneğin
  skorunu soran yeni bir yer yazarsan bu koşulu kullan. Tedavinin Excel
  dökümü bilerek bütün geçmişi basıyor (v6.147). Vitrifikasyon ekranının
  "Dondurulmuş" kartı da artık `_vit_satiri()`'nin kalitesini basıyor
  (cleavage'da "5HG3"), yalnızca blastokist skorunu değil.
- **Kapandı (v6.146'da bulunmuştu):** değerlendirmeler (örnek, gün)
  başına tek kayıt (`_gun_olay_kaydet()`). Kaynakta 5. gün kaydı olan bir
  embriyo FET (3→5)'e alınıp yine 5. gün değerlendirilirse kaynağın
  kaydının üzerine yazılırdı. **Kullanıcının cevabı (2026-09-23): "FET
  (3→5)'te blastokist değil cleavage embriyosu çözülüyor"** — yani bu
  durum klinikte doğmuyor; ne uyarı ne ayrı kayıt eklendi. FET (3→5)'e
  blastokist tüpü alınması v6.156'dan beri engelleniyor (kullanıcının
  isteği).

**Fotoğraf devralma yok.** Her aşama ekranı sadece kendi aşamasının karelerini
gösterir. (Eskiden devralıyordu, kafa karıştırdı, kaldırıldı — README v5.1.)

**Örnek kodu = `<hasta dosya no>-<cycle no>-<sıra>`** (`527078-2026-0001-03`).
`specimen.id` bunun son iki parçası ve **değişmez** — dört tablonun yabancı
anahtarı. Kodu `ornek_kodu()` üretir (Jinja global); dosya adlarında da bu
kullanılır, kaynak resmin adı asla kullanılmaz.

**Oosit → zigot → embriyo aynı örnektir, kod değişmez.** Soyağacı böyle
korunur ("bu blastokist hangi oositten çıktı"). Değişen sadece ekrandaki
isim: `ornek_adi(asama, cycle_tipi)` → Yumurta / Zigot / Cleavage /
Blastokist / Embriyo (`oosit_cryo`'da vitrifikasyon-çözme-transferde yine
Yumurta — v6.134'e kadar "Oosit" yazıyordu). Yeni bir aşama ekranı
yazarsan "Yumurta" diye sabit yazma, bu fonksiyonu kullan.

**Görüntü arşive kopyalanır, kaynağa dokunulmaz.** Kamera klasörü
(`snapshot/`) temizlense de program görüntüyü `arsiv/`'den gösterir.
Yapı: `arsiv/<hasta dosya no>/<cycle no>/` (v6.4; öncesi `<yıl>/<cycle no>`).
Veritabanı **göreli** yol saklar — tam yol yazma, makine değişince bulunamaz.

**Yol parçalarını `goruntuler.guvenli_ad()`'den geçir.** macOS NFD / Windows
NFC farkı, Windows'un yasak karakterleri ve ayrılmış adları (`CON`, `NUL`)
yüzünden klasör USB ile taşınınca yollar bozulabilir. Hasta **adı** klasör
adında yok, sadece dosya no — ad değişse bile yol bozulmasın diye (README v6.4).

**Numara üretirken `db.yazma_islemi()` kullan.** "En yüksek numarayı oku →
artır → kaydet" iki kullanıcıda aynı numarayı üretir; `BEGIN IMMEDIATE` bunu
atomik yapar. Dosya kopyalama gibi yavaş işleri işlemin içine koyma — kilit
boyunca herkes bekler. `journal_mode` WAL, bekleme 15 sn (README v6.6).

**`lab.db` ağ sürücüsüne konmaz.** SMB/NFS'te dosya kilitleme güvenilmez
(bozulma riski) ve WAL hiç çalışmaz. İkinci makine programı çalıştırmaz,
tarayıcıdan mini PC'ye bağlanır. `arsiv/` ağa taşınabilir (`yerel_kur.py`).

**Cleavage'da "Birleşme"** (v6.157, goc_048, kullanıcının isteği: "Birleşme
seçilince hücre sayısı kaybolsun, grade ve fragmantasyon gözüksün ...
Birleşme G2 gibi"). `olay.cl_birlesme` = 1: hücre sayısı ve simetri yok
(v6.158'de simetri de, kullanıcının isteği: "Simetri de gizlensin") —
sunucu birleşmede ikisini de yazmıyor, ekran kutularını gizliyor, bilgi
kartı ve silme ekranı simetri satırını basmıyor.
- **Kalitenin yazımı tek yerde: `db.cleavage_yazimi(hucre, skor)`** —
  "8HG2" / "Birleşme G2". Hücre yerini okuyan SQL `db.cl_hucre_ifadesi(x)`
  (birleşmede `db.BIRLESME` sözü): vitrifikasyon, resmî formların
  dondurma/transfer/ızgara hücreleri, tedavi Excel'i. Yeni bir yerde
  cleavage kalitesi basacaksan `cl_hucre_sayisi`'nı çıplak okuma —
  birleşme boş hücre gibi kaybolur. `formlar.son_alt()`/`gun_alt()`
  parantezli ifadeyi olduğu gibi alıyor.
- Numara şeridinde "3-Bir.", bilgi kartında "Hücre sayısı: Birleşme".
- Otomatik A/B/C skoru hücre sayısı istiyor, birleşmede yok: grade elle.
- Resmî formun NOTLAR satırı kaliteyi ve tüp parantezini bölmüyor
  (`formlar._sar()`).

**Otomatik skorlar kaynak işaretler.** Elle skor girilirse
`cl_skor_kaynagi='elle'` yazılır, otomatik hesap onu ezmez.
- **Elle `cl_skor` artık serbest metin değil, kapalı G1-G4 seçimi**
  (v6.122, kullanıcının isteği). `liste_degeri`'nde yeni bir liste
  (`cleavage_skor`, `goc_041`) — `cl_simetri`'nin aynı `.secenek`/`.sec`
  radyo deseni. **Kodlar bilerek büyük harf** ("G1", "g1" değil): POST
  handler'daki `(f.get("cl_skor") or "").strip().upper()` satırı elle
  değeri her zaman büyütüyor, kod lowercase olsaydı `liste_etiket()`
  eşleşmeyi bulamazdı (kod kendisi düşerek gizlenen bir hata, laboratuvar
  etiketi sonradan değiştirince ortaya çıkardı). Otomatik hesaplanan A/B/C
  değerine dokunulmadı, o soru hâlâ açık (bkz. "Bekleyen işler" madde 5) —
  `liste_etiket('cleavage_skor', kod)` bulunamayan bir kodu (A/B/C gibi)
  olduğu gibi döndürdüğü için ikisi çakışmıyor.

**"İşlemi yapan" her aşama ekranının altında.** Aşama başına tek değer
(`islem_yapan` tablosu, `UNIQUE(cycle_id, asama)`), sütun adı hâlâ
`yapan_ad` ama **v6.99'dan beri serbest metin değil** — şifresi olan
(aktif) personelden seçiliyor, `personel_listesi()` Jinja global'ı
dolduruyor. Kaydı giren `kullanici_id` ile karıştırma — biri "kim yaptı",
diğeri "kim girdi", bu ayrım değişmedi. Paylaşılan parça
`_islem_yapan.html`; değer Jinja global `islem_yapan_ad()` ile okunur,
varsayılan seçim (kayıt yoksa) `guncel_kullanici_ad()` — şifresiyle giren
kişi. **İkisi de `_GIRIS_KULLANICI`/`_YETKILER` gibi bir `contextvars`
üzerinden çalışıyor**, request'i elden ele taşımadan — yeni bir "şu an
giriş yapmış kim" ihtiyacı doğarsa aynı deseni kullan, her rotaya
`"kullanici": request.state.kullanici` eklemeye kalkma. **Kayıtlı değer
personel listesinde yoksa** (hesap pasif yapıldı ya da v6.99 öncesi
serbest metinle yazılmış eski bir ad) tuzak #6: `_islem_yapan.html` o
değeri listeye kendi seçeneği olarak ekliyor, yoksa seçici sessizce ilk
isme kayar. Yeni bir aşama eklersen `ASAMA_SIRASI`'na koy + şablonuna
`{{ iy.kutu(c.id, "<asama>") }}` ekle — gerisi otomatik (README v6.3).
Makro isteğe bağlı `etiket`/`ipucu` alır; varsayılanı değiştirme, sadece
belirsizlik olan ekranda ver (v6.9).

**Modül izinleri tek noktada kontrol edilir: middleware.** `yol_modulu(yol)`
yolu bir modüle eşler, middleware izni yoksa `/hastalar`'a döndürür. ~50 rotanın
her birine kontrol eklemek tuzak #1'in tarifi — **rotalara tek tek ekleme**.
Şablonlarda Jinja global `yetkim("modul")` ile bağlantı gizlenir; gizlemek tek
başına yeterli değil, asıl engel middleware'de. Aşama düğmeleri ve gezinme
çubuğu `cycle_asamalari()`'nden besleniyor, süzme orada.

**Yeni modül eklersen üç yere ekle:** `app.py` `MODULLER`, `goc_026.py`
`MODULLER`, `kullanici.py` `MODULLER` — sonra `goc_026`'yı tekrar çalıştır,
yoksa kimse o ekrana giremez. Yeni kullanıcı **tüm** modülleri alır
(`tum_yetkileri_ver`); kısıtlama yöneticinin bilinçli olarak kaldırdığı
kutulardan doğar, boş bırakılmışlıktan değil (README v6.14).

**`rol` serbest metin bir kolon, CHECK yok.** Kodda anlamlı olan tek değer
`yonetici`; başka her şey (eski kayıtlardaki `androlog` gibi) yönetici olmayan
kullanıcı demek. Rol seçicide **tanımsız rol kendi adıyla ve seçili
gösterilmeli** — yoksa tarayıcı ilk seçeneği gösterir ve tek tıkla kullanıcı
farkında olmadan yönetici olur (v6.15'te gerçekten böyleydi, düzeltildi).
Kim hangi ekrana girer sorusunu rol değil, modül izinleri belirler.

**Yetki: `rol='yonetici'` kullanıcı yönetimine girer.** v6.11'e kadar `rol`
hiçbir yerde kontrol edilmiyordu. Yeni bir yönetici rotası yazarsan başına
`yonetici_kontrol(request)` koy — ekranda düğmeyi gizlemek yetmez, sunucu da
reddetmeli (hasta silmedeki kuralın aynısı).

**Kullanıcı silme = pasif yapma.** 11 tablo `kullanici.id`'ye bağlı; kayıt
girmiş kullanıcı kalıcı silinemez — ekranda seçenek görünmez, sunucu da
reddeder. Kalıcı silme yalnızca hiç kaydı olmayan hesaplar için, kullanıcı
adı + `SIL` + tarayıcı onayı ile. **Son aktif yönetici pasif yapılamaz ve
silinemez** (kilitlenme koruması). Yeni bir tabloya `kullanici_id` eklersen
`KULLANICI_KAYITLARI` listesine de ekle, yoksa silme FOREIGN KEY hatası verir
(README v6.11).
- **`yetki` bu listede yok, ama FK'sı var** (v6.100'de bulundu). `yetki`
  bir kayıt değil, izin ataması — silmeyi engellemesin diye
  `KULLANICI_KAYITLARI`'na bilerek eklenmedi, ama tablo `kullanici_id`'ye
  FK ile bağlı. `kullanici_sil()` bunu `oturum` gibi **önce siliyor**,
  `kullanici` satırından önce — yoksa her yeni kullanıcının açılışta
  `tum_yetkileri_ver()` ile aldığı satırlar yüzünden kalıcı silme kendisi
  FOREIGN KEY hatasıyla patlıyordu (herhangi bir normal kullanıcıda,
  hiç "kaydı" olmasa bile). Yeni bir "kayıt değil ama FK'sı var" tablo
  eklersen (izin/atama gibi) aynı deseni kullan: `KULLANICI_KAYITLARI`'na
  değil, doğrudan silme rotasındaki temizlik listesine ekle.

**Var olan kullanıcının adı ve kullanıcı adı değiştirilebilir** (v6.106,
kullanıcının isteği). `/kullanici/{id}/duzenle`, `kullanici_yeni()`'deki aynı
doğrulama (boş olamaz, kullanıcı adı yalnızca harf/rakam/nokta/alt çizgi,
`kullanici_adi` **lab'dan bağımsız UNIQUE** olduğu için `sqlite3.
IntegrityError` de yakalanıyor — `kullanici_yeni()`'deki tuzağın aynısı).
**Ad değişirse hasta kayıtlarındaki "İşlemi Yapan" da otomatik güncellenir**:
`islem_yapan.yapan_ad` ve `sperm_dondurma.yapan_ad` kullaniciyi FK ile değil
o anki adın **metin kopyasıyla** tutuyor (v6.99/v6.101'in bilinçli kararı,
"personel_listesi() zaten genel amaçlıydı" gerekçesiyle) — ad değişince eski
metin kendiliğinden değişmez, `kullanici_duzenle()` bu yüzden eski adı
taşıyan satırları (`WHERE lab_id=? AND yapan_ad=<eski ad>`) elle güncelliyor.
Yeni bir "adı `personel_listesi()`'nden seçilen, metin olarak saklanan" alan
eklersen (bir sonraki `_islem_yapan`/`sperm_dondurma.yapan_ad` benzeri) aynı
listeye ekle, yoksa o alan rename'den sonra sessizce eski adda kalır.
**`kullanici_adi` (giriş adı) hiçbir hasta kaydına yazılmaz** — yalnızca
kimlik doğrulamada kullanılıyor, cascade gerektirmiyor.

**Kullanıcıya verilmiş şifreler yönetici ekranında görüntülenmez, görüntülenemez.**
Bekletilen şey hash (bkz. "Şifre değişikliği yönetici onayı ister"), düz
şifre hiçbir yerde durmuyor — var olan bir kullanıcının şifresini **geri
almak teknik olarak mümkün değil** (hash tek yönlü). Yönetici yalnızca yeni
bir şifre **belirleyebilir** (`/kullanici/{id}/sifre`, zaten kendisi yazdığı
için görmesine gerek yok) ya da personelin `/sifre`'den gönderdiği isteği
onaylayabilir (o zaman da yalnızca hash geçiyor, düz metin yöneticiye hiç
uğramıyor). Şifreleri geri okunabilir/şifre çözülebilir bir biçimde tutmak
bu mimariyi tersine çevirir ve `lab.db`'nin USB ile taşındığı, HTTPS
olmadığı bir ortamda ciddi bir güvenlik açığı olur — kullanıcı sormadan bu
yönde bir değişiklik yapma.

**Şifre değişince o kullanıcının açık oturumları düşer.** `sifre_yaz()` bunu
kendisi yapar; ayrı bir yol yazma. Yoksa eski şifreyle açılmış tarayıcı 12 saat
daha çalışır.

**`/sifre` giriş gerektirmez, ama mevcut şifre ister.** Giriş ekranından da
açılır (v6.12). Güvenliği düşürmez — kimlik yine mevcut şifreyle kanıtlanıyor.
Hata mesajı **tek ve aynı**: "Kullanıcı adı veya mevcut şifre yanlış." Ayrı
mesaj yazma, hangi kullanıcı adının var olduğunu sızdırır. Pasif kullanıcı bu
yoldan da şifre değiştiremez.

**Şifre değişikliği yönetici onayı ister** (v6.61, `goc_030`). Kullanıcının
kararı (2026-09-12). `/sifre`'nin kuralları değişmedi (giriş gerekmez, mevcut
şifre şart, hata mesajı tek); değişen, kaydetmenin şifreyi **yazmak yerine**
`sifre_istegi` tablosuna istek koyması.
- **Bekletilen şey hash.** Düz şifre hiçbir yerde durmuyor; kimlik zaten istek
  anında mevcut şifreyle kanıtlanıyor, bekleyen hash onaylanana kadar hiçbir
  girişte geçmiyor. "Yeni şifreyi onay anında sor" denmedi: onayı iki kişinin
  aynı anda orada olmasına bağlardı.
- **Yöneticinin kendi şifresi anında geçer.** Onaylayacak kişi o; tek yönetici
  kendi isteğini onaylamak için giremez duruma düşerdi (README v6.11'deki
  kilitlenme korumasının aynısı). Bu istisnayı kaldırma.
- **Bekleyen istek kullanıcı başına tek** — ikincisi birincinin yerine geçiyor,
  yoksa yönetici eski bir şifreyi onaylayabilir.
- **Onay şifreyi yazar ve o kullanıcının oturumlarını kapatır.** `sifre_yaz()`
  düz şifre beklediği için çağrılamıyor; iki satır elle yazılı, ikisi de
  kalmalı — oturum düşmezse "onayladım" yanıltıcı olur.
- **Ekran `/sifre-istekleri`, yalnızca yönetici.** Rotalar `onayla`/`reddet`
  diye adlandırıldı: `sil` ile bitse `yol_modulu()` onu "silme" modülüne
  bağlardı.
- **Göç çalıştırılmamışsa eski davranış** (`sifre_istegi_tablosu_var()`):
  şifre anında değişir. Şifre değiştirmeyi tümden engellemek, onayın çözdüğü
  sorundan pahalı (tuzak #3).
- Bekleyen istek `/yonetim` düğmesinde sayıyla ve `/kullanicilar`'ın tepesinde
  uyarıyla görünür. **Giriş yapmamış birine `/sifre`'de "onay gerekir" notu
  basılmaz** — hangi kullanıcı adının yönetici olduğunu sızdırırdı.

**Tazeleme şeridi sayfanın son düğmesini kapatmamalı** (v6.61). Şerit
`position: fixed` ve altta; `.kap`'ın alt dolgusu 96px ama şerit 320px
genişlikte satır sarıp **113px** oluyordu. Ölçüldü: `/hasta/yeni`'de
**"Hastayı kaydet"**, `/hastalar`'da "Cryo haritası" şeridin altında
kalıyordu — kullanıcı kaydet yerine **Yenile**'ye basıyor, sayfa yenileniyor,
yazdığı gidiyor, hiçbir mesaj çıkmıyor. Şerit açılırken `<body>` `seritli`
sınıfını alıyor, `body.seritli .kap` dolguyu 160px yapıyor. Şeridi açan tek
yer `seridiAc()` — `kutu.hidden = false` yazma, o fonksiyonu çağır.

**`/yonetim` paneli salt okunurdur.** Durumu gösterir, hiçbir şey değiştirmez;
ayarlar kendi ekranlarından/scriptlerinden yapılır. Buraya yazma işlemi ekleme
(v6.12).

**Klasör yolları `/klasorler` ekranından ayarlanır** (v6.41). Kamera klasörünü
(mikroskobun snapshot attığı yer), arşivi ve yedeği yönetici ekrandan
değiştiriyor; önce tek yol `python yerel_kur.py` idi. Panel yine salt okunur,
oraya yalnızca bağlantı kondu — dil seçimindeki düzenin aynısı.
- **Değer veritabanında değil** `yerel_ayar.json`'da, makine adına göre
  bölümlü. `lab.db` USB ile taşınıyor; yol `ayarlar` tablosunda olsaydı Mac'te
  girilen klasör klinikte de geçerli olurdu. `ayarlar`'a yol yazma.
- **Dosyaya yazan tek yer `db.yerel_yaz()`** — kaydetme öteki makinelerin
  bölümüne dokunmuyor. Kendi `json.dumps`'ını yazma (tuzak #8'in yazma hali;
  `yerel_kur.py` de v6.41'de buna çevrildi).
- **Üçü farklı davranır, sebebi programın onlarla ilişkisi:** kamera klasörünü
  program yalnızca **okur** → var olmayan yol **reddedilir** (yazım hatası
  olursa kamera kuyruğu aylarca boş görünür, sebebi anlaşılmaz); arşive
  **yazar** → yoksa oluşturulur; yedek olduğu gibi kaydedilir, oluşturulmaz
  (çoğu zaman takılı olmayan disk; Mac'te `E:\yedek` klasörü açmak v6.8'de
  başa geldi). Bu üçünü tek kurala indirgeme.
- Hata anahtarları adresten geliyor, `KLASOR_HATALARI` beyaz listesinden
  geçiyor (tuzak #9).
- **Gözat gezgini sunucunun klasörlerini geziyor** (v6.43). Tarayıcı sayfaya
  gerçek dosya yolunu vermiyor (`C:\fakepath`), o yüzden işletim sisteminin
  kendi "Klasör Seç" penceresi açılamıyor. `GET /klasorler/gozat` **yalnızca
  yönetici**, **yalnızca klasör adları** döndürüyor — dosya adı ve içerik yok,
  tek sayı fotoğraf sayısı. Bu üçünü gevşetme.
- **Fotoğraf sayımı `goruntuler.UZANTILAR` ile.** İkinci bir uzantı listesi
  yazma: gezginin saydığıyla kuyruğun aldığı ayrı düşer.
- **İki düğme var, ikisi de kalsın** (v6.44, kullanıcının kararı): **Gözat**
  işletim sisteminin kendi klasör penceresini açıyor, **Listeden seç** programın
  gezginini. Tarayıcı seçilen klasörün **yerini vermediği** için Gözat'ın ikinci
  adımı `POST /klasorler/bul`: klasörün adı ve içindeki dosya adları gelir,
  program onu bu makinede arar. **Ad tutması yetmez** — içindeki dosyalardan
  biri de yerinde olmalı, yoksa aynı adlı başka klasör seçilirdi. Bulunamazsa
  listeli gezgine düşülür; o her yerde çalışıyor.
- **iOS Safari'de Gözat gizlenir** (`'webkitdirectory' in
  document.createElement('input')`): orada nitelik yok sayılıp tek dosya
  seçiliyor. Çalışmayan düğme bırakma.
- Arama sınırları `ARAMA_SURESI` / `ARAMA_EN_COK_KLASOR` / `ARAMA_ATLA`'da;
  **POSIX'te `/` kökünden aranmaz** (süre sistem klasörlerinde biterdi).
  Klasör adında `/` veya `\` varsa istek reddedilir.
- **Adlar "klasör" kalacak** (kullanıcının kararı, 2026-09-12): "dosya"
  programda zaten hastanın kaydı (dosya no) ve yüklenen `.xlsx`.

**Program telefonun ana ekranına eklenebilir** (v6.45). Mağazaya gerek yok:
mağazadan inen bir uygulama da yine klinikteki sunucuya bağlanırdı. `/baglan`
ekranı karekod + adım adım yönerge veriyor, yazdırılıp laboratuvara asılıyor.
- **Karekod kütüphanesiz**: `karekod.py`, çıktı SVG. Gerekçe `excel.py` ile
  aynı — klinikteki mini PC'ye kurulum adımı eklememek. Kapsam: bayt kipi,
  M düzeyi, sürüm 1-10. Doğrulaması README v6.45'te: 618 ızgara olgun bir
  kütüphaneyle birebir aynı, ayrıca gerçek okuyucuyla çözüldü. **Dokunursan
  o karşılaştırmayı tekrar çalıştır.**
- **`/manifest.json` bir rota ve `ACIK_YOLLAR`'da.** Tarayıcı onu oturum
  çerezi göndermeden istiyor; korumalı olsaydı simge adsız eklenirdi. İçinde
  hasta verisi yok. Rota olması adın ve dilin lab ayarını izlemesi için.
- iOS yeni sürümlerde manifest'i, eskilerde `apple-mobile-web-app-capable`
  metasını okuyor — **ikisini de** bırak.
- Durum çubuğu `black-translucent`, bu yüzden `.ust`'ün dolgusu
  `env(safe-area-inset-top)` içeriyor. Kaldırırsan iOS'ta başlık saatin
  altında kalır.
- Simgeler `simge_uret.py` ile üretildi; aynı dosya hem normal hem maskable
  (içerik merkezin %25'inde bitiyor, Android'in istediği sınır %40).
- **Android'de tam ekran HTTPS istiyor**, programda yok (bekleyen iş 3):
  orada simge tarayıcı içinde açılabiliyor. iOS'ta tam ekran çalışıyor.
  HTTPS kararı paketleme aşamasına bırakıldı.
- Adres seçimi: yöneticinin kullandığı adres varsa o, yoksa `_yerel_ip()`.
  O da UDP soketiyle **paket göndermeden** buluyor; `gethostbyname` çoğu
  makinede 127.0.0.1 döndürüyor.
- **Karekod programın kendisine açılır; ilk gelen ekran şifre ekranıdır**
  (v6.48). v6.47'de `/ekle` yönergesine açılıyordu ve **gerileme oldu**:
  iPhone "Ana Ekrana Ekle" derken manifest'in `start_url`'ünü değil **o an
  açık olan adresi** kaydediyor, simge açık bir sayfayı yakalıyor ve şifre
  hiç sorulmuyordu. Karekodu açık bir yola çevirme.
- Yönerge `/ekle` **`ACIK_YOLLAR`'da** (okutanın hesabı yok, ekranda hasta
  verisi de yok) ve **giriş ekranındaki bağlantıdan** açılıyor. Ana ekrandan
  açılırsa `location.replace('/')` ile programa geçiyor — v6.47 döneminde
  yanlış adresi yakalamış simgeler böyle kendiliğinden düzeliyor.
- **Bir web sayfası kendini ana ekrana ekleyemez.** iOS'ta API yok;
  Android'de `beforeinstallprompt` var ama HTTPS + service worker istiyor.
  Kod hazır duruyor, HTTPS gelince kendiliğinden çalışacak. "Otomatik ekle"
  sözü verme.
- Simgenin altındaki ad `kisa_ad` (kullanıcının kararı: tam ad,
  "Patient Data Center"). Hem manifest `short_name` hem iOS başlığı oradan.

**"Şifremi unuttum" hiçbir şey sıfırlamaz.** Sistemde e-posta/SMS yok, kimliği
doğrulayacak ikinci kanal yok; doğrulamasız sıfırlama iç ağdaki herkese yönetici
şifresini değiştirme hakkı verirdi (HTTPS de yok). Sayfa kullanıcı adı da
listelemez. Sıfırlamayı yönetici yapar; yönetici de kilitlenirse `kullanici.py`.
Bu kararı gevşetme (README v6.11).

**Laboratuvar personeli olmayan kişi `islem_yapan`'a yazılmaz.** **OPU Hekimi**
`cycle.opu_hekim` kolonunda, **OPU Embriyoloğu** `islem_yapan`'da
(`asama='opu'`). `UNIQUE(cycle_id, asama)` aşama başına tek kişi demek; ikinci
bir kişi gerekiyorsa onu bu kısıtı gevşeterek değil, cycle verisi olarak ekle
(README v6.9).

**Embriyo Dondurma ve Sperm Dondurma tek ekranda, yan yana iki bağımsız
modül** (`/cryo`, "Cryo Haritası" — v6.84'te ayrı bir ekrandı, v6.85'te
kullanıcının isteğiyle birleştirildi: "Cryo Harita başlığı altına toplansın,
ikisinin modülü yan yana olsun"). CLAUDE.md'nin "İki sütun" ölçüsü tam
burada geçerli — iki bağımsız kart, `.sutunlar` > iki `.sutun`. Arama kutusu
**tek**, aynı `ara` iki modülü de süzüyor (ayrı arama kutuları değil — dosya
no/hasta adı araması çoğu zaman ikisi için de aynı arama).
`GET /sperm-dondurma` artık `/cryo`'ya **yönlendiriyor** (eski
bağlantılar/yer imleri kırılmasın diye) — sayfa kendisi yok, şablonu
silindi. Detay/oluşturma/silme rotaları (`/sperm-dondurma/{id}`,
`/hasta/{id}/sperm-dondurma/yeni`, `/sperm-dondurma/{id}/sil`) aynen duruyor.

Aynı taşıyıcı/konum altyapısını paylaşırlar, `tasiyici.kategori` ile
ayrılır (v6.84, `goc_033`) — `sperm_dondurma` (dondurma öncesi semen
analizi, `sperm_analiz` ile aynı kolon adları) `tasiyici_id` ile taşıyıcı/
konuma bağlanıyor. `tasiyici.kategori` (`'embriyo'`/`'sperm'`) **Embriyo
Dondurma'nın `tasiyici` sorgularına yeni bir yerden dokunursan
`t.kategori='embriyo'` süzgecini de ekle**, yoksa sperm taşıyıcıları oraya
sızar. `/disari/cryo` bu süzgece ihtiyaç duymuyor çünkü zaten
`olay.tip='vitrifikasyon'` üzerinden geliyor, sperm taşıyıcıları hiç `olay`
satırı üretmiyor.
- **Bir sperm dondurma kaydı = bir taşıyıcı** (embriyoda olduğu gibi birden
  çok örnek aynı taşıyıcıyı paylaşmıyor) — silmede "kardeş var mı" kontrolü
  yok, taşıyıcı her zaman tek başına serbest kalır.
- **İzin ayrı bir modül değil, mevcut `"cryo"`.** Yeni modül açmanın
  bedeli (üç dosyada `MODULLER` + `goc_026`'yı tekrar çalıştırmak) burada
  ödenmedi — aynı personel grubu varsayıldı, kullanıcıya sorulmadan alınmış
  bir tasarım kararı. Kullanıcı ayrı izin isterse bu ayrıma dönülmeli.
- Yeni bir cycle tipi **değil**: "Oosit dondurma" `goc_032` ile "Yumurta
  Dondurma"ya yeniden adlandırıldı (`kod`, `TIP_KODLARI`, `TIP_ASAMALARI`
  aynen duruyor) — aynı desen, yeni bir tip açmadan önce mevcut
  `liste_degeri.etiket`'in yeniden adlandırılabilir olup olmadığını düşün.
- **Gerçekten yeni bir tip açıyorsan `cycle.cycle_tipi`'nin CHECK kısıtına
  da eklemen gerekir** — `TIP_KODLARI`/`TIP_ASAMALARI`'na eklemek yetmez,
  DB kendi kodu kabul etmez. SQLite CHECK kısıtını ALTER ile değiştiremiyor;
  tablo yeniden kurulur (`goc_031`'in `fet_kultur` için yaptığı, `goc_039`
  `yumurta_cozme` için tekrarladı — aynı regex/rename dansı, kopyala). Dört
  adım: (1) CHECK'i genişlet (tablo yeniden kurma), (2) `liste_degeri`'ne
  `sira=MAX+1` ile ekle (dropdown oradan besleniyor), (3) `TIP_KODLARI`
  (`app.py`) + `TIP_ASAMALARI` (v6.147'den beri `db.py`), (4) `metinler.py`'ye
  `tip_<kod>` anahtarı.

**Sperm dondurma tüp bebek tedavisi olmayan hastalar için de yapılabilir,
tek ekranda kaydediliyor** (v6.85'te başladı, v6.86'da bugünkü haline geldi
— kullanıcının isteği: "onkoloji tedavisi görecek erkek hastalara da sperm
donduruyoruz"). `hasta` kaydı zaten cycle'dan bağımsız var olabiliyordu (0
cycle'lı hasta desteklenmiş bir durum). Cryo Haritası'nın Sperm Dondurma
sütunundaki **"Yeni hasta kaydı (Sperm Dondurma)"** düğmesi
`/sperm-dondurma/yeni-hasta`'ya gidiyor — **tek formda** hasta (yalnızca
erkek hasta alanları, `hasta_form.html`'in eş alanları yok) + dondurma
sebebi + taşıyıcı/konum/semen analizi, tek POST'ta hem `hasta` hem
`tasiyici` hem `sperm_dondurma` yazılıyor.
- **Ortak yazma mantığı `_sperm_dondurma_olustur(hasta_id, f, kid)`'de** —
  hem bu akış hem mevcut hastanın kendi `/hasta/{id}/sperm-dondurma/yeni`si
  onu çağırıyor. Doğrulama **yazmadan önce** bitiyor (fonksiyon içinde
  `FormHatasi` fırlatılıyor, hiçbir INSERT'ten önce).
- **Kayıt açıp doldurma kuralı burada da geçerli**: önce `hasta` yazılıyor,
  `_sperm_dondurma_olustur()` patlarsa (örn. mükerrer etiket) az önce açılan
  **boş hasta kaydı geri alınıyor** — yoksa lab ıssız hasta dosyalarıyla
  dolar. Yeni bir "önce ana kaydı aç, sonra bağımlı kaydı doldur" akışı
  yazarsan aynı geri alma adımını ekle.
- **Hata dönüşü formu boşaltmıyor** (v6.21 kuralı) — şablona doğrudan
  `TemplateResponse` ile `v=dict(f)` geçiliyor, redirect değil (v6.85'teki
  `/hasta/yeni?amac=sperm` denemesi bunu atlamıştı, kaldırıldı).

**Dondurulmuş sperm başka bir hastanın (eşin) tedavisine bağlanabilir**
(v6.86, `goc_034`). `sperm_dondurma.sebep` (dondurma sebebi, serbest metin —
sabit bir liste açılmadı, kategoriler kullanıcıyla birlikte belirlenmeli) ve
`sperm_dondurma.kullanim_cycle_id` (`cycle(id)`'ye FK) eklendi.
`kullanim_cycle_id` `olay.thaw_cycle_id`'nin aynı deseni: **sahiplik
değişmiyor** (`sperm_dondurma.hasta_id` hep dondurmayı yaptıran erkek
hastada kalır), yalnızca "hangi tedavi için kullanıldı" ayrı bir alanda
yanıtlanıyor.
- **Bağlama yeri Androloji ekranı** (`/cycle/{id}/androloji`, yalnızca
  `ivf_icsi`'de var — androloji zaten "bu tedavide hangi sperm kullanıldı"
  sorusunun yeri). Taze örnekten (`sperm_ornek`) bağımsız ayrı bir kart.
  `/cycle/{id}/androloji/sperm-baglama` **bütün laboratuvardaki**, henüz
  bağlanmamış (`kullanim_cycle_id IS NULL`) kayıtları arıyor — hastaya göre
  süzülmüyor, çünkü kayıt bilerek başka bir hastaya ait.
- **Taşıyıcı `durum`'una üçüncü bir değer eklendi: `'kullanildi'`**
  (`'dolu'`/`'bosaltildi'`'nin yanına) — bağlanınca yazılıyor, bağlantı
  kaldırılınca `'dolu'`ya dönüyor. `/cryo`'nun taşıyıcı sorguları buna göre
  süzmüyor (geçmiş kayıt olarak görünmeye devam ediyor), yalnızca "Kullanıldığı
  tedavi" rozeti ekleniyor.
- **Tuzak #4'ün aynısı, yeni bir cycle_id alanı için**: `cycle_tamamen_sil()`
  artık silinen cycle'a bağlı `sperm_dondurma` kayıtlarının bağını koparıyor
  (`kullanim_cycle_id=NULL`, taşıyıcı `'dolu'`ya döner) — bu olmasaydı eşin
  tedavisi kalıcı silindiğinde kocanın (başka hastanın) kaydı kırık bir
  `cycle_id`ye işaret ederdi. **`teshis_silme.py`'ye de aynı tarama + geri
  alma adımı eklendi** (CLAUDE.md'nin "aynısını teshis_silme.py'ye de ekle"
  kuralı, tuzak #4). Yeni bir `cycle_id`-referanslı tablo eklersen ikisini de
  güncelle, `cycle_tamamen_sil()` tek başına yetmiyor.

**Dosya numarası tek eşleştirme anahtarı; isimle eşleştirme yok**
(v6.125, kullanıcının isteği: "erkek hastanın dosya numarası giriliyor ...
eşi ile birlikte tüp bebek için hasta kaydı varsa uyarı mesajı ver ...
hasta kartında dondurulmuş sperm işlemi varsa dosya numarasından eşle").
Şemadaki `UNIQUE (lab_id, dosya_no)` sayesinde **"aynı dosya no" = "aynı
`hasta` satırı"**: tüp bebek çifti tek satır (`ad_soyad` kadın, `es_adi`
erkek) ve o çiftteki erkeğin sperm dondurması aynı satıra
`sperm_dondurma.hasta_id` ile bağlı. Yani "dosya numarasından eşle" ayrı
bir tablo ya da arama değil, var olan yabancı anahtarın okunması.
- **`ad_soyad` ↔ `es_adi` karşılaştırması yazma.** Teknik olarak mümkün
  ama ad benzerliği kesin değil ve yanlış hasta bu işin en pahalı hatası.
  Kullanıcı iki kez "dosya numarası üzerinden" dedi.
- **Paylaşılan iki yardımcı**: `dosya_no_sahibi(dosya_no)` (kim + tedavi
  sayısı + sperm sayısı) ve `hastanin_sperm_kayitlari(hasta_id,
  yalnizca_bagsiz=False)`. Üç ekran da bunları çağırıyor, sorgu
  kopyalanmadı. Yeni bir yerde aynı soruyu soracaksan bunları kullan.
- **Üç yer**: (1) Sperm Dondurma'nın yeni-hasta formunda dosya no
  girilirken uyarı, (2) hasta kartında dondurulmuş sperm listesi,
  (3) androloji ekranında "bu dosya numarasına ait, bağlanmayı bekleyen
  kayıt var" haberi.
- **`/hasta/kontrol` tek uç nokta, ikinci bir kopya açma.** Canlı kontrol
  zaten vardı (`hasta_form.html` ve sperm yeni-hasta formu ikisi de onu
  çağırıyor); v6.125'te **genişletildi** (`es_adi`, `cycle_sayisi`,
  `sperm_sayisi` eklendi), yanına `/sperm-dondurma/dosya-kontrol` diye
  ikinci bir rota açılmadı — ilk yazışta açılmıştı, geri alındı. Ekleme
  geriye dönük uyumlu: `/hasta/yeni`'nin betiği eski anahtarlarla
  çalışmaya devam ediyor.
- **Canlı uyarı engel değil, erken haber.** Asıl engel POST'taki
  `dosya_no_sahibi()` kontrolü (CLAUDE.md "ekranda göstermek yetmez,
  sunucu da reddetmeli"). Engel eskiden düz metin dönüyordu, artık o
  hastaya **götüren bağlantısı olan** bir kutu: çift zaten kayıtlıysa
  doğru davranış yeni hasta açmak değil, o kayda sperm dondurma eklemek.
- **Androloji uyarısı yalnızca bağlı sperm yokken çıkar** (`sd_baglanti`
  boşken) — bağlandıktan sonra zaten bağlı kaydın kendi kartı var.
- **Kapsamadığı durum v6.139'da kapandı**: erkek hasta kendi ayrı dosya
  numarasıyla kayıtlıysa (onkoloji öncesi, çiftin dosyasından bağımsız)
  dosya no tutmuyordu ve hiçbir uyarı çıkmıyordu. Artık çiftin kaydına
  **`hasta.es_dosya_no`** yazılabiliyor (`goc_045`) — aşağıya bak. Elle
  eşleme yolu (v6.86, androloji ekranı) değişmedi.

**Eşin kendi dosya numarası `hasta.es_dosya_no`'da** (v6.139, `goc_045`,
kullanıcının isteği: "Hasta kartında eşin dosya numarasının girilebileceği
yer olsun. Eğer eş erkek olarak sperm dondurma kaydı daha önce yapıldıysa
uyarı versin").
- **FK DEĞİL, düz sayı**: eş henüz kayıtlı olmayabilir (numara önce yazılır,
  kayıt sonra açılır) ve `hasta`'nın benzersizliği `UNIQUE (lab_id, dosya_no)`
  üzerinde, tek kolona FK verilemez. "Kayıtlı mı" her seferinde
  `dosya_no_sahibi()` ile soruluyor — türetilmiş, saklanmıyor.
- **Rakam olmayan değer NULL'a düşer, form reddedilmez** (`_dosya_no_sayi()`).
- **Göç çalışmamışsa alan INSERT/UPDATE'ten tümden çıkar**
  (`es_dosya_no_var()`) — `cycle_alanlari()`'nın koruması, yoksa göçü
  çalıştırmamış makinede **hasta açmak tümden bozulur** (tuzak #3).
- **Canlı uyarı yine `/hasta/kontrol`** — ikinci bir rota açma (v6.125'in
  kuralı). Üç hali var: spermi var / kayıtlı ama spermi yok / hiç kayıtlı
  değil.
- Hasta kartında **ayrı bir kart** ("Eşin dondurulmuş spermi"): kayıtlar
  başka bir `hasta` satırına ait, kendi kayıtlarıyla aynı kartta gösterilmez.

**Dondurulmuş spermi tedaviye bağlama iki ekranda, mantık tek yerde**
(v6.139): `sperm_tedaviye_bagla()` / `sperm_baglanti_kaldir()`. Androloji
ekranı (v6.86, arayarak bulur) ve hasta kartı (kayıt zaten gözün önünde)
ikisi de bunları çağırıyor — iki kopya olsaydı biri `tasiyici.durum`'u
güncellemeyi unuturdu. Üçüncü bir yerde bağlama yazarsan bu ikisini çağır.
- **Hasta kartındaki seçici yalnızca BU hastanın tedavilerini gösterir**;
  başka bir hastanın tedavisine bağlamak yanlış hasta riski taşır, o iş
  androloji ekranının arama akışında kaldı.
- **Yalnızca androloji aşaması olan tipler seçilebilir**
  (`"androloji" in TIP_ASAMALARI[...]`) — FET'e bağlanan sperm hiçbir ekranda
  görünmezdi. Tip adını elle yazma, `TIP_ASAMALARI`'na bak.

**Yalnızca sperm dondurma amacıyla açılmış hasta Tüm Hastalar'da
görünmez, aranınca görünür** (v6.98, kullanıcının isteği). Ölçü **türetilmiş**
— `_sadece_sperm_kosulu()` (`app.py`): hiç `cycle`'ı olmayan ve en az bir
iptal edilmemiş `sperm_dondurma` kaydı olan hasta. Ayrı bir işaret
(`hasta.tur` gibi bir kolon) tutulmuyor — v6.38'deki "istatistikler
türetilmiştir" gerekçesinin aynısı: sonradan bu hastanın kendi cycle'ı
açılırsa (nadir ama mümkün) koşul kendiliğinden düşer, elle bir şey
güncellemeye gerek kalmaz.
- **Mevcut bir IVF hastasına sperm dondurma eklenebilmesi bilerek
  kaldırılmadı** (örn. eşinden alınan sperm, `/hasta/{id}/sperm-dondurma/
  yeni`) — o hastanın zaten kendi cycle'ı olduğu için koşul hiç
  tutmuyor, Tüm Hastalar'dan düşmüyor. Bu davranışı bozma.
- **`/hastalar`'ın Tüm Hastalar listesinden** (hem sayım hem satırlar)
  çıkarılıyor — `hastalar()` rotasında `NOT ({_sadece_sperm_kosulu()})`.
  **Arama sonuçlarından ve `/hasta/{id}` sayfasından çıkarılmadı**: arama
  hedefli bir sorgu (personel belirli birini arıyor), onu gizlemek erişimi
  kısıtlardı. Onun yerine oralarda `sperm_hastasi` bayrağıyla "Sperm
  Dondurma" rozeti basılıyor (`.rozet`, `hastalar.html` + `hasta_detay.html`)
  — böylece karışmıyor ama bulunabiliyor.
- **Ay listesi zaten etkilenmiyor**: `cycle_listesi()` `cycle` tablosundan
  okuyor, sperm dondurma hiç `cycle` satırı açmıyor (yeni bir cycle tipi
  değil). Ekstra bir süzgece gerek yok, koşulsuz doğru.
- Yeni bir "bütün hastalar" sorgusu yazarsan (istatistik, döküm, arama
  dışı bir liste) aynı soruyu sor: bu ekran IVF tedavi hastalarını mı
  sayıyor, yoksa gerçekten her hastayı mı? İlkiyse `_sadece_sperm_kosulu()`
  ile aynı süzgeci uygula.

**Sperm dondurmanın kendi "İşlemi Yapan"ı ve "Onamlar" eki var** (v6.101,
kullanıcının isteği). İkisi de sperm dondurmanın **cycle'ı olmayabileceği**
gerçeğinden (v6.85) dolayı mevcut mekanizmaları doğrudan kullanamıyor,
paralel ama ayrı birer yol açıldı.
- **İşlemi Yapan**: aşama ekranlarındaki kutunun (v6.99) aynı deseni —
  şifresi olan personelden seçiliyor, varsayılan giriş yapan kişi — ama
  `islem_yapan` tablosu `cycle_id` istediği için kullanılamadı. Doğrudan
  `sperm_dondurma.yapan_ad` kolonuna yazılıyor, `sperm_dondurma_detay.html`
  içinde kendi küçük kutusu var (`_islem_yapan.html` makrosu **değil** —
  o makro cycle_id/asama'ya kilitli). `personel_listesi()`/
  `guncel_kullanici_ad()` global'ları zaten genel amaçlıydı, değişmedi.
- **Onamlar**: PDF/fotoğraf eki, Doktor Notu'nun (v6.81) aynı ihtiyacı ama
  `goruntu` tablosu kullanılamadı — `goruntu.cycle_id` **NOT NULL**, sperm
  dondurmanın cycle'ı olmayan bir hastada (onkoloji öncesi gibi) hiç
  yazılamazdı. Yeni tablo **`sperm_dondurma_dosya`** (`goc_038`) —
  `goruntu`'nun küçük bir kopyası, `cycle_id` yerine `sperm_dondurma_id`.
  `id` **`AUTOINCREMENT`** (tuzak #13 — `/sperm-onam/{id}` adrese yazılıyor).
  Yazma/silme `goruntuler.sperm_onam_ekle()`/`sperm_onam_sil()`,
  `elle_ekle()`/`goruntu_sil()`'in aynısı ama ayrı klasör fonksiyonuyla
  (`sperm_onam_klasoru()` — `hedef_klasor()` cycle_id istiyor, kullanılamadı):
  `arsiv/<dosya no>/sperm-dondurma/<sperm_dondurma_id>/`.
  - **PDF hâlâ yeni sekmede açılıyor** — belge eki, tarayıcının kendi PDF
    görüntüleyicisi zaten neredeyse tam ekran, Doktor Notu'nun PDF'i için
    kullanılan gerekçenin aynısı. **Fotoğraf artık değil** (v6.118,
    kullanıcının isteği: "dosya yükleme yapılan bölümde görüntüyü açtıktan
    sonra kapatma butonu olsun") — v6.101'de fotoğraf da PDF gibi yeni
    sekmede açılıyordu çünkü paylaşılan `_buyutec.html` lightbox'ının JS'i
    `/dosya/` adresine sabitti (`img.src = '/dosya/' + id`) ve
    `sperm_dondurma_dosya` ayrı bir tablo/rotaydı (`/sperm-onam/{id}`) —
    yeni sekmede açılan ham görüntü bir HTML sayfası olmadığı için içine
    bir "Kapat" düğmesi konamıyordu. v6.118'de `_buyutec.html`'in
    `buyutecAc()`'i dördüncü, isteğe bağlı bir `onEki` parametresi aldı
    (varsayılan `/dosya/`) — `sperm_dondurma_detay.html` artık onu
    `onEki="/sperm-onam/"` ile çağırıyor, fotoğraf Doktor Notu'yla aynı
    lightbox'ta (kapatma düğmesi dahil) açılıyor. **Yeni bir `/dosya/`
    dışı görüntü kaynağı** (üçüncü bir tablo/rota) eklersen aynı deseni
    kullan — `_buyutec.html`'e dokunmadan yalnızca `buyutecAc(idler, no,
    baslangic, "/kendi-onekin/")` çağır, her ekran kendi tıklama betiğini
    yazsın (paylaşılan bir global yok, bu kural değişmedi).
  - **Tuzak #4'ün aynısı**: `hasta_sil()`'in kalıcı silme dalı zaten
    `sperm_dondurma`'yı hastaya göre siliyordu (v6.85); bu göç test
    edilirken **gerçekten patladı** — `sperm_dondurma_dosya` FK'sı
    yüzünden `DELETE FROM sperm_dondurma` FOREIGN KEY hatası verdi. Önce
    o hastanın sperm dondurma kayıtlarının onam eklerini silmek gerekiyor.
    `teshis_silme.py`'ye de aynı tarama + adım eklendi — o araç hastanın
    kendi `sperm_dondurma` kayıtlarını hiç simüle etmiyordu (yalnızca
    `kullanim_cycle_id` bağlarını kontrol ediyordu), bu eksik de kapatıldı.
    Yeni bir `sperm_dondurma_id`-referanslı tablo eklersen üçünü de
    (`hasta_sil()`, `teshis_silme.py`, ileride bir `sperm_dondurma_sil()`
    kalıcı silme yolu açılırsa onu da) güncelle.
  - `disari.TUM_TABLOLAR`'a eklendi (`goruntu` gibi — `lab_formu` gibi
    büyük blob içermiyor, dökümden çıkarılmasına gerek yok).

---

## İki makine

Kullanıcı aynı programı Mac'te (evde) ve Windows mini PC'de (klinikte)
çalıştırıyor.

`yerel_ayar.json` **makine adına göre bölümlenmiştir** (`platform.node()`).
Her bilgisayarın kendi bölümü, tek dosyada. Varsayılan yollar proje klasörüne
göreli (`snapshot/`, `arsiv/`), otomatik oluşturulur. Kayıtlı bir yol bu
makinede yoksa sessizce varsayılana döner.

**`.gitignore` bunları depo dışında tutar** (v6.1'de eklendi): `lab.db` (+
`-journal/-wal/-shm`), `arsiv/`, `snapshot/`, `yedek/`, `yedek.log`,
`yerel_ayar.json`. Hepsi veri veya makineye özel — git'e girmez, USB ile taşınır.

**Kural:** aynı anda tek kopyaya kayıt gir. Birleştirme mümkün değil.

**Veri USB ile taşınır: `tasi.py`** (v6.16). `lab.db` tek dosya; "sadece yeni
kayıtları" ayırmak mümkün değil, taşınan dosyanın tamamı ve karşıdakinin üzerine
yazıyor. Bu yüzden araç kopyalamadan **önce iki tarafı karşılaştırıyor**: hedef
daha yeniyse durup açık onay istiyor ve üzerine yazmadan önce
`lab_ONCEKI_<tarih>.db` yedeği bırakıyor. "Daha yeni" ölçüsü `olusturma_zamani`
kolonları — klinik zamanları (`opu_zamani` gibi) elle geri tarihlenebildiği için
onlara bakılmaz.

**Veritabanı kopyalarken SQLite backup API kullan**, düz dosya kopyası değil.
WAL modunda yeni kayıtlar `lab.db-wal`'da olabilir; uygulama çalışırken
`lab.db`'yi kopyalamak **bomboş bir dosya** verir ("no such table"). Test
edildi. `yedek.py` ve `tasi.py` ikisi de backup API kullanıyor.

---

## Bilinen tuzaklar

Bunlar gerçekten başa geldi, tekrarlanmasın:

1. **Toplu metin değiştirme yapma.** `taraf` değişkeni eklenirken aynı kalıp
   başka bir rotada da eşleşti ve denüdasyon zamanı kaydı bozuldu. `app.py`
   içinde aynı kalıp defalarca geçiyor — hedefi daralt, değişiklikten sonra
   uygulamayı çalıştır.

2. **Import'ları koşullu dalların içine bırakma.** `_d` importu boş bir if
   dalının altında kaldı, boş cycle'da ICSI ekranı 500 verdi.

3. **Göç yazdıysan kullanıcının çalıştırdığını varsayma.** Gün 4/6/7 eksik
   görünmesinin sebebi göçün çalıştırılmamasıydı. Ekranlarda göç uyarısı var,
   yeni göçlerde de aynısını ekle.

4. **`kaynak_dosya.cycle_id` silme kaskadını kırar.** Denüdasyonda "Atla"
   denen kareler cycle'a bağlı satır bırakıyor. Yeni bir tabloya `cycle_id`
   eklersen kalıcı silme adımlarına da ekle, yoksa FOREIGN KEY hatası.
   Aynısını `teshis_silme.py`'ye de ekle — `islem_yapan` (v6.3) oraya
   eklenmediği için araç silinebilir bir hastayı aylarca yanlış raporladı.

5. **Şablon değişikliği sessizce tutmayabilir.** Değiştirdiğin ekranı tarayıcıda
   gerçekten aç.
   - **Kardeşi (v6.138'de başa geldi): şablon diskten tazeleniyor, Python
     tazelenmiyor.** Jinja `auto_reload` açık, yani `templates/` her istekte
     yeniden okunuyor; `app.py` yalnızca açılışta. Kullanıcı `git pull` yapıp
     programı yeniden başlatmazsa **yeni şablon + eski rota** çalışır: rotanın
     vermediği context değişkeni Jinja'da `Undefined` olur, `{% if %}` sessizce
     yanlış döner. Sonuç "hata yok ama çalışmıyor" — v6.138'de arama kutusu
     göründü, Enter'a basınca hiçbir şey olmadı. Kullanıcı "çalışmıyor" derse
     **ilk sorulacak şey bu**; ölçmenin yolu eski commit'i yeni şablonlarla
     çalıştırmak (bire bir yeniden üretildi). Test ederken de kendi sunucunu
     yeniden başlat — yoksa aynı tuzağa sen düşersin.
   - **Ölçmek artık kolay** (v6.162): Yönetici panelinin "Program sürümü"
     kartı çalışan sürümü (`app.CALISAN_SURUM`, açılışta README'nin en
     büyük "# v6.xxx" başlığı) ve diskteki farklıysa "yeniden başlatılmadı"
     uyarısını gösteriyor. Kullanıcı "hâlâ eskisi gibi" derse önce oraya
     baktır; sürüm yeni sürüm bölümü README'ye eklenince kendiliğinden artar.

6. **Serbest metin bir kolonu sabit bir listeyle eşleştirirken dikkat.**
   `kullanici.rol` serbest metin; `androlog` diye elle yazılmış bir rol vardı.
   Rol seçicisi yalnızca `yonetici`/`embriyolog` gösterdiği için tarayıcı ilk
   seçeneği seçili sanıyor ve "Rolü değiştir" tek tıkla o kişiyi **yönetici**
   yapıyordu. Bir `<select>`'i veritabanındaki değerle beslerken, değerin
   listede olmama ihtimalini hep düşün (v6.15).

7. **Es zamanli kullanici var.** Klinikte birkac telefon ayni anda kayit
   giriyor. Yeni bir "siradaki numara" mantigi yazarsan `db.yazma_islemi()`
   kullan, yoksa UNIQUE hatasi alan personelin girdigi kayit kaybolur
   (v6.6'da denudasyonda oosit numarasi tam olarak boyle patliyordu).

8. **Ayarı iki yerden okuma — `yedek.py` tam bunu yapıyordu (v6.8'de
   düzeltildi).** Kendi `ayar()` fonksiyonu `yerel_ayar.json`'ı düz sözlük
   sanıyordu; `db.py` dosyayı `{"makine-adi": {...}}` biçimine çevirince
   sessizce DB'deki Windows yoluna (`E:\yedek`) düşüyor, Mac'te cwd altında
   `E:\yedek` adında klasör açıp "Yedekleme tamam" diyordu — hatasız, çıkış
   kodu 0. Yeni bir script ayar okuyacaksa **kendi okuyucusunu yazma**,
   `import db; db.ayar(...)` kullan. Yol ayarları makineye özgüdür, tek kaynak
   `db.py` (README v6.8).

9. **`metin()` bulamadığı anahtarı olduğu gibi döndürür.** Bu bilinçli
   (eksik çeviri ekranda çıplak görünsün diye), ama adresten gelen bir
   değeri doğrudan `metin()`'e verirsen `?hata=...` ile ekrana istenen yazı
   yazdırılabilir. Dışarıdan gelen anahtarı **beyaz listeden geçir**
   (`DENUDASYON_HATALARI` gibi).

10. **Şablonun altındaki betik, o şablonun formu basılmadığında da
    çalışır.** Form `{% if %}` içindeyse betiğin aradığı alanlar yok;
    `getElementById(...)` null döner, `addEventListener` patlar ve **aynı
    sayfadaki öteki betikler de çalışmaz**. Betiğin başına
    `if (!document.getElementById('<form id>')) return;` koy. Bu gerçekten
    oldu: cycle'da hiç oosit yokken ICSI ekranının bütün JS'i sessizce
    ölüydü (v6.20'de görüldü).

11. **`el.hidden = true` bizim CSS'imizde çalışmayabilir.** Tarayıcının
    `[hidden] { display: none }` kuralı zayıf; `display: flex`/`block`
    veren bir sınıf onu eziyor ve eleman gizlenmiyor. v6.30'da CSS'in
    tepesine `[hidden] { display: none !important; }` konuldu, artık her
    yerde çalışıyor. Aynı sorunun yedi ayrı yaması (`.bilgikart[hidden]`,
    `.uyari[hidden]`, ...) hâlâ duruyor — gereksizler, zararsızlar.

12. **`<button>`'a bileşen sınıfı verirken `appearance: none` yaz.**
    `.sec` bileşeni `<label>` + gizli radyo için yazılmış; denüdasyondaki over
    seçimi ise `<button class="sec">` (bilerek — tek alan için ayrı "Kaydet"
    olmasın diye kendi başına gönderiyor). Sınıf aynı olunca tarayıcının kendi
    düğme biçimi devrede kaldı: beyaz kutunun etrafında ikinci bir gri çerçeve,
    farklı yazı rengi, 6px farklı ölçü. Daha kötüsü, **iOS Safari
    `appearance: auto` olan bir `<button>` içindeki `display: flex` çocuğun
    yazısını basmıyor** — düğmeler telefonda seçilmeden önce bomboş görünüyordu,
    seçilince (vurgulu zemin) okunuyordu. Masaüstü Chromium basıyor, o yüzden
    aylarca fark edilmedi. v6.56'da `.secenek button.sec` ve `.onum` sıfırlandı.
    Yeni bir yerde `<button>`'a görsel bir bileşen sınıfı verirsen aynısını
    yap ve **telefonda aç** (tuzak #5'in mobil hali).

13. **Kimliği URL'e yazılan bir tabloda `INTEGER PRIMARY KEY` yeter değil,
    `AUTOINCREMENT` de gerekir.** `goruntu.id` `AUTOINCREMENT`'sizdi; SQLite
    kuralı "yeni id = mevcut en büyük id + 1" olduğu için tablodaki en büyük
    id'ye sahip satır silinince o numara boşa çıkıyor ve bir sonraki INSERT
    onu yeniden veriyor. `/dosya/{id}` id'yi doğrudan adrese yazdığı için
    tarayıcı o adresi daha önce gördüyse önbellekten **eski, silinmiş
    fotoğrafı** gösterebiliyor — "yüklediğim resim dışında başka bir resim
    yükleniyor" (v6.92, goc_035) tam olarak buydu, en çok son eklenen
    fotoğrafın silinip yenisiyle değiştirildiği anda (2./3. oosit gibi)
    ortaya çıkıyordu. `AUTOINCREMENT` SQLite'a ayrı bir sayaç
    (`sqlite_sequence`) tutturur, silinen bir id bir daha asla verilmez.
    Yeni bir tablo açarken kimliği dışarı sızan (URL, dosya adı, bir
    kullanıcıya gösterilen referans numarası) bir `id INTEGER PRIMARY KEY`
    kolonu varsa `AUTOINCREMENT` ekle.

14. **Görsel olarak gizlenmiş bir form alanı hâlâ YER KAPLAR — genişliğini
    kendi kuralında sabitle** (v6.140). `.secenek .sec input` (Kız/Erkek gibi
    düğmelerin arkasındaki radyo) `position: absolute; opacity: 0` ile
    gizleniyor, `display: none` ile **değil** (klavye ve form gönderimi
    çalışsın diye — bilinçli). Gebelik ekranında "Bebekler" formu
    `class="alan"` taşıdığı için `.alan input { width: 100% }` bu radyoya da
    uyuyordu; `position: absolute` ve üzerinde konumlandırılmış bir ata
    olmadığı için "%100" **ekranın tamamı** demekti (1280px'lik masaüstünde
    radyo 1280px). Üçü yan yana sayfayı 2023px'e uzatıyor, sağında bomboş bir
    alanla yatay kaydırma çıkıyordu. **Hiçbir şey kesik görünmediği için
    aylarca fark edilmedi** — kullanıcı da "nasıl bir sorun anlamadım" dedi,
    ekran görüntüsüyle gösterildi.
    - Düzeltme **bileşenin kendi kuralında**: `width: auto; min-width: 0`.
      Şablondaki `class="alan"`'ı kaldırmak da çalışırdı ama yalnızca o
      ekranı kurtarırdı — bileşen başka bir gün başka bir `.alan`'ın içine
      konduğunda sorun sessizce geri gelirdi.
    - Yeni bir "gizli ama yer kaplayan" alan yazarsan ölçüsünü orada
      sabitle, kabın genel kuralına güvenme.
    - Ölçerken **yalnızca `scrollWidth > clientWidth`e bakmak yetti** ama
      sebebi bulmak için taşan ögeyi tek tek aramak gerekti
      (`getBoundingClientRect().right > clientWidth`) — v6.109'un dersinin
      tersi yönü: orada dış kabın ölçüsü doğru çıkıp içerik kayıyordu,
      burada içerik doğru görünüp görünmez bir öge sayfayı uzatıyor.

15. **Şema cevabını kendi değişkeninde saklama — geri yükleme onu
    yalanlar** (v6.144'te bulundu, v6.145'te düzeltildi). Çalışan programın
    altındaki veritabanını `/yedekleme/geri-yukle` eski bir yedekle
    değiştiriyor. v6.145'e kadar göçler yalnızca açılışta çalışıyordu ve
    `db.kolon_var()`, `thaw_cycle_var()`, `opu_hekim_var()` gibi kontroller
    ilk cevabı saklıyordu. Saklanmış "var" cevabı kolonu olmayan geri
    yüklenmiş veritabanında sorguyu "no such column" ile patlatıyordu;
    denendi: v6.143 öncesi bir yedekte FET'in vitrifikasyon ekranı program
    yeniden açılana kadar 500 veriyordu.
    - **Bugün:** `geri_yukle.geri_yukle()` takastan hemen sonra göçleri
      çalıştırıyor (`_gocleri_uygula()`, açılıştaki `goc.calistir()`'ın
      aynısı). Ekrandan geri yüklemede `veritabani_yenilendi()` saklanmış
      cevapları unutturuyor ve Yönetici panelinin göç kartını güncelliyor.
    - **Kural:** şema cevabı saklayacaksan `db.kolon_var()`/`db.tablo_var()`
      kullan. İkisi tek yerde saklıyor, `db.sema_bilgisini_unut()` hepsini
      unutturuyor. Kendi `_..._KOLONU` değişkenini açarsan
      `veritabani_yenilendi()`'ye de ekle (tazelemenin tablo listesi
      `_DEGISIM_TABLOLARI` orada), yoksa bu hata geri gelir.
    - Çekirdek bir akışın (tedavi açma gibi) INSERT/UPDATE'ine giren yeni
      kolonu her seferinde sormak daha da sağlam
      (`_planlanan_kolonu_var()`, `_elle_no_kolonu_var()`) — PRAGMA ucuz.

---

## Bekleyen işler

1. **Biyopsi / PGT modülü** — tek kalan ana modül. Biyopsi kaydı, tüp etiketi,
   haftalar sonra gelen genetik sonucun eşleştirilmesi. `pgt_sonuc` tablosu
   şemada hazır, kullanılmıyor.
2. **Yedekleme — kısmen kuruldu, hedef ayarı v6.8'de düzeltildi, elle
   tetikleme v6.119'da, geri yükleme v6.120'de eklendi.**
   - `yedek.py` artık `db.ayar()` kullanıyor; argümansız çalıştırma bu makinenin
     `yerel_ayar.json` bölümündeki `yedek_klasor`'e gider. Komut satırı argümanı
     hep kazanır. Platforma uymayan yol (Mac'te `E:\yedek`) reddedilir.
   - **Windows mini PC'de `yedek_klasor` `E:\yedek` yapılmalı** — v6.41'den
     beri ekrandan da olur (`/yonetim` → Klasörler), `python yerel_kur.py` de
     çalışıyor. Yol ayarları artık makineye özgü
     dosyadan okunuyor, DB'deki `goc_008` değeri hedefi belirlemiyor. Yapılmazsa
     o makinede varsayılan `D:\lab_yedek` olur.
   - **Mac'te otomatik zamanlama YOK.** `yedek.bat` sadece Windows Görev
     Zamanlayıcı için. İstenirse `launchd` görevi kurulacak.
   - **Asıl iş klinikteki Windows mini PC'de:** gerçek hasta verisi orada.
     Görev Zamanlayıcı + farklı disk hedefi orada kurulmalı (README v1.2).
     `~/lab_yedek` aynı diskte — bu Mac test verisi için geçici çözüm.
   - **`/yedekleme` ekranında "Şimdi yedekle" düğmesi var** (v6.119,
     kullanıcının isteği: "Elle yedekleme olsun"; ekran v6.121'de
     `/klasorler`'den ayrıldı, aşağıya bak) — otomatik zamanlamanın
     **yerine geçmiyor**, tamamlayıcısı: "hemen bir yedek almam lazım"
     anları için. `app.py` `yedekleme_yedekle_simdi()` `yedek.py`'nin
     fonksiyonlarını (`veritabani_yedekle()`/`eskileri_temizle()`/
     `arsiv_yedekle()`) **süreç içinde** çağırıyor, `goc.py`'nin göçleri
     çalıştırma deseninin aynısı — `subprocess.run([sys.executable, ...])`
     **yazılmadı**, paketlenmiş uygulamada bu satır yedeği değil programı
     yeniden başlatırdı (göçler için söylenen tuzağın aynısı, burada da
     geçerli). `yedek.main()` de çağrılmadı — `sys.exit()` kullanıyor, bir
     istek işleyicisinin içinde istenmeyen bir şey; `main()`'in çağırdığı
     fonksiyonlar elle, `try/except` ile çağrılıyor. Düğme `/yedekleme`'de
     duruyor, `/yonetim`'de **değil** — o hâlâ salt okunur (v6.12'nin
     kuralı hiç değişmedi), yalnızca sonucu (`yedek_durumu()`) gösteriyor
     ve `/yedekleme`'ye bağlantı veriyor. Yeni bir "elle tetiklenen arka
     plan işi" (goc/yedek dışında) eklersen aynı üç şeyi sor: süreç içinde
     mi çalışıyor (subprocess değil), hangi ekranda duruyor (`/yonetim`
     değilse neresi), ve `main()`'in `sys.exit()`'ini mi yoksa alt
     fonksiyonlarını mı çağırman gerekiyor.
   - **Yedekten geri yükleme** (v6.120, kullanıcının isteği: "Yönetici
     isterse yedekten geri çağırsın... her şey tekrar yerleşsin. Yönetici
     panelinden hepsini yapabilsin") — `/yedekleme/geri-yukle`, yeni
     `geri_yukle.py`. Bkz. aşağıdaki "Yedekten geri yükleme" bölümü
     (Değişmeyen kurallar) — bu, uygulamadaki en yıkıcı işlem, kendi
     kuralları var.
   - **Yedekleme kendi ekranına taşındı** (v6.121, kullanıcının isteği:
     "Yedekleme bölümünde Yedekleme olsun. Klasörlerin altında zor
     bulunuyor."). `/klasorler/yedekle-simdi` → `/yedekleme/yedekle-simdi`,
     `/klasorler/geri-yukle` → `/yedekleme/geri-yukle` (GET+POST) —
     mantık değişmedi, yalnızca adresler ve `/yonetim`'e doğrudan bir
     "Yedekleme" düğmesi eklendi (Kullanıcılar/Klasörler ile aynı
     seviyede). `/klasorler`'de yedek klasörünün **yolu** hâlâ ayarlanıyor
     (o bir klasör ayarı) — yalnızca eylemler taşındı. Yeni bir "ayar
     ekranının alt kartı" yazarken kendine sor: bu bir **eylem** mi
     (şimdi çalıştır, geri al, sil gibi düğmeler) yoksa bir **ayar** mı
     (yol, seçenek, açık/kapalı)? Eylemse kendi menü öğesi olmayı hak
     eder — kullanıcı burada tam bunu söyledi, bir ayar ekranının
     içindeki eylemi bulamadı.
3. **HTTPS yok** — iç ağ dışına açılmamalı.
4. **Kullanıcı yönetimi — v6.11'de arayüze taşındı, v6.12'de panele bağlandı.**
   Yönetici `/yonetim` panelinden `/kullanicilar`'a girer; ekler, şifre sıfırlar,
   pasif yapar, siler. Şifre değiştirme `/sifre` — giriş ekranından da açılır.
   `kullanici.py` terminal aracı duruyor: yönetici de kilitlenirse tek çıkış o.
   Rol sonradan değiştirilebiliyor (v6.13): ekrandan ya da
   `python3 kullanici.py rol <kullanici> yonetici`. **Son aktif yöneticinin rolü
   düşürülemez** — her iki yolda da engelleniyor.
5. **Cleavage skor kuralı bir varsayım.** `cleavage_skor` fonksiyonu üç boyutu
   ayrı puanlayıp en kötüsünü alıyor. Kullanıcının kendi kuralı netleşince
   değişecek — ona sor. **Elle giriş tarafı v6.122'de çözüldü** (kapalı
   G1-G4 seçimi, yukarıdaki "Otomatik skorlar kaynak işaretler" bölümüne
   bak) — bu madde yalnızca **otomatik** A/B/C hesabının kuralı için hâlâ
   açık, kullanıcı ona ayrıca bir şey söylemedi.
6. ~~**Bozuk tarih**~~ — **kapandı.** v6.51'de koruma ve araç yazıldı,
   v6.53'te denetim genişletildi (okunamayan biçimler + üst sınır).
   Kullanıcı 2026-09-12'de kendi veritabanında `tarih_duzelt.py`'yi
   çalıştırdı: **düzeltilecek kayıt bulunamadı**, `0026-09-04` artık yok.
7. **`sema_guncel.sql` güncel değil.** `goc_019`, `goc_021`, `goc_022` ve
   `goc_025`'in getirdiklerini içermiyor. v6.9'da `sifirdan_kur.py` göçleri
   kendisi çalıştırdığı için kurulum artık eksiksiz çıkıyor, ama dosyanın adı
   yalan söylüyor. Mevcut şemadan yeniden üretilmeli.

8. **Dil seçimi — karar verildi, henüz yazılmadı.** Amaç evrensel bir
   program: önce Türkçe (Türkiye'de rahat kullanılsın), sonra İngilizce + dil
   seçimi. Kullanıcının kararı (2026-09-10):
   - **Dil lab başına tektir, kullanıcı başına değil.** Yönetici bir kez seçer,
     bütün program o dile geçer. Aynı labda iki personel farklı dil görmez.
   - Değer `ayarlar` tablosunda, `db.ayar("dil", "tr")` ile okunur — lab_id'ye
     bağlı, yeni tablo gerekmez.
   - **Giriş yapılmadan da okunabilmeli:** giriş ekranının kendisi de çevrilecek,
     yani dil `ACIK_YOLLAR` üzerinde de geçerli olmalı.
   - **Değiştirmek yönetici işi** — `yonetici_kontrol(request)` ile korunmalı.
     Giriş ekranına açık bir dil seçici koyma: giriş yapmamış herkes labın
     dilini değiştirebilirdi. `/yonetim` salt okunur olduğu için değiştirme
     kendi ekranında olur, panelden yalnızca bağlantı verilir.
   - Klinik terimler iki dilde de İngilizce kalır (blastocyst, ICSI, PN, ICM,
     TE, FET) — çevrilen sadece arayüz metinleri.
   - **Durum (2026-09-10): yarım.** `metinler.py` ve `/dil` ekranı çalışıyor,
     42 şablon çevrildi. Kalan: `arsiv_sil`, `cycle_sil`, `esle`, `hasta_sil`,
     `kullanici_sil`, `kullanicilar`, `thaw_sil`, `transfer_sil` şablonları ve
     `app.py`'deki ~132 Türkçe metin (sunucu hata mesajları, `MODULLER`
     etiketleri). Kullanıcı çeviriyi **askıya aldı**, sonra dönülecek.
   - **Yeni ekran yazarken metni doğrudan şablona yazma**, `metinler.py`'ye
     anahtar ekle ve `metin("...")` kullan — yoksa İngilizce kurulumda o ekran
     Türkçe kalır.
   - **Excel çıktısının sütun başlıkları da çevrilmedi** (v6.36): `disari.py`
     içindeki ~90 başlık ve sayfa adı doğrudan yazılı. Hücre değerleri iki
     dilde doğru çıkıyor, başlıklar çıkmıyor. Bunların İngilizcesi klinik bir
     sözlük — kullanıcıyla birlikte yazılmalı, uydurulmamalı. Aynı yerde
     `specimen.durum` etiketleri de eksik (yukarı bak).

`goc_018.py` (endikasyon kopyalarını birleştirir) 2026-09-08'de bu makinede
çalıştırıldı: `erkek faktoru` ve `tubal faktor` serbest metinleri resmi
kodlara birleştirildi, endikasyon listesi 19 → 17 satır. Hiçbir cycle etkilenmedi.

---

## Nasıl çalışılsın

- Değişiklikten sonra uygulamayı **çalıştır** ve ilgili ekranı aç.
- Şema değişikliği gerekiyorsa **yeni bir `goc_0XX.py` yaz**, mevcut göçü
  değiştirme — kullanıcının veritabanında eskiler zaten çalışmış olabilir.
  Göçler idempotent olmalı.
- Yeni bir sürüm bitince `README.md`'ye o sürümün bölümünü ekle: ne değişti ve
  **neden**. Bu dosya projenin hafızası.
- Klinik bir varsayım yapman gerekiyorsa yapma — kullanıcıya sor. O embriyolog.

## Git: tek ortak hat `main` (birden çok Claude hesabı)

Kullanıcı projeyi **birden çok Claude hesabından/oturumundan** ilerletiyor.
2026-09-23'te bir hesabın işi (v6.123–v6.148, 31 commit) ayrı bir
`claude/...` dalında kaldı, `main`'e hiç girmedi; öteki hesap `main`'de
v6.122'deydi ve yeni iş eklese iki hat birbirinden ayrılacaktı. O gün
`main` o dala ileri sarıldı (fast-forward, hiçbir commit kaybolmadı).
Tekrarlanmasın diye kural — **her hesap, her oturum** için geçerli:

1. **Ortak hat `main`.** Klinikteki makine ve Mac `git pull origin main`
   ile güncelleniyor (`KOMUTLAR.md`); `main`'e girmeyen iş kullanıcının
   programına hiç ulaşmaz.
2. **Oturumun başında, bir şey değiştirmeden önce:** `git fetch origin`,
   sonra `git branch -r` ile uzak dalların hepsine bak ve
   `git log --oneline main..origin/<dal>` ile `main`'de olmayan commit var
   mı kontrol et. Varsa bu, başka bir hesabın işi — **önce onu `main`'e
   al** (`git merge --ff-only origin/<dal>`; ileri sarma olmuyorsa normal
   `git merge`, çakışmayı çöz), `main`'i push et, sonra kendi işine başla.
   README'nin son sürüm numarasına da bak: yeni sürüm numarası ondan devam
   eder, iki hesap aynı numarayı vermesin.
3. **Oturuma ayrı bir `claude/...` dalı atanmışsa:** o dalı güncel
   `main`'den başlat, işi orada yap, iş bitince **hem o dala hem `main`'e**
   push et (`git push origin HEAD:main` — `main` o dalın gerisindeyse bu bir
   ileri sarmadır). Dalı `main`'in önünde bırakıp oturumu kapatma.
4. **Asla:** `--force` push, `main` üzerinde rebase/amend, bir başkasının
   dalını silmek. Dallar birleştirmeden sonra da dursun; silmek kullanıcının
   kararı.
5. `git push` "rejected / non-fast-forward" derse öteki hesap bu arada push
   etmiş demektir: `git pull origin main` (birleştir), programı çalıştırıp
   dene, sonra tekrar push.
