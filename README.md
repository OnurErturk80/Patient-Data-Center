# Lab Kayıt — v0.1

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
