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
python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
```

Durdurmak: **Ctrl+C**.

Kendi bilgisayarında: <http://localhost:8000>

**Telefondan girmek için** bu makinenin iç ağ adresi lazım:

```
ipconfig getifaddr en0        # Mac (kablosuz)
ipconfig                      # Windows — "IPv4 Adresi" satırı
```

Çıkan adresle: `http://192.168.1.42:8000` (numara sizde farklı olacak).
Telefon aynı Wi-Fi'da olmalı. Program açık kalmalı.

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

## Yedek

```
python3 yedek.py                 # bu makinenin ayarlı klasörüne
python3 yedek.py ~/lab_yedek     # elle hedef vererek
python  yedek.py E:\yedek        # Windows, klinik
```

Hedef **farklı bir diskte** olmalı — aynı disk bozulursa yedek de gider.

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

`lab.db`, `yerel_ayar.json`, `arsiv/` ve `snapshot/` **veri klasöründe**.
Bugünkü kurulumlarda bu proje klasörünün kendisi (kodun yanında `lab.db`
varsa orası kullanılıyor). Paketlenmiş kurulumlarda işletim sisteminin veri
klasörü olacak. Nerede olduğunu görmek için:

```
python3 -c "import db; print(db.VERI_KOK)"
```

Başka bir klasörle çalıştırmak (deneme için):

```
LAB_VERI=/bir/klasor python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
```

---

## Sorun teşhisi

```
python3 teshis.py                    # genel kontrol
python3 teshis_silme.py 527078       # bu hasta neden silinemiyor
python3 liste_duzenle.py             # seçim listelerini gör / temizle
python3 tarih_duzelt.py liste        # bozuk tarih var mı (dokunmaz)
python3 yerel_kur.py                 # bu makinenin klasör yollarını ayarla
```

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

Hiçbiri veri silmez.

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

**Yeni bir kutu/düğme göründü ama hiçbir şey yapmıyor**
`git pull` yaptın, programı yeniden başlatmadın. Şablonlar diskten tazelenir,
Python kodu tazelenmez. `Ctrl+C` → `python3 baslat.py`.

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
