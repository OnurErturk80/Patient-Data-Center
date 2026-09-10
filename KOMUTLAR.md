# Komut kartı

Ara sıra lazım olan komutlar, tek sayfada. Anlatı yok — nedenleri
`MAKINE_GECISI.md` ve `README.md` içinde.

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
| Makineye **otururken** | `python3 tasi.py iceri <usb>` sonra `python3 goc_hepsi.py` |

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

```
python3 goc_hepsi.py
```

**Ne zaman:** `git pull` sonrası, `tasi.py iceri` sonrası, ya da ekranda
"göç gerekli" uyarısı çıkınca. Tekrar tekrar çalıştırmak zararsız.

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

## Sorun teşhisi

```
python3 teshis.py                    # genel kontrol
python3 teshis_silme.py 527078       # bu hasta neden silinemiyor
python3 liste_duzenle.py             # seçim listelerini gör / temizle
python3 yerel_kur.py                 # bu makinenin klasör yollarını ayarla
```

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

Çakışma (`conflict`) çıkarsa **dur**, Claude Code'a sor.

---

## Dikkat — bunu yanlışlıkla çalıştırma

```
python3 sifirdan_kur.py
```

**Boş** bir veritabanı kurar. Sadece yepyeni bir makinede, hiç veri yokken.
Mevcut `lab.db` varken çalıştırma.
