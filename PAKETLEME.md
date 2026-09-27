# Kurulabilir uygulama (kurulum dosyası)

Program git ile şöyle kuruluyor: Python kur, `pip install ...`, `git clone`,
`python3 baslat.py`, açılışta başlaması için görev tanımla. **Hiçbir klinik
bunu yapmaz.** Paketleme bunu tek dosyaya indiriyor: Windows'ta kurulum
dosyası (`.exe`), Mac'te uygulama (`.dmg`). Kullanıcı çift tıklıyor, program
kuruluyor, tarayıcıda ilk kurulum ekranı açılıyor ve bilgisayar açıldığında
program kendiliğinden çalışıyor.

Kullanıcının yapacakları (dosyayı indirmek, kurmak, güncellemek):
`KOMUTLAR.md` → "Kurulum dosyası". Bu sayfa nasıl yapıldığını anlatıyor.

Hazırlık sürümleri:

- **v6.46** — veri programdan ayrıldı (`PROGRAM_KOK` / `VERI_KOK`). Paketin
  içi salt okunur; veri oraya yazılamaz, yazılsa bile güncellemede silinirdi.
- **v6.49** — göçler açılışta kendiliğinden çalışıyor, süreç içinde. (Alt
  süreç açmak paketlenmiş uygulamada **programı** yeniden başlatırdı.)
- **v6.50** — giriş noktası (`baslat.py`) ve PyInstaller tarifi.
- **v6.203** — ağ erişimi anahtarı: yeni kurulum ağa kapalı başlıyor.
- **v6.204** — ilk açılış ekranı (`/kurulum`), Windows kurulum dosyası, Mac
  uygulaması, GitHub'da derleme ve deneme.

---

## Derleme: GitHub Actions

`.github/workflows/paket.yml`, **elle** çalıştırılıyor: Actions → Paketler →
Run workflow. Makineler tek tek seçiliyor: Windows, Mac (Apple Silicon), Mac
(Intel, varsayılan kapalı).

- **Neden her gönderimde değil:** depo özel, her dakika hesabın aylık ücretsiz
  dakikasından düşüyor ve Windows 2, Mac 10 kat sayılıyor. Windows + Apple
  Silicon Mac bir çalışmada ~150 dakika.
- PyInstaller çapraz derleme yapmıyor: Windows paketi Windows'ta, Mac paketi
  Mac'te üretiliyor. GitHub'ın makineleri bunun için.
- Intel Mac: GitHub'ın son Intel makinesi (`macos-15-intel`) Ağustos 2027'ye
  kadar. Sonra Intel Mac'ler için derleme yapılamaz.
- Çıkan dosyalar çalışmanın sayfasında "Artifacts" altında, 14 gün.

Her makinede sırayla:

1. Bağımlılıklar + PyInstaller + Pillow (simgeler için, yalnızca derlemede).
2. `pyinstaller --noconfirm --clean paket/pdc.spec`.
3. **Duman testi** (`paket/dene.py program`): paket kaynak klasörünün dışında,
   `PYTHONPATH` temizlenmiş, boş bir veri klasörüyle açılıyor; `/` ilk kurulum
   ekranına gidiyor, yeni laboratuvar kuruluyor (göçler), yönetici giriyor,
   23 ekran açılıyor, hasta ve tedavi açılıyor, resmî formlar ve Excel
   çıktıları üretiliyor, HTTPS cevap veriyor; programa ikinci kez tıklamak
   ikinci sunucu açmıyor; günlükte hata yok.
4. Windows: Inno Setup ile kurulum dosyası; sonra **sessiz kurulum**: Görev
   Zamanlayıcı programı SYSTEM olarak açtı mı, görevin süre sınırı yok mu,
   güvenlik duvarı kuralı yerel ağa mı; kurulu program aynı denemeden geçiyor.
   **İkinci kurulum** (güncelleme): program yeniden başladı mı, veritabanı
   korundu mu, ikinci güvenlik duvarı kuralı açılmadı mı. **Kaldırma**:
   program, görev, kural gitti mi, veri yerinde mi.
5. Mac: uygulama ad-hoc imzalanıyor; duman testine ek olarak yenilenmiş
   uygulamanın eski derlemeyi kapatıp yerine geçmesi, Uygulamalar'dan
   açılınca LaunchAgent yazması; DMG kurulup açılıp denetleniyor.

