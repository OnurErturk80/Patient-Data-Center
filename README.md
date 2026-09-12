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
