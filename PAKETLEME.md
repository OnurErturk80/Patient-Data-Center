# Kurulabilir uygulama yapma

Program bugün Python + `uvicorn` ile çalışıyor. Başka bir kliniğe kurmak için
bu adımlar gerekiyordu: Python kur, `pip install ...`, göçleri çalıştır,
uvicorn'u başlat, açılışta otomatik başlaması için görev tanımla. **Hiçbir
klinik bunu yapmaz.**

Paketleme bunu tek dosyaya indiriyor. Kullanıcı çift tıklıyor, program
kuruluyor ve bilgisayar açıldığında kendiliğinden çalışıyor.

Hazırlık üç sürümde yapıldı:

- **v6.46** — veri programdan ayrıldı (`PROGRAM_KOK` / `VERI_KOK`). Paketin
  içi salt okunur; veri oraya yazılamaz, yazılsa bile güncellemede silinirdi.
- **v6.49** — göçler açılışta kendiliğinden çalışıyor, süreç içinde. (Alt
  süreç açmak paketlenmiş uygulamada **programı** yeniden başlatırdı.)
- **v6.50** — giriş noktası (`baslat.py`) ve PyInstaller tarifi
  (`paket/pdc.spec`).

---

## Derleme

Hangi işletim sistemi için paket yapacaksan **o işletim sisteminde** derle.
PyInstaller çapraz derleme yapmaz: Windows paketi Windows'ta, Mac paketi
Mac'te üretilir.

```
pip install pyinstaller
pyinstaller paket/pdc.spec          # proje kökünde çalıştır
```

Çıktı: `dist/PatientDataCenter/`. İçinde çalıştırılabilir dosya ve
`_internal/` klasörü var; **ikisi birlikte** taşınır.

`build/` ve `dist/` git'e girmiyor — her makinede yeniden üretiliyor.

### Tarifte dikkat edilen iki şey

Bunlar eksik kalırsa program açılır ama **sessizce** bozuk çalışır:

1. **Şablonlar ve `static/` veri olarak ekleniyor.** PyInstaller yalnızca
   `import` edilenleri toplar; Jinja şablonlarını ve CSS'i göremez.
2. **Göç betikleri `hiddenimports`'ta.** `importlib.import_module("goc_029")`
   ile adıyla çağrıldıkları için PyInstaller onları göremiyor. Eksik kalırsa
   veritabanı güncellemeleri sessizce çalışmaz.

Yeni bir göç yazdığında tarif onu **kendiliğinden** buluyor (dosya adına
bakıyor), elle eklemek gerekmiyor.

---

## Denendi

Linux paketi üretilip **kaynak klasörünün dışında**, `PYTHONPATH` temizlenmiş
halde çalıştırıldı:

- Program açıldı, veri klasörünü ortam değişkeninden buldu
- **27 göç kendiliğinden uygulandı** (paketin içinden)
- 22 adres 200 verdi: bütün ekranlar, `static/`, `manifest.json`, karekod,
  resmî form ve Excel çıktısı
- Günlük hem konsola hem veri klasöründeki `program.log`'a düştü

Paket boyutu ~32 MB.

---

## Windows kurulum dosyası

`paket/pdc_kurulum.iss` — [Inno Setup](https://jrsoftware.org/isinfo.php) ile
derleniyor. **Bu dosya henüz Windows'ta denenmedi**; ilk kurulumda birlikte
gözden geçirilecek.

Yaptığı işler:

| | |
|---|---|
| Program | `C:\Program Files\Patient Data Center` |
| Veri | `C:\ProgramData\PatientDataCenter` |
| Açılışta başlatma | Görev Zamanlayıcı görevi (`onstart`, SYSTEM) |
| Güvenlik duvarı | 8000 portuna **yerel ağ** için izin |
| Başlat menüsü | tarayıcıyı programın adresinde açan kısayol |

Servis yerine Görev Zamanlayıcı: servis kurmak için ek bir araç (NSSM gibi)
paketlemek gerekirdi. Görev Zamanlayıcı Windows'un kendi parçası ve aynı işi
görüyor — bilgisayar açıldığında, kimse giriş yapmadan başlıyor.

**Güvenlik duvarı kuralı bilerek yalnızca yerel ağ için.** Program dışarıya
açılmamalı (bekleyen iş 3: HTTPS yok).

---

## Sırada ne var

1. **İlk kurulum ekranı.** Paket bugün `lab.db` yoksa "önce kurulumu
   tamamlayın" deyip duruyor. Yeni bir klinikte veritabanını ve ilk yönetici
   hesabını kuracak bir ilk açılış akışı gerekiyor — `sifirdan_kur.py` soru
   soruyor, paketlenmiş uygulamada terminal yok.
2. **İmzalama.** İmzasız kurulumda Windows "bilinmeyen yayıncı" uyarısı
   verir, Mac "geliştirici doğrulanamadı" deyip açmaz. Kendi kliniğin için
   gerekmez; satarken gerekir.
3. **HTTPS kararı.** Android'de ana ekran simgesinin tam ekran açılması ve
   "tek dokunuşla ekle" düğmesi buna bağlı.