### Elle derleme

Aynı işletim sisteminde, proje kökünde:

```
pip install pyinstaller pillow
pyinstaller --noconfirm --clean paket/pdc.spec
python3 paket/dene.py program dist/PatientDataCenter/PatientDataCenter      # Linux
```

Windows'ta ardından `ISCC.exe /DSurum=6.204 paket\pdc_kurulum.iss`; Mac'te
`codesign --force --deep --sign - "dist/Patient Data Center.app"` ve
`hdiutil` (iş akışının DMG adımı). `build/` ve `dist/` git'e girmiyor.

---

## Tarifte dikkat edilenler (`paket/pdc.spec`)

Bunlar eksik kalırsa program açılır ama **sessizce** bozuk çalışır:

1. **Şablonlar ve `static/` veri olarak ekleniyor.** PyInstaller yalnızca
   `import` edilenleri toplar; Jinja şablonlarını ve CSS'i göremez.
2. **Göç betikleri `hiddenimports`'ta.** `importlib.import_module("goc_029")`
   ile adıyla çağrıldıkları için PyInstaller onları göremiyor. Yeni bir göç
   yazdığında tarif onu **kendiliğinden** buluyor (dosya adına bakıyor).
3. **`README.md` pakete giriyor**: çalışan sürüm oradan okunuyor (Yönetici
   panelinin sürüm kartı, `app.kod_surumu()`).
4. **`paket_bilgisi.json`**: derlemenin kimliği ("v6.204 · abc1234 · tarih").
   Yönetici panelinde "Kurulum dosyası" satırı; Mac'te yenilenmiş uygulama
   eski derlemeyi bununla tanıyor. Her derlemede farklı olmalı.
5. **Program pencereli (konsolsuz)**: Windows'ta çift tıklayınca kara pencere
   açılmıyor, Mac'te uygulama. `sys.stdout` yok; `baslat.py` onu boş bir
   akışa bağlıyor (uvicorn'un günlük biçimi `isatty()` sorup çöküyordu) ve
   uvicorn'un iletilerini `program.log`'a yönlendiriyor.
6. Simgeler `static/ikon_512.png`'den (telefondaki simge): Windows'a `.ico`,
   Mac'e köşeleri yuvarlatılmış `.icns`. Pillow yoksa simgesiz derleniyor.

---

## Programın paketteki davranışı (`baslat.py`)

- **`--servis`**: tarayıcı açılmaz, pencere gösterilmez. Windows'ta Görev
  Zamanlayıcı (SYSTEM'in masaüstü yok, görünmeyen bir pencere programı
  bekletirdi), Mac'te oturum açılışı. Denemelerde aynısı `LAB_SESSIZ=1`.
- **Çift tıklama**: program çalışmıyorsa açılır, sunucu hazır olunca tarayıcı
  açılır. Çalışıyorsa (`GET /__pdc`: aynı veri klasörü) yalnızca tarayıcı
  açılır. Başka bir kurulum ya da başka bir program portu tutuyorsa pencereyle
  söylenir.
- **Mac'te yenilenmiş uygulama**: çalışan eski derlemeyi (farklı derleme
  kimliği) SIGTERM ile kapatıp yerine geçer. Uygulama değiştirilince eski
  süreç dosyaları altından değişmiş halde çalışmaya devam ediyordu.
- **Mac'te oturum açılışı**: Uygulamalar klasöründen açılan uygulama
  `~/Library/LaunchAgents/com.patientdatacenter.pdc.plist` yazıyor (`--servis`,
  çökerse yeniden). DMG'den ya da İndirilenler'den açılırsa yazmıyor: macOS
  oradan açılan uygulamayı geçici bir kopyadan çalıştırıyor.
- **Veritabanı yoksa** program ilk kurulum ekranıyla açılıyor (`/kurulum`,
  yalnızca o bilgisayardan). v6.50'deki paket bu durumda açılmıyordu.

---

## Windows kurulum dosyası (`paket/pdc_kurulum.iss`)

