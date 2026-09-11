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

Veritabanı göçleri: `python3 goc_hepsi.py` (idempotent, sırayla hepsini
çalıştırır). `goc_002.py` soru sorduğu için ayrıdır, elle çalıştırılır.
`sifirdan_kur.py` sonunda göçleri **kendisi** çalıştırır (v6.9) — yeni kurulumda
ayrıca çalıştırmaya gerek yok.

---

## Mimari

SQLite + FastAPI + Jinja2. Framework yok, ORM yok, build adımı yok. Mobil
öncelikli responsive HTML.

Tüm dosyalar proje klasörünün kökünde (v6.1'e kadar bir `app/` alt
klasöründeydi):

```
Patient Data Center/
  app.py            ~3300 satır — TÜM rotalar burada
  db.py             bağlantı ve yardımcılar
  guvenlik.py       oturum / kullanıcı
  goruntuler.py     snapshot kuyruğu, arşivleme, dosya yolları
  templates/        ~42 Jinja2 şablonu
  static/style.css  tüm görsel tasarım
  goc_002..028.py   veritabanı göçleri (sırayla)
  goc_hepsi.py      hepsini çalıştırır + kırık referans kontrolü
  teshis.py         genel sorun teşhisi
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
- `fet` → çözme, transfer, gebelik (**OPU yok** — oosit toplanmaz)
- `oosit_cryo` → OPU, denüdasyon, vitrifikasyon, çözme

Aşama sırası ve tip-aşama eşlemesi `app.py` içinde `ASAMA_SIRASI` ve
`TIP_ASAMALARI`. Androloji (`sperm_ornek` + iki `sperm_analiz`: bazal /
hazırlık sonrası) yalnızca `ivf_icsi`'de. Şema/listeler: README v6.2, `goc_019`.

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
**o aşamadaki adını** yazar: denüdasyon ve ICSI'de Oosit, fertilizasyonda
Zigot, gün 2/3 ve blastokistte **Embriyo** (`ornek_adi` oralarda
"Cleavage"/"Blastokist" der; kutuda kullanıcının isteğiyle Embriyo yazıyor).
Adı makroya sabit yazma, çağıran ekrandan geçir — dil değişince isim de
değişmeli. Yeni bir aşama ekranında "fotoğraf yok" diye boş kart basma,
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

**Cycle ekranı klinik özettir, fotoğraf yoktur** (v6.20). Fotoğraflar aşama
ekranlarında, tek tek ve büyük bakılacak yerde. Cycle ekranına küçük resim
ekleme.

**Kodu değil etiketi göster.** `mii`, `2pn`, `z1` gibi değerler
`liste_degeri`'nde ve laba özgü — yönetici düzenleyebiliyor. Ekranda
`liste_etiket(liste_adi, kod)` (Jinja global) kullan, sabit sözlük yazma.

**Ana ekran yapılacaklar listesidir** (v6.28). Kullanıcının kâğıt düzeni:
laboratuvarda işi bitmemiş hastaların formları bir klasörde durur, her sabah
ona bakılır, iş bitince form arşive kaldırılır. `/` tam bunun karşılığı —
`durum='aktif'` cycle'lar, hasta adı, dosya no, cycle no, OPU günü ve son
işlem. Altında **"Bugün bitenler"** (v6.29) — ölçü
`date(bitis_zamani) = date('now','localtime')`, yani kart her gece
kendiliğinden boşalıyor; saklanan bir "bugünün listesi" yok, olmasın da.
Sonra sayı özeti, en altta menü.

Düzen (v6.34, kullanıcının isteği): **Yapılacaklar ve Bugün bitenler yan
yana, Yaklaşanlar altlarında.** `.ikisutun` 720px'in altında alt alta
diziyor — telefonda iki sütun okunmuyor; sıra iki düzende de aynı. Ana ekran
`kap genis` sınıfını alıyor, sütunu 940px'e kadar genişliyor ama yan menüyle
çarpışmasın diye `calc(100vw - 500px)` ile sınırlı. Yeni bir kart eklersen
bu iki sütunu şişirme, altına koy.

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

**Örnek kodu aranabilir** (v6.35). Kod (`527078-2026-0001-03`) tüpün ve
formun üstünde yazan şey; `<hasta dosya no>-<specimen.id>` olarak
birleştirilip aranıyor, yani tam kod da kuyruğu da (`0001-03`) buluyor.
İki yerde: `/hastalar` (sonuç kartı hasta satırlarının üstünde, satır
**cycle'a** gider) ve `/cryo?ara=`. İki kural:
- Arama **yalnızca tire içeren** metinde örnek arar — tiresiz metin kod
  değildir, yoksa "3" yazan bütün örnekleri listeler.
- Örnek araması **hastanın arşivlenmiş olmasına bakmaz**; dolaptaki bir
  örneğin dosyası kapanmış olabilir. (Hasta araması eskisi gibi süzer.)

**Hasta kayıtları ay ay, arama ayı yok sayar** (v6.29). `/hastalar` iki iş
yapıyor: arama boşken **o ayın cycle'ları** (satır cycle başına), arama
doluyken **hasta satırları** ve ay süzgeci devre dışı — dosya no ya da ad
aranıyorsa hangi ayda olduğu zaten bilinmiyordur.
- **Ayın ölçüsü OPU tarihi**, yoksa cycle'ın açıldığı tarih (FET'te OPU
  olmuyor). Kullanıcının kararı: soru "kim kayıtlı" değil, "bu ay kaç vaka
  yaptık". Bunu hasta kaydının tarihine çevirme.
- Arşivlenmiş hastanın cycle'ı **ay listesinde görünür** (o iş o ay yapıldı),
  yapılacaklarda görünmez. Satırda "Arşiv" rozeti var.
- Satırın sağındaki **"Hasta kaydı"** düğmesi hastanın tüm geçmişine gider,
  satırın kendisi o ayki cycle'a (v6.31). İç içe `<a>` olamayacağı için ikisi
  kardeş, `.satirikili` yan yana diziyor — satıra bir bağlantı daha eklersen
  aynı yolu izle.
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

**Ana ekranın menüsü iki yüzeyde, aynı sırayla** (v6.26). Geniş ekranda solda
`_gezinme.html` `yan_ana()` (aşama menüsüyle aynı `.yanmenu`), telefonda
`.anadugmeler` düğme yığını; CSS 1100px'te birini gizleyip ötekini gösteriyor.
Menüye madde eklersen **ikisine birden ekle ve aynı yazıyı kullan** — aynı
düğmeyi iki isimle öğretmek personeli yanıltır. Sıra: Hasta kayıtları →
Takvim (v6.33) → Cryo haritası → Yönetici, altında ayrı grupta işlemler
(Yeni hasta, Şifre değiştir).
Menüdeki izin kontrolü yalnızca bağlantıyı gizler; asıl engel middleware ve
`yonetici_kontrol()`.

**Kayıt açıp sonra doldurma varsa, dolduramazsan açtığını geri al.**
Denüdasyonda `specimen_olustur()` önce, `goruntu_bagla()` sonra çalışıyor;
ikincisi başarısızsa **oosit geri alınmalı**, yoksa oosit sayısı şişer — o
klinik bir sayı (v6.19). Geri alma `goruntuler.bos_specimen_sil()` ile:
yalnızca hiç görüntüsü ve olayı olmayan oosit silinir. Başarısızlık **sessiz
olmasın**, sebebini ekrana yaz.

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

**`/yonetim` paneli salt okunurdur.** Durumu gösterir, hiçbir şey değiştirmez;
ayarlar kendi ekranlarından/scriptlerinden yapılır. Buraya yazma işlemi ekleme
(v6.12).

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

---

## Bekleyen işler

1. **Biyopsi / PGT modülü** — tek kalan ana modül. Biyopsi kaydı, tüp etiketi,
   haftalar sonra gelen genetik sonucun eşleştirilmesi. `pgt_sonuc` tablosu
   şemada hazır, kullanılmıyor.
2. **Yedekleme — kısmen kuruldu, hedef ayarı v6.8'de düzeltildi.**
   - `yedek.py` artık `db.ayar()` kullanıyor; argümansız çalıştırma bu makinenin
     `yerel_ayar.json` bölümündeki `yedek_klasor`'e gider. Komut satırı argümanı
     hep kazanır. Platforma uymayan yol (Mac'te `E:\yedek`) reddedilir.
   - **Windows mini PC'de bir kez `python yerel_kur.py` çalıştırılmalı** ve
     `yedek_klasor` `E:\yedek` yapılmalı. Yol ayarları artık makineye özgü
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
6. **Bozuk tarih** — bir cycle'da OPU tarihi `0026-09-04` (yıl 4 haneli değil).
   Düzeltilmeli. v6.28'de `_opu_gunu()` korumaya alındı (böyle bir değer
   yüzünden bütün yapılacaklar listesi patlamasın diye), ama kaydın kendisi
   hâlâ bozuk.
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
