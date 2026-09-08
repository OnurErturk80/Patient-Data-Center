# İki makine arasında çalışma — adım adım

Mac (evde, test verisi) ↔ Windows mini PC (klinikte, gerçek veri).
Bu dosyayı takıldığında aç. Emin olmadığın adımda dur, Claude Code'a sor.

---

## Önce bunu oku — 5 temel kural

1. **Kod** GitHub üzerinden gider gelir: `git pull` (indir) / `git push` (gönder).
2. **Veri** git'e girmez, GitHub'a gitmez: `lab.db`, `arsiv/`, `snapshot/`,
   `yedek.log`, `yerel_ayar.json`. (`.gitignore` bunları dışarıda tutar.)
3. **Gerçek hasta verisi klinikteki Windows mini PC'de yaşar.** Mac'te test
   verisiyle çalışırsın. Mac'in `lab.db`'sini Windows'a **götürme**.
4. **Aynı anda tek makinede kayıt gir.** İki makinede birden gerçek kayıt girip
   sonra birini taşırsan diğerindekiler kaybolur — birleştirmenin yolu yok.
5. `yerel_ayar.json` her makinede **ayrı kalır**, taşınmaz. (Kamera klasörü
   yolları gibi makineye özel ayarlar burada.)

Kısa hali: **kodu senkronize et, veriyi etme.**

---

## Her oturumun rutini (hangi makine olursa olsun)

### İşe başlarken
```
cd "Patient Data Center"        # Windows'ta kendi yolun
git pull
```
- "Already up to date" → değişiklik yok, devam et.
- Dosyalar indi → diğer makinede yapılan iş geldi, devam et.
- "conflict" / "unrelated histories" → **dur**, aşağıdaki "Sık sorunlar"a bak.

### İş bitince
```
git status                      # neyin değiştiğini gör
git add -A
git commit -m "kısa açıklama"
git push
```
Ya da Claude Code'a **"commit et ve push et"** de.

> **`git push` yapmadan diğer makineye geçme.** Geçersen orada eski kodla
> çalışırsın ve sonra çakışma çıkar.

---

## Senaryo 1 — Mac → Windows (evden kliniğe)

Evde Mac'te değişiklik yaptın, klinikte Windows'ta devam edeceksin.

### A. Mac'te — ayrılmadan önce
1. Uygulamayı durdur (Ctrl+C).
2. `git status` → her şey commit'li mi kontrol et.
3. `git add -A && git commit -m "ne yaptığının özeti"`
4. `git push`
5. `git status` → **"Your branch is up to date with 'origin/main'"** yazmalı.

Mac'teki `lab.db` test verisidir; hiçbir şeyini USB'ye kopyalamana gerek yok.

### B. Windows'ta — klinikte
1. Uygulama açıksa durdur.
2. **Önce yedek al** (gerçek veri burada, koda dokunmadan önce):
   ```
   python yedek.py E:\yedek
   ```
   (Görev Zamanlayıcı zaten her gün alıyorsa da elle bir kez almak iyi.)
3. Kodu güncelle:
   ```
   cd "Patient Data Center"
   git pull
   ```
4. Şema değiştiyse göçleri çalıştır:
   ```
   python goc_hepsi.py
   ```
   (Kod yeni tablo/kolon eklediyse gerekir. Ekranlarda "göç gerekli" uyarısı
   çıkarsa bu adımı atlamışsındır.)
5. Çalıştır ve gör:
   ```
   python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
   ```
   Değiştirdiğin ekranı tarayıcıda gerçekten aç.

Windows'un `lab.db`'si (gerçek veri) yerinde kaldı — sadece kod güncellendi.

---

## Senaryo 2 — Windows → Mac (klinikten eve)

Klinikte Windows'ta çalıştın, evde Mac'te devam edeceksin.

### A. Windows'ta — ayrılmadan önce
1. Uygulamayı durdur.
2. **Kod değiştiysen:**
   ```
   git add -A && git commit -m "ne yaptığının özeti" && git push
   ```
3. Kod değişmediyse (sadece kayıt girdin, ekranlara baktın) → push'a gerek yok.
   Gerçek veri zaten Windows'ta kalıyor.

### B. Mac'te — evde
1. Kodu güncelle:
   ```
   cd "Patient Data Center"
   git pull
   ```
2. Göç gerekiyorsa:
   ```
   python3 goc_hepsi.py
   ```
3. Çalıştır:
   ```
   python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
   ```

Mac kendi test `lab.db`'siyle devam eder.

### C. (İsteğe bağlı) Gerçek veriyle test etmek istersen
"Gerçek veride şu ekran nasıl duruyor" diye bakmak istediğinde:

1. **Windows'ta:** `lab.db` ve `arsiv/` klasörünü USB'ye kopyala.
2. **Mac'te:** kendi `lab.db`'ni önce bir kenara sakla → `lab_test.db` diye
   yeniden adlandır.
