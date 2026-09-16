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

**Durum:** çalışır halde, gerçek hasta verisi henüz girilmedi.

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

**Göçler açılışta kendiliğinden çalışır** (v6.49). Elle bir şey yapmak
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
  goc_002..033.py   veritabanı göçleri (sırayla)
  baslat.py         programı başlatır — paketlenmiş uygulamanın giriş noktası
  paket/pdc.spec    PyInstaller tarifi; pdc_kurulum.iss Windows kurulumu
  goc.py            bekleyen göçleri bulur ve çalıştırır (süreç içinde)
  goc_hepsi.py      aynı çalıştırıcının terminal yüzü
  teshis.py         genel sorun teşhisi
  tarih_duzelt.py   yılı bozuk tarihleri bulur, sorarak düzeltir
  teshis_silme.py   bir hasta neden silinemiyor — hiçbir şey silmez
  liste_duzenle.py  seçim listelerini görüntüle / temizle
  kullanici.py      kullanıcı listesi / şifre sıfırlama / yeni kullanıcı
  tasi.py           iki makine arasında USB ile veri taşıma
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
- `ivf_icsi` → 11 aşamanın hepsi (OPU ve androloji dahil)
- `fet` → çözme, transfer, gebelik (**OPU yok** — oosit toplanmaz, embriyo
  başka bir cycle'dan gelir, aynı gün transfer edilir)
- `fet_kultur` → çözme, **blastokist**, transfer, gebelik (v6.62, `goc_031`).
  "FET (3→5 kültür)" — gün 2/3 embriyosu çözülüp gün 5'e kadar kültürlenip
  öyle transfer ediliyor; `fet`'ten farkı yalnızca araya giren blastokist
  değerlendirmesi. **Sıra `ivf_icsi`'nin tersi**: orada blastokist
  dondurmadan (vitrifikasyon) önce gelir, burada çözme blastokistten önce
  gelir — embriyo zaten dondurulmuş halde geliyor.
- `oosit_cryo` → OPU, denüdasyon, vitrifikasyon, çözme

Aşama sırası ve tip-aşama eşlemesi `app.py` içinde `ASAMA_SIRASI` ve
`TIP_ASAMALARI`. Androloji (`sperm_ornek` + iki `sperm_analiz`: bazal /
hazırlık sonrası) yalnızca `ivf_icsi`'de. Şema/listeler: README v6.2, `goc_019`.

**`fet` ve `fet_kultur`'da embriyo BU cycle'dan gelmez** — `FET_TIPLERI`
sabiti ve Jinja global `fet_tipi_mi(cycle_tipi)` bunu tek yerden kontrol
ediyor (v6.62). Taşıyıcı/embriyo listeleri `specimen.cycle_id` ile değil,
`olay.thaw_cycle_id` ("hangi tedavi için çözüldü") ile aranıyor —
`specimen.cycle_id` embriyonun **ilk** (OPU/ICSI) cycle'ı, hiç değişmez
(README v6.7). Yeni bir `FET_TIPLERI` üyesi eklersen `cycle_thaw_listesi()`,
`_blast_kosul()` ve `cycle_thaw.html`'deki vitrifikasyon-bağlantısı koşulu
otomatik kapsar — `fet_tipi_mi()` kullanmayan yeni bir `== "fet"` kontrolü
yazma.

**Blastokist ekranında seçim `specimen.id` ile, `cycle_sira_no` ile DEĞİL**
(v6.62, yalnızca bu ekranda). `fet_kultur`'da birden çok cycle'ın embriyoları
aynı listede olabiliyor ve `cycle_sira_no` yalnızca **kendi** cycle'ı içinde
tekil (`UNIQUE(cycle_id, cycle_sira_no)`) — iki cycle'da da "1. embriyo"
olabilir. ICSI/fert/cleavage buna dokunmadı, onlar hiç birden fazla cycle'ın
embriyosunu aynı ekranda göstermiyor; oradaki `?oosit=<cycle_sira_no>`
deseni (README v6.35) hâlâ güvenli.

**`olay.cycle_id` her zaman specimen'in KENDİ cycle'ı, ekranın cycle'ı
değil** — `thaw` ve `transfer` olaylarının zaten yaptığı şey
(`e["cycle_id"]` / `sp["cycle_id"]`), `blastokist_degerlendirme` de artık
aynısını yapıyor. "Hangi tedavi için" sorusu ayrı bir alanda (`thaw_cycle_id`,
`tr_cycle_id`) yanıtlanıyor. Fotoğraf ekleme de aynı kuralı izliyor:
embriyonun **kendi** cycle'ının arşiv klasörüne gidiyor
(`/cycle/{{ sp.cycle_id }}/foto-ekle`, `thaw.html`'in zaten yaptığı gibi),
görüntülenen ekranın cycle'ına değil — iki klasöre bölünmüş bir embriyo
geçmişi olmasın diye.

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
**o aşamadaki adını** yazar -- ekranın başlığında ne yazıyorsa o: Oosit,
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
  bağımsız iki kart). Yalnızca genişleyen (`kap genis`, v6.65'ten beri
  `yanmenusuz` DEĞİL — menü artık orada da var): `/klasorler`, `/cryo`,
  `/hasta/{id}`, `/bitenler` — liste ekranlarını bölme, `_cyclesatir`
  satırları soldan sağa okunan tek bir akış.
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

**Kodu değil etiketi göster.** `mii`, `2pn`, `z1` gibi değerler
`liste_degeri`'nde ve laba özgü — yönetici düzenleyebiliyor. Ekranda
`liste_etiket(liste_adi, kod)` (Jinja global) kullan, sabit sözlük yazma.

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
- Transfer ve gebelik **tedavinin yapıldığı cycle'a** yazılır
  (`COALESCE(o.tr_cycle_id, s.cycle_id)`), ay listesindeki kuralın aynısı.
- "Son kayıtlar" on satır: kayıt defteri değil, "en son ne yapıldı"
  penceresi. Tam döküm `/disari/tumu`'da.

**Örnek kodu aranabilir** (v6.35). Kod (`527078-2026-0001-03`) tüpün ve
formun üstünde yazan şey; `<hasta dosya no>-<specimen.id>` olarak
birleştirilip aranıyor, yani tam kod da kuyruğu da (`0001-03`) buluyor.
İki yerde: `/hastalar` (sonuç kartı hasta satırlarının üstünde, satır
**cycle'a** gider) ve `/cryo?ara=`. İki kural:
- Arama **yalnızca tire içeren** metinde örnek arar — tiresiz metin kod
  değildir, yoksa "3" yazan bütün örnekleri listeler.
- Örnek araması **hastanın arşivlenmiş olmasına bakmaz**; dolaptaki bir
  örneğin dosyası kapanmış olabilir. (Hasta araması eskisi gibi süzer.)

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
- **Tüm Hastalar** (`durum='aktif'`, `ORDER BY ad_soyad`, sınırsız) aynı
  satır tasarımını kullanıyor, isme tıklamak `/hasta/{id}`'yi (aynı ekran)
  açıyor.
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

**Silme = iptal işaretleme.** Normal akışta fiziksel silme yok. Kalıcı silme
ayrı, bilinçli bir yol: dosya no yaz → `SIL` yaz → tarayıcı onayı.
**Transfer kaydı olan hasta/cycle kalıcı silinemez** — ekranda seçenek
görünmez, sunucu da reddeder. Bu kuralı gevşetme.

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

**Embriyo cycle değiştirmez; üç alan üç soruyu yanıtlar.**
`specimen.cycle_id` nereden geldiği (OPU/ICSI cycle'ı, değişmez),
`olay.thaw_cycle_id` hangi tedavi için çözüldüğü, `olay.tr_cycle_id` nerede
transfer edildiği. FET böyle bağlanır — embriyo kopyalanmaz, taşınmaz.
Transfere ulaşmayan çözme de FET'in kaydıdır, görünmesi gerekir (README v6.7).
Bu iki alan **başka bir cycle'a** işaret edebildiği için kalıcı silmede
`NULL`'a çekilmeleri şart (bkz. tuzak #4).

**Fotoğraf devralma yok.** Her aşama ekranı sadece kendi aşamasının karelerini
gösterir. (Eskiden devralıyordu, kafa karıştırdı, kaldırıldı — README v5.1.)

**Örnek kodu = `<hasta dosya no>-<cycle no>-<sıra>`** (`527078-2026-0001-03`).
`specimen.id` bunun son iki parçası ve **değişmez** — dört tablonun yabancı
anahtarı. Kodu `ornek_kodu()` üretir (Jinja global); dosya adlarında da bu
kullanılır, kaynak resmin adı asla kullanılmaz.

**Oosit → zigot → embriyo aynı örnektir, kod değişmez.** Soyağacı böyle
korunur ("bu blastokist hangi oositten çıktı"). Değişen sadece ekrandaki
isim: `ornek_adi(asama, cycle_tipi)` → Oosit / Zigot / Cleavage / Blastokist /
Embriyo (oosit cryo'da vitrifikasyon-çözme-transferde yine Oosit). Yeni bir
aşama ekranı yazarsan "Oosit" diye sabit yazma, bu fonksiyonu kullan.

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

**Otomatik skorlar kaynak işaretler.** Elle skor girilirse
`cl_skor_kaynagi='elle'` yazılır, otomatik hesap onu ezmez.

**"İşlemi yapan" her aşama ekranının altında.** Serbest metin, aşama başına tek
(`islem_yapan` tablosu, `UNIQUE(cycle_id, asama)`). Kaydı giren `kullanici_id`
ile karıştırma — biri "kim yaptı", diğeri "kim girdi". Paylaşılan parça
`_islem_yapan.html`; değer Jinja global `islem_yapan_ad()` ile okunur. Yeni bir
aşama eklersen `ASAMA_SIRASI`'na koy + şablonuna `{{ iy.kutu(c.id, "<asama>") }}`
ekle — gerisi otomatik (README v6.3). Makro isteğe bağlı `etiket`/`ipucu` alır;
varsayılanı değiştirme, sadece belirsizlik olan ekranda ver (v6.9).

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

**Embriyo Dondurma ve Sperm Dondurma aynı taşıyıcı/konum altyapısını
paylaşır, `tasiyici.kategori` ile ayrılır** (v6.84, `goc_033`). `/cryo`
ekranı artık kullanıcıya "Embriyo Dondurma" görünüyor (yalnızca
`metin("cryo_haritasi")`'nin görüntülenen metni — rota, tablo adları hâlâ
`cryo`/`tasiyici`, v6.79 deseni). Sperm Dondurma ayrı bir ekran
(`/sperm-dondurma`), kendi tablosu (`sperm_dondurma`: dondurma öncesi
semen analizi, `sperm_analiz` ile aynı kolon adları) ama **aynı** `tasiyici`/
`konum` tablolarını kullanıyor. `tasiyici.kategori` (`'embriyo'`/`'sperm'`)
ayırıyor — **Embriyo Dondurma'nın `tasiyici` sorgularına yeni bir yerden
dokunursan `t.kategori='embriyo'` süzgecini de ekle**, yoksa sperm
taşıyıcıları oraya sızar. `/disari/cryo` bu süzgece ihtiyaç duymuyor çünkü
zaten `olay.tip='vitrifikasyon'` üzerinden geliyor, sperm taşıyıcıları hiç
`olay` satırı üretmiyor.
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

---

## Bekleyen işler

1. **Biyopsi / PGT modülü** — tek kalan ana modül. Biyopsi kaydı, tüp etiketi,
   haftalar sonra gelen genetik sonucun eşleştirilmesi. `pgt_sonuc` tablosu
   şemada hazır, kullanılmıyor.
2. **Yedekleme — kısmen kuruldu, hedef ayarı v6.8'de düzeltildi.**
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
   değişecek — ona sor.
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