[Inno Setup](https://jrsoftware.org/isinfo.php) 6. Dosya UTF-8 BOM'lu (Inno
Setup BOM'suz dosyayı ANSI okur, Türkçe bozulur).

| | |
|---|---|
| Program | `C:\Program Files\Patient Data Center` |
| Veri | `C:\ProgramData\PatientDataCenter` (kaldırınca da kalıyor) |
| Açılışta başlatma | Görev Zamanlayıcı: bilgisayar açılınca, SYSTEM, `--servis` |
| Güvenlik duvarı | 8000 ve 8443, **yalnızca yerel ağ** (tek kural) |
| Kısayollar | Başlat menüsü (+ isteğe bağlı masaüstü): tarayıcıda açar; veri klasörü; program günlüğü; kaldır |

- **Görevi PowerShell kuruyor** (`paket/gorev.ps1`), schtasks değil:
  schtasks'ın kurduğu görev "3 günden uzun sürerse durdur" ayarıyla geliyor,
  sunucu üç günde bir kapanıp bilgisayar yeniden açılana kadar kapalı
  kalırdı. Süre sınırı yok, öncelik normal (Görev Zamanlayıcı'nın varsayılanı
  "normalin altı"), pilde de çalışıyor.
- **Servis değil görev**: servis kurmak için ek bir araç paketlemek gerekirdi.
  Görev Windows'un kendi parçası ve aynı işi görüyor: kimse oturum açmadan
  başlıyor.
- **Güncelleme**: kurulum çalışan programı durduruyor (görev ve elle açılmış
  kopya), `_internal` klasörünü baştan yazıyor, görevi ve kuralı yeniden
  kurup programı başlatıyor.
- Kurulum bitince tarayıcı program cevap verince açılıyor (ilk açılışta
  sertifika ve göçler birkaç saniye).
- Güvenlik duvarı kuralı yerel alt ağ: telefonların Wi-Fi'ı bilgisayardan
  farklı bir alt ağdaysa (hastane ağlarında olabilir) bağlanamazlar; o zaman
  kural bilgi işlemle genişletilir. Program ayrıca kendi ağ erişimi ayarıyla
  kapalı başlıyor (v6.203).

## Mac uygulaması

`Patient Data Center.app`, DMG içinde (Uygulamalar kısayolu + `Kurulum.txt`,
`paket/mac_kurulum.txt`).

- **Dock'ta simge yok** (`LSUIElement`): arka planda çalışan bir sunucu,
  ekranı tarayıcıda. Uygulamaya çift tıklamak tarayıcıyı açıyor.
- **Veri**: `~/Library/Application Support/PatientDataCenter`.
- **İmza**: Apple geliştirici hesabı yok, ad-hoc imzalı. İlk açılışta macOS
  15'te Sistem Ayarları → Gizlilik ve Güvenlik → "Yine de Aç"; eskilerde sağ
  tık → Aç. İmzasız (hiç imzasız) paket Apple Silicon'da "hasarlı" diye hiç
  açılmazdı; iş akışı bütün uygulamayı imzalıyor.
- Apple Silicon (arm64) ve Intel ayrı dosya.
- "Programı kapat" düğmesi yok: kapatmak Etkinlik Monitörü'nden ya da
  oturumu kapatarak. Güncellemede gerekmiyor (yenisi eskisini kapatıyor).

---

## Denendi

- **Linux** (bu geliştirme makinesi, v6.204): paket derlendi (32 MB), duman
  testi geçti -- ilk kurulum ekranı, 53 göç, 23 ekran, hasta, tedavi, iki
  resmî form, altı Excel çıktısı, HTTPS; ikinci açılış çalışan programı tanıyıp
  çıktı; SIGTERM ile düzgün kapandı; günlükte hata yok. Eski derlemeyi
  kapatma ve LaunchAgent yazma Linux'ta ayrıca denendi.
- **Windows ve Mac**: GitHub'ın makinelerinde (aşağıda, README v6.204).
- **Gerçek bir bilgisayarda henüz denenmedi**: ilk kurulumu kullanıcı yapacak.

## Sırada ne var

1. **Gerçek bilgisayarda ilk kurulum** (Windows ve Mac) ve gerekirse düzeltme.
2. **İmzalama.** İmzasız kurulumda Windows "bilinmeyen yayıncı" uyarısı
   veriyor, Mac izin istiyor. Kendi kliniğin için gerekmez; satarken gerekir
   (Windows'ta kod imzalama sertifikası, Mac'te Apple geliştirici hesabı ve
   noter onayı).
