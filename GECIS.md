# Claude Code'a geçiş — yapılacaklar

Sırayla. Takıldığın adımda dur, hata metnini sohbete getir.

## 1. Kur

**Mac** — Terminal'i aç:
```
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows** — PowerShell'i aç (başında `PS C:\` yazıyorsa doğru yerdesin):
```
irm https://claude.ai/install.ps1 | iex
```
Windows'ta ayrıca **Git for Windows** kurman öneriliyor — Claude Code komut
çalıştırmak için ona ihtiyaç duyuyor.

Kurulum bitince kontrol:
```
claude --version
claude doctor
```

## 2. Projeyi git deposuna çevir (bir kez, tek makinede)

Proje klasöründe:
```
git init
git add .
git commit -m "Lab Kayit v6.0 - Claude Code'a gecis"
```

`.gitignore` dosyası zaten hazır: `lab.db`, `arsiv/`, `snapshot/` ve
`yerel_ayar.json` git'e girmez. Bunlar veri ve makineye özel ayar — USB ile
taşınmaya devam eder.

Not: git yerel çalışır, buluta bir şey gitmez. İki makine arasında kodu
senkronize etmek istersen GitHub'da **private** bir depo açman gerekir; hasta
verisi zaten `.gitignore`'da olduğu için depoya girmez. İstemezsen kodu da
eskisi gibi USB ile taşıyabilirsin — git yine de "geri al" imkânı verir.

## 3. İlk oturum

Proje klasöründe:
```
claude
```
İlk çalıştırmada tarayıcı açılır, Claude hesabınla giriş yaparsın.

## 4. İlk mesaj

Şunu yapıştır:

> Bu bir IVF laboratuvarı kayıt programı. Proje klasöründeki CLAUDE.md
> dosyasını oku, sonra README.md'nin son 200 satırına bak. Ardından uygulamayı
> çalıştırıp ana ekranı açarak çalıştığını doğrula. Bana ne anladığını özetle,
> henüz bir değişiklik yapma.

Özet doğruysa devam et. Yanlış anladığı bir yer varsa düzelt — o düzeltmeyi
CLAUDE.md'ye de yazmasını iste.

## 5. İlk gerçek iş için öneri

Küçük ve doğrulanabilir bir şeyle başla, aleti tanı:

> goc_018.py'yi çalıştır, endikasyon listesindeki serbest metin kopyalarını
> temizle. Sonra listeyi bana göster.

Sonra bekleyen işlere geç. Sıra önerim:
1. **Yedekleme kurulumu** — gerçek hasta verisi girmeden önce
2. Bozuk OPU tarihinin düzeltilmesi (`0026-09-04`)
3. **Biyopsi / PGT modülü** — kalan tek ana modül

## Neyi nerede yapacaksın

- **Claude Code** — kod yazma, hata ayıklama, göç çalıştırma, yedekleme kurulumu
- **Sohbet (buradaki)** — tasarım tartışmaları, ekran görüntüsü paylaşımı,
  "şu ekran karışık görünüyor" türü geri bildirim, klinik mantık konuşmaları