3. USB'deki `lab.db` ve `arsiv/`'i Mac proje klasörüne koy.
4. `python3 goc_hepsi.py` (Mac'teki kod daha yeniyse göçleri uygular).
5. Bak, dene.
6. **Bittiğinde bu `lab.db`'yi Windows'a GERİ GÖTÜRME.** Sil, `lab_test.db`'yi
   geri `lab.db` yap.
   > Sebep: sen bakarken klinikte yeni kayıt girilmiş olabilir. Elindeki kopya
   > eskir; geri götürürsen klinikteki yeni kayıtları ezersin.

---

## Sık sorunlar

**`git pull` → "refusing to merge unrelated histories" / "unrelated histories"**
Klasörü `git init` + remote ekleyerek oluşturmuşsun; doğrusu boş bir yere
`git clone`. Çöz:
```
# klasörü yeniden adlandır: "Patient Data Center" -> "Patient Data Center_eski"
git clone https://github.com/OnurErturk80/Patient-Data-Center.git "Patient Data Center"
# _eski'den yeni klasöre kopyala: lab.db, arsiv/, snapshot/, yerel_ayar.json
python goc_hepsi.py        # Mac'te python3
```

**`git pull` → "conflict" (çakışma)**
İki makinede aynı dosyayı değiştirip ikisini de commit etmişsin. **Dur.**
Claude Code'a "pull çakışması var" de, birlikte çözün. Tek başına
`git checkout --theirs/--ours` gibi komutlar deneme.

**`git push` → "rejected" / "non-fast-forward"**
Diğer makineden push edilmiş, sen pull etmemişsin. Önce `git pull`, çakışma
yoksa tekrar `git push`.

**Uygulama açılıyor ama bir ekran/gün eksik görünüyor**
Göç çalıştırmayı unutmuşsun:
`python goc_hepsi.py` (Windows) / `python3 goc_hepsi.py` (Mac).

**`lab.db` yanlışlıkla git'e girmiş mi?**
```
git ls-files | grep -E "lab.db|arsiv/|snapshot/|yerel_ayar"
```
Bir şey dönerse Claude Code'a haber ver — `.gitignore`'a rağmen takibe girmiş
olabilir, çıkarmak gerekir.

**`git status` → "Your branch is ahead of 'origin/main' by N commits"**
Commit etmişsin ama push etmemişsin. `git push`.

---

## Komut özeti

| | Mac | Windows |
|---|---|---|
| Python | `python3` | `python` |
| Çalıştır | `python3 -m uvicorn app:uygulama --host 0.0.0.0 --port 8000` | `python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000` |
| Göçler | `python3 goc_hepsi.py` | `python goc_hepsi.py` |
| Yedek | `python3 yedek.py ~/lab_yedek` | `python yedek.py E:\yedek` |
| Durdur | Ctrl+C | Ctrl+C |
| Depo | `https://github.com/OnurErturk80/Patient-Data-Center.git` | aynı |

---

## İlk kurulum (her makinede bir kez — referans)

### Mac — yapıldı (2026-09-08)
Git deposu başlatıldı, GitHub'a push edildi, `~/lab_yedek` ile elle yedek test
edildi.

### Windows mini PC — bir kez yapılacak
1. **Claude Code:** PowerShell'i aç →
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
2. **Git for Windows:** git-scm.com → kur (Claude Code komut çalıştırmak için
   gerekiyor).
3. **Python 3.10+:** python.org → kurulumda **"Add Python to PATH"** işaretle.
4. **Depoyu klonla** (Masaüstünde, boş bir yere — `git init` DEĞİL):
   ```
   git clone https://github.com/OnurErturk80/Patient-Data-Center.git "Patient Data Center"
   ```
   İlk seferde GitHub girişi ister (Git Credential Manager tarayıcı açar).
5. **Eski Windows klasöründen** yeni klasöre kopyala: `lab.db`, `arsiv\`,
   `snapshot\`, `yerel_ayar.json`. (Eskiden `app\` alt klasöründeyseler oradan
   al — yeni yapı düz.)
6. **Bağımlılıklar:**
   ```
   python -m pip install fastapi uvicorn jinja2 python-multipart
   ```
7. **Göçler + test:**
   ```
   python goc_hepsi.py
   python -m uvicorn app:uygulama --host 0.0.0.0 --port 8000
   ```
8. Çalıştığını görünce eski klasörü `Patient Data Center_eski` diye adlandır,
   bir süre dursun, sonra sil.
9. **Yedekleme:** Görev Zamanlayıcı + `yedek.bat` (README v1.2 bölümü anlatıyor),
   hedef `E:\yedek` — veritabanından farklı bir disk olmalı.
