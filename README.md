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
