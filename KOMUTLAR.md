# Komut kartı

Ara sıra lazım olan komutlar, tek sayfada. Bir kararın **nedenini**
arıyorsan `CLAUDE.md` (kurallar) ve `README.md` (sürüm sürüm gerekçeler).

Hepsi **proje klasörünün kökünde** çalışır:

```
cd "Patient Data Center"          # Mac
cd "C:\...\Patient Data Center"   # Windows — kendi yolun
```

Mac'te `python3`, Windows'ta `python`. Aşağıda Mac hali yazılı.

---

## Programı çalıştır

```
python3 baslat.py
```

Durdurmak: **Ctrl+C**. (Eski yol `python3 -m uvicorn app:uygulama --host
0.0.0.0 --port 8000` de çalışır ama **güvenli adres (HTTPS) açılmaz** --
Android'de uygulama gibi açılış için `baslat.py` gerekir.)

`baslat.py` iki adres açar (v6.196): `http://...:8000` (eskisi gibi) ve
`https://...:8443` (güvenli, Android için). Açılışta terminale ikisini de
yazar.

Kendi bilgisayarında: <http://localhost:8000>

**Telefondan girmek için** bu makinenin iç ağ adresi lazım:

```
ipconfig getifaddr en0        # Mac (kablosuz)
ipconfig                      # Windows — "IPv4 Adresi" satırı
```

Çıkan adresle: `http://192.168.1.42:8000` (numara sizde farklı olacak).
Telefon aynı Wi-Fi'da olmalı. Program açık kalmalı.

**Ağ erişimi** (v6.203): Yönetici → **Ağ erişimi**. "Yalnızca bu bilgisayar"
seçiliyken telefonlar ve öteki bilgisayarlar bağlanamaz (yalnızca "Program
yalnızca kurulu olduğu bilgisayarda açık" sayfasını görürler); "İç ağa açık"
seçilince bağlanırlar. Hemen geçerli, programı yeniden başlatmak gerekmez.
Ayar her bilgisayarın kendisine özel. **Yeni bir bilgisayara kurulan program
kapalı başlar**; bugünkü Mac ve klinik kurulumu açık kaldı. Kapalıyken açmak
için programın kurulu olduğu bilgisayarda `http://localhost:8000` adresinden
girilir.

---

## Telefona uygulama olarak ekleme ve HTTPS (v6.195, v6.196)

Yönetici paneli → **Telefona ekle**: karekodlar ve adımlar orada, yazdırıp
laboratuvara asılabilir.

- **iPhone**: ana karekodu okut → Safari'de paylaş → "Ana Ekrana Ekle".
- **Android** (her telefonda bir kez): Android kartındaki karekodu okut →
  açılan "Güvenlik sertifikası" sayfasında sertifikayı indir ve Ayarlar'dan
  yükle (sayfa adım adım söylüyor, yüklenince yeşil "güvenilir" yazar) →
  "Güvenli adresi aç" → Chrome ⋮ → "Uygulamayı yükle".

Sertifika bu bilgisayarın veri klasöründe, `sertifika/` altında; program her
açılışta kendisi denetler, adres değişirse yeniler. Durumunu görmek için:

```
python3 sertifika.py
```

`sertifika/` klasörünü silme, elle başka bilgisayara kopyalama, git'e ekleme:
silinirse yeni sertifika üretilir ve **bütün telefonlara yeniden yüklemek**
gerekir. Yeni bilgisayara **geçerken** taşımanın yolu `tasi.py ... sertifika`
(aşağıda "Yeni bilgisayara geçiş").

HTTPS'i kapatmak (yalnızca düz adres): `LAB_HTTPS=0 python3 baslat.py`
(Windows: `set LAB_HTTPS=0` sonra `python baslat.py`).

---

## Veri taşıma — USB (`tasi.py`)

Kod git ile gider gelir; **veri sadece USB ile**. Yön önemli.

```
python3 tasi.py durum  /Volumes/USB     karşılaştır, hiçbir şey yapma
python3 tasi.py disari /Volumes/USB     bu makineden USB'ye
python3 tasi.py iceri  /Volumes/USB     USB'den bu makineye
```

Windows'ta yol `E:\` gibi olur: `python tasi.py durum E:\`

**Rutin — bunu ezberle:**

| | |
|---|---|
| Makineden **kalkarken** | `python3 tasi.py disari <usb>` |
| Makineye **otururken** | `python3 tasi.py iceri <usb>`, sonra sunucuyu yeniden başlat |

- `iceri` öncesi **uygulamayı durdur** (Ctrl+C) — açık dosyanın üzerine yazılamaz.
- Emin değilsen önce `durum` çalıştır; hiçbir şeye dokunmaz.
- `iceri`, bu makinedeki veri USB'dekinden yeniyse **durur ve onay ister**.
- Üzerine yazmadan önce `lab_ONCEKI_<tarih>.db` yedeği bırakır.
- **Aynı anda tek makinede kayıt gir.** Birleştirmenin yolu yok.

---

## Kurulum dosyası (v6.204)

Yeni bir bilgisayara Python ve git kurmadan: Windows için tek bir kurulum
dosyası (`.exe`), Mac için uygulama (`.dmg`). GitHub'da üretiliyor:

1. GitHub'da depo → **Actions** → solda **Paketler** → sağda **Run workflow**.
   Hangi makineler: Windows, Mac (Apple Silicon: M1 ve sonrası), Mac (Intel,
   eski Mac'ler; varsayılan kapalı). **Run workflow**.
2. 15–25 dakika sürer; her makinede program açılıp denenir. Bitince çalışmanın
   sayfasında en altta **Artifacts**: `PatientDataCenter-Windows-6.204`,
   `PatientDataCenter-Mac-arm64-6.204` ... İndir (zip içinde kurulum dosyası).
   Dosyalar 14 gün durur.
3. Depo özel olduğu için her çalışma hesabın aylık ücretsiz dakikasından düşer
   (Windows 2, Mac 10 kat sayılır; Windows + Mac ~150 dakika). Yalnızca
   gerekince çalıştır.

**Windows'ta kurmak**: dosyaya çift tıkla. İmzasız olduğu için Windows
"Windows kişisel bilgisayarınızı korudu" der: **Ek bilgi** → **Yine de
çalıştır**. Yönetici izni ister. Kurulum programı açılışta kendiliğinden
başlayacak şekilde ayarlar (Görev Zamanlayıcı, kimse oturum açmadan),
güvenlik duvarında 8000 ve 8443'ü yerel ağa açar, sonunda tarayıcıyı açar.
Başlat menüsünde: Patient Data Center (tarayıcıda açar), Veri klasörü,
Program günlüğü, kaldır. Veri: `C:\ProgramData\PatientDataCenter`.
**Güncellemek**: yeni kurulum dosyasını çalıştır; çalışan program durdurulup
yenisi başlatılır, veri yerinde kalır. Kaldırınca da veri kalır.

**Mac'te kurmak**: `.dmg`'yi aç, "Patient Data Center"ı **Applications**
klasörüne sürükle, orada çift tıkla. İlk açılışta macOS izin ister (imzasız):
"açılamadı" penceresini kapat, **Sistem Ayarları → Gizlilik ve Güvenlik** →
en altta **Yine de Aç** (eski macOS'ta: sağ tık → Aç). Program arka planda
çalışır, Dock'ta simgesi yoktur; tarayıcıyı yeniden açmak için uygulamaya
yine çift tıkla. Oturum açılınca kendiliğinden başlar (kapatmak: Sistem
Ayarları → Genel → Oturum Açma Öğeleri). **Güncellemek**: yeni uygulamayı
Applications'a sürükle ("Değiştir"), ona çift tıkla: eski sürüm kapanır,
yenisi açılır. Veri: `~/Library/Application Support/PatientDataCenter`.
Kapatmak gerekirse: Etkinlik Monitörü → PatientDataCenter → Çık.

**İlk açılış**: veritabanı olmadığı için program kurulum ekranıyla açılır
(yalnızca o bilgisayardan):
- **Eski bilgisayardan taşı** -- aşağıdaki geçişin 2. adımında hazırlanan USB
  klasörü (`lab_tasima`), eski programın klasörü ya da yedek klasörü.
  **Listeden seç** ile klasörü bul, **Klasöre bak**, veritabanını seç (sayılar
  ve son kayıt yazar), **Veriyi al**. Fotoğraf arşivi ve sertifika da gelir.
- **Yeni laboratuvar kur** -- ilk yönetici hesabı.

Program **ağa kapalı** başlar: telefonlar için Yönetici → Ağ erişimi.

---

## Yeni bilgisayara geçiş (program başka bilgisayara taşınıyor)

Programın çalıştığı bilgisayar değişiyorsa (eski bilgisayar emekli oluyor).
Günlük Mac ↔ klinik taşıması bu değil, o yukarıdaki rutin.

**Eski bilgisayarda**

1. Programı durdur (Ctrl+C).
2. Veriyi ve telefonların sertifikasını USB'ye al:
   ```
   python3 tasi.py disari /Volumes/USB sertifika     # Mac
   python  tasi.py disari E:\ sertifika               # Windows
   ```
   `sertifika` sözü telefonların güvendiği sertifikayı da götürür: Android
   telefonlara sertifika yeniden yüklenmez.

**Yeni bilgisayarda -- kurulum dosyasıyla (v6.204, kolay yol)**

3. Kurulum dosyasını çalıştır (yukarıdaki bölüm). Tarayıcı kurulum ekranıyla
   açılır: **Eski bilgisayardan taşı** → USB'deki `lab_tasima` → **Veriyi al**.
   USB'deki sertifika kopyası kendiliğinden silinir.
4. Aşağıdaki 6–9. adımlar (Klasörler, Ağ erişimi, telefonlar).

**Aynı bilgisayarda git'le çalışan programdan kurulum dosyasına geçmek**:
önce eski programı kapat (Ctrl+C; ikisi aynı anda çalışamaz, kurulan program
bunu söyler). Kurulum ekranında **Eski bilgisayardan taşı** → eski programın
klasörü (içinde `lab.db` olan). Eski klasöre dokunulmaz, yedek olarak kalır;
bir daha `python3 baslat.py` çalıştırma.

**Yeni bilgisayarda -- Python ve git ile**

3. Programı kur: Python 3.10+, sonra
   ```
   git clone https://github.com/OnurErturk80/Patient-Data-Center.git "Patient Data Center"
   cd "Patient Data Center"
   pip install fastapi uvicorn jinja2 python-multipart
   ```
   (Mac'te `pip3`, `python3`.)
4. USB'den al: `python3 tasi.py iceri /Volumes/USB` (Windows: `python tasi.py
   iceri E:\`). Veritabanı, fotoğraf arşivi ve sertifika gelir; USB'deki
   sertifika kopyası kendiliğinden silinir.
5. Başlat: `python3 baslat.py`. Program **ağa kapalı** açılır; bu bilgisayarda
   `http://localhost:8000` ile gir.
6. Yönetici → **Klasörler**: kamera, arşiv, yedek ve Cryo haritası klasörleri
   (bu bilgisayarın kendi yolları; eski bilgisayarınkiler gelmez).
7. Yönetici → **Ağ erişimi** → "İç ağa açık".
8. Telefonlar: bilgisayarın IP'si değiştiyse telefonlardaki simgeler eski
   adresi tutar. Yönetici → **Telefona ekle** yeni adresi kendisi gösterir,
   simgeyi her telefonda yeniden ekle. **Daha kolayı**: modemden ya da bilgi
   işlemden yeni bilgisayara eskisinin IP'sini verdirmek (DHCP rezervasyonu)
   -- o zaman telefonlarda hiçbir şey yapmak gerekmez.
9. Eski bilgisayar artık sunucu olmayacaksa oradaki `sertifika/` klasörünü sil.

Cryo haritasının Excel'ini taşımaya gerek yok: program açılınca veritabanından
yeniden yazıyor (laboratuvarın kendi Excel şablonu veritabanında).

---

## Yedek

```
python3 yedek.py                 # bu makinenin ayarlı klasörüne
python3 yedek.py ~/lab_yedek     # elle hedef vererek
python  yedek.py E:\yedek        # Windows, klinik
```

Hedef **farklı bir diskte** olmalı — aynı disk bozulursa yedek de gider.

**Program açıkken yedek kendiliğinden de alınır** (v6.216): Cryo Haritası'nda
bir değişiklik olunca (dondurma, çözme, taşıma, yer), değişiklikler bittikten
bir iki dakika sonra (sürerse en geç on dakikada) yedek klasörüne — "Şimdi
yedekle"nin aynısı. Durumu: Yönetici → Yedekleme → "Otomatik yedek".

- Yedek klasörü yoksa (disk takılı değil) alınmaz, disk takılınca alınır.
  Klasöre hiç yedek alınmadıysa bir kez "Şimdi yedekle"ye bas: klasörü o açar.
- Cryo Haritası'nın değişmediği günlerde otomatik yedek alınmaz.
- Saklanan: son 24 saatin bütün yedekleri, 14 güne kadar her günün sonuncusu,
  daha eskide her ayın ilki.

**Her gün 14:00'te "Tüm veriler" Excel'i** Cryo haritası klasörüne yazılır
(Yönetici → Klasörler → "Cryo haritası (Excel)"; Cryo_Haritasi.xlsx'in yanı):
`Tum_Veriler_2026-09-29.xlsx` gibi, son 30 gün. Yönetici panelindeki "Tüm
veriyi Excel'e aktar"ın aynısı — **bütün hasta kayıtları içinde**, klasörü
herkesin açabildiği bir yere koyma. 14:00'te program kapalıysa o gün
açıldığında yazılır.

**Yedekten geri yükledikten sonra programı yeniden açmana gerek yok**
(v6.145). Geri yükleme (`/yedekleme` → "Yedekten geri yükle") yedek eski bir
sürümdense eksik veritabanı güncellemelerini hemen kendisi uygular ve
mesajında kaç tane uygulandığını söyler. Terminalden geri yükleme de
(`python3 geri_yukle.py geri-yukle <dosya>`) aynısını yapar.

---

## Göçler (şema güncelleme)

**Artık elle bir şey yapmana gerek yok** (v6.49): program her açılışta
bekleyen güncellemeleri kendisi uyguluyor. `git pull` ya da `tasi.py iceri`
sonrası sunucuyu yeniden başlatman yeter. Durumu `/yonetim` panelindeki
**Veritabanı güncellemeleri** kartından görürsün.

Terminalden kontrol etmek istersen:

```
python3 goc_hepsi.py
```

Tekrar tekrar çalıştırmak zararsız; uygulanmış olanlar atlanıyor.

---

## Kullanıcı ve şifre

Normal yol **arayüzden**: `/yonetim` → Kullanıcılar. Aşağıdakiler yönetici de
giremediğinde kullanılır.

```
python3 kullanici.py                          # kim var, kim aktif
python3 kullanici.py sifre onur                # şifre sıfırla
python3 kullanici.py yeni                      # yeni kullanıcı
python3 kullanici.py rol onur yonetici         # yönetici yap
python3 kullanici.py pasif onur                # girişi kapat
python3 kullanici.py aktif onur                # geri aç
```

`yonetici` **Türkçe karakter olmadan** yazılır — `yönetici` çalışmaz.
Kullanıcı adını `<...>` içine alma, düz yaz.

---

## Veri nerede duruyor

`lab.db`, `yerel_ayar.json`, `arsiv/`, `snapshot/`, `sertifika/` ve
`cryo_harita/` (Excel haritası, v6.191; her günün "Tüm veriler"i, v6.216)
**veri klasöründe**. Arşiv, kamera,
yedek ve Cryo haritası klasörü Yönetici → Klasörler'den başka bir yere
alınabilir (Cryo haritası v6.203'ten beri).
Bugünkü kurulumlarda bu proje klasörünün kendisi (kodun yanında `lab.db`
varsa orası kullanılıyor). Kurulum dosyasıyla kurulan programda (v6.204)
işletim sisteminin veri klasörü: Windows'ta `C:\ProgramData\PatientDataCenter`,
Mac'te `~/Library/Application Support/PatientDataCenter`. Nerede olduğunu
görmek için (git ile çalışırken):

```
python3 -c "import db; print(db.VERI_KOK)"
```

Başka bir klasörle çalıştırmak (deneme için):

```
LAB_VERI=/bir/klasor python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
```

---

## Eski Access kayıtlarını içeri alma (`aktar_access.py`)

Program öncesi tutulan Access kayıtlarını programa alır. `.accdb` okunmuyor
— Access'ten **CSV** olarak dışa aktar (beş adımlık yönerge betiğin
başında, `python3 -c "import aktar_access; print(aktar_access.__doc__)"`).

**CSV'ler başka bir klasördeyse** (ör. masaüstündeki "Hasta Kayıtları"),
o klasörde kal ve betiğe **tam yol** ver — `can't open file ...
aktar_access.py` hatası betiğin o klasörde olmadığını söylüyor. Veritabanı
betiğin kendi klasöründen bulunuyor, komutun çalıştığı klasörden değil;
CSV ve `tarih_duzeltme.txt` ise çalıştığın klasörden okunuyor. Windows'ta:

```
cd /d "C:\Users\...\Desktop\Hasta Kayıtları"
set P=C:\...\Patient Data Center
python3 "%P%\aktar_access.py" liste kaynak=TEMMUZ temmuz.csv
```

**Önce `liste` ile bak, hiçbir şeye dokunmuyor:**

```
python3 aktar_access.py liste kaynak=TEMMUZ temmuz.csv
```

Tarihler doğru okunmuş mu, hangi hastalar yeni açılacak — hepsi orada.
Sonra yedek al (`/yedekleme` → "Şimdi yedekle") ve gerçekten yaz:

```
python3 aktar_access.py kaynak=TEMMUZ temmuz.csv
```

`AKTAR` yazınca uyguluyor. İki kez çalıştırmak güvenli: aktarılmış satır
atlanıyor.

**Eski bir ayı sonradan aktarmak sorun değil** (v6.144): hastanın tedavileri
tarih sırasına göre yeniden numaralanır, en eski tedavi 1. olur. Rapor bunu
söyler: `hastanın 1. tedavisi — tarih sırasına göre kayanlar: 2026-0xxx 1.→2.`
Lab kayıt numaraları (2026-0xxx) değişmez.

**`kaynak=<AD>` ne işe yarıyor:** her Access dosyası kendi kayıtlarını
1'den numaralandırıyor. Etiket olmadan ikinci dosyanın ilk satırları
birincinin numaralarıyla çakışır ve "zaten aktarılmış" sanılıp **sessizce
atlanır**. Her dosyaya kendi adını ver (`kaynak=TEMMUZ`, `kaynak=HAZIRAN`).
Unutursan betik durur, yazmaz.

> **Ağustos 2026 dosyası etiketsiz aktarıldı; onu yeniden çalıştırırsan
> `kaynak=` VERME.** Etiket verilirse o 20 tedavi ikinci kez açılır.

**Araç düzeltildiyse, zaten aktarılmış dosyayı `tamamla` ile onar:**

```
python3 aktar_access.py tamamla kaynak=TEMMUZ temmuz.csv
```

Baştan aktarmıyor: eksik kalan dondurma kayıtlarını ve taze transferleri
ekliyor, FET'in çözdüğü embriyoyu tüpüne bağlıyor (v6.148); iki kez
çalıştırmak güvenli. Aktarımdan **hemen sonra** çalıştır: aktarılan bir
embriyonun skorunu ekranda elle düzelttiysen `tamamla` onu nottaki değerle
ezer.

**Birden çok ayı aktarırken sıra önemli: eskiden yeniye** (v6.148). FET'te
çözülen embriyo, dondurulduğu tüp programdaysa ona bağlanıyor; tüpün ayı
önce aktarılmış olmalı. Ocak–haziran 2026 için:

```
python3 aktar_access.py kaynak=OCAK    duzelt=tarih_duzeltme.txt ocak.csv
python3 aktar_access.py kaynak=SUBAT   duzelt=tarih_duzeltme.txt subat.csv
python3 aktar_access.py kaynak=MART    duzelt=tarih_duzeltme.txt mart.csv
python3 aktar_access.py kaynak=NISAN   duzelt=tarih_duzeltme.txt nisan.csv
python3 aktar_access.py kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
python3 aktar_access.py tamamla kaynak=TEMMUZ temmuz.csv
python3 aktar_access.py tamamla agustos.csv
```

(Her birinden önce aynı komutu `liste` ile çalıştırıp bakabilirsin.)
Son iki satır daha önce aktarılmış temmuz ve ağustosu yeni kurallarla
tamamlıyor — temmuz/ağustos FET'lerinin tüpü ocak–hazirandaysa ona bağlanıyor.

**Mayıs 2026 (v6.149) sonradan geldi.** Tarih düzeltmesi gerekmiyor (63
satırın hepsinin tarihi mayısta). Ocak–haziranı **henüz aktarmadıysan**
mayısı nisan ile haziran arasına koy:

```
python3 aktar_access.py kaynak=NISAN   duzelt=tarih_duzeltme.txt nisan.csv
python3 aktar_access.py kaynak=MAYIS   mayis.csv
python3 aktar_access.py kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
```

**Haziranı zaten aktardıysan** mayısı aktar, sonra ondan sonraki ayları
`tamamla` ile yeniden geçir — haziran/temmuz/ağustos FET'lerinin mayısta
dondurulan tüpleri ancak o zaman bağlanıyor ve Cryo Haritası'nda boşalıyor:

```
python3 aktar_access.py liste   kaynak=MAYIS   mayis.csv
python3 aktar_access.py         kaynak=MAYIS   mayis.csv
python3 aktar_access.py tamamla kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
python3 aktar_access.py tamamla kaynak=TEMMUZ  temmuz.csv
python3 aktar_access.py tamamla agustos.csv
```

`kaynak=` etiketi o ayın ilk aktarımındakiyle **aynı** olmalı (`HAZIRAN`,
`TEMMUZ`; ağustos etiketsiz) — farklı yazılırsa `tamamla` satırları bulamaz.

**2025 (ocak–mayıs, v6.160).** 2026'nın ayları zaten aktarıldığı için iki
şey farklı:

1. **Etiket `...2025`**: `OCAK`, `SUBAT`, `MART`, `NISAN`, `MAYIS` 2026'da
   kullanıldı. Aynı etiket verilirse 2025'in satırları 2026'nınkilerle
   çakışır (betik durur). CSV'lerin adı da 2026'nınkilerle karışmasın.
2. **FET'ler tüpüne kendiliğinden bağlanıyor** (v6.163): her aktarımın
   sonunda program veritabanındaki BÜTÜN aktarılmış FET'lere bakıp yeni
   gelen tüplerle tutanları bağlıyor (2025'te dondurulup 2025'in ileri bir
   ayında ya da 2026'da çözülen embriyo). Ayrıca bir şey çalıştırmak
   gerekmiyor.

Önce `git pull` ve programı bir kez kapatıp aç. Yedek al. Ocak 2025'te bir
kaydın tarihi düzeltme istiyor: `tarih_duzeltme.txt`'ye satırı ekle (satır
sohbette verildi, hasta verisine bağlı olduğu için burada yok).

```
python3 aktar_access.py liste kaynak=OCAK2025  duzelt=tarih_duzeltme.txt ocak2025.csv
python3 aktar_access.py       kaynak=OCAK2025  duzelt=tarih_duzeltme.txt ocak2025.csv
python3 aktar_access.py       kaynak=SUBAT2025 subat2025.csv
python3 aktar_access.py       kaynak=MART2025  mart2025.csv
python3 aktar_access.py       kaynak=NISAN2025 nisan2025.csv
python3 aktar_access.py       kaynak=MAYIS2025 mayis2025.csv
```

**Aylar zaten aktarıldıysa (v6.163'ten önce), bir kez:**

```
python3 aktar_access.py bagla
```

Dosya istemez: veritabanındaki bütün aktarılmış FET'leri çözme tarihi
sırasıyla dener, bağladıklarını ve "elle bakılmalı" olanları Access kayıt
numarasıyla yazar. Bağlı olana dokunmaz, iki kez çalıştırmak güvenli.

**2025 haziran–ekim (v6.164).** Önce `git pull` ve programı bir kez kapatıp
aç, yedek al (`/yedekleme` → "Şimdi yedekle"). Sıra **eskiden yeniye**.
Ağustos dosyasının üç tarihi düzeltme istiyor: sohbette verilen
`tarih_duzeltme_agustos2025.txt` dosyasını CSV'lerin yanına koy (hasta
kaydına bağlı olduğu için depoda değil).

```
python3 aktar_access.py liste kaynak=HAZIRAN2025 haziran2025.csv
python3 aktar_access.py       kaynak=HAZIRAN2025 haziran2025.csv
python3 aktar_access.py       kaynak=TEMMUZ2025  temmuz2025.csv
python3 aktar_access.py       kaynak=AGUSTOS2025 duzelt=tarih_duzeltme_agustos2025.txt agustos2025.csv
python3 aktar_access.py       kaynak=EYLUL2025   eylul2025.csv
python3 aktar_access.py       kaynak=EKIM2025    ekim2025.csv
```

(Her birini önce `liste` ile de çalıştırabilirsin.) Ağustos dosyasının son
kayıtları 22–30 Eylül tarihli: ayın sonu o dosyaya girilmiş, eylül
dosyasında yoklar -- eylül tarihleriyle aktarılıyor, bu doğru.

Her aktarımın sonunda üç liste çıkabilir:
- **"N tanesi ertelendi"**: FET'in tüpü ile çözmesi arasında henüz
  aktarılmamış bir ay var (bugün kasım–aralık 2025). Bir şey yapma: o ay
  aktarılınca kendiliğinden yeniden denenir.
- **"Elle bakılmalı"**: tüp seçeneği birden çok ya da hiçbiri tutmuyor
  (eskisi gibi).
- **"Bağlı ama artık kesin değil"**: daha önce bağlanmış bir FET'e yeni
  gelen bir tüp de uyuyor. Bağ olduğu gibi kalır; iki tüp de yazılı,
  kâğıttan hangisinin çözüldüğüne bak.

**2025 kasım–aralık ve 2024 ocak–mart (v6.165).** Önce `git pull` ve programı
bir kez kapatıp aç, yedek al (`/yedekleme` → "Şimdi yedekle"). Sohbette
verilen beş CSV'yi ve `tarih_duzeltme_2024_2025.txt` dosyasını aynı klasöre
koy (hasta kaydına bağlı oldukları için depoda değiller).

Önce şubat 2026'nın bir tüpünü onar: araç "(8HG2 8HG2 8HG2 6HG3)" gibi
tiresiz yazılmış skorların yalnızca ilkini okuyordu, o tüpe 4 yerine 1
embriyo yazıldı. Komut yalnızca eksik embriyoyu ekler, tüpteki örneğe ve elle
düzelttiğin skorlara dokunmaz (şubatın ilk aktarımındaki etiket ve dosya):

```
python3 aktar_access.py dondurma kaynak=SUBAT subat.csv
```

Çıktıda tek bir tedavi ve "dondurma onarıldı: ...: +3" görmelisin; başka
bir tedavi de yazılırsa bana göster. Son satır "(... aktarilmis tedavi gozden
gecirildi)" diye bitmeli. Yalnızca "Bitti. 0 tedaviye eksik dondurma
yazildi." yazıyorsa araç eskidir: `git log --oneline -1` ile bak, v6.165 ya
da sonrasını göstermiyorsa `git pull origin main`'i tekrarla ve çıktısını
oku (hata veriyorsa bana gönder). Sonra beş dosya, **eskiden yeniye**:

```
python3 aktar_access.py liste kaynak=OCAK2024 ocak2024.csv
python3 aktar_access.py       kaynak=OCAK2024   ocak2024.csv
python3 aktar_access.py       kaynak=SUBAT2024  subat2024.csv
python3 aktar_access.py       kaynak=MART2024   duzelt=tarih_duzeltme_2024_2025.txt mart2024.csv
python3 aktar_access.py       kaynak=KASIM2025  duzelt=tarih_duzeltme_2024_2025.txt kasim2025.csv
python3 aktar_access.py       kaynak=ARALIK2025 duzelt=tarih_duzeltme_2024_2025.txt aralik2025.csv
```

Kasım–aralık 2025 gelince ertelenmiş 2026 FET'lerinin çoğu kendiliğinden
2025 tüplerine bağlanır (aralık 2025 aktarımının sonunda uzun bir liste çıkar).
Bundan sonra "ertelendi" diyenler çoğunlukla tüpü 2024'ün başında tutan 2025
FET'leri: arada nisan–aralık 2024 yok, o aylar gelince denenir.

**2024 nisan–ağustos (v6.167).** Önce `git pull`, sonra **programı bir kez
kapatıp aç** — bu sürüm programın kendisini de değiştiriyor (tüplerin
"yumurta"/"embriyo" yazısı). Yedek al (`/yedekleme` → "Şimdi yedekle").
Sohbette verilen beş CSV'yi ve `tarih_duzeltme_2024b.txt`'yi aynı klasöre koy.

**Mayısı aktarmadan önce** düzeltme dosyasını bir metin düzenleyiciyle aç, iki
karar ver (içinde açıklaması var):
1. Mayıs #1 ile #13 aynı hastanın aynı günkü iki farklı kaydı. Hangisi
   **yanlışsa** onun `ATLA` satırının başındaki `#`'i sil. Hiçbirine
   dokunmazsan ikisi de aktarılmaz, araç söyler.
2. Mayıs #30'da ICSI 94 yazıyor (13 yumurta). Doğrusu 9 ise `ICSI`
   satırının başındaki `#`'i sil. Dokunmazsan ICSI döllenme sonuçlarından 5
   sayılır.

Sonra bir kez, daha önce aktarılmış ICSI'siz yumurta dondurmalarının tipini
düzelt. Bende 4 tedavi değişti (MART2024#4, AGUSTOS2025#21, EYLUL2025#51,
ARALIK2025#94); ikinci çalıştırma 0 der:

```
python3 aktar_access.py tip
```

Sonra beş dosya, **eskiden yeniye**:

```
python3 aktar_access.py liste kaynak=NISAN2024 duzelt=tarih_duzeltme_2024b.txt nisan2024.csv
python3 aktar_access.py       kaynak=NISAN2024   duzelt=tarih_duzeltme_2024b.txt nisan2024.csv
python3 aktar_access.py       kaynak=MAYIS2024   duzelt=tarih_duzeltme_2024b.txt mayis2024.csv
python3 aktar_access.py       kaynak=HAZIRAN2024 duzelt=tarih_duzeltme_2024b.txt haziran2024.csv
python3 aktar_access.py       kaynak=TEMMUZ2024  duzelt=tarih_duzeltme_2024b.txt temmuz2024.csv
python3 aktar_access.py       kaynak=AGUSTOS2024 duzelt=tarih_duzeltme_2024b.txt agustos2024.csv
```

Önceki aylarda aynı gün iki kez aktarılmış tedaviler de var: üç hastada,
hepsi iptal edilmiş, farkları notun yazımında. Bu komut onları listeler,
hiçbir şey değiştirmez:

```
python3 aktar_access.py ikiz
```

Fazla olanı hasta kartından aç → Sil → kalıcı silme (dosya no + SIL).
Transferleri yok, silinebilirler. Hangisini sileceğin sana kalmış.

**2024 eylül–aralık ve ocak 2023 (v6.168).** Önce `git pull`, programı bir
kez kapatıp aç (Yönetici panelindeki "Program sürümü" v6.168 demeli), yedek
al. Sohbette verilen beş CSV'yi ve `tarih_duzeltme_2024c.txt`'yi aynı klasöre
koy. OCAK dosyası **2023**'ün ocağı (tarihleri 2023-01), etiketi o yüzden
`OCAK2023`. Eskiden yeniye:

```
python3 aktar_access.py liste kaynak=OCAK2023 duzelt=tarih_duzeltme_2024c.txt ocak2023.csv
python3 aktar_access.py       kaynak=OCAK2023   duzelt=tarih_duzeltme_2024c.txt ocak2023.csv
python3 aktar_access.py       kaynak=EYLUL2024  eylul2024.csv
python3 aktar_access.py       kaynak=EKIM2024   ekim2024.csv
python3 aktar_access.py       kaynak=KASIM2024  duzelt=tarih_duzeltme_2024c.txt kasim2024.csv
python3 aktar_access.py       kaynak=ARALIK2024 duzelt=tarih_duzeltme_2024c.txt aralik2024.csv
```

Sonra bu sürümün yeni okumaları için (yazım hataları "KACG1", "KAVVİTASYON")
daha önce aktarılmış aylara bir kez `dondurma` — yalnızca eksik olanı ekler.
Ocak 2025'te bir embriyo ("KACG2") bu yüzden eksik kaldı:

```
python3 aktar_access.py dondurma kaynak=OCAK2025 duzelt=tarih_duzeltme.txt ocak2025.csv
```

Başka aylarda da aynı yazım varsa aynı komut o ayın etiketi ve dosyasıyla
çalışır; iki kez çalıştırmak güvenli ("0 tedaviye eksik dondurma yazildi").

**2023 şubat–haziran (v6.170).** Önce `git pull`, sonra programı bir kez
kapatıp açın. Yedek alın. Sohbette verilen beş CSV'yi ve
`tarih_duzeltme_2023.txt`'yi aynı klasöre koyun. **Önce düzeltme dosyasını
açıp Haziran #41'in dosya numarası satırını okuyun**: doğru değilse
`HAZIRAN2023#41  ATLA` yapın. Sonra eskiden yeniye:

```
python3 aktar_access.py liste kaynak=SUBAT2023 duzelt=tarih_duzeltme_2023.txt subat2023.csv
python3 aktar_access.py       kaynak=SUBAT2023   duzelt=tarih_duzeltme_2023.txt subat2023.csv
python3 aktar_access.py       kaynak=MART2023    duzelt=tarih_duzeltme_2023.txt mart2023.csv
python3 aktar_access.py       kaynak=NISAN2023   duzelt=tarih_duzeltme_2023.txt nisan2023.csv
python3 aktar_access.py       kaynak=MAYIS2023   duzelt=tarih_duzeltme_2023.txt mayis2023.csv
python3 aktar_access.py       kaynak=HAZIRAN2023 duzelt=tarih_duzeltme_2023.txt haziran2023.csv
```

**2018 (v6.173).** Önce `git pull`, programı bir kez yeniden başlat
(goc_049 açılışta çalışır: Cryo Haritası 5.000 tüple açılabilsin). 11 CSV
(`ocak2018.csv` … `aralik2018.csv`, ağustos yok) ve `tarih_duzeltme_2018.txt`
proje klasörüne. Düzeltme dosyasını oku: üç tarih düzeltmesi (gerekçeleri
yazılı) ve Mayıs 2018'in "455" dosya numarası (Şubat 2019'daki aynı hastanın
kartına girer; gerçek numarayı biliyorsan önce `dosya_no_degistir.py`).
Sonra tek komut:

```
python3 aktar_toplu.py duzelt=tarih_duzeltme_2018.txt
```

Klasördeki bütün `tarih_duzeltme*.txt` dosyaları kendiliğinden kullanılır
(her yılın kendi dosyası; ekranda "Düzeltme dosyaları:" satırı hangilerini
bulduğunu söyler) -- eski yılların düzeltme dosyalarını klasörden silme.
Araç önce her dosyayı kontrol eder (dosya başına birkaç saniye) ve
"AKTAR"dan ÖNCE hangi ayın kaç tedavi yazacağını listeler. Aktarılmış aylar
"zaten aktarılmış, atlanacak" satırına düşer, yarıda kalmış bir ayın
yalnızca eksiği yazılır. **Listede 2018 dışında aylar görünüyorsa AKTAR
yazma**: bu makinenin veritabanında o aylar yok demektir, 2019–2023 başka
makinede aktarılmış olabilir (önce `tasi.py` ile doğru veritabanını getir).
Her dosyanın sonunda 2019'un FET'leri 2018'in tüplerine bağlanır. Bitince
`aktar_toplu.log`'da `UYARI` satırlarına bak.

**Yanlış tüpe bağlanmış FET'ler (v6.175).** `bagla` sonunda "Bağlı ama
artık kesin değil" listesi çıkarsa: araç hangi tüpün çözüldüğünü bilemez,
sen bilirsin (Access notunun "GERİYE N TÜPTE ..." cümlesi, kâğıt, Cryo
Excel'i). Önce `git pull`, programı bir kez yeniden başlat (goc_050 açılışta
çalışır), yedek al. Sonra 2019'un dört eksik skoru ve Temmuz/Kasım 2019
FET'lerinin doğru tüpleri:

```
python3 aktar_access.py dondurma kaynak=SUBAT2019  duzelt=tarih_duzeltme_2019_2023.txt subat2019.csv
python3 aktar_access.py dondurma kaynak=ARALIK2019 duzelt=tarih_duzeltme_2019_2023.txt aralik2019.csv
python3 aktar_access.py dondurma kaynak=OCAK2020   duzelt=tarih_duzeltme_2019_2023.txt ocak2020.csv
python3 aktar_access.py tasi TEMMUZ2019#54 2018-0890-1200
python3 aktar_access.py tasi KASIM2019#63  2019-0146-1200
```

`tasi` önce ne yapacağını yazar, "TASI" yazınca taşır. Sıra önemli:
Kasım'ın hedefi olan tüp, Temmuz taşınınca boşa çıkıyor. Genel kullanım:
`python3 aktar_access.py tasi <Access işareti> <tüp etiketi> [<tüp etiketi> ...]`.

**Cryo haritası Excel'i (v6.173).** Bütün Access ayları aktarıldıktan
sonra. Excel dosyasını (`CRYO_HARITA.xlsx` gibi) proje klasörüne koy
(`.gitignore`'da), önce ne olacağına bak, sonra yaz:

```
python3 cryo_esle.py liste  CRYO_HARITA.xlsx     # yazmaz; cryo_esle_rapor.txt
python3 cryo_esle.py uygula CRYO_HARITA.xlsx     # "ESLE" yazınca konumları yazar
```

Terminalde yalnızca sayılar; satır satır rapor `cryo_esle_rapor.txt`'de
(hasta adı içerir, depoya girmez). Yazılanlar: hasta + dondurma günü +
içerik üçü de tutan tüpler (konum, taşıyıcı tipi, renk). Yazılmayanlar
raporda başlık başlık: hasta programda yok (2011–2018), aynı adlı hasta,
o gün tüp yok, içerik tutmuyor, tüpe daha önce başka konum yazılmış.
İkinci çalıştırma hiçbir şeyi değiştirmez. Ekranda: Cryo Haritası'nda
tüplerin konumu ve tank sayımı.

**2011–2017'nin programda olmayan hastaları (v6.179).** O yılların Access
dosyası yok; Excel'deki satırlardan hasta, tedavi ve tüp açılır (konumuyla):

```
python3 cryo_esle.py yeni_hasta CRYO_HARITA.xlsx   # planı basar, "HASTA" yazınca açar
```

Yalnızca 2018'den önceki, programda adı bulunmayan satırlar. Hastalar
**geçici dosya numarasıyla** açılır (9000000001, 9000000002, …); hasta
kayıtlarında "9000000" diye aranınca hepsi çıkar. Gerçek numara:

```
python3 dosya_no_degistir.py 9000000001 <gerçek no>          # ne olacak
python3 dosya_no_degistir.py 9000000001 <gerçek no> uygula   # değiştirir
```

Bu tedaviler istatistiğe girmez (yalnızca dondurma bilgisi var). Açılmayan
satırlar ve sebepleri `cryo_esle_rapor_yeni_hasta.txt`'de. İkinci
çalıştırma hiçbir şey açmaz.

**Sperm satırları (v6.180).** Excel'deki her sperm satırı bir tüp olarak
açılır; aynı erkeğin satırları tek hasta kaydında (geçici dosya numarası)
toplanır:

```
python3 cryo_esle.py sperm CRYO_HARITA.xlsx   # planı basar, "SPERM" yazınca açar
```

Tarihsiz ve ileri tarihli satırlar açılmaz (raporda:
`cryo_esle_rapor_sperm.txt`), elle girilir. İkinci çalıştırma hiçbir şey
açmaz. Eski dondurmayı çifte bağlamak: erkeğin kartında **Eşine bağla** →
eşinin dosya numarası; sonra çiftin kartında "Eşin dondurulmuş spermi" →
**Tedaviye bağla**.

**Başka merkeze taşınan tüp (v6.182).** Program içinden: tüpün sayfası
(Cryo Haritası'nda ya da arama kutusunda tüp etiketi) → **Başka merkeze
taşındı olarak işaretle** → gün, nereye ("Memorial Hastanesi'ne" gibi,
ekiyle), not. Geri almak da orada. Hangi tüplerin taşınmış olabileceğini
görmek için (hiçbir şey yazmaz):

```
python3 cryo_esle.py eksik CRYO_HARITA.xlsx   # programda dolu, Excel'de olmayan tüpler
```

Liste `cryo_esle_rapor_eksik.txt`'de. "Adı farklı yazılmış" sınıfındakiler
büyük olasılıkla tanktadır, onları işaretlemeyin.

**Cryo haritası onarımı (v6.188) -- bir kez, `git pull`'dan sonra.**
Excel'den eşleştirme üç yerde yanlış okumuştu: TANK 3'ün 2–5. kanisterleri
1. kanister sayılmış, "Tank 1-5 üst" sayfasının gobletleri alt kattakilerle
aynı adı almış (artık "7 Üst"), yeşil ve pembe straw'lar renksiz yazılmış.
`uygula`'yı çalıştırdığın makinede (Mac), aynı Excel dosyasıyla:

```
python3 cryo_esle.py onar CRYO_HARITA.xlsx   # planı basar, "ONAR" yazınca onarır
```

Yalnızca eski okumanın yazdığı konumu düzeltir: tüpün konumunu sonradan elle
değiştirdiysen dokunmaz, raporda listeler (`cryo_esle_rapor_onar.txt`, hasta
adı içerir). Renk yalnızca boşsa yazılır; pembe renk listeye eklenir. İkinci
çalıştırma "Onarılacak bir şey yok" der. Değişiklikler değişiklik geçmişine
düşer. Sperm satırları bu üç hatadan etkilenmedi (`sperm` kipi ayrı).

**Tank düzeni (v6.189) -- bir kez, `onar`'dan sonra.** Programın boş yer
önerebilmesi için Excel'in bütün gobletleri (boşlar dahil) programa açılır;
Excel'de duran ama programda tüpü bulunamayan her satır gobletinde "Excel
kaydı" olarak kalır (yuvası dolu sayılır). TANK 5'in 2.–6. kanisterlerinin
üst katı (Excel'de numarasız) 150 **yedek** goblet olarak açılır (v6.192):
program oraya ancak olağan yerler yetmediğinde yer önerir. "TANK 2 /
CANNİSTER 2" kopya tablosu okunmaz. Önce `git pull`, programı bir kez
yeniden başlat (göç 052 ve 053), sonra aynı Excel dosyasıyla:

```
python3 cryo_esle.py yerlesim CRYO_HARITA.xlsx   # planı basar, "YERLESIM" yazınca yazar
```

Önce çalışması gereken bir kip varsa (bekleyen `uygula`, `onar`, `yeni_hasta`
ya da `sperm`) hiçbir şey yazmadan hangisini çalıştıracağını söyler -- büyük
olasılıkla önce `python3 cryo_esle.py sperm CRYO_HARITA.xlsx` ("SPERM")
isteyecek. Rapor `cryo_esle_rapor_yerlesim.txt` (hasta adı içerir). İkinci
çalıştırma "Yazılacak bir şey yok" der. Sonra Cryo Haritası tank → kanister
ağacı olarak açılır; bir kanistere basınca gobletleri, her birinin 4 yuvası.
Excel kaydının sayfasından programdaki tüpe bağlanabilir ya da "tanktan
çıkarıldı" işaretlenebilir (ikisi de geri alınabilir). **Bundan sonra harita
programda tutulur**: yeni dondurmaları eski Excel'e değil programa girin.

**Excel haritası (v6.191) -- kendiliğinden.** Program açıkken harita her
değiştiğinde (dondurma, çözme, taşıma, Excel kaydı) Excel'ini yeniden yazar:
veri klasöründe `cryo_harita/Cryo_Haritasi.xlsx`, ayrıca her günün son hali
`Cryo_Haritasi_YYYY-AA-GG.xlsx` (30 gün). Elle bir şey çalıştırmak gerekmez.
Kopyalamanın iki yolu: Cryo Haritası'nda "Excel haritasını indir", ya da
klasörden kopyala (yöneticiye kartta klasörün yolu yazar). **Dosyayı
klasördeyken Excel'de açma, önce kopyala**: açık dosya güncellenemez (kart
söyler, kapatınca program yeniden dener). Dosyada yaptığın değişiklik
programa girmez, bir sonraki güncellemede silinir. Yedekleme son halini yedek
diskine de kopyalar (`<yedek klasörü>/cryo_harita/`).

**Kendi Cryo Haritası Excel'iniz, birebir (v6.199).** Programı bir kez yeniden
başlat (göç 054), sonra **tank düzeninin kurulduğu makinede** (Mac) yönetici
olarak: Cryo Haritası → "Excel haritası" kartı → "Laboratuvarın Cryo Haritası
Excel'i" → `yerlesim`'i çalıştırırken kullandığın dosyayı seç → "Dosyayı
yükle". Bundan sonra "Tankları Excel'e aktar" ve veri klasöründeki dosya o
Excel'in kendisi: sayfalar, tablolar, yazılar aynen, yalnızca straw satırları
programın bugünkü haliyle. Dosya `lab.db`'de saklanıyor, `tasi.py` ile öteki
makineye de gider. Yeni bir sürümünü yüklemek eskisinin yerine geçer.

**2019–2022 ve temmuz–aralık 2023 (v6.172).** Önce `git pull`, sonra programı
bir kez yeniden başlat. 53 CSV ve `tarih_duzeltme_2019_2023.txt` aynı
klasöre. Etiketler ay + yıl (`OCAK2019` … `ARALIK2023`); 2020'nin mayısı
arşivde yoktu. **Aktarımdan önce iki iş:**

1. Düzeltme dosyasını oku: Kasım 2020'nin bir FET tarihi tahmin, Şubat 2019
   #6'nın dosya numarası ("455") bulunamadı, Ekim 2021'in ikiz kaydından
   #72 atlanıyor — katılmıyorsanız o satırı değiştirin/silin.
2. Aralık 2024'te dosya numarası "99" ile aktarılan hastanın gerçek numarası
   düzeltme dosyasında yazıyor (2019'daki kayıtları o numarada). Ekran dosya
   numarasını değiştirmeye izin vermiyor; araçla, **2019 aktarımından önce**
   (yeni numara kayıtlıysa araç durur):

   ```
   python3 dosya_no_degistir.py 99 <gerçek no>          # ne olacak, listeler
   python3 dosya_no_degistir.py 99 <gerçek no> uygula   # "DEGISTIR" yazınca değiştirir
   ```

Sonra **tek komut** (kullanıcının isteği: "tek komuta düşür"):

```
python3 aktar_toplu.py duzelt=tarih_duzeltme_2019_2023.txt dosya=99:<gerçek no>
```

`aktar_toplu.py` klasördeki `<ay><yıl>.csv` dosyalarını bulup tarih
sırasıyla `aktar_access.py`'ye verir; `dosya=` adımı önce 99'u gerçek numaraya çevirir (numara düzeltme dosyasında yazıyor)
(zaten yapılmışsa atlar). Ekranda dosya başına bir satır, bütün çıktı
`aktar_toplu.log`'da; bir dosya hata verirse durur, aynı komut kaldığı
yerden devam eder (bitmiş dosyalar yalnızca kontrol edilir). Klasörde daha
önce aktarılmış ayların CSV'leri de duruyorsa onlar da kontrolden geçer
(dosya başına bir dakika); 2026'nın dosyaları atlanır (yılsız etiketle
aktarıldılar). Bir saat kadar sürer. Elle, dosya dosya yapmak istersen aynı
şeyi bu komutlar yapar:

```
python3 aktar_access.py liste kaynak=OCAK2019 duzelt=tarih_duzeltme_2019_2023.txt ocak2019.csv
python3 aktar_access.py kaynak=OCAK2019     duzelt=tarih_duzeltme_2019_2023.txt ocak2019.csv
...   (her ay aynı kalıp, ARALIK2023'e kadar; etiket = AY + YIL)
```

Kaynakta ICSI sayısı olmayan ama transfer/dondurma yazan satırlar (`UYARI:
... uygun kayıt var`) döllenme uydurulmadığı için eksik kalır; sayıyı
biliyorsanız düzeltme dosyasına `KAYNAK#KAYIT  ICSI  0  <sayı>` yazıp o
dosyayı yeniden aktarın (`tamamla` gerekmez, aktarım idempotent).

**v6.161:** "2 ADET M2 OOSİT DONDURULARAK SAKLANDI" gibi tüp sayısı yazmayan
yumurta dondurması artık tek tüp. 2026'da da böyle bir satır vardı ve tüpü
yazılmamıştı; `dondurma` kipiyle 2026'nın aylarını bir kez geçir (hiç tüpü
olmayan tedaviye yazar; v6.165'ten beri tüpü olanda yalnızca eksik örneği
ekler, tüpteki örneğe dokunmaz; iki kez çalıştırmak güvenli):

```
python3 aktar_access.py dondurma kaynak=OCAK    duzelt=tarih_duzeltme.txt ocak.csv
python3 aktar_access.py dondurma kaynak=SUBAT   duzelt=tarih_duzeltme.txt subat.csv
python3 aktar_access.py dondurma kaynak=MART    duzelt=tarih_duzeltme.txt mart.csv
python3 aktar_access.py dondurma kaynak=NISAN   duzelt=tarih_duzeltme.txt nisan.csv
python3 aktar_access.py dondurma kaynak=MAYIS   mayis.csv
python3 aktar_access.py dondurma kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
python3 aktar_access.py dondurma kaynak=TEMMUZ  temmuz.csv
python3 aktar_access.py dondurma agustos.csv
```

2025'i **zaten v6.160 ile aktardıysan** aynı kip 2025 için de gerekli
(`kaynak=SUBAT2025 subat2025.csv` ...), ama not–MII düzeltmesi (iki Yumurta
Dondurma satırı) aktarılmış tedaviye uygulanmıyor — o durumda söyle.

`dondurma` satırlarındaki etiketler 2026'nın ilk aktarımındakilerle **aynı** olmalı (ağustos etiketsiz).

**FET formlarında transfer edilen embriyo boşsa (v6.154).** v6.153'e kadar
araç FET'te transfer edilen embriyonun hücre sayısını ve kalitesini
(Access'teki EMBRİYO1/2 kutuları) programa yazmıyordu; Embriyoloji Özet'in
"Embriyo transferi" kutuları ve ART Lab'ın "Uterus grade"i boş çıkıyordu.
`transfer` kipi yalnızca bunu yazar, başka hiçbir şeye dokunmaz. Önce
`git pull`, sonra aktardığın her ay için bir kez (mayıs dahil):

```
python3 aktar_access.py transfer kaynak=OCAK    duzelt=tarih_duzeltme.txt ocak.csv
python3 aktar_access.py transfer kaynak=SUBAT   duzelt=tarih_duzeltme.txt subat.csv
python3 aktar_access.py transfer kaynak=MART    duzelt=tarih_duzeltme.txt mart.csv
python3 aktar_access.py transfer kaynak=NISAN   duzelt=tarih_duzeltme.txt nisan.csv
python3 aktar_access.py transfer kaynak=MAYIS   mayis.csv
python3 aktar_access.py transfer kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
python3 aktar_access.py transfer kaynak=TEMMUZ  temmuz.csv
python3 aktar_access.py transfer agustos.csv
```

İkinci kez çalıştırmak bir şey değiştirmez ("0 FET tedavisine ... yazildi").

**İptal sebeplerini onarmak (v6.150).** v6.149'a kadar araç "OOSİT ÇIKMADI"
ve "İNMATÜR OOSİT" notlarını tanımıyordu; o tedaviler genel "İptal" olarak
kaldı. `iptal` kipi yalnızca hâlâ genel "iptal"de kalanların sebebini
günceller, başka hiçbir şeye dokunmaz — ekrandan elle seçtiğin bir sebep ve
elle düzelttiğin skorlar olduğu gibi kalır. Aktardığın her ay için bir kez:

```
python3 aktar_access.py iptal kaynak=OCAK    duzelt=tarih_duzeltme.txt ocak.csv
python3 aktar_access.py iptal kaynak=SUBAT   duzelt=tarih_duzeltme.txt subat.csv
python3 aktar_access.py iptal kaynak=MART    duzelt=tarih_duzeltme.txt mart.csv
python3 aktar_access.py iptal kaynak=NISAN   duzelt=tarih_duzeltme.txt nisan.csv
python3 aktar_access.py iptal kaynak=HAZIRAN duzelt=tarih_duzeltme.txt haziran.csv
python3 aktar_access.py iptal kaynak=TEMMUZ  temmuz.csv
python3 aktar_access.py iptal agustos.csv
```

Mayıs v6.149'la aktarıldıysa gerekmiyor (sebepler zaten doğru yazıldı).
İki kez çalıştırmak güvenli.

**`duzelt=` ne işe yarıyor:** Access'te yazım hatasıyla girilmiş tarihlerin
düzeltmeleri (OPU'su haziran yazan bir ocak tedavisi gibi). Dosyada
`KAYNAK#KAYIT  OPU|TRANSFER  eski-tarih  yeni-tarih` satırları var; düzeltme
yalnızca Access'teki değer hâlâ o ise uygulanıyor, tedavinin notuna
"... yazıyordu, ... olarak düzeltildi" düşüyor. Dosya hasta kaydına bağlı
olduğu için depoda değil, CSV'lerle birlikte duruyor.

**Aktarımın sonunda "Elle bakılmalı" listesi çıkar:** çözülen embriyonun
tüpü birden çok seçenekle tutuyor ya da hastanın dolu tüplerinden hiçbiri
tutmuyor. Bu FET'ler bağlanmadı; ilgili satırın raporunda seçenekler yazılı.

**"Veritabani guncellemesi eksik (goc_046, goc_047)" derse:** `git pull`'dan
sonra program yeniden açılmamış demektir. Programı bir kez kapatıp aç —
güncellemeler açılışta kendiliğinden uygulanır — sonra komutu tekrar
çalıştır. Araç bu durumda hiçbir şey yazmadan durur.

### Eylül 2026 (v6.207)

Önce `git pull origin main`, programı bir kez kapatıp aç, yedek al
(`/yedekleme` → "Şimdi yedekle"). Sohbette verilen `eylul.csv`'yi aktarımı
çalıştırdığın klasöre koy. **Veritabanının olduğu bilgisayarda** çalıştır
(Cryo Haritası'nın düzeni Mac'te; klinikteki makinede yapacaksan önce
`tasi.py` ile taşı). Etiket `EYLUL` (2026'nın ayları yılsız: `OCAK` … `TEMMUZ`;
`EYLUL2024` ve `EYLUL2025` başka yılların):

```
python3 aktar_access.py liste kaynak=EYLUL eylul.csv
```

Bu ay bazı hastalar programa ekrandan da girildi. `liste` onları **PROGRAMDA
VAR — atlanır** diye yazar; programdaki tedavinin numarası, günü, yumurta ve
tüp sayısı (kaçının Cryo Haritası'nda olduğu) ile Access'in sayıları yan
yana. Programdaki eksikse ekrandan tamamla. Aynı tedavi DEĞİLSE (aynı ay
içinde ikinci bir tedavi) düzeltme dosyasına `EYLUL#<kayıt no>  AKTAR` yaz, o
kayıt yine aktarılır.

Cryo Haritası'nda Excel kaydı olarak duran straw'lar satırın altında yazar
("Cryo Haritası'nda Excel kaydı olarak 3 straw: ..."). Aktarımın sonunda
bunlar tüplerine bağlanır (tüp gobletine yazılır, straw bir kez sayılır);
bağlanamayanlar sayfa adresleriyle listelenir (`/cryo/excel-kaydi/<no>`,
tarayıcıda o sayfadan "tüpe bağla").

\#19 ve \#22 aynı hastanın aynı günkü iki farklı kaydı: ikisi de atlanır.
Hangisi doğruysa ÖTEKİNİ bir düzeltme dosyasına yaz (`tarih_duzeltme_eylul.txt`,
tek satır, ör. `EYLUL#19  ATLA`) ve dosyayla aktar:

```
python3 aktar_access.py kaynak=EYLUL duzelt=tarih_duzeltme_eylul.txt eylul.csv
```

(Düzeltme dosyası yoksa `duzelt=` olmadan: `python3 aktar_access.py
kaynak=EYLUL eylul.csv`.) `AKTAR` yazınca yazar; iki kez çalıştırmak güvenli
(aktarılmış satır atlanır). Sonradan bir ikizi seçersen aynı komutu yeniden
ver: yalnızca o kayıt aktarılır, Excel kaydı da bağlanır.

**Excel kaydını sonradan bağlamak** (ekrandan girilen bir tüp, düzeltilen bir
ad; Excel dosyası gerekmez):

```
python3 cryo_esle.py excel_bagla
```

Ne bağlanacağını sayar, ayrıntıyı `cryo_esle_rapor_excel_bagla.txt`'ye yazar,
`BAGLA` yazınca bağlar. Yalnızca konumu boş tüplere bağlar; aynı gobletde aynı
içerikli, yeri girilmiş bir tüp varsa dokunmaz (ayrı bir straw olabilir),
raporda yazar.

### Transfer hekimi (v6.232)

v6.232'den önce aktarılmış tedavilerde transfer hekimi boş: araç Access'in
"TRANSFER KLİNİSYEN" sütununu okumuyordu. Yazmak için önce `git pull origin
main`, programı bir kez kapatıp aç, yedek al. **Veritabanının olduğu
bilgisayarda** çalıştır. Aktardığın bütün Access CSV'lerini ve
`tarih_duzeltme*.txt` dosyalarını tek klasöre koy -- adları aktarırken
kullandığın gibi (`ocak2019.csv` … `aralik2025.csv`; 2026'nın ayları
`ocak.csv` … `temmuz.csv`, `agustos.csv`, `eylul.csv` ya da `ocak2026.csv`):

```
python3 aktar_toplu.py kip=transfer_hekim klasor="<CSV klasörü>"
```

Dosyaları ve etiketlerini listeler, "YAZ" yazınca her ayı dener (dosya başına
birkaç saniye). Yalnızca **boş** transfer hekimini yazar: ekrandan girilmiş
ada ve başka hiçbir şeye dokunmaz; iki kez çalıştırmak güvenli (ikincisi
"0 tedaviye yazıldı" der). CSV'ler birkaç klasördeyse her klasör için ayrı
çalıştır. "YAZILMADI" diyen dosyanın mesajı sonda (çoğu zaman o ayın
düzeltme dosyası klasörde değildir). Tek bir ay:

```
python3 aktar_access.py transfer_hekim kaynak=OCAK2019 ocak2019.csv
python3 aktar_access.py transfer_hekim agustos.csv
```

(Ağustos 2026 etiketsiz aktarıldı, `kaynak=` yok.) Yeni aktarımlar transfer
hekimini kendisi yazıyor.

---

## Aynı hastanın iki kartı — birleştirme (v6.215)

Aynı hasta iki dosya numarasıyla iki kez kaydedilmişse (Access'te numara
yanlış yazılmış, aktarım ikinci bir kart açmış): **yanlış numaralı kart
silinir, her şeyi doğru numaralı karta geçer** -- tedaviler, sperm
dondurmaları, fotoğraflar ve onam ekleri (arşiv klasörü dahil), başka
kartlardaki "eşin dosya no". Doğru kartta boş olan alanlar (doğum tarihi,
telefon, ...) yanlış karttan dolar; tedaviler tarih sırasıyla numaralanır.

**Programın veritabanının durduğu bilgisayarda** (tank düzeni Mac'te),
proje klasöründe. Sıra: önce yanlış numara, sonra doğru numara.

```
python3 hasta_birlestir.py <yanlış no> <doğru no>          # ne olacak, yalnızca listeler
python3 hasta_birlestir.py <yanlış no> <doğru no> uygula   # "BIRLESTIR" yazınca birleştirir
```

Önizlemede adların, eş adlarının, doğum tarihlerinin tutup tutmadığı yazar
(adlar yazılmaz). **"FARKLI" ya da "DİKKAT" görürseniz kartları ekranda
karşılaştırın** -- iki farklı hastayı birleştirmek bu işin en pahalı hatası.
`uygula` önce veritabanının tamamını `lab_ONCEKI_<zaman>.db` diye kopyalar
(yedek klasörü bu bilgisayarda varsa oraya: Yönetici → Yedekleme → "Yedekten
geri yükle" listesinde görünür). Program açıkken çalışabilir; sonra sayfayı
yenileyin. Silinen kartın bütün alanları değişiklik geçmişinde kalır.

Araç sonunda gerekirse üç şey söyler: Access düzeltme dosyasına eklenecek
satırlar (`KAYNAK#KAYIT  DOSYA  <yanlış>  <doğru>` -- yalnızca o CSV'yi
yeniden aktaracaksanız), `python3 aktar_access.py bagla` (FET'in tüpü öteki
karttaydıysa) ve Haritadan yer tamamla (konumu girilmemiş tüp varsa).

Yalnızca numara yanlışsa ve doğru numara hiç kayıtlı değilse birleştirme
değil numara değişikliği: `python3 dosya_no_degistir.py <eski> <yeni>`.

---

## Aynı hastanın iki tedavisi — birleştirme (v6.228)

Aynı hastanın bir işlemi iki tedavide kayıtlıysa (Cryo Haritası'nın Excel
kaydından "Hastaya bağla" ile açılmış bir dondurma kaydı, Access'ten ikinci
kez gelmiş aynı OPU, boş açılmış bir tedavi): **birleşen tedavi silinir,
dondurulmuş örnekleri ve kayıtları esas tedavinin olur**. Düz toplama değil:
iki kayıt aynı yumurtaları taşıyorsa her tüp esas tedavinin eşleşen,
dondurulmamış embriyolarına geçer (aynı skor; değerlendirilmemiş embriyo;
aynı evre ve sayı), yumurta ve embriyo sayıları ikiye katlanmaz. Tüpün
etiketi, yeri, rengi ve Excel bağı kalır; etiket programın ürettiği bir
koddaysa esas tedavinin numarasına çevrilir.

**Programın veritabanının durduğu bilgisayarda** (tank düzeni Mac'te),
proje klasöründe. Sıra: önce birleşen (silinecek) tedavi, sonra esas
tedavi -- ikisi de lab kayıt no (tedavi ekranının başlığındaki 2026-0xxx).

```
python3 tedavi_birlestir.py <birleşen no> <esas no>          # ne olacak, yalnızca listeler
python3 tedavi_birlestir.py <birleşen no> <esas no> uygula   # "BIRLESTIR" yazınca birleştirir
```

Önizleme iki tedavinin ne olduğunu (Excel kaydı / Access kaydı / programda
girilmiş), seçilen yolu ve her tüpün esas tedavide hangi embriyolara
geçeceğini yazar (adlar yazılmaz). **"ENGEL" varsa hiçbir şey yazılmaz**,
sebebi satırda: farklı hastalar, farklı tip ya da OPU günü, tüpün içeriği
esas tedavide karşılık bulmuyor, silinecek yumurtada fotoğraf / PGT, ...;
ters yön daha doğruysa araç söyler. **"DİKKAT" görürseniz** (skorlar farklı,
embriyo değerlendirilmemiş) önce esas tedavinin vitrifikasyon ekranında doğru
embriyo mu bakın. `uygula` önce veritabanının tamamını
`lab_ONCEKI_<zaman>.db` diye kopyalar (hasta kartı birleştirmedeki gibi:
Yönetici → Yedekleme → "Yedekten geri yükle" listesinde görünür). Program
açıkken çalışabilir; sonra sayfayı yenileyin, esas tedavinin Embriyoloji Özet
ve ART Lab formlarına bakın. Silinen tedavinin bütün alanları değişiklik
geçmişinde kalır.

**"aynı straw olabilir" ENGEL'i** (v6.229): Excel kaydından açılmış tüp
esas tedavide birebir karşılık bulmuyor ama esas tedavinin aynı gün
dondurulmuş, yeri girilmemiş bir tüpü var -- Excel aynı straw'ı başka bir
yazımla göstermiş olabilir. Aynı straw'sa birleştirme gerekmez, programın
içinde iki adım (iletide Excel kaydının numarası ve tüpün etiketi yazar):

1. Cryo Haritası'nda o Excel kaydının sayfası → **"Açılan tüpü geri al"**:
   Excel'den açılan tüp silinir, Cryo Excel tedavisi boş kaldıysa o da.
2. Aynı sayfada **"Tüpe bağla"** → tedavinin tüpü (listede yoksa etiketini
   yazın). Tüp gobletine geçer; harita straw'ı tedavinin kaydıyla gösterir.

Excel'de yazıyı düzeltip dosyayı programa geri yüklemek mümkün değil: Excel
dosyası programın kayıtlarından her değişiklikte yeniden yazılıyor. Tedavinin
kaydı doğruysa onu Excel'in yazısına göre değiştirmeyin. Bağladıktan sonra
laboratuvarın Excel dosyasında o straw'ın HÜCRE'si de tedavinin kaydına göre
yazılır (v6.230; ad, tarih, VİAL olduğu gibi kalır).

İki tedavi farklı kartlardaysa (aynı hasta iki dosya numarasıyla) önce
`hasta_birlestir.py` (yukarıda), sonra bu.

---

## Sorun teşhisi

```
python3 teshis.py                    # genel kontrol
python3 teshis_silme.py 527078       # bu hasta neden silinemiyor
python3 teshis_form.py               # FET formunda çözme görünmüyor: listele
python3 teshis_form.py 2026-0123     # o tedaviyi adım adım incele
python3 cozme_ayir.py                # IVF/ICSI'ye yazılmış çözmeler (dokunmaz)
python3 liste_duzenle.py             # seçim listelerini gör / temizle
python3 tarih_duzelt.py liste        # bozuk tarih var mı (dokunmaz)
python3 yerel_kur.py                 # bu makinenin klasör yollarını ayarla
```

### IVF/ICSI'ye yazılmış çözme (v6.155)

v6.155'ten beri IVF/ICSI tedavisinde çözme yok: dondurulan embriyonun
çözülmesi ayrı bir FET tedavisi (çözme ekranındaki "Yeni tedavi başlat:
FET" düğmesi). Daha önce ICSI'ye yazılmış çözmeleri — ve ondan sonraki
transfer ile yeniden dondurmayı — bu araç FET'e taşır:

```
python3 cozme_ayir.py                # yalnızca listeler, hiçbir şeye dokunmaz
python3 cozme_ayir.py uygula         # taşır; onay için AYIR yazdırır
```

**Önce yedek al** (Yönetici → Yedekleme → Şimdi yedekle). Uygun FET
varsa ona, yoksa yeni bir FET açıp taşır. Gebelik sonucunu yalnızca
belirsizlik yoksa taşır; "GEBELIK SONUCU TASINMADI" ya da "DIKKAT" yazan
satırları ekrandan kontrol et. İkinci çalıştırma bir şey bulmaz.
Program açıkken çalışabilir; sonra ekranı tazele.

### Yılı bozuk tarih

`datetime-local` alanına yıl olarak "26" yazılırsa tarayıcı **26. yılı**
gönderiyor (`0026-09-04`). v6.51'den beri program böyle bir değeri kabul
etmiyor, ama daha önce girilmiş kayıtlar duruyor olabilir. Araç üç şeye
bakıyor: yılı çok eski, yılı çok ileri (`9999`), hiç okunamayan biçim
(`04.09.2026`, `88-01-05`).

```
python3 tarih_duzelt.py liste        # yalnızca listeler
python3 tarih_duzelt.py              # tek tek sorar, onayladığını düzeltir
```

Her kayıt için kime ait olduğunu ve önerilen tarihi yazar. **Enter** öneriyi
kabul eder, kendin de bir tarih yazabilirsin, `a` atlar, `q` çıkar. Doğum
tarihlerine öneri yapmaz — doğru yılı sen yazarsın.

Klasör yollarını (kamera / arşiv / yedek) **ekrandan** da ayarlayabilirsin:
yönetici olarak `/yonetim` → **Klasörler** (v6.41). `yerel_kur.py` aynı işi
terminalden yapıyor; ikisi de aynı dosyaya yazıyor.

Hiçbiri veri silmez. `cozme_ayir.py uygula` kayıt taşır (silmez), önce yedek al.

---

## Kod güncelleme (git)

```
git pull origin main                 # diğer makinedeki değişiklikleri al
git status                           # ne değişmiş
git add -A
git commit -m "kısa açıklama"
git push origin main                 # gönder
```

`git pull` **kodu** getirir, **hasta verisini getirmez** — veri `.gitignore`'da.

**`git pull`'dan sonra programı yeniden başlat.** Çalışan program `templates/`
klasörünü her istekte diskten okuyor ama Python dosyalarını (`app.py`,
`metinler.py`, ...) **yalnızca açılışta** okuyor. Yeniden başlatmazsan yeni
ekran parçaları görünür ama çalışmaz — düğme/kutu ortaya çıkar, basınca
hiçbir şey olmaz, hata da vermez. Terminalde `Ctrl+C`, sonra tekrar
`python3 baslat.py`.

Çakışma (`conflict`) çıkarsa **dur**, Claude Code'a sor.

**Programın çalıştığı makine her zaman `main` dalında durmalı.** Bütün
Claude hesapları işlerini `main`'e getiriyor (CLAUDE.md, "Git: tek ortak
hat"). Hangi dalda olduğunu görmek ve `main`'e dönmek:

```
git branch                           # başında * olan satır şu anki dal
git checkout main                    # main değilse main'e geç
git pull origin main
```

Sonra programı yeniden başlat.

---

## Sık sorunlar

**`git pull` → "conflict" (çakışma)**
İki makinede aynı dosyayı değiştirip ikisini de commit etmişsin. **Dur.**
Claude Code'a "pull çakışması var" de, birlikte çözün.
`git checkout --theirs/--ours` gibi komutları tek başına deneme.

**`git push` → "rejected" / "non-fast-forward"**
Diğer makineden push edilmiş, sen pull etmemişsin.
Önce `git pull origin main`, çakışma yoksa tekrar push.

**`git pull` → "refusing to merge unrelated histories"**
Klasör `git init` ile kurulmuş; doğrusu boş bir yere `git clone`.
Klasörü `..._eski` diye yeniden adlandır, sonra:
```
git clone https://github.com/OnurErturk80/Patient-Data-Center.git "Patient Data Center"
```
`_eski`'den yeni klasöre taşı: `lab.db`, `arsiv/`, `snapshot/`,
`yerel_ayar.json`. Sonra `python3 goc_hepsi.py`.

**`git pull` çalışmıyor, `.git` yok**
Klasör ZIP ile kurulmuş. Yukarıdaki `git clone` adımını uygula.

**`git status` → "ahead of 'origin/main' by N commits"**
Commit etmişsin, push etmemişsin. `git push origin main`.

**Araç "CRYO bulunamadı" / ".../Patient bulunamadı" diyor**
Dosya adında boşluk var, terminal adı sözlere bölüyor. Adı tırnak içine
yaz: `python3 cryo_esle.py yerlesim "CRYO HARİTA.xlsx"`. Dosyayı Finder'dan
terminal penceresine sürüklemek de olur (adı kendisi doğru yazar).

**Yeni bir kutu/düğme göründü ama hiçbir şey yapmıyor**
`git pull` yaptın, programı yeniden başlatmadın. Şablonlar diskten tazelenir,
Python kodu tazelenmez. `Ctrl+C` → `python3 baslat.py`.

**Android'de "Güvenli adresi aç" açılmıyor / "bağlantınız gizli değil"**
Sertifika telefona yüklenmemiş ya da yanlış yere yüklenmiş: "Güvenlik
sertifikası" sayfasını yeniden aç, yeşil "güvenilir" yazısı çıkmalı. Yazı
çıkıyor ama adres hiç açılmıyorsa bilgisayarın güvenlik duvarı 8443'ü
engelliyor olabilir (Windows: Güvenlik Duvarı → uygulamaya izin ver →
Python, "Özel ağ" işaretli). Program `python3 -m uvicorn` ile açıldıysa
güvenli adres yoktur -- `python3 baslat.py` ile aç.

**Bir ekran veya gün eksik görünüyor**
Göç uygulanamamış olabilir: `/yonetim` → Veritabanı güncellemeleri kartına bak, ya da `python3 goc_hepsi.py` çalıştır.

**Hasta verisi yanlışlıkla git'e girmiş mi?**
```
git ls-files | grep -E "lab.db|arsiv/|snapshot/|yerel_ayar"
```
Boş dönmeli. Bir şey dönerse Claude Code'a haber ver.

---

## Dikkat — bunu yanlışlıkla çalıştırma

```
python3 sifirdan_kur.py
```

**Boş** bir veritabanı kurar. Sadece yepyeni bir makinede, hiç veri yokken.
Mevcut `lab.db` varken çalıştırma.
