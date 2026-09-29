# Patient Data Center

IVF laboratuvarı için hasta / cycle / oosit kayıt sistemi.
Bu dosya projenin **sürüm günlüğü**: her sürümde ne değişti ve neden.

- Komutlar → `KOMUTLAR.md`
- Çalışma kuralları → `CLAUDE.md`

---

## İçindekiler

Her bölüm bir sürüm: **ne değişti ve neden**. En yeni en altta.
Bir davranışı değiştirmeden önce ilgili sürümü oku — çoğu "tuhaf" görünen karar bilinçli.

**v0 — ilk ekranlar**

- [v0.1 — ilk ekranlar](#v01--ilk-ekranlar)
- [v0.2 — giriş ve düzenleme](#v02--giriş-ve-düzenleme)
- [v0.3 — denüdasyon ekranı](#v03--denüdasyon-ekranı)
- [v0.6 — silme/arşivleme ve endikasyon listesi](#v06--silmearşivleme-ve-endikasyon-listesi)
- [v0.7 — form doğrulama düzeltmeleri](#v07--form-doğrulama-düzeltmeleri)
- [v0.8 — kaçıncı cycle](#v08--kaçıncı-cycle)
- [v0.9 — otomatik lab kayıt no ve cycle silme](#v09--otomatik-lab-kayıt-no-ve-cycle-silme)

**v1 — yedekleme ve iki makine**

- [v1.0 — fotoğraf silme ve elle yükleme](#v10--fotoğraf-silme-ve-elle-yükleme)
- [v1.1 — oosit silme ve dosya başına oosit](#v11--oosit-silme-ve-dosya-başına-oosit)
- [v1.2 — otomatik yedekleme](#v12--otomatik-yedekleme)
- [v1.3 — iki makinede çalışma (Windows + macOS)](#v13--iki-makinede-çalışma-windows--macos)
- [v1.4 — ICSI ekranı](#v14--icsi-ekranı)
- [v1.9 — taşınabilir görüntü yolları](#v19--taşınabilir-görüntü-yolları)

**v2 — fertilizasyon ve gün 2/3**

- [v2.0 — fertilizasyon kontrolü](#v20--fertilizasyon-kontrolü)
- [v2.5 — gün 2 / gün 3 değerlendirme](#v25--gün-2--gün-3-değerlendirme)
- [v2.6 — blastokist değerlendirme](#v26--blastokist-değerlendirme)

**v3 — vitrifikasyon, çözme, transfer**

- [v3.0 — vitrifikasyon ve cryo haritası](#v30--vitrifikasyon-ve-cryo-haritası)
- [v3.2 — çözme (thaw)](#v32--çözme-thaw)
- [v3.5 — gezinme düzeltmeleri](#v35--gezinme-düzeltmeleri)
- [v3.6 — transfer](#v36--transfer)
- [v3.7 — fotoğraf düzeltmeleri (göç 014)](#v37--fotoğraf-düzeltmeleri-göç-014)
- [v3.8 — aşamaya bağlı fotoğraf ve snapshot alma](#v38--aşamaya-bağlı-fotoğraf-ve-snapshot-alma)

**v4 — arşivleme ve gezinme**

- [v4.0 — arşivleme ve kalıcı silme kullanıcı kararına bırakıldı](#v40--arşivleme-ve-kalıcı-silme-kullanıcı-kararına-bırakıldı)
- [v4.5 — arayüz düzenlemeleri](#v45--arayüz-düzenlemeleri)
- [v4.4 — silme hatası düzeltildi](#v44--silme-hatası-düzeltildi)
- [v4.6 — aşamalar arası gezinme](#v46--aşamalar-arası-gezinme)
- [v4.7 — snapshot toplu eşleştirme](#v47--snapshot-toplu-eşleştirme)
- [v4.8 — adlandırma ve yerleşim](#v48--adlandırma-ve-yerleşim)

**v5 — tedavi tipi ve FET**

- [v5.0 — oosit bazında over tarafı (göç 015)](#v50--oosit-bazında-over-tarafı-göç-015)
- [v5.1 — aşama kare şeridi](#v51--aşama-kare-şeridi)
- [v5.3 — gebelik sonucu](#v53--gebelik-sonucu)
- [v5.4 — tedavi tipi ve FET akışı (göç 016)](#v54--tedavi-tipi-ve-fet-akışı-göç-016)
- [v5.6 — tedavi tipi kodu netleştirildi (göç 017)](#v56--tedavi-tipi-kodu-netleştirildi-göç-017)
- [v5.8 — iki makine arasında sorunsuz taşıma](#v58--iki-makine-arasında-sorunsuz-taşıma)

**v6 — Claude Code dönemi**

- [v6.1 — Claude Code'a geçiş + düz klasör yapısı](#v61--claude-codea-geçiş--düz-klasör-yapısı)
- [v6.2 — androloji (sperm) modülü](#v62--androloji-sperm-modülü)
- [v6.3 — "İşlemi yapan" alanı (tüm aşamalar)](#v63--i̇şlemi-yapan-alanı-tüm-aşamalar)
- [v6.4 — arşiv hasta dosya numarasına göre + iki sistemde güvenli yollar](#v64--arşiv-hasta-dosya-numarasına-göre--iki-sistemde-güvenli-yollar)
- [v6.5 — örnek kodu ve aşamaya göre isimlendirme](#v65--örnek-kodu-ve-aşamaya-göre-isimlendirme)
- [v6.6 — eş zamanlı kullanım (birden fazla personel)](#v66--eş-zamanlı-kullanım-birden-fazla-personel)
- [v6.7 — çözme hangi tedavi için yapıldı (göç 024)](#v67--çözme-hangi-tedavi-için-yapıldı-göç-024)
- [v6.8 — `yedek.py` ayarları uygulamayla aynı yerden okur](#v68--yedekpy-ayarları-uygulamayla-aynı-yerden-okur)
- [v6.9 — OPU kendi ekranı + kurulum göçleri kendisi çalıştırıyor](#v69--opu-kendi-ekranı--kurulum-göçleri-kendisi-çalıştırıyor)
- [v6.10 — `kullanici.py`: giriş sorunlarını çözen araç](#v610--kullanicipy-giriş-sorunlarını-çözen-araç)
- [v6.11 — şifre değiştirme, "şifremi unuttum", kullanıcı yönetimi ekranları](#v611--şifre-değiştirme-şifremi-unuttum-kullanıcı-yönetimi-ekranları)
- [v6.12 — şifre değiştirme giriş ekranında, yönetici paneli](#v612--şifre-değiştirme-giriş-ekranında-yönetici-paneli)
- [v6.14 — modül bazlı erişim izni](#v614--modül-bazlı-erişim-izni)
- [v6.15 — tanımsız rol tek tıkla yönetici yapıyordu](#v615--tanımsız-rol-tek-tıkla-yönetici-yapıyordu)
- [v6.16 — `tasi.py`: iki makine arasında güvenli veri taşıma](#v616--tasipy-iki-makine-arasında-güvenli-veri-taşıma)
- [v6.17 — `tasi.py` yeni kurulmuş makineye de veri alabiliyor](#v617--tasipy-yeni-kurulmuş-makineye-de-veri-alabiliyor)
- [v6.18 — ana ekran, aramadan çıkış yolu, yan aşama menüsü](#v618--ana-ekran-aramadan-çıkış-yolu-yan-aşama-menüsü)
- [v6.19 — denüdasyonda hayalet oosit](#v619--denüdasyonda-hayalet-oosit)
- [v6.20 — bilgi kartı düzeni: her aşamada aynı](#v620--bilgi-kartı-düzeni-her-aşamada-aynı)
- [v6.21 — bilgi kartı düzeni: kalan beş ekran](#v621--bilgi-kartı-düzeni-kalan-beş-ekran)
- [v6.22 — düzen artık gerçekten her ekranda aynı](#v622--düzen-artık-gerçekten-her-ekranda-aynı)
- [v6.23 — örnek kodu, ilk kare, hasta adı önde](#v623--örnek-kodu-ilk-kare-hasta-adı-önde)
- [v6.24 — denüdasyon açılışta salt okunur](#v624--denüdasyon-açılışta-salt-okunur)
- [v6.25 — denüdasyon bilgi ekranı fert/blastokistin aynısı](#v625--denüdasyon-bilgi-ekranı-fertblastokistin-aynısı)
- [v6.26 — ana ekranda sol menü](#v626--ana-ekranda-sol-menü)
- [v6.27 — her ekranın üstünde ana menüye dönüş](#v627--her-ekranın-üstünde-ana-menüye-dönüş)
- [v6.28 — ana ekran yapılacaklar listesi, cycle'ın bitişi](#v628--ana-ekran-yapılacaklar-listesi-cyclein-bitişi)
- [v6.29 — bugün bitenler, ay ay hasta kayıtları](#v629--bugün-bitenler-ay-ay-hasta-kayıtları)
- [v6.30 — yıl ve ay açılır seçici](#v630--yıl-ve-ay-açılır-seçici)
- [v6.31 — bitiş saati elle, bitişi düzenle, hasta kaydına kestirme](#v631--bitiş-saati-elle-bitişi-düzenle-hasta-kaydına-kestirme)
- [v6.32 — çözmede geri oku geldiğin yere döner](#v632--çözmede-geri-oku-geldiğin-yere-döner)
- [v6.33 — takvim: ileri tarihli işler](#v633--takvim-ileri-tarihli-işler)
- [v6.34 — ana ekran iki sütun, aramadan geri dönüş](#v634--ana-ekran-iki-sütun-aramadan-geri-dönüş)

---

# v0.1 — ilk ekranlar

Hasta ve cycle kayıt ekranları. Telefon ve tablet için tasarlandı, yerel ağda çalışır.

## Kurulum

Python 3.10+ gerekiyor.

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

## Çalıştırma

Proje klasöründe (dosyalar artık alt klasörde değil — bkz. v6.1 bölümü):

```bash
python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Mac
python  -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Windows
```

Tarayıcıda `http://localhost:8000` adresine git.

**Telefondan bağlanmak için:** `--host 0.0.0.0` parametresi uygulamayı ağa açar. Mini PC'nin yerel IP adresini öğren (Windows'ta `ipconfig`, Linux'ta `ip addr`), telefondan `http://192.168.1.X:8000` gibi yaz. İkisi de aynı ağda olmalı.

## Dosyalar

Tüm dosyalar proje klasörünün kökünde (v6.1'e kadar bir `app/` alt klasöründeydi):

```
Patient Data Center/
  app.py              rotalar (hangi adres hangi ekranı açar)
  db.py               veritabanı bağlantısı ve yardımcılar
  lab.db              veritabanı
  templates/
    base.html         ortak iskelet
    hastalar.html     hasta listesi ve arama
    hasta_form.html   yeni hasta
    hasta_detay.html  hasta kartı ve cycle listesi
    cycle_form.html   yeni cycle
    cycle_detay.html  cycle kartı
  static/
    style.css         tüm görsel tasarım
```

## Bu sürümde ne var

- Hasta arama (dosya no veya ad)
- Yeni hasta — dosya no yazılırken mükerrer kontrolü yapar, kayıt varsa uyarır ve mevcut kayda yönlendirir
- Hasta kartı ve cycle listesi
- Yeni cycle — klinik protokol, zamanlar, OPU sayıları
- Cycle kartı ve özet

## Tasarım kararları

**Sistem fontları kullanıldı.** Mini PC internetsiz çalışacağı için dışarıdan font yüklenmiyor. Rakamlar `tabular-nums` ile hizalı.

**Hasta kimliği en görünür öğe.** Dosya numarası koyu bant içinde büyük punto. Yanlış hasta bu işin en pahalı hatası; ekranın her yerinde hangi hastada olduğun görünüyor.

**Dokunma alanları en az 48px, form yazıları 16px.** 16px altındaki yazı iOS'ta sayfayı otomatik yakınlaştırır ve akışı bozar.

**Boş alan NULL kaydedilir**, boş metin değil. Sorgularda `IS NULL` ile "girilmedi" ayırt edilebilsin diye.

**Yaş kolonu yok.** Doğum tarihinden hesaplanır.

## Güvenlik notu

`kullanici.sifre_hash` alanında şu an `HASH_PLACEHOLDER` yazıyor ve giriş ekranı henüz yok. Gerçek kullanıma alınmadan önce `bcrypt` veya `argon2` ile giriş eklenmeli. Bu sürüm sadece geliştirme içindir.

## Sonraki adım

Denüdasyon ekranı: fotoğraf klasörünü izleme, oosit oluşturma, sıra numarası atama.

---

# v0.2 — giriş ve düzenleme

## Yükseltme (mevcut kurulumun üzerine)

**Önce yedek al.** `lab.db` dosyasını başka bir yere kopyala.

1. Yeni zip'i aç. İçinde `lab.db` **yok** — bu bilerek, seninkinin üzerine yazılmasın diye.
2. Çıkan dosyaları mevcut `app` klasörünün üzerine kopyala (üzerine yazsın).
3. Komut İstemi'nde `app` klasöründe:

```
python goc_002.py
```

Bu script oturum tablosunu ekler ve şifre belirlemeni ister. Kullanıcı listesini gösterir, numarayı yaz, şifreyi iki kez gir. Şifre en az 8 karakter olmalı ve yazarken ekranda görünmez — bu normal.

4. Uygulamayı yeniden başlat:

```
python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
```

Artık giriş ekranı gelecek. Kullanıcı adı `onur`, şifre az önce belirlediğin.

## Bu sürümde ne eklendi

**Giriş.** Oturum açmadan hiçbir ekran görünmüyor. 12 saat işlem yapılmazsa oturum düşer. Çıkış üst sağda.

**Şifreler scrypt ile karmalanıyor.** Ham şifre hiçbir yerde saklanmıyor, veritabanını açan biri bile şifreleri okuyamaz. Ek paket gerekmiyor — Python'un standart kütüphanesinde geliyor.

**Düzenleme.** Hasta ve cycle kayıtları düzenlenebiliyor. Üst sağdaki "Düzenle" bağlantısından.

**Değişiklik geçmişi.** Her düzenleme `degisiklik_log` tablosuna yazılıyor: hangi alan, eski değer, yeni değer, kim, ne zaman. Kayıt sayfasının altındaki "Değişiklik geçmişi" düğmesinden görülüyor. Değişmeyen alanlar loglanmıyor.

**Dosya no değiştirilemiyor.** Düzenleme ekranında kilitli. Yanlış girilmiş bir dosya no düzeltilmez, kayıt yeniden açılır — aksi halde iki hasta kaydı birbirine karışabilir.

## Yeni kullanıcı eklemek

Şu an arayüzden kullanıcı eklenemiyor. Python ile:

```python
import db, guvenlik
db.yaz("INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, kullanici_adi, sifre_hash) "
       "VALUES (1,?,?,?,?,?)",
       ("Ad Soyad", "AS", "embriyolog", "kullaniciadi", guvenlik.sifrele("sifre1234")))
```

Kullanıcı yönetimi ekranı sonraki sürümlerde.

## Hâlâ eksik olanlar

- **HTTPS yok.** Yerel ağda trafik şifresiz. Klinik ağı dışına açılmamalı.
- **Yedekleme otomatik değil.** `lab.db` dosyasını düzenli kopyala ve kopyanın açıldığını test et.
- **Kayıt silme yok.** Bilerek — klinik kayıtta silme yerine iptal işareti kullanılmalı.

---

# v0.3 — denüdasyon ekranı

## Yükseltme

**Önce `lab.db` yedeği al.**

1. Yeni dosyaları mevcut `app` klasörünün üzerine kopyala
2. `python goc_003.py`
3. Uygulamayı yeniden başlat

Göç scripti snapshot klasörünü şu yola ayarlar:

```
C:\Users\Genel\Desktop\Patient Data Center\snapshot
```

Klasör başka yerdeyse `goc_003.py` içindeki `VARSAYILAN` sözlüğünü düzenle, sonra scripti çalıştır.

## Nasıl çalışır

Cycle ekranındaki **Denüdasyon ekranı** düğmesinden girilir.

Program snapshot klasörünü okur, henüz işlenmemiş görüntüleri **çekim zamanına göre** sıralar ve ilkini büyük gösterir. Dört eylem var:

- **Kaydet → oosit N** — yeni specimen açar, görüntüyü ona bağlar, numara artar
- **Aynı oosite ekle** — görüntüyü bir önceki oosite ekler, numara değişmez
- **Atla** — görüntüyü kuyruktan çıkarır, hiçbir oosite bağlamaz
- **Fotoğrafsız oosit** — numarayı alan boş bir specimen açar, görüntü tüketilmez

Altta o ana kadar kaydedilenler küçük kareler halinde görünür. Yanlış bastıysan **Son kaydı geri al** var: arşiv dosyasını siler, görüntüyü kuyruğa geri koyar, specimen'in başka görüntüsü ve olayı yoksa onu da kaldırır.

## Önemli davranışlar

**Kaynak dosyaya dokunulmaz.** Program görüntüyü arşive *kopyalar*. Kamera klasörü temizlense bile arşiv kalır. Silme, taşıma, yeniden adlandırma yapmaz.

**Aynı dosya iki kez işlenmez.** Her dosya adı + değiştirilme zamanı + boyuttan bir imza üretilir, işlenenler `kaynak_dosya` tablosunda tutulur. Kamera sayacı sıfırlanıp aynı isimde yeni dosya gelirse yeni dosya sayılır.

**Arşiv yolu:** `arsiv/{yıl}/{cycle_no}/{specimen_id}_{aşama}_{zaman}.jpg`
Dosya adında hasta adı geçmez. Hasta ilişkisi yalnız veritabanında durur.

**Denüdasyon zamanı otomatik.** İlk oosit kaydedildiğinde cycle'ın `denudasyon_zamani` alanı boşsa o an yazılır.

**Numara boşluğu olabilir.** Araya bir kaydı geri alırsan o numara boş kalır (1, 2, 4 gibi). Bu bilerek: verilen ID'ler kalıcıdır, geriye dönük numaralandırma yapılmaz.

## Bu ekranda sorulmayanlar

Maturasyon ve oosit bulguları burada girilmez — onlar ICSI ekranında, çünkü değerlendirme orada yapılıyor. Bu ekranın tek işi oositleri oluşturmak ve görüntüleri eşleştirmek.

---

# v0.6 — silme/arşivleme ve endikasyon listesi

## Yükseltme

**Önce `lab.db` yedeği al.** Sonra Ctrl+C ile uygulamayı durdur, yeni dosyaları koy:

```
python goc_004.py
python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
```

## Silme iki farklı işlem

Hasta kartının altındaki **Sil / arşivle** bağlantısı, hastanın durumuna göre farklı davranır.

**Hiç cycle'ı yoksa → kalıcı silme.** Yanlış açılmış boş bir kayıttır, gerçekten silinir. Ekran kırmızı uyarı gösterir.

**Cycle'ı varsa → arşivleme.** Kayıt silinmez, listeden kalkar. Ekran kaç cycle, oosit ve görüntü bağlı olduğunu gösterir. Hasta kartında "arşivde" rozeti belirir ve **Arşivden çıkar** düğmesiyle geri alınır.

Klinik veriyi kalıcı silmemek bilinçli bir karar: bir kayıt silindiğinde ona bağlı cycle'lar, oositler, görüntüler ve gebelik sonuçları da anlamsız kalır, geri getirilemez.

**Her iki işlemde de onay için dosya numarasını yazman gerekiyor.** Yanlış yazarsan işlem yapılmaz. Tek tıkla silinen bir şey yok.

Her iki işlem de `degisiklik_log`'a yazılır — kim, ne zaman, hangi kaydı.

Arşivdeki hastalar liste ekranının altındaki **Arşiv** düğmesinden görülür.

## Endikasyon artık seçim listesi

Serbest metin yerine açılır liste. 17 hazır seçenek var (erkek faktörü, tubal faktör, endometriozis, azalmış over rezervi, PGT endikasyonu, donör oosit, diğer...).

**Eski kayıtlar korunur.** Göç scripti mevcut cycle'lardaki serbest metin endikasyonları listeye ekler, hiçbiri kaybolmaz.

Seçenek eklemek veya çıkarmak için `liste_degeri` tablosuna satır eklenir; kod değişikliği gerekmez:

```python
import db
db.yaz("INSERT INTO liste_degeri (lab_id, liste_adi, kod, etiket, sira) "
       "VALUES (1,'endikasyon','yeni_kod','Ekranda görünecek ad', 50)")
```

Bir sınır: şu an cycle başına **tek** endikasyon seçilebiliyor. Birden fazla endikasyon işaretlemen gerekiyorsa ayrı bir bağlantı tablosu gerekir — söylersen ekleriz.

---

# v0.7 — form doğrulama düzeltmeleri

## Düzeltilen iki hata

**Virgüllü ondalık sayı.** `2,4` gibi virgülle yazılan değerler kaydedilemiyor ve Internal Server Error veriyordu. Artık virgül de nokta gibi kabul ediliyor. Ondalık alanların klavye tipi de değişti — telefonda virgül tuşu görünür.

**Aynı cycle no.** Var olan bir cycle numarası tekrar girildiğinde veritabanı reddediyor ve hata sayfaya düşüyordu. Artık formun üstünde hangi hastaya ait olduğunu söyleyen bir açıklama çıkıyor, girilen değerler kaybolmuyor.

## Genel değişiklik

Cycle formundaki hatalar artık Internal Server Error yerine formun üstünde kırmızı açıklama olarak gösteriliyor ve **girdiğin değerler formda kalıyor**. Uzun bir formu baştan doldurmak zorunda kalmıyorsun.

Yakalanan durumlar: sayı olmayan değer (hangi alan olduğu söylenir), boş cycle no, mükerrer cycle no.

---

# v0.8 — kaçıncı cycle

Cycle'ın iki numarası var artık:

**Lab kayıt no** (`cycle_no`) — laboratuvara özgü, benzersiz. Aynı numara iki kez kullanılamaz.

**Kaçıncı cycle** (`hasta_cycle_no`) — hastanın kaçıncı denemesi. Hasta içinde sıralı, laboratuvar geneli için benzersiz değil.

Yeni cycle açarken "Kaçıncı cycle" otomatik doldurulur: o hastanın en yüksek numarasının bir fazlası. **Üzerine yazabilirsin** — hasta başka merkezde tedavi görmüşse gerçek deneme sayısını girersin.

Mevcut kayıtlar göç sırasında OPU/hCG zamanına göre otomatik numaralandırıldı.

Hasta kartındaki cycle listesi artık "3. cycle" diye gösteriyor, lab kayıt no altta. Cycle kartının başlığında da görünüyor.

## Yükseltme

```
python goc_005.py
```

---

# v0.9 — otomatik lab kayıt no ve cycle silme

## Otomatik numaralandırma

Yeni cycle açarken **Lab kayıt no** otomatik doluyor: `2026-0001`, `2026-0002`... Üzerine yazabilirsin.

Ayarlar (`ayarlar` tablosunda, kod değişikliği gerektirmez):

| anahtar | varsayılan | ne yapar |
|---|---|---|
| `lab_no_onek` | yıl | Numaranın önündeki kısım |
| `lab_no_basamak` | 4 | Sıra kaç basamaklı (0001) |
| `lab_no_bosluk_doldur` | 1 | 1 = boşalan numara yeniden kullanılır |
| `lab_no_yillik_sifirla` | 1 | 1 = her yıl önek değişir, sıra 1'den başlar |

Değiştirmek için:

```python
import db
db.yaz("UPDATE ayarlar SET deger='0' WHERE anahtar='lab_no_bosluk_doldur'")
```

Bu biçime uymayan eski numaralar (elle girilmiş olanlar) olduğu gibi kalır ve otomatik numaralandırma onlarla çakışmaz.

## Cycle silme iki farklı işlem

Cycle kartının altındaki **Sil / iptal et** bağlantısı, bağlı kayıt olup olmamasına göre farklı davranır.

**Hiçbir kayıt bağlı değilse → kalıcı silme.** Oosit, görüntü, işlem kaydı, sperm örneği, gebelik sonucu yoksa cycle tamamen silinir ve **numarası boşa düşer** — sıradaki yeni cycle o numarayı alır.

**Bağlı kayıt varsa → iptal.** Cycle "iptal" olarak işaretlenir, veriler durur, numarası kimseye verilmez. Kartta ve hasta listesinde "iptal" rozeti görünür, **İptali geri al** ile geri döner.

Onay için lab kayıt numarasını yazman gerekiyor.

## Neden numara her zaman yeniden kullanılmıyor

Bir lab kayıt numarası dish etiketine, forma veya rapora yazıldıysa, o numaranın sonradan başka bir hastaya verilmesi izlenebilirliği bozar. Bu yüzden yalnızca **hiç kullanılmamış** numaralar yeniden dağıtılıyor. Bu davranışı istemezsen `lab_no_bosluk_doldur` ayarını 0 yap; o zaman numaralar hep artar, boşluklar boş kalır.

---

# v1.0 — fotoğraf silme ve elle yükleme

## Yükseltme

```
python goc_007.py
```

## Fotoğraf silme

Oosit karesine dokunup büyük resmi açtığında, panelin altında **Bu fotoğrafı sil** bağlantısı var. Onay ekranı fotoğrafı, hangi oosite ait olduğunu, aşamasını ve kaynağını gösterir.

**Oosit kaydı silinmez**, yalnızca o fotoğraf. Bir oositin üç karesi varsa ikisini silip birini bırakabilirsin.

Kameradan gelen bir fotoğrafı silersen, kamera klasöründeki orijinal dosyaya dokunulmaz ve dosya **denüdasyon kuyruğuna geri döner** — yanlış oosite eşleştirdiysen silip yeniden eşleştirirsin.

Silme işlemi `degisiklik_log`'a yazılır.

## Elle fotoğraf ekleme

Cycle kartındaki **Fotoğraf ekle** düğmesi. Başka kaynaktan gelen görüntüleri (dış merkez raporu, telefonla çekilmiş bir kare, eski arşiv) sisteme koyabilirsin.

- **Hangi oosite** — belirli bir oosite bağlar, veya "oosite bağlama" seçilirse cycle arşivine koyar
- **Aşama** — denüdasyon, ICSI, blastokist, thaw sonrası...
- **Dosyalar** — birden fazla seçilebilir, hepsi aynı oosite ve aşamaya kaydedilir

Sınırlar: dosya başına 25 MB; jpg, jpeg, png, tif, tiff, bmp, webp. Desteklenmeyen tür yüklenirse açıklama gösterilir ve hiçbiri kaydedilmez.

Elle yüklenen görüntüler `goruntu.kaynak = 'elle'` olarak işaretlenir; kameradan gelenler `'kamera'`. Silme onay ekranında hangisi olduğu yazar. Bu ayrım ileride önemli: kamera görüntüleri standart büyütme ve aydınlatmayla çekilir, elle yüklenenler değil — morfoloji karşılaştırması yaparken karıştırılmamalı.

---

# v1.1 — oosit silme ve dosya başına oosit

## Oosit silme

Oosit karesine dokun, açılan panelde **Oositi sil** var. Fotoğrafsız oositler de artık tıklanabilir — panel "fotoğraf yok" der ve silme bağlantısını gösterir.

**Bağlı fotoğraflar da silinir.** Kameradan gelenler denüdasyon kuyruğuna geri döner, kamera klasöründeki orijinallere dokunulmaz.

**İşlem kaydı olan oosit silinmez.** Maturasyon, ICSI, fertilizasyon gibi bir kaydı varsa ekran bunu söyler ve silme çalışmaz. Klinik işlem kaydı olan bir oositi silmek, o işlemin hiç yapılmamış gibi görünmesine yol açar.

Silinen oositin numarası boş kalır (1, 2, 4 gibi). Verilen oosit kimlikleri kalıcıdır, geriye dönük numaralandırma yapılmaz.

## Dosya başına ayrı oosit

Fotoğraf ekleme ekranındaki "Hangi oosite" listesinin başına yeni seçenek geldi: **Her dosya ayrı oosit olsun**.

Beş oositin fotoğrafını birlikte yüklersen her biri kendi numarasını alır. Belirli bir oosit seçersen eskisi gibi hepsi ona eklenir (aynı oositin birden çok karesi için).

Bir dosya reddedilirse (desteklenmeyen tür, boyut aşımı) onun için açılan boş oosit geri alınır, numara boşa düşmez.

---

# v1.2 — otomatik yedekleme

## Kurulum

```
python goc_008.py
```

Varsayılan hedef `D:\lab_yedek`. Değiştirmek için:

```
python -c "import db; db.yaz(\"UPDATE ayarlar SET deger='E:\\yedek' WHERE anahtar='yedek_klasor'\")"
```

**Hedef, veritabanının bulunduğu diskten farklı olmalı.** Aynı diske yedek almak, disk bozulduğunda ikisini birden kaybetmek demektir. Harici disk, ağ sürücüsü veya ikinci bir dahili disk kullan.

Elle denemek için:

```
python yedek.py
```

## Görev Zamanlayıcı (her gün 15:00)

1. Başlat menüsüne `Görev Zamanlayıcı` yaz, aç
2. Sağdaki **Temel Görev Oluştur**
3. Ad: `Lab Kayit Yedekleme` → İleri
4. **Günlük** → İleri
5. Başlangıç saati **15:00** → İleri
6. **Program başlat** → İleri
7. Program/betik: `yedek.bat` dosyasını **Gözat** ile seç
8. Başlangıç yeri: `app` klasörünün yolu (bu alan boş kalırsa script dosyaları bulamaz)
9. İleri → **Son**

Sonra göreve sağ tıklayıp **Çalıştır** de, doğru işlediğini gör.

Görevin özelliklerinden **Kullanıcı oturum açmamış olsa da çalıştır** seçilirse bilgisayar açıkken kimse oturum açmasa da yedek alınır.

## Script ne yapıyor

**Tutarlı kopya.** SQLite'ın kendi yedekleme API'sini kullanıyor, düz dosya kopyası değil. Uygulama tam o anda yazıyor olsa bile yedek bütün çıkar. Düz kopyada yarım yazılmış bir veritabanı elde edebilirsin ve bunu ancak geri yüklemeye çalışırken fark edersin.

**Doğrulama.** Kopya alındıktan sonra `integrity_check` çalıştırılıyor ve tablo/kayıt sayıları okunuyor. Doğrulanamayan yedek silinip hata veriliyor. Test edilmemiş yedek yedek değildir.

**Arşiv fotoğrafları.** Yalnızca yeni veya değişmiş dosyalar kopyalanıyor, her gün terabaytlar taşınmıyor. Hedeften hiçbir şey silinmiyor — kaynakta bir dosya silinse bile yedekte kalır.

**Saklama.** Son 14 günlük veritabanı kopyası tutuluyor, her ayın 1'inde alınan yedek kalıcı olarak saklanıyor. En yeni kopya asla silinmiyor. Bu değerler `yedek.py` başındaki `GUNLUK_SAKLA` ve `AYIN_BIRI_SAKLA` ile ayarlanır.

**Günlük kayıt.** Her çalışma `yedek.log` dosyasına yazılıyor. Sorun olduğunda ilk bakılacak yer orası.

## Uygulama içi uyarı

Hasta listesinin üstünde, son yedek 3 günden eskiyse turuncu uyarı çıkıyor. Hiç yedek alınmamışsa da uyarıyor. Eşiği değiştirmek için `yedek_uyari_gun` ayarı.

Bu önemli: zamanlanmış görevler sessizce durur (parola değişir, disk takılı olmaz, klasör taşınır). Uyarı olmasa aylarca yedeksiz çalıştığını fark etmezsin.

## Geri yükleme

1. Uygulamayı durdur (Ctrl+C)
2. Mevcut `lab.db` dosyasını `lab_bozuk.db` diye yeniden adlandır (silme — sorunun ne olduğunu anlamak gerekebilir)
3. Yedek klasöründen istediğin `lab_YYYYAAGG_SSDD.db` dosyasını kopyala, adını `lab.db` yap
4. Fotoğraflar için yedekteki `arsiv` klasörünü uygulama klasörüne kopyala
5. Uygulamayı başlat

Bunu **bir kez şimdi dene.** Geri yüklemeyi ilk kez gerçek bir kayıp anında denemek kötü bir fikir.

---

# v1.3 — iki makinede çalışma (Windows + macOS)

Kod her iki sistemde de aynı çalışır. Dikkat edilecek üç şey var.

## 1. Kodu senkronize et, veriyi etme

**Senkronize edilecek:** `.py` dosyaları, `templates/`, `static/`
**ASLA senkronize edilmeyecek:** `lab.db`, `arsiv/`, `yerel_ayar.json`

Sebep: SQLite dosyasını bulut senkronizasyonuyla paylaşmak bozulmaya yol açar (iki taraf aynı anda yazarsa dosya kilitleri çalışmaz). Ayrıca iki kopya birbirinden ayrıldığında birleştirmenin pratik bir yolu yoktur.

**Pratik kural: gerçek veri lab'daki mini PC'de kalır, evde test verisiyle çalışırsın.** Evde `lab.db`'yi silip `kur.py` + `listeler.py` ile temiz bir tane oluşturabilirsin — geliştirme yaparken bunu sık yapacaksın, gerçek veriyle yapmak tehlikeli olurdu.

Senkronizasyon için iCloud Drive, OneDrive veya Dropbox yeterli. `.gitignore` dosyası hazır — ileride Git'e geçersen doğru dosyalar zaten hariç tutulmuş olur.

## 2. Klasör yolları makineye özgü

Snapshot, arşiv ve yedek klasörleri artık `yerel_ayar.json` dosyasından okunuyor. Bu dosya her makinede ayrı, senkronize edilmiyor.

Her yeni makinede bir kez:

```
python yerel_kur.py
```

İşletim sistemini algılar, uygun yolları önerir, onaylayınca yazar. Yollar yanlışsa dosyayı metin editörüyle açıp düzeltebilirsin:

```json
{
  "goruntu_kaynak_klasor": "/Users/onur/Desktop/snapshot",
  "goruntu_arsiv_klasor": "/Users/onur/lab/arsiv",
  "yedek_klasor": "/Users/onur/lab_yedek"
}
```

Öncelik sırası: `yerel_ayar.json` → `ayarlar` tablosu. Yani yerel dosyada olmayan bir ayar veritabanından okunur. Dosya bozuksa program durmaz, veritabanına düşer.

## 3. Komut farkları

| | Windows | macOS |
|---|---|---|
| Python | `python` | `python3` |
| Paket kurma | `python -m pip install ...` | `python3 -m pip install ...` |
| Çalıştırma | `python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000` | `python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000` |
| Durdurma | Ctrl+C | Ctrl+C |

macOS'ta Terminal'de klasöre gitmenin kolay yolu: `cd ` yaz (sonda boşluk), klasörü Finder'dan sürükleyip Terminal penceresine bırak, Enter.

Mac'te ilk kez kütüphaneleri kurman gerekir:

```
python3 -m pip install fastapi uvicorn jinja2 python-multipart
```

## Özet akış

**Evde (Mac):** kod yaz, test verisiyle dene
**İşte (Windows):** güncellenen kodu al, gerçek veriyle çalış

Her iki yönde de yalnızca kod dosyaları taşınır. `lab.db` iki makinede ayrı yaşar ve karışmaz.

---

# v1.4 — ICSI ekranı

Cycle kartındaki **ICSI ekranı** düğmesinden girilir. Göç scripti gerekmiyor.

## Akış

Ekran senin çalışma sıranı izler: önce oosite bak, sonra enjeksiyonu değerlendir.

Bir oosit gösterilir (denüdasyon fotoğrafıyla birlikte), sen sırayla:

1. **Maturasyon** — MII / MI / GV / Dejenere / Atretik
2. **Oosit bulguları** — kalın zona, granüllü sitoplazma, SER kümesi... çoklu seçim, bulgu yoksa hiçbirine dokunmazsın
3. **Enjeksiyon** — yapıldı / yapılmadı
4. **Geçiş zorluğu** — kolay / normal / zor
5. **Enjeksiyon sonucu** — başarılı / dejenere

**Kaydet ve sonraki oosit** ile ilerlersin. Program otomatik olarak henüz kaydedilmemiş bir sonraki oosite geçer.

MII dışında bir maturasyon seçersen enjeksiyon kendiliğinden "yapılmadı"ya döner ve alttaki iki blok gizlenir. Elle geri açabilirsin (MII olmayan bir oosite enjeksiyon yaptığın nadir durum için).

## Üst şerit

Ekranın üstünde oosit numaraları var. Kaydedilmiş olanlar dolu, dejenere olanlar kırmızı, üzerinde çalıştığın çerçeveli. Herhangi birine dokunup o oosite atlayabilirsin — düzeltme yapmak için sıraya girmene gerek yok.

## Otomatik kaydedilenler

Zaman ve operatör her kayıtta otomatik yazılır. Her oositin kendi enjeksiyon saati olur; on oositlik bir seride ilk ve son arasında yarım saat geçebilir ve fertilizasyon kontrolü zamanlaması buna göre hesaplanır.

## Düzeltme

Bir oositi tekrar kaydedersen mükerrer kayıt oluşmaz, mevcut kayıt güncellenir ve **değişiklik `degisiklik_log`'a yazılır**. Enjeksiyonu "yapılmadı"ya çevirirsen eski ICSI kaydı silinmez, iptal işaretlenir.

## Bilinen sınır

Bu ekran ICSI sırasında yeni fotoğraf çekmiyor — denüdasyonda çekilen kareyi gösteriyor. ICSI anında ayrı kare çekiyorsan şimdilik **Fotoğraf ekle** ekranından "ICSI" aşamasını seçerek yükleyebilirsin. Kamera kuyruğunu bu ekrana da bağlamak sonraki adım olabilir.

## ICSI kaydını silme

Kaydı olan bir oosite girdiğinde ekranın altında **Bu oositin kaydını sil** bağlantısı çıkar. Onay ekranı ne silineceğini tek tek gösterir (maturasyon, bulgular, geçiş zorluğu, sonuç, kaydedilme zamanı).

**Oosit ve fotoğrafları durur**, yalnızca değerlendirme temizlenir. Oositi baştan değerlendirebilirsin.

İşlem kayıtları veritabanından fiziksel olarak silinmez, `iptal_mi` işaretlenir ve `degisiklik_log`'a yazılır. Klinik işlem kaydında silme yerine iptal kullanılır: bir işlemin yapıldığı ve sonradan geri alındığı bilgisi, o işlemin hiç yapılmamış görünmesinden daha doğrudur.

Kaydı temizlenen oosit yeniden silinebilir hale gelir — daha önce "işlem kaydı olan oosit silinemez" uyarısı veren oositi, önce ICSI kaydını temizleyip sonra silebilirsin.

## Bulgular açılır panelde

Oosit bulguları ICSI ekranında artık listeyi kaplamıyor. Kartta tek bir satır var; seçili bulgular orada özet olarak yazıyor ("Kalın zona, Granüllü sitoplazma"), bulgu yoksa "Bulgu yok".

Satıra dokununca alttan açılan panelde tüm bulgular listeleniyor. Seç, **Tamam** de. **Temizle** hepsini kaldırır.

Seçimler formun içinde duruyor, yani panel açılmadan da kaydedersen mevcut seçimler korunur. Panel kapalıyken bile özet satırında ne seçili olduğunu görürsün.

Bu değişiklik ICSI ekranını kısalttı: bir oosit için maturasyon, bulgu özeti ve enjeksiyon tek ekranda kaydırmadan görünüyor.

---

# v1.9 — taşınabilir görüntü yolları

## Sorun

Fotoğraf yolları veritabanında tam yol olarak saklanıyordu:
`C:\Users\Genel\Desktop\Patient Data Center\arsiv\2026\...`

`lab.db` başka bir makineye taşındığında bu yol orada yok, fotoğraflar açılmıyordu.

## Çözüm

Artık arşiv klasörüne göre **göreli yol** saklanıyor: `2026/2026-0417/xxx.jpg`

Program okurken bunu o makinenin kendi arşiv klasörüyle birleştiriyor. Windows'ta `C:\...\arsiv\2026\...`, Mac'te `/Users/onur/lab/arsiv/2026/...` olur. Aynı veritabanı iki makinede de çalışır.

## Yükseltme

```
python goc_009.py          (Mac'te: python3 goc_009.py)
```

Mevcut kayıtları çevirir ve dosyaların gerçekten yerinde olup olmadığını kontrol edip söyler. Windows'ta yazılmış yolları da tanır.

Eski tam yollar da okunmaya devam eder: dosya o yolda duruyorsa kullanılır, durmuyorsa yoldaki `arsiv` klasöründen sonrası alınıp bu makinenin arşiviyle birleştirilir. Yani göçü çalıştırmayı unutsan bile fotoğraflar kaybolmaz.

## İki makine arasında taşıma

`lab.db` taşınacaksa **`arsiv` klasörü de taşınmalı.** Veritabanı sadece yolu tutuyor, fotoğraflar dosya sisteminde duruyor.

Kural değişmedi: aynı anda tek kopya canlı olsun. İki makinede de kayıt girip sonra birini seçersen diğerindekiler kaybolur, birleştirmenin yolu yok.

## sifirdan_kur.py

Yeni bir makinede temiz veritabanı kurmak için tek komut:

```
python3 sifirdan_kur.py
```

Güncel şemayı kurar, 24 seçim listesini ve varsayılan ayarları doldurur, kullanıcı oluşturup şifresini sorar, işletim sistemine uygun klasör ayarlarını yazar. Mevcut `lab.db` varsa dokunmaz — önce yeniden adlandırman gerekir.

Test veritabanıyla çalışmak için ideal: gerçek veriye dokunmadan denemeler yaparsın.

---

# v2.0 — fertilizasyon kontrolü

Cycle kartındaki **Fertilizasyon kontrolü** düğmesinden girilir. Göç gerekmiyor.

## Akış

ICSI ekranıyla aynı mantık: üstte oosit şeridi, altta o oositin kaydı.

1. **Sonuç** — normal / dejenere / kayıp
2. **Pronükleus sayısı** — 0PN / 1PN / 2PN / 3PN / 4PN ve üzeri
3. **PN skoru** — Z1–Z4
4. **Zigot bulguları** — halo, PN hizasız, sitoplazmik granülasyon, vakuol

**Kaydet ve sonraki oosit** ile ilerlersin.

## Alan bağımlılıkları

Sonuç "dejenere" veya "kayıp" seçilirse PN blokları gizlenir ve kaydedilmez — "0PN" ile "dejenere" karışmaz.

PN sayısı 2 değilse Z skoru sorulmaz. Z sınıflaması iki pronükleusun birbirine göre konumu üzerinden tanımlı olduğu için 1PN veya 3PN'de anlamı yok. Ekranda gizlense bile yanlışlıkla gönderilirse sunucu da temizler.

## Zaman göstergesi

Ekranın üstünde ICSI'den bu yana kaç saat geçtiği ve hedef saat yazıyor. Hedeften iki saatten fazla saparsa turuncuya döner.

Hedef `ayarlar` tablosundaki `fert_kontrol_saat` (varsayılan 17). Değiştirmek için:

```python
import db
db.yaz("UPDATE ayarlar SET deger='16' WHERE anahtar='fert_kontrol_saat'")
```

Bu ayar hedefi belirler; gerçek zaman her kayıtta ayrıca saklanır. İkisi karıştırılmaz — hedef 17 saatse ama pratikte 15 ile 19 arasında değişiyorsa bunu ancak gerçek zamanları kaydedince fark edersin.

## Şeritteki PN

Üst şeritte her oosit numarasının yanında PN sayısı küçük olarak yazıyor. Bir bakışta cycle'ın fertilizasyon tablosunu görürsün.

## Durum takibi

Kayıt sonrası oositin durumu güncellenir: 2PN → `zigot`, diğerleri → `0pn` / `1pn` / `3pn`, dejenere → `degenere`. 0PN ve 1PN'ler kültüre devam ettiği için silinmez, sonraki aşamalarda da görünür.

## Silme

Ekranın altında **Bu oositin kaydını sil**. Yalnızca fertilizasyon değerlendirmesi temizlenir; oosit, fotoğrafları ve ICSI kaydı durur. Kayıt fiziksel olarak silinmez, iptal işaretlenir ve `degisiklik_log`'a yazılır.

## İşlem saati elle girilebilir

ICSI ve fertilizasyon ekranlarında **İşlem saati** alanı var. Şu anki saat dolu gelir; geriye dönük kayıt giriyorsan (dünkü cycle'ı bugün girmek gibi) değiştirirsin.

Kayıtlı bir oosite döndüğünde alan o kaydın saatiyle dolar, üzerine yazmadıkça değişmez.

Boş bırakılırsa veya geçersiz bir değer girilirse şu anki saat kullanılır.

Bu alan zincirin tamamını etkiliyor: fertilizasyon ekranındaki "ICSI'den bu yana X saat" göstergesi buradan hesaplanıyor, ve ileride QC analizlerinde zamanlama sorularının cevabı bu değerlerden çıkacak. Geriye dönük kayıt girerken doğru saati yazmak, o kaydın analitik değerini korumanın tek yolu.

## Şerit gösterimi

Üst şeritte oosit numarası ile durum bilgisi birbirine karışıyordu ("1" + "2PN" → "12"). Artık iki satır: numara üstte kalın, durum altta küçük.

ICSI ekranında altta maturasyon (MII, GV, MI), fertilizasyon ekranında PN sayısı (2PN, 0PN) yazıyor. Kaydedilmiş ama PN girilmemiş oositlerde tire görünür.

---

# v2.5 — gün 2 / gün 3 değerlendirme

Cycle kartındaki **Gün 2 / Gün 3** düğmesinden girilir. Göç gerekmiyor.

Ekranın üstünde gün seçici var; gün 2 ve gün 3 **ayrı kayıtlardır**, biri diğerinin üzerine yazmaz. Aynı oositi iki günde de değerlendirip gelişim hızını izleyebilirsin.

## Alanlar

- **Hücre sayısı** ve **fragmentasyon (%)** yan yana
- **Simetri** — eşit / hafif eşitsiz / eşitsiz
- **Bulgular** — multinükleasyon, düzensiz bölünme, vakuol
- **Skor** — boş bırakılırsa hesaplanır
- **İşlem saati**

Fragmentasyon virgüllü girilebilir (12,5).

## Otomatik skor

Boş bırakılan skor üç boyuttan hesaplanır ve **en kötüsü belirleyicidir**:

| | A | B | C |
|---|---|---|---|
| Hücre (gün 2: 2–4, gün 3: 6–8) | beklenen aralıkta | ±1 | daha uzak |
| Simetri | eşit | hafif eşitsiz | eşitsiz |
| Fragmentasyon | <%10 | %10–25 | >%25 |

8 hücre + eşit + %5 → A. 4 hücre + eşitsiz + %30 → C.

**Bu kural bir varsayım.** Kendi laboratuvarının kuralı farklıysa `app.py` içindeki `cleavage_skor` fonksiyonunu değiştir; kayıt yapısı değişmez. Elle skor girersen otomatik hesaplama devreye girmez ve kayıtta `elle` olarak işaretlenir — ileride "kuralımız pratikte ne kadar tutuyor" sorusunu sorabilmen için bu ayrım saklanıyor.

## Şerit

Numaranın yanında o günkü hücre sayısı yazıyor: `1-8H`, `2-4H`. Kaydedilmemiş oositlerde sadece numara.

Fertilizasyonda 2PN olmayan oositlerde ekranın üstünde hatırlatma çıkar (0PN, 1PN, 3PN) — kültüre devam ettirdiğin oositleri değerlendirirken hangisi olduğunu bilirsin.

## Silme

**Bu oositin gün N kaydını sil** yalnızca o günü temizler. Diğer gün ve diğer aşamalar durur.

---

# v2.6 — blastokist değerlendirme

Cycle kartındaki **Blastokist** düğmesinden girilir. Göç gerekmiyor.

Gün 5, 6 ve 7 ayrı kayıtlardır. Gün 5'te morula olan bir embriyoyu gün 6'da blastokist olarak kaydedersin; ikisi de saklanır ve gelişim hızı izlenebilir.

## Alanlar

**Genişleme** — 1 (erken blastosöl), 2 (yarım), 3 (tam), 4 (genişlemiş), 5 (hatching), 6 (hatched), artı morula, erken morula, arrest.

**ICM** ve **Trofektoderm** — A / B / C.

Morula, erken morula veya arrest seçilirse ICM ve TE blokları gizlenir ve kaydedilmez — bu durumlarda tanımsız oldukları için.

## Otomatik skor

Genişleme + ICM + TE birleştirilir: `4AA`, `3BC`, `5AB`. Blastokist dışı durumlar kısaltılır: morula `M`, erken morula `EM`, arrest `ARR`.

Elle skor girersen otomatik devreye girmez ve kayıtta `elle` işaretlenir.

## Şerit

Numaranın yanında o günün skoru yazıyor: `1-4AA`, `3-ARR`. Arrest olanlar kırmızı. Bir bakışta o günkü blastokist tablosunu görürsün.

## Silme

**Bu oositin gün N kaydını sil** yalnızca o günü temizler. Diğer günler ve diğer aşamalar durur.

---

## Akışın şu anki hali

denüdasyon → ICSI → fertilizasyon kontrolü → gün 2/3 → blastokist

Her ekranda: üst şerit, aşamaya özel fotoğraf, seçim düğmeleri, işlem saati, fotoğraf ekle/sil, kayıt silme, değişiklik geçmişi.

Kalan aşamalar: biyopsi/PGT, vitrifikasyon ve cryo harita, thaw, transfer, gebelik sonucu.

## Kavitasyon eklendi (göç 010)

Blastokist genişleme listesine **Kavitasyon** eklendi. Morula ile erken blastosöl arasındaki geçiş aşaması.

Liste artık gelişim sırasında: 1–6, sonra erken morula → morula → kavitasyon → arrest.

Kavitasyon da blastokist dışı bir durum sayılır: seçilince ICM ve TE sorulmaz, skor `KAV` olur, oositin durumu `kavitasyon` olarak işaretlenir. Ertesi gün blastokiste ilerlerse gün 6 kaydı ayrı tutulur ve gün 5'teki kavitasyon kaydı korunur.

Yükseltme: `python goc_010.py`

## Blastokist dışı derecelendirme (göç 011)

Morula, erken morula ve kavitasyon için **Derece** alanı eklendi: 1 / 2 / 3.

Ekranda üç durum var:

| Genişleme seçimi | Sorulan |
|---|---|
| 1–6 (blastokist) | ICM ve TE |
| Erken morula, morula, kavitasyon | Derece |
| Arrest | hiçbiri |

Seçim değiştiğinde ilgili blok açılır, diğerinin seçimleri temizlenir. Ekranda gizlense bile yanlış alan gönderilirse sunucu da temizler — blastokiste derece, arreste derece yazılmaz.

Skor buna göre birleşir: `M2`, `KAV1`, `EM3`. Derece girilmezse sadece kısaltma kalır (`M`). Blastokistler eskisi gibi `4AA` biçiminde.

Şeritte de görünür: `1-M2`, `2-KAV1`, `5-4AB`.

Yükseltme: `python goc_011.py`

---

# v3.0 — vitrifikasyon ve cryo haritası

## Yükseltme

```
python goc_012.py
```

Konum şemasını kurar. Varsayılan dört seviye: **Tank / Kanister / Goblet / Pozisyon**.

Farklı çalışıyorsan (Tank/Rack/Box/Slot gibi) `goc_012.py` içindeki `SEVIYELER` listesini düzenleyip scripti yeniden çalıştır — ekrandaki alan adları buna göre değişir.

## Vitrifikasyon

Cycle kartındaki **Vitrifikasyon** düğmesinden. Ekran ikiye ayrılır: üstte daha önce dondurulanlar, altta adaylar.

Akış: dondurulacak embriyoları işaretle → taşıyıcı bilgisi (etiket, tip, renk) → konum → saat → kaydet.

**Birden fazla embriyo tek taşıyıcıya konabilir.** Birlikte seçtiklerin aynı taşıyıcıya gider. Farklı taşıyıcılara koyacaksan ayrı ayrı kaydedersin.

Etiket laboratuvar geneli benzersizdir; aynı etiket ikinci kez kullanılamaz. Cycle no + saat şeklinde bir öneri dolu gelir.

## Cryo haritası

Hasta listesinin sağ üstündeki **Cryo** bağlantısından veya vitrifikasyon ekranından.

- **Tanklar** — her tankta kaç taşıyıcı ve kaç embriyo olduğu
- **Dolu taşıyıcılar** — etiket, tip, renk, embriyo sayısı, konum
- **Arama** — etiket, konum, dosya no veya hasta adıyla

Konumu girilmemiş taşıyıcılar turuncu uyarıyla işaretlenir.

Taşıyıcıya dokununca içindeki embriyolar listelenir: hangi hasta, hangi cycle, kaçıncı oosit, son blastokist skoru. Birden fazla embriyo varsa "çözüldüğünde hepsi etkilenir" uyarısı çıkar.

## Harita türetilmiştir

Ayrı bir harita belgesi tutulmaz. Vitrifikasyon kaydı girilince konum dolar; kayıt geri alınınca boşalır. Elle harita güncellemesi diye bir iş yoktur.

## Kaydı geri alma

Dondurulmuş listesindeki **geri al** bağlantısı. Bu yalnızca **yanlış girilmiş bir kayıt** içindir — gerçekten çözülen embriyo için thaw kaydı girilecek (sonraki adım).

Taşıyıcıda başka embriyo varsa yalnızca seçilenin kaydı iptal edilir, taşıyıcı ve diğerleri yerinde kalır. Son embriyo da çıkarılırsa taşıyıcı "boşaltıldı" işaretlenir ve konumu boşa düşer.

## Devreye alırken

Tanktaki **mevcut** embriyolar sisteme girilmelidir. Yalnızca bundan sonra donduracaklarını girersen harita eksik olur ve sistem "boş" derken tank dolu görünür. Bu tek seferlik giriş, fiziksel envanter kontrolüyle birlikte yapılmalı.

---

# v3.2 — çözme (thaw)

Taşıyıcı detayındaki **Bu taşıyıcıyı çöz** düğmesinden. Göç gerekmiyor.

## Neden taşıyıcı bazında

Çözme fiziksel olarak taşıyıcı üzerinde yapılır. Bir cryotop'ta iki embriyo varsa ikisi de aynı anda çözülür — birini çözüp diğerini yerinde bırakmak mümkün değil.

Ekran bu yüzden taşıyıcının tamamını gösterir ve **her embriyo için sağkalım girilmeden kaydetmez.** Eksik bırakırsan uyarı verir.

## Alanlar

Her embriyo için ayrı: **sağkalım** (canlı / dejenere / kısmi hasar) ve **re-expansion (%)**. Çözme saati taşıyıcı geneli için tek.

Re-expansion virgüllü girilebilir (85,5) ve 0–100 aralığına sınırlanır.

## Kaydın etkisi

- Embriyo durumu: canlı → `cozuldu`, diğerleri → sağkalım değeri
- Taşıyıcı → `boşaltıldı`
- Konum → haritada boşa düşer, cryo listesinden kalkar

Böylece harita gerçek durumu yansıtır: çözülen taşıyıcının yeri otomatik açılır.

## Geri alma

**Çözme kaydını sil** yalnızca yanlış girilmiş kayıt içindir. Embriyo `dondurulmuş` durumuna döner, ama taşıyıcı "boşaltıldı" olarak kalır — fiziksel olarak geri koyduysan yeni bir vitrifikasyon kaydı girilmelidir. Bu bilerek böyle: bir kez çıkarılmış taşıyıcının eski konumuna otomatik geri konması, haritanın gerçekle uyuşmama riskini yaratırdı.

## Canlılık oranı ve iki kontrol noktası (göç 013)

Çözme ekranı genişletildi.

**Zamanlar** kartında iki saat var:
- **Çözme saati** — taşıyıcının çözüldüğü an
- **İkinci kontrol saati** — re-expansion değerlendirmesinin yapıldığı an. Henüz yapılmadıysa boş bırakılır, sonra doldurulur.

**Her embriyo için iki fotoğraf yuvası:**
- Çözme sonrası
- İkinci kontrol

Yuvaların altındaki bağlantıdan fotoğraf eklenir, üstüne dokununca tam ekran açılır. Aynı aşamaya birden çok kare eklenirse köşede sayı görünür ve tam ekranda oklarla geçilir.

**İki ayrı yüzde alanı:**
- **Canlılık oranı** — çözme anında canlı kalan hücre oranı
- **Re-expansion** — ikinci kontroldeki yeniden genişleme

İkisi de virgüllü girilebilir ve 0–100 aralığına sınırlanır. Ayrı tutulmaları önemli: biri çözmenin kendi başarısını, diğeri embriyonun toparlanma kapasitesini ölçüyor ve ileride farklı sorulara cevap verecekler.

**Taşıyıcı özeti.** Çözme kaydı girilmiş taşıyıcının detay sayfasında üç sayı görünür: kaç embriyodan kaçı canlı, sağkalım yüzdesi ve ortalama canlılık oranı.

---

# v3.5 — gezinme düzeltmeleri

## Üst çubuk sabitlendi

Hangi ekranda olduğunu gösteren üst çubuk artık kaydırırken de görünür kalıyor. Uzun formlarda (ICSI, çözme) aşağı indiğinde hangi aşamada olduğunu kaybetmiyorsun.

## Çözme ekranına cycle'dan erişim

Çözme, taşıyıcı bazlı olduğu için cryo haritasından geçmek gerekiyordu ve hastanın içinden görünmüyordu. Artık üç giriş var:

- **Cycle kartında "Çözme (thaw)" düğmesi** → o cycle'ın embriyolarını içeren taşıyıcıları listeler, her birinin yanında **Çöz** düğmesi
- **Vitrifikasyon ekranında** dondurulmuş her embriyonun altında **çöz** bağlantısı
- **Cryo haritasından** taşıyıcıya girip **Bu taşıyıcıyı çöz**

Cycle çözme listesi ikiye ayrılır: tankta duranlar (çözülebilir) ve çözülmüş olanlar (geçmiş kayıt).

## Boşalan taşıyıcı temizliği

Bir embriyo başka bir taşıyıcıya taşındığında eski taşıyıcı "dolu" görünmeye devam ediyordu — haritada var olmayan bir dolu yer gibi. Artık son embriyo da çıkınca taşıyıcı otomatik "boşaltıldı" işaretleniyor ve konumu haritada boşa düşüyor.

---

# v3.6 — transfer

Cycle kartındaki **Transfer** düğmesinden. Göç gerekmiyor.

## Hangi embriyolar listelenir

**Hastanın tüm cycle'larından** transfer edilebilir embriyolar. Bu FET için gerekli: 2026-0417 cycle'ında dondurulan embriyoyu, aylar sonra açılan FET cycle'ında transfer edersin.

Listelenenler: blastokist, morula, kavitasyon, gün 2/3 aşamasındaki taze embriyolar; çözülmüş (canlı veya kısmi hasarlı) embriyolar. Dejenere, arrest, discard ve zaten transfer edilmiş olanlar listelenmez.

## Taze / donmuş ayrımı otomatik

Embriyonun çözme kaydı varsa **donmuş transfer**, yoksa **taze** olarak kaydedilir. Elle seçmene gerek yok, zaten kayıttan çıkıyor.

## Şema açısından

Transfer kaydı iki cycle'ı birbirine bağlar:

- `specimen.cycle_id` — embriyonun **geldiği** cycle (OPU'nun yapıldığı)
- `olay.tr_cycle_id` — transferin **yapıldığı** cycle (FET ise yeni cycle)

Embriyo kendi cycle'ında kalır, transfer ayrı bir cycle'a bağlanır. Böylece "hangi stimülasyondan gelen embriyo, hangi hazırlıkta transfer edildi" sorusu cevaplanabilir olur — ayrı tablolar kurulsaydı bu bağ kopardı.

## Geri alma

**Kaydı geri al** embriyoyu transfer öncesi durumuna döndürür ve tekrar listede görünür yapar. Çözülmüşse `cozuldu`, taze ise son blastokist değerlendirmesine göre (`blastokist`, `morula`, `kavitasyon`) geri döner.

Kalan tek aşama: gebelik sonucu.

---

# v3.7 — fotoğraf düzeltmeleri (göç 014)

## Oosite bağlanmayan fotoğraflar görünmüyordu

Fotoğraf ekleme ekranında "Oosite bağlama — cycle arşivine koy" seçilirse fotoğraf kaydediliyor ama hiçbir ekranda gösterilmiyordu. Kayboldu sanılıyordu.

Cycle kartına **Cycle arşivi** kartı eklendi: oosite bağlanmamış fotoğraflar orada listeleniyor, dokununca tam ekran açılıyor, her birinde silme düğmesi var. Arşivde fotoğraf yoksa kart hiç görünmüyor.

## Blastokist günleri aşama listesinde yoktu

Blastokist ekranı gün 4, 5, 6 ve 7 kaydı tutuyordu ama fotoğraf aşama listesinde karşılıkları yoktu. Eklendi: **Gün 4, Gün 5, Gün 6, Gün 7**.

Blastokist ekranındaki "Fotoğraf ekle" bağlantısı artık bulunduğun günü otomatik seçiyor — gün 6'dayken eklediğin fotoğraf gün 6'ya kaydediliyor. Ekranda gösterilen fotoğraf da önce o günün karesi, yoksa eski "blastokist" kayıtları, yoksa en son kare.

Eski `blastokist` aşaması korundu ve "Blastokist (gün belirtilmemiş)" olarak etiketlendi — daha önce yüklediğin fotoğraflar kaybolmadı.

Yükseltme: `python goc_014.py`

---

# v3.8 — aşamaya bağlı fotoğraf ve snapshot alma

## Fotoğraf devralma kaldırıldı

Her ekran kendi aşamasının fotoğrafı yoksa bir öncekini gösteriyordu. Gün 6 ekranında gün 3 karesini görmek yanıltıcıydı — o kare o güne aitmiş gibi duruyordu.

Artık **her ekran yalnızca kendi aşamasının fotoğrafını gösterir.** Yoksa "Bu aşamaya ait fotoğraf yok" der ve ekleme bağlantısı sunar. Gün 4, 5, 6, 7 birbirinden bağımsız.

## Snapshot'tan doğrudan ekleme

Denüdasyon dışındaki ekranlarda (ICSI, fertilizasyon, gün 2/3, blastokist) snapshot klasöründe bekleyen kare varsa ekranın üstünde vurgulu bir kart çıkar:

- Bekleyen **en yeni** karenin önizlemesi
- **"Bu kareyi oosit N'e ekle"** — tek dokunuşla o oosite ve o aşamaya bağlar
- Birden fazla bekliyorsa **"N karenin hepsini ekle"**

Kare eklendikten sonra kuyruktan düşer ve aynı ekrana geri dönersin. Klasörde bekleyen kalmayınca kart görünmez.

Akış artık şu: mikroskopta snapshot al → ekranda "bu kareyi ekle" → devam. Klasörü izleme, aşama seçme, oosit seçme adımları kalktı.

Elle yükleme (dış kaynaktan gelen dosyalar için) yerinde duruyor.

## Arşivi toplu silme

Cycle arşivi kartındaki **arşivi temizle** bağlantısı. Onay ekranı silinecek fotoğrafları küçük kareler halinde gösterir (dokununca tam ekran), altında her birinin aşaması, dosya adı ve kaynağı (kamera / elle) listelenir.

Onay için **fotoğraf sayısını yazman** gerekiyor — tek tıkla giden bir şey yok.

Yalnızca oosite bağlanmamış arşiv fotoğrafları silinir; oositlere bağlı fotoğraflar etkilenmez. Kameradan gelenlerde kaynak klasördeki orijinal dosyaya dokunulmaz ve dosyalar tekrar eşleştirilebilir hale gelir. Silmeler `degisiklik_log`'a yazılır.

Tek tek silmek için her fotoğrafın köşesindeki × kalmaya devam ediyor.

---

# v4.0 — arşivleme ve kalıcı silme kullanıcı kararına bırakıldı

Önceden karar program tarafından veriliyordu: veri varsa zorunlu arşivleme, yoksa silme. Artık **sen seçiyorsun.**

## Hasta ve cycle silme ekranları

Ekran önce bağlı kayıtları sayar (cycle, oosit, işlem kaydı, fotoğraf, sperm örneği, taşıyıcı, PGT ve gebelik sonucu), sonra iki seçenek sunar:

**Arşivle / İptal et** — veri korunur, listeden kalkar, geri alınabilir.

**Kalıcı olarak sil** — kayıt ve ona bağlı her şey veritabanından ve diskten silinir.

## Kalıcı silme için üç onay

1. Dosya numarasını (veya lab kayıt numarasını) yaz
2. İkinci kutuya **SIL** yaz
3. Tarayıcı onay penceresinde kaç kaydın silineceğini görüp onayla

Kalıcı sil seçilene kadar ikinci onay kutusu ve kırmızı uyarı görünmez.

## Neler siliniyor

Cycle silindiğinde: oositler, işlem kayıtları, bulgular, fotoğraflar (**arşiv klasöründeki dosyalar dahil**), sperm örneği ve analizleri, PGT sonuçları, beta hCG ve gebelik sonucu.

Boşalan taşıyıcılar silinir ve konumları cryo haritasında serbest kalır. Başka cycle'lardan bu cycle'a yapılmış transfer kayıtları iptal işaretlenir — o embriyolar silinmez, sadece transfer bağı kopar.

Hasta silindiğinde tüm cycle'ları için aynısı yapılır.

## Silme kaydı

Kalıcı silmeler `degisiklik_log`'a `KALICI_SILME` olarak yazılır ve ne silindiğinin özetini içerir:

```
dosya 77001 · Silinecek Hasta · 1 cycle · 3 oosit · 3 goruntu
```

Kaydın kendisi gider ama silindiğine dair iz kalır — kim, ne zaman, ne sildi.

## Bir uyarı

Klinik kayıtların saklanmasına ilişkin yükümlülükler var. Kalıcı silme yanlış açılmış kayıtlar ve hukuken gerekli haller için; rutin temizlik için değil. Ekranlarda da bu hatırlatma duruyor. Şüphedeysen arşivle — arşiv her zaman geri alınabilir, silme alınamaz.

## Transfere gitmiş kayıtlar silinemez

Bir cycle'ın veya hastanın **aktif transfer kaydı** varsa kalıcı silme seçeneği hiç görünmez. Ekranda gerekçe ve transfer kayıtlarının listesi çıkar (hangi cycle, hangi oosit, ne zaman, hangi cycle'da transfer edildi).

Sunucu tarafında da aynı kontrol var — ekranı atlayıp doğrudan istek gönderilse bile reddedilir.

Kilit iki yönlü çalışır: cycle'ın embriyoları başka bir cycle'da transfer edilmişse de, cycle bir FET olarak başka cycle'ın embriyolarının transfer edildiği yer ise de silinemez.

Bu durumda **arşivle / iptal et** seçenekleri çalışmaya devam eder.

Transfer kaydı geri alınırsa (yanlış girilmişse) kilit açılır ve silme seçeneği geri gelir.

**Yanlışlıkla açılmış kayıtlar etkilenmez:** hiç transferi olmayan hasta ve cycle'lar eskisi gibi kalıcı olarak silinebilir.

---

# v4.5 — arayüz düzenlemeleri

**Cryo bağlantısı taşındı.** Üst çubukta kullanıcı kodunun yanında duruyordu; hasta listesinde "Yeni hasta"nın altına ikincil düğme olarak alındı. Üst çubukta artık sadece çıkış var.

**Cycle formunda sıra değişti.** Klinik protokol artık zamanlar ve OPU bölümünün üstünde — tedavi bilgisi önce, laboratuvar bilgisi sonra.

**Oosit alanları netleştirildi.** "Sağ oosit / Sol oosit" yerine **"Sağ overden toplanan / Sol overden toplanan"**, üstünde "OPU'da toplanan oosit sayıları" açıklaması. Cycle kartındaki özet de "Toplanan oosit" oldu.

**Denüdasyon zamanı kendi ekranına taşındı.** Cycle formundan kaldırıldı, denüdasyon ekranının üstüne alındı. İlk oosit kaydedildiğinde otomatik doluyor, gerekirse oradan düzeltiliyor. Değişiklik `degisiklik_log`'a yazılıyor.

Mevcut değerler korundu: cycle düzenleme ekranında denüdasyon zamanı gizli alanda taşınıyor, düzenleme yapınca silinmiyor.

---

# v4.4 — silme hatası düzeltildi

Denüdasyon ekranında **"Atla"** denen kareler `kaynak_dosya` tablosuna cycle'a bağlı bir satır bırakıyor (aynı dosya tekrar kuyruğa girmesin diye). Bu satırlar hiçbir görüntüye bağlı olmadığı için kalıcı silme adımlarında temizlenmiyordu ve cycle silinemiyordu.

Belirtisi şuydu: hastanın hiç oositi, işlemi, fotoğrafı olmamasına rağmen silme "FOREIGN KEY constraint failed" hatası veriyordu.

Silme artık bu satırları da temizliyor. `teshis_silme.py` de bu tabloyu tarıyor.

---

# v4.6 — aşamalar arası gezinme

Her aşama ekranının altında üç düğmeli bir çubuk var:

```
‹ Önceki aşama    |    Cycle    |    Sonraki aşama ›
```

Ortadaki düğme cycle ana sayfasına döner ve kaçıncı aşamada olduğunu gösterir (3/8 gibi).

Sıra: Denüdasyon → ICSI → Fertilizasyon → Gün 2/3 → Blastokist → Vitrifikasyon → Çözme → Transfer

İlk aşamada "önceki", son aşamada "sonraki" düğmesi görünmez ama yer tutar; düğmeler yerinden oynamaz.

Böylece bir cycle'ı baştan sona işlerken her aşamadan sonra cycle sayfasına dönüp yeni ekran seçmek gerekmiyor.

---

# v4.7 — snapshot toplu eşleştirme

Denüdasyon dışındaki aşamalarda da mikroskoptan alınan kareleri sırayla oositlere dağıtabilirsin.

## Nereden

- Cycle kartında **Snapshot eşleştirme** düğmesi
- Her aşama ekranındaki snapshot kartının altında **toplu eşleştir (N kare)** bağlantısı

## Nasıl çalışır

Ekranın üstünde aşama seçici var — kareler hangi aşamaya kaydedilecekse onu seçersin (ICSI, gün 5, thaw sonrası, ne gerekiyorsa).

Altında bekleyen ilk kare büyük gösterilir, onun altında oosit numaraları. **Numaraya dokunursun, kare o oosite eklenir** ve sıradaki kare gelir; hedef otomatik olarak bir sonraki oosite kayar.

- Çerçeveli numara sıradaki hedeftir
- Numaranın altındaki küçük sayı o aşamada kaç kare olduğunu gösterir
- Yeşilimsi numaralar o aşamada zaten fotoğrafı olanlar
- Aynı oosite birden fazla kare eklemek için numaraya tekrar dokunursun
- **Bu kareyi atla** ile bir kareyi hiç kullanmadan geçersin

Kuyruk bitince ekran bunu söyler.

## Tek karelik hızlı ekleme duruyor

Aşama ekranlarındaki snapshot kartı ("Bu kareyi oosit N'e ekle") aynen kalıyor. Tek kare için o daha hızlı; birden çok kareyi farklı oositlere dağıtacaksan toplu eşleştirme ekranı daha uygun.

---

# v4.8 — adlandırma ve yerleşim

## "Snapshot" yerine genel terimler

"Snapshot" bazı kamera yazılımlarının kendi terimi. Farklı sistem kullanan laboratuvarlarda karışıklık yaratmasın diye ekranlardaki metinler genelleştirildi:

| Eski | Yeni |
|---|---|
| Snapshot eşleştirme | Görüntü eşleştirme |
| Snapshot klasöründe N kare bekliyor | Kamera klasöründe N kare bekliyor |
| Snapshot klasörü bulunamadı | Kamera klasörü bulunamadı |
| Snapshot alıp sayfayı yenile | Kameradan kare alıp sayfayı yenile |

Veritabanı alan adları (`goruntu_kaynak_klasor`) değişmedi — sadece ekranda görünen metinler.

## Eşleştirme bağlantısı modüllerin içinde

Cycle kartındaki düğme kaldırıldı. Bunun yerine **her aşama ekranının içinde** bağlantı var:

- Kamera klasöründe bekleyen kare **varsa**: kartın altında "oositlere tek tek dağıt (N kare)"
- Bekleyen kare **yoksa**: fotoğraf alanının altında sade bir "Görüntü eşleştirme" bağlantısı

Böylece hangi aşamadaysan eşleştirme oradan başlıyor ve aşama seçili geliyor — cycle sayfasına dönüp aşamayı elle seçmen gerekmiyor.

---

# v5.0 — oosit bazında over tarafı (göç 015)

Daha önce sağ/sol bilgisi yalnızca cycle düzeyinde toplam sayı olarak tutuluyordu. Artık **her oosit hangi overden geldiğini taşıyor.**

## Nasıl girilir

Denüdasyon ekranının üstünde **Toplandığı over** seçicisi var: Belirtme / Sağ / Sol.

Seçim yapıştır: sağ overi seçtiğinde ondan sonra oluşturduğun tüm oositler sağ olarak işaretlenir. Sol overe geçerken seçiciyi değiştirirsin. Fotoğrafsız oositler de aynı tarafı alır.

## Nerede görünür

- **Izgara hücrelerinde** numaranın yanında küçük rozet: `S` (sağ), `L` (sol)
- **Aşama ekranlarının başlığında**: "Oosit 3 sağ"
- **Görüntü eşleştirme ekranında** numaraların üstünde

Taraf girilmemiş oositlerde rozet çıkmaz.

## Sonradan değiştirme

Oosit karesine dokunup açılan panelde **Over: Sağ / Sol / —** düğmeleri var. Değişiklik `degisiklik_log`'a yazılır.

## Neden oosit düzeyinde

Cycle düzeyindeki `opu_sag_oosit` / `opu_sol_oosit` sayıları yerinde duruyor — onlar OPU'da sayılan toplamlar. Oosit düzeyindeki taraf ise farklı bir soruyu cevaplıyor: "sağ over oositlerinin fertilizasyon veya blastokist oranı sol overden farklı mı?" Bu soru ancak her oositin kendi tarafı kayıtlıysa sorulabilir.

Sıralı çalışmıyorsan (sağ ve sol dish'leri ayırmıyorsan) alanı boş bırakabilirsin; hiçbir yerde zorunlu değil.

---

# v5.1 — aşama kare şeridi

## Sorun

"Hepsini ekle" ile birden çok kare eklendiğinde arka planda hepsi kaydediliyordu ama ekran yalnızca **son kareyi** gösteriyordu. Diğerleri eklenmemiş gibi görünüyordu.

Ayrıca fotoğrafın altındaki "N kare" etiketi o oositin **tüm aşamalardaki** kare sayısını gösteriyordu — ICSI ekranında blastokist kareleri de sayılıyordu.

## Çözüm

Büyük fotoğrafın altına **kare şeridi** eklendi. O aşamaya ait tüm kareler küçük küçük yan yana duruyor:

- Kareye dokununca tam ekran açılıyor, dokunduğun kareden başlıyor
- Her karenin köşesinde kırmızı × ile silme
- Altında "N kare · bu aşamada" yazıyor

Şerit yalnızca **bulunduğun aşamanın** karelerini sayar ve gösterir. ICSI ekranındaki şerit ICSI karelerini, gün 6 ekranındaki gün 6 karelerini gösterir.

Yanıltıcı "N kare" etiketi kaldırıldı.

ICSI, fertilizasyon, gün 2/3 ve blastokist ekranlarının hepsinde var. Çözme ekranındaki iki yuvalı yapı zaten aynı mantıkla çalışıyordu.

---

# v5.3 — gebelik sonucu

Cycle kartındaki **Gebelik sonucu** düğmesinden. Göç gerekmiyor. Gezinme çubuğunda 9. ve son aşama.

## Ekranın bölümleri

**Transfer özeti** — bu cycle'da transfer edilen embriyolar (hangi oosit, hangi cycle'dan geldi, taze mi donmuş mu, ne zaman). Transfer kaydı yoksa uyarı çıkar.

**Beta hCG** — birden fazla ölçüm girilebilir. Her ölçümde değer ve zaman. Ardışık iki ölçüm arasında **artış hızı otomatik hesaplanır**: "48 saatte 2.49 kat". Tek tek silinebilir.

Değer sayı olarak saklanıyor, pozitif/negatif olarak değil. Eşiği istediğin zaman istediğin gibi uygularsın; pozitif/negatif yazılsaydı değer bir daha geri gelmezdi.

**Klinik gebelik** — var / yok / bilinmiyor, artı gebelik kesesi sayısı.

**Fetal kalp atımı** — pozitif / negatif / bilinmiyor, artı kontrol zamanı.

**Sonlanma** — canlı doğum, abortus, biyokimyasal gebelik, ektopik, devam ediyor, takip kaybı. Yanında doğum zamanı ve bebek sayısı.

## Zamanla güncellenen kayıt

Bu kayıt tek seferde dolmaz. Transferden sonra "devam ediyor", dokuz ay sonra "canlı doğum" olur. Tekrar kaydettiğinde mükerrer satır oluşmaz, mevcut güncellenir ve değişiklik `degisiklik_log`'a yazılır. Ekranın altında son güncelleme zamanı görünür.

**Takip kaybı ayrı bir seçenek.** Ulaşılamayan hastayı "hayır" olarak kaydedersen sonuç oranların yanlış çıkar; bilinmeyen ile olumsuz farklı şeylerdir.

## Sonuç neden cycle düzeyinde

İki embriyo transfer edilip tek gebelik olduğunda hangisinin tuttuğu bilinemez. Bu yüzden sonuç transferin yapıldığı cycle'a bağlanır, embriyoya değil. Embriyo–sonuç ilişkisi kuracak analizlerde tek embriyolu transferler filtrelenir.

---

## Akış tamamlandı

Denüdasyon → ICSI → Fertilizasyon → Gün 2/3 → Blastokist → Vitrifikasyon → Çözme → Transfer → Gebelik sonucu

Kalan tek modül: biyopsi / PGT.

---

# v5.4 — tedavi tipi ve FET akışı (göç 016)

## Yükseltme

```
python3 goc_016.py
```

Veritabanındaki `cycle_tipi` kısıtı sadece taze/fet kabul ediyordu; göç bunu genişletiyor. Tablo yeniden oluşturuluyor ama **veri korunuyor** — script sonunda kırık referans kontrolü de yapıyor.

## Tedavi tipi

"Tip" başlığı **Tedavi tipi** oldu ve üç seçenek var:

- **Taze**
- **FET (donmuş embriyo transferi)**
- **Oosit dondurma**

## Tipe göre aşamalar

Cycle kartında yalnızca o tedaviye uygun aşama düğmeleri görünür. Gezinme çubuğu da buna göre daralır.

| Tedavi tipi | Aşamalar |
|---|---|
| Taze | Denüdasyon → ICSI → Fertilizasyon → Gün 2/3 → Blastokist → Vitrifikasyon → Çözme → Transfer → Gebelik (9) |
| FET | Çözme → Transfer → Gebelik (3) |
| Oosit dondurma | Denüdasyon → Vitrifikasyon → Çözme (3) |

FET cycle'ında denüdasyon, ICSI, fertilizasyon gibi ekranlar hiç gösterilmez — o embriyolar zaten önceki tedavide işlenmiş.

## FET çözme listesi

FET cycle'ının çözme ekranı **hastanın tüm tedavilerindeki taşıyıcıları** listeler; dondurulan embriyo başka bir cycle'dan gelir. Her taşıyıcının altında dondurulduğu cycle yazar.

Taze cycle'larda liste eskisi gibi yalnızca o cycle'ın taşıyıcılarını gösterir.

## Çözme kaydı iki yerde de görünür

Çözme kaydı embriyonun **kendi cycle'ına** (dondurulduğu tedaviye) yazılır. Böylece:

- Kaynak cycle'ın çözme ekranında "Çözülmüş taşıyıcılar" bölümünde görünür
- FET cycle'ının çözme ekranında da görünür, çünkü o liste hastanın tüm taşıyıcılarını kapsar

Transfer ise ayrı: `tr_cycle_id` transferin yapıldığı FET cycle'ını gösterir. Yani embriyo nereden geldiğini de nerede kullanıldığını da taşır.

## Tedavi tipi adlandırması

"Taze" adı sonucu baştan varsayıyordu; freeze-all kararı çoğu zaman gün 5'te veriliyor. Etiket **"IVF / ICSI cycle'ı"** olarak değiştirildi — fertilizasyonun yapıldığını söylüyor, sonuç hakkında bir şey varsaymıyor.

Veritabanı kodu `taze` olarak kaldı; mevcut kayıtlar etkilenmedi.

Başlıklarda kısa gösterim kullanılıyor: **IVF/ICSI**, **FET**, **Oosit cryo**.

Freeze-all ayrı bir tedavi tipi değil — veriden çıkıyor: o cycle'da transfer kaydı yoksa ve embriyolar vitrifiye edilmişse freeze-all yapılmış demektir.

---

# v5.6 — tedavi tipi kodu netleştirildi (göç 017)

## Neden

`taze` kodu iki farklı şeyi çağrıştırıyordu: tedavi tipi ve taze transfer. İleride "taze ET yapılan hastalar" gibi bir ayrım gerektiğinde karışıklık çıkarırdı.

Kod **`ivf_icsi`** oldu. Mevcut kayıtlar otomatik çevrildi.

## İki kavram ayrı yerlerde

| Alan | Nerede | Ne söyler |
|---|---|---|
| `cycle.cycle_tipi` | Cycle | Tedavi tipi: `ivf_icsi` / `fet` / `oosit_cryo` |
| `olay.tr_tipi` | Transfer kaydı | Transfer tipi: `taze` / `donmus` |

Transfer tipi zaten embriyonun çözme kaydı olup olmamasına göre otomatik belirleniyor. Yani "taze ET mi, donmuş ET mi" sorusu transfer düzeyinde cevaplı; tedavi tipiyle karışmıyor.

Bir IVF/ICSI cycle'ında hem taze transfer hem (kalanlar için) vitrifikasyon olabilir — bu yapı onu doğru temsil ediyor.

## Yükseltme

```
python3 goc_017.py
```

`lab.db` yedeği al; göç cycle tablosunu yeniden oluşturuyor. Script sonunda cycle dağılımını, transfer tiplerini ve kırık referans sayısını yazar.

---

# v5.8 — iki makine arasında sorunsuz taşıma

## Sorun

`yerel_ayar.json` klasör yollarını tutuyordu. Klasörün tamamı USB ile taşınınca bu dosya da gidiyor ve diğer makinede olmayan yolları arıyordu: Windows'ta `/Users/onurerturk/...`, Mac'te `C:\Users\Genel\...`. Her taşımada `yerel_kur.py` çalıştırmak gerekiyordu.

## Çözüm

**Ayar dosyası makine adına göre bölümlendi.** Her bilgisayarın kendi bölümü var, tek dosyada:

```json
{
  "Onur-Air":      { "goruntu_kaynak_klasor": "/Users/onurerturk/...", ... },
  "LAB-MINIPC":    { "goruntu_kaynak_klasor": "C:\\Users\\Genel\\...", ... }
}
```

Uygulama açılırken bu makinenin bölümüne bakar. Yoksa oluşturur, diğer makinelerin bölümlerine dokunmaz.

**Varsayılan yollar uygulama klasörüne göreli.** Yeni bir makinede `snapshot/` ve `arsiv/` klasörleri uygulama klasörünün altına düşer ve **otomatik oluşturulur**. Klasörle birlikte taşındıkları için her yerde çalışır.

**Kayıtlı bir yol bu makinede yoksa** sessizce varsayılana döner ve dosya güncellenir. Hata vermez.

## Sonuç

Klasörün tamamını (kod + `lab.db` + `arsiv`) USB ile taşıyıp doğrudan çalıştırabilirsin. Ayar yapmana gerek yok.

Kamera klasörünü başka bir yerde tutmak istersen `python yerel_kur.py` ile o makinenin yolunu değiştirirsin; diğer makinenin ayarı etkilenmez.

## Kural değişmedi

Aynı anda tek kopyaya kayıt gir. İki makinede birden kayıt girip sonra birini taşırsan diğerindekiler kaybolur — bunun teknik çözümü yok, birleştirme mümkün değil.

---

# v6.1 — Claude Code'a geçiş + düz klasör yapısı

## Ne değişti

**Proje artık bir git deposu.** `git init` yapıldı, ilk commit atıldı. Git yerel
çalışır, buluta bir şey gitmez. Amaç: her değişiklikten ön­ce/sonra "geri al"
imkânı ve neyin ne zaman değiştiğinin kaydı.

**`.gitignore` hasta verisini ve makineye özel ayarı depo dışında tutar:**
`lab.db`, `lab.db-journal/-wal/-shm`, `arsiv/`, `snapshot/`, `yedek/`,
`yedek.log`, `yerel_ayar.json`. Bunlar eskisi gibi USB ile taşınır. Kod
senkronizasyonu istersen GitHub'da **private** bir depo aç — hasta verisi zaten
ignore'da olduğu için depoya girmez.

**Klasör düzleştirildi.** v6.1'e kadar tüm kod bir `app/` alt klasöründeydi ve
çalıştırmak için `cd app` gerekiyordu. Artık dosyalar doğrudan proje klasörünün
(`Patient Data Center/`) kökünde. `db.py` yolları `Path(__file__).parent`'a
göreli olduğu için kod bundan etkilenmedi; sadece `cd app` adımı kalktı.

## Neden düz yapı

Proje klasörünün kendisi git deposu ve çalışma dizini. Kodu tekrar `app/`
içine gömmek, üstte boş bir sarmalayıcı klasör bırakırdı. Tek katman = daha az
kafa karışıklığı.

## Eski sürüm bölümlerindeki `app/` referansları

Bu dosyadaki v0.1–v5.8 bölümleri o dönemin `app/` alt klasörü yapısına göre
yazılmış ("app klasörünün üzerine kopyala", "app klasöründe `python goc_XXX.py`"
gibi). Onlar tarihsel kayıt, olduğu gibi bırakıldı. Bugün geçerli olan:
komutları **proje klasörünün kökünde** çalıştır, `cd app` yok.

## Çalıştırma (güncel)

```bash
python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Mac
python  -m uvicorn app:uygulama --host 0.0.0.0 --port 8000   # Windows
```

Göçler: `python3 goc_hepsi.py` (kök dizinde).

---

# v6.2 — androloji (sperm) modülü

## Ne eklendi

Cycle akışına **Denüdasyon'dan önce** yeni bir aşama: **Androloji**. Yalnızca
`ivf_icsi` tipinde görünür (`fet` ve `oosit_cryo`'da sperm yok).

Ekran üç bölüm:

1. **Örnek bilgisi** — alınma zamanı, abstinans günü, alınma yöntemi,
   likefaksiyon zamanı (tamamlandığı saat), hazırlama yöntemi ve zamanı, not.
2. **Makroskopik** — hacim, pH, görünüm/renk, viskozite.
3. **Bazal analiz (hazırlık öncesi)** ve **Hazırlık sonrası analiz** — WHO
   parametreleri: konsantrasyon, total motilite %, PR / NP / IM %, normal
   morfoloji %, vitalite %, TMSC, yuvarlak hücre, lökosit, aglütinasyon.

Bir cycle'da genelde **tek örnek**; yedek / ikinci örnek için "+ Yeni".
İşlem saatleri her yerde olduğu gibi elle düzenlenebilir, varsayılan "şu an".
Boş alan NULL kaydedilir.

## Şema

Tablolar (`sperm_ornek`, `sperm_analiz`) ve `sperm_alinma` / `sperm_hazirlama`
/ `viskozite` listeleri şemada zaten vardı; kalıcı silme kaskadı da sperm
kayıtlarını zaten temizliyordu. Eksik olan ekranlar, rotalar ve şu ekler:

**`goc_019.py`** (idempotent):
- `sperm_analiz` tablosuna: `total_motil_yuzde`, `morfoloji_normal_yuzde`,
  `vitalite_yuzde`, `yuvarlak_hucre_milyon_ml`, `lokosit_milyon_ml`,
  `aglutinasyon`.
- `sperm_hazirlama` listesine: Gradient + swim-up, MACS, PICSI, Mikroakışkan
  (ZyMōt), TESE örneği işleme.
- `sperm_alinma` listesine: Kesintili ilişki (kondom), Elektroejakülasyon,
  Retrograd ejakülasyon, mikroTESE, PESA.
- Yeni listeler: `sperm_aglutinasyon` (Yok / İzole / Hafif / Orta / Ağır),
  `sperm_gorunum` (Normal / Berrak / Sarımsı / Kırmızı-kahve / Bulanık).

Listeleri sonradan düzenlemek: `python liste_duzenle.py sperm_hazirlama` vb.

## Neden bu tasarım

- **Denüdasyon'dan önce**, çünkü sperm hazırlığı klinik akışta oositler
  işlenmeden yapılır ve ICSI'ye girecek örneği belirler.
- **Bazal / hazırlık sonrası ayrı satır** (`asama` kolonu) — aynı tabloda iki
  kayıt; hazırlık öncesi ve sonrası değerler yan yana okunabilsin, geri
  kazanım (recovery) değerlendirilebilsin diye.
- **Makroskopik alanlar örnekte, mikroskopik alanlar analizde** — makroskopik
  bulgu örnek başına tek; mikroskopik değerlendirme her aşamada tekrarlanır.

## Bilinmeyen / sonra netleşecek

Hazırlama ve alınma yöntemi listeleri makul bir varsayılanla dolduruldu;
laboratuvarın kendi listesi netleşince `liste_duzenle.py` ile düzenlenecek.

---

# v6.3 — "İşlemi yapan" alanı (tüm aşamalar)

## Ne eklendi

Her aşama ekranının **en altına**, elle yazılan bir **"İşlemi yapan"** alanı:
androloji, denüdasyon, ICSI, fertilizasyon, gün 2/3, blastokist, vitrifikasyon,
çözme, transfer, gebelik.

Kaydı giren kullanıcıdan (`kullanici_id`) ayrıdır — CLAUDE.md'deki "saatler
sonradan girilebilir" mantığıyla aynı: aşamayı fiilen yapan kişi, bilgisayara
giren kişi olmayabilir. **Serbest metin** (açılır liste değil) — hesabı olmayan
biri de yazılabilsin diye. **Aşama başına tek değer**, kaydedince ekranda
kalır, sonradan düzeltilebilir; değişiklikler `degisiklik_log`'a yazılır.

## Şema

**`goc_020.py`** (idempotent) — yeni tablo:

```
islem_yapan (id, lab_id, cycle_id, asama, yapan_ad, zaman, kullanici_id)
UNIQUE (cycle_id, asama)
```

`sema_guncel.sql`'e de eklendi (sıfırdan kurulum için). Cycle kalıcı silme
kaskadına `DELETE FROM islem_yapan` eklendi (FK bütünlüğü).

## Nasıl çalışıyor

- Paylaşılan şablon parçası `_islem_yapan.html` → `{{ iy.kutu(c.id, "asama") }}`
  her aşama şablonunun en altında, `gez.cubuk`'tan hemen önce.
- Mevcut değer, Jinja global `islem_yapan_ad(cycle_id, asama)` ile okunur —
  aşama GET rotalarına dokunulmadı.
- Kaydetme: `POST /cycle/{id}/islem-yapan` (asama + yapan_ad), `Referer`'a
  geri döner. Geçersiz aşama anahtarı yazılmaz.

## Neden bu tasarım

Değeri her aşama tablosuna (`olay`, `sperm_ornek`, `specimen`...) ayrı kolon
olarak eklemek ~12 rotayı ve yazma mantığını değiştirmeyi gerektirirdi
(CLAUDE.md tuzak #1: toplu değişiklik). Bunun yerine tek tablo + tek paylaşılan
kutu: mevcut kayıt mantığına hiç dokunulmadı, riski düşük, sonradan cycle
kartında/geçmişte göstermek kolay.

---

# v6.4 — arşiv hasta dosya numarasına göre + iki sistemde güvenli yollar

## Ne değişti

Arşiv klasör yapısı:

```
önce:  arsiv/<yıl>/<cycle no>/<dosya>        arsiv/2026/2026-0001/...
sonra: arsiv/<hasta dosya no>/<cycle no>/    arsiv/527078/2026-0001/...
```

Yıl zaten cycle numarasının içinde (`2026-0001`), bilgi kaybı yok. Artık bir
hastanın bütün cycle'ları ve görüntüleri Finder / Dosya Gezgini'nde tek klasörde.

**`goc_021.py`** dosyaları taşır **ve** veritabanındaki yolları günceller;
boşalan eski klasörleri siler. Dosyası bulunamayan kayda dokunmaz, bildirir.
Birden fazla çalıştırılabilir.

## Fotoğraflar zaten kaynaktan bağımsızdı

Bu sürümde değişmedi, ama not: bir görüntü bir modüle kaydedildiğinde arşive
**kopyalanır**, kaynağa dokunulmaz. Kamera klasörü (`snapshot/`) temizlense
veya oradaki dosya silinse bile program görüntüyü arşivden gösterir.
Veritabanı **göreli** yol saklar (`527078/2026-0001/...`), makineden bağımsız.

Korunmayan tek şey `arsiv/` klasörünün kendisinin silinmesi — `yedek.py` bu
yüzden `arsiv/`'i de yedekliyor.

## Hasta adı neden klasör adında değil

Sadece dosya numarası kullanılıyor. Üç sebep:

1. **macOS NFD / Windows NFC.** macOS dosya adlarını ayrıştırılmış Unicode ile
   saklar (`u` + birleşen umlaut), Windows birleştirilmiş (`ü`). Klasör USB ile
   taşınınca Türkçe harfli yollar eşleşmeyebilir.
2. **Windows yasakları.** `< > : " / \ | ? *`, sondaki nokta/boşluk ve `CON`,
   `NUL`, `COM1`... ayrılmış adları kabul edilmez.
3. **Ad değişir.** Evlilik veya düzeltmede hasta adı değişince eski yollar
   bozulurdu. Dosya no değişmez.

Hangi numaranın kime ait olduğu zaten programda görünüyor.

## `guvenli_ad()` — yeni ortak süzgeç

`goruntuler.py` içindeki bu fonksiyon yola giren her parçayı temizler: NFC'ye
normalize eder, Windows'un yasakladığı karakterleri `_` yapar, sondaki
nokta/boşluğu atar, ayrılmış adların önüne `_` koyar, boşsa varsayılana düşer.
Klasör adlarında ve üretilen dosya adlarında kullanılıyor.

Yeni bir yerde kullanıcı verisinden yol parçası üretirsen bunu kullan.

---

# v6.5 — örnek kodu ve aşamaya göre isimlendirme

## Örnek kodu

Her örnek artık hasta dosya numarasını da içeren tam bir kodla anılıyor:

```
527078 - 2026-0001 - 03
  │         │        └ cycle içindeki sıra
  │         └ cycle no
  └ hasta dosya no
```

`specimen.id` **değişmedi** (`2026-0001-03`) — dört tablonun (`olay`, `goruntu`,
`specimen_bulgu`, `pgt_sonuc`) yabancı anahtarı, değiştirmek riskli ve
gereksiz. Kod, gösterim ve dosya adı için `ornek_kodu()` ile üretiliyor.

**Dosya adları** artık kodu kullanıyor, kaynak resmin adını değil:

```
527078-2026-0001-03_gun5_20260906-224440.jpg
└ kod ────────────┘ └aşama┘ └ arşivlenme zamanı
```

Dosya klasöründen çıkarılıp bir yere kopyalansa bile hangi hasta, hangi cycle,
kaçıncı örnek, hangi aşama olduğu adından okunur. Kaynak resmin adı
(`oocyte2.jpg`) yalnızca `goruntu.orijinal_dosya_adi` alanında iz olarak
kalıyor, hiçbir ekranda gösterilmiyor.

**`goc_022.py`** mevcut dosyaları yeniden adlandırır ve veritabanı yollarını
günceller. İdempotent.

## Aşamaya göre isim — asıl karışıklık buydu

Oosit → zigot → embriyo **aynı örnektir**; kod bilerek değişmez, yoksa "bu
blastokist hangi oositten çıktı?" sorusu cevapsız kalır (soyağacı = akreditasyon
gereği). Ama ekranlar her aşamada "Oosit 3" yazıyordu — gün 5 blastokiste
bakarken "Oosit 3" görmek yanıltıcıydı. Artık ekran örneğin **o anki halini**
yazıyor:

| Aşama | Etiket |
|---|---|
| Denüdasyon, ICSI | Oosit 3 |
| Fertilizasyon | Zigot 3 |
| Gün 2 / 3 | Cleavage 3 |
| Blastokist | Blastokist 3 |
| Vitrifikasyon / Çözme / Transfer / Gebelik | Embriyo 3 — **oosit cryo cycle'ında Oosit 3** |

`app.py` içindeki `ASAMA_ORNEK_ADI` + `ornek_adi(asama, cycle_tipi)` bunu
belirliyor; Jinja global olarak şablonlardan çağrılıyor.

## Silme ekranları

Kalıcı silmeden önce kimliği doğrulayabilmek için her silme ekranı artık
aşama adı **ve tam kodu** gösteriyor: `Blastokist 1 · 527078-2026-0001-01 · Gün 5`.
Kaynak resim adı kaldırıldı — yerine örnek kodu ve zaman geldi.

---

# v6.6 — eş zamanlı kullanım (birden fazla personel)

Klinikte program mini PC'de sunucu olarak çalışıyor, personel telefondan
bağlanıyor — yani **birden fazla kullanıcı aynı anda** kayıt giriyor. Test
edince üç sorun çıktı, üçü de düzeltildi.

## 1. Numara yarışı — en ciddisi

`specimen_olustur()` "en yüksek sıra numarasını oku → bir artır → kaydet"
yapıyordu, arada kilit yoktu. İki personel aynı cycle'a aynı anda oosit
eklerse ikisi de aynı numarayı hesaplıyordu.

Ölçüm — 8 personel aynı cycle'a aynı anda oosit ekliyor:

```
önce:   1 başarılı, 7 HATA (UNIQUE constraint failed: specimen.cycle_sira_no)
sonra:  8 başarılı, 0 hata — sıralar 1..8 kesintisiz
```

Gerçek hayattaki karşılığı: biri telefonla, biri mini PC'de aynı cycle'ı
denüde ederken birinin ekranı 500 veriyor ve girdiği oosit kayboluyordu.

**Çözüm:** `db.yazma_islemi()` — `BEGIN IMMEDIATE` ile okuma ve yazmayı tek
atomik işleme alır. Yazma kilidini baştan aldığı için ikinci kullanıcı bekler,
sonra bir sonraki numarayı alır.

> Yeni bir yerde "sıradaki numarayı üret" yazarsan bu yardımcıyı kullan.
> Dosya kopyalama gibi yavaş işleri işlemin **içine koyma** — kilit boyunca
> herkes bekler.

## 2. Okuyanlar yazana takılıyordu

`journal_mode = delete` idi: biri yazarken okuyanlar da bekliyordu. **WAL**
moduna alındı (`goc_023.py`, kalıcı ayar; `db.py` açılışta da garantiler).

```
4 okuyucu + 3 yazıcı eş zamanlı: 120 okuma, 30 yazma, 0 hata, 0,40 sn
```

Bekleme süresi de 5 → **15 saniye** çıkarıldı (`db.BEKLEME_SN`).

## 3. Aynı kareyi iki kişi bağlarsa

`goruntu_bagla()` kaynak kareyi arşive kopyalayıp iki kayıt yazıyordu; iki
personel aynı kareyi aynı anda bağlarsa ikincisi `kaynak_dosya.imza` birincil
anahtarında patlıyordu. Artık iki kayıt tek atomik işlemde ve kare alınmışsa
ikinci kullanıcı sessizce vazgeçiyor, **boşa alınan arşiv kopyası da siliniyor.**

Cycle numarasında da benzer bir açık vardı (kontrol ile INSERT arasında);
`sqlite3.IntegrityError` yakalanıp "bu numarayı az önce başkası aldı, sıradaki
boş numara: X" mesajı gösteriliyor.

## Kalan bilinen sınır

**Aynı kaydı iki kişi aynı anda düzenlerse son yazan kazanır** — çakışma
uyarısı yok, diğerinin girdiği sessizce gider. Nadir ve fark edilir olduğu için
şimdilik bırakıldı.

## Veritabanı ağ sürücüsüne konmamalı

SQLite dosya kilitleriyle çalışır; SMB/NFS paylaşımlarında kilitleme birçok
uygulamada hatalıdır (bozulma riski) ve **WAL ağ sürücüsünde hiç çalışmaz** —
SQLite sessizce eski moda döner, yani yukarıdaki iyileştirme kaybolur.

Buna ihtiyaç da yok: veritabanına **yalnızca mini PC** dokunuyor, diğer
cihazlar HTTP ile bağlanıyor. İkinci bir bilgisayardan girmek için orada
programı çalıştırma, tarayıcıdan `http://<mini-pc-ip>:8000` adresine git.

**Ağa taşınabilecek olan `arsiv/`** (fotoğraflar): disk dolunca
`python yerel_kur.py` ile `goruntu_arsiv_klasor` NAS yolunu gösterebilir,
kod değişikliği gerekmez. Veritabanı göreli yol sakladığı için eski kayıtlar da
yeni konumdan okunur. Ölçü: fotoğraf başına ~178 KB, cycle başına ~18 MB.

Veritabanının kendisi gerçekten merkezileşmesi gerekirse tek doğru yol
PostgreSQL'e geçmektir — ölçek bunu gerektirmiyor.

---

# v6.7 — çözme hangi tedavi için yapıldı (göç 024)

## Sorun

Donmuş embriyo doğduğu cycle'a bağlı kalır (`specimen.cycle_id` değişmez), FET
cycle'ı ile bağı **transfer** kaydı kurardı (`olay.tr_cycle_id` — v5.4).

Eksik olan: **transfere ulaşmayan çözme.** FET'te iki embriyo çözülüp ikisi de
canlı çıkmazsa transfer kaydı oluşmuyor, dolayısıyla o FET cycle'ında tek satır
iz kalmıyordu. Aylar sonra ikinci bir FET açıldığında çözme ekranı yine aynı
listeyi gösteriyordu; hangi çözmenin hangi tedaviye ait olduğu veriden
okunamıyordu. Cycle bazında sağkalım oranı da hesaplanamıyordu.

Embriyolog için başarısız çözme o FET'in kaydıdır — görünmesi gerekir.

## Çözüm: `olay.thaw_cycle_id`

`tr_cycle_id` ile aynı mantık, bir aşama önce:

| Alan | Ne söyler |
|---|---|
| `specimen.cycle_id` | embriyo **nereden geldi** — OPU/ICSI cycle'ı (değişmez) |
| `olay.thaw_cycle_id` | **hangi tedavi için çözüldü** (yeni) |
| `olay.tr_cycle_id` | **nerede transfer edildi** |

Artık üç soru da ayrı ayrı yanıtlanıyor ve çözme transfere ulaşmasa da kayıtta.

## Ekranda

**Çözme formunda** (`/cryo/tasiyici/<id>/thaw`) en üste bir seçim geldi: *"Bu
çözme hangi tedavi için?"* — hastanın tüm cycle'ları listelenir. FET'in çözme
ekranındaki **Çöz** düğmesi `?cycle=<id>` taşıdığı için doğru tedavi zaten
seçili gelir; cryo haritasından girilirse embriyonun kendi cycle'ı seçili olur
ve elle değiştirilebilir. Kaydedilmiş bir çözme yeniden açılırsa önceki seçim
korunur.

Seçim **elle değiştirilebilir olmalıydı**: taşıyıcı cryo haritasından da
çözülebiliyor, orada cycle bağlamı yok. Tahmin etmek yerine sormak, yanlış
tedaviye sessizce yazmaktan iyidir.

**FET cycle'ının çözme ekranına** "Bu tedavide çözülenler" kartı eklendi: örnek
kodu, sağkalım, canlılık %, re-expansion %, taşıyıcı, kaynak cycle ve
**transfer edildi / transfer edilmedi**. Üstte özet: `Canlı 1/2 (%50) · transfer
edilen 1`.

Taşıyıcı tek bir vitrifikasyon ekranından doldurulduğu için tek hastaya aittir.
Karışık bir taşıyıcı çıkarsa (elle veri düzeltmesi) seçim hiç sunulmaz, her
embriyo kendi kaynak cycle'ına yazılır — sessiz yanlış veri üretmez.

## Göç 024 ve geriye dönük doldurma

Mevcut çözme kayıtları boş kalmasın diye:

1. Embriyo sonradan transfer edilmişse → transferin yapıldığı cycle
2. Edilmemişse → çözmenin yazıldığı cycle (bugüne kadarki davranış)

Göç çalıştırılmadan da ekranlar açılır: `thaw_cycle_var()` kolonun varlığına bir
kez bakar, yoksa çözme ekranında `python goc_024.py` uyarısı çıkar ve yeni alan
yazılmaz (tuzak #3).

## Silme kaskadı

`thaw_cycle_id` de tıpkı `tr_cycle_id` gibi **başka bir cycle'a** işaret
edebiliyor. Kalıcı silmede bağı koparmadan `DELETE FROM cycle` denenirse
`FOREIGN KEY constraint failed` alınıyor (tuzak #4 — test edildi, hata
üretildiği doğrulandı). `cycle_tamamen_sil` artık bağı `NULL`'a çekiyor; çözme
kaydının kendisi silinmiyor, yalnızca hangi tedavi için olduğu bilinmez oluyor.

`teshis_silme.py` de güncellendi. Bu arada v6.3'ten kalma bir eksik çıktı:
`islem_yapan` adımı teşhis aracında yoktu, bu yüzden araç silinebilir bir hastayı
"CYCLE → FOREIGN KEY constraint failed" diye **yanlış** raporluyordu. Eklendi.

## Doğrulanan senaryo

2026-0001 (IVF/ICSI) cycle'ında iki blastokist vitrifiye edildi, 2026-0002 (FET)
cycle'ından çözüldü: biri canlı, biri dejenere. FET'in çözme ekranı
`Canlı 1/2 (%50) · transfer edilen 0` ve dejenere olan için "transfer edilmedi"
gösterdi. Canlı olan transfer edilince özet `transfer edilen 1` oldu. Kaynak
cycle'ın (2026-0001) ekranında bu liste **görünmedi** — çözme oraya ait değil.

---

# v6.8 — `yedek.py` ayarları uygulamayla aynı yerden okur

## Sorun

`yedek.py`'nin kendi `ayar()` fonksiyonu vardı ve `yerel_ayar.json`'ı **düz bir
sözlük** sanıyordu:

```python
d = json.loads(yerel.read_text())
if anahtar in d:            # {"yedek_klasor": "..."} bekliyor
    return str(d[anahtar])
```

v6.4'te `db.py` bu dosyayı makine adına göre bölümlü biçime çevirdi
(`{"vm": {"yedek_klasor": "..."}}` — her bilgisayarın kendi bölümü). Artık üst
seviyede yalnızca makine adı var, `"yedek_klasor" in d` hiçbir zaman tutmuyor.
Okuyucu sessizce bir alt seçeneğe, veritabanındaki değere düşüyordu — orada da
Windows mini PC'nin yolu yazılı: `E:\yedek`.

Sonuç, Mac'te argümansız `python3 yedek.py`:

```
Yedekleme basladi -> E:\yedek
Veritabani: lab_20260909_0957.db  (0.2 MB, 22 tablo, ...)
Yedekleme tamam.
```

`E:\yedek` POSIX'te yasak bir ad değil — sıradan bir dosya adıdır. Program
çalışma klasörünün altına **`E:\yedek` adında bir klasör** açtı, yedeği oraya
yazdı ve "tamam" dedi. Hata yok, çıkış kodu 0. En kötü yedekleme hatası budur:
yedek aldığını sanırsın.

## Çözüm

`yedek.py` artık `db.ayar()` kullanıyor — uygulamanın okuduğu kaynağın aynısı.
Yol ayarları makineye özgü dosyadan gelir, gerisi (`yedek_uyari_gun`,
`son_yedek`) veritabanından. Tek kaynak, iki okuyucu yok.

Öncelik sırası: **komut satırı argümanı → bu makinenin `yerel_ayar.json`
bölümü.** Argüman her zaman kazanır, ki elle test yapılabilsin.

Üç şey daha eklendi:

**1. Hedefin nereden geldiği yazılıyor.**

```
Yedekleme basladi -> /Users/onur/lab_yedek   (kaynak: MacBook ayari)
```

**2. Platforma uymayan yol reddediliyor.** Sürücü harfli bir yol
(`E:\yedek`) Mac/Linux'ta, `/` ile başlayan bir yol Windows'ta kabul edilmiyor:

```
HATA: 'E:\yedek' bu isletim sisteminin yolu degil (vm ayari).
      Yedek alinmadi. Bu makinenin hedefini 'python yerel_kur.py' ile ayarla.
```

Çıkış kodu 1 — Görev Zamanlayıcı başarısızlığı böyle görür. Bu, `db.ayar()`
düzeltmesinden bağımsız ikinci bir emniyet: ayar başka bir yoldan bozulsa bile
program yanlış yere yedek alıp "tamam" demez.

**3. Veritabanındaki eski değer farklıysa söyleniyor**, sessizce yok
sayılmıyor:

```
NOT: veritabanindaki yedek_klasor (E:\yedek) baska bir makineye ait, kullanilmadi.
```

## Windows mini PC'de dikkat

Yol ayarları artık **makineye özgü dosyadan** okunduğu için, veritabanındaki
`yedek_klasor = E:\yedek` (göç 008) yedek hedefini belirlemiyor. Klinikteki
makinede bir kez şu çalıştırılmalı:

```
python yerel_kur.py
```

ve `yedek_klasor` `E:\yedek` (ya da hangi diskse) olarak yazılmalı. Yapılmazsa
o makinenin varsayılanı `D:\lab_yedek` olur — D: yoksa program hata verip durur
(sessiz başarı yok), D: varsa yedek yanlış diske gider. Ayarın amacı yedeğin
**farklı bir diskte** olması; bunu makine başına doğrulamak gerekiyor.

## Test edildi

- Argümansız çalıştırma → `~/lab_yedek`, cwd altında sahte klasör yok
- Makine ayarına `E:\yedek` konarak → reddedildi, çıkış kodu 1, klasör açılmadı
- Komut satırı argümanı → makine ayarını eziyor
- `son_yedek` veritabanına yazıldı; uygulama ana ekranı taze yedekte uyarı
  göstermedi, tarih elle eskitilince "Son yedek 39 gün önce alındı" uyarısı çıktı
- Arşiv kopyalama ve `integrity_check` doğrulaması bozulmadı

---

# v6.9 — OPU kendi ekranı + kurulum göçleri kendisi çalıştırıyor

## Sorun 1: androloji ekranında seçenekler boş

Kullanıcı yeni bir Windows kurulumunda üç şey bildirdi: androloji renk seçeneği
yok, aglütinasyon seçeneği yok, OPU'da işlemi yapan alanı yok. İlk ikisi aynı
kökten.

`sifirdan_kur.py` şemayı `sema_guncel.sql`'den kurar. O dosya `goc_019`,
`goc_021` ve `goc_022`'nin gerisinde kalmış. Temiz bir kurulum yapıp ölçtük:

| Eksik | Etkisi |
|---|---|
| `sperm_gorunum` listesi | Renk seçeneği boş |
| `sperm_aglutinasyon` listesi | Aglütinasyon seçeneği boş |
| `sperm_analiz`'de 6 kolon | Aglütinasyon, morfoloji, vitalite, lökosit kaydedilemez |
| `specimen.taraf` + `taraf` listesi | Denüdasyonda sağ/sol çalışmaz |
| `olay.thaw_canlilik`, `thaw_kontrol_zamani` | Çözmede canlılık kaydı |
| `tasiyici_tipi`, `tasiyici_renk` listeleri | Taşıyıcı ekranı |

Yani hata androloji ile sınırlı değildi; kullanıcının henüz açmadığı üç ekran
daha yarım çalışıyordu. Program **hata vermiyor** — sadece seçenekler boş
görünüyor, sebebi ekrandan anlaşılmıyor. Tuzak #3'ün en pahalı hâli.

### Çözüm: kurulum göçleri kendisi çalıştırır

`sifirdan_kur.py` sonunda `goc_hepsi.py`'yi alt süreç olarak çalıştırıyor.
Göçler zaten idempotent, tekrar çalışmalarının zararı yok. Başarısız olursa
uyarı basıp elle komutu gösteriyor, kurulumu sessizce yarım bırakmıyor.

`sema_guncel.sql`'i yeniden üretmek de bir seçenekti; kullanıcı bu yolu seçti.
Göçler her kurulumda çalıştığı için sonuç aynı yere varıyor, ama
`sema_guncel.sql` hâlâ güncel değil — CLAUDE.md onu "güncel şema referansı"
diye tanımlıyor, artık öyle değil. Ayrı bir işte tazelenmeli.

Doğrulandı — tek komutluk temiz kurulum sonrası:

```
sperm_gorunum      5 deger      specimen.taraf        var
sperm_aglutinasyon 5 deger      olay.thaw_canlilik    var
taraf              2 deger      sperm_analiz.aglutinasyon  var
tasiyici_tipi      5 deger      cycle.opu_hekim       var
tasiyici_renk      8 deger
```

## Sorun 2: OPU'da işlemi yapan yok

Bu bir hata değildi — OPU aşama olarak tanımlı değildi. `ASAMA_SIRASI`'ndaki 10
aşamanın hepsinde "işlemi yapan" kutusu var, ama OPU verileri (zaman, sağ/sol
oosit sayısı) cycle formunda duruyordu, kendi ekranı yoktu.

Kullanıcı kararı: **OPU'ya ayrı ekran, hem hekim hem embriyolog kaydedilsin.**

### İki kişi, iki ayrı yer — neden

| Kim | Nereye | Neden |
|---|---|---|
| **OPU Hekimi** | `cycle.opu_hekim` | Laboratuvar personeli değil. `opu_zamani` ile aynı satırda, cycle verisi. |
| **OPU Embriyoloğu** | `islem_yapan`, `asama='opu'` | Diğer on aşamayla aynı yol. Şema değişikliği gerekmiyor. |

`islem_yapan` tablosunda `UNIQUE(cycle_id, asama)` var — aşama başına tek kişi.
İkinci kişiyi oraya sığdırmak için `rol` kolonu eklemek ve bu kısıtı değiştirmek
gerekirdi; bu on aşamanın tamamını etkiler. Hekim zaten laboratuvar aşamasını
yapan kişi değil, dolayısıyla cycle verisi olarak durması hem daha doğru hem
daha az riskli.

### Aşama sırası

OPU **en başa** kondu: oositlerin kaynağı, denüdasyondan önce gelir.

- `ivf_icsi` → 11 aşama (OPU dahil)
- `oosit_cryo` → OPU, denüdasyon, vitrifikasyon, çözme
- `fet` → **OPU yok** — oosit toplanmaz, embriyo başka bir cycle'dan gelir

Gezinme çubuğu, cycle detaydaki aşama düğmeleri ve `islem_yapan` doğrulaması
`ASAMA_SIRASI`'ndan türediği için hepsi kendiliğinden güncellendi.

### "İşlemi yapan" etiketi artık değiştirilebilir

OPU'da iki kişi olduğu için alt kutunun "İşlemi yapan" demesi belirsiz kalıyordu.
`_islem_yapan.html` makrosu isteğe bağlı `etiket` ve `ipucu` parametresi aldı;
varsayılanlar aynı, **diğer on ekran hiç değişmedi** (test edildi). OPU'daki iki
alan **"OPU Hekimi"** ve **"OPU Embriyoloğu"**.

İlk yazımda alanların altına klinik açıklamalar koymuştum ("oositleri aspire
eden hekim", "folikül sıvısını tarayıp oositleri bulan kişi"). Bunlar bana ait
varsayımlardı ve kullanıcı ikincisinin doğru bir ifade olmadığını söyledi —
kaldırıldı. Etiketler kendi başına yeterince açık; uydurulmuş klinik tanım
ekranda kalmamalı (CLAUDE.md: klinik varsayım yapma, sor).

## Göç 025 ve göç çalıştırılmamış makine

`goc_025.py` yalnızca `cycle.opu_hekim` kolonunu ekler.

Göç çalıştırılmadan da ekran çalışmalı (tuzak #3). `opu_hekim_var()`,
`thaw_cycle_var()` ile aynı kalıp: kolon yoksa ekranda göç uyarısı çıkar, hekim
alanı gizlenir, diğer alanlar normal kaydedilir. Test edildi — kolonu silinmiş
bir veritabanında ekran HTTP 200 verdi, uyarı göründü, kayıt çalıştı, 500 yok.

## Test edildi

- Temiz kurulum tek komutla eksiksiz (yukarıdaki tablo)
- OPU ekranından zaman, sağ/sol oosit, hekim ve embriyolog kaydedildi;
  veritabanında `cycle.opu_hekim` ve `islem_yapan(asama='opu')` doğrulandı
- 11 aşama ekranının hepsi HTTP 200; diğer onunda etiket hâlâ "İşlemi yapan"
- FET cycle'ında OPU görünmüyor, `ivf_icsi` ve `oosit_cryo`'da görünüyor
- Göçsüz veritabanında OPU ekranı çökmüyor, uyarı gösteriyor

---

# v6.10 — `kullanici.py`: giriş sorunlarını çözen araç

## Sorun

Kullanıcı Mac'te giriş yapamadı. Arayüzde kullanıcı yönetimi ekranı yok
(bilinçli), şifreler scrypt ile karmalanıyor ve **geri okunamıyor**. Giriş
reddedilirse ekranda tek bir "hata" görünüyor; sebebin hangisi olduğu
anlaşılmıyor. `guvenlik.giris_yap` üç ayrı durumda `None` döndürüyor:

1. Kullanıcı adı yok
2. `aktif_mi = 0` — kullanıcı pasif
3. Şifre yanlış

Bunları ayırt etmenin tek yolu terminalde elle Python yazmaktı. Python'a yeni
başlamış bir kullanıcı için bu, tırnak ve girinti hatasıyla dolu bir yol.

## Çözüm

`kullanici.py` — `teshis.py` / `liste_duzenle.py` / `yerel_kur.py` ile aynı
ailede küçük bir yönetim aracı:

```
python3 kullanici.py                    kullanıcıları listele
python3 kullanici.py sifre <kullanici>  şifresini değiştir
python3 kullanici.py yeni               yeni kullanıcı ekle
python3 kullanici.py aktif <kullanici>  girişe tekrar izin ver
python3 kullanici.py pasif <kullanici>  girişi kapat
```

Argümansız çalıştırma sadece listelemiyor, **üç sebebi de hatırlatıyor** —
teşhis araçlarının işi bu.

## Kararlar

**Şifre değişince açık oturumlar düşürülür.** `oturum` satırları siliniyor.
Yoksa "şifreyi değiştirdim" yanıltıcı olurdu: eski şifreyle açılmış bir
tarayıcı 12 saat daha çalışmaya devam ederdi.

**Pasif kullanıcının şifresi değiştirilebilir, ama uyarı veriliyor.** Sıfırlayıp
"neden hâlâ giremiyorum" demesin diye; `aktif` komutu ekranda gösteriliyor.

**Pasif ≠ silinmiş.** Kullanıcı silinmiyor, `aktif_mi = 0` yapılıyor — girdiği
kayıtlar `kullanici_id` ile bağlı, silmek geçmişi bozar. Projenin "silme = iptal
işaretleme" kuralıyla aynı mantık.

**Şifre karması hiçbir zaman ekrana yazılmaz.** Liste çıktısında `sifre_hash`
kolonu yok.

**Kullanıcı adı küçük harfe çevrilir.** `giris_yap` da öyle arıyor, yani `ONUR`
ile `onur` aynı kullanıcı. Test edildi.

## Test edildi

- Listeleme; olmayan kullanıcı için anlaşılır hata
- Şifre sıfırlama → eski şifre reddedildi, yenisi kabul edildi
- 8 karakterden kısa ve birbirini tutmayan şifre reddedildi
- Pasif yapma → giriş reddedildi; tekrar aktif → giriş kabul edildi
- Pasif kullanıcının şifresi değiştirilince uyarı çıktı
- Yeni kullanıcı eklendi; aynı kullanıcı adı ikinci kez reddedildi
- Tarayıcıdan gerçek giriş: `ayse`, `onur` ve `ONUR` girdi, yanlış şifre giremedi

---

# v6.11 — şifre değiştirme, "şifremi unuttum", kullanıcı yönetimi ekranları

## En önemlisi: yetki kontrolü ilk kez var

`kullanici.rol` kolonu baştan beri vardı ama **kodda hiçbir yerde
kontrol edilmiyordu** — giriş yapan herkes her şeyi yapabiliyordu. Kullanıcı
silme ekranı bunu zorunlu kıldı: yetki olmadan herhangi bir personel yöneticiyi
silebilirdi.

`yonetici_kontrol(request)` eklendi, tüm yönetim rotalarının başında.
Ekranda düğmeyi gizlemek yetmiyor — sunucu da reddediyor. Test edildi:
embriyolog hesabıyla `/kullanicilar/yeni`, `/kullanici/1/durum` ve
`/kullanici/1/sifre` adreslerine doğrudan POST atıldı, üçü de `/hastalar`'a
döndü ve hiçbir şey değişmedi.

## "Şifremi unuttum" neden şifre sıfırlamıyor

Sistemde e-posta ve SMS yok, yani kimliği doğrulayacak **ikinci bir kanal yok**.
Doğrulamasız bir sıfırlama ekranı, iç ağdaki herkese yönetici şifresini
değiştirme ve tüm hasta verisine erişme hakkı verirdi — HTTPS de yok.

Kullanıcıya üç seçenek sunuldu (yönetici sıfırlasın / kurtarma kodu /
doğrulamasız sıfırlama); **yönetici sıfırlasın** seçildi.

Sayfa dolayısıyla:
- Hiçbir şey sıfırlamaz, kime başvurulacağını söyler
- **Kullanıcı adı listelemez** — giriş yapmamış birine kimlerin olduğunu söylemez
- Yönetici de kilitlenirse `python3 kullanici.py sifre <ad>` yolunu gösterir

## Kullanıcı silme: projenin silme kuralıyla aynı

11 tablo `kullanici.id`'ye bağlı (`goruntu`, `olay`, `degisiklik_log`,
`islem_yapan`, `sperm_analiz`...). Kayıt girmiş bir kullanıcıyı fiziksel silmek
"bu blastokisti kim değerlendirdi" sorusunu cevapsız bırakır.

Hasta silmedeki kalıbın aynısı:

| Durum | Ne olur |
|---|---|
| Kayıt girmiş | Kalıcı silinemez. Ekran hangi kayıtlardan kaç tane olduğunu sayar, "bunun yerine pasif yap" der |
| Hiç kaydı yok | Kullanıcı adı + `SIL` + tarayıcı onayı ile kalıcı silinir |
| Kendisi | Silinemez, pasif yapılamaz |
| Son aktif yönetici | Silinemez, pasif yapılamaz — yoksa yönetime kimse giremez |

Kayıt koruması hem ekranda hem sunucuda: form gösterilmiyor **ve** POST
reddediliyor (test edildi — ikinci bir yöneticiyle giriş yapılıp doğrudan POST
atıldı, "5 kaydı var" diye reddedildi).

## Şifre değişince oturumlar düşer

`sifre_yaz()` şifreyi değiştirir ve o kullanıcının `oturum` satırlarını siler.
Yoksa "şifreyi değiştirdim" yanıltıcı olurdu: eski şifreyle açılmış bir tarayıcı
12 saat daha çalışmaya devam ederdi. Kendi şifresini değiştiren kullanıcı da
çıkışa düşer ve yeniden giriş yapar.

**Kendi şifresini değiştirmek için mevcut şifre şart.** Açık kalmış bir
tarayıcıyı bulan biri hesabı ele geçiremesin diye.

## Ekranlar

| Yol | Kim | Ne yapar |
|---|---|---|
| `/sifre` | herkes | Kendi şifresini değiştirir (mevcut şifre ister) |
| `/sifremi-unuttum` | **giriş gerektirmez** | Bilgilendirir, sıfırlamaz |
| `/kullanicilar` | yönetici | Liste, ekleme, şifre sıfırlama, aktif/pasif |
| `/kullanici/<id>/sil` | yönetici | Bilinçli silme ekranı |

Bağlantılar: giriş ekranında "Şifremi unuttum", ana ekranda "Şifre değiştir"
ve (yalnızca yöneticiye) "Kullanıcılar".

`.minidugme.ikincil` stili eklendi — "Sil" ile "Pasif yap" aynı ağırlıkta
görünmemeli, pasif yapmak normal yol.

## Test edildi

- Giriş yapmadan `/sifremi-unuttum` açılıyor, kullanıcı adı sızdırmıyor;
  `/kullanicilar` giriş ekranına atıyor
- Embriyolog hesabında "Kullanıcılar" düğmesi görünmüyor; adresi elle yazınca
  ve doğrudan POST atınca reddediliyor
- Tek yöneticiyi pasif yapma / silme engellendi; kendi hesabını pasif yapma
  engellendi
- Kullanıcı ekleme: aynı kullanıcı adı, tutmayan şifreler reddedildi
- Silme: yanlış kullanıcı adı ve eksik `SIL` reddedildi, doğru onayla silindi
- Kayıt girmiş kullanıcı: ekranda form yok, POST reddedildi, kullanıcı duruyor
- Kendi şifresi: yanlış mevcut şifre, tutmayan tekrar, eskisiyle aynı reddedildi;
  tarayıcıyı atlayarak 3 karakterlik şifre POST edildi, sunucu reddetti
- Başarılı değişiklikte oturum düştü, eski şifre çalışmadı, yenisi çalıştı

---

# v6.12 — şifre değiştirme giriş ekranında, yönetici paneli

## Şifre değiştirme neden giriş ekranına taşındı

v6.11'de `/sifre` yalnızca giriş yaptıktan sonra açılıyordu. Kullanıcının
itirazı yerinde: şifresini değiştirmek isteyen biri zaten şifresini biliyor —
önce giriş yapıp sonra ayrı bir ekrana gitmesi gereksiz bir adım.

**Güvenliği düşürmüyor.** Ekran her iki durumda da **mevcut şifreyi** istiyor,
yani kimlik yine kanıtlanıyor. Giriş yapmışsa kullanıcı adı hazır gelir,
yapmamışsa kendisi yazar. Tek ekran, tek rota.

Yeni bir saldırı yüzeyi de açmıyor: `/giris` zaten şifre denenebilen bir
adres, `/sifre` fazladan bir şey vermiyor.

### Kullanıcı adı sızdırmama

Giriş yapmamış birine "böyle bir kullanıcı yok" demek, hangi kullanıcı
adlarının geçerli olduğunu söylemek demektir. Bu yüzden üç durumda da **tek ve
aynı** mesaj dönüyor:

- kullanıcı yok
- kullanıcı var, şifre yanlış
- kullanıcı pasif

Hepsi: *"Kullanıcı adı veya mevcut şifre yanlış."* Test edildi — var olan ve
olmayan kullanıcı için mesajlar birebir aynı çıktı.

Pasif kullanıcı bu yoldan da şifre değiştiremiyor (sorgu `aktif_mi = 1`
istiyor). Test edildi: pasif hesapla doğru şifre girildi, reddedildi ve karma
değişmedi.

## Yönetici paneli

`/kullanicilar` tek başına ana ekrandan asılı duruyordu. `/yonetim` bunları tek
yerde topluyor:

| Kart | Ne gösterir |
|---|---|
| Yedekleme | Son yedek, uyarı eşiği, nasıl alınacağı |
| Veritabanı | Hasta / cycle / örnek / fotoğraf / olay sayıları, dosya boyutu, kırık referans |
| Bu makinenin klasörleri | Makine adı + snapshot / arşiv / yedek yolları, her biri için "klasör var mı" |
| Kullanıcılar | Aktif–pasif sayısı, `/kullanicilar`'a bağlantı |

**Panel salt okunurdur.** Buradan hiçbir şey silinmez veya değiştirilmez —
ayarlar yine kendi ekranlarından ve scriptlerinden yapılır. Amaç "her şey
yolunda mı" sorusunu terminale inmeden yanıtlamak; `teshis.py`'nin ekran
karşılığı.

Klasör kartı özellikle iki makineli kullanım için: yolların bu makinede
gerçekten var olup olmadığını gösteriyor, USB ile taşındıktan sonra ilk
bakılacak yer orası.

Ana ekrandaki "Kullanıcılar" düğmesi "Yönetim" oldu (yalnızca yöneticide
görünür); kullanıcı listesinin geri düğmesi panele döner.

## Test edildi

- Giriş ekranında "Şifre değiştir" bağlantısı var; oturum açmadan `/sifre`
  açılıyor ve kullanıcı adı soruyor
- Var olan / olmayan kullanıcı için hata mesajları birebir aynı
- Pasif kullanıcı doğru şifresiyle bile değiştiremedi, karma değişmedi
- Giriş yapmışken kullanıcı adı sorulmuyor, kim olduğu yazıyor
- Başarılı değişiklikte oturum düşüyor, giriş ekranına dönüyor
- `/yonetim` yöneticide açılıyor; embriyologda düğme görünmüyor ve adres elle
  yazılınca reddediliyor

---

# v6.14 — modül bazlı erişim izni

Yönetici artık her kullanıcının hangi ekranlara girebileceğini tek tek
belirliyor. 15 modül: hasta kaydı, 11 laboratuvar aşaması, cryo, fotoğraf,
silme.

## Kontrol nerede yapılıyor — ve neden orada

~50 rota var. Her birine izin kontrolü eklemek tuzak #1'in tam tarifi: aynı
kalıp defalarca geçiyor, biri atlanırsa açık kalıyor ve fark edilmiyor.

Bunun yerine **tek nokta: middleware**. `yol_modulu(yol)` yolu modüle eşliyor,
middleware izni yoksa `/hastalar`'a döndürüyor. Yollar zaten düzenli:

```
/cycle/{id}/transfer          -> transfer
/cycle/{id}/denudasyon-zaman  -> denudasyon
/specimen/{id}/taraf          -> denudasyon
/cryo/tasiyici/{id}/thaw      -> thaw   (gerçek bir çözme işlemi)
herhangi bir .../sil, -sil, geri-al -> silme
```

**Görüntüleme serbest.** Hasta listesi, hasta detayı, cycle özeti ve değişiklik
geçmişi izin istemiyor — kısıtlanırsa program kullanılamaz hale gelir. İzin,
**işlem yapılan** ekranlar için.

Bir istisna rotanın içinde: `/cycle/{id}/islem-yapan` hangi aşamaya yazdığını
form gövdesinde taşıyor, `yol_modulu` göremiyor. Kontrol o rotada. Test edildi —
izinsiz aşamaya ad yazma denemesi reddedildi ve satır oluşmadı.

## Ekranda gizlemek yetmez

Düğmeleri gizlemek kolaylık; **asıl engel middleware'de**. İkisi de yapıldı:

- Aşama düğmeleri ve gezinme çubuğu `cycle_asamalari()`'nden besleniyor, süzme
  orada — tek yerde, ikisi birden doğru. "3/8" sayacı da kullanıcının kendi
  adımlarını sayıyor.
- Şablonlarda Jinja global `yetkim("modul")`: yeni hasta, cryo, fotoğraf ekle,
  silme bağlantıları, taşıyıcı çözme.

Doğrulandı: kısıtlı kullanıcı adresi elle yazdığında da, tarayıcıyı atlayıp POST
attığında da engellendi ve **veritabanına hiçbir şey yazılmadı**.

## Varsayılan: her şey açık

Kısıtlama yöneticinin bilinçli olarak kaldırdığı kutulardan doğmalı, bir
unutkanlıktan değil. Bu yüzden:

- `goc_026` **mevcut tüm kullanıcılara tüm modülleri** verir — kimse göç sonrası
  ekran kaybetmez
- Sonradan açılan kullanıcı da hepsini alır (`tum_yetkileri_ver`), hem ekrandan
  hem `kullanici.py yeni` ile. Bu atlanırsa yeni kullanıcı **hiçbir ekrana**
  giremez ve sebebi anlaşılmaz — test sırasında tam olarak bu çıktı, düzeltildi.
- Göç çalıştırılmadıysa herkes her yere girer (tuzak #3). Test edildi: `yetki`
  tablosu silinmiş bir veritabanında kısıtlı kullanıcı bile 14 düğmenin hepsini
  gördü, 500 yok, yönetici ekranında göç uyarısı çıktı.

Yöneticiler bu tablodan bağımsız: `rol='yonetici'` her yere girer, kutulara
bakılmaz. Ekranda da bu yazıyor.

## Şema

```sql
yetki(id, lab_id, kullanici_id, modul, UNIQUE(kullanici_id, modul))
```

Satır varsa izin var. İzinler kaydedilirken önce hepsi silinip işaretliler
yazılıyor — form işaretsiz kutuları hiç göndermediği için "kaldırılan izin" ayrı
bir istek olarak gelmiyor. Tek işlemde (`db.yazma_islemi`).

## Test edildi

- Bir kullanıcı 15 modülden 2'sine indirildi (denüdasyon + ICSI)
- Ana ekranda "Yeni hasta" ve "Cryo haritası" kayboldu; cycle ekranında 14
  düğmeden 3'ü kaldı
- İzinsiz 6 ekrana doğrudan gidildi, hepsi engellendi
- İzinli 2 ekran normal açıldı
- Tarayıcı atlanarak POST atıldı: `opu_sag_oosit` değişmedi,
  `islem_yapan(transfer)` satırı oluşmadı
- Yeni kullanıcı hem ekrandan hem terminalden 15/15 izinle açıldı
- `yetki` tablosu yokken kimse ekran kaybetmedi

---

# v6.15 — tanımsız rol tek tıkla yönetici yapıyordu

## Hata

Kullanıcının makinesinde `androlog` diye bir rol çıktı. `kullanici.rol` serbest
metin bir kolon (CHECK yok) ve `kullanici.py yeni` ne yazılırsa kabul ediyordu.

v6.13'te eklediğim rol seçicisi yalnızca iki seçenek gösteriyor:

```html
{% for kod, ad in roller %}   <!-- yonetici, embriyolog -->
<option value="{{ kod }}" {% if k.rol == kod %}selected{% endif %}>
```

`androlog` hiçbiriyle eşleşmediği için **hiçbir seçenek `selected` olmuyor** —
tarayıcı da bu durumda ilk seçeneği gösteriyor: *Yönetici*. Ekranda o kullanıcı
yöneticiymiş gibi duruyor ve "Rolü değiştir"e bir tık, onu gerçekten yönetici
yapıyordu. Üstelik yönetici rolü tüm modül izinlerini de baypas ediyor.

Doğrulandı:

```
veritabanindaki rol : androlog
secicide gorunen    : yonetici     <<< tek tikla gercek olurdu
```

## Düzeltme

**1. Tanımsız rol kendi adıyla ve seçili gösteriliyor:**

```
secenekler : ['androlog — tanımsız', 'Yönetici', 'Embriyolog']
```

**2. Değişmemiş rol artık no-op.** Doğrulama sonraya alındı; seçiciye
dokunmadan kaydedilirse hiçbir şey olmuyor (önceki sırada "Geçersiz rol"
hatası verirdi).

**3. Yeni tanımsız rol üretilemiyor.** `kullanici.py yeni` artık serbest metin
kabul etmiyor, listeyi gösterip reddediyor ve doğru mekanizmayı söylüyor:
kim hangi ekrana girer sorusunu **rol değil, modül izinleri** belirler.

Mevcut tanımsız roller olduğu gibi çalışmaya devam ediyor — yönetici olmayan
kullanıcı sayılıyorlar, ki zaten davranışları buydu.

## Ders

Bir `<select>`'i veritabanındaki bir değerle beslerken, o değerin listede
olmama ihtimalini hep düşün. Sessiz sonuç en kötüsü: hiçbir hata çıkmıyor,
sadece ekran yanlış şeyi gösteriyor ve bir tık yetkiyi yükseltiyor.
CLAUDE.md tuzak #6.

## Test edildi

- `androlog` rollü kullanıcı seçicide kendi adıyla ve seçili görünüyor
- Seçiciye dokunmadan kaydedince rol değişmiyor
- Bilerek "Embriyolog" seçilince normal çalışıyor
- `kullanici.py yeni` tanımsız rolü reddediyor

---

# v6.16 — `tasi.py`: iki makine arasında güvenli veri taşıma

## Sorun

Kullanıcı iki makinede de aynı veriyi istiyor ve "hangi makinede yeni veri
girdiysem diğerine taşımak istiyorum" diyor. Asıl makine yok — nöbet devri.

Bunun teknik gerçeği şu: `lab.db` **tek dosyadır**, 23 tablo içinde. "Sadece
dün girdiğim 3 hastayı" ayırmanın yolu yok. Taşınan dosyanın tamamıdır ve
karşıdakinin **üzerine yazar**.

Yani asıl tehlike kopyalama değil, **yanlış yöne kopyalama**:

```
Mac'te 3 hasta girdin, USB'ye almadın
Klinikte 5 hasta girdin
Sonra Mac'ten kliniğe kopyaladın  ->  kliniğin 5 hastası yok oldu
```

Elle dosya kopyalamada bu tek bir unutkanlıkla oluyor ve geri dönüşü yok.

## Çözüm: kopyalamadan önce karşılaştır

```
python3 tasi.py durum  /Volumes/USB     sadece bak
python3 tasi.py disari /Volumes/USB     bu makineden USB'ye
python3 tasi.py iceri  /Volumes/USB     USB'den bu makineye
```

`iceri` iki tarafı yan yana koyar ve hedef daha yeniyse **durur**:

```
DIKKAT: BU MAKINEDEKI veri USB'dekinden YENI.
  bu makinede son kayit : 2026-09-09 20:19:01
  USB'de son kayit      : 2026-09-09 20:18:41
Devam edersen bu makinede girdigin YENI KAYITLAR SILINIR.
Muhtemelen once bu makineden 'disari' yapman gerekiyordu.
  Devam etmek icin EVET yaz:
```

Aynı koruma ters yönde de var: USB'deki kopya daha yeniyken `disari`
çalıştırılırsa uyarıyor.

### "Daha yeni" nasıl ölçülüyor

`olusturma_zamani` kolonları (satırın oluşturulma anı) ve değişiklik günlüğü.
Klinik zamanlarına **bakılmıyor** — `opu_zamani` gibi alanlar elle geri
tarihlenebiliyor ("işlem saatleri elle girilebilir" kuralı), o yüzden "bu
veritabanına en son ne zaman yazıldı" sorusuna cevap veremezler.

### Üzerine yazmadan önce yedek

`iceri` mevcut veritabanını `lab_ONCEKI_<tarih>.db` olarak bırakıyor. Yanlışlıkla
onay verildiyse geri dönülebilir. `.gitignore`'a eklendi — hasta verisi içerir,
depoya sızmamalı.

## WAL tuzağı — düz kopyalama veriyi yok eder

Uygulama çalışırken `lab.db`'yi düz kopyalamayı denedim:

```
Uygulama calisirken sadece lab.db kopyalandi  ->  "no such table: hasta"
Uc dosya birden (lab.db + -wal + -shm)        ->  1 hasta
Uygulama duzgun kapandiktan sonra lab.db      ->  1 hasta
```

Kopya **bomboş** çıktı. SQLite WAL modunda yeni kayıtları önce `lab.db-wal`
dosyasına yazıyor. Bu yüzden `tasi.py` de `yedek.py` gibi **SQLite backup API**
kullanıyor: uygulama açıkken bile tutarlı kopya alıyor ve `integrity_check` ile
doğruluyor.

`iceri` sırasında eski `-wal`/`-shm` dosyaları siliniyor — yeni veritabanıyla
tutarsız olurlardı.

## Diğer ayrıntılar

- **Arşiv birleşir, silinmez.** Fotoğraflar boyut karşılaştırmasıyla kopyalanıyor;
  hedefte olan hiçbir şey silinmiyor.
- **Yarım dosya bırakmıyor.** Önce `lab.db.yeni` yazılıp doğrulanıyor, sonra
  yerine geçiyor.
- **Uygulama açıksa** `iceri` Windows'ta dosya kilidine takılır; hata yakalanıp
  "Ctrl+C ile durdur" deniyor ve önceki hal korunuyor.
- `TASIMA_BILGI.txt` USB'ye yazılıyor: hangi makineden, ne zaman, ne içerikle.

## Test edildi

İki makine (`makineA`, `makineB`) ve bir USB klasörüyle tam tur:

- Boş USB'de `durum` → doğru rapor, hiçbir şey değişmedi
- A'ya hasta eklendi → `disari` → B'de `iceri` → **hasta B'ye geldi**, yedek alındı
- B'ye hasta eklendi, eski USB'den `iceri` denendi → **uyardı, durdu, veri duruyor**
- B `disari` → A `iceri` → B'nin hastası A'ya geldi
- USB daha yeniyken `disari` denendi → **uyardı ve durdu**
- Fotoğraflar taşındı; ikinci çalıştırmada "2 zaten guncel" dedi
- USB takılı değil / taşıma klasörü yok / yanlış komut → anlaşılır hatalar
- **Taşınan veritabanı uygulamada açıldı**, iki makinenin hastaları da ekranda

---

# v6.17 — `tasi.py` yeni kurulmuş makineye de veri alabiliyor

## Sorun

Kullanıcı Windows'ta ZIP indirerek kurmuştu (git clone değil), yeni bir klasöre
temiz kurulum yapması gerekti. O klasörde henüz `lab.db` yok — ve `tasi.py`
oraya veri alamıyordu:

```
Bu makinede lab.db yok: C:\...\lab.db
```

`karsilastir()` her iki tarafın da var olduğunu varsayıyordu. Oysa "yeni
bilgisayara ilk kez veri alma" en doğal senaryolardan biri.

## Düzeltme

Bu makinede `lab.db` yoksa:

- **`iceri`** karşılaştırmayı ve yedeklemeyi atlar, doğrudan alır —
  karşılaştıracak bir şey yok, kaybedilecek bir şey de yok:
  ```
  Bu makinede lab.db yok — ilk kurulum. Guvenle alinabilir.
  ```
- **`disari`** durur ve ne yapılacağını söyler: gönderecek veri yok, önce
  `iceri` ya da `sifirdan_kur.py`.
- **`durum`** "bu makine henuz bos" der, hata vermez.

Dolu makinedeki korumalar aynen duruyor — regresyon testiyle doğrulandı.

## Test edildi

- Boş klasöre `iceri` → 4 hasta ve 6 kullanıcı geldi, fotoğraflar kopyalandı
- Boş klasörde `disari` → anlaşılır hata, ne yapılacağı yazıyor
- Dolu makinede daha yeni veri varken `iceri` → hâlâ uyarıyor ve duruyor

---

# v6.18 — ana ekran, aramadan çıkış yolu, yan aşama menüsü

Kullanıcının üç ayrı gözlemi; üçü de aynı şeye bakıyor: **programda nerede
olduğunu ve oradan nereye gidebileceğini görmek.**

## Ana ekran: hasta adları artık ilk ekranda değil

`/` doğrudan `/hastalar`'a gidiyordu. Yani program açılır açılmaz son
kaydedilen hastaların **adı soyadı** ekrandaydı. Program klinikte gün boyu
açık duruyor; ekrana bakan herkes — bekleyen hasta, hasta yakını, teknik
servis — o listeyi görüyordu.

`/` artık bir ana ekran: **aktif hasta**, **aktif cycle**, **dondurulmuş
embriyo** sayıları ve varsa **bekleyen kamera karesi**. Sayılar kimseyi
tanımlamaz. Adlar ancak `/hastalar`'a girilince görünüyor — bir tık, ama
bilinçli bir tık.

Giriş sonrası ve "bu ekrana yetkin yok" yönlendirmesi de artık buraya.
Dondurulmuş embriyo sayısı `/cryo` ile **aynı ölçüden** türetiliyor (dolu
taşıyıcıdaki iptal edilmemiş vitrifikasyon kayıtları) — ayrı bir sayaç
tutulmuyor, cryo haritası kuralı bozulmasın diye.

## Aramadan çıkış yolu yoktu

`/hastalar?ara=demir` ekranından listeye dönmenin yolu yoktu: arama kutusunu
elle silip tekrar göndermek gerekiyordu. Arşiv görünümünün "Aktif hastalara
dön" düğmesi vardı, aramanın karşılığı yoktu.

İki ekleme: üst çubukta **geri oku** (ana ekrana) ve arama varken
**"Aramayı temizle"** düğmesi.

## Yan aşama menüsü (geniş ekranda)

OPU / Denüdasyon / ICSI / ... bağlantıları cycle ekranının **en altında** bir
yığındı. Aşamalar arası geçmek için her seferinde cycle ekranına dönüp
kartların altına kadar kaydırmak gerekiyordu.

Geniş ekranda (≥1100px) bu bağlantılar artık **solda sabit bir menü**, içinde
bulunulan aşama işaretli. Telefonda menü yok: içerik sütunu 640px, yanında yer
kalmıyor — ve telefon bu programın birinci ekranı. Orada gezinme eskisi gibi
(alt çubuk + cycle ekranındaki düğmeler). Menü DOM'da duruyor, CSS gizliyor;
böylece 11 aşama şablonunun hiçbirine dokunmak gerekmedi.

Menü `asama_gezinme()`'nin döndürdüğü listeden besleniyor — yani **tedavi
tipine ve modül izinlerine göre süzülmüş** hali. FET'te menüde yalnızca çözme,
transfer ve gebelik var. Alt çubuk da aynı listeden besleniyordu; süzme tek
yerde kaldı.

Kimlik bandı (koyu banttaki dosya no ve ad) geniş ekranda içerik sütunuyla
hizalandı — menü onun üstüne biniyordu. "Hasta kimliği her ekranda görünür"
kuralı menüden önce gelir.

## Test edildi

- Ana ekran, hasta listesi, cycle, denüdasyon, ICSI, OPU, çözme, cryo → hepsi 200
- FET cycle'ında menüde yalnızca üç aşama
- 1280px ve 390px ekran görüntüleri: telefon görünümü değişmedi
- Şablonlar iki dilde de render oluyor, eksik çeviri anahtarı yok

---

# v6.19 — denüdasyonda hayalet oosit

## Sorun

Kullanıcı: *"Denüdasyon bölümünde foto kayıtları ve oositler hakkında
bilgilerin kaydedilmesinde sorun var — kaydediyor ama listede görünmüyor."*

Tek kamera karesini iki kez kaydedince (telefonda çift dokunma, ya da geri
gelip formu tekrar göndermek) **fotoğrafsız bir oosit** kalıyordu:

```python
sid = goruntuler.specimen_olustur(...)      # önce oosit açılır
goruntuler.goruntu_bagla(im, ..., sid, ...) # sonra kare bağlanır
```

İkinci gönderimde `goruntu_bagla` "bu kare zaten alınmış" deyip `None`
dönüyor, arşive aldığı kopyayı da geri siliyor — ama **az önce açılan oosit
olduğu yerde kalıyordu**. Ekranda "fotoğrafsız" görünen, hiçbir şeye karşılık
gelmeyen bir oosit. Hiçbir uyarı da çıkmıyordu.

Aynısı kare kaynak klasörden kaybolunca da oluyordu (dosya taşındı, silindi,
kamera yazılımı aldı).

**Oosit sayısı klinik bir sayıdır.** Şişmesi kabul edilemez.

## Düzeltme

Kare bağlanamazsa az önce açılan oosit geri alınıyor ve **sebep ekranda
yazıyor**:

- "Bu kare zaten kaydedilmiş. Yeni kayıt oluşturulmadı."
- "Kare kaynak klasörde bulunamadı — taşınmış veya silinmiş olabilir."

"Aynı oosite ekle" yolunda oosit açılmıyor ama kare **sessizce** kayboluyordu;
orada da artık mesaj çıkıyor.

Geri alma `goruntuler.bos_specimen_sil()` ile, guard `geri_al`'dakiyle aynı:
**yalnızca hiç görüntüsü ve olayı olmayan oosit silinir.** Yani bilerek
oluşturulan "fotoğrafsız oosit" etkilenmiyor.

Adresten gelen hata anahtarı beyaz listede tutuluyor: `metin()` bulamadığı
anahtarı olduğu gibi döndürdüğü için, `?hata=...` ile ekrana istenen yazı
yazdırılabilirdi.

Bu yol **elle fotoğraf ekleme** rotasında zaten doğruydu (boş specimen'i geri
alıyordu); kameradan gelen yolda atlanmış.

## Test edildi

- Aynı imzayla iki POST → tek oosit, tek kare, ikincide uyarı
- Olmayan kare → oosit açılmıyor, "kare bulunamadı"
- Bilerek "fotoğrafsız oosit" → hâlâ oluşuyor, silinmiyor
- `?hata=UYDURMA` → ekrana yazılmıyor

---

# v6.20 — bilgi kartı düzeni: her aşamada aynı

Kullanıcının dört ayrı isteği; hepsi tek bir soruya bakıyor: **kaydettiğim şeyi
nasıl görürüm?**

## Cycle ekranı klinik özete döndü

Cycle ekranında oosit fotoğrafları ve arşiv küçük resimleri vardı. Ekran artık
yalnızca klinik bilgi: sayılar, zamanlar, protokol ve oosit numaraları (yanında
toplandığı over). Fotoğraflar kendi aşama ekranlarında — tek tek ve büyük
bakılacak yerde.

## Denüdasyon yeniden sıralandı

Kullanıcının istediği sıra:

1. denüdasyon saati
2. oosit ekleme alanı (kare önizleme + kaydet; kare yoksa **fotoğrafsız
   ekleme aynı kartın içinde**)
3. toplandığı over
4. kaydedilen oositler — **karenin üstünde over rozeti, altında numara**
5. bir kareye basınca **altında** bilgi kartı
6. en altta işlemi yapan

Over seçicisi ekleme alanının **altında**, çünkü seçim bundan sonra eklenecek
oositlere yazılıyor — sıra, işin sırası. Tek bir oositin over'ını değiştirmek
için karesine bas: bilgi kartında over satırı yerinde düzenlenebiliyor.

## Bilgi kartı: dört aşama ekranında da

ICSI, fertilizasyon, gün 2/3 ve blastokist ekranlarında form **her zaman
açıktı**. Kaydedilmiş bir oosite dönünce yine doldurulmuş radyo düğmeleri
karşılıyordu; "ne kaydetmiştim" sorusunun cevabı form alanlarından okunuyordu.

Artık kayıt varsa salt okunur bir **bilgi kartı** görünüyor ("Kaydedildi"
rozetiyle), değiştirmek için **Düzenle** ile forma dönülüyor (`?duzenle=1`).
Kaydı olmayan örneklerde form doğrudan açılıyor — yani **"kaydet → sonraki
oosit" toplu giriş akışı bozulmadı.** Bu önemliydi: 20 oositlik bir cycle'da
her oosit için fazladan bir tıklama, 20 fazladan tıklamadır.

Düzen böylece her yerde aynı: **üstte örnekler, birine basınca altta bilgi
kartı.** Denüdasyonda üstteki şerit fotoğraf kareleri, aşama ekranlarında numara
şeridi — davranış aynı.

## Kartlar kodu değil etiketi gösterir

Kayıtta duran `mii`, `2`, `z1` gibi kodların ekranda görünen karşılığı
`liste_degeri` tablosunda ve **laba özgü** (yönetici düzenleyebiliyor). Yeni
Jinja global `liste_etiket(liste_adi, kod)` çeviriyi oradan okuyor. Bulunamayan
kod kendi adıyla dönüyor — sessizce boşalmıyor.

## Yan düzeltmeler

- **Form betikleri artık form yoksa erken çıkıyor.** Bu zaten gizli bir hataydı:
  cycle'da hiç oosit yokken `bulguAc` null oluyor, `addEventListener` patlıyor
  ve sayfanın öteki betikleri de çalışmıyordu. Bilgi kartı modu bunu görünür
  hale getirdi.
- **`_buyutec.html` içinde "Oosit" sabit yazılıydı** — blastokist ekranında da,
  İngilizce kurulumda da yanlıştı. Çağıran tam etiket verebiliyor.
- **`yuzde()` tam sayıda ondalık yazmıyor**: "%10.0" değil "%10". Kolon `REAL`.

## Test edildi

- Dört ekranda da: kayıt varken kart, `?duzenle=1`'de form (kayıtlı değerler
  seçili), kaydı olmayan örnekte doğrudan form
- Kaydet → sonraki oosite geçiyor, dönünce kart güncel
- Kartlar iki dilde: etiketler çevriliyor, liste değerleri labın kendi
  yazdığı gibi kalıyor (v6.17'deki karar)
- 31 ekran 200, tarayıcı konsolunda JS hatası yok

---

# v6.21 — bilgi kartı düzeni: kalan beş ekran

v6.20'de ICSI, fertilizasyon, gün 2/3 ve blastokist bu düzene geçmişti.
Kullanıcı kalanları da istedi: **OPU, denüdasyon, vitrifikasyon, çözme,
transfer.** Bunlar iki farklı şekilde:

## Form olanlar: OPU ve denüdasyon saati

Kayıt varsa salt okunur bilgi kartı ("Kaydedildi" rozetiyle), değiştirmek için
**Düzenle** (`?duzenle=1`). v6.20'deki `_bilgikart.html` `kart()` makrosu
aynen kullanıldı.

OPU'da "kaydedilmiş" ölçüsü **`opu_zamani`**. Oosit sayıları bilerek boş
bırakılabiliyor (`NULL` = girilmedi, projenin kuralı), o yüzden onlara bakmak
yanlış olurdu — ama OPU yapıldıysa saati vardır.

Yan düzeltme: **hatalı giriş artık formu kapatmıyor.** Sayı alanına harf
yazılınca rota `?hata=...` ile geri dönüyordu; kart modu geldikten sonra bu
"mesajı göster, formu gizle" anlamına gelirdi. Rota artık
`?duzenle=1&hata=...` diyor, yani mesaj **formun üstünde** çıkıyor ve
kullanıcı yazdığını düzeltebiliyor.

Denüdasyon saati ilk oosit kaydedilince kendiliğinden doluyor, yani o kart
neredeyse hep görünür halde — form ancak Düzenle'yle açılıyor.

## Kayıt listesi olanlar: vitrifikasyon, çözme, transfer

Bu üç ekranda "yapılmış olanlar" listesi vardı: `.fsatir` biçiminde alt alta
metin satırları (küçük fotoğraf + ad + meta satırları + bağlantılar). Görünüş
programın geri kalanından farklıydı.

Artık **kare ızgarası + basınca altında bilgi kartı** — denüdasyondaki düzenin
aynısı. Kartların satırları:

- **Vitrifikasyon:** numara, skor (+ gün), taşıyıcı (bağlantılı), konum;
  altında "çöz" ve "kaydı geri al"
- **Çözme:** örnek kodu, sağkalım, canlılık, re-expansion, çözme saati,
  taşıyıcı, kaynak cycle (farklıysa), transfer durumu
- **Transfer:** numara, skor, geldiği cycle, tip (taze/donmuş), transfer saati;
  altında "kaydı geri al"

Çözme ekranındaki özet satırı ("Canlı 1/1 · transfer edilen 1") ayrı bir
karttaydı, ızgara kartının içine taşındı — iki kart yerine bir kart.

## Neden ikinci bir makro

`_izgara.html` denüdasyona özgü: over rozeti, over'ı yerinde düzenleme ve
**tek panel** (içeriğini JS dolduruyor, çünkü 40 oositlik bir cycle'da her
oosit için ayrı panel basmak sayfayı şişirir).

Yeni `_ornekkart.html` genel hali ve kartları **sunucu basıyor**. Sebebi:
her ekranın satırları farklı ve içlerinde bağlantı var (taşıyıcı sayfası,
"çöz", "kaydı geri al") — bunları JS ile kurmak `_izgara`'daki gibi ayrı bir
doldurma mantığı isterdi. Bu listeler zaten kısa (bir cycle'ın embriyoları),
sunucuda basmanın maliyeti yok.

Çağıran satırlarını `{% call(e) %}` bloğuyla veriyor, yani makro düzeni
biliyor, ekran içeriği biliyor. Olaylar tek yerden dinleniyor
(`ok.baglama()`), makro kaç kez kullanılırsa kullanılsın tek betik yetiyor.

## Test edildi

- Beş ekranda da gerçek kayıtla: kart görünüyor, kareye basınca doğru kart
  açılıyor, ikinci basış kapatıyor
- OPU: kart → Düzenle → kaydet → kart; hatalı girişte form açık kalıyor ve
  mesaj görünüyor
- İki dilde: etiketler çevriliyor, liste değerleri labın yazdığı gibi kalıyor
- 32 ekran 200, tarayıcı konsolunda JS hatası yok

---

# v6.22 — düzen artık gerçekten her ekranda aynı

v6.20 ve v6.21'den sonra iki ekran hâlâ farklıydı; kullanıcı ekran görüntüsüyle
gösterdi: **"aynı bu düzende olsun hepsi, yani üst kısımda numaralar yazsın."**

## Denüdasyon

v6.21'de denüdasyonda fotoğraf kareleri ızgarası vardı: kareye basınca içeriği
JS ile doldurulan tek bir panel açılıyordu. Çalışıyordu ama öteki aşama
ekranlarından farklıydı — orada "Kaydedildi" rozeti ve **Düzenle** düğmesi
yoktu, seçim de adresten değil tıklamayla oluyordu.

Artık aynı iskelet:

```
numara şeridi (1-Sağ  2-Sol  3)
   ↓ seçilen
büyük fotoğraf + kare şeridi
   ↓
bilgi kartı: Kaydedildi · Numara / Toplandığı over / Kare / Örnek kodu
             [Düzenle]
```

Seçim adresten (`?oosit=N`) — ICSI, fertilizasyon, gün 2/3 ve blastokist de
böyle. Kamera kuyruğundan oosit ekleme bölümü olduğu gibi duruyor; asıl iş o.

Bu ekranda **düzenlenebilecek iki ayrı şey** var, hangisi olduğu adreste
yazıyor:
- `?duzenle=saat` → cycle'ın denüdasyon saati
- `?duzenle=oosit` → seçili oositin toplandığı over

Over düzenlemede her düğme kendi başına gönderiyor; ayrı bir "Kaydet" adımı
yok, çünkü tek alan var.

`_izgara.html` silindi — başka kullananı yoktu.

## Androloji

Form her zaman açıktı. Artık kayıt varsa **dört bölüm salt okunur bilgi kartı**
olarak basılıyor (örnek bilgisi, makroskopik, bazal analiz, hazırlık sonrası),
en altta tek **Düzenle** düğmesi. Sperm örneği seçici (1 · tarih, + Yeni) zaten
üstteydi, olduğu gibi kaldı.

Hatalı girişte form açık kalıyor (`?duzenle=1&hata=...`) — v6.21'de OPU'ya
konan kuralın aynısı.

## `_bilgikart.kart()` iki küçük değişiklik

- `duzenle_yolu` artık **isteğe bağlı**. Androloji gibi kaydı bölümlere
  yayılan ekranlarda bölümler arka arkaya kart olarak basılıp tek Düzenle
  düğmesi en alta konabiliyor.
- **Vurgulu kenarlık yalnızca rozetli kartta.** Androlojide dört kartın da
  kenarlığı kırmızı olunca ekran bağırıyordu; rozet zaten "kaydın başlık
  kartı" demek.

## Test edildi

- Denüdasyon: şerit seçimi, saat düzenleme, over düzenleme (üçü de kaydedip
  karta dönüyor), hiç oositi olmayan cycle
- Androloji: kart → Düzenle → kaydet → kart; hatalı girişte form açık kalıyor
- İki dilde; 31 ekran 200, JS hatası yok

---

# v6.23 — örnek kodu, ilk kare, hasta adı önde

Dört ayrı düzeltme.

## Denüdasyondaki ikinci over seçicisi kalktı

"Bundan sonraki oositler için over" seçicisi ekleme kartındaydı; aynı seçim
bilgi kartındaki **Düzenle**'de de var. Kullanıcı ikincisinin yettiğini söyledi.

**Karşılığı var:** eski seçici bir kez "Sağ" deyip o overden gelen bütün
oositleri sağ olarak kaydetmeye yarıyordu. Artık yeni oositler over'sız
açılıyor ve her birinin over'ı tek tek giriliyor. 20 oositlik bir cycle'da bu
20 ayrı düzenleme demek — geri istenirse seçici geri gelir.

## Örnek kodu fotoğrafın altında

`527078-2026-0001-03` kodu artık ana fotoğrafın altında yazıyor.

Kod **oosit → zigot → embriyo boyunca değişmiyor** (`specimen.id` sabit,
CLAUDE.md'deki "soyağacı böyle korunur" kuralı), o yüzden aynı kod
denüdasyon, ICSI, fertilizasyon, gün 2/3 ve blastokist ekranlarında aynı
yerde çıkıyor. "Bu blastokist hangi oositten çıktı" sorusu ekrandan
okunabiliyor.

## Aşama ekranları ilk kareyi gösteriyor

Bir aşama ekranı açılınca **son** kare geliyordu. Dört sorgu
`ORDER BY g.id DESC LIMIT 1` diyordu (ICSI, fertilizasyon, gün 2/3,
blastokist), denüdasyon şablonunda da `kareler[-1]` vardı. Hepsi ilk kareye
çevrildi. Kare şeridi ve büyüteç zaten sıralı geziyor.

## Hasta adı üstte ve büyük

Kimlik bandında dosya no 34px ile en üstteydi, ad altında 17px. Kullanıcının
isteği: **ad üstte ve büyük, dosya no altında.** Aynı sıralama hasta
listesinde de.

Sıra **şablonda değil CSS'te** çevrildi: kimlik bandı 31 şablonda aynı sırayla
basılıyor ve hepsini tek tek düzenlemek tuzak #1'in tarifi. `display: flex` +
`order` ile tek yerden dönüyor, hiçbir şablonun HTML'ine dokunulmadı.

İki ekranda hasta adı yok (taşıyıcı detayı, çözme) — orada `.dosya` başlığın
kendisi. Onlar `kimlik tekli` diye işaretlendi, küçülmüyorlar.

Hasta listesindeki sıralama `.satir.hasta`ya daraltıldı: `.satir` taşıyıcı,
cycle, kullanıcı ve geçmiş listelerinde de kullanılıyor ve orada `.no` başlık
görevinde — hepsini çevirmek onları bozardı.

## Test edildi

- Çok kareli bir oositle: aşama ekranları ilk kareyi gösteriyor
- Örnek kodu beş ekranda da fotoğrafın altında, iki dilde
- Kimlik bandı ve hasta listesi: ad üstte; taşıyıcı/çözme başlıkları küçülmedi;
  cycle ve kullanıcı listeleri değişmedi
- 31 ekran 200, JS hatası yok

---

# v6.24 — denüdasyon açılışta salt okunur

Ekran açılınca oosit ekleme kartı, numara şeridi ve seçilen oositin fotoğrafı
görünüyordu. Kullanıcının isteği net: **bunların hiçbiri bilgi kartlarının
üstünde olmasın, Düzenle deyince çıksın.**

## İki kip

**Açılış — salt okunur:**

- Denüdasyon zamanı kartı (+ Düzenle)
- **Kaydedilen oositler** özet kartı: toplam, sağ, sol, belirtilmemiş,
  fotoğraflı ve varsa bekleyen kamera karesi (+ Düzenle)
- İşlemi yapan

**Çalışma kipi (`?duzenle=oosit`):** oosit ekleme kartı, numara şeridi,
seçilen oositin fotoğrafı ve kare şeridi, oositin bilgi kartı (over düğmeleri
yerinde), "Oositi sil", en altta **Bitir**.

Kamera klasörü ve boş dosya uyarıları da çalışma kipine taşındı — ekrana
bakmaya gelen kişiyi ilgilendirmiyorlar, kayıt girene ilgilendiriyorlar.

## Neden özet kartı, tek bir oositin kartı değil

Numara şeridi çalışma kipine taşınınca açılışta hangi oositin gösterileceğini
seçmenin yolu kalmıyor. Denüdasyon aşamasının **kaydı** zaten tek bir oosit
değil, oositlerin tamamı — kart onu özetliyor. Tek tek bakmak ve düzeltmek
çalışma kipinde.

## Kare kaydettikten sonra çalışma kipinde kalınıyor

`denudasyon_islem` artık `?duzenle=oosit` adresine dönüyor. Özete düşseydi her
kayıttan sonra tekrar Düzenle demek gerekirdi — 20 oositlik bir cycle'da 20
fazladan dokunuş.

## Test edildi

- Açılışta çalışma alanından tek parça yok (`Oosit ekle`, `serit`, `foto`,
  `Elle fotoğraf ekle`, `Son kaydı geri al` → hepsi 0 eşleşme)
- Çalışma kipinde hepsi var
- Kare kaydet → çalışma kipinde kalıyor; over değiştir → çalışma kipi;
  saat düzenle → özet
- Özet sayıları kayıttan sonra güncel
- İki dilde; 24 ekran 200, JS hatası yok

---

# v6.25 — denüdasyon bilgi ekranı fert/blastokistin aynısı

v6.24'te fazla sakladım. Kullanıcı "oosit ekleme bloğu Düzenle'nin arkasına
geçsin" demişti; ben numara şeridini ve fotoğrafı da oraya attım, ekranda
yalnızca bir sayı özeti kaldı. İstenen bu değildi:

> "Ben bilgi kartında sıra numaraları ile altlarında kodu olan oosit fotoları
> olsun. Aynı fertilizasyon, blastokist ekranları gibi bilgi ekranı olsun,
> tasarım ve görüntü benzerliği ve bütünlüğü olsun istedim."

## Doğrusu

**Bilgi ekranı (açılış)** artık fertilizasyon/blastokist ekranlarının birebir
aynısı:

```
numara şeridi (1-Sağ  2-Sol  3)
sayaç: "3 oosit kaydedildi"        "Oosit 1 sağ"
seçilenin büyük fotoğrafı
   altında örnek kodu (527078-2026-0001-01)
kare şeridi · Bu fotoğrafı sil · Fotoğraf ekle
bilgi kartı: Oosit 1 [Kaydedildi]
             Numara / Toplandığı over / Kare / Örnek kodu
             [Düzenle]
```

**Düzenle'nin arkasında kalan tek şey oosit eklemek:** kamera kuyruğu,
fotoğrafsız ekleme, elle fotoğraf, son kaydı geri al — bir de seçili oositin
over'ını değiştirme. Kamera klasörü ve boş dosya uyarıları da orada; kayıt
girmeyeni ilgilendirmiyorlar.

Şerit ve fotoğraf **iki kipte de** duruyor; değişen yalnızca seçim adresi
(`?oosit=N` / `?duzenle=oosit&oosit=N`).

## v6.24'ten geri alınanlar

Özet kartı ve onun sözlük anahtarları (`toplam_oosit`, `belirtilmemis`,
`fotografli`, `oositleri_duzenle`) kaldırıldı, rotadaki `ozet` hesabı da.
Bilgi kartı yine **tek oositin** kartı — öteki aşama ekranlarındaki gibi.

Hiç oositi olmayan cycle'da boş kartın altında "Oosit ekle" düğmesi çalışma
kipine götürüyor; yoksa ilk oositi eklemenin yolu kalmıyordu.

## Test edildi

- Bilgi ekranı: şerit, fotoğraf, kod, bilgi kartı var; "Oosit ekle",
  "Elle fotoğraf ekle", "Son kaydı geri al" yok
- Çalışma kipi: hepsi var + over düğmeleri + Bitir
- Şerit bağlantıları kipe göre doğru adresi veriyor
- Kare kaydet → çalışma kipinde kalıyor; over değiştir → çalışma kipi;
  Bitir → bilgi ekranı
- Hiç oositi olmayan cycle; iki dilde; 25 ekran 200, JS hatası yok

---

# v6.26 — ana ekranda sol menü

Ana ekran v6.18'de eklenmişti (sayılar, hasta adı yok). Kullanıcı şimdi
giriş sonrası gelen bu ekranda **sol menü** istedi: en üstte hasta kayıtları,
altında cryo haritası, onun altında da "Yönetim" düğmesi **"Yönetici"** adıyla.

## Menü yeni bir şey değil, olanın ana ekrana taşınması

Aşama ekranlarında v6.18'den beri `.yanmenu` var — `position: fixed`, solda,
yalnızca 1100px ve üstünde. Ana ekran için ikinci bir menü tasarlamak yerine
`_gezinme.html`'e `yan_ana(kullanici)` makrosu eklendi; aynı `.yanmenu`
görünümünü kullanıyor, içeriği bir cycle'a değil programa ait.

Sıra kullanıcının söylediği gibi: **Hasta kayıtları → Cryo haritası →
Yönetici.** Altında kalın çizgiyle ayrılmış ikinci grup var (Yeni hasta,
Şifre değiştir) — bunlar ekran değil işlem, o yüzden ayrıldı ve yazıları
daha sönük. Kullanıcı bu ikisini saymamıştı ama ana ekrandan erişilen tek
yol onlardı; menüye alınmasalar geniş ekranda kaybolacaklardı.

## Telefonda menü yine düğme yığını

Personel telefonla giriyor, `.yanmenu` 1100px altında gizli. Bu yüzden ana
ekranın düğmeleri duruyor; yalnız artık `.anadugmeler` sarmalayıcısı içinde
ve geniş ekranda CSS onu gizliyor (`.asama-dugmeler` ile aynı mantık).
**İki yüzeyin sırası ve yazıları birebir aynı** — telefonda "Hasta ara ve
listele", bilgisayarda "Hasta kayıtları" yazması aynı düğmeyi iki isimle
öğretmek olurdu. İlk düğmenin metni de `hasta_kayitlari` oldu, artık
kullanılmayan `hasta_ara_listele` anahtarı silindi.

## "Yönetim" → "Yönetici"

`metinler.py`'deki `yonetim` anahtarının **değeri** değişti (tr "Yönetici",
en "Administrator"); anahtarın kendisi ve `/yonetim` rotası aynı kaldı. Aynı
anahtarı `hastalar.html` de kullandığı için oradaki düğme de aynı anda
değişti — iki ekranda aynı yere giden düğmenin farklı isimde olması istenmezdi.
Panelin kendi başlığı ("Yönetim") değişmedi.

## İzinler

Menüdeki `yetkim("cryo")` / `kullanici.rol == "yonetici"` kontrolleri yalnızca
bağlantıyı gizler. Asıl engel yerinde duruyor: modül izinleri middleware'de,
`/yonetim` rotasının başında `yonetici_kontrol(request)`. Test edilirken
embriyolog hesabıyla `/yonetim` denendi, `/hastalar`'a döndürüldü.

## Test edildi

- Yönetici: menüde üç madde + alt grup; embriyolog: "Yönetici" maddesi yok
- Embriyolog `/yonetim` → 303 `/hastalar`; girişsiz `/` → 303 `/giris`
- 1280px'te menü solda, düğme yığını gizli; 390px'te menü gizli, düğmeler
  aynı sırada
- İki dilde; 7 ekran 200, JS hatası yok

---

# v6.27 — her ekranın üstünde ana menüye dönüş

Üst çubukta v1'den beri bir geri oku var ama o **bir önceki** ekrana gider:
denüdasyondan cycle'a, cycle'dan hastaya, hastadan listeye. Ana menüye dönmek
için üç dört kez geri basmak gerekiyordu. Kullanıcı "geri dönüş olduğu gibi
ana menüye de dönüş olsun, sayfaların en üstünde" dedi.

## Tek yerde: `base.html`

Bağlantı üst çubuğa, geri okunun yanına kondu. 42 şablonun hepsi `base.html`'i
genişlettiği için hiçbirine dokunulmadı — aynı işi 42 dosyada tekrarlamak
tuzak #1'in tarifi.

Nerede basılacağı iki koşula bağlı:

```jinja
{% if (kullanici or request.state.kullanici) and request.url.path != "/" %}
```

- **Ana ekranın kendisinde** basılmaz; zaten oradasın.
- **Giriş yapılmamışken** basılmaz. İki kaynağa birden bakılmasının sebebi
  şu: middleware `request.state.kullanici`'yi yalnızca korumalı yollarda
  dolduruyor, `/sifre` ise açık bir yol (giriş ekranından da açılabiliyor,
  v6.12). Orada kullanıcıyı rotanın kendisi `oturumdaki(request)` ile bulup
  bağlama koyuyor. Tek koşul yazılsaydı şifre ekranı ya bağlantısız kalırdı
  ya da giriş yapmamış birine ana menü bağlantısı gösterirdi.

## Simge neden çizim

"⌂" (U+2302) her yazı tipinde yok; telefonda boş kare çıkma ihtimali var.
Bunun yerine satır içi SVG ev çizildi, `fill: currentColor` ile çubuğun
rengini alıyor. Dokunma hedefi geri okuyla aynı: 36×36. Yazı yerine simge
seçildi çünkü "Fertilizasyon kontrolü" gibi uzun başlıklarla birlikte
390px'e sığması gerekiyordu.

## Test edildi

- 23 ekranda bağlantı var (cycle, 11 aşama, hasta, liste, cryo, yönetim,
  kullanıcılar, şifre, silme ekranları)
- `/` ve `/giris`'te yok; `/sifre` girişliyken var, girişsizken yok;
  `/sifremi-unuttum`'da yok
- Tıklayınca `/` açılıyor
- 390px ve 1280px'te üst çubuk taşmıyor (en uzun başlık "Fertilizasyon
  kontrolü" ile ölçüldü), JS hatası yok

---

# v6.28 — ana ekran yapılacaklar listesi, cycle'ın bitişi

Kullanıcının anlattığı kâğıt düzeni:

> Laboratuvarda tedavileri bitmemiş, daha yapılacak işlemleri olan hastaların
> formlarını bir klasörde tutuyorum. Her gün geldiğimde "bugün neler
> yapılacak" diye ona bakıyorum. Hastanın işlemi bitince — embriyolar
> dondurulmuş, transfer yapılmış veya iptal olmuş olabilir — formu arşive
> kaldırıyorum.

Program bu ayrımı yapamıyordu. `cycle.durum` yalnızca `aktif` ve `iptal`
alıyordu ve `iptal`i yazan tek yer **silme ekranıydı**. Yani "işi bitti"
demenin tek yolu cycle'ı iptal etmekti — oysa dondurma ve transfer bir iptal
değil, işin olağan sonu. Üç sonu birbirine karıştırmak veriyi de bozardı
("kaç cycle iptal oldu" sorusunun cevabı yanlış çıkardı).

## Üçüncü bir durum: `tamamlandi`

`goc_027` iki kolon ekliyor:

| kolon | ne | değerler |
|---|---|---|
| `bitis_sebebi` | nasıl bitti | `dondurma` \| `transfer` \| `iptal` |
| `bitis_zamani` | ne zaman kapatıldı | kaydın kapatıldığı an |

`durum` ile eşlemesi `BITIS_DURUMU`'nda: dondurma ve transfer
`durum='tamamlandi'`, iptal ise **var olan** `durum='iptal'` değerini
kullanıyor. Böylece silme ekranının "İptali geri al" akışı olduğu gibi
duruyor. `durum` kolonunda CHECK yok, yeni değer için şema değişikliği
gerekmedi.

Eski kayıtlar `aktif` kalıyor — kimse geriye dönük bitmiş sayılmıyor,
klasörü kullanıcı kendisi boşaltacak.

## Ana ekran artık klasörün kendisi

`/` üstte **Yapılacaklar** kartını basıyor: `durum='aktif'` cycle'lar, her
satırda hasta adı, dosya no · cycle no, tedavi tipi, **OPU günü** ve **son
işlem**. Altında eski sayı özeti, en altta menü.

OPU günü satırda vurgulu, çünkü "bugün ne yapılacak" sorusuna embriyoloğun
önce baktığı sayı o. OPU'su olmayan cycle'da (FET) hiç basılmıyor —
uydurma bir gün numarası yanıltıcı olurdu. Son işlem `olay` tablosundan
geliyor (iptal edilmemiş en son kayıt); **sıradaki** aşama tahmin
edilmiyor, o klinik bir karar.

Sıra: **en eski OPU üstte.** Unutulmuş bir cycle listenin dibine düşüp
gözden kaybolmasın diye.

### v6.18 kuralı gevşetildi

v6.18'de bu ekranda hasta adı yoktu: program klinikte gün boyu açık duruyor,
ekrana bakan herkes (bekleyen hasta, hasta yakını, teknik servis) listeyi
görüyordu. Bu sefer kullanıcıya üç seçenek sunuldu — isimsiz liste (cycle no
+ aşama), sadece sayı + bir tık ötede liste, isimli liste — ve **isimli
listeyi seçti**. Kâğıt klasörün karşılığı olması adsız bir listeyle
mümkün değil. Karar kullanıcının; kendiliğinden geri alınmayacak.

## "İşlemi bitir"

Cycle ekranının altında, aşama düğmelerinin ardında. `/cycle/{id}/bitir`
ayrı bir ekran: sebep soruluyor ve yanlışlıkla basılması zorlaşıyor.
Üç seçenek, her birinin altında ne demek olduğu tek satırla yazıyor.

Ekran **silme ekranı değil** ve öyle görünmüyor: hiçbir şey silinmiyor,
cycle yalnızca listeden düşüyor, hasta ekranında rozetiyle duruyor.

**Geri al ekranda hep tek.** "Bitir" ekranından kapatılan cycle
`/cycle/{id}/bitisi-geri-al` ile dönüyor; silme ekranından iptal edilmiş eski
kayıtlar eski `/cycle/{id}/geri-al` ile. İkincisi `not c.bitis_sebebi` ile
susturuluyor, yoksa yan yana iki "geri al" çıkıyordu.

Bitirmek `yetkim("silme")` **istemiyor**, geri alması da: bitirmek günlük bir
iş, silmek değil. `yol_modulu()` bu iki yolu bilerek modülsüz bırakıyor.
Rotanın adı da bu yüzden `bitisi-geri-al` — `geri-al` deseydi
`yol_modulu()` onu "silme" modülüne düşürürdü.

`/bitenler` kâğıt düzendeki arşiv klasörü; satırlar `_cyclesatir.html`
makrosuyla ana ekranla aynı.

## Göç çalıştırılmadıysa

Tuzak #3: kullanıcının göçü çalıştırdığını varsayma. `_bitis_kolonu_var()`
kolonu yoksa ana ekran yine açılıyor (sorgu `NULL AS bitis_sebebi`'ye
düşüyor) ve tepede "goc_hepsi.py çalıştır" uyarısı çıkıyor; "İşlemi bitir"
de kaydetmeden aynı uyarıya dönüyor.

## Yol boyunca düzeltilen iki şey

- **`.rozet`'in taban biçimi yoktu.** Yalnızca `.kimlik` ve `.bilgikart`
  içinde tanımlıydı; liste satırlarındaki `.rozet.arsiv` koyu zemine koyu
  yazı basıyordu. İptal rozeti hasta ekranında zaten böyle görünüyormuş.
- **Tarayıcı dosya numarasını telefon sanıyordu.** `527078` ve `2026-09-11`
  mavi altı çizili çıkabiliyordu; `base.html`'e `format-detection` eklendi.

Ayrıca ana ekranın alt ipucusu ("hasta adları bu ekranda görünmez") artık
yalan söylediği için değişti, ve `/cycle/{id}/bitir` ekranında "Vazgeç"
yerine **"Geri dön"** kullanıldı: `vazgec` anahtarı İngilizcede "Discard"
diyor ve embriyo dondurmanın yanında klinik "discard" ile karışırdı.

## Test edildi

- Liste: OPU günü doğru (OPU 2 gün önce → "OPU günü 2"), FET'te gün yok,
  son işlem `olay`dan geliyor, işlemsiz cycle'da "işlem girilmedi"
- Bitirme: üç sebep de doğru `durum`/`bitis_sebebi`/`bitis_zamani` yazıyor
  ve `degisiklik_log`'a üç satır düşüyor
- Bitince listeden ve "Aktif cycle" sayacından düşüyor, `/bitenler`'e geçiyor
- Geri al: her iki yolda da tek düğme, alanlar `NULL`'a dönüyor
- Sebepsiz ve uydurma sebeple POST reddediliyor; `?hata=` beyaz listeden
  geçiyor (tuzak #9), liste dışı anahtar ekrana basılmıyor
- 29 ekran 200, 390px ve 1280px'te yatay taşma yok, JS hatası yok, iki dilde

---

# v6.29 — bugün bitenler, ay ay hasta kayıtları

v6.28'in üç devamı, hepsi kullanıcının isteği.

## 1. "İşlemi bitir" vitrifikasyon ve transferde de

v6.28'de düğme yalnızca cycle ekranındaydı. Oysa işin gerçekten bittiği yer
çoğu zaman vitrifikasyon ya da transfer ekranı; oradan cycle ekranına dönmek
gereksiz bir adım.

Düğme `_bitir.html` `dugme(c)` makrosunda, üç şablon da onu çağırıyor. Tek
yerde durmasının sebebi koşulun ve yazının üçünde aynı kalması: yalnızca
`durum='aktif'` cycle'da basılıyor, bitmiş olanda yerini cycle ekranındaki
"Listeye geri al" kartı alıyor. İki aşama ekranında düğme **"işlemi yapan"
kutusunun altında** — önce kim yaptı yazılır, sonra iş kapatılır.

## 2. Ana ekranda "Bugün bitenler"

v6.28'de ana ekranda bitenlere yalnızca bir bağlantı vardı. Kullanıcı gün
sonunda "bugün neyi kapattım" diye bakabilmek istedi, **ve her gün
yenilenmesini**.

Kart `date(c.bitis_zamani) = date('now','localtime')` ile besleniyor: gece
yarısı kendiliğinden boşalıyor, saklanan bir "bugünün listesi" yok. Ölçü
`localtime`, çünkü sunucu klinikte duruyor ve doğru gün yerel gün.
Tamamı "Tümü" bağlantısıyla `/bitenler`'de.

## 3. Hasta kayıtları ay ay

`/hastalar` iki işi olan tek ekran oldu:

**Arama boşken** o ayın cycle'ları — "bu ay hangi vakaları yaptık". Üstte
`‹ Eylül 2026 ›` gezgini, bulunduğumuz ayda değilsek altında **"Bu ay"**
düğmesi. Ay geçişi `_ay_kaydir()` ile, yıl sınırını kendisi çeviriyor
(Ocak'tan geri → önceki yılın Aralık'ı). `?ay=13` gibi bir değer sessizce
bulunduğumuz aya düşüyor.

**Ayın ölçüsü OPU tarihi**, yoksa cycle'ın açıldığı tarih — kullanıcının
seçimi. Üç seçenek sunulmuştu (OPU tarihi / cycle'ın açıldığı tarih / hasta
kaydının açıldığı tarih); "bu ay kaç vaka yaptık" sorusunun cevabı OPU.
FET'te OPU olmadığı için orada cycle'ın açıldığı tarihe düşülüyor.

Satır **cycle başına**, hasta başına değil: aynı hastanın Mart ve
Temmuz'daki iki cycle'ı iki ayrı satır, çünkü soru "kim kayıtlı" değil "ne
zaman ne yapıldı".

**Arama doluyken** ay süzgeci yok sayılıyor ve **hasta** satırları dönüyor.
Dosya no ya da ad aranıyorsa amaç kişiyi bulmaktır; hangi ayda olduğu
bilinseydi zaten aranmazdı. Arama kutusu ekranın en üstünde, her iki kipte
de görünür.

### Arşivlenmiş hastanın cycle'ı ay listesinde görünür

Ana ekranın yapılacaklarında görünmüyor (hasta arşivi "bu dosya kapandı"
demek), ama ay listesi bir **iş kaydı**: o cycle o ay yapıldı, dosyanın
sonradan kapanmış olması onu yapılmamış saymaz. Karışmasın diye satırda
"Arşiv" rozeti var. `?arsiv=1` eskisi gibi duruyor: arşivlenmiş hastaların
listesi, ay yok.

### Ekrandan kalkanlar

Hasta kayıtlarının altındaki **"Yönetim"** ve **"Şifre değiştir"** düğmeleri
kaldırıldı. İkisi de v6.26'dan beri ana menüde ve ana ekran her sayfadan tek
dokunuş uzakta (v6.27 ev simgesi); ekran zaten ay gezgini + liste + düğmeler
ile uzamıştı. Geri istenirse tek satır.

## Ay adları `metinler.py`'de

`strftime("%B")` kullanılmadı: o işletim sisteminin yerel ayarına bağlı ve
Windows mini PC'de İngilizce çıkabilirdi. `ay_1`…`ay_12` anahtarları var,
ekrana `ay_adi(yil, ay)` Jinja global'i basıyor.

## `cycle_listesi()` tek fonksiyon, dört görünüm

Ana ekranın yapılacaklarını, bugün bitenleri, `/bitenler` arşivini ve ay
listesini aynı sorgu üretiyor (`bitmis`, `bugun`, `ay` parametreleri). Satır
da tek: `_cyclesatir.html` `satir(s, kip)` — `yapilacak` OPU günü ve son
işlemi, `bitmis` bitiş sebebi ve tarihini, `ay` işlem tarihini gösteriyor.
Dört liste aynı görünsün diye.

## Test edildi

- Bitir düğmesi: aktif cycle'ın cycle / vitrifikasyon / transfer ekranında
  var; bitmiş cycle'da üçünde de yok
- Bugün bitenler: bugün bitirilen görünüyor; `bitis_zamani` bir gün geriye
  çekilince karttan düşüyor ama `/bitenler`'de duruyor
- Ay gezgini: Ocak'tan geri → Aralık 2025, Aralık'tan ileri → Ocak 2026;
  `?ay=13` bulunduğumuz aya düşüyor; "Bu ay" yalnızca başka aydayken
  görünüyor ve `/hastalar`'a dönüyor (tarayıcıda tıklanarak da denendi)
- Arama: dosya no ve ad ile çalışıyor, ay süzgecini yok sayıyor, hasta
  satırı döndürüyor; boş sonuç mesajı çıkıyor
- Arşivlenmiş hasta: ay listesinde "Arşiv" rozetiyle var, yapılacaklarda yok
- 31 ekran 200, iki dilde, 390px/1280px'te yatay taşma yok, JS hatası yok

---

# v6.30 — yıl ve ay açılır seçici

v6.29'da ay yalnızca `‹ ›` oklarıyla değişiyordu. Bir yıl geriye gitmek on
iki dokunuş demekti. Kullanıcı yıl ve ayın **ayrı açılır seçiciler** olmasını
istedi.

Oklar yerinde kaldı: komşu aya geçmek en sık yapılan hareket ve tek dokunuş,
seçici açıp kapatmaktan hızlı. İkisi bir arada:
`‹  [Eylül ▾]  [2026 ▾]  ›`. Sıra Türkçe okunuşa göre ay → yıl.

## Yıl aralığı veriden geliyor

`_yil_araligi()` en eski cycle'dan bugüne kadarki yılları veriyor. İki
ayrıntı:

- **`>= 2000` süzgeci var.** Bir cycle'da OPU tarihi `0026-09-04` yazıyor
  (bekleyen iş 6). Süzgeç olmasaydı seçicide iki bin satır çıkardı. Test
  edildi: o değer veriye konduğunda seçici yine yalnızca 2026 gösteriyor ve
  ana ekran ayakta kalıyor.
- **Seçili yıl listede yoksa yine de ekleniyor.** Oklarla aralığın dışına
  çıkılmış olabilir; seçicinin boş görünmemesi gerekiyor.

## JS kapalıyken de çalışır

Seçiciler `change` olayında formu gönderiyor. JS kapalıysa bunu yapacak bir
şey yok, o yüzden formda bir "Göster" düğmesi var ve **betik onu kendisi
gizliyor** — JS varsa gereksiz, yoksa tek çıkış yolu. Betiğin başında
`if (!d) return;` var: arama kipinde ay gezgini basılmıyor (tuzak #10).

## Yol boyunca: `hidden` niteliği çalışmıyordu

"Göster" düğmesi `d.hidden = true` ile gizlenmiyordu. Sebep: tarayıcının
`[hidden] { display: none }` kuralı, bizim `.aygezgin .ok { display: flex }`
kuralımızdan **daha zayıf**. Aynı tuzağa daha önce de düşülmüş — CSS'te
`.bilgikart[hidden]`, `.uyari[hidden]`, `.tabaka[hidden]` gibi **yedi ayrı**
elle yazılmış kural vardı, hepsi aynı sorunun tek tek yamaları.

Tepeye tek kural konuldu:

```css
[hidden] { display: none !important; }
```

Eski yedi kural duruyor (artık gereksizler ama zararsızlar); bundan sonra
`el.hidden = true` her yerde çalışıyor.

## Test edildi

- Ay ve yıl seçilince sayfa kendiliğinden gidiyor; adres iki parametreyi de
  taşıyor (`?ay=11&yil=2025`)
- "Göster" düğmesi JS açıkken gizli; oklar ve "Bu ay" eskisi gibi
- Yıl aralığı 2024'e kadar eski bir kayıt konunca genişliyor, aralık dışı
  bir yıla (`?yil=2023`) gidilince o yıl da listeye giriyor
- Bozuk `0026-09-04` tarihiyle seçici şişmiyor, ekranlar 200
- 32 ekran 200, iki dilde, 390px/1280px'te yatay taşma yok, JS hatası yok

---

# v6.31 — bitiş saati elle, bitişi düzenle, hasta kaydına kestirme

## 1. Bitiş saati elle girilebiliyor

v6.28'de `bitis_zamani` otomatik yazılıyordu: düğmeye basıldığı an. Bu
projenin kendi kuralına aykırıydı —

> **İşlem saatleri elle girilebilir.** Her aşamada varsayılan "şu an", ama
> değiştirilebilir; personel işlemi yaparken değil sonra kaydediyor olabilir.
> Bu özelliği asla kaldırma.

— ve kullanıcı ilk kullandığında fark etti. Bitir ekranının başına
`datetime-local` alanı kondu, öteki aşama ekranlarıyla aynı: varsayılan "şu
an", boş ya da bozuk girilirse yine "şu an" (`islem_zamani()` yardımcısı).

Yan etkisi bilinçli: **geriye tarihlenen bir bitiş "Bugün bitenler"de
görünmez.** Kart `date(bitis_zamani) = bugün` diyor; 5 Eylül'de bitmiş bir
cycle bugünün listesine girmemeli. `/bitenler` arşivinde kendi tarihiyle
duruyor.

Saat biçimi de düzeldi: `bitis_zamani` artık öteki tablolarla aynı
`YYYY-MM-DD HH:MM:SS` biçiminde yazılıyor (önce `isoformat()`'ın `T`'li hali
kullanılıyordu — SQLite ikisini de anlıyor, ama tek biçim daha az sürpriz).

## 2. Bitişi düzenleme

Bitmiş cycle'ın kartına **"Düzenle"** düğmesi eklendi:
`/cycle/{id}/bitir?duzenle=1`. Sebep ve saat dolu geliyor, kayıtlı sebep
"Seçili" rozetiyle işaretli — yalnızca saati değiştirmek isteyen hangi
düğmeye basacağını görüyor.

**Düzenle cycle'ı listeye döndürmez.** "Listeye geri al" ayrı bir düğme;
ikisi farklı iş ve karışmaları pahalı olurdu. Kartta ikisi de var, Düzenle
üstte.

Hata dönüşü `?hata=...&duzenle=1` — v6.21'deki kural: hata mesajı formu
kapatmamalı.

## 3. Ay listesinden hastanın tüm kaydına

Kullanıcı: "ilgili ayda hastayı bulunca o aydaki tedaviyi görüyorum ama bir
de hastanın bütün kaydını görebileceğim bir buton olsun."

Ay listesinin her satırının sağına **"Hasta kaydı"** düğmesi kondu. Satırın
kendisi o ayki cycle'a, düğme hastanın tüm geçmişine (`/hasta/{id}`)
gidiyor.

İç içe `<a>` yazılamayacağı için ikisi kardeş; sarmalayan `.satirikili`
yan yana diziyor. Tarayıcıda denendi: satır cycle'a, düğme hastaya gidiyor
ve sayfada iç içe bağlantı yok.

Düğme **yalnızca ay listesinde** (`kip="ay"`); ana ekranın yapılacaklarında
ve `/bitenler`'de yok — istenmedi, liste de dar.

## Test edildi

- Geçmiş tarihle bitirme: kayıt o tarihi alıyor, "Bugün bitenler"e girmiyor,
  `/bitenler`'de doğru tarihle duruyor
- Düzenle: saat tek başına değişiyor; sebep dondurma → transfer → iptal
  değiştirilebiliyor ve `durum` buna göre `tamamlandi` / `iptal` oluyor
- Sebepsiz gönderim düzenleme kipinde kalıyor (`&duzenle=1`)
- "Listeye geri al" alanları `NULL`'a çekiyor
- "Hasta kaydı" düğmesi `/hasta/1`'e, satır `/cycle/2`'ye gidiyor; iç içe
  `<a>` derinliği 1
- 33 ekran 200, iki dilde, 390px/1280px'te yatay taşma yok, JS hatası yok

---

# v6.32 — çözmede geri oku geldiğin yere döner

Kullanıcı: "Çözme bölümünde içeriği gör'e girdikten sonra geri aynı sayfaya
değil cryo haritaya dönüyor."

Doğru: taşıyıcı ekranının geri oku `/cryo`'ya sabitlenmişti. Cryo
haritasından girildiğinde doğru, çözme ekranından girildiğinde yanlış — iki
farklı yerden gelinen bir ekranın tek bir geri adresi olamaz.

## Serbest adres değil, cycle numarası

Çözme ekranındaki bağlantılara `?cycle={{ c.id }}` eklendi; taşıyıcı ekranı
geri adresini **kendisi kuruyor**: `/cycle/<n>/thaw`.

Projede `?geri=<yol>` diye serbest adres taşıyan bir kalıp da var
(`goruntu_sil`, `foto_ekle`). Burada bilerek kullanılmadı: adresten gelen
metin doğrudan `href`'e yazılıyor ve `javascript:` gibi bir değer
girilebiliyor. Sayı almak bu kapıyı açmıyor, üstelik bu bölgede zaten
`?cycle=` kalıbı vardı (`/cryo/tasiyici/<id>/thaw?cycle=<n>`). Değer ayrıca
"böyle bir cycle var mı" diye doğrulanıyor; yoksa `/cryo`'ya düşüyor.

Aynı zincirin bir alt basamağı da düzeltildi: çözme **formunun** geri oku ve
"Vazgeç" düğmesi de cycle'ı taşıyor, böylece form → taşıyıcı → çözme ekranı
yolu baştan sona geri geliyor.

## Test edildi

- Çözme → "içeriği gör" → geri: `/cycle/1/thaw` (tarayıcıda tıklanarak)
- Cryo haritası → taşıyıcı → geri: `/cryo` (eskisi gibi)
- `?cycle=999` (olmayan cycle) → `/cryo`; `?cycle=abc` → 422
- Çözme formu: cycle'lı ve cycle'sız geri adresleri doğru
- 13 ekran 200, JS hatası yok

---

# v6.33 — takvim: ileri tarihli işler

Kullanıcı: "Ana sayfada ileri günler için hasta ekleme olsun. Mesela haftaya
14/09/2026 Pazartesi tarihine FET olacak diye kayıt açabileyim. Ana sayfada
ileri tarihte neler varmış diye bakabileyim. Takvim bölümü olsun."

## Plan ayrı bir randevu kaydı değil, cycle'ın kendisi

Üç seçenek soruldu (2026-09-11) ve kullanıcı **cycle'a planlanan tarih**
seçeneğini seçti: FET cycle'ı bugün açılıyor, `planlanan_tarih` giriliyor.
Ayrı bir randevu tablosu aynı hastayı iki kez girdirirdi; bu yolda gün
geldiğinde cycle zaten hazır.

`goc_028` tek kolon ekliyor: `planlanan_tarih` (`YYYY-MM-DD`, saat yok —
plan gün bazında yapılıyor).

### Planlanan iş Yapılacaklar'ı kirletmiyor

Bu, kâğıt klasör mantığıyla doğrudan çakışan noktaydı: cycle açıldığı anda
ana ekrandaki Yapılacaklar'a giriyordu. Haftaya olacak bir FET bu hafta
boyunca her sabah listede duracaktı — oysa o form henüz klasöre girmemiş
olurdu.

Kural: **tarihi gelecekte olan cycle Yapılacaklar'da görünmez.** Takvimde ve
"Yaklaşanlar"da durur; tarih gelince (`<= bugün`) kendiliğinden listeye
düşer. `planlanan_tarih` boş olan cycle eskisi gibi davranır, eski kayıtların
hiçbiri etkilenmedi.

## Üç yüzey

| nerede | ne gösterir |
|---|---|
| Ana ekran → **Yaklaşanlar** | önümüzdeki **14 gün** (`YAKLASAN_GUN`) |
| **`/takvim`** | seçili ayın tamamı, gün gün |
| Cycle ekranı | "Planlandı" rozeti + Zamanlar kartında tarih |

"Yaklaşanlar" bugünü **içermez** — tarihi gelen iş artık "yaklaşan" değil,
Yapılacaklar'da. İki hafta seçildi çünkü plan "haftaya" diye yapılıyor, bir
hafta dar kalırdı.

Takvim **ay ızgarası değil, gün gün liste**: telefonda okunaklı ve işi
olmayan günler hiç yer kaplamıyor. Ay seçici hasta kayıtlarındakiyle birebir
aynı (v6.30) — aynı düzeni iki ekranda iki türlü öğretmek personeli yorar.
Gün başlığı `takvim_basligi()` ile: "14 Eylül 2026 Pazartesi", bugünse
yanında "Bugün" rozeti.

Gün adları da ay adları gibi `metinler.py`'de (`gun_1`…`gun_7`, ISO sırası).
`strftime("%A")` işletim sisteminin yerel ayarına bağlı; Windows mini PC'de
İngilizce çıkardı.

## Göç çalıştırılmazsa cycle açmak bozulmamalı

Burada tuzak #3'ün bedeli ağırdı: `planlanan_tarih` doğrudan
`CYCLE_ALANLARI`'na eklenince, göç çalıştırılmamış bir veritabanında
**cycle açmak tümden patlardı** — çekirdek bir akış.

`cycle_alanlari()` kolon yoksa alanı INSERT/UPDATE'ten çıkarıyor. Gerçekten
denendi: kolon geçici olarak düşürüldü, 8 ekran 200 verdi, takvimde göç
uyarısı çıktı ve cycle açma çalıştı.

## Test edildi

- Planlanan tarih 14 Eylül (bugün 11'i): Yapılacaklar'da yok, Yaklaşanlar'da
  var, takvimde Eylül'de var
- Bugün: Yapılacaklar'da var, Yaklaşanlar'da yok
- Geçmiş (1 Eylül): Yapılacaklar'da var
- 20 Ekim (14 günden uzak): ikisinde de yok, takvimde Ekim'de var
- Boş: eskisi gibi
- Form: tarih kaydediliyor, boş gönderilince `NULL` oluyor
- Takvim ay seçici ve "Bu ay" tarayıcıda tıklanarak denendi
- Göçsüz veritabanında ekranlar ayakta, cycle açılıyor
- 36 ekran 200, iki dilde, 390px/1280px'te yatay taşma yok, JS hatası yok

---

# v6.34 — ana ekran iki sütun, aramadan geri dönüş

## Yapılacaklar ve Bugün bitenler yan yana

Kullanıcı: "böyle yukarıdan aşağı değil de Yapılacaklar ve Bugün bitenler yan
yana, Yaklaşanlar onların altına."

İkisi `.ikisutun` sarmalayıcısında. **720px'in altında alt alta** — telefonda
iki sütun okunmuyor ve personel telefonla giriyor. Alt alta düşerken sıra
HTML sırasıyla aynı kalıyor: Yapılacaklar → Bugün bitenler → Yaklaşanlar,
yani iki düzen aynı şeyi öğretiyor.

`align-items: flex-start`: boş bir kart ötekinin boyuna uzamıyor. "Bugün
biten işlem yok" kartı sabah boş oluyor ve Yapılacaklar uzunsa yanında
kocaman bir boşluk açardı.

### Sütun 640px'e sıkışmıyordu

Yan yana koyunca ortaya çıktı: `.kap` her ekranda 640px ve iki kart 296px'e
düşüyordu, 1280px'lik ekranda sağda yarım ekran boş kalıyordu. Satırdaki
"IVF/ICSI · OPU günü 2 · Son işlem: …" iki satıra sarıyordu.

Ana ekran `kap genis` sınıfını alıyor (`base.html`'e `{% block kapsinif %}`
eklendi) ve sütun genişliyor. Ölçü yan menüye göre sınırlı:

```css
@media (min-width: 860px)  { .kap.genis { max-width: 940px; } }
@media (min-width: 1100px) { .kap.genis { max-width: max(640px, min(940px, calc(100vw - 500px))); } }
```

Yan menü 1100px'ten sonra soldaki 216px'i kaplıyor; ikinci kural sütunu
`100vw - 500px` ile sınırlayıp çarpışmayı önlüyor, `max(640px, …)` de dar
ekranda sütunun eski ölçünün altına inmesini engelliyor. Sekiz genişlikte
ölçüldü (390 → 1920), hiçbirinde menü ile çakışma ve yatay taşma yok;
kartlar 1280px'te 296 → **366px**, 1600px'te **446px**.

## Aramadan geri dönüş

Kullanıcı: "hasta kayıtlarında arama yaptıktan sonra geri hasta kayıtları
sayfasına dönmüyor."

Doğru: geri oku `/`'a sabitti, arama sonucundan basınca programın ana
ekranına çıkıyordu. v6.32'deki taşıyıcı ekranının aynı hatası — bir ekran
iki durumda görünüyorsa tek geri adresi yetmiyor.

```jinja
href="{{ '/hastalar' if (ara or arsiv) else '/' }}"
```

Arama ya da arşiv sonucundayken ay görünümüne, orada zaten isek ana ekrana.
Tarayıcıda denendi: `/hastalar?ara=Test` → geri → `/hastalar` → geri → `/`.

## Test edildi

- 390 / 720 / 768 / 900 / 1100 / 1280 / 1600 / 1920 px: sütun genişliği,
  kart genişliği, menü çakışması ve yatay taşma ölçüldü — hepsi temiz
- 720px altında kartlar alt alta ve sıra bozulmuyor
- Geri oku: ay görünümünde `/`, aramada ve arşivde `/hastalar`
- 33 ekran 200, iki dilde, JS hatası yok

---

# v6.35 — örnek kodu araması, ekranlar ilk örnekten açılıyor, fotoğrafsız örneğin kutusu

Kullanıcının üç isteği: "oosit kodunu arama da olsun", "denüdasyondan
ICSI'ye fertilizasyona embriyolara geçişte alanlar açıldığında hep ilk
fotodan başlasın en son kaydedilen fotodan değil", "fotoğrafsız eklemede
denüdasyonda, ICSI'de içinde oosit yazsın, fertilizasyonda zigot,
embriyolarda embriyo".

## Örnek kodu araması

Örnek kodu (`527078-2026-0001-03`) tüpün, pipetin ve formun üstünde yazan
şeydir. Şimdiye kadar program o kodu **gösteriyordu ama aramıyordu**:
elinde kod olan personel "bu kim" sorusunu ancak dosya no'yu ayırıp
aratarak çözebiliyordu.

Kodun yapısı: `<hasta dosya no>-<cycle no>-<sıra>`. Son iki parça
`specimen.id`, ilk parça hastadan geliyor; arama ikisini birleştirip
tarıyor, böylece hem tam kod hem kodun kuyruğu (`0001-03`) buluyor:

```sql
WHERE (CAST(h.dosya_no AS TEXT) || '-' || s.id) LIKE ?
```

İki yerde:

- **Hasta kayıtları** (`/hastalar`) — sonuçlar "Örnek kodu" kartında, hasta
  satırlarının **üstünde**. Satır o örneğin **cycle'ına** gidiyor: kod
  arandıysa soru "bu kim" değil, "bu hangi tedavi". Yalnız örnek bulunduysa
  altına boş bir "uyan kayıt yok" kartı basılmıyor.
- **Cryo haritası** (`/cryo?ara=`) — tanktaki tüpün üstünde yazan kod
  çoğu zaman aranan şeyin kendisi.

İki karar:

- **Arama yalnızca tire içeren metinde örnek arıyor.** Kod biçimi gereği
  tireli; tiresiz bir metin kod değildir. Yoksa "3" yazan biri bütün
  örnekleri listelerdi. (`527078` yazınca yalnızca hasta çıkıyor, kod
  `527078-2026-0001-01` yazınca örnek.)
- **Örnek araması hastanın arşivlenmiş olmasına bakmaz.** Dolapta duran bir
  örneğin dosyası kapanmış olabilir; kodu okunuyorsa bulunabilmeli. (Hasta
  araması eskisi gibi `durum='aktif'` süzüyor.)

## Ekranlar ilk örnekten açılıyor

Denüdasyon, ICSI, fertilizasyon, gün 2/3 ve blastokist ekranları adreste
`?oosit=N` yoksa **sonuncuyu** seçiyordu (ICSI ve sonrasında önce "ilk
kaydedilmemiş", o da yoksa sonuncu). Aşamalar arasında geçerken ekran her
seferinde listenin sonunda açılıyordu; kullanıcı baştan başlamak istiyor.

Beş ekranda da varsayılan artık `oositler[0]`. Toplu giriş akışı bozulmadı:
"kaydet → sıradaki oosit" zaten **adrese yazarak** geçiyor
(`?oosit=<sıradaki kaydedilmemiş>`), varsayılan yalnızca ekran ilk kez
açıldığında devreye giriyor. Hepsi kaydedilmişse adres bir şey söylemiyor
ve ekran başa dönüyor — doğru davranış.

Denüdasyon bunun istisnasıydı: POST adrese oosit yazmıyor,
`?duzenle=oosit`'e dönüp "sonuncu" varsayılanına güveniyordu. Yani yeni
eklenen oosit ekranda kalıyordu. Varsayılan ilke çekilince bu kırılırdı, o
yüzden **seçim POST'a taşındı**: yeni/aynı/fotoğrafsız kaydından sonra
sunucu o örneğin sırasını adrese yazıyor, atla ve geri al ise formdaki
gizli `secili` alanını taşıyor. Alan adrese yazıldığı için yalnızca rakam
kabul ediliyor.

## Fotoğrafsız örneğin kutusu

Fotoğrafsız örnek olağan (kamera boş, kare bulanık, sonradan eklenecek),
ama o örneğe geçince ekranın ortası boşalıyordu — hangi kayıtta olduğun
ancak yukarıdaki şeride bakınca anlaşılıyordu. Beş ekranda beş ayrı boşluk
vardı: ikisi "Bu aşamaya ait fotoğraf yok" kartı, biri o kart ama
"Fotoğraf ekle" bağı olmadan (fertilizasyon — gözden kaçmış), ikisi hiçbir
şey.

Tek makro: `_kareler.html` `yer(ad, sp, ekle_yolu)`. Fotoğrafın tuttuğu
yeri tutuyor (kesikli kenarlık, `.foto.yok`), içinde örneğin **o aşamadaki
adı** ve sırası, altında fotoğraflı halindeki gibi örnek kodu:

| Ekran | Yazan |
|---|---|
| Denüdasyon, ICSI | Oosit *n* |
| Fertilizasyon | Zigot *n* |
| Gün 2/3 | Cleavage *n* |
| Blastokist | Blastokist *n* |

Ad çağıran ekrandan `ornek_adi(asama, cycle_tipi)` ile geliyor, makroya
sabit yazılmadı — dil değişince ekrandaki isim de değişmeli. İlk denemede
gün 2/3 ve blastokistte "Embriyo" yazıyordu; kullanıcı ekranın kendi adını
istedi, kutu artık başlıkla aynı şeyi söylüyor.

## Test edildi

- Arama: tam kod, kuyruk (`0001-01`), yalnız tire (`-01`), ad, dosya no ve
  eşleşmeyen tireli metin — kart doğru çıkıyor/çıkmıyor
- Beş aşama ekranı adressiz açıldığında ilk örneği seçiyor (şerit, başlık
  ve örnek kodu ile doğrulandı)
- Denüdasyon POST'u: fotoğrafsız ×3 → `&oosit=2/3/4`; atla `secili=3` →
  `&oosit=3`; `secili=javascript:alert(1)` → adrese yazılmıyor
- ICSI toplu giriş: 1 → 2 → 3 → 4 → (sıradaki yok) başa
- Fotoğrafsız kutu beş ekranda: Oosit / Oosit / Zigot / Embriyo / Embriyo
- 39 ekran 200, iki dilde, JS hatası yok, 390px'te yatay taşma yok
- Test verisi geri alındı (1 hasta, 2 cycle, 1 örnek, 0 olay)

---

# v6.36 — Excel çıktısı

Kullanıcının sorusu: "tüm bu kayıtlar bir excel formatında çıktı alınabilir
mi?" Dört çıktı ve dosya biçimi kullanıcının seçimi (2026-09-11).

## Neden kütüphanesiz

Seçenekler: hazır bir kütüphane (`openpyxl`), CSV, ya da dosyayı elle yazmak.
Kullanıcı **"gerçek .xlsx, ek kurulum yok"** dedi ve bu proje için doğru
seçim:

- **CSV**, Türkçe Windows'ta tuzaklı: Excel ayraç olarak noktalı virgül
  bekler, dosya BOM'suz UTF-8 ise ı-ş-ğ-ö-ü-ç bozulur ve bütün satır tek
  hücreye düşer. Ayarlanabilir ama yine "gerçek Excel dosyası" olmaz —
  tarih tarih değildir, süzgeç yoktur.
- **`openpyxl`** hem Mac'e hem klinikteki Windows mini PC'ye kurulmalıydı.
  Proje bugüne kadar dört bağımlılıkla (`fastapi uvicorn jinja2
  python-multipart`) idare ediyor; beşincisi iki makinede takip edilecek bir
  şey daha demek.
- **Elle yazmak**: `.xlsx` içinde XML dosyaları olan bir ZIP; Python'un kendi
  `zipfile` modülü yetiyor. `excel.py` ~300 satır ve hiçbir şey kurulmuyor.

`excel.py` ne veriyor: gerçek tarih hücreleri (sıralanabilir, süzülebilir),
sayı hücreleri, donmuş başlık satırı, süzgeç okları, içeriğe göre sütun
genişliği, Türkçe karakterler bozulmadan.

İki incelik:
- **Hücrenin türü değerden anlaşılıyor.** `"2026-09-11"` tarih, `"2026-09-11
  08:15"` tarih+saat, sayı sayı, gerisi metin. Veritabanı zaten ISO metin
  sakladığı için çağıran tarafın tür belirtmesi gerekmiyor.
- **Yılı 1900'den küçük tarih metin olarak yazılıyor.** Excel'in tarih sayacı
  1900'den başlıyor; veritabanındaki bozuk `0026-09-04` OPU tarihi (bekleyen
  iş 6) tarihe çevrilseydi dosya bozulurdu. Aynı koruma `2026-02-30` gibi
  olmayan günleri de yakalıyor.
- Denetim karakterleri ayıklanıyor: serbest metin alanlarına yapıştırma
  yoluyla girmiş bir karakter Excel'e dosyayı "bozuk" dedirtir.

Üretilen dosya `openpyxl` ile geri okunarak doğrulandı (bu makinede yalnızca
test için kuruldu, projeye girmedi): sayfalar, hücre türleri, tarih biçimi,
donmuş bölme, süzgeç, Türkçe karakterler, XML kaçışı.

## Dört çıktı

| Yol | Ne | Satır |
|---|---|---|
| `/disari/ay?yil=&ay=` | O ayın vakaları | Bir cycle |
| `/disari/cycle/{id}` | Bir cycle'ın tamamı | Bir örnek (+ bilgi sayfası) |
| `/disari/cryo` | Dolabın dökümü | Bir örnek |
| `/disari/tumu` | Ham tablo dökümü | Tablo başına bir sayfa |

- **Ay listesi** istatistik için: dosya no, hasta, tip, endikasyon, protokol,
  OPU, sonra sayılar — toplam oosit, sağ/sol, MII, ICSI, 2PN, gün 2, gün 3,
  blastokist, donan, çözülen, transfer — ve bitiş. Ayın ölçüsü ekrandakiyle
  aynı: OPU tarihi, yoksa cycle'ın açıldığı tarih.
  **Çözme ve transfer sayısı tedavinin yapıldığı cycle'a yazılıyor**
  (`thaw_cycle_id` / `tr_cycle_id`), örneğin geldiği cycle'a değil: FET
  cycle'ında oosit yoktur ama transfer vardır.
- **Cycle detayı** hastanın dosyasına konacak çıktı. İki sayfa: cycle
  bilgisi (alan/değer) ve örnekler (oosit başına bir satır, denüdasyondan
  transfere 36 sütun). İki sayfa, çünkü protokol bilgisi tek satırlık değil
  tek sütunluk bir liste; 40 oositlik tabloya sıkıştırmak okunmaz yapardı.
- **Cryo dökümü** çözülmüş örnekleri de içeriyor, "Dolapta" sütunu ayırıyor.
  Böylece aynı dosya hem bugünkü sayımı hem taşıyıcının geçmişini veriyor.
- **Tüm veri** ham: kodlar etikete çevrilmiyor, kolon adları veritabanındaki
  adlar. Amaç okumak değil aktarmak.

Ötekilerde **kod değil etiket** yazıyor (`mii` → MII, `2pn` → 2PN): listeler
laba özgü ve yönetici düzenleyebiliyor, ekranda ne görünüyorsa Excel'de de o
görünmeli. Etiketler tek sorguda okunup sözlüğe alınıyor — satır başına
sorgu atmak 40 oositlik bir cycle'da 400 sorgu ederdi.

`specimen.durum` bunun istisnası, **kodla yazılıyor**. Kolonun on dörde yakın
değeri var (oosit, zigot, immatur, degenere, enjekte, gun2, morula,
kavitasyon, blastokist, dondurulmus, transfer_edildi, discard, kayip,
arrest); bir kısmının `metinler.py`'de karşılığı var, çoğunun yok. Yarısını
çevirmek sütunu tutarsız yapardı ("Dondurulmuş" ile "enjekte" yan yana),
eksiklerini uydurmak ise klinik bir varsayım olurdu. Etiket listesi
kullanıcıyla kararlaştırılınca tek satırla çevrilebilir.

## İzinler

Excel çıktısı ekranda görülebilen veriyi dosyaya yazıyor; izni de ekranın
izni olmalı:

- Ay listesi ve cycle detayı görüntüleme ekranları gibi serbest (`yol_modulu`
  onlara `None` diyor) — hasta listesi ve cycle özeti de öyle.
- Cryo dökümü `cryo` modülüne bağlı. Yetkisi olmayan kullanıcı `/cryo` gibi
  `/disari/cryo`'dan da döndürülüyor; denendi.
- **Tüm veri yalnızca yönetici.** Ötekiler ekrandaki veriyi verir, bu
  laboratuvarın bütün hasta kayıtlarını tek dosyada klinik dışına
  çıkarabilir. Rota `yonetici_kontrol(request)` ile başlıyor — düğmeyi
  gizlemek yetmez, sunucu da reddetmeli (hasta silmedeki kuralın aynısı).
  Yönetici olmayan kullanıcıyla denendi: `/hastalar`'a dönüyor.

**Dökümde şifre özeti ve oturum anahtarı yok.** `oturum` ve `yetki` tabloları
hiç çıkmıyor; `kullanici` tablosundan yalnızca kimlik alanları alınıyor
(`kullanici_id` kolonlarının kimi gösterdiği okunabilsin diye). Dosyanın
içinde veritabanındaki `sifre_hash` ve jeton değerlerinin geçmediği
doğrulandı.

Dosya `Content-Disposition: attachment` ile **indiriliyor**, tarayıcıda
açılmıyor: içinde hasta adı var, ekranda açık kalmasın.

## Başlıklar Türkçe kaldı

Excel'deki sütun başlıkları ve sayfa adları doğrudan yazıldı,
`metinler.py`'ye girmedi — hücre **değerleri** iki dilde doğru çıkıyor ama
başlıklar çıkmıyor. Sebep: ~90 başlığın İngilizcesi klinik bir sözlük ve onu
uydurmak kullanıcının işi ("klinik bir varsayım yapman gerekiyorsa yapma").
Çeviri zaten askıda; bekleyen iş 8'e eklendi.

## Test edildi

- Üretilen dosya `openpyxl` ile geri okundu: hücre türleri, tarih biçimi,
  donmuş bölme, süzgeç aralığı, sayfa adı kısaltma ve tekrar önleme
- Uç değerler: bozuk tarih (`0026-09-04`), olmayan gün (`2026-02-30`),
  `&`/`<`/`"`, denetim karakteri, boş hücre, negatif sayı, ondalık, bool
- Dört çıktı gerçek veriyle (5 örnek, 23 olay, bir taşıyıcı, bir FET
  transferi): sayılar elle doğrulandı, FET'in transferi FET cycle'ında çıktı
- İzinler: yönetici olmayan, cryo yetkisi olmayan, giriş yapmamış kullanıcı
- Boş ay (yalnızca başlık satırı), olmayan cycle (`/hastalar`'a dönüyor),
  geçersiz ay numarası
- 30 ekran 200, iki dilde, JS hatası yok, 390 ve 1280px'te yatay taşma yok
- Test verisi geri alındı (1 hasta, 2 cycle, 1 örnek, 0 olay, 0 taşıyıcı)

---

# v6.37 — resmî formlar ve zaman çizelgesi

Kullanıcı iki form gönderdi ve "bu formlar benim tutma zorunluluğumun olduğu
formlar, programdaki verileri forma işletip çıktı alıp fiziksel dosyasına
koymak istiyorum" dedi. Formlar Akdeniz Üniversitesi Tıp Fakültesi ÜYTE
Merkezi'nin kalite sisteminden:

- **Embriyoloji Özet Formu** — DH.FR.91 Rev.03, dikey, cycle başına bir sayfa
- **ART Lab. Raporu** — DH.FR.107 Rev.01, yatay, oosit ızgaralı

Gönderilen `.xls` dosyaları okundu (birleşik hücreler, sütun genişlikleri,
satır yükseklikleri, künye şeridi) ve kalıp birebir yeniden kuruldu.

## İki çıktı, tek içerik

Kullanıcının seçimi "ikisi de" oldu:

- **Yazdırılabilir sayfa** — `/form/ozet/{id}`, `/form/artlab/{id}`. Ekranda
  açılıyor, Ctrl+P ile kâğıda ya da PDF'e. `@media print` üst çubuğu, menüyü
  ve düğmeleri gizliyor; kâğıda yalnızca form iniyor. ART raporu yatay
  basılıyor (`@page yatay`), 13 sütunluk ızgara dikey A4'e sığmıyor.
- **Excel** — `/disari/form/ozet/{id}`, `/disari/form/artlab/{id}`.

İçerik tek yerden geliyor (`formlar.py` `*_verisi()`), yerleşim ikiye ayrılmış
durumda. Böylece bir alan değiştiğinde iki çıktı birbirinden ayrı düşmüyor.

`excel.py` bunun için genişletildi: **yerleşim sayfası**. Tablo sayfasından
farkı, hücrelerin adresle verilmesi (`{"C8": (değer, "deger")}`) — form kâğıdı
satır-sütun düzeni değil, belirli kutulara yazılan bir kalıp. Birleşik hücre,
kenarlık, dolgu, sütun genişliği, satır yüksekliği ve yazdırma ayarı (A4,
dikey/yatay, tek sayfaya sığdır) eklendi. Dokuz stil tanımlı; sıraları
`styles.xml`'e sayı olarak yazıldığı için **araya stil eklenmez, sona eklenir**.

## Zaman çizelgesi

Formun satır başlıkları saat cinsinden: "PM durumu (18 sa)", "24 saat",
"40-45 saat", "72 saat". Bunları programın gün bazlı kayıtlarına (fert
kontrolü, gün 2, gün 3) eşlemeyi önerdim; kullanıcı **kabul etmedi** ve daha
iyisini istedi: "programda tarih ve saat girip bir önceki işlem üzerinden kaç
saat geçmiş ise onun yazılacağı bir bölüm ekle."

Doğru olan bu: eşleme bir varsayım olurdu, hesap ise veri. `zaman_cizelgesi()`
cycle'ın bütün aşama saatlerini toplayıp iki süre veriyor — **önceki işlemden**
ve **OPU'dan bu yana**. İkisi birden, çünkü "kaç saatte bir baktık" ile
"kaçıncı saatteki değerlendirme" ayrı sorular; formun satır başlıkları
ikincisini soruyor.

Üç karar:
- **Ayrı kayıt tutulmuyor.** Saatler zaten her aşama ekranında elle
  girilebiliyor ("işlem saatleri elle girilebilir" kuralı); çizelge onlardan
  türüyor. İkinci bir yere yazmak veriyi ikiye ayırırdı.
- **Sıra zamana göre, klinik akışa göre değil.** Aynı gün önce transfer edip
  sonra kalanı dondurmak olağan; akış sırası kullanılsaydı o satır **eksi
  saat** gösterirdi. Testte tam olarak bu çıktı, düzeltildi.
- **Zamanı girilmemiş aşama çizelgede yok.** Boş satır "o iş yapılmadı" ile
  "saati girilmedi"yi karıştırırdı.

Çizelge cycle ekranında bir kart, ART raporunda da formun kendi "İŞLEM /
Tarih / Sa." bloğunu dolduruyor.

## Programda karşılığı olmayan alanlar

Kullanıcı "daha sonra düşüneyim" dedi; şimdilik **boş kutu** çıkıyorlar,
kalemle dolduruluyor. Uydurmak, resmî bir forma yanlış veri yazmak olurdu.

| Form | Boş çıkan |
|---|---|
| Embriyoloji Özet | Kimlik no, Empty zona, Morfolojik anomalili, İntakt, Transfer klinisyen |
| ART Lab | Tüp (folikül), Medium/Lot (IVF, sperm prep, PVP, hyalüronidaz, freeze/thaw pack), Seleksiyon, Raporu dolduran |

**Ad ve soyad** formda iki ayrı kutu, programda tek alan (`ad_soyad`). Son
kelime soyadı sayılıyor — Türkçede olağan yazım ve alan adının söylediği sıra.
Bileşik soyadlarda yanılabilir; resmî formda boş kimlik kutusu bırakmaktansa
doldurup kullanıcının görüp düzeltmesi tercih edildi. Hasta kaydında ad ve
soyad ayrılırsa `_ad_soyad_ayir()` tek satırla düzelir.

`x10⁶` üst simgesi bazı yazıcılarda bozuk çıktığı için kâğıt aslındaki gibi
`x106` yazılıyor.

## Ortaklaşan iki SQL parçası

`gun_alt()` ve `son_alt()` (örnek başına alt sorgu kuran iki küçük fonksiyon)
hem `disari.py` hem `formlar.py` tarafından kullanılıyor. `formlar.py`'de
duruyorlar, `disari.py` oradan alıyor — iki kopya birbirinden ayrı düşerdi.

## Test edildi

- 8 oositlik gerçekçi fikstür (5 MII, 4×2PN, 3 blastokist, 2 transfer,
  1 dondurma, bazal + hazırlık sonrası sperm analizi, beş aşamada işlemi
  yapan): iki formun iki çıktısı da elle doğrulandı, sayılar tutuyor
- Yazdırma görünümü tarayıcıda (`emulate_media("print")`) ve PDF olarak
  alındı: özet formu A4 dikeyde tek sayfa, ART raporu A4 yatayda tek sayfa
- Üretilen `.xlsx`'ler `openpyxl` ile geri okundu: birleşik hücreler,
  kenarlık, dolgu, sayfa yönü, tek sayfaya sığdırma
- Çizelge: eksi saat hatası bulundu ve düzeltildi (zamana göre sıralama)
- Bilinmeyen form adı (`/form/yok/1`) cycle'a dönüyor — şablon adı adresten
  gelen metinle kurulmuyor, beyaz listeden geçiyor
- 13 ekran 200, JS hatası yok, yatay taşma yok

---

# v6.38 — yönetici panelinde istatistikler

Kullanıcının sorusu: "yapılan her kayıt hasta olsun cycle olsun opu olsun,
yönetici bölümünde yer alan bir istatistikler bölümüne anlık kaydedilebilir
mi?"

## Kaydedilmiyor — hesaplanıyor

Cevap "evet" ama sorulandan biraz farklı: **kaydetmeye gerek yok, zaten
kayıtlı.** `/istatistik` her açılışta sayıları `hasta`, `cycle`, `specimen` ve
`olay` tablolarından hesaplıyor.

Ayrı bir sayaç tutmak aynı bilgiyi iki yere yazmak demek. İkisi er geç ayrı
düşer — bir kayıt silinir, bir göç araya girer, bir işlem yarım kalır — ve
hangisinin doğru olduğu anlaşılmaz. Türetilmiş sayı her zaman doğrudur; cryo
haritasının türetilmiş olmasıyla aynı gerekçe. Ekranın altında bunu söyleyen
bir not var, kullanıcı sayıların nereden geldiğini bilsin diye.

## Ne gösteriyor

- **Genel toplam** — hasta, cycle, OPU, oosit, 2PN, blastokist, dondurulan,
  transfer edilen embriyo.
- **Oranlar** — MII (MII/oosit), fertilizasyon (2PN/ICSI), blastokist
  (blastokist/2PN), klinik gebelik (gebelik/transfer edilen cycle). Her
  oranın yanında payı ve paydası yazıyor; **paydası sıfır olan oran
  basılmıyor** — "%0" yanıltıcı olurdu, ölçülmemiş demek.
- **Aylara göre** — son 12 ayın kırılımı; işlem yapılmamış ay hiç satır
  açmıyor.
- **Son kayıtlar** — en son girilen on kayıt (hasta, cycle, laboratuvar
  işlemi), satır ilgili cycle'a gidiyor. Kullanıcının "her kayıt anlık"
  isteğinin ikinci yarısı: sayının yanında **ne olduğu** da görünsün.
  On satır, çünkü bu bir kayıt defteri değil "en son ne yapıldı" penceresi;
  uzun tutulunca ekranın yarısını kaplayıp yanındaki ay kırılımını eziyordu
  (ilk denemede 25'ti, ekran görüntüsünde görüldü). Tam döküm `/disari/tumu`.

Excel hali `/disari/istatistik`: ay ay kırılım + genel toplam, iki sayfa.

## İzin

**Yalnızca yönetici** — ekran hem laboratuvarın bütün üretimini hem son
girilen hasta adlarını tek sayfada gösteriyor. Hem `/istatistik` hem
`/disari/istatistik` `yonetici_kontrol(request)` ile başlıyor; düğmeyi
gizlemek yetmez. Yönetici olmayan kullanıcıyla denendi, ikisi de
`/hastalar`'a dönüyor.

## Transfer ve gebelik hangi cycle'a yazılıyor

Transfer edilen embriyo başka cycle'dan gelmiş olabilir (FET). Ölçü
**tedavinin yapıldığı cycle**: `COALESCE(o.tr_cycle_id, s.cycle_id)`. Aynı
kural ay listesinde de geçerli (v6.36). "Transfer edilen cycle" ile "transfer
edilen embriyo" ayrı sayılıyor — gebelik oranının paydası cycle, embriyo
değil.

## Test edildi

- 8 oositlik fikstürle sayılar elle doğrulandı: 8 oosit, 5 MII, 5 ICSI,
  4×2PN, 3 blastokist, 1 dondurma, 1 cycle'da 2 embriyo transferi →
  MII %62.5, fertilizasyon %80, blastokist %75
- Ekran ve Excel aynı sayıları veriyor
- Yönetici olmayan kullanıcı ikisinden de döndürülüyor
- 34 ekran 200, iki dilde, JS hatası yok, 390 ve 1280px'te yatay taşma yok
- Test verisi geri alındı (1 hasta, 2 cycle, 1 örnek, 0 olay)

---

# v6.39 — formlar kâğıt aslının kalıbıyla basılıyor

Kullanıcı v6.37'de çıkan formlara baktı: **"Formlar orijinal görüntüsünde
değil. Birebir aynı formları kullanmaz mısın?"** Haklıydı. v6.37'de formların
*içeriği* doğruydu ama *görünümü* benim kurduğum tablolardı — kutuların yeri,
puntolar, çerçeveler, bölüm başlıkları kâğıda benziyordu, kâğıt değildi.
Kalite sisteminden gelen bir forma "benzemek" yetmez; hastanın fiziksel
dosyasına giren kâğıt, boş formun aynısı olmalı.

## Kalıp artık kâğıdın kendisinden çıkıyor

Kullanıcının yüklediği iki `.xls` dosyası (`formlar_asil/`) **programatik
olarak** okundu ve ızgaraları `form_kalip.json`'a çıkarıldı:

- satır yükseklikleri ve sütun genişlikleri (Excel'in kendi ölçüleriyle)
- birleşik hücreler
- her hücrenin puntosu, kalınlığı, yatay/dikey hizası
- her hücrenin **dört kenarının** çizgi tipi (ince / kesik / kalın / kıl)
- kâğıtta basılı olan bütün yazılar

Elle kopyalanmadı; `formlar_asil/kalip_uret.py` çıkardı. Bu yüzden kâğıttaki
yazım hataları bile duruyor: **"TRANSFES EMBRİYOLOG"**, "Nukleus durmu",
"Labratuvar", "Oasit tipi". Bunlar düzeltilmedi — form kalite sisteminin
belgesi, düzeltmek onu başka bir belge yapardı.

`formlar.py` artık kalıbı **kurmuyor**, yalnızca dolduruyor: `*_verisi()`
cycle'ın verisini toplar, `*_dolgu()` onu hücre adreslerine dağıtır. Aynı
dolgu iki yere gidiyor — `form.html` (yazdırılabilir sayfa) ve `.xlsx` — o
yüzden ikisi birbirinden ayrı düşemiyor. İki ayrı şablon (`form_ozet.html`,
`form_artlab.html`) silindi; tek `form.html` her iki kalıbı da basıyor.

## Excel'de tarafsız stil

`excel.py`'nin stil tablosu sabitti (on üç hazır stil). Kalıp bunu
kaldırmıyordu: kâğıtta 45 ayrı punto/kenarlık birleşimi var. Artık
`styles.xml` **dosya başına** kuruluyor — taban stiller aynı sırada duruyor
(numaraları dosyaya yazılıyor, değiştirilemez), kalıbın stilleri sonuna
ekleniyor. Font Arial, kenarlıklar kâğıttaki çizgi tipiyle aynı.

## Excel'in "taşma"sı HTML'de yok

Excel'de bir hücrenin yazısı, yanındaki hücre boşsa ve aralarında dikey çizgi
yoksa oraya taşar — kâğıttaki `Dosya No : ..........` tek bir açık alan gibi
görünür, aslında altı ayrı hücredir. HTML tablosunda taşma yok, yazı kırpılır.
Kalıp çıkarılırken bu birleştirildi: aralarında çizgi olmayan boş hücreler
soldaki hücreye katılıyor. Görüntü aynı, kutular gerçekten geniş.

Aynı sebeple hücreler `white-space: pre` ile basılıyor: kâğıtta bazı yazılar
boşlukla hizalanmış (`"            grade"`, `"Raporu dolduran      ' Tarih"`),
HTML normalde o boşlukları tek boşluğa indirir ve hiza bozulurdu.

## A4'e sığdırma

Kâğıdın kendi puntoları ve satır yükseklikleri A4'e sığmıyor; Excel bunu
"sayfaya sığdır" ile çözüyor. Tarayıcıda aynısı tek katsayıyla yapılıyor:
bütün yükseklikler ve puntolar aynı oranda küçülüyor, oranlar bozulmadığı
için form aynı görünüyor. Özet formu %85, ART raporu %80 ile basılıyor ve
ikisi de tek A4'e oturuyor (dikey / yatay).

Telefonda form sıkıştırılmıyor — sıkıştırılınca yazılar kırpılıp okunmaz
oluyordu. `.kalip`'in en az genişliği var, kâğıt kartının içinde yana
kaydırılıyor. Yazdırırken bu sınır kalkıyor.

## Programdan forma ne geçiyor

**Embriyoloji Özet Formu (DH.FR.91).** Bütün kutular programdan doluyor;
programda karşılığı olmayanlar boş kalıyor: kimlik no, empty zona, morfolojik
anomalili, intakt, transfer klinisyen.

**ART Lab. Raporu (DH.FR.107).**

- Kimlik satırları kâğıttaki `:` işaretinin arkasına yazılıyor
- "İşlem" ve "Sperm" kutularında seçenekler basılı (`IVF , ICSI`); kâğıtta
  doğru olan daire içine alınıyor. Program daire çizemediği için seçenekleri
  olduğu gibi bırakıp cevabı **okla** arkasına yazıyor:
  `IVF , ICSI  →  IVF/ICSI`. Yoksa `IVF , ICSI IVF/ICSI` diye üç seçenek gibi
  okunuyordu.
- Oosit ızgarası: Over (R/L), Nukleus durumu, PN durumu, gün 2 hücre/grade,
  gün 3 hücre/grade, transfer işareti. Blastokist skoru "Yorum" satırına
  yazılıyor — kâğıtta blastokist satırı yok, form gün 3'te bitiyor.
- **"24 saat : hücre" satırı boş kalıyor** — programda 24. saat kaydı yok,
  uydurulmadı.
- "İŞLEM / Tarih / Sa." bloğu (OPU, Mikro, Freeze, Thaw, Transf) zaman
  çizelgesinden doluyor: tarih ve saat. Geçen saat hesabı v6.37'deki yerinde,
  cycle ekranının çizelge kartında.
- Medium/Lot satırları boş — programda tutulmuyor.

**Oosit sayısı 13'ü geçerse** kalıp ikinci kez basılıyor ve kalan oositler
oraya yazılıyor; kâğıtta ikinci form demek. Özet ve işlem saatleri yalnızca
ilk sayfada — aynı toplamı iki kez basmak hangisinin doğru olduğunu
sordururdu. Kırpmak klinik bir sayıyı gizlerdi, sütun eklemek kalıbı bozardı.

## Gün 2 / gün 3 hangi satıra yazılıyor

Kâğıttaki satır başlıkları "40-45 saat" ve "72 saat". Program gün 2 kaydını
birinciye, gün 3 kaydını ikinciye yazıyor.

Bu bir eşleme olduğu için kullanıcıya soruldu — v6.37'de saat başlıklarını
aşamalara eşleme önerisi **reddedilmişti** ("gerçek geçen saati hesapla").
Buradaki fark, satırın içeriğinin zaten o günün değerlendirmesi olması; gerçek
saatler de çizelgede duruyor, bakıp doğrulanabiliyor. Kullanıcı **"kalsın"
dedi** (2026-09-11), eşleme onaylandı. Kendiliğinden boşaltma.

"24 saat : hücre" satırı ayrı: programda 24. saat kaydı **yok**, o yüzden boş
kalıyor. Bir gün böyle bir kayıt eklenirse oraya yazılır.

## Amblem

Kullanıcı ilk baskılara bakınca eksiği gördü: **"Formlarda üniversitenin
amblemi var."** Vardı — ve iki `.xls`'in **içine gömülüydü**, sayfanın
hücrelerinde değil.

Amblem Excel'de Escher (`MSODRAWINGGROUP`) kaydında duruyor ve CONTINUE
kayıtlarına bölünmüş olabiliyor; dosyada PNG imzasını arayıp kesmek bozuk bir
dosya veriyor (ilk denemede tam bunu yaptım, resim açılmadı). Kayıtları
birleştirip çıkarınca temiz PNG geldi: 236×236, iki formda da aynı görsel,
`static/form_amblem.png`.

**Yeri de kâğıttan geliyor.** Excel'in "sabitleyici"si (client anchor) sekiz
sayı: şu sütunun %4.6'sından şu satırın %6.6'sına, şu sütunun %4.8'ine şu
satırın %53'üne. Amblemin yeri ve boyu bundan hesaplanıyor —
ekranda mutlak konumlu bir `<img>` (yüzde ve punto), Excel'de `twoCellAnchor`
çizim parçası (EMU). Sabit bir boy vermek yerine kâğıttaki kutuyu kurmak
önemli: iki hücre arasına oturduğu için "sayfaya sığdır" ile basılınca amblem
de tabloyla birlikte küçülüyor.

`excel.py` artık `.xlsx` içine resim gömebiliyor — yine kütüphanesiz:
`xl/media/`, `xl/drawings/drawing1.xml`, çizimin ve sayfanın ilişki dosyaları,
`[Content_Types].xml`'e PNG türü. Aynı amblem iki sayfada kullanılsa da
dosyaya bir kez yazılıyor.

## Test edildi

- İki form da tek A4'e oturuyor (dikey 780pt / yatay 535pt), Chromium'un
  yazdırma önizlemesiyle ölçüldü
- Amblem iki formda da kâğıttaki yerinde; `.xlsx` openpyxl+Pillow ile okundu,
  236×236 PNG doğru hücrelere sabitlenmiş
- `.xlsx` openpyxl ile okundu: Arial, kesik çizgili kutular, kalın bölüm
  çizgisi, kâğıttaki sütun genişlikleri ve satır yükseklikleri, A4
  dikey/yatay, sayfaya sığdır
- 20 oositlik veriyle iki sayfa üretiliyor, ikinci sayfada oositler 14-20 ve
  özet bloğu boş
- 39 adres 200, iki dilde, JS hatası yok, 390 ve 1280px'te yatay taşma yok
- Form iki dilde de **Türkçe** basılıyor: kurum belgesi, arayüz metni değil

---

# v6.40 — başka bir laboratuvar kendi formunu yükleyebiliyor

Kullanıcının isteği: *"Bu formlar benim kullandığım. Başka bir lab farklı bir
form kullanmak isterse diye laboratuvar formlarını yönetici alanında yükleme
yapsak."*

Gömülü iki form (DH.FR.91, DH.FR.107) **bu** laboratuvarın kalite sisteminden.
Başka bir laboratuvarın formu bambaşka. Artık yönetici kendi formunu yükleyip
programdaki verilerle doldurup basabiliyor.

## Neden `.xlsx`, `.xls` değil

Kullanıcının kendi formları `.xls`'ti ve onları okumak için `xlrd` gerekmişti —
ama o **geliştirme aracı**, programın bağımlılığı değil (`formlar_asil/`).
Çalışma anında, klinikteki mini PC'de okumak başka bir şey: `.xls` ikili bir
belge biçimi, elle ayrıştırmak yüzlerce satır risk demek.

`.xlsx` ise içinde XML olan bir ZIP — Python'un kendi `zipfile` ve `xml.etree`
modülleri yetiyor. Zaten `.xlsx` **yazıyorduk**; okumak bunun simetriği.
Laboratuvara düşen tek iş: formu Excel'de bir kez "Farklı Kaydet → Excel
Çalışma Kitabı (.xlsx)" ile kaydetmek. Program yanlış biçimi kabul etmiyor ve
hata mesajı tam bunu söylüyor.

`xlsx_oku.py` şunları çıkarıyor: satır yükseklikleri, sütun genişlikleri,
birleşik hücreler, her hücrenin punto/kalınlık/hiza/kenarlık bilgisi, basılı
yazılar, sayfa yönü ve **sayfadaki görseller** (logo — `twoCellAnchor` ve
`oneCellAnchor` ikisi de). Çıktı `form_kalip.json`'daki ile aynı biçimde, yani
yüklenen form da gömülü form da tek yoldan basılıyor.

**Doğrulama:** gömülü kalıp → `.xlsx` → geri oku → kalıp turunda hücre sayısı,
birleşmeler ve logonun sabitleyicisi **birebir** aynı çıkıyor.

### Çevirme yönergesi ekranın kendisinde

Hata mesajı "Excel'de Farklı Kaydet ile .xlsx yapın" diyordu ama **nasıl**
yapılacağını söylemiyordu. Bilgisayarla arası iyi olmayan biri için bu cümle
bir çözüm değil, ikinci bir soru. Yükleme kutusunun hemen altına açılır bir
yardım kondu: beş adım, sonra Mac'te o kutunun adının farklı olduğu notu, en
sonda "formun görünümü değişmez, eski dosyanız yerinde durur" güvencesi.
Kullanıcının isteği — ek bir işlem gerekmeden yükleyebilsin.

Kapalı duruyor (`<details>`): `.xlsx` dosyası olan kullanıcı beş adımı
okumak zorunda kalmıyor. Metinler `metinler.py`'de (`form_xls_*`), iki dilde;
şablona doğrudan yazılmadı.

Programa `.xls` okuma yeteneği eklemek yerine yönerge yazmanın sebebi yukarıda:
`xlrd`'yi çalışma anına sokmak klinikteki mini PC'ye kalıcı bir kurulum adımı
eklemek demekti. Bir kerelik "Farklı Kaydet" tıklaması bundan ucuz.

## Hangi kutuya ne yazılacağı: etiket

Kalıp yüklenince program formun *düzenini* öğreniyor ama *anlamını*
öğrenmiyor — hangi kutuya "MII sayısı" gireceğini bilemez. İki yol vardı:
ekranda ızgarayı gösterip kutuya tıklatarak eşlemek, ya da laboratuvarın kendi
Excel'inde kutunun içine bir etiket yazması. Kullanıcı **"önce Excel etiketi,
sonra ekran"** dedi; bu sürüm birincisi.

Kutunun içine `{{dosya_no}}` yazılıyor, program onu değerle değiştiriyor.
Kutuda başka yazı da olabilir: `Dosya No: {{dosya_no}}`. 60 etiket var; listesi
`/formlar/etiketler` ekranında, Türkçe açıklamalarıyla.

- Etiketler `formlar.ALAN_ACIKLAMA`'da **tek yerde** duruyor; hem doldurma hem
  ekran oradan okuyor. İki liste olsaydı ekrandaki ile gerçekte çalışan
  etiketler er geç ayrı düşerdi.
- Değerlerin çoğu `ozet_verisi()`'nden geliyor — resmî özet formunun kutuları
  zaten bir laboratuvarın bir cycle için isteyeceği şeylerin listesi.
- **Tanınmayan etiket olduğu gibi basılıyor.** `{{dosyano}}` diye yazılmış bir
  etiket boş kutu olarak geçseydi yazım hatası fark edilmezdi; formda göze
  çarpsın diye duruyor. Yükleme ekranı da o formun yanında uyarı gösteriyor.
  (`metin()`'in bilinmeyen anahtarı olduğu gibi döndürmesiyle aynı gerekçe.)
- Bu sürümde **oosit ızgarası yok** (kullanıcının kararı): bir kutu = bir
  değer. Izgaralı bir form yüklenebiliyor, ızgarası elle dolduruluyor.

## Kalıp neden veritabanında

`lab.db` `tasi.py` ile USB'de taşınan **tek** dosya. Kalıp diskte ayrı bir
klasörde dursaydı taşınırken unutulur, program karşı makinede "form yok"
derdi. Formun içindeki logo da aynı sebeple kalıbın içinde, base64 olarak.

`/disari/tumu` dökümüne **girmiyor**: `TUM_TABLOLAR` beyaz liste ve `lab_formu`
orada yok. Kalıp klinik bir kayıt değil, laboratuvarın kâğıdı; üstelik tek
hücreye sığmaz (Excel'in hücre sınırı 32767 karakter, kalıp yüz kilobaytlarca).

## İzinler

Yükleme, gizleme ve silme **yalnızca yönetici** — üçü de
`yonetici_kontrol(request)` ile başlıyor, ekrandaki düğmeyi gizlemek yetmez.
Yüklenen formu **basmak** serbest: gömülü formlarla aynı, personelin günlük
işi. Doğrulandı: embriyolog hesabı `/formlar`, `/formlar/yukle` ve silmeden
döndürülüyor, ama `/form/lab/1/1`'i açabiliyor.

Silme kalıcı (tarayıcı onayıyla). Hasta kaydı gibi değil: kalıp laboratuvarın
kâğıdı, yeniden yüklemek bir dosya seçmek kadar — ve her kalıp yüz
kilobaytlarca JSON, USB ile taşınan dosyayı şişirmesin.

## Dışarıdan gelen dosya

Yönetici yüklüyor ama dosya yine de dışarıdan geliyor:

- dosya boyu 5 MB, ZIP'teki parça sayısı 200, açılmış boyut 20 MB,
  500 satır × 200 sütun, görsel 2 MB ile sınırlı
- XML'de `<!DOCTYPE` ya da `<!ENTITY` varsa dosya **hiç açılmıyor** —
  "milyar kahkaha" saldırısı belleği tüketebilir
- ZIP'ten yalnızca bilinen parça adları okunuyor, hiçbir şey diske yazılmıyor
  (logo doğrudan veritabanına gidiyor), yani dizin dışına çıkan bir ad işe
  yaramaz
- tanınmayan bir görsel türü dosyaya konmuyor (PNG / JPEG / GIF)

Bozuk ZIP, `.xls`, boş dosya ve varlık tanımlı XML ile denendi; dördü de
anlaşılır bir hata mesajıyla dönüyor, sunucu ayakta kalıyor.

## Ortak ızgara kuralı

Kalıbı iki yer üretiyor: `kalip_uret.py` (kâğıt aslından, tek seferlik) ve
`xlsx_oku.py` (yüklenen dosyadan, çalışma anında). Izgarayı kuran kural —
hangi boş hücrenin soldakine katılacağı dahil — `form_kalip.izgara_kur()`'da
**tek kopya**. İki kopya olsaydı yüklenen form ile gömülü form farklı basılırdı.
Taşındıktan sonra gömülü kalıp yeniden üretildi: çıktı bayt bayt aynı.

## Test edildi

- openpyxl ile üretilmiş (bizim yazıcımız değil) gerçekçi bir laboratuvar
  formu yüklendi: 18 etiket, logo, birleşik hücreler, kenarlıklar, sütun
  genişlikleri — ekranda ve `.xlsx`'te doğru çıktı
- Bilerek yazılmış `{{dosyano}}` hatası hem formda göründü hem listede uyardı
- Yönetici olmayan kullanıcı yükleme/silmeden döndürülüyor, basmaya giriyor
- 45 adres 200, iki dilde, JS hatası yok, 390 ve 1280px'te yatay taşma yok
- Test formu ve oturumları geri alındı (lab_formu 0, 1 hasta / 2 cycle)

---

# v6.41 — gömülü formlar gizlenebiliyor, klasörler ekrandan ayarlanıyor

## Sorun: başka bir laboratuvar benim formumdan kurtulamıyordu

v6.40 başka bir laboratuvarın kendi formunu yüklemesini sağladı ama gömülü iki
formu **kaldıramıyordu**: cycle ekranı o iki düğmeyi her zaman basıyordu.
Kullanıcı sordu — "başka bir laba verdiğimde default benim formlarım mı
çıkacak" — cevap evet ve bu bir kusur.

Kusurun ağırlığı şurada: DH.FR.91 ve DH.FR.107 bu kullanıcının kurumunun
**kalite sistemi belgeleri**; üzerinde o kurumun doküman kodu, revizyon tarihi
ve üniversitenin ambleminin var. Başka bir hastanenin embriyoloğu yanlışlıkla o
düğmeye bastığında ortaya çıkan şey "yanlış form" değil, **ait olmadığı kurumun
belgesinde gerçek hasta verisi**.

## Çözüm: gizleme, silme değil

`/formlar` ekranına "Programla gelen formlar" kartı eklendi; iki formun
yanında Gizle/Göster düğmesi var. Gizlenen form cycle ekranında görünmüyor.

Silme değil gizleme, çünkü kalıp **programın dosyasında** (`form_kalip.json`),
veritabanında değil — silinecek bir kayıt yok. Ayar `ayarlar` tablosunda
(`form_gizli_ozet`, `form_gizli_artlab`), varsayılanı görünür: bu
laboratuvarda hiçbir şey değişmiyor.

Adres parçası `FORMLAR` beyaz listesinden geçiyor. Geçmeseydi ayar anahtarı
adresten gelen metinle kurulurdu ve `ayarlar` tablosuna istenen satır
yazılabilirdi.

**Gizli form adresten hâlâ basılabiliyor** (`/form/ozet/5`). Bilerek: yüklenen
formlarda da öyle ve gizleme bir yetki sınırı değil, ekran düzeni. Kimse o
adresi elle yazmıyor; yetki sınırı `yonetici_kontrol()`'de.

## Ticari dağıtım: gömülü form hiç olmayacak

Kullanıcının kararı (2026-09-12): programı ticari olarak verirse **hiçbir form
gömülü gelmeyecek**, kendi formları da depodan çıkacak, her laboratuvar
kendininkini yükleyecek.

O gün kod değiştirmek gerekmesin diye bugün hazırlandı:

- `form_kalip.py` dosyayı bulamazsa `KALIPLAR = {}` ile devam ediyor, hata
  vermiyor.
- `FORMLAR` yalnızca **kalıbı olan** formlardan kuruluyor.
- `gomulu_formlar()` boş dönünce cycle ekranında düğme, `/formlar`'da kart
  basılmıyor.

Yani ticari sürüm iki dosyayı silmekten ibaret: `form_kalip.json` ve
`static/form_amblem.png` (istenirse `formlar_asil/` de). **Denendi:** ikisi
yokken ana ekran, cycle, `/formlar` ve `/yonetim` 200 veriyor, form düğmesi
çıkmıyor, `/form/ozet/2` cycle'a dönüyor.

## Kamera klasörü artık ekrandan seçiliyor

Görüntü eşlemesi kuracak laboratuvarın kamera klasörünü göstermesi gerekiyor.
Tek yol terminaldi: `python yerel_kur.py`. Kullanıcının isteği — yönetici
alanından seçilsin.

Yeni ekran: **`/klasorler`**, yalnızca yönetici. Üç yol da orada.

**`/yonetim` salt okunur kaldı.** Panel yolları göstermeye devam ediyor,
değiştirme kendi ekranında; panelden yalnızca bağlantı veriliyor — dil
seçiminde alınan kararın aynısı.

**Ayar veritabanında değil**, `yerel_ayar.json`'da ve makine adına göre
bölümlü. `lab.db` USB ile taşınıyor; yollar orada olsaydı Mac'te girilen
klasör klinik bilgisayarında da geçerli olurdu. Test edildi: kaydetme dosyadaki
öteki makinenin bölümüne dokunmuyor.

### Üç klasör, üç farklı davranış

Aynı ekranda ama kuralları farklı, çünkü programın onlarla ilişkisi farklı:

| Klasör | Program ne yapıyor | Yoksa |
|---|---|---|
| Kamera | yalnızca **okur** | **kabul edilmez** |
| Arşiv | **yazar** | oluşturulur |
| Yedek | yazar (ara sıra) | olduğu gibi kaydedilir |

- **Kamera klasörü var olmalı.** Kareleri oraya mikroskop yazıyor; olmayan bir
  yolu açmak işe yaramaz, kamera oraya yazmıyor olurdu. Yazım hatası kabul
  edilseydi kamera kuyruğu aylarca boş görünürdü ve sebebi anlaşılmazdı.
- **Arşiv yoksa oluşturulur** — oraya yazan biziz.
- **Yedek oluşturulmaz.** Çoğu zaman takılı olmayan bir disk (klinikte `E:`).
  Mac'te `E:\yedek` adında klasör açmak v6.8'de gerçekten başa geldi; hedefi
  `yedek.py` çalışma anında doğruluyor.

Ekranın altında bir uyarı var: **arşiv klasörünü taşımadan değiştirme.**
Veritabanı görüntü yollarını bu klasöre göre saklıyor; yol değişirse eski
fotoğraflar yeni klasörde aranır.

### Dosyaya yazan tek yer: `db.yerel_yaz()`

`yerel_ayar.json`'a iki yerden yazılıyordu — `yerel_kur.py` kendi
`json.dumps`'ını çağırıyordu. Yeni ekranla üçüncü bir yazıcı olacaktı.
`db.py`'ye `yerel_yaz()` kondu, `yerel_kur.py` de ona çevrildi. Ayarı iki
yerden okumak v6.8'de başa gelmişti (tuzak #8); yazmak daha kötüsü olurdu.

## Test edildi

- Gizle → cycle ekranında düğme kayboldu, Göster → geri geldi; ayar tabloda
- Uydurma form adıyla (`/formlar/gomulu/dil/gizle`) istek: hiçbir şey yazılmadı
- Embriyolog hesabı: `/klasorler` ve `/formlar` GET'i, ikisinin POST'u ve
  gizleme reddedildi (303) — ama form **basabiliyor** (200)
- Olmayan kamera klasörü reddedildi, var olan kabul edildi, arşiv oluşturuldu,
  `E:\yedek` olduğu gibi kaydedildi
- Dosyada ikinci bir makine bölümü varken kaydetme ona dokunmadı
- `form_kalip.json` yokken bütün ekranlar açıldı, form düğmesi çıkmadı
- Test verisi geri alındı (oturum 22, 1 hasta / 2 cycle, 0 kırık referans)

---

# v6.42 — geniş ekranda iki sütun

## Sorun

Kullanıcı bilgisayarda baktı: içerik ekranın ortasında dar bir şeritte
toplanıyor, iki yanda büyük boşluk kalıyor. Ölçüldü — 1440 px'lik bir ekranda
içerik sütunu **640 px**, iki yanda ~400'er piksel boş; `/yonetim` ekranı da
1954 px'e uzuyor, yani ekranın iki katı.

Sebep tasarımın kendisi: program telefon önceliğiyle yazıldı, `.kap` 640 px'te
sabit. v6.34'te yalnızca ana ekran (`kap genis`, 940 px) ve sonra istatistikler
genişletilmişti.

## Neden sadece genişletmek yetmiyor

İlk akla gelen çözüm sütunu 940'a çıkarmak. Ama cycle ekranındaki "Protokol"
kartında etiket solda, değer sağda duruyor: kartı genişletince "Gonadotropin"
ile "girilmedi" arası daha da açılıyor, okumak zorlaşıyor. Geniş ekranın
cevabı **daha geniş kart değil, daha çok sütun**.

Kullanıcıya soruldu, **"kartlar yan yana iki sütun"** dedi; kapsam olarak da
**"önce yönetim + cycle"**.

## Nasıl

`.sutunlar` > iki `.sutun`. Ana ekranın `.ikisutun`'u ile aynı fikir, farkı
sütunun içine **birden çok kart** koyabilmesi.

**Medya sorgusu yok, sarma var.** `flex: 1 1 380px` + `flex-wrap`: sütun
380 px'in altına düşecekse kendiliğinden alt alta diziliyor. Böylece tek kural
her genişlikte doğru — telefonda, tablette ve sütunu dar kalan sayfada tek
sütun; yeri olan ekranda iki. Sabit bir kırılma noktası yazsaydık, sütunu
940 yerine 780 px olan bir sayfada iki sütun 380'in altına inerdi.

**Sütunlar şablonda ayrılıyor, `column-count` ile değil.** CSS'in çok sütunu
kartları *yüksekliğe* göre bölüyor; hangi kartın nereye düşeceği veriye göre
değişiyor ve "İşlemi bitir" düğmesi verinin üstünde başlayabiliyor. Hangi
kartın nerede duracağı anlamla ilgili bir karar, ölçüyle ilgili değil.

**Bölme noktası kaynak sırasında.** Şablonda sıra değişmiyor, araya
`</div><div class="sutun">` giriyor. Böylece sütunlar alt alta dizildiğinde
(telefon) sıra **bire bir eskisi gibi** kalıyor. Ölçüldü: cycle ekranı
telefonda değişiklikten önce de sonra da 1846 px.

Bölme:

| Ekran | Sol sütun | Sağ sütun |
|---|---|---|
| `/cycle/{id}` | sayı özeti, Zamanlar, Protokol, protokol notu | Oositler, arşiv, işlem düğmeleri, zaman çizelgesi |
| `/yonetim` | gidilecek ekranlar, Excel çıktısı, Yedekleme | Veritabanı, klasörler, salt okunur notu |

Yedekleme kartı sağdan sola alındı — sol sütun 720 px'te bitip altında boşluk
bırakıyordu; şimdi 800'e 992.

## Genişlik formülü tek yerde

Cycle ekranının sütunu genişleyince **kimlik bandının** hizası da değişmeli:
bant `.kap`'ın dışında, tam genişlikte duruyor ve yazısını içerik sütunuyla
hizalıyor. İki yerde ayrı formül olsaydı band ile kartlar birbirinden kayardı.

Formül `:root`'ta bir değişken: `--genis-sutun`. Hem `.kap.genis` hem bandın
dolgusu onu kullanıyor. Bandın hangi ölçüyü kullanacağını **gövdedeki sınıf**
söylüyor (`body.genissayfa`) — bant `.kap`'ın kardeşi olduğu için `:has()`
gerekirdi, o da eski Safari'de yok.

Bu arada bandın yazısı kartların **16 px soluna** düşüyormuş (eskiden beri):
dolgu hesabı `.kap`'ın kendi 16 px'lik iç boşluğunu saymıyordu. `+ 16px`
eklendi, artık hasta adı kartın sol kenarıyla tam hizalı.

## `yanmenusuz`

`.kap.genis` 1100 px'ten sonra `100vw - 500px` ile sınırlı — solda duran yan
menüyle çarpışmasın diye. `/yonetim`'de yan menü yok, o pay boşuna: 1280 px'lik
bir ekranda sütun 780'de kalıyor ve iki sütun sığmıyordu.
`.kap.genis.yanmenusuz` payı kaldırıyor.

Sınıf bilerek **opt-in**: unutulursa sayfa dar kalır, menünün altına girmez.
Yanlış tarafa düşmesi ucuz olan seçenek bu.

## Ölçüldü

| Ekran | Önce | Sonra (1440 px) |
|---|---|---|
| `/yonetim` | 1954 px | 1404 px |
| `/cycle/{id}` | 1626 px | 964 px |

Cycle ekranı artık tek ekrana sığıyor.

- 390 / 768 / 1024 / 1100 / 1280 / 1366 / 1440 / 1920 px'te bakıldı; hiçbirinde
  yatay taşma yok, yan menü hiçbir genişlikte içeriğin üstüne binmiyor
- Telefonda sıra ve sayfa yüksekliği değişmedi (1846 px → 1846 px)
- Kimlik bandı cycle ve aşama ekranlarında sekiz genişlikte de kartlarla
  tam hizalı (fark 0 px)
- Ana ekran, istatistikler ve hasta kayıtları etkilenmedi — ölçüleri aynı
- 30 adres 200, sunucu günlüğünde hata yok

---

# v6.43 — klasör seçmek için gözat

## Sorun

v6.41'de klasör yolları ekrandan ayarlanabilir oldu ama **elle yazılıyordu**.
Kullanıcı haklı olarak takıldı: `C:\Users\lab\Documents\Octax\Snapshot` gibi
bir yolu yazmak zor ve bir harf yanlışsa kamera kuyruğu sessizce boş kalıyor —
kimse sebebini bulamıyor.

## Neden işletim sisteminin kendi penceresi açılmıyor

İlk akla gelen "Klasör Seç" düğmesi. Olmuyor: tarayıcı, güvenlik gereği
sayfaya **gerçek dosya yolunu vermiyor**. `<input type="file" webkitdirectory>`
ile seçilen klasörün dosya adları geliyor ama tam yolu gelmiyor (`C:\fakepath`).
Yani seçilen klasörün nerede olduğunu sunucuya söylemenin yolu yok.

## Çözüm: sunucu tarafında gezinmek

Program **kendi çalıştığı makinenin** klasörlerini listeliyor, kullanıcı
tıklayarak iniyor. Aranan klasör zaten o makinede — mikroskop oraya yazıyor,
telefona değil. Bu yüzden personel telefondan baksa bile doğru klasörleri
görüyor.

`GET /klasorler/gozat?yol=...` → `{yol, ust, kok, klasorler, fotograf}`.
Ekranda her alanın altında bir **Gözat** düğmesi, açılınca o klasörün alt
klasörleri, "En üst" ve "Üst klasör" satırları, altta "Bu klasörü seç".

**Fotoğraf sayısı da dönüyor.** Kamera klasörünü bulmanın en kolay yolu bu:
"Bu klasörde 37 fotoğraf var" yazıyorsa doğru yerdesin. Sayım
`goruntuler.UZANTILAR` ile yapılıyor — ayrı bir uzantı listesi yazsaydık
gezginin saydığı dosyalarla kuyruğun aldığı dosyalar ayrı düşerdi ve "37
fotoğraf var" denen klasörde kuyrukta 34 kare çıkardı.

## Sınırlar

- **Yalnızca yönetici** (`yonetici_kontrol`). Yönetici olmayan hesapla
  denendi: 303.
- **Yalnızca klasör adları döner** — dosya adları değil, dosya içeriği hiç
  değil. Tek sayı geri gidiyor (fotoğraf sayısı).
- Yetki artışı değil: yönetici zaten istediği yolu **elle yazabiliyordu** ve
  `/disari/tumu` ile bütün veritabanını dışarı alabiliyor. Gezgin yeni bir
  kapı açmıyor, var olan alanı görünür kılıyor.
- `EN_COK_KLASOR = 300` ve `EN_COK_SAYIM = 2000`: devasa bir klasörde sayfa
  kilitlenmesin. Liste kendi içinde kayıyor (260 px), sayfayı uzatmıyor.
- Okuma izni olmayan klasör (`/proc/1/root` gibi) sessizce ev klasörüne
  düşüyor — hata sayfası yok, sızıntı yok.
- Gizli klasörler (`.` ile başlayanlar) listelenmiyor; Mac'te ev klasörünü
  okunmaz hale getiriyorlardı.
- Windows'ta "En üst" sürücü harflerini veriyor (`C:\`, `D:\`, `E:\`),
  ötekinde `/`.

## Test edildi

- Gözat → alt klasöre in → "Bu klasörü seç": yol alana yazıldı, gezgin kapandı
- Fotoğraf sayısı doğru (7 dosyalı deneme klasöründe 7; `snapshot/`'ta 3 —
  `.dng` sayılmıyor, program da onu kabul etmiyor)
- 50 alt klasörlü bir yerde liste kendi içinde kaydı, sayfa uzamadı
- Olmayan yol ve izinsiz klasör ev klasörüne düştü, hata vermedi
- Yönetici olmayan hesap gezgine giremedi (303)
- 390 px'te yatay taşma yok, JS hatası yok (tek 404 `favicon.ico`)
- İki dilde metinler yerinde

---

# v6.44 — Gözat işletim sisteminin kendi penceresini açıyor

## İstek

Kullanıcı v6.43'teki listeyi beğenmedi: "fotoğraf kaydederken kullandığımız
tarzda... gözata basınca işletim sisteminin kendi ekranında bulalım."

## Neden tek başına olmuyor

Tarayıcı o pencereyi **açabiliyor** (`<input type="file" webkitdirectory>`)
ama seçilen klasörün **nerede olduğunu sayfaya söylemiyor** — `C:\fakepath`
diye sahte bir yol veriyor. Chrome'un yeni `showDirectoryPicker()` API'si de
yalnızca klasörün *adını* veriyor, yolunu değil. Bu bir ayar değil, bütün
tarayıcıların güvenlik kuralı: bir web sayfası ziyaretçinin disk düzenini
öğrenemez.

## Çözüm: pencere + arama

İki adım:

1. **Gözat** işletim sisteminin kendi klasör penceresini açıyor. Kullanıcı
   tanıdığı ekranda geziyor, klasörü seçiyor.
2. Tarayıcı bize klasörün **adını** ve içindeki **dosya adlarını** veriyor
   (`webkitRelativePath`: `Snapshot/2026-09-09/x.jpg`). Program o klasörü
   kendi makinesinde **arıyor** ve yolu alana yazıyor.

**Ad tutması yetmiyor**, içindeki dosyalardan en az biri de yerinde olmalı.
Yoksa aynı adlı başka bir klasör seçilirdi — laboratuvarda "Snapshot" adında
birkaç klasör olması çok olası.

Sonuç üç türlü:
- **Tek aday** → yol kendiliğinden yazılıyor.
- **Birden çok aday** → hepsi listeleniyor, kullanıcı doğru olanı seçiyor.
- **Bulunamadı** → sebebi yazılıyor ve **listeli gezgin açılıyor**; o her
  yerde çalışıyor.

## İki düğme, kullanıcının kararı

**Gözat** (işletim sisteminin penceresi) ve **Listeden seç** (v6.43'ün
gezgini) yan yana. Kullanıcı "ikisi de olsun" dedi ve doğrusu bu: birincisi
tanıdık ama her durumda sonuç vermiyor, ikincisi her yerde çalışıyor.

**iOS Safari'de Gözat basılmıyor.** Orada `webkitdirectory` yok sayılıyor ve
pencere klasör değil tek dosya seçiyor; çalışmayan bir düğme, olmayan bir
düğmeden kötü. Destek `'webkitdirectory' in document.createElement('input')`
ile bakılıyor, desteklenmiyorsa düğme gizleniyor ve yalnızca liste kalıyor.

## Arama sınırları

- Gezilen yerler: önce ev klasörü, sonra program klasörü, Windows'ta sürücü
  harfleri, ayrıca `/Volumes`, `/media`, `/mnt`. **POSIX'te `/` kökünden
  aranmıyor** — süre bütçesi sistem klasörlerinde biter, kullanıcının
  klasörüne hiç ulaşılmazdı.
- `Windows`, `Program Files`, `ProgramData`, `$Recycle.Bin`, `node_modules`,
  `__pycache__`, `proc`, `sys`, `dev` ve nokta ile başlayanlar atlanıyor. Bu
  dallar `os.walk`'ın listesinden **çıkarılıyor**, yani oraya hiç girilmiyor —
  asıl hızlanma orada.
- 4 saniye ve 40000 klasör tavanı, en çok 8 aday. Süre dolarsa liste açılıyor.
- Klasör adı tek parça olmalı: içinde `/` ya da `\` varsa istek reddediliyor.
  Örnek dosya yollarında `..` kabul edilmiyor.
- **Yalnızca yönetici.**

## Adlandırma

Kullanıcı "Klasörler yerine Dosyalar olsun mu" diye sordu; etiketlerin tam
karşılığı sorulunca **"klasör kalsın"** dedi. Programda "dosya" zaten iki şey
demek — hastanın kaydı (dosya no) ve yüklenen `.xlsx` — üçüncü bir anlam
karışıklık yaratırdı.

## Test edildi

- Gerçek klasör seçildi → tek aday bulundu, yol alana yazıldı
- Aynı adlı iki klasör kuruldu → ikisi de listelendi, seçilen alana yazıldı
- Aranmayan bir yerdeki klasör seçildi → açıklama çıktı ve liste açıldı
- Boş dosya listesi, yol ayıracı içeren ad ve bozuk JSON: üçü de reddedildi
- Yönetici olmayan hesap `/klasorler/bul`'a giremedi (303)
- 390 ve 1440 px'te yatay taşma yok, JS hatası yok, liste hâlâ çalışıyor
- 11 adres 200, iki dilde metinler yerinde

---

# v6.45 — telefonun ana ekranına, karekodla

## İstek

Kullanıcı programı önce kendi laboratuvarında deneyecek, sonra ticari yolları
arayacak. Bu aşamada istediği iki şey: personel adresi elle yazmasın
(**karekod**), ve program telefonda uygulama gibi dursun (**ana ekran
simgesi**) — hem iOS'ta hem Android'de.

Mağazaya gerek yok: mağazadan inen bir uygulama da yine klinikteki sunucuya
bağlanacaktı. Ana ekran simgesi aynı görüntüyü ücretsiz, onay süreci olmadan
veriyor.

## Karekod kütüphanesiz

`karekod.py` karekodu kendi çiziyor. Gerekçe `excel.py` ile aynı: klinikteki
mini PC'ye kurulum adımı eklememek. Çıktı **SVG** — resim kütüphanesi
gerekmiyor, her boyutta keskin, yazdırınca da düzgün basılıyor.

Kapsam bilerek dar: bayt kipi, M düzeltme düzeyi, sürüm 1–10 (213 karaktere
kadar). Bizim yazdığımız şey `http://klinik-pc:8000` gibi kısa bir adres.

**Doğrulama iki aşamalı:**

1. Olgun bir kütüphaneyle (`qrcode`, yalnızca geliştirme sırasında kuruldu)
   ürettiğimiz **ızgaralar karşılaştırıldı**: 18 elle seçilmiş örnek + 600
   rastgele metin, hepsi **birebir aynı**. Türkçe karakter (çok baytlı UTF-8)
   dahil.
2. Gerçek bir okuyucuya (`opencv`) **okutuldu**: yedi örneğin yedisi de doğru
   çözüldü.

Yol boyunca üç hata bulundu ve düzeltildi: biçim bilgisinin iki kopyası yer
değiştirmişti, 4. ceza kuralının formülü yanlıştı, ve maske seçimi biçim
bitleri yazıldıktan **sonra** puanlanıyordu. Üçüncüsü yaygın uygulamaların
tersiydi; düzeltilince 618 denemenin 618'i tuttu.

## Ana ekran simgesi

- `/manifest.json` bir **rota**, statik dosya değil: program adı ve dil
  laboratuvarın diline göre değişiyor.
- Manifest `ACIK_YOLLAR`'da. Tarayıcı onu **oturum çerezi göndermeden**
  istiyor; korumalı olsaydı giriş ekranına yönlenir, simge adsız ve ikonsuz
  eklenirdi. İçinde hasta verisi yok.
- iOS yeni sürümlerde manifest'in `display` alanını okuyor, eskilerde
  `apple-mobile-web-app-capable` metasına bakıyor — **ikisi de** var.
- Durum çubuğu `black-translucent`: sayfanın üstüne biniyor, o yüzden üst
  çubuk `env(safe-area-inset-top)` kadar aşağıdan başlıyor. Tarayıcıda bu
  değer 0, hiçbir şey değişmiyor.
- Simgeler `simge_uret.py` ile üretildi (geliştirme aracı, Pillow istiyor —
  `kalip_uret.py` gibi). Çizim: koyu zeminde bir oosit; dışta zona halkası,
  içinde dört blastomer. 48 pikselde bile okunuyor.
- Aynı dosya hem normal hem **maskable**: Android kenarlardan kırpıyor,
  içeriğin merkezin %40'lık dairesinde kalması gerekiyor; çizim %25'te
  bitiyor.

## `/baglan` ekranı

Karekod, adresin yazılı hali, bilgisayarın adı ve iki telefon için adım adım
yönerge. **Yazdırılabilir** — laboratuvara asılınca yeni gelen personel
okutup kendi telefonuna ekliyor.

Adres seçimi: yönetici zaten ağ üzerinden bağlandıysa **onun kullandığı
adres** yazılıyor (çalıştığı kanıtlanmış). Sunucunun kendi tarayıcısından
bakılıyorsa (`localhost`) yerel ağ adresi bulunuyor — UDP soketiyle, **paket
göndermeden**: `connect` yalnızca çekirdeğe "bu hedefe hangi arayüzden
çıkardım" diye soruyor. `gethostbyname` çoğu makinede `127.0.0.1` döndürüyor,
işe yaramıyor.

**Yalnızca yönetici**, öteki `/yonetim` ekranlarıyla aynı.

## Bilinen sınır: Android'de tam ekran HTTPS istiyor

iOS'ta ana ekrana eklenen program **tam ekran** açılıyor, adres çubuğu yok.
Android'de tam ekran (`display: standalone`) yalnızca güvenli bağlantıda
geçerli; programda HTTPS yok (bekleyen iş 3), o yüzden simge Chrome içinde
açılabiliyor. Simge, ad ve tek dokunuşla erişim yine çalışıyor.

HTTPS kararı paketleme aşamasına bırakıldı — yerel ağda sertifika ayrı bir
tasarım işi.

## Test edildi

- 618 karekod referans uygulamayla birebir aynı; 7 örnek gerçek okuyucuyla
  çözüldü
- `/manifest.json` oturumsuz 200 veriyor, üç simge de 200
- `/baglan` 390 ve 1440 px'te taşmıyor; geniş ekranda iOS/Android adımları
  yan yana, telefonda alt alta
- Yazdırma denendi (A4 PDF üretildi)
- Yönetici olmayan hesap `/baglan`'a giremiyor (303)
- İki dilde metinler yerinde; manifest dile göre değişiyor
  (`short_name` "Lab Kayıt" / "Lab Record")
- 13 adres 200, JS hatası yok

---

# v6.46 — veri programdan ayrıldı (paketlemenin ön şartı)

## Neden

Program kurulabilir bir uygulama haline gelecek (PyInstaller + kurulum
dosyası). O zaman **kodun durduğu yer salt okunur** olur: Mac'te `.app`
paketinin içi, Windows'ta `Program Files`. Bugün `lab.db`, `yerel_ayar.json`,
`arsiv/` ve `snapshot/` kodun yanında duruyor — paketlenince ya yazılamaz ya
da program güncellenince **üzerine yazılır ve veri silinir**.

Bu iş ne kadar geç yapılırsa o kadar pahalı: bugün kod değişikliği, sonra
"kurulmuş makinelerdeki veriyi taşıma" işi.

## İki kök

`db.py` artık iki ayrı kök tanımlıyor ve **karıştırılmamalı**:

| | ne var | pakette |
|---|---|---|
| `PROGRAM_KOK` | kod, `templates/`, `static/`, `sema_guncel.sql`, göçler | salt okunur |
| `VERI_KOK` | `lab.db`, `yerel_ayar.json`, `arsiv/`, `snapshot/`, `yedek.log` | yazılabilir |

Veri kökü üç adımda bulunuyor, sıra bilerek böyle:

1. **`LAB_VERI` ortam değişkeni** — kurulum dosyası ve testler bunu kullanıyor.
2. **Kodun yanında `lab.db` varsa orası.** Kullanıcının Mac'i ve klinik mini
   PC'si böyle çalışıyor; veri **olduğu yerde bırakılıyor**, hiçbir şey
   taşınmıyor, hiçbir şey bozulmuyor.
3. Yoksa işletim sisteminin veri klasörü — yeni (paketlenmiş) kurulumlar:
   - Windows `%PROGRAMDATA%\PatientDataCenter`
   - macOS `~/Library/Application Support/PatientDataCenter`
   - ötekiler `~/.local/share/PatientDataCenter`

`PROGRAM_KOK` ayrıca `sys.frozen`'a bakıyor: paketlenmiş çalıştırmada
PyInstaller'ın açtığı klasörü döndürüyor. Yani paketleme günü bu dosyada
**kod değişmeyecek**.

## Asıl tehlike: 28 betik kendi yolunu kuruyordu

`goc_002.py` … `goc_029.py`, `goc_hepsi.py`, `teshis.py`, `teshis_silme.py`,
`liste_duzenle.py` — her biri `Path(__file__).parent / "lab.db"` yazıyordu.

Veri taşınsaydı bu betikler **kod klasöründe bomboş yeni bir `lab.db`
açardı**: göç sorunsuz çalışırdı, "27 başarılı" derdi, ve kullanıcı göçün
uygulandığını sanırdı. Gerçek veritabanına hiç dokunulmamış olurdu. Tuzak
#8'in ("ayarı iki yerden okuma") en pahalı hali — çünkü sessiz.

Hepsi `db.DB_YOLU`'na bağlandı. **Veritabanının yerini kendi başına kuran kod
yazma.**

`teshis.py` ve `sifirdan_kur.py`'de iki kök birden lazım: şema dosyası ve göç
betikleri `PROGRAM_KOK`'te, veritabanı ve ayar dosyası `VERI_KOK`'te. `yedek.py`
ve `tasi.py`'nin dokunduğu her şey veri.

## Test edildi

Paketlenmiş kurulum `LAB_VERI` ile taklit edildi:

- **Boş veri klasörü:** `goc_hepsi.py` "lab.db bulunamadi" deyip durdu,
  **boş veritabanı açmadı** (asıl korkulan buydu)
- Gerçek veritabanı o klasöre konunca 27 göç orada çalıştı, proje
  klasöründeki `lab.db` **bitine kadar değişmedi** (md5 aynı)
- Uygulama ayrı veri klasörüyle açıldı; `yerel_ayar.json`, `arsiv/` ve
  `snapshot/` oraya oluşturuldu
- `yedek.py` iki kipte de çalıştı, `yedek.log` veri klasörüne yazıldı
- **Normal kip (bugünkü kurulum) bozulmadı:** 20 adres 200, sunucu günlüğünde
  hata yok, `goc_hepsi.py` ve `teshis.py` doğru veritabanını buluyor

## Sırada ne var

1. **Göçler açılışta kendiliğinden çalışsın.** Bugün `python goc_hepsi.py`
   elle çalıştırılıyor; hiçbir klinik bunu yapmaz. Bu aynı zamanda tuzak #3'ü
   (göç çalıştırılmamış makinede ekranların bozulması) kalıcı olarak bitirir.
2. **Windows kurulum dosyası** — PyInstaller + Inno Setup, servis olarak
   kurulum, açılışta başlatma, güvenlik duvarı kuralı.
3. **Mac paketi** (`.app` + `.dmg`) — kullanıcının evdeki makinesi için.
4. İmzalama: Windows SmartScreen ve Mac Gatekeeper uyarıları. Kendi kliniğin
   için gerekmez, satarken gerekir.

---

# v6.47 — karekod doğrudan yönergeye açılıyor, simgenin adı tam ad

## "Okutunca direkt eklensin"

Kullanıcının isteği. Bunu tam olarak yapmak **mümkün değil**: bir web sayfası
kendini ana ekrana ekleyemiyor. iOS'ta böyle bir API hiç yok — "Ana Ekrana
Ekle" yalnızca kullanıcının paylaşma menüsünden yapabileceği bir iş.
Android'de `beforeinstallprompt` var ama **güvenli bağlantı (HTTPS) ve
service worker** istiyor; ikisi de bizde yok (bekleyen iş 3).

Yapılabilecek en yakın şey yapıldı: karekod artık programın **giriş ekranına
değil, ekleme yönergesine** açılıyor (`/ekle`).

Önceden okutan kişi giriş ekranına düşüyordu ve "şimdi ne yapacağım" sorusunun
cevabı yöneticinin elindeki kâğıtta kalıyordu. Şimdi telefonunda **kendi
telefonuna göre** üç adım görüyor: iPhone'a iPhone adımları, Android'e Android
adımları, bilgisayara "bu sayfa telefon içindir" notu.

Üç ayrıntı:

- **Giriş gerektirmiyor** (`ACIK_YOLLAR`). Okutan kişinin henüz hesabı yok;
  ekranda da yalnızca yönerge var, hasta verisi yok.
- Program **zaten ana ekrandan açıldıysa** (`display-mode: standalone`)
  yönerge basılmıyor, "eklemeye gerek yok" yazıyor.
- Android kurulum istemi verirse **gerçek bir "Ana ekrana ekle" düğmesi**
  çıkıyor ve adım listesi gizleniyor. Bugün tetiklenmiyor (HTTPS yok), ama
  HTTPS geldiğinde kod hazır — o gün tek dokunuşla eklenecek.

## Simgenin altındaki ad

"Lab Kayıt" yazıyordu; kullanıcı **Patient Data Center** istedi. `kisa_ad`
değişti, hem manifest'in `short_name`'i hem iOS'un
`apple-mobile-web-app-title`'ı oradan geliyor.

Telefon uzun adı kısaltıp "..." koyabilir — simgenin altında yaklaşık 12
karakter sığıyor. Kısaltılmış bir ad istenirse tek yerden değişiyor.

## Test edildi

- `/ekle` oturumsuz 200 veriyor
- iPhone, Android ve masaüstü kimliğiyle açıldı; üçünde de **yalnızca kendi
  kartı** görünüyor, JS hatası yok
- Karekod artık `http://<adres>/ekle` taşıyor
- Manifest ve iOS başlığı "Patient Data Center"
- 12 adres 200, iki dilde metinler yerinde

---

# v6.48 — ilk gelen ekran yine şifre ekranı (v6.47'nin gerilemesi)

## Ne oldu

Kullanıcı bildirdi: karekodu okutup ana ekrana ekleyince **şifre ekranı
çıkmıyor**.

Sebep v6.47'de yaptığım değişiklik. Karekodu `/ekle` yönergesine çevirmiştim;
iPhone "Ana Ekrana Ekle" derken çoğu zaman **manifest'in `start_url`'ünü
değil, o an açık olan adresi** kaydediyor. Simge `/ekle`'yi yakalamış oluyor
ve o sayfa `ACIK_YOLLAR`'da — program hiç açılmadığı için şifre de hiç
sorulmuyor.

Giriş kapısının kendisi sağlamdı: oturumsuz `/`, `/hastalar`, `/cycle/...`,
`/yonetim`, `/baglan` hepsi `/giris`'e dönüyordu; `/ekle` yalnızca yönerge
gösteriyordu, hasta verisi değil. Ama kullanıcı haklı — **ilk gelen ekran
şifre ekranı olmalı.**

## İki katmanlı düzeltme

**1. Karekod yine programın kendisine açılıyor.** Okutan kişi doğrudan şifre
ekranını görüyor; ana ekrana oradan eklerse simge `/giris`'i yakalıyor ve her
açılışta yine şifre ekranı geliyor.

Yönerge kaybolmadı: **giriş ekranına "Ana ekrana ekle" bağlantısı** kondu.
Yani sıra artık şifre ekranı → (isterse) yönerge.

**2. Yönerge sayfası ana ekrandan açılırsa programa geçiyor.** Birinin
simgesi v6.47 döneminde `/ekle`'yi yakaladıysa `location.replace('/')` ile
programa düşüyor — oradan da şifre ekranına. Eski simgeler kendiliğinden
düzeliyor, kimsenin bir şey silip yeniden eklemesi gerekmiyor.

`replace` bilerek: geri tuşu yönergeye dönmesin.

## Test edildi

- Oturumsuz `/` → `/giris`, şifre alanı ekranda
- Giriş ekranında "Ana ekrana ekle" bağlantısı var, `/ekle` oradan açılıyor
- Safari'den `/ekle`: yönerge görünüyor
- **Ana ekrandan açılmış gibi** (`navigator.standalone`) `/ekle`: `/giris`'e
  düşüyor ve şifre alanı geliyor
- Oturumsuz açık olan adresler yalnızca: `/giris`, `/sifre`,
  `/sifremi-unuttum`, `/manifest.json`, `/ekle` — hiçbirinde hasta verisi yok
- Oturumlu 12 adres 200, sunucu günlüğünde hata yok

---

# v6.49 — göçler açılışta kendiliğinden çalışıyor

## Neden

Paketlemenin ikinci adımı. Bugün veritabanı güncellemeleri terminalden elle
çalıştırılıyor (`python goc_hepsi.py`). **Hiçbir klinik bunu yapmaz** — ve
yapmazsa ekranlar sessizce eksik davranır. Bu aynı zamanda tuzak #3'ün
("göç yazdıysan kullanıcının çalıştırdığını varsayma") kalıcı çözümü.

## Paketlemenin tuzağı: alt süreç

`goc_hepsi.py` her göçü şöyle çalıştırıyordu:

```python
subprocess.run([sys.executable, "goc_029.py"])
```

Paketlenmiş uygulamada `sys.executable` **programın kendisidir**. Bu satır
göçü çalıştırmaz, programı yeniden başlatır — ve `.py` dosyaları diskte
olmayabilir bile.

Çözüm: göçler **süreç içinde** çalışıyor. Göç betikleri en üst düzeyde
çalışan betikler, yani `import goc_029` demek onu çalıştırmak demek.
`goc.py` bunu yapıyor, çıktısını yakalıyor, `sys.exit()`'i çıkış koduna
bakarak hata sayıp saymıyor.

## Hangi göç çalıştı: `goc_kaydi`

Yeni bir tablo uygulanan göçlerin adını tutuyor. Tabloyu **çalıştırıcı
kendisi açıyor**, bir göçle değil — kendi kaydını tutan tabloyu göçle kurmak
tavuk-yumurta olurdu.

Eski kurulumlarda kayıt yok ama göçler uygulanmış: ilk açılışta 27'si
yeniden koşuyor (hepsi idempotent, saniyenin altında) ve kaydediliyor.
Sonraki açılışlarda hiçbiri çalışmıyor.

Kazanç sadece hız değil: artık **hangi göçün ne zaman uygulandığı** yazılı.

## Soru soran göç

`goc_002` şifre soruyor, kendiliğinden çalıştırılamaz. Ama her açılışta
"elle çalıştır" diye uyarmak da yanlış — çoğu kurulumda **zaten
uygulanmış**. `ELLE` sözlüğü artık her biri için o göçün **etkisini** arayan
bir sorgu tutuyor (`goc_002` → `oturum` tablosu var mı). Etki varsa göç
uygulanmış sayılıp kaydediliyor ve panel susuyor.

## Göç patlarsa program yine açılıyor

Bilerek: açılmayan bir program teşhis edilemez. Hata terminale ve
`/yonetim` paneline yazılıyor, ekranlar çalışmaya devam ediyor. Sıradaki
göçler çalıştırılmıyor — biri ötekine dayanıyor olabilir.

**Denendi:** bilerek patlayan bir göç konuldu. 27 sağlam göç uygulandı,
patlayan rapor edildi, program açıldı, bütün ekranlar 200 verdi ve panelde
göçün adı, çıktısı ve hata mesajı göründü.

## Eşzamanlılık

İki süreç aynı anda başlarsa aynı `ALTER` iki kez çalışabilirdi.
`BEGIN IMMEDIATE` ile bir işaret konuyor; işareti kapan çalıştırıyor, öteki
atlıyor. Beş dakikadan eski işaret çökmüş bir süreçten kalmış sayılıp yok
sayılıyor.

## `goc_hepsi.py` duruyor ama artık ince

Aynı çalıştırıcıyı (`goc.calistir()`) kullanıyor — ikinci bir kopya yok.
İşi terminalden kontrol etmek, ayrıntılı çıktı görmek ya da sunucuyu
başlatmadan veritabanını güncellemek.

## Test edildi

- Ayrı bir veri klasöründe 27 göç açılışta uygulandı, ikinci açılışta hiçbiri
- Bir göçün etkisi **gerçekten geri geldi**: `cycle.planlanan_tarih` kolonu ve
  indeksi elle silindi, göç ikisini de geri getirdi
- Patlayan göç: program açıldı, 4 ekran 200, panel hatayı adıyla gösterdi
- `goc_002` artık uyarmıyor (etkisi var)
- Normal kip: açılışta çıktı yok, panel "Veritabanı güncel" diyor,
  19 adres 200, sunucu günlüğünde hata yok

## Sırada

Windows kurulum dosyası: PyInstaller + Inno Setup, servis olarak kurulum,
açılışta başlatma, güvenlik duvarı kuralı. Göç betiklerinin pakete
alınması için PyInstaller'a `hiddenimports` verilecek — `goc.py` zaten
dosya bulamazsa modül listesine bakıyor.

---

# v6.50 — kurulabilir paket

Paketlemenin üçüncü adımı: programın Python kurulu olmayan bir makinede
çalışması.

## Giriş noktası

Geliştirmede sunucu `python3 -m uvicorn app:uygulama ...` ile açılıyor.
Pakette bu **çalışmaz**: `python` yok, `-m` yok, `"app:uygulama"` metniyle
modül aramak da paketin içinde güvenilir değil.

`baslat.py` uvicorn'u kütüphane gibi çağırıp uygulama nesnesini doğrudan
veriyor. Geliştirmede de aynı yol kullanılıyor (`python3 baslat.py`) — iki
ayrı başlatma yolu olsaydı biri er geç ötekinden ayrı düşerdi.

Ayarlar ortam değişkeninden: `LAB_ADRES`, `LAB_PORT`, `LAB_VERI`. Kurulum
dosyası bunları göreve yazacak.

## `print` yerine `logging`

İlk paket denemesinde göçler **çalıştı** (`goc_kaydi`'da 28 satır vardı) ama
"27 göç uygulandı" satırı günlüğe hiç düşmedi. Sebep: `print` çıktısı dosyaya
yönlendirilince tamponda kalıyor ve süreç çalışmaya devam ettiği için
boşalmıyor.

Servis olarak çalışırken konsol yok; bir şey ters giderse bakılacak **tek yer**
günlük dosyası. `app.py`'deki bütün `print`'ler `logging`'e çevrildi;
`baslat.py` günlüğü hem konsola hem veri klasöründeki `program.log`'a
bağlıyor (1 MB'ta yenileniyor, üç eski kopya).

## Tarifte iki tuzak

İkisi de sessizce bozar — program açılır, sonra yanlış davranır:

1. **Şablonlar ve `static/` veri olarak eklenmeli.** PyInstaller yalnızca
   `import` edilenleri toplar; Jinja şablonlarını ve CSS'i göremez.
2. **Göç betikleri `hiddenimports`'ta olmalı.** `importlib.import_module(
   "goc_029")` ile adıyla çağrıldıkları için görünmezler. Eksik kalsalar
   veritabanı güncellemeleri sessizce çalışmazdı.

Tarif her ikisini de dosya adına bakarak kendiliğinden topluyor: yeni bir göç
yazdığında `pdc.spec`'e dokunmak gerekmiyor.

## Gerçekten denendi

Linux paketi üretilip **kaynak klasörünün dışına** kopyalandı ve `PYTHONPATH`
temizlenmiş halde çalıştırıldı:

- Veri klasörünü ortam değişkeninden buldu
- **27 göç paketin içinden uygulandı**
- 22 adres 200: bütün ekranlar, `static/`, `manifest.json`, karekod, resmî
  form ve Excel çıktısı (24 KB'lık geçerli bir `.xlsx`)
- Günlük hem konsola hem `program.log`'a düştü

Paket ~32 MB. Windows ve Mac paketleri **o işletim sistemlerinde** üretilecek
— PyInstaller çapraz derleme yapmıyor.

## Windows kurulum dosyası (taslak)

`paket/pdc_kurulum.iss`, Inno Setup ile derleniyor. **Henüz Windows'ta
denenmedi**, ilk kurulumda birlikte gözden geçirilecek.

- Program `C:\Program Files\Patient Data Center`, veri
  `C:\ProgramData\PatientDataCenter` — ayrı, çünkü paketin içi güncellemede
  siliniyor
- Açılışta başlatma **Görev Zamanlayıcı** ile (servis kurmak için NSSM gibi
  bir aracı pakete katmak gerekirdi; bu Windows'un kendi parçası)
- Güvenlik duvarı kuralı bilerek yalnızca **yerel ağ** için
- Kaldırma verileri **silmiyor**

## Sırada

**İlk kurulum ekranı.** Paket bugün `lab.db` yoksa "önce kurulumu tamamlayın"
deyip duruyor. Yeni bir klinikte veritabanını ve ilk yönetici hesabını kuracak
bir ilk açılış akışı gerekiyor — `sifirdan_kur.py` terminalde soru soruyor,
paketlenmiş uygulamada terminal yok.


---

# v6.51 — bozuk tarihler: bulundu, düzeltildi, bir daha girilemiyor

Bekleyen iş 6 kapandı. Bir cycle'da OPU tarihi `0026-09-04` yazıyordu; bu
sürüm hem o kaydı düzeltmenin yolunu veriyor, hem de aynı hatanın bir daha
kaydedilmesini engelliyor.

## Hata nasıl oluyor

`datetime-local` ve `date` alanlarına yıl olarak "26" yazılırsa tarayıcı
bunu **26. yıl** diye gönderiyor: `0026-09-04`. Telefonda yıl kutusuna iki
hane yazmak çok kolay.

Asıl mesele şu: `0026-09-04` **geçerli bir ISO tarihidir**. `fromisoformat`
onu sorunsuz okur, SQLite sorunsuz saklar, ekran sorunsuz basar. Hiçbir
katman itiraz etmiyor, o yüzden kayıt aylarca fark edilmeden duruyor.
Sessizce yanlış olan veri, gürültüyle patlayan veriden pahalıdır.

Görünen sonuçları: o vaka ay listesinde çıkmıyor (ayın ölçüsü OPU tarihi),
`_opu_gunu()` None dönüyor, resmî formda saçma bir tarih basılıyor, yıl
seçicisi iki bin satır olmak istiyor (v6.30'da `>= 2000` süzgeciyle
kapatılmıştı — o yama artık sebebin kendisini de düzeltiyor).

## Üç katman

**1. Bulunanı düzeltmek: `tarih_duzelt.py`.**

Yılı 1900'den küçük bütün tarihleri buluyor — tek bir kolona bakmıyor,
veritabanındaki adında `tarih` ya da `zaman` geçen **bütün metin
kolonlarını** tarıyor (`gun`, `stim_gun_sayisi` gibi sayı kolonları tipten
eleniyor). Bir tanesini biliyorduk; aracın işi bilmediklerimizi de bulmak.

**Hiçbir şeyi kendiliğinden değiştirmiyor.** Her kayıt için ne bulduğunu,
**kime ait olduğunu** (dosya no, hasta adı, cycle no) ve ne önerdiğini
yazıyor; kararı kullanıcı veriyor. Tarih klinik veridir, varsayımla
düzeltilmez — bu projenin kuralı.

Öneri de uydurma değil: gün ve saat olduğu gibi kalıyor, **yıl kaydın kendi
oluşturma yılından** geliyor. Kayıt 2026'da girildiyse o gün yazılan klinik
tarih de 2026'dır. `olusturma_zamani` yoksa cycle'ınkine bakılıyor.

**Doğum tarihlerine öneri yapılmıyor** (`dogum_tarihi`, `es_dogum_tarihi`,
`dogum_zamani`): kaydın girildiği yılla doğum yılının ilgisi yok. Orada araç
"öneremiyorum, doğru tarihi kendin yaz" diyor. Yanlış öneri, önerisizlikten
kötüdür — kullanıcı Enter'a basıp geçer.

```
python3 tarih_duzelt.py         bulur, tek tek sorar, onayladığını düzeltir
python3 tarih_duzelt.py liste   yalnızca listeler, hiçbir şeye dokunmaz
```

Terminalden çalıştırılmadıysa (boru, betik) soru soramayacağı için hiçbir
şey değiştirmiyor.

**2. Bir daha girilememesi: `yil_kontrol()`.**

`zaman()` artık yılı 1900'den küçük değeri kabul etmiyor, `FormHatasi`
atıyor. Sınır 2000 değil **1900**, çünkü doğum tarihleri 1900'lerde olabilir.

Hata dönüşü v6.21 kuralına uyuyor: **form kapanmıyor, yazılan duruyor.**
Cycle formu ve hasta formları yazılan değerlerle yeniden basılıyor; OPU
ekranı kendi `?duzenle=1&hata=...` yoluyla dönüyor. Kullanıcı ne yazdığını
görüyor ve yalnız yılı düzeltiyor.

Hasta ekleme/düzenleme ekranlarında hata gösterecek yer **yoktu** — bu sürümde
eklendi (`{% if hata %}`), doğum tarihleri artık orada da korunuyor.

`islem_zamani()` ayrı davranıyor: aşama ekranlarının POST'unda hata
gösterecek yer yok, bu yüzden bozuk yıl "geçersiz" sayılıp **şu ana**
düşülüyor — fonksiyonun zaten belgelenmiş davranışı. Kullanıcı kaydettikten
sonra bilgi kartında yazan saati görüyor.

**3. Tarayıcı tarafı: `min` niteliği.**

18 tarih alanına `min="1900-01-01"` kondu. Tarayıcı yılı küçük değeri
göndermeden reddediyor, hata da alan altında kendi diliyle çıkıyor — sunucuya
hiç gitmeden. Ama asıl engel sunucudaki kontrol: tarayıcıya güvenilmez.

## Teşhiste de görünüyor

`teshis.py`'nin **veritabanı** bölümüne kondu, klasör bölümüne değil: klasör
yolu yanlışsa betik orada `sys.exit` ediyor ve arkasındaki hiçbir kontrol
çalışmıyor. Tarih kontrolü o çıkışın önünde duruyor.

## Bir şey açıkta kaldı

Cycle formunda `denudasyon_zamani` **gizli alan** olarak taşınıyor. Bir
cycle'ın denüdasyon saati bozuksa cycle formundan kaydetmek artık hata
veriyor ve gizli alan ekranda görünmediği için oradan düzeltilemiyor.
Çıkışı `tarih_duzelt.py`. Bugüne kadar böyle bir kayıt görülmedi.

## Test edildi

- Araç, kasten bozulmuş üç kayıtla denendi: cycle OPU zamanı (öneri kabul
  edildi), hasta doğum tarihi (önerisiz dal, elle yazıldı), sayı tipli `gun`
  kolonu (doğru şekilde hiç taranmadı). İkinci çalıştırmada "düzeltilecek bir
  şey yok" dedi.
- Cycle formu, hasta ekleme, hasta düzenleme ve OPU ekranı bozuk yılla
  denendi: dördü de hata gösterdi, **yazılan değerler ekranda kaldı** ve
  veritabanına hiçbir şey yazılmadı.
- `islem_zamani()`: `0026-...` → şu an, `2026-...` → olduğu gibi.
- Deneme verisi geri alındı (1 hasta, 2 cycle, 22 oturum).

> Geri alırken WAL tuzağına girildi: uygulama çalışırken `lab.db`'nin üzerine
> kopyalamak işe yaramıyor, `lab.db-wal` sonradan üstüne biniyor. README
> v6.6'da yazılı olan kural burada da geçerliymiş — önce durdur, sonra kopyala.


---

# v6.52 — geniş ekran düzeni öteki ekranlara yayıldı

v6.42'de iki sütunlu düzen yalnızca iki ekranda vardı (yönetim ve cycle),
kullanıcının kararıyla: "önce yönetim + cycle, sonra bakarız". Sonrası bu.

## Kural: iki sütun her yerin çözümü değil

Şikâyet "ekranın yarısı boş kalıyor"du. Çözümü her ekranda ikiye bölmek
değil — **bölmenin bir anlamı olmalı.** Ölçü şu: ekranda birbirinden bağımsız
kartlar mı var, yoksa genişliğe ihtiyacı olan tek bir şey mi?

**İki sütun** (bağımsız kartlar, ikisi de dar içerik):

| ekran | solda | sağda | boy |
|---|---|---|---|
| `/kullanicilar` | kullanıcı listesi | yeni kullanıcı + açıklama | 2596 → 1705 |
| `/istatistik` | oranlar + aylık çizelge | son kayıtlar | 1103 → 913 |
| `/formlar` | form yükleme | gömülü + yüklenen formlar | 1090 → 692 |

`/istatistik`'te "Genel toplam" sütunların **üstünde tam genişlikte** kaldı:
sekiz sayılık şerit genişliği zaten kullanıyor, ikiye bölmek onu sıkıştırırdı.

**Yalnızca genişleme** (tek bir şey var, ona genişlik lazım):

| ekran | neden | genişlik |
|---|---|---|
| `/klasorler` | tek form kartı; klasör yolları uzun metin | 640 → 940 |
| `/cryo` | taşıyıcı satırında tam konum yolu yazıyor | 640 → 940 |
| `/hasta/{id}` | cycle satırları; ana ekrandaki satırın aynısı | 640 → 940 |
| `/hastalar`, `/bitenler`, `/takvim` | aynı `_cyclesatir` satırları | 640 → 940 |

Liste ekranlarını bölmedim: `_cyclesatir.html` satırları soldan sağa okunan
tek bir akış. İki sütuna bölmek "aşağı devam et"i "yukarı dön"e çevirirdi.
Şimdi altısı da ana ekranın listeleriyle **aynı ölçüde** görünüyor.

**Bilerek dar bırakılanlar:**

- `/cycle/{id}/bitir` — onay ekranı. Üç düğmeden biri cycle'ı kapatıyor;
  dar olması yanlışlıkla basmayı zorlaştırıyor, bu bir özellik.
- `/dil` ve form ekranları (`/hasta/yeni`, `/hasta/{id}/duzenle`,
  cycle formu) — form alanı genişledikçe etiketle değer birbirinden uzaklaşır.
  v6.42'nin "genişletmek tek başına çözüm değil" gerekçesinin aynısı.
- Aşama ekranları — kendi düzenleri var (şerit → fotoğraf → kart).

## Kimlik bandının hizası

`/hasta/{id}` genişleyen ilk **kimlik bantlı, yan menüsüz** ekran oldu ve
orada bir boşluk çıktı: bant `--genis-sutun` ile hizalanıyordu, `.kap` ise
`.yanmenusuz` yüzünden 940'ta duruyordu. 1440'ta ikisi aynı sayıya geliyor,
**1100–1440 arasında bandın yazısı kartlardan ~120px kayıyordu.**

Ölçü ikinci bir değişkene alındı: `--genis-sutun-menusuz`. Hem
`.kap.genis.yanmenusuz` hem `body.genissayfa.menusuzsayfa .kimlik` onu
kullanıyor — v6.42'nin "içerik sütununun genişliği tek yerde" kuralının
yan menüsüz hali. Şablon ikisini birlikte veriyor:

```jinja
{% block kapsinif %} genis yanmenusuz{% endblock %}
{% block govde %}genissayfa menusuzsayfa{% endblock %}
```

## Bir tuzak: bölme noktası `{% if %}`'in içine düşmemeli

`/formlar`'da bölme noktası ilk yazışta `{% if gomulu %}`'nin **içine**
düştü. Gömülü form yoksa `</div>` hiç basılmayacak, sondaki kapanışlar
açıkta kalacaktı — ve ticari dağıtımda gömülü form **olmayacak** (v6.41),
yani tam da o durumda bozulacaktı. Sütun sınırı koşulun dışına alındı.

Yeni bir ekranı bölerken: bölme noktası **her zaman** basılan bir yerde
olmalı.

## Test edildi

- 15 ekran 1440 ve 1280px'te ölçüldü: genişlik, sayfa boyu, kimlik bandı ile
  kart sütununun hizası. Bant farkı her ekranda tam 16px (istenen iç boşluk).
- 1100 / 1150 / 900 / 860 / 700px'te yatay taşma ve yan menü çakışması
  arandı — hiçbirinde yok.
- 390px'te (telefon) sütunlar alt alta diziliyor ve **sıra kaynak sırasıyla
  bire bir aynı**: değişen ekranların telefon görünümü eskisinin aynısı.
- 31 adres 200 verdi. Deneme verisi geri alındı.

> Ölçerken görülen, bu sürümün dışında bir şey: `/cycle/{id}` 1280px'te tek
> sütuna düşüyor (`--genis-sutun` = 780, iki sütuna yetmiyor). Yan menüsü
> olduğu için `yanmenusuz` sınıfını alamıyor. 1440'ta iki sütun. Kullanıcı
> isterse menü payı ayrıca gözden geçirilir.


---

# v6.53 — tarih denetimi sıkılaştırıldı

Kullanıcı v6.51'in aracını kendi veritabanında çalıştırdı ve "düzeltilecek bir
şey bulunamadı" çıktı — bekleyen iş 6'nın kaydı artık yok. Ama "temiz" cevabı
aracın **ne kadar geniş baktığına** bağlı ve orada bir boşluk vardı.

## Boşluk

v6.51 tek bir şeye bakıyordu: dört haneli yıl, 1900'den küçük mü. Bunlar
elinden kaçıyordu:

| değer | v6.51 | neden kaçıyordu |
|---|---|---|
| `20026-09-02 09:00` | kaçtı | ilk dört hane `2002`, sınırın içinde |
| `04.09.2026 14:35` | kaçtı | `^\d{4}-` kalıbına hiç uymuyor |
| `88-01-05` | kaçtı | yıl iki haneli, kalıp eşleşmiyor |
| `0026-09-04` | buldu | |
| `0085-04-11` | buldu | |

Yani "bozuk tarih yok" demek "dört haneli yılı küçük tarih yok" demekti. Bir
aracın işi sessiz duran bozuk veriyi bulmaksa, dar bir kalıba güvenmemesi
gerekir.

## Denetim tersine çevrildi

Artık **"bozuk olanı tanı" değil, "makul olanı geçir"**: değer tarihe
çevrilmeye çalışılıyor (`_coz`, `datetime.fromisoformat`) ve üç şey
bildiriliyor — yılı çok eski, yılı çok ileri, hiç okunamıyor. Ekranda sebep
de yazıyor.

Üst sınır `bu yıl + 5`. `planlanan_tarih` bilerek gelecekte olabiliyor
(ileri tarihli cycle) ve bebeğin doğum tarihi dokuz ay ileri; beş yıl ikisine
bol bol yetiyor, `9999` gibi bir yazım hatasını yakalıyor.

**Öneri artık ayrıştırılmış tarihten kuruluyor**, dizginin ilk dört hanesini
değiştirerek değil: `20026-09-04`'te ilk dört hane yılı vermiyordu. 29 Şubat
kaydı artık yıl olmayan bir yıla taşınırsa öneri yapılmıyor (ValueError
yakalanıyor).

Okunamayan değere öneri yok — gün ve ay da belirsiz, kullanıcı yazacak.

## Göç defteri taranmıyor

Yeni denetim ilk çalıştığında hemen bir şey buldu: `goc_kaydi.zaman =
'onceden'`. Bu yanlış alarm değil bir **yanlış hedef**: `goc.py` zaten
uygulanmış bir göç için bilerek o işareti yazıyor (`ELLE` sözlüğü,
`_etkisi_var()` yolu).

`goc_kaydi` taramadan çıkarıldı (`ATLA_TABLO`) — iki sebeple: tarih tutmuyor,
ve o tabloyu düzenlemeye davet etmek tehlikeli. Oradaki bir satırı değiştirmek
bir göçün yeniden çalışmasına ya da atlanmasına yol açar. Klinik veri değil,
çalıştırıcının kendi kaydı.

## Sunucu tarafı: üst sınır da kondu

`yil_kontrol()` yalnızca alt sınırı tutuyordu. `9999-01-01` de `0026-09-04`
kadar sessiz bir yazım hatası, ve aynı şekilde hiçbir katmanda patlamıyor.
Sınır artık iki yönlü, aynı ölçüyle (`EN_YENI_YIL_PAYI = 5`) ve **her çağrıda
hesaplanıyor** — yıl dönünce sabit kalmasın.

**Şablonlarda yalnızca `min` var, `max` yok.** Üst sınır her yıl değişen bir
değer; şablona sabit yazılsa eskirdi, Jinja global'i eklemek 18 alan için
kurulacak makineden fazla iş. Asıl engel zaten sunucuda.

## Test edildi

- Beş bozuk biçim aynı anda konuldu (yukarıdaki tablo): **beşi de bulundu**,
  sebepleriyle. v6.51 bunlardan ikisini buluyordu.
- Düzeltme yolu gerçek bir terminal üzerinden sürüldü: elle tarih yazma,
  Enter ile öneriyi kabul, `a` ile atlama. Dört kayıt düzeltildi, **atlanan
  kayıt olduğu gibi kaldı** ve ikinci çalıştırmada yine bildirildi.
- Sunucu sınırı: 1899 red, 1900 kabul, 2031 kabul, 2032 red; `0026` ve `9999`
  cycle formunda reddedildi ve form yazılanla birlikte geri geldi.
- 32 adres 200; `teshis.py` "tarihlerin yılları makul" diyor.
- Denemeler **veritabanının kopyası** üzerinde yapıldı, asıl dosyaya
  dokunulmadı; deneme verisi geri alındı.


---

# v6.54 — ekran kendini tazeler

Kullanıcı fark etti: telefondan bir cycle'a bilgi ve fotoğraf girdi,
masaüstünde açık duran sayfa **elle yenilenene kadar** eskiyi göstermeye
devam etti. Klinikte birkaç telefon aynı anda kayıt giriyor; "ekranda ne
görüyorsam o güncel" olması gerekiyor.

## Veri zaten anında kaydoluyordu

Önce bunu ayırmak lazım: telefondan girilen kayıt **o anda** veritabanına
yazılıyordu. Eski olan veri değil, **masaüstündeki sayfa**. Tarayıcı bir
kere aldığı HTML'i kendiliğinden güncellemez. Yani sunucuda düzeltilecek bir
gecikme yoktu; eksik olan, açık duran sayfanın "yeni bir şey oldu mu" diye
sorması.

## Neden yoklama, neden push değil

WebSocket `websockets`/`wsproto` paketi ister — projenin "ek bağımlılık yok"
kuralı bunun için var (`excel.py`, `karekod.py` ile aynı gerekçe). SSE
kütüphanesiz olurdu ama her açık sayfa için canlı bir bağlantı demek;
telefon ekranı kilitlenince kopuyor, yeniden bağlanma mantığı yazmak
gerekiyor.

Beş saniyede bir küçük bir JSON sorusu hem daha basit hem daha dayanıklı.
Üstüne bir şey eklendi: **sekmeye/pencereye dönünce hemen soruyor.**
Kullanıcı masaüstüne geçtiğinde ekran zaten güncel oluyor, beş saniye
beklemiyor — algılanan gecikme sıfır. Sayfa arkadayken yoklama duruyor
(telefon pili).

## "Değişti mi" sorusunun ucuz cevabı

Denenen ve çalışmayan yollar:

- **`PRAGMA data_version`** — bağlantı başına çalışıyor. Her istek kendi
  bağlantısını açtığı için değeri hiç değişmiyor; ölçüldü, hep aynı sayı.
- **Dosya damgası (`lab.db` mtime)** — her yazıyı yakalar, ama **oturum
  tablosu her istekte yazılıyordu**. Yani sayfa, kendi sorusunun yazdığı
  satır yüzünden "değişti" cevabı alıp sonsuz yenilenirdi.

Kalan yol: veriden türetilen bir imza. `veri_damgasi()` her tablo için
`COUNT(*)` ve `MAX(rowid)` topluyor — en büyük rowid **eklemeyi**, sayı
**silmeyi** yakalıyor, ikisi de rowid indeksinden okunuyor. Ölçüldü:
23 tablo, **0.7 ms**.

`DEGISIM_ATLA` bir **dışlama** listesi (`oturum`, `goc_kaydi`), kapsama
listesi değil: yeni bir tablo eklersen kendiliğinden kapsanır, bir şey
yapmana gerek yok.

**Kapsam** — her yeni kayıt, her silme, her iptal, ve `degisiklik_log`'a
satır yazan her düzenleme. Son madde önemli: programın ekranlarından yapılan
düzenlemeler günlüğe yazıyor, o yüzden yerinde düzenleme de yakalanıyor —
telefondan hasta adı değiştirildi, masaüstü **4 saniyede** güncellendi.

**İptal ayrıca sayılıyor** (`DEGISIM_EK`): `iptal_mi` yerinde 1'e çekiliyor
ve günlüğe düşmüyor. İptal klinik bir karar (atılan oosit, geri alınan
işlem), öteki ekranda görünmesi gerekir.

**Kapsam dışı:** günlüğe hiç yazmayan bir yerinde düzenleme. O ekran bugünkü
gibi elle yenilenene kadar eski kalır — gerileme değil, kapsanmayan bir
durum. Damga hiçbir veri sızdırmıyor, yalnızca sayılardan oluşan bir dizgi.

## Yazdığın asla silinmez

En büyük risk şu: personel telefonda form doldururken sayfa kendiliğinden
yenilenirse **yazdığı gider**. Bu, çözdüğü sorundan pahalı bir hata olurdu.

Bu yüzden yenilemeden önce sayfa "kirli mi" diye bakıyor: herhangi bir
alanın değeri varsayılanından farklıysa ya da imleç bir alanın içindeyse
**kendiliğinden yenilenmiyor**. Onun yerine altta bir şerit çıkıyor —
"başka bir cihazdan yeni kayıt girildi, yazdıkların kaybolur, önce kaydet" —
ve yenileme kararı kullanıcının. Denendi: forma yarım bir not yazılmış
haldeyken kayıt girildi, **not yerinde kaldı**, şerit çıktı.

Şerit **altta** duruyor: üstteki kimlik bandını kapatmamalı, "yanlış hasta"
bu işin en pahalı hatası.

## Yazdırma ekranları dışarıda

`form.html` (resmî form) ve `/baglan` (karekod, yazdırılıp laboratuvara
asılıyor) `{% block tazeleme %}` bloğunu boşaltıyor. Ctrl+P açıkken sayfanın
altından değişmesi çıktıyı bozar ve ikisinde de tazelenecek canlı veri yok.
Yeni bir yazdırma ekranı yazarsan aynısını yap.

## İki yan etki, ikisi de bilerek

**Oturum yazısı kısıldı.** `son_erisim` her istekte değil, bir dakikadan
eskiyse yazılıyor. Birkaç telefon beş saniyede bir soruyor; her soruda
veritabanına yazmak dakikada yüzlerce gereksiz yazı demekti. Oturum ömrü
12 saat, bir dakikalık kabalık onu etkilemiyor.

**Yoklama oturumu tazelemiyor** (`oturumdaki_kullanici(..., dokun=False)`).
Bu olmasa ekranı açık bırakılmış bir telefon **hiç düşmezdi** ve 12 saatlik
sınır işlevsiz kalırdı. Yoklama kullanıcının işlemi değil, sayfanın kendi
işi. Ölçüldü: `son_erisim` geriye alındı, yoklamadan sonra değişmedi, sayfa
açılınca güncellendi.

## Test edildi

- İki ayrı tarayıcı bağlamı: masaüstünde cycle ekranı açık, telefondan kayıt
  girildi → **5 saniyede kendiliğinden yenilendi**. Yeni hasta kaydı da
  5 saniyede listeye düştü.
- Telefondan hasta adı düzenlendi (gerçek ekrandan, POST ile) → masaüstü
  4 saniyede güncellendi.
- İptal işareti yerinde 1'e çekildi (günlüğe yazmadan) → damga değişti.
- **Döngü yok:** üç ekranda 26 saniye beklendi, hiçbir şey değişmedi —
  5 yoklama, **0 yenileme**. Gezinmek de damgayı değiştirmiyor.
- Kirli form korundu (yukarı bak). Şerit 1280 ve 390px'te denendi, yatay
  taşma yok.
- 36 adres 200; yazdırma ekranlarında betik yok, giriş ekranında da yok.
- Deneme verisi geri alındı.


---

# v6.55 — aynı kaydı iki kişi düzenlerse uyarı

Kullanıcının isteği: "biri bir alana bilgi girerken başka cihazdan aynı alana
bir şey girilmek istendiğinde uyarı verse". v6.54 **ne değiştiğini**
gösteriyordu; bu sürüm **kimin şu anda yazdığını** gösteriyor.

## Uyarının birimi "alan" değil "kayıt"

İstek alan bazında geldi ama alan bazında uyarmak **yanlış bir güven**
verirdi. Sebebi kodda: kayıt edilirken formun **tamamı** yazılıyor —

```python
db.yaz(f"UPDATE olay SET {set_ifade}, zaman=?, kullanici_id=? WHERE id=?", ...)
```

`set_ifade` o formun bütün alanları. Yani iki kişi **farklı** alanları
düzenlese bile, ikinci kaydeden birincinin alanını kendi tarayıcısının
yüklediği eski değere geri çeviriyor. "Ben başka alandayım, sorun yok"
demek tam da kaybın yaşandığı durum.

Bu yüzden birim **kayıt**: bir oositin ICSI kaydı, bir cycle'ın OPU'su, bir
hastanın künyesi. Farklı oosit, farklı aşama, farklı cycle → uyarı yok
(denendi, dördü de doğru).

## Uyarı engellemez

Katı kilit klinikte yanlış olurdu:

- Telefonun pili biterse kayıt kilitli kalır ve kimse giremez.
- Acele eden personeli kayıt girmekten alıkoymak, çarpışmadan pahalıya gelir.

Program haber veriyor, kararı kullanıcı veriyor — projenin "ekranda gizlemek
yetmez ama insanın işini de kesme" dengesiyle aynı çizgide.

## Bellekte, `lab.db`'de değil

İki sebep:

1. Bu veri **o anki sunucu çalışmasına** ait, klinik kayıt değil. Göç de
   gerekmiyor.
2. `lab.db` USB ile taşınıyor; "düzenleniyor" satırları tabloda olsaydı
   bayat haberler de onunla birlikte klinikten eve giderdi.

`_duzenleyenler` sözlüğü + `threading.Lock` (rotalar iş parçacığı havuzunda
çalışıyor, eş zamanlı erişim gerçek). 45 saniye ses vermeyen bırakmış
sayılıyor; sözlük `DUZENLEME_EN_COK` ile sınırlı.

> **Sunucu tek süreç çalışıyor** (`baslat.py`). Birden çok işçiyle
> çalıştırılırsa bu sözlük paylaşılmaz ve uyarı çalışmaz. O gün ortak bir
> yere taşınması gerekir — bugünkü kurulumda gerek yok.

## Kimlik sekme başına, kullanıcı başına değil

Aynı kişi telefonundan ve masaüstünden aynı kaydı açtıysa **o da gerçek bir
çarpışma**: iki tarayıcıdan ikisi de kaydeder ve biri ötekini siler. O yüzden
kimlik sayfa başına üretilen rastgele bir dizgi; uyarı kendi kısa kodunu
göstererek "öteki cihazında da açık" diyor.

## Yalnızca izleyen ekran hiçbir şey yazmıyor

İki ayrı yol var, bilerek:

- `GET /degisim?anahtar=...` — damgayı **ve** o kaydı başka kim düzenliyorsa
  onu döndürüyor. **Hiçbir şey yazmıyor.** İkinci bir yoklayıcı eklemek
  yerine v6.54'ün isteğine bindirildi: klinikte birkaç telefon var, istek
  sayısı iki katına çıkmasın.
- `POST /duzenliyorum` — haber. Yalnızca **gerçekten düzenleyen** gönderiyor,
  15 saniyede bir.

Yani bir kaydı sadece izleyen ekran ne veritabanına ne belleğe dokunuyor.

**Yanlışlıkla bir alana dokunup bırakan** haber vermeyi bırakıyor: hiçbir şey
yazılmamış ve iki dakika dokunulmamışsa haber kesiliyor. Olmasa öteki kişi
sonsuza kadar boşuna uyarılırdı.

## Anahtarı şablon söylüyor

`{% block kayitanahtari %}` — hangi kaydı düzenlediğini ekranın kendisi
biliyor. Adresten türetmek denenmedi çünkü yanlış olurdu: aşama ekranı
adressiz açıldığında ilk örneği seçiyor (v6.35), yani `/cycle/1/icsi` ile
`/cycle/1/icsi?oosit=1` **aynı kaydı** gösterip farklı anahtar üretirdi ve
uyarı kaçardı.

Anahtar sunucuda `ANAHTAR_KALIBI`'ndan geçiyor (tuzak #9): kalıba uymayan
istek hiç işlenmiyor. Ekrana basılan yazı yalnızca **veritabanındaki**
`kisa_kod`; istemciden gelen metin hiç basılmıyor.

**Bu sürümde kapsanan ekranlar:** OPU, androloji, denüdasyon, ICSI,
fertilizasyon, gün 2/3, blastokist, gebelik, işlemi bitir, cycle formu,
hasta künyesi. **Kapsam dışı:** vitrifikasyon, çözme ve transfer — orada tek
ekranda birden çok örneğin kartı var (`_ornekkart.html` ızgarası), ekran
bazında anahtar iki kişiyi **farklı embriyolarda** çalışırken de uyarırdı.
Yanlış alarm, uyarıya olan güveni bitirir. İstenirse açık kartın örnek
kodundan anahtar üretilerek eklenir.

## Test edildi

- İki tarayıcı bağlamı, iki farklı kullanıcı (TK ve AD), ikisi de aynı
  cycle'ın OPU ekranı: kimse yazmazken **uyarı yok**; AD telefondan yazınca
  TK'nin ekranında **"Bu kaydı şu anda AD da düzenliyor"**; TK de yazınca
  AD'de karşılığı çıktı; AD sayfayı kapatınca uyarı **5 saniyede** kalktı.
- Yanlış alarm aranıp bulunamadı: farklı aşama, farklı cycle, farklı kayıt
  türü — üçünde de uyarı yok.
- Kötü anahtarlar reddedildi (büyük harf, 70 karakter, `x;drop table`,
  `../../etc`, boş). İki rota da oturumsuz erişimde `/giris`'e döndü.
- İki izleyen ekran aynı anahtarı sorduğunda ikisi de boş liste aldı —
  `GET` gerçekten yazmıyor.
- 37 adres 200. Deneme verisi geri alındı.

## Yol boyunca: `metinler.py`'de beş ölü anahtar

Sözlükte beş anahtar iki kez tanımlıydı (`bekleyen_kare`, `dondurulmus`,
`sagkalim`, `geri_don`, `son_kayitlar`). Python'da sonraki kazanıyor, yani
öncekiler **ölü** satırlardı — ikisinin İngilizcesi de farklıydı ("Waiting
frame" / "Pending frames"). Türkçeleri aynı olduğu için bugün bir şey
bozmuyordu, ama birini düzeltip "neden değişmedi" demek için hazır bir
tuzak. Ölü olanlar silindi, davranış birebir aynı kaldı (714 anahtar).

## Sırada — bu uyarının yapmadığı şey

Uyarı **haber veriyor**, kaybı **engellemiyor**: iki kişi uyarıya rağmen
kaydederse ikinci yine birincinin üzerine yazıyor. Asıl güvenlik ağı şu
olurdu: form basılırken kaydın imzası forma gömülür, kaydederken imza
değişmişse kayıt **reddedilir** ve "bu kayıt sen düzenlerken değişti"
denir. Kullanıcıya sorulacak: uyarı yeterli mi, yoksa bu da eklenecek mi?


---

# v6.56 — denüdasyondaki over düğmeleri ötekilerin aynısı oldu

Kullanıcı iki şey bildirdi ve ikisinin **tek bir sebebi** vardı: denüdasyondaki
Sağ / Sol düğmelerinin yazısı telefonda seçilmeden önce görünmüyordu, ve o
düğmeler ICSI / fertilizasyon / blastokistteki aynı bileşenden farklı
duruyordu.

## Sebep: `<button>` ile `<label>` aynı sınıfı paylaşıyordu

`.sec` bileşeni **`<label>` + gizli radyo + `<span>`** için yazılmış: bütün
görsel biçim iç `<span>`'de. ICSI, fertilizasyon, gün 2/3, blastokist ve
gebelik böyle kullanıyor.

Denüdasyondaki over seçimi ise `<button class="sec">` — bilerek, çünkü tek
alanlık bir seçim için ayrı bir "Kaydet" düğmesi olmasın diye düğme kendi
başına gönderiyor (JS de gerekmiyor). Ama sınıf aynı olunca tarayıcının
**kendi düğme biçimi** devrede kalıyordu. Ölçüldü:

| | denüdasyon (`<button>`) | ICSI (`<label>`) |
|---|---|---|
| dış kutu | 96×58, **gri zemin + 2px kenarlık** | 105×52, şeffaf, kenarlıksız |
| iç span | 80×52 — içe gömülü | 105×52 — kutuyu tam dolduruyor |
| `appearance` | **auto** | none |
| yazı rengi | `rgb(0,0,0)` | `rgb(23,34,43)` (`--ink`) |

Yani beyaz kutunun etrafında **ikinci bir gri çerçeve** vardı, 6px daha
dar ve 6px daha yüksekti, yazı rengi de projenin mürekkebi değil tarayıcının
siyahıydı.

**Telefonda yazının kaybolması da buradan:** iOS Safari, `appearance: auto`
olan bir `<button>` içindeki `display: flex` çocuğun yazısını basmıyor.
Seçildikten sonra görünmesinin sebebi `.secili span`'in vurgulu zemini —
kutu renklenince boşluk fark ediliyordu. Chromium bu çocuğu basıyor, bu
yüzden masaüstünde sorun görünmüyordu.

## Düzeltme: elemanı sıfırla, `<span>`'i bırak

```css
.secenek button.sec {
  appearance: none; -webkit-appearance: none;
  margin: 0; padding: 0; border: 0; background: none;
  font: inherit; color: inherit; text-align: inherit;
}
```

Tek kural. Şablona, Python'a dokunulmadı — **`<button>` olarak kaldı**, yani
tek dokunuşla gönderme davranışı ve JS'siz çalışması korundu. Kullanıcının
istediği "tasarım bütünlüğü" görünüşle ilgiliydi, davranışla değil; davranış
zaten daha iyisiydi.

`appearance: none` satırını kaldırma: yazının iOS'ta görünmesi ona bağlı.

## Aynı hata `esle` ekranında da bekliyordu

Tararken görüldü: `/cycle/{id}/esle` ekranındaki oosit numaraları da
`<button class="onum">` ve `.onum` kendisi `display: flex`. Ölçüldü,
`appearance: auto` — yani **iPhone'da o numaralar da boş kare olarak
çıkabilirdi**. Kullanıcı bunu henüz bildirmedi; kamera eşleştirme ekranı
laboratuvarda telefonla kullanılan bir ekran, beklemeye bırakmanın anlamı yok.
`.onum`'a da aynı satır kondu. Chromium'da görünüm birebir aynı kaldı
(56×56, beyaz, 1px kenarlık) — kural yalnızca tarayıcının kendi biçimini
kapatıyor, zemin/kenarlık/renk zaten CSS'te veriliyordu.

## Test edildi

- Yedi aşama ekranındaki ilk seçim düğmesi ölçüldü: denüdasyon dahil hepsi
  artık `appearance: none`, dış kenarlık 0px, yazı rengi `rgb(23,34,43)` ve
  **span kutuyu tam dolduruyor**. Denüdasyon (`BUTTON`) ötekilerle
  (`LABEL`) birebir aynı.
- Blastokist 46px: o `.secenek.dar` varyantı (satıra dört seçenek),
  bilinçli ölçü — gerileme değil.
- Görsel karşılaştırma: denüdasyonun Sağ/Sol/Belirtme şeridi ile ICSI'nin
  MII/MI/GV şeridi aynı kutu, aynı kenarlık, aynı yazı, aynı yükseklik.
- 39 adres 200, sunucu günlüğünde hata yok, 390px'te yatay taşma yok.
- Yalnızca `static/style.css` değişti. Deneme verisi geri alındı.


---

# v6.57 — aşama ekranları iki sütuna geçti

> **Bu değişiklik v6.59'da geri alındı.** Aşağısı ne denendiğinin ve
> neden olmadığının kaydı; uygulama bugün böyle çalışmıyor.

Kullanıcının isteği: "büyük ekranlı bir monitörde çok fazla boş alan
görünüyor". v6.52'de aşama ekranları **bilerek** dışarıda bırakılmıştı
("kendi düzenleri var: şerit → fotoğraf → kart"). Bu sürüm o kararı gözden
geçiriyor — düzen aynı kalıyor, yalnızca yan yana diziliyor.

## Bölme: solda fotoğraf, sağda form

Fotoğraflı dört ekranda (denüdasyon, fertilizasyon, gün 2/3, blastokist)
sol sütun **fotoğraf + kare şeridi**, sağ sütun **bilgi kartı / form**.
Gerekçe klinik: embriyoya bakarken puanı giriyorsun, aralarında aşağı yukarı
kaydırmıyorsun.

**Numara şeridi sütunların üstünde tam genişlikte** kaldı: o seçici, ekranın
tamamına ait, bir sütuna ait değil.

Androlojide fotoğraf yok; orada bölme **anlamla** yapıldı: solda örneğin
kendisi (alınma + makroskopik), sağda iki mikroskobik analiz. `fotolu`
sınıfı verilmedi, sütunlar eşit.

Denüdasyonda üstteki iki işlem kartı da (denüdasyon saati | oosit ekleme)
kendi satırında yan yana.

## Fotoğraf küçülmesin diye ayrı bir ölçü

Doğrudan `--genis-sutun` (940px) kullanılsaydı ikiye bölünen fotoğraf
446px'e düşerdi — bugünkü 608'den **küçük**. Oysa "fotoğraflar aşama
ekranlarında, tek tek ve **büyük** bakılacak yerde" (v6.20).

`--genis-sutun-asama` 1240px'te duruyor. 1920px'lik bir monitörde:

| ekran | boy önce | boy sonra |
|---|---|---|
| Androloji | 2940 | **2096** (−%29) |
| Denüdasyon | 1856 | **1495** (−%19) |
| Fertilizasyon | 1770 | **1376** (−%22) |
| Gün 2/3 | 1788 | **1383** (−%23) |
| Blastokist | 1964 | **1560** (−%21) |

Fotoğraf 608 → **646px**: sayfa kısaldı *ve* fotoğraf büyüdü.

Sol sütun sağdan geniş (`flex-basis` 460 / 360): fotoğraf tarafı büyük
kalsın, form tarafı v6.52'nin "alan genişledikçe etiketle değer birbirinden
uzaklaşır" sınırında kalsın diye.

**1240'ta durmasının sebebi** formun kendisi: daha genişi form sütununu da
şişirir. Yan menü payı (`100vw - 500px`) burada da var — bu ekranların menüsü
**var**, o yüzden `yanmenusuz` değil yeni `asama` sınıfı.

## 1440px'te bir ödünleşme var

Orada sütun en fazla 940 olabiliyor (yan menüye çarpmasın diye), ikiye
bölününce fotoğraf 608 → **496px** düşüyor. Sayfa yine ~%20 kısalıyor ama
fotoğraf küçülüyor. Kullanıcıya soruldu; 1920'de kazanç net, 1440'ta tercih
meselesi.

1280px ve altında sütunlar kendiliğinden alt alta diziliyor (taban
genişliklerin toplamı sığmıyor) — ama sayfa artık `genis` olduğu için orada
da fotoğraf **748px**, yani eskisinden büyük.

## Tam genişlik kartları şişiriyordu

Denüdasyonun üstündeki "Denüdasyon zamanı" kartı 1206px'e yayılınca
**1178px'lik bir "Düzenle" düğmesi** çıkıyordu. Düzeltildi: o iki kart kendi
`.sutunlar` satırında. Bilgi kipinde oosit ekleme kartı yok — tek kalan sütun
tam genişliğe yayılmasın diye `.sutunlar.ustblok > .sutun:only-child`
620px'te sınırlı. Kural **`.ustblok` ile sınırlı**: `/cryo` gibi tek sütunun
genişlemesi *gereken* yerler etkilenmesin (v6.52).

Sonuç: en geniş düğme 1178 → **590px**.

## Test edildi

- **Telefonda sıra bire bir aynı**: beş ekranda 138 başlık/etiket/düğmenin
  görsel sırası önce ve sonra karşılaştırıldı, beşi de birebir eşleşti.
  Bölme noktaları kaynak sırasında (v6.42 kuralı).
- 2560 / 1920 / 1600 / 1440 / 1280 / 1100 / 900 / 700 / 390px: yan menü
  çakışması yok, yatay taşma yok, kimlik bandı kart sütunuyla hizalı.
- 40 adres 200, sunucu günlüğünde hata yok. Deneme verisi geri alındı.

> Ölçerken görülen, bu sürümün dışında bir şey: **1100px altında kimlik
> bandının hizası zaten kayık** (700px'te −14px, 900px'te dokunulmamış
> ICSI/OPU'da −114px). Band hizası kuralı `@media (min-width: 1100px)`
> içinde, altında yalnızca 16px dolgu var. Eskiden beri böyle; dönüştürülen
> ekranlar 900px'te aksine düzeldi. Kullanıcıya bildirildi.


---

# v6.58 — aşama sütunları eşit genişliğe getirildi

> **Bu değişiklik v6.59'da geri alındı.** Aşağısı ne denendiğinin ve
> neden olmadığının kaydı; uygulama bugün böyle çalışmıyor.

v6.57 kullanıcıya gösterildi ve **beğenilmedi**: "bölümler çok asimetrik,
düzensiz görünüyor, simetrik şekilde yerleşmesi gerekiyor".

## Haklıydı, ve sebebi ikiydi

**1. Sütunları bilerek eşit olmayan yapmıştım** (taban 460 / 360 → 646 / 546).
Gerekçem "fotoğraf büyük kalsın"dı ama sonuç göze düzensiz geliyor. Kaldırıldı:
ikisi de `flex: 1 1 380px`, yani **eşit**.

**2. Sütunların bittiği yer çok farklı.** Ölçüldü:

| ekran | sol | sağ | fark |
|---|---|---|---|
| Androloji | 844 | 1464 | 620px |
| Blastokist | 404 | 924 | 520px |
| Gün 2/3 | 404 | 747 | 343px |
| Fertilizasyon | 404 | 732 | 328px |

Bu **düzeltilemez**, ve bunu bilmek önemli. Androlojinin dört kartı
586/235/877/563px; sırayı bozmadan (v6.42 kuralı) yapılabilecek üç bölme
noktasının verdiği farklar 1089 / **619** / 1135 — yani seçilen zaten en
iyisi. Üstelik fotoğraf geldiğinde sol sütun ~500px büyüyor ve denge
**tersine** dönüyor: bir durum için dengelenen düzen ötekinde bozuluyor.

## Kullanıcı seçti

Üç seçenek ölçülüp ekran görüntüleriyle sunuldu:

- **Tek geniş sütun (940px)** — tam simetrik, fotoğraf 608 → 908px, ama sayfa
  boyu hiç kısalmıyor (2940 / 1770 / 1964 — birebir eski değerler). Formlar
  zaten `.alan ikili` ile iki sütunlu satır kullandığı için genişlik boyu
  kısaltmıyor.
- **İki eşit sütun, boy farkını kabul et** ← **seçilen**
- Eskiye dönmek

Karar kullanıcının: sayfanın kısalması (%20–29) boy farkından önemli.

## Ölçü değişti: her sütun eski tek sütunun genişliğinde

Sütunlar eşitlenince 1240px'te her biri 596px olurdu — fotoğraf bugünkü
608'den **küçük**. Ölçü 1320'ye çıkarıldı; artık her sütun **636px**, yani
projenin bildiği 640px'lik sütunun neredeyse aynısı. Fotoğraf 608 → 636.

Sayı keyfi değil: `2 × sütun + 16px boşluk + 32px kenar dolgusu`.

## Test edildi

- Dokuz genişlikte (2560 → 390) sütunlar **her yerde eşit**; yan menü
  çakışması ve yatay taşma yok.
- 1920px'de: androloji 596→**636**/636, fert/gün2-3/blastokist 636/636.
- Sayfa boyları v6.57'deki gibi: androloji 2096, fert 1366, blastokist 1560
  (eski değerler 2940 / 1770 / 1964).
- 34 adres 200. Deneme verisi geri alındı.

> Ders: bir düzen kararını "daha iyi görünür" diye gerekçelendirip
> asimetri üretme. v6.57'de fotoğrafı büyütmek için sütunları farklı
> genişlikte yaptım; kazanç 38px, bedeli ekranın düzensiz görünmesiydi.
> Simetriyi ölçüyle koru — fotoğraf gerekiyorsa **kabı** genişlet, sütunları
> değil.


---

# v6.59 — aşama ekranları eski haline döndü

Kullanıcı v6.58'i de beğenmedi: "eski halinde kalsın, daha sonra bir şeyler
düşünürüz". Beş ekran (androloji, denüdasyon, fertilizasyon, gün 2/3,
blastokist) v6.56'daki haline döndürüldü — 640px'lik tek sütun.

Geri alınanlar: şablonlardaki `.sutunlar` bölmeleri ve `genis asama` /
`genissayfa asamasayfa` sınıfları, CSS'te `--genis-sutun-asama`,
`.kap.genis.asama`, `.sutunlar.ustblok`, `body.genissayfa.asamasayfa .kimlik`.
`static/style.css` ve beş şablon v6.56 ile **birebir aynı**.

## İki denemeden kalan: ölçüler

Bu ekranların neden bölünmediği artık tahmin değil, ölçülmüş bilgi — sıradaki
denemeye başlamadan önce buraya bakılsın.

**Kart boyları (1920px, androloji):** 586 / 235 / 877 / 563px. Sırayı bozmadan
(v6.42) yapılabilecek üç bölme noktasının verdiği fark: **1089 / 619 / 1135px**.
Yani en iyi bölme bile ~600px ragged bırakıyor. Öteki ekranlarda fark 328–520px.

**Fotoğraf dengeyi tersine çeviriyor.** Deneme verisinde fotoğraf yok; gerçek
fotoğrafla sol sütun ~500px büyüyor ve sağ sütun kısa kalan taraf oluyor. Bir
duruma göre dengelenen düzen ötekinde bozuluyor — statik bir bölme bu ekranlar
için yeterli değil.

**Tek geniş sütun da çözüm değil.** 940px'te denendi ve gösterildi: tam
simetrik, fotoğraf 608 → 908px büyüyor, **ama sayfa boyu birebir aynı kalıyor**
(2940 / 1770 / 1964). Sebebi formların zaten `.alan ikili` ile iki sütunlu
satır kullanması: genişlik artınca satır sayısı değişmiyor, alanlar geniyor.

## Sıradaki deneme için üç yol

Kullanıcı "daha sonra bir şeyler düşünürüz" dedi. Bugünden görünen seçenekler:

1. **Fotoğrafı sabitlemek** (`position: sticky`): tek sütun kalır, form
   kaydırılırken fotoğraf ekranda durur. Simetri bozulmaz, sayfa kısalmaz ama
   kaydırma sorunu çözülür.
2. **Formun içini yeniden düzenlemek**: kartları bölmek yerine kart
   *içindeki* alanları geniş ekranda üçlü/dörtlü satıra çıkarmak. Sayfa
   gerçekten kısalır, sütun bölünmez.
3. **Kabul etmek**: telefon öncelikli bir program büyük monitörde boşluk
   bırakır; klinikte asıl kullanım telefonda.

Hangisi olacağı kullanıcının kararı — ona sorulmadan yeniden bölünmesin.

## Test edildi

- Beş şablon ve `static/style.css` v6.56 ile birebir aynı (`git diff` boş).
- 34 adres 200, sunucu günlüğünde hata yok.
- Deneme verisi geri alındı.

> **Ders.** İki sürüm boyunca "ölçülebilir kazanç" (sayfa %20-29 kısaldı,
> fotoğraf büyüdü) ile "ekran nasıl görünüyor" ayrı şeylermiş gibi davrandım.
> Kullanıcı ikisini birlikte değerlendirdi ve düzeni seçti. Bir düzen
> değişikliğini sayı ile savunmadan önce **görüntüsünü göster ve sor** —
> v6.57'de ekran görüntüsü istenmesinin sebebi buydu, ilk turda anlamadım.


---

# v6.60 — "Gün 2 / 3" aşaması artık "Cleavage"

Kullanıcının kararı (2026-09-12): "sol taraftaki menüde yer alan Gün 2/3
yerine Cleavage olsun, daha doğru olur". Klinik olarak doğrusu bu — o gün
numarası değil, embriyonun **evresi**. Projenin kendi kuralıyla da uyumlu:
klinik terimler iki dilde de İngilizce kalır (blastocyst, ICSI, PN, ICM, TE,
FET). `ornek_adi()` zaten o aşamadaki örneğe "Cleavage" diyordu; aşamanın
adı ondan geri kalmıştı.

## Ad tek yerden geliyor — ama beklenen yerden değil

İlk arama `ASAMA_SIRASI`'ndaki `("cleavage", "Gün 2 / 3", ...)` satırını
gösterdi. **O değil.** Ekrana giden ad `asama_adi(kod)` → `metinler.t("asama_"
+ kod)` üzerinden geliyor; anahtar çalışma anında kurulduğu için düz arama
bulmuyor. `ASAMA_SIRASI`'ndaki Türkçe metin yalnızca kimlik/okunurluk için
duruyor (app.py'deki docstring bunu söylüyor).

Doğru yer: `metinler.py`, `asama_cleavage`. Oradan **üç yüzey birden**
besleniyor — sol menü, cycle ekranındaki aşama düğmeleri, alt gezinme çubuğu.

## Dört yer değişti

| yer | ne besliyor |
|---|---|
| `metinler.asama_cleavage` | sol menü + cycle ekranı düğmeleri + alt gezinme |
| `metinler.olay_cleavage_degerlendirme` | ana ekranda "son işlem" satırı |
| `app.MODULLER` | yetki ekranındaki modül adı, "yetkisiz" mesajı |
| `app.ASAMA_SIRASI` | kimlik/okunurluk (ekrana gitmiyor, tutarlı dursun) |

İlk üçü **ekranda görünüyor**; üçünü birden değiştirmemin sebebi CLAUDE.md'nin
kendi kuralı: "aynı düğmeyi iki isimle öğretmek personeli yanıltır".

## Ekranın kendi başlığı da hizalandı

Değişiklik bir tutarsızlık ortaya çıkardı: menü "Cleavage" derken ekranın
başlığı **"Gün 2 değerlendirme"** idi — aşama adını hiç taşımıyordu. Oysa
kardeş ekran zaten doğru kalıbı kullanıyor: **"Blastokist · Gün 5"**.

`gun_n_degerlendirme` o kalıba çevrildi: **"Cleavage · Gün 2"** /
"Cleavage · Day 2". Gün numarası kayboldu değil — hangi günün
değerlendirildiği gerçek bir bilgi, duruyor.

## Bilerek değişmeyenler

- **Silme ekranı**: "Gün 2 kaydını sil", "Gün 2 değerlendirmesi temizlenecek".
  Orada silinen şey o **günün** kaydı; blastokistin silme ekranı da aynı
  şekilde günle anıyor.
- **Excel sütun başlıkları** (`disari.py`): "Gün 2", "Gün 3", "Gün 2 hücre",
  "Gün 2 simetri"… Bunlar belirli günlerin sütunları, aşama adı değil.
- **`goruntu_asama` seçim listesi** (`gun2`, `gun3` → "Gün 2", "Gün 3"):
  fotoğrafın hangi gün çekildiğini söylüyor, laba özgü ve yönetici
  düzenleyebiliyor.

Kullanıcı isterse bunlar da çevrilir — klinik terim kararı onun.

## Test edildi

- Sol menü okundu: OPU, Androloji, Denüdasyon, ICSI, Fertilizasyon,
  **Cleavage**, Blastokist, Vitrifikasyon, Çözme, Transfer, Gebelik sonucu.
- Altı ekranda "Gün 2 / 3" metni **sıfır** kez geçiyor.
- Başlıklar: "Cleavage · Gün 2", "Cleavage · Gün 3", "Blastokist · Gün 5".
- İki dilde de doğru (İngilizcede de "Cleavage" — klinik terim).
- 31 adres 200, günlükte hata yok. Deneme verisi geri alındı.

---

# v6.61 — şifre değişikliğinde yönetici onayı + tazeleme şeridi düğmeyi kapatmıyor

Kullanıcının iki isteği: "Yeni kullanıcı ekliyemiyorum. Ayrıca şifre değiştirme
işlemlerinde yönetici onayı olsun."

## Şifre değişikliği artık onaya gidiyor

Kullanıcının kararı (2026-09-12): personel kendi şifresini değiştirsin ama
**yönetici onaylayınca** geçsin. `/sifre` ekranının kuralları **değişmedi** —
giriş gerektirmiyor, mevcut şifreyi istiyor, hata mesajı yine tek ve aynı
(README v6.12). Değişen tek şey: kaydetme anında şifre yazılmıyor, istek
kuyruğa giriyor.

- **Yeni tablo `sifre_istegi`** (`goc_030`): kim, hangi hash, hangi durum
  (`bekliyor` / `onaylandi` / `reddedildi`), kim karar verdi ve ne zaman.
- **Bekletilen şey hash, düz şifre değil.** Program şifreleri hiçbir yerde düz
  metin tutmuyor; bu da tutmuyor. Kullanıcı isteği gönderirken kimliğini
  **mevcut şifresiyle** kanıtlıyor, yani bekleyen hash onaylanana kadar hiçbir
  girişte işe yaramıyor — kimlik bilgisi değil, bir teklif.
  - Alternatif "yeni şifreyi onay anında sor" olurdu; o, onayı iki kişinin aynı
    anda aynı yerde olmasına bağlardı. Klinikte olmuyor.
- **Yöneticinin kendi şifresi anında geçer.** Onaylayacak kişi o; kendi isteğini
  onaylamak için giriş yapamaz duruma düşerdi. Tek yönetici varsa bu tam
  kilitlenme demekti — README v6.11'deki korumanın aynısı.
- **Bekleyen istek kullanıcı başına tek.** İkinci istek birincinin yerine
  geçiyor (önce siliniyor, sonra yazılıyor). Yoksa yönetici hangisinin
  sonuncusu olduğunu bilemez ve **eski bir şifreyi** onaylayabilirdi.
- **Onaylamak şifreyi o anda yazar ve o kullanıcının açık oturumlarını
  kapatır** — "şifre değişince oturumlar düşer" kuralı burada da geçerli.
  `sifre_yaz()` çağrılamıyor (o düz şifre bekliyor), o yüzden iki satır elle
  yazıldı; gerekçesi kodun içinde duruyor.
- **Reddetmek hiçbir şeyi değiştirmiyor**, eski şifre kalıyor.
- **Ekran `/sifre-istekleri`, yalnızca yönetici** (`yonetici_kontrol`).
  Rota adları `onayla` / `reddet` — `sil` ile bitse `yol_modulu()` onu "silme"
  modülüne bağlardı ve silme izni olmayan yönetici bu işi yapamazdı
  (v6.40'taki `kaldir`/`gizle` kararının aynısı).
- **Bekleyen istek iki yerde görünüyor**: `/yonetim` panelinde düğme vurgulu ve
  sayıyla, `/kullanicilar`'ın tepesinde uyarı olarak. Onaylanmayan bir şifre
  isteği, "değiştirdim" sanıp giremeyen bir personel demek — saklanacak bir şey
  değil.
- **Göç çalıştırılmamışsa eski davranış**: şifre anında değişiyor
  (`sifre_istegi_tablosu_var()`). Personelin şifre değiştirmesini tümden
  engellemek, onayın çözdüğü sorundan pahalı olurdu (tuzak #3).
- **Kullanıcıya önceden söyleniyor.** `/sifre` ekranı, giriş yapmış ve yönetici
  olmayan kişiye "bu değişiklik yönetici onayı ister" yazıyor; oturum uyarısı
  o durumda basılmıyor, çünkü oturumlar **şimdi** düşmüyor.
  - Giriş yapmamış birine bu not **yazılmıyor**: yazılsaydı "bu kullanıcı adı
    yönetici mi" sorusu ekrandan okunabilirdi. Aynı sebeple hata mesajı da
    tek ve aynı (v6.12).

## "Yeni kullanıcı ekliyemiyorum" — bulunanlar

Bildirilen belirti: sayfa yenileniyor, kullanıcı listede yok, mesaj da yok.
Rota ve şablon satır satır okundu, her ret yolu tarayıcıda 390px'te denendi:
zaten var olan kullanıcı adı, Türkçe karakter, boşluk, tutmayan şifreler —
**dördü de ekranın tepesinde görünür uyarı veriyor**; geçerli bir giriş
kullanıcıyı ekliyor. Yani bildirilen belirti bu yollardan **hiçbirine**
uymuyor. Onun yerine iki şey yapıldı:

- **Sessiz kalabilecek tek yol kapatıldı.** `kullanici_adi` şemada
  laboratuvardan bağımsız olarak `UNIQUE`, ama rotadaki kopya kontrolü
  `lab_id`'ye göre bakıyor. İki lab satırı olan bir veritabanında kontrol
  geçer, `INSERT` patlar ve ekran çıplak bir 500 verirdi. Artık
  `sqlite3.IntegrityError` yakalanıyor ve sebebi ekrana yazılıyor.
- **Her ret ve her ekleme `program.log`'a düşüyor.** Ekranda mesaj
  görünmediğini söyleyen kullanıcının elindeki tek kanıt günlük olur.

## Gerçek bulunan hata: tazeleme şeridi kaydet düğmesinin üstüne düşüyordu

Aramanın yan ürünü, ama aynı belirtiyi veren **ölçülmüş** bir hata. v6.54'ün
"yeni kayıt var" şeridi `position: fixed` ve altta duruyor; `.kap`'ın alt
dolgusu 96px. Şerit 390px genişlikte 65px, ama **320px'te satır sarıyor ve
113px** oluyor — dolguyu aşıyor.

320px'te sekiz ekran tarandı, şerit açıkken hangi düğmenin gerçekten
kapandığına `elementFromPoint` ile bakıldı:

| ekran | şerit altında kalan |
|---|---|
| `/hasta/yeni` | **"Hastayı kaydet"** |
| `/hastalar` | "Cryo haritası" |

Yani telefonda dar ekranda, sayfa sonuna kaydırılmış halde, kullanıcı
"Hastayı kaydet"e basmak isterken şeridin **"Yenile"** düğmesine basıyor:
sayfa yenileniyor, yazdığı gidiyor, hiçbir mesaj çıkmıyor. Bildirilen
belirtinin birebir aynısı.

Düzeltme: şerit görünürken `<body>` `seritli` sınıfını alıyor ve
`body.seritli .kap` alt dolgusu 160px'e çıkıyor. Tek yerde, bütün ekranlar
için. Aynı tarama düzeltmeden sonra tekrar çalıştırıldı: **kapanan düğme yok.**

## Test edildi

- Embriyolog `/sifre`'den şifre değiştirdi → istek kuyruğa girdi, **eski şifre
  hâlâ geçerli**, yeni şifre geçmiyor.
- Yönetici onayladı → yeni şifre geçti, eski geçersiz, o kullanıcının
  oturumları kapandı, istek `onaylandi` olarak kapandı.
- Reddetme → eski şifre kaldı, yeni şifre geçmedi.
- Aynı kullanıcı iki istek gönderdi → bekleyen istek **bir** kaldı.
- Embriyolog `/sifre-istekleri`'ne girmeye çalıştı → `/hastalar`'a döndü;
  `POST .../onayla` da döndü ve **şifre değişmedi** (ekranda gizlemek yetmez).
- Yönetici kendi şifresini değiştirdi → **anında** geçti, `/giris?sifre=1`.
- Giriş yapılmamış `/sifre` ekranında "yönetici onayı" notu **yok**.
- Tazeleme şeridi: sayfa kirliyken şerit çıkıyor, `body.seritli` geliyor,
  dolgu 160px, forma yazılan değer **yerinde duruyor**, JS hatası yok.
- Göç açılışta kendiliğinden uygulandı (`GOC: 1 goc uygulandi (goc_030)`).
  Deneme kullanıcıları ve istekleri geri alındı.

---

# v6.62 — yeni tedavi tipi: FET (3→5 kültür)

Kullanıcının isteği (2026-09-12): "FET tedavilerinde bazen 2 veya 3. gün
embriyosu çözülüp 5. güne kadar kültür edilip 5. gün transfer yapılıyor.
Bazen de 2 veya 3. gün çözülen embriyo aynı gün transfer ediliyor." Mevcut
`fet` tipi ikinci senaryoyu (doğrudan transfer) karşılıyordu; birincisi için
araya blastokist değerlendirmesi giren ayrı bir tip gerekti: **`fet_kultur`**.
Seçildiğinde sol menüde **Çözme → Blastokist → Transfer → Gebelik sonucu**
görünür.

## Şema ve seçim listesi

`cycle.cycle_tipi` kolonundaki CHECK kısıtı yalnızca `ivf_icsi`/`fet`/
`oosit_cryo` kabul ediyordu. `goc_031` bunu goc_016/017'deki aynı yöntemle
genişletti (SQLite CHECK değiştirilemiyor, tablo yeniden kuruldu) ve
`liste_degeri`'ne `fet_kultur` satırını ekledi. **Kod değiştirmeden** yeni
tip seçilebilir oldu — `/hasta/{id}/cycle/yeni` dropdown'ı `db.liste
("cycle_tipi")`'den besleniyor.

## Aşama sırası ASAMA_SIRASI'nın sırası değil, TIP_ASAMALARI'nın kendi sırası

Bu, bu sürümün en can alıcı kararı. `cycle_asamalari()` eskiden
`ASAMA_SIRASI`'nı **filtreleyip** o listenin sırasını kullanıyordu; her tipin
kendi listesi (`TIP_ASAMALARI[tip]`) sadece "hangileri" sorusunu
yanıtlıyordu, sırayı değil. `ivf_icsi`/`fet`/`oosit_cryo`'da bu ikisi zaten
aynı sonucu veriyordu ama `fet_kultur`'da vermiyor: `ASAMA_SIRASI`'nda
`blast` dondurmadan (`vitrifikasyon`/`thaw`) **önce** duruyor -- çünkü
`ivf_icsi` akışında blastokist önce değerlendirilir, sonra dondurulur.
`fet_kultur`'da ise embriyo **önce** çözülüyor, **sonra** gün 5'e
kültürleniyor -- sıra ters. Eski koddan gitseydi ekranda Blastokist, Çözme'den
**önce** çıkardı; klinik akışın tam tersi.

Çözüm: `cycle_asamalari()` artık `TIP_ASAMALARI[tip]` listesinin **kendi
sırasını** kullanıyor, `ASAMA_SIRASI` yalnızca "bu kod neye karşılık geliyor"
sözlüğü olarak kalıyor. Üç eski tip için sonuç bire bir aynı (listeleri
zaten `ASAMA_SIRASI` sırasıyla yazılmıştı); değişen yalnızca `fet_kultur`.

## Embriyo başka bir cycle'dan geliyor -- `FET_TIPLERI`

`fet`'in kendi kuralı ("dondurulan embriyo başka bir cycle'dan gelir,
taşıyıcılar hastanın tüm cycle'larından listelenir") `fet_kultur`'a da
uygulandı. Tek tek `== "fet"` yerine artık **`FET_TIPLERI = ("fet",
"fet_kultur")`** ve Jinja'ya açılan `fet_tipi_mi(cycle_tipi)`:

- `/cycle/{id}/thaw` -- taşıyıcı listesi ve ipucu metinleri.
- `cycle_thaw.html` -- "Vitrifikasyon ekranı" bağlantısı gizleniyor (bu
  cycle'da dondurma yok, embriyo zaten başka yerde dondurulmuş).

## Blastokist ekranı: embriyo BU cycle'a değil, thaw_cycle_id'ye göre bulunuyor

`blast_durum()` eskiden `specimen.cycle_id = ?` ile arıyordu -- ivf_icsi'de
doğru (embriyo hep kendi cycle'ında), ama `fet_kultur`'da **hiçbir zaman**
doğru değil: `specimen.cycle_id` hâlâ embriyonun **ilk** (OPU/ICSI) cycle'ını
gösterir, hiç değişmez (README v6.7, v6.35 -- "embriyo cycle değiştirmez").
Ekran bomboş görünürdü.

Yeni `_blast_kosul(cycle_tipi)`: `FET_TIPLERI`'nde ise embriyoyu **hangi
tedavi için çözüldüğünü tutan `olay.thaw_cycle_id`** ile buluyor -- `/thaw`
ekranının zaten kullandığı mantığın aynısı. `blast_ekran` ve `blast_kaydet`
artık `c["cycle_tipi"]`'yi bu sorguya geçiyor.

## Bu işin en pahalı hatası: `cycle_sira_no` iki cycle'da da "1." olabilir

Blastokist, ICSI, fert, cleavage ekranlarının hepsi seçimi adresten
`?oosit=<cycle_sira_no>` ile yapıyor (README v6.35) -- bu güvenli, **çünkü**
o alan `UNIQUE(cycle_id, cycle_sira_no)`: tek cycle içinde tekil.
`fet_kultur`'da blastokist ekranı **birden fazla cycle'ın** embriyolarını
aynı listede gösterebiliyor (biri Cycle #3'ün "1. embriyo"su, öteki Cycle
#5'in "1. embriyo"su) ve `cycle_sira_no` orada tekil DEĞİL. Eski koddan
gitseydi ikinci embriyonun linkine basmak **ilk eşleşeni** (yanlış embriyoyu)
seçerdi -- bu işin en pahalı hatası, sessizce.

Test edildi: aynı sırayla (`cycle_sira_no=1`) iki ayrı cycle'dan iki embriyo
aynı `fet_kultur` cycle'ına çözüldü; blastokist ekranında ikisi de doğru
kodlarıyla (`527078-2026-0001-01` / `527078-2026-0003-01`) ayrı ayrı
seçilebiliyor.

Düzeltme **blastokist ekranına özel**: seçim artık `specimen.id`
(globalde tekil) ile yapılıyor, `cycle_sira_no` ile **değil**. Değişen dört
yer: sayı şeridinin linki, "kaydet → sıradaki" yönlendirmesi, fotoğraf
ekleme/silme dönüşleri, blast-sil ekranı. Görünen numara (`o.cycle_sira_no`,
şeritteki küçük etiket) **değişmedi** -- o klinik bir gösterim, seçim
mekanizması değil. ICSI/fert/cleavage'a dokunulmadı: onlar hiçbir zaman
birden fazla cycle'ın embriyosunu aynı ekranda göstermiyor.

`blast_kaydet`'teki "kaydet → sıradaki oosit" sorgusu da aynı sebeple
yeniden yazıldı: `cycle_sira_no > ?` karşılaştırması yerine `blast_durum()`
listesinde şimdiki embriyonun **konumundan** ilerleyip kaydı olmayan
sıradakini buluyor -- iki cycle'ın numaraları çakışsa da doğru ilerliyor.

## `olay.cycle_id` her zaman specimen'in KENDİ cycle'ı, ekranın cycle'ı değil

Blastokist kaydı artık `_gun_olay_kaydet(specimen_id, sp["cycle_id"], ...)`
ile yazılıyor -- ekranın `cycle_id`'siyle **değil**. Bu, `thaw` ve `transfer`
olaylarının zaten yaptığı şeyin aynısı (`e["cycle_id"]` / `sp["cycle_id"]`):
"hangi tedavi için" sorusu ayrı bir alanda tutulur (`thaw_cycle_id`,
`tr_cycle_id`), `olay.cycle_id` hep embriyonun kendi kökenini gösterir. İki
kod yolunu birbirinden farklı davransın diye ayırmak yerine tek kurala
uyduruldu -- ivf_icsi'de ikisi zaten aynı olduğu için görünürde bir şey
değişmedi.

## Fotoğraf ekleme de embriyonun KENDİ cycle'ına arşivleniyor

`blast.html`'deki "Fotoğraf ekle" bağlantısı `/cycle/{{ c.id }}/foto-ekle`
yerine `/cycle/{{ sp.cycle_id }}/foto-ekle` oldu -- `thaw.html`'in ve
`snapshot_al()`'ın (kamera kuyruğu) zaten izlediği kural: görüntü
`arsiv/<dosya_no>/<cycle_no>/` altına, embriyonun **tüm** fotoğraflarının
zaten durduğu klasöre gidiyor; `fet_kultur` cycle'ının kendi klasörüne değil.
İki klasöre bölünmüş bir embriyo geçmişi olmasın diye. Geri dönüş adresi
(`geri=`) hâlâ görüntülenen `fet_kultur` ekranına -- o ayrı bir soru.

## İki yerden gelinen ekranın geri oku: blast-sil

`/specimen/{id}/blast-sil` her zaman `sp.cycle_id`'ye (embriyonun kendi
cycle'ı) dönüyordu. `fet_kultur`'da bu **yanlış** cycle'a dönmek demek --
kullanıcı `fet_kultur` cycle'ının blastokist ekranındayken silme yapıp
embriyonun **ilk** cycle'ına (görmek istemediği, tümüyle başka bir ekrana)
fırlatılırdı. `?cycle=` deseni eklendi (taşıyıcı ekranındaki
aynı desen, README v6.32): adres ve gizli form alanı hangi ekrandan
gelindiğini taşıyor, adres bir şey söylemezse embriyonun kendi cycle'ına
dönülüyor (ivf_icsi'de zaten aynı).

## Test edildi

- Dropdown'da "FET (3→5 kültür)" görünüyor, seçilince kayıt geçiyor.
- Yeni cycle'ın menüsü: Çözme → Blastokist → Transfer → Gebelik sonucu (bu
  sırayla, kaynak kodda da bu sırayla).
- `ivf_icsi` cycle'ın menüsü **değişmedi** (11 aşama, aynı sıra).
- İki farklı `ivf_icsi` cycle'dan (her ikisinde de "1. embriyo") dondurulmuş
  embriyolar aynı `fet_kultur` cycle'ına çözüldü:
  - `/cycle/{id}/thaw` ikisinin taşıyıcısını da hastanın tüm cycle'larından
    listeledi; "Vitrifikasyon ekranı" bağlantısı yok.
  - `/cycle/{id}/blast` ikisini de gösterdi, ikisi de **doğru** örnek koduyla
    ayrı ayrı seçilebildi (`cycle_sira_no` çakışmasına rağmen).
  - Birini kaydettikten sonra "kaydet" ötekine **doğru** ilerledi.
  - `olay.blastokist_degerlendirme.cycle_id` her ikisinde de embriyonun
    **kendi** cycle'ı (fet_kultur cycle'ı değil).
  - `/specimen/{id}/blast-sil?cycle=<fet_kultur>` doğru cycle'a geri döndü.
  - `/cycle/{id}/transfer` ikisini de aday olarak gösterdi, transfer
    kaydedildi; `tr_cycle_id` fet_kultur cycle'ı, `cycle_id` embriyonun
    kendisi.
  - `/cycle/{id}/gebelik` ikisini de "Bu cycle'da transfer edilen" altında
    listeledi, kaynak cycle numarasıyla ayırt edilebilir durumda.
- 17 adres tarandı, hepsi 200; günlükte hata yok.
- Deneme cycle'ları, taşıyıcıları, oturumu ve bir eski deneme oturumundan
  kalmış kırık `kaynak_dosya` referansı geri alındı; `PRAGMA
  foreign_key_check` temiz.

---

# v6.63 — Hasta kayıtları: Tüm Hastalar sütunu, "Hasta kartı"

Kullanıcının gözlemi (2026-09-16): **"hasta kayıtları ve takvim sanki aynı
şey gibi."** İkisi de aynı ay/yıl gezinme kutusunu ve aynı satır tasarımını
kullanıyordu (bilerek — v6.30'da "aynı düzeni iki ekranda iki türlü öğretmek
personeli yorar" diye) ve bir cycle'ın hem OPU tarihi hem planlanan tarihi
aynı aya denk gelirse **aynı cycle iki ekranda birden** görünebiliyordu.

Soruldu, kullanıcı takvime dokunmadı; bunun yerine hasta kayıtları
ekranının kendisini netleştirdi: **"Şöyle yapalım hasta kayıtları bölümü
olsun bir tek. Orada ay ay hastalar görünsün. Ayrıca orada sayfaya
sığacak şekilde yan tarafında tüm hastalar diye bir modül olsun... Hasta
ismine tıklandığında hasta kartı açılsın... hasta kaydı yazan butonunun
ismi hasta kartı olarak değişsin."**

## Arama artık ay görünümünü kapatmıyor

**Bu, v6.29'dan beri süregelen bir davranışın tersine çevrilmesi.** Eskiden
`/hastalar` iki **ayrı mod**du: arama boşken ay listesi, doluyken **onun
yerine** hasta arama sonuçları — ikisi asla birlikte görünmezdi. Kullanıcının
isteği bu ayrımı kaldırdı: şimdi ay listesi **solda**, hep görünür; sağda
**Tüm Hastalar** — arama boşken aktif hastaların tamamı alfabetik, doluyken
aynı sütun arama sonucuna dönüşür. İkisi **aynı anda** ekranda.

- **İki sütun, `.sutunlar`/`.sutun`** (v6.42'nin deseni). `/hastalar`
  CLAUDE.md'de "yalnızca genişleyen" (bölünmeyen) ekranlar arasında
  sayılıyordu — o kural `_cyclesatir` satırlarının soldan sağa okunan **tek
  bir akış** olduğu, bölmenin o akışı kestiği durumlar için. Burada
  bölünen şey bir liste değil: ay listesi ile Tüm Hastalar **birbirinden
  bağımsız iki kart** — v6.52'nin ölçüsü ("ekranda birbirinden bağımsız
  kartlar mı var") tam bunu destekliyor. `/hastalar` artık iki sütun
  kategorisinde.
- **Ay/yıl seçimi ve arama terimi birbirini geçirmiyor.** Ay değiştirirken
  arama terimi (`aygezgin` formunda gizli `ara` alanı ve ok linklerinde
  `&ara=...`) korunuyor; arama yaparken görüntülenen ay (`arama` formunda
  gizli `yil`/`ay` alanları) korunuyor. Biri ötekini sıfırlamasın diye.
- **Arşiv hâlâ ayrı, tam genişlik bir mod** — dokunulmadı. "Bu dosya
  kapandı" demek, günlük ay/Tüm Hastalar akışının parçası değil.
- **Geri oku basitleşti**: artık yalnızca arşiv ayrı bir "nereden geldim"
  sorusu soruyor (`arsiv ise /hastalar, değilse /`). Arama tam sayfa mod
  olmaktan çıkınca "arama sonucundan çıkma" diye ayrı bir geri hedefi
  gerekmedi.

## Tüm Hastalar

Yeni sorgu: `durum='aktif'` hastaların tamamı, `ORDER BY ad_soyad` —
alfabetik. Sınırsız (var olan "son 50" sınırı yalnızca arşiv-arama-boş
durumunda kalıyor, kullanıcı açıkça "tüm hastalar" istedi). Satır tasarımı
arama sonucuyla aynı (dosya no, ad, eş, cycle sayısı) — aynı bilgiyi iki
farklı görünümde iki türlü göstermemek için.

**İsme tıklamak `/hasta/{id}`'yi açıyor** — zaten var olan sayfa,
değişmedi. Değişen, oraya giden ikinci bir yol: eskiden yalnızca ay
listesindeki "Hasta kaydı" düğmesinden ya da arama sonucundan gidilirdi,
şimdi Tüm Hastalar'daki her satır da doğrudan oraya gidiyor.

## "Hasta kaydı" → "Hasta kartı"

Tek bir metin anahtarı (`hasta_kaydi`), tek kullanım yeri
(`_cyclesatir.html`'in "ay" kipindeki düğme). Kullanıcının kararı: sayfanın
adı zaten "hasta kaydı" — aynı kelimeyi bir de düğmede kullanmak neyin
nereye gittiğini belirsizleştiriyordu. "Hasta kartı" o kişinin **tüm
geçmişine** giden, tek bir kaydı değil bütün dosyayı temsil eden sayfayı
daha iyi anlatıyor. `/hasta/{id}` ekranının kendi başlığı zaten sade
"Hasta" — çakışma yok.

## Test edildi

- Geniş ekran ve 390px'te ekran görüntüsü alındı: sol ay listesi, sağ Tüm
  Hastalar (alfabetik: Ahmet Yıldız, Merve Kaya, Test Hasta, Zeynep
  Aydın), arama kutusu üstte. Telefonda kaynak sırasıyla alt alta diziliyor.
- Arama ("Ahmet") → sağ sütun sonuca döndü, **sol sütun (ay listesi)
  değişmedi**. "Aramayı temizle" görüntülenen ayı koruyarak döndü.
- Örnek kodu araması (`527078-2026-0001-01`) → doğru satırı buldu; eşleşen
  hasta yoksa "Arama sonucu" kartı basılmadı (mevcut "gölgeleme" davranışı
  korundu).
- Arşiv modu (`?arsiv=1`) tam genişlikte, tek sütun, değişmeden çalışıyor.
- `_cyclesatir.html`'in "ay" kipindeki düğme artık "Hasta kartı" yazıyor;
  `/hasta/{id}`'ye gidiyor.
- Deneme hastaları ve oturum geri alındı; `PRAGMA foreign_key_check` temiz.

---

# v6.64 — hasta kartında doğum tarihi gün.ay.yıl

Kullanıcının isteği: "hasta kartında doğum tarihi gün ay yıl şeklinde
olsun." `hasta.dogum_tarihi` veritabanında ISO (`YYYY-MM-DD`) duruyor ve
öyle kalıyor — kaydetme, arama, sıralama hep ISO'ya güveniyor. Ekranda
`/hasta/{id}` (hasta kartı) tek yerde **ham ISO'yu** basıyordu
(`hasta_detay.html`), tarih girişleri (`<input type="date">`) zaten
tarayıcının kendi yerel biçiminde gösteriyor.

Yeni Jinja global `gg_aa_yyyy(tarih)`: `'1990-05-12'` → `'12.05.1990'`.
`takvim_basligi()`'nin kullandığı `_dt.fromisoformat` deseninin aynısı —
bozuk/boş değerde olduğu gibi döner, sessizce boş basmaz. `%d.%m.%Y`
sayısal — `%B`/`%A` gibi işletim sisteminin yerel ayarına bağlı değil,
projede yasak olan o değil.

Kapsam yalnızca `hasta_detay.html`'deki doğum tarihi satırı — cycle
listesindeki OPU/işlem tarihleri (`[:10]` ISO) ve Excel çıktısındaki
`dogum_tarihi` (ISO kalmalı ki Excel kendi tarih hücresi olarak tanısın)
dışarıda; kullanıcı yalnızca hasta kartındaki doğum tarihini sordu.

## Test edildi

- `/hasta/{id}`'de doğum tarihi `12.05.1990` olarak görünüyor, eski ISO
  biçimi ekranda yok.
- Boş/`None`/bozuk değerlerle `gg_aa_yyyy()` çökmedi, olduğu gibi döndü.

---

# v6.65 — ana menü her ekranda solda, giriş ekranına tanıtım, Takvim kaldırıldı

Kullanıcının istekleri, tek istekte dört parça:

1. "Şifre girilen ana ekranda program ile ilgili bir yazı olsun."
2. "Ana ekranda yapılacaklar yerine Devam Eden Tedaviler yazsın."
3. "Ana sayfada arama olsun."
4. "Soldaki menü ... cycle ekranları hariç hep solda olsun. Ayrıca takvim
   ortadan kalksın."

## Ana menü artık global

**En büyük değişiklik.** `yan_ana()` (Hasta kayıtları / Cryo haritası /
Yönetici bağlantılarını taşıyan sol menü) eskiden yalnızca `/` (ana ekran)
tarafından çağrılıyordu — başka hiçbir ekranda görünmüyordu. Kullanıcının
isteğiyle artık **cycle ekranları hariç her ekranda** solda:

- `base.html`'de yeni `{% block yanmenu %}` — `.ust` bandının hemen altında,
  varsayılanı `gz.yan_ana(...)`. Bunu **tek yerde** eklemek, her yeni ekranın
  bunu kendi başına çağırmasına gerek bırakmıyor (tuzak #1'in tersi: burada
  merkezi durması bilinçli).
- **Cycle ekranları (OPU, androloji, ..., cycle_detay, cycle_thaw) bu bloğu
  boş bırakıyor** (`{% block yanmenu %}{% endblock %}`) — onlar zaten kendi
  aşama menülerini (`gez.cubuk`/`gez.yan`) gösteriyor; ikisi üst üste binmesin
  diye. 12 şablona tek satır eklendi.
- **`aktif` vurgusu adresten türetiliyor** (`base.html`'de kaba bir
  `startswith` eşlemesi: `/hastalar` ve `/hasta/...` → "hastalar", `/cryo` →
  "cryo", `/yonetim`/`/kullanici...`/`/sifre-istekleri`/`/istatistik`/
  `/klasorler`/`/dil`/`/formlar` → "yonetim"). Kapsamadığı bir adres varsa
  yalnızca vurgu kaçar, işlev bozulmaz — riski düşük tutuldu.
- **Genişleyen ekranlar `yanmenusuz`'dan `genis`'e geçti.** `/hastalar`,
  `/yonetim`, `/kullanicilar`, `/istatistik`, `/klasorler`, `/cryo`,
  `/bitenler`, `/hasta/{id}`, `/formlar`, `/baglan`, `/sifre-istekleri` —
  hepsi eskiden menüsüz olduğu için `--genis-sutun-menusuz` (940px, menü
  payı yok) kullanıyordu. Menü artık orada da olduğu için `--genis-sutun`
  (menü payını içeren ölçü) kullanmaları gerekiyordu — yoksa 1100-1440px
  arası içerik menünün altına girerdi. `/hasta/{id}` ve `/sifre-istekleri`
  kimlik bandı hizalamasını da aynı sebeple `menusuzsayfa`'dan çıkardı.
- **Dar (`.kap`, 640px) ekranlara dokunulmadı** — 1100px eşiği zaten
  `(1100-640)/2 = 230px > 216px` (menünün bittiği yer) ile kurulmuştu, menü
  hep vardı gibi çalışıyordu.
- Test edildi: 1400px'te dört ekranın ekran görüntüsü alındı (çakışma yok,
  doğru öğe vurgulu), 1130px'te (eşiğin hemen üstü) hâlâ çakışma yok, 390px'te
  menü CSS ile gizli (telefonun kendi düğme yığını hâlâ yalnızca ana ekranda).

## Takvim kaldırıldı

`/takvim` rotası ve `takvim.html` silindi; sol menüdeki ve telefon düğme
yığınındaki bağlantı kaldırıldı. **"Yaklaşanlar" kartı kalıyor** — kullanıcı
onu kaldırmadı, yalnızca artık gitmediği "Tümü → Takvim" bağlantısı
kaldırıldı; kart kendi 14 günlük penceresini gösteriyor.

- `cycle_listesi(plan_ay=...)` kod yolu **bilerek dokunulmadan bırakıldı** —
  artık çağıran yok ama `yaklasan` moduyla iç içe geçmiş, ayıklaması riskli;
  ölü kod olduğu docstring'e yazıldı.
- `takvim_basligi()` **kalıyor** — `/takvim`'e özel değildi, `cycle_detay.html`
  planlanan tarihi göstermek için hâlâ kullanıyor.

## Ana ekran: "Devam Eden Tedaviler", arama, giriş ekranı tanıtımı

- `"yapilacaklar"` metin anahtarının **değeri** "Yapılacaklar" →
  "Devam Eden Tedaviler" oldu (anahtar adı aynı kaldı, tek kullanım yeri
  `ana.html`).
- Ana ekrana arama kutusu eklendi — **ayrı bir arama mantığı yazılmadı**,
  form `/hastalar`'a gidiyor ve v6.63'te zaten kurulan Tüm Hastalar/arama
  sütununu kullanıyor.
- `/giris` ekranına yeni `giris_aciklama` metniyle kısa bir tanıtım
  eklendi: "IVF laboratuvarının hasta, cycle ve oosit kayıtlarını tuttuğu
  program..."

## Test edildi

- 30'a yakın adres tarandı (ana ekran, hasta kayıtları, tüm cycle
  ekranları, yönetici ekranları, `/takvim` dahil) — `/takvim` 404,
  gerisi 200/303, günlükte hata yok.
- Cycle ekranında `.yanmenu` **tek** (aşama menüsü), ana menü orada
  basılmıyor. Cycle-dışı ekranlarda `.yanmenu` **tek** (ana menü), doğru
  öğe vurgulu.
- Deneme oturumu geri alındı.

# v6.66 — ana ekran kart başlıkları, şifre ekranında program adı

Kullanıcının isteği: ana ekrandaki iki kart başlığı daha açık olsun, ve
`/sifre` ekranı hangi programda olunduğunu göstersin.

- `"bugun_bitenler"` metin anahtarının **değeri** "Bugün bitenler" →
  "Bugün Biten Tedaviler" oldu.
- `"yaklasanlar"` metin anahtarının **değeri** "Yaklaşanlar" →
  "Yaklaşan Tedaviler" oldu.
  İkisinde de yalnızca değer değişti, anahtar adı aynı kaldı — `"yapilacaklar"`
  (v6.65) ile aynı desen. Tek kullanım yerleri `ana.html`, grep ile doğrulandı.
- `/sifre` ekranına, `/giris`'teki tanıtım metninin üstüne konduğu yere
  benzer şekilde (v6.65), `{{ metin("program_adi") }}` eklendi — "Patient
  Data Center". Yeni bir metin anahtarı gerekmedi, `program_adi` zaten bu
  değeri taşıyordu (başlıkta ve manifest'te kullanılan aynı anahtar).
  Ekran hem giriş yapılmadan (`/giris` üzerinden) hem giriş yapılmış halde
  (`/sifre-degistir` bağlantısından) açıldığı için metin ikisinde de basılıyor.

## Test edildi

- Ana ekranda iki başlık, `/sifre` ekranında (giriş yapılmış ve yapılmamış
  halde) "Patient Data Center" metni doğrulandı — hem `curl` ile hem
  telefon genişliğinde (390px) ekran görüntüsüyle.
- Deneme oturumu geri alındı.

# v6.67 — ekrandaki tarihler gün.ay.yıl, ana ekranda üç sütun, arama küçüldü

Kullanıcının üç isteği: (1) ekrandaki bütün tarihler gün.ay.yıl sırasıyla
görünsün — v6.64'te yalnızca hasta kartındaki doğum tarihi düzeltilmişti,
geri kalan ekranlarda hâlâ ham ISO (`2026-09-04`) görünüyordu; (2) ana
ekrandaki üç kart (Devam Eden Tedaviler / Bugün Biten Tedaviler / Yaklaşan
Tedaviler) yan yana sığsın — v6.34'te ilk ikisi yan yana, üçüncüsü altındaydı;
(3) ana ekrandaki arama kutusu küçük olsun, satırı boydan boya kaplamasın.

## Tarihler

- Yeni Jinja global **`gg_aa_yyyy_saat(zaman)`**: `'2026-09-16 08:23:11'` →
  `'16.09.2026 08:23'`. `gg_aa_yyyy()` ile aynı gerekçe (v6.64) — yalnızca
  saat de taşıyan kayıtlar için (saniye basılmıyor, kalabalık ediyordu).
- Ekrana ham `[:10]` dilimiyle ISO tarih basan yerler `gg_aa_yyyy()`'ye
  çevrildi: `hasta_detay.html` (cycle satırındaki OPU tarihi),
  `androloji.html` (sperm örneği alınma tarihi), `_cyclesatir.html` (üç
  yerde — bitiş, OPU, kayıt tarihi; ana ekran/hasta kayıtları/bitenler hepsi
  buradan besleniyor), `cycle_detay.html` (bitiş kartı), `lab_formlari.html`
  (form yükleme tarihi).
- Saat de taşıyan ham zamanlar `gg_aa_yyyy_saat()`'e çevrildi: `gebelik.html`
  (son güncelleme), `sifre_istekleri.html` (istek zamanı), `tasiyici.html`
  (vitrifikasyon zamanı), `gecmis.html` (değişiklik geçmişi satırları),
  `yedek_durumu()` (`/yonetim`'deki "Son yedek ... alındı" uyarısı — bu
  mesaj `metinler.py`'den bile geçmiyordu, sunucuda elle kurulan bir
  f-string'di, yine de düzeltildi).
- **Dokunulmayanlar, bilerek**: `type="date"`/`type="datetime-local"` form
  alanlarının `value`'su ISO kalıyor — tarayıcı zaten kendi yerel biçiminde
  gösteriyor, değeri ISO olmayan bir şeye çevirmek input'u bozardı.
  `cycle_detay.html`'deki `planlanan_tarih[:10] > bugun` karşılaştırması da
  dokunulmadı — o bir görüntüleme değil, sıralama/karşılaştırma. Resmî form
  çıktılarındaki (`formlar.py`, DH.FR.91/107) tarih hücreleri de
  dokunulmadı: kâğıt aslının birebir kopyası, formatı kalite sisteminden
  geliyor — "kalıba dokunma" kuralı burada da geçerli.
- `CLAUDE.md`'ye tek bir kural olarak yazıldı: yeni bir tarih/zaman alanı
  ekranda görünecekse `gg_aa_yyyy()`/`gg_aa_yyyy_saat()`'ten birini çağır,
  `[:10]` dilimleme.

## Ana ekran: üç sütun, küçük arama

- `.ikisutun` → **`.ucsutun`**. Artık üç kart da aynı flex sarmalayıcıda.
  **Medya sorgusu yok**: her kart `flex: 1 1 260px` — sığan kadarı aynı
  satırda kalıyor, gerisi alt satıra sarıyor. Bu, aşama ekranlarının
  denenip vazgeçilen sabit-kırılma-noktalı iki sütununun (README v6.57–59)
  tam tersi bir çözüm ama kart içerikleri (kısa liste satırları, hepsi aynı
  genişlikte) orada asimetrik olan şeyi burada sorun etmiyor — kartlar zaten
  farklı boyda olabiliyordu (v6.34'ten beri), üçüncüsü de aynı satıra
  girince görünüm bozulmadı.
  1400px, 900px, 700px ve 390px'te ekran görüntüsüyle doğrulandı: geniş
  ekranda üçü yan yana, ~700px'te iki + biri alt satırda, telefonda tek
  sütun — sıra hep aynı.
- Arama kutusuna `.arama.kucuk` (`max-width: 280px`) eklendi. **Yalnızca
  ana ekranın** arama formu bu sınıfı alıyor — `/hastalar` ve `/cryo`'daki
  aramalar dokunulmadı, onlar sonuç listesine giriş olduğu için geniş
  kalmalı.

## Test edildi

- `curl` ile: hasta kartında "OPU 09.09.2026", değişiklik geçmişinde
  "09.09.2026 17:04", `/yonetim`'de "Son yedek ... (12.09.2026 11:14)
  alındı" doğrulandı.
- Androloji ve cycle ekranı 200 döndü (sperm örneği/taşıyıcı test verisi
  yoktu, şablon hatası olup olmadığı bu şekilde kontrol edildi).
- `PRAGMA foreign_key_check` temiz. Deneme oturumu geri alındı.

# v6.68 — üç sütun 24" ekranda yan yana durmuyordu (v6.67'nin düzeltmesi)

Kullanıcı v6.67'nin üç sütununu 24" ekranında test etti: **yan yana durmadılar**.
Sebep hesap hatasıydı, hemen bulundu.

- Ana ekranın genişliği `--genis-sutun` ile veriliyor:
  `max(640px, min(940px, calc(100vw - 500px)))` — yan menüye pay ayırdığı için
  **640px'e kadar daralabiliyor**, yalnızca `100vw ≥ 1440px` olunca 940px'lik
  tavana çıkıyor (v6.42'den beri böyle, `.kap.genis` ve kimlik bandı hep bunu
  kullanıyor).
- v6.67'de kartlara verilen `flex: 1 1 260px` en az `3×260 + 2×16 = 812px`
  istiyordu. **812px, 640-1350px arası viewport genişliklerinin hiçbirine
  sığmıyordu** — yani tarayıcı penceresi ~1100-1350px olan (çoğu 24" monitörde
  gerçekçi bir pencere/ölçekleme durumu) her kullanıcıda kartlar sarıp alt
  satıra düşüyordu. Yalnızca pencere ~1440px'i geçince (tam ekran geniş
  monitör) yan yana duruyorlardı — v6.67'de test ederken kullanılan genişlikler
  (1400, 900, 700, 390) bu dar-orta aralığı hiç yoklamamıştı, kusur öyle
  kaçtı.
- **Düzeltme**: kart basisi 260px → **190px**. Taban ihtiyaç artık
  `3×190 + 2×16 = 602px` — `--genis-sutun`'un garantili **en dar** hali olan
  640px'in bile içinde kalıyor, yani üç kart artık **her** genişlikte
  (≥1100px, yan menünün göründüğü eşik) yan yana duruyor; pencere daraldıkça
  yalnızca kart içindeki metinler sarıyor, sütun sayısı değişmiyor.

## Test edildi

- 1100, 1200, 1280, 1366, 1536, 1920px genişliklerinde ekran görüntüsü —
  hepsinde üç kart yan yana. 1100px'te (en dar "geniş ekran" eşiği) "Bugün
  Biten Tedaviler" başlığı iki satıra sarıyor ama sütun düzeni bozulmuyor.
  v6.67'nin testinde atlanan tam bu ara genişlik aralığı hedeflendi.
- Deneme oturumu geri alındı.

# v6.69 — style.css tarayıcı önbelleğinde takılı kalıyordu

Kullanıcı v6.68'i **doğru makinede, doğru commit'te** çalıştırıyordu
(`git log` ile doğrulandı) ama üç sütun hâlâ görünmüyordu. Teşhis iki adımda:
`/static/style.css`'i doğrudan açtırdım — içinde `ucsutun` **yoktu** — ama
sayfanın kaynağında (View Page Source) **vardı**. Yani sunucu güncel HTML'i
basıyordu, tarayıcı ise `style.css`'i eski haliyle önbellekten okuyordu.

- **Sebep**: `base.html` `style.css`'i hep aynı adresten çağırıyordu
  (`/static/style.css`, sürüm numarasız). Dosya güncellendiğinde adres
  değişmediği için tarayıcının "bunu yeniden indirmem gerekir" diye
  düşünmesi için hiçbir sebep yok — normal yenileme (F5) sırasında CSS'i
  önbellekten kullanmaya devam ediyordu. Sert yenile (Ctrl+Shift+R) bunu
  düzeltirdi ama **kullanıcıdan her güncellemede bunu hatırlamasını
  istemek** kırılgan bir çözüm; 22 yıllık embriyolog, tarayıcı önbelleği
  kavramıyla uğraşmak istemiyor.
- **Çözüm**: yeni Jinja global `statik_surum()` — `style.css`'in dosya
  sistemindeki **son değişim zamanını** (`st_mtime`) okuyup döndürüyor.
  `base.html`'deki bağlantı artık `/static/style.css?v={{ statik_surum() }}`.
  Dosya her değiştiğinde `?v=...` değeri de değişiyor, tarayıcı bunu **farklı
  bir adres** sanıp yeniden indiriyor — sert yenile gerekmiyor, kullanıcı
  hiçbir şey yapmadan otomatik düzeliyor.
- **`db.PROGRAM_KOK` üzerinden okunuyor** (`KOK / "static" / "style.css"`),
  diğer statik-yol kurallarıyla aynı (tuzak #8). Dosya bulunamazsa (olmayacak
  ama) `"0"` döner, sayfa hâlâ açılır — sürüm numarası eksik olsun, CSS hiç
  yüklenmesin daha kötü.
- Yalnızca `style.css` kapsandı; `apple-touch-icon` gibi nadiren değişen
  statikler dokunulmadı — bu tur bir sorun onlarda hiç görülmedi, kapsamı
  büyütmeye gerek yok.

## Test edildi

- Sunucu başlatıldı, ana sayfa `curl` ile çekildi: bağlantı
  `style.css?v=1789550130` gibi bir sürüm numarasıyla geliyor. O adresten
  doğrudan `style.css` istendi, içinde `ucsutun` kuralının geldiği
  doğrulandı (200, 2 eşleşme).
- Kullanıcının kendi makinesinde de aynı teşhis (CSS'te `ucsutun` yok, HTML'de
  var) doğrulanarak bu sürümün gerçek sebebi bulundu — tahminle değil.
- Deneme oturumu geri alındı.

# v6.70 — giriş ekranının üst başlığı program adı

Kullanıcının isteği: `/giris` ekranının en üstünde (koyu bant) "Patient Data
Center" yazsın. Üst bant zaten `base.html`'de tek yerden basılıyor
(`{% block ustbaslik %}`, varsayılanı `metin("program_adi")`) — `giris.html`
bunu kendi başlığıyla (`metin("giris")`, "Giriş") eziyordu. Override kaldırıldı,
ekran artık `ana.html`'in de yaptığı gibi `program_adi`'yi açıkça yazıyor.
`metin("giris")` anahtarı artık hiçbir şablonda kullanılmıyor; kaldırılmadı
— çevrilmiş bir metin, ileride yine lazım olabilir, tutmanın maliyeti yok.

## Test edildi

- `curl` ile `/giris`'in `<h1>`'i "Patient Data Center" döndürdüğü
  doğrulandı, telefon genişliğinde (390px) ekran görüntüsüyle de görüldü.

# v6.71 — koyu tema DENEMESİ + üst başlıkta amblem (henüz kesinleşmedi)

Kullanıcı bir mockup gönderdi: koyu zemin, pembe/magenta vurgu rengi, üst
başlıkta halka + dört nokta amblemi. "Böyle olsa nasıl olur, dene" dedi.
**Bu sürüm bir denemedir, kullanıcı henüz karar vermedi** — kalıcı olacaksa,
tek tema mı yoksa sistem tercihine bağlı mı kalacağı da sonra netleşecek.

## Ne yapıldı

- Bütün tasarım zaten `:root` CSS değişkenleri üzerinden kuruluydu
  (`--ink`, `--yuzey`, `--vurgu`, ...), o yüzden tek tek şablon değiştirmek
  yerine bu değişkenler `@media (prefers-color-scheme: dark)` içinde
  yeniden tanımlandı. Sistemi koyu temaya ayarlı kullanıcıda program
  otomatik koyu açılıyor; ayarlı değilse **hiçbir şey değişmiyor** — açık
  tema hâlâ eskisiyle birebir aynı.
- Yeni değişken **`--ust-bg`**: üst bant, kimlik bandı, aktif sekme gibi
  öğeler `--ink`'i arka plan (kasa rengi) olarak kullanıyordu; koyu temada
  `--ink` metin rengine (açık) dönüşünce bu öğeler yanlışlıkla beyaza
  dönerdi. `--ust-bg` bu öğeler için ayrı tutuldu, açık temada `var(--ink)`
  ile aynı değeri alıyor (görünüm değişmedi), koyu temada sabit koyu lacivert.
- **Amblem PNG değil, satır içi SVG** (`base.html`, `.ust` içinde,
  `<h1>`'in yanında). `simge_uret.py`'nin çizdiği "zona halkası + dört
  hücre" fikrinin aynısı ama dört nokta `fill="var(--vurgu)"` kullanıyor —
  tema değişince amblem de kendiliğinden renk değiştiriyor, ayrı bir dosya
  üretmeye gerek yok.
- **Dokunulmayanlar (bilerek)**: birkaç durum rozeti (iptal/tamamlandı gibi)
  ve uyarı rengi hâlâ sabit açık-tema tonları kullanıyor — koyu temada hafif
  uyumsuz kalabilirler, düzeltilmedi. Resmî form ekranı (`/form/...`)
  hiç dokunulmadı, o hep beyaz kâğıda basacak. Favicon/PWA ikon dosyaları
  (`static/ikon_*.png`) da **değiştirilmedi** — yalnızca ayrı bir örnek
  üretilip kullanıcıya gösterildi, `simge_uret.py`'nin kendisi güncellenmedi.

## Test edildi

- Playwright ile `color_scheme='dark'` ve `'light'` bağlamlarında giriş,
  ana ekran ve bir cycle ekranı (`/cycle/1`) ekran görüntüsü alındı,
  kullanıcıya gönderildi. Açık temada yalnızca amblemin eklendiği,
  başka hiçbir şeyin değişmediği doğrulandı.
- Deneme oturumu geri alındı.

# v6.72 — koyu tema kalıcı ve tek tema oldu

Kullanıcı v6.71'deki denemeyi (ekran görüntüleriyle) inceledi, karar
**"2"**: koyu tema sistem tercihine bağlı kalmasın, **varsayılan/tek tema**
olsun. Açık tema tamamen kaldırıldı.

## Ne yapıldı

- `@media (prefers-color-scheme: dark)` bloğu kaldırıldı, içindeki değerler
  doğrudan `:root`'a taşındı. Artık tek bir renk seti var.
- **Kalan sabit-renkli parçalar temizlendi.** v6.71'de "deneme" olduğu için
  bilerek dokunulmamış ~15 sabit renk vardı — artık kalıcı olduğu için hepsi
  koyu temaya uyacak şekilde güncellendi:
  - Yeşil "dolu/kaydedildi" rozetleri (`.kart h2.ikili .rozet`,
    `.bilgikart .rozet`, `.serit .sn.dolu`, `.onum.dolu`) — kullanıcının
    kendi gönderdiği ekran görüntüsündeki "Kaydediidi" etiketinin tam
    karşılığı, en görünür olanlardı.
  - Kırmızı "dikkat/tehlike" renkleri (`.serit .sn.deg`, `.tehlike`,
    `.dugme.tehlikeli`, `.tehlike-bag` bağlantıları, `.sfalt`/`.fotoalt`
    silme bağlantıları) — koyu kart üzerinde eski soluk kırmızı okunmuyordu.
  - Turuncu uyarı renkleri (`.uyari.birlikte`, `.zaman.sapma`, `.uyari`
    kenarlığı) — metin koyu kahverengiydi, koyu zeminde neredeyse görünmüyordu.
  - Hepsi tek tek elle seçildi (sabit değerler, değişken değil) çünkü her
    biri farklı bir "durum" rengi (yeşil/kırmızı/turuncu) taşıyor — tek bir
    `--vurgu`'ya indirgemek anlamlarını birbirine karıştırırdı.
- **Gerçek bir hata bulundu ve düzeltildi**: `.tazelekutu a` (başka bir
  cihazdan kayıt girildiğinde çıkan şeritteki bağlantı) zemini sabit beyazdı
  ama yazı rengi `var(--ink)` kullanıyordu. v6.71'de --ink açık renge
  dönünce bu buton **beyaz zemin üzerinde beyaza yakın yazı** olurdu —
  okunmaz. Yazı rengi şimdi sabit koyu (`#17222b`). Ekranda hiç tetiklenmedi
  (eş zamanlı düzenleme gerektiriyor), kod taranarak bulundu.
- `simge_uret.py`'deki `ZEMIN`/`ZONA`/`HUCRE` değerleri yeni palete
  güncellendi, favicon/PWA ikonları (`static/ikon_180/192/512.png`)
  yeniden üretildi — artık koyu zemin + beyaz halka + pembe dört nokta.
- `CLAUDE.md`'ye kalıcı kural olarak yazıldı: yeni bileşen yazarken renk
  sabitleme, `--ink`/`--ust-bg` ayrımına dikkat et, sabit zeminde sabit yazı
  kullan (bu sürümde tam bunun tersi bir hata bulunduğu için özellikle).

## Test edildi

- Playwright ile (artık `color_scheme` zorlamaya gerek yok, tek tema)
  ana ekran (dar + geniş), denüdasyon ekranı (numara şeridi, "Kaydedildi"
  rozeti — kullanıcının orijinal ekran görüntüsüyle karşılaştırıldı) ve
  hasta silme ekranı (tehlike kutusu) görüldü — hepsi okunaklı, renkler
  tutarlı.
- Kod tarandı: önceki tüm sabit açık-tema renkleri (`#e4eae7`, `#a11f1f`,
  `#fdf3e3` vb.) style.css'te aratıldı, geriye yalnızca temadan bağımsız
  kalması gereken ikisi bırakıldı (fotoğraf silme rozeti, `.kagit` yazdırma
  kutusu).
- Deneme oturumu geri alındı.

# v6.73 — üst başlık amblemi büyütüldü

Kullanıcının isteği: amblem biraz daha büyük olsun. `.ust .amblem`
24px → 32px (`base.html`'deki `.marka` sarmalayıcısı zaten `align-items:
center` ile hizalıyor, tek satır değişti).

# v6.74 — koyu temada bazı yazılar okunmuyordu (rozet zemini + native kontroller)

Kullanıcı: "Arayüzde bazı yazılar okunmuyor." İki ayrı sebep bulundu.

## 1. Genel `.rozet` zemini artık açık renkti

`.rozet` (İptal/Arşiv/Tamamlandı etiketleri — hemen her liste ekranında:
hasta kartı, cycle listeleri, bitenler) zemin olarak `var(--ink-2)`
kullanıyordu. v6.72'de `--ink-2` **metin** rengi olarak açık bir tona
çevrilmişti (koyu tema); zemin olarak kullanılan yerlerde beyaz yazının
üstüne binince neredeyse okunmuyordu. Aynı hata üç yerde daha bulundu
(`.hucre .kk.bos .tarafr`, `.hucre .alt .tar` / `.onum b .tar` — taraf
etiketleri). Hepsi sabit koyu bir gri-lacivert (`#3d4f63`) aldı — bunlar
"durum" rengi taşımıyor (yeşil/kırmızı/turuncu gibi), nötr bir zemin yeterli.
- **Ders**: `--ink-2`/`--ink-3` artık yalnızca **metin** için güvenli;
  zemin/kenarlık olarak kullanılacaksa sabit bir renk seç. v6.72'nin
  taramasında bu ikisi (arka plan olarak `--ink-2`) atlanmıştı çünkü arama
  yalnızca eskiden-açık-temaya-özel sabit hex renkleri hedefliyordu, CSS
  değişkeni kullanan ama *anlamı tersine dönen* bu satırları yakalamadı.

## 2. Tarayıcının kendi çizdiği kontroller hâlâ "açık" sanıyordu

`<select>` açılır listesi, tarih/saat seçici gibi öğeleri tarayıcı kendisi
çiziyor. Sayfa CSS'i onlara doğrudan renk veremez; tarayıcı yalnızca sayfanın
**`color-scheme`**'ine bakıp kendi açık ya da koyu setini seçiyor. v6.71'de
`prefers-color-scheme` ile otomatik koyuyken tarayıcı bunu zaten biliyordu;
v6.72'de tek/kalıcı temaya geçilince bu sinyal hiç verilmedi — tarayıcı hâlâ
"açık" sanıp `<select>`'in açılan listesini kendi açık renkleriyle çiziyordu,
bizim CSS'imiz yalnızca **kapalı** kutuya açık renk yazı vermişti (dark tema
metni) → bazı tarayıcılarda okunmuyordu. `html { color-scheme: dark; }`
eklendi — artık tarayıcı kendi çizdiği her şeyi (açılır liste, tarih/saat
seçici, kaydırma çubuğu) koyu setiyle çiziyor.

## Test edildi

- Bir cycle'ı "Tamamlandı" durumuna alıp `/hasta/{id}` ekranında rozeti
  ekran görüntüsüyle kontrol ettim — önce (aynı hex ile canlandırılan) düşük
  kontrast doğrulandı, düzeltmeden sonra net okunuyor.
- `getComputedStyle(document.documentElement).colorScheme` ile `dark`
  döndüğü doğrulandı.
- Deneme verisi (cycle durumu) geri alındı, `PRAGMA foreign_key_check` temiz.

# v6.75 — arka plana tüp bebek temalı görsel eklendi

Kullanıcının isteği: "Programın background'unda güzel bir görsel istiyorum.
Tüp bebek ile ilgili bu renk tonlarına uygun."

## Ne yapıldı

- İki yeni statik SVG: `static/desen.svg` (sağ üst köşe) ve `static/desen2.svg`
  (aynı motifin 180° çevrilmişi, sol alt köşe — CSS background katmanlarında
  tek tek `transform` verilemediği için iki dosya gerekti). Motif amblemle
  (`base.html`'deki halka + dört nokta) **aynı aile**: dört hücreli embriyo
  kümesi, zona pellucida halkası, ikiye bölünen hücre, dağılmış tek hücreler
  — hepsi `--vurgu` (pembe) ve biraz `--ink-3` tonunda mavi ile, yumuşak bir
  radial gradient üstünde. Köşede yoğun, merkeze doğru soluyor.
- `body`'de iki katmanlı arka plan: `background: url(desen.svg) no-repeat
  top right / 46vw fixed, url(desen2.svg) no-repeat bottom left / 46vw fixed,
  var(--zemin);`. **`vw` tabanlı boyut** — sabit piksel olsaydı telefonda
  fazla büyük ya da masaüstünde fazla küçük kalırdı, oranlı kalıyor.
  **`fixed`**: kaydırırken köşelerde sabit duruyor, kartlarla kaymıyor.
  **Kartların üstüne binmiyor** çünkü `.kart` zaten opak (`--yuzey`) — desen
  yalnızca kartlar arasındaki/köşelerdeki boşluklarda görünüyor, metnin
  önüne geçmiyor.
- **Yazdırma etkilenmedi**: `@media print`'teki `body { background: #fff }`
  `background` kısayolu olduğu için görsel katmanları da sıfırlıyor,
  resmî formlar hâlâ düz beyaz basılıyor.
- **Bir hata bulundu ve düzeltildi**: ilk yazışta SVG yorumlarında Türkçe
  metin içinde `--` (çift tire) kullanılmıştı — XML yorumlarında bu geçersiz,
  tarayıcı SVG'yi hiç render etmiyor, hata sayfası gösteriyordu (arka plan
  sessizce boş kalıyordu). Yorumlardaki `--` kaldırıldı.

## Test edildi

- SVG dosyaları doğrudan tarayıcıda açılıp XML hatası olmadığı doğrulandı
  (ilk denemede "Double hyphen within comment" hatası tam burada yakalandı).
- Playwright ile `getComputedStyle` üzerinden `background-image`,
  `background-position` (`100% 0%, 0% 100%`), `background-size` (46vw) ve
  `background-attachment` (`fixed, fixed`) değerleri doğrulandı.
- Giriş, ana ekran (dar + geniş) ekran görüntüsüyle görsel kontrol edildi —
  desen görünüyor, kartların içeriği hâlâ tam okunaklı.
- Deneme oturumu geri alındı.

# v6.76 — form Excel çıktısı "içerikte sorun var" hatası veriyordu

Kullanıcı: "Form Excele aktar dediğimde Excel uygulaması bazı öğelerde bir
sorunla karşılaştık şeklinde hata veriyor." (Excel'in klasik "bu dosyanın
bir kısmında okunamayan içerik var, onarmak ister misiniz" uyarısı.)

## Sebep

`excel.py`'deki sayfa XML'i amblem varsa `<drawing r:id="rId1"/>` etiketini
`<pageMargins>`/`<pageSetup>`'tan **önce** yazıyordu. OOXML'in
`CT_Worksheet` şeması sıkı bir sırayla çalışıyor (`xsd:sequence`) —
`drawing` **`pageSetup`'tan sonra** gelmek zorunda. Excel bu sırayı
bozan dosyayı "bir kısmı onarılabilir içerik" diye açıyor, resim taşıyan
elemanı (amblem) genelde tam da bu yüzden düşürüyor — kullanıcının
"bazı öğelerde" dediği şey büyük ihtimalle amblemdi.
- Etkilenen: amblem taşıyan **her** Excel çıktısı — gömülü iki resmî form
  (`/disari/form/ozet/{id}`, `/disari/form/artlab/{id}`) ve laboratuvarın
  kendi yüklediği form (`/disari/form/lab/{id}/{id}`). Üçü de aynı paylaşılan
  `excel.kitap()`/`_sayfa_xml()` fonksiyonunu kullanıyor, tek yerden düzeldi.
- Amblemsiz Excel çıktıları (ay listesi, cryo, istatistik, tüm döküm)
  etkilenmiyordu — onlarda `<drawing>` hiç yok.

## Düzeltme

`<drawing r:id="rId1"/>` satırı `<pageSetup>`'tan **sonra**, `</worksheet>`
kapanışından hemen önceye taşındı. Sıra artık: `mergeCells → pageMargins →
pageSetup → drawing` — şemanın istediği sıra.

## Test edildi

- Her iki gömülü form için (`ozet`, `artlab`) test verisiyle Excel çıktısı
  üretildi, `.xlsx` açılıp `xl/worksheets/sheet1.xml` elle incelendi:
  `drawing` artık `pageSetup`'tan sonra.
- `openpyxl` (yalnızca bu test için geçici kuruldu, projenin bağımlılığı
  **değil** — `excel.py`'nin "kütüphanesiz" kuralı bozulmadı) ile hem eski
  hem yeni dosyalar açıldı: ikisi de istisna vermiyor (openpyxl sıra
  hatasına o kadar sıkı bakmıyor), ama yeni dosyada resim, sayfa boyutu ve
  birleşik hücreler doğru okundu.
- Deneme oturumu geri alındı.

# v6.77 — Excel'deki form kutularının sağ/alt kenarı eksikti

Kullanıcı v6.76'yı denedi: hata penceresi gitmişti ama "formlar orijinaline
tam anlamıyla benzemiyor, Excel hücreleri sağ tarafları kesik" dedi.

## Sebep

Kâğıttaki her kutu (örn. "Dosya No" kutusu) Excel'de birden çok hücrenin
**birleştirilmesiyle** kuruluyor (`form_kalip.izgara_kur()`). Birleşmiş bir
kutunun görünen kenarlığı Excel'de **anchor** (sol üst) hücrenin değil,
kutunun en sağındaki/en alttaki hücrenin **kendi** kenarlık bilgisinde
duruyor — Excel birleştirmede her hücrenin kendi sınırını korur, devretmez.
`izgara_kur()` birleşmenin **kapladığı** hücreleri (anchor hariç) hiç
okumuyordu (`kapali` listesindeydi, atlanıyordu) — yani kutunun sağ/alt
kenar bilgisi kalıba hiç girmemişti. v6.76'nın düzeltmesi (kapladığı
hücrelere de anchor'ın stilini vermek) bunu çözmüyordu, çünkü anchor'ın
kendi stili zaten "sağ" bilgisini hiç taşımıyordu — o bilgi hep en sağdaki
hücrenin kendi `xf.border`'ındaydı.

Kod tabanında aynı fikrin **zaten** bir örneği vardı: boş hücreler soldakine
"colspan" ile katılırken (`_katilir`) kod son katılan hücrenin sağ kenarını
alıyordu (`stil[5][3]`). Gerçek birleşmeler (`birlesmeler`, Excel'in kendi
`MergedCells`'i) için aynı şey yapılmıyordu.

## Düzeltme

`izgara_kur()`'da bir hücre birleşmenin anchor'ıysa (`rs>1 veya cs>1`),
kutunun en sağ hücresinin **kendi** sağ kenarını ve en alt hücresinin
**kendi** alt kenarını okuyup anchor'ın kenar bilgisiyle birleştiriyor.
Bu, hem `kalip_uret.py` (orijinal `.xls`'ten) hem `xlsx_oku.py` (yüklenen
`.xlsx`'ten) tarafından paylaşılan **tek** fonksiyonda olduğu için ikisi de
düzeldi, ikinci bir kopya yazılmadı.

**`form_kalip.json` yeniden üretildi** — bu bir çalışma zamanı hesabı değil,
önceden çıkarılmış statik bir dosya (`kalip_uret.py`nin ürettiği). Düzeltme
yalnızca ARACIN mantığını değiştirdiği için, aracı `formlar_asil/`'deki
orijinal iki `.xls` üstünde tekrar çalıştırıp kalıbı yeniden ürettim
(`python3 formlar_asil/kalip_uret.py ...`) — CLAUDE.md'nin kuralı zaten bu:
"kalıp elle yazılmadı... değişirse aracı tekrar çalıştır." Amblem PNG'si
etkilenmedi (bit bit aynı çıktı).

## Test edildi

- `openpyxl` (yalnızca test için, projeye eklenmedi) ile birleşmiş
  hücrelerin *hem* anchor *hem* en sağ/en alt köşesinin kenarlık bilgisi
  karşılaştırıldı: düzeltmeden önce köşe hücrede `R=None`/`B=None`,
  sonrasında kâğıttaki çizgiyle eşleşen stil (`thin`/`dashed`) görünüyor.
  Birkaç kutunun köşesi hâlâ kenarlıksız çıktı — kâğıt aslında da o
  alanların kutusu yok, bu doğru davranış.
  - LibreOffice ile görsel karşılaştırma **denendi ama bu ortamda
    çalışmadı** — headless LibreOffice bu sandbox'ta hiçbir `.xlsx`'i (hatta
    `openpyxl`'in kendi ürettiği basit bir dosyayı bile) açamadı; bu ortamın
    kendi eksikliği, üretilen dosyanın bozukluğu değil (ayrıca doğrulandı).
  - Ekrandaki/yazdırılabilir sürüm (`/form/ozet/{id}`) `izgara_kur()`'u
    paylaştığı için ekran görüntüsüyle ayrıca kontrol edildi — hâlâ doğru
    görünüyor, bu değişiklik yalnızca Excel'in kenarlık hesabını etkiliyor.
- Zip/XML yapısı yine kontrol edildi: geçerli XML, yinelenen hücre adresi
  yok, `openpyxl` istisnasız açıyor.
- Deneme oturumu geri alındı, `PRAGMA foreign_key_check` temiz.

# v6.78 — ana ekran kartları 5 ile sınırlandı, "Tümü" bağlantıları eklendi

Kullanıcının isteği: Devam Eden Tedaviler / Bugün Biten Tedaviler / Yaklaşan
Tedaviler beşten fazla göstermesin; fazlası varsa "Tümü" çıksın. Ayrıca
"Bugün Biten Tedaviler"in yalnızca bugünkü tarihlileri göstermesi istendi —
bu zaten `cycle_listesi(bugun=True)`'nin ölçüsüydü
(`date(c.bitis_zamani) = date('now','localtime')`, v6.29'dan beri); kod
tekrar okunup doğrulandı, ek bir değişiklik gerekmedi. Kullanıcı hâlâ eski
tarihli bir kayıt görürse (örnek istiyorum) — o zaman kod değil, o kaydın
`bitis_zamani`'ı incelenmeli.

## Ne yapıldı

- Üç kartın da `<h2>`'si `class="ikili"` oldu (Bugün Biten Tedaviler'de
  zaten vardı), satırlar `liste[:5]` şeklinde kırpıldı. **Rozet sayısı
  kırpılmadı** — `liste|length` hâlâ gerçek toplamı gösteriyor, yalnızca
  görünen satırlar 5'te kesiliyor.
- "Tümü" bağlantısı yalnızca `liste|length > 5` iken basılıyor:
  - Bugün Biten Tedaviler → `/bitenler` (v6.29'dan beri var olan tüm-zamanlı
    arşiv; sadece görünürlük koşulu eklendi, hedef değişmedi).
  - Devam Eden Tedaviler → yeni `/devam-eden` (`devam_eden.html`,
    `cycle_listesi()`'nin tam listesi, `bitenler.html` ile aynı kalıp).
  - Yaklaşan Tedaviler → yeni `/yaklasanlar` (`yaklasanlar.html`,
    `cycle_listesi(yaklasan=YAKLASAN_GUN)`'ın tam listesi, aynı 14 günlük
    pencere). **Takvim değil** — v6.65'te kaldırılan `/takvim` ay ızgarasıydı,
    bu düz bir liste, aynı "aynı şey gibi" gerekçesi burada geçerli değil.
- Üç ekran de `yol_modulu()`'nda özel bir kural gerektirmedi — `/bitenler`
  gibi onlar da görüntüleme ekranı, middleware'in varsayılanı (serbest)
  zaten kapsıyor.
- Yeni metin anahtarı yalnızca `n_devam_eden`/`n_devam_eden_tekil`;
  `/yaklasanlar` mevcut `n_planli_is` (eski takvim özelliğinden kalma,
  anlamı birebir uyuyor) ve `yaklasan_yok`'u yeniden kullandı.

## Test edildi

- Test verisiyle her üç listeyi 5'in üstüne çıkarttım (9/7/7):
  ana ekranda üçü de ilk 5'i + "Tümü"yü gösterdi, rozet sayıları gerçek
  toplamı (9/7/7) korudu.
- `/devam-eden` ve `/yaklasanlar` tam listeyi (9, 7) doğru başlıkla
  gösterdi; `/yaklasanlar`'ı boş durumda da kontrol ettim
  ("planlanmış iş yok" mesajı doğru çıktı).
- Test verisi silinip 2 kayda dönünce üç "Tümü" bağlantısı da kayboldu
  (`grep -c "Tümü"` → 0).
- Deneme oturumu geri alındı, `PRAGMA foreign_key_check` temiz.

# v6.79 — arayüzde "cycle" yerine "tedavi" deniyor

Kullanıcının isteği: "Cycle yerine tedavi demek istiyorum." Program veritabanında
ve kodda "cycle" terimini kullanmaya devam ediyor (tablo adı, `cycle_id`,
`/cycle/{id}` rotaları, Python değişkenleri — bunlara dokunmak koca bir iç
mimari değişikliği olurdu ve hiçbir kullanıcı faydası yok), ama **ekranda
görünen Türkçe metinlerin hepsinde** "cycle" sözcüğü "tedavi" ile değiştirildi.

## Kapsam

- `metinler.py`: "tr" değerlerinde geçen ~35 "cycle" sözcüğü Türkçe dilbilgisi
  kurallarına uygun çekimlerle "tedavi"ye çevrildi (`cycle'ı` → `tedaviyi`,
  `cycle'da` → `tedavide`, `cycle'ların` → `tedavilerin`, vb.). **"en" değerleri
  değişmedi** — İngilizce çeviri zaten yarım ve askıda (bekleyen iş 8), üstelik
  "cycle" İngilizce IVF literatüründe zaten kullanılan bir klinik terim; bu
  değişiklik yalnızca Türkçe arayüzle ilgili.
- Henüz `metin()`'e taşınmamış beş şablonda (`arsiv_sil.html`, `cycle_sil.html`,
  `esle.html`, `hasta_sil.html`, `transfer_sil.html` — bekleyen iş 8'deki liste)
  elle yazılmış "Cycle" metinleri de aynı şekilde değiştirildi.
- `app.py`'de üç yerde kullanıcıya gösterilen metin vardı: `MODULLER` listesindeki
  "Hasta ve cycle kaydı" etiketi (yönetici izin ekranı), `/yonetim` panelindeki
  kayıt sayıları tablosunun "Cycle" satır adı, ve birkaç sunucu hata mesajı
  ("Cycle no boş bırakılamaz.", "numaralı cycle zaten var" gibi). Bu arada
  "Cycle no boş bırakılamaz." mesajının aslında `cycle_no` alanının ekrandaki
  etiketiyle (`lab_kayit_no` → "Lab kayıt no") hiç eşleşmediği fark edildi —
  düzeltilirken doğru etikete ("Lab kayıt no boş bırakılamaz.") çevrildi.
- Değişmeyenler: tablo adı `cycle`, kolon adları (`cycle_id`, `cycle_no`,
  `cycle_tipi`, `hasta_cycle_no`, `thaw_cycle_id`, `tr_cycle_id`,
  `cycle_sira_no`...), rota yolları (`/cycle/{id}`, `/hasta/{id}/cycle/yeni`),
  Python değişken/fonksiyon adları, şablon dosya adları (`cycle_detay.html`,
  `cycle_form.html`, ...), `metin()` **anahtarları** (`"cycle"`, `"cycle_duzenle"`
  gibi — yalnızca değerleri değişti), SQL sorguları, docstring'ler ve kod
  yorumları. Bunlar kod tarafının iç ismi; ekranda hiç görünmüyor.

## Test edildi

Sunucu ayağa kaldırıldı, yönetici oturumu açılarak ana ekran, `/hastalar`,
`/hasta/{id}`, `/cycle/{id}`, `/istatistik`, `/hasta/{id}/sil`, `/cycle/{id}/sil`,
`/hasta/{id}/cycle/yeni`, `/cycle/{id}/esle`, `/kullanicilar` ve `/yonetim`
gerçek tarayıcı isteğiyle çekildi; hiçbirinde ekrana basılan "Cycle" sözcüğü
kalmadığı, "Tedavi" ile değiştiği doğrulandı. Test oturumu silindi,
`PRAGMA foreign_key_check` temiz.

# v6.80 — hasta kartında tedaviler yanlış sırada duruyordu

Kullanıcının isteği: "Hasta kartında en üstte en son tedavi olsun, en altında
ilk tedavi olsun." Sıralama zaten en yeniyi üste koymaya çalışıyordu
(`ORDER BY COALESCE(opu_zamani, hcg_zamani) DESC`) ama ölçü yanlıştı.

## Sebep

`fet` ve `fet_kultur` tipi tedavilerde OPU hiç yapılmıyor (embriyo başka bir
cycle'dan geliyor) — bu yüzden hem `opu_zamani` hem `hcg_zamani` bu tedavilerde
her zaman NULL. SQLite `DESC` sıralamada NULL'ları **en sona** koyuyor; sonuç
olarak bir hastanın en son açtığı tedavi FET ise, tarihi ne olursa olsun listenin
en altına düşüyordu — IVF/ICSI tedavisi ondan önce açılmış olsa bile üstte
kalıyordu. Test verisiyle doğrulandı: hasta 1'in 1. tedavisi (ivf_icsi,
opu_zamani dolu) ile 2. tedavisi (fet, ikisi de NULL) — düzeltmeden önce 1.
tedavi üstte çıkıyordu, halbuki 2. tedavi daha sonra açılmıştı.

## Düzeltme

`app.py`'de `hasta_detay()` sorgusu `ORDER BY hasta_cycle_no DESC, id DESC`
oldu. `hasta_cycle_no` ("Kaçıncı tedavi") her tedavi tipinde atanıyor
(`sonraki_hasta_cycle_no()` ile otomatik öneriliyor) ve tedavi tipinden
bağımsız, hep artan bir sıra numarası — klinik tarih alanlarının aksine NULL
kalma ihtimali pratikte yok. Aynı desen zaten `/cycle/{id}/vitrifikasyon`
ekranının taşıyıcı/kaynak tedavi seçicisinde kullanılıyordu
(`ORDER BY hasta_cycle_no DESC, id DESC`, app.py satır ~4996) — yeni sıralama
onunla tutarlı.

## Test edildi

Sunucu ayağa kaldırıldı, test hastasının (2 tedavi: 1. ivf_icsi/OPU'lu,
2. fet/OPU'suz) `/hasta/1` ekranı çekildi: düzeltmeden önce "1. tedavi"
üstte çıkıyordu, düzeltmeden sonra "2. tedavi" (daha sonra açılan) üstte,
"1. tedavi" altta — istenen sıra. Test oturumu silindi,
`PRAGMA foreign_key_check` temiz.

# v6.81 — tedavi ekranına "Doktor Notu" eklendi (foto/PDF, önizleme, tam ekran)

Kullanıcının isteği: tedavi kaydına Doktor Notu bölümü — fotoğraf veya PDF
eklenebilsin, küçük önizlemesi görünsün, üstüne basınca tam ekran açılsın.

## Neden bu kadar kolay oldu

Program zaten "cycle arşivi" diye bir şey biliyordu: bir örneğe (oosit/embriyo)
bağlı olmayan, doğrudan tedaviye bağlı fotoğraflar (`goruntu.specimen_id IS
NULL`). Doktor Notu'nu bunun **yeni bir `asama` değeri** olarak kurdum
(`"doktor_notu"`) — `goruntu.asama` serbest metin, CHECK kısıtı yok, yeni bir
tablo ya da göç gerekmedi. Asıl iş iki yerde:
- `goruntuler.elle_ekle()` yalnızca görüntü uzantılarını kabul ediyordu
  (`UZANTILAR`); Doktor Notu PDF de kabul etmeli. Fonksiyona `izin_uzantilari`
  parametresi eklendi (varsayılan hâlâ `UZANTILAR`, eski çağıranlar
  etkilenmedi), yeni `DOKTOR_NOTU_UZANTILARI = UZANTILAR | {".pdf"}` sabiti
  yalnızca yeni rotadan geçiyor.
- Önizleme/tam ekran: görüntüler için zaten var olan `_buyutec.html` fullscreen
  görüntüleyicisi kullanıldı (aynı desen: `.kfoto` düğme + `data-idler` +
  `buyutecAc()`). PDF için `_buyutec` işe yaramaz (o yalnızca `<img>` basıyor);
  PDF kutusu tıklanınca `/dosya/{id}`'yi yeni sekmede açıyor — tarayıcının
  kendi PDF görüntüleyicisi zaten neredeyse tam ekran, ek kütüphane gerekmedi
  (`excel.py`/`karekod.py` ile aynı "kütüphanesiz" gerekçe).

## "Cycle ekranı klinik özettir, fotoğraf yoktur" kuralıyla çelişmiyor mu?

v6.20'deki kural embriyoloji fotoğrafları içindi: onlar aşama ekranlarında
tek tek büyük bakılacak, cycle ekranı özet kalsın diye oraya küçük resim
konmuyordu. Doktor Notu farklı bir kavram — rapor/konsültasyon yazısı gibi bir
**belge eki**, embriyo fotoğrafı değil; klinik özetin parçası, protokol notu
kartının hemen yanında durması doğru. Kullanıcı ekran görüntüsü göstererek
tam olarak bu ekranı işaret etti. `cycle_detay.html`'deki yorum bunu netleştirecek
şekilde güncellendi, kural embriyoloji fotoğrafları için hâlâ geçerli.

## Ne değişti

- `goruntuler.py`: `DOKTOR_NOTU_UZANTILARI` sabiti, `elle_ekle()`'ye
  `izin_uzantilari` parametresi.
- `app.py`: `cycle_detay()` artık `arsiv`'i `asama != 'doktor_notu'` ile
  süzüyor (iki bölüm karışmasın), ayrıca `doktor_notlari` (her satırda
  `pdf_mi` bayrağı) ve `doktor_notu_resim_ids` (yalnızca görüntülerin id
  listesi, `_buyutec` gezinmesi için) hesaplıyor; `hata` parametresi eklendi.
  Yeni rota `POST /cycle/{id}/doktor-notu-ekle` — `foto-ekle`'nin
  kopyası, yalnızca `asama` sabit "doktor_notu" ve izin listesi PDF içeriyor.
  `yol_modulu()`'nda `doktor-notu-ekle` de `foto-ekle`/`esle` gibi `foto`
  modülüne bağlandı. `/goruntu/{id}/sil` **değişmeden** yeniden kullanıldı —
  zaten `son == "sil"` kuralıyla `silme` modülüne bağlı, genel bir silme
  ekranı; yalnızca "Aşama" etiketi `doktor_notu` için `metin("doktor_notu")`
  gösterecek, `<img>` yerine `<embed type="application/pdf">` basacak şekilde
  küçük bir dallanma eklendi (`goruntu_sil_ekran()`'da `pdf_mi` hesaplanıp
  şablona geçiyor).
- `templates/cycle_detay.html`: yeni "Doktor Notu" kartı (protokol notu
  kartının hemen altında, `id="doktor-notu"` çapa), `_buyutec.html` include +
  `.notfoto` tıklama kablolaması (her `_buyutec` kullanan ekranın kendi
  betiğini yazması gerekiyor, bu ekranda daha önce hiç yoktu). Yükleme
  formundan dönen hata `#doktor-notu`'ya işaret ediyor, sayfanın tepesinde
  `{% if hata %}` bandıyla gösteriliyor.
- `static/style.css`: `.kfoto.pdf` — `.kfoto.yok`'un ("henüz yok, tıklanamaz")
  aksine gerçek bir bağlantı, düz koyu zemin (`#3d4f63`, v6.74'teki sabit ton)
  ve `cursor` mirasıyla tıklanabilir görünüyor.
- `metinler.py`: `doktor_notu`, `doktor_notu_yok`, `doktor_notu_ipucu`.

## Test edildi

Sunucu ayağa kaldırıldı; PDF + PNG birlikte yüklendi (`multipart/form-data`,
gerçek dosya baytlarıyla) — PDF "PDF" etiketli kutu olarak, PNG küçük resim
olarak doğru render edildi. `/dosya/{id}` PDF için `content-type:
application/pdf` döndürdü. Desteklenmeyen uzantı (`.docx`) doğru hata mesajını
(PDF dahil izin listesiyle) verdi. Genel "Fotoğraf ekle" ekranına aynı PDF
yüklenmeye çalışıldığında **hâlâ reddedildi** — regresyon yok, iki yükleme
yolu birbirinden bağımsız. `/goruntu/{id}/sil` onay ekranı PDF için `<embed>`,
görüntü için `<img>` bastı, "Aşama" alanı "Doktor Notu" gösterdi. Her iki
kayıt da silindi; veritabanı satırları ve arşivdeki dosyalar birlikte
kayboldu (diskte kontrol edildi), `PRAGMA foreign_key_check` temiz.

# v6.82 — kart başlıkları çok küçüktü, büyütüldü

Kullanıcının isteği: "Devam Eden Tedaviler / Bugün Biten Tedaviler / Yaklaşan
Tedaviler gibi Zamanlar Protokol Doktor Notu (1) Zaman çizelgesi gibi modül
başlıkları küçük görünüyor." Bu tek bir ekranın sorunu değildi — `.kart h2`
uygulamadaki **her** kartın başlığı için tek, paylaşılan kural
(`static/style.css`), yani her yerde aynı anda küçüktü: 13px, `var(--ink-2)`
(ikincil/soluk metin rengi).

## Düzeltme

`.kart h2`: `13px` → `16px`, `font-weight: 600` → `700`, `color: var(--ink-2)`
→ `var(--ink)` (birincil, koyu temada açık renk). Tek yerde değişti, bütün
uygulamaya yayıldı — ana ekranın üç kartı, tedavi ekranındaki Zamanlar/
Protokol/Doktor Notu/Zaman çizelgesi, `/yonetim`, `/kullanicilar`,
`/istatistik`, aşama ekranlarının bilgi kartları, kısacası her `<div
class="kart">` içindeki `<h2>`.

`.bilgikart h2` (aşama ekranlarının salt okunur bilgi kartı — `_bilgikart.html`
`kart()` makrosu) ayrıca `font-size: 14px; color: var(--ink);` ile küçük bir
override taşıyordu; bu satırlar kaldırıldı, artık `.kart h2`'nin yeni (daha
büyük) değerlerini miras alıyor — `.bilgikart` her zaman `.kart` ile birlikte
kullanıldığı için (`class="kart bilgikart"`, dört template'te doğrulandı)
güvenli.

`.kart h2.gun` (takvim gün başlığı, 15px + `var(--ink)`) dokunulmadan
bırakıldı — `/takvim` v6.65'te kaldırıldığından beri hiçbir şablon `gun`
sınıfını basmıyor, ölü CSS; bu değişiklik onu kapsamıyordu.

## Test edildi

Sunucu ayağa kaldırıldı, Playwright ile `/cycle/{id}` (Zamanlar, Protokol,
Doktor Notu, Oositler, Zaman çizelgesi kartları), `/` (Devam Eden/Bugün
Biten/Yaklaşan Tedaviler, Durum) ve `/yonetim` (Excel çıktısı, Yedekleme,
Veritabanı, Bu makinenin klasörleri) ekran görüntüsüyle karşılaştırıldı —
her kart başlığı artık belirgin şekilde daha büyük ve daha parlak, gövde
metninden net ayrışıyor.

# v6.83 — kart başlıkları ayrı bir renk aldı

Kullanıcının isteği: "Bu başlıklar başka renkte olsa. Programın arka rengini
düşünerek okunabilir bir renk yap." v6.82'de kart başlıkları büyütülmüş ama
rengi gövde metniyle aynı bırakılmıştı (`var(--ink)`) — kullanıcı bunları
görsel olarak ayrı bir renkte görmek istedi.

## Renk seçimi

Doğrudan `var(--vurgu)` (düğmelerin pembesi) denendi ama hesaplandı: kart
zemini `--yuzey` (#172230) üzerinde `--vurgu` (#e0356f) yalnızca **~3.75:1**
kontrast veriyor — WCAG'in normal boyuttaki metin için istediği 4.5:1'in
altında, "okunabilir" isteğiyle çelişirdi. Aynı ton hue/saturation'da
tutulup (HSL ~340°/73%) yalnızca **açıklık** kademeli yükseltilerek kontrast
hesaplandı; %65 açıklıkta (`#e76491`) kontrast **~5.07:1**'e çıkıyor — hem
markanın pembe rengiyle aynı aile hem WCAG AA'yı geçiyor. Yeni bir CSS
değişkeni **`--baslik`** olarak eklendi (`--vurgu`'nun düğmeler/aktif
rozetlerdeki kullanımına dokunmadan, yalnızca kart başlıkları için).

## Ne değişti

- `static/style.css`: `:root`'a `--baslik: #e76491;` eklendi. `.kart h2`
  `color: var(--ink)` → `color: var(--baslik)`.
- `.kart h2.gun` (kullanılmayan takvim kalıntısı, README v6.65) ve
  `.snapkart h2` (`var(--vurgu)`, kendi bilinçli vurgusu) dokunulmadan
  bırakıldı — kapsam yalnızca genel kart başlığı kuralı.

## Test edildi

Playwright ile `/cycle/{id}` ve `/` ekran görüntüsü alındı: "Zamanlar",
"Protokol", "Doktor Notu", "Zaman çizelgesi", "Devam Eden Tedaviler",
"Bugün Biten Tedaviler", "Yaklaşan Tedaviler", "Durum" başlıkları artık
gövde metninden (beyaz) ayrı, yumuşak pembe bir tonda ve düğmelerin canlı
pembesinden görsel olarak ayrışıyor. Test oturumu silindi,
`PRAGMA foreign_key_check` temiz.

# v6.84 — Yumurta Dondurma yeniden adlandırma + Sperm Dondurma modülü

Kullanıcının isteği: "Tedavilere Yumurta Dondurma tedavisi de ekle. Ayrıca
Cryo Harita bölümüne Sperm Dondurma ekleyelim. Şuan ki Tank başlığını
Embriyo Dondurma olarak değiştir. Bu modülün yanına Sperm Dondurma ekle."
Üç ayrı soru soruldu, üçü de netleştirdi:

1. **"Oosit dondurma" yeni bir tip mi, yeniden adlandırma mı?** Klinik yol
   aynı (OPU → Denüdasyon → Vitrifikasyon → Çözme), kullanıcı yeniden
   adlandırmayı seçti — yeni bir `cycle_tipi` kodu açılmadı.
2. **Embriyo Dondurma / Sperm Dondurma nasıl ayrılsın?** Kullanıcı "iki ayrı
   menü bağlantısı, iki ayrı ekran" seçti (aynı ekranda sekme değil).
3. **Sperm Dondurma hangi veriyi tutsun?** Kullanıcı yalnızca "dondurma
   öncesi semen analizi (hacim, konsantrasyon, motilite)" seçti — çözme/
   kullanım takibi bilerek kapsam dışı bırakıldı.

## "Oosit dondurma" → "Yumurta Dondurma" (`goc_032`)

Yalnızca `liste_degeri.etiket` güncellendi — v6.79'daki cycle→tedavi
deseninin aynısı: `kod` ("oosit_cryo"), `TIP_KODLARI`, `TIP_ASAMALARI` ve
mevcut cycle kayıtları hiç değişmedi, yalnızca ekranda görünen ad değişti.
Yeni bir cycle tipi açmak (yeni kod, yeni `TIP_ASAMALARI` girişi, göç ile
mevcut kayıtları taşıma) burada haksız bir karmaşıklık olurdu — klinik yol
zaten var ve birebir aynı.

## Embriyo Dondurma / Sperm Dondurma ayrımı

Mevcut "Cryo haritası" ekranı (`/cryo`, `cryo.html`) artık ekranda "Embriyo
Dondurma" yazıyor — yine yalnızca `metin("cryo_haritasi")`'nin görüntülenen
metni değişti, rota (`/cryo`), tablo adları (`tasiyici`, `konum`) ve iç kod
aynı kaldı (v6.79 deseni burada da).

Sperm Dondurma **tamamen yeni bir ekran** (`/sperm-dondurma`), ama mevcut
taşıyıcı/konum altyapısını paylaşıyor:

- **`tasiyici.kategori`** (`goc_033`, yeni kolon, varsayılan `'embriyo'`) —
  embriyo ve sperm taşıyıcıları aynı `tasiyici` tablosunda (ikisi de etiket/
  tip/renk/konum aynı fikir), ama Embriyo Dondurma ekranı yalnızca kendi
  taşıyıcılarını görmeli. `cryo_harita()`'daki üç sorgu (`tasiyicilar` iki
  dal + `tanklar`) `t.kategori='embriyo'` süzgeci aldı; `/disari/cryo`
  (Excel) dokunulmadan kaldı çünkü o zaten `olay.tip='vitrifikasyon'`
  üzerinden geliyor, sperm taşıyıcıları hiç `olay` satırı üretmiyor.
- **`sperm_dondurma`** (`goc_033`, yeni tablo) — `sperm_analiz` ile aynı
  kolon adlarıyla (`hacim_ml`, `konsantrasyon_milyon_ml`,
  `total_motil_yuzde`) dondurma öncesi semen analizini tutuyor,
  `tasiyici_id` ile taşıyıcı/konuma bağlanıyor. `hasta_id`'ye doğrudan
  bağlı — bir cycle'a değil, çünkü uzun süreli saklama belirli bir tedaviye
  ait olmayabilir (`sperm_ornek` gibi `cycle_id NOT NULL` olsaydı aynı
  günkü ICSI hazırlığı için tasarlanmış tabloyu yanlış amaçla kullanmış
  olurduk). **Bir kayıt = bir taşıyıcı** — embriyoda olduğu gibi birden çok
  örnek aynı taşıyıcıyı paylaşmıyor, bu yüzden silmede "kardeş var mı"
  kontrolüne gerek yok, taşıyıcı her zaman tek başına serbest kalıyor.
  `iptal_mi`/`iptal_kullanici_id`/`iptal_zamani`/`iptal_sebep` deseni
  `olay`'daki ile birebir aynı (CLAUDE.md "Silme = iptal işaretleme") —
  normal silme taşıyıcıyı ve konumu `vit_sil()`'deki gibi serbest bırakıyor
  (`durum='bosaltildi'`/`'bos'`), fiziksel silme yalnızca hasta kalıcı
  silinirken oluyor.
- **İzin: ayrı bir modül açılmadı.** Yeni bir modül CLAUDE.md'nin
  belgelediği üç yerlik törenle geliyor (`app.py` `MODULLER`, `goc_026.py`
  `MODULLER`, `kullanici.py` `MODULLER`, sonra `goc_026`'yı tekrar
  çalıştırmak) — Sperm Dondurma aynı personel grubunun işi olduğu için
  mevcut `"cryo"` izni yeniden kullanıldı (`yol_modulu()`'na
  `/sperm-dondurma*` ve `/hasta/{id}/sperm-dondurma/*` için `"cryo"`
  dönen iki dal eklendi). `MODULLER`'daki etiket "Cryo haritası (Embriyo /
  Sperm Dondurma)" olarak güncellendi ki yönetici kime bu izni verdiğini
  bilsin. **Kullanıcı ayrı bir izin isterse** bu ayrıma dönüp yeni bir
  modül açmak gerekir — bu, kullanıcıya sorulmadan alınmış bir tasarım
  kararı, bilerek buraya not edildi.
- **Silme rotası** `/sperm-dondurma/{id}/sil` — `sil` ile bittiği için
  `yol_modulu()` onu otomatik olarak `"silme"` modülüne bağlıyor, özel bir
  kural yazmaya gerek kalmadı.
- **Hasta kalıcı silindiğinde** (`hasta_sil()`, `eylem="sil"`) artık o
  hastanın `sperm_dondurma` kayıtları ve kendi taşıyıcıları da temizleniyor
  — `cycle_tamamen_sil()`'in taşıyıcı serbest bırakma adımının basiti
  (kardeş kontrolü yok, çünkü ilişki zaten 1:1). Bu eklenmeseydi tuzak
  #4'ün aynısı olurdu: `sperm_dondurma.hasta_id` FOREIGN KEY hatası verip
  hasta hiç silinemezdi.
- **`veri_damgasi()`'nin `DEGISIM_EK`'i** `sperm_dondurma` için de
  `olay`'daki gibi `COALESCE(SUM(iptal_mi), 0)` aldı — iptal işareti
  yerinde değiştiği için satır sayısı/`MAX(rowid)` onu yakalamıyor,
  `olay`'daki gerekçenin aynısı.
- **`/disari/tumu`** (yönetici, tam döküm) `TUM_TABLOLAR`'a `sperm_dondurma`
  eklendi — klinik bir kayıt, dökümde eksik kalmamalı.
- Menü: `_gezinme.html` `yan_ana()` ve `ana.html` `.anadugmeler`'e "Sperm
  Dondurma" bağlantısı Embriyo Dondurma'nın hemen altına eklendi (ikisi de
  `yetkim("cryo")` ile), CLAUDE.md'nin "ikisine birden ekle, aynı yazıyı
  kullan" kuralına uyarak. `base.html`'in `_aktif_menu` türetmesine
  `/sperm-dondurma` dalı eklendi. `hasta_detay.html`'e "Yeni Sperm
  Dondurma" düğmesi ("Yeni tedavi aç"ın altında).

## Yeni ekranlar

- `sperm_dondurma.html` — ana ekran, `cryo.html`'in basitleştirilmiş hali
  (arama + düz taşıyıcı listesi, tank özeti kartı yok — kapsam kullanıcının
  isteğiyle zaten sade tutuldu).
- `sperm_dondurma_form.html` — oluşturma formu, `vitrifikasyon.html`'in
  taşıyıcı/konum/zaman bloklarının aynısı + semen analizi kartı (mevcut
  `hacim_ml`/`konsantrasyon`/`total_motilite` `metin()` anahtarları
  `androloji.html`'den yeniden kullanıldı).
- `sperm_dondurma_detay.html` — salt okunur detay, `tasiyici.html`'in
  deseni.
- `sperm_dondurma_sil.html` — silme onayı, `vit_sil.html`'in deseni (SIL
  yazma zorunluluğu yok, bu kalıcı silme değil — normal iptal işaretleme).

## Test edildi

Sunucu ayağa kaldırıldı, gerçek bir sperm dondurma kaydı oluşturuldu (etiket,
tip, renk, konum, hacim/konsantrasyon/motilite, elle girilen saat) ve:
- `/sperm-dondurma`'da listelendi, `/cryo`'da (Embriyo Dondurma) **hiç
  görünmedi** (`kategori` süzgeci doğrulandı).
- Detay ekranında bütün alanlar doğru okundu.
- Aynı etikette ikinci kayıt denendi, "etiketli bir taşıyıcı zaten var"
  hatası döndü.
- Silme ekranından silindi: `iptal_mi=1`, taşıyıcı `durum='bosaltildi'`,
  konum `durum='bos'` oldu; `/sperm-dondurma` listesi tekrar boşaldı.
- Ayrı bir test hastasına yeni bir sperm dondurma kaydı açılıp hasta kalıcı
  silme akışından (`/hasta/{id}/sil`, dosya no + `SIL` onayıyla) geçirildi:
  `sperm_dondurma` satırı ve taşıyıcısı silindi, `PRAGMA foreign_key_check`
  temiz çıktı.
- Playwright ile hem telefon hem geniş ekran görüntüsü alındı: mobil menü
  ve masaüstü yan menüde "Embriyo Dondurma" ve "Sperm Dondurma" art arda,
  aktif sayfa doğru vurgulanıyor; form telefon genişliğinde düzgün akıyor.
- `goc_032` ve `goc_033` iki kez çalıştırılıp idempotent olduğu doğrulandı.
- Test verisi (kayıt, taşıyıcı, konum, test hastası, test oturumu) temizlendi.

# v6.85 — Cryo Haritası: Embriyo ve Sperm Dondurma tek ekranda, sperm için yeni hasta girişi

Kullanıcının isteği, v6.84'ün hemen ardından: "Sperm Dondurma ile Embriyo
Dondurma Cryo Harita başlığı altına toplansın. Cryo Harita içinde ikisinin
modülü yan yana olsun. Bir de Sperm Dondurma sadece tüp bebek tedavisi olan
hastalara yapılmıyor. Bazı durumlarda onkoloji tedavisi görecek erkek
hastalara da sperm donduruyoruz. O yüzden Cryo Harita içinden Sperm Dondurma
başlığından hasta kaydı yapılsın."

İki ayrı düzeltme:

## 1. Tek ekran, yan yana iki modül

v6.84'te Embriyo Dondurma ve Sperm Dondurma **iki ayrı ekrandı** (`/cryo` ve
`/sperm-dondurma`), ana menüde de iki ayrı bağlantı. Kullanıcı bunun yerine
tek bir "Cryo Haritası" başlığı altında ikisini yan yana istedi.

- **`cryo_haritasi` metni tekrar "Cryo Haritası" oldu** (v6.84'te "Embriyo
  Dondurma" idi) — artık ekranın kendisi ikisinin ortak başlığı, modül
  adları ayrı: yeni anahtar **`embriyo_dondurma`**, `sperm_dondurma`
  zaten vardı.
- **`cryo_harita()` (`/cryo`) artık sperm sorgusunu da çalıştırıyor** ve
  `cryo.html`'e ikisini birden veriyor. Şablon `.sutunlar` > iki `.sutun`
  kullanıyor (CLAUDE.md'nin "İki sütun" ölçüsü tam burada geçerli: iki
  bağımsız modül). Bölme noktası kaynak sırasında (embriyo sütunu önce) —
  telefonda alt alta dizilince sıra bozulmuyor.
- **Arama kutusu tek.** Aynı `ara` iki modülü de süzüyor — ayrı ayrı arama
  kutuları da düşünüldü ama dosya no/hasta adı araması çoğu zaman ikisi
  için de aynı arama, iki kutu gereksiz tekrar olurdu.
- **`GET /sperm-dondurma` artık `/cryo`'ya yönlendiriyor**, sayfayı basmıyor
  — eski bağlantı/yer imi kırılmasın diye rota duruyor ama içi boşaldı.
  `sperm_dondurma.html` şablonu silindi (içeriği `cryo.html`'e taşındı).
  Detay/oluşturma/silme rotaları (`/sperm-dondurma/{id}`,
  `/hasta/{id}/sperm-dondurma/yeni`, `/sperm-dondurma/{id}/sil`) dokunulmadı
  — onların "başarılı" yönlendirmeleri de `/sperm-dondurma` yerine doğrudan
  `/cryo`'ya güncellendi (gereksiz ekstra bir yönlendirme adımı olmasın diye).
- **Menü tek bağlantıya indi**: `_gezinme.html` `yan_ana()` ve `ana.html`
  `.anadugmeler`'den ayrı "Sperm Dondurma" satırı kaldırıldı, yalnızca
  "Cryo Haritası" kaldı. `base.html`'in `_aktif_menu` türetmesi `/cryo` ile
  başlayan ya da içinde `/sperm-dondurma` geçen (örn.
  `/hasta/3/sperm-dondurma/yeni`) her yolu artık **tek** `'cryo'` kimliğine
  eşliyor — ayrı bir `sperm_dondurma` menü kimliği kalmadı.
- CLAUDE.md'nin "İki sütun her ekranın çözümü değil" listesindeki `/cryo`
  girdisi "yalnızca genişleyen" kategorisinden "iki sütun" kategorisine
  taşındı.

## 2. Sperm Dondurma için tüp bebek hastası olmayan yeni hasta kaydı

Kullanıcının klinik gerekçesi: sperm dondurma yalnızca IVF/ICSI hastalarının
eşlerine değil, bazen onkoloji tedavisi öncesi erkek hastalara da yapılıyor
— bu hastaların bir IVF cycle'ı hiç olmayabilir.

- **`hasta` kaydı zaten cycle'dan bağımsız var olabiliyordu** (0 cycle'lı
  hasta desteklenen bir durum, `hasta_detay.html`'in "Bu hastada henüz
  tedavi yok" boş durumu buna kanıt) — eksik olan yalnızca giriş noktasıydı.
  Yeni bir tablo ya da form gerekmedi, mevcut `/hasta/yeni` formuna bir
  **"nereye git" parametresi** eklendi.
- **Cryo Haritası'nın Sperm Dondurma sütununa "Yeni hasta kaydı (Sperm
  Dondurma)" düğmesi eklendi** → `/hasta/yeni?amac=sperm`.
- **`amac` beyaz listeden geçiyor** (tuzak #9, `?geri=<yol>` yasağının aynı
  gerekçesi): tek geçerli değer `"sperm"`, her yerde (`GET`/`POST`
  `/hasta/yeni`, hata dönüşü, mükerrer dosya no uyarısının JS'i) doğrudan
  karşılaştırılıyor — adresten/formdan gelen metin hiçbir yerde doğrudan
  `href`'e ya da `RedirectResponse`'a yazılmıyor. Yeni fonksiyon
  `_hasta_sonrasi_yol(hasta_id, amac)` yolu **kendi kuruyor**:
  `amac == "sperm"` ise `/hasta/{id}/sperm-dondurma/yeni`, değilse eskisi
  gibi `/hasta/{id}`.
- **Kayıt başarılı olunca (ya da dosya no zaten varsa) doğrudan sperm
  dondurma formuna düşülüyor** — oncology hastası için ayrı bir "şimdi
  sperm dondurma ekranına git" tıklaması gerekmiyor.
- `hasta_form.html`'e `amac == "sperm"` iken küçük bir bilgi notu eklendi
  ("Bu hasta yalnızca sperm dondurma için kaydediliyor olabilir...") —
  personel neden bu formun IVF dışı bir hasta için açıldığını anlasın diye.
  Geri oku da `amac`'e göre değişiyor (`/cryo` ↔ `/hastalar`).

## Test edildi

Sunucu ayağa kaldırıldı:
- `/cryo` iki sütunlu açıldı, Embriyo Dondurma ve Sperm Dondurma yan yana
  görüldü (Playwright, hem 1400px hem 420px genişlikte — telefonda embriyo
  sütunu üstte, sperm altta, sıra bozulmadı).
- `GET /sperm-dondurma` → `303` → `/cryo` doğrulandı.
- `/hasta/yeni?amac=sperm` formu bilgi notuyla açıldı, gizli `amac` alanı
  doğru taşındı (Playwright ekran görüntüsü).
- Yeni bir "oncology" test hastası `amac=sperm` ile oluşturuldu: yönlendirme
  doğrudan `/hasta/{id}/sperm-dondurma/yeni`'ye gitti (hasta ekranına
  **uğramadan**). Bir sperm dondurma kaydı girildi, `/cryo`'nun sperm
  sütununda listelendi, embriyo sütununda **hiç görünmedi**.
- `amac` alanına `javascript:alert(1)` gibi rastgele bir değer denendi:
  beyaz listeden geçmediği için normal `/hasta/{id}` yönlendirmesine
  düştü — enjeksiyon riski doğrulanarak kapatıldı.
- Test verisi (sperm dondurma kaydı, taşıyıcı, konum, iki test hastası, test
  oturumu) temizlendi, `PRAGMA foreign_key_check` temiz.

# v6.86 — Sperm Dondurma: erkek hasta formu, dondurma sebebi, eşin tedavisine bağlama

Kullanıcının isteği: "Cryo Harita içindeki Yeni hasta kaydı (Sperm Dondurma)
da sadece erkek hasta bilgileri olsun. Dondurma sebebi olsun ve
.../hasta/1/sperm-dondurma/yeni sayfasındaki veri girilecek alanlar olsun.
Bu hasta ileride evlenir ve tüp bebek yaparsa eşine yeni hasta olarak kayıt
açılırsa bu dondurmayı o tedaviye bağlayabileyim ve orada sperm dondurma
tedavisi olarak görünsün."

Üç parça:

## 1. Tek ekranda erkek hasta + dondurma kaydı

v6.85'teki "Yeni hasta kaydı (Sperm Dondurma)" düğmesi genel `/hasta/yeni`
formuna gidiyordu (eş alanları dahil), sonra ayrı bir adımda sperm dondurma
formuna geçiliyordu. Artık **tek ekran**: `/sperm-dondurma/yeni-hasta`.

- **`hasta_form.html`'in eş alanları (eş adı/doğum tarihi) yok** — bu hasta
  bir IVF tedavisi görmüyor olabilir (onkoloji öncesi sperm dondurma gibi),
  eş sorması yanlış varsayım olurdu.
- Hasta alanları (dosya no, ad soyad, doğum tarihi) + dondurma sebebi +
  `/hasta/{id}/sperm-dondurma/yeni`'deki bütün alanlar (taşıyıcı, konum,
  semen analizi, dondurma saati) **tek formda**, tek POST'ta.
- **Doğrulama yazmadan önce bitiyor, hata dönüşü formu boşaltmıyor**
  (v6.21 kuralı) — bu form uzun olduğu için (4 kart) kaybı özellikle can
  sıkıcı olurdu; önceki `/hasta/yeni?amac=sperm` denemesi (v6.85) bunu
  atlamıştı, bu sürümde düzeltildi.
- **Kayıt açıp doldurma kuralı** (CLAUDE.md, denüdasyonun `specimen`+
  `goruntu` deseninin aynısı): önce `hasta` yazılıyor, sonra taşıyıcı +
  `sperm_dondurma`. İkincisi doğrulama hatasıyla patlarsa (örn. mükerrer
  etiket) **az önce açılan boş hasta kaydı geri alınıyor** — yoksa lab
  hiçbir kaydı olmayan ıssız hasta dosyalarıyla dolar. Test edildi: mükerrer
  etiketle deneme yapıldı, hasta sayısı değişmedi.
- Ortak yazma mantığı yeni bir yardımcıya çıkarıldı:
  `_sperm_dondurma_olustur(hasta_id, f, kid)` — hem mevcut hastanın kendi
  "Yeni Sperm Dondurma"su hem bu yeni akış onu çağırıyor, iki kopya
  birbirinden ayrı düşmesin diye.
- `/hasta/yeni?amac=sperm` (v6.85) kaldırıldı — artık gereksiz, kod
  sadeleşti.

## 2. Dondurma sebebi

`sperm_dondurma.sebep` (`goc_034`, yeni kolon) — **serbest metin**, sabit
bir `liste_degeri` açılmadı. Gerekçe: hangi klinik kategorilerin
("onkoloji", "elektif" gibi) olacağı kullanıcıyla birlikte belirlenmesi
gereken bir karar (CLAUDE.md "klinik bir varsayım yapman gerekiyorsa
yapma"), serbest metin bu kararı ileriye erteliyor ve `notlar` alanlarıyla
aynı, zaten tanıdık bir desen. Hem yeni-hasta formunda hem mevcut hastanın
"Yeni Sperm Dondurma" formunda (`sperm_dondurma_form.html`) var; detay
ekranında (`sperm_dondurma_detay.html`) ve androloji ekranındaki bağlantı
kartında da gösteriliyor.

## 3. Dondurulmuş spermi eşin tedavisine bağlama

`sperm_dondurma.kullanim_cycle_id` (`goc_034`, yeni kolon, `cycle(id)`'ye
FK) — embriyo tarafındaki `olay.thaw_cycle_id` deseninin aynısı: **sahiplik
değişmiyor** (`sperm_dondurma.hasta_id` hep erkek hastada kalıyor), yalnızca
"hangi tedavi için kullanıldı" sorusu ayrı bir alanda yanıtlanıyor.

- **Bağlama yeri: Androloji ekranı** (`/cycle/{id}/androloji`, yalnızca
  `ivf_icsi` tedavilerinde var). Taze örnekten (`sperm_ornek`+
  `sperm_analiz`) tamamen bağımsız yeni bir kart: "Sperm Dondurma". Boşsa
  "Dondurulmuş sperm bağla" düğmesi `/cycle/{id}/androloji/sperm-baglama`'ya
  gidiyor — **bütün laboratuvardaki**, henüz hiçbir tedaviye bağlanmamış
  dondurulmuş sperm kayıtlarını arayıp listeleyen bir ekran (dosya no/ad
  soyad/etiket ile). "Bağla" düğmesi `sperm_dondurma.kullanim_cycle_id`'yi
  bu tedaviye yazıyor ve taşıyıcının `durum`'unu `'kullanildi'` yapıyor
  (yeni bir üçüncü durum — `'dolu'`/`'bosaltildi'`'nin yanına: "dolapta" ile
  "boşaltıldı" arasında, "bir tedavide kullanıldı" ayrı bir bilgi).
  Bağlıyken kart bağlı kaydı gösteriyor, "Bağlantıyı kaldır" düğmesiyle geri
  alınabiliyor (taşıyıcı `'dolu'`ya döner).
- **Neden Androloji, Tedavi ekranı değil**: androloji zaten "bu tedavide
  hangi sperm örneği kullanıldı" sorusunun sorulduğu yer, `ivf_icsi` dışı
  tedavilerde (FET, oosit dondurma) zaten hiç görünmüyor — sperm dondurma
  bağlantısı da klinik olarak yalnızca ICSI yapılan tedavilerde anlamlı.
- **`/cryo`'nun Sperm Dondurma sütunu ve `/sperm-dondurma/{id}` detay
  ekranı** bağlı olduğu tedaviyi de gösteriyor ("Kullanıldığı tedavi: dosya
  no · ad soyad · cycle no") — hem taşıyıcıyı arayan embriyoloğa hem kaydın
  kendisine bakan birine "bu nerede kullanıldı" sorusunu yanıtlıyor.
- **Tuzak #4'ün aynısı, yeni bir cycle_id alanı için.** `cycle_tamamen_sil()`
  şimdi bu tedaviye bağlı `sperm_dondurma` kayıtlarının bağını koparıyor
  (`kullanim_cycle_id=NULL`, taşıyıcı `'dolu'`ya döner) — eklenmeseydi eşin
  tedavisi kalıcı silindiğinde (kendi hastası ya da eşininki üzerinden)
  `sperm_dondurma` kırık bir `cycle_id`ye işaret ederdi. `teshis_silme.py`'ye
  de aynı tarama + geri alma adımı eklendi (bu araç yalnızca **dener**, hiçbir
  şey silmez — CLAUDE.md'nin "aynısını teshis_silme.py'ye de ekle" kuralı).
  Test edildi: eşin hastası + tedavisi açıldı, kocanın (başka hasta) sperm
  dondurması o tedaviye bağlandı, eşin hastası **kalıcı** silindi — kocanın
  sperm dondurma kaydı korundu, yalnızca bağlantısı koptu, taşıyıcı `'dolu'`ya
  döndü, `PRAGMA foreign_key_check` temiz çıktı.

## Test edildi

- Yeni-hasta formu: erkek hasta + dondurma kaydı tek POST'ta oluşturuldu,
  `/sperm-dondurma/{id}` detayına yönlendirildi.
- Doğrulama hatası (boş alan, mükerrer etiket) formu **yazılanları koruyarak**
  yeniden bastı; mükerrer etiket denemesinde az önce açılan hasta kaydı geri
  alındığı doğrulandı (hasta sayısı değişmedi).
- Mükerrer dosya no ile deneme "zaten var" hatası verdi.
- Androloji ekranında "Sperm Dondurma" kartı boş durumda "bağlı yok" gösterdi;
  bağlama ekranı kaydı listeledi; "Bağla" sonrası kart bağlı kaydı gösterdi,
  `/cryo` ve detay ekranı "Kullanıldığı tedavi"yi doğru gösterdi, taşıyıcı
  `durum='kullanildi'` oldu; "Bağlantıyı kaldır" sonrası hepsi eski haline
  döndü (`durum='dolu'`).
- Kalıcı silme kaskadı: eşin hastası + tedavisi silindiğinde kocanın (başka
  hastaya ait) sperm dondurma kaydı korundu, yalnızca bağlantısı koptu;
  `PRAGMA foreign_key_check` temiz.
- `goc_034` iki kez çalıştırılıp idempotent olduğu doğrulandı.
- Playwright ile yeni-hasta formu, androloji kartı, bağlama ekranı ve detay
  ekranı görüntülendi — telefon genişliğinde düzgün akıyor.
- Test verisi (sperm dondurma kayıtları, taşıyıcılar, konumlar, test
  hastaları/tedavileri, test oturumu) temizlendi.

# v6.87 — Tüm Hastalar sayfalandı

Kullanıcının sorusu: "binlerce hasta olunca yavaşlar mı" — cevapta
`/hastalar`'daki "Tüm Hastalar" kartının hiçbir sınır (`LIMIT`) olmadan
aktif hastaların **tamamını** tek seferde bastığını, bunun asıl sorunun
SQL sorgusunun yavaşlığı değil, hasta sayısı arttıkça telefonun o kadar
satırı ekrana basarken zorlanması olduğunu söyledim. Kullanıcı "şimdiden
ekle" dedi.

## Ne değişti

- **`hastalar()` (`app.py`)**: yeni `sayfa` parametresi, `TUM_HASTALAR_
  SAYFA_BOYU = 50`. Arama **boşken** "Tüm Hastalar" artık `LIMIT ? OFFSET
  ?` ile 50'şer 50'şer geliyor; toplam sayfa sayısı ayrı bir `COUNT(*)`
  ile hesaplanıp `sayfa` o aralığa **sunucuda** sabitleniyor (`min(max(sayfa,
  1), toplam_sayfa)`) — adresten `?sayfa=9999` gibi bir değer gelirse son
  sayfaya düşer, hataya değil.
- **Arama sonucu sayfalanmadı.** Zaten süzülmüş, küçük bir liste —
  gereksiz karmaşıklık olurdu. `ara` doluyken "Tüm Hastalar" sorgusu artık
  **hiç çalışmıyor** (`gereksiz sorgu atılmasın diye` — arşiv modunun zaten
  uyduğu kurala Tüm Hastalar da uydu).
- **Ay/yıl gizli alanlarda korunuyor**: sayfa değiştirince sol sütundaki
  ay seçimi kaybolmasın diye Önceki/Sonraki bağlantıları `yil`/`ay`'i de
  taşıyor. Ay veya arama değişince `sayfa` adresten düşer, kendiliğinden
  1'e döner — ayrı bir sıfırlama kodu yazmaya gerek kalmadı.
- **Görünüm**: `/hastalar`'daki ay gezgininin (`‹ Eylül 2026 ›`) aynı
  kutusu (`.aygezgin`) yeniden kullanıldı, ortada seçici yerine düz
  "Sayfa 3 / 42" metni (`.sayfabilgi`, yeni bir küçük CSS kuralı). Sayfa 1
  ya da son sayfadayken ilgili ok `<span>` olarak basılıp gizli kalıyor —
  aynı kutunun genişliği bozulmasın diye boş bir `<a>` değil.
- Başlığa sayı da eklendi: "Tüm Hastalar (121)" — kaç aktif hasta olduğu
  sayfalar arasında gezmeden görünsün diye.

## Test edildi

120 test hastası eklendi (121 aktif hasta oldu, 3 sayfa): sayfa 1/2/3
doğru 50'şer/50'şer/21 kayıt gösterdi, `?sayfa=99` gibi aralık dışı bir
değer son sayfaya (3) sabitlendi, arama doluyken sayfalama hiç görünmedi.
Playwright ile sayfa gezgini görüntülendi — ay gezginiyle aynı görünümde,
telefon genişliğinde düzgün. Test hastaları temizlendi,
`PRAGMA foreign_key_check` temiz.

# v6.88 — Ay listesi de sayfalandı

Kullanıcının isteği, v6.87'nin hemen ardından: "Tüm Hastalar yanındaki
aylık tedavilerin olduğu yerde aynı şekilde olsun."

## Ne değişti

- **`cycle_listesi()`'ye üç yeni, hepsi isteğe bağlı parametre**: `limit`,
  `offset`, `sayisi`. `limit` verilmezse (varsayılan `0`) davranış aynen
  eskisi gibi sınırsız — bu fonksiyonu çağıran 5 yerin (ana ekran,
  `/bitenler`, `/yaklasanlar`, ikisi daha) hiçbiri bunları vermiyor,
  dokunulmadılar. `sayisi=True` satırları değil toplam sayıyı döndürüyor
  (aynı `kosullar` üzerinden — sayfa sayısını hesaplamak için ikinci bir
  sorgu yazmaya gerek kalmadı). CLAUDE.md'nin "bütün cycle listeleri tek
  fonksiyon" kuralına uyuldu: ayrı bir sorgu yazmak yerine mevcut
  fonksiyona kip eklendi.
- **`hastalar()`**: yeni `aysayfa` parametresi, `TUM_HASTALAR_SAYFA_BOYU`
  → `HASTALAR_SAYFA_BOYU` olarak yeniden adlandırıldı (artık iki liste de
  aynı sabiti kullanıyor). Ay listesi `cycle_listesi(ay=..., sayisi=True)`
  ile toplam sayıyı, `cycle_listesi(ay=..., limit=..., offset=...)` ile o
  sayfanın satırlarını alıyor. `aysayfa` da Tüm Hastalar'ın `sayfa`'sı gibi
  sunucuda `[1, toplam_sayfa]`'ya sabitleniyor.
- **İki sayfa numarası birbirinden bağımsız** (`sayfa` / `aysayfa`) ama
  gezinme bağlantıları ikisini de taşıyor — bir listede sayfa değiştirmek
  ötekinin konumunu sıfırlamasın diye (`yil`/`ay` zaten taşınıyordu, aynı
  gerekçe).
- **Başlık artık `liste|length` değil `ay_sayisi` kullanıyor**
  (`say("n_cycle_ayda", ay_sayisi)`) — `liste` artık yalnızca o sayfanın
  satırlarını taşıyor, uzunluğu toplamı yanlış gösterirdi (örn. 122
  tedavi varken "50 tedavi" yazardı).
- Görünüm Tüm Hastalar'ın sayfa gezginiyle birebir aynı: `.aygezgin`
  kutusu, ortada "Sayfa 2 / 3" metni (`.sayfabilgi`, v6.87'de eklenmiş
  CSS kuralı yeniden kullanıldı, yeni bir kural gerekmedi).

## Test edildi

Bu ay için 120 test tedavisi eklendi (122 tedavi, 3 sayfa): sayfa 1/2/3
doğru 50'şer/50'şer/22 kayıt gösterdi, başlık her sayfada doğru "122
tedavi" yazdı (kırpılmış sayı değil), `?aysayfa=999` gibi aralık dışı bir
değer son sayfaya sabitlendi. Tüm Hastalar tarafında yalnızca 1 aktif hasta
olduğu için o listenin sayfa gezgini hiç görünmedi — iki liste birbirinden
gerçekten bağımsız çalıştığı doğrulandı. Playwright ile geniş ekran
görüntülendi. Test tedavileri temizlendi, `PRAGMA foreign_key_check` temiz.

# v6.89 — Hasta kartında tedavinin yapıldığı yıldaki yaş

Kullanıcının isteği: hasta kartındaki tedavi satırlarında hastanın o
tedaviyi yaptığı yıldaki yaşı görünsün.

## Ne değişti

- **`app.py`'de yeni Jinja global `tedavi_yasi(dogum_tarihi, tarih)`**:
  tam yaş değil, yalnızca **yıl farkı** (`tedavi_yili - dogum_yili`).
  Kullanıcının sorduğu "o yıl kaçındaydı" sorusu doğum günü öncesi/sonrası
  ay/gün karşılaştırmasını gerektirmiyor — `gg_aa_yyyy()` grubundaki öteki
  yardımcılar gibi ISO tarihten yıl okuyup çıkarıyor. Tarihlerden biri boş
  ya da okunamıyorsa `None` döner, şablon o zaman hiçbir şey basmaz (yeni
  hasta kaydı, doğum tarihi girilmemiş — sessizce çıplak "yaşında" yazmaz).
- **Tedavi yılı ölçüsü `/hastalar`'ın ay listesindeki ölçüyle aynı**:
  `c.opu_zamani`, yoksa `c.olusturma_zamani` (FET'te OPU yok). CLAUDE.md'nin
  "Hasta kartında tedaviler ... klinik tarih alanıyla DEĞİL" kuralı burada
  geçerli değil — o kural **sıralama** için (`hasta_cycle_no`), bu ise
  **görüntülenen bir değer**; iki alan farklı amaçlara hizmet ediyor.
- **`templates/hasta_detay.html`**: her tedavi satırının `meta` bilgisine
  `· 36 yaşında` ekleniyor (`metinler.py`'de yeni `n_yas` anahtarı, "N
  yaşında" / "age N", `say()` ile sayı biçimlendiriliyor — projedeki `say()`
  deseninin aynısı).

## Test edildi

Test hastasına geçici doğum tarihi (1990) verilip iki tedavi satırında
doğru yaş (36) göründüğü doğrulandı; doğum tarihi boşken satırın hiçbir
şey basmadığı (boş `·` kalmadığı) ayrıca kontrol edildi. `say()` çıktısı
`en` ve `tr` dillerinde elle çağrılıp doğrulandı. Playwright ile telefon
genişliğinde ekran görüntülendi. Test verisi (doğum tarihi, oturum jetonu)
temizlendi.

# v6.90 — Denüdasyonda OPU'da toplanan oosit başlık olarak görünür

Kullanıcının isteği: denüdasyon öncesi OPU kaydında girilen oosit sayıları,
denüdasyon ekranında başlık/bilgi olarak görünsün — embriyolog oosit
girerken kaçının toplandığını yeniden OPU ekranına gitmeden görebilsin.

## Ne değişti

- **`templates/denudasyon.html`**: ekranın en üstüne, hasta kimliğinin hemen
  altına salt okunur bir kart eklendi — "OPU'da toplanan oosit" başlığıyla
  sağ/sol over sayıları ve toplam. Rota değişmedi: `c` zaten `SELECT c.*`
  ile geliyor, `opu_sag_oosit`/`opu_sol_oosit` hazır duruyordu.
- **Kart `_bilgikart.html`'in mevcut `kart()` makrosuyla** basılıyor,
  `duzenle_yolu` verilmeden — CLAUDE.md'nin "androloji gibi bölüm kartları"
  deseni: salt bilgi, düğmesiz. Sayıları **değiştirmek burada değil**, OPU
  ekranında oluyor; denüdasyon yalnızca referans veriyor.
  Değerler boşsa `kart()`'ın kendi "girilmedi" davranışı devreye giriyor —
  OPU henüz doldurulmamışsa embriyolog bunu burada da görüyor.
- **Kart hem görüntüleme hem `?duzenle=oosit` çalışma kipinde aynı yerde**
  duruyor — kamera kuyruğuyla oosit girerken de OPU referansı ekrandan
  kaybolmuyor.
- Yeni metin anahtarı: `opu_ozet_baslik` ("OPU'da toplanan oosit" /
  "Oocytes collected at OPU"); satır etiketleri OPU ekranındaki
  `sag_overden_oosit`/`sol_overden_oosit`/`toplanan_oosit` anahtarlarının
  aynısı — aynı sayı iki ekranda farklı adla anılmasın diye.

## Test edildi

Test cycle'ında OPU'ya 5 sağ + 4 sol oosit girilmişti; denüdasyon ekranında
kart "Sağ overden toplanan oosit 5 / Sol overden toplanan oosit 4 / Toplanan
oosit 9" gösterdi. Hem salt görüntüleme hem `?duzenle=oosit` çalışma
kipinde Playwright ile telefon genişliğinde ekran görüntülendi, kart doğru
yerde ve doğru sayılarla çıktı. Test oturum jetonu temizlendi, hiçbir
veri değişmedi (yalnızca okuma).

# v6.91 — Denüdasyonda OPU sayısınca oosit kaydı hazır dursun

Kullanıcı v6.90'ı **reddetti**: "Hayır denüdasyona oosit1 oosit2 şeklinde
dizilsin. Hazır olsun daha sonra resim ekleyebilirim." İstenen salt bilgi
kartı değilmiş — OPU'da kaç oosit toplandıysa o kadar **gerçek oosit kaydı**
(numara şeridinde 1, 2, 3...) fotoğrafsız hazır dursun, fotoğraf her birine
sonra tek tek eklensin. v6.90'ın kartı bu yüzden kaldırıldı.

## Ne değişti

- **`templates/denudasyon.html`**: v6.90'daki salt okunur OPU kartı
  kaldırıldı. Yerine, `kayıtlı oosit sayısı < OPU'da toplanan sayı` olduğu
  sürece görünen tek bir düğme geldi: "N oosit için kayıt hazırla". Basınca
  eksik kadar oosit **fotoğrafsız** açılıyor (`kr.yer()` zaten "fotoğrafsız
  örnek boş alan bırakmaz" kuralını uyguluyor — CLAUDE.md), her biri
  numara şeridinde kendi yerinde, "Fotoğraf ekle" bağlantısıyla hazır.
  Düğme hem görüntüleme hem `?duzenle=oosit` çalışma kipinde aynı yerde,
  kamera akışının hemen üstünde.
- **`app.py`'de yeni `eylem="hepsi"`** (`denudasyon_islem`): OPU toplamı
  (`opu_sag_oosit + opu_sol_oosit`) ile mevcut specimen sayısını karşılaştırıp
  yalnızca **eksik** kadarını `goruntuler.specimen_olustur()` ile açıyor —
  düğmeye ikinci kez basmak fazladan oosit açmaz, zaten var olanları
  saymadan üstüne eklemez. Numaralandırma ve `denudasyon_zamani` otomatik
  doldurma zaten `specimen_olustur()`'ün içinde, buraya yeni bir mantık
  yazılmadı.
- **`taraf` (sağ/sol over) bilerek atanmadı.** OPU yalnızca toplam sayıyı
  veriyor, hangi oositin hangi overden geldiğini sıra numarasından çıkarmak
  klinik bir varsayım olurdu — CLAUDE.md'nin "klinik bir varsayım yapman
  gerekiyorsa yapma" kuralı. Taraf, var olan akışla (`?duzenle=oosit`
  içindeki Sağ/Sol/Belirtme düğmeleri) embriyolog tarafından elle giriliyor.
- **"Hepsi" kamera akışının parçası değil** — kayıttan sonra `?duzenle=oosit`
  yerine salt görüntülemeye dönüyor (`RedirectResponse` özel durumu), çünkü
  amaç kamera kuyruğuyla fotoğraf eklemek değil, boş kayıtları açmak;
  fotoğraflar sonra her oosit için ayrı ayrı "Fotoğraf ekle" ile ekleniyor.
- v6.90'ın `opu_ozet_baslik` metin anahtarı kaldırıldı (kullanılmıyor);
  yerine `n_oosit_hazirla` / `n_oosit_hazirla_tekil` / `oosit_hazirla_ipucu`
  eklendi.

## Test edildi

Test cycle'ında (OPU: 5 sağ + 4 sol = 9, 1 oosit zaten elle kaydedilmişti)
düğme doğru "8 oosit için kayıt hazırla" yazdı; basınca `2026-0001-02`
… `-09` sırayla açıldı, toplam 9 specimen, hepsi fotoğrafsız ve `taraf`
boş. Ardından numara şeridi 1-9 gösterdi, her biri "Oosit N" yer
tutucusuyla ve "Fotoğraf ekle" bağlantısıyla hazır; oosit 5 seçilip
kaydın doğru geldiği ayrıca kontrol edildi. Düğme, tüm oositler açıldıktan
sonra (eksik=0) ekrandan kayboldu. Playwright ile telefon genişliğinde
ekran görüntülendi. Test verisi (fazladan 8 specimen, oturum jetonu)
temizlendi.

# v6.92 — Fotoğraf yanlış eşleşmesi: goruntu.id yeniden kullanılıyordu

Kullanıcının bildirdiği hata: "Denüdasyon ve ICSI'de oosit resmi
yüklediğim zaman yüklediğim resim dışında başka bir resim yükleniyor. 2.
ve 3. oositlerde oluyor."

## Sebep

`goruntu.id` (her fotoğrafın kimliği, `/dosya/{id}` adresinde doğrudan
kullanılıyor) `INTEGER PRIMARY KEY` olarak tanımlıydı, `AUTOINCREMENT`
**değil**. SQLite'ın standart kuralı: yeni satırın id'si "tablodaki en
büyük id + 1"dir. Tablodaki en büyük id'ye sahip satır silinirse, o
numara **boşa çıkar** ve bir sonraki INSERT onu yeniden kullanır.

Elle doğrulandı: bir cycle'da 3 fotoğraf vardı (id 1, 2, 3). id=3
(`Bu fotoğrafı sil` ile) silindi, ardından farklı bir oosite yeni bir
fotoğraf yüklendi — yeni kayıt **id=3'ü yeniden aldı**, önceki tamamen
farklı fotoğrafın kimliğini. Tarayıcı o id'yi daha önce görmüşse
(`/dosya/3`'ü bir kez açtıysa) önbellekten **eski, silinmiş fotoğrafı**
gösterebiliyor — kullanıcının gördüğü "yüklediğim resim dışında başka
bir resim" tam olarak bu. 2. ve 3. oosit gibi üzerinde en son
çalışılan, dolayısıyla yanlış çekilip silinip yeniden eklenmesi en
olası kayıtlarda ortaya çıkması da bununla tutarlı — bu tam olarak "son
eklenen fotoğrafı sil, doğrusunu ekle" anının kendisi.

## Ne değişti

- **`goc_035.py`** (yeni göç): `goruntu` tablosu `id INTEGER PRIMARY KEY
  AUTOINCREMENT` ile yeniden kuruluyor (goc_016/017/031'deki "SQLite CHECK/
  kısıt sonradan eklenemez, tablo yeniden oluşturulur" yöntemiyle). Veri ve
  id'ler **aynen** korunuyor, indeksler (`idx_goruntu_cycle`,
  `idx_goruntu_specimen`) yeniden kuruluyor. `AUTOINCREMENT` SQLite'a ayrı
  bir sayaç (`sqlite_sequence`) tutturuyor — bir id silindikten sonra bir
  daha asla verilmiyor.
- Kod tarafında değişiklik **yok** — sorun tamamen şema kısıtındaydı,
  `elle_ekle()`/`goruntu_bagla()`/`/dosya/{id}` hep doğru çalışıyordu, id
  üretimi yanlıştı.
- **CLAUDE.md'ye tuzak #13 eklendi**: yeni bir tabloda kimliği doğrudan
  URL'e yazılan (yani "silinip yeniden verilirse eski içerik önbellekten
  görünebilir" riski taşıyan) bir `id INTEGER PRIMARY KEY` kolonu açılırsa
  `AUTOINCREMENT` eklenmesi gerektiği not edildi.

## Test edildi

Göç öncesi hatayı elle üretip doğrulandı (id=3 silinip yeni fotoğraf
id=3'ü yeniden aldı). `goc_035.py` çalıştırıldı: 3 kayıt, en büyük id 3,
kırık referans 0. İkinci kez çalıştırılıp idempotent olduğu ("zaten
AUTOINCREMENT") doğrulandı. Göç sonrası aynı senaryo tekrarlandı: id=3
silinip yeni fotoğraf yüklendiğinde kayıt artık **id=4** aldı, id=3 bir
daha hiç verilmedi. Üç farklı renkte (kırmızı/yeşil/mavi) test görüntüsü
üç oosite yüklenip piksel içerikleri doğrulandı — arka planda başka bir
karışma olmadığı ayrıca kontrol edildi. Test fotoğrafları, fazladan
specimen'ler, arşiv klasörü ve oturum jetonları temizlendi.

# v6.93 — Kaçırılan ISO tarih/saat gösterimleri düzeltildi

Kullanıcının isteği: "Tarih yazan her yeri gün ay yıl olarak değiştir."
v6.64/v6.67'de ekranların büyük çoğunluğu `gg_aa_yyyy()` /
`gg_aa_yyyy_saat()`'e geçirilmişti; tüm şablonlar tek tek tarandığında o
taramanın kaçırdığı **22 dosyada 25 yer** bulundu — hepsi ham ISO
(`2026-09-09 08:15:00` gibi) ya da elle `[:16]` dilimlenmiş biçimde
basıyordu.

## Ne değişti

Hepsi `{{ alan }}` → `{{ gg_aa_yyyy_saat(alan) }}` (saat taşıyanlar) şeklinde
düzeltildi, davranış değişmedi — yalnızca gösterim:
- **Silme onay ekranları** (kayıt zamanını gösteren `dt/dd` satırı):
  `arsiv_sil`, `blast_sil`, `cleavage_sil`, `fert_sil`, `icsi_sil`,
  `thaw_sil`, `transfer_sil`, `vit_sil`, `goruntu_sil`.
- **"Transfer kaydı olan silinemez" uyarı listesi**: `cycle_sil`,
  `hasta_sil` (`t.zaman`).
- **Aşama bilgi kartları** (`bk.kart()` satırları): `opu.html` (OPU zamanı),
  `denudasyon.html` (denüdasyon saati), `blast.html`/`cleavage.html`/
  `fert.html`/`icsi.html` (işlem saati), `androloji.html` (alınma/
  likefaksiyon/hazırlama zamanı + bazal ve hazırlık-sonrası analiz zamanı —
  5 ayrı satır).
- **`cycle_detay.html`**: "Zamanlar" kartındaki hCG/OPU/Denüdasyon satırları
  (önceden `c.opu_zamani or 'girilmedi'` gibi ham ISO basıyordu) ve zaman
  çizelgesi tablosundaki `z.zaman[:16]`.
- **`cycle_thaw.html`** (çözme kaydı bilgi kartı) ve **`transfer.html`**
  (transfer saati) — `e.zaman[:16]` / `e.zaman`.
- **`gebelik.html`**: transfer listesindeki ve beta hCG satırlarındaki zaman.
- **`istatistik.html`**: "Son kayıtlar" listesindeki `k.z[:16]`.

## Dokunulmayanlar (bilinçli)

- **`type="date"`/`type="datetime-local"` form alanlarının `value`'su** —
  CLAUDE.md'nin istisnası: tarayıcı zaten kendi yerel biçiminde gösteriyor,
  `value` ISO kalmalı. `dt()`/`dz()` macroları, `kz[:16]|replace(' ','T')`
  kalıpları hep form değeriydi, dokunulmadı.
- **ISO karşılaştırmalar** (`c.planlanan_tarih[:10] > bugun`,
  `{% if c.denudasyon_zamani %}` gibi) — görüntüleme değil, mantık.
- **Resmî formlar (`/form/...`) ve Excel çıktıları.** `formlar.py`'deki
  `opu_tarihi`/`transfer_tarihi`/`saat_<asama>` gibi alanlar hem yazdırılan
  HTML'e hem Excel hücresine **aynı** ham ISO değerle gidiyor —
  `excel.py`'nin hücre türünü ISO metinden çıkarma mekanizması (v6.36) buna
  dayanıyor. Bu değeri gün.ay.yıl'a çevirmek Excel çıktısındaki tarih
  hücrelerinin **tür algısını bozar**. Kullanıcıya sorulmadan bu ayrımı
  bozmadım — yalnızca yazdırma ekranındaki görünümü değiştirmek istenirse
  (Excel'e dokunmadan) ayrı bir iş: `form_kalip.satirlar()`'ın HTML yolu
  Excel'e giden değerden ayrılmalı. **Ona sormadan yapılmadı**, ayrı bir
  istek gerekir.

## Test edildi

Bütün şablonlar (`env.get_template()` ile 71 dosya) değişiklik sonrası
hatasız derlendi. Sunucu ayağa kaldırılıp gerçek verilerle kontrol edildi:
`/cycle/1` "Zamanlar" kartı ve OPU/Denüdasyon ekranlarındaki bilgi kartları
artık "09.09.2026 08:15" biçiminde basıyor (önceden "2026-09-09 08:15:00").
Bir test fotoğrafı yüklenip `/goruntu/{id}/sil` ekranında "Zaman" satırının
"17.09.2026 13:09" gibi doğru biçimde çıktığı doğrulandı. Test fotoğrafı,
arşiv klasörü ve oturum jetonu temizlendi.

# v6.94 — Resmî formlara aktarılan tarihler de gün.ay.yıl

Kullanıcının isteği: "Formlara aktarım sırasında tarihler ters çıkıyor.
Gün ay yıl olarak çıksın." v6.93'te ekranlar düzeltilmişti; resmî formlar
(Embriyoloji Özet, ART Lab. Raporu) ve laboratuvarın kendi yüklediği form
o taramanın **dışında** bırakılmıştı, çünkü aynı dolgu hem yazdırılan
sayfaya hem Excel'e gidiyor ve Excel'in ISO tarihi otomatik tarih hücresine
çevirme mekanizması (v6.36) buna dayanıyor sanılıyordu — bu sefer önce o
varsayım test edildi.

## Neden güvenli olduğu doğrulandı

`excel.py`'nin `_hucre()`'sindeki ISO algılaması yalnızca hücrenin biçimi
**`_DUZ` (varsayılan) olduğunda** çalışıyor. Resmî formların "yerleşim"
sayfasında (`_yerlesim_xml()`) her hücre **kâğıdın kendi kalıp stilini**
taşıyor (`bicim = taban + stil_no`) — hiçbir zaman `_DUZ` değil. Yani bu
hücreler zaten hep düz metin (`inlineStr`) olarak yazılıyordu, ISO
biçiminin "akıllı" tarih algısı buraya hiç uygulanmıyordu. Doğrulama:
`/disari/form/ozet/1` indirilip `xl/worksheets/sheet1.xml` içinde OPU
tarihinin hücresi incelendi — `t="inlineStr"` olarak duruyordu, biçim
`YYYY-MM-DD` iken de `DD.MM.YYYY` iken de fark etmiyor. Değeri
değiştirmek Excel'in tür algısını **bozmuyor**.

## Ne değişti

- **`formlar.py`'ye iki yeni yerel yardımcı**: `_gg_aa_yyyy()` ve
  `_gg_aa_yyyy_saat()` — `app.py`'deki aynı adlı globallerin küçük bir
  kopyası (döngüsel import olmasın diye; `formlar.py` `app.py`'den
  bağımsız bir modül). `_zaman_coz()` üzerinden kuruluyor, bozuk/boş
  tarihte `None` dönüyor.
- **`ozet_verisi()`**: `opu_tarihi`, `transfer_tarihi` artık
  `_gg_aa_yyyy(...)` ile geliyor (`(zaman or "")[:10]` yerine).
- **`artlab_dolgu()`**: "İşlem / Tarih / Sa." bloğundaki tarih hücresi
  (`_ISLEM_TARIH`) `_gg_aa_yyyy(z)` kullanıyor; saat hücresi (`_ISLEM_SAAT`,
  yalnızca `HH:MM`) sıra değişmediği için dokunulmadı.
- **`alanlar()`** (laboratuvarın kendi yüklediği forma aktarılan değerler,
  v6.40): `bugun` ve `saat_<asama>` alanları (OPU/denüdasyon/ICSI/fert/
  vitrifikasyon/thaw/transfer tarihi ve saati) aynı şekilde düzeltildi.
  `opu_tarihi`/`transfer_tarihi` zaten `ozet_verisi()`'nden miras aldığı
  için ayrıca dokunmaya gerek kalmadı.
- Aynı dolgu hem `/form/{ad}/{id}` (yazdırma) hem `/disari/form/{ad}/{id}`
  (Excel) tarafından kullanıldığı için **tek noktadan** düzeldi.

## Test edildi

`/form/ozet/1` ve `/form/artlab/1` yazdırma ekranları açılıp basılan tüm
tarihlerde ISO (`\d{4}-\d{2}-\d{2}`) kalıp kalmadığı, veri alanlarının
"09.09.2026" biçiminde çıktığı doğrulandı (kalıptaki sabit "Yayın Tarihi"/
"Revizyon Tarihi" etiketleri zaten kâğıttan geldiği için hep doğru
biçimdeydi, onlara dokunulmadı). Her iki formun `.xlsx` çıktısı indirilip
hem ham XML'de (`t="inlineStr"`, biçim bozulmamış) hem `openpyxl` ile
açılıp hücre değeri "09.09.2026" olarak doğrulandı — dosya bozulmadı,
tarih hücresi hâlâ düz metin. `formlar.alanlar()` çıktısı da elle
çağrılıp `bugun` ve `saat_opu`/`saat_denudasyon` alanlarının doğru
biçimde geldiği kontrol edildi. Test oturum jetonu temizlendi.

# v6.95 — Hasta ve eş telefon numarası

Kullanıcının isteği: hasta kaydederken hastanın ve eşinin telefon numarası
da tutulsun.

## Ne değişti

- **`goc_036.py`** (yeni göç): `hasta` tablosuna `telefon` ve `es_telefon`
  (ikisi de `TEXT`, serbest metin — format kısıtı yok, klinikte 0 ile
  başlayan/tireli/boşluklu yazımların hepsi geçerli olsun diye) eklendi.
  Basit `ALTER TABLE ADD COLUMN`, tablo yeniden kurulmadı (CHECK kısıtı
  gibi bir engel yok).
- **`/hasta/yeni`, `/hasta/{id}/duzenle`**: form ve kayıt/güncelleme
  rotalarına `telefon` (hastanın kendi) ve `es_telefon` eklendi — `es_adi`
  ile aynı desende: boşsa `NULL`, hata dönüşünde yazılanlar korunur (v6.21
  kuralı).
- **`/sperm-dondurma/yeni-hasta`** (v6.86'nın eş alanları olmayan erkek
  hasta formu): yalnızca `telefon` eklendi — bu ekranda zaten "eş" kavramı
  yok, `es_telefon` burada anlamsız.
- **`hasta_detay.html`**: kimlik bandının alt satırına doğum tarihinin
  yanına "Telefon: ..." ve "Eş: Ad Soyad (telefon)" eklendi — `es_adi`
  zaten oradaydı, aynı satıra doğal ek.
- `/disari/tumu` dökümüne dokunulmadı: o tablo kolonlarını
  `PRAGMA table_info()` ile **dinamik** okuyor (`disari.py`), yeni kolonlar
  kendiliğinden dökümde görünür.

## Test edildi

Sunucu ayağa kaldırılıp üç akış da uçtan uca denendi: `/hasta/yeni`'den
telefon + eş telefonuyla yeni hasta açıldı, `/hasta/{id}` kimlik bandında
"Telefon: 05551112233" ve "Eş: Es Test (05559998877)" doğru göründü;
`/hasta/{id}/duzenle`'de alanlar doğru önceden dolduruldu, değiştirilip
kaydedilince güncellendiği doğrulandı; `/sperm-dondurma/yeni-hasta`'dan
telefonlu bir erkek hasta + sperm dondurma kaydı tek seferde açılıp
`hasta.telefon`'un doğru yazıldığı veritabanından kontrol edildi. Tüm
şablonlar hatasız derlendi. Test hastaları, taşıyıcı kaydı ve oturum
jetonu temizlendi.

# v6.96 — Yumurta Dondurma'da dondurmadan önce maturasyon/bulgu

Kullanıcının isteği: "Yumurta dondurmada yumurtanın maturasyonu ve
bulguları girilecek yerler olsun. Dondurmadan önce bu bilgileri
girebileyim." Nereye ekleneceği soruldu, kullanıcı **denüdasyon
ekranını** seçti — ICSI'deki değerlendirmeyle aynı klinik an, sadece
`oosit_cryo`'da ICSI aşaması hiç olmadığı için o soru hiç sorulmuyordu.

## Ne değişti

- **Yeni kod yolu değil, ICSI'nin kullandığı mekanizmanın aynısı**:
  `olay.tip='maturasyon_kontrolu'` (MII/MI/GV/Dejenere/Atretik) ve
  `specimen_bulgu` (aynı `bulgu_icsi` listesi — zona/sitoplazma/polar
  cisim gibi morfolojik bulgular, ICSI'ye özel değil, oositin kendisine
  ait). Yalnızca `specimen_bulgu.asama='denudasyon'` ile ayrılıyor ki
  ICSI'nin kendi bulgularıyla (asama='icsi') hiç karışmasın.
- **Yalnızca `oosit_cryo`'da görünür.** `ivf_icsi`'de bu soru zaten ICSI
  ekranında soruluyor — iki yerde aynı soruyu sormamak için denüdasyon
  ekranı `c.cycle_tipi == 'oosit_cryo'` dışında bu bölümü hiç basmıyor.
- **`app.py`**: `denudasyon()` GET'i artık seçili oosit için `mat` ve
  `secili_bulgular`'ı da yüklüyor (yalnızca oosit_cryo'da anlamlı, ötekinde
  hesaplansa da şablon basmıyor). Yeni rota
  **`POST /specimen/{id}/oosit-degerlendirme`** — `icsi_kaydet()`'in
  maturasyon/bulgu kaydetme kısmının aynısı, enjeksiyon bölümü olmadan.
- **`denudasyon.html`**: çalışma kipinde "Toplandığı over" kartının hemen
  altına yeni bir "Oosit değerlendirmesi" kartı geldi — maturasyon
  düğmeleri (ICSI'deki `.secenek` düğmeleriyle birebir aynı görünüm) ve
  bulgular için alt sayfa (bottom sheet) modalı, ICSI'nin
  `#bulguAc`/`#bulguTabaka` desenin bire bir kopyası. Salt okunur görünümde
  (`bk.kart()`) de aynı iki satır ekleniyor, `bk.bulgu_metni()` makrosuyla.
  **İşlem saatleri elle girilebilir** kuralı burada da geçerli, saat alanı
  var. Yeni JS bloğu tuzak #10'a uyuyor:
  `if (!document.getElementById('oositdegform')) return;`.

## Test edildi

Test amaçlı bir `oosit_cryo` cycle (2 oosit) açılıp denüdasyonun çalışma
kipinde "Oosit değerlendirmesi" kartının yalnızca bu tedavi tipinde
göründüğü, `ivf_icsi` cycle'da hiç basılmadığı doğrulandı. Maturasyon
"MII" + iki bulgu ("Vakuol", "Geniş PVS") kaydedilip veritabanında
`olay.tip='maturasyon_kontrolu'` ve `specimen_bulgu.asama='denudasyon'`
satırlarının doğru yazıldığı kontrol edildi; salt okunur görünümde
"Maturasyon: MII" ve "Oosit bulguları: Vakuol, Geniş PVS" doğru çıktı;
çalışma kipine dönüldüğünde radyo düğmesi ve bulgu çipleri önceden
doğru işaretli geldi. Playwright ile hem çalışma hem görüntüleme kipi
hem bulgu modalı ekran görüntüsüyle doğrulandı. Test cycle'ı, oositleri,
arşiv klasörü ve oturum jetonu temizlendi.

# v6.97 — Gebelik sonucunda doğum haftası ve bebek başına cinsiyet/kilo

Kullanıcının isteği: "Gebelik bölümünde doğum olduğunda kız mı erkek mi
olduğu kaç kilo ve kaçıncı hafta doğum olduğu bölümleri olsun." Birden
fazla bebek (ikiz/üçüz) olduğunda cinsiyet ve kiloyu nasıl gireceği
soruldu — kullanıcı **her bebek için ayrı satır**'ı seçti (tek satıra
serbest metin değil).

## Ne değişti

- **`goc_037.py`** (yeni göç): `gebelik_sonucu.dogum_haftasi INTEGER`
  eklendi (doğum tek bir haftada olur, ikizde de aynı) ve yeni tablo
  **`dogan_bebek`** (`id`, `lab_id`, `cycle_id`, `sira`, `cinsiyet`,
  `kilo_kg`, `UNIQUE(cycle_id, sira)`). `beta_hcg` ile aynı desen: satır
  doğrudan `cycle_id`'ye bağlı, `gebelik_sonucu.id`'ye değil — `beta_hcg`
  zaten bunu yapıyordu, mimari tutarlılık için aynısı tekrarlandı.
  `dogan_bebek.id` URL'e hiç sızmıyor (tuzak #13), `AUTOINCREMENT`
  gerekmedi.
- **`gebelik.html`**: "Sonlanma" kartına `dogum_haftasi` sayısal alanı
  eklendi. Ana formdan (`#gform`) **sonra**, ayrı bir "Bebekler" kartı:
  `bebek_sayisi` kadar (en az 1) satır, her biri **kendi `<form>`'unda**
  (HTML formları iç içe olamaz) `/cycle/{id}/gebelik/bebek`'e POST ediyor.
  Cinsiyet radyo düğmesiyle (ICSI/denüdasyon'daki `.secenek` görünümü,
  sayfadaki genel toggle scripti zaten her `.secenek` grubunu kapsıyor,
  yeni JS gerekmedi), kilo serbest metin (`sayi()` virgüllü ondalığı
  kabul ediyor). **Radyo bilerek self-submit buton değil** — "Kaydet"e
  basıldığında cinsiyet yeniden işaretlenmemişse önceki değeri `NULL`'a
  düşürmesin diye, seçili durum forma gömülü kalıyor.
- **`app.py`**: `gebelik_ekran()` artık `dogan_bebek` satırlarını okuyup
  `bebek_siralari` (1'den `max(bebek_sayisi, kayıtlı en yüksek sıra)`'ya
  kadar) ve `bebek_kayitli` (sıra → satır) hesaplıyor — `bebek_sayisi`
  girilmeden önce de en az 1 satır görünsün, sonradan azaltılsa bile
  kayıtlı üst sıralar kaybolmasın diye. `gebelik_kaydet()`'e
  `dogum_haftasi` (`tam()` ile) eklendi. Yeni rota
  **`POST /cycle/{cycle_id}/gebelik/bebek`**: `sira`+`kilo_kg`'ı doğrulayıp
  `dogan_bebek`'e upsert yapıyor, hata dönüşü `?hata=`'ya, formu kapatmıyor.
- **Tuzak #4 (cascade delete)**: `cycle_tamamen_sil()`'e `dogan_bebek`
  silme satırı eklendi (`beta_hcg` ile `gebelik_sonucu` arasına — aynı
  konum, aynı desen). **`teshis_silme.py`'ye de** aynı tarama + silme adımı
  eklendi — CLAUDE.md'nin "aynısını teshis_silme.py'ye de ekle" kuralı.
- **`disari.py`**: `dogan_bebek` `TUM_TABLOLAR`'a eklendi, `/disari/tumu`
  dökümünde kendiliğinden çıkacak (kolonlar `PRAGMA table_info()` ile
  dinamik okunuyor).
- **`metinler.py`**: `dogum_haftasi`, `bebekler`, `n_bebek`, `kiz`,
  `erkek`, `dogum_kilosu` anahtarları eklendi.

## Test edildi

Sunucu ayağa kaldırılıp bir cycle'ın gebelik ekranında `dogum_haftasi=38`
ve `bebek_sayisi=2` kaydedildi; "Bebekler" kartının 1 satırdan 2 satıra
çıktığı doğrulandı. 1. bebek "Kız" + 3,2 kg, 2. bebek "Erkek" + 2,95 kg
ayrı formlarla kaydedildi; `sayi()`'nin virgüllü ondalığı doğru çevirdiği
(`2,95` → `2.95`) veritabanından kontrol edildi. Sayfa yeniden yüklenince
her iki bebeğin cinsiyet radyosu (`checked`) ve kilo alanı (`value`)
doğru önceden dolu geldi. `dogum_haftasi` alanı da (`38`) doğru
round-trip etti. Tüm şablonlar hatasız derlendi. Test `dogan_bebek`
satırları, `gebelik_sonucu`'na yazılan test değerleri ve oturum jetonu
temizlendi.

# v6.98 — Sperm dondurma hastaları Tüm Hastalar'dan ayrıldı

Kullanıcının isteği: "Sperm dondurma işlemleri ayrı hasta kaydı olarak
tutulsun. Aylık tedavilerin gösterildiği yerde de sperm dondurma
kayıtları gösterilmesin." Ne demek istediği soruldu: mevcut bir IVF
hastasına sperm dondurma eklenebilmesi (örn. eşinden alınan sperm)
kalsın, ama yalnızca sperm dondurma amacıyla açılmış hastalar (v6.86'nın
"Yeni hasta kaydı (Sperm Dondurma)" akışı) `/hastalar`'daki Tüm Hastalar
listesinde IVF hastalarıyla karışmasın; arandıklarında yine bulunabilsinler.

## Ne değişti

- **Göç yok — ölçü tamamen türetilmiş.** `app.py`'ye yeni bir yardımcı
  `_sadece_sperm_kosulu()` eklendi: hiç `cycle`'ı olmayan ve en az bir
  iptal edilmemiş `sperm_dondurma` kaydı olan hasta. `/hastalar` ay
  listesi zaten `cycle` tablosundan okuyor ve sperm dondurma hiç `cycle`
  satırı açmıyor, o yüzden orada ek bir değişikliğe gerek yoktu.
- **`hastalar()` rotası**: Tüm Hastalar'ın hem sayımı hem satırları artık
  `NOT (_sadece_sperm_kosulu())` ile bu hastaları çıkarıyor. Arama sonucu
  ve arşiv listesi (aynı `ortak` sorgu) etkilenmedi — bunlar hedefli
  sorgular, personel belirli birini arıyorsa bulabilmeli. Onun yerine
  oradaki satırlara ve `/hasta/{id}` sayfasının kimlik bandına
  `sperm_hastasi` bayrağıyla "Sperm Dondurma" rozeti eklendi
  (`.rozet` — sabit koyu zemin, v6.74'ün "zemin sabitse yazı da sabit"
  kuralına uygun, yeni CSS gerekmedi).
- **Mevcut bir IVF hastasına sperm dondurma eklemek hâlâ mümkün**
  (`/hasta/{id}/sperm-dondurma/yeni`) — o hastanın kendi cycle'ı olduğu
  için koşul hiç tutmuyor, Tüm Hastalar'dan düşmüyor, rozet de
  basılmıyor. Kullanıcı bunu açıkça istedi.
- **`metinler.py`**: `sperm_dondurma_hastasi` anahtarı eklendi.

## Test edildi

Sunucu ayağa kaldırılıp üç senaryo denendi: (1) `/sperm-dondurma/yeni-hasta`
ile yeni bir sperm dondurma hastası açıldı — Tüm Hastalar sayısı
değişmedi, hasta o listede hiç görünmedi; (2) aynı hasta adıyla arandığında
arama sonucunda "Sperm Dondurma" rozetiyle bulundu, kendi `/hasta/{id}`
sayfasında da aynı rozet kimlik bandında çıktı; (3) mevcut bir IVF
hastasına (`cycle`'ı olan) `/hasta/{id}/sperm-dondurma/yeni` ile sperm
dondurma eklendi — bu hasta Tüm Hastalar'da rozetsiz görünmeye devam
etti. Ay listesi zaten cycle bazlı olduğu için hiçbir senaryoda sperm
dondurma hastası orada görünmedi. Test hastası, taşıyıcı kayıtları,
sperm dondurma kayıtları ve oturum jetonu temizlendi.

# v6.99 — "İşlemi yapan" artık seçiliyor, yazılmıyor

Kullanıcının isteği: "İşlem yapanlar kısmında isim girilen kısımda
şifresiyle giren kişinin adı otomatik çıksın. Diğer şifresi olanlar da
seçilebilir olsun. Yazmadan seçilerek işlemi yapan kişi girilsin."

## Ne değişti

- **Göç yok.** `islem_yapan.yapan_ad` kolonu aynı kaldı (hâlâ metin), yalnızca
  *nasıl doldurulduğu* değişti — serbest yazma yerine seçim. `kullanici_id`
  (kaydı giren) zaten ayrı bir alandı, ona dokunulmadı.
- **`_islem_yapan.html`**: `<input type="text">` yerine `<select>`. Seçenekler
  `personel_listesi()` (yeni Jinja global — şifresi olan/aktif kullanıcıların
  adları, alfabetik). Kayıt henüz yoksa varsayılan seçim
  `guncel_kullanici_ad()` (yeni Jinja global — şifresiyle giriş yapmış
  kişi); kayıt varsa o değer seçili gelir, değiştirilebilir. "Kaydet"
  düğmesi duruyor — seçmek otomatik kaydetmiyor, "işlem saatleri elle
  girilebilir" ile aynı gerekçe: varsayılan bir öneri, dayatma değil.
- **Tuzak #6'ya uyuldu**: kayıtlı `yapan_ad` aktif personel listesinde yoksa
  (hesap sonradan pasif yapıldı ya da v6.99 öncesi serbest metinle
  yazılmış bir ad listede hiç yoksa) o değer listeye kendi seçeneği olarak
  ekleniyor — yoksa tarayıcı ilk ismi seçili gösterir ve "Kaydet"e
  basılınca kayıt sessizce değişirdi.
- **İki yeni Jinja global, ikisi de `contextvars` üzerinden** —
  `_YETKILER`'in kullandığı desenin aynısı: `_GIRIS_KULLANICI`
  middleware'de `request.state.kullanici` ile birlikte set ediliyor,
  `guncel_kullanici_ad()` oradan okuyor. Böylece `hasta_detay()` gibi
  "kullanici" bağlamını context'e hiç eklemeyen rotalarda bile makro
  doğru çalışıyor — ~50 rotanın hepsine `"kullanici": request.state.
  kullanici` eklemek gerekmedi.

## Test edildi

Sunucu ayağa kaldırılıp bir cycle'ın denüdasyon ekranında İşlemi Yapan
seçicisi kontrol edildi: kayıt hiç yokken giriş yapan kullanıcının adı
("Test Kullanici") önceden seçili geldi, listede diğer aktif kullanıcılar
("Ayse Demir", "Test Androlog") da alfabetik sırada göründü. Başka bir
kullanıcı ("Ayse Demir") seçilip kaydedildi; sayfa yeniden yüklendiğinde
o isim seçili kaldı (giriş yapan kişi hâlâ "Test Kullanici" olsa da).
Veritabanında `yapan_ad` doğrudan "Eski Personel Adi" gibi aktif personel
listesinde olmayan bir değere değiştirilip sayfa yenilendi — seçici o
değeri listeye ekleyip seçili gösterdi, ilk isme kaymadı. Test verileri
(oturum jetonu, test amaçlı `islem_yapan` satırı) temizlendi.

# v6.100 — Test kullanıcı silindi, kullanıcı silme hatası düzeltildi, doğum kilosu öneri menüsü

Kullanıcının isteği: test amaçlı "androlog" hesabını sil; gebelik
sonucundaki doğum kilosu alanı elle yazılmasın, seçilebilir bir menü olsun.

## Ne değişti

- **`kullanici_sil()`'de gerçek bir hata bulundu ve düzeltildi.** Test
  hesabını (`kullanici_adi='androlog'`, hiç kaydı yok) kalıcı silmeye
  çalışırken rota `FOREIGN KEY` hatasıyla patladı — `yetki` tablosu
  `kullanici_id`'ye bağlı ama `KULLANICI_KAYITLARI`'nda yok (izin ataması,
  "kayıt" değil, bilerek silmeyi engellemiyor) ve rota onu hiç silmiyordu.
  Bu **her** kullanıcıyı etkileyen bir hataydı — `tum_yetkileri_ver()`
  yeni açılan her hesaba `yetki` satırı yazıyor, kayıtsız bile olsa. Düzeltme:
  `kullanici_sil()` artık `oturum` gibi `yetki`'yi de kullanıcıdan **önce**
  siliyor (`yetki_tablosu_var()` ile korunarak — `goc_026` çalışmamışsa
  tablo yok). "androlog" hesabı bu düzeltmeyle gerçek `/kullanici/{id}/sil`
  rotasından kalıcı olarak silindi.
- **`gebelik.html`**: bebek başına doğum kilosu artık `<input list=
  "kilo_secenekleri">` + paylaşılan bir `<datalist>` (0,50–5,00 kg arası,
  0,1 kg adımlarla, 46 öneri). Dropdown gibi görünüyor ama kutuya **elle de
  yazılabiliyor** — kapalı bir `<select>` olsaydı gerçek bir tartı
  sonucunun (örn. 3,245 kg) hassasiyeti kaybolurdu. `sayi()` sunucuda
  hâlâ aynı, virgüllü ondalığı kabul ediyor.
- Bu ikisi CLAUDE.md'ye eklendi: "kayıt değil ama FK'sı var" tablo deseni
  (`yetki`) ve "kategori kesinleşmemiş/sayısal alan → datalist, kapalı
  `<select>` değil" kuralı — ikincisi bir sonraki sürümde sperm dondurma
  sebebi alanına da uygulanacak.

## Test edildi

Sunucu ayağa kaldırılıp gerçek `/kullanici/{id}/sil` rotasıyla "androlog"
test hesabı silindi — önce hatayı doğrulamak için düzeltmeden önce
denendi (FOREIGN KEY hatası doğrulandı), düzeltmeden sonra başarıyla
silindi; `yetki` ve `oturum` satırlarının da gittiği veritabanından
kontrol edildi. Gebelik ekranında kilo alanına önce öneri listesinden bir
değer, sonra elle "3,245" yazılıp kaydedildi — ikisi de tam olarak
yazıldığı gibi kaydedildi ve sayfa yenilenince aynı değer geri geldi. Test
verileri (test `dogan_bebek` satırı, oturum jetonu) temizlendi.

# v6.101 — Sperm dondurmada dondurma sebebi önerisi, İşlemi Yapan, Onamlar

Kullanıcının istekleri: "Sperm Dondurma sebeplerine Tedavi Öncesi Koruma,
Onkolojik, TESE, TESA, PESA olsun. Sperm dondurma işlemini yapan kaydı
olsun... Ayrıca sperm dondurma bölümüne dosya kaydedebileyim. Onamlar
diye bir bölüm olsun, buraya PDF ve Fotoğraf kaydedebileyim. Ayrıca
gebelik kilosunun girme ekranını eskiye çevir, beğenmedim."

## Ne değişti

- **Gebelik doğum kilosu v6.100 öncesine döndürüldü** — `<datalist>`
  önerisi kaldırıldı, düz `<input type="text" inputmode="decimal">`'e
  geri dönüldü. Kullanıcı denedi, istemedi.
- **Dondurma sebebi artık öneri menüsü**: aynı `<datalist>` deseni (v6.100'de
  tanımlandı) sperm dondurma formlarına (`sperm_dondurma_form.html`,
  `sperm_dondurma_yeni_hasta.html`) uygulandı. Beş öneri — Tedavi Öncesi
  Koruma, Onkolojik, TESE, TESA, PESA — `app.py`'de tek yerde
  (`SPERM_DONDURMA_SEBEPLERI`, Jinja global `sperm_dondurma_sebepleri()`),
  iki form da oradan okuyor. `sperm_dondurma.sebep` hâlâ serbest metin;
  listede olmayan bir sebep de yazılabiliyor.
- **Sperm dondurmanın kendi "İşlemi Yapan" kutusu** (`goc_038`:
  `sperm_dondurma.yapan_ad`). Aşama ekranlarındaki kutunun (v6.99) aynı
  deseni — şifresi olan personelden seçiliyor, varsayılan giriş yapan
  kişi — ama `islem_yapan` tablosu kullanılamadı (`cycle_id` istiyor,
  sperm dondurmanın cycle'ı olmayabilir). `sperm_dondurma_detay.html`'de
  kendi kutusu, `POST /sperm-dondurma/{id}/islem-yapan`.
- **Onamlar bölümü**: PDF/fotoğraf eki, `sperm_dondurma_detay.html`'e yeni
  bir kart. Yeni tablo **`sperm_dondurma_dosya`** (`goc_038`,
  `AUTOINCREMENT` — tuzak #13, id adrese yazılıyor) — Doktor Notu'nun
  (v6.81) `goruntu` mekanizması kullanılamadı çünkü `goruntu.cycle_id`
  NOT NULL, sperm dondurmanın cycle'ı olmayan bir hastada (onkoloji
  öncesi gibi) hiç yazılamazdı. `goruntuler.sperm_onam_ekle()`/
  `sperm_onam_sil()` yeni fonksiyonlar, `arsiv/<dosya no>/sperm-dondurma/
  <id>/` klasörüne yazıyor. Fotoğraf da PDF gibi **yeni sekmede** açılıyor
  — paylaşılan `_buyutec.html` lightbox'ı `/dosya/` adresine sabit
  yazıldığı için kullanılamadı, ayrıca bunlar embriyo fotoğrafı değil
  belge eki, yakınlaştırma gerekmiyor.
- **Gerçek bir hata bulundu ve düzeltildi**: `hasta_sil()`'in kalıcı silme
  dalı zaten hastanın `sperm_dondurma` kayıtlarını siliyordu; test
  edilirken yeni `sperm_dondurma_dosya` FK'sı yüzünden bu satır FOREIGN
  KEY hatasıyla patladı. Düzeltme: o hastanın sperm dondurma kayıtlarının
  onam ekleri önce siliniyor. **`teshis_silme.py`'ye de eklendi** — o araç
  hastanın kendi `sperm_dondurma` kayıtlarını hiç simüle etmiyordu
  (yalnızca `kullanim_cycle_id` bağlarını kontrol ediyordu), bu eksik de
  kapatıldı.
- `disari.TUM_TABLOLAR`'a `sperm_dondurma_dosya` eklendi (`goruntu` gibi).
- `metinler.py`'ye `onamlar`, `onam_yok`, `onam_ipucu`, `onam_sil`,
  `onam_kalici_silinecek` anahtarları eklendi; `dondurma_sebebi_ipucu`
  metni artık öneri menüsünü anlatıyor.

## Test edildi

Sunucu ayağa kaldırılıp yeni bir sperm dondurma hastası açıldı, sebep
alanında öneri listesi doğru göründü ("Onkolojik" seçildi). Kayıt
sayfasında İşlemi Yapan kutusu giriş yapan kullanıcıyı önceden seçili
gösterdi, başka bir kullanıcı seçilip kaydedildi ve doğru kaldığı
doğrulandı. Onamlar bölümüne bir PDF ve bir JPG yüklendi — ikisi de
listelendi (PDF rozetli, JPG küçük resimli), `/sperm-onam/{id}`'den bayt
bayt aynı şekilde indirildiği doğrulandı, biri silinip hem veritabanından
hem diskten gittiği, öteki kalanın etkilenmediği kontrol edildi.
`teshis_silme.py <dosya_no>` bu test hastası için çalıştırılıp yeni
`sperm_dondurma_dosya` taramasının ve silme adımlarının doğru çalıştığı
görüldü; ardından gerçek `/hasta/{id}/sil` (kalıcı silme) rotasıyla aynı
hasta silindi — düzeltmeden önce FOREIGN KEY hatasıyla patladığı
doğrulandı, düzeltmeden sonra `hasta`, `sperm_dondurma`,
`sperm_dondurma_dosya` ve `tasiyici` satırlarının hepsinin gittiği
kontrol edildi. Gebelik ekranında kilo alanının düz metin kutusuna
döndüğü doğrulandı. Test hastası, dosyaları, arşiv klasörü ve oturum
jetonları temizlendi.

# v6.102 — Yumurta Çözme tedavi tipi, çözme notu, NOTLAR kutusu düzeltildi

Kullanıcının istekleri: "Çözme tedavilerinde (FET, FET 3-5 kültür) Çözme
bölümüne Not eklenebilsin, bu notlar Embriyoloji Özet formunun NOTLAR
bölümüne yazılsın. Yumurta Çözme tedavisi de tedavi tiplerine eklensin,
Çözme bölümü olsun ve viabilite girilebilsin." Kullanıcının seçtiği
tasarım: not tek/paylaşılan (taşıyıcı başına), NOTLAR kutusunda protokol
notunun altına eklensin, Yumurta Çözme yalnızca çözme aşamasından oluşsun.

## Ne değişti

- **Yeni tedavi tipi `yumurta_cozme`** (`goc_039`). `oosit_cryo`'da
  dondurulmuş bir yumurtanın, FET'in embriyo için yaptığı gibi, AYRI bir
  tedavide çözülmesi — yalnızca **Çözme** aşaması, kullanıcının kararıyla
  bilinçli olarak minimal (ICSI/fertilizasyon gerekirse ayrı bir tedavi
  açılır). `FET_TIPLERI`'ne eklendi — taşıyıcı/örnek listeleri
  `thaw_cycle_id` ile aranıyor, `fet`/`fet_kultur` ile aynı mekanizma
  (mekanizma zaten embriyo/oosit ayrımı yapmıyor, hiç değişmedi).
  **`cycle.cycle_tipi`'nin CHECK kısıtı genişletildi** — `goc_031`'in
  `fet_kultur` için yaptığı tablo-yeniden-kurma tekniğinin aynısı (SQLite
  ALTER ile CHECK değiştiremiyor). `liste_degeri`'ne "Yumurta Çözme"
  eklendi (dropdown oradan besleniyor).
- **Çözme notu**: `thaw.html`'e tek, paylaşılan bir "Not" alanı
  (`olay.thaw_notu`, `goc_039`) — taşıyıcıdaki tüm örnekler için ortak,
  `thaw_kontrol_zamani` ile aynı desen. `formlar.ozet_verisi()` bu cycle'a
  ait bir çözme notu bulursa protokol notunun **altına** ekliyor (üzerine
  yazmıyor). Cycle tipinden bağımsız çalışıyor — sorgu zaten yalnızca bu
  cycle'a ait çözmeleri buluyor, `ivf_icsi`/`oosit_cryo`'nun kendi
  çözmesinde not yazılırsa o da aynı şekilde eklenir.
- **Gerçek bir hata bulundu ve düzeltildi**: Embriyoloji Özet formunun
  NOTLAR kutusu **hiçbir zaman** protokol notunu basmıyormuş —
  `formlar._OZET_NOTLAR = (70, 2)` kalıptaki yanlış satırı gösteriyordu
  (satır 70 boş, gerçek NOTLAR kutusu satır 71'de). Kimse fark etmemiş
  çünkü kutu sessizce boş kalıyordu, hata vermiyordu. Düzeltme yalnızca
  Python sabiti (`(71, 2)`) — kalıba (`form_kalip.json`) dokunulmadı.
- `metinler.py`'ye `tip_yumurta_cozme`, `cozme_notu`, `cozme_notu_ipucu`
  anahtarları eklendi; `fet_ipucu` metni Yumurta Çözme'yi de anlatıyor.

## Test edildi

Sunucu ayağa kaldırılıp test hastasına bir `oosit_cryo` cycle'ı ve
vitrifiye bir yumurta (taşıyıcı) oluşturuldu. Yeni cycle formunda "Yumurta
Çözme" seçeneği göründü, seçilince cycle detayında **yalnızca** "Çözme"
aşaması listelendi (OPU/ICSI/Transfer gibi diğer düğmeler hiç çıkmadı).
`/cycle/{id}/thaw` ekranı `oosit_cryo` cycle'ındaki taşıyıcıyı doğru
listeledi (FET_TIPLERI mekanizmasının oosit için de çalıştığı doğrulandı).
Çözme kaydedilirken "Test çözme notu" yazıldı, `olay.thaw_notu`'na doğru
kaydedildiği görüldü. Embriyoloji Özet formu yazdırılıp önce yalnızca
protokol notunun, sonra yalnızca çözme notunun, sonra **ikisinin birlikte**
(protokol notu üstte, çözme notu altta, ayrı satırlarda) doğru basıldığı
doğrulandı — bu sırada `_OZET_NOTLAR` hatası bulunup düzeltildi ve üç
senaryo da yeniden test edildi. Test cycle'ları, taşıyıcı, specimen ve
oturum jetonu temizlendi.

# v6.103 — İşlemi bitir: altı ayrıntılı iptal sebebi

Kullanıcının isteği: "İşlem bitir de seçeneklere Yumurta Çıkmadı İptal,
İmmatür Yumurta İptal, Fertilizasyon Olmadı İptal, PN Arrest İptal,
Cleavage Arrest İptal, 5. Gün Arrest İptal seçenekleri ekle." Mevcut genel
"İptal" seçeneğiyle çakışma sorulduğunda kullanıcının kararı: genel İptal
kalsın, altısı ek olarak eklensin.

## Ne değişti

- **`/cycle/{id}/bitir` ekranına altı yeni düğme.** Genel üç seçeneğin
  (Dondurma tamamlandı / Transfer yapıldı / İptal) altında ayrı bir grupta:
  Yumurta Çıkmadı İptal, İmmatür Yumurta İptal, Fertilizasyon Olmadı İptal,
  PN Arrest İptal, Cleavage Arrest İptal, 5. Gün Arrest İptal. Hepsi genel
  İptal ile aynı şekilde `durum='iptal'` yapıyor — yalnızca hangi aşamada
  durduğunu ayırt ediyorlar, `cycle_detay.html`/`_cyclesatir.html`'de
  (Bugün Bitenler, /bitenler) doğru etiketle görünüyorlar.
- **Şema değişmedi.** `cycle.bitis_sebebi` zaten CHECK kısıtı olmayan
  serbest bir metin kolon; yeni sebep kodları (`yumurta_cikmadi`,
  `immatur_yumurta`, `fert_olmadi`, `pn_arrest`, `cleavage_arrest`,
  `gun5_arrest`) doğrudan yazılabildi, göç gerekmedi. `BITIS_DURUMU`
  sözlüğü (`app.py`) yeni bir `IPTAL_DETAY_SEBEPLERI` tuple'ından
  kendiliğinden kuruluyor.
- **Genel "İptal" kaldırılmadı** — kullanıcının kararı: listede olmayan
  bir sebep için hâlâ kullanılabiliyor.
- `metinler.py`'ye `bitis_yumurta_cikmadi`, `bitis_immatur_yumurta`,
  `bitis_fert_olmadi`, `bitis_pn_arrest`, `bitis_cleavage_arrest`,
  `bitis_gun5_arrest` ve `iptal_detay_baslik` anahtarları eklendi —
  isimlendirme mevcut `"bitis_" ~ kod` deseniyle aynı, `_cyclesatir.html`
  ve `cycle_detay.html` hiç değişmeden yeni sebepleri de doğru gösteriyor.

## Test edildi

Sunucu ayağa kaldırılıp `/cycle/{id}/bitir` ekranında dokuz düğmenin de
(üç genel + altı ayrıntılı) doğru metinle göründüğü doğrulandı. Test
cycle'ı "PN Arrest İptal" ile bitirildi; cycle detayının başlığında ve
`/bitenler` listesinde "PN Arrest İptal" doğru göründü. `?duzenle=1`
kipinde doğru düğmenin "Seçili" rozetiyle işaretlendiği kontrol edildi.
"Listeye geri al" ile cycle'ın tamamen eski (aktif, sebep/saat boş)
haline döndüğü doğrulandı. Oturum jetonu temizlendi.

# v6.104 — Seçilen iptal sebebi resmî formlarda da görünsün

Kullanıcının isteği: "Burada seçilen iptal seçeneği Embriyoloji özet
formunda Notlara yazılsın. Art Lab formunda da alt kısmında tam ortasında
görünür şekilde çıksın. Puntoları normal yazılandan büyük olsun."

## Ne değişti

- **`formlar._iptal_notu(c)`** — yeni ortak yardımcı: cycle iptal edildiyse
  (`durum=='iptal'`) seçilen sebebin ekran etiketini döndürür
  (`metin("bitis_"+bitis_sebebi)`), değilse `None`. `bitis_sebebi` yalnızca
  `cycle_bitir()`'in `BITIS_DURUMU` ile doğruladığı kodlardan biri olabildiği
  için `metin()`'e doğrudan verilebildi — tuzak #9'daki "adresten gelen
  anahtar" durumu burada geçerli değil.
- **Embriyoloji Özet Formu**: iptal notu mevcut NOTLAR kutusuna, protokol
  notu ve çözme notunun (v6.102) altına üçüncü satır olarak ekleniyor.
  Ayrı bir görsel vurgu yok — kutunun kendi puntosunu kullanıyor.
- **ART Lab. Raporu**: ART Lab'da böyle bir "notlar" kutusu yok, kullanıcı
  da ayrıca "alt kısmında tam ortada, büyük punto" istedi — bu yüzden
  kalıbın **dışına**, son sayfanın hemen altına yeni bir şerit eklendi:
  - Ekranda (`form.html`, `.formiptalnotu`): sabit siyah/beyaz (kâğıt aslı
    gibi), 15pt kalın ortalı — formun gövde metninden (8-10pt) bariz büyük.
    Yalnızca son sayfada basılıyor (özet bloğunun yalnızca ilk sayfada
    basılmasının simetriği).
  - Excel'de (`app.py` `form_excel()`): kalıbın son satırının hemen altına
    tam genişlikte birleşik bir hücre ekleniyor, hazır stil adı `"formadi"`
    (`excel.STILLER`, 14pt kalın ortalı) ile. Bunun için `form_kalip.py`'ye
    iki küçük yardımcı eklendi: `olcu(kaynak)` (kalıbın satır/sütun sayısı)
    ve `hucre_adresi(satir, sutun)` (`_adres()`'in dışarıdan çağrılabilir
    hali). **`form_kalip.json` ve kalıbın kendi stil listesi hiç
    değişmedi** — "kalıba dokunma" kuralı korundu, ekleme tamamen kalıbın
    ürettiği ızgaranın dışında/altında yapılıyor. Adlandırılmış `"formadi"`
    stili kalıba özgü değil (`excel.STILLER`, global) olduğu için kalıbın
    kendi `stiller` listesine (paylaşılan/önbellekli `KALIPLAR` sözlüğünün
    parçası) dokunmadan kullanılabildi.
  - Yalnızca `ad=="artlab"` iken devreye giriyor; Özet'te `iptal_notu`
    context'i hiç verilmiyor çünkü orada aynı bilgi zaten NOTLAR'a yazıldı.

## Test edildi

Sunucu ayağa kaldırılıp test hasta + cycle açıldı. Cycle `pn_arrest`
sebebiyle bitirildiğinde: Embriyoloji Özet'in NOTLAR kutusunda "PN Arrest
İptal" (protokol notuyla birlikte doğru sırada, alt alta) ve ART Lab'ın
ekran çıktısında `.formiptalnotu` şeridinde aynı metin görüldü. Excel
çıktıları (`openpyxl` ile açılıp) doğrulandı: Özet'in NOTLAR hücresi
(C72) doğru metni taşıyor, ART Lab'da yeni satır (A39, `A39:AC39`
birleşik) 14pt kalın ortalı stille doğru basılmış, dosya bozulmadan
açılıyor. Cycle aktif duruma alınıp "dondurma" ile bitirildiğinde notun
**basılmadığı**, genel "İptal" ile bitirildiğinde "İptal" etiketinin
doğru çıktığı da ayrıca doğrulandı. Test hasta/cycle/oturum kayıtları
temizlendi.

# v6.105 — ICSI'de "yapılmadı" işaretli oosit sonraki aşamalarda

Kullanıcının isteği: "ICSI bölümünde yapılmadı işaretlenen oositler diğer
bölümlere fertilizasyon bölümüne yapılmadı işaretlensin, cleavage blastokist
ve vitrifikasyon bölümlerinde hiç görünmesin."

## Ne değişti

- **`app.py`'ye `_ICSI_YAPILMADI` SQL parçası eklendi.** ICSI ekranında
  "Enjekte edildi mi?" hayır seçilince (`icsi_kaydet()`) hiçbir `icsi` olayı
  yazılmıyor; bu koşul maturasyonun değerlendirildiğini (ICSI ekranı
  doldurulmuş) ama aktif bir `icsi` olayının olmadığını arıyor.
  **`specimen.durum`'a bakmıyor** — enjekte edilip ICSI'den sonra dejenere
  olan oosit de `durum='degenere'` yazıyor ama onun kendi `icsi` olayı var;
  ikisi karıştırılmasın diye ölçü olay tablosu.
- **Fertilizasyon ekranı (`fert_durum()`):** yeni `icsi_yapilmadi` bayrağı.
  Oosit hâlâ numara şeridinde görünüyor (görsel olarak dejenere/kayıp gibi
  soluk), ama seçildiğinde form yerine "ICSI yapılmadığı için bu oosite
  fertilizasyon kaydı girilmiyor" bilgi kartı basılıyor — daha önce girilmiş
  bir kayıt varsa (özellik öncesi) o kayda dokunulmadı, düzenleme/silme yolu
  bozulmadı.
- **Cleavage (`cleavage_durum()`) ve blastokist (`blast_durum()`):** sorguya
  `AND NOT (_ICSI_YAPILMADI)` eklendi, bu oositler listede **hiç** çıkmıyor.
- **Vitrifikasyon (`vit_ekran()`):** aynı süzgeç eklendi ama **yalnızca
  `ivf_icsi`'de** — o ekran `oosit_cryo` ile de paylaşılıyor ve orada
  maturasyon denüdasyonda değerlendirildiği (v6.96) için ICSI aşaması hiç
  yok; süzgeç şartsız uygulansaydı `oosit_cryo`'nun **her** oositini
  filtreleyip ekranı boş bırakırdı.
- `metinler.py`'ye `icsi_yapilmadi` ve `icsi_yapilmadi_fert_form_yok`
  anahtarları eklendi.

## Test edildi

Test hasta + `ivf_icsi` cycle'ında üç oosit açıldı: biri ICSI'de enjekte
edilip başarılı, biri enjekte edilip dejenere, biri enjekte edilmedi
(immatür — "yapılmadı"). Fertilizasyon ekranında: başarılı oosit normal
formu gösterdi; enjekte-edilip-dejenere olan oosit **hâlâ** formu gösterdi
(ICSI gerçekten denenmiş, yalnızca sonucu kötü — bu ekrandan
filtrelenmemesi gerekiyordu, doğrulandı); "yapılmadı" oosit form yerine
bilgi kartını gösterdi. Cleavage ve blastokist ekranlarının numara
şeritlerinde yalnızca ilk iki oositin (enjekte edilenlerin) göründüğü,
"yapılmadı" oositin şeritte hiç çıkmadığı doğrulandı. Vitrifikasyon
ekranında da aynısı doğrulandı. Ayrıca ayrı bir `oosit_cryo` cycle'ında
denüdasyonda immatür işaretlenmiş bir oositin vitrifikasyon ekranında
**hâlâ** göründüğü doğrulandı — `ivf_icsi` dışı süzgecin yanlışlıkla
uygulanmadığı böyle kanıtlandı. Test hasta/cycle/specimen/oturum kayıtları
temizlendi.

# v6.106 — Kullanıcı adı/kullanıcı adı düzenleme, hasta kayıtlarına yansıması

Kullanıcının isteği: "Yönetici ekranında kullanıcılara verilen şifreleri
yönetici görsün. Var olan kullanıcının Adını ve kullanıcı adını
değiştirebilsin. Hasta kaydı var ise oralardaki Adı da değişsin."

Üç istekten ikisi (ad/kullanıcı adı düzenleme ve hasta kayıtlarına yayılma)
bu sürümde yapıldı. Şifre görüntüleme **yapılmadı** — mimari buna izin
vermiyor, kullanıcıya ayrıca soruldu (aşağıya bak).

## Ne değişti

- **`POST /kullanici/{id}/duzenle`** (yeni rota, `app.py`) — var olan bir
  kullanıcının `ad_soyad` ve `kullanici_adi`'sini değiştirir.
  Doğrulama `kullanici_yeni()` ile birebir aynı: boş olamaz, kullanıcı adı
  yalnızca harf/rakam/nokta/alt çizgi (Türkçe karakter yok), aynı laptaki
  başka bir kullanıcıyla çakışamaz. `kullanici_adi` şemada **lab'dan
  bağımsız UNIQUE** olduğu için `kullanici_yeni()`'deki gibi
  `sqlite3.IntegrityError` de ayrıca yakalanıyor.
- **Ad değişirse hasta kayıtlarındaki "İşlemi Yapan" da otomatik güncellenir.**
  `islem_yapan.yapan_ad` ve `sperm_dondurma.yapan_ad` kullaniciyi FK ile
  değil, o anki adın metin kopyasıyla tutuyor (v6.99/v6.101'in bilinçli
  kararı) — `kullanici_duzenle()` eski adı taşıyan bütün satırları
  (`lab_id` + eski `yapan_ad` eşleşmesiyle) yeni adla güncelliyor.
  `kullanici_adi` (giriş adı) hiçbir hasta kaydına yazılmadığı için onun
  değişmesi bir cascade gerektirmiyor.
- **`templates/kullanicilar.html`**: her kullanıcı satırına "Şifresini
  değiştir"in yanına "Adını / kullanıcı adını değiştir" açılır formu
  eklendi, ad/kullanıcı adı alanları mevcut değerle geliyor.

## Neden şifre görüntüleme yapılmadı

Şifreler `sifre_hash` kolonunda **tek yönlü** hash olarak tutuluyor (bkz.
CLAUDE.md "Kullanıcıya verilmiş şifreler yönetici ekranında görüntülenmez").
Var olan bir kullanıcının şifresini geri okumak teknik olarak imkânsız —
hash'ten düz metne dönüş yok. Bunu "görülebilir" yapmanın tek yolu şifreleri
geri döndürülebilir bir biçimde (düz metin ya da şifre çözülebilir) tutmak,
ki bu README v6.11/v6.61'de bilinçli olarak reddedilen mimariyi tersine
çevirir ve `lab.db`'nin USB ile taşındığı, HTTPS olmadığı bu ortamda ciddi
bir güvenlik açığı olur. Yönetici zaten yeni bir şifre **belirleyebiliyor**
(`/kullanici/{id}/sifre` — kendisi yazdığı için görmesine gerek yok) ve
personelin kendi `/sifre` isteğini onaylayabiliyor (v6.61) — düz metin o
akışta da yöneticiye hiç uğramıyor, yalnızca hash geçiyor. Kullanıcıya bu
kısıtlama ve mevcut alternatifler anlatılıp nasıl ilerlemek istediği
soruldu.

## Test edildi

Sunucu ayağa kaldırılıp test hasta + `ivf_icsi` cycle açıldı, cycle'ın OPU
aşamasına "İşlemi Yapan" olarak "Ayse Demir" yazıldı, ayrı bir test
`sperm_dondurma` kaydı da aynı adla oluşturuldu. `ayse` kullanıcısı
`/kullanici/2/duzenle` ile "Ayse Yilmaz" / `ayse2` yapıldı: hem
`islem_yapan.yapan_ad` hem `sperm_dondurma.yapan_ad` satırlarının otomatik
"Ayse Yilmaz"a güncellendiği doğrulandı. Doğrulama hataları (boş ad, başka
bir kullanıcıyla çakışan kullanıcı adı, Türkçe karakter içeren kullanıcı
adı) ayrı ayrı denendi, hepsi doğru hata mesajıyla döndü; aynı kullanıcı
adını değiştirmeden yeniden gönderme de sorunsuz kabul edildi. Ekranın
yeni "Adını / kullanıcı adını değiştir" bölümünün bastığı doğrulandı.
Kullanıcı ve hasta kayıtları eski haline döndürüldü, test verileri
(hasta/cycle/specimen/sperm_dondurma/tasiyici/oturum) temizlendi.

# v6.107 — Resmî form ekranı: ekrana sığdırma

Kullanıcının isteği: "Embriyoloji özet formu ve ART lab raporu çıktısı
yapılacak yapılan ekrana formlar sığmıyor. Daha düzgün tam görünür olsun.
Bir de yazdır butonu çalışmıyor. Printer bağlantısı çıksın."

## Ne değişti

- **Formlar artık ekrana sığıyor.** `.kalipkap` (form ızgarasının kendisi)
  kâğıdın doğal genişliğinde kalmak zorundaydı (660px Özet, 980px ART Lab
  — amblemin yeri buna göre yüzdeyle hesaplanıyor), dar bir telefon
  ekranında bu, yatay kaydırma gerektiriyordu — kullanıcının bildirdiği
  "sığmıyor" tam olarak buydu. Ölçüldü: Playwright ile 375/390px
  genişliklerde `.kagit` içinde ~300-620px'lik bir taşma vardı.
  `templates/form.html`'e yeni bir `.kalipolcek` sarmalayıcı ve küçük bir
  betik eklendi: `.kalipkap`'ı **bütün olarak** (`transform: scale`) mevcut
  ekran genişliğine küçültüyor. Punto, sütun genişlikleri, amblemin yeri
  hepsi aynı oranda küçüldüğü için hiçbir şey bozulmuyor — sadece küçük bir
  kâğıt görüyormuş gibi. `form_kalip.json`'a dokunulmadı, "kalıba dokunma"
  kuralı bozulmadı; bu tamamen ekrandaki bir görüntüleme meselesi.
- **Yazdırma etkilenmedi.** `@media print` bu yeni ölçeği `transform: none
  !important` ile devre dışı bırakıyor (satır içi `style` yazıldığı için
  `!important` şart) — çıktı her zaman kâğıdın A4'e sığdırılmış gerçek
  boyutunda. Bunun ayrı bir mekanizma olduğunu unutma: A4'e sığdırma
  (`s.olcek`) sunucuda hesaplanıyor ve yazdırırken geçerli, ekrana sığdırma
  (`oran`) tarayıcıda hesaplanıyor ve yalnızca görüntülemede geçerli —
  ikisi birbirinin yerine geçmiyor, ikisi de gerekli.
- **"Yazdır" düğmesi test edildi, kod tarafında çalıştığı doğrulandı.**
  Playwright ile `window.print` üzerine bir gözlemci konup düğmeye
  tıklandı: her iki formda da, üç farklı ekran genişliğinde çağrıldığı
  doğrulandı. Yazdırma medyası emüle edilip PDF üretildi, iki form da
  sorunsuz bastı (`page.pdf()` ile), konsolda yeni bir hata görülmedi.
  Bu ortamda "yazdır çalışmıyor" hatası **tekrarlanamadı** — kod düzeyinde
  bir bug bulunamadı. En olası açıklama: kullanıcı bildirmeden önce ekran
  sığmıyordu, düğmeye ulaşmak/görmek zor olabiliyordu ya da yazdırma
  önizlemesi taşan/bozuk görünüyordu; sığma düzeltmesi bunu dolaylı olarak
  çözmüş olabilir. Sorun devam ederse kullanıcıdan tam olarak ne olduğu
  (hiçbir şey mi olmuyor, önizleme mi bozuk çıkıyor, hangi cihaz/tarayıcı)
  istendi — `window.print()` bir web sayfasının yazıcı bağlantısını açması
  için tek standart yol, bunun ötesinde JS'ten yapılabilecek başka bir şey
  yok.

## Test edildi

Sunucu ayağa kaldırılıp Playwright ile üç viewport genişliğinde (375, 390,
1280px) hem Embriyoloji Özet hem ART Lab formu açıldı. Düzeltmeden önce
`.kagit`'in `scrollWidth`'i `clientWidth`'ten büyüktü (taşma vardı);
düzeltmeden sonra üçünde de eşit çıktı (taşma yok). `transform` matrisinin
gerçekten uygulandığı (`getComputedStyle`) ve `.kalipolcek`'in yüksekliğinin
ölçeklenmiş içeriğe göre doğru ayarlandığı doğrulandı. Yazdırma medyası
emüle edilip `.kalipkap`'ın `transform: none`'a döndüğü, `.kalipolcek`'in
doğal (ölçeklenmemiş) yüksekliğe geri döndüğü ve iki formun da PDF olarak
sorunsuz basıldığı (`page.pdf()`) doğrulandı — ekran ölçeği yazdırmaya hiç
karışmıyor. "Yazdır" düğmesinin her denemede `window.print()`'i doğru
çağırdığı ayrıca doğrulandı. Test oturum jetonu temizlendi.

# v6.108 — Ekrana sığdırma: yükseklik de hesaba katıldı

Kullanıcının izleyen mesajı: "Formları basıyor sıkıntı yok. Fakat basmadan
önce formlara baktığım ekranda formun tamamını göstermiyor ekranda kesik
gözüküyor. Tam görünsün. Önizlenim gibi basmadan önce kontrol edeyim."

v6.107'de yazdırma düğmesinin çalıştığı doğrulanmış, ekrana sığdırma da
eklenmişti — ama yalnızca **genişlik** hesaba katılmıştı. Playwright ile
ölçüldü: dar bir telefon ekranında (390px) genişlik zaten kısıtlayıcı
olduğu için form küçülüyor ve dikeyde de sığıyordu, ama **geniş bir
masaüstü/mini PC ekranında** (1280px) genişlik hiç kısıtlamıyor (form
zaten dar), ölçek 1 kalıyor ve dikey Özet formu (doğal 1040px boy) 900px'lik
ekrandan 153px taşıp kesik görünüyordu — kullanıcının "kesik gözüküyor"
bildirdiği tam olarak buydu.

## Ne değişti

- `templates/form.html`'deki `formlariSigdir()` betiği artık **hem
  genişliğe hem yüksekliğe** sığdırıyor: `window.innerHeight` eksi
  sarmalayıcının sayfa üstündeki başlangıç konumu (`getBoundingClientRect
  ().top`) kadar dikey alan hesaplanıyor, genişlik ve yükseklik oranlarının
  **küçük olanı** kullanılıyor — tıpkı bir yazıcı önizlemesinin "sayfaya
  sığdır" görünümü gibi, kâğıdın **tamamı** her zaman tek ekranda görünüyor.
- Yükseklik hesabı yalnızca sayfa yüklendiğinde ve `resize`/
  `orientationchange`'de yapılıyor, kaydırma pozisyonuna göre değil —
  yoksa kullanıcı sayfayı kaydırdıkça ölçek anlamsızca değişirdi.
- Yazdırma yine etkilenmedi (`@media print`'teki `transform: none
  !important` sıfırlaması zaten hem genişlik hem yükseklik ölçeğini
  kapsıyordu, ek bir değişiklik gerekmedi).

## Test edildi

Playwright ile dört ekran boyutunda (375x812, 390x844 — telefon; 1280x900,
1920x1080 — masaüstü) hem Embriyoloji Özet hem ART Lab formu açıldı.
Düzeltmeden önce 1280x900'de Özet formu 153px taşıyordu
(`getBoundingClientRect().bottom > innerHeight`); düzeltmeden sonra
**dördünde de** hem yatay (`.kagit`'in `scrollWidth == clientWidth`) hem
dikey (`.kalipolcek`'in alt kenarı `innerHeight`'in içinde) taşma
kalmadığı doğrulandı. Yazdırma medyası tekrar emüle edilip `.kalipkap`'ın
`transform: none`'a döndüğü, `.kalipolcek`'in doğal yüksekliğe geri
döndüğü ve PDF çıktısının öncekiyle birebir aynı boyutta kaldığı yeniden
doğrulandı. Test oturum jetonu temizlendi.

# v6.109 — `transform-origin` eksikti: ölçek ortaya doğru büzülüyordu

Kullanıcı bir ekran görüntüsü gönderdi: mobilde formun kartı büyük bir
boşlukla başlıyor, içerik alt kenarda kesik ve sıkışık görünüyordu. Mesajı:
"Mobilde böyle gözüküyor. Masaüstünde de kesik tam ekran değil."

v6.107/v6.108'in ölçek hesabı doğruydu ama `.kalipkap`'a hiçbir zaman
`transform-origin` yazılmamıştı — CSS'in varsayılanı `center center`.
`transform: scale(oran)` bu yüzden kâğıdı **sol üst köşeden değil ortadan**
küçültüyordu; `.kalipolcek` sarmalayıcının yüksekliği betikte "küçültülmüş
boy" kadar (sol-üstten sayarak) ayrıldığı için ikisi uyuşmuyordu — içeriğin
üst yarısı sarmalayıcının üstüne taşıp görünmez oluyor (`overflow: hidden`),
alt yarısı da sarmalayıcının dışına taşıp kırpılıyordu. Ekranda kalan tek
şey ortadaki dar bir şerit — tam olarak ekran görüntüsündeki görünüm.

## Ne değişti

- `static/style.css`'e tek kural: `.kalipkap { transform-origin: top left;
  }`. Artık küçültme sol-üst köşeden başlıyor, `.kalipolcek`'in ayırdığı
  alanla (`dogalYukseklik * oran`, sol-üstten sayarak hesaplanmıştı) birebir
  örtüşüyor.
- `form.html`'e ve CLAUDE.md'ye bu hatanın nedenini ve dersini açıklayan bir
  not eklendi: `transform: scale()` kullanılan her yeni yerde
  `transform-origin` açıkça yazılmalı, varsayılana güvenilmemeli.

## Neden v6.107/v6.108'in testleri bu hatayı yakalayamadı

O testler yalnızca `.kalipolcek` sarmalayıcının **kendi**
`getBoundingClientRect()`'ine bakıyordu (`scrollWidth`, `clientWidth`,
`bottom <= innerHeight`) — bunlar sarmalayıcının içindeki `.kalipkap`'ın
GÖRSEL olarak nereye render edildiğinden tamamen bağımsız, `transform-
origin` ne olursa olsun hep doğru çıkıyordu. Hatayı yalnızca bir ekran
görüntüsü (ya da içerideki `.kalip` tablosunun sarmalayıcıya göre kendi
konumunu ölçmek) ortaya çıkarabilirdi.

## Test edildi

Sunucu ayağa kaldırılıp Playwright ile önce içerideki `.kalip` tablosunun
`.kalipolcek` sarmalayıcıya göre üst kenar farkı (`gap_above`) ölçüldü:
düzeltmeden önce bu fark sıfır değildi (içerik sarmalayıcının içinde
ortalanmış duruyordu), düzeltmeden sonra mobil (390x844) ve masaüstü
(1280x900) viewport'larında, hem Embriyoloji Özet hem ART Lab formunda
`gap_above: 0` çıktı — yani ölçeklenmiş içerik artık tam sarmalayıcının
sol-üst köşesinden başlıyor. Dört kombinasyonun ekran görüntüsü alınıp
görsel olarak da doğrulandı: form artık baştan sona, boşluksuz ve kesiksiz
görünüyor. Yazdırma medyası yeniden emüle edildi — `.kalipkap`'ın
`transform: none`'a döndüğü ve PDF çıktısının boyutunun (Özet 106081 bayt,
ART Lab 63578 bayt) düzeltmeden önceki ile birebir aynı kaldığı doğrulandı;
bu değişiklik ekranı etkiliyor, yazdırmayı hiç etkilemiyor. Test oturum
jetonu ve sunucu süreci temizlendi.

# v6.110 — Cycle ekranına türetilmiş embriyoloji özeti

Kullanıcının isteği: "Hasta tedavi ekranından Oositler ve Fotoğraf ekleyi
kaldır. Kısa bir özet kısmı olsun. Kaç yumurta alındı m2 kaç döllenen kaç
cleavage kaç Blastokist kaç gibi. Diğer ekranlarda ilgili bilgi girildikçe
bu özete eklensin."

Cycle ekranındaki "Oositler" numara şeridi (her oositi tek tek listeleyen,
kendi başına pek bilgi vermeyen bir kart) ve genel amaçlı "Fotoğraf ekle"
düğmesi (parametresiz, `/cycle/{id}/foto-ekle`'ye giden — CLAUDE.md'nin
"cycle ekranında fotoğraf olmaz" kuralının, v6.20, sessiz bir istisnasıydı)
kaldırıldı. Yerine embriyoloji ilerlemesini tek bakışta özetleyen bir kart
geldi: Toplanan oosit, M2 (olgun), Döllenen (2PN), Cleavage, Blastokist.

## Ne değişti

- `app.py`'de yeni `cycle_ozet(cycle_id, kodlar)` fonksiyonu —
  `disari.istatistikler()`'deki lab-geneli sayımların (v6.38, "sayaç
  tutma, her açılışta türet") tek-cycle hali. Ayrı bir sayaç tutulmuyor:
  sayılar her sayfa yüklemesinde `specimen` ve `olay` tablolarından anlık
  hesaplanıyor, bu yüzden bir kayıt düzeltilir ya da iptal edilirse özet
  otomatik doğru kalır.
- `cycle_detay()` rotası artık `cycle_asamalari()`'nin zaten hesapladığı
  aşama kodlarını `cycle_ozet()`'e veriyor — özet yalnızca **bu cycle
  tipinde gerçekten var olan** aşamalar için bir satır gösteriyor
  (`fet` gibi OPU/ICSI'siz bir tipte kart hiç basılmıyor, `oosit_cryo`'da
  yalnızca Toplanan + M2 görünüyor). "0" ile "ölçülmedi" farklı şeyler —
  ilgisiz bir sayı için satır hiç yok, kart tamamen kayboluyor.
- `templates/cycle_detay.html`: "Oositler" kartı ve parametresiz "Fotoğraf
  ekle" düğmesi kaldırıldı, yerine `istatistik.html`'deki `.ozet.ozetsar`
  ızgarasının aynısını kullanan "Embriyoloji özeti" kartı eklendi.
- `metinler.py`'ye `embriyoloji_ozeti`, `ozet_m2`, `ozet_dollenen`
  anahtarları eklendi (mevcut `cleavage_ad`/`blastokist_ad`/
  `toplanan_oosit` yeniden kullanıldı); yalnızca bu ekranda kullanılan
  `oositler`/`henuz_oosit_yok`/`denudasyondan_ekle` anahtarları kaldırıldı.
- **Fotoğraf eklemek kaldırılmadı** — yalnızca cycle ekranındaki genel
  giriş noktası kaldırıldı. `/cycle/{id}/foto-ekle` rotası aynen duruyor,
  her aşama ekranının kendi "Fotoğraf ekle" düğmesi (denüdasyon, ICSI,
  fertilizasyon, cleavage, blastokist, çözme) değişmedi.

## Test edildi

Sunucu ayağa kaldırılıp gerçek bir `ivf_icsi` test tedavisi açıldı: önce 6
oosit toplandı (özet "6 / 0 / 0 / 0 / 0" gösterdi), sonra sırayla 4'ü
olgun (M2) işaretlendi, 3'ü 2PN döllendi, 3'ü cleavage (bilerek gün 2 VE
gün 3'te iki ayrı kayıtla — DISTINCT specimen sayımının çift saymadığı
doğrulandı) ve 2'si blastokist değerlendirildi. Her adımdan sonra
`/cycle/{id}` yeniden çekilip özetin sırasıyla 6/0/0/0/0 → 6/4/0/0/0 →
6/4/3/0/0 → 6/4/3/3/2 olarak **anında** güncellendiğini gösterdi — ayrı bir
kayıt olmadığı için hiçbir ek adım gerekmedi. Ayrıca bir `fet` test
tedavisinde özet kartının hiç basılmadığı, bir `oosit_cryo` test
tedavisinde yalnızca Toplanan + M2 satırlarının göründüğü doğrulandı.
Playwright ile mobil (390px) ve masaüstü (1280px) ekran görüntüsü alınıp
`.ozetsar` ızgarasının 5 öğeyi düzgün sardığı (mobilde 3+2, masaüstünde
4+1) görsel olarak da doğrulandı. Etkilenen diğer ekranlar (ICSI, Fert,
Cleavage, Blastokist, hasta kartı, ana ekran, aşama ekranlarındaki kendi
"Fotoğraf ekle" düğmeleri) 200 döndürüp hatasız yüklendi. Test hasta/
cycle/specimen/olay kayıtları ve oturum jetonu temizlendi, sunucu
kapatıldı.

# v6.111 — Cycle ekranına "Hasta kartı" bağlantısı

Kullanıcının isteği: "Hasta tedavi ana ekranında Hastanın Hasta Kartına
gidilebilsin." Cycle ekranından (`/cycle/{id}`) hastanın tüm geçmişine
(`/hasta/{id}`) açık, etiketli bir bağlantı yoktu — üst çubuktaki geri oku
teknik olarak oraya gidiyordu ama bu bilinçli bir gezinme değil, "bir
önceki ekran" konvansiyonunun bir yan etkisiydi ve etiketsizdi.

## Ne değişti

- `templates/cycle_detay.html`'de aşama düğmelerinin hemen altına
  `<a class="dugme ikincil" href="/hasta/{{ c.hasta_id }}">` eklendi.
  Metin ve hedef, `_cyclesatir.html`'in ay listesindeki "Hasta kartı"
  düğmesiyle (v6.31, v6.63'te bugünkü adını aldı) **birebir aynı** —
  `metin("hasta_kaydi")` yeniden kullanıldı, yeni bir metin anahtarı ya da
  yeni bir CSS sınıfı gerekmedi (`.dugme.ikincil` zaten var).

## Test edildi

Sunucu ayağa kaldırılıp bir test tedavisi açıldı, `/cycle/{id}` çekilip
düğmenin doğru metinle (`Hasta kartı`) ve doğru adresle (`/hasta/{hasta_id}`)
basıldığı doğrulandı. Playwright ile düğmeye gerçekten tıklanıp tarayıcının
`/hasta/{id}`'ye gittiği ve sayfanın hasta adını içerdiği doğrulandı; mobil
ekran görüntüsüyle düğmenin diğer ikincil düğmelerle (Değişiklik geçmişi,
İşlemi bitir, Excel'e aktar) aynı görünümde, aşama düğmelerinin hemen
altında durduğu görsel olarak da onaylandı. Test hasta/cycle kayıtları ve
oturum jetonu temizlendi, sunucu kapatıldı.

# v6.112 — İki özet kutusu tek kutuda birleşti

Kullanıcının isteği: "Tedavi ana sayfasının en üstünde şuanda toplanan
oosit kayıtlı Folikül var. Bir de toplanan oosit M2 (olgun) Döllenen
(2PN) cleavage Blastokist var. Bu ikisi birleşsin sayfanın en üstünde
Folikül Sayısı, Toplanan Yumurta Sayısı, M2(Olgun) Yumurta Sayısı,
Döllenen Yumurta (2PN) Sayısı, Cleavage Sayısı, Blastokist Sayısı
Şeklinde bilgilendirme alanı olsun."

v6.110'da eklenen "Embriyoloji özeti" kutusu ile ekranın en üstünde zaten
duran Folikül/Toplanan Oosit/Kayıtlı kutusu ayrı ayrı duruyordu. Bu ikisi
birleştirilirken bir tutarsızlık da ortaya çıktı: v6.110'un "Toplanan"
sayısı yanlışlıkla specimen kaydı sayısını (üstteki kutunun "Kayıtlı"sıyla
aynı şey) kullanıyordu, üstteki kutunun kendi "Toplanan Oosit"i ise OPU'da
elle girilen sayıydı — iki kutu ayrı dururken fark edilmemişti, tek kutuda
yan yana durunca görünür olurdu.

## Ne değişti

- `app.py` `cycle_ozet(cycle, kodlar)` artık `cycle_id` yerine **tüm cycle
  satırını** alıyor (Folikül ve OPU sağ/sol sayıları için) ve altı satır
  döndürüyor: Folikül (koşulsuz, cycle seviyesinde), Toplanan (yalnızca
  `opu` aşaması varsa — artık `opu_sag_oosit + opu_sol_oosit`, specimen
  `COUNT(*)` değil), M2, Döllenen, Cleavage, Blastokist (her biri kendi
  aşaması varsa).
- `templates/cycle_detay.html`: sol sütunun ilk kartı (eski Folikül/
  Toplanan/Kayıtlı) ile sağ sütundaki "Embriyoloji özeti" kartı **tek
  karta** birleşti, sayfanın en üstünde. "Kayıtlı" satırı kullanıcının
  verdiği listede olmadığı için düşürüldü.
- `metinler.py`'ye `ozet_folikul`, `ozet_toplanan`, `ozet_cleavage`,
  `ozet_blastokist` eklendi (`ozet_m2`/`ozet_dollenen` v6.110'dan kalanlar,
  metni güncellendi); `cleavage_ad`/`blastokist_ad` bilerek yeniden
  kullanılmadı çünkü onlar başka ekranlarda (`cleavage_sil.html` gibi)
  farklı bir cümlenin parçası.
- `cycle_detay()` rotasındaki artık kullanılmayan `specimenler` (üç alt
  sorgulu) ve `taraf_sayilari` sorguları kaldırıldı — kaldırılan kartla
  birlikte hiçbir yerde okunmuyorlardı.

## Test edildi

Sunucu ayağa kaldırılıp Folikül=15, sağ 4/sol 2 OPU girilen bir test
tedavisi açıldı; 6 specimen, 4 M2, 3 döllenen, 3 cleavage, 2 blastokist
kaydı eklendi. `/cycle/{id}` çekilip tek kutuda altı sayının da doğru
(15/6/4/3/3/2) ve sağ/sol kırılımının ("sağ 4 · sol 2") Toplanan'ın altında
göründüğü doğrulandı; "Kayıtlı" ya da ayrı bir "Embriyoloji özeti"
başlığının ekranda **ikinci kez** basılmadığı (`grep -c` ile tek eşleşme)
kontrol edildi. Bir `fet` test tedavisinde kutunun yalnızca "Folikül
sayısı: —" satırıyla, tek satır olarak göründüğü doğrulandı. Playwright
ile mobil (390px, 3+3 sarma) ve masaüstü (1280px, 4+2 sarma) ekran
görüntüsü alınıp görsel olarak onaylandı. Etkilenen diğer ekranlar (ICSI,
Fert, Cleavage, Blastokist, hasta kartı, ana ekran, `/istatistik`) 200
döndürdü. `opu.html`'in kendisinin ayrı `toplanan_oosit`/`folikul`
etiketlerinin (bu değişiklikten etkilenmemesi gereken) dokunulmadan
kaldığı doğrulandı. Test hasta/cycle/specimen/olay kayıtları ve oturum
jetonu temizlendi, sunucu kapatıldı.

# v6.113 — Zaman çizelgesi tablosu mobilde kaydırılabilir oldu

Kullanıcı bir ekran görüntüsü gönderdi: tedavi ekranındaki "Zaman
çizelgesi" tablosunun sağ sütunu ("OPU'dan bu yana") kesik görünüyor,
değerler ("-1", "2", "3"...) yarım kalıyordu. Mesajı: "Tedavi ana
sayfasındaki zaman çizergesi tablosu kesik olmuş tablo tam görünmüyor."

Sebep: `.cizelge` tablosu dört sütun ve her hücre `nowrap` (README v6.37 —
sayılar okunaklı kalsın diye bilinçli bir karar, sütunları daraltmak yanlış
çözüm olurdu). Dar bir telefon ekranında (390px) tablonun doğal genişliği
kartın genişliğini aşıyor ve taşan kısım için hiçbir kaydırma mekanizması
yoktu — taşan sütun sessizce görünmez kalıyordu.

## Ne değişti

- `templates/cycle_detay.html`'deki zaman çizelgesi tablosu ve
  `templates/istatistik.html`'deki iki `.cizelge` tablosu (Oranlar, Aylara
  göre) yeni bir `<div class="cizelgekap">` ile sarmalandı.
- `static/style.css`'e `.cizelgekap { overflow-x: auto; }` eklendi —
  `form.html`'in `.kalipolcek`'inin (v6.107) kullandığı aynı desen: tabloyu
  değil, onu saran kutuyu kaydırılabilir yap. Tablonun kendisi hâlâ
  `nowrap`, sütun genişlikleri değişmedi.

## Test edildi

Sunucu ayağa kaldırılıp kullanıcının bildirdiğiyle birebir aynı senaryo
kuruldu (Fertilizasyon 08:30, OPU 10:20, ICSI 12:35, Denüdasyon 14:03,
"-1.8 sa" gibi eksi değerler dahil). Playwright ile 390px genişlikte
ölçüldü: tablonun doğal genişliği (~471px) sarmalayıcının genişliğini
(~356px) gerçekten aşıyordu (düzeltmeden önceki hatayı doğruluyor);
düzeltmeden sonra sarmalayıcı kaydırılıp sonuna gidildiğinde
(`scrollLeft + clientWidth >= scrollWidth`) "OPU'dan bu yana" sütunundaki
tüm değerlerin ("-1.8 sa", "2.2 sa", "3.7 sa") tam göründüğü hem ölçüm hem
ekran görüntüsüyle doğrulandı. `/istatistik` ve diğer etkilenen ekranlar
200 döndürdü. Test hasta/cycle/specimen/olay kayıtları ve oturum jetonu
temizlendi, sunucu kapatıldı.

# v6.114 — Zaman çizelgesi kaydırma yerine genişletildi

Kullanıcının izleyen isteği: "yatay kaydırma yerine sadece zaman
çizergesini uzat. Başka hiçbir yeri uzatmadan. Ne üstündeki işlemi bitir
butonunu ne de Embriyoloji özet formu butonunu uzat." v6.113'ün
`.cizelgekap` kaydırma çözümü kullanıcının istediği yön değildi — kaydırma
yerine kartın kendisinin genişlemesi istendi, ama sadece o kart; aynı
sütundaki diğer düğmeler (İşlemi bitir, Embriyoloji Özet Formu, ART Lab
Raporu, Excel'e aktar, Sil) eskisi gibi kalmalı.

## Ne değişti

- `templates/cycle_detay.html`: "Zaman çizelgesi" kartı `.sutunlar`'ın
  (iki sütunlu bölge) **dışına** taşındı — artık iki sütunun ikisini
  birden kapsayan tam genişlikte, `.kap.genis`in kendi `--genis-sutun`
  genişliğinde (geniş masaüstünde ~940px'e kadar) duruyor. `.cizelgekap`
  kaydırma sarmalayıcısı bu karttan kaldırıldı.
- Diğer düğmeler (`İşlemi bitir`, `Hasta kartı`, `Değişiklik geçmişi`,
  form/Excel düğmeleri) hâlâ kendi `.sutun`larının içinde — genişlikleri
  hiç değişmedi.
- `/istatistik`'in iki `.cizelge` tablosundaki `.cizelgekap` kaydırma
  sarmalayıcısına dokunulmadı (kullanıcının isteği yalnızca tedavi
  ekranıyla ilgiliydi, o ekranı bu değişiklik kapsamıyor).

## Bilinen sınır

Bu çözüm yalnızca **gerçek iki-sütunlu görünümde** (geniş masaüstü)
işe yarıyor — `.sutunlar` iki 380px'lik sütunu yan yana sığdıramadığı her
genişlikte (dar telefon dahil, o durumda zaten tek sütuna diziliyor) kart,
tek sütunla aynı genişlikte kalıyor ve tablo hâlâ taşabilir. Kullanıcının
orijinal ekran görüntüsü (geniş bir tarayıcı penceresinden, iki sütunlu
görünümden alınmıştı) bu düzeltmeyle tam çözülüyor; gerçekten dar bir
telefonda dördüncü sütun yine kesik görünebilir — kaydırma bilerek
kaldırıldığı için. Kullanıcı bu ödünü bilerek kabul etti.

## Test edildi

Sunucu ayağa kaldırılıp aynı test senaryosu (Fertilizasyon/OPU/ICSI/
Denüdasyon saatleri) dört ekran genişliğinde ölçüldü:
- **390px (telefon):** `.sutunlar` zaten tek sütuna diziliyor, kart 358px
  — değişmedi, tablo (470px) hâlâ taşıyor (bilinen sınır, yukarıda).
- **1280px:** container 748px ama iki 380px sütun + boşluk (776px) hâlâ
  sığmıyor, `.sutunlar` tek sütuna diziliyor — kart 748px, tablo (746px)
  **tam sığıyor**.
- **1440px ve 1920px:** gerçek iki sütun yan yana (`sutun` 446px'er) ama
  Zaman çizelgesi kartı 908px — tablo (906px) **tam sığıyor**, "İşlemi
  bitir"/"Excel'e aktar" gibi düğmeler hâlâ 446px'lik kendi sütununda,
  genişlikleri değişmedi.
Playwright ile 1440px'de ekran görüntüsü alınıp "OPU'dan bu yana"
sütunundaki tüm değerlerin ("-1.8 sa", "2.2 sa", "3.7 sa") kesiksiz
göründüğü ve diğer düğmelerin dar sütunda kaldığı görsel olarak da
doğrulandı. Test hasta/cycle/specimen/olay kayıtları ve oturum jetonu
temizlendi, sunucu kapatıldı.

# v6.115 — Hasta ve eş adı her zaman büyük harfle kaydedilir

Kullanıcının isteği: "Bütün hasta ve eş isimleri büyük harf olsun. Nasıl
yazarsam yazayım sonunda büyük harflerle kaydolsun."

## Ne değişti

- `app.py`'ye `tr_buyuk()` eklendi — hasta/eş adını her zaman büyük harfe
  çeviriyor, üç yazma yolunda da (`hasta_kaydet()`, `hasta_guncelle()`,
  `sperm_dondurma_yeni_hasta_kaydet()`) INSERT/UPDATE'ten hemen önce
  çağrılıyor.
- **Python'un `str.upper()`'ı tek başına Türkçe için yanlış** — "Turkish I
  problem": varsayılan Unicode kuralı küçük 'i'yi noktasız 'I' yapar
  ("iyi" → "IYI" olurdu, doğrusu "İYİ"). `tr_buyuk()` önce 'i'yi 'İ'ye
  çevirip sonra `.upper()` çağırıyor — 'ı' zaten Unicode'da doğru
  çevriliyor ('ı'.upper() == 'I'), ç/ğ/ö/ş/ü'de sorun yok.
- Hata dönüşünde (form doğrulaması patlarsa) kullanıcı hâlâ **kendi
  yazdığını** görüyor (v6.21 kuralı) — `tr_buyuk()` yalnızca gerçek
  yazma anında çağrılıyor, hata şablonuna geçilen değerlere dokunmuyor.
- **`goc_040`** eklendi: daha önce girilmiş `hasta.ad_soyad`/`es_adi`
  kayıtlarını aynı kurala getiriyor (idempotent, `tr_buyuk()`'ün göç
  içindeki birebir kopyasıyla — göç betikleri `app.py`'yi import etmiyor).
- **Personel adı (`kullanici.ad_soyad`) bu kuralın dışında** — yalnızca
  hasta ve eş isimleri için, kullanıcı yönetimi ekranındaki isimler
  değişmedi.

## Test edildi

Sunucu ayağa kaldırılıp üç yazma yolu da gerçek rotalar üzerinden
denendi: `/hasta/yeni`'ye "ışık öztürk çelik" / eş adı "mehmet iyi
yılmaz" gönderildi → `IŞIK ÖZTÜRK ÇELİK` / `MEHMET İYİ YILMAZ` olarak
kaydedildiği doğrulandı (Türkçe 'ı'/'i' ayrımı doğru). `/hasta/{id}/
duzenle`'de "ilker iğdemir" → `İLKER İĞDEMİR`, `/sperm-dondurma/
yeni-hasta`'da "ibrahim yıldız" → `İBRAHİM YILDIZ` olarak kaydedildiği
doğrulandı. `goc_040` elle çalıştırılıp önceden lowercase girilmiş bir
test kaydının ("eski kayıt ışık" / "eş ismi çiğdem") doğru büyük harfe
çevrildiği (`ESKİ KAYIT IŞIK` / `EŞ İSMİ ÇİĞDEM`), ikinci çalıştırmada
hiçbir satırın değişmediği (idempotent) doğrulandı. Sunucu yeniden
başlatılıp göçün açılışta kendiliğinden bulunup `goc_kaydi`'na
kaydedildiği doğrulandı. Test hasta kayıtları ve oturum jetonu
temizlendi, sunucu kapatıldı.

# v6.116 — Küçük harfle Türkçe isim araması sonuç vermiyordu

Kullanıcının bildirdiği hata: "hasta adı veya soyadı ile ararken küçük
harf ile arama yaparsam hasta çıkmıyor." v6.115'in doğrudan sonucuydu:
hasta adları artık her zaman büyük harfle kayıtlı, ama arama sorguları
kullanıcının yazdığı terimi olduğu gibi `LIKE`'a veriyordu.

## Sebep

SQLite'ın `LIKE` operatörü büyük/küçük harf eşitlemesini **yalnızca
ASCII harflerde** yapıyor — `'ali' LIKE '%ALI%'` eşleşir. Türkçe'ye özgü
ı/İ, ş/Ş, ğ/Ğ, ö/Ö, ü/Ü, ç/Ç için eşitleme **yapmıyor**: `'ışık' LIKE
'%IŞIK%'` eşleşmiyor, çünkü küçük 'ı' ve büyük 'I' farklı Unicode
karakterler ve SQLite bunları Türkçe kuralına göre eşdeğer saymıyor.
v6.115 öncesinde isimler kullanıcının yazdığı gibi (çoğunlukla karışık
harfle) duruyordu, isim + arama terimi tesadüfen aynı harf biçimini
paylaşma ihtimali daha yüksekti. Tüm isimler büyük harfe sabitlenince bu
gizli sorun görünür oldu: Türkçe harf içeren hemen her isimde küçük
harfle arama sıfır sonuç veriyordu.

Doğrulama (Python REPL'de SQLite ile):
```
'ali'    LIKE '%ALI VELI%' -> eşleşir   (ASCII, sorun yok)
'ışık'   LIKE '%IŞIK ÖZTÜRK%' -> eşleşmez  (Türkçe ı/İ)
'öztürk' LIKE '%IŞIK ÖZTÜRK%' -> eşleşmez  (Türkçe ö/ü)
```

## Ne değişti

`app.py`'de `h.ad_soyad LIKE` içeren dört sorguda (`/hastalar`,
`/cycle/{id}/androloji/sperm-baglama`, `/cryo`'nun hem embriyo hem sperm
dondurma aramaları) yalnızca `ad_soyad` karşılaştıran `?` parametresi
`f"%{tr_buyuk(ara)}%"`'e çevrildi. Aynı sorgudaki **diğer** alanlar
(dosya no, taşıyıcı etiketi, konum yolu, örnek kodu) dokunulmadan kaldı
— onlar büyük harfe sabitlenmiş değil, `tr_buyuk()` onlara da
uygulanırsa küçük harfli bir etiket/yol araması bozulurdu.

## Test edildi

Sunucu ayağa kaldırılıp `IŞIK ÖZTÜRK ÇELİK` adlı bir test hastası ve ona
bağlı embriyo/sperm dondurma taşıyıcıları oluşturuldu. Dört arama
ekranının hepsinde "ışık", "öztürk", "çelik" (küçük harf) ve "IŞIK"
(büyük harf) terimleriyle hastanın bulunduğu doğrulandı. Taşıyıcı etiketi
araması ("tst-1", "emb-tst") ayrı test edilip `tr_buyuk()`'ten
etkilenmediği (küçük harfle hâlâ çalıştığı) doğrulandı. Diğer ekranlar
(`/`, `/hastalar`, `/cryo`, `/cycle/{id}`) 200 döndürdü. Test hasta,
cycle, specimen, olay, taşıyıcı, sperm dondurma kayıtları ve oturum
jetonu temizlendi, sunucu kapatıldı.

# v6.117 — Zaman çizelgesi: genişletme yetmedi, kaydırma da istenmiyordu

Kullanıcının bildirdiği hata, v6.114'ün tam öngördüğü "bilinen sınır"ın
gerçekleşmesiydi: "Tedavi ana sayfasında zaman çizergesi mobilde tam
gözükmüyor. Kaydırmalı olarak görünüyor. Bakınca görünecek şekilde olsun.
İlk bakışta görünsün ekranı kaydırarak değil."

## Sebep

v6.114 `.cizelgekap`'ın (v6.113) `overflow-x: auto` kaydırma
sarmalayıcısını kaldırıp kartı `.sutunlar`'ın dışına, tam genişliğe
çıkarmıştı — ama bu yalnızca `.sutunlar` **gerçekten iki sütuna
bölündüğünde** (≳1440px) ek genişlik veriyordu. Dar telefonda `.sutunlar`
zaten tek sütuna dizilmiş olduğu için kart hiç ek genişlik kazanmıyordu
ve artık hiçbir şey taşmayı kırpmıyordu (kaydırma sarmalayıcısı
kaldırılmıştı) — taşan tablo doğrudan **sayfanın kendisini** yatay
kaydırılabilir yapıyordu. Bu, v6.113'ün karta hapsedilmiş kaydırmasından
daha kötü bir sonuçtu ve kullanıcının "ilk bakışta görünsün, kaydırarak
değil" isteğini hiç karşılamıyordu. v6.114'teki "Bilinen sınır" bölümü bu
riski zaten yazmıştı, şimdi gerçekleşti.

## Ne değişti

`templates/cycle_detay.html`: `<table class="cizelge">` artık yeni bir
`<div class="cizelgeolcek">` sarmalayıcının içinde. `static/style.css`'e
eklenen kural (`.cizelgeolcek { overflow: hidden; }` +
`.cizelgeolcek table.cizelge { transform-origin: top left; }`) ve
kartın altına eklenen küçük bir betik (`cizelgeSigdir()`), `form.html`'in
`.kalipolcek`/`formlariSigdir()` deseninin (v6.107, v6.109) birebir
aynısı: tabloyu **kırpmak/kaydırmak yerine bütün olarak `transform:
scale()` ile mevcut genişliğe küçültüyor**. Punto ve hücre aralığı
birlikte küçülür, hiçbir sütun kesilmez, sayfa hiçbir zaman yatay
kaymaz. Yalnızca genişlik hesaba katılıyor — form.html'in aksine bu
tablo ekran yüksekliğini zorlamıyor. `transform-origin: top left` burada
da v6.109'un dersiyle aynı sebeple şart: yoksa küçültme ortaya doğru
büzülüp içeriğin bir kısmını sarmalayıcının üstüne taşırdı.

`/istatistik`'in iki `.cizelge` tablosu `.cizelgekap` kaydırmasında
kaldı — kullanıcının şikâyeti yalnızca "Tedavi ana sayfası"yla
(cycle_detay.html) ilgiliydi, orada değişiklik istenmedi.

## Bilinen sınır kapandı

v6.114'ün "gerçekten dar bir telefonda dördüncü sütun kesik
görünebilir" notu artık geçerli değil: tablo hiçbir genişlikte kesilmiyor
ya da kaydırma gerektirmiyor, yalnızca gerektiğinde (dar ekranda)
görsel olarak küçülüyor. Geniş ekranda v6.114'ün kazancı (tam boyutta,
küçülmeden gösterim) korunuyor — oran zaten ~1 çıkıyor.

## Test edildi

Sunucu ayağa kaldırılıp cycle 1'e (OPU/Denüdasyon zaten kayıtlıydı)
ICSI/Fertilizasyon/Cleavage(gün 2)/Blastokist için `olay` satırları
eklenip altı satırlık bir zaman çizelgesi oluşturuldu. Playwright ile
320, 375, 390, 428, 700, 1000, 1100, 1280, 1360, 1440 ve 1920px
genişliklerde ölçüldü:
- **Hiçbir genişlikte `document.body.scrollWidth >
  document.documentElement.clientWidth` çıkmadı** — sayfa artık hiçbir
  zaman yatay kaymıyor (önceki davranışın tam tersi).
- 320px'te ekran görüntüsüyle tablo tam olarak (dört sütun, "OPU'dan bu
  yana" dahil) kesiksiz, kaydırma göstergesi olmadan doğrulandı.
- 700px ve üstünde oran zaten 1 (tablo doğal boyutunda, `matrix(1,0,0,
  1,0,0)`) — v6.114'ün kazancı korunuyor.
- 375-428px arası oranın 0.72-0.84 arasında kademeli değiştiği,
  hiçbir noktada kırpma olmadığı ölçüldü.
Test `olay` kayıtları ve oturum jetonu temizlendi, sunucu kapatıldı.

# v6.118 — Sperm dondurma onamlarına kapatma düğmeli görüntüleme

Kullanıcının isteği: "Dosya yükleme yapılan bölümde görüntüyü açtıktan
sonra kapatma butonu olsun." İki dosya yükleme bölümü var (Doktor Notu ve
Sperm Dondurma Onamları); ikisi de istendi.

## Sebep

Doktor Notu (`cycle_detay.html`) fotoğrafları zaten `_buyutec.html`'in
paylaşılan büyütecinde (lightbox) açılıyordu — sağ üstte `×` kapatma
düğmesi hep vardı, burada eksik yoktu. Sperm Dondurma Onamları
(`sperm_dondurma_detay.html`) farklıydı: fotoğraf `<a target="_blank"
href="/sperm-onam/{id}">` ile doğrudan **yeni bir tarayıcı sekmesinde**,
ham görüntü dosyası olarak açılıyordu (v6.101'in bilinçli kararı — "PDF
gibi yeni sekme, pixel pixel yakınlaştırma gerekmiyor"). Orası bir HTML
sayfası değil, tarayıcının kendi görüntü görüntüleyicisi; uygulamanın
içine bir "Kapat" düğmesi konamaz, yalnızca sekmeyi kapatmak/geri gitmek
vardı — kullanıcının bahsettiği eksiklik buydu.

## Ne değişti

- `_buyutec.html`'in `window.buyutecAc()`'i **dördüncü, isteğe bağlı bir
  parametre** aldı: `onEki` (görüntü adresinin öneki). Vermeyen çağıran
  hâlâ `/dosya/` alır (bütün embriyoloji ekranları, Doktor Notu dahil —
  davranışları değişmedi).
- `sperm_dondurma_detay.html`: onam **fotoğrafları** (PDF değil) artık
  `<a target="_blank">` yerine Doktor Notu'nun aynı deseniyle
  `<button class="kfoto onamfoto">` — tıklanınca `_buyutec.html`'i
  `onEki="/sperm-onam/"` ile açıyor. Sayfa artık `{% include
  "_buyutec.html" %}` içeriyor ve kendi tıklama betiğini yazıyor (CLAUDE.md
  kuralı: paylaşılan bir global yok, her ekran kendi betiğini yazar).
  Birden çok onam fotoğrafı varsa büyüteçteki ‹ › ile aralarında gezinilir
  (Doktor Notu'nun `doktor_notu_resim_ids` deseninin aynısı, `app.py`'de
  yeni `onam_resim_ids`).
- **PDF onamlar dokunulmadı** — hâlâ yeni sekmede, `target="_blank"`.
  Kullanıcının isteği "görüntüyü açtıktan sonra" diyordu, PDF için
  tarayıcının kendi görüntüleyicisi zaten neredeyse tam ekran ve kendi
  kapatma/geri deneyimini veriyor (v6.81'in PDF gerekçesinin aynısı).

## Test edildi

Sunucu ayağa kaldırılıp gerçek rotalardan (`/cycle/1/doktor-notu-ekle`,
`/sperm-dondurma/yeni-hasta` + `/sperm-dondurma/{id}/onam-ekle`) bir test
görüntüsü ve bir test PDF'i yüklendi. Playwright ile:
- Doktor Notu fotoğrafına tıklanınca büyüteç açıldı (`#buyut` hidden=false),
  `#bimg.src` `/dosya/<id>` idi, `.bkapat`'a tıklanınca büyüteç kapandı
  (hidden=true) — regresyon yok.
- Sperm Onam fotoğrafına tıklanınca büyüteç açıldı, `#bimg.src`
  `/sperm-onam/<id>` idi (yeni `onEki` doğru geçiyor), `.bkapat`'a
  tıklanınca kapandı.
- Ekran görüntüsüyle iki büyütecin de görsel olarak birebir aynı
  (başlık + `×` kapatma düğmesi + Yakınlaştır çubuğu) olduğu doğrulandı.
- Sperm Onam PDF yüklemesi test edildi: bağlantı hâlâ
  `<a class="kfoto pdf" href="/sperm-onam/{id}" target="_blank">` —
  değişmedi.
Test hasta, taşıyıcı, sperm dondurma, `goruntu`/`sperm_dondurma_dosya`
kayıtları, arşiv klasöründeki test dosyaları ve oturum jetonu temizlendi,
sunucu kapatıldı.

## Bilinen not

Test sırasında **bu değişiklikle ilgisiz**, önceden var olan bozuk bir
kayıt bulundu: `sperm_dondurma.id=1`, `hasta_id=4`'e işaret ediyor ama
`hasta` tablosunda 4 no'lu kayıt yok (muhtemelen daha önceki bir test
temizliğinde hasta silinirken bu satır atlanmış). Rota zaten `JOIN hasta`
kullandığı için bu kayıt `/sperm-dondurma/1` açılınca sessizce `/cryo`'ya
yönlendiriyor — uygulamadan hiç erişilemiyor, zararsız ama silinmemiş
ölü veri. Bu oturumda dokunulmadı (kapsam dışı); kullanıcı isterse
`sperm_dondurma`/`tasiyici` tablosundan elle temizlenebilir.

# v6.119 — Elle yedekleme düğmesi

Kullanıcının isteği: "Elle yedekleme olsun." Yedekleme o zamana kadar
yalnızca terminalden (`python3 yedek.py`) ya da Windows Görev
Zamanlayıcı'yla otomatik çalışıyordu (bkz. CLAUDE.md "bekleyen iş 2");
ekrandan tetiklenen bir yol yoktu.

## Ne değişti

- `/klasorler`'e (yönetici ekranı, klasör ayarlarının yapıldığı yer) yeni
  bir **"Yedekleme"** kartı eklendi: son yedeğin ne zaman alındığını
  (`gg_aa_yyyy_saat`), eskiyse `/yonetim`'in zaten gösterdiği uyarı
  metniyle aynısını (`yedek_durumu()`), ve bir **"Şimdi yedekle"**
  düğmesini gösteriyor.
- Düğme ayrı, tek amaçlı bir `<form action="/klasorler/yedekle-simdi">` —
  yukarıdaki klasör-kaydetme formunun içine gömülmedi. Bilerek: bu düğme
  ekrandaki (belki henüz kaydedilmemiş) yol kutusunu değil, veritabanında
  **zaten kayıtlı** `yedek_klasor` ayarını kullanıyor.
- Yeni rota `app.py` `klasorler_yedekle_simdi()`: `yedek.py`'nin
  `veritabani_yedekle()` / `eskileri_temizle()` / `arsiv_yedekle()`
  fonksiyonlarını **süreç içinde** (`import yedek`) çağırıyor —
  `goc.py`'nin göçleri çalıştırma deseninin aynısı.
  **`subprocess.run([sys.executable, ...])` yazılmadı**: paketlenmiş
  uygulamada `sys.executable` programın kendisi olur, o satır yedeği değil
  programı yeniden başlatırdı (CLAUDE.md'nin göçler için söylediği aynı
  tuzak, burada da geçerli).
  **`yedek.main()` de çağrılmadı** — o `sys.exit()` kullanıyor (CLI için
  doğru, bir istek işleyicisinin içinde `SystemExit` fırlatmak istenmeyen
  bir şey); `main()`'in çağırdığı fonksiyonlar burada elle, normal
  `try/except` ile çağrılıyor.
- Hata durumları: yedek klasörü hiç ayarlanmamışsa ya da bu makinenin
  işletim sistemine uygun bir yol değilse (`yedek.bu_makineye_uygun_mu()`,
  v6.8'in aynı kontrolü) açıklayıcı bir mesajla `/klasorler`'e dönülüyor.
  Diğer her hata (disk dolu, izin sorunu, doğrulama başarısız...) olduğu
  gibi (`Yedekleme başarısız: {e}`) gösteriliyor — `FormHatasi`
  mesajlarının kullandığı "sunucunun ürettiği bitmiş metni doğrudan
  göster" deseninin aynısı, `metin()`'e adresten gelen bir anahtar
  verilmiyor (tuzak #9 burada geçerli değil).
- Yeni metin anahtarları `metinler.py`'ye eklendi (iki dilde de):
  `yedekleme`, `son_yedek`, `hic_yedek_yok`, `simdi_yedekle`,
  `yedekleniyor_uyari`, `yedek_alindi`, `yedek_klasoru_yok_hata`,
  `yedek_klasoru_yanlis_makine`, `yedekleme_basarisiz`,
  `yedekleme_ipucu`.
- **`/yonetim`'e dokunulmadı** — o hâlâ salt okunur (v6.12), yalnızca son
  yedek durumunu gösteriyor. Düğme bilerek `/klasorler`'de: "ayarlar kendi
  ekranlarından yapılır" kuralının aynısı, klasör yolu ayarının zaten
  orada olması.

## Bilinen sınır

Düğme **eşzamanlı** (senkron) çalışıyor — istek, yedekleme bitene kadar
yanıt vermiyor, ilerleme çubuğu yok. Bugünkü test verisinde (birkaç MB)
saniyeler sürüyor; gerçek hasta arşivi büyüdükçe (`arsiv_yedekle()`
`rglob` ile bütün klasörü tarıyor) bu daha uzun sürebilir. Ekranda "sayfadan
ayrılma" uyarısı var ama gerçek bir ilerleme göstergesi yok. Otomatik
zamanlanmış yedeklemenin (Windows Görev Zamanlayıcı) yerini almıyor —
düğme günlük rutinin **tamamlayıcısı**, "hemen şimdi bir yedek almam
lazım" anları için (örn. büyük bir veri girişinden önce/sonra).

## Test edildi

Sunucu ayağa kaldırılıp `/klasorler` ekranı ve yeni rota gerçek yönetici
oturumuyla test edildi:
- **Başarılı yol**: mevcut `yedek_klasor` (`/root/lab_yedek`) ile düğmeye
  basıldı — `lab_YYYYMMDD_HHMM.db` dosyası oluştu, `PRAGMA
  integrity_check` geçti, `yedek.log`'a hem başlangıç/bitiş satırları
  (`kaynak: /klasorler, <kullanıcı adı>`) hem `veritabani_yedekle()`'nin
  kendi özet satırı yazıldı, `son_yedek` ayarı güncellendi ve ekranda
  "Yedekleme tamamlandı." + güncel tarih göründü, eski stale-yedek uyarısı
  kayboldu.
- **Yanlış makine yolu**: `db.yerel_yaz()` ile `yedek_klasor` geçici
  olarak `E:\yedek`'e çevrildi (Mac/Linux'ta geçersiz), düğmeye basıldı —
  yedek alınmadı, "'E:\yedek' bu işletim sisteminin yolu değil, yedek
  alınamadı." mesajı ekranda doğru (HTML-escape'lenmiş) göründü. Ayar
  gerçek değerine geri çevrildi.
- Playwright ile 390px mobil genişlikte ekran görüntüsü alınıp kartın
  düzeninin diğer kartlarla tutarlı olduğu doğrulandı.
- Test sırasında oluşan yedek `.db` dosyaları (`/root/lab_yedek/`) ve
  oturum jetonu temizlendi, sunucu kapatıldı. (`yedek.log`'daki test
  satırları `.gitignore`'da olduğu için depoya girmiyor, elle
  temizlenmedi.)

# v6.120 — Yedekten geri yükleme

Kullanıcının isteği: "Yedekten geri çağırma var mı? Yoksa olsun. Yönetici
isterse yedekten geri çağırsın programa hastalar tedaviler her şey tekrar
yerleşsin. Yönetici panelinden hepsini yapabilsin." v6.119'un tersi:
o yedek **alıyordu**, bu yedekten **geri yüklüyor** — tüm veritabanını
seçilen yedeğin içeriğiyle değiştiriyor.

## Sebep ve tasarım

Bu, uygulamadaki en yıkıcı işlem: bir hastayı kalıcı silmek tek bir kaydı
etkiliyor, geri yükleme **tüm** veritabanını (bütün hastalar, tedaviler,
oositler, işlem kayıtları) seçilen yedeğin alındığı andaki hâline
döndürüyor — aradan girilmiş her şey kayboluyor. Bu yüzden üç kat güvenlik
katmanı var, hasta kalıcı silmenin (dosya no + SIL) kuralından daha ağır:

1. **Seçilen yedeğin dosya adını yazmak** (hangi yedek olduğunu doğrulatıyor).
2. **"GERİ YÜKLE" yazmak** (ikinci, ayrı bir onay — iki dilde de aynı sabit
   metin, çünkü sunucu tarafındaki kontrol dilden bağımsız aynı stringi
   arıyor).
3. **Tarayıcının `confirm()`'ü.**

**Değiştirmeden önce mevcut veritabanının güvenlik kopyası otomatik
alınır** (`lab_ONCEKI_<tarih>.db`, `tasi.py`'nin USB'den içeri alırken
kullandığı aynı adlandırma ve aynı gerekçe) — yanlış yedek seçilirse o
kopyadan geri dönülebiliyor. Bu kopya `yedek_klasor`'e yazılıyor (bkz.
"Bilinen hata (düzeltildi)" aşağıda) — hem "başka bir diskte olmalı"
kuralından faydalansın hem geri yükleme ekranındaki listede kendisi de bir
seçenek olarak görünsün diye.

**Değiştirme mekaniği `tasi.py`'nin USB'den içeri alma deseninin aynısı**,
elle taklit edilmedi, doğrudan onun `tutarli_kopya()`/`ONCEKI`/atomik
takas üçlüsü kopyalandı (`geri_yukle.py` yeni bir dosya, `tasi.py`'yi
import etmedi — o script'in kendi CLI akışı `sys.exit()`/`input()`
kullanıyor, web rotasında istenmeyen şeyler, CLAUDE.md'nin "yedek.main()
çağrılmadı" bölümündeki gerekçenin aynısı):
1. Yedeğin kendisi bozuk mu diye `PRAGMA integrity_check` ile önce bak —
   bozuk bir dosyayı canlıya taşımadan yakala.
2. Mevcut canlı veritabanının güvenlik kopyasını SQLite backup API ile al.
3. Seçilen yedeği SQLite backup API ile bir **geçici dosyaya** kopyala
   (`lab.db.geri-yukleniyor`, `VERI_KOK`'ta — `Path.replace()`'in atomik
   kalması için hedefle **aynı dosya sisteminde** olmak zorunda, `yedek_
   klasor` başka bir diskte olabileceği için oraya yazılamaz).
4. Eski `-wal`/`-shm` yardımcı dosyalarını sil (kalırsa yeni dosyanın
   içeriğiyle uyuşmayan sayfalar yeniden oynatılmaya çalışılır — `tasi.py`
   README v6.16'nın aynı önlemi).
5. `Path.replace()` ile **atomik** takas — ya tam olur ya hiç olmaz, yarım
   kalan bir kopya asla canlı veritabanının yerine geçmez.

**Neden düz dosya kopyası değil ("`shutil.copy2`") burada da geçerli**
(README v6.16'nın gerekçesi): WAL modunda düz kopya yarım/tutarsız çıkar.
**Neden canlı `db.DB_YOLU`'na doğrudan `kaynak.backup(hedef)` değil de
geçici-dosya+atomik-takas**: `db.baglan()` her istekte kendi bağlantısını
açıp kapatıyor (kalıcı bir havuz yok), yani teoride doğrudan backup API ile
canlıya yazmak da güvenli olurdu — ama `tasi.py` zaten bu deseni (geçici
dosya + atomik takas) seçmiş ve Windows'ta dosya "kullanımda" hatasını
`OSError` olarak yakalayıp temiz bir mesajla durabiliyor (canlı veritabanına
hiç dokunulmadan). Aynı olgun deseni tekrar icat etmek yerine kopyalandı.

## Ne değişti

- Yeni dosya **`geri_yukle.py`**: `yedekleri_listele()` (yedek klasöründeki
  `lab_*.db` dosyalarını tarih/boyutla listeler, `lab_ONCEKI_*.db` güvenlik
  kopyalarını da `onceki_mi` bayrağıyla dahil eder) ve `geri_yukle()`
  (yukarıdaki beş adım). Terminalden de çalışır (`python3 geri_yukle.py
  listele` / `geri-yukle <dosya>`) — `kullanici.py`'nin "yönetici de
  kilitlenirse" felsefesinin aynısı, web ekranı çalışmasa bile bir çıkış
  yolu olsun diye.
- `app.py`: `GET/POST /klasorler/geri-yukle` — ikisi de `yonetici_kontrol()`
  ile başlıyor (rota adı `-sil` ile bitmediği için `yol_modulu()` bunu
  "silme" modülüne bağlamıyor, kasıtlı: bu iş "silme" izninden bağımsız,
  doğrudan yönetici işi). `/klasorler`'e `gymesaj` parametresi eklendi
  (başarı mesajı, `yhata` gibi sunucunun ürettiği bitmiş metin — `metin()`'e
  adresten gelen bir anahtar verilmiyor, tuzak #9 burada geçerli değil).
- `templates/geri_yukle.html`: yedek listesi (radyo seçim,
  `.secsatir`/hasta_sil.html'in aynı deseni), iki yazılı onay alanı, kırmızı
  "Yedekten geri yükle" düğmesi, tarayıcı `confirm()`.
- `/klasorler`'in "Yedekleme" kartına kırmızı bir "Yedekten geri yükle"
  bağlantısı eklendi (`.tehlike-bag`, hasta silmedeki "kalıcı sil"
  düğmesiyle aynı görsel dil).
- **Güvenlik: `dosya` form alanı whitelist'ten geçiyor.** Adresten/formdan
  gelen bir dosya adını doğrudan `Path(hedef) / dosya`'ya eklemek yol
  aşımına (`../../lab.db` gibi) açık olurdu (tuzak #9'un dosya-yolu hali).
  `klasorler_geri_yukle()` önce `yedekleri_listele()`'nin döndürdüğü
  **gerçek** dosya adlarının kümesini kuruyor, `dosya` o kümede değilse
  reddediyor — yol aşımı denemesi normal bir "yedek seçilmedi" hatasına
  düşüyor, hiçbir zaman `yedek_klasor`'ün dışına çıkamıyor.

## Bilinen hata (düzeltildi, geliştirme sırasında yakalandı)

İlk yazımda güvenlik kopyası (`lab_ONCEKI_*.db`) `tasi.py`'yi birebir
kopyalayarak `VERI_KOK`'a (canlı veritabanıyla aynı klasöre) yazılıyordu.
Test sırasında fark edildi: `yedekleri_listele()` yalnızca `yedek_klasor`'ü
tarıyor, yani bu kopya hiçbir zaman geri yükleme listesinde görünmeyecekti
— kullanıcı "önceki hâle dön" seçeneğini asla göremezdi. Ayrıca `yedek_
klasor`'ün "başka bir diskte olmalı" kuralından (v6.41) hiç faydalanmıyordu.
Düzeltme: güvenlik kopyası artık `yedek_dosyasi.parent`'a (seçilen yedeğin
bulunduğu, yani `yedek_klasor`'ün ta kendisi) yazılıyor — `tasi.py`'nin
kendi ONCEKI'si hâlâ `VERI_KOK`'ta kalıyor, çünkü onun bağlamı farklı ("bu
makinede hemen geri alınacak bir USB taşıma hatası", ayrı diske ihtiyaç
yok). Yeni bir "önceki hâli sakla" ihtiyacı doğarsa sor: bu kopya nereden
tekrar seçilecek/bulunacak, oraya mı yoksa `VERI_KOK`'a mı ait?

## Bilinen sınır

**Arşivdeki fotoğraflar geri yüklenmiyor.** `yedek.arsiv_yedekle()`
hedeften hiçbir şey silmiyor, yalnızca birikimli kopyalıyor — yani "şu
yedeğin arşiv anlık görüntüsü" diye bir kavram yok, hangi fotoğrafın hangi
DB anına ait olduğunu ayıklamanın bir yolu yok. Bu bilinçli bir sınır:
fotoğraf dosyaları kendi başına asla silinmiyor/üzerine yazılmıyor olduğu
için risk yalnızca "eski DB, aradan silinmiş bir fotoğrafa işaret ediyor"
(kırık bağlantı), veri kaybı değil. Ekrandaki uyarı metni bunu açıkça
söylüyor.

**Geri yükleme sonrası oturumlar geçersiz olabilir.** Eski bir yedeğe
dönüldüğünde, o yedekten SONRA açılmış oturum jetonları (`oturum` tablosu)
artık veritabanında yok — geri yükleyen yönetici dahil herkes bir sonraki
istekte `/giris`'e düşebilir. Bu beklenen, doğru davranış (kimlik doğrulama
verisi de veritabanının parçası), ayrıca bir işlem gerektirmiyor.

## Test edildi

**Gerçek proje veritabanına hiç dokunulmadı** — `LAB_VERI` ortam
değişkeniyle tamamen izole bir kopya üzerinde, ayrı bir portta (8124) ikinci
bir sunucu örneği çalıştırıldı:
- İzole veritabanının SQLite backup API ile bir kopyası alındı, üzerine
  iki test hastası eklenerek iki farklı "yedek" üretildi (1 hastalı temel
  durum, sonra 2 hastalı "canlı" durum).
- **Mutlu yol**: temel duruma geri yüklendi — canlı veritabanı 1 hastaya
  döndü, `PRAGMA integrity_check` "ok" verdi, güvenlik kopyası doğru
  klasörde (`yedek_klasor`) oluştu ve sonraki listede kendisi de seçenek
  olarak göründü, sunucu çökmeden yanıt vermeye devam etti.
- **Doğrulama hataları**: yanlış dosya adı yazma, yanlış onay metni yazma
  — ikisi de doğru hata mesajıyla reddedildi, canlı veritabanı
  değişmedi.
- **Bozuk yedek**: gerçek bir SQLite dosyası olmayan bir dosya "yedek" diye
  seçilip gönderildi — `PRAGMA integrity_check` başarısız olmadan önce
  SQLite'ın kendi hatasıyla reddedildi, canlı veritabanı ve yedek klasörü
  hiç değişmedi (yeni bir ONCEKI kopyası bile oluşmadı — doğrulama
  güvenlik kopyasından ÖNCE yapılıyor).
- **Yol aşımı denemesi**: `dosya=../../../etc/passwd` gönderildi, whitelist
  kontrolü tarafından "yedek seçilmedi" hatasıyla reddedildi.
- Playwright ile 390px mobil genişlikte onay ekranının görüntüsü alındı:
  uyarı kutusu, yedek listesi (tarih/boyut/"önceki hâl" rozeti), iki onay
  alanı ve kırmızı düğme doğru görünüyordu.
- İzole test klasörü (`LAB_VERI` ile işaret edilen geçici dizin) ve test
  sunucusu tamamen silindi/durduruldu; gerçek proje `lab.db`'sinde hasta/
  cycle sayıları test öncesiyle birebir aynı kaldığı doğrulandı.

# v6.121 — Yedekleme kendi ekranına taşındı

Kullanıcının bildirdiği sorun: "Yedekleme bölümünde Yedekleme olsun.
Klasörlerin altında zor bulunuyor." v6.119/v6.120'de yedekleme/geri
yükleme `/klasorler`'in bir kartıydı — yedek klasörünün **yolu** zaten o
ekranda ayarlandığı için mantıklı görünmüştü, ama kullanıcı ekranı ararken
bulamadı: "Klasörler" bir eylem menüsü gibi görünmüyor.

## Ne değişti

- Yeni ekran **`/yedekleme`** (`templates/yedekleme.html`) — son yedek
  durumu, "Şimdi yedekle" düğmesi ve "Yedekten geri yükle" bağlantısı
  artık kendi sayfasında, `/klasorler`'in dışında.
- Rotalar taşındı: `/klasorler/yedekle-simdi` → `/yedekleme/yedekle-simdi`,
  `/klasorler/geri-yukle` → `/yedekleme/geri-yukle` (GET+POST). Mantık
  (üç kademeli onay, güvenlik kopyası, atomik takas, whitelist) hiç
  değişmedi — yalnızca adresler.
- **`/yonetim`'e doğrudan "Yedekleme" düğmesi eklendi** — Kullanıcılar,
  Şifre istekleri, İstatistikler, Cryo haritası, Dil seçimi, Laboratuvar
  formları, Klasörler, Telefona ekle ile **aynı seviyede**, bir üst
  ekranın içine gömülü değil. Kullanıcının şikâyeti tam buydu: eylem bir
  alt-kart değil, kendi menü öğesi olmalıydı.
- `/yonetim`'in eski "Yedekleme" durum kartı (salt okunur, v6.12 kuralı
  hâlâ geçerli) güncellendi: tarih artık `gg_aa_yyyy_saat()` ile
  basılıyor (önceden ham ISO metniydi), ve **"terminalden python3
  yedek.py çalıştır" tavsiyesi kaldırıldı** — o artık yanlış/eksik bir
  tavsiye, ekrandan da yapılabiliyor. Yerine `/yedekleme`'ye bağlantı
  kondu.
- `/klasorler`'de yedek klasörünün **yolu** hâlâ ayarlanıyor (o bir klasör
  ayarı, taşınmadı) — kaydetme formunun altında artık yalnızca `/yedekleme`
  ekranına giden tek bir bağlantı var, eski büyük kart kaldırıldı. İki
  ekran birbirine çapraz bağlı: Klasörler → Yedekleme (eylemler için),
  Yedekleme → Klasörler (yolu değiştirmek için).

## Sebep

Kullanıcının kâğıt/menü sezgisi: bir eylem ("şimdi yedekle", "geri yükle")
bir ayar ekranının (klasör yolları) alt kartı değil, kendi başına bir menü
öğesi olmalı. `/yonetim` zaten "gidilecek ekranlar" listesi tutuyor
(Kullanıcılar, İstatistikler, Cryo haritası, ...) — Yedekleme'nin oraya
katılması, aranan yerde bulunması demek.

## Test edildi

Gerçek proje veritabanına dokunulmadan, `LAB_VERI` ile izole bir kopya
üzerinde ayrı bir sunucu örneğinde (port 8125):
- `GET /yedekleme`, `GET /klasorler`, `GET /yonetim` üçü de 200 döndü.
- Eski adres `POST /klasorler/yedekle-simdi` artık 404 (rota gerçekten
  taşınmış, eski yere düşen bir çağrı sessizce eski davranışa dönmüyor).
- `/yonetim` ve `/klasorler` sayfalarında `/yedekleme`'ye giden bağlantılar
  doğru adreste bulundu.
- **Uçtan uca**: `POST /yedekleme/yedekle-simdi` gerçek bir yedek dosyası
  oluşturdu; `GET /yedekleme/geri-yukle` o dosyayı listede gösterdi;
  `POST /yedekleme/geri-yukle` (üç onay alanıyla) veritabanını gerçekten
  geri yükledi ve `/yedekleme?gymesaj=...`'a yönlendirdi.
- Playwright ile `/yonetim` ve `/yedekleme` ekran görüntüleri alındı:
  Yedekleme düğmesi diğer yönetim düğmeleriyle aynı sırada/görünümde,
  yeni ekran üç ayrı kart halinde (durum, yedekle, geri yükle) düzgün
  render ediyor.
- İzole test klasörü ve sunucu temizlendi; gerçek proje `lab.db`'sinde
  hasta/cycle sayıları test öncesiyle birebir aynı kaldı.

# v6.122 — Cleavage skoru: elle giriş artık G1-G4 seçimi

Kullanıcının isteği: "Cleavage bölümünde skor kısmı elle girilebilsin.
G1,G2,G3,G4 şeklinde seçilebilsin." Elle skor girme zaten vardı
(`cl_skor`/`cl_skor_kaynagi`, "Otomatik skorlar kaynak işaretler" kuralı)
ama serbest bir metin kutusuydu — kullanıcı kapalı bir seçim istedi.

## Ne değişti

- Yeni `liste_degeri` listesi **`cleavage_skor`** (`goc_041.py`, dört
  satır: G1, G2, G3, G4) — `simetri`'nin izlediği aynı kalıp.
  `sifirdan_kur.py`'nin `LISTELER`'ine de eklendi, sıfırdan kurulan bir
  laboratuvarda göç beklemeden hazır gelsin diye.
- Cleavage ekranındaki serbest metin `<input id="cl_skor">` kaldırıldı,
  yerine `cl_simetri`'nin hemen üstündeki aynı `.secenek`/`.sec` radyo
  grubu geldi (`templates/cleavage.html`). Salt okunur özet kartındaki
  skor satırı da `liste_etiket('cleavage_skor', kayit.cl_skor)` ile
  basılıyor — ham kod değil etiket.
- `app.py` `cleavage_ekran()` context'ine `"skorlar": db.liste("cleavage_skor")`
  eklendi.
- **Otomatik A/B/C hesabına dokunulmadı** — `cleavage_skor()` fonksiyonu
  hâlâ aynı şekilde çalışıyor, kullanıcının isteği yalnızca elle girişin
  şeklini kapsıyordu ("bekleyen iş 5"in kendisi açık kaldı, kullanıcı ona
  ayrıca sorulmadan cevap vermedi).
- `cleavage_kaydet()` (POST) değişmedi — `(f.get("cl_skor") or "").strip().upper()`
  satırı zaten vardı, G1-G4 kodları büyük harfle seçildiği için hâlâ
  aynen çalışıyor.

## Sebep

`liste_degeri` kodları bilerek **büyük harf** ("G1", lowercase "g1"
değil) seçildi: `cleavage_kaydet()`'in mevcut `.upper()` satırı elle
girilen değeri her zaman büyütüyordu (eski serbest metin girişinde de
öyleydi, değiştirilmedi). Kod lowercase olsaydı kaydedilen değer
büyütülüp "G1" olurdu ama `liste_degeri`'ndeki gerçek kod "g1" kalırdı —
bugün `liste_etiket()`'in bulunamayan kodu olduğu gibi döndürme
davranışı bunu gizler (ekranda yine "G1" görünür, kodun kendisi düşer)
ama laboratuvar etiketi sonradan değiştirirse (örn. "Grade 1
(mükemmel)") o değişiklik bu örnek için sessizce hiç uygulanmazdı. Kod ve
etiketi eşit tutmak bu riski en baştan kapattı.

## Test edildi

Gerçek proje `lab.db`'sine karşı (yalnızca `liste_degeri`'ne satır ekleyen,
yıkıcı olmayan bir göç ve normal bir klinik kayıt olduğu için izole kopya
gerekmedi):
- `python3 goc_041.py` iki kez çalıştırıldı — ilkinde 4 satır eklendi,
  ikincisinde "cleavage_skor listesi zaten guncel." ile idempotent çıktı.
- `GET /cycle/1/cleavage?gun=2`: G1-G4 radyo düğmeleri doğru etiketlerle
  render edildi.
- `POST /cycle/1/cleavage` (`cl_skor=G2` ile) gerçek bir specimen için
  kaydedildi; veritabanında `olay.cl_skor='G2'`, `cl_skor_kaynagi='elle'`
  doğrulandı.
- Kayıt sonrası salt okunur özet kartı "G2" gösterdi; `?duzenle=1` ile
  form moduna dönüldüğünde G2 radyosu `checked`, etiketi `secili`
  sınıflı, ve ipucu metni "Şu anki kayıt: **G2** (elle girildi)."
  doğru basıldı.
- Test kaydı (`olay` satırı) ve test oturum jetonu temizlendi; gerçek
  veritabanında başka hiçbir şey değişmedi.

# v6.123 — istatistiklerde aylık oranlar ve yıl/ay seçici

Kullanıcının isteği: "Yönetici bölümünde istatistik alanında aylık olarak
oranlar tutulsun. M2 oranı, PN oranı, Blastokist oranı, Klinik gebelik
oranı (transfer başına) bunlar aylık olarak tutulsun ve yıl ve tarih
seçerek bakabileyim."

**"Tutulsun" yine bir sayaç açmak değil.** v6.38'in kararı burada da
geçerli: sayılar her açılışta `hasta`/`cycle`/`specimen`/`olay`'dan
türetiliyor. İstenen dört oranın **tanımı zaten vardı** ve tam bu adlarla
(`oran_mii`, `oran_fert`, `oran_blast`, `oran_gebelik`); `istatistikler()`
zaten `ay="2026-09"` alıp süzebiliyordu. Eksik olan yalnızca ekrandaki
karşılığıydı — ay seçilemiyordu ve ay kırılımı tablosu dört orandan
yalnızca birini (fertilizasyon) basıyordu.

## Ne değişti

- **Ay/yıl seçici** (`/istatistik?yil=&ay=`) — `/hastalar`'ın ay gezgininin
  birebir aynısı (`.aygezgin`, `‹ ›` okları, iki açılır seçici, JS kapalıysa
  kalan "Göster" düğmesi). Aynı işi yapan iki ekran aynı görünsün diye
  yeniden yazılmadı, kopyalandı; tek fark bu ekranda arama olmadığı için
  gizli `ara` alanının olmaması.
- **Oranlar kartı artık iki değer sütunu taşıyor**: seçilen ay ve
  laboratuvarın tamamı. Ayın sütununda yüzdenin yanında **payı ve
  paydası** da yazıyor (`20 / 32`).
- **"Aylara göre" tablosu seçilen yılın ayları** (eskiden "son 12 ay") ve
  dört oranı birden basıyor. Ayın adı bağlantı: üstteki kartı o aya
  çeviriyor. Seçili ayın satırı `--vurgu-ac` zeminle işaretli.
- **Excel çıktısı** (`/disari/istatistik?yil=`) ekrandaki yılı taşıyor;
  "Aylara göre" sayfası artık sayıların yanında dört oranı da veriyor
  (13 sütun), sayfa adı `2026 aylara göre`.
- `oran_mii`'nin ekran etiketi **"MII oranı" → "M2 oranı (MII / kayıtlı
  oosit)"**. Kullanıcı bu orana "M2" diyor ve tedavi ekranının özet kutusu
  (`ozet_m2`, v6.112) zaten "M2" yazıyordu; aynı ekranda sütun başlığı "M2"
  iken satırın "MII oranı" demesi tutarsız olurdu. Paydası da yazıldı —
  öteki üç etiketin zaten izlediği desen.

## Neden ay kırılımı oranları kendi başına hesaplamıyor

`istatistik_aylari()` her ay için `istatistikler(ay)` çağırıyor ve oranı
ondan alıyor. Kendi `pay/payda` formülünü yazsaydı ekranın üstündeki kart
ile altındaki tablo iki ayrı formülle aynı sayıyı hesaplardı; biri
düzeltilip öteki unutulurdu. Sayaç tutmama gerekçesinin (v6.38) formül
hali. Bedeli on iki ekstra sorgu kümesi — SQLite yerelde, ekran zaten
yalnızca yöneticinin ara sıra açtığı bir ekran.

## Neden "genel toplam" ve "son kayıtlar" seçiciden etkilenmiyor

İkisi de bilerek laboratuvarın tamamı. "Genel toplam" zaten adıyla bunu
söylüyor ve `istatistikler(ay)` ay verildiğinde hasta sayılarını `None`
döndürüyor (hasta kaydı bir aya ait değil). "Son kayıtlar" ise "en son ne
yapıldı" penceresi (v6.38) — geçmiş bir aya bakarken o ayın son on kaydını
göstermek onu başka bir şeye çevirirdi.

## Neden boş ay "%0" değil "—" yazıyor

"Paydası sıfır olan oran basılmaz" kuralı (v6.38) ay kırılımında daha da
önemli: bir laboratuvarın işlem yapmadığı ayda "%0 blastokist" yazmak
"ölçüldü ve sıfır çıktı" demek olurdu. `_oran()` paydası sıfırken `None`
döndürüyor, ekran `—` basıyor. Kaydı hiç olmayan ay tabloya **girmiyor** —
on iki satır tire tabloyu uzatmaktan başka bir şey yapmazdı; o ayın seçili
olması durumunda kartın altında "Bu ayda kayıt yok." notu çıkıyor.

## Adresten gelen yıl/ay: `_istatistik_donemi()`

`?yil=`/`?ay=` dışarıdan geliyor ve üç şey birden yapılıyor (tuzak #9'un
sorgu hali):

- **Değer iki tamsayıdan kuruluyor.** `ay_str` `disari.istatistikler()`
  içinde SQL metnine giriyor; orada tırnak da ayıklanıyor ama asıl güvence
  adresten gelen metnin sorguya hiç ulaşmaması.
- **Yıl `EN_ESKI_YIL` .. bu yıl + `EN_YENI_YIL_PAYI` arasına sıkıştırılıyor.**
  `_yil_araligi()` seçili yılı listeye zorla ekliyor; `?yil=99999` gelseydi
  seçicide doksan bin satır olurdu. Tarih doğrulamasının kendi sınırları
  kullanıldı — iki ayrı "makul yıl" tanımı olmasın diye.
- **Boş gelirse bugüne düşüyor**, `/hastalar`'daki gibi.

## Tablo genişliği: ölçü "sığıyor" dese de ekran görüntüsü yalan söylemez

İlk yazışta oran tablosu dört sütunla `.sutun`un genişliğini (masaüstünde
~444px) aşıyordu. `.cizelgekap`'ın `overflow-x`i (v6.113) teknik olarak
kaydırılabilir yapıyordu ve Playwright ölçümü de "sayfa yatay taşmıyor"
diyordu — **ama ekran görüntüsünde "Tüm zamanlar" sütununun başlığı "Tüm
zam" diye kesilmişti ve hücrelerin yalnızca "%" işareti görünüyordu.**
Kimse iki değeri karşılaştırmak için tabloyu yatay kaydırmaz; görünmeyen
değer yok demektir. v6.109'un dersinin bir kere daha doğrulanması: dış
kabın geometrisi doğru çıkabilir, içerideki asıl içeriğin nerede
göründüğüne ayrıca bakmak gerekiyor.

Düzeltme `nowrap`'i kaldırmak değil, **kapsamını daraltmak**:
`.cizelge`nin `white-space: nowrap`'i sayılar için ("%77.8", "12 / 20"
ortasından bölünmesin); etiket sütununun sarmasında bir sakınca yok.
`.cizelge.oran td.ad { white-space: normal; }` — yalnızca bu tabloya, yeni
bir `oran` sınıfıyla. Aylık tablo da yeni bir `aylik` sınıfıyla yatay
dolgusunu 14px'ten 8px'e çekiyor (altı sütunda 72px kazanç).
`cycle_detay.html`'in zaman çizelgesi ve `form_etiketleri.html`
sınıfsız `.cizelge` olarak kaldı, ikisi de etkilenmedi.

## Test edildi

Ayrı bir test veritabanında (2025 Kasım + 2026 Haziran/Temmuz/Eylül'e
yayılmış 11 tedavi, 103 oosit, 264 olay; oranlar aydan aya bilerek farklı):

- Dört oran elle yapılan hesabın aynısı çıktı — örn. 2026-09: M2 20/32
  = %62,5, PN 12/20 = %60, blastokist 4/12 = %33,3, klinik gebelik 1/3
  = %33,3.
- Kaydı olmayan ay (`?yil=2026&ay=1`) "Bu ayda kayıt yok.", kaydı olmayan
  yıl (`?yil=2024`) ayrıca "Bu yılda kayıt yok." bastı; oranlar `—` çıktı,
  "%0" değil.
- `?yil=99999` 2031'e sıkıştırıldı, yıl seçicide yedi satır kaldı.
- Oklar yıl sınırını çeviriyor: Ocak 2026'da `‹` → Aralık 2025, Aralık
  2026'da `›` → Ocak 2027.
- Yönetici olmayan kullanıcı hem `/istatistik` hem `/disari/istatistik`
  için `/hastalar`'a döndürüldü; aynı kullanıcı `/hastalar`'ı açabildi.
- Excel: iki sayfa (`2026 aylara göre` + `Genel`), 13 sütun, sayılar ve
  oranlar ekrandakiyle birebir aynı.
- Playwright ile dört ekran boyutunda (1440x1000, 1100x900, 390x844,
  360x740): sayfa hiçbirinde yatay kaymıyor; 390px'e kadar iki tablo da
  kaba **tam sığıyor** (kaydırma yok), yalnızca 360px'lik dar telefonda
  `.cizelgekap` içinde 13/22px kaydırma kalıyor — bu ekran için kabul
  edilmiş çözüm (v6.113).
- `cycle_detay.html`'in zaman çizelgesi masaüstünde ve telefonda
  değişmedi (`transform: none`, sayfa taşması yok).
- 21 ekran (ana, hasta kayıtları, yönetim, cryo, formlar, bitenler,
  devam eden, yaklaşanlar, kullanıcılar, klasörler, yedekleme, dil,
  tedavi ve aşama ekranları, hasta kartı, bağlan) 200 döndü; sunucu
  günlüğünde hata yok.

# v6.124 — "Son kayıtlar" haftalık ve sayfalı

Kullanıcının isteği: "İstatistikteki son kayıtları sayfada çok gösterme,
haftalık tut. Onları da ekranda beş sayfada göster ki çok uzun liste
olmasın."

İki ayrı sınır isteniyor ve ikisi de gerekiyor: **pencere** (ne kadar
geriye bakılacak) ve **liste boyu** (bir seferde kaç satır görünecek). Kart
eskiden sabit on satır gösteriyordu ve pencere yoktu — laboratuvarın en
son on kaydı, ne kadar eski olurlarsa olsunlar.

## Ne değişti

- **Pencere `SON_KAYIT_GUN` = 7 gün.** Kart artık "en son ne yapıldı"
  değil, "bu hafta ne yapıldı" penceresi.
- **Liste sayfalı**: `SON_KAYIT_SAYFA_BOYU` = 5, `SON_KAYIT_EN_COK_SAYFA`
  = 5 → en çok 25 kayıt, beşerli beş sayfa. Gezgin `/hastalar`'ın sayfa
  gezgininin aynısı (`.aygezgin` + `.sayfabilgi`, "Sayfa 2 / 5").
- `son_kayitlar()` artık liste değil **sözlük** döndürüyor: `satirlar`,
  `sayfa`, `sayfa_toplam`, `toplam`, `gun`, `sinirli`.
- Kartın başlığının altında pencere yazıyor: "Son 7 gün", tavana
  değiliyorsa yanında "· en yeni 25 kayıt".
- Kayıt yoksa mesaj artık genel "Henüz kayıt yok." değil,
  **"Son 7 günde kayıt yok."** (`son_kayit_bos`) — eskisi boş bir
  laboratuvar sanılmasına yol açardı; asıl sebep pencerenin boş olması.

## Sayfa boyu neden 5

Kullanıcının "beş sayfa" demesi bir yana, **ana ekranın üç kartı zaten
`liste[:5]` ile kesiliyor** (v6.78, yine kullanıcının isteği). Aynı
programda "kısa liste" ölçüsü iki farklı sayı olmasın diye o boy
tekrarlandı. Beş satır × beş sayfa aynı zamanda kullanıcının cümlesindeki
iki sınırı da karşılıyor: sayfada çok satır yok, toplam beş sayfa.

## Tavanı aşan kayıt gizlenmiyor, sayısı yazılıyor

Bir haftada 25'ten fazla kayıt olması olağan (bir tedavi tek başına
onlarca `olay` satırı üretiyor — test verisinde bir hafta 40 kayıttı).
Kart o durumda en yeni 25'i gösterip **"en yeni 25 kayıt"** yazıyor.
Sessizce kesseydi ekran "bu hafta 25 iş yapılmış" der gibi görünürdü;
bu kart bir kayıt defteri değil, tam döküm hâlâ `/disari/tumu`'da.

## Ay seçicisinden bağımsız, ama adres ikisini birlikte taşıyor

Kart **seçilen aya değil bugüne** bakıyor — "bu hafta ne yapıldı"
sorusunun geçmiş bir ayla ilgisi yok (v6.123'te "Son kayıtlar seçiciden
etkilenmez" diye yazılmıştı, o karar değişmedi). Ama ikisi aynı adreste
durduğu için sayfa bağlantıları `yil`/`ay`'ı **taşımak zorunda**: yoksa
son kayıtlarda sayfa çevirmek seçili ayı bugüne sıfırlardı.
`/hastalar`'ın `?sayfa=` / `?aysayfa=` ikilisinde çözülen sorunun
aynısı, çözümü de aynı.

## Haftalık süzgeç `localtime` KULLANMIYOR — bilerek

`olusturma_zamani` hiçbir yerde elle yazılmıyor; hasta, cycle ve olay
tablolarında şemanın `DEFAULT (datetime('now'))` değerine düşüyor ve
SQLite'ın `datetime('now')`'ı **UTC**. Süzgeç de bu yüzden
`datetime('now', '-7 days')` — iki tarafın aynı saate göre olması
gerekiyor.

Bu, klinik tarih alanlarındaki desenle karıştırılmamalı: "Bugün bitenler"
(v6.29) `date(bitis_zamani) = date('now','localtime')` kullanıyor, çünkü
`bitis_zamani` **personelin elle girdiği yerel bir zaman**. Biri
veritabanının kendi damgası, öteki kullanıcının saati; aynı ifadeyi
ikisine birden uygulamak ikisinden birini kaydırır.

## Havuz neden tablo başına 25 çekiyor

Üç tablodan ayrı ayrı okunup zamana göre birleşiyor (mekanizma
değişmedi). Birleşik listenin ilk 25'i, her tablonun **kendi** ilk
25'inin içindedir — o yüzden tablo başına `LIMIT 25` yetiyor, ayrı bir
`COUNT(*)` sorgusu gerekmiyor. Sayfa numarası da sunucuda kendi
`[1, sayfa_toplam]` aralığına sabitleniyor: aralık dışı bir değer hataya
değil son sayfaya düşer (`/hastalar`'daki kuralın aynısı).

## Test edildi

Son 7 güne yayılmış 40 kayıtlık (2 hasta + 2 tedavi + 36 olay) bir test
kümesiyle:

- Havuz 25'te duruyor, `sinirli` bayrağı doğru, kart "Son 7 gün · en yeni
  25 kayıt" bastı.
- Sayfa 1/3/5 beşer satır verdi; `?kayitsayfa=99`, `0` ve `-4` son/ilk
  sayfaya düştü, hata vermedi.
- Pencere daraltılınca sayfa sayısı küçüldü (2 gün → 20 kayıt / 4 sayfa),
  sıfırlanınca "Son 7 günde kayıt yok." çıktı.
- 3 Eylül'deki eski test verisi pencereye **girmedi** — süzgeç çalışıyor.
- `?yil=2026&ay=7&kayitsayfa=2`: sayfa bağlantıları yılı ve ayı taşıdı,
  ay seçici Temmuz'da kaldı; Playwright ile "Sonraki sayfa"ya tıklandı,
  adres `?yil=2026&ay=9&kayitsayfa=2` oldu ve seçici Eylül'de kaldı.
- 1440x1000 ve 390x844'te sayfa yatay kaymıyor; kartın boyu kısaldığı
  için masaüstünde sayfa yüksekliği 1550 → 1201px'e indi.
- 19 ekran 200 döndü, sunucu günlüğünde hata yok.

# v6.125 — dosya numarasından sperm dondurma eşleşmesi ve uyarı

Kullanıcının isteği: "Sperm dondurma alanında dondurma işlemi yapılan erkek
hastanın dosya numarası giriliyor. Eğer bu hastanın eşi ile birlikte tüp
bebek için hasta kaydı varsa uyarı mesajı ver. Aynı şekilde hasta kartında
dondurulmuş sperm işlemi varsa dosya numarasından eşle. Elle eşleme var.
Bir de dosya numarası üzerinden bu şekilde uyarı ver."

## Eşleştirme neden dosya numarasıyla yapılabiliyor

Şemada **`UNIQUE (lab_id, dosya_no)`** var. Yani lab içinde bir dosya
numarası bir `hasta` satırına aittir ve **"aynı dosya no" ile "aynı hasta
kaydı" aynı şeydir**. Tüp bebek çifti tek bir `hasta` satırı olarak
tutuluyor (`ad_soyad` kadın, `es_adi` erkek); o çiftteki erkeğin sperm
dondurması aynı satıra `sperm_dondurma.hasta_id` ile bağlanıyor. Dolayısıyla
"dosya numarasından eşle" ayrı bir eşleştirme tablosu ya da arama değil,
**var olan yabancı anahtarın okunması**.

**İsimle eşleştirme bilerek yazılmadı.** `hasta.ad_soyad` (kadın) ile
`hasta.es_adi` (erkek) karşılaştırıp "bu adam şu çiftin kocası" demek
teknik olarak mümkün, ama ad benzerliği kesin değil ve "yanlış hasta bu
işin en pahalı hatası" (CLAUDE.md). Dosya numarası kesin; kullanıcının
kendisi de iki kez "dosya numarası üzerinden" dedi.

## Üç yer

**1. Sperm Dondurma > yeni hasta formu — dosya no girilirken uyarı.**
Canlı kontrol zaten vardı (`/hasta/kontrol`, yazarken soruyor) ama yalnızca
"kayıtlı, adı şu" diyordu. Artık **tedavi sayısını, dondurulmuş sperm
sayısını ve eşin adını** da söylüyor:

> Bu dosya no zaten kayıtlı: **AYŞE YILMAZ** · 1 tüp bebek tedavisi var ·
> 1 dondurulmuş sperm kaydı var · eşi: MEHMET YILMAZ — kaydı aç

**`/hasta/kontrol` genişletildi, ikinci bir uç nokta yazılmadı.** İlk
yazışta `/sperm-dondurma/dosya-kontrol` diye ayrı bir rota açılmıştı;
`hasta_form.html`'in aynı işi yapan betiği görülünce geri alındı — iki
kopya olsaydı biri güncellenip öteki unutulurdu (`izgara_kur()`,
`gun_alt()` gibi yerlerdeki aynı kural). `/hasta/yeni` ekranı değişmeden
çalışmaya devam ediyor: eklenen alanlar eski cevabın üstüne, onun
kullanmadığı anahtarlar olarak geliyor.

**Sunucu tarafındaki engel de zenginleşti.** POST'ta mükerrer dosya no
eskiden düz bir metinle reddediliyordu; artık aynı bilgiyi taşıyan ve
**o hastaya götüren bağlantısı olan** bir kutu basılıyor. Engelin kendisi
değişmedi (`UNIQUE` zaten izin vermezdi) — değişen, çıkmaz sokak yerine
yolu göstermesi: çift zaten kayıtlıysa doğru davranış yeni bir hasta
açmak değil, o kayda sperm dondurma eklemek.

**2. Hasta kartı — dondurulmuş sperm kayıtları listeleniyor.**
`/hasta/{id}` şimdiye kadar yalnızca "Yeni Sperm Dondurma" düğmesini
gösteriyordu; **var olanları göstermiyordu**. Yani bir tüp bebek çiftinin
kartına bakan embriyolog, o çiftin dondurulmuş spermi olduğunu göremiyordu.
Artık taşıyıcı etiketi, tarih, konum, sebep ve "Kullanıldığı tedavi" (ya da
"Henüz bir tedaviye bağlanmadı") ile listeleniyor.

Kaydı olmayan hastada kart **hiç basılmıyor** — boş bir "yok" kutusu her
tüp bebek hastasının kartını boşuna uzatırdı. İzni düğmeyle aynı (`cryo`).

**3. Androloji — dosya numarasından otomatik haber.**
Elle eşleme ekranı (`/cycle/{id}/androloji/sperm-baglama`, v6.86) duruyor ve
**bütün laboratuvarı** arıyor; öyle olmak zorunda, çünkü kayıt bilerek
başka bir hastaya ait olabiliyor. Buraya eklenen, aramayı beklemeden
söylenen şey: bu tedavinin dosya numarasına ait, henüz hiçbir tedaviye
bağlanmamış sperm varsa kartta uyarı çıkıyor ve taşıyıcı etiketini yazıyor.
Dosya numarası tutuyorsa eşleşme kesin — personelin arayarak bulmasına
gerek yok.

Uyarı yalnızca bu tedaviye **henüz sperm bağlanmamışken** çıkıyor
(`sd_baglanti` boşken): bağlandıktan sonra zaten bağlı kaydın kendi kartı
var, ikisi birlikte görünmesi gürültü olurdu.

## Paylaşılan iki yardımcı

`dosya_no_sahibi(dosya_no)` ve `hastanin_sperm_kayitlari(hasta_id,
yalnizca_bagsiz=False)`. Üç ekran da bunları çağırıyor; sorgu üç yere
kopyalanmadı. İkincisinin `yalnizca_bagsiz` süzgeci androloji uyarısı için
(bağlanmayı bekleyenler), hasta kartı ise hepsini gösteriyor.

## Kapsamadığı durum

Erkek hasta **kendi ayrı dosya numarasıyla** kayıtlıysa (onkoloji öncesi
sperm dondurma için açılmış, çiftin dosyasından bağımsız bir kayıt) dosya
numarası tutmaz ve bu uyarıların hiçbiri çıkmaz. O durum zaten **elle
eşlemenin** kapsamı (v6.86): androloji ekranından bütün laboratuvar aranıp
bağlanıyor, `sperm_dondurma.hasta_id` erkekte kalıyor,
`kullanim_cycle_id` eşin tedavisini gösteriyor. Bu sürüm o yolu
değiştirmedi, yanına kesin olan ikinci bir yol koydu.

## Test edildi

Tek `hasta` satırında bir çift (dosya no 700001, AYŞE YILMAZ / eşi MEHMET
YILMAZ), bir `ivf_icsi` tedavisi ve aynı dosya numarasına bağlı bir
dondurulmuş sperm kaydı (SP-700001-01) kurularak:

- `/hasta/kontrol?dosya_no=700001` → `cycle_sayisi: 1`, `sperm_sayisi: 1`,
  `es_adi: "MEHMET YILMAZ"`; kayıtsız numara ve rakam olmayan metin
  `{"var": false}` döndü. Oturumsuz istek `/giris`'e düştü — uç nokta
  hasta adı sızdırmıyor.
- Playwright: yeni-hasta formuna "700001" yazılınca uyarı kutusu açıldı ve
  dört bilgiyi de bastı, bağlantısı `/hasta/14/sperm-dondurma/yeni`;
  "999999" yazılınca kutu kapandı.
- POST ile aynı numara gönderildi: kutu bağlantısıyla birlikte basıldı,
  **yeni hasta kaydı açılmadı** (tabloda hâlâ tek satır), forma yazılanlar
  korundu.
- Hasta kartı kaydı listeledi; tedaviye bağlanmadan önce "Henüz bir
  tedaviye bağlanmadı", `/androloji/sperm-baglama` ile bağlandıktan sonra
  "Kullanıldığı tedavi: 2026-7001 · 700001 · AYŞE YILMAZ" yazdı.
- Androloji uyarısı bağlanmadan önce çıktı, bağlandıktan sonra kayboldu.
- `/hasta/yeni` (aynı uç noktayı kullanan öteki ekran) eski mesajıyla
  çalışmaya devam etti — gerileme yok.
- 24 ekran 200 döndü, sunucu günlüğünde hata yok; 1440x1000 ve 390x844'te
  sayfa yatay kaymıyor.

# v6.126 — geri oku gerçekten bir önceki ekrana gidiyor

Kullanıcının bildirdiği sorun: "Programda sol en üstte geri butonu var. Bir
önceki menüye geçmesi gerekirken farklı menülere geçiyor. Geri butonu hep
bir önceki menüye geçsin."

## Sorun neydi

Geri oku (`‹`) her şablonda **sabit yazılıydı** (`{% block geri %}`) — yani
"nereden geldiysen oraya" değil, "bu ekranın bir üst seviyesi neresiyse
oraya" gidiyordu. Ekrana tek bir yoldan giriliyorsa ikisi aynı şey; birden
çok yoldan giriliyorsa değil. En bariz ikisi:

| Ekran | Geri oku | Gerçekte nereden açılıyor |
|---|---|---|
| Cryo Haritası | `/hastalar` | ana menü (`_gezinme.html`, `ana.html`) |
| Yönetici | `/hastalar` | ana menü |

Yani ana ekrandan Cryo Haritası'na girip geri basınca Hasta Kayıtları'na
düşülüyordu — kullanıcının dediği "farklı menüye geçiyor" tam buydu. Aynı
sorun `/hasta/{id}` (istatistikten, cryo'dan, aramadan da açılıyor),
`/cycle/{id}` (ana ekrandan, `/bitenler`'den, ay listesinden) ve
`/sperm-dondurma/{id}` (cryo'dan, hasta kartından, androlojiden) için de
vardı.

v6.32/v6.34 bu sorunu görmüş ve **ekran ekran** çözmüştü (taşıyıcıda
`?cycle=N`, hasta kayıtlarında arşiv/ay ayrımı). Kullanıcı şimdi kuralın
genelleşmesini istedi.

## Çözüm: tek yerde, şablonlara dokunmadan

`base.html`'in sonunda küçük bir betik: sayfanın geri okuna tıklanınca,
**gerçekten bir önceki ekran biliniyorsa** `history.back()` çalışıyor.
55 şablonun geri okuna tek tek dokunmak tuzak #1'in tarifiydi.

**Şablonlardaki adres kaldırılmadı.** O hâlâ ekranın "bir üst seviyesi" ve
şu üç durumda tek davranış o: JS kapalı, doğrudan adresle/yer iminden
girilmiş, karekoddan ya da telefonun ana ekran simgesinden açılmış. Yani
değişiklik **eklemeli**: en kötü ihtimalle bugünkü davranış.

## Betiğin KARIŞMADIĞI dört durum

Hepsi bilerek — "hep geçmişe dön" demek bu programda birkaç yerde daha
kötü olurdu:

1. **Referrer yok ya da başka bir siteden gelinmiş.** Geçmişte bu
   uygulamanın bir ekranı olduğunu bilmiyoruz; `history.back()` kullanıcıyı
   programın dışına atardı.
2. **Gelinen sayfanın YOLU aynı, yalnızca sorgusu farklı** (`?oosit=`,
   `?duzenle=`, `?gun=`, `?asama=`). Bu "bir önceki ekran" değil, aynı
   ekranın başka bir hali. Kritik örnek: ICSI'nin "kaydet → sıradaki oosit"
   toplu giriş akışı (v6.35). Beşinci oositteyken geri basan embriyolog
   dördüncü oosite değil **tedavi ekranına** dönmek ister; saf
   `history.back()` onu tek tek geri yürütürdü. `esle.html`'in
   `location.href='...?asama='` seçicisi de bu kuralla kapsanıyor.
3. **Sayfaya bir yönlendirmeyle gelinmiş** (`performance` Navigation
   Timing'in `redirectCount`'u). Bu programda neredeyse her zaman
   "POST → 303" demek, yani az önce kaydedilen form: geri ok formun
   kendisine dönmemeli. Ölçüm doğrulandı — hasta düzenleme kaydından sonra
   `redirectCount = 1` çıkıyor ve betik devreye girmiyor.
4. **Ekranda geri oku yok** (ana ekran, giriş) — yapacak iş yok.

`location.reload()` (tazeleme, v6.54) ve `location.replace('/')`
(`/ekle`, v6.47) geçmişe satır **eklemiyor**, o yüzden ikisi de bu mantığı
bozmuyor.

## Yedek adresler de düzeltildi

Betik yalnızca bir önceki ekran bilinirken devreye giriyor; bilinmediğinde
şablonun adresi kullanılıyor. `cryo.html` ve `yonetim.html`'inki **o
durumda bile yanlıştı** (ikisi de ana menü öğesi, `/hastalar`'ın altında
değiller): `/hastalar` → `/`. Öteki 53 şablonun adresi doğru olduğu için
dokunulmadı.

## Neden `history.back()`, `?geri=<yol>` değil

CLAUDE.md'nin kuralı: adresten gelen metni doğrudan `href`'e yazmak
`javascript:` sokulmasına açık. `history.back()` tarayıcının kendi
yığınını kullanıyor, adrese hiçbir şey yazılmıyor. Referrer yalnızca
**karar vermek** için okunuyor (aynı köken mi, aynı yol mu) — hiçbir yere
yazılmıyor, `href` olarak kullanılmıyor.

## Test edildi

Playwright ile sekiz durum:

| Durum | Sonuç |
|---|---|
| ana ekran → Cryo → geri | `/` (eskiden `/hastalar`) |
| ana ekran → Yönetici → geri | `/` (eskiden `/hastalar`) |
| istatistik → hasta kartı → geri | `/istatistik` (eskiden `/hastalar`) |
| cryo → hasta kartı → geri | `/cryo` (eskiden `/hastalar`) |
| ICSI `?oosit=2` → geri | `/cycle/11` — toplu giriş akışı korundu |
| doğrudan adresle girildi → geri | şablonun adresi |
| hasta düzenleme kaydı sonrası → geri | `/hastalar` — forma dönmedi |
| **JS kapalı** → geri | şablonun adresi (artık doğru) |

Ayrıca 24 ekran 200 döndü, sunucu günlüğünde hata yok. Betik yazdırma
ekranlarında da var (`/form/ozet/{id}`, `/baglan`) — `{% block tazeleme %}`'nin
**dışına** konuldu, o blok oralarda boşaltılıyor.

---

# v6.129 — cryo harita Excel içeri alma geri alındı

Kullanıcının kararı: "Cryo Harita istediğim gibi olmadı. Cryo exceli
yükleme öncesi sürüme dönebilir misin?"

v6.127 (programdan önceki cryo haritasını Excel'den içeri alma, eşleştirme
ekranı) ve v6.128 (dolap haritası, konum yazım birliği) `git revert` ile
geri alındı. Kod ağacı v6.126 ile **birebir aynı** (doğrulandı:
`git diff 630654b` boş).

Geri alınan dosyalar: `eski_cryo.py`, `goc_042.py`, `templates/eski_cryo*.html`,
`templates/dolap.html`; `app.py`/`db.py`/`disari.py`/`xlsx_oku.py`/
`metinler.py`/`tarih_duzelt.py`/`teshis_silme.py` ve dört şablondaki
değişiklikler. **Silinmedi, revert edildi** — geçmişte duruyor
(`3dfd58a`…`51efd53`), gerekçeleriyle birlikte geri getirilebilir.

## Neden bir de temizlik betiği gerekti

**Kodu geri almak veritabanını geri almıyor.** Kullanıcı Excel'i gerçek
kurulumunda yüklemişti: `eski_cryo` tablosunda 5.415 kayıt ve içeri almanın
açtığı 2.522 `konum` satırı yerinde kalıyor.

Sadece durmalarına izin verilemezdi: `eski_cryo.hasta_id` `hasta(id)`'ye
yabancı anahtarla bağlı ve geri alınmış kod o bağı temizlemeyi bilmiyor.
Yani **bağ kurulmuş bir hastayı kalıcı silmek FOREIGN KEY hatası verir**,
üstelik `teshis_silme.py` de (o da geri alındı) sebebini söyleyemez.
Ölçüldü, gerçekten böyle patlıyor — tuzak #4'ün geri-alma hali.

`eski_cryo_temizle.py`: `eski_cryo` tablosunu düşürür, taşıyıcısı olmayan
`konum` satırlarını siler, `goc_kaydi`'ndan `goc_042`'yi çıkarır,
kullanılmamışsa iki taşıyıcı tipini (Rapid-i, Vitrifit) kaldırır. Yıkıcı
olduğu için `SIL` yazılmasını istiyor ve `liste` kipinde hiçbir şeye
dokunmadan ne silineceğini gösteriyor. **Kaynak Excel dosyasına
dokunulmuyor** — silinen, onun programa alınmış kopyası; kaybolan tek şey
elle kurulmuş hasta bağları.

Doğrulandı: temizlikten sonra kalıcı hasta silme FOREIGN KEY hatası
vermiyor, `PRAGMA foreign_key_check` temiz, 19 ekran 200 döndürüyor,
`/eski-cryo` ve `/dolap` 404, `/cryo` ve vitrifikasyon ekranında hiçbir iz
kalmamış, JS hatası yok.

## Bir sonraki oturuma not

Kullanıcı özelliğin **kendisini** istemedi; hatalı olduğu için değil.
Aynı şeyi kendiliğinden yeniden yazma. Eski haritayı programa almak
yeniden gündeme gelirse önce v6.127/v6.128 bölümlerini git geçmişinden
oku — orada neyin neden öyle yapıldığı, ölçülen sayılar ve üç somut tuzak
(koordinat kimliğinin bağ kaydırması, `.xlsx` ilişki yolunun iki türlü
yazılması, kâğıt düzeninin başlık tekrarları) yazılı.

# v6.130 — program öncesi Access kayıtlarının içeri alınması

Kullanıcının isteği: "Bu accdb dosyasında ağustos ayında laboratuvarda
tedavisini yaptığım hastalar... hasta kartı oluşturup tedavileri ekler
misin? Eğer aynı hasta varsa oluşturulmuş hasta kartına tedaviyi ekle."
Amacı ayrıca söyledi: "bir hastanın tedavi sayısı, daha önce ne yapıldığı,
kaç yumurta toplanıp ne kadar döllenip ne kadarı embriyo olduğu, ne kadar
dondurulduğu, transfer yapılıp sonuca ulaştı mı önemli."

Yeni dosya: **`aktar_access.py`**. Programın koduna neredeyse hiç
dokunmuyor (tek istisna aşağıdaki istatistik düzeltmesi) — ayrı bir araç,
veritabanına kayıt yazıyor.

## `.accdb` okunmuyor, CSV okunuyor

Access dosyasını doğrudan okumak ek bir kütüphane isterdi. Projenin "ek
bağımlılık yok" kuralı (`excel.py`, `karekod.py`, `xlsx_oku.py` hepsi
kütüphanesiz) burada da geçerli: kullanıcı Access'ten CSV'ye aktarıyor,
betik onu okuyor. Beş adımlık dışa aktarma yönergesi betiğin başında;
ayırıcı olarak hem virgül hem noktalı virgül tanınıyor (Türkçe Windows'ta
Access noktalı virgül yazıyor).

## Eşleştirme: yalnızca dosya numarası

Şemadaki `UNIQUE (lab_id, dosya_no)` sayesinde "aynı dosya no" = "aynı
hasta satırı". İsim karşılaştırması yok (v6.125'in kuralı: "isimle
eşleştirme yok" — kullanıcı iki kez böyle dedi). Dosya no programda varsa
tedavi o karta ekleniyor ve **ad üzerine yazılmıyor**; yalnızca boş olan
alanlar (eş adı, doğum tarihi, telefon) dolduruluyor.

**Aynı satır iki kez girmiyor.** Her tedavinin protokol notuna kaynağın
kendi kayıt numarası yazılıyor (`[Access kaydı #19]`); o işareti taşıyan
tedavi varsa satır atlanıyor. Yani betik iki kez çalıştırılabilir, yarıda
kalırsa kaldığı yerden devam eder. Ölçüldü: ikinci çalıştırmada 20 satırın
20'si atlandı.

## Sayılar neden oosit oosit açılıyor

Access toplam tutuyor ("8 toplandı, 7 MII, 3 2PN"); program her oositi ayrı
kaydedip sayıları **ondan türetiyor** (v6.38, v6.110). Yani sayıyı yazacak
bir kolon yok — yedi oosit kaydında "MII" yazması gerekiyor. Bu yüzden her
tedavi için toplanan oosit kadar `specimen` ve sayılara uyan `olay` satırı
açılıyor; tedavi özeti, hasta kartı, `/istatistik` oranları ve Excel
çıktıları hiçbir kod değişikliği olmadan doğru çalışıyor.

Bedeli: hangi oositin MII olduğu kaynakta yok, sırayla dağıtılıyor (önce
MII'ler, sonra immatür, sonra empty zona/dejenere/atretik; ICSI listenin
başından, yani önce MII'lere). Her tedavinin protokol notunda bu cümle
duruyor ve resmî forma da basılıyor: "oosit kayıtları toplam sayılardan
üretildi, tek tek gözlem değildir."

## INTAKT = 0PN

Kaynakta her satırda `İŞLEME ALINAN = 2PN + ANORMAL + İŞLEM SONRASI
DEJENERE + INTAKT` tutuyor — yirmi satırın hepsinde. Yani INTAKT
"döllenmemiş, bütün kalmış" oosit; programın `pn_sayisi` listesindeki `0`
tam olarak bu. Formun "ANORMAL FERTİLİZASYON (0/1/3PN)" kutusu programın
kendi tanımı gereği 0PN'i de sayıyor, o yüzden orada kaynağın ANORMAL
sütunundan büyük bir sayı görünür — kutunun etiketi zaten bunu söylüyor
(`formlar.py`: `anormal = sum(n for k, n in pn.items() if k and k != "2")`).

## FET: embriyo nereden geliyor

`fet` tedavilerinde çözülen embriyolar önceki aylarda, programın olmadığı
dönemde dondurulmuş; kaynak tedavi programda yok. `specimen.cycle_id`
embriyonun kendi cycle'ı olmalı (CLAUDE.md) ama burada öyle bir cycle hiç
yok. İki seçenek vardı:

- (a) embriyoyu hiç kaydetmemek,
- (b) FET'in kendi altına kaydetmek.

**(b) seçildi**, çünkü ağustosta yapılan **bütün** transferler FET
(ivf_icsi tedavilerinde taze transfer hiç yok). (a) ile program "ağustosta
hiç transfer yapılmamış" derdi — kullanıcının en çok istediği bilgi
kaybolurdu. `thaw`/`transfer` olayları `thaw_cycle_id`/`tr_cycle_id` ile
yine aynı tedaviyi gösteriyor; program her yerde `COALESCE(tr_cycle_id,
s.cycle_id)` kullandığı için sayılar doğru çıkıyor.

### Tek yan etkisi ve programdaki tek düzeltme

`/istatistik`'in "kayıtlı oosit" sayısı `specimen` satırlarını sayıyordu;
FET embriyoları toplanmış yumurta gibi görünüp M2 oranını düşürdü
(ölçüldü: 105 oosit, %63.8 — doğrusu 94 ve %71.3). Bu **aktarımdan
bağımsız bir doğruluk hatası**: çözülmüş bir embriyo hiçbir dünyada
"toplanan oosit" değil. `disari.istatistikler()` düzeltildi — oosit sayımı
artık yumurta toplanan tedavilerle sınırlı.

Bunun için `FET_TIPLERI` **`db.py`'ye taşındı**: `disari.py` de aynı
ayrımı soruyor ve `app`'i import edemiyor (app zaten disari'yi import
ediyor). `app.FET_TIPLERI` adı duruyor, `db.FET_TIPLERI`'den besleniyor —
yirmiye yakın kullanım yeri değişmedi.

## Tedavi nasıl kapanıyor

Aktarılan tedavi **açık bırakılmıyor**: bırakılsaydı ana ekranın
"Yapılacaklar" listesi (v6.28, her sabah bakılan kâğıt klasörün karşılığı)
ağustos işiyle dolardı. Ama kapanış sebebi uydurulmuyor:

- transfer tarihi **ve** transfer edilen embriyo sayısı varsa → `transfer`
- dondurulan embriyo sayısı varsa → `dondurma`
- kaynağın NOTLAR metni açıkça "iptal edildi"/"uygulanmadı" diyorsa →
  `iptal` (aşağıya bak)
- hiçbiri değilse → `durum='tamamlandi'`, **sebep boş**. `cycle_detay.html`
  bu durumu zaten biliyor (`c.durum == "tamamlandi" or c.bitis_sebebi`,
  sebep yoksa "Tamamlandı" rozeti basıyor).

### İptal sebebi serbest metinden, iki kademeli

Serbest metinden klinik karar çıkarmak riskli. Bu yüzden önce metin açıkça
"İPTAL"/"UYGULANMADI" demeli; **ancak ondan sonra** hangi ayrıntılı sebep
olduğuna bakılıyor (v6.103'ün `IPTAL_DETAY_SEBEPLERI`'si), tanınmazsa genel
"İptal" kalıyor. Yirmi satırda: 3 `cleavage_arrest` ("2./3. gün embriyo
arresti", "klivaj aşamasında embriyo arresti"), 1 `fert_olmadi`, 3 genel
iptal (empty zona — listede karşılığı yok). `liste` kipi hangi satıra ne
yazılacağını tek tek basıyor; aktarmadan önce okunacak.

Aynı iki kademeli mantık dondurma için de var: yumurta dondurmada
"DONDURULAN EMBRİYO SAYISI" alanı boş (o kolon embriyo için) ve kaç
yumurtanın dondurulduğunu yalnızca not söylüyor ("16 ADET OOSİT 4 TÜPTE
... DONDURULARAK SAKLANDI") — o cümle varsa tedavi `dondurma` ile
kapanıyor. Sayı **not metninden çıkarılmıyor**, vitrifikasyon kaydı
açılmıyor: serbest metinden sayı ayıklamak kırılgan olurdu.

## `_sade()` bütün Türkçe harfleri katlıyor

İlk yazışta yalnızca `İ` katlanıyordu ve "3. GÜN EMBRİYO ARRESTİ SEBEBİYLE
İŞLEM İPTAL EDİLDİ" notu `cleavage_arrest` yerine genel iptale düşüyordu:
kalıptaki `GUN` ile metindeki `GÜN` tutmuyordu. `str.maketrans("İIŞĞÜÖÇ",
"IISGUOC")` ile hepsi katlanıyor, kalıplar ASCII yazılıyor. Aynı katlama
sperm alınma/hazırlama yöntemlerinin yazım farklarını da tekliyor
(SWİM UP/SWIM UP, EJAKÜLAT, ÇÖZME SPERM).

## Protokol notu kısa tutuldu — form kutusu taşıyordu

İlk yazışta aktarımın bütün ayrıntıları (empty zona sayısı, taşıyıcı yok,
MI/GV ayrımı, taraf ayrımı) protokol notuna yazılmıştı. O metin Embriyoloji
Özet formunun NOTLAR kutusuna basılıyor (v6.102) ve kutu `white-space: pre`
— uzun satır sarmıyor, **kutunun dışında kesiliyor**. Ekran görüntüsünde
görüldü. Şimdi notta yalnızca kaynağın kendi metni, tek cümlelik uyarı ve
işaret var; satırlar 68 karakterde sarılıyor. Ölçüldü: kutunun
`scrollWidth == clientWidth` ve `scrollHeight == clientHeight`, yani hiçbir
yönde taşma yok. Ayrıntılar zaten verinin kendisinde: maturasyon olayı
olmayan oosit = empty zona, taşıyıcısız vitrifikasyon kaydı = yeri bilinmiyor.

## Aktarılmayanlar — uydurulmadı

- **Gebelik sonucu**: kaynağın bütün gebelik alanları (BHCG, USG, doğum)
  boş. "Transfer yapılıp sonuca ulaştı mı" sorusunun ilk yarısı aktarıldı,
  ikinci yarısı bu dosyada yok.
- **Cleavage/blastokist sayısı**: kaynakta gün 2/3/5'te kaç embriyo olduğu
  yok. Aşama yalnızca dondurulan ve transfer edilen embriyo için yazılı.
  Dondurulanlar için o kadarı kaydedildi (gün ≥ 5 blastokist, öncesi
  cleavage değerlendirmesi, skor alanları boş) — yani bu sayılar "en az"
  demek. FET'te transfer edilen embriyo için yazılmadı: o embriyo bu
  tedavide gelişmedi, `oran_blast`'ın paydasında karşılığı yok.
- **Taşıyıcı ve konum**: kaynakta yok. Vitrifikasyon olayı
  `vit_tasiyici_id` olmadan yazılıyor — sayı doğru, Cryo Haritası'nda
  görünmüyor. Taşıyıcı uydurmak v6.127'nin geri alınan hatasıydı.
- **EMPTY ZONA**: `maturasyon` listesinde karşılığı yok. O oositler kayıt
  olarak açılıyor, maturasyon olayı yazılmıyor (7 oosit).
- **MI/GV ayrımı**: kaynak ikisini toplamış, hepsi `mi` yazıldı (18 oosit).
- **OPU sağ/sol**: kaynakta taraf yok; toplam `opu_sag_oosit`e yazıldı
  ("Toplanan" bu ikisinin toplamı, v6.112), özet kutusunda "sağ N · sol 0"
  görünüyor.
- **TEDAVİ PROTOKOLÜ** (GONAPEPTYL gibi ilaç adı) `protokol_tipi`
  listesine (antagonist/long agonist/...) uymuyor; eşlemek klinik bir
  varsayım olurdu. Ham metin notta, `protokol_tipi` boş.
- **NOTLAR CONFIDENTIAL**: telefon `hasta.telefon`a, parantez içindeki
  endikasyon (`AOR`, `ERKEK FAKTÖR`) `cycle.endikasyon`a gidiyor. Protokol
  notuna **yazılmıyor** — o metin resmî forma basılıyor, hasta telefonunun
  orada işi yok.

## `olusturma_zamani` tedavinin tarihine çekiliyor

Kayıt bugün açılıyor ama iş ağustosta yapıldı. Ay listeleri ve
`/istatistik`'in ay süzgeci `COALESCE(c.opu_zamani, c.olusturma_zamani)`
kullanıyor — FET'te `opu_zamani` yok, bu alan olmasa yedi FET eylül ayına
düşerdi. Aynı sebeple hasta kaydının damgası da ilk tedavisinin tarihine
çekiliyor: "Son kayıtlar" (v6.124, son 7 gün) aktarılan eski kaydı "bu
haftanın işi" gibi göstermemeli.

## Ölçüm

20 satır, 20 hasta, 20 tedavi (8 ivf_icsi, 7 fet, 5 oosit_cryo), hata yok.
Kaynak ile program satır satır karşılaştırıldı:

| | kaynak | program |
|---|---|---|
| toplanan oosit | 94 | 94 |
| MII | 67 | 67 |
| immatür (MI) | 18 | 18 |
| dejenere | 2 | 2 |
| empty zona | 7 | 7 (maturasyon olayı yok) |
| ICSI | 44 | 44 |
| 2PN | 23 | 23 |
| 0PN (intakt) | 19 | 19 |
| ICSI sonrası dejenere | 2 | 2 |
| dondurulan | 7 | 7 |
| çözülen | 11 | 11 |
| transfer | 8 | 8 |
| sperm örneği | 7 | 7 |

`/istatistik?yil=2026&ay=8`: 20 tedavi, %71.3 M2, %52.3 fertilizasyon,
%17.4 blastokist, gebelik oranı %0 (kaynakta sonuç yok). 45 adres 200
döndürdü (bütün aşama ekranları, iki resmî form, beş Excel çıktısı dahil).
`teshis.py` "tarihlerin yılları makul" diyor, `teshis_silme.py` aktarılan
bir hastada bütün silme adımlarını geçiyor, `PRAGMA foreign_key_check`
temiz. Ana ekranın "Devam Eden Tedaviler" kartı ağustos işiyle dolmuyor.

## Sonraki oturuma not

Kaynak dosya ve ondan üretilen CSV **depoya girmedi** ve girmemeli: gerçek
hasta verisi. Bu bölümde de hiçbir hasta adı/dosya numarası yok, bilerek.

# v6.131 — dondurulan embriyonun skoru nottan çıkarılıp aşama ekranlarına yazıldı

Kullanıcının isteği (v6.130'un aktarımını gördükten sonra): "Vitrifikasyon
yapılan yani dondurulan embriyosu olan hastaların sadece not olarak
belirtiliyor. Notta embriyo adedi kalitesi ve nasıl dondurulduğu bilgisi
var. Bunları ilgili menülere yerleştirsen. Yani 4BB blastokist dondurulmuş
yazıyor ise blastokist bölümüne fotoğrafsız 4BB embriyo kaydedip
vitrifikasyonda da bunun dondurulduğunu ilgili bölüme yaz."

Haklıydı: v6.130 skoru serbest notta bırakıyordu ve dondurma aşamasından
yalnızca boş bir değerlendirme olayı üretiyordu ("gün 5 blastokist", skor
alanları boş).

## Serbest metinden klinik veri — neden bu sefer yapılabilir

Normalde kaçınılan bir şey. İki gerekçeyle yapıldı:

1. **Yazım programın kendi skor biçiminin birebir aynısı.** `app.blast_skor()`
   blastokistte `genişleme + ICM + TE` ("4BB"), blastokist dışında
   `kısaltma + derece` ("KAV2") üretiyor; kâğıda da tam böyle yazılmış.
   Yani eşleme yorum değil, çeviri.
2. **Tanınmayan hiçbir şey atılmıyor.** Her değerlendirme olayının notuna
   kullanıcının kendi yazımı olduğu gibi giriyor ("Kaynak kayıttaki yazım:
   4BB HATCHED"), tanınmayan parça ayrıca raporda listeleniyor ve `liste`
   kipi yazmadan önce hepsini basıyor.

Tanınan yazımlar (hepsi gerçek kayıtlardan geldi):

| nottaki yazım | programa yazılan |
|---|---|
| `3AA` | `bl_genisleme=3`, `bl_icm=a`, `bl_te=a`, `bl_skor=3AA` |
| `4BB HATCHED` | `bl_genisleme=4`, `bl_icm=b`, `bl_te=b` — "HATCHED" olayın notunda |
| `KAVG2` | `bl_genisleme=kavitasyon`, `bl_derece=2`, `bl_skor=KAV2` |
| `4HG2` / `3HG2` | `cl_hucre_sayisi=4/3`, `cl_skor=G2` |
| `2*M2`, `3*M2` | dondurulan **yumurta** grubu (tüp başına adet) |

Çözümleme yalnızca "... DONDURULARAK SAKLANDI" cümlesinin **öncesine**
bakıyor: bir kayıtta o cümleden sonra ilgisiz metin geliyor ("SPERM
MORFOLOJİSİ KÖTÜ ... MOTİLİTE %0") ve oradaki sayılar skor sanılmamalı.

`bl_skor_kaynagi`/`cl_skor_kaynagi` **"elle"** yazılıyor, "otomatik" değil:
skor bir insanın verdiği not, otomatik hesap onu ezmemeli (v6.122'nin
"otomatik skorlar kaynak işaretler" kuralı).

## Vitrifikasyon kaydı bilerek AÇILMIYOR

v6.130 taşıyıcısız `vitrifikasyon` olayları yazıyordu. Ölçüldü: bunlar
**vitrifikasyon ekranında hiç görünmüyor** — "Dondurulmuş" listesi
`embriyolar|selectattr('tasiyici_id')` ile kuruluyor, taşıyıcısı olmayan
kayıt "aday" tarafında kalıyor. Yani istatistik "7 donduruldu" derken ekran
"hiçbiri dondurulmamış" diyordu; iki ayrı yerin birbirini tutmaması,
saklanan bir sayacın yarattığı soruna benziyor.

Taşıyıcı uydurulamaz:
- **Etiket tüpün üstünde yazan gerçek ad**, kaynak kayıtta yok (Access'in
  "TÜP NO" alanı hiç doldurulmamış; notlar yalnızca tüp **sayısını**
  söylüyor: "2 TÜPTE (3*M2) (3*M2)").
- `tasiyici.etiket` **`UNIQUE` ve değiştirilemiyor** — düzenleme rotası yok.
  `vit_sil` yalnızca taşıyıcıyı "boşaltıldı"ya düşürüyor, etiket kalıyor.
  Yani yanlış bir etiket Cryo Haritası'na kalıcı bir hayalet bırakırdı.
- Cryo Haritası'nın bütün amacı "bu hastanın embriyosu hangi tüpte, nerede".
  Oraya gerçekte olmayan bir ad yazmak, boş bırakmaktan kötü.

Bunun yerine embriyolar **skorlarıyla birlikte vitrifikasyon ekranının aday
listesinde** çıkıyor ("Embriyo 1 · 3AA · gün 5"); kullanıcı orada seçip
gerçek etiketi ve tank konumunu girerek donduruyor. v6.130'un yazdığı
taşıyıcısız kayıtlar `tamamla` kipinde iptal ediliyor (silinmiyor — sebebi
`iptal_sebep`'te yazılı).

Aynı sebeple **yumurta dondurmaya da vitrifikasyon yazılmıyor**; bunun
yerine notun söylediği sayı ve tüp dağılımı raporda basılıyor
("6 yumurta, 2 tüpte 3+3"), kullanıcı ekrandan giriyor. Bu, v6.130'da açık
bırakılan "kaç yumurta donduruldu" sorusunu da yanıtlıyor: sayı nottan
okunabiliyor, eksik olan yalnızca tüp etiketi.

## `tamamla` kipi — aktarılmış veriyi baştan almadan güncellemek

```
python aktar_access.py tamamla agustos_2026.csv
```

Kullanıcı v6.130'u kendi kurulumunda **çalıştırmıştı**; yeni sürüm için
yedekten dönüp baştan aktarmak gerekmesin diye. Yalnızca nottan çözümlenen
kayıtları işliyor, var olan değerlendirmeyi **güncelliyor**, ikinci satır
açmıyor (`_degerlendirme_yaz()` aynı örnek + aynı tipte iptal edilmemiş bir
olay varsa onu `UPDATE` ediyor). Art arda iki kez çalıştırıldı, ikincisi
hiçbir şeyi değiştirmedi.

Hedef örnekler önce "daha önce vitrifikasyon kaydı olanlar", sonra 2PN
olanlar sırasıyla seçiliyor — böylece `tamamla` taze aktarımla aynı
embriyolara denk geliyor.

## Ölçüm

Yedi dondurma notunun hepsi doğru çözümlendi, tanınmayan parça çıkmadı:
2×`3AA`, 1×`4BB HATCHED`, 1×`KAVG2`, 3×`4HG2/3HG2`, ve üç yumurta dondurma
(2 / 6 / 16 yumurta; 1 / 2 / 4 tüp). Ekranlarda doğrulandı: blastokist
ekranı şeritte "1-3AA 2-3AA" gösteriyor, kartta Genişleme "3 - Tam
blastokist" / ICM A / TE A / Skor 3AA; cleavage ekranı "1-4H 2-4H 3-3H",
Hücre sayısı 4, Skor G2; vitrifikasyon ekranı embriyoları "3AA · gün 5"
etiketiyle aday listesinde gösteriyor. 18 adres 200 döndürdü.

Ağustos sayıları: blastokist 4, cleavage 3, dondurulmuş 0 (taşıyıcı
girilene kadar — bilinçli).

# v6.132 — dondurma kaydı taşıyıcısıyla yazılıyor (v6.131'in kararı geri alındı)

Kullanıcının tek cümlelik düzeltmesi: **"Vitrifikasyon bölümünde etiket kodu
üretiyor. Onu kullansan."**

v6.131 taşıyıcı açmamıştı, gerekçesi "etiket tüpün üstünde yazan gerçek ad,
uydurulamaz" idi. **Bu gerekçe yanlıştı.** `vit_ekran()` zaten şunu
döndürüyor:

```python
"onerilen": f"{c['cycle_no']}-{_d.now().strftime('%H%M')}"
```

Yani etiket tüpten okunan bir ad değil, **programın kendi ürettiği kod**;
personel ekranda çoğu zaman onu kabul edip tüpün üstüne o kodu yazıyor.
Aktarım da aynı kalıbı kullanabilir — ve kullanmalı, çünkü taşıyıcı olmadan
dondurma ne vitrifikasyon ekranında ne Cryo Haritası'nda görünüyor.

Ders: **bir alanın "elle girilen gerçek bir ad" mı yoksa "programın ürettiği
bir kod" mu olduğunu, kullanıldığı ekranın kendi varsayılanına bakarak
belirle.** v6.131 bunu yapmadan "uydurulamaz" dedi ve kullanıcıya gereksiz
iş çıkardı.

## Bir parantez grubu = bir tüp

Notlardaki grup yapısı tüp dağılımını da veriyor. Yazılı tüp sayısı olan üç
satırın **üçünde de** grup sayısı birebir tutuyor:

| not | grup | yazılı |
|---|---|---|
| `6 ADET OOSİT 2 TÜPTE (3*M2) (3*M2)` | 2 | 2 |
| `16 ADET OOSİT 4 TÜPTE (4*M2) ×4` | 4 | 4 |
| `1TÜPTE 3 ADET D3 EMBRİYOSU (4HG2-4HG2-3HG2)` | 1 | 1 |

Grup içinde `-` örnekleri ayırıyor, `N*M2` ise N yumurta demek. Tüp sayısı
yazılmamış satırlarda (`2 ADET D5 EMBRİYO (3AA) (3AA)` → 2 tüp) dağılım bu
yapıdan okunuyor. Kural doğrulanabilir olduğu için varsayım değil.

## Ne yazılıyor

- **Taşıyıcı**: `tasiyici` satırı, etiket `<tedavi no>-<SSDD>`, tip
  `cryotop`, `durum='dolu'`, `kategori='embriyo'`. Aynı tedavide birden çok
  tüp varsa dakika ilerliyor (`UNIQUE(lab_id, etiket)`) — tüpler zaten arka
  arkaya hazırlanıyor.
- **Vitrifikasyon saati**: embriyoda kaynak kaydın söylediği gün (OPU + 5 /
  OPU + 3) saat 12:00; yumurtada OPU günü 14:00 (denüdasyondan sonra).
- **Konum boş** — kaynak kayıtta tank/kanister/goblet/pozisyon yok ve ekranın
  kendisi de boş bırakılmasına izin veriyor ("taşıyıcı sistemde görünür ama
  nerede olduğu bilinmez"). Cryo Haritası bu tüpleri **"konum girilmemiş"**
  diye işaretliyor, kullanıcı oradan giriyor. Uydurulan tek şey yok.
- v6.131'in bıraktığı taşıyıcısız vitrifikasyon olayları iptal ediliyor
  (silinmiyor, `iptal_sebep` yazılı).

## İdempotanlık

`tamamla` ikinci kez çalıştırıldığında: değerlendirme güncelleniyor,
**dondurmaya hiç dokunulmuyor** ("dondurma zaten girilmiş"). Sebep: kullanıcı
o arada konumu elle girmiş olabilir; yeniden yazmak onu silerdi. Kontrol
`_vitrifikasyon_var()` — taşıyıcıya bağlı, iptal edilmemiş bir vitrifikasyon
olayı varsa o tedavinin dondurması bitmiş sayılıyor.

## Ölçüm

12 taşıyıcı açıldı, 31 örnek donduruldu (7 embriyo + 24 yumurta) — kaynak
notların söylediği sayıların aynısı. Ağustos istatistiği: dondurulmuş 31,
blastokist 4, cleavage 3, M2 oranı %71.3 (değişmedi). Cryo Haritası 12 tüpü
"konum girilmemiş" uyarısıyla listeliyor, vitrifikasyon ekranı embriyoları
"Dondurulmuş (2)" başlığı altında gösteriyor. 16 adres 200 döndürdü, ikinci
`tamamla` hiçbir şeyi değiştirmedi.

## Bilinen kusur — kullanıcıya soruldu

Cryo Haritası taşıyıcı satırında `say("n_embriyo", t.adet)` yazıyor, yani bir
tüp dolusu **yumurta** da "4 embriyo" diye görünüyor. Bu v6.132'nin açtığı
bir hata değil — program daha önce hiç yumurta dondurma kaydı görmemişti, o
yüzden ortaya çıkmamıştı. Düzeltmek `cryo_harita()`'nın sorgusuna taşıyıcının
cycle tipini eklemeyi gerektiriyor; kelimenin ne olacağı (yumurta/oosit)
kullanıcının sözlüğü, ona soruldu.

# v6.133 — taşıyıcıda yumurta varsa "yumurta", embriyo varsa "embriyo"

Kullanıcının isteği: **"Yumurta donduruluyorsa Yumurta, Embriyo
donduruluyorsa Embriyo yazsın."**

Cryo Haritası her taşıyıcı için `say("n_embriyo", t.adet)` basıyordu, yani
bir tüp dolusu yumurta da **"4 embriyo"** diye görünüyordu. Bu v6.132'nin
açtığı bir hata değil: program o güne kadar hiç yumurta dondurma kaydı
görmemişti (`oosit_cryo` tedavilerinde vitrifikasyon hiç girilmemişti), o
yüzden ortaya çıkmamıştı.

## Karar tek yerde: `_yumurta_mi(cycle_tipi)`

Ayrım zaten `_ornek_adi()` içinde vardı (`"oosit_ad" if cycle_tipi ==
"oosit_cryo" else "embriyo_ad"`) ama satır içine gömülüydü. Ayrı bir
fonksiyona alındı; artık iki soruyu birden yanıtlıyor — aşama ekranında
örneğe ne deneceği ve taşıyıcının içinde ne olduğu. **Yumurta donduran yeni
bir cycle tipi eklenirse tek satır değişecek, ikisi birden doğru olacak.**

Yalnızca `oosit_cryo`'da yumurta donuyor: `ivf_icsi`'nin vitrifikasyon
ekranı zaten `_ICSI_YAPILMADI` süzgeciyle enjekte edilmiş (embriyo olmuş)
örnekleri listeliyor, `fet` tiplerinde de dondurma yapılmıyor.

## Altı yerde aynı etiket

Aynı nesnenin ("bu taşıyıcıda ne var") altı ayrı yerde yazıldığı ortaya
çıktı; biri düzeltilip ötekiler bırakılsaydı ekranlar birbirini tutmazdı:

- `cryo.html` — tank satırı, taşıyıcı satırı
- `cycle_thaw.html` — dolu taşıyıcı, çözülmüş taşıyıcı
- `tasiyici.html` — "İçerik" satırı, "Bu taşıyıcıda n ... var" uyarısı,
  "İçindeki embriyolar" başlığı

Hepsi yeni Jinja global `icerik_sayisi(adet, cycle_tipi)` ya da
`yumurta_mi(cycle_tipi)` üzerinden geçiyor. Yeni metin anahtarları:
`n_yumurta`, `n_yumurta_tekil`, `tasiyicida_n_yumurta`,
`icindeki_yumurtalar` — İngilizceleri de yazıldı (`oocyte(s)`).

## Taşıyıcının içeriği sorguya eklendi

`ICERIK_TIPI` — taşıyıcının içindeki ilk örneğin tedavi tipini veren alt
sorgu, metin olarak üç sorguda paylaşılıyor (üçünde de taşıyıcı `t` diye
adlanıyor). **İlk satır yeter**: bir taşıyıcı tek bir tedavinin örneklerini
taşıyor — ekrandaki vitrifikasyon kaydı tek seferde tek cycle'dan seçim
yapıyor, `aktar_access.py` de tüp başına tek grup yazıyor.
`tasiyici_icerigi()` ayrıca `c.cycle_tipi` döndürüyor.

## Tank satırı ikisini ayrı sayıyor

Bir tankta hem embriyo hem yumurta olabilir, orada tek bir kelime seçmek
mümkün değil. Tank sorgusu ikisini ayrı sayıyor, şablon sıfır olmayanı
basıyor: tek tip varsa görünüm eskisiyle aynı ("3 taşıyıcı · 12 embriyo"),
karışıksa ikisi de yazıyor. Ölçüldü: aynı tanka bir embriyo ve bir yumurta
taşıyıcısı konunca satır **"Tank 9 · 2 taşıyıcı · 1 embriyo · 4 yumurta"**
oluyor.

## Ölçüm

Cryo Haritası: dört embriyo tüpü "embriyo", sekiz yumurta tüpü "yumurta".
Taşıyıcı detayında üç etiketin üçü de (İçerik / uyarı / başlık) doğru
kelimeyi kullanıyor. Çözme ekranı: `oosit_cryo` tedavisinde "4 yumurta",
`ivf_icsi`'de "3 embriyo". 11 adres 200 döndürdü.

**`oosit_ad` metnine dokunulmadı** — o hâlâ "Oosit" ve aşama ekranlarında
öyle görünüyor. Kullanıcı bu ekran için "Yumurta" dedi; aşama ekranlarının
sözlüğünü değiştirmek ayrı bir karar, sorulmadan yapılmadı.


# v6.134 — ekranda "oosit" yazan her yer "yumurta" oldu

Kullanıcının isteği: **"oosit yazan her yeri Yumurta ile değiştir."** v6.133
taşıyıcının içeriğini ("yumurta"/"embriyo") düzeltmiş ama `oosit_ad`
metnine bilerek dokunmamıştı — "aşama ekranlarının sözlüğü ayrı bir karar,
sorulmadan yapılmadı" diye yazılmıştı. Kullanıcı o kararı verdi: her yerde.

## Ölçü: ekranda görünen Türkçe metin — kod tarafı değil

v6.79'un ("cycle" → "tedavi") kuralının aynısı uygulandı. Değişen yalnızca
kullanıcının gördüğü yazı:

- `metinler.py`'nin **`tr` değerleri** (61 metin). `en` değerlerine
  dokunulmadı: "oocyte" İngilizce klinik literatürün kendi kelimesi, ayrıca
  o çeviri zaten yarım ve askıda (bekleyen iş 8).
- `app.py`'de ekrana basılan iki doğrulama etiketi ("Sağ/Sol over yumurta
  sayısı") ve `/yonetim`'deki tablo adı ("Örnek (yumurta/embriyo)").
- `disari.py`'nin dört Excel sütun başlığı.
- `formlar.py`'nin `/formlar/etiketler` ekranındaki beş açıklaması.
- `liste_degeri.etiket`'te iki satır (`goc_043`): "Oval oosit" → "Oval
  yumurta", "Donör oosit" → "Donör yumurta". Yalnızca **hâlâ eski etiketi
  taşıyan** satır güncelleniyor — yönetici kendi eliyle değiştirmişse
  üzerine yazılmıyor.
- `aktar_access.py`'nin protokol notuna yazdığı cümle + daha önce
  aktarılmış kayıtlar (`goc_044`, aşağıda).

**Değişmeyen (bilerek):**

- **Kod tarafının tamamı**: `specimen.durum='oosit'`, `opu_sag_oosit`/
  `opu_sol_oosit` kolonları, `?oosit=N` adres parametresi, `oosit_cryo`
  tedavi kodu, `metin()` **anahtarları** (`oosit_ad`, `oosit_n`,
  `henuz_oosit_yok_icsi`, …), Jinja değişkenleri (`oositler`), Python
  fonksiyon adları (`_oositleri_ac`, `_oosit_sayilari`). v6.79'da "cycle"
  için ne yapıldıysa aynısı: anahtar ve kolon adı değiştirmek göç +
  şablon + rota zinciri demek, kazancı sıfır.
- **Resmî formların kâğıt kalıbı.** Embriyoloji Özet'in üstünde hâlâ
  "OOSİT BİLGİLERİ", "TOPLANAN OOSİT", "İŞLEME ALINAN OOSİT SAYISI"
  yazıyor — bunlar kalite sisteminden gelen kurum belgesinin kendi
  yazısı ("kalıba dokunma", v6.37). Kâğıt değişirse
  `formlar_asil/kalip_uret.py` yeniden çalıştırılır.
- **Access'ten gelen serbest metin.** Aktarılan tedavilerin notunda
  laboratuvarın kendi cümleleri var ("EZ OOSİT OLDUĞUNDAN DOLAYI İŞLEM
  İPTAL EDİLDİ"). O, ağustos ayının kaydının aslı — programın yazdığı
  cümle değil, düzeltilmedi.
- **`degisiklik_log`'un kalıcı silme özeti** (`"… 12 oosit · 30 islem …"`).
  Denetim izi, ekran metni değil; geçmişe dönük yazılmış bir kayıt.

## Türkçe ek çekimi: düz değiştirme olmaz

"oosit" ünsüzle, "yumurta" ünlüyle bitiyor — ekler farklı. Tuzak #1
("toplu metin değiştirme yapma") burada dilin kendisinden de geliyor:

| eski | düz değiştirme | doğrusu |
|---|---|---|
| oosite | ~~yumurtaa~~ | yumurtaya |
| oositin | ~~yumurtain~~ | yumurtanın |
| oositi | ~~yumurtai~~ | yumurtayı |
| oositler | yumurtalar | yumurtalar |

Değiştirme bu yüzden en uzun ekten başlayan bir eşleme listesiyle yapıldı
ve **61 metnin her biri tek tek okundu**. Sonuç ekrandan doğrulandı:
"Yumurtayı yeniden değerlendirebilirsin.", "Klinik işlem kaydı olan bir
yumurta silinmez.", "her dosya kendi yumurta numarasını alır".

`oosit_hazirla_ipucu` bir yan etki olarak **yanlış hale gelmişti**:
"fotoğrafsız yumurta kaydı açar (Oosit 1, Oosit 2, ...)" diyordu ama
`ornek_adi()` artık "Yumurta 1" basıyor. İpucu gerçeğe getirildi.

## Form etiketleri yeniden adlandırıldı, eskisi de çalışıyor

`/formlar/etiketler` ekranında yüklenen `.xlsx` formuna yazılacak
etiketler listeleniyor (v6.40). İkisi "oosit" diyordu:
`{{toplanan_oosit}}` ve `{{islenen_oosit}}`. Bunlar hem **ekran metni**
(kullanıcı listeden okuyup kutuya yazıyor) hem **sözleşme** (başka bir
laboratuvar formunu çoktan yüklemiş olabilir) — ikisi birden.

Çözüm: ekranda görünen ad `{{toplanan_yumurta}}` / `{{islenen_yumurta}}`
oldu, **eski adlar da kabul edilmeye devam ediyor** ve aynı değeri
basıyor. `formlar.ESKI_ALAN_ADI` tek satırlık eşleme; `ALAN_ADLARI` (yükleme
sırasında "tanınmayan etiket" uyarısını veren liste) ikisini de içeriyor,
`alanlar()` değer sözlüğüne yeni adları ekliyor. **`ozet_verisi()`'nin
kendi anahtarları ve hücre eşlemeleri (`OZET_KUTULARI`, `ARTLAB_IZGARA`)
hiç değişmedi** — değişen yalnızca etiketin adı. Ölçüldü: dört adın
dördü de aynı değeri veriyor (`toplanan_oosit` = `toplanan_yumurta` = 10).

Yeni bir etiket adı değiştireceksen aynı yolu izle: adı değiştir, eskisini
`ESKI_ALAN_ADI`'na koy. Sessizce kaldırmak, o etiketi kullanan yüklü bir
formu bir daha basılmaz hale getirirdi — hata da vermez, kutu boş çıkar.

## `goc_044` — aktarılmış tedavilerin protokol notu

`aktar_access.py` her aktardığı tedavinin protokol notuna şunu yazıyordu:

    Program öncesi Access kaydından aktarıldı; oosit kayıtları toplam
    sayılardan üretildi, tek tek gözlem değildir. [Access kaydı #N]

Bu cümle tedavi kartında **ve** resmî Embriyoloji Özet formunun NOTLAR
kutusunda basılıyor, yani ekran metni. Betik düzeltildi; göç daha önce
aktarılmış kayıtları aynı hale getiriyor (kullanıcı ağustos verisini çoktan
aktardı, göçler açılışta kendiliğinden çalışıyor — elle bir şey gerekmiyor).

**Göç metin içinde arama/değiştirme yapmıyor, paragrafı yeniden üretiyor.**
Sebep ölçülü: not `textwrap.fill(..., 68)` ile sarılıyor ve "oosit" →
"yumurta" iki karakter uzun. Düz değiştirme satırı 69-70 karaktere
çıkarırdı; NOTLAR kutusu `white-space: pre` olduğu için uzun satır sarmaz,
**sessizce kesilir** (v6.130'un kendi kuralı). Göç notun sonundaki
"Program öncesi Access kaydından aktarıldı;" ile başlayan paragrafı bulup
`[Access kaydı #N]` işaretini çıkarıyor ve paragrafı baştan kuruyor;
üstündeki her şey (kaynak protokol + Access'in serbest metni) olduğu gibi
kalıyor. İdempotent: ikinci çalıştırma 0 satır güncelliyor.

## Ölçüm

Playwright ile 51 ekran gezildi; `<script>`/`<style>` ve bütün etiketler
atılıp **basılan yazıda** `[Oo]osit` arandı — hiçbirinde kalmadı. Ayrıca
elle kontrol edilenler: `/cycle/{id}/fert`, `/blast`, `/cleavage?gun=3`,
`/cycle/{id}/arsiv-sil`, `/cryo/tasiyici/{id}`, `/cryo/tasiyici/{id}/thaw`,
`/yedekleme/geri-yukle`, `/cycle/{id}/denudasyon?duzenle=oosit` (hem
`ivf_icsi` hem `oosit_cryo`) — hepsi temiz.

Resmî formlar bozulmadı: `/form/ozet/{id}` ve `/form/artlab/{id}` 200,
`/disari/form/...` iki `.xlsx` da geçerli bir ZIP (10 parça, bozuk parça
yok), `/disari/tumu` ve `/disari/cryo` 200. NOTLAR kutusunun taşması
ölçüldü: yatay 0px, dikey 0px — yeni cümle kutuya sığıyor (ekran
görüntüsüyle de bakıldı, v6.109'un dersi).

`goc_044` bu makinede çalıştı: 13 tedavinin notu güncellendi, ikinci
çalıştırmada 0. Göç çalıştırıcısı açılışta da uyguladı.


# v6.135 — dondurulan embriyolar iki resmî forma da yazılıyor

Kullanıcının isteği, dört madde: (1) Embriyoloji Özet'in **EMBRİYO DONDURMA
AŞAMASI** kutusuna embriyonun kaçıncı gün dondurulduğu; (2) dondurulan
embriyolar **NOTLAR**'a, kaç tüp olduğu ve kalitesi **parantez içinde, her
parantez bir tüp**; (3) ART Lab'ın **FREEZE** bölümüne aynı parantezler,
birden çok tüp varsa alt satırlara; (4) ART Lab'ın **yorum** bölümüne varsa
yumurta bulguları.

## Bir tüp = bir taşıyıcı, bir parantez = bir tüp

Kullanıcının kendi yazım geleneği zaten buydu: Access notlarında ayrı tüpler
"(3AA) (3AA)", bir tüpteki üç embriyo "(4HG2-4HG2-3HG2)" diye yazılıydı.
`aktar_access.py` v6.132'de bu kuralı okuyup taşıyıcıları açmıştı; formlar
şimdi aynı kuralı tersinden okuyor.

Cevabı **tek yer** veriyor: `formlar.dondurma_tupleri(cycle_id)` — `olay`in
`vit_tasiyici_id`'sine göre gruplanmış, her tüp için içindeki örneklerin
kalitesi ve günü. İki form da onu çağırıyor; iki kopya olsaydı Özet'in
NOTLAR'ı ile ART Lab'ın FREEZE sütunu birbirini tutmazdı.

- **Kalite** `bl_skor` ("3AA", "KAV2"), cleavage'da hücre+skor ("8HG2") —
  `tasiyici_icerigi()`/Cryo Haritası'nın gösterdiğiyle aynı alan.
- **Gün** örneğin **kendi son değerlendirmesinin** günü (blastokist, yoksa
  cleavage). Programda "kaçıncı günde donduruldu" diye ayrı bir alan yok ve
  uydurulmadı: değerlendirmesi olmayan örnek güne katkı vermiyor, kutu boş
  kalıyor (yumurta dondurmada hep böyle).
- **Kalitesi kayıtlı olmayan tüp sayıyla görünür** — `(4)`, yani "bu tüpte
  dört örnek". Yumurta dondurmada hiçbirinin skoru olmaz; on üç tane `?`
  basmak kutuyu okunmaz yapardı. Bazısının kalitesi varsa eksik olan `?`
  ile görünüyor: sessizce düşürmek "bu tüpte bir tane var" derdi.

Ölçüldü (kullanıcının ağustos verisi, gerçek kayıtlar):

| tedavi | NOTLAR satırı | kaynak Access notu |
|---|---|---|
| 17 | `Dondurulan: 2 embriyo, 5. gün, 2 tüp: (3AA) (3AA)` | "2 ADET D5 EMBRİYO (3AA) (3AA)" |
| 32 | `Dondurulan: 3 embriyo, 3. gün, 1 tüp: (4HG2-4HG2-3HG2)` | "1TÜPTE 3 ADET D3 EMBRİYOSU (4HG2-4HG2-3HG2)" |
| 30 | `Dondurulan: 16 yumurta, 4 tüp: (4) (4) (4) (4)` | "16 ADET OOSİT 4 TÜPTE (4*M2) …" |

Program, kaynak metni hiç okumadan kendi kayıtlarından aynı cümleyi kuruyor.

## "EMBRİYO DONDURMA AŞAMASI" artık gün yazıyor

Kutu önceden blastokist **genişleme etiketini** basıyordu ("Tam blastokist").
O bilgi kaybolmadı: skoruyla birlikte NOTLAR'daki parantezlerde duruyor
(`3AA`'nın ilk hanesi zaten genişleme). Kutuya kullanıcının istediği
"kaçıncı gün" geldi.

## NOTLAR satırı 68 karakterde sarılı

Kutu `white-space: pre` — uzun satır sarmaz, **sessizce kesilir** (v6.130'un
kendi kuralı). `dondurma_notu()` bu yüzden `textwrap.fill(..., 68)` ile
sarıyor, `aktar_access.py`'nin protokol notuyla aynı ölçü. Sıra klinik akış:
protokol notu → dondurma → çözme notu (v6.102) → iptal sebebi (v6.104).

Ölçüldü: 34 tedavinin Özet formunda NOTLAR kutusunun taşması 0px (yatay ve
dikey), ekran görüntüsüyle de bakıldı.

## ART Lab: FREEZE sütunu sayı değil, tüp tüp parantez

Kâğıtta FREEZE sütununda **dört kutu** var (satır 28-31) — "birden çok tüp
varsa alt satırlarına yaz" tam buraya oturuyor. Dörtten çok tüp varsa son
kutu kalanı sayıyla söylüyor ("+3 tüp"); sessizce kırpmak "toplam dört tüp
var" derdi, tam liste zaten Özet'in NOTLAR'ında.

### Dar kutu: kesmek yerine taşırmak

Bir tüpte üç embriyo varsa "(4HG2-4HG2-3HG2)" bir oosit sütunu genişliğindeki
kutuya sığmıyor ve `.kalip td`'nin `overflow: hidden`'ı onu **sessizce
kesiyordu** — ekran görüntüsünde "(4HG2-4HG2" diye yarım görünüyordu.
Kullanıcıya soruldu, kararı: *"Thaw ve onun[ki] alana kadar satırı
uzatabilirsin."*

Çözüm yeni bir `.tasabilir` sınıfı (`overflow: visible`): yazı sığmazsa
sağdaki boş kutulara akıyor. **Excel'in kendi davranışı da bu** (dolu bir
hücrenin yazısı boş komşusuna akar), yani iki çıktı aynı görünüyor ve Excel
tarafında hiçbir şey eklemek gerekmedi.

- Hangi hücrelerin taşabileceğini **doldurma tarafı** söylüyor:
  `form_kalip.satirlar()`'a `tasan` parametresi eklendi, `deger`/`ek` ile
  aynı yerden geliyor. **Kalıp (`form_kalip.json`) değişmedi** — "kalıba
  dokunma" kuralı korunuyor, kâğıt aynı kâğıt.
- Yüklenen lab formları etkilenmiyor: `tasan` verilmezse davranış eskisi.
- **Bilinen tek sıkışıklık**: aynı tedavide hem üç örneklik bir tüp hem de
  çözme varsa (THAW kutusu satır 28'de dolu), uzun yazı onun üstüne 30px
  kadar biniyor. Kullanıcının verisinde böyle bir tedavi yok (ölçüldü);
  kesilmesindense binmesi tercih edildi, kesilen bir skor yanlış bilgi olurdu.

## ART Lab: yumurta bulguları alttaki geniş "Yorum:" satırında

"Yorum bölümü" belirsizdi, kullanıcıya soruldu: formda **iki tane** var —
ızgaranın en alt satırı (oosit başına, çok dar) ve kâğıdın altındaki
"Raporu dolduran … Yorum:" satırı (sayfa genişliğinde tek birleşik hücre).
Kullanıcı **alttaki geniş satırı** seçti. Doğru seçim olduğu ölçüldü:
ızgaraya konduğunda "3AA, Vakuol, Geniş PVS" kutudan **52px taşıyordu**.

Bulgular oosit numarasıyla yazılıyor, çünkü satır tek ve bütün tedaviyi
kapsıyor: `Yorum: 1: Vakuol, Geniş PVS · 3: Kalın zona`. Kâğıtta basılı
"Yorum:" yazısının arkasına ekleniyor — `ek` mekanizmasının tam işi
(`"Dosya No :"` + numara deseni).

- Bulgu **iki aşamada da** girilebiliyor (`ivf_icsi`'de ICSI ekranı,
  `oosit_cryo`'da denüdasyon — v6.96), bu yüzden aşama süzülmüyor; aynı
  bulgu iki aşamada da işaretliyse bir kez yazılıyor.
- Izgaranın kendi "Yorum" satırı **değişmedi**: blastokist skorunu
  göstermeye devam ediyor (v6.37'nin kararı, o skorun ART formunda başka
  yeri yok).
- Bulgu yoksa satıra hiçbir şey eklenmiyor, kâğıt aslındaki gibi kalıyor.

## `db.yumurta_mi()` — "2 embriyo" mu "12 yumurta" mı

`_yumurta_mi()` v6.133'te `app.py`'deydi; `formlar.py` de aynı soruyu
soruyor (NOTLAR satırındaki kelime) ve `app`'i import edemez — app zaten
formlar'ı import ediyor. Karar `db.py`'ye taşındı, `FET_TIPLERI`'nin
(v6.130) aynı gerekçesi; `app._yumurta_mi()` oradan besleniyor, ekrandaki
davranış değişmedi.

## Ölçüm

34 tedavinin **iki formu da** (68 sayfa) gezildi: `.kalip` hücrelerinde
kırpılan yazı **yok** (taşabilir işaretlileri hariç tutularak ölçüldü).
`%` ile başlayan iki hücrenin 8px taşması v6.37'den beri var, bu sürümle
ilgisi yok — dokunulmadı.

Excel: `/disari/form/ozet/32` ve `/disari/form/artlab/{17,32}` geçerli ZIP
(10 parça, bozuk parça yok) ve içlerinde yeni içerik doğrulandı —
`(4HG2-4HG2-3HG2)`, `(3AA)` iki satır, `Dondurulan: 3 embriyo, 3. gün,
1 tüp: …`, `Yorum:   1: Vakuol, Geniş PVS · 3: Kalın zona`.

Bulgusuz bir tedavide alt satır kâğıttaki gibi "… Yorum:" diye bitiyor.
51 ekranlık genel tarama yine temiz.


# v6.136 — "%  85.0" kutuya sığmıyordu: anlamsız ".0" düşürüldü

v6.135'in ölçümünde kalan tek kesilme: ART Lab'ın SEMEN bloğundaki
"% Motil" / "% Normal" kutuları. Kullanıcı "ona da bak" dedi.

**Sebep sayının biçimiydi, kutunun darlığı değil.** `sperm_analiz`'in yüzde
kolonları SQLite'ta REAL; 85 değeri `str()` ile "85.0" oluyor ve kâğıttaki
"%" ile birleşince "%  85.0" çıkıyordu. Ölçüldü: kutu **32px**, yazı
**40px** — fazlası `.kalip td`'nin `overflow: hidden`'ıyla sessizce
kesiliyor, ekranda "%  85." görünüyordu. v6.37'den beri böyleydi.

Düzeltme `_sayi()`'de, tek yerde: değer tam sayıysa ondalık düşüyor.

| yazı | genişlik | kutu 32px |
|---|---|---|
| `%  85.0` (önce) | 40px | 8px kesiliyordu |
| `%  85` (sonra) | 32px | **tam sığıyor** |
| `%  100` | 37px | 5px taşıyor (kesilmiyor, aşağıya bak) |

- **Gerçekten kesirli bir değer olduğu gibi kalıyor** — `0.8` ml, `0.1`
  lökosit, `85.5`%. Yuvarlamak klinik bir sayıyı değiştirirdi; resmî forma
  yanlış veri yazmak boş bırakmaktan da kötü (v6.37'nin kuralı).
- Düzeltme `_sayi()`'nin **17 çağıranının hepsini** kapsıyor, yani iki form
  da: ART Lab'ın "M/ml" kutusu artık "30.0" değil "30", Özet'in BAZAL VOLÜM
  kutusu "5.0" değil "5". Geniş kutular zaten kesilmiyordu, orada değişen
  yalnızca okunaklılık. Yüklenen lab formlarının `{{bazal_volum}}` gibi
  etiketleri de aynı değeri alıyor (geriye dönük uyumlu, sadece kısaldı).
- **Dört yüzde kutusu ayrıca `.tasabilir`** (v6.135'in mekanizması): %100
  ya da gerçekten kesirli bir değer 5px taşıyorsa komşunun 2px dolgusuna
  akıyor, kesilmiyor. Ekran görüntüsüyle bakıldı: "%  100Motil" diye sıkışık
  ama **eksiksiz** görünüyor. Kesilmesindense sıkışması tercih edildi.

## Ölçüm

34 tedavinin iki formu da (68 sayfa) yeniden gezildi: **kırpılan hücre 0**.
Kutusundan geniş tek yazı ART Lab'ın `(4HG2-4HG2-3HG2)`'si ve o `.tasabilir`
olduğu için tamamı görünüyor. Gerçek veride yüzde kutularının hiçbiri artık
taşmıyor (`%  85` ve `%  99` tam 32px).

Excel: `/disari/form/artlab/17` ve `/disari/form/ozet/17` geçerli ZIP; içinde
`%  85` / `%  99` var ve **hiçbir yerde `.0` ile biten değer kalmadı**.


# v6.137 — vitrifikasyon listesi süzüldü, devam edenler yeniden eskiye

Kullanıcının üç isteği: (1) vitrifikasyonda "Dondurulacak embriyolar"da bir
önceki aşamada kaydı yapılmamış embriyo görünmesin; (2) ana ekranın "Devam
Eden Tedaviler" kartı yeniden eskiye doğru sıralansın; (3) yumurta dondurma
tedavisinde başlık "Dondurulacak yumurtalar" olsun.

## 1) Kaydı olmayan örnek listeye girmiyor

Ölçüldü (kullanıcının ağustos verisi): bir `ivf_icsi` tedavisinde ekran
**dokuz** satır basıyordu ama yalnızca ikisi dondurulabilir bir embriyoydu.
Kalan yedi satır 0PN, zigotta kalmış ve immatür örneklerdi — hiçbiri
dondurulamaz, yalnızca yanlış seçim riski ve gürültü.

Süzgeç `_DEGERLENDIRILMIS`: örneğin iptal edilmemiş bir **cleavage ya da
blastokist** değerlendirmesi (ya da zaten bir vitrifikasyon kaydı) olmalı.

- **`oosit_cryo`'da UYGULANMIYOR.** `_ICSI_YAPILMADI`'nın (v6.105) birebir
  aynı tuzağı: yumurta dondurmada cleavage/blastokist aşaması hiç yok,
  süzgeç her yumurtayı eler ve ekran bomboş kalırdı. Koşul
  `TIP_ASAMALARI`'na bakıyor (`"blast" in ...`), cycle tipini elle
  yazmıyor — yeni bir tip eklenirse kendiliğinden doğru davranır.
- **Cleavage de sayılıyor, yalnızca blastokist değil.** Kullanıcının isteği
  "blastokist menüsünde kaydı yapılmamış" diyordu ama bu laboratuvar **gün 3
  embriyosu da donduruyor** — ağustos kaydı: "1 TÜPTE 3 ADET D3 EMBRİYOSU
  (4HG2-4HG2-3HG2)". Yalnızca blastokist aransaydı gün 3'te dondurma
  programda **tümden yapılamaz** hale gelirdi; istenen temizlik ise cleavage
  dahil edilince de bire bir sağlanıyor (dokuz satır yine ikiye iniyor).
- **Zaten dondurulmuş örnek her koşulda listede kalır.** Ekranın üst kartı
  ("Dondurulmuş") aynı listeden besleniyor; süzgeç var olan bir kaydı
  görünmez yapardı. `vitrifikasyon` da bu yüzden `_DEGERLENDIRILMIS`'in
  içinde.

Ölçüm: cycle 17 (ivf_icsi) 9 → **2**; cycle 32 (ivf_icsi, gün 3 dondurma)
8 → **3** (üç embriyo da korundu); cycle 28/30 (`oosit_cryo`) 5 → 5 ve
16 → 16, yani hiç değişmedi.

### Yan etki: gün 3 embriyosu artık skorunu gösteriyor

Liste satırı yalnızca `bl_skor` okuyordu; cleavage'da dondurulan embriyoda o
alan boş olduğu için **her gün 3 embriyosu "değerlendirilmemiş" yazacaktı** —
kaydı olmayanı eleyen bir listede bu kendi kendisiyle çelişirdi.
`_vit_satiri()` artık sırayla bakıyor: blastokist skoru → cleavage'ın kendi
yazımı (`4HG2`, laboratuvarın notasyonu, v6.135'te resmî formlarda da bu) →
"değerlendirilmemiş".

`sqlite3.Row`'a alan eklenemediği için satırlar sözlüğe çevriliyor
(`cycle_listesi()`'nin zaten yaptığı şey).

**Bilinen, dokunulmayan durum:** v6.5 öncesi test kayıtlarında
`bl_genisleme` dolu ama `bl_skor` NULL (skor o zaman saklanmıyordu) —
o satırlar "değerlendirilmemiş" yazıyor. Yalnızca cycle 1-11'de var,
kullanıcının gerçek verisinde (15-34) hiç yok; `blast_skor()` bugün her
kayıtta skoru yazıyor.

## 2) Devam Eden Tedaviler: en yeni üstte

`cycle_listesi()`'nin yapılacaklar dalı **en eski OPU'yu** üste alıyordu ve
bu bilinçliydi (v6.28: "unutulan bir cycle listenin dibine düşüp gözden
kaybolmasın"). Kullanıcı tersini istedi — günlük iş en yeni hastada.
`ORDER BY COALESCE(opu_zamani, olusturma_zamani) DESC`.

Eski gerekçe tümden geçersiz değil: kart 5 satır gösteriyor (v6.78), yani
artık **en eskiler** kartın dışında kalıyor. Tamamı "Tümü" bağlantısındaki
`/devam-eden` sayfasında, o da aynı fonksiyondan besleniyor. Öteki listeler
(`/bitenler`, ay listesi, Yaklaşanlar) **değişmedi** — onlar zaten kendi
sıralarını kullanıyordu; ölçüldü.

## 3) Yumurta dondurmada "Dondurulacak yumurtalar"

Vitrifikasyon ekranı `oosit_cryo` ile paylaşılıyor ve iki kart başlığı
sabit "embriyo" diyordu (satırların kendisi zaten `ornek_adi()` ile doğru
kelimeyi basıyordu — yalnızca başlıklar unutulmuştu). İki yeni metin
anahtarı (`dondurulacak_yumurtalar`, `dondurulacak_yumurta_kalmadi`),
seçim Jinja global `yumurta_mi(c.cycle_tipi)` ile — karar zaten `db.py`'de
tek yerde (v6.135).

## Ölçüm

Ekrandan doğrulandı: `oosit_cryo` tedavisinde başlık "Dondurulacak
yumurtalar", satırlar "Yumurta 3/4/5"; hepsi dondurulmuşsa "Dondurulacak
yumurta kalmadı."; `ivf_icsi`'de ikisi de eskisi gibi "embriyo". Ana ekran
listesi 20.09 → 18.09 15:20 → 18.09 12:55 sırasında. 51 ekranlık genel
tarama temiz.

---

# v6.138 — taşıyıcı etiketi aranabilir oldu

Kullanıcının isteği: *"Vitrifikasyonda etiket kodu ile arama olsun. Ana
sayfadaki aramada o da aranabilsin."*

Etiket, tüpün üstünde yazan şey — vitrifikasyon ekranının ürettiği
`<tedavi no>-<SSDD>` (ya da elle yazılmış bir şey) ve laboratuvar genelinde
benzersiz. Elde tüp varken sorulan soru hep aynı: **bu kimin, içinde ne var,
nerede duruyor.** O soruyu cevaplayan tek yer `/cryo` haritasıydı; artık iki
yerden daha soruluyor.

## Tek sorgu, iki ekran

`app.etiket_ara(ara)` — `ornek_kodu_ara()`'nın (v6.35) taşıyıcı hali. İki
ekran da onu çağırıyor, ikinci bir sorgu yazılmadı; satır da tek yerde
(`templates/_etiketsonuc.html`, `_cyclesatir.html`'in gerekçesinin aynısı)
ki aynı şey iki ekranda aynı görünsün.

Satır: etiket · hasta adı ve dosya no · içerik ve konum. Gideceği yer
(`yol`) **sunucuda** kuruluyor, şablon kategoriye göre adres kurmuyor.

### Neden `durum` süzülmüyor

`/cryo` haritası `durum='dolu'` süzüyor — o bir **envanter** ekranı
("dolapta bugün ne var"). Bu ise hedefli bir **arama** ("bu etiket kimin").
Çözülmüş ya da başka bir tedavide kullanılmış bir tüpün etiketi arandığında
"yok" demek yanlış olurdu; bulunuyor, durumu rozetle söyleniyor. Örnek kodu
aramasının arşivlenmiş hastayı da bulmasıyla (v6.35) aynı gerekçe.

Rozet ikiye ayrıldı: `bosaltildi` → "boşaltıldı", `kullanildi` → "kullanıldı"
(v6.86: sperm başka bir tedaviye bağlandı — tüp duruyor, boşalmadı).
`tasiyici.html`'in eski tek rozeti olduğu gibi kaldı.

### Embriyo ve sperm birlikte

Etiket lab genelinde benzersiz ve elde tutulan tüpün hangi modüle ait olduğu
aranırken bilinmiyor olabilir. Hasta iki ayrı yoldan bulunuyor — embriyo
taşıyıcısında vitrifikasyon olayı üzerinden, sperm taşıyıcısında doğrudan
`sperm_dondurma.hasta_id` üzerinden — ikisi de **bağıntılı alt sorgu**
(`_ETIKET_HASTA`); JOIN yazılsaydı çok örnekli bir taşıyıcı satırı
çoğaltırdı. Sperm satırı `/sperm-dondurma/{id}`'ye, embriyo/yumurta satırı
`/cryo/tasiyici/{id}`'ye gidiyor.

`tr_buyuk()` **uygulanmıyor**: `etiket` büyük harfe sabitlenmiş bir alan
değil (v6.116'nın kuralı — yalnızca `ad_soyad` karşılaştıran parametre
büyütülür).

## 1) Vitrifikasyon ekranı

Kutu ekranın en üstünde, `?ara=` ile aynı rotaya GET.

- **Kendi formu; dondurma formunun içinde DEĞİL.** İçinde olsaydı arama
  kutusunda Enter'a basmak vitrifikasyonu kaydederdi. Ölçüldü: arama
  sonrası `tasiyici` sayısı değişmiyor, dondurma formu yerinde duruyor.
- **Bu tedaviyle sınırlı değil.** Aranan tüp çoğu zaman başka bir tedaviye
  ait; soru zaten "bu etiket kimin".
- **`cryo` izni yoksa kutu hiç basılmıyor** — sonuç satırı cryo sayfalarına
  gidiyor. Asıl engel her zamanki gibi middleware'de, bu yalnızca gizleme.
- Geri oku etkilenmiyor: aynı yol + farklı sorgu, v6.126'nın betiğinin (2)
  numaralı durumu — ok tedavi ekranına dönüyor.

## 2) Ana ekranın araması

Ana ekranın kutusu zaten `/hastalar`'a gönderiyor; etiket sonucu oraya,
örnek kodu kartının hemen altına eklendi — aynı gerekçeyle hasta
satırlarının üstünde: elde bir kod varsa aranan şey odur. Arşiv modunda da
çalışıyor, kutu orada da aynı kutu. `ara_ipucu` artık "Dosya no, ad, örnek
kodu veya etiket".

**Tire kapısı yok** (örnek kodunda var, v6.35). Orada gerekçe kodun
`<dosya no>-<specimen.id>` diye **birleştirilmesi**: tiresiz "3" bütün
örnekleri listelerdi. Etiket ise gerçek, kayıtlı bir alan — "1400" yazan
biri gerçekten etiketi 1400 içeren tüpleri arıyor. `/cryo`'nun etiket
araması da kapısız; sonuç 50 satırla sınırlı ve kart yalnızca eşleşme
varken basılıyor.

## Ölçüm

Playwright, 1440x1000 ve 390x844: vitrifikasyondan "1400" → 3 taşıyıcı,
doğru hastalar, `/cryo/tasiyici/…` bağlantıları; dondurma formu ve önerilen
etiket yerinde; "Aramayı temizle" ve geri ok doğru. Ana ekrandan
"2026-0025" → dört taşıyıcı, "4 yumurta" (v6.133'ün ayrımı çalışıyor),
"SP-700001" → sperm kaydı ve `/sperm-dondurma/1`. Bulunamayan etikette
"Bu etikete uyan taşıyıcı yok." 25 adres 200, JS hatası yok, hiçbir
genişlikte yatay taşma yok.

## "Vitrifikasyon ekranında çalışmıyor" — sebep: bayat süreç

Kullanıcı sürümü aldıktan sonra bildirdi: arama kutusu **görünüyordu**, ama
Enter'a basınca hiçbir şey olmuyordu — hata da yoktu.

Sebep kodda değildi: **Jinja şablonları diskten her istekte yeniden okunuyor
(`auto_reload` açık), `app.py` ise yalnızca açılışta.** `git pull` yapıp
programı yeniden başlatmayan bir makinede **yeni şablon + eski rota** çalışır.
Eski `vit_ekran()` `ara` parametresini ve `etiket_sonuc` context'ini vermiyor;
Jinja'da eksik değişken sessizce `Undefined` (yani `{% if ara %}` yanlış).
Sonuç tam olarak "kutu var, çalışmıyor, hata da yok".

Bire bir yeniden üretildi: v6.137'nin `app.py`'si + v6.138'in şablonları →
kutu var, sonuç 0, `/hastalar`'da kart hiç yok. Aynı anda HEAD → kutu var,
3 taşıyıcı, kart yerinde. Çözüm kullanıcı tarafında tek satır: `Ctrl+C`,
`python3 baslat.py`.

Kalıcı olarak yazıldı: `KOMUTLAR.md`'de "Kod güncelleme" ve "Sık sorunlar"
bölümlerine, `CLAUDE.md`'de tuzak #5'in kardeşi olarak. **Bir kullanıcı "yeni
şey görünüyor ama çalışmıyor" derse ilk sorulacak soru bu.**

### Yan karar: izin kapısı kaldırıldı

Kutu ilk yazışta `{% if yetkim("cryo") %}` ile gizleniyordu. Kaldırıldı:
`/hastalar`'daki aynı kart gizlenmiyor, ikisinin aynı davranması gerekiyor —
ve bu kapı, kutunun **sessizce hiç görünmemesi** demekti, yani yukarıdaki
sorunun bir başka kaynağı. İzni olmayan biri sonuç satırına basarsa
middleware onu döndürür; bu görünür bir cevap, sessiz bir yokluk değil.

---

# v6.139 — dejenere yumurta kilitleniyor, eşin dosya numarası

Kullanıcının dört isteği:

1. *"ICSI veya Fertilizasyon ekranında dejenere işaretlenen yumurta ileriki
   menülerde yumurtanın kutucuğunda Dej. kısaltmasıyla gösterilsin ve işlem
   yapılamasın. Yani cleavage ve Blast embriyo yazılamasın."*
2. *"ICSI de GV işlem yapılmadı yumurtaları ileride küçük kutucuğunda GV
   kısaltmasıyla gösterilsin."*
3. *"Hasta kartında Eşin dosya numarasının girilebileceği yer olsun. Eğer Eş
   erkek olarak sperm dondurma kayıt daha önce yapıldıysa uyarı versin."*
4. *"Hasta kartında tedaviye bağlama opsiyonu versin."*

## 1) Dejenere yumurta: görünür ama kilitli

Süzgeç `_DEJENERE`. **`specimen.durum`'a değil OLAY tablosuna bakıyor** ve bu
sürümün tek gerçek tasarım kararı bu: `durum` her aşamada **üzerine yazılıyor**
(`cleavage_kaydet()` `gun2` yazar, `vit_kaydet()` `dondurulmus`), yani dejenere
bir örneğe bir kez kayıt girilse `durum` artık `'degenere'` demezdi ve süzgeç
**sessizce** susardı. Olay kalıcı: ICSI'de `icsi_sonuc='degenere'` ya da
fertilizasyonda `fert_sonuc='degenere'` iptal edilene kadar duruyor.
`_ICSI_YAPILMADI`'nın (v6.105) "durum'a bakma" gerekçesinin başka bir yüzü.

- **Gizlenmiyor, kilitleniyor.** Kullanıcı "gösterilsin **ve** işlem
  yapılamasın" dedi. Gizlemek "o yumurta hiç yoktu" der gibi olurdu; oysa
  toplandı, enjekte edildi ve dejenere oldu — numarası da listede kalmalı.
- **Kutucukta `10-Dej.`** ve kutu `deg` sınıfını alıyor (kırmızı çerçeve,
  `.sn.deg` zaten vardı).
- **Form hiç basılmıyor**, yerine bilgi kartı: "Dejenere olduğu için bu
  yumurtaya embriyo kaydı girilmiyor." — v6.105'in fertilizasyondaki
  `icsi_yapilmadi_fert_form_yok` deseninin birebir aynısı.
- **Var olan kayıt dokunulmaz.** `{% elif sp.dejenere and not kayit %}` —
  daha önce girilmiş (ya da dejenere işaretinden önce girilmiş) bir kayıt
  varsa normal düzenleme/silme akışı bozulmuyor. Yoksa kullanıcı kendi
  verisine kilitlenirdi: yanlışlıkla dejenere işaretlenen bir embriyonun
  kaydı bir daha düzeltilemezdi.
- **Asıl engel sunucuda**: `_dejenere_engel()` yalnızca **yeni** bir
  değerlendirme açılmasını reddediyor (CLAUDE.md "ekranda göstermek yetmez").
  Ölçüldü: dejenere örneğe doğrudan POST atıldığında `olay` tablosuna hiçbir
  satır yazılmıyor, normal örnek etkilenmiyor.

## 2) Enjekte edilmeyen yumurta kendi maturasyonunu yazıyor

Fertilizasyon şeridi enjekte edilmeyen her yumurtaya `∅` basıyordu — hangisi
olduğunu söylemiyordu. Artık kendi değerlendirmesini yazıyor: **GV**, **MI**,
**Dej.**, **Atr.** Kullanıcının seçimi (soruldu): "Kendi maturasyonu".

`mat_kisa(kod)` Jinja global'ı: yalnızca uzun iki etiketin (`degenere`,
`atretik`) kısaltması `metinler.py`'de; MII/MI/GV kendi `liste_degeri`
etiketiyle basılıyor — liste laba özgü ve yönetici düzenleyebiliyor, burada
sabit bir sözlük yazmak CLAUDE.md'nin "kodu değil etiketi göster" kuralını
bozardı. ICSI şeridi de `|upper`'dan (ekranda "DEGENERE" yazıyordu) buna
geçti.

### v6.105 gevşetilmedi

Kullanıcıya soruldu — *"MI şu an nasılsa öyle kalsın. GV/Dej. kısaltmalarını
fertilizasyonda göster, sonra gösterme."* Yani ICSI'de **enjekte edilmeyen**
yumurtalar (GV / MI / atretik / enjekte edilmeden dejenere) cleavage ve
blastokistte **hâlâ hiç görünmüyor**. Kilitlenen ve "Dej." yazan grup,
enjekte edilip **sonra** dejenere olanlar ile fertilizasyonda dejenere
işaretlenenler — onlar zaten o ekranlarda görünüyordu, bugüne kadar
düzenlenebilir haldeydiler.

**Vitrifikasyon elden geçirilmedi, gerekmiyor**: v6.137'nin
`_DEGERLENDIRILMIS` süzgeci zaten cleavage/blastokist/vitrifikasyon kaydı
olmayan örneği eliyor — dejenere bir yumurtaya artık kayıt açılamadığı için
oraya hiç ulaşamıyor.

## 3) Eşin dosya numarası (`goc_045`)

v6.125 eşleştirmeyi **yalnızca dosya numarasıyla** yapıyordu ve bir durumu
bilerek kapsam dışı bırakmıştı: erkek hasta kendi **ayrı** dosya numarasıyla
kayıtlıysa (onkoloji öncesi sperm dondurma, çiftin dosyasından bağımsız)
numara tutmuyor, hiçbir uyarı çıkmıyordu. Yeni `hasta.es_dosya_no` tam bu
boşluğu kapatıyor.

- **FK değil, düz sayı.** Eş henüz kayıtlı olmayabilir (numara önce yazılır,
  kayıt sonra açılır) ve `hasta`'nın benzersizliği `UNIQUE (lab_id,
  dosya_no)` üzerinde — tek kolona FK verilemezdi. "Kayıtlı mı" sorusu her
  seferinde `dosya_no_sahibi()` ile yeniden soruluyor (türetilmiş,
  saklanmıyor).
- **Rakam olmayan değer NULL'a düşüyor**, reddedilmiyor: eş sonradan
  kaydedilebilir, formu bu yüzden bloke etmek yanlış olurdu.
- **Göç çalışmamışsa alan tümden yok sayılıyor** (`es_dosya_no_var()`) —
  `cycle_alanlari()`'nın (v6.33) aynı koruması. Yoksa göçü çalıştırmamış bir
  makinede **hasta açmak tümden bozulurdu** (tuzak #3'ün en pahalı hali).
- **Canlı uyarı aynı uç noktadan**: `/hasta/kontrol`, ikinci bir rota
  açılmadı (v6.125'in kuralı). Üç cevap veriyor: dondurulmuş spermi var
  ("Eşin kendi dosya numarasında 1 dondurulmuş sperm kaydı var" + kayda
  bağlantı), kayıtlı ama spermi yok (adı + bağlantı), hiç kayıtlı değil.
- Hasta kartında **ayrı bir kart**: "Eşin dondurulmuş spermi". Kendi
  kayıtlarıyla aynı kartta değil — bunlar **başka bir hasta kaydına** ait,
  sahiplik hep dondurmayı yaptıran kişide kalıyor.

## 4) Hasta kartından tedaviye bağlama

v6.86'dan beri bağlama yalnızca androloji ekranındaydı ve kayıt orada
**aranarak** bulunuyordu. Hasta kartında kayıt zaten gözün önünde; eksik olan
tek şey hangi tedaviye bağlanacağıydı.

- **Bağlama mantığı artık tek yerde**: `sperm_tedaviye_bagla()` /
  `sperm_baglanti_kaldir()`. Androloji rotaları da bunları çağırıyor —
  iki kopya olsaydı biri taşıyıcı durumunu güncellemeyi unuturdu.
- **Tedavi seçimi BU hastanın tedavileri arasından.** Başka bir hastanın
  tedavisine buradan bağlamak yanlış hasta riski taşırdı (CLAUDE.md'nin en
  pahalı hatası); o iş hâlâ androloji ekranının arama akışında.
- **Yalnızca androloji aşaması olan tipler seçilebiliyor**
  (`"androloji" in TIP_ASAMALARI[...]`). FET'e bağlanan bir sperm hiçbir
  ekranda görünmezdi — androloji kartı yalnızca `ivf_icsi`'de basılıyor.
  Koşul `TIP_ASAMALARI`'na bakıyor, tip adı elle yazılmıyor.
- **Bağlantıyı kaldırma yalnızca bağ BU hastanın tedavisindeyse** —
  androloji ekranındaki kuralın aynısı.
- Satır tasarımı tek yerde (`hasta_detay.html`'de `sperm_satiri()` makrosu),
  kendi kayıtları ve eşin kayıtları aynı görünsün diye. Form `<a>`'nın
  **içine** konamadı (iç içe etkileşimli öge), kardeşi olarak altına
  basılıyor — `/hastalar`'ın `.satirikili` gerekçesinin aynısı.

## Ölçüm

Gerçek veriyle (ağustos aktarımındaki bir `ivf_icsi` tedavisi: 15 yumurta, 1'i
enjekte edilip dejenere, 5'i MI/enjekte edilmedi):

| Ekran | Önce | Sonra |
|---|---|---|
| ICSI şeridi | `10-MII`, `11-MI` | aynı (uzun etiket artık kısaltılıyor) |
| Fertilizasyon | `10--`, `11-∅` | `10-Dej.`, `11-MI` |
| Cleavage / Blastokist | `10` düzenlenebilir | `10-Dej.`, form yok, uyarı var |
| Cleavage / Blastokist, MI'lar | görünmüyor | görünmüyor (değişmedi) |

Sunucu engeli ayrıca doğrulandı: dejenere örneğe doğrudan POST → hiçbir satır
yazılmıyor; normal örnek yazılabiliyor; fertilizasyonda dejenere işaretlenen
bir örneğin **var olan** cleavage kaydı korunuyor ve düzenlenebilir kalıyor.

Eş akışı uçtan uca: düzenleme formundan numara girildi → kart "Eşin
dondurulmuş spermi"ni gösterdi → "Tedaviye bağla" ile bağlandı (`tasiyici.
durum='kullanildi'`) → bağ androloji ekranında göründü → hasta kartından
kaldırıldı (`'dolu'`ya döndü). Yeni hasta formunda canlı uyarının üç hali de
doğru. 40 adres 200, masaüstü ve telefonda JS hatası yok.

**Bu sürümde düzeltilmeyen, ayrı bir sorun:** `/cycle/{id}/gebelik` ekranı
1280px'de yatay taşıyor (bir `.secenek` satırı sarmıyor). v6.138'de de
taşıyordu — ölçüldü, bu sürümün getirdiği bir gerileme değil, ayrıca
bildirildi.

---

# v6.140 — Gebelik ekranının yatay taşması

Kullanıcı v6.139'un sonunda bildirilen "bu sürümün getirmediği sorun"u
sordu: *"cycle/{id}/gebelik ekranı geniş ekranda yatay taşıyor dediğin nasıl
bir sorun anlamadım"*. Ekran görüntüsüyle gösterildi, sonra düzeltildi.

## Belirti

1280px'lik bir masaüstünde sayfa **2023px** genişliğinde oluyordu: altta yatay
kaydırma çubuğu, sağda kocaman boş bir alan, fare tekerleğiyle sayfa yana
kayabiliyor. **Hiçbir şey kesik değildi, veri kaybı yoktu** — kartların hepsi
okunuyordu; fazlalık 743px tamamen boştu. Telefonda (390px) hiç olmuyordu.

## Sebep — üç kuralın kesişimi

1. `gebelik.html`'de "Bebekler" kartındaki form `class="alan"` taşıyor.
2. `.alan input { width: 100% }` — normal metin kutuları boydan boya olsun diye.
3. `.secenek .sec input { position: absolute; opacity: 0 }` — Kız/Erkek/
   Belirtme düğmelerinin arkasındaki **gizli radyo**.

Gizli radyo da bir `input` olduğu için 2. kural ona da uyuyordu. `position:
absolute` ve üzerinde **konumlandırılmış bir ata olmadığı** için kapsayıcı
blok doğrudan görüntü alanı: "%100" = **ekranın tamamı**, yani 1280px. Üç
tanesi yan yana sayfayı 2023px'e uzatıyordu. Radyo görünmez ama **yer
kaplıyor** — görünmezlik `opacity: 0` ile, `display: none` ile değil (klavye
ve form gönderimi çalışsın diye, bilinçli).

Aynı ekrandaki öteki seçenek grupları (Var/Yok/Bilinmiyor, Pozitif/Negatif/
Bilinmiyor) `.alan`'ın **içinde olmadığı** için sağlamdı — sorun bu yüzden tek
bir kartta görünüyordu ve gözden kaçmıştı.

## Düzeltme

`static/style.css`, tek yer — bileşenin kendisi:

```css
.secenek .sec input {
  position: absolute; opacity: 0; pointer-events: none;
  width: auto; min-width: 0;
}
```

**Şablondaki `class="alan"`'ı kaldırmak da işe yarardı ama yanlış çözüm
olurdu**: yalnızca o ekranı kurtarır, aynı bileşen başka bir gün başka bir
`.alan`'ın içine konduğunda sorun sessizce geri gelirdi. Bileşeni her kaptan
bağımsız kılan yer gizli radyonun kendi kuralı.

## Ölçüm

| | önce | sonra |
|---|---|---|
| Sayfa genişliği (1280px ekran) | 2023px | **1280px** |
| Gizli radyonun genişliği | 1280px | **13px** |

`.secenek` kullanan **16 ekranın hepsi** masaüstü (1280x900) ve telefonda
(390x844) tarandı: hiçbirinde yatay taşma yok, hiçbir gizli radyo 30px'i
geçmiyor ve hepsi hâlâ görünmez (`opacity: 0`). Bileşenin işlevi de uçtan
uca doğrulandı (veritabanı kopyası üzerinde): etikete tıklamak radyoyu
seçiyor, kaydetmek `dogan_bebek.cinsiyet='kiz'` yazıyor, ekran dönüşünde
"Kız" seçili görünüyor. JS hatası yok.

**Tarayıcı önbelleği sorun çıkarmıyor**: `style.css` sürüm numarasıyla
bağlanıyor (v6.69, `statik_surum()` dosyanın `st_mtime`'ı) — kullanıcının
sert yenileme yapması gerekmiyor.

---

# v6.141 — temmuz 2026 Access kayıtları: kaynak etiketi ve bölünen işaret

Kullanıcının isteği: *"Şimdi daha önce son halini verdiğimiz eski kayıtları
programlamaya devam edelim. Bu da 2026 temmuz ayı hasta kayıtları. Bunu da
programa yerleştir."* — v6.130'un ağustos aktarımından sonra ikinci bir
Access dosyası.

Dosya aynı yapıda: tek tablo (`VERİTABANI`), kolon başlıkları ağustosunkiyle
**bire bir aynı**, 86 satır, hepsinin tarihi temmuz 2026. Yani
`aktar_access.py` dosyayı olduğu gibi okuyabiliyordu. Ama aktarım
denendiğinde iki ayrı hata çıktı; ikisi de **sessiz veri kaybı** üretiyordu,
o yüzden bu sürüm aslında aracın iki düzeltmesi.

## 1. Kayıt numaraları dosya başına 1'den başlıyor

`aktar_access.py` aynı satırı iki kez girmemek için her tedavinin protokol
notuna kaynağın kendi kayıt numarasını yazıyor (`[Access kaydı #12]`,
v6.130) ve o işareti taşıyan tedavi varsa satırı atlıyor. Bu, **tek bir
dosya** için doğru çalışıyordu.

İkinci dosyada çalışmıyor: her Access dosyası kendi kayıtlarını 1'den
numaralandırıyor. Ağustosun #1..#20'si programda dururken temmuz dosyası
aktarılsaydı, temmuzun #1..#20'si "zaten aktarılmış" sanılıp **sessizce
atlanacaktı** — 86 satırın 20'si, hiçbir hata vermeden. Ölçüldü: iki dosyada
20 numara çakışıyor.

**Çözüm: kaynak etiketi.**

```
python3 aktar_access.py liste kaynak=TEMMUZ temmuz.csv
python3 aktar_access.py       kaynak=TEMMUZ temmuz.csv
```

İşaret `[Access kaydı TEMMUZ#5]` oluyor; ağustosun `[Access kaydı #5]`'iyle
karışmıyor. Kapanış `]` sayesinde `#1]` deseni `#10]`'u da yakalamıyor,
yani numara sınırları da güvende.

**Ağustos etiketsiz kaldı ve öyle kalmalı.** `KAYNAK` boşken işaret
v6.130'daki haliyle basılıyor, yani bayt bayt aynı — ağustos dosyasını
yeniden çalıştırmak hâlâ 20 satırın 20'sini atlıyor (ölçüldü). Ağustosa
sonradan etiket verilirse o satırlar **yeniden** aktarılır; verme.

**Unutulursa betik duruyor, uyarıp devam etmiyor.** Etiket vermeyi unutmak
tam da yukarıdaki sessiz kaybı üretirdi. Ölçü hastanın dosya numarası:
gerçek bir yeniden çalıştırmada işaret **aynı** hastanın tedavisini bulur,
çakışmada **başkasınınkini**. Bulduğu tedavi başka hastanınsa betik hiçbir
şey yazmadan çıkıyor ve ne yapılacağını söylüyor:

```
DUR -- hicbir sey yazilmadi. 20 satirin kayit numarasi baska bir
aktarimin numarasiyla cakisiyor:
  #  2 dosya … -> isaret 2026-0002 tedavisini buluyor (dosya …, BASKA hasta)
  ...
  python3 aktar_access.py kaynak=<AD> temmuz.csv
```

Bu ölçünün tek boşluğu, çakışan iki kaydın **aynı** hastaya ait olması
(aynı çift, iki ayrı ayda tedavi). Bu dosya çiftinde öyle bir satır yok
(20 çakışmanın 20'sinde dosya no farklı), ama teorik olarak mümkün — asıl
koruma yine etiketin kendisi, bu yalnızca unutmaya karşı ağ.

## 2. `textwrap` işareti ortasından bölüyordu

Etiket eklenince ikinci bir hata ortaya çıktı, ve bu daha sinsiydi.

Protokol notu `textwrap.fill(..., 68)` ile sarılıyor (v6.130 — resmî formun
NOTLAR kutusu `white-space: pre`, uzun satır sarmıyor, sessizce kesiliyor).
İşaret cümlenin **sonuna** ekleniyordu, yani sarma onu ortasından bölebilir:

```
Program öncesi Access kaydından aktarıldı; yumurta kayıtları toplam
sayılardan üretildi, tek tek gözlem değildir. [Access kaydı
TEMMUZ#9]
```

Bölünmüş işareti `_zaten_var()`'ın `LIKE '%[Access kaydı TEMMUZ#9]%'` deseni
**bulamıyor**. Yani aktarım idempotent olmaktan çıkıyordu: betiği ikinci kez
çalıştırmak aynı tedavileri bir daha açacaktı. Ölçüldü: 86 satırın **60**'ında
işaret bölünüyordu.

Ağustosta olmamasının sebebi şans: etiketsiz işaret altı karakter kısa ve
satıra rastgele sığıyordu (20/20 sağlam, ölçüldü). Yani hata v6.130'dan beri
oradaydı, yalnızca tetiklenmemişti.

**Düzeltme iki katlı.**

- **İşaret kendi satırında.** `_not_kur()` onu artık cümleye eklemiyor, ayrı
  bir paragraf yapıyor — tek başına 68'in çok altında, hiçbir etiketle
  bölünemez. Not bir satır uzuyor: en uzun hâli sekiz satır (protokol +
  kaynağın notu + aktarım cümlesi + işaret + v6.104'ün iptal sebebi).
  Kutuyu taşırmıyor, ölçüldü — Playwright ile `scrollHeight == clientHeight`,
  86 tedavinin hiçbirinde kesik hücre yok.
- **Arama satır sonlarına dayanıklı.** Sorgu `REPLACE(...char(10), ' ')` ile
  satır sonlarını boşluğa katlıyor. Kemer + askı: notu elle düzenleyen ya da
  daha uzun bir etiket kullanan biri işareti yine bölerse arama tutmaya devam
  ediyor. Zaten yazılmış bölünmüş işaretleri de buluyor — denendi, bozuk
  aktarımın 86 satırının 86'sı bulundu, hiçbiri ikinci kez yazılmadı.

**Ders:** üretilmiş bir metnin içine gömülen bir işaret, o metni biçimleyen
her şeye bağımlıdır. Sarma genişliği, bir kelimenin uzunluğu, sonradan eklenen
bir cümle — hepsi işareti sessizce bölebilir. Makinenin okuyacağı işaret,
insanın okuyacağı metinden **ayrı bir satırda** dursun; arayan sorgu da
boşluk/satır sonu farklarına dayanıklı olsun.

## Aktarımın sonucu

Kopya bir veritabanında baştan sona denendi (kullanıcının makinesine
dokunulmadı):

| | |
|---|---|
| CSV satırı | 86 (hepsinin tarihi temmuz 2026, tarihsiz satır yok) |
| Tedavi tipi | 47 `ivf_icsi`, 26 `fet`, 13 `oosit_cryo` |
| Yazılan tedavi | 86 (0 atlandı, 0 hata) |
| Yeni hasta kartı | 83 |
| Var olan karta eklenen | 3 — ağustosta da tedavisi olan hastalar |
| Ağustos kayıtlarından değişen | **yok** (tedavi, protokol notu, durum, hasta adı — hepsi birebir aynı) |

Üç satır uyarı verdi (tedavi numaraları bu denemenin; gerçek
veritabanında o anki tedavi sayısına göre farklı olabilir — sabit olan
Access kayıt numarası):

```
Access #11  (2026-0039): notta 2 örnek yazıyor ama 0 uygun kayıt var
Access #33  (2026-0070): notta 1 örnek yazıyor ama 0 uygun kayıt var
Access #80  (2026-0107): notta 6 örnek yazıyor ama 5 uygun kayıt var
```

#11 ve #80'de kaynağın kendi sayıları tutmuyor (#11'de 2PN 0 ama notta
dondurulan iki embriyo var; #80'de 5 2PN, altı embriyo); araç fertilizasyon
kaydı olmayan bir örneğe dondurma yazmıyor ve bunu söylüyor.

> **#33 için yukarıdaki yorum YANLIŞTI — v6.142'de düzeltildi.** O satırda
> kaynak tutarlıydı; hata aracındı. Notta "OOSİT" kelimesi geçmediği için
> yumurta dondurmayı embriyo sandı ve 10 yumurtayı hiç yazmadı. Aynı
> "UYARI" satırı iki farklı şeyi (kaynağın tutarsızlığı / aracın yanlış
> okuması) aynı cümleyle söylüyordu; ayrım ancak notun kendisine bakınca
> ortaya çıktı.

Aktarım sonrası ekranlar açıldı (tuzak #5): ana ekran, `/hastalar`,
`/istatistik`, aktarılan üç tedavinin `/cycle/{id}` ekranı, Embriyoloji Özet
ve ART Lab formları (hem HTML hem Excel — üç `.xlsx` de geçerli ZIP).
Hiçbirinde hata yok.

## Dosyanın kendisi depoya girmiyor

v6.130'un kuralı: `.accdb` ve ondan üretilen CSV **gerçek hasta verisi**,
depoya girmiyor (`.gitignore`: `*.accdb`, `*.mdb`, `*.csv`). Bu dosyada da
öyle — README'ye, CLAUDE.md'ye ve commit mesajına hasta adı ya da dosya
numarası yazılmadı. Yukarıdaki tedavi numaraları (`2026-0039`) programın
kendi sıra numarası, hasta kimliği değil.

---

# v6.142 — yumurta dondurma notu embriyo sanılıyordu; FET'te yeniden dondurma

Kullanıcı temmuz dosyasını kendi veritabanına aktardı ("Tamamdır aktardı").
Aktarımın çıktısına son kez bakılırken v6.141'in "kaynağın sayıları
tutmuyor" dediği üç uyarıdan birinin aslında **aracın hatası** olduğu
görüldü.

## 1. "OOSİT" kelimesi olmayan yumurta notu embriyo sanılıyordu

Temmuzun #33 numaralı satırı bir yumurta dondurma tedavisi (`oosit_cryo`):
11 yumurta toplanmış, 10'u MII, notu:

```
2 TÜPTE 10 ADET (5*M2) (5*M2) ŞEKLİNDE DONDURULARAK SAKLANDI.
```

Kaynak tamamen tutarlı: 10 MII, iki tüpte beşer. Ama `_dondurma_coz()`
yumurta mı embriyo mu kararını **yalnızca nottaki kelimeye** bakarak
veriyordu (`"OOSIT" in cumle or "YUMURTA" in cumle`) ve bu notu yazan kişi
"OOSİT" kelimesini atlamış. Araç notu embriyo sandı, yumurta dondurma
tedavisinde 2PN'li örnek aradı, bulamadı, ilk tüpte durdu ve **10 yumurtayı
hiç yazmadı**: vitrifikasyon kaydı yok, taşıyıcı yok, Cryo Haritası o iki
tüpü göstermiyor. Verdiği uyarı ("notta 1 örnek yazıyor ama 0 uygun kayıt
var") kaynağın tutarsızlığını söyleyen uyarıyla aynı cümleydi, o yüzden
v6.141 onu da "kaynak tutmuyor" diye okudu.

**Çözüm: üç işaretten biri yeter.**
1. **Tedavinin tipi** — programın kendi kuralı `db.yumurta_mi(cycle_tipi)`.
   CLAUDE.md bu soru için "karar orada" diyor; araç ona hiç sormuyordu.
   Yapılandırılmış veri (tedavi tipi) serbest metinden önce gelir.
2. **Nottaki kelime** — eskisi gibi; `ivf_icsi`'de yumurta dondurulmuşsa
   (sperm yokken olabilir) tek işaret bu.
3. **Her öğe yumurta yazımı** (`N*M2`, `N*M1`) — MII/MI bir olgunluk
   derecesi, embriyo için hiç yazılmaz.

Karşılaştırma iki dosyanın **her** satırında eski ve yeni ayrıştırıcıyla
yapıldı: değişen tek satır temmuz #33 (`oosit_mi` False → True). Ağustosun
yedi dondurma notunun ve temmuzun öteki 51 notunun çözümü bire bir aynı —
hepsinde "OOSİT" yazıyordu ya da embriyo notuydu.

## 2. FET'te çözme sonrası yeniden dondurma yazılamıyor — artık söyleniyor

Temmuz #37 bir FET: 5 embriyo çözülmüş, 2'si transfer edilmiş, notu:

```
KÜLTÜRE EDİLEN TRANSFER FAZLASI 1 ADET D5 EMBRİYOSU (1CC) ŞEKLİNDE
DONDURULARAK SAKLANDI.
```

Yani bir embriyo tankta yeniden duruyor. **Programda bunun yeri yok**:
`fet`'in aşamaları çözme/transfer/gebelik, vitrifikasyon aşaması hiç yok
(`TIP_ASAMALARI`). Nasıl gösterileceği klinik bir karar — kullanıcıya
soruldu, cevap gelene kadar **yazılmıyor**.

Ama sessizce de geçilmiyordu ve asıl hata oydu: aktarım FET satırlarında
dondurma adımını hiç çağırmıyor, yani bu satır için **hiçbir şey
söylemiyordu**. `tamamla` ise çağırıyordu ve yanlış sebeple uyarıyordu
("OPU tarihi yok, dondurma kaydı yazılamadı"). İkisi aynı satır için iki
farklı şey söylüyordu. Artık:

- `_dondurma_kayitlari()` FET'te **hiçbir şeye dokunmadan** dönüyor ve
  `UYARI: çözme sonrası yeniden dondurma var (1CC) -- program bunu
  kaydedemiyor, tüp Cryo Haritası'nda görünmeyecek` diyor. Dönüş
  taşıyıcısız-vitrifikasyon iptalinden de önce — FET'in kayıtlarına
  hiçbir yoldan dokunulmuyor.
- Aktarım FET dalında da bu işlevi çağırıyor, yani aktarım ve `tamamla`
  aynı satır için aynı cümleyi söylüyor. FET dışı yolun yazma sırası
  **değişmedi** (bilerek: ağustostan beri doğrulanmış sıra).
- `liste` önizlemesi o satırın yanına `<- FET'te yeniden dondurma,
  YAZILMAYACAK` yazıyor — karar yazmadan önce görülsün.

İki dosyada bu durumdaki tek satır temmuz #37 (ağustosun yedi FET'inde
yeniden dondurma yok).

**Aynı ilkeyle üçüncü bir sessiz dönüş kapatıldı**: notta dondurma cümlesi
var ama skor parantezi yoksa ("3 ADET EMBRİYO DONDURULDU.") araç kaç
örnek/tüp olduğunu bilemiyor ve hiçbir şey yazmadan, **hiçbir şey
söylemeden** dönüyordu. Artık `UYARI: notta dondurma var ama kaç örnek/tüp
olduğu okunamadı -- dondurma kaydı yazılmadı` diyor, önizleme de o satırı
işaretliyor. Temmuz ve ağustosta böyle satır **yok** (ölçüldü), yani bugünkü
sonuçları değiştirmiyor; sonraki aylar için. Yeni dallar uydurma notlarla
ayrıca denendi (on durumun onu doğru) ve veritabanı yerine `None` verilerek
çağrıldı: erken dönen dalların hiçbir şeye dokunmadığı böyle gösterildi.

## Kullanıcının veritabanı nasıl onarılıyor

Aktarım zaten yapılmıştı, yani #33'ün tüpleri kullanıcının veritabanında
eksik. Onarım v6.132'nin `tamamla` kipiyle — baştan aktarmadan, yalnızca
eksiği ekleyerek:

```
python3 aktar_access.py tamamla kaynak=TEMMUZ temmuz.csv
```

Hatalı aktarımın bire bir kopyası üzerinde denendi, **her tablo satır satır**
karşılaştırıldı:

| | |
|---|---|
| Eklenen taşıyıcı | 2 (`<tedavi no>-1400`, `-1401`, konum boş) |
| Eklenen vitrifikasyon olayı | 10, hepsi #33'ün tedavisinde |
| Değişen örnek | 10 yumurta, `durum`: `oosit` → `dondurulmus` |
| Başka herhangi bir tablo/satır | **değişmedi** |
| İkinci `tamamla` + ağustosa `tamamla` | **hiçbir şey değişmedi** (idempotent) |

Ayrıca **temiz kopyaya yeni kodla sıfırdan aktarım** yapılıp onarılmış
hâlle tedavi tedavi karşılaştırıldı (kimlikten bağımsız: tip, durum,
protokol notu, örnek durumları, her olayın skoru/saati/tüp etiketi, işlemi
yapan, taşıyıcılar, hastalar): 120 tedavinin hiçbiri farklı değil. Yani
onarılan veritabanı, en baştan doğru aktarılsaydı olacağı hâlle aynı.

Ekranlar açıldı (tuzak #5): Cryo Haritası iki tüpü "5 yumurta" diye
gösteriyor; vitrifikasyon ekranında "Dondurulmuş (10)", tüp etiketleri
kartlarda — eski kodun doğru aktardığı başka bir yumurta dondurma
tedavisiyle (#53, beş tüp) aynı görünüm; Embriyoloji Özet'in NOTLAR
kutusunda `Dondurulan: 10 yumurta, 2 tüp: (5) (5)`, kesik değil.

**`tamamla` hemen çalıştırılmalı.** `_dondurma_kayitlari()` var olan
değerlendirmeyi nottaki değerle güncelliyor (v6.132'nin tasarımı): kullanıcı
aktarılan bir temmuz embriyosunun skorunu ekranda elle düzeltirse, sonra
çalışan `tamamla` o düzeltmeyi nottakiyle ezer. Aktarımdan hemen sonra bu
risk yok — bu denemede 85 satırın hiçbirinde tek alan değişmedi.

## Ders

**Aynı uyarı cümlesi iki farklı sebebi taşıyorsa, uyarıyı okuyan sebebi
ayırt edemez.** "Notta N örnek yazıyor ama M uygun kayıt var" hem "kaynak
kendi içinde tutarsız" (#11, #80) hem "araç notu yanlış okudu" (#33)
demekti; ayrım ancak notun kendisine bakınca çıktı. Bir uyarıya sonuç
bağlamadan önce kaynağına bak.

**Serbest metinden bir klinik kategori çıkarırken yapılandırılmış veriye
önce sor.** Tedavi tipi zaten "yumurta dondurma" diyordu; araç ona değil,
personelin not yazarken kullanıp kullanmadığı bir kelimeye güveniyordu.

---

# v6.143 — çözülen embriyo aynı FET'te yeniden dondurulabiliyor

Kullanıcının isteği: *"Programa ekleyelim. Çözülen embriyo aynı FET
tedavisinde yeniden dondurulabilsin ve tüp Cryo Haritası'na girsin."*
v6.142'de temmuz Access kayıtlarından biri (#37) bunu anlatıyordu —
"KÜLTÜRE EDİLEN TRANSFER FAZLASI 1 ADET D5 EMBRİYOSU (1CC) ŞEKLİNDE
DONDURULARAK SAKLANDI" — ve programda karşılığı yoktu: FET'in aşamaları
çözme/transfer/gebelik, vitrifikasyon hiç yok. Soru yalnızca aktarımın değildi:
laboratuvar çözüp yeniden dondurduğunda bunu bugün programa hiç giremiyordu.

## Asıl iş: "örnek başına tek dondurma, tek çözme" varsayımı

FET'e bir vitrifikasyon ekranı eklemek kolaydı; zor olan, programın her
yerinde duran bir varsayımdı. `olay_kaydet_veya_guncelle()` aynı tipte kayıt
varsa onu **güncelliyor** — dondurma da çözme de böyle yazılıyordu. Yeniden
dondurma eklenip bu varsayım bırakılsaydı:

- yeniden dondurma **ilk dondurmanın üzerine yazardı** (tüp A'nın kaydı B'ye
  dönüşür, A'nın geçmişi kaybolurdu);
- yeniden dondurulan embriyo ileride tekrar çözülünce **ikinci çözme ilk
  FET'in çözme kaydını ezerdi** — ilk FET'in "çözülen embriyo" sayısı, resmî
  formu, çözme listesi sessizce değişirdi;
- tüp B'nin sayfası tüp A'dan yapılan çözmeyi "bu tüp çözüldü" diye gösterirdi
  (çözme kaydı hangi tüpten yapıldığını bilmiyordu);
- FET'in çözme listesinde embriyo **iki kez** görünürdü (iki dondurmasıyla
  birleşiyordu);
- Cryo Excel'i dolu tüp B için "Dolapta: Hayır" derdi;
- resmî formlarda tüp B, kaynak ICSI tedavisinin formuna **o tedavide
  dondurulmuş gibi** yazılırdı; FET'in kendi formunda hiç görünmezdi;
- ay listesinin "Donan" sütunu yeniden dondurmayı kaynak tedaviye yazardı.

## İki yeni alan (`goc_046`)

- **`olay.vit_cycle_id`** — bu dondurma **hangi tedavide yapıldı**. Boşsa
  örneğin kendi tedavisi (bugüne kadarki bütün dondurmalar). `thaw_cycle_id`
  ve `tr_cycle_id`'nin deseni: `olay.cycle_id` her zaman örneğin KENDİ
  tedavisi kalıyor. SQL ifadesi tek yerde: `db.vit_tedavisi()`
  (`COALESCE(vit_cycle_id, cycle_id)`) — `formlar.py` ve `disari.py` de
  soruyor, `app`'i import edemiyorlar; `FET_TIPLERI` ile aynı gerekçe.
- **`olay.thaw_tasiyici_id`** — bu çözme **hangi tüpü boşalttı**. Göç var
  olan çözmelere, o çözmeden ÖNCE açılmış dondurmanın tüpünü yazıyor (kimlik
  sırası; saat elle geri tarihlenebildiği için ona bakılmıyor). Denendi:
  çözmeden sonra dondurması iptal edilip başka tüpe yazılmış bir örnekte doğru
  tüp (çözmeden önceki) seçildi. Dondurması programda olmayan program öncesi
  FET embriyolarının çözmesi boş kalıyor — tüpü gerçekten bilinmiyor.
- İlk yazışta göç patladı: SQLite alt sorgunun `ORDER BY`'ında dıştaki
  tabloyu görmüyor (`no such column: olay.id`); `WHERE`'de görüyor. İki adıma
  bölündü. Yarım kalan göç (kolonlar eklenmiş, doldurma yapılmamış) yeniden
  çalışınca tamamlandı — idempotent.
- Göç çalışmamışsa (tuzak #3) her şey eski davranışla çalışıyor, FET'in
  vitrifikasyon ekranı göç uyarısı basıyor: `db.kolon_var()`,
  `db.cozme_tupu_var()`, `db.yeniden_dondurma_var()`.

`olay_kaydet_veya_guncelle()`'ye `ek_kosul`/`ek_deger` eklendi: aynı tipte
birden çok kaydı olabilen olaylar için hangisinin güncelleneceği. Vitrifikasyon
**bu tedavide yapılan** dondurmayı günceller (aynı tedavide başka tüpe taşıma
eski davranış), çözme **bu tüpten yapılan** çözmeyi. Verilmezse eski davranış.

## Ekranlar

- **FET ve FET (3→5 kültür)'e vitrifikasyon aşaması** — transferden sonra
  (`TIP_ASAMALARI`): dondurulan şey transferin fazlası. Liste
  `_FET_DONDURULABILIR`: bu tedavi için çözülüp dejenere çıkmayan (kısmi hasar
  listede — laboratuvar onu transfere de uygun sayıyor, karar embriyoloğun),
  transfer edilmemiş embriyolar; bu tedavide zaten yeniden dondurulmuş olanlar
  da, sonradan başka bir FET'te transfer edilseler bile üst kartta kalıyor.
  Satırda kaynak tedavinin numarası: liste birden çok kaynaktan gelebilir,
  `cycle_sira_no` yalnızca kendi tedavisinde tekil (v6.62). Sunucu aynı
  koşulla doğruluyor.
- **Taşıyıcı sayfası** çözme özetini artık **bu tüpten** yapılan çözmelerden
  hesaplıyor; tüpten çözülüp başka tüpe dondurulan embriyonun satırında
  "Yeniden donduruldu: <tüp>" bağlantısı (şu anki tüpü). Geçmiş iki yönden
  izlenebiliyor.
- **Tedavinin çözme ekranı** satırın tüpünü çözmenin kendi tüpünden alıyor
  (embriyo iki kez listelenmiyor), "transfer edildi" yalnızca **bu** tedavideki
  transfer. Vitrifikasyon ekranına bağlantı tipin o aşaması varsa
  (`TIP_ASAMALARI`'dan, FET adını elle yazmadan).
- **Yumurta dondurma, normal ICSI dondurması değişmedi** — denendi: aynı
  tedavide başka tüpe taşıma aynı kaydı güncelliyor, geri alma eski durumuna
  ("blastokist") döndürüyor, adressiz eski "geri al" bağlantısı çalışıyor.

## Geri alma: önce en son adım

Bir örneğin geçmişi artık bir dizi (dondur A → çöz A → dondur B → çöz B), ve
ortadan bir adım silinirse dizi kendi içinde çelişir. Kural: **önce en son
adım geri alınır.**

- Çözülmüş bir tüpün dondurması geri alınamıyor — "hiç dondurulmadı" demek
  olurdu ama çözme kaydı duruyor. Önce çözme geri alınmalı.
- Çözmeden sonra yeniden dondurma varsa çözme geri alınamıyor.
- Dondurmayı geri alma bağlantısı ekranın tedavisini taşıyor
  (`/specimen/{id}/vit-sil?cycle=N`): ICSI ekranından basılan ilk tüpü, FET
  ekranından basılan yeniden dondurmayı bulur. Yeniden dondurma geri alınınca
  embriyo **o tedavideki çözülmüş hâline** döner (canlı → "çözüldü", kısmi
  hasar → "kısmi hasar"); ölçü "bu dondurmadan önce açılmış bir çözme var mı"
  — "kaynak tedaviden farklı bir FET mi" değil, çünkü program öncesi FET
  embriyolarının kendi tedavisi zaten o FET (ilk yazışta bu yüzden yanlıştı,
  denemeden önce düzeltildi).
- Aynı kural kayıt tarafında da var: eski bir sekmedeki form, bu arada
  dondurulup çözülmüş bir örneği gönderirse **reddediliyor** — yoksa kayıt
  yeni tüpe taşınır, çözmenin tüpü içeriksiz kalırdı.
- Engel ekranda açık bir mesaj ve taşıyıcıya bağlantı; sunucu da reddediyor.
- **Değişmeyen karar:** çözmeyi geri almak tüpü haritaya geri koymuyor.
  `thaw_sil.html` bunu zaten söylüyor ("Taşıyıcı boşaltıldı durumunda kalır…
  Fiziksel olarak geri koyduysan yeni bir vitrifikasyon kaydı girilmelidir");
  ilk bakışta hata sanıldı, bilinçli olduğu görüldü, dokunulmadı.

## Resmî formlar ve Excel

- `formlar.dondurma_tupleri()` dondurmanın **yapıldığı** tedaviye bakıyor:
  FET'in Özet NOTLAR'ı ve ART Lab FREEZE'i yeniden dondurmayı gösteriyor
  (denendi: "Dondurulan: 2 embriyo, 3. gün, 2 tüp: (8HG1) (9HG2)"), kaynak
  ICSI'nin formu yalnızca kendi dondurmasını ("7 embriyo, 2 tüp" — değişmedi).
  ART Lab'ın yumurta sütunundaki dondurma saati de o tedavinin dondurması.
- Ay listesinin "Donan"ı yapıldığı tedaviye (FET'te 2, kaynak ICSI'de 7,
  değişmedi) — "Çözülen" ve "Transfer" zaten öyleydi.
- Cryo Excel'inde her satır bir dondurma, çözme sütunu **o tüpten** yapılan
  çözme: tüp B'nin satırı kendi çözmesini (01.10), A'nın satırları FET1'inkini
  (20.09) gösteriyor; "Dolapta" doğru.
- `formlar.son_alt()`'a `ek` koşulu eklendi (`disari.py` de oradan alıyor).
- **İstatistikteki "Donan" değişmedi**: `COUNT(DISTINCT specimen)` — yeniden
  dondurulan embriyo kaynak tedavisinde zaten sayılmıştı, bir kez daha
  sayılmıyor.

## Kalıcı silme (tuzak #4)

`vit_cycle_id` başka bir tedaviye işaret edebildiği için FET kalıcı
silinirken bağ koparılıyor (`thaw_cycle_id`'nin aynısı): kayıt kalıyor —
tüp tankta, silmek onu haritadan düşürürdü — yalnızca hangi tedavide
dondurulduğu bilinmez oluyor. Tüp silinmeden önce ona işaret eden
`thaw_tasiyici_id` de boşaltılıyor. `teshis_silme.py` de biliyor. Denendi:
yeniden dondurmalı, transfersiz bir FET kalıcı silindi, FOREIGN KEY hatası
yok, `PRAGMA foreign_key_check` temiz, tüp dolu kaldı.

## Aktarım aracı: #37 artık yazılıyor

v6.142'nin "program bunu kaydedemiyor" uyarısı yerine gerçek kayıt: bu FET'te
çözülüp transfer edilmeyen ilk embriyoya nottaki skor (1CC, gün 5), bir tüp ve
`vit_cycle_id`'si bu FET olan bir dondurma. Tarih: kaynak kayıtta yalnızca
transfer günü var, kültürün kaçıncı güne sürdüğü yazmıyor — değerlendirme ve
dondurma o güne, transferden sonraya yazılıyor (program öncesi kayıtların
bütün saatleri gibi yaklaşık).

- **Araç göçü kendisi çalıştırmıyor**; göç yoksa hiçbir şey yazmadan
  duruyor ("programı bir kez kapatıp aç"). Yoksa FET satırı işlemin ortasında
  patlardı.
- Kullanıcının veritabanı iki hâlde olabilir, ikisi de denendi: v6.142'nin
  `tamamla`'sı çalışmadıysa #33'ün 10 yumurtası ve #37 birlikte ekleniyor;
  çalıştıysa yalnızca #37. Her iki durumda başka hiçbir satır değişmiyor,
  ikinci çalıştırma hiçbir şey yapmıyor. Sıfırdan aktarım onarılmış hâlle
  (yeni kolonlar dahil) birebir aynı. Uyarı sayısı üçten ikiye indi (#11, #80).

## Uçtan uca deneme

Onarılmış kopyada, program kendi ekranlarının formlarıyla sürüldü (49 kontrol):
ICSI'de dört embriyolu bir tüp → FET1 için çözme (canlı, canlı, kısmi hasar,
dejenere) → biri transfer → vitrifikasyon adayları yalnızca kalan ikisi →
yeni tüpe yeniden dondurma → Cryo Haritası, taşıyıcı sayfaları, iki tedavinin
vitrifikasyon ve çözme ekranları, formlar ve Excel → geri alma sırası (dört
engel ve bir izinli geri alma) → FET2'de yeni tüpün tekrar çözülüp transferi:
FET1'in çözmesi ezilmedi, FET1'in sayfaları değişmedi. Masaüstü ve telefonda
beş ekran: yatay taşma yok.

## Yan yolda bulunanlar

- **Düzeltildi:** vitrifikasyon kaydı seçilen örnekler doğrulanmadan önce
  taşıyıcıyı açıyordu — hiçbiri uygun değilse Cryo Haritası'nda içi boş bir
  "dolu" tüp kalırdı. Artık önce doğrulama.
- **Düzeltildi:** taşıyıcı sayfası embriyolar için "yumurta 5" yazıyordu
  (`oosit_n` v6.134'ten beri "Yumurta N" döndürüyor); artık `ornek_adi()`.
- **Düzeltilmedi, kapsam dışı:** zaman çizelgesi (`formlar._olay_ilk()`)
  saatleri örneğin **kaynak** tedavisinden topluyor. FET'in çizelgesi boş
  (çözme/transfer yok), kaynak ICSI'nin çizelgesinde FET'in çözme ve transferi
  görünüyor. Bu sürümden önce de böyleydi; yeniden dondurma durumu
  kötüleştirmiyor (ICSI'nin dondurma satırı en erken saati alıyor, ilk
  dondurma). Ayrı bir iş olarak önerildi.
- `yumurta_cozme` (çözülen yumurta) yeniden dondurmaya açılmadı — istek
  embriyo içindi.

---

# v6.144 — hastanın tedavileri tarih sırasıyla numaralanıyor

Kullanıcının isteği: *"sonradan eklenen hasta kayıtlarında işlem tarihi yeni
olan son tedavi olarak eklensin. Bir daha aynı hastaya eski tedavi kaydı
eklenirse tarih sırasına göre en eski tedavi 1. tedavi olarak eklensin. Bu
daha sonra hep uygulansın."*

"Kaçıncı tedavi" (`hasta_cycle_no`) tedavi açılırken "hastanın en yüksek
numarası + 1" diye veriliyordu: yeni açılan tedavinin hep en yenisi olduğu
varsayımı. v0.8'in niyeti aslında tarih sırasıydı (`goc_005` var olan
kayıtları OPU/hCG zamanına göre numaralamıştı); "+1" yalnızca bir kısayoldu.
Program öncesi Access kayıtları onu bozdu: temmuz dosyası ağustostan SONRA
aktarıldı (v6.141). Kopyada ölçüldü: iki ayda da tedavisi olan üç hastanın
temmuz tedavisi "2. tedavi", ağustos tedavisi "1. tedavi" idi.

## Kural

- **Tedavinin günü** `db.tedavi_tarihi()`: yumurta toplanan tedavide OPU,
  yoksa hCG; FET'te çözme ya da transfer (`thaw_cycle_id`/`tr_cycle_id` —
  `olay.cycle_id` örneğin kendi tedavisi); hiçbiri yoksa planlanan tarih, o da
  yoksa kaydın açıldığı an. Aktarılan eski kayıtlarda açılış anı zaten
  tedavinin tarihine çekili (v6.130). Yalnızca gün karşılaştırılıyor.
- **Programın verdiği numara bir önceki tedavininkinin bir fazlası**, ilk
  tedavi 1 — kullanıcının istediği bu.
- **Elle yazılan numara korunur** (`cycle.hasta_cycle_no_elle`). v0.8'den beri
  kutu elle değiştirilebiliyor: "hasta başka merkezde tedavi görmüşse gerçek
  deneme sayısını girersin". Bir önceki tedavinin numarasından büyükse
  tutuluyor; değilse tarih sırası kazanıyor. Elle yazılan değer silinmiyor:
  çakışma kalkınca (önceki tedavinin tarihi düzeltildi, yanlış açılan tedavi
  silindi) numara ona dönüyor.
- **Neden ayrı bir kolon.** İki gerçek durum var:
  1. Hasta başka merkezde iki deneme yapmış; ilk tedaviye 3 yazılmış.
  2. Embriyolog programdaki eylül tedavisine temmuz ve ağustosu sayarak 3
     yazmış, o kayıtlar sonradan Access'ten aktarılmış.

  "İlk tedavinin numarasını koru" kuralı (2)'de temmuzu 3., ağustosu 4.,
  eylülü 5. yapardı — aynı iki tedavi iki kez sayılır. "Hep 1'den başla"
  kuralı (1)'i silerdi. Elle yazılanı o tedavinin kendi bilgisi saymak ikisini
  de doğru çözüyor; ikisi de denendi. Bedeli: elle yazılmış bir numaranın
  önünde boşluk kalabiliyor (1., 3., 4. — aradaki 2. başka merkezdeki deneme).
  Gerçek veride hiç elle yazılmış numara bulunmadı.
- Kural tek yerde: `db.tedavileri_sirala()`. Program, aktarım aracı ve göç aynı
  işlevi çağırıyor.

## Nerede uygulanıyor

- **Tedavi formu** (açma ve düzenleme): kaydetmek ve numaralamak tek işlem.
  Elle yazılan numara tarih sırasıyla bağdaşmazsa hiçbir şey kaydedilmiyor,
  form yazılanlarla geri geliyor: *"Kaçıncı tedavi 2 olamaz: tarih sırasına
  göre bu tedaviden önce gelen tedavi hastanın 4. tedavisi. En az 5 yaz ya da
  kutuyu boş bırak…"*. Hangisi elle yazılmış:
  - yeni tedavide kutudaki değer programın önerisinden farklıysa (öneri gizli
    alanda da gidiyor; iki kişi aynı anda tedavi açarsa bayat öneri elle
    yazılmış sanılmasın diye);
  - düzenlemede kutudaki değer bugünkü numaradan farklıysa.

  Boş kutu tarih sırası demek. Düzenleme ekranı elle yazılmış numarayı
  söylüyor.
- **OPU ekranı, çözme ve transfer (kayıt ve geri alma), kalıcı silme**:
  `tedavi_sirasini_duzelt()` çağırılıyor. Numara türetilmiş bir bilgi.
  Güncellenemezse asıl kayıt geri alınmıyor, sebep günlüğe yazılıyor, bir
  sonraki kayıtta düzeliyor.
- **Kayan her numara değişiklik geçmişine yazılıyor** (`hasta_cycle_no 1 → 2`)
  — "bu tedavi neden 2. oldu" sorusunun cevabı orada.
- **Aktarım aracı** her satırın sonunda numaralıyor. Rapor satırı *"hastanın
  1. tedavisi — tarih sırasına göre kayanlar: 2026-0xxx 1.→2."* diyor. Göç
  yoksa araç hiçbir şey yazmadan duruyor: yoksa eski tedavi eski kuralla
  "en yüksek + 1" alırdı.
- **Lab kayıt no (2026-0xxx) değişmiyor.** Tüp etiketinde, örnek kodunda ve
  arşiv klasöründe yazıyor.

## goc_047

- `cycle.hasta_cycle_no_elle` kolonunu ekliyor.
- Kolon ilk eklendiğinde eski elle yazılanları buluyor. Program numarayı
  açılışta "o ana kadarki en yüksek + 1" diye öneriyordu; tedaviler açılış
  sırasıyla (kimlik) dizildiğinde bu kurala uymayan numara elle yazılmıştır.
  Sonraki çalıştırmalarda bu kural uygulanmıyor: numaralar artık tarih
  sırasında, açılış sırasına bakmak onları elle yazılmış sanırdı.
- Silinmiş bir tedavinin bıraktığı boşluk da kurala uymuyor ve elle yazılmış
  sayılıyor. O numara bugünkü haliyle kalıyor; bu sürümden önce de öyleydi.
- Sonra her hastayı numaralıyor. İdempotent.
- **Göç çalışmamışsa eski davranış** (tuzak #3): `db.tedavileri_sirala()`
  hiçbir şeye dokunmuyor. Elle yazılanı ayırt edemeden sıralamak onu ezerdi.
- **Tedavi formu kolonun varlığını saklamıyor** (`_elle_no_kolonu_var()`,
  `_planlanan_kolonu_var()`'ın deseni). Yedekten geri yüklenen eski bir
  veritabanında kolon yok ve göçler ancak program yeniden açılınca çalışıyor.
  Saklanmış bir "var" cevabı o arada tedavi açmayı "no such column" ile
  bozardı. Denendi.

## Deneme

- **Göç, temmuz aktarımından sonraki kopyada:** 3 hastanın 6 tedavisi yeniden
  numaralandı, başka hiçbir şey değişmedi. İkinci çalıştırma hiçbir şey
  yapmadı. Program açılışta göçü kendisi uyguladı.
- **Aktarım aracı gerçek sırayla:** ağustos kopyasına temmuz aktarıldı.
  - Üç hastanın rapor satırında "kayanlar" çıktı.
  - Sonuç, göçün sonucuyla 120 tedavide birebir aynı.
  - İkinci çalıştırma her satırı atladı.
  - Göçten önce araç çıkış kodu 1 ile durdu, hiçbir şey yazmadı.
- **Dokuz yapay vaka:**
  - başka merkezdeki denemeler için elle yazılmış numara;
  - silinmiş tedavinin boşluğu;
  - aynı numara iki kez;
  - boş numara;
  - bildirilen durum (ağustos önce aktarılmış);
  - Access kayıtlarını zaten sayan elle numara (çift sayım yok);
  - elle numaradan sonra iki eski kayıt (tarih sırası kazanıyor, elle yazılan
    saklanıyor);
  - FET'in geriye tarihli çözmesi;
  - planlanan tarih.
- **Programın kendi ekranlarıyla 42 kontrol:**
  - eski tedavinin araya girmesi ve geçmişe yazılması;
  - elle numaranın reddi (hiçbir şey kaydedilmedi, kutu yerinde) ve kabulü;
  - sonraki önerinin ondan devam etmesi;
  - kutuyu boşaltma;
  - düzenleme formunda OPU tarihini değiştirme;
  - düzenlemede elle numara, reddi ve tarihle birlikte kabulü;
  - OPU ekranı;
  - FET'te geriye tarihli çözmenin tedaviyi araya alması; transfer ve geri
    almalar; çözme geri alınınca tedavinin en sona dönmesi;
  - kalıcı silme;
  - resmî formun "Önceki tedavi sayısı".
- **Göç yokken** numaralar eski kuralla kaldı, ekranlar hatasız açıldı.
- **Çalışan programda eski bir yedek geri yüklenince** tedavi açma bozulmadı.
- **26 adres ve Excel çıktıları** 200 döndü, JS hatası yok. Telefon ve
  masaüstünde yatay taşma yok.

## Yan yolda bulunan

- **Düzeltilmedi, önceden vardı:** yedekten geri yüklemeden sonra göçler
  çalışmıyor, ve programın kolon kontrollerinin çoğu cevabı saklıyor
  (`db.kolon_var()`, `thaw_cycle_var()`, `opu_hekim_var()`).
  - Denendi: çalışan programa v6.143 öncesi bir yedek geri yüklenince FET'in
    vitrifikasyon ekranı, program yeniden açılana kadar `no such column:
    o.vit_cycle_id` ile 500 veriyor.
  - Geçici çözüm: geri yüklemeden sonra programı bir kez kapatıp açmak.
  - Kalıcı çözüm geri yüklemenin ardından göçleri çalıştırıp saklanmış
    cevapları unutmak olur. Ayrı iş.

---

# v6.145 — geri yüklemeden sonra güncellemeler kendiliğinden

Kullanıcının isteği: *"Geri yüklemeden sonra da kendisi yapsın."* v6.144'te
bulunmuştu: çalışan programa eski bir yedek geri yüklenince, program yeniden
açılana kadar yeni kolonlara dayanan ekranlar hata veriyordu (v6.143 öncesi
bir yedekte FET'in vitrifikasyon ekranı `no such column: o.vit_cycle_id` ile
500). İki ayrı eksik vardı:

1. **Göçler yalnızca açılışta çalışıyordu.** Geri yüklenen yedeğin eksik
   güncellemeleri ancak bir sonraki açılışta uygulanıyordu.
2. **Program şema cevaplarını saklıyordu.** "Bu kolon var mı" sorusunun ilk
   cevabı yedi ayrı yerde tutuluyordu: `db.kolon_var()` ve `app.py`'de altı
   değişken. Saklanmış "var" cevabı, kolonu olmayan veritabanında sorguyu
   patlatıyordu.

## Ne değişti

- **`geri_yukle.geri_yukle()` takastan hemen sonra göçleri çalıştırıyor**
  (`_gocleri_uygula()`). Çalıştırıcı açılıştakinin aynısı: `goc.calistir()`,
  süreç içinde. Ekrandan ve terminalden (`geri_yukle.py`) geri yükleme aynı
  işlevden geçiyor.
- **Saklanmış cevaplar tek yerde.** `yetki_tablosu_var()`,
  `sifre_istegi_tablosu_var()`, `es_dosya_no_var()`, `thaw_cycle_var()` ve
  `opu_hekim_var()` artık kendi değişkenlerinde değil, `db.kolon_var()` ve
  yeni `db.tablo_var()`'da saklıyor. `db.sema_bilgisini_unut()` hepsini
  unutturuyor. Beş değişkeni tek tek sıfırlamak da olurdu, ama ileride
  eklenecek altıncısı unutulurdu (tuzak #4'ün deseni). Tek kalan ayrı
  saklama tazelemenin tablo listesi; onu `veritabani_yenilendi()`
  unutturuyor.
- **Ekran söylüyor:** *"Geri yüklendi: … Yedek eski bir sürümdendi: 2
  veritabanı güncellemesi hemen uygulandı, programı yeniden açmana gerek
  yok."* Uygulanacak güncelleme yoksa bu cümle çıkmıyor. Yönetici panelinin
  göç kartı en son çalışmayı gösteriyor: "Son geri yüklemede N güncelleme
  uygulandı." `yedek.log` hangi güncellemelerin uygulandığını yazıyor.
- **Bir göç patlarsa** geri yükleme yine tamam sayılıyor: yedek yerinde,
  önceki hâlin kopyası duruyor. Mesaj ve panel hatayı gösteriyor; açılıştaki
  davranışın aynısı.

## Deneme

- **Gerçek "Yedekten geri yükle" ekranı**, çalışan programda, yeniden
  başlatmadan:
  - goc_046 öncesi bir yedek geri yüklendi, iki güncelleme hemen uygulandı;
  - önceden 500 veren FET vitrifikasyon ekranı açıldı;
  - tazeleme yoklaması, Yönetici paneli ve on ekran çalıştı;
  - yeni tedavi açıldı ve tarih sırasına göre numaralandı;
  - aynı sürümden bir yedek geri yüklenince güncelleme cümlesi çıkmadı, panel
    "Veritabanı güncel." dedi.
- **Terminalden `geri_yukle.py`:** güncellemeleri uyguladı ve söyledi.
- **Taşınan kontroller için gerileme denemesi:**
  - v6.144'ün 42 kontrolü yeniden geçti;
  - yönetici 27, yönetici olmayan kullanıcı 9 adreste sorunsuz, JS hatası
    yok.

---

# v6.146 — zaman çizelgesi işlemin yapıldığı tedaviye bağlı

Kullanıcının isteği: *"Zaman çizelgesini de işlemin yapıldığı tedaviye
bağla."* v6.143'te kapsam dışı bırakılmıştı. `formlar._olay_ilk()` saatleri
örneğin **kendi** tedavisinden topluyordu (`specimen.cycle_id`). Bir embriyo
FET'te çözülünce:
- FET'in çizelgesi bomboş kalıyordu;
- kaynak ICSI'nin çizelgesinde FET'te yapılan çözme ve transfer görünüyordu;
- ICSI'nin resmî ART Lab formundaki İŞLEM saatleri de öyleydi. Yüklenen
  formların `{{saat_thaw}}`/`{{saat_transfer}}` etiketleri de o yüzden
  ICSI'ye FET'in saatini basıyordu.

## Kural: `db.olay_tedavisi()`

- **Çözme, transfer, dondurma** "hangi tedavide" sorusunu kendi alanında
  yanıtlıyor: `thaw_cycle_id`, `tr_cycle_id`, `vit_cycle_id` (v6.143). Boşsa
  kendi tedavisi.
- **Değerlendirmelerin böyle bir alanı yok.** Ölçü embriyonun o andaki
  tedavisi: işlemden önceki son çözme hangi tedavi içinse o, çözülmemişse
  kendi tedavisi. FET (3→5 kültür)'te çözülen 3. gün embriyosunun blastokist
  değerlendirmesi böylece FET'in çizelgesine düşüyor.
  - Ölçü saat, kimlik değil: `_gun_olay_kaydet()` kaydı güncellerken kimliği
    koruyor, saati değiştiriyor.
- **"Bu tedavide yapılan olaylar"** koşulu tek yerde: `db.tedavide_yapilan()`.
  Adaylar tedavinin kendi örnekleri ile bu tedavi için çözülenler.

## Özet kutusu da aynı koşulla

Tedavi ekranının üstündeki "Embriyoloji özeti" kutusu da `s.cycle_id` ile
sayıyordu. FET (3→5)'te blastokist değerlendirmesi yapılmış olsa da kutu
"Blastokist sayısı 0" diyordu. Çizelge düzelince aynı sayfada birbirini
tutmayan iki bilgi olacaktı, bu yüzden `cycle_ozet()` de aynı koşula
bağlandı.

## Deneme

- **Var olan kayıtlar:** 120 tedavinin çizelgesi eski ve yeni kuralla birebir
  aynı, 480 özet sayısı da aynı. Programda açılmış FET yoktu; aktarılan
  FET'lerin embriyoları zaten FET'in kendi altında.
- **FET** (ekranlardan):
  - tüp çözüldü (20.09 09:00) ve transfer edildi (12:00);
  - FET'in çizelgesinde iki satır, arada 3 saat;
  - kaynak ICSI'nin çizelgesi değişmedi;
  - eski kuralın çözmeyi ICSI'ye yazdığı da gösterildi;
  - ART Lab İŞLEM saatleri ve `{{saat_thaw}}` ICSI'de boş, FET'te dolu.
- **FET (3→5 kültür)** (3. günde dondurulmuş embriyoyla):
  - çözme (21.09 09:00) ve FET'te 5. gün blastokisti (23.09 10:00);
  - çizelgede arada 49 saat;
  - özet kutusu 0'dan 1'e çıktı;
  - kaynak ICSI'nin çizelgesi ve sayıları değişmedi.
- Eski/yeni farkı yalnızca bu iki FET'te ve kaynaklarında çıktı. İlgili
  ekranlar, formlar ve Excel çıktısı açıldı.

## Yan yolda bulunan (düzeltilmedi)

Değerlendirmeler (örnek, gün) başına **tek kayıt** tutuluyor
(`_gun_olay_kaydet()`, v6.62'den beri).
- Kaynak tedavide 5. gün blastokist kaydı olan bir embriyo FET (3→5
  kültür)'e alınıp yine 5. gün değerlendirilirse, kaynağın kaydının
  **üzerine yazılıyor**. Denendi: kaynaktaki 4BB (24.08) → 4AA (23.09).
- Olağan kullanımda olmuyor: FET (3→5)'e 2/3. gün embriyosu alınıyor,
  kaynağında blastokist kaydı yok. Yalnızca blastokist evresinde
  dondurulmuş bir embriyo bu tiple çözülürse oluyor.
- Nasıl ele alınacağı klinik bir karar: uyarmak mı, ayrı kayıt mı? Kullanıcıya
  soruluyor.

# v6.147 — Yumurta Çözme'de ICSI'den gebeliğe bütün aşamalar

Kullanıcının isteği: *"yumurta çözme tedavisinde denüdasyon haricinde diğer
bütün işlemler IVF/ICSI cycle tedavisi ile aynı olmalıydı."* v6.102'de
Yumurta Çözme yalnızca çözmeydi; o günkü karar "çözmeden sonra ICSI
gerekiyorsa ayrı bir tedavi açılır" idi. Kullanıcı kararını değiştirdi.
(Ocak–haziran Access kayıtlarındaki yedi "OOSİT ÇÖZME" satırı bu değişikliği
bekliyor, onlar bir sonraki sürümde aktarılacak.)

## Aşamalar

Çözme → Androloji → ICSI → Fertilizasyon → Cleavage → Blastokist →
Vitrifikasyon → Transfer → Gebelik.
- **Denüdasyon yok**: yumurta dondurulmadan önce soyuldu.
- **OPU da yok**: bu tedavide yumurta toplanmıyor, `fet`'in gerekçesi.
- Göç gerekmedi: tip zaten vardı, yalnızca aşama listesi değişti.
- `TIP_ASAMALARI` `db.py`'ye taşındı (`app.TIP_ASAMALARI` aynı sözlük):
  resmî formlar ve Excel de "bu tipte çözülen yumurtaya ICSI yapılıyor mu"
  diye soruyor (`db.cozulen_yumurta_islenir()`), `app`'i import edemiyorlar.

## Çözülen yumurta başka bir tedavinin örneği

Yumurtanın `specimen.cycle_id`'si Yumurta Dondurma, hiç değişmiyor. Bunun
aşama ekranlarında dört sonucu var:
- **Örnekler `thaw_cycle_id` ile bulunuyor**: `db.tedavi_ornekleri()` (v6.62'de
  blastokist için yazılmış `_blast_kosul()`; artık ICSI, fertilizasyon ve
  cleavage de kullanıyor).
- **Seçim `specimen.id` ile**, dört ekranda (v6.62'de yalnızca blastokistte):
  liste iki ayrı Yumurta Dondurma'nın yumurtalarını taşıyabilir, sıra no orada
  tekil değil. Eski adres (`?oosit=3`) tek tedavili listede hâlâ çalışıyor.
  "Kaydet → sıradaki" listenin sırasıyla (`_sonraki_ornek()`) — cleavage'da
  eski sorgu enjekte edilmemiş, listede olmayan bir yumurtaya atlayıp ekranı
  başa döndürebiliyordu, o da düzeldi.
- **Olay örneğin kendi tedavisine yazılıyor** (CLAUDE.md kuralı): ICSI,
  fertilizasyon ve cleavage POST'ları rotanın `cycle_id`'sini yazıyordu
  (IVF/ICSI'de ikisi aynıydı). Fotoğraf da yumurtanın kendi arşivine.
- **Silme ekranları tedaviyi taşıyor** (`?cycle=`), sunucu doğruluyor
  (`_hedef_tedavi()`).

## Maturasyon iki kez soruluyor, iki ayrı kayıt

Denüdasyonda (Yumurta Dondurma, v6.96) ve çözmeden sonra ICSI ekranında.
ICSI ekranı eskisi gibi "yumurtanın son maturasyonu"na baksaydı çözülen her
yumurtayı kaydedilmiş sanıp formu açmazdı; kaydetse kaynağın kaydının üzerine
yazardı (Yumurta Dondurma'nın M2 sayısı ve formu bozulurdu).
- ICSI ekranı yalnızca BU tedavinin maturasyonunu okuyor ve güncelliyor
  (`_tedavi_ek()` → `db.olay_tedavisi()`, v6.146'nın kuralı).
- ICSI silmesi de yalnızca bu tedavininkini iptal ediyor. ICSI aşaması
  olmayan bir tedaviye düşerse (adressiz eski bir bağlantı çözülen yumurtayı
  kendi tedavisine götürür) hiçbir şey iptal etmiyor — denemede gerçekten
  kaynağın maturasyonunu da iptal ediyordu, bu engel o yüzden var.

## İşlem saati çözmeden önce olamaz

FET tiplerinin dört aşama ekranı (ICSI, fertilizasyon, cleavage, blastokist)
bu tedavideki çözmeden önceki bir saati reddediyor, sebebini ve çözme saatini
yazıyor ("İşlem saati bu tedavideki çözmeden (20.09.2026 09:00) önce olamaz").
- Neden: `olay_tedavisi()` saate bakıyor. Öyle bir kayıt kaynak tedavinin
  sayılırdı; ICSI ekranı yazdığını göremez, her kaydette yeni bir maturasyon
  açardı.
- Saati sessizce değiştirmek (bozuk yılın "şu ana düşmesi" gibi) düşünüldü,
  seçilmedi: yanlış yazılan saat çoğu zaman çözme saatinin kendisi.
- Bilinen sınır: reddedilince yazılanlar forma geri gelmiyor, kayıtlı
  değerler basılıyor.

## Çözmede dejenere çıkan yumurta

ICSI şeridinde "Dej.", form yerine bilgi kartı, sunucu yeni kayıt açmıyor
(v6.139'un "gizlemek değil kilitlemek" kuralı). Yalnızca bu tedavinin çözmesi
sayılıyor. Enjekte edilmediği için cleavage ve blastokistte zaten görünmüyor.

## Vitrifikasyon ve transfer

- **Dondurulacaklar**: bu tedavi için çözülüp transfer edilmeyen (FET'in
  koşulu, v6.143) + enjekte edilmiş (v6.105) + cleavage/blastokist
  değerlendirmesi olan (v6.137). Dondurma kaydı sayılacaksa BU tedavininki
  olmalı: kaynağın yumurta dondurması sayılsaydı enjekte edilip hiç
  değerlendirilmemiş yumurta da listeye girerdi.
  - Koşul tek yerde (`_vit_adaylari()`), kayıt da aynısını soruyor. IVF/ICSI'de
    kayıt tarafı bugüne kadar yalnızca "bu tedavinin örneği mi" diye
    bakıyordu, ekranın iki süzgecini artık o da uyguluyor.
  - Dondurmanın `vit_cycle_id`'si bu tedavi (goc_046), tüp Cryo Haritası'na
    giriyor.
- **Yumurta transfer adayı değil.** Çözülen yumurta 'cozuldu' durumuna
  geçiyor — çözülen embriyonunkiyle aynı değer — ve hastanın bütün transfer
  ekranlarında aday olarak görünüyordu. Ölçü: yumurta donduran bir tipin
  örneği ve hiç ICSI'si yok. Döllenince aday.

## Yumurta mı embriyo mu

- `db.yumurta_mi(tip, asama)`: Yumurta Çözme'de çözülen yumurta, ICSI'den
  sonra dondurulan ya da transfer edilen embriyo.
- **Taşıyıcının içeriği dondurmanın yapıldığı tedavinin tipinden**
  (`icerik_tipi_sql()`, `tasiyici_icerigi().icerik_tipi`); önce örneğin kendi
  tedavisinden bakılıyordu ve Yumurta Çözme'de dondurulan embriyonun tüpü
  "yumurta" diyecekti. Sabit bir SQL metni değil fonksiyon: `vit_cycle_id`
  eski bir yedekte yok (tuzak #15).
- Çözme ekranı yumurta tüpünde artık "Yumurta N" yazıyor (önce hep
  "Embriyo").

## Tedavi ekranı, resmî formlar, Excel

- **Özet kutusu**: "Toplanan"ın yerinde "Çözülen yumurta sayısı" (kırılımında
  canlı), sonra M2 (ICSI ekranındaki), döllenen, cleavage, blastokist.
- **Resmî formlar**:
  - ART Lab'ın yumurta ızgarası Yumurta Çözme'de çözülen yumurtalar
    (`formlar.yumurta_kosulu()`).
  - Izgaranın her hücresi ve formların sayımları BU tedavide yapılan
    işlemden (`db.bu_tedavide()`, `db.tedavide_yapilan()`). Yoksa ICSI,
    döllenme, "F/✓" işaretleri Yumurta Dondurma'nın formuna da yazılırdı.
  - Özet formunun "Toplanan"ı FET tiplerinde boş. Aktarılan FET'lerin
    embriyoları FET'in altında duruyor (v6.130), kutu çözülen embriyo
    sayısını "toplanan yumurta" diye basıyordu.
- **Ay listesi**: M2'den blastokiste sayılar işlemin yapıldığı tedaviden
  (`db.tedavide_yapilan_ifade("c.id")`), FET tiplerinde "Toplam yumurta /
  Sağ / Sol" boş.
- **Tedavinin Excel dökümü** bir geçmiş: hücreleri örneğin son kaydı,
  bilerek kısıtlanmadı. FET tiplerinde satırlara bu tedavi için çözülenler
  eklendi (önce yalnızca aktarılanlar vardı).
- **İstatistik**: MII yalnızca toplanan yumurtalardan (paydayla aynı süzgeç).
  Sayılar örneğin kendi tedavisinin ayına yazılmaya devam ediyor; çözülen
  yumurtanın ICSI'si toplandığı ayda.

## Çözmeyi geri almak

Çözmeden sonra girilmiş HER kayıt engel (ICSI, değerlendirme, transfer),
yalnızca yeniden dondurma değil. Çözme gidince yumurta tedavinin
ekranlarından düşer, kayıtları sahipsiz kalırdı. Önce en son adım.

## Deneme

- **Uçtan uca** (104 kontrol, sentetik "DENEME" hastası):
  - Yumurta Dondurma'da 4 yumurta, denüdasyonda MII, iki tüp;
  - Yumurta Çözme'de tüp A çözüldü (2 canlı, 1 dejenere), ICSI (MII
    enjekte, MI enjekte edilmedi), fertilizasyon 2PN, gün 3, blastokist
    4AA, dondurma; tüp B çözüldü, gün 3'te transfer;
  - çözmeden önceki saat reddedildi, dejenere yumurtaya kayıt yazılmadı,
    kaynağın maturasyonu hiçbir adımda değişmedi;
  - özet kutusu, zaman çizelgesi, iki resmî form, Excel dökümü ve ay
    listesi iki tedavide de doğru;
  - silme ve geri alma akışları, IVF/ICSI'nin aynı ekranlarda eski gibi
    çalıştığı, bütün tedavilerin aşama ekranları ve taşıyıcı sayfaları.
- **Var olan 120 tedavi**: eski ve yeni kodun formları, Excel dökümleri, ay
  listeleri ve istatistiği karşılaştırıldı. Tek fark 33 FET'in Özet'indeki
  "Toplanan" ve ay listesindeki yumurta sütunları (ikisi de boş kaldı).
- v6.144 ve v6.146 denemeleri yeniden geçti. Ekranlar telefonda ve
  masaüstünde açıldı: yatay taşma yok, betik hatası yok.

## Değişmeyen

- v6.146'daki açık soru (FET (3→5 kültür)'te aynı gün değerlendirmesi
  kaynağın kaydının üzerine yazılıyor) hâlâ açık. Yumurta Çözme'de o sorun
  doğmuyor: çözülen yumurtanın kaynakta cleavage/blastokist kaydı yok.
- Tedavi ekranının "Zamanlar" kartı (hCG/OPU/denüdasyon) her tipte basılıyor,
  FET'te de öyleydi; dokunulmadı.

---

# v6.148 — ocak–haziran Access kayıtları; FET'in çözdüğü embriyo tüpüne bağlanıyor

Kullanıcının isteği: *"Bu kayıtları da aynı şekilde programa ekler misin?"*
(ocak, şubat, mart, nisan, haziran 2026 Access dosyaları; mayıs dosyası
gelmedi). Kullanıcının dört kararı:
- **Tüpler:** *"Bağla, belirsizi listele"* — FET'te çözülen embriyo, hastanın
  programdaki dolu tüpüyle skoruna göre eşleşiyorsa o tüpe bağlanır, tüp Cryo
  Haritası'nda boşalır; temmuz/ağustosun aktarılmış FET'leri de. Eşleşmeyen
  ya da birden çok seçenekli olanlar kayıt numarasıyla listelenir.
- **"OOSİT ÇÖZME" satırları:** önce Yumurta Çözme'ye ICSI ve sonrası
  eklendi (v6.147), sonra bu satırlar Yumurta Çözme olarak aktarıldı.
- **Tarihsiz satır:** *"Yakın kaydın tarihine yaz"* — Access'teki bir önceki
  kaydın tarihi, not "yaklaşık" diyor; OPU/transfer alanı boş kalıyor.
- **Yazım hatalı tarih:** *"Önerdiğin tarihlerle aktar"* — düzeltmeler ayrı
  bir dosyada (`duzelt=`), not "... yazıyordu, ... olarak düzeltildi" diyor.

Kaynak dosyalar ve düzeltme dosyası depoya girmedi (gerçek hasta verisi);
aşağıda yalnızca sayılar var.

## Dondurma notu artık daha çok yazımı tanıyor

Ocak–haziran notları aynı işi çok farklı yazmış. v6.147'ye kadar tanınmayan,
her biri gerçek kayıtlardan:
- **Fiiller:** "DONDURULMUŞTUR", "DONDURULARAK KORUNMUŞTUR", "REFREEZE
  EDİLDİ/EDİLEREK", yazım hatalı "DONDURULRAK", "DONDURULARK". Tanınmasaydı
  altmışa yakın dondurma (yedi tüplük biri dahil) hiç yazılmayacaktı.
- **Nesnenin yeri:** "REFREEZ EDİLEN (4CC) İLE BİRLİKTE ... KALDI",
  "REFREEZE (KAVG1) KALDI" — skor fiilden **sonra**. Fiilsiz yazım da var:
  "KÜLTÜRE EDİLEN 2 ADET D5 EMBRİYOSU (3CB) (2CC) İLE BİRLİKTE TOPLAMDA 3
  TÜPTE 6 ADET EMBRİYOSU KALDI". Bunun gerçekten dondurma olduğunu temmuzdaki
  bir FET'in o (3CB)'yi transfer etmesi gösteriyor; rapor bunu ayrıca söylüyor.
- **Cümle sınırı:** yalnızca fiilin cümlesine bakılıyor, aynı cümlede önce
  transfer geçiyorsa ondan sonrası. "(1BB) TRANSFER EDİLDİ. GERİDE KALAN ...
  (1CC-1CC) ŞEKLİNDE DONDURULARAK SAKLANDI" notunda transfer edilen 1BB
  dondurulmuş sayılıyordu.
- **FET'te stok cümlesi dondurma değil:** "GERİDE 8 ADET ... DONDURULARAK
  SAKLANMIŞTIR" depoda kalanları anlatıyor. Karar yapılandırılmış alandan:
  çözülen − transfer edilen = 0 ise o FET'te dondurulacak embriyo yoktu
  (v6.142'nin dersi, serbest metinden önce yapılandırılmış veri).
- **Yumurta:** "1*M1" (MI yumurta, kendi havuzundan), "5M2", "(M2)"; "6 ADET
  (M2) OOSİT (3*M2) (3*M2)"daki "(M2)" tüp değil, sayının niteliği.
- **"BB"** (D3 listelerinde bir embriyonun yerini tutan yazım): skorsuz
  dondurulmuş embriyo; skor alanları boş bir cleavage değerlendirmesi
  yazılıyor, yazım notunda. Skor uydurulmuyor ama "Cleavage sayısı" onu
  sayıyor.
- Gün "D5"in yanında "3.GÜN" / "5,GÜN" yazımından da okunuyor.
- Eski ve yeni ayrıştırıcı bütün notlarda karşılaştırıldı: temmuz ve
  ağustosta değişen yalnızca bu kurallara giren satırlar.

## Var olan tüpler onarılıyor (`tamamla`)

Eski araç "BB"yi ve MI yumurtayı tanımıyordu: temmuzun üç tüpünde birer
embriyo, üç tüpünde birer MI yumurta eksik yazılmıştı, bir tüpte "((4CB"
yazım hatası yüzünden bir blastokist düşmüştü, bir FET'in yeniden dondurması
hiç yazılmamıştı. `_dondurma_kayitlari()` artık notun gruplarını var olan
tüplerle sırayla eşleştiriyor: tüpteki örnek kendi kaydından (skoru, yumurtada
olgunluğu) tanınıyor, eksik yer tamamlanıyor, notta olmayan örnek tüpten
çıkıyor. **Tüp silinmiyor, etiketi ve konumu değişmiyor** — kullanıcı Cryo
Haritası'ndan konum girmiş olabilir.

## Taze transfer yazılıyor

Araç yalnızca FET transferini yazıyordu. IVF/ICSI'de embriyo aynı tedavide
transfer edildiğinde tedavi "transfer ile bitti" diyor ama transfer ekranı,
istatistiğin transfer sayısı ve gebelik ekranı boş kalıyordu. Ocak–haziranda
24, temmuzda 1 satır. Transfer edilen embriyo 2PN'lerden, dondurulmayanlardan
seçiliyor; EMBRİYO1/2 kutusundaki skor o günün değerlendirmesi. Kutuların
yazımı ("8" + "1") "81" diye birleşiyordu, artık "8HG1".

## Kaynağın kendi tutarsızlıkları

- **ICSI toplamı** 12 satırda tutmuyor (İŞLEME ALINAN ≠ 2PN + anormal +
  intakt + dejenere). Birinde 11 ICSI'nin 10'u dejenere yazılmış ama 5'i 2PN
  ve ikisi dondurulmuş. 2PN, anormal ve intakt korunuyor, dejenere kalana
  kısılıyor; rapor söylüyor. Tutan satırda dağıtım v6.130'dakiyle aynı.
- **2PN sayısı 0 ama embriyo dondurulmuş** (dört satır; birinin embriyolarını
  ağustostaki bir FET çözmüş, yani tüpler gerçekten tankta). Embriyo enjekte
  edilmiş ama döllenme kaydı olmayan yumurtaya yazılıyor, rapor söylüyor.
  Tankta duran tüpün programda görünmemesi (v6.142) boş bir döllenme
  sayısından pahalı.
- **Viabilite** dokuz satırda 100'ü aşıyor ("9080", "1001000"): embriyo
  başına değerler bitişik yazılmış gibi. Bölünmüyor; alan boş, ham değer
  çözmenin notunda. Temmuzun üç kaydı `tamamla` ile düzeltildi (ekranda
  "%9080" yazıyordu).
- **Ad**: 13 satırda aynı dosya numarası farklı yazılmış adla geliyor; hepsi
  aynı kişi (bir harf, yer değiştirmiş ad, aynı doğum tarihi). Eşleşme yine
  dosya numarasıyla, programdaki ad korunuyor, rapor "DİKKAT" diyor.

## Yeni satır türleri

- **"OOSİT ÇÖZME"** Yumurta Çözme (7 satır): yumurtalar çözme olayıyla
  açılıyor (`thaw_cycle_id` bu tedavi), olgunluk, ICSI, döllenme, dondurma ve
  transfer IVF/ICSI'deki gibi. Çözme günü transfer günü − transfer aşaması.
- **PGT kültürü** (3 satır): protokolü boş ya da ilaç adı, OPU'su yok,
  ÇÖZDÜRÜLEN dolu, not "çözme sonrası kültüre edilen ... PGT ... dondurularak
  saklandı" — FET (3→5 kültür). `ivf_icsi` sayılsaydı yumurta toplanmış gibi
  görünürdü. Karar sayılardan, nottaki kelimeden değil.
- **Tarihsiz** 11 satır, **boş kopya** 1 satır (aynı hastanın aynı günkü dolu
  satırının içi boş ikizi, atlandı), **yazım hatalı tarih** 5 satır.
- FET tiplerinde "Toplanan" yazılmıyor (`opu_sag_oosit`): Yumurta Çözme
  satırının TOPLANAN OOSİT'i çözülen yumurta sayısı.
- İptal kalıpları: "D2/D3 EMBRİYO ARRESTİ", "KLİVAJ ARRESTİ" → Cleavage
  Arrest, "D5 ... ARRESTİ" → 5. Gün Arrest.

## FET'in çözdüğü embriyo tüpüne bağlanıyor

`_kaynaga_bagla()`. v6.130'dan beri FET'te çözülen embriyo FET'in kendi
altında açılıyordu, çünkü dondurulduğu tedavi programda yoktu. Ocak–haziran
gelince çoğunun kaynağı programda: tüp Cryo Haritası'nda hâlâ "dolu"
görünürdü, soyağacı ("bu embriyo hangi tedaviden") kopuk kalırdı.
- **Adaylar:** hastanın dolu, çözmeden önce dondurulmuş, tek tedavinin
  içeriğini taşıyan tüpleri (yumurta çözmede yumurta tüpleri).
- **Eşleşme:** toplam örneği çözülen sayıya eşit tüp kümeleri (bir tüp bütün
  olarak çözülür) ve transfer edilen embriyonun yazımı kümedeki bir örnekle
  tutmalı. Aynı evrede skor aynı olmalı; tüpteki örnek daha erken evredeyse
  (gün 3 tüpü, gün 5 transferi) kültürde ilerlemiş olabilir, tutar; ileri
  evredeyse tutmaz (blastokist tüpü, gün 3 transferi). Skoru birebir tutan
  küme, "kültürde ilerlemiş olabilir" diye tutandan önce gelir — yoksa her
  FET'te bir kavitasyon tüpü belirsizlik yaratıyordu (provada üç kayıt).
- **Tek küme** → bağlanıyor. Aynı tedavinin içeriği birebir aynı tüpleri
  ("(4AA) (4AA)") ayırt edilemez, fark da etmez: ilki. **Farklı tedavilerin**
  aynı skorlu tüpleri belirsiz sayılıyor — hangi tedavinin embriyosu olduğu
  soyağacını değiştirir.
- **Bağlamak:** FET'in kendi örneklerinin bütün olayları tüpteki örneğe
  taşınıyor (`olay.cycle_id` örneğin kendi tedavisi), çözmeye tüp yazılıyor,
  FET'in boş kalan örnekleri siliniyor, tüp programın kendi çözmesindeki gibi
  boşaltılıyor. Protokol notunun "tedavi programda yok" cümlesi kaynağın
  numarasıyla yeniden kuruluyor.
- **Provada:** 50 çözme bağlandı (biri Yumurta Çözme; ocak–haziran 37,
  temmuz/ağustos 13); 16'sı
  listelendi (4 birden çok seçenek, 12 dolu tüpler tutmuyor); geri kalanın
  tüpü programda yok (program öncesi dondurma). Tutarlılık: nisandaki bir
  FET'in "tutmuyor" dediği blastokist tüpünü temmuzdaki FET çözüyor; martın
  fiilsiz yeniden dondurması temmuzdaki bir transferin kaynağı oldu.

## goc_046'nın bir yan etkisi

goc_046 eski çözmelere tüpünü geriye dönük yazarken, çözmeden önce dondurması
olmayan örneğe "herhangi bir tüpünü" yazıyor. Program öncesi FET embriyosunun
tek tüpü yeniden dondurulduğu tüp olabilir; göç yeniden dondurmadan sonra
çalıştıysa o tüp "çözülmüş" görünür, dondurma geri alınamaz, bir sonraki
FET'e aday olmaz (prova kopyasında bir tüpte). `tamamla` bunu düzeltiyor:
bir FET kendi dondurduğu tüpü çözemez. Göç değiştirilmedi (kuralı: eski göç
değiştirilmez); kullanıcının veritabanında büyük olasılıkla yok, çünkü orada
göç yeniden dondurmadan önce çalıştı.

## Programda: dondurulan örneğin skoru dondurmanın tedavisinden

Bağlama, programda gizli duran bir hatayı görünür yaptı. Vitrifikasyon
ekranı, taşıyıcı sayfası ve resmî formların dondurma satırı "örneğin en son
değerlendirmesi"ni basıyordu. Embriyo sonra bir FET (3→5 kültür)'de
yeniden değerlendirilince kaynak tedavinin ekranı FET'in skorunu gösteriyordu:
4. gün morula olarak dondurulan embriyo "3AC · gün 5". Programın kendi
girdiği veride de olurdu. `db.bu_tedavinin_skoru()`: o tedavide herhangi bir
değerlendirme varsa yalnızca onlar, hiç yoksa (düz FET'te yeniden dondurulan
embriyonun FET'te skoru olmaz) hepsi — eski davranış. Sıralamayla
çözülmüyordu: tüpün tedavisinde yalnızca cleavage, FET'te blastokist varsa
blastokist skorunu soran alt sorgu yine FET'inkini bulurdu. Tedavinin Excel
dökümü bilerek dokunulmadı (v6.147: bütün geçmişi basıyor).

Vitrifikasyon ekranının "Dondurulmuş" kartı da yalnızca blastokist skorunu
basıyordu: gün 3'te dondurulan her embriyo "girilmedi" görünüyordu, oysa
kaydı var. v6.137 aday listesi için cleavage yazımını ("5HG3") eklemişti,
kart da artık aynısını basıyor.

## Deneme (kullanıcının veritabanı kopyasında)

- Beş dosya tarih sırasıyla aktarıldı (443 tedavi, 289 yeni hasta), temmuz
  ve ağustos `tamamla` ile tamamlandı; 433 yeni tüp (temmuzun iki eksik
  tüpü dahil). Hata yok.
- **İkinci çalıştırma hiçbir şeyi değiştirmedi**: yedi dosyaya `tamamla` ve
  bir dosyanın aktarımı yeniden; her tablo satır satır karşılaştırıldı.
- Bütünlük: yabancı anahtar ve SQLite bütünlük denetimi temiz; yetim olay,
  kendi tedavisine yazılmamış olay, içi boş "dolu" tüp, çözülmüş "dolu" tüp,
  aynı tedavide iki tüpteki örnek, iki kez transfer, bağlanmış FET'te kalan
  kendi örneği, saatsiz olay, 100'ü aşan canlılık: hiç. 127 çok tedavili
  hastanın hepsi tarih sırasıyla numaralı.
- 8392 ekran adresi (bütün tedavilerin bütün aşama ekranları, iki resmî
  form ve Excel, bütün taşıyıcı ve hasta sayfaları, ay listeleri,
  istatistik) açıldı: hiçbiri hata vermedi. 549 aktarılmış tedavinin Özet
  formunda NOTLAR kutusu tarayıcıda ölçüldü: en uzunu 11 satır, hiçbiri
  kesilmiyor.
- v6.147 (104 kontrol), v6.146 (25) ve v6.144 (42) denemeleri yeniden geçti.

## Bilinen / yazılmayan

- **Mayıs dosyası yok.** Mayısta çözülen tüpler programda hâlâ "dolu".
- Parantezsiz iki dondurma ("2 ADET M2 OOSİT", "2 TÜPTE 4 ADET D5
  EMBRİYOSU"): tüplere dağılım bilinmiyor, yazılmadı, uyarı çıkıyor.
- Bir satırda notta 6 dondurulan embriyo var, 5 2PN — biri yazılmadı.
- Bir satırda iki embriyo transfer edilmiş ama ICSI/2PN sayısı hiç
  girilmemiş: transfer yazılmadı (döllenme uydurulmuyor).
- Bir dosya numarası iki haneli ("99"): Access'te yer tutucu olabilir,
  `liste` "DİKKAT" diyor.
- v6.146'daki açık soru hâlâ açık.

---

# v6.149 — mayıs 2026 Access kayıtları

Kullanıcının isteği: *"Şimdi diğer claude hesabında yaptığım gibi aynı
şekilde 2026 mayıs ayı eski hasta kayıtlarını programa ekle."* v6.148'de
ocak–haziran aktarılırken mayıs dosyası gelmemişti.

Dosya öteki aylarla aynı yapıda: tek tablo (`VERİTABANI`), 92 kolon, 63
satır. `.accdb` bu oturumda `mdbtools` ile CSV'ye çevrildi
(`LC_ALL=C.UTF-8 mdb-export dosya.accdb VERİTABANI > mayis.csv` — yerel ayar
UTF-8 değilse `mdb-export` Türkçe tablo adında "Invalid byte sequence" diye
duruyor). Kaynak dosya ve CSV depoya girmedi (`.gitignore`); aşağıda
yalnızca sayılar var.

## Aracın üç düzeltmesi

Önizleme (`liste`) üç yerde yanlış okuyordu; üçü de sessizdi.

**1. Parantez içindeki "(REFREEZE)" fiil sanılıyordu.** Bir FET notu:
"(1CB) ŞEKLİNDE (REFREEZE) DONDURULARAK SAKLANDI". `_DONDURMA_FIILI`'nin
yalın `REFREEZE` seçeneği (skor fiilden SONRA yazılır: "REFREEZE (KAVG1)
KALDI") en soldaki eşleşme olarak bunu yakalıyordu; skor fiilin arkasında
aranınca (1CB) kaçtı ve tüp olarak ") DONDURULARAK SAKLANDI" yazılacaktı.
Düzeltme: yalın `REFREEZE` parantez içindeyse fiil değil (`(?<!\()` /
`(?!\s*\))`), "(REFREEZE)" grubu da tüp sayılmıyor.

**2–3. İki ayrıntılı iptal sebebi hiç tanınmıyordu.** v6.103'ün altı
sebebinden araç yalnızca üçünü arıyordu (fertilizasyon olmadı, cleavage
arrest, 5. gün arrest). Mayıs notları öteki ikisini programdaki adıyla
birebir yazıyor: "OPUDA OOSİT ÇIKMADI" (4 satır) ve "İNMATÜR OOSİT
SEBEBİYLE" (1 satır). Bunlar genel "İptal"e düşecekti; artık "Yumurta
Çıkmadı" ve "İmmatür Yumurta". Kalıplar arrest/fertilizasyondan **sonra**
deneniyor — iki sebep birden yazıyorsa işlemin daha ileri aşamadaki sonu
kazanır. "EMPTY ZONE" (2 satır) ve "3PN" (1 satır) genel "İptal"de kaldı:
listede karşılıkları yok (v6.130'un kararı).

**Gerileme denendi.** Öteki ayların CSV'leri bu oturumda yoktu; belgelerde
geçen gerçek REFREEZE ve dondurma yazımları (fiilden sonra skor, bitmiş fiil,
"İLE BİRLİKTE ... KALDI", "REFREEZE YAPILAMADI", yumurta ve D3 notları)
eski ve yeni araçla ayrıştırıldı: hepsi aynı, fark yalnızca hedeflenen
yazımlarda.

**Önceki aylar:** onlarda da "OOSİT ÇIKMADI" diyen satır varsa genel
"İptal" olarak aktarıldı. `tamamla` iptal sebebini güncellemiyor; istenirse
ayrı bir iş.

## Aktarım (test veritabanının kopyasında)

Kullanıcının gerçek veritabanı bu oturumda yoktu. Bu yüzden 63 satırın
hepsi "yeni hasta" olarak açıldı ve FET'in çözdüğü embriyo hiçbir tüpe
bağlanamadı. Önceki ayların tüpleri yalnızca kullanıcının makinesinde var;
bağlama orada olacak.

| | kaynak | program |
|---|---|---|
| tedavi | 63 | 63 (32 ivf_icsi, 21 fet, 10 oosit_cryo; 0 hata) |
| toplanan / MII / ICSI / 2PN | 344 / 247 / 209 / 118 | aynı |
| transfer | 32 | 32 (30 FET + 2 taze) |
| dondurulan embriyo | 71 | 71 (2 FET'te 3 yeniden dondurma dahil) |
| dondurulan yumurta | — | 60 (not metninden), toplam 51 tüp |
| çözülen | 31 | 33 |
| iptal | 10 | 4 yumurta çıkmadı, 1 immatür, 1 fert. olmadı, 1 cleavage arrest, 3 genel |

Çözülen farkı kaynağın iki satırından: birinde ÇÖZDÜRÜLEN boş ama bir
transfer var, ötekinde 2 yazıyor ama 2 transfer ve 1 yeniden dondurma var.
v6.148'in "transfer + dondurma alttan sınır" kuralı ikisini de doğru sayıyor.
Tarih düzeltmesi gerekmedi: bütün satırlar 4–21 Mayıs, boş ya da ay dışı
tarih yok. Uyarı satırı çıkmadı.

- İkinci aktarım 63/63 atladı; ardından `tamamla` hiçbir tabloyu
  değiştirmedi (sekiz tablo satır satır karşılaştırıldı).
- `PRAGMA foreign_key_check` ve `integrity_check` temiz.
- 851 adres 200 döndü: 63 tedavinin her aşama ekranı, hasta kartları, iki
  resmî form ve Excel'i, bütün taşıyıcı sayfaları, mayıs ay listesi,
  istatistik, Cryo Excel'i, tam döküm.
- 126 resmî form sayfası tarayıcıda ölçüldü: JS hatası yok, NOTLAR kutuları
  kesilmiyor.

## Bilinen, bu sürümde düzeltilmeyen

Embriyoloji Özet'te **19 harflik bir hasta adı ad kutusundan 3 piksel
taşıyor**, son harf kısmen kesiliyor (128 piksellik kutuya 131 piksel yazı).
Aktarımla ilgisi yok, programdan girilen uzun bir adda da olur; öteki
ayların verisinde bu uzunlukta ad çıkmamış. Kimlik bilgisi olduğu için
ayrıca bildirildi. Çözüm büyük olasılıkla o hücrenin `.tasabilir`
olması (v6.135'in mekanizması, kalıba dokunmadan).

## Kullanıcının makinesinde

KOMUTLAR.md "Eski Access kayıtları" → "Mayıs 2026". Haziran zaten
aktarıldıysa mayıstan sonra haziran, temmuz ve ağustos `tamamla` ile yeniden
geçirilmeli: sonraki ayların FET'lerinin mayısta dondurulan tüpleri ancak o
zaman bağlanıyor.

---

# v6.150 — resmî formda sığmayan ad küçülüyor; eski iptallerin sebebi

Kullanıcının isteği: *"İkisini de düzelt."* v6.149'un sonunda bildirilen iki
sorun.

## 1. Kimlik kutusunda sığmayan ad küçülüyor

Embriyoloji Özet'in EŞİNİN ADI kutusu 128 piksel; 19 harflik bir ad 131
piksel tutup son harfi kesiliyordu. v6.135'in çözümü (`.tasabilir`, yazı
sağdaki boş kutulara akar) burada olmaz: kutu formun **sağ kenarında**,
taşan yazı kâğıdın dışına çıkardı. Kâğıda elle yazarken de sığmayan ad
küçük yazılır — program da öyle yapıyor.

- **Hangi hücreler**: `formlar.sigdir_hucreleri(ad)`. Özet'te SOYADI, ADI,
  EŞİNİN ADI; ART Lab'da Adı ve Eşinin adı (yedi sütun genişliğinde, bugün
  sığıyor — kural iki formda aynı olsun diye).
- **Ekranda ve çıktıda**: hücre `.sigdir` alıyor; `form.html`'in
  `adlariSigdir()`'i puntoyu kutuya sığana kadar 0,25 piksel adımlarla
  düşürüyor, en çok yarısına (~40 harflik ad). Çıktıda kutu ekrandakinden
  geniş (ölçüldü: 128 → 249 piksel), o yüzden `beforeprint`'te yeniden
  ölçülüyor, `afterprint`'te ekrana göre geri alınıyor.
- **Excel'de**: aynı hücreler "sığacak şekilde küçült" (`shrinkToFit`)
  alıyor. Kalıbın stil listesi önbellekte paylaşılıyor; `yerlesim()` listenin
  **kopyasına** o stilin küçülen bir eşini ekliyor, kalıba dokunmuyor.
  `shrinkToFit` ile `wrapText` Excel'de birlikte kullanılamıyor, küçülen
  hücrede sarma kapalı.
- Kalıp (`form_kalip.json`) değişmedi.

### Ölçüm

Mayıs verisinin 63 tedavisinde iki form (126 sayfa): kesilen hücre 0 (önce
1), JS hatası yok. 19 harflik ad 11,1 piksele indi (kutu 128, yazı 129 —
1 piksellik tolerans içinde). Uç örnek olarak 32 harflik uydurma bir eş adı
6,4 piksele inip sığdı (%60'lık ilk alt sınırda 4 piksel taşıyordu, sınır
%50'ye indirildi). Çıktı düzeninde (249 piksel) aynı adlar tam puntoyla
sığdı. Excel: `H8` hücresi `shrinkToFit="1"` hizalamasıyla, dosya geçerli
ZIP.

## 2. Eski iptallerin sebebi: `iptal` kipi

v6.149 araca "OOSİT ÇIKMADI" → Yumurta Çıkmadı ve "İNMATÜR OOSİT" →
İmmatür Yumurta kalıplarını ekledi, ama ondan önce aktarılan aylarda aynı
notlar genel "İptal" olarak kaldı.

- `tamamla`'ya beşinci adım eklendi (`_iptal_sebebi_duzelt()`), ayrıca
  **yalnızca bu adımı** çalıştıran yeni bir kip: `iptal`. Sebep: `tamamla`
  dondurma değerlendirmesini nottaki değerle yeniden yazıyor (v6.142), yani
  aylar önce aktarılmış bir tedavide ekrandan elle düzeltilmiş bir skoru
  ezer. İptal sebebini onarmak için o riski almaya gerek yok.
- **Yalnızca sebep hâlâ genel `'iptal'` ise** değiştiriliyor. Kullanıcı
  ekrandan başka bir sebep seçtiyse dokunulmuyor. Değişiklik
  `degisiklik_log`'a yazılıyor (`iptal → yumurta_cikmadi`).
- Log satırı aracın kendi bağlantısından yazılıyor: `guvenlik.
  degisiklikleri_yaz()` ayrı bir bağlantı açıyor ve `yazma_islemi()`'nin
  `BEGIN IMMEDIATE` kilidi içinde 15 saniye beklerdi.

### Deneme (test kopyasında, mayıs verisiyle)

Mayısın beş ayrıntılı iptali eski araç yazmış gibi genel "iptal"e çevrildi,
birine de sanki ekrandan seçilmiş gibi "PN Arrest" yazıldı:
- `iptal` kipi dördünü güncelledi, "PN Arrest"e dokunmadı, üç empty zone /
  3PN iptali genel kaldı; `degisiklik_log`'a dört satır.
- Başka hiçbir tablo değişmedi (hasta, specimen, olay, taşıyıcı, işlemi
  yapan ve tedavinin öteki alanları karşılaştırıldı).
- İkinci çalıştırma: "0 tedavinin iptal sebebi güncellendi".
- `tamamla` da aynı sonucu verdi, ikinci çalıştırması 0.
- Tedavi ekranı ve ART Lab formu "Yumurta Çıkmadı İptal" basıyor.

## Kullanıcının makinesinde

KOMUTLAR.md "Eski Access kayıtları" → "İptal sebeplerini onarmak": aktarılan
her ay için bir `iptal` komutu.

## Açık: 3. gün dondurulan embriyoların cleavage kaydı

Kullanıcı aynı mesajda bildirdi: eski tedavilerde 3. gün dondurulan
embriyoların cleavage aşamasında hücre sayısı ve grade yok. Test kopyasında
aracın bugünkü hali doğru yazıyor (mayısta 8HG1 → gün 3, 8 hücre, G1, ekranda
görünüyor). Kullanıcının veritabanında boş kalmış olabilecek iki yol
bulundu:
- **Ağustos, v6.130'la aktarıldıysa ve sonra `tamamla` çalışmadıysa**: o
  sürüm 3. gün dondurmasını skor alanları boş yazıyordu. Test kopyasında
  değerlendirmeler boşaltılıp `tamamla` çalıştırıldı, 11 embriyonun 11'i
  hücre sayısı ve grade'le doldu.
- **"BB" ve "BİRLEŞME" yazımları** v6.148'den beri bilerek skorsuz
  yazılıyor (hücre sayısı ve grade boş). Mayısta bir tane var
  ("BİRLEŞMEG3"). "BB"nin laboratuvarın yazımında ne demek olduğu kullanıcıya
  soruldu; cevap gelene kadar dokunulmadı.

---

# v6.151 — hasta kartında yeniden dondurma görünüyor

Kullanıcının isteği: "Hasta kartı bölümünde hastanın bütün tedavileri
göründüğü gibi eğer refreeze yapıldıysa görünsün istiyorum."

Yeniden dondurma v6.143'ten beri kayıtlı (FET'te çözülüp transfer
edilmeyen embriyo aynı tedavide yeniden donduruluyor, `vit_cycle_id`). Tüp
sayfası bunu söylüyordu; hastanın tedavi listesi söylemiyordu. Artık
`/hasta/{id}`'nin Tedaviler kartında:

- **Yeniden dondurmanın yapıldığı tedavi** satırında "Yeniden dondurma"
  rozeti ve bir satır: `Yeniden donduruldu: 2 embriyo · tüp 0002-1430 →
  3. tedavide çözüldü`. Tüp sonradan çözülmediyse ok kısmı yok.
- **O tüpü çözen tedavi** satırında: `Yeniden dondurulmuş tüp çözüldü:
  0002-1430 (2. tedaviden)`.

Yani FET'ten FET'e zincir kartta iki yönden okunuyor. Satırın kendisi
tedaviye giden bir bağlantı, içine ikinci bir `<a>` konamıyor; öteki
tedavinin numarası düz metin ("3. tedavi"), kart zaten aynı ekranda.

**Yeniden dondurmanın ölçüsü türetilmiş**, işaret tutulmuyor:
`app.hastanin_yeniden_dondurmalari()` bir dondurmayı, aynı örneğin ondan
önce (kimlik sırası, v6.143'ün kuralı) iptal edilmemiş bir çözmesi varsa
yeniden dondurma sayıyor. **Tek istisna Yumurta Çözme**: orada çözülen
yumurta, dondurulan onun ICSI'sinden gelişen embriyo — aynı örnek ama
yeniden dondurma değil. Ayrım `db.yumurta_mi()`'nin iki aşamadaki cevabıyla
(çözülen tür ≠ dondurulan tür → sayılmıyor), tip adı elle yazılmadı.

Göç (goc_046) çalışmamışsa işlev boş dönüyor, kart eskisi gibi.

### Deneme

Test kopyasında: ICSI → tüp A → 2. tedavide (FET) çözme, bir transfer, iki
embriyo tüp B'ye → 3. tedavide (FET) tüp B çözme. Ayrıca Yumurta
Dondurma → Yumurta Çözme → embriyo dondurma. Kart: 2. tedavi rozetli ve
"→ 3. tedavide çözüldü", 3. tedavi "2. tedaviden", 1., 4. ve 5. tedaviler
değişmedi. Göçsüz veritabanında işlev boş döndü. 390 ve 1440 piksel
genişlikte sayfa yana kaymıyor.

---

# v6.152 — FET formları: çözülen embriyolar, canlılık, kalan tüpler

Kullanıcının isteği: "FET çözme tedavilerinde formlara işlem geçmiyor. Art
lab formunda Thaw bölümüne çözülen embriyolar eklensin. Transfer edilen
embriyolar da transfer bölümünde Uterus grade (x sayı) bölümüne canlılık
yüzdesi yanına yazılarak eklensin. Embriyoloji Özet Formunda da ÇÖZDÜRÜLEN
EMBRİYO SAYISI ... ÇÖZDÜRME SONRASI VİABİLİTE ... Notlar bölümüne de
çözülen embriyoların bilgisi eklensin. Hangi embriyo çözüldü geriye
dondurulmuş embriyo kaldı mı bilgisi yazsın."

Bir de soru: ART Lab'ın ızgarasındaki "Transfer" satırında bazı yumurtaların
altında **F** yazıyor. **F = Freeze**: o embriyo transfer edilmedi,
donduruldu. ✓ transfer edildi demek, boş kutu ikisi de olmadı demek. Bu
v6.37'den beri böyle; anlamı formda yazmıyor. Değiştirilmedi, istenirse
başka bir işarete çevrilebilir.

## Tek kaynak: `formlar.cozulen_ornekler()`

İki form da çözmeden yalnızca bir **sayı** basıyordu (Özet'te çözülen sayı
ve farklı sağkalım etiketleri, ART Lab'ın THAW ve TRANSFER kutularında
birer sayı). Artık her çözülen örnek için şunlar tek yerde toplanıyor:

- kodu (`specimen.id`, "2026-0001-02": kaynak tedavinin lab no'su + sırası —
  hangi embriyo olduğu soyağacıyla okunuyor);
- tüpü (çözmenin boşalttığı taşıyıcı, v6.143);
- tüpe konduğu andaki kalitesi (önceki dondurmanın tedavisinin
  değerlendirmesi, `db.bu_tedavinin_skoru()` — v6.148'in kuralı);
- sağkalımı ve çözme ekranındaki canlılık oranı (`thaw_canlilik`);
- bu tedavide ne oldu: transfer / yeniden donduruldu.

Özet'in kutuları ve NOTLAR'ı, ART Lab'ın THAW ve TRANSFER sütunları
buradan okuyor; `dondurma_tupleri()`'nin gerekçesiyle, birbirini tutsunlar
diye.

## Embriyoloji Özet

- **ÇÖZDÜRÜLEN EMBRİYO SAYISI**: çözülen örnek sayısı.
- **ÇÖZDÜRME SONRASI VİABİLİTE**: "2 Canlı, 1 Dejenere · %90-%85" —
  sağkalım etiketleri sayılarıyla, girilmişse canlılık oranları embriyo
  embriyo. Ortalama alınmıyor: resmî forma programın hesapladığı değil,
  girilen sayı yazılsın. Kutu sağ kenarda; uzarsa küçülüyor (v6.150).
- **NOTLAR**, dondurma satırının altına:
  `Çözülen: 3 embriyo, 1 tüp (0001-0910): 2026-0001-01 3AA Canlı %90,
  transfer; 2026-0001-02 3AB Canlı %85, yeniden donduruldu; ...`
  ve `Kalan dondurulmuş: 2 embriyo, 1 tüp (0002-1430).` (yoksa "Kalan
  dondurulmuş embriyo yok."). Hastanın yumurta tüpleri ayrıca sayılıyor.
  **Ölçü bu tedavinin son işleminin anı**, bugünkü tank değil: form aylar
  sonra basılsa da o gün geriye ne kaldığını söylesin. O ana kadar
  dondurulmuş (bu tedavide yeniden dondurulan dahil), o ana kadar
  çözülmemiş örnekler.

## ART Lab

- **THAW**: FREEZE gibi dört kutu, her satır bir tüp, aynı parantez yazımı
  (`tup_metni()`): `(3AA-3AB-4BB)`.
- **TRANSFER → Uterus grade (x sayı)**: kâğıdın başlığındaki gibi kalite ve
  sayı, yanında çözmedeki canlılık: `3AA x2 · %90-%85`. Taze transferde
  çözme yok, oran da yok: `3AA x1`. Kalitesi kayıtlı değilse `?`.
- Önceden bu iki kutuda duran sayılar kalktı; sayı parantezlerden ve
  "x N"den okunuyor.

## Taşma ve küçülme artık sayfanın verisine bağlı

FREEZE'in yazısı sağdaki THAW kutusuna taşıyordu (v6.135, kullanıcının
kararı). FET'te THAW da dolu — taşan yazı onun üstüne binerdi.
`tasan_hucreleri(ad, deger)` / `sigdir_hucreleri(ad, deger)` sayfanın
dolgusuna bakıyor: FREEZE yanı boşsa taşar, doluysa küçülür; THAW hep
küçülür (sağı TRANSFER); TRANSFER taşar (sağındaki "Deselect grade"
programda tutulmuyor). Excel'de de aynı: küçülen hücre stilin kopyasıyla
`shrinkToFit`, taşan hücreyi Excel kendisi taşırıyor.

## Yazdırırken tek sayfa

Ölçüldü: kâğıdın NOTLAR kutusu iki satır boyunda ve Özet 3 satırı aşan
notta **iki sayfaya** basılıyordu (4 satır = 2 sayfa). Access'ten aktarılan
tedavilerin protokol notları zaten bunu aşıyordu; çözme satırları FET'lerde
daha da uzatıyor. `form.html`'in `baskiyaSigdir()`'i yazdırmadan önce
kâğıdı, kalıbın kendi boyuna (`data-yukseklik`) sığacak kadar `zoom` ile
bütün olarak küçültüyor — Excel'in "sayfaya sığdır"ı gibi, hiçbir satır
kesilmiyor. Yazdırma bitince geri alınıyor. 13 satırlık notta da tek sayfa.

### Deneme

Test kopyasında: ICSI → tüp A (3AA-3AB-4BB) → 2. tedavide (FET) üçü çözüldü
(%90/%85/%80), biri transfer, ikisi tüp B'ye yeniden donduruldu → 3. tedavide
tüp B çözüldü (biri %95 transfer, biri dejenere); ayrıca hastanın bir yumurta
tüpü. Özet ve ART Lab ekranda, PDF'de ve Excel'de açıldı:

- 2. tedavi Özet: "3 · 3 Canlı · %90-%85-%80", NOTLAR'da üç embriyo
  ve "Kalan dondurulmuş: 2 embriyo, 1 tüp (0002-1430); 1 yumurta, 1 tüp".
- ART Lab: FREEZE `(3AB-4BB)` (THAW dolu olduğu için küçüldü), THAW
  `(3AA-3AB-4BB)`, TRANSFER `3AA x1 · %90`.
- 3. tedavi: "1 Canlı, 1 Dejenere · %95", "Kalan dondurulmuş embriyo yok."
- Çözmesi olmayan ICSI tedavisinin formları değişmedi.
- Beş tedavinin dört çıktısı (iki form, iki Excel) hatasız; Özet PDF'i
  uzun notla tek sayfa.

Kullanıcının gerçek verisinde denenmedi (kopya yok): Access'ten aktarılan
FET'lerde çözülen embriyonun skoru ya aktarılan tüpten ya da FET'in kendi
altına açılan örneklerden geliyor (v6.148); skor kayıtlı değilse parantez
sayı ya da `?` basar.

---

# v6.153 — `teshis_form.py`: FET formunda çözme neden görünmüyor

Kullanıcı v6.152'den sonra "şu an bir şey değişmedi, formlarda görünmüyor"
dedi. Veritabanı bende yok; test kopyasında formlar doluyor. Sebep ancak
kullanıcının makinesinde görülebilir, o yüzden salt okuyan bir araç yazıldı.

Bilinen iki aday:

1. **Program yeniden başlatılmadı** (tuzak #5): formlar Python kodu,
   `git pull` programı açıkken yapılırsa eski kod çalışmaya devam ediyor.
   Araç diskteki kodun sürümünü basıyor.
2. **Çözme FET'e değil kaynak tedaviye yazılmış.** Çözme ekranı Cryo
   Haritası'ndan açıldığında "Çözme hangi tedavi için" seçimi embriyonun
   kaynak (ICSI) tedavisine düşüyor (`thaw_ekran()`: adreste `?cycle=` yoksa
   önceki kayıt, o da yoksa kaynak). Değiştirilmeden kaydedilen çözme
   ICSI'nin formunda çıkar, FET'inkinde değil — v6.152'den önce de
   "formlara işlem geçmiyor" şikâyetinin sebebi bu olabilir.

`python3 teshis_form.py` bütün çözme tedavilerini "çözme N, transfer N"
diye listeliyor ve çözmesi olmayanları işaretliyor. `python3 teshis_form.py
<tedavi no>` o tedavi için kaydedilmiş çözmeleri, transferleri, hastanın
başka tedaviye yazılmış çözmelerini ve formun göreceği değerleri basıyor.
**Transferden hemen önceki çözme** başka tedaviye yazılmışsa satır
"BU TEDAVIDE TRANSFER EDILMIS ama cozmesi ... tedavisine yazilmis" diyor;
aynı embriyonun daha önceki, doğru yazılmış çözmeleri işaretlenmiyor
(ilk yazışta işaretleniyordu, test kopyasında görüldü, düzeltildi).

Hiçbir şey değiştirmiyor, hasta adı basmıyor. İkinci sebep çıkarsa
onarım (ve varsayılan seçimin değişip değişmeyeceği) kullanıcıyla
konuşulup ayrıca yazılacak.

---

# v6.154 — FET formlarında transfer edilen embriyo

Kullanıcı: "FET tedavileri hâlâ formlara işlenmiyor." `teshis_form.py`
çıktısı gelmeden sebep, yüklenen mayıs Access dosyası bir deneme
veritabanına aktarılarak bulundu (dosya ve CSV depoya girmedi).

## Sebep

Access'teki FET satırlarında transfer edilen embriyonun hücre/aşama ve
kalitesi var (`EMBRİYO1 HÜCRE/AŞAMA` = "8H", `KALİTE` = "G1"; ya da "3" +
"BB"). `aktar_access.py` bunu FET'te **yalnızca transfer olayının notuna**
yazıyordu; embriyonun hiçbir değerlendirmesi yoktu. Resmî formlar kaliteyi
değerlendirmelerden okuduğu için:

- Özet'in EMBRİYO1/2 HÜCRE-AŞAMA ve KALİTE kutuları, EMBRİYO TRANSFER
  AŞAMASI boş;
- ART Lab'ın "Uterus grade" kutusu (v6.152) `? x2`.

Taze transferde (`_taze_transfer()`, v6.148) aynı kutular zaten
değerlendirme olarak yazılıyordu; FET'te unutulmuştu. Çözme sayısı,
canlılık ve notlar (v6.152) mayıs verisinde de doğru geliyordu —
eksik olan transfer bölümüydü.

## Düzeltme

`_fet_transfer_kalitesi()`: transfer edilen embriyolara, transfer sırasıyla,
kutudaki skor o günün değerlendirmesi olarak yazılıyor (blastokistte gün 5,
cleavage'da 3 ya da kaynağın "N.GÜN" aşaması; saat 11:00 — çözmeden sonra,
transferden önce, `db.olay_tedavisi()` onu FET'in işi saysın diye).

- **Aktarımda** kaynağa bağlamadan (`_kaynaga_bagla()`) sonra çalışıyor.
- **Dokunmadığı iki durum**: bu tedavide o tipte değerlendirmesi olan
  embriyo (ekrandan girilmiş ya da düzeltilmiş olabilir) ve kaynak
  tedavisinde **aynı günün** kaydı olan embriyo (tüpüne bağlanmış;
  değerlendirme örnek+gün başına tek kayıt, v6.146'nın açık sorunu —
  kalitesi zaten kaynağından görünüyor).
- `tamamla`'nın 6. adımı ve **dar kip `transfer`** (`iptal`'in gerekçesi:
  `tamamla` elle düzeltilmiş dondurma skorunu ezebilir, bu kip ezmez).

Özet'in "EMBRİYO TRANSFER AŞAMASI" kutusu yalnızca blastokist evresini
basıyordu; cleavage embriyosunda artık günü ("3. gün").

## Deneme (mayıs, deneme veritabanı)

- Önceden aktarılmış kopyada `transfer` kipi: 21 FET'e 30 değerlendirme
  (25 blastokist, 5 cleavage); tablolar satır satır karşılaştırıldı, başka
  hiçbir satır değişmedi. İkinci çalıştırma: "0 FET", fark yok.
- Baştan aktarım: aynı 1020 olay; ardından `tamamla` hiçbir şeyi
  değiştirmedi.
- Örnek: 3. gün FET'i — Özet "3. gün · 8 hücre G1 · 7 hücre G2", ART Lab
  THAW `(8HG1-7HG2)`, Uterus grade `8HG1 x1`, `7HG2 x1`. Blastokist FET'i —
  "3 - Tam blastokist · 3BB", `3BB x1 · %100`.
- 63 tedavinin Özet, ART Lab ve Excel çıktısı (189 adres) hatasız.

Tüpüne bağlanmış (kaynağı programda olan) embriyo yolu mayıs verisinde
yok (21 FET'in hiçbirinin tüpü programda değil); o dal yalnızca koşulla
korunuyor, gerçek veride denenmedi.

# v6.155 — IVF/ICSI'de çözme yok: çözme ayrı bir FET tedavisi

Kullanıcı: "Önce ivf/icsi tedavisi olarak başlayıp embriyosu dondurulan
hastanın daha sonra çözme yapılıp transfer edileceği FET tedavisi bir
birinden ayrı tedaviler. ivf/icsi tedavisi içinde çözme bölümü
olmamalıydı ... Embriyoloji özet formu ve art lab formuna iki tedaviyi
birleştirip yazıyor. ... bunu çöz dediğimizde FET tedavisi adı altında
yeni bir tedavi başlatması gerekiyor."

v6.152–v6.154'te FET formları düzeltildi ama kullanıcı yine "yalnızca
temmuz formlarında görünüyor" dedi. Sebep form kodu değil, **akıştı**:

- IVF/ICSI'nin aşama listesinde çözme vardı (`TIP_ASAMALARI`).
- Cryo Haritası'ndan açılan çözme ekranı hastanın **bütün** tedavilerini
  sunuyor, seçim yoksa embriyonun **kaynak** tedavisini (IVF/ICSI) seçili
  getiriyordu. Değiştirmeden kaydedilen çözme ICSI'nin kaydı oluyordu;
  sonraki transfer de ICSI'nin transfer ekranından girilebiliyordu (o ekran
  hastanın bütün embriyolarını listeliyordu).
- Sonuç: ICSI'nin Özet/ART Lab formu iki tedavinin işini birlikte basıyor,
  FET'inki boş kalıyordu. Temmuz Access'ten aktarıldığı için (araç çözmeyi
  hep FET'e yazıyor) düzgündü.

## Ne değişti

- **IVF/ICSI'nin aşamalarından çözme çıktı** (`db.TIP_ASAMALARI`). Gezinme
  çubuğunda ve tedavi ekranında yok; vitrifikasyon ekranındaki "Çözme
  ekranı" bağlantısı tipin aşamalarına bakıyor
  (`db.cozme_tedavisi_mi()`). Eski bir bağlantı `/cycle/{id}/thaw`'a
  düşerse tedavi ekranına dönülüyor. Taze transfer IVF/ICSI'de kaldı.
  Yumurta Dondurma'nın kendi çözmesine dokunulmadı (sorulacak, aşağıya bak).
- **Çözme ekranı yalnızca uygun tedavileri sunuyor**
  (`thaw_tedavi_tipleri()`): embriyo tüpü için FET / FET (3→5), yumurta
  tüpü için Yumurta Çözme (ve Yumurta Dondurma). Seçim yoksa tek açık
  (aktif) tedavi seçili geliyor; o da yoksa **boş** — kaynak tedaviye
  düşmek yok. Sunucu seçimsiz kaydı reddediyor
  (`?hata=cozme_tedavisi_sec`).
- **Çözme ekranından yeni tedavi açılıyor**: "Yeni tedavi başlat: FET"
  düğmesi (`POST /cryo/tasiyici/{id}/yeni-tedavi`). Tedavi formu
  atlanıyor — FET'in doldurulacak alanı yok denecek kadar az, protokol
  sonradan tedavi ekranından girilir. Lab kayıt no ve "kaçıncı tedavi"
  programın verdiği (tarih sırası, v6.144); ekran yeni tedavi seçili
  geri geliyor. Tip beyaz listeden geçiyor, adresten gelen metin tipe
  yazılmıyor. Aynı anda iki kişi açarsa UNIQUE hatasında sıradaki
  numarayla tekrar deneniyor.
- **Transfer ekranı tedaviye göre süzülüyor** (`transfer_adaylari(hasta,
  tedavi)`): FET tiplerinde yalnızca bu tedavi için çözülenler, IVF/ICSI'de
  yalnızca tedavinin kendi, hiç çözülmemiş embriyoları. Kayıt da aynı
  listeye karşı doğrulanıyor (eski sekme). Göç yoksa eski davranış.

## Eski kayıtlar: `cozme_ayir.py`

v6.155'ten önce IVF/ICSI'ye yazılmış çözmeleri FET'e taşıyan araç.
Varsayılanı yalnızca listelemek; `uygula` "AYIR" yazdırıp taşıyor. Grup:
aynı tedavi + aynı gün. Hedef FET sırasıyla: transferi zaten bir FET'e
yazılmışsa o (teshis_form'un bulduğu durum), o gün açılmış hiç kaydı
olmayan tek FET, yoksa yeni FET (FET (3→5) çözmeden sonra değerlendirme
varsa; yumurtada Yumurta Çözme). Taşınanlar:

- çözmenin `thaw_cycle_id`'si; sonraki çözmeye kadar ICSI'ye yazılmış
  transfer (`tr_cycle_id`) ve yeniden dondurma (`vit_cycle_id`).
  Değerlendirmeler taşınmıyor: tedavileri önceki çözmeden türetiliyor
  (`db.olay_tedavisi()`, v6.146).
- "İşlemi yapan" satırları FET'e kopyalanıyor, ICSI'de o işlem kalmadıysa
  kaldırılıyor.
- Gebelik sonucu / beta hCG / doğan bebek **yalnızca** ICSI'de başka
  transfer kalmadıysa ve FET'te yoksa taşınıyor; taze transfer + FET
  birlikteyse dokunulmuyor, rapor söylüyor (hangi gebeliğin hangisi
  olduğu klinik bir karar).
- Yeni FET transfer/dondurma ile bitmiş sayılıyor; ICSI'nin bitiş sebebi
  "transfer" kaldıysa rapor "dondurma" yapılmasını söylüyor, araç
  değiştirmiyor.
- Hiçbir satır silinmiyor, embriyo kopyalanmıyor; her değişiklik
  değişiklik geçmişine yazılıyor, tedaviler tarih sırasıyla yeniden
  numaralanıyor. Aday birden çoksa grup atlanıyor.

`teshis_form.py` IVF/ICSI'ye yazılmış çözme görürse bu aracı söylüyor.

## Deneme

- Program (deneme veritabanı): FET'i olmayan hastada çözme ekranı formu
  göstermiyor, "FET" / "FET (3→5)" düğmeleri var; düğme FET açıp ekrana
  seçili dönüyor, geçersiz tip reddediliyor; seçimsiz çözme reddediliyor;
  ICSI'nin transfer ekranı çözülen embriyoyu listelemiyor, zorla gönderilen
  kayıt yazılmıyor; ICSI'nin formu yalnızca kendi dondurmasını, FET'inki
  çözme + transfer + kalan tüpleri basıyor. Telefonda (390px) yatay kayma
  yok.
- `cozme_ayir.py` üç kurguda (transferi FET'te; hepsi ICSI'de + yeniden
  dondurma + gebelik; aynı tedavide taze transfer de var): tablolar satır
  satır karşılaştırıldı, yalnızca beklenen satırlar değişti, gebelik
  üçüncüde taşınmadı. İkinci çalıştırma üçünde de "yapılacak bir şey yok".

## Açık soru

Yumurta Dondurma'nın (`oosit_cryo`) kendi çözme aşaması duruyor.
v6.147'den beri dondurulmuş yumurta Yumurta Çözme tedavisinde çözülüyor;
aynı ayrım orada da istenir mi, kullanıcıya sorulacak.

**Cevap (2026-09-23):** "Yumurta dondurmada çözme kalkmasın." Kod
değişmedi; ayrım yalnızca IVF/ICSI için.

Aynı gün v6.146'nın açık sorusu da kapandı: "FET (3→5)'te blastokist değil
cleavage embriyosu çözülüyor." Kaynağın 5. gün kaydının üzerine yazılma
durumu klinikte doğmuyor; uyarı ya da ayrı kayıt eklenmedi.

# v6.156 — FET (3→5)'te yalnızca cleavage tüpü çözülür

Kullanıcı: "FET (3→5)'te sadece cleavage tüplerinin çözülmesine izin ver."
(Aynı gün: "FET (3→5)'te blastokist değil cleavage embriyosu çözülüyor" —
v6.146'nın açık sorusunun cevabı.)

## Kural

- **Blastokist tüpü**: içinde dondurmanın yapıldığı tedavide blastokist
  değerlendirmesi olan bir örnek var (`tasiyici_icerigi()`'nin yeni
  `blastokist` kolonu; skorla aynı kural, `db.bu_tedavinin_skoru()`).
  Skor boş olabildiği için (kavitasyon evresi) ayrı bir soru — 4. gün
  değerlendirmesi de blastokist ekranında girildiği için o tüp de
  blastokist sayılıyor.
- **Evresi bilinmeyen tüp** (hiç değerlendirmesi yok, skoru okunamamış
  eski kayıt) kapalı değil: blastokist olduğu gösterilemiyor.
- Tip listesi `db.CLEAVAGE_COZEN_TIPLER` (bugün yalnızca `fet_kultur`).
  Kapı `thaw_tedavi_tipleri()`'nde: tedavi seçici, "Yeni tedavi başlat"
  düğmeleri ve kaydetmenin doğrulaması aynı listeden geçiyor, yani sunucu
  da reddediyor.
- FET (3→5)'in çözme ekranında blastokist tüpünün "Çöz" düğmesi yerine
  "Blastokist" rozeti ve sebebi; o tedaviden tüpün çözme ekranına
  gelinirse ekranın üstünde aynı sebep.
- **Var olan kayıt dokunulmaz** (v6.139'un kuralı): bu tüpten bir FET
  (3→5) için zaten çözme yazılmışsa kapı açık kalıyor, düzeltilebilsin.

## Deneme

Deneme veritabanında bir FET (3→5), bir blastokist ve bir cleavage tüpü:
blastokist tüpü listede rozetle, düğmesiz; tüpün ekranında FET (3→5)
seçeneği ve "Yeni tedavi başlat: FET (3→5)" yok, sebep yazıyor; zorla
gönderilen çözme ve yeni tedavi isteği reddedildi, hiçbir satır yazılmadı.
Cleavage tüpü FET (3→5) için çözüldü. Var olan çözmesi olan blastokist
tüpünde FET (3→5) seçili geldi. Telefonda (390px) yatay kayma yok.

# v6.157 — Cleavage'da "Birleşme"

Kullanıcı (v6.150'deki soruya cevap): "BB birleşme başlangıcı demek.
Birleşme olarak yazılsın. Cleavage bölümüne kalitede Birleşme ekle.
Birleşme seçilince hücre sayısı kaybolsun, grade ve fragmantasyon
gözüksün. Yani embriyo kalitesi Birleşme G2 gibi olabilsin."

## Ne değişti

- **`goc_048`: `olay.cl_birlesme`** (1 = birleşme). Cleavage ekranında
  "Birleşme" düğmesi; seçilince hücre sayısı kutusu kayboluyor, sunucu
  birleşmede hücre sayısı yazmıyor (gizli kutuda kalmış değer de).
  Fragmantasyon, grade (G1–G4), bulgular, saat yerinde. **Simetri de
  yerinde** — kullanıcı yalnızca hücre sayısını saydı; birleşmede anlamı
  yoksa kaldırılması tek satır.
- **Kalitenin yazımı tek yerde: `db.cleavage_yazimi()`** — "Birleşme G2",
  grade yoksa "Birleşme". Hücre yerini okuyan sorgular
  `db.cl_hucre_ifadesi()` ile: vitrifikasyon listesi, resmî formların
  dondurma satırı (Özet NOTLAR, ART Lab FREEZE), çözülen ve transfer edilen
  embriyonun kalitesi (THAW, Uterus grade, Özet EMBRİYO1/2 "Birleşme"),
  ART Lab ızgarasının 40-45 / 72 saat hücre kutusu, tedavi Excel'i.
- Numara şeridi "3-Bir.", bilgi kartı ve silme ekranı "Birleşme".
- Otomatik A/B/C skoru hücre sayısı istiyor; birleşmede hesaplanmıyor,
  grade elle seçiliyor.
- NOTLAR satırı artık kaliteyi ve tüp parantezini ortasından bölmüyor
  (`formlar._sar()`): "(Birleşme G3)" iki satıra düşüp "(Birleşme" / "G3)"
  okunuyordu. Eski satırların sarma yeri yalnızca bir parantez ortadan
  bölünüyorsa değişir.

## Access kayıtları

- `aktar_access.py` "BB", "BİRLEŞME G1", "BİRLEŞMEG3"ü birleşme olarak
  yazıyor, grade varsa onu da (önce skorsuz embriyo, v6.148). "BİRLEŞME G1"
  boşluklu yazımı önce hiç tanınmıyordu. Tüp eşleştirmesi değişmedi:
  hücre sayısı olmayan değerlendirmenin anahtarı hâlâ "bilinmiyor".
- **Daha önce aktarılmış olanları `goc_048` düzeltiyor**, program açılınca
  kendiliğinden: notu "Kaynak kayıttaki yazım: BB" (ya da BİRLEŞME…) olan,
  hücre sayısı boş değerlendirmeler birleşme oluyor, yazımdaki grade boş
  grade'in yerine giriyor. Ekrandan girilmiş kayıtlara dokunmuyor.

## Deneme

Deneme veritabanında: göç açılışta uygulandı, aktarılmış "BİRLEŞMEG3"
→ birleşme + G3, ekrandan girilmiş hücresiz kayıt dokunulmadı. Ekrandan
birleşme G2 kaydedildi (gizli kutudaki 8 yazılmadı), birleşme kaldırılıp
6 hücre kaydedildi. Vitrifikasyon "Birleşme G3 · gün 3", ART Lab ızgarası
"Birleşme" (kutuya sığıyor: 68/68 ve 63/63 px), FREEZE "(Birleşme G3)",
Özet NOTLAR bölünmeden. Excel çıktıları 200, hata yok. Telefonda (390px)
yatay kayma yok.

# v6.158 — Birleşmede simetri de gizli; ART Lab'ın ikinci sayfası

Kullanıcı: "Simetri de gizlensin. Bir de yumurta sayısı çok olan
tedavilerde ART lab formu ikinci sayfaya geçiyor. Ama ikinci sayfayı
göremiyorum. Birinci sayfanın altında küçük bir resim olarak duruyor. Onu
birinci sayfa gibi görünür yap."

## Birleşmede simetri

v6.157'de yalnızca hücre sayısı gizleniyordu. Artık "Birleşme" seçilince
simetri kartı da kayboluyor; sunucu birleşmede simetriyi yazmıyor (gizli
kartta seçili kalmış değer de), bilgi kartı ve silme ekranı simetri
satırını basmıyor. Kalan: fragmantasyon, grade, bulgular, saat.

## Çok sayfalı formun ekranda görünüşü

Yumurta 13'ü geçince kalıp ikinci kez basılıyor (v6.37). Ekranda her kâğıt
`formlariSigdir()` ile ekrana sığdırılıyor (v6.108) ve kullanılabilir
yükseklik **o kâğıdın kendi tepesinden** ekranın altına kalan yerdi. İkinci
kâğıdın tepesi birincinin altında, kalan yer neredeyse sıfır → ikinci sayfa
küçücük bir resim gibi basılıyordu. Tek sayfalı formlarda hiç görünmediği
için v6.108'in denemesi yakalamamıştı.

Artık kullanılabilir yükseklik ilk kâğıdın **belge içindeki** tepesinden
(üst bant ve düğmeler; kaydırmadan bağımsız) ölçülüyor ve bütün sayfalar
**aynı oranla** küçülüyor: her sayfa tek başına bir ekran, birincisi gibi.
Yazdırmaya etkisi yok (`@media print` ölçeği zaten kaldırıyor).

Deneme: 17 yumurtalı bir tedavinin ART Lab'ı 1280×900, 1920×1080 ve
390×844'te iki sayfa birebir aynı boyda (ör. 718×522 / 718×522), yatay
kayma yok.

# v6.159 — Özet NOTLAR'ında kod yok, embriyo bilgisi bir kez

Kullanıcı: "Embriyoloji özet formunun notlar bölümünde bazı tedavilerde
embriyo bilgisi yazarken sadece oosit kodu yazılan tedaviler gördüm. Bir de
bazı tedavilerde de embriyo bilgisi iki kere yazılıyor. ... Yazı kod
yazmasın. Tüp içinde embriyo bilgisi parantez ile belirtilsin. Embriyo
bilgisi tek sefer yazılsın, ikinci kere tekrar etmesin."

Mayıs aktarımının deneme kopyasında 63 tedavinin NOTLAR'ı basılıp
bakıldı; üç ayrı sebep çıktı:

1. **Kod** — v6.152'nin "Çözülen:" satırı her embriyoyu örnek koduyla
   yazıyordu ("2026-0004-01 8HG1 Canlı, transfer"). Artık tüp tüp parantez,
   "Dondurulan:" satırıyla aynı yazım: "Çözülen: 2 embriyo, 1 tüp:
   (8HG1-7HG2); 2 transfer". Sağkalım ve canlılık zaten ÇÖZDÜRME SONRASI
   VİABİLİTE kutusunda; ne olduğu sayıyla.
2. **İki kez** — Access'ten aktarılan tedavinin protokol notu dondurmayı
   kendi cümlesiyle anlatıyor ("2 ADET D3 EMBRİYOSU (8HG1-8HG1) ŞEKLİNDE
   DONDURULARAK SAKLANDI") ve v6.135'in "Dondurulan:" satırı aynı tüpleri
   yeniden yazıyordu. Aktarımın o nottan yazdığı dondurmalar bir notla
   işaretli (`db.KAYNAK_DONDURMA_NOTU`); notu Access kaydı olan tedavide o
   tüpler "Dondurulan:" satırına girmiyor. Programda dondurulan tüpler
   yazılıyor. Denemede 32 satırın 32'si Access notunun tekrarıydı.
   "Kalan dondurulmuş:" da bu tedavide dondurulan tüpleri artık tekrar
   etmiyor ("bu tedavide dondurulan 1 tüp"), ötekileri etiketle (kod)
   değil içindekiyle yazıyor.
3. **Yanlış "yok"** — "Kalan dondurulmuş embriyo yok." aktarılmış FET'lerde
   de basılıyordu; oysa kaynak tüpler programda değil (notun kendisi "GERİDE
   7 TÜPTE 7 ADET D5 EMBRİYOSU KALDI" diyor). Çözülen bir embriyonun
   dondurması programda yoksa satır artık hiç yazılmıyor.

ART Lab'ın FREEZE/THAW/TRANSFER kutuları değişmedi (notu yok, tekrar yok).

Deneme: mayıs kopyasında 63 tedavide NOTLAR'da tek bir örnek kodu kalmadı;
programda girilmiş bir FET'te (çözme, transfer, yeniden dondurma, tankta
başka tüp) "Dondurulan: 1 embriyo ... (4AA)", "Çözülen: 2 embriyo, 1 tüp:
(4AA-4AA); 1 transfer, 1 yeniden donduruldu", "Kalan dondurulmuş: 2
embriyo, 2 tüp: bu tedavide dondurulan 1 tüp, (1)".

---

# v6.160 — ocak–mayıs 2025 Access kayıtları; `bagla` kipi

Kullanıcının isteği: *"şimdi 2025 yılına geçiyorum. Bu kayıtları daha önce
belirlediğimiz gibi programa yerleştir."* Beş dosya (ocak, şubat, mart,
nisan, mayıs 2025), 2026'nınkilerle aynı yapıda: tek tablo `VERİTABANI`,
92 kolon; 89 + 66 + 84 + 69 + 109 = 417 satır. `.accdb` v6.149'daki gibi
`mdb-export` ile CSV'ye çevrildi. Kaynak dosyalar, CSV'ler ve tarih
düzeltmesi depoya girmedi; aşağıda yalnızca sayılar var.

## Etiketler yıl taşıyor

2026 `OCAK` … `TEMMUZ` etiketleriyle aktarıldı. 2025'in dosyaları aynı adı
alsaydı ilk satırları 2026'nın aynı numaralı satırlarıyla çakışırdı (araç
durur, v6.141). 2025 için `kaynak=OCAK2025` … `MAYIS2025`.

## Bir tarih düzeltmesi

Ocak 2025'te bir **Yumurta Çözme** satırının OPU TARİHİ 07.11.2022. Öteki
yumurta çözme satırları o alana çözme gününü yazıyor; bu satırınki büyük
olasılıkla yumurtaların toplandığı gün. Olduğu gibi aktarılsaydı tedavinin
lab numarası 2022-… olur ve hastanın tedavi sırası 2022'ye kayardı. Kayıt
Access'te 3 ve 6 ocak kayıtlarının arasında girilmiş: v6.148'in kararıyla
("yakın kaydın tarihi") 03.01.2025'e düzeltilmesi önerildi, `duzelt=` ile
(not "07.11.2022 yazıyordu, 03.01.2025 olarak düzeltildi" diyor).
Öteki 416 satırın tarihi kendi ayında; iki satır tarihsiz ("yaklaşık").

## Aracın iki düzeltmesi (yalnızca yumurta dondurma notları)

**1. "N ADET M2 OOSİT 1 TÜPTE" okunmuyordu.** Parantez grubu olmayan
dondurma v6.148'den beri yalnızca tek örnekse yazılıyordu: birden çok
örneğin tüplere dağılımı bilinmiyor. Tüp sayısı 1 yazıyorsa dağılım
bellidir. İki satır (5'er yumurta) artık tek tüp olarak yazılıyor.
Tüp sayısı yazmayan ("2 ADET M2 OOSİT DONDURULARAK SAKLANDI", bir satır)
ve olgunluğu karışık olan (M1 ile M2 birlikte, sayısız) hâlâ yazılmıyor,
uyarı çıkıyor.

**2. Olgunluğu kaynakta hiç sayılmamış yumurta dondurulamıyordu.** Bir
Yumurta Dondurma satırında 1 yumurta toplanmış, MII/İMMATÜR kutuları boş,
not "1 ADET OOSİT DONDURULARAK SAKLANDI. (M1-M2 ? ZONAFREE)". Dondurma
havuzu yalnızca MII ya da MI kaydı olan yumurtaya bakıyordu; tank tüpü
programa hiç girmeyecekti. Havuza, kaynağın sayılarının (MII + immatür +
empty zona + dejenere + atretik) ÖTESİNDEKİ yumurtalar eklendi; olgunluğu
boş kalıyor, rapor söylüyor. **Empty zona dışarıda**: onlar da maturasyon
kaydı olmadan açılıyor (`_oositleri_ac()`), ilk yazışta havuza girdiler ve
denemede empty zona iki "yumurta" dondurulmuş yazıldı. Sınır bu yüzden
sayıların ötesi.

Gerileme: 2025'in beş dosyası ve 2026 mayıs, eski ve yeni araçla `liste`
çıktısı karşılaştırıldı — fark yalnızca bu iki satırda.

## `bagla` kipi

2026'nın ayları kullanıcının makinesinde zaten aktarılmış. 2026 FET'lerinin
bir kısmı 2025'te dondurulan embriyoyu çözdü; aktarıldıkları gün tüp
programda yoktu, embriyolar FET'in kendi altında kaldı (v6.130) ve tüp
2025'ten sonra Cryo Haritası'nda "dolu" görünecekti. `tamamla` bağlıyor
ama dondurma skorlarını nottaki değerle yeniden yazıyor — aylar önce
aktarılmış tedavide elle düzeltilmiş bir skoru ezer (v6.142). `bagla`
`tamamla`'nın 4. adımını (`_kaynaga_bagla()`) tek başına çalıştırıyor,
`iptal`/`transfer` kiplerinin deseni. 2026'nın ayları eskiden yeniye,
ilk aktarımdaki etiketle.

## Deneme (test veritabanının kopyasında)

Kullanıcının veritabanı bu oturumda yoktu; deneme mayıs 2026'nın aktarıldığı
test kopyasında yapıldı.
- Beş ay sırayla: 417 tedavi, 0 hata. 313 yeni hasta; aynı dosya numaralı
  hastalarda 2025 tedavileri 2026'nınkinden önce numaralandı
  (`1: 2025-…, 2: 2026-…`).
- FET'in kaynağa bağlanması 2025 içinde: 27 FET 2025'te dondurulan tüpüne
  bağlandı, 139'unun tüpü programda yok (2025'ten önce dondurulmuş), 10'u
  "elle bakılmalı" (2'si belirsiz, 8'inde tüpteki sayı/skor tutmuyor).
- `bagla kaynak=MAYIS` (2026): 2 FET 2025 tüpüne bağlandı; ikinci
  çalıştırma tablo tablo karşılaştırıldı, hiçbir satır değişmedi.
- 2025'in 417 tedavisi + bağlanan iki FET: tedavi ekranı, iki resmî form,
  Excel dökümleri, vitrifikasyon/çözme/transfer ekranları, Cryo Haritası,
  istatistik — 3358 istek, hepsi 200. NOTLAR'da örnek kodu yok, "Dondurulan"
  hiçbirinde iki kez yok (v6.159).
- `teshis.py`, `tarih_duzelt.py`: bozuk tarih yok.

## Bilinen / yazılmayan

- **Kaynağın olgunluk sayısı notla tutmuyor, iki satır.** Yumurta
  Dondurma'da MII 4 / immatür 3 ama not 6 M2 + 1 M1 donduruyor; bir
  başkasında MII 3 / immatür 6, not 5 M2. Kullanıcıya soruldu — v6.161.
- Tüp sayısı yazmayan bir yumurta dondurması (2 yumurta) yazılmadı —
  v6.161.
- v6.148'deki "Parantezsiz iki dondurma" kararı değişmedi.

---

# v6.161 — ART Lab'da FREEZE ikinci kâğıtta devam ediyor; iki aktarım cevabı

## ART Lab: dördü aşan tüp ikinci kâğıtta

Kullanıcının isteği: *"Dondurulan embriyo tüp 3'ten fazla ise ART Lab
formunda freeze yerine tamamı sığmayınca +1 veya +2 şeklinde yazılmış.
Halbuki ikinci kâğıt var, orada freeze bölümünde devam etsin."*
FREEZE sütununun dört kutusu var (v6.135); dördü aşınca son kutu kalanı
sayıyla söylüyordu ("+2 tüp"), yani ekranda üç tüp + sayı görünüyordu.
Artık liste kırpılmıyor (`artlab_verisi()`), `artlab_dolgu()` her sayfaya
dörder tane dağıtıyor: 5.–8. tüp ikinci kâğıdın aynı kutularında. THAW ve
TRANSFER'in dört kutusu da aynı kuralla (v6.152'den beri aynı "+N"
davranışı vardı). Oosit 13'ü geçmese de dördü aşan tüp ikinci kâğıdı
açıyor — kâğıtta da öyle doldurulurdu. Özet bloğunun öteki kutuları ve
işlem saatleri hâlâ yalnızca ilk kâğıtta.

Deneme (2025 aktarımının kopyası, 482 tedavi): ART Lab dolgusu eski ve yeni
kodla karşılaştırıldı, yalnızca dörtten çok tüpü olan 10 tedavi değişti.
8 tüplü bir tedavinin ikinci kâğıdında 5.–8. tüpler ekranda görüldü; bu 10
tedavinin form sayfası, Excel'i ve Özet formu 200.

## Aktarım: kullanıcının iki cevabı

**"2 ADET M2 OOSİT DONDURULARAK SAKLANDI tek tüptür."** Yumurta dondurma
notunda tüp sayısı hiç yazmıyorsa artık tek tüp (v6.160 yalnızca "1 TÜPTE"
yazanı tek tüp sayıyordu). Embriyoda varsayılmıyor; "2 TÜPTE 4 ADET" gibi
çok tüplü ama dağılımı yazmayan not hâlâ yazılmıyor.

**Olgunluk sayısı notla tutmuyorsa: "yanlış yazılmıştır, en son yazılanı
kullan".** En son yazılan dondurma notu. `olgunlugu_nottan_duzelt()`
satırlar okunduktan sonra çalışıyor: notun M2 sayısı MII'den çoksa fark
immatürden MII'ye geçiyor (toplam değişmiyor), protokol notu "Access'te MII
4, immatür 3 yazıyordu; dondurma notuna göre MII 6, immatür 1 alındı"
diyor, `liste` satırı "[MII 4 → 6, nottan]". İki satırda uyarı kalktı,
tüpler notun sayısıyla yazıldı. Yalnızca yumurtanın bu tedavide toplandığı
tiplerde; immatür yetmezse fark eksik kalır ve dondurma uyarısı çıkar.

**Dar kip `dondurma`.** 2026'da da (v6.148) "2 ADET M2 OOSİT" bir satır
vardı, tüpü yazılmadı. `tamamla` yazardı ama öteki tedavilerde elle
düzeltilmiş skorları ezer; `dondurma` yalnızca bu tedavide taşıyıcılı hiç
dondurması olmayan satıra yazıyor. v6.160 ile aktarılmış 2025 kopyasında
beş ay geçirildi: yalnızca o satıra bir tüp açıldı; ikinci çalıştırma
tablo tablo karşılaştırıldı, hiçbir şey değişmedi. Not–MII düzeltmesi
aktarılmış tedaviye uygulanmıyor (yumurtalar aktarım anında açılıyor).

Gerileme: 2025'in beş dosyası ve 2026 mayıs, `liste` çıktısı eski ve yeni
araçla karşılaştırıldı — fark yalnızca bu üç satırda. Baştan aktarım
(beş ay): 417 tedavi, 0 hata; tek uyarı olgunluğu kaynakta hiç yazılmamış
yumurtanın bilgisi.

---

# v6.162 — Yönetici panelinde çalışan program sürümü

Kullanıcı: *"Hâlâ +2 tüp yazıyor."* v6.161'den sonra ART Lab'ın FREEZE
kutusuna "+N tüp" yazan hiçbir kod kalmadı (arandı; test sunucusunda 8 tüplü
tedavinin 5.–8. tüpü ikinci kâğıtta görüldü). Kullanıcının programı eski
kodla çalışıyordu: `git pull` yapılmamış ya da program yeniden
başlatılmamış — tuzak #5, formun verisi Python'da (`formlar.py`) ve Python
yalnızca açılışta okunuyor.

Her seferinde tahmin etmemek için Yönetici paneline **Program sürümü**
kartı eklendi (`app.kod_surumu()`): README'deki en büyük "# v6.xxx"
başlığı, açılışta bir kez okunuyor (`CALISAN_SURUM`) ve panel her açıldığında
diskteki yeniden okunuyor. İkisi farklıysa kart "Program güncellendi ama
yeniden başlatılmadı" diyor. `git pull` yapılmadıysa ikisi de eski sürümü
gösteriyor — kullanıcı sürümü sohbetteki numarayla karşılaştırabiliyor.
README paketlenmiş kurulumda yoksa kart basılmıyor. Panel salt okunur
kaldı (v6.12).

---

# v6.163 — Aktarılmış bütün FET'ler tüpüne kendiliğinden bağlanıyor

Kullanıcının isteği: *"Aktardığım bütün tedavileri birbirine bağla. 2025'te
dondurulmuş embriyoları 2025 yılının ileri tarihinde ve 2026'da çözmüş
olabilirim. Ben her yeni aktarım yaptığımda eski kayıtlardan bağlantılı
hasta varsa tedavileri bağla."* 2025 ocak–mayıs ve 2026'nın tümü zaten
aktarılmış; 2026 önce aktarıldığı için 2026 FET'lerinin 2025 tüpleri o gün
programda yoktu.

## Ne değişti

- **`butun_fetleri_bagla()`**: veritabanında hâlâ kendi embriyolarını
  taşıyan (tüpüne bağlanmamış) bütün aktarılmış FET'leri, çözme tarihi
  sırasıyla `_kaynaga_bagla()`'dan geçiriyor. CSV istemiyor: eşleştirmenin
  ihtiyacı olan transfer yazımı transfer olayının notunda duruyor
  ("Embriyo: 3AA", `_vt_satiri()`).
- **Her aktarımın sonunda kendiliğinden** (`aktar()`): önce yeni dosyanın
  FET'leri (eskisi gibi), sonra bütün eski FET'ler. Özet satırı kaç FET'in
  bağlandığını ve kaçının tüpü programda olmadığını söylüyor.
- **`bagla` kipi dosyasız**: `python3 aktar_access.py bagla` — zaten
  aktarılmış aylar için bir kez. Eski yazım (`bagla kaynak=X x.csv`) da
  çalışıyor, dosya yok sayılıyor.
- **Sonradan bağlanan FET'in transfer değerlendirmesi**: v6.154 FET'te
  transfer edilen embriyonun kalitesini o günün değerlendirmesi olarak
  yazıyor, ama tüpüne bağlı embriyoya (kaynağında aynı gün kaydı varsa)
  yazmıyordu. Önce yazılıp sonra bağlanan FET'te iki kayıt çakışırdı; artık
  bağlanırken FET'inki iptal ediliyor. Sonuç tarih sırasıyla aktarılmışla
  aynı (denendi).

## Deneme (mayıs 2026 aktarılmış test kopyası + 2025'in beş ayı)

- **Tarih sırasıyla** (ocak→mayıs): 29 FET bağlandı (27'si 2025 içinde,
  2'si 2026 mayıs FET'i 2025 tüplerine).
- **Ters sırayla** (mayıs→ocak, kullanıcının durumuna benzer): 30 FET
  bağlandı. Bağlanan tüpler Access kayıt numarasıyla karşılaştırıldı:
  29'u birebir aynı. Fark tek FET: tarih sırasında iki tüp seçeneği vardı
  ("belirsiz", bağlanmadı); ters sırada öteki seçeneğin ayı henüz yoktu ve
  tek tutan tüpe bağlandı. **Bilinen sınır**: bağ sonradan gelen bir tüp
  yüzünden geri alınmıyor. Mümkünse dönemler eskiden yeniye aktarılmalı.
- Transfer günü değerlendirmeleri iki sırada da aynı (iptal edilenler hariç
  tutulunca birebir).
- İkinci `bagla`: tablo tablo karşılaştırıldı, hiçbir şey değişmedi.

---

# v6.164 — haziran–ekim 2025 Access kayıtları; dondurma notunun yedi okuması; FET bağlamada aktarılmamış ay

Kullanıcının isteği: *"2025'in mayısa kadar aktarmıştım. Şimdi bu ayları
aktar."* Beş dosya (haziran, temmuz, ağustos, eylül, ekim 2025), öncekilerle
aynı yapıda: tek tablo `VERİTABANI`, 92 kolon; 40 + 113 + 95 + 74 + 82 = 404
satır. Üç satır boş (yalnızca kimlik numarası), atlanıyor. `.accdb` v6.149'daki
gibi `mdb-export` ile CSV'ye çevrildi; kaynak dosyalar, CSV'ler ve tarih
düzeltmesi depoya girmedi, aşağıda yalnızca sayılar var.

## Dosyalar

- Etiketler `HAZIRAN2025` … `EKIM2025` (v6.160'ın kuralı: yıl taşıyor).
- **Ağustos dosyasının son 18 kaydı 22–30 Eylül tarihli.** Eylül dosyası
  2–24 Eylül'ü kapsıyor; ayın sonu ağustos dosyasına girilmiş. İki dosyada
  aynı dosya no + aynı gün olan hiçbir satır yok, yani tekrar değil: kendi
  eylül tarihleriyle aktarılıyorlar.
- **Üç yazım hatalı tarih** (ağustos dosyası) `duzelt=` ile düzeltiliyor,
  v6.148'in kararıyla: iki FET'in transfer tarihi (19 Temmuz → 19 Ağustos,
  27 Mayıs → 27 Ağustos) ve bir OPU (29 Haziran → 29 Eylül). Üçü de
  Access'te komşu kayıtlarının arasında girilmiş, yalnızca ay rakamı tutmuyor.
  Hiçbiri kendi ayının dosyasında yok. 27 Mayıs yazan FET'in hastasının
  OPU'su 1 Temmuz 2025'te; düzeltilmiş tarihle FET o temmuz tüpünü çözüyor.
- Tarihsiz bir satır bir önceki kaydın tarihini alıyor (v6.148).

## Aracın düzeltmeleri — yedisi de sessizdi

Hepsi bu dosyaların gerçek satırlarından; hiçbirinde araç uyarmıyordu.

1. **"REFREEZ YAPILARAK DONDURULDU"** (iki FET): "YAPILARAK" fiil sanıldı,
   skor fiilin arkasında arandı, bulunamadı ve yeniden dondurulan tüp hiç
   yazılmadı. "REFREEZ YAPILARAK" / "REFREEZ YAPILAN" artık niteleme;
   fiil arkadaki "DONDURULDU".
2. **"GERİYE 1 ADET REFREEZ YAPILAN D5 EMBRİYOSU (KAVG2) ŞEKLİNDE
   DONDURULDU"** (bir FET, 3 çözme, 1 transfer, DONDURULAN boş): v6.148'in
   stok kuralı ("GERİDE/GERİYE" + DONDURULAN 0 → önceki dondurmadan kalan)
   bunu atlıyordu. Cümle REFREEZ diyor ve fiili bitmiş ("DONDURULDU",
   "SAKLANDI", "EDİLDİ"): bu tedavide yapılmış bir yeniden dondurma. Stok
   cümlesi "SAKLANMIŞTIR" / "KALDI" der, ona dokunulmadı.
3. **Bir notta iki gün** (beş satır): "2 ADET D3 EMBRİYOSU (8HG3-10HG2)
   2 ADET D5 EMBRİYOSU (3CC-1CC)". Araç notun ilk gününü bütün tüplere
   veriyordu: D5 tüpü OPU + 3'te dondurulmuş, blastokistleri 4. gün
   değerlendirmesi. Artık her grubun günü önündeki son işaret (`_son_gun()`),
   işaretsiz grup bir öncekinin gününde; dondurma saati ve değerlendirme günü
   grup grup. Tek günlü notta hiçbir şey değişmedi.
4. **Aynı tüp iki kez** (bir satır): not "19 ADET D3 EMBRİYOSU" ve
   DONDURULAN 19, ama beş parantez grubu 24 embriyo tutuyor; ikinci ve
   dördüncü grup birebir aynı (kopyala-yapıştır). Araç tankta olmayan beşinci
   bir tüp yazıyordu. İki bağımsız sayı (notun ADET'i ve DONDURULAN)
   tekrarı çıkarınca tam tutuyorsa tekrar düşüyor, not bunu söylüyor. Aynı
   içerikli iki tüp olağan ("(4AA) (4AA)"); sayılar tutuyorsa hiçbir şey
   değişmiyor. Yalnızca embriyoda: yumurta satırında DONDURULAN embriyo sayısı,
   ikinci sayı yok.
5. **Yumurta yazım hataları** (üç satır): "(4-M2)" (tire sayıyı olgunluktan
   ayırıyor), "1*1" ("M" düşmüş), "1M*1" (yıldız yer değiştirmiş). Tanınmayan
   parça atılıyordu, tüpe 4 yerine 1, 4 yerine 3, 5 yerine 4 yumurta
   yazılıyordu. Üçü de artık okunuyor; yalnızca yumurta notunda.
6. **Okunamayan embriyo yazımı** ("(8HGT1-6HG3-8HG3)", bir satır): "8HGT1"
   tanınmadığı için tüpe 3 yerine 2 embriyo yazılıyordu. Rakamla başlayan
   ama okunamayan yazım artık **skorsuz embriyo**: sayı tutuyor, skor
   uydurulmuyor, yazım değerlendirmenin notunda, ekrandan düzeltilebilir.
   Rakamla başlamayan tanınmayan parça hâlâ yazılmıyor ama artık UYARI
   çıkıyor, `liste` de "TANINMADI" diyor.
7. **ICSI sayısı boş, döllenme sonuçları dolu** (bir satır): yöntem ICSI,
   MII 8, 2PN 7, intakt 1, İŞLEME ALINAN boş. ICSI yazılmayınca 2PN de
   açılmıyor, dondurulan 6 embriyonun 4 tüpü Cryo Haritası'na hiç girmiyordu.
   2PN + intakt + anormal + işlem sonrası dejenere enjeksiyonun
   sonuçları; toplamları enjekte edilen sayının kendisi, uydurma değil
   (`icsi_sayisini_tamamla()`). Not "ICSI sayısı Access'te boş" diyor.
   Döllenme sonucu da yoksa ICSI yine yazılmıyor.

Kaynağın kendi tutarsızlığı olan üç satır olduğu gibi kaldı, rapor UYARI
diyor: bir yumurta dondurmasında not "11 ADET" diyor, gruplar 12; bir embriyo
dondurmasında 5 embriyo, 4 2PN; bir yumurta dondurmasında "6 ADET", gruplar 8
(MII 4). Fazlası yazılmıyor.

"4BA TA" gibi skorlar (temmuzda 17, ağustosta 2 satır): skor okunuyor,
"TA" değerlendirmenin notunda kalıyor. Anlamı kullanıcıya soruldu.

## FET bağlama: aktarılmamış ay

v6.163 her aktarımın sonunda bütün aktarılmış FET'leri **o an programda olan**
tüplerle bağlıyor. Kullanıcının makinesinde asıl durum "ters sıra": 2026
aktarılmışken 2025 ay ay geliyor. Haziran 2025 aktarılınca bir 2026 FET'i
için tek tutan tüp haziranda görünür; gerçek tüpü eylülde olsa bile bağlanır
ve eylül gelince bağ geri alınmaz. v6.163'ün README'si bunu "bilinen sınır"
diye yazmıştı. Kullanıcının veritabanının kopyasında (v6.148 provası)
ocak–haziran 2026 v6.163 koduyla baştan aktarılınca bir temmuz FET'i böyle
bağlandı: tarih sırasıyla iki tüpü (şubat, nisan) tutan, v6.148'de "belirsiz"
kalan FET, şubat aktarıldığında nisan tüpü henüz yokken şubat tüpüne
bağlandı. O satır dışında sonuç v6.148'inkiyle birebir aynıydı.

- **Erteleme**: tutan tüp ile çözme arasında programda hiç tedavisi olmayan
  bir ay varsa (dosyası gelmemiş) bağlanmıyor, rapor "ertelendi" diyor ve
  ayları yazıyor. O ay aktarılınca her aktarımın sonundaki deneme
  kendiliğinden yeniden bakıyor (`_aktarilmamis_aylar()`). "Hastanın tüpleri
  tutmuyor" da arada boş ay varsa "elle bak" değil "ertelendi": gerçek tüp o
  ayda olabilir.
  - Ölçü **tedavinin günü** (`db.tedavi_tarihi()`), olayların günü değil:
    ekimin son OPU'larının 5. gün dondurmaları kasıma düşüyor, kasım dosyası
    gelmeden ay dolu görünürdü (denemede görüldü).
  - Bir ay ancak en az 10 tedavisi varsa aktarılmış sayılıyor
    (`_AY_EN_AZ_TEDAVI`): kullanıcının veritabanında programdan girilmiş iki
    tedavi, dosyası hiç gelmemiş bir ayı dolu gösteriyordu. Aktarılan aylar
    20 ile 130 tedavi arası.
- **Yeniden sınama**: bağlı FET'ler her seferinde bugünkü tüplerle
  sınanıyor (`_baglantilari_yeniden_sina()`); başka bir tüp de tutuyorsa
  "Bağlı ama artık kesin değil" listesine iki tüple giriyor. **Bağ
  çözülmüyor**: FET'in kendi örnekleri silindi, tüpün yeri elle girilmiş
  olabilir; kullanıcı kâğıttan bakıyor ("belirsizi listele", v6.148).
  v6.163'le daha önce yapılmış erken bağları da böyle buluyor.
- Aday araması `_bag_siniflari()`'na ayrıldı: bağlama ve yeniden sınama aynı
  kuralı kullansın diye.
- **Bilinen sınır**: en eski aktarılmış aydan önceki bir tüp (ör. 2024)
  programda yok; o dönem aktarılınca yeniden sınama söyler.

## Deneme

Kullanıcının veritabanının kopyasında (v6.148 provası; mayıs 2026 ve
ocak–mayıs 2025 bu oturumda yok):

- Beş ay tarih sırasıyla: 404 tedavi (163 FET, 179 IVF/ICSI, 53 Yumurta
  Dondurma, 9 Yumurta Çözme), 0 hata, 430 tüp. Dosyaların kendi FET'lerinden
  36'sı 2025 tüplerine bağlandı. 35 FET ertelendi: kasım–aralık 2025, bu
  kopyada mayıs 2026 da yok. Kullanıcının makinesinde mayıs var, orada
  erteleme yalnızca kasım–aralık 2025 yüzünden.
- Yeniden sınama yukarıdaki erken bağlanmış temmuz FET'ini iki tüpüyle
  listeledi.
- İkinci çalıştırma: beş dosyanın yeniden aktarımı (hepsi atlandı),
  `tamamla` ve `bagla`; tablolar satır satır karşılaştırıldı, hiçbir şey
  değişmedi. Bütünlük kontrolleri temiz (yabancı anahtar, boş "dolu" tüp,
  çift çözme, çift transfer, tekrarlanan tedavi no).
- Düzeltilen satırlar aktarımda doğrulandı: yumurta tüpleri 4+3, 5, 4+3;
  19 embriyo 4 tüpte; ICSI'si boş satırın 6 embriyosu 4 tüpte; iki gün
  notlarında D3 tüpü OPU + 3'te, D5 tüpü OPU + 5'te, bir satırda D6
  blastokisti 6. gün.
- Gerileme: 2026'nın yedi dosyası ve 2025'in beşi, eski ve yeni araçla
  `liste` (boş veritabanında). 2026'da tek fark temmuz 2026'daki bir satırın
  gün gösterimi (aşağıda); 2025'te yalnızca hedeflenen satırlar.

## Bilinen / yazılmayan

- **Temmuz 2026'nın zaten aktarılmış bir satırında da iki günlü not var**
  (D2 + D5): orada iki blastokist 4. gün değerlendirmesi olarak duruyor. Bu
  sürüm onu kendiliğinden değiştirmiyor. `tamamla kaynak=TEMMUZ` düzeltir,
  ama o ayda ekrandan elle düzeltilmiş skorları nottakiyle ezer (v6.142).
  Ekrandan düzeltmek de mümkün.
- Kasım–aralık 2025 henüz gelmedi: gelene kadar 2026 FET'lerinin 2025
  tüplerine bağlanması erteleniyor.

# v6.165 — kasım–aralık 2025 ve ocak–mart 2024 Access kayıtları; eksik parantez, bitişik skor; şubat 2026'nın eksik tüpü

Kullanıcının isteği: *"2025 son ayları ve 2024'ün ilk üç ayını da aynı şekilde
ekle."* Beş dosya (kasım, aralık 2025; ocak, şubat, mart 2024), öncekilerle
aynı yapıda: tek tablo `VERİTABANI`, 92 kolon; 77 + 112 + 115 + 82 + 97 = 483
satır. Mart dosyasının bir satırı boş (yalnızca kimlik numarası), atlanıyor:
482 tedavi. Kaynak dosyalar, CSV'ler ve tarih düzeltmesi depoya girmedi,
aşağıda yalnızca sayılar var.

## Dosyalar

- Etiketler `KASIM2025`, `ARALIK2025`, `OCAK2024`, `SUBAT2024`, `MART2024`.
  Dosya adlarında yıl yok; yıl tarihlerden okundu. Her dosya kendi ayını
  kapsıyor.
- **Dört yazım hatalı tarih** `duzelt=` ile düzeltiliyor (v6.148'in kararı):
  - Üçü bir ayın dosyasının ilk kayıtları. Tarih, komşu kayıtlarla aynı gün
    numarasını taşıyor ama bir önceki ayda: mart dosyasında 4 Şubat (FET),
    kasımda 3 Ekim (OPU), aralıkta 1 Kasım (FET). Ay başında eski ayın rakamı
    yazılmış. İkisi hafta sonuna düşüyor; dosyalardaki işlemlerin %2'sinden
    azı hafta sonunda. Önceki ayın dosyasında bu üç hastanın o güne yakın bir
    kaydı yok. Düzeltilmiş üç tarih de pazartesi.
  - Dördüncüsü yıl hatası: aralık dosyasının son kaydında OPU 30.12.2026,
    yani henüz gelmemiş bir gün.
- Şubat 2024 dosyasında bir OPU 1 Mart tarihli: komşuları 26–28 Şubat, gün
  numarası da tutmuyor, yani "ay rakamı" hatası deseni değil. Mart dosyasında
  da yok. Olduğu gibi (1 Mart) aktarılıyor.
- Tarihsiz beş satır bir önceki kaydın tarihini alıyor (v6.148).

## Aracın düzeltmeleri

Hepsi bu dosyaların gerçek satırlarından. İlk dördünde araç ya hiç uyarmadan
eksik yazıyordu ya da örneği "tanınmadı" diye atıyordu.

1. **Ayırıcısız yazılmış skorlar** (iki satır): "(BBG2-8HG1-10HG28HG2)" ve
   "(8HG16HG2-5HG2-7HG3)" ("10HG2" + "8HG2", "8HG1" + "6HG2"). `_skor_coz()`
   baştaki skoru tanıyıp arkasına bakmıyor: "8HG1BB", "4BA TA", "10HG1OVAL"
   gibi nitelemeler için bilerek böyle. Arkadaki embriyo tüpe hiç
   yazılmıyordu. Arkası rakamla başlıyor ve kendisi de skor olarak
   okunuyorsa artık ayrı embriyo (`_bitisik_ayir()`); nitelemeler eskisi gibi.
   **Aynı hata şubat 2026'da da vardı**, aşağıya bak.
2. **"BBG1" / "BB G2" ve "BİRG1" / "BİRG2"** (üç satır, 6 embriyo): birleşme +
   grade. "BB" v6.157'de kullanıcının cevabı (birleşme başlangıcı), grade'li
   yazımı tanınmıyordu. "BİR", BİRLEŞME'nin kısaltması sayıldı ve bu
   kullanıcıya bildirildi. "BİR" tek başına tanınmıyor, yalnızca grade'iyle:
   Türkçede "bir" sayı da demek.
3. **Eksik parantez** (üç satır):
   - "(3AB) (3BB (3BC) (3BA) ...": ")" unutulmuş, "3BB" ayrı bir tüp.
   - "(4AA-4AA) 4AA-3AA) (1AA-3BC)" ve "24 ADET D3 EMBRİYOSU
     5HG2-8HG1-6HG2-8HG1) (...": "(" unutulmuş.

   Kural, parantezin dışında kalan parçanın bütün öğeleri tanınıyorsa o
   parçayı tüp saymak. "((4CB-1BB)" ve "D3 (EMBRİYOSU (8HG1-10HG2)" gibi
   eski dosyalardaki yazım hataları değişmedi: önceki parça boş ya da skor
   değil.
4. **"1 TÜPTE84*M2)"** (üç yumurta satırı): "(" yerine shift'siz "8"
   basılmış; Türkçe klavyede "(" Shift+8. Grup açılmadığı için iki tüp
   hiç yazılmıyordu. Yalnızca "TÜPTE"den hemen sonra, ardından rakam gelirse
   ve ")" "(" açmadan kapanırsa uygulanıyor.
5. **Kaynağın sayısı tüplerden çoksa UYARI** (yeni): "10 ADET D5 EMBRİYOSU
   (4AA) (4AA) (3AA-2BB) (KAVG1-KAVG1) (KAVG1-KAVG1)" ve DONDURULAN 10, ama
   tüplerde 8 embriyo var. Eksik ikisinin tüpü ve skoru bilinmiyor, uydurulmuyor.
   Ama tankta duran embriyo programda görünmeyecek, bu yüzden söyleniyor
   (v6.142'nin kuralı). Embriyoda iki sayının büyüğü alınıyor: günü karışık
   notta ADET yalnızca ilk günün sayısı. Yumurtada yalnızca notun ADET'i
   alınıyor. `liste` de söylüyor.
6. **"İLE TOPLAM 6 TÜPTE 20 ADET EMBRİYOSU KALDI"** artık "İLE BİRLİKTE"
   gibi durak: arkası hastanın bütün stoku. Gruplar değişmiyor, yalnızca
   5. maddenin uyarısı "20" sayısını dondurulan sanmıyor (ağustos 2025'te
   bir satır).

## Şubat 2026'nın bir tüpü: `dondurma` kipi eksiği de ekliyor

Şubat 2026 dosyasının bir satırı "(BB 10HG3 8HG3 8HG2)( 8HG2 8HG2 8HG2 6HG3)"
diyor. 1. maddenin hatası yüzünden ikinci tüpe 4 yerine 1 embriyo yazıldı.
Kullanıcının makinesinde de böyle, çünkü o ayı v6.148'de aktardı. Bütün
dosyalar tarandı: eski aylarda bu kurallardan etkilenen başka satır yok.

- `dondurma` kipi v6.161'de yalnızca hiç tüpü olmayan tedaviye yazıyordu.
  Artık tüpü olan tedavide yalnızca eksiği ekliyor
  (`_dondurma_kayitlari(yalnizca_ekle=True)`): tüpteki örneğe, skoruna ve
  durumuna dokunmuyor, hiçbir şeyi tüpten çıkarmıyor, yalnızca yazdığı
  tedaviyi basıyor. `tamamla` da düzeltirdi, ama aylar önce aktarılmış
  tedavilerde elle düzeltilmiş skorları ezer (v6.142).
- Denendi: şubat için tek değişiklik o tüp oldu. Üç 2PN "dondurulmuş" oldu;
  üç vitrifikasyon ve üç 3. gün değerlendirmesi eklendi. Başka hiçbir satır
  değişmedi. Öteki on bir dosyada kip hiçbir şey yazmadı. Onarımdan sonraki
  ilk aktarımda, 8 embriyo çözen bir şubat 2026 FET'i o iki tüpe bağlandı
  (4 + 4). Önce "tüpler tutmuyor" listesindeydi.

## Deneme

Kullanıcının veritabanının kopyasında (v6.164 provası: ocak–mayıs 2025 ve
mayıs 2026 bu oturumda yok):

- Beş dosya tarih sırasıyla (ocak → mart 2024, kasım → aralık 2025):
  - 482 tedavi, 0 hata: 199 FET, 230 IVF/ICSI, 46 Yumurta Dondurma,
    7 Yumurta Çözme. 451 tüp açıldı.
  - Dosyaların kendi FET'lerinden 52'si bağlandı.
  - Kasım–aralık 2025 gelince, daha önce aktarılmış 2026 FET'lerinden 52'si
    2025 tüplerine bağlandı. 53. bağ yukarıdaki şubat onarımından geldi.
  - Sonda 18 FET ertelendi: nisan–aralık 2024, bu kopyada ayrıca ocak–mayıs
    2025 ve mayıs 2026 yok.
- Düzeltilen satırlar aktarımda doğrulandı: tüpler 4+4+5+4 (17), 4, 9, 7,
  5+5+5+5 (20, "BİRG" dördü birleşme), 12 ve 22 yumurta, 10; birleşme
  değerlendirmelerinde hücre sayısı boş, grade yazılı.
- İkinci çalıştırma: beş dosyanın `tamamla`'sı, yeniden aktarım (hepsi
  atlandı) ve `bagla`. Tablolar satır satır karşılaştırıldı, hiçbir şey
  değişmedi. Bütünlük kontrolleri temiz.
- Gerileme: 2026'nın yedi, 2025'in beş dosyası eski ve yeni araçla `liste`
  (boş veritabanında) ve bütün satırların dondurma okuması. Tek okuma farkı
  şubat 2026'nın o satırı. Önizlemede ayrıca bir ocak 2026 satırı yeni uyarıyı
  alıyor: DONDURULAN 8, notta 7 embriyo var. Bu kaynağın kendisi; tüpü
  bilinmeyen embriyo zaten o tedavide yok.

## Bilinen / yazılmayan

- **Kaynağın sayıları tutmayan satırları** olduğu gibi yazıldı, rapor UYARI
  diyor:
  - Dört embriyo dondurmasında tüplerde notun sayısından az embriyo var
    (kaynak / tüplerde: 13/12, 10/8, 13/10, 24/23).
  - İki yumurta dondurmasında tüpler MII'den fazla. Not 12 diyor, tüpler
    4×4; not 22 diyor, tüpler 23. MII kadarı yazıldı.
- **Nisan–aralık 2024 yok.** 2025 FET'lerinden tüpü 2024'ün başında tutanlar,
  arada boş ay olduğu için erteleniyor. O aylar gelince kendiliğinden
  denenecek.
- Aynı hastanın iki mart 2024 FET'i elle bakılmalı listesinde. Kaynak
  tedavinin notu 13 embriyonun yalnızca 12'sini yazıyor. İlk FET üç eşit
  tüpten 8 çözmüş, hangi ikisi olduğu belli değil. İkincisi 5 çözmüş, kalan
  tüpte 4 görünüyor.
- "4BA TA"daki "TA"nın anlamı hâlâ soruda.

# v6.166 — `dondurma` kipi ne yaptığını söylüyor

Kullanıcı şubat 2026 onarımını çalıştırdı (`dondurma kaynak=SUBAT subat.csv`),
çıktı "Bitti. 0 tedaviye eksik dondurma yazildi." oldu. Sebep arandı:

- **O satırı şubatın aktarıldığı dönemin bütün sürümleri (v6.148–v6.164)
  aynı okuyor**: ikinci tüpe 1 embriyo. Yani kullanıcının veritabanında
  onarılacak tüp var.
- Kullanıcının veritabanı kopyası (v6.147 dönemi) üzerine ocak ve şubat 2026
  **v6.148 aracıyla** yeniden aktarıldı, sonra iki araç çalıştırıldı. Eski
  araç (v6.164) birebir aynı çıktıyı verdi, "0 tedaviye". Yeni araç (v6.165)
  "+3" dedi. En olası sebep: kullanıcının makinesinde `git pull` yeni sürümü
  getirmemiş.
- Yeni aracın çıktısı da iki durumda sessiz kalabiliyordu:
  - Etiket yanlışsa hiçbir satır bulunmuyor ve yine "0 tedaviye" deniyordu.
  - Tüpü olan tedavide eksik olup eklenemeyen örnek (havuz boş) hiç
    basılmıyordu. "Yazamıyorsan söyle" kuralı (v6.142) burada da geçerli.

Değişenler:
- Son satır kaç aktarılmış tedaviye bakıldığını söylüyor: "(89 aktarilmis
  tedavi gozden gecirildi)". Sıfırsa altına "kaynak= etiketi aktarımdakiyle
  aynı mı?" yazıyor.
- UYARI veren tedavi, hiçbir şey yazılmasa da basılıyor. On yedi dosyada
  bunlar yalnızca kaynağın bilinen tutarsızlıkları: notta 2PN'den çok
  embriyo, notun sayısı tüplerden fazla.
- "Tüpler notla tutuyor" satırı eksik varken basılmıyor; UYARI ile
  çelişiyordu.
- Sayaç yalnızca gerçekten yazılan tedaviyi sayıyor.

Denendi: on yedi dosyada kip veritabanında hiçbir şeyi değiştirmedi.

Kullanıcı 2026-09-24'te v6.165'in sorusunu cevapladı: **"BİRG1" = Birleşme
G1, doğru.** "TA"nın anlamını sonra düşünecek.

# v6.167 — nisan–ağustos 2024 Access kayıtları; tüpün içeriği içerikten; aynı gün iki kez girilmiş kayıt

Kullanıcı nisan, mayıs, haziran, temmuz ve ağustos 2024'ün Access dosyalarını
verdi (`kaynak=NISAN2024` … `AGUSTOS2024`, 369 satır). Önizleme beş yeni
durum gösterdi; üçü daha önce aktarılmış aylarda da vardı ve sessizdi.

## Tüpün içindeki yumurta mı embriyo mu: içerikten

v6.133'ten beri tüpün içeriği dondurmanın yapıldığı tedavinin **tipinden**
okunuyordu (`db.yumurta_mi(tip)`: yalnızca Yumurta Dondurma yumurta
dondurur). Programın kendi akışı için doğru, IVF/ICSI'nin vitrifikasyon ekranı
yalnızca enjekte edilmiş embriyoyu donduruyor. Ama Access kayıtlarında:

- IVF/ICSI tedavisinde ICSI'ye alınmayan MII'ler dondurulmuş ("16 ADET OOSİT
  ... (4*M2)"). Kullanıcının veritabanı kopyasında 5 tedavinin 9 tüpü, 31
  yumurta. Cryo Haritası, taşıyıcı sayfası ve resmî formlar bunlara
  "embriyo" diyordu. Çözme ekranı Yumurta Çözme yerine FET öneriyordu.
  Aktarımın tüp eşleştirmesi de (`_bag_siniflari()`) onları embriyo adayı
  sayıyordu. Skoru olmayan örnek her transfer yazımıyla tuttuğu için bir
  FET'in çözdüğü embriyolar yumurta tüpüne bağlanabilirdi. Yumurta Çözme
  ise o tüpü hiç bulamazdı.
- Yumurta Dondurma'da beş yumurtaya ICSI yapılmış, blastokisti ayrı tüpte
  (aşağıda). Tipe bakan ölçü o tüpe "yumurta" derdi.

Kural artık tek yerde: **`db.dondurulan_yumurta_sql(o)`**. Dondurmadan önce
enjekte edilmemiş, döllenmemiş ve değerlendirilmemiş örnek yumurtadır.
FET ve FET (3→5)'in dondurduğu hep embriyodur. Dondurmadan sonraki olaya
bakılmıyor: Yumurta Çözme'de enjekte edilen yumurtanın ilk tüpü yine yumurta.

Bu kuralı soran yerler:
- Program: `app.icerik_sql()` (eski `icerik_tipi_sql()`), sütunu `icerik` =
  `'yumurta'`/`'embriyo'`. `tasiyici_icerigi()`, çözme tipinin seçimi
  (`_tup_yumurta_mi()`), Cryo Haritası'nın tank sayımı ve beş şablon da
  ondan okuyor. Jinja: `icerik_sayisi(adet, icerik=t.icerik)`.
- Resmî formlar: `dondurma_tupleri()` her tüpe `yumurta` işareti koyuyor.
  `dondurma_notu()` ikisi birden varsa şöyle yazıyor: "Dondurulan: 1
  embriyo, 5. gün, 1 tüp: (1CB); 16 yumurta, 3 tüp: (6) (5) (5)".
  `_kalan_dondurulmus()` da aynı kuralı kullanıyor.
- Araç: `_bag_siniflari()`.

Bilinen sınırlar:
- IVF/ICSI tedavisinin vitrifikasyon ekranı aktarılmış dondurulmuş yumurtayı
  "Embriyo N" diye listeliyor, çünkü ızgaranın adı tedavinin tipinden geliyor.
- `transfer_adaylari()` yumurtayı tipe bakarak eliyor. IVF/ICSI'den gelen bir
  yumurta çözülüp ICSI'si yazılmadan o tedavinin transfer ekranında
  görünebilir.

## Tedavi tipi: protokolde yazım hatası ve ICSI'siz yumurta dondurma

Beş satır IVF/ICSI açılmıştı, oysa yalnızca yumurta donduruyorlardı:

- İkisinin protokolünde yazım hatası var: "OOSİT CRTYO" (ağustos 2025) ve
  "OOSİT CRRYO" (mart 2024). Kural artık C/K + R + en çok iki harf + YO. Otuz
  farklı protokol adında başka hiçbiri tutmuyor (ölçüldü).
- Üçünün protokolü yalnızca ilaç ("GONAPEPTLY"): eylül 2025, aralık 2025 ve
  temmuz 2024'te birer satır. ICSI, 2PN, transfer ve DONDURULAN embriyo yok,
  notun bütün tüpleri yumurta.

Tedavi ekranı bu satırlarda boş ICSI/döllenme aşamaları gösteriyordu. Resmî
formun "fertilizasyon yöntemi" kutusu da "IVF/ICSI" basıyordu. Tip artık
veriden okunuyor (`tipi_veriden_duzelt()`, v6.142'nin dersi).

Daha önce aktarılmış olanlar için **`tip` kipi** var (CSV'siz, bütün
veritabanı). Tedavinin kendi kayıtlarına bakıyor: hiç ICSI, döllenme,
değerlendirme ya da transfer yok, bu tedavi için çözme yok, en az bir
dondurma var ve hepsi yumurta. Değişen yalnızca `cycle_tipi` (değişiklik
geçmişine yazılıyor) ve Yumurta Dondurma'da olmayan aşamaların "İşlemi
yapan"ı. Kopyada dört tedavi değişti, ikinci çalıştırma hiçbir şeyi
değiştirmedi.

**Kısmi ICSI'li satırlar Access'teki tipinde kalıyor.** Bunlarda birkaç
yumurtaya ICSI yapılmış, kalanı dondurulmuş: ekim 2025'te ve mayıs 2024'te
IVF/ICSI, mayıs ve haziran 2024'te üç Yumurta Dondurma. Tüpleri içerik
kuralıyla doğru adlanıyor. Programın kendi akışında böyle bir tedavinin yeri
yok: IVF/ICSI kalan yumurtayı donduramıyor, Yumurta Dondurma'nın ICSI aşaması
yok. Bu yüzden kullanıcıya soruldu.

## Aynı notta yumurta ve embriyo tüpü

Haziran 2024'teki satırın notu: "1 ADET 5,GÜN EMBRİYOSU 1 TÜPTE(1CB) GERİYE
KALAN 16 ADET OOSİT 1 TÜPTE(6*M2) 1 TÜPTE(5*M2) 1 TÜPTE(5*M2) ...
DONDURULARAK SAKLANDI". Tedavi Yumurta Dondurma. Not bütün olarak yumurta
sayıldığı için blastokistin tüpü **sessizce** yazılmıyordu (v6.142'nin
kuralı: yazamıyorsan söyle).

Şimdi tür grup grup belirleniyor (`_dondurma_coz()`'ün `grup_yumurta`'sı):
- Embriyo tüpü 2PN'den yazılıyor, OPU + 5. günde.
- Yumurta tüpleri OPU gününde (`_grup_zamanlari()`).
- Var olan tüpler türünün içinde sırasıyla eşleşiyor.
- Aynı tüpte ikisi birden yazılmışsa UYARI veriliyor.

Kopyada ağustosun bir FET'i bu blastokist tüpüne bağlandı. Tüp yazılmasaydı
o FET "tüpü programda yok" diyecekti.

## Aynı gün iki kez girilmiş kayıt

Mayıs 2024'te bir hastanın aynı OPU'su iki kez girilmiş (#1 ve #13). Toplanan
ve MII aynı; immatür (2/7), empty zona (5/0) ve sperm hazırlık sayıları farklı.
İkisi de aktarılsaydı hastanın kartında aynı gün iki tedavi açılır, aynı 16
yumurta iki kez dondurulmuş görünürdü (Cryo Haritası'nda sekiz tüp).

`ikizleri_ayikla()` aynı hastanın aynı günkü aynı tipteki iki dolu kaydını
ayırıyor:
- Birebir aynıysa ikincisi atlanıyor. Notta boşluk ve noktalama farkı
  sayılmıyor.
- Farklıysa **ikisi de** atlanıyor ve söyleniyor. Hangisinin doğru olduğunu
  araç tahmin etmiyor. Kullanıcı doğru olmayanı düzeltme dosyasına
  `KAYNAK#KAYIT  ATLA` diye yazıp dosyayı yeniden aktarıyor.

Bu yalnızca önizlemede ve aktarımda geçerli. Onarım kipleri aktarılmış
tedavilere işaretleriyle ulaşıyor.

Daha önce üç çift böyle aktarıldı: haziran 2025 #1/#19, temmuz 2025 #79/#85
ve aralık 2025 #63/#85. Hepsi iptal edilmiş IVF/ICSI, yalnızca notun yazımı
farklı. **`ikiz` kipi** bunları listeliyor ve hiçbir şey yazmıyor. Transferleri
yok, fazlası ekrandan kalıcı silinebilir.

## Sayılar

- **Embriyoda beklenen sayı önce DONDURULAN** (v6.165'te ADET ile
  DONDURULAN'ın büyüğüydü). Haziran 2024'te not "16 ADET" diyor, DONDURULAN
  15 ve dört tüpte 15 embriyo var. Eski kural tutan tüpe "1 embriyo eksik"
  dedirtiyordu.
- **Yumurta sayısından fazla ICSI** yazım hatası sayılıyor. Mayıs 2024'te bir
  satırda 13 yumurta, 9 MII, İŞLEME ALINAN 94. Araç sayıyı 13'e kısıyor ve
  empty zona yumurtalara da ICSI yazıyordu. Şimdi sayı boş kabul ediliyor ve
  döllenme sonuçlarından (5) hesaplanıyor (v6.164'ün kuralı). Not
  Access'teki değeri söylüyor. Doğrusu biliniyorsa düzeltme dosyasına
  `KAYNAK#KAYIT  ICSI  eski  yeni` yazılıyor.
- **Açılan yumurta sayısı** TOPLANAN, olgunluk sayılarının toplamı ve ICSI
  sayısının büyüğü (`_yumurta_sayisi()`; Yumurta Çözme'de v6.148'den beri
  böyle).
  - Mayıs 2024'te bir Yumurta Dondurma satırında TOPLANAN boş ama MII 1 ve
    not o yumurtayı donduruyor. Kayıt açılmadığı için dondurma
    yazılamıyordu.
  - Ağustos 2024'te TOPLANAN 6, olgunluk sayılarının toplamı 7. Bir dejenere
    düşüyordu.
  - "Toplanan" kutusu Access'teki değeri tutuyor, not farkı söylüyor.
- Mayıs 2024'teki bir satırda 2PN 1, intakt 2, ama not iki embriyo
  donduruyor. Bir embriyo yazılamıyor ve UYARI çıkıyor. Bu kaynağın kendi
  tutarsızlığı.

## Denendi

- **Okuma karşılaştırması:** eski ve yeni araç 1805 CSV satırının hepsini
  okudu. 7'sinin okuması değişti, hepsi yukarıda anlatıldı.
- **Prova:** kullanıcının veritabanı kopyasında beş ay tarih sırasıyla
  aktarıldı. Sonuç 367 tedavi (mayısın çifti bekliyor) ve 180 yeni hasta
  kartı. 63 FET tüpüne bağlandı. Kopyada ocak–mayıs 2025 ile mayıs 2026 yok,
  "ertelendi" diyenlerin çoğu onları bekliyor.
- **İkinci çalıştırma** (`dondurma` kipi ve yeniden aktarım) hiçbir tabloyu
  değiştirmedi. Bütünlük denetimi temiz.
- **Ekran:** Cryo Haritası, taşıyıcı ve çözme ekranı, iki resmî form,
  vitrifikasyon ve tedavi ekranı açıldı. Hepsi 200 döndü, JS hatası yok.
  Yumurta tüpleri "yumurta", blastokist tüpü "1 embriyo" diyor.

# v6.168 — eylül–aralık 2024 ve ocak 2023 Access kayıtları; dondurma notunun dört yeni okuması

Kullanıcı beş Access dosyası verdi: EYLÜL, EKİM, KASIM, ARALIK (2024) ve OCAK.
OCAK'ın tarihleri **2023** (141 satırın hepsi 2023-01), 2025'in ocağı değil.
Etiketler `OCAK2023`, `EYLUL2024` … `ARALIK2024` (v6.160: etiket yıllar
arasında tekil). 524 satır.

## Tarih düzeltmeleri (`tarih_duzeltme_2024c.txt`, depoda değil)

Üç satırın yılı ya da ayı açık bir yazım hatası:
- Kasım 2024'te bir FET'in transferi 2024-01-13 (komşu kayıtlar 13 kasım,
  doğrusu 2024-11-13).
- Aralık 2024'te bir OPU 2025-12-31 (dosya aralık 2024).
- Ocak 2023'te bir OPU 2023-03-16 (dosya ocak 2023, önceki/sonraki kayıtlar
  16 ocak).

## Dondurma notunun yeni okumaları

Hepsi önizlemede sessizce eksik tüp ya da yanlış tüp veriyordu:

- **"KACG1" / "KACG2"**: kavitasyon'un C ile yazılmışı (klavyede V'nin
  yanında). Kasım 2024'te bir ve daha önce aktarılmış ocak 2025'te bir
  embriyo "tanınmayan yazım" deyip yazılmıyordu. `_skor_metni()` "KAC"ı
  yalnızca arkasından derece geliyorsa KAV sayıyor.
- **"KAVVİTASYONG3"** (V iki kez, ocak 2023): aynı işlevde `KAV+ITASYON`.
- **İlk dondurma cümlesinde tüp yok, ikincisinde var** (ocak 2023):
  "ÇÖZÜLEN 3 ADET OOSİTTEN 2 TANE M2 OOSİT REFREEZE YAPILDI. OPUDA TOPLANAN
  2 ADET M2 OOSİTLE BİRLİKTE TOPLAM 1 TÜPTE(4*M2) ... DONDURULARAK SAKLANDI."
  Araç ilk fiilin cümlesini okuyordu, tüp bulamadı. Artık parantezi olan ilk
  dondurma cümlesi seçiliyor; hiçbirinde yoksa eski okuma. "REFREEZE
  YAPILDI" da dondurma fiili (önceden yalnızca "REFREEZE EDİLDİ").
  - Ocak 2023'teki başka bir satırda aynı eksiklik tüpü "(YAPILDI)" diye
    okutuyordu; artık "(2BC)".
- **"(%80 VİABİLİTE)"** tüp değil, çözmenin notu (aralık 2024). Tüp sayısını
  bir fazla gösteriyordu.

## Not "M1" diyor, kutu "MII" diyor

Kasım 2024'te bir Yumurta Dondurma: 1 yumurta, MII 1, immatür 0, not
"1 TÜPTE(1*M1)". v6.161'in kuralı (kullanıcı: "en son yazılanı kullan", not
kazanır) yalnızca notun M2'si fazlayken çalışıyordu. Ters yönü eklendi:
notun M1'i immatürden fazlaysa fark MII'den immatüre geçer, not Access'teki
değeri söyler. Tüp önceden hiç yazılmıyordu ("notta 1 örnek ... 0 uygun").
Kullanıcı doğruladı: "M1 kararı doğru."

## Kalan uyarılar

- Ocak 2023'teki satır: not 4 M2 donduruyor, programda 2 yumurta var. Öteki
  ikisi o tedavide çözülen yumurtalar ve dondurmaları program öncesi. Bu
  kaynağın kendisi, uydurulmuyor.
- Mart 2025'te (önceden aktarılmış) "M1-M2 ?" yazılı tek yumurta hâlâ
  yazılmıyor: olgunluk kaynakta da belirsiz.

## FET bağlama

Eylül–ekim 2024 aktarılırken FET'ler bağlanmadı: arada aktarılmamış aylar
var (v6.164'ün ertelemesi). Kasım ve aralık 2024 gelince 9 ve 68 FET tüpüne
bağlandı (kopyada; kullanıcının makinesinde ocak–ağustos 2024 de olduğu için
sayı farklı olacak). Ocak 2023'ün tüplerini çözen FET'ler şubat–aralık 2023
aktarılana kadar bekler.

## Denendi

- **Okuma karşılaştırması:** eski ve yeni araç 11 CSV'yi (2025 ocak–mayıs,
  mayıs 2026 ve bu beş dosya) okudu. Değişen satırlar yalnızca yukarıdakiler.
- **Prova:** test veritabanında beş dosya eskiden yeniye aktarıldı: 524
  tedavi, 0 hata, bir uyarı (yukarıda).
- **İkinci çalıştırma** (yeniden aktarım, `dondurma`, `bagla`) hiçbir tabloyu
  değiştirmedi.
- `dondurma kaynak=OCAK2025` o ayın eksik KACG2 embriyosunu ekledi.
- **Ekran:** 524 tedavinin her biri için tedavi ekranı, iki resmî form, ART
  Lab Excel'i ve tedavi dökümü; ana ekran, Cryo Haritası, istatistik: hepsi
  200.

# v6.169 — Yumurta tüpünün parantezi olgunluğu yazıyor

Kullanıcının isteği: "Yumurta dondurma işlemlerinde özet formlarının not
kısmında, ART Lab formunun freeze kısmında belirtmiyor. Sadece rakam yazıyor.
Detay yazsın."

`tup_metni()` kalitesi kayıtlı olmayan tüpe (yumurtada hiçbirinin skoru
olmaz) v6.135'ten beri yalnızca sayı basıyordu: "(5)". Artık yumurtaların
**olgunluğunu** sayısıyla basıyor: "(5*MII)", karışıksa "(4*MII-1*MI)". Bu,
kullanıcının Access'teki kendi yazımı ("(5*M2)"). Etiket `liste_degeri`'nden
geliyor (kodu değil etiketi göster kuralı).

- **Olgunluk dondurmadan ÖNCEKİ son maturasyon** (`_yumurta_olgunlugu()`,
  kimlik sırası, v6.143'ün kuralı). Yumurta Çözme'de çözülüp yeniden
  değerlendirilen yumurtanın sonraki maturasyonu tüpün içeriği değil.
- **Yalnızca yumurta tüpünde** (`db.dondurulan_yumurta_sql()`). Skoru
  kayıtlı olmayan bir embriyo tüpü "(2*MII)" basmasın diye: embriyonun MII'si
  ICSI'den önceki hali.
- Olgunluğu kayıtlı olmayan yumurta "?" ile görünüyor. Hiçbirininki yoksa
  eskisi gibi yalnızca sayı basılıyor, uydurulacak bir şey yok.
- Aynı parantez her yerde: Özet'in NOTLAR'ındaki "Dondurulan:", "Çözülen:" ve
  "Kalan dondurulmuş:" satırları, ART Lab'ın FREEZE ve THAW kutuları.
- Access'ten aktarılmış tedavide Özet'in "Dondurulan:" satırı yine basılmıyor
  (v6.159). Access notunun kendi cümlesi zaten "(5*M2)" diyor. ART Lab'ın
  FREEZE kutuları ise değişti.

**Denendi:** test veritabanının 1006 tedavisinde eski ve yeni kodla Özet
NOTLAR'ı, FREEZE ve THAW karşılaştırıldı. 117 tedavide 200 yumurta tüpü
değişti ("(N*MII)" 166, "(N*MII-N*MI)" 30, "(N*MI)" 3, bir de Yumurta
Çözme'nin THAW'ı). Hiçbir embriyo tüpü değişmedi. Değişen tedavilerin iki formu,
iki Excel'i ve tedavi ekranı 200 döndü. ART Lab'ın FREEZE kutusunda
"(1*MII-2*MI)" sığıyor.

# v6.170 — şubat–haziran 2023 Access kayıtları; düzeltme dosyasında DOSYA satırı

Kullanıcı şubat, mart, nisan, mayıs ve haziran 2023'ün Access dosyalarını
verdi (`kaynak=SUBAT2023` … `HAZIRAN2023`, 563 satır). Önizleme uyarısız
geçti. Kayıtlar dosyalarda tarih sırasıyla dizili, bu yüzden ayına ve
komşularına uymayan tarih kolay görünüyor.

## Düzeltme dosyası (`tarih_duzeltme_2023.txt`, depoda değil)

- Dört tarih açıkça yazım hatası, ay rakamı yanlış: şubatta bir OPU "mart",
  bir FET transferi "mart"; mayısta bir OPU "haziran" (aynı hastanın
  haziranda başka bir OPU'su var); haziranda bir FET transferi "mart".
- Şubatın son iki satırı mart transferi (2 ve 21 Mart). Dosyanın sonunda
  oldukları için sonradan girilmiş gerçek kayıtlar olabilir, düzeltilmedi.
- **Haziranda bir FET'in DOSYA NO'su "41"**, kaydın kendi sıra numarası (yer
  tutucu, `liste` "DİKKAT" diyor). Notundaki önceki deneme tarihi, doğum
  tarihi ve dondurulup transfer edilen embriyonun skoru nisandaki bir
  tedaviyle tutuyor. Ama araç hastayı adından ya da doğum tarihinden
  **eşleştirmiyor** (v6.125). Yanlış hasta bu işin en pahalı hatası. Onun
  yerine düzeltme dosyasına yeni bir satır türü geldi:

      KAYNAK#KAYIT  DOSYA  eski-no  yeni-no

  Satır yalnızca Access'teki numara hâlâ `eski-no` ise uygulanıyor, tarih
  düzeltmeleri gibi. Tedavinin notu "Dosya numarası Access'te 41 yazıyordu,
  ... olarak düzeltildi" diyor. Numarayı kullanıcı onaylıyor. Yanlışsa
  satır `ATLA` oluyor ve kayıt aktarılmıyor. Prova: düzeltilen FET
  nisandaki tüpe bağlandı.

## Kalan uyarılar

- Nisanda bir satırın 2PN'i 3, ama notta 5 embriyo dondurulmuş. 3'ü
  yazıldı, UYARI çıkıyor. Bu kaynağın kendi tutarsızlığı.
- Her ayın sonunda 1–4 FET "elle bakılmalı": tüpü birden çok seçenekle
  tutuyor ya da hastanın dolu tüplerinden hiçbiri tutmuyor. Önceki aylardaki
  gibi bağlanmadılar, raporda seçenekleri yazılı.

## Denendi

- **Prova:** test veritabanında (ocak 2023 dahil) beş dosya eskiden yeniye
  aktarıldı: 563 tedavi, 0 hata. 97 FET tüpüne bağlandı. Temmuz–aralık
  2023 aktarılmadığı için sonraki FET'ler "ertelendi".
- **İkinci çalıştırma** (yeniden aktarım, `dondurma`, `bagla`) hiçbir
  tabloyu değiştirmedi.

# v6.184 — FET'in tüpüne bağlanması: sayılar eşitse skor yazımı engel değil

Kullanıcının açıklaması (2026-09-25, v6.183'ün örnek hastası için): "sorun
yanlış yazım. Ama mantıklı analiz yapınca dondurulan ve çözülen embriyo
sayıları eşit o yüzden hiç embriyosu kalmamış olması lazım." v6.183'te
sebebi "çözmeden sonra yeniden değerlendirme" diye anlatmıştım -- bu bir
tahmindi, doğrusu Access'teki yazım hatası. Kullanıcının ölçüsü skordan
bağımsız: 3 embriyo donduruldu, 1 + 2 çözüldü, geride bir şey kalmaz.

**Kural** (`_sayi_esitligi_engeli()`, `_kaynaga_bagla()`): skor yazımıyla
hiçbir tüp kümesi tutmuyorsa ama hastanın dolu tüplerindeki TOPLAM embriyo
(çözmeden önce dondurulmuş, türü aynı) tam çözülen sayı kadarsa, FET o
tüplerin hepsine bağlanıyor: seçim yok, geride tüp kalmıyor. Rapor "skor
tutmuyor ama hastanın kalan bütün tüpleri ... çözülen sayıya eşit" diyor.
Bağlanmadığı durumlar:
- **toplam tutmuyor** (kısmi çözme; rapor "tüplerde N, çözülen M" diyor);
- **aktarılmamış ay** varsa önce "ertelendi" (gerçek tüp o ayda olabilir);
- **tüplerden biri Cryo Haritası Excel'iyle eşleşmiş** (konumu yazılı):
  tank bugün o tüpü gösteriyor, çözülmüş olamaz;
- **FET'in notu dışarıdan gelen embriyodan söz ediyor** ("ÖZELDEN TAŞINDI",
  "DIŞ MERKEZ", `_DIS_MERKEZ`): çözülen o embriyolar olabilir, programdaki
  tüpler tankta durur.

Denendi (test kopyası, v6.183'ün `bagla`'sından sonra): 6 FET daha
bağlandı; altısının da Access notu "GERİYE EMBRİYOSU KALMADI/KALMAMIŞTIR"
diyor. İkinci çalıştırma 0. Kalan "tutmuyor"ların 45'inde toplam sayı
tutmuyor, 2'sinde tüp Excel'de konumlu -- bunlar elle bakılacak.

# v6.183 — FET'in tüpüne bağlanması: blastokistte genişleme sayısı yeter

(v6.184'te düzeltildi: aşağıdaki "2CC → 2BB çözmeden sonra yeniden
değerlendirme" bir tahmindi; kullanıcı doğrusunun yazım hatası olduğunu
söyledi. Kural değişmedi, sayı eşitliği kuralı eklendi.)

Kullanıcının bildirdiği (2026-09-25): bir hastanın en son tedavisinden sonra
dondurulmuş embriyosu kalmamış olmalıydı, ama formda kalan embriyo
yazıyordu. Eylül 2024'te iki tüp dondurulmuş: (3AA) ve (2BC-2CC). Ocak 2025
FET'i 3AA tüpünü çözmüş (bağlı). Mayıs 2025 FET'inde iki embriyo transfer
edilmiş, Access'e "2BB" ve "2BC" yazılmış: çözmeden sonra yeniden
değerlendirilen 2CC, 2BB olmuş. `_uyumlu()` blastokist skorunu birebir
istiyordu; `bagla` "dolu tüpler tutmuyor -- elle bakılmalı" dedi, tüp "dolu"
kaldı. Cryo Haritası'nda ve sonraki formların "Kalan dondurulmuş"unda
görünüyordu (v6.181'in bildirilen hatasının blastokist hali).

Kullanıcıya üç seçenek soruldu (genişleme aynıysa bağla / blastokistse bağla /
kural kalsın, elle bağla); cevabı **"Genişleme aynıysa bağla"**:

- **Blastokistte genişleme sayısı tutmalı, ICM/TE farklı olabilir**: 2CC
  tüpü 2BB transferiyle tutar, 3BB tüpü 4AA transferiyle tutmaz.
- Kavitasyon/morula ve evre kuralı değişmedi (erken evredeki tüp kültürde
  ilerlemiş olabilir, geri gidemez). Cleavage'da v6.181'in kuralı: hücre
  sayısı.
- **Birebir tutan küme yine önce** (`tam()`); birden çok tüp yalnızca
  ICM/TE farkıyla tutuyorsa belirsiz, bağlanmaz. Bağlı olanlar aynı kuralla
  yeniden sınanıyor, bağ çözülmüyor.

Ölçüldü (test kopyası, v6.181'in `bagla`'sından sonra): 73 "tutmuyor"
FET'in 17'si bu kuralla bağlandı; kaliteyi tümden yok saymak yalnızca 1 FET
daha ekliyordu -- kalanların sebebi başka (sayı tutmuyor, ay aktarılmamış).
Bildirilen hastanın Mayıs FET'i tüpüne bağlandı, tüp boşaltıldı, formu
"Kalan dondurulmuş embriyo yok" diyor. Access notunun kendi "GERİYE 1 TÜPTE
2 ADET EMBRİYOSU KALDI" cümlesi kaynağın yazısı, olduğu gibi basılıyor.

Kullanıcının yapacağı: `git pull origin main`, `python3 aktar_access.py
bagla`.

# v6.182 — Başka merkeze taşınan tüp ve "Excel'de yok" aday listesi

Kullanıcının bilgisi (2026-09-25): "Tedavide embriyosu var gözüküp ama cryo
haritada embriyo gözükmüyorsa bazen hastalar embriyolarını başka tüp bebek
ünitesine taşıma yapabiliyor." İki şey önerildi, "İkisini de yap" dedi;
notun biçimi de onun: "1 tüp 12.03.2025 tarihinde şuraya taşındı".

Programda bir tüp yalnızca dolu / boşaltıldı (çözüldü) / kullanıldı (sperm)
olabiliyordu. Başka merkeze giden tüp "dolu" kalıyor: Cryo Haritası'nda
duruyor, sonraki formların "Kalan dondurulmuş" satırına giriyordu -- v6.181'in
bildirilen hatasının aynı görünümü, sebebi başka. Access notlarında dışarıya
gönderim hiç yazılmamış (içeriye gelen var: "ÖZELDEN TAŞINDI"), yani program
bu tüpleri kendisi bulamaz; bilgi kullanıcıda ya da Cryo Excel'inde (satırın
olmaması).

**1. Taşıyıcı sayfasında "Başka merkeze taşındı olarak işaretle"**
(`goc_051`: `tasiyici.gonderim_zamani` / `gonderim_yeri` / `gonderim_notu`,
`durum='gonderildi'` -- kolon serbest metin, CHECK yok).
- Açılır kutuda gün (zorunlu), nereye, not + tarayıcı onayı. Gün tüpün
  dondurulmasından önce ve bugünden sonra olamaz (yapılmış bir işin kaydı);
  yıl kontrolü `yil_kontrol()`. Hatalar `?hata=` ile, beyaz liste
  `GONDERIM_HATALARI` (tuzak #9).
- **Kayıt silinmiyor, örneklerin durumu değişmiyor** -- yalnızca tüpün.
  "Taşındı işaretini kaldır" geri alıyor (rota `gonderimi-geri-al`:
  `geri-al` ile bitseydi `yol_modulu()` onu "silme" modülüne bağlardı;
  izin `cryo`). İkisi de `degisiklik_log`'a düşüyor.
- Taşınan tüp: Cryo Haritası'ndan çıkıyor (zaten `durum='dolu'` süzüyordu),
  çözülemiyor (çözme ekranı, çözme kaydı ve "yeni tedavi aç" sunucuda
  reddediyor), `bagla` onu aday saymıyor (dolu tüplere bakıyor), etiket
  aramasında "başka merkeze taşındı" rozetiyle bulunuyor, hasta kartında
  ayrı bir "Başka merkeze taşınan tüpler" kartında (tüpün sayfasına -- ve
  geri almaya -- oradan gidiliyor), Cryo Excel dökümünün "Dolapta"sı
  "Taşındı".
- **Yer kullanıcının yazdığı gibi**, ekiyle ("Memorial Hastanesi'ne"): not
  "... 12.03.2025 tarihinde Memorial Hastanesi'ne taşındı." Program Türkçe
  ek uydurmuyor (ünlü uyumu, kaynaştırma, kesme işareti -- özel adda yanlış
  ek resmî forma yanlış yazı demek); yazılmamışsa "başka merkeze".

**Resmî form (Embriyoloji Özet) NOTLAR'ı:**

    Taşınan: 2 embriyo, 1 tüp: (3AB-1BB) 01.03.2025 tarihinde Memorial
    Hastanesi'ne taşındı.

- Tüpün **dondurulduğu tedavinin** formunda, "Dondurulan:" satırının hemen
  altında (`formlar.tasinan_notu()`, içerik `tup_metni()`'nin yazımıyla).
- **"Kalan dondurulmuş" o günün tankını söylüyor** (v6.152'nin kuralı):
  tedavinin son işleminden ÖNCE (ya da aynı gün) taşınan tüp kalan
  sayılmıyor ve çözme satırlarının altında "Taşınan: ..." yazıyor; SONRA
  taşınan tüp o formda hâlâ kalan -- o gün tanktaydı. Gün bilinmiyorsa
  kullanıcı yaklaşığını yazar; ölçü bu gün.
- ART Lab'ın kutuları değişmedi.

**2. `cryo_esle.py eksik` -- programda dolu, Excel'de karşılığı olmayan
tüpler.** Hiçbir şey yazmıyor; `cryo_esle_rapor_eksik.txt` (hasta adı
içerir, `.gitignore`). Excel'in hiçbir satırının almadığı dolu embriyo/
yumurta tüpleri, dört sınıf:
- **Adı farklı yazılmış**: Excel'de aynı gün, aynı içerikli ama hastaya
  atanamamış satır var (ad tutmuyor ya da aynı adlı birden çok hasta).
  Test kopyasında 117 tüp; örnekler I/İ farkı ve soyadın bir harfi -- tüp
  büyük olasılıkla tankta. Bunlar taşınmış sayılmamalı.
- **Hastanın Excel'de hiç satırı yok**: taşınmış, çözülmüş ama programa
  yazılmamış ya da Excel'de eksik (test kopyasında 540).
- Aynı adlı hasta, satır atanamadı (8).
- **Hastanın satırı var ama bu tüple eşleşmedi**: önce Excel satırına bakmak
  gerek -- tarih/içerik yazımı tutmuyor olabilir; raporda o hastanın
  eşleşmeyen satırları yazıyor (439).
Her satırda hastanın tüpüne bağlanmamış aktarılmış FET'i varsa günü de
yazıyor: öyle bir tüp aslında çözülmüş olabilir. Excel'in son tarihinden
sonra dondurulan tüpler sayılıyor, listelenmiyor. Taşınanı kullanıcı tüpün
sayfasından işaretliyor; araç kimseyi "taşındı" diye işaretlemez.

Denendi (test kopyası): göç iki kez, eksik kipi 1,3 sn; bir tüp FET'ten
sonra / önce taşınınca FET formunun "Kalan"ı ve kaynak tedavinin "Taşınan"ı
beklenen gibi; geri alma, çözme engeli, ileri/eski/bozuk tarih, hatalı
`?hata=`, hasta kartı, etiket araması, Excel dökümü; telefon ve masaüstünde
yatay kayma yok.

# v6.181 — FET'in tüpüne bağlanması: cleavage derecesi çözmeden sonra değişebilir

Kullanıcının bildirdiği hata (2026-09-25): bir hastanın Eylül 2025 FET'inin
formunda NOTLAR "Kalan dondurulmuş: 5 embriyo, 2 tüp" diyordu, Access notu
"GERİYE 1 TÜPTE 2 ADET EMBRİYOSU KALDI". Fazla tüp, hastanın Ekim 2024'te
dondurulan (8HG2-8HG2-6HG2) tüpüydü: Nisan 2025 FET'inde çözülmüş (3 çözülen,
8HG2 + 6HG3 transfer, "GERİYE EMBRİYOSU KALMADI"), ama program FET'i o tüpe
BAĞLAMAMIŞTI -- tüp "dolu" kaldı, sonraki bütün formlarda ve Cryo
Haritası'nda kalan gibi göründü. Sebep `_uyumlu()`: transfer edilen
embriyonun yazımı tüpteki örnekle birebir tutmalıydı; 6HG3 ile 6HG2 tutmadı,
`bagla` "dolu tüpler tutmuyor -- elle bakılmalı" dedi.

Embriyo çözmeden sonra yeniden değerlendiriliyor, yazılan kalite dondurmadaki
kaliteden farklı olabiliyor. Test kopyasında bağlanamayan 94 FET'in çoğu
böyle (6HG2→6HG3, 3BB-3BC→4BA-4AA, 4G2→8G2, 3CB→3BC). Kullanıcıya soruldu,
üç seçenek (kaliteyi tümden yok say / yalnızca cleavage derecesi / hiç
gevşetme); cevabı **"Yalnızca cleavage derecesi"**:

- **Cleavage'da hücre sayısı tutmalı, derece (G) farklı olabilir**: 6HG2
  tüpü 6HG3 transferiyle tutar, 8HG2 tüpü 6HG2 transferiyle tutmaz.
- **Blastokist skoru hâlâ birebir** (genişleme, ICM, TE); evre kuralı
  değişmedi (erken evredeki tüp kültürde ilerlemiş olabilir, geri gidemez).
- **Birebir tutan küme yine önce**: `_bag_siniflari()`'nin `tam()` sayısı
  derece farkını tam saymıyor, yani hastanın hem birebir hem yalnızca
  derecesi farklı tutan tüpü varsa birebir olan seçilir; ikisi de yalnızca
  derece farkıyla tutuyorsa BELİRSİZ, bağlanmaz. Var olan bağlar da aynı
  kuralla yeniden sınanıyor (`_baglantilari_yeniden_sina()`), bağ çözülmüyor.

Kod `_uyumlu()`'de, tek yer -- `_eslestir()`, `_kaynaga_bagla()`, `tasi`
kipi ve yeniden sınama hep oradan geçiyor. Test kopyasında `bagla`: 13 FET
yeni bağlandı (12'si derece farkı, 1'i zincirleme -- önce çözen FET tüpünü
alınca sonraki FET'in belirsizliği kalktı: "önce çözen önce alır", v6.163);
ikinci çalıştırma 0. Bildirilen hastada Nisan 2025 FET'i tüpe bağlandı, tüp
boşaltıldı, formu "Kalan dondurulmuş embriyo yok" diyor; Eylül 2025'inki
Access notuyla aynı tek tüpü söyleyecek.

# v6.180 — Cryo Excel'inin sperm satırları ve Sperm Dondurma haritası

Kullanıcının isteği (2026-09-25): "Excel'deki sperm sayfaları da programa
alınsın. Cryo Haritalar bölümünde Sperm Dondurma diye bir bölüm olsun oraya
harita eklensin. Tedavi hastalarına bağlama seçeneği olsun." Soruldu, cevaplar:

- **Kimin kaydı**: "Eşinin adı olan kadın hasta olabilir, karışıklık olur ...
  Sperm için erkek kaydı aç." Satır EŞİ adından ya da erkeğin adından çiftin
  kaydına bağlanmıyor.
- **Bağlama**: "Dosya numarası eski sperm dondurmada olmadığı için bağlanmaz.
  Program ile yeni sperm dondurmalar dosya numarasından bağlanacak." Eskiler
  elle: "Eski sperm dondurmaları elle ben eşleştirebileyim."
- **Tüp**: "Her satır bir tüp" -- "tek hastanın 3 tüp spermi dondurulduysa
  cryo haritada 3 satır işgal ediyor". Yani bir erkeğin birden çok satırı
  TEK hasta kaydında toplanıyor, her satır o kaydın altında bir tüp.
- **Harita**: "Tank → kanister → goblet ağacı".

**`python3 cryo_esle.py sperm <excel>`** (yeni kip, "SPERM" onayıyla).
Excel'in sperm satırları (kategori HÜCRE metninden, v6.173; sperm sayfaları
ve embriyo sayfalarındaki sperm satırları) için:
- **Hasta**: aynı ad kelime kümesinde yalnızca-sperm (tedavisi olmayan) TEK
  bir kayıt varsa onun altına (programda açılmış erkek ya da önceki
  çalıştırma); yoksa geçici dosya numarasıyla (v6.179'un 9000000001…
  dizisinden devam) yeni erkek kaydı. Aynı adın iki farklı eşi varsa iki
  kişi, eşsiz satırı atlanıyor (v6.179'un kuralı). Çift kayıtlarına (kadının
  adı) hiç bakılmıyor.
- **Her satır**: bir `sperm_dondurma` + bir taşıyıcı (`kategori='sperm'`,
  v6.84'ün "bir kayıt = bir taşıyıcı" kuralı). Etiket programın sperm
  formunun kalıbı `<dosya no>-SP-<SSDD>`; saat bilinmiyor, 10:00'dan
  başlayıp aynı gün dakika dakika. Konum Excel'in tank / kanister / goblet'i.
  Taşıyıcı tipi Excel'de yazıyorsa o (8 straw, 11 vial), yazmıyorsa
  **vial** -- sütunun adı VİAL, STRAW yalnızca dış merkezden gelen birkaç
  satırda ayrıca yazılmış. "Sayfa1"in tank bandı yok (tank adı sayfa adından
  geliyordu): haritada uydurma bir "SAYFA1" tankı açılmıyor, konum boş
  kalıyor, Excel'deki yer nota yazılıyor (15 tüp).
- **Dondurma sebebi**: HÜCRE'de "CA" geçiyorsa (EJAKÜLAT-CA, CA-SPERM,
  TESE-CA, "EJAKÜLAT(CA)") **Onkolojik** -- kullanıcının cevabı: "CA
  kanser"; değer programın sebep önerisinden (`SPERM_DONDURMA_SEBEPLERI`).
  Deneme: 1.531 tüpün 796'sı. Aracın ilk hali (aynı gün) sebep yazmıyordu;
  zaten çalıştırılmışsa ikinci çalıştırma bu aracın açtığı kayıtlara
  (notta `CRYO_EXCEL_ISARETI`) sebebi ekliyor (`sebep_yaz`, `degisiklik_log`),
  ekrandan girilmiş kayda dokunmuyor. CA yoksa HÜCRE'deki **TESE / TESA**
  sebep olarak yazılıyor (kullanıcı: "TESE/TESA yazılsın"; ikisi de listede;
  deneme: 240 TESE, 1 TESA). "TESE-CA"da alan tek, Onkolojik kazanıyor --
  HÜCRE'nin tamamı notta. Deneme: 1.531 tüpün 1.037'sinin sebebi dolu,
  494'ünde (düz EJAKÜLAT) boş.
- **Uydurulmayan**: hacim / konsantrasyon / motilite ("9 MİLYON %35" ml başına mı toplam mı
  belli değil). HÜCRE ve VİAL metni olduğu gibi nota:
  "Örnek: EJAKÜLAT-CA · VİAL: 1(A,B,C)", altında sayfa/satır ve
  `db.CRYO_EXCEL_ISARETI`.
- **Açılmayan**: tarihsiz (8) ve ileri tarihli (5; 2027/2028, yazım hatası)
  satırlar -- dondurma zamanı zorunlu alan, tarih uydurulmuyor; raporda
  listeleniyor, elle girilir.
- **Programda zaten varsa**: aynı ad + aynı gün + aynı konum "zaten"; o gün
  kaydı olup konumu boşsa (ekrandan girilmiş dondurma) konum yazılıyor
  (`degisiklik_log`); konumu farklıysa dokunulmuyor. İkinci çalıştırma
  hiçbir şeyi değiştirmez (denendi: 1.531 "zaten").
- Rapor `cryo_esle_rapor_sperm.txt` (hasta adı içerir, depoya girmez).

Deneme veritabanında: 1.544 sperm satırından 1.531 tüp, 609 erkek kaydı
(225'inin tek tüpü, en çok 12). Bu hastalar yalnızca-sperm olduğu için Tüm
Hastalar'da görünmüyor, aranınca rozetle çıkıyor (v6.98). İstatistik
etkilenmiyor (sperm dondurma oranlara girmiyor).

**Sperm Dondurma haritası** (`/cryo`, sağ sütun). Arama yokken düz liste
yerine ağaç: tank → kanister → goblet, her düzeyde tüp sayısı, kapalı
başlıyor (`<details>`; 1.500 tüp açık olsa sayfa metrelerce uzardı). Konumu
olmayan tüpler ayrı "konum girilmemiş" grubunda. Sıralama doğal (`"2" <
"10"`, `_dogal_sira()`). Aramada liste eskisi gibi düz -- hedefli bir
sorguda ağaç gereksiz tıklama. Ağaç `app.sperm_agaci_kur()`, satır tek
makro (`sperm_satiri`). Tank / kanister / goblet `konum.seviye1..3`: embriyo
tarafıyla aynı konum tablosu, ayrı yapı yok.

**Elle eşleştirme: erkeğin kartından "Eşine bağla"**. Bağın yeri v6.139'dan
beri çiftin `hasta.es_dosya_no`'su; çiftin kartından yazmak için erkeğin
geçici numarasını bilmek gerekiyordu. Şimdi spermi olan erkeğin kartında
"Eşinin tüp bebek kaydı" kartı: eşinin dosya numarası yazılıyor (canlı
önizleme `/hasta/kontrol`, v6.125: ikinci rota açılmadı), `POST
/hasta/{id}/es-bagla` çiftin `es_dosya_no`'suna bu hastanın numarasını
yazıyor. Aynı alan olduğu için çiftin kartındaki "Eşin dondurulmuş spermi"
ve oradaki **tedaviye bağla** kendiliğinden çalışıyor -- "tedavi hastalarına
bağlama" budur. Çiftin kaydında başka bir eş numarası yazılıysa ezilmiyor
(hata, beyaz liste `ES_BAG_HATALARI`, tuzak #9); değiştirmek o kaydın kendi
düzenleme ekranının işi. "Bağı kaldır" yalnızca numara bu hastanınsa
boşaltıyor; spermin tedaviye bağına dokunmuyor. İkisi de `degisiklik_log`'a
düşüyor, izin `hasta` modülü (`yol_modulu()`). Yalnızca-sperm erkeğin sperm
satırındaki "önce tedavi açılmalı" ipucu "tedaviye eşinin kaydından bağlanır"
oldu -- erkeğe tedavi açmak yanlış yöne gönderirdi.

**`dosya_no_degistir.py`**: sperm tüpünün etiketi dosya numarasını içeriyor
(embriyo tüpünün etiketi içermiyor). Eski numara **geçiciyse** hastanın
`<eski>-SP-SSDD` etiketleri `<yeni>-SP-SSDD` oluyor; gerçek numaralı tüpün
etiketine dokunulmuyor (tankta tüpün üstünde yazıyor olabilir). Denendi:
geçici → gerçek üç etiketi değiştirdi, gerçek → gerçek değiştirmedi.

# v6.179 — Cryo Excel'inden 2011–2017'nin hastaları

Kullanıcının isteği (2026-09-25): "390: hastanın programda kaydı yok. Büyük
kısmı 2011–2017'den. Bunları programa ekle." İki karar soruldu:

- **Kapsam: yalnızca 2011–2017** (TARİH < 2018). O yılların Access dosyası
  yok. 2018 ve sonrasında "hasta yok" satırlarının çoğunun programda
  **benzer adlı** bir hastası var (deneme veritabanında 2018–2023'ün 120
  satırının 86'sı: bir harf, eksik/fazla bir soyad) -- yeni kart aynı kişiyi
  iki kez açardı, yanlış hasta bu işin en pahalı hatası. Onlar açılmıyor.
- **Geçici dosya numarası**: Excel'de dosya numarası yok, `hasta.dosya_no`
  zorunlu. 9000000001'den başlayarak (gerçek numaralar 9 haneyi aşmıyor);
  hastanın notunda "GEÇİCİ dosya numarası" yazıyor, gerçeği
  `dosya_no_degistir.py` ile (denendi: tedavi, tüp etiketi değişmiyor).

`python3 cryo_esle.py yeni_hasta <excel>`: eşleştirmeyi çalıştırır, "hasta
yok" + 2018 öncesi satırları hastaya göre gruplar (ad kelime kümesi; aynı
adın iki farklı eşi varsa iki kişi, eşsiz satır atlanır), planı ve raporu
(`cryo_esle_rapor_yeni_hasta.txt`, hasta adı içerir, depoya girmez) basar,
"HASTA" onayıyla yazar:
- **Hasta** -> **tedavi**: aynı OPU günü (`_excel_opu()`, "D5" = TARİH − 5)
  bir tedavi; yalnızca yumurta tüpü varsa Yumurta Dondurma, yoksa IVF/ICSI.
  `durum='tamamlandi'`, `bitis_sebebi='dondurma'`. Protokol notu "Program
  öncesi kayıt: yalnızca Cryo Haritası Excel'indeki dondurma bilgisi (sayfa,
  satır). OPU, ICSI ve döllenme kaydı yok." + `db.CRYO_EXCEL_ISARETI`.
- **Tüp**: HÜCRE'nin her parantez grubu bir taşıyıcı (Access aktarımıyla
  aynı etiket kalıbı, `aktar_access._tasiyici_ac()`), konum/tip/renk
  Excel'den. Her öğe bir örnek: embriyoda değerlendirme
  (`aktar_access._oge_alanlari()`/`_degerlendirme_yaz()`, gün Excel'in
  "D"sinden), yumurtada olgunluk yazılıysa maturasyon; ardından
  vitrifikasyon. OPU/ICSI/döllenme **uydurulmuyor**.
- **İstatistik dışı**: `disari.istatistikler()`'in tedavi koşulu
  `db.CRYO_EXCEL_ISARETI` taşıyan tedavileri dışlıyor. v6.127'nin "sahte
  tedavi istatistiği bozar" gerekçesi: yalnızca dondurma bilgisi olan
  tedaviler oranlara girse 2011–2017 aylarında "%0 MII" gibi ölçülmemişi
  ölçülmüş gösterirdi. Denendi: öncesi/sonrası bütün istatistikler aynı,
  yalnızca hasta sayısı değişti.
- **Tek okuyucu**: `excel_icerik()` artık `excel_ogeleri()`'nin (öğe
  sözlükleri) metin hali; açılan tüp eşleştirmenin okuduğunu birebir tutsun
  diye. Refaktör sonrası 5.401 satırın hiçbiri farklı okunmadı.
- **İkinci çalıştırma hiçbir şey açmaz** (hasta artık var, tüpler "zaten
  yazılı"). Aynı gün birebir aynı içerikli tüpler Excel'in sırasıyla
  açılıyor -- başka sırayla açılınca ikinci eşleştirme onları çapraz
  eşleyip "başka konum yazılmış" diyordu (denemede 4 tüp, düzeltildi).

**2011–2017'nin HÜCRE yazımı** (kullanıcının cevapları, aynı gün):
"2G1" = **iki G1 embriyo** (hücre sayısı yazılmamış; "2 hücreli" değil --
v6.176'ya kadar öyle okunuyordu), "G1" tek G1 embriyo, "2XG1", "2 G1";
"10H" / "10H%5" = 10 hücreli, %5 fragmantasyon (`cl_fragmentasyon`); "UE" =
uneven, önündeki embriyonun simetrisi (`cl_simetri='esitsiz'`); "KAVKAV" =
iki kavitasyon; "7OOSİT" = yedi yumurta; "2MOR" = iki morula; "4H G1",
"GRD1" = G1; parantezsiz embriyo satırı ("D5 4BB-4BB", "5.GÜN 4AA 4AA
BİRARADA") tek tüp -- en az bir öğesi tanınıyorsa. Hücre sayısı yazılmamış
G'li embriyo programın her yerindeki gibi "skor girilmedi" görünüyor, derece
değerlendirmede saklı. Embriyo sayfalarındaki sperm satırları ("EJAJULAT-CA",
"TESTİS-CA") `cryo_excel._SPERM_IZI`'ne eklendi -- embriyo tüpü olarak
açılacaklardı. Eşleştirmeye etkisi: 2018 sonrasında 4 satır farklı okunuyor,
sınıfı değişen tek satır "içerik tutmuyor"dan "eşleşti"ye geçti.

Deneme veritabanında: 78 hasta, 79 tedavi, 110 tüp, 254 örnek; 7 satır
açılmadı (hücre okunamadı: boş, "OOSİT" sayısız, "D3ÜST3").

# v6.178 — Cryo Excel'i: yumurta ve refreeze tarihleri

v6.177'nin iki sorusuna kullanıcının cevabı (2026-09-25): "yumurta dondurma
OPU günü yapılıyor. Refreezeler çözme günü tekrar dondurulabilir, 3'ten 5
birkaç embriyo büyütülüp transfer sonrası kalan embriyolar tekrar
dondurulabilir, veya 4. gün dondurulmuş embriyolar 5. güne büyütülebilir.
Transfer fazlaları tekrar dondurulabilir."

`_TARIH_OLCULERI`: tarih tutmayan satır için sırayla üç ölçü, hepsinde hasta
aynı ve içerik birebir:
1. `opu` (v6.177): TARİH − Excel'in günü = tedavinin OPU'su.
2. `yumurta_bir_gun`: yumurta satırı ile yumurta tüpü (dondurma günü = OPU)
   arasında bir gün fark. Bir tedavide tek OPU var, yumurta o gün
   dondurulur; bir günlük kayma iki ayrı dondurma olamaz. Hangi tarihin
   doğru olduğu (Access'in OPU'su mu, Excel mi) bilinmiyor, tarihe
   dokunulmuyor -- yalnızca konum yazılıyor.
3. `refreeze_gunu`: FET'te yeniden dondurulan tüp (dondurmanın tedavisi
   `FET_TIPLERI`'nde): program çözme/transfer gününü yazıyor, Excel 1–3 gün
   sonrasını (kültür 3→5, 4→5, transfer artığı). Excel'in günü programdan
   ÖNCE olamaz.

Serbest bir ±N gün toleransı yine yok. Deneme veritabanında 28 satır "o gün
tüp yok"tan çıktı (15 `yumurta_bir_gun`, 9 `refreeze_gunu`, 3 eş adı
tutmuyor, 1 içerik tutmuyor); başka hiçbir satır değişmedi.

# v6.177 — Cryo Excel'i: tarih tutmayınca OPU gününden eşleştirme

v6.176'daki soruya kullanıcının cevabı (2026-09-25): "Excel'de dondurma günü
yazıyor. 5. gün dondurma ise OPU gününden 5 gün sonra, 3. gün dondurma ise
OPU gününden 3 gün sonra dondurma yapılıyor."

Programdaki tüpün günü Access'ten kuruldu: OPU + nottaki gün, gün okunamazsa
5 (`aktar_access._dondurma_zamani()`). Not gün yazmadığında ya da farklı
yazdığında (Excel D6, program D5) tüp bir iki gün kayık duruyor. Excel'in
günü ise kendi HÜCRE'sinde: "D6 (4AA)".

`_excel_opu()`: tarih tutmayan satırda TARİH − Excel'in günü (yumurtada 0) =
OPU günü; hastanın dondurma tedavisinin (`db.vit_tedavisi()`) OPU'su bununla
tutuyorsa aynı tedavi, tüp içerikle yine birebir aranıyor. Yeni sınıf
`opu_gunu` (yazılır, raporda ayrı başlık). Önce günü tutan satırlar dağıtılıyor,
OPU'dan bulunan satır onların tüpünü almıyor.

Deneme veritabanında 13 satır "o gün tüp yok"tan `opu_gunu`'na geçti (çoğu
Excel D6 / program D5), 5'i "içerik tutmuyor"a (tedavi bulundu, içerik
farklı); başka hiçbir satır değişmedi.

**Hâlâ tutmayanlar, kullanıcıya soruldu:**
- Yumurta satırları Excel'de düzenli olarak OPU'dan **bir gün sonra**
  (program yumurtayı OPU günü dondurulmuş sayıyor, v6.130'dan beri).
- OPU'su olmayan tüpler (FET'te yeniden dondurulan, program çözme/transfer
  gününü yazıyor): Excel 1–3 gün sonrasını yazıyor.

# v6.176 — Cryo Excel'inin hücre yazımları (cryo_esle.py)

Kullanıcı güncel Cryo haritası Excel'ini gönderdi (2026-09-25; önceki
dosyadan 6 satır eksik, 1 satır fazla -- çözülen/yeni dondurulan tüpler).
Deneme veritabanında (2018–2023, eyl–ara 2024, oca–may 2025, mayıs 2026)
`liste` çalıştırıldı; tam aktarılmış yıllarda "içerik tutmuyor" satırlarının
bir kısmı Excel'in kendi yazım alışkanlığıydı, veride bir fark değil:

- Evre ile derece arasında boşluk: "MORULA G2", "KAV G3", "BİRLEŞME G1",
  "BİR G2" -- boşluktan bölünüp iki okunamayan öğe oluyordu.
- İki embriyo arasında yıldız: "3BB*3BB", "3BA*1CC" ("3*KAVG3" ise çarpan).
- Blastokist skoruna bitişik evre: "2CCKAVG3" -- 2CC okunuyor, KAVG3
  sessizce düşüyordu (tüp iki embriyo, Excel bir diyordu).
- Çarpan: "3*KAVG3", "2X8HG1", "3 ADET MORULA G2" (Access okuyucusunun
  v6.173 kuralı; yalnızca embriyoda, yumurtada `_skor_coz()` kendisi sayıyor).

`_yazimi_duzelt()` + `excel_icerik()`'in çarpan dalı. Eski ve yeni araç satır
satır karşılaştırıldı: 13 satır "içerik tutmuyor"dan yazılır bir sınıfa
geçti, daha önce eşleşen hiçbir satır değişmedi. Yazılacak 2046 → 2059.

**Bilerek yapılmayan: tarih toleransı.** 2019–2023'te "o gün tüp yok"
satırlarının ~45'inde programdaki dondurma günü Excel'inkinden 1–5 gün farklı
(yumurtalar çoğunlukla Excel'de bir gün sonra, bazı D5/D6 embriyolar üç gün
önce). Düzeni tek değil; hangisinin doğru olduğu (Access'in tarihi mi,
haritanın mı) kullanıcıya soruldu, cevap gelmeden gevşetilmedi.

Kalan büyük sınıflar deneme veritabanının eksik aylarından (oca–ağu 2024,
haz–ara 2025, 2026'nın mayıs dışı) -- "hasta yok" 1197'nin ~940'ı 2024–2026.
Kullanıcının veritabanında bu aylar var; sayılar orada ölçülecek.

# v6.175 — Yanlış tüpe bağlanmış FET: skor onarımı, `tasi` kipi, kayıt sırası (goc_050)

Kullanıcı `bagla`'yı çalıştırdı (v6.174), çıktının "Bağlı ama artık kesin
değil" listesinde üç FET vardı (TEMMUZ2019#54, MAYIS2025#25, HAZIRAN#37) ve
listeyi gönderdi. İlkini inceleyince üç ayrı hata çıktı.

**1. Skoru okunmamış tüp her transferle tutuyordu.** Şubat 2019'da bir
embriyo "1 ADET 5.GÜN 4AB EMBRİYOSU DONDURULARAK SAKLANMIŞTIR" diye
dondurulmuş: parantezsiz yazım. v6.172'nin okuyucusu bunu skorsuz embriyo
sandı (v6.173'ünki 4AB okuyor), tüp skorsuz yazıldı. Skorsuz tüp her transfer
yazımıyla tutar: Temmuz 2019 FET'i (1BB transfer) o gün tek seçenek olarak
ona bağlandı. 2018 gelince hastanın 1BB'lik gerçek tüpü de göründü ("kesin
değil"); Kasım 2019 FET'i (4AB transfer) ise 2018'in KAV3 tüpüne bağlanmıştı
("kültürde ilerlemiş olabilir"), listede bile yoktu. Access notları kesin:
Temmuz sonrası "GERİYE 2 TÜPTE 2 ADET", Kasım sonrası "GERİYE 1 TÜPTE(KAVG3)".
Yani Temmuz 1BB'yi, Kasım 4AB'yi çözdü, KAV3 tankta. İki bağ da yanlıştı.
- **Kaç kayıt:** eski (v6.172) ve yeni okuyucu, elimdeki 69 aylık dosyanın
  (2019–2023, 2024 eylül–aralık, 2025 ocak–mayıs, 2026 mayıs) bütün
  dondurma notlarında karşılaştırıldı: dört satır farklı (SUBAT2019 #56 ve
  #66, ARALIK2019 #17, OCAK2020 #69). Yalnızca #56'nın tüpü yanlış bağlandı;
  öteki üçü doğru bağlı ya da hiç çözülmemiş. v6.173'teki "2019 ve sonrası
  değişmedi" ölçümü `liste` çıktısını karşılaştırıyordu, skoru değil --
  yanlıştı.
- **Onarım yolu `dondurma` kipi** (v6.165'ten beri "yalnızca eksik olanı
  yazar"): tüpte duran örneğin bu tedavide hiç değerlendirmesi yoksa ve not
  gerçek bir skor veriyorsa (blastokist ya da hücre sayılı cleavage) skor
  yazılıyor. Aktarımın kendi boş değerlendirmesi (hücre, skor, genişleme boş;
  not "Kaynak kayıttaki yazım: ...") "yok" sayılıyor: v6.172 "1 ADET 3.GÜN
  8HG2 EMBRİYOSU"nu öyle yazmıştı. Birleşme, elle girilmiş ya da dolu her
  değerlendirme olduğu gibi kalıyor (`_degerlendirmesi_var()`). Skorsuz öğe
  ("G1", "HG2") yazılmıyor. Deneme: 80 dosyanın hepsinde `dondurma` -- tam
  bu dört skor yazıldı (iki yeni blastokist, iki boş cleavage kaydı
  dolduruldu); ayrıca test veritabanında o aylar için `dondurma` hiç
  çalıştırılmamış üç tedaviye eski kuralın eksik örnekleri eklendi, başka
  hiçbir şey değişmedi.

**2. Yanlış bağ çözülemiyordu.** v6.164'ten beri araç "kesin değil" diyor
ama bağı çözmüyordu, çünkü hangi tüpün çözüldüğünü kâğıt biliyor. Yeni
**`tasi` kipi** kullanıcının gösterdiği tüpe taşıyor:
`python3 aktar_access.py tasi TEMMUZ2019#54 2018-0890-1200`. Yeni tüp
`_bag_siniflari()`'nin adayı olmalı (hastanın dolu, çözülmemiş, çözmeden önce
dondurulmuş, doğru türde tüpü) ve örnek sayısı tutmalı. FET'te yapılan her
olay (çözme, transfer, yeniden dondurma, değerlendirme; `db.bu_tedavide()`)
yeni örneğe geçiyor. Eski örnek "dondurulmuş"a, eski tüp "dolu"ya dönüyor,
yeni tüp boşaltılıyor, protokol notunun "... tedavisinde dondurulmuştu"
cümlesi yenileniyor. Transfer günü değerlendirmesinin çakışma kuralı
(v6.163) yeni kaynağa göre yeniden uygulanıyor. Eski örneklerde bu FET'ten
sonra başka tedavinin kaydı ya da fotoğraf/bulgu varsa taşımıyor. Önce planı
basıyor, "TASI" yazınca yazıyor, değişiklik geçmişine düşüyor; aynı tüpe
ikinci kez "zaten bu tüpte" diyor. Transfer yazımı seçilen tüple tutmuyorsa
"DİKKAT" basıyor ama engellemiyor: karar kullanıcının.

**3. Kayıt sırası: 2018'in tüpleri "yeniden dondurma" görünüyordu.** Program
"önce dondurma mı çözme mi" sorusunu kayıt kimliğinin sırasıyla soruyor, saatle
değil (v6.143: saat elle geri tarihlenebilir). Aylar karışık sırayla
aktarıldı. Bir FET'in çözmesi yazıldıktan SONRA çözülen tüpün dondurması
aktarıldı ve `_kaynaga_bagla()` ikisini aynı embriyoya bağladı: çözmenin
kimliği küçük kaldı. Hasta kartı 2018'de dondurulup 2019'da çözülen tüpe
"Yeniden donduruldu → 4. tedavide çözüldü" diyordu. FET'in formu çözülmüş
tüpü "Kalan dondurulmuş"ta sayıyordu. Deneme veritabanında 342 FET'in 555
çözmesi böyleydi.
- **`goc_050`** (`db.olay_sirasini_duzelt()`): bu örneklerin çözmeden
  sonraki bütün olayları, saat sırasıyla (aralarındaki sıra korunuyor), yeni
  kimlikle yeniden yazılıyor. İçerik aynı (deneme: 157.584 olayın çoklu
  kümesi birebir), 1.600 satır yeni kimlik aldı. Olay kimliğine bağlı tablo
  yok; değişiklik geçmişinin olay satırları yeni kimliğe çevriliyor. Yalnızca
  aktarımın kayıtları: çözme [Access kaydı] işaretli bir FET'in, dondurma
  aktarımın notunu taşıyor, aynı tüp. Programdan girilmiş kayıtta kimlik
  sırası gerçekten giriş sırası, oraya dokunulmuyor. İkinci çalıştırma 0.
- `_kaynaga_bagla()` ve `tasi` aynı işlevi bağladıkları örneklerde
  çağırıyor.
- **Kural:** aktarımda olayları bir örnekten ötekine taşıyan yeni bir yol
  yazarsan sonunda `db.olay_sirasini_duzelt(b, örnekler)` çağır.

**Sonuç (deneme kopyası, göç + iki `dondurma` + iki `tasi`):** Temmuz FET'inin
formu "Kalan dondurulmuş: 2 tüp: (KAV3) (4AB)", Kasım'ınki "1 tüp: (KAV3)"
diyor, Access'in iki notu ile aynı. Hasta kartında yanlış rozet yok. Tablo
tablo karşılaştırmada yalnızca beklenen satırlar değişti. 21 ekran 200.
`bagla` sonrası TEMMUZ2019#54 "kesin değil" listesinden çıktı.

**Öteki iki kayıt kullanıcının kararı** (araç tahmin etmiyor):
- MAYIS2025#25: çözülen 8, transfer "5. gün 2BA, 1BA", not "KÜLTÜRE EDİLEN
  1 ADET D5 EMBRİYOSU (1CC) ... TOPLAMDA 2 TÜPTE 3 ADET EMBRİYOSU KALDI".
  Bağlı seçenek mart'ın iki 4'lü 3. gün tüpü: çözüp 5. güne kültür ile tutuyor,
  geride kalan 5. gün embriyoları (ocak tüpünün 2'si + yeni 1CC) "2 tüpte 3".
  Öteki seçenek bir 3. gün ve bir 5. gün tüpünü birlikte çözmek. Kullanıcı
  doğruladı (2026-09-25): "MAYIS ayı doğru, 2 tüpte 3 D5 embriyo kaldı".
  Bağ olduğu gibi kalıyor; `bagla` onu "kesin değil" listesinde göstermeye
  devam eder (araç kullanıcının onayını saklamıyor).
- HAZIRAN#37 (2026): haziran 2026 dosyası elimde değildi, karar
  kullanıcının. Kendi makinesinde `tasi` ile 2022-0135'in üç tüpüne taşıdı
  (5 embriyo); 2026-0507-1200 yeniden dolu. Bu, gerçek veride `tasi`'nin ilk
  çalışması; çıktı denemeyle aynı biçimde.
- Kullanıcının makinesinde sonuç (2026-09-25): üç `dondurma` komutu ilk
  seferde "CSV dosyasi bulunamadi" ile durdu (2019–2023'ün CSV'leri proje
  klasöründe değildi), KASIM2019#63 bu yüzden skorsuz 2019-0146 tüpüyle "kesin
  değil" listesinde kaldı. Dosyalar klasöre konup veritabanı `tasi.py` ile
  Mac'e alınarak yeniden çalıştırıldı; `bagla`'nın listesinde yalnızca
  onaylanmış MAYIS2025#25 ve HAZIRAN#37 kaldı. **Ders**: dosya isteyen bir
  onarım komutu verirken dosyanın o makinede nerede olduğunu da sor.

# v6.174 — Ağustos 2018 boş ay

Kullanıcının cevabı (2026-09-25): "Ağustos 2018'de laboratuvarda hiç işlem
yapılmadı." Ay, mayıs 2020 gibi `aktar_access._BOS_AYLAR`'a eklendi.

**Neden önemli**: FET bağlama (`butun_fetleri_bagla()`, v6.164) tutan tüp ile
çözme arasında aktarılmamış bir ay varsa bağlamayı erteliyor -- o ayda
dondurulmuş başka bir tüp olabilir, soyağacı yanlış kurulmasın diye. Ağustos
2018'in dosyası yoktu; ay "aktarılmamış" sayılıyor, 2018'in ilk yedi ayının
tüplerini eylül 2018 ve sonrasında çözen FET'ler bekliyordu. Ay boş olduğu
için bekleyecek bir şey yok.

**Kullanıcının makinesinde bir kez**: `git pull origin main`, sonra
`python3 aktar_access.py bagla` (dosyasız, bütün veritabanı; ~20 dk). Deneme
kopyasında (2019–2023 + 2018 aktarılmış) ertelenenler 119'dan 57'ye indi,
52 FET 2018'in tüplerine bağlandı. İkinci çalıştırma hiçbir şey değiştirmez.

Başka değişiklik yok. `_BOS_AYLAR`'a ay eklemek "o ayda dondurulmuş tüp yok"
demek; yalnızca kullanıcı söyleyince eklenir.

# v6.173 — Cryo haritası Excel'i tüplere bağlanıyor; 2018 Access aktarımı

İki iş, ikisi de kullanıcının isteğiyle (2026-09-24): "aktarım yapılırken
daha önce denediğim cryo haritayı yeniden incelemeni istiyorum ... Bu hasta
kayıtları ile cryo haritayı ilişkilendirmeni istiyorum" ve ardından "2018
hasta aktarımı var. Önce onu yapsan".

## Cryo haritası: `cryo_esle.py` + `cryo_excel.py`

Laboratuvarın kriyo haritası Excel'de (6 sayfa, 5.406 satır: 3.868
embriyo/yumurta, 1.538 sperm; 2011–2026; tank / kanister / goblet başına
SOYAD, AD, EŞİ, TARİH, HÜCRE, VİAL). Dosya numarası yok. v6.127/v6.128 bu
haritayı ayrı bir tabloya alıp isimle aday öneriyordu, v6.129'da geri alındı
("istediğim gibi olmadı"). Şimdi kullanıcının veritabanında Access'ten
aktarılmış 5.000'den fazla dondurma tüpü var (2019–2026), konumları boş
(Access'te konum yoktu). **Bu sefer harita o tüpleri konumlandırıyor**:
yeni tablo yok, Excel satırı tüpe bağlanıyor, tüpün `konum_id`'si (Tank /
Kanister / Goblet), tipi ve rengi yazılıyor. Cryo Haritası ekranı ve
`/disari/cryo` zaten `tasiyici.konum_id`'den besleniyor, dokunulmadı.

**Eşleşme ölçüsü üç parça, ad tek başına yetmiyor:**

1. Hasta: Excel'in SOYAD + AD kelime kümesi programdaki `ad_soyad`'ın kelime
   kümesine eşit (sıra önemsiz: Excel'de iki sütun, programda tek kutu).
   Aynı adlı birden çok hasta varsa eş adı ayırıyor; o da ayırmazsa Excel'in
   tarihinde tüpü olan tek aday (89 satır böyle çözüldü, raporda ayrı
   başlık).
2. Dondurma günü: Excel TARİH = tüpün vitrifikasyon günü.
3. İçerik: HÜCRE'nin skorları ("D5 (3AA-4AB)", "OOSİT (3M2-1M1)", "3 M2
   OOSİT") tüpteki örneklerin skor/olgunluk çoklu kümesine eşit. Yazım
   Access notlarınınkiyle aynı, `aktar_access._skor_coz()` çözüyor;
   karşılaştırma gevşek ("8HG2" = "8G2", MII = M2, morfoloji nitelemesi
   HATCHİNG/OVAL atlanıyor, "10HG2*" yıldızsız). Olgunluğu yazılmamış
   yumurta ("3 OOSİT") sayıyla tutuyor.

**Aynı hasta + aynı günün satırları ve tüpleri birlikte dağıtılıyor.**
Programda birebir aynı içerikli iki tüp (iki "(4AA)") birbirinden ayırt
edilemez: etiket Access'ten üretilmiş, konum boş. Excel'de aynı içerikli iki
satır varsa sırayla eşleşiyor (v6.148'in "aynı tedavinin birebir aynı
tüpleri fark etmez" kuralı; ölçüm 414 satır). Tüp sayısı satır sayısını
aşıyorsa (Excel'de bir satır, programda üç aynı tüp) o satır listeleniyor,
yazılmıyor: hangisinin tankta olduğu bilinmiyor.

**Yazılmayan her satır raporda kendi başlığıyla** (`cryo_esle_rapor.txt`,
hasta adı içerir, depoya girmez): hasta programda yok, aynı adlı hasta, o
gün tüp yok (hastanın programdaki dondurma günleriyle), içerik tutmuyor
(tüplerin içeriğiyle), programda boşaltılmış/kullanılmış tüp (Excel tankta
diyor -- bakılmalı), tüpe daha önce başka bir konum yazılmış (elle girilmiş
olabilir, ezilmiyor), iki satır aynı tüpü istiyor, ad tutuyor eş adı
tutmuyor (bulunan tüp yazılı, karar kullanıcının). **Sahte tedavi/tüp
açılmıyor** -- v6.127'nin gerekçesi: eşleşmeyen satır için kayıt üretmek
istatistikleri bozar. Sperm sayfaları yalnızca sayılıyor: Access'te sperm
tablosu yoktu, programda karşılığı yok.

Test veritabanında (2019–2023 + 2024 eylül–aralık + 2025 ocak–mayıs + 2026
mayıs) 3.868 satırın **1.977'si yazıldı** (1.456 birebir, 414 aynı içerikli
dağıtım, 18 sayıyla, 89 tarih ayırdı), 1.282'si "hasta yok" (951'i test
veritabanında olmayan aylar, ~210'u 2011–2018 -- Access dosyası yok), 336
"o gün tüp yok", 158 "hiç tüpü yok", 77 içerik tutmuyor, 20 eş adı, 8
tarihsiz, 3 boşaltılmış. İkinci çalıştırma: 1.977 "zaten", 0 yazma.
`uygula` "ESLE" onayı istiyor, `yazma_islemi()` içinde yazıyor,
`degisiklik_log`'a düşüyor (tablo `tasiyici`, alan `konum`/`tip`/`renk`);
Rapid-i ve Vitrifit taşıyıcı tipleri listede yoksa ekleniyor (goc_042'nin
geri alınan iki satırı). Ekranlar denendi: `/cryo`, arama, taşıyıcı
sayfası, `/disari/cryo` 200.

**`/cryo` 5.000 tüple açılmıyordu -- `goc_049`.** Ekran her dolu tüp için
"kaç örnek" ve "yumurta mı embriyo mu" alt sorgularını `olay.vit_tasiyici_id`
üzerinden soruyor; kolonun dizini yoktu, tüp başına 137.000 satırlık `olay`
taranıyordu. Programın kendi girdiği birkaç yüz tüpte fark edilmedi; test
veritabanında sorgu bir dakikada bitmedi, `olay(vit_tasiyici_id)` diziniyle
0,04 sn (sayfa 0,7 sn). Çözmenin tüpü goc_046'dan beri dizinliydi,
dondurmanınki unutulmuştu. Kullanıcı 2019–2023'ü aktardığı için bu artık
onun makinesinde de böyle: göç açılışta kendiliğinden çalışır.

Kod: `cryo_excel.py` v6.128'in çözümleyicisi (`git show 51efd53:eski_cryo.py`)
olduğu gibi, içeri alma/aday kısımları atılmış; `xlsx_oku.izgara()` (aynı
sürümden) geri geldi; `konum_bul_veya_olustur()` app.py'den `db.py`'ye
taşındı (araç açık bağlantıda aynı kuralı kullanıyor, ikinci kopya olmasın
diye). Kullanıcının cevabı bekleyen sorular CLAUDE.md'de (geçen sefer neyi
istemediği, `eski_cryo_temizle.py`, VİAL sütunundaki renk+sıra, sperm
sayfaları); cevaba göre `/cryo` ekranı yeniden tasarlanacak.

## 2018 Access aktarımı

11 dosya (ağustos yok), 918 satır; sütunlar 2019 ile aynı. 2018'in not
yazımı daha eski: tüp "VİAL", parantez seyrek, sayı yazıyla. `liste` 13
notta "kaç örnek/tüp okunamadı" dedi; hepsi okundu (bkz. aşağıda), eski/yeni
karşılaştırmasında **2019 ve sonrasının okuması değişmedi**.

- **VİAL = tüp**: "2 VİALDE", "3 VİAL OLARAK", "2 VİAL OLMAK ÜZERE", "1
  VİALDE BİRARADA", "AYNI VİALDE", "2 AYRI VİALDE"; **sayı yazıyla**: "BİR
  ADET 3AC EMBRİYO", "İKİ ADET 3.GÜN EMBRİYOSU". Okuma kuralları "TÜPTE" ve
  rakam bekliyor; `_esanlam()` yazımı ona çeviriyor -- `ham` ve hizalı
  metne **aynı konumlardan** (ikisi aynı uzunlukta kalmalı: nota yazılan
  "Kaynak kayıttaki yazım" ham metinden, eşleşmeler hizalıdan).
- **"DR." cümle sonu değil**: "... 2 VİALDE DR. MEHMET ...'NIN İSTEĞİ ÜZERİNE
  DONDURULMUŞTUR". Cümle "DR."den sonra başlatılıyor, parantezler cümlenin
  dışında kalıyor, üç notun tüpleri yazılmıyordu. `_CUMLE_SONU` /
  `_CUMLE_BASI` tek yerde.
- **Embriyo çarpanı**: "(3xMORULAG2)", "(2XMORULAG3)", "(3*KAVG3)", "2X8HG1"
  -- yumurtanın "4*M2" yazımının embriyo hali (`_grup_coz()`).
- **Parantezsiz embriyo** (`_parantezsiz_embriyo()`): "1 TÜPTE 7HG1 VE 1
  TÜPTE 10HG1 ... AYRI AYRI" (her "N TÜPTE"den sonraki skorlar o tüpte); "1
  ADET 4AA, 1 ADET 4BB VE 2 ADET 2BB-1BB OLMAK ÜZERE 3 VİAL" (öğe sayısı tüp
  sayısına eşit, her öğe bir tüp); "2 ADET 1BB-3AA ... BİRARADA", "2 ADET
  3.GÜN 8HG1 ... AYNI VİALDE" (tek tüp, tek skor ADET kez), "BİR ADET 3AC".
  Skor sayısı ADET'le tutmuyorsa yazılmıyor, uyarı. "8 ADET 3.GÜN EMBRİYOSU
  2 VİAL OLMAK ÜZERE" (dağılım yok) hâlâ yazılmıyor -- uydurulmuyor.
- Parantezsiz embriyonun sayısı önce DONDURULAN ("1 ADET 10HG2 VE 12HG1 ...
  BİRARADA": notun ADET'i 1, DONDURULAN 2 -- yapılandırılmış alan önce,
  v6.142); "KAVİTASYON G3" derece ayrı kelime. Not grupsuzsa aşama
  kutusundaki parantezler okunuyor (not "1 TÜPTE 4 EMBRİYO ... BİRARADA",
  kutu "(3X8H2-7HG2)").
- Yumurtada "3XMII, 2XMII, 2XMI-7GV OLMAK ÜZERE OOSİTLER 3 VİALDE AYRI AYRI":
  X çarpanı, GV, virgül/VE ile ayrılmış parçalar tüp sayısı kadarsa her
  parça bir tüp.
- **Kaynakta hiçbir sayı yok**: üç Yumurta Dondurma satırında TOPLANAN, MII,
  İMMATÜR, ICSI boş; not 14, 12 ve 4 yumurta donduruyor. Açılan yumurta 0
  olduğu için tüp yazılmıyordu -- tankta duran 30 yumurta programda
  görünmeyecekti. Dondurulan yumurta toplanmış yumurtadır: sayı nottan
  (alttan sınır, `_cozulen_sayisi()`'nin mantığı), olgunluk yalnızca notta
  yazılıysa ("4 ADET OOSİT BİRARADA" olgunluksuz, v6.160'ın `olcusuz`'u).
  Not bunu söylüyor, `liste` "[toplanan boş → 14, dondurma notundan]".
- Aşama kutusundaki "1X7HG1-1X10HG1", "2X8HG1", "2BC", "8HG1-8HG2" gün
  değil (1, 2 ya da 8. gün okunuyordu; not "3.GÜN" diyor): rakamın
  arkasında harf varsa gün yok. 2019 ve sonrasında bu yazım yok (ölçüldü).
- **Dondurulan sperm**: "1 VİAL SPERMİ DONDURULMUŞTUR", "GV OOSİTİN ZONA
  PELLUSİDASI İÇİNDE 10 ADET HAREKETLİ SPERM DONDURULARAK SAKLANMIŞTIR" --
  fiilin nesnesi sperm, embriyo/yumurta dondurması değil (önce "okunamadı"
  ya da "10 örnek, 0 uygun kayıt" uyarısı çıkıyordu).
- "7HGW", "9HG", hücre sayısı yazılmamış "G1"/"HG2": skorsuz embriyo, sayı
  doğru, yazım değerlendirmenin notunda.
- **Düzeltme dosyasında eski tarih `-`**: kaynakta okunamayan tarih ("01/00/00
  00:00:00"; araç boş okuyor). `tarih_duzeltme_2018.txt` (depoda değil): üç
  tarih (ay/yıl yanlış, transfer okunamıyor; gerekçeler dosyada), bir yer
  tutucu dosya numarası (Şubat 2019 #6'daki aynı hasta, aynı "455").
- **`aktar_toplu.py` aktarılmış ayı atlıyor**: klasörde 2019–2023'ün 53
  dosyası duruyor; hepsini yeniden çalıştırmak (idempotent ama dosya başına
  dakikalar) saatler alırdı. İlk hali "o etiketle tek tedavi varsa bitmiş"
  sayıyordu -- yarıda kalmış bir dosyanın kalan satırlarını hiç aktarmazdı.
  Bugün ölçü aracın kendi `liste`'si: her dosya önce `liste`'den geçiyor
  (dosya başına ~7 sn), ekrana "OCAK2018  52 tedavi yazılacak" basılıyor,
  "AKTAR" ondan sonra soruluyor; "0 yazılacak" diyen dosya atlanıyor.
- **Windows'ta ilk dosyada çöküyordu** (kullanıcı, kliniğin makinesinde):
  `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfd`. Windows'ta bir
  Python süreci boruya konsolun değil sistemin kod sayfasıyla yazıyor --
  Türkçe Windows'ta cp1254 ("ı" 0xFD, "İ" 0xDD); `aktar_toplu.py` UTF-8
  okuyordu. cp1254'te "→" da yok: alt süreç o karakteri basarken kendisi de
  patlayabilir. Mac'te boru UTF-8 olduğu için görülmemişti. Alt süreç artık
  `PYTHONIOENCODING=utf-8` ile çalışıyor, okuma `errors="replace"`.
  Burada Windows benzetimiyle (alt süreç borusu cp1254) eski araçla hata
  birebir üretildi; yeni araçla yarıda kalmış OCAK2018 (30/82) kalan 52
  satırla tamamlandı, SUBAT2018 aktarıldı, aktarılmış OCAK2019 atlandı.
- **Kontrol haziran 2023'te durdu** (kullanıcı, aynı makinede, düzeltmeden
  sonra): "DUR -- ... # 41 dosya 41 -> işaret 2023-0637 tedavisini buluyor
  (BAŞKA hasta)". Çakışma gerçek değildi: haziran 2023'ün yer tutucu dosya
  numarası 2023'ün düzeltme dosyasında gerçek numarasına çevriliyor, araç
  ise bütün klasörü yalnızca verilen tek dosyayla (2018'inki) kontrol
  ediyordu. Artık klasördeki bütün `tarih_duzeltme*.txt` dosyaları
  birleştirilip her aya veriliyor (satırlar kendi etiketini taşıyor, araç
  yalnızca o ayınkini uyguluyor); aynı kayda iki dosyada farklı düzeltme
  varsa araç durup ikisini gösteriyor. Kontrolü geçemeyen bir ay da artık
  bütün işi durdurmuyor: "KONTROL EDİLEMEDİ -- aktarılmayacak" diye
  listeleniyor, sebebi planın altında, öteki aylar aktarılıyor. Denendi:
  yalnız 2018 dosyasıyla haziran 2023 listelendi ve 2018 planı geldi;
  2023'ün dosyası da klasördeyken haziran 2023 "zaten aktarılmış" sayıldı.

Denendi: 11 dosya test veritabanına (2019–2023'ün üstüne) aktarıldı --
**918 tedavi, 0 hata, 11 uyarı**, 533 yeni hasta kartı, 290 tüp. Uyarılar
kaynağın boşlukları: dört satırda ICSI ve 2PN boş ama embriyo dondurulmuş
(döllenme uydurulmuyor; ICSI sayısı düzeltme dosyasına yazılırsa tüpler
girer -- dosyada yorum satırı olarak hazır), bir satırda 2PN 1 / dondurulan
2, "(3M2-1M1) (M2)" diyen notun ADET'i 7, "(8HG1HG1)", "(2BC-BC-1BB)",
dağılımsız "8 ADET ... 2 VİAL" ve olgunluğu yazılmamış 4 yumurta (bilgi).
Son dosyanın bağlaması: 50 FET 2018'in tüplerine bağlandı, "tüpü programda
yok" 388'den 339'a indi. **Ağustos 2018 dosyası arşivde yok**: ay boşsa
(mayıs 2020 gibi) `_BOS_AYLAR`'a eklenecek, değilse dosyası gelince
aktarılacak -- kullanıcıya soruldu; o zamana kadar ağustosu aşan FET'ler
"ertelendi" (cevap geldi, v6.174). Cryo Excel'iyle eşleşme 1.977'den 2.040 satıra çıktı. Yeni
Yumurta Dondurma tedavisinin sayfaları ve iki formu 200; ART Lab'ın FREEZE
kutuları "(3*MII) (2*MII) (2*MI-7*GV)".

# v6.172 — 2019–2022 ve temmuz–aralık 2023 Access aktarımı: yeni okuma kuralları

Kullanıcı beş yılın Access dosyalarını `.rar` arşivleriyle verdi (2019, 2020,
2021, 2022 tam; 2023'ün temmuz–aralık'ı; 2020'nin mayısı arşivde yok). 53
dosya, 5.7 bin satır. Hepsi CSV'ye çevrilip `liste` kipinden geçirildi; eski
yılların not yazımı bugünkünden farklı, aracın tanımadığı on kadar kalıp
çıktı. Hepsi yalnızca `aktar_access.py`'de; program değişmedi.

**Eski/yeni karşılaştırması** (CLAUDE.md'nin kuralı): bütün CSV'lerin
`liste` çıktısı eski ve yeni araçla karşılaştırıldı. **Daha önce aktarılmış
ayların (2023 ocak–haziran, 2024 eylül–aralık, 2025 ocak–mayıs, 2026)
okuması değişmedi** — onarım gerekmiyor. Farklar yalnızca yeni dosyalarda.

## Yumurta notlarında

- **GV bir olgunluk**: "(4*GV)", "(2M1-1GV)", "(M2-M2-M2-GV)". Tanınmıyor,
  o yumurtalar tüpe hiç yazılmıyordu (uyarıyla; aralık 2022'nin bir
  tedavisinde 14 yumurtanın 8'i). Programın maturasyon listesinde `gv` zaten
  var. Access'in kutusu "İMMATÜR (MI+GV)" tek sayı: GV yumurta MI havuzundan
  alınıyor, atanınca maturasyon kaydı `gv` yazılıyor — not kazanır (v6.161'in
  kuralı). İkinci çalıştırmada yer değişmesin diye tüpteki yumurta önce kendi
  ham olgunluğuyla eşleşiyor (`_ham_olgunluk()`): GV yeri GV yumurtaya, MI
  yeri MI'ya.
- **"(1MA)"** — "MORFOLOJİK ANOMALİLİ OOSİT ... (1MA)": morfolojik
  anomalili yumurta (kullanıcı doğruladı), olgunluğu yazmıyor. Olgunluk boş (uydurulmuyor), form "?" basar; kaynağın sayılarının
  ötesindeki yumurtadan (`olcusuz` havuzu, v6.160).
- **Parantezsiz ama sayılı yazım**: "2M2 VE 1M1 TOPLAM 3 OOSİT BİR TÜPTE",
  "1 TÜPTE 5M2 1 M1 OOSİTİ", "6 ADET MII OOSİT 1 TÜPTE 3 MII VE 1 TÜPTE 3MII
  ... 2 TÜPTE". Olgunluklar sayısıyla yazılı; toplamı notun sayısıyla
  tutuyorsa (ya da not sayı vermiyorsa) yazılıyor — tek tüpte hepsi, tüp
  sayısı öğe sayısına eşitse her öğe kendi tüpünde. "BİR TÜPTE" = 1 tüp;
  "TOPLAM 3 OOSİT" de ADET gibi sayı. "15 ADET OOSİT 5'ERLİ ŞEKİLDE 3 TÜPTE":
  eşit bölünmüş tüpler. Önceden "kaç örnek/tüp okunamadı" deyip hiç
  yazılmıyordu.

## Embriyo notlarında

- **Morfoloji nitelemesi ayrı embriyo değil**: "(3AA(OVAL))", "(4AB-ELİPTİK)",
  "(2BB(COLLAPSED))", "(3AB)(COLLAPSED)", "(4AA(HATCHİNG)-3BB)". 12 kayıtta
  ölçüldü: notun ADET'i ve DONDURULAN hep nitelemesiz sayıyla tutuyor. Araç
  nitelemeyi tanınmayan öğe sayıp o tüpe eksik yazıyordu; iç parantezde skoru
  da ("3AA") atıyordu. Şimdi niteleme önündeki skorun yazımına ekleniyor
  ("3AA (OVAL)") ve değerlendirmenin notuna gidiyor (`_NITELIK`). Tek başına
  bir tüpü dolduruyorsa ("(COLLAPSED BLAST)") skorsuz embriyo.
- **Virgül de ayırıcı**: "(8HG1,9HG2)", "(1CC,1CC)", "(4BB, 3AB)",
  "(KAVİTASYON G3, KAVİTASYON G3, KAVİTASYON G3)". Tek öğe okunuyor, tüpe
  eksik yazılıyordu (uyarıyla).
- **"8HG1* 8HG2"**: yıldızlı skorun arkası okunmuyordu.
- **"BİRŞELMEG2"** = birleşme G2 (harfler yer değiştirmiş).
- **Kapanmamış son grup**: "1 TÜPTE (8HG1-6HG2-10HG3 OLACAK ŞEKİLDE" — ")"
  hiç yok. v6.165 ")"si olan yazımları okuyordu; "("den sonra tire/virgülle
  bağlı öğeler bütünüyle tanınıyorsa tüp.
- **Dondurma birden çok cümlede**: "TOPLAM 3 ADET EMBRİYO DONDURULDU. 1 ADET
  5. GÜN EMBRİYOSU 1 TÜPTE (3BC) ... SAKLANDI. 2 ADET 6. GÜN EMBRİYOSU 1 TÜPTE
  (3AB-3BB) ... SAKLANDI." v6.168 ilk parantezli cümleyi alıyordu; tüpler
  kaynağın sayısına ulaşmıyorsa sonraki dondurma cümleleri de okunuyor
  (parantezli; stok ya da transfer anlatmayan), günü kendi cümlesinden
  (5 ve 6). Grup toplama işlevi bunun için `_gruplari_topla()` oldu.

## Düzeltme dosyası

`tarih_duzeltme_2019_2023.txt` (depoda değil, hasta verisi): 30 tarih (ay
rakamı yanlış; komşu kayıtlarla ve aynı hastanın öteki tedavileriyle
gerekçelendirildi — FET'i OPU'sundan önce görünen üç kayıt dahil), iki kesik
dosya numarası (aynı doğum tarihi ve eş adıyla başka dosyada tam numarası
var), bir ikiz kayıt (`ATLA`). Kasım 2020'nin bir FET'inin tarihi tahmin
(dosyada bunu söylüyor). Dosya numarası "99" olan hasta aralık 2024'te de
"99" ile aktarılmıştı: kullanıcı programda numarayı 2019 aktarımından ÖNCE
düzeltmeli, yoksa iki kart olur — `KOMUTLAR.md`'de.

Kaynakta ICSI/2PN sayısı hiç olmayan ama transfer ya da dondurma yazan
satırlar var; araç döllenmeyi uydurmuyor (v6.148), uyarı basıyor. Kullanıcı
sayıyı biliyorsa düzeltme dosyasına `ICSI 0 <sayı>` satırı ekler.

## Dosyası aktarılmış seyrek ay "aktarılmamış" sayılmıyor

Ağustos 2019'un dosyasında 4, nisan 2020'ninkinde 1 kayıt var (pandemi).
v6.164'ün eşiği (ayda 10 tedavi) bu ayları aktarılmamış sayıyor, o aylardan
geçen her FET'i "ertelendi" bırakıyordu — sonsuza dek, çünkü gelecek dosya
yok. Ölçü artık veriden: aktarılmış her etiketin tedavilerinin en çok düştüğü
ay o dosyanın ayıdır (`_etiket_aylari()`), etiket adı okunmuyor (2026'nın
etiketlerinde yıl yok). Dosyası aktarılmış ay, kaç tedavisi olursa olsun
aktarılmış. **Mayıs 2020'nin dosyası hiç yok**; kullanıcının cevabı:
"Mayıs 2020'de hiç kayıt yoksa pandemi yüzünden yapılmamıştır." Ay
`_BOS_AYLAR`'da, aktarılmış sayılıyor. Test veritabanında o aydan geçen 116
FET `bagla` ile tüpüne bağlandı.

## `dosya_no_degistir.py`: yer tutucu dosya numarası

Aralık 2024'ün "99" numaralı hastasının gerçek numarası 2019'un
dosyalarında; kullanıcı ekrandan düzeltmeye kalktı, ekran izin vermedi —
hasta düzenleme dosya numarasını bilerek kilitliyor (arşiv klasörünün adı ve
`goruntu.dosya_yolu`'nun ilk parçası o numara; README v6.4). "Silip yeniden
aç" burada uygun değil: tedavi Access'ten aktarılmış, tüpleri tankta, sonraki
bir Yumurta Çözme onları çözmüş olabilir. Yeni araç numarayı her yerde
birlikte değiştiriyor: `hasta.dosya_no`, iki `dosya_yolu` kolonu, başka
hastaların `es_dosya_no`'su, sonra `arsiv/<eski>/` klasörü; hepsi
`degisiklik_log`'da. Yeni numara başka hastada kayıtlıysa duruyor — kart
birleştirme yok, bu yüzden 2019 aktarımından ÖNCE çalıştırılmalı.
Denendi: sahte fotoğraf yolu ve arşiv klasörüyle birlikte değişti, ikinci
çalıştırma "kayıtlı değil" dedi, çakışan numara reddedildi.

## `aktar_toplu.py`: 53 dosya tek komutla

Kullanıcı: "aktarma işini sen yap ya da tek komuta düşür, tek tek
uğraşmayayım." Aktarım kullanıcının makinesinde çalışmak zorunda (gerçek
veri orada); araç klasördeki `<ay><yıl>.csv` dosyalarını tarih sırasına
dizip her birini `aktar_access.py`'ye alt süreç olarak veriyor (`sys.
executable` -- bu bir geliştirme aracı, paketlenmiş programın parçası
değil), `dosya=99:<gerçek no>` adımını başa alıyor, çıktıyı `aktar_toplu.log`'a
yazıyor, hata verende duruyor. 2026 dosyaları atlanıyor: onlar yılsız
etiketle aktarıldı, `MAYIS2026` diye yeniden aktarılsa her tedavi ikinci
kez açılırdı. Denendi: iki dosyalık klasörde iki kez çalıştırıldı -- ilkinde
208 tedavi, ikincisinde 0 aktarıldı / 208 atlandı, dosya numarası adımı
ikincisinde "zaten yapılmış" dedi.

## Aktarım hızı: ay sayımı artımlı

Ay sorguları (`db.tedavi_tarihi()` her tedavi için alt sorgular) 3.000
tedavide 14 saniye sürüyor ve aktarım sırasında her FET satırı için yeniden
soruluyordu — satır başına bir tedavi eklendiğinden önbellek hep düşüyordu;
43 satırlık ocak 2021 dosyası 10 dakika sürdü. `_yeni_tedaviler()`: yalnızca
önbellekten sonra eklenen tedaviler sorulup sayıya ekleniyor; tedavi
silinmişse baştan. Aynı dosya bir dakikanın altına indi.

**Denendi:** 53 dosya test veritabanına (2023 ocak–haziran, 2024 eylül–aralık,
2025 ocak–mayıs, 2026 mayıs üstüne) tarih sırasıyla aktarıldı: 5.494 tedavi,
0 hata; bütün düzeltmeler uygulandı (kesik dosya numaraları 2019/2020'deki
kartlarla birleşti, ikiz atlandı). Uyarılar yalnızca kaynağın kendi
eksikleri: 13 satırda ICSI/2PN sayısı dondurulandan az, 4 satırda olgunluğu
yazılmamış yumurta. 23 dosya ikinci kez aktarıldı, `dondurma` ve `bagla`
kipleri çalıştırıldı: veritabanı farkı boş. GV tüpü formda "(4*GV)", iki
cümlelik dondurma "(3BC) (3AB-3BB)" 5./6. gün, "5'ERLİ" üç tüp "(5*MII)".
Hasta kartı, tedavi, vitrifikasyon, iki form, Excel çıktıları, Cryo Haritası,
istatistik ve ay listesi 200. Aktarımın son dosyası 3.000 tedavilik
veritabanında bir dakikanın altında.

# v6.171 — Yumurtanın olgunluğu dondurmadan sonra girilmiş olsa da okunuyor

Kullanıcı v6.169'dan sonra bildirdi: "Sadece bir tedavide sorun varmış"
(2026-0001). O tedavide form yumurta tüpüne hâlâ yalnızca sayı basıyordu.

v6.169 olgunluğu dondurmadan **önce** girilmiş son maturasyondan okuyordu
(kimlik sırası). Programın akışında Yumurta Dondurma'nın olgunluğu denüdasyon
ekranında işaretleniyor ve bu dondurmadan **sonra** da yapılabiliyor. O zaman
kural hiçbir şey bulamıyordu. Test veritabanında yeniden üretildi: bir
tedavinin maturasyon kayıtları dondurmadan sonra girilmiş gibi yazılınca form
"(3)" dedi, düzeltmeden sonra "(1*MII-2*MI)".

Kural artık `formlar._olgunluk_sql()`'de ve iki basamaklı:
1. **Dondurmanın yapıldığı tedavideki** maturasyon, giriş sırasına bakmadan
   (`db.olay_tedavisi()` = `db.vit_tedavisi()`).
2. O tedavide yoksa dondurmadan önceki son maturasyon (v6.169'un kuralı).
   Yumurta Çözme'de sonradan başka tedavide yapılan değerlendirme tüpün
   içeriği değil.

İki ayrı alt sorgu ve `COALESCE`, çünkü SQLite iç sorgunun `ORDER BY`'ında
dış sorgunun kolonuna izin vermiyor ("no such column"). Yeni bir alt sorguda
"önce şu, yoksa bu" sıralaması gerekirse bu deseni kullan.

**Denendi:** iki test veritabanının 2575 tedavisinde Özet NOTLAR'ı, FREEZE ve
THAW eski ve yeni kodla birebir aynı. Yeniden üretilen tedavinin formları,
Excel'i ve ekranları 200 döndü. Kullanıcı doğruladı (2026-09-24): 2026-0001'in
özet formunda olgunluk görünüyor.

# v6.185 — Embriyonun ekranlarında yumurta karesi yok

Kullanıcı bildirdi: "Program yumurta fotoğrafı eklenmiş ama embriyo fotoğrafı
eklenmemiş hastanın embriyo işlemlerinde yumurta fotoğrafını gösteriyor.
Göstermesin, embriyo fotoğrafsız kalsın."

Aşama ekranları (ICSI, fertilizasyon, cleavage, blastokist) zaten yalnızca
kendi aşamalarının karelerini gösteriyordu (v5.1, "fotoğraf devralma yok").
Sorun birden çok aşamanın örneğini gösteren dört sorgudaydı:
vitrifikasyon ekranı, taşıyıcı sayfası ve transfer ekranının iki listesi. Bu
sorgular önce ekranın aşamasının karesini arıyordu (blastokist ya da transfer
öncesi). Bulamazsa örneğin **herhangi bir** karesine düşüyordu: embriyonun
karesi yoksa denüdasyonda ya da ICSI'de çekilmiş yumurta karesine. Büyüteç ve
kare sayısı da bütün kareleri sayıyordu, embriyo karesi olan örnekte bile
yumurta karesi büyüteçte çıkıyordu.

Artık dördü de tek işlevden: **`app.ornek_kareleri_sql()`**.
- **Embriyoda yumurta ve zigot kareleri yok.** Denüdasyon, ICSI ve
  fertilizasyon kontrolü kareleri ne gösteriliyor, ne büyüteçte, ne
  sayıda. Karesi yoksa ekran "fotoğrafsız" basıyor.
- **Zigot (2PN) karesi de gizli** — kullanıcı yalnızca yumurtayı söyledi,
  ama 2PN karesi de dondurulan ya da transfer edilen embriyonun karesi değil.
  Kullanıcıya söylendi, isterse geri açılır.
- **Yumurtada her kare, eskisi gibi.** Dondurulan yumurtanın karesi onun
  denüdasyon karesi. Yumurta mı:
  - taşıyıcıda dondurma anına göre (`db.dondurulan_yumurta_sql()`);
  - vitrifikasyon ekranında bugünkü haline göre (`db.embriyo_izi_sql()`:
    ICSI, döllenme ya da cleavage/blastokist değerlendirmesi var mı);
  - transferde hep embriyo.
- Çözme ekranı değişmedi: orada zaten yalnızca "çözme sonrası" ve "ikinci
  kontrol" kareleri var.

**Denendi:** kullanıcının veritabanının deneme kopyasına dört örneğe kare
eklendi, sonra eski ve yeni kod aynı kopyada açıldı:

| Örnek ve ekran | Eski kod | Yeni kod |
|---|---|---|
| Yalnızca yumurta ve 2PN karesi olan dondurulmuş embriyo, vitrifikasyon ekranı ve tüp sayfası | 2PN karesi, büyüteçte yumurta karesi | fotoğrafsız |
| Yumurta ve gün 5 karesi olan embriyo | gün 5 karesi, büyüteçte yumurta karesi | gün 5 karesi, büyüteçte yalnızca o |
| Yumurta Dondurma'nın tüpü | yumurta karesi | yumurta karesi (değişmedi) |
| Yalnızca yumurta karesi olan transfer edilmiş embriyo | yumurta karesi | fotoğrafsız |

Altı ekranın hepsi 200 döndü.

# v6.186 — Seçili gün belirgin (cleavage, blastokist)

Kullanıcı bildirdi: "cleavage ekranında gün 2 ve gün 3 seçildiği ekranda
anlaşılmıyor. Hangi günü seçtiğimiz daha belirgin olsun."

**Sebep:** gün seçicinin (`.gunsec`) seçili düğmesi `--ust-bg` zeminindeydi.
Açık temada (v6.71'e kadar) bu, beyaz kartların arasında koyu bir sekmeydi.
Koyu temada `--ust-bg` (#111a25), seçili olmayan düğmenin zemini `--yuzey`
(#172230) ile neredeyse aynı renk; seçili düğmenin kenarlığı da yok. Ölçüldü:
iki düğmeyi yalnızca yazı rengi ayırıyordu (beyaz / gri-mavi). Seçili gün
seçili olmayandan sönük, boş bir yuva gibi görünüyordu.

**Düzeltme tek CSS kuralı:** seçili gün pembe zemin (`--vurgu`), beyaz ve
kalın yazı. Programın öteki seçicileri zaten böyle: aşama ekranlarındaki
seçenek düğmeleri (`.secenek .sec.secili`) ve androlojinin over seçicisi
(`.tarafsec a.aktif`). Aynı seçici blastokist ekranında da (gün 4–7)
kullanılıyor, o da düzeldi.
- **Seçili hal için `--ust-bg` kullanma** (v6.74'ün `--ink-2` dersinin
  kardeşi): koyu temada kasa rengi kart zemininden ayırt edilmiyor. Seçili
  düğme ya da sekme `--vurgu`. `:root`'taki açıklama da ("aktif sekme bunu
  kullanıyor") buna göre düzeltildi.
- Telefonda altta duran gezinme çubuğunun ortası ("Tedavi 6/10") hâlâ
  `--ust-bg`: bir seçim değil, iki okun arasındaki tedaviye dönüş bağlantısı.
  Dokunulmadı.

**Denendi:** uydurma bir hastayla (gerçek veri yok), telefon (390 px) ve
masaüstü (1280 px) genişliğinde cleavage (gün 2, gün 3) ve blastokist (gün 5)
ekranları açıldı. Seçili günün zemini rgb(224, 53, 111), seçili olmayanlar
değişmedi, yatay taşma yok.

Yalnızca `style.css` değişti. Bağlantı `?v=<değişim zamanı>` taşıdığı için
(v6.69) `git pull`'dan sonra sayfa yenilenince yeni görünüm geliyor, programı
yeniden başlatmak gerekmiyor. Yönetici panelinin sürüm kartı (v6.162) yeniden
başlatılana kadar "yeniden başlatılmadı" diyebilir; zararsız.

# v6.187 — ART Lab'ın Yorum satırında "Normal" yazmıyor

Kullanıcı sordu: "ART Lab formunda bazı durumlarda normal yazıyor. Neden?"

Yumurta ızgarasının en alttaki **Yorum** satırı (kâğıdın altındaki geniş
"Yorum:" satırı değil) embriyonun blastokist skorunu gösteriyor. Kâğıtta ayrı
bir blastokist satırı yok (v6.37). Skor yoksa kod, fertilizasyon ekranındaki
sonucu yazıyordu: Normal, Dejenere ya da Kayıp. Bu yedek formun ilk
sürümünden beri vardı ve hiçbir yerde yazılı değildi. Blastokiste gitmeyen
her embriyoda kutu "Normal" diyordu: gün 2–3'te transfer edilen ya da
dondurulan, arrest olan, değerlendirmesi girilmemiş olanlar.
- "Normal" kontrolün sonucu, embriyo hakkında bir yorum değil. Formu okuyan
  onu embriyonun değerlendirmesi sanabilir. Aynı sütunun "PM durumu" satırı
  zaten 2PN yazıyor.
- Kullanıcının deneme kopyasında son 400 IVF/ICSI tedavisinde 1.260 kutu
  (307 tedavi) "Normal" yazıyordu; 651 kutuda blastokist skoru vardı.

**Kullanıcının kararı:** kutu blastokist skorunu göstersin. Skor yoksa
yalnızca Dejenere ya da Kayıp yazsın; "Normal" hiç yazmasın. "Dejenere" o
yumurtada neden cleavage olmadığını açıklıyor.
- Süzgeç `fert_sonuc`'un **koduna** bakıyor (`normal`), etikete değil;
  etiketi laboratuvar düzenleyebiliyor (`liste_degeri`).
- Ekran ve Excel aynı veriden (`formlar.artlab_verisi()`), ikisi birlikte
  değişti. Embriyoloji Özet formunda bu satır yok.

**Denendi:** deneme kopyasının 1.816 tedavisinin hepsi hatasız basıldı.
Yorum kutularında artık hiç "Normal" yok; 2.089 blastokist skoru aynı, 2
kutu "Dejenere". Uydurma bir hastanın formunda (4AA, 2PN, Dejenere, Kayıp)
satır "4AA, boş, Dejenere, Kayıp" basıldı; form ve Excel çıktısı 200 döndü.

Yalnızca `formlar.py` değişti: `git pull`'dan sonra programın **yeniden
başlatılması** gerekiyor (tuzak #5).

# v6.188 — Cryo haritası Excel'inin üç okuma hatası ve onarımı

Kullanıcı Cryo Haritası'nın bugünkü halini sordu ("en önemli kayıt ...
kesinlikle bozulmaması gerekiyor") ve Excel'ini yeniden verdi ("Düzeni
araştır. Her goblete 4 straw/Cryotop konuyor. Ve goblette farklı renkler
konuyor"). Düzen çıkarılırken v6.173'ün okumasının üç hatası bulundu; üçü de
`cryo_esle.py uygula` ile kullanıcının veritabanına yazılmıştı (2026-09-25).

## Tankın düzeni (Excel'den)

| Tank | Kanister | Goblet | İçerik |
|---|---|---|---|
| TANK 1 | 6 | altta 1A–30A, üstte 1–30 ("Tank 1-5 üst") | embriyo, 4 straw |
| TANK 5 | 6 | altta 1–30; üstte yalnızca 1. kanister | embriyo, 4 straw |
| TANK 4 | 21–42 | A–P (14: her harf üst/alt, AÜ/AA) | embriyo, 4 straw |
| TANK 4 | 1–13, 15–18 | A–P / A1–P5 | sperm, tek vial |
| TANK 3 | 1 / 2–5 | A–D | sperm / embriyo |
| TANK 2 | 6 | 1–30 ve harfli yerler | karışık |
| YENİ SPERM | 15 | A1–P5 | sperm |

Kullanıcının cevapları: "Tank 1-5 üst" kanisterlerin üst katı; VİAL'deki
sondaki numara ("CRYOLOCK MAVİ 2") hastanın kaçıncı straw'ı (bir gobletin 1.
ve 3. sırasında aynı hastanın 2 ve 3 numaralı straw'ları duruyordu). Renkli
yazılmış gobletlerin %90'ında (736'nın 661'i) straw renkleri birbirinden
farklı. Excel'de 31 goblet 5, 3 goblet 6 satırla yazılı (4'ü aşıyor).

## Üç hata (`cryo_excel.py`)

1. **Blok içindeki kanister ayracı.** TANK 3'ün 2–5. kanisterleri tek
   sütunda alt alta, araya NO sütununa "CANİSTER 2" gibi satırlar konarak
   yazılmış. Ayraç tanınmıyordu, 49 embriyo satırı 1. kanister sayıldı:
   haritada "TANK 3 / 1 / B", tankta 3. kanister. Artık ayraç sonraki
   satırların kanisterini değiştiriyor (`_KANISTER_AYRAC`, "CANNİSTER" da).
   Bloğun **üstündeki** etiket eski kuralla kaldı: genişletmek, TANK 2'nin
   etiketsiz bir bloğundaki 9 satırı doğrulanmamış bir kanistere taşırdı.
2. **Üst kat.** "Tank 1-5 üst" sayfasının gobletleri alt kattakilerle aynı
   adı aldı. TANK 5'te 1–30 iki katta da var: "TANK 5 / 1 / 7" alttaki mi
   üstteki mi ayırt edilmiyordu (üstte 110 satır). Kullanıcının seçimiyle
   üst goblet "7 Üst" (`cryo_excel.UST_KAT`); TANK 1'in üst gobletleri de
   (alttakiler zaten "7A" idi, çakışma yoktu ama ad tutarlı olsun diye).
3. **Renk.** `_n()` "İ"yi "I" yapıyor, "Ş" kalıyor: "YEŞİL" "YEŞIL" oluyor,
   ne "YEŞİL" ne "YESIL" tutuyordu. 684 yeşil straw renksiz yazıldı. Üç
   satırda "YEŞİL CRYOTOP MEMORİAL"daki "MOR" mor sayılmıştı, şimdi yeşil.
   Pembe (12 satır) programın renk listesinde yoktu; `cryo_esle.py` artık
   tip kodları gibi listeye ekliyor (`RENK_ETIKETLERI`).

Eski ve yeni okuma satır satır karşılaştırıldı: 5.401 satırın hiçbiri
kaybolmadı; değişen yalnızca 773 üst kat gobletinin adı, TANK 3'ün 49
satırının kanisteri, 696 satırın rengi.

## Onarım: `cryo_esle.py onar`

Okumayı düzeltmek yazılmış konumu düzeltmiyor. Her Excel satırı artık eski
okumanın yerini de taşıyor (`eski_yer`); `onar` aynı eşleştirmeyi yapıp
**yalnızca tüpün bugünkü konumu o eski yerse** yeni yeri yazıyor. Başka bir
konumu olan tüpe (kullanıcı elle düzeltmiş ya da taşımış olabilir)
dokunulmuyor, raporda ayrı başlıkta. Renk yalnızca boşsa yazılıyor. Kilit
içinde tüpün konumu/rengi yeniden okunuyor (program açıkken biri bu arada
değiştirdiyse dokunulmuyor). Her değişiklik `degisiklik_log`'da (tablo
`tasiyici`, alan `konum`/`renk`). Rapor `cryo_esle_rapor_onar.txt` (hasta
adı içerir, `.gitignore`'da). Onay "ONAR".

**Denendi:** veritabanının bir kopyasına önce eski `uygula` (HEAD'in kodu)
uygulandı -- 969 tüpe konum, kullanıcının makinesinde olanın küçüğü. Sonra
`onar`: 541 tüpün konumu (TANK 1 üst 456, TANK 5 üst 78, TANK 3'ün 2/3/5.
kanisterleri 7), 230 tüpün rengi (yeşil). Tablo tablo karşılaştırma:
değişen yalnızca `tasiyici.konum_id` (541) ve `renk` (230); 186 yeni konum
satırı ("N Üst" ve yeni kanister yolları), 771 günlük satırı; başka hiçbir
tabloda tek satır değişmedi. Onarımdan önce 12 gobletin içinde 4'ten fazla
straw görünüyordu (alt ve üst kat birleşmişti), sonra 5 -- beşi de Excel'de
5 satırla yazılı. İkinci `onar`: "Onarılacak bir şey yok"; `liste`: 969
"zaten". `sperm`, `eksik`, `yeni_hasta` kipleri yeni okumayla çalışıyor.
Sperm satırları üç hatadan etkilenmedi.

Sıradaki işler (kullanıcının isteği): tank düzenini programa tanıtmak (her
goblet 4 straw), dondurma ekranında boş yer önerisi (hastanın straw'ları
farklı renkte, mümkünse birbirine yakın, gobletteki renklerle çakışmadan) ve
her değişiklikte kendiliğinden güncellenen Excel haritası (bugünkü düzen +
düz liste).

# v6.189 — Tank düzeni: bütün gobletler ve Excel kaydı

Kullanıcının isteği (2026-09-25): "Laboratuvarda cryo harita en önemli kayıt
... Bu haritanın kesinlikle bozulmaması gerekiyor. Benim programı yaparken
istediğim bir hastanın embriyolarını dondururken program bana tanklarda boş
yerleri önermesiydi ... zaten kayıtlı olan embriyo bilgileri de cryo haritaya
kendiliğinden geçsin ... cryo harita excel olarak hep arkada yapılan her
değişiklikte dinamik olarak işlensin ve saklansın." Üç iş; bu sürüm ilki,
ötekilerin temeli: program tankların **düzenini** bilmiyordu. `konum`
yalnızca bir tüpe yazılmış yerdi, boş goblet programda hiç yoktu; boş yer
önermek için hangi gobletlerin var olduğunu, kaçar straw aldığını ve
hangisinde ne durduğunu bilmek gerek.

## Düzen Excel'den bir kez, sonra program türetiyor

- `cryo_excel.duzen()`: Excel'in bütün gobletleri, **boş satırlarıyla**.
  `coz()` ile aynı satır yürüyüşünü paylaşıyor (`_veri_satirlari()`; yeniden
  yazılan `coz()`'un çıktısı eskisiyle birebir aynı, 5.401 satır). Goblet =
  aynı tank + kanister içinde aynı ad; Excel'de bir gobletin satırları bazen
  iki yerde yazılmış ("G" önce 3, en altta 1 satır) -- ad aynıysa birleşiyor,
  büyük/küçük harf farkı yok ("p" = "P"). NO sütunundaki not satırları
  ("***** kuyuda 17 tane cane var ...", "KÜÇÜK TANK") goblet değil.
- **Kapasite**: kullanıcı "Her goblete 4 straw/Cryotop konuyor". Excel'de
  düzenli goblet 4 satır (973 goblet; 31'i 5, 3'ü 6 satır -- sığdırılmış
  fazladan straw). En az 3 satırlı embriyo gobleti 4 yuvalı sayılıyor (1.014
  goblet); TANK 2'nin 2–4. kanisterlerindeki 2014–2017 tek satırlık yerler
  ("cane") ve tek satırlık birkaç harfli yer (TANK 4'ün 21 ve 23.
  kanisterlerinde) kapasitesi **bilinmeyen** yer: haritada görünüyor, hiç
  önerilmeyecek. Sperm yerlerinin kapasitesi yok (öneri embriyo için).
- `goc_052`: `konum.kapasite`, `konum.kategori`, `konum.sira` (kanister
  içinde Excel'deki sıra; üst kat 1000'den) ve `excel_kaydi` tablosu.
- Doluluk **türetiliyor** (`yerlesim.doluluk()`), sayaç yok: goblet = içinde
  duran dolu tüpler + Excel kayıtları. Yer adları serbest metin olduğu için
  (dondurma ekranında elle yazılıyordu) tüpün gobleti `konum_id` ile değil
  **`yerlesim.yer_anahtari()`** ile soruluyor: "T1 / K3 / 12a" ile
  "TANK 1 / 3 / 12A" aynı goblet. Anahtar yalnızca karşılaştırma için;
  ekrana ve veritabanına Excel'deki yazım yazılıyor. Excel'in 2.920
  gobletinde iki farklı goblet aynı anahtara düşmüyor (ölçüldü).

## Excel kaydı

Kullanıcının seçimi: Excel'de bir gobletde duran ama programda karşılığı olan
tüp bulunamayan satır "gobletinde 'Excel kaydı' olarak dursun" -- Excel'deki
ad, tarih, hücre ve VİAL yazısıyla, yuvası dolu sayılsın. Sahte tüp
açılmıyor (v6.127'nin gerekçesi). Sebebi kayıtta (hasta yok, o gün tüp yok,
içerik tutmuyor, tüp programda çözülmüş görünüyor, tüp başka konumda, yalnızca
adı yazılı satır ...). Çözülmüş görünen ya da başka konumdaki tüpün satırı
da Excel kaydı: hangisi doğru bilinmeden yuva boş sayılırsa oraya yeni bir
straw önerilebilirdi.

Excel kaydının sayfasında (`/cryo/excel-kaydi/{id}`) iki iş, ikisi de geri
alınabilir, kayıt silinmez:
- **Tüpe bağla**: aynı gün dondurulmuş tüpler aday olarak listeleniyor
  (konumu olmayanlar önce -- Excel'le eşleşemeyen tüp çoğu zaman o), ya da
  etiket yazılıyor. Tüp Excel kaydının gobletini alıyor, rengi/tipi boşsa
  Excel'inki yazılıyor; straw artık tüpün kendisiyle sayılıyor, iki kez
  değil. "Bağı çöz" tüpü bağlamadan önceki konumuna döndürüyor, bağlarken
  doldurulan rengi/tipi siliyor.
- **Tanktan çıkarıldı**: tarih + not; yuva boşalıyor. "Tanka geri koy".
Hepsi `degisiklik_log`'da. Tüp kalıcı silinirse bağlı Excel kaydı yeniden
"tankta" oluyor (tüpün kaydı silindi diye straw haritadan düşmesin;
`excel_kaydi_bagini_birak()`, `teshis_silme.py` de biliyor).

## `cryo_esle.py yerlesim`

Gobletleri açar/düzene alır ve Excel kayıtlarını yazar ("YERLESIM" onayı).
**Önce öteki kipler**: bekleyen `uygula` / `onar` / `yeni_hasta` / `sperm`
yazısı varsa hiçbir şey yazmadan hangisinin çalıştırılacağını söylüyor --
yoksa aynı straw hem Excel kaydı olur hem de sonradan tüpüne konum yazılır,
goblet iki kez dolu görünürdü. Bir satır "programda temsil ediliyor" =
eşleştiği tüp dolu ve o gobletde (anahtarla). Excel kaydının kimliği içerik
anahtarı (yer + ad + tarih + hücre + VİAL, aynı içerikteki sırası; sayfa/
satır numarası değil): ikinci çalıştırma hiçbir şey yazmıyor; Excel'e satır
eklenmişse yenisi ekleniyor; Excel'den silinmiş satırın Excel kaydı
kendiliğinden kaldırılmıyor, raporda listeleniyor (straw'ın çıktığını
söyleyecek olan kullanıcı). Rapor `cryo_esle_rapor_yerlesim.txt`.

**Denendi** (veritabanının kopyası; yalnızca bazı ayların aktarıldığı eski
bir kopya, o yüzden "hasta yok" çok): önce kip `yeni_hasta` ve `sperm`'i
istedi; ikisi çalışınca 941 goblet açıldı, 1.963 goblet düzene alındı, 2.799
Excel kaydı yazıldı. Tablo tablo karşılaştırma: `tasiyici`, `olay`,
`specimen`, `sperm_dondurma`, `hasta`, `cycle` tek satır değişmedi; eski
`konum` satırlarının hiçbiri değişmedi (945 yeni satır, kapasite/kategori/
sıra kolonları). **Her gobletin programdaki doluluğu Excel'deki dolu satır
sayısına eşit** (2.904 gobletin 2.898'i birebir; kalan 6'sı 2011–2017'nin
tek satırında "2 straw" yazan yerler, programda iki tüp -- straw sayısı
doğru). İkinci çalıştırma: "Yazılacak bir şey yok". Bağla / bağı çöz /
tanktan çıkar / geri koy denendi: doluluk her adımda tutarlı.

## Cryo Haritası

Düzen kurulunca Embriyo ve Sperm Dondurma sütunları düz liste değil **tank →
kanister ağacı** (sayılar her düzeyde: tüp, Excel kaydı, boş yuva); kanister
sayfası (`/cryo/yer`) gobletleri Excel'deki sırasıyla, alt kat / üst kat,
her yuvası renginin noktasıyla. Kapasitesi bilinmeyen yerde "boş yuva"
yazılmıyor. Konumu girilmemiş ya da düzende olmayan bir yere yazılmış tüpler
`/cryo/yersiz`'de (gizlenecek şey değil: tankta, yeri programda yok).
Arama Excel kayıtlarını da buluyor. Sayfa 517 KB'tan 29 KB'a indi (1.531
sperm tüpü tek sayfada basılıyordu). Düzen kurulmamışsa ekran eskisi gibi.

## Kullanıcıya sorulacak (Excel'in belirsiz iki yeri)

- "TANK 1+2+3" sayfasının altında ikinci bir "TANK 3" tablosu (6 kanister):
  yalnızca 1. kanisterinde 2015'ten 4 embriyo satırı (A4–A7) dolu. Sağ
  üstteki "KÜÇÜK TANK / TANK 3" tablosuyla aynı tank mı, o embriyolar hâlâ
  orada mı? Bugün ikisi TANK 3'te birleşiyor (v6.173'ten beri böyle).
- En altta "TANK 2 / CANNİSTER 2" başlıklı küçük bir sperm tablosu (9
  satır, 2015–2017); 5'i TANK 2'nin 6. kanisterindeki satırların birebir
  aynısı. Kopya mı? `sperm` kipi bugün ikisini ayrı tüp açıyor; kopyaysa
  aynı vial iki kez sayılır.

Sıradaki: dondurma ekranında boş yer önerisi (v6.190), kendiliğinden
güncellenen Excel haritası.

# v6.190 — Dondurma ekranında boş yer önerisi

Kullanıcının isteği: "hastanın embriyolarını dondururken program bana
tanklarda boş yerleri önermesiydi. Yani ben kendim aramayım program bana
uygun yeri bulsun." Kuralı (2026-09-25): "Bir hastanın birden fazla strawu
varsa renkleri farklı olsun. Mümkünse birbirine yakın olsun. Kondukları
goblette aynı renklerin olmadığına dikkat edilsin." v6.189'un tank düzenini
kullanıyor; düzen kurulmamışsa ekran eskisi gibi.

## Öneri (`yerlesim.oneriler()`)

Vitrifikasyon ekranının Konum kartında en çok 6 aday; ilki konum kutularına
ve renk seçimine yazılı, başkasına dokunmak kutuları değiştiriyor. Sıra:

1. Hastanın **bugün** dondurulmuş straw'ının gobleti (boş yuvası varsa).
2. Hastanın başka straw'larının gobleti.
3. Aynı kanisterde onlara en yakın goblet (Excel'deki sıra).
4. Geri kalanlar, **bugün kaç straw** dondurulacağına göre (1 / 2 / 3 / 4+,
   ekranda seçiliyor; hasta bugün straw dondurduysa seçici görünmüyor):
   o kadar boş yuvası olan gobletlerin en az boş olanı -- boş gobletler çok
   straw'lı hastaya kalsın -- eşitse düzen sırası.

Excel'deki alışkanlık da bu: aynı günün straw'ları çoğunlukla aynı gobletde
(2 straw'da 452'ye 36), dolunca yanındaki gobletde devam ediyor.

**Renk**: gobletteki straw'ların renkleri dışında kalan ilk palet rengi;
hastanın bugünkü straw'larının renkleri sona. **Palet veriden**
(`renk_paleti()`): son bir yılın tüplerinde payı %5'ten çok olan renkler,
renk listesinin sırasıyla (yönetici sıralıyor). Listenin tamamı
kullanılsaydı üç straw'lı bir gobletin boş rengi "beyaz" önerilirdi;
laboratuvar 2022'den beri dört renk kullanıyor (mavi, sarı, turuncu,
yeşil). Bütün palet renkleri dolu olan goblet önerilmiyor (aynı renk ikinci
kez girerdi). Rengi yazılmamış straw'ı olan gobletde bu ekranda turuncuyla
yazıyor ("2 straw'ın rengi yazılmamış" -- önerilen renk onunla çakışabilir)
ve eşitlikte o goblet sona. Kapasitesi bilinmeyen yer hiç önerilmiyor.

## Denetim (engel değil, onay)

Seçilen yer yazılınca ekran soruyor (`/cycle/{id}/vitrifikasyon/yer-kontrol`,
izni vitrifikasyonun): goblet dolu mu, bu renkte straw zaten var mı, yazılan
goblet tank düzeninde var mı (yazım hatası ya da yeni bir yer), kapasitesi
biliniyor mu. Sorun varsa uyarı ve "Biliyorum, yine de bu yere kaydet" kutusu
çıkıyor; kutu işaretlenmeden form gönderilmiyor. Sunucu kaydederken aynı
denetimi yeniden yapıyor (eski bir sekme, bu arada aynı gobleti dolduran
başka bir telefon) ve onaysız kaydı reddediyor. v6.55'in "uyarı engellemez,
karar kullanıcının" kuralı: yeni bir tank/goblet de gerçek olabilir.

Yazılan yer düzendeki bir gobletse tüp **o gobletin konum satırına**
yazılıyor: "t1 / k1 / 24 üst" yazılsa da haritada tek goblet kalıyor.

**Denendi** (veritabanı kopyası): ilk straw önerilen goblete ve renge
kaydedildi; aynı hastanın ikinci straw'ında ilk öneri "bu hastanın
straw'larına yakın" (önceki goblet dolmuştu) ve seçici gizli; dolu goblet
onaysız doğrudan POST edilince sunucu reddetti, tüp açılmadı; küçük harfli,
kısaltılmış yazım (onaylı) düzendeki gobletin kendi konum satırına düştü.
Ekran 390 ve 1280 px'te yatay taşmıyor.

# v6.191 — Kendiliğinden güncellenen Excel haritası

Kullanıcının isteği (v6.189'un başındaki sözü): "ben istediğim zaman bu
excel cryo haritayı kopyalıyabileyim istiyordum." Seçimi (2026-09-25):
"Bugünkü düzen + düz liste" -- her tank ayrı sayfa, kanisterler yan yana,
her goblet 4 satır, boş yerler de görünür; ek olarak süzülebilir tek bir
liste sayfası. Dosya programın veri klasöründe durur, her günün son hali 30
gün saklanır. Böylece v6.189–v6.191 isteğin üç parçasını kapatıyor: harita
programda (düzen + Excel kaydı), dondururken boş yer önerisi, her
değişiklikte kendiliğinden yazılan Excel.

## Dosya

`<veri klasörü>/cryo_harita/Cryo_Haritasi.xlsx` (bugünkü iki kurulumda veri
klasörü program klasörünün kendisi, `lab.db`'nin yanı) ve günün kopyası
`Cryo_Haritasi_YYYY-AA-GG.xlsx`; 30 günden eski günlük kopyalar siliniyor,
klasördeki başka dosyaya dokunulmuyor. Sayfalar:

- **Bilgi**: üretildiği an, sayılar ve dört not -- dosyayı program yazar,
  elle değişiklik programa girmez ve bir sonraki yazımda silinir; Excel
  kaydının ne olduğu; açmadan önce kopyalayın (aşağıya bak).
- **Tank sayfaları** (TANK 1 … YENİ SPERM): laboratuvarın Excel'indeki gibi
  kanister blokları yan yana (bir bantta 6), her goblet kapasitesi kadar
  satır, boş yuva boş satır; gobletler kalın çizgiyle ayrılıyor. Üst kat
  ayrı bölüm ("KANİSTER 1 · ÜST KAT"). Kanisterinde olup düzende olmayan bir
  goblete yazılmış tüp bloğun sonunda "GOBLETİ BELİRSİZ" (goblet ekranının
  kartı). Blok sütunları: NO, HASTA, EŞİ, DOSYA NO, TARİH, HÜCRE ("D5
  (3AA-4AB)", "Yumurta (5*MII)", "Sperm · TESE" -- tüp yazımı
  `formlar.tup_metni()`), VİAL (tip + renk), ETİKET (programdaki etiket; Excel
  kaydında "EXCEL KAYDI" ve Excel'deki yazısı olduğu gibi).
  - **Soyad ve ad tek sütun (HASTA)**: program adı tek alanda tutuyor
    (`hasta.ad_soyad`); soyadın nerede başladığını tahmin etmek iki soyadlı
    hastada yanlış yazardı. Excel kaydında ad + soyad, programın sırası.
  - **DOSYA NO eklendi**: Excel'de yoktu, tek güvenilir anahtar (v6.125).
- **Liste**: her dolu tüp ve tankta duran her Excel kaydı bir satır (tank,
  kanister, goblet, tür, hasta, eşi, dosya no, dondurma günü, içerik,
  taşıyıcı, renk, etiket, kaynak: Program / Excel kaydı, yer). Yeri
  bilinmeyenler de var: "Konum girilmemiş", "Düzende yok". Tarih burada ISO
  (Excel tarih olarak alıyor), tank sayfalarında gün.ay.yıl metin -- tablo
  sayfası ile yerleşim sayfası ayrımı (v6.94).
- **Boş yerler**: boş yuvası olan her goblet, boş sayısı ve gobletteki
  renklerle.

Tank düzeni kurulmamışsa (`cryo_esle.py yerlesim` çalışmamış) tank
sayfaları tüplerin yazılı konumlarından kuruluyor: yalnızca dolu gobletler,
boş yuva bilinmiyor, "Boş yerler" sayfası yok; Bilgi sayfası söylüyor.

## Ne zaman yazılıyor (`harita_excel.py`)

Program açılınca (göçlerden sonra) arka planda bir iş parçacığı başlıyor;
dakikada bir veritabanının damgasına bakıyor (`veri_damgasi()`, açık
ekranları tazeleyen damganın aynısı -- ekleme, silme, iptal ve günlüğe
yazılan her düzenleme). Damga değiştiyse haritanın **içeriği** kuruluyor
(deneme veritabanında ~1,2 sn: 3.142 tüp, 2.799 Excel kaydı) ve içeriğin
imzası son yazılanla karşılaştırılıyor; dosya yalnızca harita gerçekten
değiştiyse yazılıyor. Bir ICSI kaydı dosyayı yeniden yazdırmıyor; bir
dondurma ya da Excel kaydı işlemi yazdırıyor (denendi). Çözme ve başka
merkeze taşıma da tüpün durumunu değiştirdiği için aynı yoldan.

- **Türetilmiş**: harita her seferinde tank düzeni, dolu tüpler ve Excel
  kayıtlarından baştan kuruluyor, ayrıca saklanan bir harita yok.
- **Atomik yazım**: yanındaki geçici dosyaya, sonra `os.replace`.
- **Windows'ta Excel'de açık duran dosya değiştirilemez.** Yazılamazsa
  Cryo Haritası'nın kartı "başka bir programda açık olabilir" diyor, program
  bir sonraki turda yeniden deniyor. Bu yüzden dosyayı açmadan önce
  kopyalamak ya da Cryo Haritası'ndaki "Excel haritasını indir"i kullanmak
  gerekiyor -- indirilen oradakiyle aynı içerik, indirirken yeniden kuruluyor.
- **Hiçbir hata programı durdurmuyor**: günlüğe (`program.log`) bir kez ve
  karta yazılıyor.
- İmza bellekte: program yeniden açılınca ilk tur dosyayı bir kez daha
  yazıyor (içerik aynı, zaman yeni).

## Ekran ve yedek

Cryo Haritası'nın sol sütununda "Excel haritası" kartı: son güncelleme
zamanı, yazılamadıysa sebebi, yöneticiye klasörün yolu; altında "Excel
haritasını indir" (`/disari/cryo/harita`, izni Cryo Haritası'nınki,
`/disari/cryo` gibi).

Yedekleme (`yedek.py` ve `/yedekleme`'deki "Şimdi yedekle") haritanın son
halini yedek diskine de kopyalıyor (`<yedek klasörü>/cryo_harita/`):
bilgisayar bozulursa harita programsız da okunabilsin. Kopyalanamazsa
yedekleme durmuyor -- asıl yedek veritabanı, harita ondan yeniden üretilir.

`cryo_harita/` ve `Cryo_Haritasi*.xlsx` `.gitignore`'da: hasta adları var ve
bugünkü kurulumlarda klasör depo klasörünün içinde açılıyor.

Goblet ekranının tüp ayrıntısı (`_tup_ayrintilari()`) `yerlesim.py`'ye
taşındı (`tup_ayrintilari()`, eşin adı ve sperm dondurma sebebi eklendi):
ekran ile dosya aynı satırı basıyor.

**Denendi** (veritabanı kopyası): açılıştan 5 sn sonra dosya ve günün
kopyası yazıldı; cryo dışı bir değişiklik (günlüğe satır) dosyayı yeniden
yazdırmadı; bir Excel kaydını "tanktan çıkarıldı" yapmak yazdırdı (liste
5.941 → 5.940), geri almak yine yazdırdı; önerilen goblete kaydedilen bir
dondurma 8 sn içinde listede o gobletle çıktı; ana dosya yazılamayınca hata
karta düştü, düzelince yazıldı; 30 günden eski iki günlük kopya silindi,
başka dosyalar kaldı; tank düzeni kurulmamış eski bir kopyada da dosya
üretildi. Dosya openpyxl ile açılıyor (9 sayfa); tank sayfası adları
maskelenmiş bir kopyada görüntüye çevrilip kontrol edildi. Kart 390 ve
1440 px'te taşmıyor.

**Bilinen**: TANK 5'in 2.–6. kanisterlerinin üst katında Excel'de goblet
numarası yok (bloklar boş); program oraları bilmiyor, önermiyor ve haritada
göstermiyor.

# v6.192 — Excel'in üç sorusu cevaplandı: TANK 3, kopya tablo, TANK 5'in yedek üst katı

v6.189'da sorulan üç şeyin cevabı (kullanıcı, 2026-09-26): "1-evet aynı
2-Kopya 3-Tank 5'in 2-6 üst katları yer biterse diye hazırlandı ihtiyaç
olursa oralara da hasta konulacak."

## 1. İkinci "TANK 3" tablosu = KÜÇÜK TANK / TANK 3

"TANK 1+2+3" sayfasının altındaki ikinci TANK 3 tablosu sağ üstteki
"KÜÇÜK TANK / TANK 3" ile aynı tank. Program ikisini v6.173'ten beri zaten
TANK 3'te birleştiriyordu: **değişiklik yok.** O tablonun boş 2.–6.
kanisterlerinden (51/67 satırlık boş kalıp tablolar) goblet açılmıyor --
yer değil, boş tablo.

## 2. "TANK 2 / CANNİSTER 2" tablosu kopya: okunmuyor

Sayfanın en altındaki küçük sperm tablosu TANK 2'nin 6. kanisterinin eski
bir kopyası. `cryo_excel.KOPYA_TABLOLAR` onu başlığının üstündeki
etiketlerle tanıyor ("TANK 2", "CANNİSTER 2"); `coz()` ve `duzen()` ikisi
de atlıyor, `coz()`'un uyarısı ve `yerlesim` raporu söylüyor ("kopya, 9
satırı okunmadı").

- **Eski/yeni okuma satır satır**: 5.401 satırdan yalnızca kopya tablonun
  9'u çıktı, kalan 5.392 satırın hiçbiri değişmedi; düzende kanistersiz 10
  "TANK 2" yeri çıktı, öteki 2.910 goblet aynı.
- 9 satırın hepsi 6. kanisterde aynı hasta ve aynı tarihle duruyor (5'i
  birebir). Sperm satırlarını `uygula` hiç yazmıyor; iki "embriyo" satırı
  tarihsiz, hiçbir tüpe bağlanamazdı. Yani **kullanıcının veritabanına
  kopya tablodan bir şey yazılmadı, onarım gerekmiyor.** `sperm` kipi
  (kullanıcı henüz çalıştırmadı) artık 1.531 değil 1.524 tüp açıyor --
  kopyanın 7 vial'i iki kez açılmıyor; erkek hasta sayısı aynı (609).

## 3. TANK 5'in 2.–6. kanisterlerinin üst katı: yedek goblet

Excel'de bu beş katın tablosu var (120'şer satır) ama NO sütunu boş, içleri
bomboş: program o yerleri hiç bilmiyordu. Artık:

- **`cryo_excel._hazir_kat_gobletleri()`**: üst kat sayfasında bütünüyle
  boş (NO, ad, tarih, hücre, VİAL yok), satır sayısı 4'ün katı olan tablo
  hazırlanmış kattır; gobletleri Excel'in kendi düzeniyle adlandırılıyor --
  her goblet 4 satır, sırayla "1 Üst" … "30 Üst" (TANK 5'in 1. kanisterinin
  üst katı da böyle). 5 × 30 = 150 goblet, 600 yuva, embriyo.
- **`goc_053`: `konum.yedek`** (1 = yedek). `yerlesim` kipi bu gobletleri
  yedek işaretleyerek açıyor; raporu ve ekran çıktısı söylüyor. Göç yoksa
  kip durup programı bir kez açmayı istiyor.
- **Öneri** (`yerlesim.oneriler()`): yedek goblet, hastanın kendi gobleti
  değilse "yakınlık" üstünlüğü almıyor ve bugünkü straw'ları alabilen
  bütün olağan gobletlerden SONRA geliyor -- ama alamayanlardan ÖNCE.
  Sıra: sığan olağan < sığan yedek < sığmayan olağan < sığmayan yedek.
  Yani yedek yalnızca olağan yerler hastanın straw'larını alamadığında
  öneriliyor; o durumda bir hastanın straw'ları gobletlere dağılmasın diye
  yedek goblet olağan bir yerin tek boş yuvasından önce. Öneri satırında
  "Yedek kat (olağan yerler yetmiyor)" yazıyor. Yedek goblete elle yazılan
  straw uyarısız kaydediliyor (yer düzende).
- **Haritada**: ağaçta kanister "üst katı yedek", kanister sayfasında
  "Üst kat · yedek (yer biterse diye hazırlandı)"; Excel haritasında blok
  "KANİSTER 2 · ÜST KAT (YEDEK)", "Boş yerler" sayfasında "Yedek" sütunu,
  Bilgi sayfasında açıklaması.

**Denendi** (kullanıcının durumundaki kopya: `onar` çalışmış, göç 052 ve
`sperm` yok): program açılışı göç 052 ve 053'ü uyguladı; `sperm` 1.524 tüp;
`yeni_hasta` (bu kopyada çalışmamıştı); `yerlesim` 3.044 goblet yazdı
(1.088 yeni, 1.956 düzene), 150'si yedek (TANK 5 / 2–6, sıra 1001–1030, 4
yuva), 2.797 Excel kaydı (önceden 2.799: kopyanın tarihsiz iki satırı);
ikinci çalıştırma "Yazılacak bir şey yok". Gobletlerin programdaki doluluğu
Excel'deki dolu satır sayısına 3.044'ün 3.038'inde eşit (kalan 6'sı
v6.189'daki "2 straw" satırları), yedek gobletler boş. Öneri: bugünkü
veride yedek hiç önerilmedi (10 olağan boş goblet var); olağan yerlerin
hepsi dolu varsayılınca ilk öneriler yedek; olağanda yalnızca tekli boşluk
kalınca 1 straw'a olağan, 4 straw'a yedek goblet. Ekranlar 200; kanister
sayfasının yedek bölümü 390 ve 1440 px'te taşmıyor.

# v6.193 — "Dolap" değil "tank"

Kullanıcı sordu: "Dolap kelimesi laboratuvarda kullanılmıyor. Dolap demek
ile neyi kastediyorsun. Dolap tank mı demek?" Evet: v6.36'da Cryo
Haritası'nın Excel dökümü yazılırken tankların tamamı için "dolap" denmişti
-- programın kendi sözü, laboratuvarın değil (aynı düğmenin İngilizcesi
zaten "tank" diyordu). Ekranda iki yerde geçiyordu, ikisi de o dökümde:

- `/cryo`'daki düğme "Dolabı Excel'e aktar" → **"Tankları Excel'e aktar"**
  (`metinler.excel_cryo`).
- Dosyanın ilk sütunu "Dolapta" → **"Tankta"** (`disari.CRYO_BASLIK`);
  değerler aynı: Evet (tankta), Hayır (çözülmüş), Taşındı (başka merkeze,
  v6.182).

Kodun açıklamalarındaki "dolap" da "tank" oldu (`app.py`, `disari.py`,
`cryo.html`), yeni bir metne yeniden sızmasın diye; CLAUDE.md'ye kural
eklendi. Eski göç (`goc_034`) ve README'nin eski bölümleri olduğu gibi
kaldı: biri çalışmış bir göç, öteki o günün kaydı. Bu döküm, v6.191'in
Excel haritasından ayrı: dondurulan her embriyo/yumurta bir satır ve
çözülenler de listede; harita ise bugünkü tankın goblet goblet hali.

# v6.194 — `cryo_esle.py` boşluklu dosya adını da tanıyor

Kullanıcı `python3 cryo_esle.py yerlesim CRYO HARİTA.xlsx` yazdı, araç
"CRYO bulunamadı" dedi: terminal boşluklu adı iki söze böldü. Tam yolla
çalıştırınca `yerlesim` önce `uygula`'yı istedi (2 tüp) ve önerdiği komutu
tırnaksız yazdı -- proje klasörünün adı da boşluklu ("Patient Data
Center"), o satır kopyalanınca yine bölünürdü. İki düzeltme:

- **Önerilen komutta dosya adı tırnak içinde** (`_komut_yolu()`): boşluk
  varsa çift tırnak, Mac'te de Windows'ta da geçiyor.
- **Bölünmüş ad birleştiriliyor**: ilk söz bir dosya değilse ve sözler
  birleşince bir dosya çıkıyorsa o kullanılıyor (kiplerin hepsi tek dosya
  alıyor). Yine bulunamazsa hata tırnaklı komutu gösteriyor.

KOMUTLAR.md'nin "Sık sorunlar"ına eklendi. Denendi: tırnaksız `CRYO
HARİTA.xlsx` dosyayı buldu; olmayan adda tırnaklı öneri çıktı.

# v6.195 — Telefonda açılır menü, düğme ızgaraları ve uygulama kurulumu

Kullanıcının isteği (2026-09-26): "Android ve iOS için programı daha güzel
kurulabilir ve kullanılabilir hale getir. Yani app gibi ikisine de
yükleyebileyim. Ve bazı menüler yukarıdan aşağıya sıralanıyor. Aşağıda
kaldığı için kaydırma yapmazsak görünmüyor ... Mesela açılır menü tarzı."
Ölçüldü (390px telefon): ana ekranın menü düğmeleri 1.419px'lik sayfanın en
dibindeydi, tedavi ekranının on bir aşama düğmesi 2.848px'lik sayfanın sağ
sütununda -- telefonda iki sütun alt alta dizildiği için bütün kartların
altında. Yönetici paneli dokuz büyük düğmeyle iki ekran boyuydu.

## Açılır menü

- Üst çubukta, sağda **menü düğmesi (☰)**, yalnızca dar ekranda (<1100px).
  Açtığı şey yeni bir menü değil, sayfada zaten duran `.yanmenu`: geniş
  ekranda solda sabit duran ana menü ya da tedavi ekranlarının aşama menüsü
  (v6.65). Dar ekranda gizliydi; artık üst çubuğun hemen altında panel
  olarak açılıyor, arkası karartılıyor. Tek yerde (`base.html` + CSS):
  60 şablonun hiçbirine dokunulmadı.
- Kapanma: menünün dışına dokununca, bir bağlantıya basınca, Esc, ekran
  genişleyince, geri tuşuyla dönülünce (`pageshow`). Menü açıkken arkadaki
  sayfa kaymıyor.
- Menüsü olmayan ekranda (giriş) düğme görünmüyor -- betik yalnızca
  `.yanmenu` varsa açıyor.
- Panelin tepesi üst çubuğun **ölçülen** alt kenarı (`--menu-ust`): iPhone'un
  çentiği çubuğun boyunu değiştiriyor, sabit bir sayı yazılmadı.

## Düğme ızgarası (`.dugmeizgara`)

İki sütunlu ızgara; `.genis` alan düğme iki sütunu kaplıyor. Üç yerde:
ana ekranın telefon menüsü (artık sayfanın dibinde değil, arama kutusunun
hemen altında; "Hasta kayıtları" geniş), tedavi ekranının aşama düğmeleri,
yönetici paneli ("Kullanıcılar" geniş). Sıra ve yazılar değişmedi; ana
ekranın düğmeleri sol menüyle hâlâ birebir aynı yazıyı kullanıyor.
Ölçüldü: ana ekran 1.419 → 1.280px, tedavi ekranı 2.848 → 2.498px, yönetici
paneli 2.755 → 2.448px; menü her ekranda tek dokunuşta.

## Uygulama gibi kurulum

- **Manifest**: renkler koyu temaya çekildi (`background_color` hâlâ v6.72
  öncesinin açık zeminiydi, Android'in açılış ekranı beyaz yanıp sönerdi),
  `id`, simgeler `any` ve `maskable` diye ayrı (birleşik yazım Chrome'un
  uyardığı biçim), simgeye uzun basınca üç kısayol (Hasta kayıtları, Cryo
  Haritası, Yeni hasta). `theme-color` da üst çubuğun rengi (`#111a25`).
- **Service worker** (`/sw.js`, kök adreste çünkü kapsamı bulunduğu klasör;
  `ACIK_YOLLAR`'da). **Hiçbir şeyi önbelleğe almıyor**: hasta verisi
  personelin telefonunda kalmasın, ekran her zaman sunucudaki güncel kaydı
  göstersin. Tek işi, sunucuya ulaşılamazsa (telefon klinik ağından çıktıysa)
  boş tarayıcı hatası yerine "Programa ulaşılamıyor -- Wi-Fi'ye bağlı mı,
  bilgisayar açık mı? [Tekrar dene]" sayfası. Kaydı yalnızca güvenli
  bağlantıda (`isSecureContext`); düz HTTP'de tarayıcı zaten izin vermiyor,
  sessizce atlanıyor.
- Uygulama olarak açıldığında sayfa sonunda esneme ve dokunma gölgesi yok;
  yatay tutulan iPhone'da üst çubuk çentiğin altında kalmıyor.
- Yönerge metinleri güncellendi: yeni iOS'ta paylaş düğmesi `•••` altında,
  Chrome'da seçenek artık "Uygulamayı yükle" de olabiliyor.
- Denendi (Chromium, localhost -- güvenli sayılan tek adres): service worker
  etkin, Chrome'un kurulabilirlik denetiminin tek itirazı test tarayıcısının
  gizli pencere olması; çevrimdışıyken sayfa açılınca yukarıdaki sayfa çıktı.

**Bilinen sınır -- Android için karar bekliyor:** Android'de "uygulama gibi"
(adres çubuksuz, kendi penceresinde) açılış ve "Uygulamayı yükle" düğmesi
**HTTPS** istiyor; program iç ağda düz HTTP ile çalışıyor (bekleyen iş 3).
iPhone'da bugün de tam ekran açılıyor. Bu sürümün parçaları HTTPS gelince
kendiliğinden devreye girecek şekilde yazıldı; HTTPS'in nasıl kurulacağı
(yerel sertifika, her telefona bir kez yüklenmesi) kullanıcıya soruldu.

Denendi: 390 ve 360px telefonda 17 ekranda yatay kaydırma yok, menü düğmesi
menüsü olan her ekranda var, girişte yok; 29 adres 200; geniş ekranda (1280px)
sol menü eskisi gibi, düğme gizli.

# v6.196 — HTTPS: kliniğin kendi sertifikası, Android'de uygulama gibi açılış

Kullanıcının kararı (2026-09-26): "Android için sertifikalı HTTPS'i hazırla"
(v6.195'in sonunda sunulan yol: kliniğe özel yerel sertifika, her telefona
bir kez). Android'de programın adres çubuksuz, kendi penceresinde açılması
ve "Uygulamayı yükle" güvenli bağlantı istiyor; program iç ağda düz HTTP
ile çalışıyordu (bekleyen iş 3). Bir sertifika kurumu iç ağ adresine
(192.168.x.x) sertifika vermediği için tek yol kliniğin kendi sertifikası.

## Sertifika: `sertifika.py`, kütüphanesiz

- **Kök** (`kok.crt` + `kok.key`, on yıl): telefona bir kez yüklenen "bu
  bilgisayarın imzasına güven". Özel anahtarı bilgisayardan çıkmıyor.
- **Sunucu sertifikası** (`sunucu.crt`, 397 gün): bilgisayarın adresleri
  (iç ağ IP'leri, 127.0.0.1, makine adı, `ad.local`, `localhost`) "Subject
  Alternative Name"de, kök tarafından imzalı. **Her açılışta denetleniyor**:
  yoksa, bugünkü adres sertifikada yoksa (DHCP adresi değiştirdi), makine
  adı değiştiyse ya da bitmesine 30 gün kaldıysa yeniden imzalanıyor --
  telefonlara bir şey yüklemek gerekmiyor, çünkü telefon köke güveniyor.
- Hepsi veri klasöründe `sertifika/`. **`.gitignore`'da**: bugünkü
  kurulumlarda veri klasörü depo klasörü; kök anahtarı ele geçen kliniğin
  telefonlarına sahte bir sunucu tanıtabilir.
- Kütüphanesiz (`excel.py`, `karekod.py`'nin gerekçesi: klinikteki makineye
  kurulum yok). RSA-2048 anahtar (Miller-Rabin ile asal arama), SHA-256 +
  PKCS#1 v1.5 imza, X.509 v3 (DER) elle yazılıyor; ilk üretim ~1,3 saniye.
  Telefonların kuralları: Apple (iOS 13+) RSA ≥ 2048, SHA-2, adres SAN'da,
  "serverAuth", sunucu sertifikası ≤ 825 gün; Chrome adresi SAN'da istiyor.
- Doğrulandı: OpenSSL `verify -x509_strict -purpose sslserver -verify_ip`
  geçti, yanlış adres reddedildi; curl kök sertifikayla IP'ye, makine adına
  ve `.local`'e bağlandı, sertifikada olmayan bir adı reddetti; ikinci
  çalıştırma hiçbir şeyi yeniden üretmedi, adres değişince yeniledi.

## İki kapı: düz HTTP (8000) ve HTTPS (8443)

`baslat.py` aynı süreçte iki sunucu açıyor. **Düz kapı kalıyor**: bugünkü
adres, iPhone simgeleri ve bilgisayarlar değişmeden çalışsın; kök sertifika
telefona oradan indiriliyor (köke güvenmeyen telefon güvenli adreste
"bağlantınız gizli değil" uyarısı görürdü). Aynı süreç olduğu için "aynı
kaydı iki kişi düzenliyor" uyarısı (bellekte, v6.55) iki kapıda ortak;
oturum çerezi de (çerezler porta bağlı değil).
- Açılış işleri (göçler, Excel haritası) yalnızca düz kapıda; güvenli kapı
  düz kapı açıldıktan SONRA açılıyor -- göç bitmeden gelen istek eski şemaya
  çarpmasın.
- Ctrl+C iki kapıyı birden kapatıyor: iki uvicorn sunucusu kendi sinyal
  işleyicisini kursa sonraki öncekini eziyordu, sinyali `baslat.py` tutuyor.
- **HTTPS hiçbir koşulda programı açılmaz yapmıyor**: sertifika
  hazırlanamazsa günlüğe yazılıp yalnızca HTTP ile açılıyor. `LAB_HTTPS=0`
  tümden kapatır, `LAB_HTTPS_PORT` portu değiştirir.
- `python3 -m uvicorn app:uygulama` ile açılan program HTTPS'siz (eskisi
  gibi); HTTPS `python3 baslat.py` ile. `app.HTTPS_PORTU` None ise ekranlar
  sertifika adımını göstermiyor.

## Telefonun yolu

- **`/sertifika`** (giriş istemiyor, `ACIK_YOLLAR`; hasta verisi yok):
  "Sertifikayı indir" (`/sertifika/kok.crt`, `application/x-x509-ca-cert`:
  iPhone "Profil indirildi" diyor, Android dosyayı indiriyor -- Android 11'den
  beri tarayıcıdan doğrudan yüklenemiyor, Ayarlar'dan seçiliyor), telefona
  göre adımlar, "Güvenli adresi aç", kökün SHA-256 parmak izi. Sayfa
  telefonun köke güvenip güvenmediğini **ölçüyor** (güvenli adresten küçük
  bir resim istiyor; güvenilmeyen sertifikada tarayıcı yüklemiyor) ve
  güveniyorsa yeşil "yüklü ve güvenilir" yazıyor.
- **"Telefona ekle" (`/baglan`)**: ana karekod eskisi gibi düz adres
  (iPhone düz adresle de tam ekran açılıyor, eklenmiş simgeler bozulmasın);
  Android kartında ikinci karekod `/sertifika`'ya açılıyor, altında güvenli
  adres ve sertifikanın geçerlilik sonu. Güvenli kapıdan bakılsa da düz
  adres düz kapının portuyla kuruluyor (`app.DUZ_PORTU`).
- `/ekle`'nin Android kartı güvenli bağlantı varken önce sertifikaya
  yönlendiriyor.
- iPhone için sertifika **isteğe bağlı** (sayfada yazılı).

## Denendi

Kök sertifikaya güvenen Chromium'da (telefon görünümü) güvenli adreste
`isSecureContext` doğru, service worker (v6.195) etkin, Chrome'un
kurulabilirlik denetimi **hiç engel bildirmedi**; aynı tarayıcıda düz adreste
tek engel "not-from-secure-origin" (bugünkü durum). 14 ekran iki kapıda da
200; HTTPS kapalıyken (`LAB_HTTPS=0`) program eskisi gibi açıldı, sertifika
sayfası "açık değil" dedi.

**Bilinen sınırlar**: gerçek bir Android telefonda ve iPhone'da henüz
denenmedi (menü adları markaya göre değişiyor, sayfa bunu söylüyor).
`sertifika/` yedeklenmiyor: bilgisayar değişir ya da klasör silinirse yeni
kök üretilir ve telefonlara sertifika yeniden yüklenir. Mac ile klinik
bilgisayarının kökleri ayrı (her makine kendi kökünü üretiyor; `tasi.py`
yalnızca `lab.db`'yi taşıyor). Windows güvenlik duvarı 8443'ü engellerse
telefon güvenli adrese ulaşamaz (KOMUTLAR.md).

# v6.197 — Blastokistte arrest yazılan embriyo vitrifikasyonda görünmüyor

Kullanıcının isteği (2026-09-26): "Blastokist aşamasında arest olarak
kaydedilen embriyoları vitrifikasyon aşamasında hiç gösterme." v6.137'den
beri vitrifikasyon listesi yalnızca değerlendirilmiş embriyoyu gösteriyordu
(`_DEGERLENDIRILMIS`), ama arrest de bir değerlendirme: blastokist ekranında
"Arrest" seçilen embriyo listede duruyor, seçilip dondurulabiliyordu.

- **Süzgeç `_blastokistte_arrest(cycle_id)`**, `_vit_adaylari()`'na
  blastokist aşaması olan her tipte ekleniyor (IVF/ICSI, FET (3→5 kültür),
  Yumurta Çözme; koşul `TIP_ASAMALARI`'na bakıyor). Ekran ve kayıt aynı
  koşulu soruyor: eski bir sekmeden gönderilen arrest embriyo da
  kaydedilmiyor.
- **Ölçü son blastokist değerlendirmesi** (gün, sonra saat): 5. gün arrest,
  6. gün 4AA yazılan embriyo listede kalıyor. `specimen.durum`'a
  bakılmıyor -- her aşamada üzerine yazılıyor (v6.139'un gerekçesi).
- **Bu tedavinin değerlendirmesi** (`db.bu_tedavide()`): FET (3→5)'te
  çözülüp arrest yazılan embriyo FET'in listesinden düşüyor.
- **Bu tedavide zaten dondurulmuş örnek kalır** (sonradan arrest yazılmış
  olsa da): "Dondurulmuş" kartı aynı listeden besleniyor, geri alma yolu
  kaybolmasın (v6.137'nin kuralı).
- **Gizleniyor, kilitlenmiyor**: dejenere yumurta "Dej." ile kilitli
  görünüyor (v6.139, kullanıcının isteği); burada kullanıcı "hiç gösterme"
  dedi. Arrest kaydı blastokist ekranında duruyor; silinir ya da sonraki gün
  başka bir değer yazılırsa embriyo listeye döner.
- Transfer ekranı arrest embriyoyu zaten göstermiyordu (`TRANSFERE_UYGUN`'da
  `arrest` yok). Arrest yalnızca blastokist değerlendirmesinin bir seçeneği
  (`bl_genisleme`); cleavage'da böyle bir değer yok.

## Denendi

Kullanıcının veritabanının bir kopyasında (hiç arrest kaydı yoktu, bir
IVF/ICSI tedavisinde yazıldı): dondurulmamış embriyo arrest olunca listeden
ve kayıt denetiminden düştü, dondurulmuş olan kaldı; ertesi güne başka bir
değer yazılınca döndü, o gün de arrest olunca yine düştü. Beş tedavi tipinin
vitrifikasyon ekranı 200.

# v6.198 — Vitrifikasyon kaydı vitrifikasyon ekranına dönüyor

Kullanıcı bildirdi (2026-09-26): "Vitrifikasyon işleminde bir embriyonun
işlemi bittikten sonra başka embriyosu varsa tedavinin vitrifikasyon
aşamasına geri dönemiyorum." Kayıt tüpün sayfasına (`/cryo/tasiyici/{id}`)
gidiyordu. O sayfa bir tedavi ekranı değil: aşama menüsü yok, geri oku sabit
`/cryo` adresinde. v6.126'nın geri betiği yönlendirmeyle gelinen sayfada
bilerek karışmıyor (az önce kaydedilen forma dönülmesin diye), yani geri ok
Cryo Haritası'na çıkıyordu. Telefonda ana ekrandan açılan programda
tarayıcının kendi geri düğmesi de yok.

- **Kayıt vitrifikasyon ekranına dönüyor**:
  `/cycle/{id}/vitrifikasyon?kaydedildi=<tüp>`. Öteki aşama ekranlarının
  "kaydet → sıradaki" akışının karşılığı: kalan embriyolar listede, az önce
  dondurulan "Dondurulmuş" listesinde (tüp bağlantısıyla), "İşlemi bitir"
  de bu ekranda (v6.29'un "işin bittiği yer" gerekçesi).
- **Üstte yeşil mesaj**: "Kaydedildi: 2 embriyo, taşıyıcı …" ve "Taşıyıcıya
  git" bağlantısı. Adresten yalnızca tüpün numarası geliyor; metin
  veritabanından, tüpte bu tedavinin dondurması yoksa (geri alınmış kayıt,
  başka tedavinin tüpü) mesaj basılmıyor (tuzak #9).
- **Önerilen etiket aynı dakikada çakışmıyor** (`_etiket_onerisi()`).
  Ekran hemen geri gelince ikinci tüp çoğu zaman aynı dakikada dondurulur;
  öneri ilk tüpün etiketi olurdu, kayıt "zaten var" diye reddedilir ve
  seçimler boşalırdı. Etiket varsa dakika ilerliyor, aktarım aracının kuralı
  (`aktar_access._tasiyici_ac()`).

## Denendi

Kullanıcının veritabanının bir kopyasında, iki adayı olan bir IVF/ICSI
tedavisinde: ilk embriyonun kaydı vitrifikasyon ekranına döndü, mesaj doğru
tüpü yazdı, ikinci embriyo listede kaldı; aynı dakikadaki ikinci öneri bir
dakika ilerledi ve ikinci tüp hatasız kaydedildi. Başka bir tüpün numarası
verilince mesaj basılmadı.

# v6.199 — "Tankları Excel'e aktar" laboratuvarın kendi Cryo Haritası Excel'ini veriyor

Kullanıcının isteği (2026-09-26): "Tankları Excel'e aktar dediğimde benim
kullandığım orjinal cryo haritaya çıktı alsam. Farklı yapıda excel oluşturma
benim orjinal cryo harita excelimi birebir kullan." Düğme v6.36'dan beri
programın kendi düz listesini, veri klasöründeki otomatik dosya (v6.191)
programın kendi tank düzenini yazıyordu; ikisi de laboratuvarın 6 sayfalık,
36 Excel tablolu (NO, SOYAD, AD, EŞİ, TARİH, HÜCRE, VİAL) dosyasından farklıydı.

## Nasıl çalışıyor

Program laboratuvarın dosyasını bir kez alıyor (Cryo Haritası → "Excel
haritası" kartı, yönetici; `POST /cryo/sablon`), `lab.db`'de saklıyor
(`goc_054`, `cryo_sablon` tablosu: `lab.db` USB ile taşınan tek dosya, şablon
ayrı dursaydı öteki makinede olmazdı -- `lab_formu`'nun gerekçesi) ve her
çıktıda **o dosyayı dolduruyor** (`cryo_sablon.py`). Sayfalar, Excel
tabloları, sütun genişlikleri, biçimler, başlıklar, NO sütunu, yazıcı
ayarları bayt bayt aynı; yalnızca straw satırlarının değer hücreleri
değişiyor:

- **Straw hâlâ o gobletteyse satırı aynen kalır** (laboratuvarın yazdığı
  gibi). Hangi satırın hangi straw olduğu `cryo_esle.py`'nin eşleştirmesiyle
  (hasta + gün + içerik; sperm satırında ad + gün) ve Excel kayıtlarında
  içerik anahtarıyla bulunuyor -- `yerlesim_plani()`'nin "temsil" ölçüsü:
  tüp tankta ve konumu bu goblet. Eşleştirme 1 saniye sürdüğü için
  saklanmıyor, her çıktıda yeniden kuruluyor (şablonun okunmuş hali bellekte).
- **Straw artık orada değilse** (çözüldü, başka merkeze taşındı, başka yere
  kondu, Excel kaydı "tanktan çıkarıldı") satırın değerleri silinir; NO ve
  hücre biçimi kalır.
- **Programda o goblete konmuş straw** gobletin boş satırına yazılır: önce
  Excel'de zaten boş olan satırlar, sonra boşalanlar (yazılı straw'lar yer
  değiştirmesin). Başka gobletten taşınmışsa eski satırının yazısı taşınır.
  Programda dondurulmuşsa laboratuvarın son yıllardaki yazımıyla (Excel'den
  ölçüldü): TARİH gerçek tarih hücresi (sütunun biçimiyle), HÜCRE "D5
  (3BA-1BB)", yumurtada "OOSİT (4M2-1M1)", FET'te yeniden dondurulan
  "... REFREEZE", VİAL "1 CRYOLOCKMAVİ 2" (baştaki sayı straw adedi, sondaki
  aynı tedavide aynı gün dondurulanlar arasındaki sırası -- iki ayrı günde
  numaralı straw'ı olan 78 hastanın 50'sinde ikinci gün 1'den başlıyor; tek
  straw'da yok), sperm "EJAKÜLAT" / "EJAKÜLAT-CA" (onkolojik) / "TESE", VİAL "1".
- **SOYAD / AD** (kullanıcının kararı): hastanın Excel'de satırı varsa
  oradaki yazım; yoksa son kelime soyad, gerisi ad (programdaki adların
  3.125'te 3.116'sı "AD SOYAD" sırasında; iki kelimelik soyadında ilk kelime
  AD'a kayar ama ad yine tam okunur). Çiftin kaydındaki sperm eşindir
  (`es_adi`), EŞİ o zaman kadının adı.
- **"2 CRYOLOCK" gibi birden çok straw'ı tek satırda anlatan satır** aynı
  hastanın aynı gün dondurulmuş öteki tüplerini de taşıyor, onlar ayrıca
  yazılmıyor (v6.189'da 6 goblet).
- **Programın hiçbir kaydıyla eşleşmeyen dolu satır boşaltılmıyor**: dosya
  tank düzeni kurulduktan sonra Excel'de elle değiştirilmişse program o
  straw hakkında hiçbir şey bilmiyor, "gitti" sayamaz. Kart sayısını söyler.
- **Yer bulamayan straw** (goblet dolu, gobleti dosyada yok) yazılmıyor;
  sayısı ve etiketiyle listesi kartta. Konumu girilmemiş ya da tank
  düzeninde olmayan tüpler laboratuvarın dosyasında da yoktu, yine yok.
- **Paylaşılan metin tablosu (sharedStrings) baştan kuruluyor**: boşalan
  satırın adı başka hiçbir hücrede geçmiyorsa dosyada görünmeyen bir köşede
  de kalmıyor (denendi).

Dosya kütüphanesiz, XML düzeyinde değiştiriliyor (`excel.py`/`xlsx_oku.py`
gibi): satırlar ve hücreler sırasıyla okunuyor, beklenmeyen bir yapı varsa
dosyaya dokunulmuyor (hata); yazılan her parça XML olarak yeniden
denetleniyor. Dışarıdan gelen dosya için `xlsx_oku.py`'nin korumaları
(boyut, parça sayısı, DOCTYPE/ENTITY).

## Otomatik dosya ve düğme

Kullanıcı veri klasöründeki otomatik dosyanın da bu biçimde olmasını seçti.
`harita_excel.guncelle()` şablon yüklüyse onu dolduruyor (imza, atomik yazım,
günlük kopya aynı); doldurulamazsa programın düzenine düşüyor, sebebi karta
(dosyasız kalmaktansa). "Tankları Excel'e aktar" (`/disari/cryo`) aynı dosyayı
veriyor; şablon yokken eski düz liste. Şablon yüklüyken kartın ikinci indirme
düğmesi gizli: aynı dosyayı iki adla göstermesin.

## Denendi

Kullanıcının veritabanının bir kopyasında (`yerlesim`'den sonraki hal) ve
laboratuvarın dosyasıyla: değişiklik yokken 38.138 değerli hücrenin hepsi
değeri ve biçimiyle birebir aynı, öteki bütün parçalar bayt bayt aynı,
openpyxl 36 tabloyla açıyor. Senaryolar: çözülen tüpün satırı boşaldı,
başka gobletlere taşınan tüpün eski satırı boşaldı ve yeni gobletinde kendi
yazısıyla çıktı, tanktan çıkarılan Excel kaydının satırı boşaldı, programda
dondurulan yeni straw boş satıra doğru yazımla yazıldı (TARİH hücresi tarih
biçiminde). Yükleme, kart ve düğme uygulamadan denendi; .xlsx olmayan,
bozuk ve yanlış dosya reddedildi, önceki şablon yerinde kaldı. Süre:
eşleştirme + doldurma ~1 sn (şablonun ilk okunması 2 sn).

**Bilinen sınırlar**: gerçek Excel'de açılarak denenmedi -- bu ortamdaki
LibreOffice hiçbir .xlsx'i açamıyor, programın kendi ürettiği en basit
dosyayı bile. Satır eklenmiyor (kanister blokları yan yana, bir satır
eklemek komşu kanisterleri kaydırırdı): gobletin satırı yetmezse straw
yazılmıyor, kart söylüyor. Tank düzeni Mac'teki veritabanında; dosya da
orada yüklenmeli, `tasi.py` ile kliniğe gider.

# v6.200 — ICSI'de genel bulgular; ART Lab'ın Yorum satırına onlar yazılıyor

Kullanıcının isteği (2026-09-26): "ICSI bölümünde de yumurtaların bulguları
tek tek yazılıyor. ART lab formunda en altta yorum bölümüne yazılıyordu.
Bunu kaldıralım. Onun yerine ICSI bölümüne genel bulgular bölümü olsun,
açılır pencere şeklinde, aynı yumurta bulguları gibi bulgular olsun; bunlara
ek olarak sperm problemleri olsun: Sperm morfolojisi kötü, Baş Boyun
anomalisi var, Sperm motilitesi kötü, diğer elle yazılabilir olsun. Bunlar
ART lab formunun en alt kısmındaki yorum bölümüne eklensin."

## Ne değişti

- **ICSI ekranında "Genel bulgular" kartı**, "İşlemi yapan"ın hemen üstünde
  (ikisi de tedavinin, yumurtanın değil). Karta basınca yumurta
  bulgularınınkiyle aynı açılır pencere: "Yumurta" grubu (yumurta yumurta
  bulgunun aynı listesi, `bulgu_icsi`), "Sperm" grubu (kullanıcının üç
  sorunu, onun yazımıyla) ve elle yazılan "Diğer". Pencerenin kendi
  "Kaydet"i var; kaydetmeden kapatılan pencere kayıtlı hale döner, kart hep
  kayıtlı hali gösteriyor.
- **ART Lab formunun alttaki "Raporu dolduran … Yorum:" satırına** bu
  bulgular yazılıyor: "Yorum: Kalın zona, Vakuol, Sperm motilitesi kötü,
  …". Yumurta yumurta bulgular (v6.135) artık oraya yazılmıyor.
- **Yumurta yumurta bulgu ICSI ekranında duruyor**: yumurtanın bilgi
  kartında görünüyor, değiştirilebiliyor; yalnızca forma basılmıyor.
  "Bunu kaldıralım"ı formdaki satır olarak okudum. Ekrandan da kalksın
  denirse kaldırmak kolay.
- **Yumurta Dondurma'nın formu değişmedi**: orada ICSI yok, genel bulgu
  bölümü de yok; denüdasyonda işaretlenen yumurta bulguları eskisi gibi
  numarasıyla yazılıyor. Yumurta Çözme'de ICSI var, genel bulgular geçerli.

## Nasıl

- **`goc_055`**: `tedavi_bulgu` tablosu (tedavi + aşama; satır ya bir liste
  değeri, `liste_adi` + `bulgu_kodu`, ya da elle `metin`) ve `bulgu_sperm`
  listesi. `specimen_bulgu`'nun tedavi hali, küme olarak yazılıyor (sil +
  ekle, tek işlemde). Liste adı tutuluyor, çünkü seçenekler iki listeden
  geliyor ve etiket listesinden aranıyor. Etiketler `liste_degeri`'nde.
- **Okuma tek yerde**: `db.tedavi_bulgulari()` (listelerin sırasıyla) ve
  `db.tedavi_bulgu_metni()`. Karttaki özet ile formun satırı aynı metin.
- **Yumurta formundan ayrı bir form** (`POST /cycle/{id}/icsi/genel-bulgu`):
  yumurtanın kaydına dokunmuyor, dönüş aynı yumurtaya. Adres ICSI modülüne
  düşüyor, izin ekranınkiyle aynı. Sunucu yalnızca iki listenin değerlerini
  kabul ediyor; "Diğer" tek satıra indiriliyor, en çok 120 harf.
- **Listeden kaldırılmış değer** bir tedavide kayıtlıysa pencerede kendi
  çipiyle kalıyor, "Kaydet" onu sessizce silmiyor (tuzak #6).
- **Sayfada artık iki çip penceresi var**: yumurta bulgusunun betiği
  sayfadaki bütün çiplere bakıyordu ("Temizle" genel bulguları da
  silerdi). Artık yalnızca kendi penceresine bakıyor.
- **Kalıcı silme** tabloyu biliyor (`cycle_tamamen_sil()`, `teshis_silme.py`,
  tuzak #4); tam dökümde sayfası var; `liste_duzenle.py` iki listenin
  kullanımını sayıyor. Göç çalışmamışsa kart basılmıyor, form eskisi gibi
  (tuzak #3).

## Satıra sığma

Kâğıdın basılı "Raporu dolduran … Yorum:" yazısı satırın ~%80'ini
kaplıyor: "Yorum:"dan sonra tam puntoda ~35 harf sığıyor (ölçüldü). Satır
sayfanın sağ kenarında bitiyor, taşarsa kâğıdın dışına çıkar. v6.150'nin
kuralı: taşma yoksa küçült, asla kesme. Hücre `.sigdir` oldu, Excel'de
`shrinkToFit`. 94 harflik bir bulgu satırı puntoyu %79'a indiriyor ve tam
sığıyor; bulgusuz formda punto değişmiyor. **Bilinen sınır**: küçültme en
çok yarıya iniyor (~200 harf); bütün çipler birden seçilirse sığmaz.

## Denendi

Kullanıcının veritabanının bir kopyasında (telefon boyutu, 390px) bir
IVF/ICSI tedavisinde:
- iki yumurta ve iki sperm bulgusu + "Diğer" kaydedildi, karta ve ART Lab
  formunun Yorum satırına (ekran, yazdırma ve Excel) aynı metin yazıldı;
- kaydetmeden kapatılan pencere kayıtlı hale döndü;
- yumurta penceresinin "Temizle"si genel bulgulara dokunmadı;
- sayfa hatası ve yatay taşma yok;
- sahte bir kod ve dönüş adresine yazılmış başka bir değer düştü;
- pasif yapılan bir değer pencerede işaretli kaldı, yeniden kaydedince
  silinmedi;
- ICSI'li formda yumurta yumurta bulgu artık yok, Yumurta Dondurma'nın
  formunda eskisi gibi var;
- "Temizle" + "Kaydet" hepsini sildi, Yorum satırı kâğıttaki gibi kaldı;
- yumurtası olmayan tedavide kart çıkmadı;
- kalıcı silme (`cycle_tamamen_sil()` bir kopyada, `teshis_silme.py`)
  kırık bağ bırakmadı;
- göçsüz veritabanında ekran ve form hatasız.

# v6.201 — Sağlık Bakanlığı'nın aylık verileri (Yönetici)

Kullanıcının isteği (2026-09-26): "Ünite olarak Sağlık Bakanlığı'nın bizden
istediği aylık veriler var: OPU SAYISI, DONDURULMUŞ OOSİT SAYISI, TESE
SAYISI, DONDURULMUŞ SPERM SAYISI, IUI SAYISI, SİKLUS SAYISI, EMBRİYO
TRANSFER SAYISI, EMBRİYO İMHA SAYISI, GEBELİK SAYISI, CANLI DOĞUM SAYISI,
TOTAL HASTA SAYISI. Yönetici bölümünde bunların tutulduğu bir bölüm olsun.
IUI sayısı ve İmha sayısı hariç ay ay gösterilen bir bölüm olsun. 2026
yılından öncesi olmasın."

## Ne var

- **Yönetici paneli → "Bakanlık verileri"** (`/bakanlik`, yalnızca
  yönetici). Satır başına bir ay, bakanlığın formundaki dokuz sütun ve
  sırası (IUI ile embriyo imha programda tutulmuyor, yok). Yıl seçici
  2026'dan başlıyor; bu yılın bitmemiş ayı "ay bitmedi" diye işaretli, en
  altta yılın toplamı.
- **Excel'e aktar** (`/disari/bakanlik?yil=`): aynı tablo, bakanlığın
  sütun adlarıyla.
- **"Nasıl sayılıyor"**: her sütunun tanımı ekranın altında yazılı —
  sayılar bakanlığa gidiyor, neyin sayıldığı görünmeli.
- **Tarihi girilmemiş için sayılmayanlar** listeleniyor: kontrol zamanı
  girilmemiş klinik gebelik, doğum zamanı girilmemiş canlı doğum. Satır o
  tedavinin gebelik ekranına gidiyor.
- "Tutulsun" ayrı bir tablo değil: sayılar her açılışta kayıtlardan
  türetiliyor (v6.38'in kuralı). Geçmiş bir ayın kaydı düzeltilince o
  ayın sayısı da düzeliyor.

## Tanımlar (kullanıcının cevapları)

Her sütun birden çok şekilde sayılabildiği için kullanıcıya soruldu; sekiz
sorunun dördünde benim önerim seçilmedi.

| Sütun | Sayılan | Ay |
|---|---|---|
| OPU | OPU'su yapılan tedavi | OPU günü |
| DONDURULMUŞ OOSİT | yumurta dondurma **işlemi**: yumurtası dondurulan tedavi (adet değil) | dondurma günü |
| TESE | bütün cerrahi alımlar (TESE, mikroTESE, TESA, PESA, MESA): androlojinin alınma yöntemi ve sperm dondurmanın sebebi; aynı kişi aynı gün bir | alım / dondurma günü |
| DONDURULMUŞ SPERM | dondurma **işlemi**: aynı kişinin aynı gün dondurulan tüpleri bir | dondurma günü |
| SİKLUS | bütün tedaviler (her tip, iptal edilenler de) | tedavinin günü |
| EMBRİYO TRANSFER | transfer **işlemi** (taze ve donmuş), embriyo sayısı değil | transfer günü |
| GEBELİK | klinik gebelik | gebelik ekranındaki kontrol zamanı |
| CANLI DOĞUM | sonucu canlı doğum olan gebelik; ikiz doğum bir | doğum zamanı |
| TOTAL HASTA | o ay yeni kaydedilen hasta | hastanın ilk kaydı |

- **Tedavinin günü** `db.tedavi_tarihi()`: OPU, yoksa hCG; FET'te çözme ya
  da transfer; hiçbiri yoksa planlanan tarih ya da açılış (numaralamanın
  kuralı, v6.144). Hasta kayıtlarının ay listesi FET'te açılış gününe
  bakıyor (`COALESCE(opu_zamani, olusturma_zamani)`); programda açılan bir
  FET ay sonunda açılıp ertesi ay transfer edildiyse iki ekran o FET'i
  farklı aylarda sayar. Aktarılan kayıtlarda ikisi aynı gün.
- **Yeni hastanın ölçüsü ilk kaydı**: kartın açılışı, ilk tedavisi, ilk
  sperm dondurması — hangisi önceyse. Kartın açılış tarihi tek başına
  yetmiyordu: Access dosyaları karışık sırayla aktarıldı (önce 2026, sonra
  2025 … 2018) ve aktarım var olan kartın tarihine dokunmuyor. 2026
  dosyasından açılmış bir kartın 2025 tedavisi sonradan geldiyse hasta
  2026'da "yeni" görünürdü. Kullanıcıya gösterilen seçenek de bunu
  söylüyordu: "Access'ten aktarılanlar ilk tedavilerinin ayında".
- **"Aynı kişi"**: erkeğin kendi kartı bir çiftin `es_dosya_no`'suyla o
  çifte bağlıysa ikisi bir sayılıyor (dosya numarası tek eşleştirme
  anahtarı, v6.125). Aynı gün hem ICSI'de kullanılıp hem dondurulan bir
  TESE iki kez sayılmasın diye. Bağlanmamış ayrı erkek kartında bu
  eşleşme yapılamıyor, isimle eşleştirme yazılmadı.
- **Sütun adları bakanlığın yazısı** ("SİKLUS", "OOSİT"): ekrandaki
  "tedavi"/"yumurta" kuralının dışında, resmî formların kâğıt kalıbı gibi.
- Cryo Haritası Excel'inden açılan program öncesi tedaviler (2011–2017)
  dışarıda, istatistiğin kuralı; 2026'ya zaten düşmüyorlar.

## Klinik gebelik: `evet` de sayılıyor (istatistikte de)

Gebelik ekranı "Klinik gebelik"i `evet` / `hayir` / `bilinmiyor` diye
yazıyor. `/istatistik`'in gebelik oranı `klinik_gebelik = 1` sayıyordu:
ekrandan girilen klinik gebeliklerin **hiçbiri** oranda yoktu, yalnızca ilk
test kayıtlarının `1`'leri sayılıyordu. Koşul tek yerde
(`db.klinik_gebelik_sql()`: `evet` ya da `1`), istatistik ve bakanlık
verileri onu kullanıyor.

## `goc_056`: `olay(tr_cycle_id)` dizini

Tedavinin günü FET'lerde `olay`'a "bu tedavi için yapılan çözme ya da
transfer" diye soruyor (`thaw_cycle_id = c.id OR tr_cycle_id = c.id`).
`tr_cycle_id`'nin dizini yoktu; OR'un bir kolu dizinsiz olunca her FET
için bütün tablo taranıyordu. 1.909 tedavinin günü dizinsiz 5,2 sn,
dizinle 0,01 sn sürüyor. Bakanlık ekranı 0,05 sn'de açılıyor. Aktarım
aracının ay önbelleğini de hızlandırıyor ("3.000 tedavide 14 sn").

## Telefonda

On sütun dar ekrana sığmıyor. İlk denemede tablo kartın içinde yatay
kayıyordu, ay sütunu da yapışkandı. Ekran görüntüsünde yapışkan sütunun
altına yarım giren sayılar yanlış okunuyordu: Nisan'ın 128'i "28",
toplamın 561'i "61" görünüyordu. Kaydırmayı sütun başlarına oturtmak
tablonun sonunda yine yarım sütun bıraktı. Kullanıcı da telefonda yatay
kaydırmayı v6.117'de istememişti. Bugün kutu 740px'ten darsa her ay kendi
bloğu, satır satır "SÜTUN ADI — sayı". Ölçü ekranın değil kutunun
genişliği (container query); desteklemeyen eski tarayıcıda tablo kayar.

## Denendi

Kullanıcının veritabanının bir kopyasında (mayıs 2026'nın aktarımı o
kopyada yok):
- sayılar ayrı sorgularla karşılaştırıldı: TESE ve sperm ay ay elle
  sayılanla, yumurta dondurma Yumurta Dondurma tedavilerinin dondurma
  ayıyla, transfer tedavi-gün sayımıyla, siklus tip dökümüyle birebir;
- `goc_056` açılışta kendiliğinden uygulandı;
- telefon (390), tablet (768) ve masaüstü (1440) genişliğinde sayfa
  taşmıyor, hücre kesilmiyor, sayfa hatası yok;
- yıl 2019 ve 2031 verilince 2026'ya düşüyor;
- Excel dosyası açılıyor (11 satır: başlık, 9 ay, toplam);
- gebelik ekranından girilen `evet`li bir gebelik kontrol ayında, ikiz
  doğum doğum ayında bir kez sayıldı; istatistik ekranı da artık onu
  görüyor.

# v6.202 — Hasta kartında FET tiplerinin günü; dondurmada tanka göre boş yer önerisi

Kullanıcının isteği (2026-09-26): "FET, FET 3-5, Yumurta çözme
tedavilerinin altında tarih hasta kartında görünmüyor. Hangi tarihte
yapıldığı görünsün. Bir de dondurma işlemi yapılacağı zaman boş yer önerisi
sabit, değiştirilebilsin. Eğer olabiliyorsa tank belirterek de öneri
versin. Hem otomatik öneri versin hem de ben sorgulayabileyim."

## Hasta kartı: işlemin günü

Tedavi satırı yalnızca OPU tarihini basıyordu. FET, FET (3→5) ve Yumurta
Çözme'de OPU yok, satırda hiç tarih yoktu. Artık bu üç tipte çözme günü
yazıyor ("FET · Çözme 14.10.2025"); transfer başka bir gündeyse o da
("Çözme 10.03.2026 · Transfer 12.03.2026", FET (3→5)'te ve Yumurta
Çözme'de olağan).

- Gün bu tedavi İÇİN yapılan olaylardan: çözme `thaw_cycle_id`, transfer
  `tr_cycle_id`, boşsa örneğin kendi tedavisi (aktarılmış FET'in kendi
  örnekleri) -- `db.olay_tedavisi()`'nin kuralı. Sorgu
  `app._islem_gunleri_sql()`.
- Yalnızca `db.FET_TIPLERI`'nde: IVF/ICSI'nin günü OPU. v6.155'ten önce
  ICSI'ye yazılmış bir çözme IVF satırına "Çözme" diye düşmesin.
- Satırdaki yaş da o günün yılından. Eskiden kaydın açıldığı andan
  hesaplanıyordu; önceden açılan bir FET'te bu gün çözme günü değildi.
- Ay listesi (`/hastalar`) değişmedi: ayın ölçüsü OPU, yoksa açılış
  (v6.29, kullanıcının kararı).

## Dondurma: otomatik öneri ve sorgu

v6.190'ın önerisi her açılışta aynı kuralla aynı yerleri gösteriyordu.
Başka bir tank istenirse kutulara elle yazmak gerekiyordu; orada da o
gobletin durumu görünmüyordu, yalnızca sorun varsa uyarı çıkıyordu.

- **Otomatik öneri aynı**: ekran bütün tanklara bakan öneriyle açılıyor,
  ilk aday kutulara ve renge yazılı.
- **Tank / kanister seçicisi**: tank seçilince aynı kural (hastanın o
  yerdeki straw'ları önce, sonra yakını, sonra "bugün kaç straw"a en iyi
  sığan) yalnızca o tankın gobletleri için soruluyor; kanister de
  seçilebiliyor. İlk aday kutulara yazılıyor, başka bir adaya dokunmak yine
  değiştiriyor. "Bütün tanklar (otomatik)" otomatik öneriye döndürüyor.
- Seçicide her tankın ve kanisterin **önerilebilir boş yuvası** yazıyor:
  öneriyle aynı ölçü (`yerlesim._aday()`: embriyo gobleti, kapasitesi
  bilinen, paletin boş bir rengi olan). Yedek katların yuvası ayrı sayılıyor
  ("TANK 5 · 25 boş yuva · 599 yedek yuva"), olağan yer biterse diye
  hazırlandılar (v6.192).
- Liste başına 6 aday görünüyor, gerisi "N öneri daha göster"in arkasında:
  otomatikte 12 aday, sorguda o yerin bütün adayları (en çok 60; bugünkü
  düzende bir kanisterin kapasitesi bilinen gobleti en çok 60).
- **Elle yazılan yer de sorgulanıyor**: yazılan ya da seçilen goblet
  düzendeyse altında "Seçilen goblet: 3 / 4 straw · Yeşil, Mavi, Sarı"
  (`yer-kontrol`'ün cevabı).

Liste tek yerde, `templates/_yer_oneri.html`. Ekran ilk açılışta onu
basıyor; sorgunun cevabı
`GET /cycle/{id}/vitrifikasyon/yer-oneri?kac=&tank=&kanister=` aynı
makronun HTML'i. Hiçbir şey yazmaz, izni vitrifikasyonun (`yer-kontrol`
gibi). "Kaç straw" değişince de liste sunucudan geliyor: sayfada dört
liste değil tek liste var. Kaydetme değişmedi: denetim, onay kutusu ve
sunucunun reddi aynı (`yer_uyarilari()`).

## Denendi

Kullanıcının veritabanının bir kopyasında (tank düzeni v6.192'deki
haliyle):
- 705 FET tipi tedavinin 701'i gün aldı; 4'ünde henüz çözme ya da transfer
  yok. 1.909 tedavinin sorgusu 0,01 sn.
- Tank seçilince listede yalnızca o tank, kanister seçilince yalnızca o
  kanister vardı. "3 straw"da ilk aday 3 boş yuvalı goblet oldu. Otomatiğe
  dönünce kanister seçicisi kapandı.
- 390 ve 1280 px'te sayfa taşmıyor. Telefonda iki seçici yan yana
  sığmıyordu, yazıları kesikti; artık dar ekranda alt alta diziliyorlar.

# v6.203 — Ağ erişimi anahtarı, Cryo haritası klasörü, yeni bilgisayara geçiş

Kullanıcının soruları (2026-09-27): "Uygulamayı başka PC'de çalıştırmak
istersem nasıl bir yol izlemeliyim ... Cryo haritanınki başka bir PC'de
programı açarsam nasıl olacak, hangi klasöre gidecek? ... Program sadece
olduğu PC'de çalışsın ... önce yerelde açıp daha sonra ağdan yaysak?"
Kararları: yeni kurulum ağa kapalı başlasın (kendisi açacak), yeni bilgisayara
geçerken sertifika da taşınsın, kurulum dosyası Windows ve Mac için birlikte
(v6.204).

## Ağ erişimi

Yönetici → **Ağ erişimi** (`/ag-erisimi`): "Yalnızca bu bilgisayar" ya da
"İç ağa açık". Kapalıyken başka bir bilgisayardan ya da telefondan gelen
**her** istek (giriş ekranı, `/static`, sertifika sayfası dahil) tek bir
sayfa görüyor: "Program yalnızca kurulu olduğu bilgisayarda açık". Sayfada
hasta verisi, menü, bağlantı yok; biçimi satır içinde, çünkü `/static` de
kapalı.

- **Hemen geçerli.** Middleware her istekte soruyor (`db.ag_erisimi()`,
  dosyanın değişme zamanına bakan küçük önbellek); programı yeniden başlatmak
  gerekmiyor. Sunucu yine `0.0.0.0`'da dinliyor, kararı uygulama veriyor.
  Açılışta dinleme adresini değiştirmek (127.0.0.1) değişikliği yeniden
  başlatmaya bağlardı; kullanıcının istediği "önce yerelde aç, sonra ağdan
  yay" buydu.
- **"Bu bilgisayar"**: bağlantının öteki ucu döngü adresi (localhost) ya da
  bilgisayarın kendi ağ adresi. Başlık okunmuyor: `baslat.py` uvicorn'a
  `proxy_headers=False` veriyor, `X-Forwarded-For: 127.0.0.1` yazan cihaz
  yine engelleniyor (denendi).
- **Makineye özel** (`yerel_ayar.json`, `ag_erisimi`): `lab.db` USB ile
  taşınıyor, ayar veritabanında olsaydı bir bilgisayarın "açık"ı ötekine
  giderdi.
- **Yazılmamışsa açık**: bugünkü Mac ve klinik kurulumu değişmedi.
  "Yalnızca bu bilgisayar"ı yeni kurulum yazıyor: `sifirdan_kur.py`, boş bir
  makineye ilk `tasi.py iceri`, v6.204'ün ilk açılış ekranı. "Makinenin
  bölümü yoksa yeni kurulum" demek güvenilir olmazdı: Mac'in makine adı ağa
  göre değişebiliyor, telefonlar sessizce düşerdi.
- Ağ üzerinden bağlı yönetici kapatırsa kendi bağlantısını da keser: ekran
  bunu yazıyor ve onay istiyor. Açmak ancak programın bilgisayarından.
- Yönetim panelinde düğmenin yazısı durumu söylüyor ("Ağ erişimi: yalnızca bu
  bilgisayar"); Telefona ekle sayfası ağ kapalıyken uyarıyor; açılış günlüğü
  kapalıyken personel adresi yerine `http://localhost:8000` yazıyor.

## Cryo haritası klasörü

Program Excel haritasını (v6.191) hep veri klasörüne yazıyordu; klasör
seçilemiyordu. Artık Klasörler ekranında dördüncü satır: "Cryo haritası
(Excel)" (`cryo_harita_klasor`, makineye özel; varsayılanı yine veri
klasöründe `cryo_harita/`).

- Arşiv gibi: program yazıyor, yoksa oluşturuluyor; oluşturulamayan yol
  reddediliyor.
- Yedek gibi: açılışta klasör yoksa (takılı olmayan disk) varsayılana
  dönülmüyor. Harita kartı "yazılamadı" diyor, disk gelince yazım sürüyor.
  Arşivin "yoksa varsayılana dön" kuralı burada seçilmedi: kullanıcının
  seçtiği yer sessizce kaybolurdu.
- Klasör değişince dosya **en geç bir dakika içinde** yeni yere yazılıyor.
  Yazıcı döngü yalnızca veri değişince kuruyordu; artık dosya hedef klasörde
  yoksa da kuruyor. Eski klasördeki dosyalar silinmiyor.
- Cryo Haritası kartı (yönetici) klasörü ve Klasörler'e bağlantıyı gösteriyor.

Başka bilgisayarda program o bilgisayarın ayarını kullanıyor; ayar yoksa veri
klasörü. Taşımaya gerek yok: harita veritabanından yeniden yazılıyor.

## Yeni bilgisayara geçiş

`KOMUTLAR.md`'de adım adım "Yeni bilgisayara geçiş" bölümü. `tasi.py`
sertifikayı yalnızca açıkça istenince taşıyor:
`python3 tasi.py disari <usb> sertifika`.

- **Günlük Mac ↔ klinik taşıması sertifikaya dokunmuyor.** İki bilgisayarın
  her birinin kendi sertifikası var (v6.196); birininki ötekinin üzerine
  yazılsaydı o bilgisayarın telefonları güvenli adrese giremezdi. Sertifikasız
  `disari`, USB'de önceki bir geçişten kalmış sertifikayı da siliyor.
- `iceri` USB'de sertifika bulursa alıyor ve **USB'deki kopyayı siliyor**:
  kök anahtarı ele geçen, kliniğin telefonlarına sahte bir sayfa
  gösterebilir. Bu makinenin kendi sertifikası varsa ve farklıysa "EVET"
  onayı istiyor, eskisini `sertifika_ONCEKI_<zaman>` diye saklıyor. "Hayır"
  denirse hiçbir şeye dokunmuyor.
- Boş makineye ilk `iceri` ağ erişimini kapalı yazıyor (yeni kurulum).
- Sunucu sertifikası yeni bilgisayarın adresine açılışta kendiliğinden
  yenileniyor (v6.196); telefonlarda yalnızca simge yeniden ekleniyor. IP de
  eskisiyle aynı verilirse (modemde DHCP rezervasyonu) telefonlarda hiçbir
  şey yapmak gerekmiyor.
- `iceri`'nin son satırı artık `python3 baslat.py` diyor (göçler açılışta
  kendiliğinden, v6.49).

## Denendi

Kullanıcının veritabanının bir kopyasında; uzaktaki cihaz, bu makinenin ağ
adresinin "başka cihaz" sayıldığı bir deneme sunucusuyla taklit edildi:

- Uzaktan kapatıldı: aynı cihazın sonraki istekleri (giriş, `/static`,
  `manifest.json`, `/sertifika`, `/degisim`, `/sw.js`) 403 aldı; bu
  bilgisayar her şeye girdi. Bu bilgisayardan açılınca uzaktaki cihaz hemen
  geri geldi; değişiklik günlüğe yazıldı.
- Cryo haritası klasörü değişince dosya birkaç saniye içinde yeni klasöre
  yazıldı (deneme sunucusunda döngü 5 saniye); oluşturulamayan yol reddedildi.
- `tasi.py` sahte verili bir veritabanıyla: boş makineye veritabanı, arşiv ve
  sertifika geldi, USB'deki sertifika silindi, ağ erişimi kapalı yazıldı.
  Kendi sertifikası olan makinede onay soruldu; "hayır"da hiçbir şey
  değişmedi, "EVET"te eskisi saklandı.

# v6.204 — Kurulum dosyası: ilk açılış ekranı, Windows kurulumu, Mac uygulaması

v6.203'teki planın 4. adımı; kullanıcının kararı "Windows ve Mac birlikte".
Yeni bir bilgisayara Python ve git kurmadan: Windows'ta tek bir kurulum
dosyası, Mac'te `.dmg` içinde uygulama. Nasıl yapıldığı `PAKETLEME.md`'de,
kullanıcının adımları `KOMUTLAR.md` → "Kurulum dosyası".

## İlk açılış ekranı (`/kurulum`)

Veritabanı yoksa program artık açılıyor; v6.50'den beri `baslat.py` "önce
kurulumu tamamlayın" deyip duruyordu, kurulum dosyasıyla kurulan programda
terminal yok. Bütün istekler `/kurulum`'a gidiyor, yalnızca o bilgisayardan
(başka cihaz "Program henüz kurulmadı" sayfasını görüyor). İki yol:

- **Eski bilgisayardan taşı**: USB'deki taşıma klasörü (`tasi.py disari <usb>
  sertifika`), eski programın klasörü ya da yedek klasörü. Klasörde bulunan
  veritabanları sayılarıyla ve son kayıtla listeleniyor, biri seçiliyor;
  fotoğraf arşivi ve sertifika isteğe bağlı. Aynı bilgisayarda git'le çalışan
  programdan kurulum dosyasına geçiş de bu yol (eski klasöre dokunulmuyor).
- **Yeni laboratuvar kur**: laboratuvarın adı ve ilk yönetici (şifre en az 8).

Kurallar:

- **Kurulum kipinde veritabanına hiç dokunulmuyor.** Middleware'in dil ayarı,
  oturum denetimi SQLite'a soruyor; `sqlite3.connect` olmayan dosyayı açınca
  boş bir `lab.db` oluşuyor ve program kendini "kurulmuş" sanırdı.
  `kurulum.html` bu yüzden `base.html`'i kullanmıyor (menü, tazeleme,
  kullanıcı alanı veritabanına soruyor).
- **Kurulum atomik**: geçici dosya (`lab.db.kurulum`) kuruluyor, bütünlüğü
  denetleniyor, tek hamlede yerine konuyor, sonra göçler. Sürerken gelen
  istekler "Kurulum sürüyor" sayfası (503, kendini tazeliyor).
- Taşımada veritabanı SQLite yedek API'siyle kopyalanıyor (düz kopya WAL'da
  boş dosya verebilir, v6.16); seçilen dosyanın adı klasörün listesine karşı
  doğrulanıyor (yol aşımı). Sertifika taşıma klasöründen alınınca USB'deki
  kopya siliniyor (v6.203), eski programın klasöründen alınınca kaynağa
  dokunulmuyor. Bu bilgisayarda eski bir sertifika varsa saklanıyor.
- Kurulan program ağa kapalı başlıyor (v6.203).
- **Şema, seçim listeleri ve varsayılan ayarlar tek yerde**:
  `kurulum.sema_kur()`; `sifirdan_kur.py` de onu çağırıyor.
- `aktar_access.py`'nin modül düzeyindeki "lab.db bulunamadı" çıkışı
  `main()`'e taşındı: program onu (`cryo_sablon` → `cryo_esle` üzerinden)
  import ediyor, veritabanı yokken program hiç açılmıyordu. Programın import
  ettiği bir modüle modül düzeyinde `sys.exit` yazma.

## Aynı bilgisayarda ikinci açılış

`GET /__pdc` (yalnızca 127.0.0.1'e, veritabanına dokunmadan): sürüm, derleme
kimliği, süreç, veri klasörü. `baslat.py` portu dolu bulunca soruyor:

- **Aynı kurulum** (aynı veri klasörü): "Program zaten çalışıyor", 0 ile
  çıkıyor; kurulum dosyasıyla kurulmuş programda tarayıcıyı açıyor. Git ile
  çalışırken de: ikinci `python3 baslat.py` artık uvicorn'un "address already
  in use" hatası yerine bunu söylüyor.
- **Başka kurulum ya da başka program**: söylüyor (paketlenmiş programda
  pencereyle), açılmıyor. İki kurulum aynı anda çalışamaz.
- **Mac'te farklı derleme**: yenilenmiş uygulama eskisini SIGTERM ile
  kapatıp yerine geçiyor (aşağıda).

Kurulum dosyasıyla kurulan program çift tıklamayla açılınca sunucu hazır
olunca tarayıcıyı açıyor. `--servis` (Windows'ta Görev Zamanlayıcı, Mac'te
oturum açılışı) ve `LAB_SESSIZ=1` (denemeler) iken tarayıcı ve pencere yok:
SYSTEM'in görünmeyen masaüstünde bir pencere programı sonsuza dek bekletirdi.

Pencereli pakette `sys.stdout` yok: uvicorn'un günlük biçimi `isatty()`
sorup çöküyordu. Boş bir akışa bağlanıyor; uvicorn'un iletileri (açılamayan
kapı, 500'ün ayrıntısı) `program.log`'a düşüyor, her isteğin satırı değil.
Git ile çalışırken terminal eskisi gibi.

## Windows kurulum dosyası

`paket/pdc_kurulum.iss` (Inno Setup; v6.50'nin hiç denenmemiş taslağı
baştan yazıldı):

- Program `C:\Program Files\Patient Data Center`, veri
  `C:\ProgramData\PatientDataCenter`. Kaldırınca veri kalıyor.
- **Açılışta başlatma: Görev Zamanlayıcı, PowerShell'le** (`paket/gorev.ps1`).
  v6.50'nin taslağı `schtasks /Create` kullanıyordu; o görev "3 günden uzun
  sürerse durdur" ayarıyla geliyor, sunucu üç günde bir kapanırdı. Süre sınırı
  yok, SYSTEM, kimse oturum açmadan, öncelik normal (varsayılan "normalin
  altı"), `--servis`.
- Güvenlik duvarı: 8000 ve 8443 (v6.196'nın güvenli kapısı; taslakta yoktu),
  yalnızca yerel ağ, tek kural.
- **Güncelleme**: yeni kurulum dosyası çalışan programı durduruyor, PyInstaller
  klasörünü baştan yazıyor, görevi ve kuralı yeniden kurup başlatıyor.
- Kısayollar tarayıcıda açıyor (program zaten arka planda); kurulum bitince
  tarayıcı program cevap verince açılıyor.

## Mac uygulaması

- `Patient Data Center.app`, DMG'de (Uygulamalar kısayolu + `Kurulum.txt`).
  Dock'ta simge yok: arka planda çalışan sunucu, ekranı tarayıcıda;
  uygulamaya çift tıklamak tarayıcıyı açıyor.
- **Oturum açılışında başlama**: Uygulamalar klasöründen açılınca
  `~/Library/LaunchAgents/com.patientdatacenter.pdc.plist`. DMG'den ya da
  İndirilenler'den açılırsa yazılmıyor: macOS oradan açılan uygulamayı geçici
  bir kopyadan çalıştırıyor, yol sonra kaybolurdu.
- **Güncelleme**: yeni uygulamayı Uygulamalar'a sürükle, çift tıkla: eski
  derleme kapanıyor, yenisi açılıyor. Uygulama değiştirilince eski süreç
  dosyaları altından değişmiş halde çalışmaya devam ediyordu (eski kod, yeni
  şablonlar -- tuzak #5'in paketteki hali). Ölçü derlemenin kimliği
  (`paket_bilgisi.json`), sürüm numarası değil: aynı sürümün yeniden derlemesi
  de yerine geçmeli.
- Ad-hoc imzalı (Apple hesabı yok): ilk açılışta macOS 15'te Sistem Ayarları
  → Gizlilik ve Güvenlik → "Yine de Aç". Apple Silicon ve Intel ayrı dosya.

## Derleme GitHub'da, her seferinde deneniyor

`.github/workflows/paket.yml`, elle çalıştırılıyor (Actions → Paketler → Run
workflow). Depo özel ve Mac dakikası 10 kat sayılıyor: her gönderimde değil,
istenince; makineler seçilebiliyor, Intel Mac varsayılan kapalı. Her makinede
program derlenip `paket/dene.py` ile deneniyor (ilk kurulum, 23 ekran, hasta,
tedavi, resmî formlar, Excel, HTTPS, ikinci açılış, günlük); Windows'ta
kurulum dosyası sessizce kurulup güncellenip kaldırılıyor, Mac'te yenilenmiş
uygulamanın yerine geçmesi, LaunchAgent ve DMG deneniyor.

Tarifte (`paket/pdc.spec`): `README.md` pakete giriyor (sürüm kartı),
`paket_bilgisi.json` (derleme kimliği; Yönetici panelinde "Kurulum dosyası"
satırı), simgeler telefon simgesinden (Mac'e köşeleri yuvarlatılmış),
program pencereli.

## Denendi

- Linux'ta paket derlendi ve `dene.py`'den geçti: ilk kurulum ekranı, 53 göç,
  23 ekran, hasta ve tedavi, iki resmî form, altı Excel çıktısı, HTTPS; ikinci
  açılış tanındı; SIGTERM ile düzgün kapandı; günlükte hata yok. Eski
  derlemeyi kapatma (3 sn) ve LaunchAgent yazma (yalnızca Uygulamalar'dan)
  ayrıca denendi.
- Git ile çalışırken: aynı veri klasörüyle ikinci `baslat.py` "zaten
  çalışıyor" deyip 0 ile, başka veri klasörüyle açıklamasıyla 3 ile çıktı;
  `/__pdc` ağdan gelen isteğe cevap vermedi.
- Kurulum ekranı ilk kurulum ve taşıma (USB taşıma klasörü ve eski programın
  klasörü) için sahte veriyle denendi: sayılar kaynakla birebir, geçici dosya
  kalmadı, yol aşımı reddedildi, telefonda ve masaüstünde taşma yok.
- **Windows** (GitHub'ın `windows-latest` makinesi): paket kurulmadan
  duman testinden geçti. Kurulum dosyası (16 MB) sessizce kuruldu: program
  Görev Zamanlayıcı'yla `NT AUTHORITY\SYSTEM` olarak açıldı, veri
  `C:\ProgramData\PatientDataCenter`, görevin süre sınırı yok (`PT0S`),
  tetik açılış, öncelik 4, güvenlik duvarında 8000,8443 yalnızca yerel alt ağ;
  aynı deneme (ilk kurulum, 23 ekran, formlar, Excel, HTTPS) geçti. İkinci
  kurulum (güncelleme) programı yeniden başlattı, veritabanı korundu, tek
  kural kaldı. Kaldırma: program, görev ve kural gitti, `lab.db` yerinde.
  İlk çalışmada yalnızca iş akışının kendi denetimi yanlıştı (`<BootTrigger />`).
- **Mac** (Apple Silicon, `macos-latest`): imza geçerli, duman testi geçti,
  yenilenmiş uygulama eski derlemeyi kapatıp yerine geçti, Uygulamalar'dan
  açılan uygulama LaunchAgent'ı yazdı, DMG doğrulanıp açıldı.
- **Bulunan: Mac'te açılış 70 saniye takılıyordu.** Uygulamalar'a kopyalanan
  uygulama (ve yerine geçme denemesindeki kopya) açılırken
  `sertifika.yerel_ipler()`'in makine adını çözmesi (`gethostbyname_ex`)
  70 sn sürdü; program o arada hiç cevap vermedi. Aynı çağrı ilk derlemede
  anında dönmüştü: sebep macOS'un "yerel ağ" izni ya da makinenin adını
  bilmeyen ad sunucusu olabilir, gerçek bir Mac'te de olabilir. Çözüm en çok
  2 sn bekliyor (`_adin_adresleri()`), dönmezse o ek adresler atlanıyor --
  asıl adres UDP yolundan geliyor. `dene.py` artık açılış süresini ölçüyor,
  45 sn'yi aşarsa başarısız sayıyor.
- **Son derleme** (commit 7c5b286, üç makine birden): Windows yine baştan
  sona geçti; Mac'te takılma gitti -- makine adı 2 sn'de bırakıldı, ilk
  açılış 2,3 sn, yenisinin yerine geçmesi 3,3 sn, Uygulamalar'dan açılış
  4,5 sn (önce 70 sn). **Intel Mac** (`macos-15-intel`) de aynı denemelerden
  geçti; yükleme adımı bir kez GitHub'ın dosya servisinin zaman aşımına düştü
  (kodla ilgisiz), yeniden çalıştırınca yüklendi. Dosyalar: Windows 16,2 MB,
  Mac Apple Silicon 18,4 MB, Mac Intel 19,4 MB.
- **Gerçek bir bilgisayarda ilk kurulum henüz yapılmadı.**

# v6.205 — Cryo Haritası'nda Taşınma bölümü: embriyo, yumurta ve sperm başka merkeze

Kullanıcının isteği (2026-09-28): "Bazı hastalar embriyo, yumurta ve
spermlerini başka üniteye taşıyor. Bu işlem sonrası cryo haritadan örnekler
siliniyor. Bunun için cryo harita bölümünde taşınma diye bir bölüm olsun.
Embriyosu ve yumurtası taşınan hastanın örneği cryo haritadan silinsin. Bu
hastaların hasta kartında tedaviler bölümünde taşıma yapıldığı belirtilsin."

v6.182'den beri tek bir tüp, kendi sayfasından "başka merkeze taşındı"
işaretlenebiliyordu (`tasiyici.durum='gonderildi'`, gün / yer / not). Eksik
olan üç şeydi: hastanın bütün örneklerini tek seferde işaretlemek, sperm
tüpü (işaret yalnızca embriyo tüpünün sayfasındaydı) ve hasta kartında
tedavinin satırı. Yeni tablo ya da göç yok: tüpün v6.182 alanları yetiyor.

**"Haritadan silinsin" = haritadan ÇIKAR, kayıt silinmez.** Programın kuralı
(silme = işaretleme) ve v6.182'nin kararı: tüp 'gonderildi' olur; Cryo
Haritası, kanister sayfası, boş yer önerisi, iki Excel dosyası (programın
düzeni ve laboratuvarın kendi Cryo Excel'i) ve formların "Kalan dondurulmuş"u
yalnızca dolu tüpü saydığı için örnek hepsinden kalkıyor, goblet yuvası
boşalıyor. Kayıt hasta kartında, Taşınma bölümünde ve resmî formun
"Taşınan:" satırında duruyor; geri alınabiliyor.

**Taşınma bölümü (`/cryo/tasima`)** -- Cryo Haritası'nın en üstünde tek
satır ("Taşınma · Başka üniteye taşınan embriyo, yumurta ve sperm · 4 tüp
taşındı · son taşıma ..."). İki kart:
- **Taşıma kaydet**: dosya no, hasta ya da eş adıyla arama (ad `tr_buyuk()`,
  v6.116); yalnızca tankta ya da taşınmış örneği olan hastalar, sayılarıyla.
  Programda tüpü olmayan Excel kayıtları da bulunuyor (Cryo Haritası'nın
  araması, v6.189).
- **Taşınanlar**: aynı hastanın aynı gün aynı yere giden tüpleri bir satır,
  en yeni üstte ("3 embriyo (2 tüp) · 5 yumurta (1 tüp) · 1 sperm tüpü ·
  Memorial Hastanesi'ne"). Türetilmiş (`app.tasinanlar()`), ayrı bir "taşıma"
  kaydı yok.

**Hastanın taşıma ekranı (`/cryo/tasima/hasta/{id}`)** -- kimlik bandı üstte.
- Tanktaki tüpler tedavi tedavi (hasta kartının sırası: son tedavi üstte),
  sonra sperm; satır Cryo Haritası'nın goblet satırıyla aynı
  (`yerlesim.tup_ayrintilari()`: etiket, renk, tip, "D5 (3AB-4BB)", yumurtada
  "(5*MII)", dondurma günü, konum). **Hepsi işaretli gelir** -- hasta çoğu
  zaman bütün örneklerini taşıtıyor; kalanın işareti kaldırılır. Tek bir
  tüpün sayfasından gelindiyse (`?sec=<tüp>`, sperm sayfası) yalnızca o.
- Gün (varsayılan bugün), nereye (daha önce yazılan yerler öneri olarak,
  `<datalist>`: listede olmayan merkez de yazılır), not; tarayıcı onayı.
  Yer kullanıcının yazdığı gibi, ekiyle (v6.182: program Türkçe ek
  uydurmuyor).
- **Hepsi ya da hiçbiri**: seçilenlerden biri bu arada tanktan çıktıysa
  (çözüldü, başka ekrandan taşındı) hiçbir şey yazılmaz, ekran güncel haliyle
  açılır. Gün zorunlu, bugünden sonra ve seçilenlerin hiçbirinin
  dondurulmasından önce olamaz (`_gonderim_gunu()`, tek tüpün formuyla aynı
  denetim). Hata anahtarları beyaz listeden (`TASIMA_HATALARI`, tuzak #9).
- Her tüp değişiklik geçmişine yazılıyor (`_gonderildi_yaz()`, tek tüpün
  formu da artık bundan geçiyor): açık ekranlar tazeleniyor, Excel haritası
  bir dakika içinde yeniden yazılıyor (ikisi de günlüğün damgasına bakıyor).
- **Taşınanlar** taşıma başına ("03.02.2026 tarihinde Memorial Hastanesi'ne
  taşındı."), altında "Bu taşımayı geri al" (`/cryo/tasima/hasta/{id}/geri`:
  `geri-al` adı "silme" modülüne düşerdi).
- **Adı bu hastaya benzeyen Excel kayıtları** -- Cryo Excel'inde duran,
  programda tüpü bulunamamış satırlar (v6.189). Hastaya BAĞLI DEĞİLLER: ölçü
  `cryo_esle`'nin hasta ölçüsü (SOYAD + AD kelime kümesi = ad soyad), ama ad
  tek başına kanıt değil (v6.125), o yüzden **işaretsiz** geliyor; tarihe,
  içeriğe, eşin adına bakıp kullanıcı seçiyor. İşaretlenen kayıt v6.189'un
  "tanktan çıkarıldı"sı oluyor, notu "... tarihinde ... taşındı." Bunların
  geri alınması kendi sayfasından ("Tanka geri koy"): "Bu taşımayı geri al"
  yalnızca programın tüplerini geri koyuyor -- hangi Excel kaydının hangi
  taşımaya ait olduğunu program ad benzerliğinden çıkaramaz.
- Eşin ayrı dosyası (v6.139 `es_dosya_no`, iki yönde): o dosyada tankta ya da
  taşınmış örnek varsa bağlantı -- çiftin taşıması çoğu zaman birlikte, sperm
  erkeğin kendi numarasında olabiliyor.

**Sperm** -- şimdiye kadar taşınamıyordu. Taşınan sperm tüpü Cryo
Haritası'nın sperm listesinden ve aramasından çıkıyor (ağaçta zaten yalnızca
dolu tüp vardı), androloji ekranının "bağlanacak sperm" listesine ve hasta
kartının "bağlanmayı bekleyen" uyarısına girmiyor, tedaviye bağlanamıyor
(`sperm_tedaviye_bagla()`: bağlansaydı `durum` 'kullanildi' olup taşındığı
bilgisi silinirdi). Sperm sayfasında "Başka merkeze taşındı" kartı ve geri
alma; dolu tüpte "Başka merkeze taşındı olarak işaretle" bu hastanın taşıma
ekranına, yalnızca o tüp işaretli. Kullanılmış tüp taşınmaz.

**Hasta kartı** -- tedavi satırında "Taşındı" rozeti ve taşıma başına bir
satır: "**3 embriyo**, 2 tüp (3AB-4BB) (8HG1) — 03.02.2026 tarihinde
Memorial Hastanesi'ne taşındı." Tüp **dondurulduğu tedavinin** satırında
(`db.vit_tedavisi()`: FET'te yeniden dondurulan tüp FET'in satırında), içerik
resmî formun "Taşınan:" satırının kaynağından (`formlar.tasinan_tupler()` +
`tup_metni()`) -- kart ile form aynı şeyi yazsın. Sperm satırında "Taşındı ...
tarihinde ... taşındı." ve bağlama formu yok. v6.182'nin ayrı "Başka merkeze
taşınan tüpler" kartı kaldırıldı (içeriği artık tedavinin satırında); yerinde
"Başka merkeze taşıma" düğmesi (tankta ya da taşınmış tüpü olan hastada)
Taşınma ekranına gidiyor.

Denendi (sahte veri: iki embriyo tüpü, bir yumurta tüpü, çiftin ve eşin ayrı
dosyasının sperm tüpleri, bir Excel kaydı, küçük bir tank düzeni): seçimsiz /
ileri / dondurmadan önceki / geçersiz tüp hiçbir şey yazmadı; toplu taşıma,
Cryo Haritası'nın ağacı ve kanister sayfası (yuvalar boşaldı), Excel haritası
(taşınanlar yok, kalanlar var), resmî formun "Taşınan:" satırı, hasta kartı,
sperm bağlama engeli, sperm sayfasından ve taşımadan geri alma (tüpler ve
konumlar geri döndü); telefon (390px) ve masaüstünde yatay kayma yok. Gerçek
veri kopyasında (1.823 hasta) tek harfle arama 0,3 sn, hastanın ekranının
sorguları 0,01 sn.

# v6.206 — Beklenmeyen hatada açıklayıcı sayfa; ayrıntısı program.log'a

Kullanıcı bildirdi (2026-09-28): "Embriyoloji özet formu, Art lab formu
bastırmak isteyince Internal Server Error hatası veriyor."

**Burada tekrarlanamadı.** Gerçek veri kopyalarında iki formun ekranı açıldı:
b202'de 1.909 tedavinin 3.818 formu, 2024–2026 kopyasında 1.816 tedavinin
formları ve Excel'leri. v6.205'in Taşınma bölümüyle 26 hastanın tüpleri
(sperm dahil) taşınınca da o hastaların 74 tedavisinin formları ve Excel'leri
açıldı. v6.205 formların koduna yalnızca iki alan ekledi (tüpün etiketi ve
dondurulduğu tedavi); ikisini yalnızca hasta kartı okuyor. Form şablonu
v6.158'den, `base.html` v6.195'ten beri değişmedi. Yani "yeni şablon + eski
kod" (tuzak #5) da bu hatayı açıklamıyor. Sebep büyük olasılıkla kullanıcının
veritabanındaki, deneme kopyalarında olmayan bir kayıt (2018 ayları, v6.205'ten
sonra girilenler).

**Sebep hiçbir yerden okunamıyordu.** Tarayıcı yalnızca "Internal Server
Error" gösteriyordu. Kaynaktan çalışırken (`python3 baslat.py`) uvicorn'un
kendi günlükçüsü hatayı yalnızca terminale yazıyor (köke iletmiyor), yani
`program.log`'a düşmüyordu.

**Artık** yakalanmamış her hatada (`app.beklenmeyen_hata()`,
`@exception_handler(Exception)`):
- Ekranda Türkçe bir sayfa çıkıyor ("Beklenmeyen bir hata oluştu"). Kutuda
  hatanın türü ve programdaki yeri (`TypeError · formlar.py:1123
  (ozet_verisi)`), adres, çalışan sürüm ve saat yazıyor. Bir ekran görüntüsü
  sebebi bulmaya yetiyor.
- Hatanın **iletisi ekrana basılmıyor**; bir değer ya da ad içerebilir. İleti
  `program.log`'a traceback'le birlikte yazılıyor ("Beklenmeyen hata: GET
  /form/ozet/… -- …").
- Yer, programın kendi dosyasındaki son çerçeve (`_hata_yeri()`: proje
  klasöründeki `.py`, pakette dizinsiz ad, şablonlar). Son çerçeve çoğu zaman
  sqlite3 ya da jinja2'nin içinde oluyor.
- Starlette yanıtı gönderdikten sonra hatayı yeniden fırlatıyor, yani terminal
  de görmeye devam ediyor. İşlev veritabanına dokunmuyor (metinler bağlam
  değişkeninden okunuyor) ve kendisi patlarsa düz yanıta düşüyor.
- Sayfa `_duz_sayfa()`'dan geliyor (ağ kapalı ve kurulum sayfalarının
  yardımcısı): `ayrinti` kaçışlı bir `<pre>`, `baglantilar` koddan gelen
  "Geri dön · Ana ekran".

Denendi: bilerek hata veren geçici bir rotada sayfa `TypeError · formlar.py:535
(tup_metni)` yazdı, `program.log`'a satır ve traceback düştü. Formun asıl
sebebi kullanıcının ekran görüntüsü ya da `program.log` satırı gelince
düzeltilecek.

# v6.207 — Eylül 2026 Access kayıtları: programda olan atlanıyor, Cryo Haritası'ndaki Excel kaydı tüpüne bağlanıyor

Kullanıcının isteği (2026-09-28): "Eylül 2026 hasta kayıtları. Programa kayıt
yapılmış hastalar var. Programa kayıt yapılmadan cryo harita kaydı olan hasta
var. Bunları analiz edip programa hastaları kaydet. Kaydı yapılmış cryo
haritaya da kaydedilmiş hastayı kaydetmene gerek yok."

Eylül dosyasında 48 kayıt var (27 OPU'lu, 20 FET, bir yumurta çözme). İki şey
şimdiye kadarki aylardan farklı: bazı hastalar bu ay programın ekranlarından
da girildi, ve Cryo Excel'inde duran eylül straw'ları programda hastası
olmadığı için Cryo Haritası'nda "Excel kaydı" olarak (v6.189) duruyor.
Kullanıcının veritabanı burada yok (deneme kopyası 2026-09-20'ye kadarki
Access aylarından kurulu, ekrandan girilmiş gerçek tedavi yok); o yüzden
ayrım aracın içinde, kullanıcının makinesinde yapılıyor ve `liste` hepsini
yazmadan gösteriyor.

**Programa ekrandan girilmiş tedavi atlanıyor** (`aktar_access.
programdaki_tedavi()`). İşaret (`[Access kaydı EYLUL#12]`) aynı satırın
ikinci aktarımını tanıyor, ekranda girileni tanımıyordu: aynı tedavi ikinci
kez açılır, tankta olmayan ikinci bir tüp takımı yazılırdı. Ölçü:
- **Aynı hasta** (dosya numarası -- eşleştirmenin tek anahtarı, v6.125),
  **aynı tür** (yumurta toplanan: IVF/ICSI, Yumurta Dondurma; çözme: FET, FET
  3→5, Yumurta Çözme -- ekranda türü farklı seçilmiş aynı tedavi yine aynı),
  günleri **en çok 30 gün** farklı, protokol notunda ne Access ne Cryo Excel
  işareti olan tedavi. Pencere geniş: ekranda açılıp OPU'su girilmemiş
  tedavinin günü planlanan tarih ya da açıldığı an (`db.tedavi_tarihi()`);
  aynı türden iki tedavi bir ay içinde neredeyse hiç olmuyor.
- Silme ekranından iptal edilen tedavi (bitiş sebebi yok) sayılmıyor, "İptal"
  diye bitirilen sayılıyor.
- **Aynı gün başka bir Access dosyasından aktarılmış** tedavi de (ayın sonu
  bir sonraki ayın dosyasına girilmiş olabilir, 2025'te oldu).
- **Dosya numarası programda yok ama aynı adlı hastanın** aynı dönemde ekrandan
  girilmiş tedavisi var: numara farklı yazılmış olabilir. Ad tek başına hiçbir
  şeye bağlamıyor, yalnızca durduruyor; satır o hastanın dosya numarasını
  yazıyor.
- `liste` satırı: "PROGRAMDA VAR — atlanır: ... tedavi 2026-0xxx (ivf_icsi,
  07.09.2026, 19 yumurta, 3 tüp (3'ü Cryo Haritası'nda)) -- Access: 19
  yumurta, 3 tüp". Programdaki eksik girilmişse görünsün diye iki taraf yan
  yana; eksik ekrandan tamamlanır. Aynı tedavi değilse düzeltme dosyasına
  `EYLUL#12  AKTAR` (yeni satır türü): o kayıt yine aktarılır. Aktarımın
  sonunda da liste olarak basılıyor.
- Önizleme ile aktarım aynı kararı kullanıyor (`programdakileri_isaretle()`,
  yazmadan önce bir kez). `liste`'nin "N tedavi yazılacak" satırı atlananları
  saymıyor (`aktar_toplu.py` o satırı okuyor).

**Cryo Haritası'ndaki Excel kaydı tüpüne bağlanıyor** (`cryo_esle.
excel_kayitlarini_bagla()`, aktarımın sonunda `aktar_access.
cryo_haritasina_bagla()`). Hastası programda yokken `yerlesim` straw'ı
gobletde Excel kaydı olarak açmıştı; aktarım tüpü **konumsuz** açıyor
(Access'te konum yok) ve straw iki kez görünürdü: gobletde Excel kaydı, "yeri
belirsiz"de tüp. Artık:
- Ölçü `cryo_esle.py uygula`'nınki (`esle()`: ad kelime kümesi + gün +
  içerik); Excel dosyası gerekmiyor, satırın yazısı Excel kaydında
  (`excel_kaydi_satirlari()`).
- Yazım Excel kaydının sayfasındaki "tüpe bağla" ile aynı: ikisi de
  `yerlesim.excel_kaydini_bagla()` (v6.189'un route'u oraya taşındı). Tüp
  gobletin konumunu alıyor, rengi/tipi boşsa Excel'inki; Excel kaydı
  'baglandi'. Bağ o sayfadan çözülüyor. Aktarımın açtığı tüpün tipi
  ("cryotop" varsayılan, kaynakta yok) Excel'in VİAL'iyle değişiyor --
  `uygula` da öyle yazıyor; ekranda girilen tüpün tipine dokunulmuyor.
- **Yalnızca konumu boş, bir Excel kaydına bağlı olmayan tüp aday.** Konumu
  olan tüp bir straw'ı zaten anlatıyor. Aynı gobletde aynı içerikli bir Excel
  kaydı İKİ ayrı straw olabilir (Excel iki satır, programda bir tüp: deneme
  kopyasında böyle beş goblet var) ya da ekranda sonradan girilmiş aynı straw;
  içerik ayırmıyor. Kendiliğinden bağlamak bir straw'ı haritadan
  düşürebilirdi: listeleniyor ("aynı gobletde aynı içerikli tüp: ..."),
  kararı kullanıcı sayfasında veriyor. İlk denemede bağlanıyordu; kopyadaki
  o beş goblet görülünce geri alındı.
- Aktarımda yalnızca bu dosyanın hastalarının, satırların günlerindeki
  (tedavinin gününden bir gün önce, yedi gün sonrasına kadar) Excel kayıtları
  -- hastanın başka yıllardan kalan kayıtları bu işin konusu değil.
- **Programdaki ad Access'teki addan farklıysa** (kart daha önce başka yazımla
  açılmış: ikinci ad, harf farkı) Excel'deki ad Access'inkiyle tutuyor olabilir.
  Access satırı hastaya dosya numarasıyla bağlı, o yüzden eşleştirme o adı da
  kullanıyor (`_ad_dizini()`'nin `ek_adlar`'ı): zincir kesin.
- Bağlanamayanlar sayfa adresiyle ve sebebiyle basılıyor; aynı gün aynı
  içerikli ama adı hiçbir hastayla tutmayan Excel kaydı "adı farklı yazılmış
  olabilir" diye (`ad_farkli_excel_kayitlari()`, `eksik` kipinin ölçüsü) --
  bağlanmıyor, gösteriliyor.
- `liste` her satırın altında hastanın Excel kaydı straw'larını yazıyor
  ("Cryo Haritası'nda Excel kaydı olarak 3 straw: TANK 5 / 1 / 28 Üst: D5
  (4AA); ..."): hangi hastanın haritada programdan önce durduğu buradan
  okunuyor.
- Sonradan (ekrandan girilen tüpler, düzeltilen bir ad): `python3 cryo_esle.py
  excel_bagla` -- dosyasız, bütün Excel kayıtları, "BAGLA" onayıyla, satır
  satır rapor `cryo_esle_rapor_excel_bagla.txt`'ye.

**İki okuma düzeltmesi** (eski/yeni okuma satır satır karşılaştırıldı):
- Access notunda "DONDURULARAK **AKLANDI**" (S düşmüş, #32, bir yumurta):
  dondurma okunmuyordu, tüp yazılmayacaktı. Okunan 23 dosyanın 1.858
  satırında başka bir satırın okuması değişmedi.
- Aynı satırda MII ve İMMATÜR kutuları boş, TOPLANAN 1, not "(1*M2)": not
  kazanır kuralı (v6.161) yalnızca immatürden MII'ye geçiriyordu; kutuya hiç
  sayılmamış yumurtada da artık notun olgunluğu yazılıyor
  (`olgunlugu_nottan_duzelt()`), not "Access'te MII 0 ... yazıyordu" diyor.
  Aynı 1.858 satırda yalnızca bu satır değişti.
- Cryo Excel'inde parantez içinde sayı ile olgunluk arasında boşluk ("OOSİT
  (1 M2)", "(4 M2)", "(1 MII 2MI)"): sayı ayrı öğe okunuyor, tüp tutmuyordu
  (`cryo_esle._ADET_OLGUNLUK`). 5.392 satırlık Excel'de yalnızca bu üç satırın
  okuması değişti; üçü de doğruya. Laboratuvarın kendi Excel çıktısı
  (v6.199) bu satırları artık tanıyor: tüpü tankta ve gobletindeyse satır
  aynen, tüpü yoksa Excel kaydıyla yine aynen kalıyor.

**Eylül dosyasının kendisi** (deneme kopyasında, adlar ve numaralar yok):
- #19 ve #22 aynı hastanın aynı günkü iki farklı kaydı (v6.167'nin ikizi):
  ikisi de atlanıyor, kullanıcı doğru olmayanı `ATLA` ile söyleyecek. Farklar:
  protokol yazımı, immatür/dejenere, bazal volüm, hazırlık sonrası değerler,
  fertilizasyon yöntemi yazımı, not; hasta adının yazımı da farklı.
- #8 (yumurta çözme) tarihsiz: bir önceki kaydın günü yazılıyor, not
  "yaklaşık" diyor.
- #35'in altı straw'ı Excel'de 14.09.2026 "D5", Access'te OPU 08.09.2026 + 5.
  gün = 13.09.2026 ve 5×4AA + 1×4BA (Excel 6×4AA): bağlanmıyor (serbest ±N gün
  toleransı yok, v6.177), elle.
- #11, #20, #29, #37'nin birer-ikişer straw'ının içeriği Excel ile Access
  arasında farklı (tüp dağılımı ya da sayı); #5'in straw'ı Excel'de adı farklı
  yazılmış (aynı gün aynı içerik): hepsi aktarımın sonunda sayfalarıyla
  listeleniyor.
- Deneme kopyasında: 46 tedavi aktarıldı, 32 Excel kaydı tüpüne bağlandı, 12
  tüpün konumu boş kaldı (yukarıdakiler), 0 hata. Gobletlerin doluluğu
  aktarımdan önce ve sonra aynı (bağlanan straw Excel kaydından tüpe geçti),
  tek fark bir FET'in çözdüğü tüpün boşalması. Aktarılan 46 tedavinin tedavi
  ekranı, iki resmî formu, hasta kartları, Cryo Haritası sayfaları (199
  sayfa) hatasız açıldı. Senaryo kopyasında (ekrandan girilmiş IVF, planlı
  FET, başka dosya numarasıyla aynı ad, başka etiketli aktarım, başka türde
  tedavi, silinmiş ve iptalle bitmiş tedavi, `AKTAR`) her biri beklenen
  kararı verdi. Excel kaydı sayfasının "tüpe bağla / bağı çöz"u ortak işlevle
  denendi: konum, renk, günlük ve geri alma aynı.

# v6.208 — ART Lab'da Cryo yeri ve Deselect, İşlemi yapan üstte, arama sonucu kutunun altında, FET çözme akışı, GV yumurta, denüdasyonda kayma

Kullanıcının tek mesajdaki sekiz isteği. Her birinin sebebi aşağıda.

**ART Lab: dondurulan tüplerin Cryo Haritası'ndaki yeri** (kullanıcı:
"dondurma yapılan hastanın dondurulan örneğin cryo haritada nereye
yerleştirildiği art lab özet formunun orta alt kısmına yazılsın. Embriyo,
yumurta bilgisi ile birlikte").
- Yer: kâğıtta ÖZET tablosunun hemen altındaki boş ara satır (0'dan sayarak
  32; kalıpta hücresi yok). Tam genişlikte, ortalı, 10 punto, FREEZE
  kutularının hemen altında. "Orta alt kısım" ÖZET'in altı diye okundu.
  İptal notu (v6.104) kalıbın DIŞINA, en alta yazılıyor; bu yazı ise kalıbın
  içinde. Başka bir yer istenirse `formlar.ARTLAB_CRYO_SATIR`.
- İçerik tüp başına: "TANK 1 / 3 / 12 · Mavi Cryotop: 1 embriyo (4AA)".
  Tüpler ";" ile ayrılıyor, uzun olunca satır satır bölünüyor (115 harf, bir
  tüp ortasından bölünmüyor). Yer, tüpün kayıtlı konumu (Cryo Haritası'nın
  gösterdiği); girilmemişse "konum girilmemiş". İçerik FREEZE kutusunun
  parantezi (`tup_metni()`), tür tüpün içeriğinden. Sonradan çözülen ya da
  taşınan tüp işaretlenmiyor: form bu tedavinin dondurmasını anlatıyor,
  FREEZE kutuları gibi.
- Kalıp değişmiyor: hücre, `form_kalip.not_satiri()` / `not_satiri_excel()`
  ile çıktının kopyasına ekleniyor. Satırda kâğıdın bir hücresi varsa hiçbir
  şey yazılmıyor. Ekranda satır içerikle uzuyor; yazdırırken form yine tek A4'e
  sığıyor (`baskiyaSigdir`). Excel'de birleşik hücre sarmalı, yüksekliği satır
  sayısından. Yalnızca ilk sayfada.

**ART Lab: Deselect grade** (kullanıcı: "Çözülen ama transfer edilmeyen ve
tekrar dondurulmayan embriyo art lab deselect bölümüne yazılsın").
- `formlar._deselect_satirlari()`: bu tedavi için çözülen, bu tedavide
  transfer edilmeyen ve yeniden dondurulmayan embriyolar. Yumurta sayılmıyor
  (Yumurta Çözme'nin çözdüğü yumurta): kullanıcı "embriyo" dedi.
- Yazım "Uterus grade"inkiyle aynı: "7HG2 x1". Çözmede canlı çıkmayanın
  sağkalımı da yazılıyor ("4BB x1 · Dejenere").
- Dört kutu; dördü aşan kutular ikinci kâğıda geçiyor (FREEZE/THAW/TRANSFER'in
  kuralı, `_ARTLAB_DORT_KUTU`).
- Taşma: TRANSFER artık yalnızca yanındaki Deselect boşsa taşıyor; önce
  Deselect hep boştu, TRANSFER hep taşıyordu. Deselect'in sağında İŞLEM
  sütununun basılı yazıları var: taşmıyor, küçülüyor.

**İşlemi yapan üstte, ayrı "Kaydet" yok** (kullanıcı: "işlem yapan kaydı
yapılan ekranlarda karışıklık oluyor. Mesela OPU kaydı yapılıyor isim kaydı
ayrı yapılıyor. Bazı ekranlarda isim değişince kayıt yenileniyor. İşlemi
yapan kaydı üst tarafta olsun aşağıda değil").
- Sebep: kutu her ekranın en altında, kendi "Kaydet"i olan ayrı bir formdu.
  - Aşamanın kendi kaydı adı yazmıyordu.
  - Ekranda görünen varsayılan (giriş yapan kişi) kaydedilmeden kalıyor,
    formlara boş basılıyordu.
  - Değiştirilen ad, aşama kaydedilince eski haline dönüyordu.
  - Kutunun "Kaydet"i sayfayı yeniliyordu; aynı ekranda yazılıp henüz
    kaydedilmemiş form gidiyordu.
- Bugün kutu 11 aşama ekranında `{% block icerik %}`'in ilk satırı.
  - Seçmek yetiyor: ad sayfa yenilenmeden kaydediliyor ve kutu
    "Kaydedildi: X." yazıyor. Bunu `POST /cycle/{id}/islem-yapan` ile `json=1`
    yapıyor; cevap JSON, içinde tazelemenin yeni damgası var
    (`window.pdcDamgaGuncelle`, `base.html`). Damga güncellenmeseydi sayfa beş
    saniye sonra kendi kaydı yüzünden yenilenirdi. Betik çalışmazsa düğme
    görünüyor, eski yol işliyor.
  - Ad boşsa aşamanın kaydı giriş yapan kişiyi yazıyor
    (`app.islem_yapani_doldur()`, `INSERT OR IGNORE`). Kayıtlı ad ezilmiyor:
    başka bir telefondan seçilen adı bozmasın. Bunu 15 kayıt rotası çağırıyor:
    OPU, androloji, denüdasyon (üç yol), ICSI (+ genel bulgu), fertilizasyon,
    cleavage, blastokist, vitrifikasyon, çözme (tüp sayfasında; çözmenin
    tedavisine), transfer, gebelik (+ bebek).
- v6.99'un "Kaydet elle onay ister, otomatik yazmıyor" kararı bu sürümde
  değişti; sebep kullanıcının bildirdiği karışıklık.

**Arama sonucu kutunun hemen altında, aramadan dönüş** (kullanıcı:
"Programda arama yapılan her alanda arama sonucu aramanın hemen altında
görünsün aramadan geriye dönüş olsun").
- `/hastalar`:
  - Kutu sağ sütundaydı. Telefonda sütunlar alt alta dizilince sonuç ay
    listesinin (50 satıra kadar) altında kalıyordu; ana ekrandan aranan hasta
    sayfanın dibindeydi.
  - Artık kutu sütunların üstünde, sonuçlar (örnek kodu, etiket, hasta) hemen
    altında, ay listesi onların altında (v6.63'ün "ikisi birlikte" kararı
    duruyor).
  - Aramadayken Tüm Hastalar sütunu basılmıyor.
  - Geri ok aramadayken aramasız hale dönüyor, seçili ay korunuyor.
- `/cryo`:
  - Aramadayken Taşınma satırı ve Excel kartları basılmıyor; sonuçların
    arasına giriyorlardı, aramayı temizleyince geri geliyorlar.
  - "Aramayı temizle" eklendi, geri ok `/cryo`'ya dönüyor.
- `/cryo/tasima` ve dondurulmuş sperm bağlama: "Aramayı temizle" eklendi,
  geri ok aramasız hale dönüyor.
- Vitrifikasyonun etiket araması zaten böyleydi.

**Cleavage 3. günle açılıyor** (kullanıcı: "Clavage ekranını açınca ilk 3.
günü göstersin"). Rota adressiz açılınca zaten 3. günü seçiyordu; aşama
menüsünün bağlantısı `?gun=2` veriyordu (`ASAMA_SIRASI`).

**FET: çözmeden sonra çözme ekranına dönüş, transfere geçiş** (kullanıcı:
"Fet tedavilerinde çözme işlemi yapınca transfer sayfasına gidiş yok. Ayrıca
birden fazla embriyo çözülecekse biri çözüldükten sonra diğerine geri dönüş
yok").
- Sebep: çözme kaydı, yalnızca çözme formuna tedavinin ekranından gelindiyse
  (`geri_cycle`) oraya dönüyordu.
  - Tüpün "İçeriği gör" sayfasından "Bu taşıyıcıyı çöz"e basınca tedavi
    kayboluyordu; bağlantı `?cycle=` taşımıyordu.
  - Cryo Haritası'ndan gelinince de aynısı oluyordu.
  - İkisinde de kayıt tüp sayfasına düşüyordu. Orada aşama menüsü yok, geri ok
    `/cryo`'ya çıkıyor (v6.198'in vitrifikasyondaki dersi).
- Bugün kayıt, çözmenin yapıldığı tedavinin çözme ekranına dönüyor
  (`?kaydedildi=<tüp>`).
  - Üstte mesaj: "Kaydedildi: taşıyıcı X çözüldü, 1 embriyo (1 Canlı). Tankta
    N taşıyıcı daha var".
  - Mesajın altında sıradaki aşamanın düğmesi: "Transfer ekranına geç";
    FET (3→5)'te Blastokist.
  - Tankta kalan tüpler aşağıdaki listede.
  - Tüp sayfasının çözme bağlantısı `?cycle=`'yi taşıyor.

**Yumurta Dondurma'da GV yumurta dondurma adayı değil** (kullanıcı: "Yumurya
dondurmada gv çıkan yumurtaları dondurulacak yumurta olarak gösterme").
- `app._gv_yumurta()`: bu tedavideki son maturasyonu GV olan yumurta
  vitrifikasyon listesinde görünmüyor, sunucu da dondurmasını reddediyor
  (`_vit_adaylari()`: ekran ve kayıt aynı koşulu soruyor).
- GV yazılıp sonra MII'ye düzeltilen yumurta listede.
- Bu tedavide zaten dondurulmuş GV yumurta (Access'ten "(4*GV)") listede
  kalıyor.
- Yalnızca GV. MI, dejenere ve atretik yumurta değişmedi; kullanıcıya soruldu.

**Denüdasyonda sayfa kayması** (kullanıcı: "Denüdasyon ekranı işlem yaparken
sayfa kayıyor"). İki sebep vardı, ikisi de telefonda ölçüldü (resim 1,5 sn
gecikmeli).
- Birinci sebep: `.foto img` `height: auto` idi. Resim gelene kadar kutu
  sıfır yükseklikteydi; gelince "Kaydet / Atla" düğmeleri 267 px aşağı
  kayıyordu. Hızlı dokunan yanlış düğmeye basardı.
- İkinci sebep: her düğme sayfayı yeniliyor, yeni sayfa en üstten açılıyordu.
  Telefonda "Kaydet" ekranın dışında kalıyordu; her karede aşağı kaydırmak
  gerekiyordu.
- Düzeltme:
  - `.foto img` artık 4:3 bir kutu (`aspect-ratio`, `contain`), bütün aşama
    ekranlarında. Başka oranlı resim (dikey telefon fotoğrafı) bantlı
    görünüyor.
  - Denüdasyonda form gönderilirken kaydırma konumu sekmede saklanıyor
    (sessionStorage). Aynı ekrana bir dakika içinde dönülünce oraya
    kaydırılıyor; hata mesajı varsa kaydırılmıyor (mesaj en üstte).
- Sonuç: kayma 0 px; kayıttan sonra düğme ekranda.

**Deneme** (sahte veritabanında, gerçek hasta verisi yok):
- İki tüp donduruldu; İşlemi yapan ilk kayıtla yazıldı.
- Seçici sayfa yenilenmeden kaydetti; 6,5 sn sonra sayfa yenilenmedi, şerit
  çıkmadı.
- FET tüp sayfasından (tedavisiz) açıldı. İki tüp çözüldü: ikisi de FET'in
  çözme ekranına döndü, "İçeriği gör" üzerinden gelinince tedavi korundu.
  "Transfer ekranına geç" transfere götürdü.
- ART Lab'da çözülüp transfer edilmeyen embriyo Deselect'e "7HG2 x1" yazıldı.
  Dondurma tedavisinin formunda iki tüpün yeri ÖZET'in altında çıktı; Excel'de
  `A33:AC33` birleşik hücre, openpyxl açtı.
- GV yumurta listede yok, elle gönderimi reddedildi; dondurulmuş GV listede
  kaldı.
- Arama ekranları telefon ve masaüstünde sonucu kutunun altında gösterdi.
- 56 ekran (üç tedavi tipinin bütün aşamaları, formlar, listeler) hatasız ve
  yatay taşmasız açıldı.

# v6.209 — Yumurta Dondurma'da dejenere ve atretik yumurta da dondurma adayı değil

Kullanıcı (v6.208'deki soruya cevap): *"Dejenere ve atretik yumurtalar da
gizlensin"*.

- v6.208'de Yumurta Dondurma'nın vitrifikasyon listesinden yalnızca GV
  yumurta çıkmıştı. Artık dejenere ve atretik yumurta da çıkıyor.
- Olgunluklar tek yerde: `app.DONDURULMAYAN_OLGUNLUK` (`gv`, `degenere`,
  `atretik`, maturasyon listesinin kodları). `_gv_yumurta()`'nın adı
  `_dondurulmayan_yumurta()` oldu; kural aynı:
  - Ölçü yumurtanın bu tedavideki SON maturasyonu (denüdasyonda soruluyor).
    Dejenere yazılıp sonra MII'ye düzeltilen yumurta listede.
  - Ekran ve kayıt aynı koşulu soruyor (`_vit_adaylari()`): eski bir
    sekmeden gönderilen dondurma da reddediliyor.
  - Bu tedavide zaten dondurulmuş yumurta listede kalıyor.
  - Yalnızca yumurta donduran tipte (`db.yumurta_mi()`). IVF/ICSI'de
    enjekte edilmeyen yumurta zaten görünmüyordu (v6.105).
- **MI değişmedi**: MI yumurta listede. Kullanıcı yalnızca bu üçünü söyledi.

**Deneme** (sahte veritabanında): MII, GV, MI, dejenere ve atretik birer
yumurta. Listede yalnızca MII ve MI kaldı. GV, dejenere ve atretik yumurtanın
elle gönderilen dondurması reddedildi, kayıt ve tüp yazılmadı.

# v6.210 — Kayıttan sonra bütün aşama ekranları kaldığı yerde açılıyor

Kullanıcı (v6.208'deki soruya cevap): *"kaydırma konumunun başka aşama
ekranlarında da korunsun"*.

- v6.208'de yalnızca denüdasyon kayıttan sonra kaldığı yerde açılıyordu.
  Artık OPU, androloji, ICSI, fertilizasyon, cleavage, blastokist,
  vitrifikasyon, çözme, transfer ve gebelik de.
- Betik tek yerde: `templates/_kaydirma.html`. Her aşama ekranının son satırı
  `{% include "_kaydirma.html" %}`; denüdasyonun kendi kopyası kaldırıldı.
- Kurallar denüdasyondakiyle aynı:
  - "Kaydet"e basınca kaydırma konumu sekmede saklanıyor. Aynı ekrana bir
    dakika içinde dönülünce oraya kaydırılıyor.
  - Hata varsa sayfa en üstten açılıyor, mesaj görünsün.
  - Başka ekrana geçiş (menü, numara şeridi) yine en üstten (v6.35).
- İki fark:
  - Yalnızca POST formları konum saklıyor. Vitrifikasyondaki etiket araması
    gibi GET formları saklamıyor.
  - Konum sayfa bitince bir kez daha uygulanıyor. Üst çubuğun menü düğmesi
    içerikten sonra açılıyor ve çubuk 4 px uzuyor; tek uygulamada sayfa 4 px
    kayıyordu (denüdasyonda da böyleydi, ölçüldü).
- Kayıttan sonra sayfa kısalıyorsa (form bilgi kartına dönüyor: OPU,
  androloji, kaydı olan sıradaki yumurta) sayfanın sonuna iniyor.
- Vitrifikasyonda üstteki "Kaydedildi" mesajı artık ekranın yukarısında
  kalıyor. Dondurulan tüp "Dondurulmuş" listesinde de görünüyor.

**Deneme** (sahte veritabanında, telefon boyutu 390×844):
- ICSI'de kaydı olmayan iki yumurta arka arkaya kaydedildi. Düğme ekranın
  aynı yerinde kaldı (kaydırma 1015 → 1015).
- Gebelik, vitrifikasyon, transfer ve denüdasyon: kaydırma birebir aynı,
  düğme ekranda.
- Fertilizasyon, cleavage, blastokist, OPU, androloji: yeni sayfa daha kısa,
  sonuna indi; düğme varsa ekranda.
- OPU'da hatalı tarih ve vitrifikasyonda embriyo seçmeden kaydet: sayfa en
  üstten açıldı, hata görünüyor.
- ICSI'den fertilizasyona geçiş ve vitrifikasyondaki arama: en üstten.
- 56 ekran hatasız açıldı, betik hatası yok.

# v6.211 — ART Lab formunda çözülen tüplerin Cryo Haritası'ndaki yeri

Kullanıcı: *"ART Lab formunda dondurulan örneklerin yeri yazdığı gibi çözme
işlemlerinde de ART formunda yeri yazsın. Embriyo ve yumurta ikisi de
yazsın."*

- v6.208'den beri ART Lab formunda ÖZET tablosunun altındaki boş satırda bu
  tedavide dondurulan tüplerin yeri yazıyordu. Artık bu tedavi için çözülen
  tüplerin yeri de yazıyor: FET, FET (3→5), Yumurta Çözme ve Yumurta
  Dondurma'nın kendi çözmesi.
- Yazım dondurulanla aynı: "TANK 1 / 3 / 12 · Mavi Cryotop: 2 embriyo
  (8HG1-7HG2)"; yumurta tüpünde "1 yumurta (1*MII)".
- Yalnızca dondurma varsa satır değişmedi ("Cryo Haritası: ..."). Çözme
  varsa iki grup, çözme önce:
  - "Cryo Haritası (çözülen): ..."
  - "Cryo Haritası (dondurulan): ..." (FET'te yeniden dondurma olduysa).
- Çözülen tüpün yeri tüpün kayıtlı konumu. Çözme tüpü yalnızca "boşaltıldı"
  yapıyor, konumu silmiyor; yani yazılan, tüpün çözülmeden önce durduğu yer.
- Tüpü programda olmayan çözme yazılmıyor (Access'ten aktarılmış FET'in
  kendi altına açılan embriyoları, v6.130): "konum girilmemiş" demek
  programda olmayan bir tüp için yanlış olurdu.
- Yalnızca ART Lab formu ve ilk sayfası, v6.208'deki gibi. Embriyoloji
  Özet'in NOTLAR'ı değişmedi.
- `formlar.cozulen_tupler()` her tüpe `tup` (taşıyıcı) ve `yumurta` alanını
  da veriyor; `cryo_yeri_satirlari(tupler, cozulenler)` iki grubu kuruyor.

**Deneme** (sahte veritabanında):
- FET'te iki tüp çözüldü: "Cryo Haritası (çözülen): TANK 1 / 3 / 12 · Mavi
  Cryotop: 1 embriyo (4AA); TANK 1 / 3 / 12 · Sarı Cryotop: 1 embriyo
  (7HG2)". Çözülen bir embriyo aynı FET'te yeniden dondurulunca altına
  "Cryo Haritası (dondurulan): TANK 2 / 1 / 5 · ...: 1 embriyo (7HG2)".
- Yumurta tüpü bir Yumurta Çözme tedavisinde çözüldü: "Cryo Haritası
  (çözülen): konum girilmemiş · Cryotop: 1 yumurta (1*MII)".
- IVF/ICSI ve Yumurta Dondurma'nın formunda satır v6.210'dakiyle aynı.
- Excel'de aynı metin birleşik `A33:AC33` hücresinde, satır yüksekliği
  satır sayısından.
- Gerçek verili deneme kopyasında (1.909 tedavi) bütün ART Lab formları
  hatasız kuruldu. 255 formda çözülen tüplerin yeri yazıldı (3'ü yumurta,
  13'ünde yeniden dondurma da var; en çok 6 satır). Çözmesi olan 446
  tedavinin tüpü programda yok (aktarılmış FET), onlarda çözme grubu yok.
  Yalnızca dondurma olan 983 formun satırı v6.210'dakiyle, Özet formu da
  bütün tedavilerde birebir aynı.

# v6.212 — ART Lab ızgarasında "F" yerine "Freezing"

Kullanıcı: *"ART lab formunda dondurma yapılan hastada transfer kısmında F
yazıyor. Onu Freezing ile değiştirelim."*

- ART Lab formunun yumurta ızgarasında "Transfer" satırı, transfer edilen
  embriyoya ✓, dondurulana "F" yazıyordu (v6.37'den beri). Artık dondurulana
  "Freezing" yazıyor; ✓ değişmedi.
- Yazı tek yerde: `formlar.ARTLAB_DONDURULDU`.
- Kutu bir yumurta genişliğinde ve yanı öteki yumurtanın kutusu, yani
  taşamaz. Bugün sığıyor (ekranda 68 px kutuya 68 px yazı, yazdırırken de).
  Yine de "Freezing" yazan kutular küçülecekler listesinde
  (`sigdir_hucreleri()`): kâğıt ya da punto değişirse yazı kesilmez, küçülür.
  Excel'de aynı hücrelere `shrinkToFit`.

**Deneme** (sahte veritabanında): IVF/ICSI formunda iki dondurulan embriyo
"Freezing", transfer edilen ✓; Yumurta Dondurma formunda dondurulan yumurta
"Freezing". Ekranda ve yazdırırken kesilme yok. Excel'de D22 ve F22
hücrelerinde "Freezing", ikisinde de `shrinkToFit`.

# v6.213 — Tüpü programda olmayan Excel kaydı hastaya bağlanıyor

Kullanıcı: *"Excelde yeri olup Acsess kaydından oluşturulmamış hastaya excel
cryo haritasındaki tüpleri hastaya bağlama olsun. Yani cryodaki hasta kaydı
olmayan dondurulmuş örneği hastaya bağlama olsun."*

Excel kaydı (v6.189) Cryo Haritası Excel'inde bir gobletde duran, programda
tüpü bulunamayan straw. Tüpü programdaysa "Tüpe bağla" yetiyordu; tüpü hiç
yoksa (Access kaydı yok, o gün tüp yok, içerik tutmuyor) straw'ı bir hastaya
vermenin yolu yoktu.

**Excel kaydının sayfasında "Hastaya bağla" kartı:**

- Hasta araması: dosya no, hasta ya da eş adı. Her kelime ayrı aranıyor,
  sıra önemsiz (Excel'de soyad önde). "Excel'deki adla ara" kutuyu Excel'in
  adıyla arıyor -- yalnızca arama: ad tek başına kanıt değil, hastayı
  kullanıcı seçiyor. Arşivlenmiş hasta da çıkıyor (dosyası kapanmış hastanın
  straw'ı tankta olabilir). Sonuç kutunun hemen altında; "Aramayı temizle" ve
  geri ok aramasız sayfaya (v6.208'in kuralı).
- Seçilen hasta: kimliği; Excel'deki adla karşılaştırma (aynı / kaydın eşinin
  adı / farklı yazılmış -- farklıysa uyarı, eş adı da); hastanın tanktaki
  bütün tüpleri, **günü ne olursa olsun**. Excel'in tarihi yanlış yazılmışsa
  straw'ın tüpü başka bir gündedir: o zaman o tüpe bağlanır, yeni tüp açılmaz.
- "Bu hastaya açılacak tüp": içerik (HÜCRE, programın yazımıyla: "D5
  (3BA-1BB)", yumurtada "(4*MII-1*MI)"), dondurma günü, OPU günü (HÜCRE'nin
  "D5"inden, v6.177), hangi tedaviye gireceği, konum/tip/renk (Excel
  kaydınınki). "Bu hastaya tüp olarak aç" onayla yazıyor. Ekran ile kayıt aynı
  planı kuruyor (`cryo_esle.acilis_plani()`).

**Ne yazılıyor** (`cryo_esle.excel_kaydindan_ac()`):

- Embriyo / yumurta: v6.179'un `yeni_hasta` kipinin yazımı, aynı işlevlerle
  (`_excel_tedavisi_ac()`, `_excel_tupu_ac()` -- bu sürümde
  `yeni_hasta_yaz()`'dan ayrıldı; eski ve yeni kod sahte bir planla bütün
  tablolarda birebir aynı yazdı). Yalnızca dondurma bilgisi olan bir "Cryo
  Excel" tedavisi: IVF/ICSI, tüpte yalnızca yumurta varsa Yumurta Dondurma;
  tamamlanmış, bitiş sebebi dondurma, protokol notunda `[Cryo Excel kaydı]` --
  istatistik ve Bakanlık verileri bu tedavileri dışlıyor. OPU, ICSI ve
  döllenme uydurulmuyor; embriyonun skoru değerlendirme, yumurtanın olgunluğu
  maturasyon olarak, sonra dondurma.
- Hastanın aynı güne (aynı OPU günü; günü yazmayan embriyoda aynı dondurma
  günü) açılmış bir Cryo Excel tedavisi varsa tüp ona ekleniyor: aynı
  dondurmanın ikinci straw'ı ikinci bir tedavi açmasın. Yumurta Dondurma'ya
  embriyo konmuyor.
- Hastanın o gün programda başka bir tedavisi varsa uyarı çıkıyor: straw o
  tedavinin tüpü olabilir. Tüp o tedaviye **eklenmiyor**: yumurtaları orada
  zaten sayılı, yeni örnek açmak "kayıtlı yumurta" sayısını ve oranları
  bozardı. Ayrı Cryo Excel tedavisi istatistiğe girmiyor.
- Sperm: v6.180'in `sperm` kipinin yazımı -- seçilen hastaya bir sperm
  dondurma kaydı ve tüpü (etiket `<dosya no>-SP-SSDD`; sebep HÜCRE'den: "CA"
  Onkolojik, yoksa TESE/TESA).
- Tüp Excel kaydının gobletinde, tipi ve rengi Excel'inki. Excel kaydı
  'baglandi' oluyor: straw artık tüpün kendisiyle sayılıyor, iki kez değil.
  Tedavi numaraları tarih sırasıyla yeniden (v6.144), kayan numaralar
  günlükte.
- **Dondurma günü** Excel'inki. Excel'de yoksa, okunamıyorsa ya da bugünden
  ileriyse kullanıcı yazıyor; önizleme o günle yeniden kuruluyor. Elle yazılan
  günde notlar Excel'deki tarihi de söylüyor.
- Açılmayanlar: HÜCRE okunamıyorsa (boş, "PGT") -- içeriği bilinmeyen tüp
  açmak uydurmak olurdu; bir satırda birden çok tüp (parantez) yazıyorsa --
  Excel kaydı tek straw'ın yeri.

**Geri alma.** Bu yolla açılmış tüpte kaydın "Bağı çöz"ü "Açılan tüpü geri
al" oluyor: tüp, örnekleri ve olayları (spermde dondurma kaydı) siliniyor,
tedavi boş kaldıysa o da; Excel kaydı yeniden tankta. Yalnızca el değmemişse:
tüp tankta ve kaydın gobletinde, ona başka Excel kaydı bağlı değil, örneklerinde
bu açılışın yazdığından başka kayıt yok (çözme, transfer, fotoğraf, bulgu, PGT;
spermde tedaviye bağlama, onam eki). Silinen, Excel kaydının programdaki
karşılığı; kaydın kendisi duruyor, günlükte `KALICI_SILME` satırları. Hasta ya
da tedavi kalıcı silinince de kayıt tankta kalıyor; bağlamanın notu artık
temizleniyor (`app.excel_kaydi_bagini_birak()`).

**Aynı straw iki kez görünmesin diye üç koruma daha:**

- "Tüpe bağla" başka bir Excel kaydının straw'ı olan tüpe ikinci kaydı
  bağlamıyor. v6.189'dan beri açıktı: ikinci bağlama tüpü kendi gobletine
  alıyor, öteki kayıt "bağlandı" sayıldığı için haritadan bir straw düşüyordu.
- `cryo_esle.py yeni_hasta` ve `sperm` kipleri Cryo Haritası'nda Excel kaydı
  olan satırı atlıyor (raporda "Excel kaydı olarak duruyor"): o straw'ın
  kararı kaydın sayfasında verilmiş olabilir. `yerlesim`'in "önce öteki
  kipleri çalıştırın" denetimi de bu satırları artık beklemiyor.
- `eksik` raporu Excel kaydına bağlı tüpü "Excel'de karşılığı yok" diye
  listelemiyor.

**Deneme** (sahte veritabanında, uçtan uca): blastokist straw'ı yeni Cryo
Excel tedavisiyle açıldı (OPU "D5"ten), aynı günün ikinci straw'ı aynı
tedaviye girdi, yumurta straw'ı Yumurta Dondurma'yla, tarihsiz straw elle
yazılan günle, sperm straw'ı sperm dondurma kaydıyla; okunamayan HÜCRE, iki
tüplü satır, gün olmadan kayıt ve bağlı tüpe ikinci bağlama reddedildi. Geri
alma: çözülmüş, taşınmış ve sonradan transfer yazılmış tüpte reddedildi;
ikinci straw geri alınınca tedavi kaldı, ilki geri alınınca boş tedavi silindi.
Eski "Tüpe bağla / Bağı çöz" değişmeden çalışıyor. 70 ekranlık taramada sorun
yok. Gerçek verinin deneme kopyasında (yalnızca sayılar): 2.727 embriyo/yumurta
Excel kaydından tüp açılabiliyor; 14'ünün HÜCRE'si okunamıyor, 1'inde iki tüp
yazıyor, 39'unda ve 15 sperm kaydının hepsinde gün elle yazılmalı. 12 kayıtta
açılıp geri alındı: gobletlerin straw sayısı değişmedi, geri almadan sonra
düzen birebir aynı.

# v6.214 — Konumu girilmemiş tüpün yeri haritadan tamamlanıyor

Kullanıcı: *"Konumu girilmemiş yazılan dondurulmuş örnekler var. Ama haritada
yeri görünüyor. Neden konumu girilmemiş yazıyor? Haritaya bakıp yeri
tamamlansa."*

**Neden "konum girilmemiş".** Access kayıtlarında tüpün yeri yoktu. Konumlar
Cryo Haritası Excel'inden yazıldı (`cryo_esle.py uygula`, v6.173; aktarımın
sonunda kendiliğinden, v6.207) -- ad, dondurma günü ve içerik üçü birden
birebir tutunca. Biri tutmayan tüp konumsuz kaldı; straw'ı ise haritada Excel
kaydı olarak gobletinde duruyor (v6.189). Aynı straw iki yerde, birbirine
bağlı değil. Deneme kopyasında konumu boş 514 dolu tüpün 168'inin haritada
olası eşi var. Tutmayan: ad bir harf farklı ya da Türkçe harfsiz yazılmış,
Excel'deki tarih 1-7 gün kayık, skor farklı yazılmış (sayı aynı), eş adı
farklı, ad hiç tutmuyor ama gün ve içerik aynı. Kuralla tutup bağlanmamış
çift kopyada yok.

**Program kendisi bağlamıyor, kanıtıyla öneriyor** -- ad benzerliği tek
başına kanıt değil (v6.125, v6.205). `cryo_esle.yer_onerileri()`:

- Aday: haritada yeri olan, tankta duran Excel kaydı; tüpün dondurma
  gününden en çok 7 gün kayık (`YER_ONERI_GUN`) ya da tarihsiz.
- Kanıt: ad (aynı / farklı yazılmış / bir kısmı eksik / bir kelimesi farklı /
  tutmuyor), gün (aynı / OPU'dan tutuyor / N gün kayık / Excel'de yok),
  içerik (aynı / sayı aynı, yazım farklı), eş adı (tutuyor / farklı), "bu ad
  programda başka bir hastada da var". Ekranda "Tutan" ve "Farklı" iki ayrı
  liste; farklı olan hep yazılıyor.
- Önerilmeyen: içeriğin sayısı bile tutmuyorsa; gün 7'den çok kayıksa; ad hiç
  tutmuyorsa (yalnızca aynı gün aynı içerikte öneriliyor); Excel'deki ad
  programda BAŞKA bir hastanın adıysa hiç -- straw o hastanın. Kanıt puanı
  (küçük = güçlü) 4'ü aşan önerilmiyor.
- **Her tüpe ayrı bir straw** (`_bire_bir()`). Aynı hastanın aynı içerikli
  tüpleri aynı straw'ları aday gösteriyor (kopyada birden çok tüpe aday 82
  Excel kaydının hepsi böyle); tüp başına en iyi aday iki tüpe aynı straw'ı
  önerirdi. Birbirine aday üzerinden bağlı tüpler bir küme; kümede önce en
  çok eşleşme, sonra en küçük toplam puan, eşitlikte sıra (aynı tüpler
  programda ayırt edilmiyor, v6.148). Straw'ı kardeşine önerilen tüp
  listede "önerilmedi" diye duruyor.
- Programın kuralıyla kesin tutan (`excel_kaydi_plani()`'nin "bagla"sı)
  işaretli geliyor -- aktarım da onu kendisi bağlıyor. Ötekiler işaretsiz.

**Ekranlar:**

- "Haritada yeri belirsiz" (`/cryo/yersiz`) -> **"Haritadan yer tamamla"**
  (`/cryo/yer-tamamla`): hasta hasta, her tüpün önerilen straw'ı (goblet,
  Excel'deki yazısı, tutan ve farklı olan), onay kutusu, "Bu hastanınkileri
  seç", "Seçilenleri bağla (N)". Kayıt aynı kilidin içinde öneriyi yeniden
  kuruyor: bu arada değişen çift (tüp çözüldü, straw başka tüpe bağlandı) ve
  aynı straw'ı ikinci kez isteyen seçim yazılmıyor, sayısı ekranda.
- **Tüpün sayfası**: konum girilmemişse nedeni ("Access kayıtlarında konum
  yoktu ..." ya da "Dondurulurken konum yazılmamış."), haritadaki olası
  yerleri ve her birinde "Bu yere bağla"; programdaki hastanın adı üstte,
  Excel'deki yazımla yan yana okunsun diye. Bir Excel kaydına bağlı tüpte o
  kayda bağlantı ("Bağı çöz" orada).

**Yazım** Excel kaydının bağlamasının aynısı
(`cryo_esle.excel_kaydini_tupe_bagla()`): tüp straw'ın gobletine geçiyor,
rengi boşsa Excel'inki, aktarımın açtığı tüpün varsayılan tipi ("cryotop",
Access'te tip yoktu) Excel'inkiyle değişiyor (v6.207'nin kuralı), Excel kaydı
'baglandi'. Excel kaydının sayfasındaki "Tüpe bağla" da artık bu işlevden
geçiyor: üç bağlama yolu tipte de aynı davranıyor. Geri alma kaydın
sayfasındaki "Bağı çöz".

**Bulunan hata: "Bağı çöz" tipi değişen tüpte hata veriyordu** (v6.207'den
beri). Bağlama üzerine yazdığı tipi notuna yalnızca adıyla yazıyordu
("doldurulan: renk,tip"), geri alma o alanı boşaltmaya çalışıyordu; tüpün
tipi boş olamaz (NOT NULL): "Beklenmeyen hata". Aktarımın kendiliğinden
bağladığı (v6.207) her tüpte geri alma bu yüzden çalışmıyordu. Artık not eski
değeri de yazıyor ("tip=cryotop"), geri alma onu geri koyuyor. Eski biçimli
notta eski değer değişiklik geçmişinden bulunuyor, bulunamazsa tip olduğu gibi
kalıyor. Bağlamadan sonra elle değiştirilmiş renge/tipe dokunulmuyor.

**Deneme.** Sahte veritabanında her durum: bir harf farkı, 2 gün kayık tarih,
farklı yazılmış skor, tutmayan ad, başka hastanın adı (önerilmedi), farklı eş,
aynı iki tüp + iki straw (ayrı straw'lar önerildi), aynı iki tüp + bir straw,
kuralla kesin tutan (işaretli), olası yeri olmayan tüp. Tüpün sayfasından
bağlama ve bağı çözme; toplu bağlamada aynı straw'ı iki tüpe seçmek, geçersiz
seçim ve öneri olmayan çift reddedildi; eski biçimli notla geri alma. 72
ekranlık taramada sorun yok, telefonda yatay taşma yok. Gerçek verinin deneme
kopyasında (yalnızca sayılar): 514 konumsuz tüpün 168'ine öneri (işaretli 0;
puanı 1: 84, 2: 60, 3: 9, 4: 15). Hepsi bir seferde bağlandı (0,16 sn):
gobletlerin straw sayısı değişmedi, her bağlı tüp kaydının gobletinde. 168'inin
bağı çözülünce tüpler ve Excel kayıtları birebir önceki hali.

# v6.215 — Aynı hastanın iki kartı birleştiriliyor (`hasta_birlestir.py`)

Kullanıcı: *"... ile ... dosya numaralı hasta aynı. Doğru numara .... Bu iki
hasta kayıtlarını birleştirir misin?"* (numaralar sohbette; buraya hasta
bilgisi yazılmıyor).

Kullanıcının veritabanı bu oturumda yok, iki kart deneme kopyasında da yok
(kopya daha eski). Birleştirmeyi kullanıcı kendi bilgisayarında çalıştırıyor;
bu sürüm onun aracını yazdı. `dosya_no_degistir.py` (v6.172) yetmiyordu: doğru
numara kayıtlıysa bilerek duruyor ("iki kart birleştirilmez") -- artık o mesaj
bu araca yönlendiriyor.

**Ne yapıyor.** Doğru numaralı kart kalıyor, yanlış numaralı kart siliniyor,
tek yazma işleminde:

- Tedaviler ve sperm dondurmaları doğru karta (`cycle.hasta_id`,
  `sperm_dondurma.hasta_id` -- şemada hastaya bağlı yalnızca bu iki tablo var;
  örnekler, olaylar, tüpler, fotoğraflar, bulgular tedaviyle birlikte gidiyor).
- Fotoğraf ve onam eki yolları `<yanlış>/...` -> `<doğru>/...`; v6.4 öncesinin
  mutlak yolları da yanlışın arşiv klasörüne düşüyorsa göreli yola çevriliyor.
  Veritabanı yazıldıktan sonra arşivdeki dosyalar doğrunun klasörüne taşınıyor
  (iki klasörde de olan alt klasörün içine iniliyor). **Aynı adlı dosya iki
  klasörde de varsa araç baştan duruyor** -- fotoğraflar karışırdı.
- Başka kartların "eşin dosya no"su yanlış numarayı gösteriyorsa doğrusu;
  doğru kartın kendi "eşin dosya no"su bu iki numaradan biriyse boşalıyor
  (kendisini gösterirdi).
- Kart alanları: doğru kartta boş olan yanlış karttan doluyor; ikisinde de dolu
  ve farklıysa doğrununki kalıyor, önizleme hangi alanlar olduğunu söylüyor;
  notlar alt alta ("(... kartından) ..."). Açılış günü ikisinin erkeni
  (Bakanlık verisinin "yeni hasta"sı, v6.201); biri aktifse kart aktif.
- Geçici numaralı kartta (9000000001…, `cryo_esle.py`) sperm tüpünün
  `<numara>-SP-SSDD` etiketi yeni numaraya -- `dosya_no_degistir.py`'nin
  kuralı ve işlevi; gerçek numaralı tüpün etiketine dokunulmuyor.
- Tedaviler tarih sırasıyla yeniden numaralanıyor (`db.tedavileri_sirala()`).
- Her değişiklik `degisiklik_log`'a, aynı işlemin içinde; silinen kartın bütün
  alanları JSON olarak "BIRLESTIRME" satırında (kalmayan telefon, doğum tarihi
  orada okunabilir).

**Karar kullanıcının.** Önizleme hiçbir şey yazmıyor: iki kartın tedavi / sperm
/ fotoğraf sayıları, adın, eş adının, doğum tarihinin tutup tutmadığı (adlar
basılmıyor), doldurulacak ve farklı alanlar, taşınacaklar. "DİKKAT" satırları:
adlar hiç tutmuyor, doğum tarihleri farklı, yanlış kartın adı doğru kartın eş
adı (eşin kendi kartı olabilir -- o zaman birleştirilmez, "Eşine bağla"
kullanılır, v6.180), aynı gün aynı tipte iki tedavi (aynı tedavi iki kez
girilmiş olabilir; birleştirme ikisini de koruyor). `uygula` "BIRLESTIR"
istiyor ve önce veritabanının tamamını `lab_ONCEKI_<zaman>.db` diye
kopyalıyor: yedek klasörü o bilgisayarda varsa oraya (Yedekleme ekranının
"geri yükle" listesi onu gösteriyor, günlük temizlik bu adı silmiyor), yoksa
veri klasörüne. Plan kilidin içinde yeniden kuruluyor.

**Birleştirmeden sonra** araç gerekirse söylüyor: yanlış kartın tedavileri
Access'ten geldiyse düzeltme dosyasına eklenecek satırlar
(`KAYNAK#KAYIT  DOSYA  <yanlış>  <doğru>`): aynı CSV yeniden aktarılırsa
yanlış numara "başka hastanın tedavisi" diye çakışırdı (`_carpismalar()`).
Kaynak tüpüne bağlanmamış aktarılmış FET varsa `aktar_access.py bagla` (tüp
öteki karttaydı, artık aynı hasta); konumu girilmemiş tüp varsa Haritadan yer
tamamla (v6.214).

**Hasta kartının adresi kart yoksa `/hastalar`'a dönüyor** (`hasta_detay`).
Silinen (kalıcı silme ya da birleştirme) kartın açık kalmış sekmesi tazelenince
boş bir kart ve olmayan hastaya "Yeni tedavi aç" düğmesi basılıyordu.

**Deneme.** Sahte veritabanında iki kart (iki klasörde fotoğraf, biri mutlak
yolla; sperm dondurma + onam eki; Access işaretli iki tedavi; eş numarası
yanlış kartı gösteren üçüncü kart; aynı gün aynı tipte iki tedavi): önizleme,
birleştirme, arşiv taşıma, alanların doldurulması, eş numarası, günlük,
tedavi sırası; programda kart, tedaviler, formlar, fotoğraf ve onam 200, eski
kartın adresi `/hastalar`'a. Ayrıca: olmayan / aynı numara, doğru kart yoksa
`dosya_no_degistir.py`'ye yönlendirme, arşiv çakışmasında hiçbir şey yazılmıyor
(kopya da alınmıyor), vazgeçme, geçici numaralı sperm etiketi, ikinci
çalıştırma, farklı ad / doğum tarihi / eş adı uyarıları. Gerçek verinin deneme
kopyasında (yalnızca sayılar) iki kart birleştirildi (0,35 sn): hasta 1.823 ->
1.822, öteki tablolar aynı, yabancı anahtar ve bütünlük denetimi temiz, ekranlar
200; kopya silindi.

# v6.216 — Cryo Haritası değişince yedek, her gün 14:00'te "Tüm veriler"

Kullanıcı: *"Cryo haritada yapılan her değişiklikten sonra yedekleme yapsın.
Yönetici kısmındaki tüm verileri excele aktarda her gün 14:00 da cryo haritanın
yedeklendiği dosyaya aktarsın aktarma yapsın."*

Programın kendiliğinden aldığı bir yedek yoktu: Mac'te zamanlama hiç
kurulmadı, klinikteki Windows'ta Görev Zamanlayıcı görevi de kurulmadı (bekleyen
iş 2); yedek yalnızca "Şimdi yedekle"ye basılınca ya da terminalden
`yedek.py` ile alınıyordu. Cryo Haritası'nın Excel'i her değişiklikte
yazılıyordu (v6.191) ama bilgisayarın kendi diskine; yedek diskine yalnızca
yedekle birlikte gidiyordu.

## Cryo Haritası değişince yedek (`oto_yedek.py`)

Haritanın iş parçacığının yanında ikinci bir iş parçacığı dakikada bir
haritanın **içerik imzasına** bakıyor (`harita_excel.guncel_imza()`: dolu
tüpler, Excel kayıtları, yerler, straw'ların yazıları; dosyanın yazılıp
yazılamamasından bağımsız). İmza yedek klasörüne son yedeklenen halinkinden
farklıysa yedek alınıyor: "Şimdi yedekle"nin aynısı (veritabanı, arşivdeki
yeni fotoğraflar, haritanın Excel'i). Bir ICSI kaydı yedek aldırmıyor (harita
değişmiyor); dondurma, çözme, taşıma, yer tamamlama, Excel kaydı aldırıyor.

- **Değişiklikler bitince.** Harita bir tur (bir dakika) değişmeden kalınca;
  değişiklik sürüp gidiyorsa ilk değişiklikten en geç 10 dakika sonra. Bir
  hastanın dört straw'ı arka arkaya dondurulunca dört değil bir yedek.
- **Son yedeğin imzası yedek klasöründe** (`cryo_yedek_durumu.json`: imza,
  zaman, dosya adı; hasta bilgisi yok). Program yeniden açılınca harita
  değişmemişse yedek alınmıyor; kapalıyken değişmişse (terminal aracı, USB ile
  gelen veritabanı) açılışın ilk dakikalarında alınıyor. Başka bir disk ya da
  klasör kendi dosyasıyla sayılıyor. Bellekte tutulsaydı her açılış bir yedek
  aldırırdı; veritabanında tutulsaydı USB ile öteki bilgisayara gider, orada
  "yedeklendi" derdi.
- **Yedek klasörü yoksa beklenir, oluşturulmaz.** Takılı olmayan disk
  takılınca yedek alınıyor. Mac'te takılı olmayan bir diskin yerine
  (`/Volumes/...`) iç diskte klasör açılırsa disk takılınca başka adla bağlanır
  ve yedek yanlış yerde birikirdi. Hiç yedek alınmamış klasörü "Şimdi yedekle"
  açıyor (o, v6.119'dan beri oluşturuyor); ekran bunu söylüyor.
- **Harita kurulamıyorsa** (bir hata) veritabanının damgasına bakılıyor:
  yedek haritanın hatası yüzünden durmuyor.
- **Hata** (disk dolu, izin): günlüğe bir kez, Yedekleme ekranına; 10 dakika
  sonra yeniden.
- **"Şimdi yedekle" aynı yoldan** (`oto_yedek.yedekle()`): elle alınan yedekten
  sonra aynı harita için otomatik yedek alınmıyor. İkisi aynı anda çalışmıyor
  (`yedek.KILIT`): otomatik yedek sürerken basılan düğme onun bitmesini
  bekliyor. Yedeğin adımları tek yerde, `yedek.yedekle()`: terminal, düğme ve
  otomatik yedek onu çağırıyor (düğme v6.215'e kadar adımları ayrıca
  yazıyordu).
- Cryo Haritası'nın değişmediği günlerde otomatik yedek alınmıyor; Görev
  Zamanlayıcı ile günlük yedek yine kurulabilir (ekran söylüyor).

**Saklama değişti** (`yedek.silinecek_yedekler()`): son 24 saatin bütün
yedekleri; 14 güne kadar her günün son yedeği; daha eskide her ayın ilk yedeği
kalıcı. v6.215'e kadar "14 günün hepsi + ayın 1'inde alınanlar"dı -- günde bir
yedekle aynı sonuç; günde birkaç otomatik yedekle yedek diski dolardı. Ayın
1'inde birden çok yedek varsa artık yalnızca ilki kalıcı; ayın 1'inde yedek
alınmamışsa o ayın ilk yedeği. Güvenlik kopyalarına (`lab_ONCEKI_*`) ve adı
kalıba uymayan dosyaya dokunulmuyor.

**Yedek önce geçici dosyaya yazılıyor** (`<ad>.<süreç>.yaziliyor`),
doğrulanınca adını alıyor: yazım yarıda kalırsa (disk çekildi, program
kapandı) geri yükleme listesinde yarım bir `lab_*.db` durmuyor; aynı dakikada
başka bir süreçteki yedek (terminalden `yedek.py`) öncekinin yazılmakta olan
dosyasına yazmıyor. Bir günden eski yarım dosyayı temizlik siliyor.

`yedek.yaz()` programın içinde `print` yerine günlüğe (`program.log`) yazıyor;
terminalde (`yedek.py`, `geri_yukle.py`) ekrana da. Satırlar yine `yedek.log`'a.

**Ekranlar**: Yedekleme'de "Otomatik yedek" kartı (durum ve nasıl çalıştığı),
Yönetici panelinin Yedekleme kartında bir satır, Cryo Haritası'nın Excel
kartında (yönetici) bir satır -- cümle tek yerden (`_oto_yedek.html`): "Cryo
Haritası'nın şu anki hali yedekli: <zaman> (<dosya>)", bekleyen değişiklik,
klasör yok / ayarlanmamış / bu bilgisayarın yolu değil, son hata. Durum
bellekten (`oto_yedek.durum()`): sayfa açılırken takılı olmayan bir diske ya da
yavaş bir ağ klasörüne sorulmuyor.

## Her gün 14:00'te "Tüm veriler"

Yönetici panelindeki "Tüm veriyi Excel'e aktar"ın dosyası (aynı içerik,
`disari.tumu_sayfalari()`) her gün 14:00'te **Cryo haritası klasörüne**
(Klasörler ekranı; varsayılanı veri klasöründe `cryo_harita/`, Cryo_Haritasi.xlsx
ve günlük kopyalarının yanı): `Tum_Veriler_YYYY-AA-GG.xlsx`, son 30 gün.

- "Cryo haritanın yedeklendiği dosya" bu klasör diye okundu: Klasörler ekranı
  onu "Programın her değişiklikte yazdığı Cryo Haritası Excel'i ... ve son 30
  günün kopyaları" diye anlatıyor; yedek diskindeki kopya
  (`<yedek>/cryo_harita/`) hiçbir ekranda yazmıyordu. Başka bir yer
  isteniyorsa klasör Klasörler'den değişiyor.
- Bugünün dosyası varsa yazılmıyor; 14:00'te program kapalıysa o gün
  açıldığında yazılıyor. Kaçan günün dosyası sonradan yazılmıyor (o günün
  hali yok).
- Klasöre yazılamıyorsa döküm hiç kurulmuyor (her denemede bütün veritabanını
  okumak boşa olurdu), 10 dakika sonra yeniden; hata Cryo Haritası kartında.
- **Dosya bütün hasta kayıtlarını taşıyor.** `/disari/tumu`'nun "yalnızca
  yönetici" kuralı değişmedi: dosya ağdan verilmiyor, yöneticinin seçtiği
  klasöre yazılıyor. Klasörler ekranı, Cryo Haritası kartı ve yönetici
  panelindeki düğmenin açıklaması bunu söylüyor. Varsayılan klasör
  `.gitignore`'da.
- Temizlik yalnızca `Tum_Veriler_YYYY-AA-GG.xlsx` adlarını siliyor; klasördeki
  haritanın dosyalarına ve başka dosyalara dokunmuyor.

## Deneme

- Birim: saklama kuralı 16 dosya adında (24 saat, günün sonu, ayın ilki,
  saniyeli ad, `lab_ONCEKI_*`, kalıp dışı ad); tetik: harita kurulmamış,
  açılışın ilk değişikliği (bir tur sonra), tek değişiklik, 14 dakika süren
  değişiklik (10. dakikada), aynı imzayla yeniden açılış (yedek yok), kapalıyken
  değişmiş (yedek), disk yok / geldi, elle yedekten sonra (tekrar yok), hata
  (10 dakika bekleme), harita kurulamıyor (damga). "Tüm veriler": 13:59 yok,
  14:00 var, ikinci tur yazmıyor, ertesi gün 10:00 yok / 16:00 var, 30 günden
  eski siliniyor, başka dosyalar kalıyor, yazılamayan klasörde döküm
  kurulmuyor, klasör düzelince yazılıyor; sayfaları indirmeyle aynı.
- Uçtan uca (sahte veritabanı, kısa aralıklarla): açılışta yedek + döküm; bir
  tüpü "taşındı" yapmak -> yedek, geri almak -> yedek (imza ilk hale döndü);
  "Şimdi yedekle" -> sonra otomatik tekrar yok; yeniden başlatma -> yedek ve
  döküm tekrarlanmıyor. 75 ekran telefon ve masaüstü genişliğinde hatasız,
  yatay kayma yok.
- Paket: Linux'ta derlendi, `paket/dene.py program` TAMAM; derlenmiş program
  sahte veritabanında kendi yedeğini aldı, satırlar `program.log`'da.
- Gerçek verinin deneme kopyasında (1.823 hasta): döküm 3,3 MB, arka planda
  ~4 sn; yedek 14,6 MB. O sırada sayfalar en çok 136 ms'de açıldı (ortanca
  4 ms). Kullanıcının veritabanı bunun yaklaşık üç katı. Kopya ve ürettikleri
  silindi.

# v6.217 — Hasta kartında "Dondurulmuş örnekler", çöz → FET; genel bulgular Özet'e

Kullanıcı: *"Hasta kartının içinde hastanın dondurulmuş örnekleri bölümü olsun.
Orada örnekler görünsün çöz diyerek FET tedavisi başlatabilelim. Ayrıca başka
merkeze taşıma bu alanın altında olsun. Genel bulgular ART lab formunda
yorumlara yazıldığı gibi Embriyoloji özet formunda notlara da yazılsın."*

## Dondurulmuş örnekler

Hasta kartının en üstünde (düğmelerin altında) tek bir kart:

- **Tanktaki embriyo ve yumurta tüpleri**, dondurulduğu tedavi tedavi (son
  tedavi üstte). Satır Taşınma ekranınınkiyle ve Cryo Haritası'nın goblet
  satırıyla aynı: etiket, renk, tip, "2 embriyo · D5 (3AA-4AB) · 12.03.2026",
  tanktaki yeri ya da "konum girilmemiş". Satıra basınca tüpün sayfası.
- **"Çöz"** her tüpün altında. Kural çözme ekranınınki
  (`thaw_tedavi_tipleri()`, v6.155/v6.156): embriyo tüpü FET, cleavage
  tüpü ayrıca FET (3→5) (blastokist tüpü FET (3→5)'e kapalı), yumurta tüpü
  Yumurta Çözme.
  - **"Çöz · yeni FET"**: onay soruluyor ("Bu tüp için yeni bir FET tedavisi
    açılacak ve çözme ekranına geçilecek"), sonra çözme ekranının v6.155'ten
    beri var olan "Yeni tedavi başlat" yolu: tedavi açılıyor, çözme formu bu
    tedavi seçili açılıyor. Kaydedince FET'in çözme ekranı (v6.208): sıradaki
    aşama Transfer, tankta kalan tüpler.
  - **"Çöz · <no> (FET) için"**: hastanın bu tüpe uygun, bitmemiş ve henüz
    transferi yapılmamış bir tedavisi varsa önce o. İki tüp aynı FET için
    çözülecekse ikincisi yeni bir FET açmasın. Transferi yapılmış ama
    bitirilmemiş FET önerilmiyor ("İşlemi bitir" unutulmuş olabilir); gerekirse
    çözme ekranında seçilir.
  - Yumurta Dondurma'nın kendi çözmesi (kullanıcının kararı, 2026-09-23)
    çözme ekranında kaldı; kartta yalnızca amacı çözme olan tedaviler.
- **Dondurulmuş sperm**: v6.125'in ayrı kartı bu kartın içine taşındı, satır ve
  "Tedaviye bağla" aynı. Başka merkeze taşınan sperm burada tekrar edilmiyor.
- **Cryo Haritası'nda adı benzeyen Excel kayıtları**: programda tüpü olmayan,
  adı bu hastanınkiyle aynı kelimelerden oluşan straw'lar (Taşınma ekranının
  ölçüsü, v6.205). Hastaya bağlı değiller (ad tek başına kanıt değil), buradan
  çözülemez; satır kaydın sayfasını bu hasta seçili açıyor (v6.213 "Hastaya
  bağla"), bağlanınca tüp yukarıdaki listeye geliyor.
- **Başka merkeze taşıma** kartın en altında: taşınanlar taşıma taşıma (gün ve
  yer, embriyo, yumurta ve sperm) ve Taşınma ekranının düğmesi ("Başka
  merkeze taşı"; taşımak da geri almak da orada). Sayfanın dibindeki eski
  düğme kalktı. Tedavi satırı taşımayı söylemeye devam ediyor (v6.205).
- Hiçbiri olmayan hastada kart basılmıyor.

Veri tek yerden: `hastanin_dondurulmus_ornekleri()` Taşınma ekranının
tüplerini (`hastanin_tasima_tupleri()`) ve gruplamasını (`tankta_gruplari()`,
`tasinan_gruplari()`, ekranla ortak) kullanıyor; satır `_tup_bilgisi.html`
(iki ekranın ortak makrosu). Gerçek verinin deneme kopyasında en çok tüpü olan
hasta (9 tüp) 53 ms; 372 yumurta tüpünün hepsi Yumurta Çözme, embriyo
tüplerinin bir kısmı FET (3→5) de öneriyor.

## Onay pencereleri hiç açılmıyordu

Deneme sırasında bulundu: `onsubmit="return confirm({{ metin('...')|tojson }})"`
yazılan 13 onayın hiçbiri sorulmuyordu. `tojson` metni çift tırnakla basıyor,
nitelik ilk tırnakta bitiyor; tarayıcı yalnızca `return confirm(` görüp
sözdizimi hatası veriyor ve **form onaysız gönderiliyordu** (denendi: taşıma
formu tek dokunuşla kaydediliyordu). Etkilenenler v6.180'den beri: taşıma ve
geri alması, tüpün "taşındı" kaydı ve geri alması (tüp ve sperm sayfası),
Excel kaydının tüpe bağlanması / tanka geri konması / bağının çözülmesi /
hastaya tüp açılması / tanktan çıkarılması, haritadan yer tamamlamanın tek
tüp bağlaması, eş bağının kaldırılması. Nitelik tek tırnakla yazıldı
(`onsubmit='...'`, `tojson` tek tırnağı kaçırıyor); tarayıcıda denendi: onay
çıkıyor, "vazgeç" formu göndermiyor. `<script>` içindeki iki onay (geri
yükleme, ağ erişimi) zaten doğruydu. CLAUDE.md tuzak #16.

## Genel bulgular Embriyoloji Özet'in NOTLAR'ında

ICSI ekranının genel bulguları (v6.200) ART Lab'ın alttaki "Yorum:" satırına
yazılıyordu; artık Özet'in NOTLAR kutusuna da: "Genel bulgular: Kalın zona,
Vakuol, Sperm hareketsiz" (`formlar.genel_bulgu_notu()`, aynı metin
`db.tedavi_bulgu_metni()`). Yer protokol notunun hemen altı -- klinik akışta
ICSI dondurmadan önce; sıra protokol → genel bulgular → dondurma → taşınan →
çözülen → çözme notu → iptal sebebi. ART Lab'ın koşuluyla aynı: yalnızca
ICSI'si olan tipte. Yumurta Dondurma'da genel bulgu bölümü yok (orada ART
Lab'ın Yorum'u yumurta yumurta bulguları yazıyor; NOTLAR'a girmedi, istenen
genel bulgulardı). Önek Türkçe sabit (form iki dilde de Türkçe), satır 68'de
sarılı. Yüklenen formların `{{notlar}}` etiketi aynı metni alıyor
(açıklaması güncellendi).

## Deneme

Sahte veritabanında tarayıcıyla: iki tüplü hastada "Çöz · yeni FET" -> onay ->
yeni FET, çözme formu o tedavi seçili; kayıt -> FET'in çözme ekranı; kartta
çözülen tüp listeden çıktı, kalan tüp "Çöz · <yeni FET> için" + "Çöz · yeni
FET" gösterdi, ilki çözme formunu o FET seçili açtı. Transferi yapılmış açık
FET önerilmedi. Taşıma: onay soruluyor, vazgeçince tüp tankta kalıyor, kabulle
taşınıyor; kartta tanktaki tüp yok satırı, taşınanlar (embriyo + sperm),
sperm listesinde tekrar yok, geri alınca ikisi yeniden listede. Özet formunun
NOTLAR'ı ve ART Lab'ın Yorum'u aynı genel bulgu metnini basıyor. 84 ekran
telefon ve masaüstü genişliğinde hatasız, yatay kayma yok. Gerçek verinin
deneme kopyasında yalnızca süre ve sayılar ölçüldü; kopya silindi.

# v6.218 — Hasta kartında "Dondurulmuş örnekler" Tedaviler'in altında

Kullanıcı: *"Hasta kartında dondurulmuş örnekler tedavilerinin altında olsun."*

v6.217'de kart sayfanın en üstündeydi (düğmelerin hemen altı, v6.125'in
"Dondurulmuş sperm" kartının yeri). Artık Tedaviler kartının hemen altında;
içeriği ve sırası değişmedi (tanktaki tüpler ve "Çöz", dondurulmuş sperm,
adı benzeyen Excel kayıtları, en altta başka merkeze taşıma). Eş kartları
("Eşinin tüp bebek kaydı", "Eşin dondurulmuş spermi") istenmediği için
yerinde, Tedaviler'in üstünde.

Kartın içindeki "Tedaviye bağla" ve bağı kaldırma formları sayfayı yeniden
yüklüyor. Kart en üstteyken sonuç hemen görünüyordu; aşağıda sayfa en üstten
açılır, sonucu görmek için yeniden aşağı inmek gerekirdi. Hasta kartı bu
yüzden aşama ekranlarının kaydırma parçasını kullanıyor (`_kaydirma.html`,
v6.210): kayıttan sonra kaldığı yerde açılıyor, bağlantıyla gelince yine en
üstten. Eş bağlamanın hatası (`es_hata`) varsa en üstten, mesaj görünsün.

Deneme (sahte veritabanı, telefon ve masaüstü genişliği): dört hastada kart
Tedaviler'in hemen ardından; telefonda spermi tedaviye bağlayıp bağı kaldırınca
sayfa aynı yerde (828 px) açıldı, satır "Kullanıldığı tedavi" / "Henüz bir
tedaviye bağlanmadı" dedi; bağlantıyla açılış en üstte; olmayan bir eş dosya
numarası sayfanın dibinden gönderilince sayfa en üstten, hata mesajıyla açıldı.
84 ekran iki genişlikte hatasız, yatay kayma yok.

# v6.219 — Tedavide bulaş hastalığı, kimlik bandında kırmızı uyarı

Kullanıcı: *"Hastaların tedavi kayıtları sırasında kadın ve erkeğin bulaş
hastalığı olup olmadığı seçeneği olsun. Bu hastalıkları seçebilelim. Hepatit
HİV gibi virütik hastalıklar seçilebilsin. Seçim tedavi boyunca en üstte
adının olduğu yerde fark edilebilecek şekilde görünsün."*

## Kayıt: tedavinin, kişi başına

`goc_057`: `cycle.bulas_kadin` ve `cycle.bulas_erkek` (kadın hastanın kendisi,
erkek eşi). Değer boşsa girilmedi, `yok` ise bulaş hastalığı yok; öteki
değerler seçilen hastalıkların kodları ("hbv,hiv"), elle yazılan hastalık
`|`'den sonra ("hbv|Sifiliz"). Biçimi okuyan ve yazan tek yer
`db.bulas_oku()` / `db.bulas_yaz()`.

- **Tedavinin kaydı, hastanın değil**: istek "tedavi kayıtları sırasında" ve
  "tedavi boyunca" diyor. Tahlil her tedavide yenileniyor; her tedavi kendi
  zamanındaki durumu tutuyor (tüplerin dondurulduğu andaki durum da o).
- **Tablo değil kolon**: tedavinin bir alanı. Tedavi formu yazıyor, değişiklik
  geçmişi formun öteki alanlarıyla birlikte tutuyor; kalıcı silme, kart
  birleştirme ve "Tüm veriler" dökümü onu tedaviyle birlikte götürüyor, ayrı bir
  adım gerekmedi.
- **Liste `bulas_hastaligi`**: Hepatit B, Hepatit C, HIV (kullanıcının
  örnekleri: "Hepatit HİV gibi virütik hastalıklar"). Programda listeyi
  düzenleyen ekran olmadığı için her kişinin yanında bir **"Diğer"** kutusu var;
  listede olmayan hastalık oraya yazılıyor (en çok 80 harf).

## Tedavi formu

"Tedavi" kartının altında yeni bir **"Bulaş hastalığı"** kartı var. Kadın ve
erkek için ayrı satırlar: **Yok**, Hepatit B, Hepatit C, HIV ve "Diğer" kutusu.
Hiçbiri seçilmezse "girilmedi" sayılıyor. "Yok" ile hastalık birbirini
dışlıyor: "Yok"a basınca hastalıklar ve "Diğer" temizleniyor, hastalık seçince
"Yok" kalkıyor. İkisi birden gelirse sunucu hastalığı alıyor, bulaş hastalığı
sessizce kaybolmuyor. Seçili hastalık kırmızı, "Yok" pembe görünüyor. Görünüm
betiğe değil kutunun işaretine (`:checked`) bağlı. Kutular `.alan`'ın dışında
duruyor, yoksa gizli işaret kutusu sayfayı genişletirdi (tuzak #14; `.cip input`
da bileşenin kendi kuralında sabitlendi).

- **Yeni tedavi hastanın en son girilen seçimiyle açılıyor.** Değer kişi başına
  geliyor (`db.son_bulas()`: tedavilerin tarih sırası, silme ekranından iptal
  edilen tedavi sayılmıyor). Formda "Hastanın önceki tedavisinden (2026-0012)
  geldi; tahlil değiştiyse düzeltin" yazıyor. Çözme ekranının "Yeni tedavi
  başlat" düğmesi ve hasta kartının "Çöz · yeni FET"i tedaviyi formsuz açıyor;
  onlar da aynı değeri alıyor. Gerekçe: bilinen bir HIV'li hastanın yeni
  FET'i uyarısız açılmasın. Bu kullanıcıya sorulmadan konan bir varsayılan.
- Hata dönüşünde seçim korunuyor (v6.21). Sürümden önce açılmış bir sekmenin
  formu bu bölümü taşımıyorsa (`bulas_formu` işareti yok), kayıtlı seçime
  dokunulmuyor. Listede olmayan bir kod formdan gelirse yazılmıyor. Göç
  çalışmamışsa kart hiç basılmıyor; basılsaydı seçim kayda girmeden kaybolurdu.

## Kimlik bandında uyarı

Tedavinin bütün ekranlarında, hastanın adının hemen altında, bandın koyu
zemininde kırmızı bir kutu çıkıyor: "⚠ BULAŞ HASTALIĞI / Kadın: Hepatit B /
Erkek: HIV, Sifiliz". Kapsanan ekranlar: tedavi ekranı, OPU'dan gebeliğe bütün
aşamalar, bitirme, fotoğraf ekleme, tedavi formunun düzenlemesi, tüpün çözme
formu (çözmenin yapıldığı tedavi). Yalnızca hastalığı olan kişi yazılıyor;
"Yok" ve girilmemiş olan susuyor.

- **Hasta kartında** (ve yeni tedavi formunda, taşıma ekranında) kişi başına
  en son girilen durum gösteriliyor, yanında hangi tedavide girildiği: "Kadın:
  Hepatit B · 2026-0012 tedavisinde".
- **Tek yerde**: `base.html` kimlik bandından hemen sonra `_bulas_bandi.html`'i
  basıyor. 41 şablonun bandına tek tek dokunulmadı (tuzak #1). Ölçü ekranın
  kendi değişkeni: `c` / `cycle_id` / `secili_cycle` o tedavinin kaydını,
  `hasta` en son girileni veriyor. Bandı olmayan ekranda (yazdırılan resmî
  form) hiç sorulmuyor.
- `db.bulas_uyarilari()` hata verirse boş döner: parça her hasta ekranında
  çalışıyor, onu bozmamalı.
- Tedavi ekranında ayrıca bir "Bulaş hastalığı" kartı var. Kart tam durumu
  gösteriyor: kişi başına Yok, girilmedi ya da hastalıklar.
- Renk `--tehlike` (#c62f2f, silme düğmesinin tonu), üzerindeki yazı sabit
  beyaz (~8:1).

Resmî formlara, Cryo Haritası'na ve tedavi listelerine girmiyor: istek
kimlik bandıydı.

## Deneme

Sahte veritabanında tarayıcıyla, telefon ve masaüstü genişliğinde:

- Göç açılışta kendiliğinden uygulandı. İkinci çalıştırmada "zaten var" dedi,
  liste üç değerde kaldı.
- Bir tedaviye "Kadın: Hepatit B, Erkek: Yok", ötekine "Erkek: HIV + Diğer:
  Sifiliz" yazıldı. Bant iki tedavinin denenen 9 ekranında doğru çıktı,
  bulaşsız tedavinin ekranlarında hiç çıkmadı. Hasta kartı iki kişiyi kendi
  tedavi numaralarıyla gösterdi.
- Yeni tedavi formu iki seçimle ve notlarıyla açıldı. Var olan lab no ile hata
  dönüşünde seçim korundu, kayıt iki kolonu da yazdı. "Çöz · yeni FET" ile
  açılan FET de aynı değerleri aldı.
- Kenar durumlar:
  - Eski sekme kayıtlı seçimi silmedi.
  - Uydurma kod ve virgüllü kod yazılmadı.
  - Hepsi kaldırılınca girilmedi oldu.
  - Yok ile hastalık birlikte gelince hastalık kaldı.
  - Değişiklik geçmişine düştü.
- Resmî form ekranlarında bant yok. Göçsüz veritabanında yardımcılar boş döndü.
- 84 ekran iki genişlikte hatasız, yatay kayma yok.

# v6.220 — Tedavi ekranının "Zamanlar" kartında OPU ve denüdasyon saati yok

Kullanıcı: *"Hastanın tedavisinde Opu bölümünde opu ile ilgili zamanlar var.
Bir önceki sayfa tedavi ana sayfasındaki zamanlar bölümünde denüdasyon ve opu
tarih ve saatleri gereksiz bu bilgiler ilgili yerlerde giriliyor zaten.
Zamanlardan bunları kaldır."*

Tedavi ekranının (`/cycle/{id}`) "Zamanlar" kartından OPU ve denüdasyon
satırları kalktı. İkisi kendi aşama ekranında giriliyor ve görünüyor: OPU
saati OPU ekranında, denüdasyon saati denüdasyon ekranında. Aşamaların sırası
ve aralarındaki süre aynı sayfanın zaman çizelgesinde duruyor. Kartta hCG
kaldı, çünkü hCG başka hiçbir ekranda gösterilmiyor (yalnızca tedavi formunda
giriliyor). Planlanan tarih de varsa kartta görünmeye devam ediyor. Kayıtlara
ve tedavi formuna dokunulmadı; değişen yalnızca ekrandaki iki satır.

Deneme: dört tedavinin ekranında kart yalnızca hCG'yi gösteriyor, zaman
çizelgesi yerinde. 84 ekran telefon ve masaüstü genişliğinde hatasız.

# v6.221 — Tedavi formunda da OPU ve denüdasyon saati yok

Kullanıcı (v6.220'den sonra): *"Düzenle değimde hala görünüyorlar"*

v6.220 saatleri yalnızca tedavi ekranının "Zamanlar" kartından kaldırmıştı.
Tedavinin "Düzenle" formunda (yeni tedavi formu da aynı şablon) OPU saati hâlâ
bir kutu olarak duruyordu. Artık iki formda da OPU saati yok. Denüdasyon saati
zaten görünmüyordu, gizli bir alanla dolaşıyordu; o alan da kalktı. "Zamanlar
ve OPU" kartında hCG saati ve OPU'da toplanan yumurta sayıları kaldı. Sayılar
da OPU ekranında giriliyor, ama kullanıcı yalnızca tarih ve saatleri söyledi;
istenirse onlar da kalkabilir.

## Kutuyu kaldırmak yetmezdi

Form kaydedilirken bütün alanları okuyup yazıyordu (`cycle_formu_oku()` +
`UPDATE cycle SET <bütün alanlar>`). Formda olmayan alan boş değer sayılırdı:
kutuyu kaldırmak, Düzenle'den her kayıtta OPU saatini silmek demekti. OPU günü
tedavinin günü de olduğu için tedavi numaraları da kayardı (v6.144). v6.220'ye
kadar denüdasyon saati bu yüzden gizli alanla dolaşıyordu. Ama gizli alanın
da bir kusuru vardı: Düzenle formu açıkken biri denüdasyon ekranında saati
değiştirirse, formu kaydetmek eski saati geri yazıyordu.

Bugün: `app.ASAMA_EKRANI_ALANLARI` (OPU ve denüdasyon saati) POST'ta yoksa
`cycle_formu_oku()` onları sözlüğe hiç koymuyor. Yeni tedavi ve Düzenle
rotaları yalnızca sözlükteki alanları yazıyor ve değişiklik geçmişine veriyor.
Formu kaydetmek bu iki kolona dokunmuyor. Bu sürümden önce açılmış bir sekme
alanları hâlâ taşıyor ve eskisi gibi yazıyor.

## Yeniden başlatılmamış program (tuzak #5)

Şablonlar diskten her istekte okunuyor, Python kodu yalnızca açılışta. `git
pull`'dan sonra program yeniden başlatılmazsa yeni form eski kodla çalışır.
Eski kod formda olmayan alanı boş sayıp yazar. Bu sürümün ilk gönderimi
(3324941) tam bunu yapıyordu. Bunu 10956b8'in (v6.220) kodu ve yeni şablonla
denedim: Düzenle'den bir kayıt OPU ve denüdasyon saatini NULL yaptı.

Düzeltme: program açılışta şablona `asama_ekrani_alanlari` adını veriyor.
Şablon bu adı görmezse, yani program eski ise, iki saati gizli alanla taşıyor
(v6.220'ye kadar denüdasyon saatinin yaptığı gibi) ve eski kod saatleri
yerinde bırakıyor. Program yeniden başlatılınca gizli alanlar da kalkıyor.
Aynı denemede güvenceli şablonla iki saat korundu.

## Deneme

Sahte veritabanında tarayıcıyla:

- Düzenle formunda ve yeni tedavi formunda OPU ve denüdasyon alanı yok. hCG
  ve yumurta sayıları duruyor.
- Protokol notunu değiştirip kaydetmek:
  - OPU ve denüdasyon saatini değiştirmedi.
  - Değişiklik geçmişine yalnızca notu yazdı.
- Form açıkken OPU saati değiştirildi, sonra form kaydedildi: yeni saat yerinde
  kaldı.
- Alanları taşıyan eski sekme POST'u saati yazdı.
- Bozuk hCG yılıyla hata dönüşü formda kaldı, saatlere dokunmadı.
- Yeni tedavi saatsiz açıldı. OPU ekranında girilen saat, Düzenle'den kayıttan
  sonra da yerinde.
- Yeniden başlatılmamış eski program: güvencesiz şablonla saatler silindi,
  bugünkü şablonla korundu (yukarıda).
- 84 ekran, telefon ve masaüstü genişliğinde hatasız. Tedavi formları iki
  genişlikte yatay kaymıyor.

# v6.222 — Tedavi formunda yumurta sayıları da yok; fotoğraf yakınlaştırma

Kullanıcı, v6.221'den sonra: *"Onlar da kalksın. Bir de yüklenen fotoğraflar
masaüstünde mouse orta düğmesi ile scroll ile büyüyüp küçülsün. Alt kısımda
artı eksi işareti ile de büyüyüp küçültsün. Mouse ile büyütülmüş fotoğraf
tutulup kaydırılabilsin."*

## Tedavi formu

OPU'da sağ ve sol overden toplanan yumurta sayıları da yeni tedavi ve Düzenle
formundan kalktı. Sayılar OPU ekranında giriliyor. Kartın adı "Zamanlar ve
OPU" yerine "Zamanlar" oldu; kartta yalnızca hCG saati var. Folikül sayısı
formda kaldı (Stimülasyon kartı): OPU ekranı onu yalnızca gösteriyor,
girmiyor.

Veri tarafı v6.221'in kuralı. İki sayı `ASAMA_EKRANI_ALANLARI`'na eklendi:
form onları taşımıyorsa kaydetmek bu kolonlara dokunmuyor. Form açıkken OPU
ekranında değişen sayı da formun kaydıyla geri gitmiyor.

Yeniden başlatılmamış programa karşı güvence artık alan alan çalışıyor. Şablon
her alanı çalışan programın listesinde arıyor. Listede olmayan alanı gizli
alanla taşıyor, çünkü o programın kodu formda olmayan alanı boş sayıp siler.
Böylece v6.221'in programı (listesinde yalnızca saatler var) sayıları, v6.220
ve öncesinin programı dört alanı da gizli taşıyor.

## Fotoğraf görüntüleyicisi

Fotoğrafa basınca açılan tam ekran görüntüleyici (`_buyutec.html`) bütün
ekranlarda ortak: aşama ekranları, tedavi ekranının Doktor Notu, taşıyıcı
sayfası, sperm dondurma onamları.

- **Fare tekerleği** büyütüp küçültüyor. İmlecin altındaki nokta yerinde
  kalıyor; baktığınız yer kaçmıyor. Dokunmatik yüzeyde iki parmakla kaydırma
  da aynı olay.
- **Alttaki − ve +** ekranın ortasından 1,5 kat küçültüp büyütüyor. Aralarındaki
  **Sığdır** görüntüyü ekrana sığan boyuna döndürüyor.
- En az ekrana sığan boy, en çok 8 kat. Sığan boydayken − ve Sığdır, 8 katta +
  soluk görünüyor.
- **Büyütülmüş görüntü fareyle tutulup sürükleniyor** (imleç el oluyor). Telefonda
  parmakla sürükleniyor, iki parmakla da büyüyüp küçülüyor. Görüntünün
  kenarı ekranın içine kaçmıyor.
- Önceki / sonraki fotoğrafa geçince ve görüntüleyici yeniden açılınca sığan
  boy. Büyük değilken görüntünün dışına basmak eskisi gibi kapatıyor.
  Sürüklemenin sonunda fareyi bırakmak kapatmıyor.

Eski "Yakınlaştır / Sığdır" düğmesi kalktı. O düğme görüntüyü tek bir boyda
(%220) açıp kaydırma çubuğuyla gezdiriyordu; − / + ile tekerlek onun yerini
aldı.

Nasıl yapıldı: görüntü CSS `transform` ile büyüyor. `transform-origin`
açıkça yazıldı (v6.109'un dersi). Görüntünün çerçevesi kaydırma çubuğu
açmıyor. Dokunmayı betik yönetiyor (`touch-action: none`). Tıklama ya da
sürükleme işaretçiyi yakalamıyor (`setPointerCapture`): yakalanan tıklamanın
hedefi çerçeve olurdu, görüntüye basmak görüntüleyiciyi kapatırdı.

## Deneme

Sahte veritabanında tarayıcıyla:

- Tedavi formu:
  - Yeni tedavi ve Düzenle formunda dört alanın (OPU saati, denüdasyon
    saati, iki sayı) hiçbiri yok.
  - Kaydetmek dördünü de değiştirmedi. Değişiklik geçmişine yalnızca
    değiştirilen not yazıldı.
  - Açık formun kaydı OPU ekranında değişen sayıyı ezmedi. Eski sekme
    sayıları yazdı.
  - Yeni tedavi dört alan boş açıldı. OPU ekranında girilen saat ve sayılar
    Düzenle kaydından sonra yerinde; tedavi ekranının özeti toplananı
    gösteriyor.
  - Yeni şablonlar yeniden başlatılmamış v6.221 ve v6.220 programıyla
    çalıştırıldı. v6.221'in programında iki sayı, v6.220'ninkinde dört alan
    gizli taşındı. Kaydetmek ikisinde de dördünü korudu.
- Görüntüleyici, masaüstünde (1280 px) 22 kontrol:
  - Tekerlek büyüttü; imlecin altındaki nokta yerinde kaldı (görüntüdeki
    yeri 0,5451 → 0,5451).
  - Sürükleme görüntüyü fare kadar kaydırdı. Uzağa sürüklenince kenar
    çerçevede durdu.
  - Bırakmak da görüntüye tıklamak da kapatmadı.
  - + 1,5 / 2,25 kat verdi, − ve Sığdır geri döndürdü. 8 katta + soluk oldu.
    Tekerlekle küçültmek sığan boyda durdu.
  - Dışarıya tıklamak ve Escape kapattı.
  - Önceki / sonraki fotoğrafa geçince yakınlaştırma sıfırlandı (aşama ekranı
    ve Doktor Notu).
- Görüntüleyici, telefonda (390 px, dokunma):
  - + düğmesi çalıştı.
  - Parmakla sürükleme kaydırdı. Görüntünün boyu ekrana sığarken dikeyde
    kaymadı.
  - İki parmakla açmak parmak aralığı kadar (3 kat) büyüttü; parmakların
    ortası yerinde kaldı.
  - Alt çubuk tek satır, taşmadı.
- 84 ekran, telefon ve masaüstü genişliğinde hatasız.

# v6.223 — Ana ekranda bulaş hastalığı olan hastanın adının yanında kırmızı nokta

Kullanıcı: *"Bulaş kayıtlı hasta programın ana sayfasında görünüyorsa burada
da adının yanında ufak kırmızı nokta ile bunu uyarsın."*

Ana ekranın üç kartında (Devam Eden, Bugün Biten, Yaklaşan Tedaviler) bulaş
hastalığı kayıtlı tedavinin satırında hastanın adının hemen yanında küçük
kırmızı bir nokta var. Kartların "Tümü" sayfalarında da var (`/devam-eden`,
`/bitenler`, `/yaklasanlar`): onlar aynı listenin kartta görünmeyen devamı,
altıncı satırdaki hasta da uyarılmalı. Fare noktanın üstünde durunca hangi
kişide ne olduğu yazıyor: "Bulaş hastalığı: Kadın: Hepatit B · Erkek: HIV".
Ekran okuyucu da aynı metni okuyor. Ayrıntı yine tedavinin ekranında,
kimlik bandının altındaki kırmızı kutuda (v6.219).

- **Ölçü tedavinin kendi kaydı**, tedavinin bandınınki (v6.219). Noktalı
  satıra basınca açılan ekranda bant var; noktasız satırın ekranında yok.
  Yalnızca hastalığı olan kişi sayılıyor: "Yok" ve girilmemiş nokta vermiyor.
- **Satır başına sorgu yok.** Listenin sorgusu (`cycle_listesi()`) tedavinin
  iki bulaş kolonunu da okuyor. `db.bulas_isaretle()` satırlara uyarıyı
  sorgusuz ekliyor; hastalıkların adları için liste yalnızca hastalıklı bir
  satır varsa bir kez okunuyor. `/bitenler` binlerce satır olabiliyor.
- **Hasta kayıtları ekranının ay listesinde nokta yok.** O liste de aynı
  satır parçasını kullanıyor, ama istenen ana ekrandı (v6.219'da listeler
  bilerek dışarıda bırakılmıştı). Satır parçası `bulas=True` verilince nokta
  basıyor; istenirse ay listesine de yalnızca bu eklenir.
- **Renk**: `--tehlike`nin (#c62f2f) aynı tonu, biraz açık (#d65252,
  `--tehlike-isaret`). Düz `--tehlike` kart zemininde 2,9:1 kontrast
  veriyor, metin dışı bir işaret için istenen 3:1'in altında. Bu ton kart
  zemininde ~4:1.
- Göç çalışmamış veritabanında (kolonlar yok) liste eskisi gibi, nokta yok.
  Elle yazılan "Diğer" hastalık ipucunda metin olarak kalıyor (kaçışlı).

## Deneme

Sahte veritabanında tarayıcıyla, masaüstü (1280 px) ve telefon (390 px)
genişliğinde:

- Üç kartın satırları: nokta yalnızca hastalıklı tedavilerde (7 satırın
  6'sında). Bugün biten ve yaklaşan birer tedavi ayrıca hazırlandı; kartında
  noktalı çıktı.
- "Tümü" sayfaları: 6, 9 ve 1 satırın hepsi doğru.
- Hasta kayıtları ekranı: 13 satır (ay listesinin 7'si ve Tüm Hastalar), nokta yok.
- İpucu kişi kişi, listenin etiketleriyle. Elle yazılan HTML metin olarak
  kaldı.
- Nokta 10 px, renk doğru, sayfa yatay kaymıyor.
- Noktalı satırın tedavisinde bant var, noktasızınkinde yok.
- Kolonsuz (göçsüz) veritabanında beş liste kipi hatasız.
- 84 ekran iki genişlikte hatasız.

# v6.224 — Ay listesinde de bulaş noktası

Kullanıcı: *"Ay listesinde de olsun."*

Hasta kayıtları ekranının ay listesinde de bulaş hastalığı kayıtlı tedavinin
satırında adın yanında aynı kırmızı nokta var (v6.223). Ölçü, renk ve ipucu
ana ekranınkiyle aynı: tedavinin kendi kaydı, tedavi ekranının bandının
ölçüsü. Aynı hastanın bir tedavisinde nokta olup ötekinde olmayabilir; her
satır kendi tedavisini söylüyor.

- Değişen tek satır `hastalar.html`: ay listesi `satir(s, "ay", bulas=True)`
  çağırıyor. Liste zaten `cycle_listesi()`'nden geliyor, satırların bulaş
  bilgisi v6.223'ten beri hazırdı; yeni sorgu yok.
- **Aynı ekranın Tüm Hastalar'ı ve arama sonuçları noktasız.** Onlar hasta
  satırı, tedavi satırı değil; noktanın ölçüsü bir tedavinin kaydı. İstenen
  ay listesiydi.

## Deneme

Sahte veritabanında tarayıcıyla, masaüstü (1280 px) ve telefon (390 px)
genişliğinde:

- Ay listesi: 7 satırın noktaları tedavilerin kayıtlarıyla birebir (5
  noktalı, 2 noktasız). İpucu ana ekranınkiyle aynı.
- Nokta satırın içinde, yanındaki "Hasta kartı" düğmesine binmiyor. Çok uzun
  bir adla 320 px'te nokta adın altına iniyor, sayfa yatay kaymıyor.
- Tüm Hastalar'da nokta yok. Ana ekranın kartları ve Tümü sayfaları eskisi
  gibi.
- 84 ekran iki genişlikte hatasız.

# v6.225 — PGT: tedavinin işareti, biyopsi ekranı, PGT numarası

Kullanıcı: *"Bazı hastalarda PGT yapılıyor. Tedavinin başında PGT
yapılacağına dair laboratuvarda formunun üstüne yazıyorum. Tedavi bitene
kadar üstünde PGT yapılacağı yazıyor. Bu hastanın oluşursa embriyolarından
biyopsi yapıyorum ve parçaları genetiğe gönderiyorum. Embriyoları
numaralandırıp dondurup saklıyorum. Daha sonra genetik sonuç gelince sonucu
dosyasına koyup hangi embriyolar genetik incelemede sorunsuz çıkarsa onu
belirleyip FET tedavisinde ona bakıp sorunsuz embriyoları transfer
ediyorum."*

Kullanıcının cevapları: biyopsi blastokistte (trofektoderm); genetiğe giden
tüpte ve raporda numara biyopsi sırasıyla 1'den, ekranda "PGT 1"; PGT-A,
PGT-M, PGT-SR ve HLA'nın hepsi olabiliyor; "sorunsuz" kararını kendisi
işaretliyor; sorunlu embriyo hastaya göre tankta kalıyor ya da imha
ediliyor; imha kaydı bütün tüplerde olsun.

Bu sürüm akışın ilk yarısı: işaret, biyopsi, numara, dondurma. Genetik
sonucun girilmesi, raporun dosyaya eklenmesi, "sorunsuz" kararı ve FET'te
uyarı v6.226'da; tüp imhası v6.227'de.

**Tedavinin başında.** Tedavi formunda "PGT" kartı: PGT-A, PGT-M, PGT-SR,
HLA (birden çoğu seçilebiliyor) ve kısa bir not (hastalık, translokasyon,
genetik laboratuvarı). Seçilince:

- tedavinin bütün ekranlarında kimlik bandının altında mavi PGT kutusu:
  testler, not, biyopsi yapıldıysa kaç embriyoya ve numaraları
  ("3 embriyoya biyopsi yapıldı · PGT 1–3"). Bulaş uyarısının kırmızısından
  ayrı renk: tehlike değil, "bu tedavide biyopsi var" bilgisi;
- ana ekranın kartlarında, Tümü sayfalarında, ay listesinde ve hasta
  kartının tedavi satırında adın yanında "PGT" rozeti -- kâğıtta formun
  üstüne yazılan şey;
- aşamalara blastokistin arkasında **Biyopsi** ekleniyor.

Yeni tedavi PGT'yi önceki tedaviden almıyor (bulaş hastalığının tersi): PGT
o tedavinin kararı. Not yazılıp test seçilmezse form soruyor; not
kaybolmuyor.

**Biyopsi ekranı** öteki aşama ekranlarının düzeninde: üstte embriyolar
(biyopsi yapılanda "PGT 2", yapılmayanda blastokist skoru), seçilenin
fotoğrafı ve örnek kodu, altında bilgi kartı ya da form. Listede bu
tedavide blastokist değerlendirmesi olan embriyolar var; blastokistte
arrest yazılan yok (vitrifikasyonun kuralı). Formda:

- **PGT numarası**: program sıradakini öneriyor (en büyüğün bir fazlası);
  değiştirilebilir. İki telefon aynı öneriyi aynı anda kaydederse ikincisi
  sıradaki boş numarayı alıyor; elle yazılan bir numara başka embriyoda
  varsa kayıt reddediliyor, form açık kalıyor.
- **Biyopsi günü** (öntanımı embriyonun bu tedavideki son blastokist günü),
  işlem saati (elle değiştirilebilir), not. Biyopsinin tipi (trofektoderm)
  kayıtta, seçici yok.
- "Kaydet ve sonraki embriyo": biyopsisi olmayan sıradaki embriyo.
- Biyopsi kaydı silinebiliyor (iptal işareti, geçmişte kalır); genetik
  sonucu girilmiş biyopsi silinmiyor (v6.226).

Kayıt şemanın ilk sürümünden beri hazır duran biyopsi olayı: numara
`biy_tup_etiketi`'nde. Olay, öteki değerlendirmeler gibi embriyonun kendi
tedavisine yazılıyor; hangi tedavide yapıldığı saatten çıkıyor (FET (3→5)'te
çözülüp biyopsiye alınan embriyo o tedavinin). Yazılan saatte embriyo başka
bir tedavi için çözülmüşse kayıt o tedavinin sayılır, bu ekrandan
kaybolurdu: program bunu kaydederken soruyor, öyleyse kaydı geri alıp
"İşlem saati bu tedaviye düşmüyor" diyor. Bir embriyonun her tedavide tek
biyopsisi var; sonucu çıkmayan embriyo başka bir tedavide yeniden biyopsiye
alınabiliyor, geçerli olan en sonuncusu.

**Dondurma.** Vitrifikasyon ekranında biyopsili embriyonun satırında
"PGT 2 · sonuç bekleniyor". İki biyopsili embriyo aynı tüpe seçilince uyarı
çıkıyor: sonuçları farklı çıkarsa tüpten yalnızca biri çözülemez. Engel
değil: "Yine de aynı tüpe koy" işaretlenirse kaydediliyor; sunucu da aynı
şeyi soruyor.

**Tüplerde PGT.** Taşıyıcı sayfası, tüpün çözme formu, Cryo Haritası'nın
goblet sayfası, yeri belirsizler ve hasta kartının "Dondurulmuş örnekler"i
tüpteki embriyonun PGT numarasını ve durumunu yazıyor. Hepsi tek bir
parçadan (`_pgt.html`) ve tek bir sorgudan (`db.biyopsi_bilgisi()`).

**Formlar ve çizelge.** Embriyoloji Özet'in NOTLAR kutusuna, genel
bulguların arkasına bir PGT satırı: "PGT: PGT-A, PGT-M (Talasemi) · 3
embriyoya biyopsi, 5/6. gün: PGT 1–3" (biyopsi yoksa "biyopsi yapılmadı").
Satır sarılırken numara bölünmüyor. Tedavi ekranının özet kutusunda
"Biyopsi sayısı", zaman çizelgesinde Biyopsi satırı. ART Lab formunda PGT
kutusu yok, bir şey eklenmedi.

**İzin.** Biyopsi ekranı blastokistin izniyle açılıyor (aynı personel);
ayrı bir modül açılmadı. İstenirse ayrılır.

**Göç 058**: tedavinin iki kolonu, sonucun hangi biyopsinin olduğu
(`pgt_sonuc.biyopsi_id`, v6.226 için), test ve sonuç listeleri (PGT-A için
şemanın kendi listesi: Öploid, Anöploid, Mozaik, Sonuç yok, No-call; PGT-M:
Sağlam, Taşıyıcı, Etkilenmiş; PGT-SR: Dengeli, Dengesiz; HLA: Uyumlu,
Uyumsuz), fotoğraf aşamalarına "Biyopsi", biyopsi satırlarının dizini. Göç
çalışmamışsa PGT kartı, bant ve aşama görünmüyor; öteki her şey eskisi gibi.

**Yeniden başlatılmamış program** (tuzak #5): yeni şablonlar eski Python'la
açılınca yeni işlevleri tanımıyor. PGT bandı her ekranda çağrıldığı için
korumasız bir çağrı bandı olan her ekranı bozardı; şablonlar işlevin var
olup olmadığına bakıyor.

## Deneme

Sahte veritabanında tarayıcıyla, masaüstünde ve telefonda:

- Tedavi formunda PGT-A + PGT-M ve not; kayıt, bant (tedavi ve aşama
  ekranında), Biyopsi aşamasının yeri, PGT'siz tedavide bant ve aşama yok.
- Biyopsi listesi: bu tedavide blastokist değerlendirmesi olan üç embriyo;
  arrest yazılan yok.
- Başka bir tedavi için çözülmüş embriyoya "şimdi" saatiyle biyopsi:
  reddedildi, kayıt yazılmadı, form açık. Doğru saatle kaydedildi.
- Numaralar biyopsi sırasıyla 1, 2, 3; "kaydet → sıradaki"; gün öntanımı
  embriyonun blastokist günü; şerit ve bilgi kartı PGT numarasını yazıyor.
- Dolu numara elle yazılınca reddedildi; 0 numara sunucuda reddedildi.
- Silme; aynı öneri iki kez gönderilince ikincisi sıradaki boş numarayı
  aldı.
- Bant "3 embriyoya biyopsi yapıldı · PGT 1–3"; özet kutusunda Biyopsi
  sayısı 3; zaman çizelgesinde Biyopsi.
- Dondurma: adaylarda PGT numarası; iki biyopsili embriyoda uyarı ve onay
  kutusu, onaysız kayıt sunucuda reddedildi (tüp açılmadı); tek tek
  donduruldu.
- Taşıyıcı sayfası, çözme formu, goblet sayfası, hasta kartı, dondurulmuş
  kartı "PGT 2 · sonuç bekleniyor".
- Özet formunun NOTLAR'ı; numara iki satıra bölünmedi.
- PGT kartı olmayan form (eski sekme) PGT'ye dokunmadı; değişiklik
  geçmişinde PGT alanları.
- Göç çalışmamış veritabanı (göçü atlayan başlatıcıyla): 17 ekran hatasız,
  PGT arayüzü yok, tedavi Düzenle ve yeni tedavi kaydı çalışıyor.
- v6.224'ün programı bu sürümün şablonlarıyla: aynı 17 ekran hatasız.
- Telefonda (390 px) dokuz ekran yatay kaymıyor; 84 ekran iki genişlikte
  hatasız; bulaş noktası ve tedavi formu denemeleri eskisi gibi.
