"""Access'ten dışa aktarılmış tedavi kayıtlarını programa alır.

Kullanıcının isteği (2026-09-22): "Bu accdb dosyasında ağustos ayında
laboratuvarda tedavisini yaptığım hastalar... hasta kartı oluşturup
tedavileri ekler misin? Eğer aynı hasta varsa oluşturulmuş hasta kartına
tedaviyi ekle." Amacı: "bir hastanın tedavi sayısı, daha önce ne yapıldığı,
kaç yumurta toplanıp ne kadar döllenip ne kadarı embriyo olduğu, ne kadar
dondurulduğu, transfer yapılıp sonuca ulaştı mı önemli."

**Bu bir araç, programın parçası değil.** Program `.accdb` okumuyor ve
okumayacak (ek bağımlılık yok kuralı) -- Access'ten CSV'ye aktarılmış bir
dosyayı okuyor. Programın koduna dokunmuyor, yalnızca kendi tablolarına
kayıt yazıyor.

Kullanım:
    python3 aktar_access.py liste  agustos.csv    ne yazılacağını gösterir
    python3 aktar_access.py        agustos.csv    AKTAR yazınca uygular

**İkinci bir Access dosyası aktarıyorsan `kaynak=` ver:**

    python3 aktar_access.py liste kaynak=TEMMUZ temmuz.csv
    python3 aktar_access.py       kaynak=TEMMUZ temmuz.csv

Her Access dosyası kendi kayıtlarını 1'den numaralandırıyor; etiket olmadan
ikinci dosyanın ilk satırları birincinin numaralarıyla çakışır ("Aynı tedavi
iki kez girmiyor" bölümüne bak). Unutursan betik **durur**, yazmaz.

**Önce `liste` ile bak.** Ne yazılacağını satır satır döküyor; hiçbir şeye
dokunmuyor. Aktarmadan önce yedek al (`/yedekleme` → "Şimdi yedekle").

**Dosyaları tarih sırasıyla aktar** (ocak, şubat, ...): FET'te çözülen
embriyo, dondurulduğu tüp programdaysa ona bağlanıyor (v6.148) -- tüpün
dondurulduğu ay önce aktarılmış olmalı. Daha önce aktarılmış dosyalar için
`tamamla` (aşağıda) aynı işi yapıyor.

**Yazım hatalı tarihler için `duzelt=`** (v6.148): Access'te bir OPU
"02.06.2026" yazıyor ama iş ocakta yapılmış. Düzeltmeler ayrı bir dosyada
(kayıt numaraları hasta verisine bağlı, depoya girmez), satır biçimi
`duzeltmeleri_oku()`'da:

    python3 aktar_access.py kaynak=OCAK duzelt=tarih_duzeltme.txt ocak.csv

**Daha önce aktarılmış dosya: `tamamla`.** Aracın yeni kuralları (dondurma
onarımı, taze transfer, çözmenin kaynağa bağlanması) baştan aktarmadan
uygulanıyor; ikinci kez çalıştırmak hiçbir şeyi değiştirmez:

    python3 aktar_access.py tamamla kaynak=TEMMUZ temmuz.csv
    python3 aktar_access.py tamamla agustos.csv

**Yalnızca iptal sebebi: `iptal`** (v6.150). v6.149'a kadar araç "Yumurta
Çıkmadı" / "İmmatür Yumurta" sebeplerini tanımıyordu, o notlar genel
"İptal" oldu. Bu kip yalnızca hâlâ genel "iptal"de kalan tedavinin sebebini
günceller, başka hiçbir şeye dokunmaz (`tamamla` elle düzeltilmiş skoru
ezebilir, bu kip ezmez):

    python3 aktar_access.py iptal kaynak=OCAK ocak.csv

**Yalnızca FET transfer kalitesi: `transfer`** (v6.154). v6.153'e kadar
araç FET'te transfer edilen embriyonun kaynaktaki hücre/kalite kutularını
(EMBRİYO1/2) yalnızca transfer notuna yazıyordu; resmî formların transfer
bölümü boş kalıyordu. Bu kip yalnızca o değerlendirmeyi yazar, başka hiçbir
şeye dokunmaz:

    python3 aktar_access.py transfer kaynak=MAYIS mayis.csv

------------------------------------------------------------------------
ACCESS'TEN CSV NASIL ÇIKAR

1. Access'te veritabanını aç, sol taraftaki tablolardan **VERİTABANI**'nı
   seç (tıkla, açmana gerek yok).
2. Dış Veri (External Data) → Dışa Aktar → **Metin Dosyası**.
3. "Verileri kaynak biçimlendirmesi ... ile dışa aktar" seçeneğini işaretle.
4. Sihirbazda **Ayrılmış (Delimited)**, ayırıcı virgül ya da noktalı virgül
   (ikisi de okunuyor), "İlk satır alan adlarını içerir" **işaretli**,
   metin niteleyici `"`.
5. Kodlama **UTF-8** olsun (Gelişmiş düğmesi). Değilse Türkçe harfler
   bozulur ve betik kolon adlarını bulamaz.

Betik `.accdb` dosyasını okumuyor: okumak için ek bir kütüphane gerekirdi
ve bu programın "ek bağımlılık yok" kuralı tam bunun için var (`excel.py`,
`karekod.py`, `xlsx_oku.py` hepsi aynı sebeple kütüphanesiz).

**Tarih biçimi**: `19.08.2026`, `08/19/26` ve `2026-08-19` tanınıyor.
Gün/ay sırası belirsizse (ikisi de 12'den küçük) nokta ayıracı gün.ay,
eğik çizgi ay/gün sayılıyor -- Access ile mdbtools'un yaptığı bu. `liste`
kipi her satırın tarihini basıyor; **aktarmadan önce oradan bak**, yanlış
okunmuşsa hemen görürsün.

------------------------------------------------------------------------
NASIL EŞLEŞTİRİYOR

**Dosya numarasıyla.** Access'te "DOSYA NO" var ve şemadaki
`UNIQUE (lab_id, dosya_no)` sayesinde "aynı dosya no" = "aynı hasta satırı".
İsim benzerliğine hiç bakılmıyor (CLAUDE.md "isimle eşleştirme yok").
- Dosya no programda varsa: yeni hasta açılmıyor, tedavi o karta ekleniyor.
  Hastanın adı **üzerine yazılmıyor** -- programdaki kayıt daha yeni
  olabilir; yalnızca BOŞ olan alan (eş adı, doğum tarihi, telefon)
  dolduruluyor.
- Yoksa yeni hasta kartı açılıyor (ad ve eş adı `tr_buyuk()` ile, v6.115).

**Aynı tedavi iki kez girmiyor.** Her tedavinin protokol notuna Access'in
kendi kayıt numarası yazılıyor (`[Access kaydı #12]`); o işareti taşıyan
bir tedavi zaten varsa satır atlanıyor. Yani betiği iki kez çalıştırmak
güvenli, yarıda kalırsa kaldığı yerden devam eder.

**Ama numara dosya başına 1'den başlıyor** -- ağustos dosyasının #1'i ile
temmuz dosyasının #1'i aynı işareti üretir ve ikinci dosyanın o satırları
"zaten aktarılmış" sanılıp SESSİZCE atlanır. Bu yüzden ikinci dosyadan
itibaren `kaynak=TEMMUZ` verilir: işaret `[Access kaydı TEMMUZ#5]` olur,
ağustosun `[Access kaydı #5]`'iyle karışmaz (kapanış `]` sayesinde `#1]`
deseni `#10]`'u da yakalamıyor). Ağustos etiketsiz kaldı, öyle kalmalı --
etiket verilirse o satırlar yeniden aktarılır.

Unutulursa betik **durup soruyor**: işaret bir tedavi buluyor ama o tedavi
BAŞKA bir hastanınsa (dosya no tutmuyorsa) bu bir yeniden çalıştırma değil,
çakışmadır; hiçbir şey yazılmadan çıkıyor. Uyarıp devam etmiyor -- sessiz
veri kaybı bu projenin tuzak listesinin tam olarak uyardığı şey.

------------------------------------------------------------------------
SAYILAR NEDEN OOSİT OOSİT AÇILIYOR

Access toplam tutuyor ("8 toplandı, 6 MII, 4 2PN"); program her oositi ayrı
kaydedip sayıları ONDAN HESAPLIYOR (CLAUDE.md "istatistikler türetilmiştir",
`cycle_ozet()`). Yani sayıyı yazacak bir kolon yok -- altı tane oosit
kaydında "MII" yazması gerekiyor.

Bu yüzden her tedavi için TOPLANAN OOSİT kadar `specimen` satırı ve
sayılara uyan `olay` satırları açılıyor. Böylece tedavi ekranındaki özet,
hasta kartı, `/istatistik` oranları ve Excel çıktıları hiçbir kod
değişikliği gerekmeden doğru çalışıyor.

**Bedeli dürüstçe yazılıyor**: hangi oositin MII olduğu Access'te yok,
sırayla dağıtılıyor. Her tedavinin protokol notunda bu satır duruyor, yani
ekranda da resmî formda da görünüyor:

    Yumurta kayıtları toplam sayılardan üretildi, tek tek gözlem değildir.

Dağıtım kuralı (tek yerde, `_oositleri_ac()`): önce MII'ler, sonra immatür,
sonra empty zona, dejenere, atretik. ICSI önce MII'lere veriliyor; İŞLEME
ALINAN sayısı MII'den fazlaysa (bir satırda öyle: 12 MII, 13 işlem) kalanı
immatürlere gidiyor. Fertilizasyon işlem gören oositlere: önce 2PN'ler,
sonra INTAKT'lar.

**INTAKT = 0PN.** Kaynak kayıtta her satırda
`İŞLEME ALINAN = 2PN + ANORMAL + İŞLEM SONRASI DEJENERE + INTAKT`
tutuyor (yirmi satırın hepsinde doğrulandı) -- yani INTAKT "döllenmemiş,
bütün kalmış" oosit demek, programın `pn_sayisi` listesindeki `0` bu.

------------------------------------------------------------------------
KARŞILIĞI OLMAYAN ALANLAR -- UYDURULMUYOR

- **EMPTY ZONA**: `maturasyon` listesinde karşılığı yok (mii/mi/gv/
  degenere/atretik). O oositler kayıt olarak açılıyor ama maturasyon olayı
  yazılmıyor, sayısı nota düşüyor.
- **İMMATÜR (MI+GV)**: Access ikisini toplamış, program ayrı tutuyor.
  Hepsi `mi` yazılıyor, nota "MI/GV ayrımı kaynak kayıtta yok" düşüyor.
- **OPU sağ/sol**: kaynakta taraf yok, tek toplam var. Toplam
  `opu_sag_oosit`e yazılıyor ("Toplanan" bu ikisinin toplamı, v6.112) ve
  nota "taraf ayrımı kaynak kayıtta yok" düşüyor.
- **Cleavage / blastokist sayısı**: kaynakta gün 2/3/5'te kaç embriyo
  olduğu YOK. Aşama yalnızca **dondurulan** ve **transfer edilen** embriyo
  için yazılı ("5,GÜN", "3.GÜN").
  - Dondurulanlar ve IVF/ICSI'de taze transfer edilenler (v6.148) için o
    kadarı kaydediliyor, skoru nottan / EMBRİYO1-2 kutusundan
    (`_dondurma_kayitlari()`, `_taze_transfer()`). Yani bu sayılar "en az"
    demek -- gün 5'e ulaşıp dondurulmayan embriyo kaynakta hiç görünmüyor.
    `/istatistik`'in blastokist oranı bu yüzden olduğundan düşük çıkar.
  - FET'te transfer edilen embriyo için **yazılmıyor**: kültür yapılmayan
    FET'te bu tedavide bir değerlendirme yok. Aşaması ve kalitesi transfer
    olayının notunda duruyor ("5. gün", "3AA").
- **Dondurulan örneğin taşıyıcısı**: nottaki her parantez grubu bir tüp
  (v6.132), etiketi vitrifikasyon ekranının kendi önerisi. **Konum**
  kaynakta yok, boş kalıyor; Cryo Haritası tüpü "konum girilmemiş" gösterir.
  Dondurulan yumurta da (yumurta dondurma, "(3*M2) (2*M1)") tüp tüp
  yazılıyor (v6.142, MI yumurta v6.148).
- **Gebelik sonucu**: kaynağın bütün gebelik alanları (BHCG, USG, doğum)
  **boş**. "Transfer yapılıp sonuca ulaştı mı" sorusunun ilk yarısı
  aktarılıyor (transfer var/yok), ikinci yarısı bu dosyada yok.
- **TEDAVİ PROTOKOLÜ** (GONAPEPTYL gibi ilaç adı) `protokol_tipi`
  listesine (antagonist/long agonist/...) uymuyor; eşlemek klinik bir
  varsayım olurdu. Ham metin nota yazılıyor, `protokol_tipi` boş kalıyor.
- Karşılığı olmayan ötekiler (INTAKT dışındaki sayımlar, transfer
  klinisyeni, medium/lot) forma da boş giriyor -- README v6.37'nin kuralı.

------------------------------------------------------------------------
FET: EMBRİYO NEREDEN GELİYOR

`fet` tedavilerinde çözülen embriyolar daha önceki aylarda -- programın
olmadığı dönemde -- dondurulmuş. Kaynak tedavi programda YOK.

CLAUDE.md `specimen.cycle_id`'nin embriyonun KENDİ cycle'ı olduğunu
söylüyor; burada o cycle hiç yok. İki seçenek vardı: (a) embriyoyu hiç
kaydetmemek, (b) FET tedavisinin kendi altına kaydetmek.

**(b) seçildi**, çünkü ağustosta yapılan BÜTÜN transferler FET: (a) ile
program "ağustosta hiç transfer yapılmamış" derdi ve kullanıcının en çok
istediği bilgi (transfer yapıldı mı) kaybolurdu. Embriyolar FET'in kendi
altında açılıyor, `thaw`/`transfer` olayları `thaw_cycle_id`/`tr_cycle_id`
ile yine aynı tedaviyi gösteriyor -- program her yerde
`COALESCE(tr_cycle_id, s.cycle_id)` kullandığı için sayılar doğru çıkıyor.

Bunun tek yan etkisi vardı: `/istatistik`'in "kayıtlı oosit" sayısı
`specimen` satırlarını sayıyor ve FET embriyoları toplanmış yumurta gibi
görünüp MII oranını düşürüyordu. Bu, aktarımdan bağımsız bir doğruluk
hatası (çözülmüş bir embriyo hiçbir dünyada "toplanan oosit" değil), o
yüzden `disari.istatistikler()`'de düzeltildi: oosit sayımı artık yumurta
toplanan tedavilerle sınırlı.

**v6.148: kaynak programdaysa bağlanıyor.** Ocak-haziran aktarılınca çoğu
FET'in çözdüğü tüp programda. Embriyolar yine önce FET'in altında açılıyor,
sonra `_kaynaga_bagla()` hastanın dolu tüpleri arasında tek bir eşleşme
bulursa bütün olayları o tüpün örneklerine taşıyıp FET'in kendi örneklerini
siliyor -- program bir tüpü kendisi çözmüş gibi. Birden çok seçenek ya da hiç
tutmayan tüp varsa bağlanmıyor, rapor kayıt numarasıyla söylüyor
(kullanıcının kararı: "Bağla, belirsizi listele").

------------------------------------------------------------------------
YUMURTA ÇÖZME, PGT KÜLTÜRÜ, TARİHSİZ SATIR (v6.148)

- "OOSİT ÇÖZME" protokolü Yumurta Çözme tedavisi (`cycle_tipi()`):
  yumurtalar çözme olayıyla açılıyor, ICSI ve sonrası IVF/ICSI'deki gibi
  (`_oositleri_ac()`), çözme günü = transfer günü − transfer aşaması.
- OPU'su ve toplanan yumurtası olmayan, ÇÖZDÜRÜLEN sayısı dolu satır FET
  (3→5 kültür): çözülüp kültüre edilen, PGT'den sonra yeniden dondurulan
  embriyo (`_satir_tipi()`).
- Tarihi olmayan satır Access'teki bir önceki kaydın tarihini alıyor, not
  "yaklaşık" diyor; OPU/transfer alanı boş kalıyor (`tarihleri_tamamla()`).
- Aynı hastanın aynı günkü dolu satırının boş kopyası atlanıyor
  (`bos_kopyalari_ayikla()`).
"""


import csv
import datetime as _dt
import glob
import itertools
import os
import re
import sys
import textwrap

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)

DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi.")


# --------------------------------------------------------------- yardımcılar

def tr_buyuk(deger):
    """Türkçe büyük harf. `app.tr_buyuk()`'ün birebir kopyası.

    Göç/araç betikleri `app.py`'yi import etmiyor (goc_040'ın deseni).
    `str.upper()` Türkçe 'i'yi yanlış çeviriyor -- v6.115.
    """
    if deger is None:
        return None
    return deger.replace("i", "İ").upper()


def _m(s):
    return (s or "").strip()


def _sayi(s, varsayilan=None):
    s = _m(s)
    if not s:
        return varsayilan
    try:
        return int(float(s.replace(",", ".")))
    except ValueError:
        return varsayilan


def _ondalik(s):
    s = _m(s)
    if not s:
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def _tarih(s):
    """Access'in yazdığı tarihi ISO'ya çevirir. Çevrilemezse None.

    mdbtools `08/19/26 00:00:00` (ay/gün/yıl), Access'in kendi dışa
    aktarımı `19.08.2026` ya da `19/08/2026` yazabiliyor. Üçü de tanınıyor;
    belirsiz olan ilk iki parça, ay/gün sırası **12'den büyük olana** göre
    çözülüyor.
    """
    s = _m(s)
    if not s:
        return None
    s = s.split()[0]
    e = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if e:
        return s
    p = re.split(r"[./-]", s)
    if len(p) != 3 or not all(x.isdigit() for x in p):
        return None
    a, b, y = int(p[0]), int(p[1]), int(p[2])
    if y < 100:
        # İki haneli yıl: 00-29 -> 2000'li, 30-99 -> 1900'lü (Excel/Access'in
        # kendi kuralı). Düz "+2000" doğum tarihlerini 2088'e taşıyordu --
        # tedavi tarihleri 26 (2026), doğum tarihleri 88/96 (1988/1996).
        y += 2000 if y < 30 else 1900
    gun, ay = (b, a) if a <= 12 and b > 12 else (a, b)
    if a <= 12 and b <= 12:          # ikisi de olabilir -> gün.ay (Access TR)
        gun, ay = (a, b) if "." in s else (b, a)
    try:
        return _dt.date(y, ay, gun).isoformat()
    except ValueError:
        return None


def _zaman(iso, saat="09:00:00"):
    return f"{iso} {saat}" if iso else None


# Kaynak kayıttaki metinler elle yazılmış: aynı şey iki türlü yazılmış
# (GONAPEPTLY/GONAPEPTYL, OOSİT/OOİT CRYO, SWİM UP/SWIM UP, KONSANTRAYON/
# KONSANTRASYON, 5,GÜN/5.GÜN). Karşılaştırmadan önce büyük harfe çevirip
# **bütün Türkçe harfleri ASCII'ye katlıyoruz**.
#
# Yalnızca `İ`yi katlamak yetmiyor: ilk yazışta öyleydi ve "3. GÜN EMBRİYO
# ARRESTİ SEBEBİYLE İŞLEM İPTAL EDİLDİ" notu `cleavage_arrest` yerine genel
# "iptal"e düşüyordu — kalıptaki "GUN" ile metindeki "GÜN" tutmuyordu.
# Yeni bir kalıp yazarken kalıbı da ASCII yaz (GUN, ASAMA, COZME).
_KATLA = str.maketrans("İIŞĞÜÖÇ", "IISGUOC")


def _sade(s):
    return re.sub(r"\s+", " ", _m(s)).upper().translate(_KATLA)


FET_TIPLERI = ("fet", "fet_kultur", "yumurta_cozme")   # app.FET_TIPLERI


def cycle_tipi(protokol: str) -> str:
    p = _sade(protokol)
    if "COZME" in p:
        # "OOSİT ÇÖZME" (v6.148): Yumurta Dondurma'da dondurulmuş yumurtanın
        # ayrı bir tedavide çözülüp ICSI'ye alınması -- programın Yumurta
        # Çözme'si (v6.147'den beri ICSI ve sonrası var). Temmuz ve ağustos
        # dosyalarında bu protokol yok (ölçüldü), onların tipi değişmiyor.
        if "OOSIT" in p or "YUMURTA" in p:
            return "yumurta_cozme"
        return "fet"
    if "CRYO" in p or "KRIYO" in p:
        return "oosit_cryo"
    return "ivf_icsi"


def _satir_tipi(protokol: str, opu, toplanan, cozulen) -> str:
    """Satırın tedavi tipi. Protokol adı yetmediğinde sayılar karar veriyor.

    Üç satırın protokolü boş ya da ilaç adı ama OPU'su ve toplanan yumurtası
    yok, ÇÖZDÜRÜLEN sayısı dolu ve notu "çözme sonrası kültüre edilen ...
    PGT ... dondurularak saklandı" diyor: embriyo çözülmüş, 5./6. güne
    kültüre edilip biyopsiden sonra yeniden dondurulmuş. Programda bunun
    karşılığı FET (3→5 kültür) -- `ivf_icsi` sayılsaydı yumurta toplanmış
    gibi görünür, çözme hiç yazılmazdı. Yapılandırılmış alanlara bakılıyor,
    nottaki kelimeye değil (v6.142'nin dersi).
    """
    tip = cycle_tipi(protokol)
    if tip == "ivf_icsi" and not opu and not toplanan and cozulen:
        return "fet_kultur"
    return tip


_HAZIRLAMA = {"SWIM UP": "swim_up", "SWIMUP": "swim_up",
              "KONSANTRASYON": "gradient", "KONSANTRAYON": "gradient",
              "GRADIENT": "gradient", "YIKAMA": "yikama"}
_ALINMA = {"EJAKULAT": "masturbasyon", "EJAKÜLAT": "masturbasyon",
           "TESE": "tese", "TESA": "tesa", "MIKROTESE": "mikrotese",
           "COZME SPERM": "thaw", "ÇÖZME SPERM": "thaw", "DONOR": "donor"}


# ------------------------------------------------------------------ okuma

def satirlari_oku(yol: str) -> list:
    """CSV'yi okur ve her satırı programın anlayacağı bir sözlüğe çevirir."""
    with open(yol, encoding="utf-8-sig", newline="") as f:
        baslik = f.readline()
        f.seek(0)
        # Access Türkçe Windows'ta CSV'yi noktalı virgülle yazıyor, mdbtools
        # virgülle. Ayıracı başlık satırındaki sayısına bakarak seçiyoruz --
        # `csv.Sniffer` kolon adlarındaki noktalı virgülsüz metinlerde
        # yanılabiliyor.
        ayirac = max((";", ",", "\t"), key=baslik.count)
        ham = list(csv.DictReader(f, delimiter=ayirac))
    if not ham:
        sys.exit("CSV bos.")
    gerekli = ("DOSYA NO", "SOYADI", "ADI")
    eksik = [k for k in gerekli if k not in ham[0]]
    if eksik:
        sys.exit(f"CSV'de su kolonlar yok: {', '.join(eksik)}\n"
                 f"Access'te VERITABANI tablosunu disa aktardigina emin ol.")

    cikti = []
    for s in ham:
        def v(k):
            return _m(s.get(k))
        dosya_no = _sayi(v("DOSYA NO"))
        if not dosya_no:
            continue                       # dosya numarasi olmayan satir alinmaz
        opu = _tarih(v("OPU TARİHİ"))
        transfer = _tarih(v("TRANSFER TARİHİ"))
        tip = _satir_tipi(v("TEDAVİ PROTOKOLÜ"), opu,
                          _sayi(v("TOPLANAN OOSİT"), 0),
                          _sayi(v("ÇÖZDÜRÜLEN EMBRİYO SAYISI"), 0))
        # Viabilite yüzde; 100'ü aşan değer (9080, 10090, 1001000) embriyo
        # başına değerlerin bitişik yazılmışı gibi duruyor ("90 ve 80").
        # Hangi embriyonun hangisi olduğu bilinmiyor -- bölünmüyor, alan boş
        # kalıyor, ham yazı çözme olayının notuna gidiyor (v6.148).
        viabilite = _ondalik(v("ÇÖZDÜRME SONRASI VİABİLİTE"))
        viabilite_ham = None
        if viabilite is not None and viabilite > 100:
            viabilite_ham, viabilite = v("ÇÖZDÜRME SONRASI VİABİLİTE"), None
        cikti.append({
            "kimlik": v("Kimlik"),
            # Tedavinin tarihi: OPU, yoksa transfer (FET'te OPU yok). Hem
            # sıralama hem `olusturma_zamani` bundan besleniyor.
            "tarih": opu or transfer,
            "dosya_no": dosya_no,
            "ad_soyad": tr_buyuk(f'{v("ADI")} {v("SOYADI")}'.strip()),
            "es_adi": tr_buyuk(v("EŞİNİN ADI")) or None,
            "dogum_tarihi": _tarih(v("DOĞUM TARİHİ")),
            "tip": tip,
            "protokol": _m(v("TEDAVİ PROTOKOLÜ")),
            "opu": opu,
            "transfer": transfer,
            "opu_hekim": _m(v("OPU KLİNİSYEN")) or None,
            "notlar": _m(v("NOTLAR")),
            "gizli_not": _m(v("NOTLAR CONFIDENTIAL")),
            # --- oosit sayıları ---
            "toplanan": _sayi(v("TOPLANAN OOSİT"), 0),
            "mii": _sayi(v("MATÜR (MII)"), 0),
            "immatur": _sayi(v("İMMATÜR (MI+GV)"), 0),
            "empty_zona": _sayi(v("EMPTY ZONA"), 0),
            "dejenere": _sayi(v("DEJENERE"), 0),
            "atretik": _sayi(v("ATRETİK"), 0),
            # --- ICSI / fertilizasyon ---
            "islenen": _sayi(v("İŞLEME ALINAN OOSİT SAYISI"), 0),
            "iki_pn": _sayi(v("NORMAL FERTİLİZASYON (2PN)"), 0),
            # INTAKT = döllenmemiş, bütün kalmış oosit = 0PN (docstring'de
            # aritmetiğiyle yazılı: işlenen = 2pn + anormal + dejenere + intakt)
            "intakt": _sayi(v("INTAKT"), 0),
            "anormal_fert": _sayi(v("ANORMAL FERTİLİZASYON"), 0),
            "islem_dejenere": _sayi(v("İŞLEM SONRASI DEJENERE"), 0),
            "fert_yontemi": _m(v("FERTİLİZASYON YÖNTEMİ")),
            # --- transfer / dondurma / çözme ---
            "transfer_adet": _sayi(v("TRANSFER EDİLEN EMBRİYO SAYISI"), 0),
            "transfer_asama": _m(v("EMBRİYO TRANSFER AŞAMASI")),
            "dondurulan": _sayi(v("DONDURULAN EMBRİYO SAYISI"), 0),
            "dondurma_asama": _m(v("EMBRİYO DONDURMA AŞAMASI")),
            "cozulen": _sayi(v("ÇÖZDÜRÜLEN EMBRİYO SAYISI"), 0),
            "viabilite": viabilite,
            "viabilite_ham": viabilite_ham,
            # Tarihi kaynakta olmayan satır (v6.148): `_tarihleri_tamamla()`
            # bir önceki kaydın tarihini yazıyor, OPU/transfer alanı boş kalıyor.
            "tarih_yaklasik": False,
            # Yazım hatası düzeltilen tarihler: [(alan, Access'teki, yeni)]
            "duzeltme": [],
            "emb1": (_m(v("EMBRİYO1 HÜCRE/AŞAMA")), _m(v("EMBRİYO1 KALİTE"))),
            "emb2": (_m(v("EMBRİYO2 HÜCRE/AŞAMA")), _m(v("EMBRİYO2 KALİTE"))),
            # --- androloji ---
            "sperm_kaynak": _m(v("SPERM KAYNAĞI")),
            "hazirlama": _m(v("HAZIRLAMA YÖNTEMİ")),
            "bazal": {
                "hacim_ml": _ondalik(v("BAZAL VOLÜM (ML)")),
                "konsantrasyon_milyon_ml": _ondalik(v("BAZAL KONSANTRASYON (x106/ML)")),
                "total_motil_yuzde": _ondalik(v("BAZAL MOTİLİTE (%)")),
                "pr_yuzde": _ondalik(v("BAZAL PROGRESSİF (%)")),
                "morfoloji_normal_yuzde": _ondalik(v("MORFOLOJİ (% NORMAL)")),
                "lokosit_milyon_ml": _ondalik(v("LÖKOSİT (x106/ML)")),
            },
            "hazirlik": {
                "hacim_ml": _ondalik(v("HAZIRLAMA SONRASI VOLÜM (ML)")),
                "konsantrasyon_milyon_ml": _ondalik(
                    v("HAZIRLAMA SONRASI KONSANTRASYON (x106/ML)")),
                "total_motil_yuzde": _ondalik(v("HAZIRLAMA SONRASI MOTİLİTE (%)")),
                "pr_yuzde": _ondalik(v("HAZIRLAMA SONRASI PROGRESSİF (%)")),
            },
            # --- işlemi yapan ---
            "yapan": {
                "opu": _m(v("OPU EMBRİYOLOG")) or None,
                "androloji": _m(v("HAZIRLAYAN EMBRİYOLOG")) or None,
                "icsi": _m(v("EMBRİYOLOG")) or None,
                "transfer": _m(v("TRANSFER EMBRİYOLOG")) or None,
            },
        })
    return cikti


def _gg(iso: str) -> str:
    """'2026-01-02' -> '02.01.2026' (nota yazılan tarih, CLAUDE.md'nin
    gün.ay.yıl kuralı)."""
    y, a, g = iso[:10].split("-")
    return f"{g}.{a}.{y}"


# Tarih düzeltme dosyası (`duzelt=`): kaynak kayıttaki yazım hatalı tarihler.
# Ocak dosyasında bir OPU "02.06.2026" yazıyor ama aynı hastanın o tedavisi
# ocakta; kullanıcı önerilen düzeltmeleri onayladı (v6.148). Düzeltme DOSYADA,
# betikte değil: kayıt numaraları hasta verisine bağlı, depoya girmez.
#
#     # kaynak#kayıt  alan      Access'te    düzeltilmiş
#     OCAK#8          OPU       2026-06-02   2026-01-02
#
# Satır yalnızca Access'teki değer hâlâ yazılan değerse uygulanıyor -- CSV
# sonradan düzeltilmişse ya da yanlış dosya verildiyse hiçbir şey değişmez,
# `liste` bunu söyler.
_DUZELTILEBILIR = {"OPU": "opu", "TRANSFER": "transfer"}


def duzeltmeleri_oku(yol: str) -> list:
    satirlar = []
    with open(yol, encoding="utf-8-sig") as f:
        for no, satir in enumerate(f, start=1):
            satir = satir.split("#", 1)[0] if satir.lstrip().startswith("#") else satir
            parca = satir.split()
            if not parca:
                continue
            if len(parca) != 4 or "#" not in parca[0] \
                    or parca[1].upper() not in _DUZELTILEBILIR \
                    or not all(_tarih(p) == p for p in parca[2:]):
                sys.exit(f"{yol}:{no}: anlaşılmadı -- beklenen: "
                         "KAYNAK#KAYIT  OPU|TRANSFER  eski-tarih  yeni-tarih")
            kaynak, kimlik = parca[0].split("#", 1)
            satirlar.append((_kaynak_ayikla(kaynak) if kaynak else "", kimlik,
                             parca[1].upper(), parca[2], parca[3]))
    return satirlar


def duzeltmeleri_uygula(satirlar, duzeltmeler, kaynak) -> list:
    """Bu dosyanın (`kaynak`) düzeltmelerini uygular. Döner: uygulanamayanlar."""
    kimlige = {r["kimlik"]: r for r in satirlar}
    tutmayan = []
    for k, kimlik, alan, eski, yeni in duzeltmeler:
        if k != kaynak:
            continue
        r = kimlige.get(kimlik)
        anahtar = _DUZELTILEBILIR[alan]
        if not r or r[anahtar] != eski:
            tutmayan.append(f"{k}#{kimlik} {alan} {eski}")
            continue
        r[anahtar] = yeni
        r["tarih"] = r["opu"] or r["transfer"]
        r["duzeltme"].append((alan, eski, yeni))
    return tutmayan


def tarihleri_tamamla(satirlar) -> None:
    """Tarihi olmayan satıra Access'teki bir önceki kaydın tarihini yazar.

    Kullanıcının kararı (v6.148): "Yakın kaydın tarihine yaz". Access kayıt
    numarası girişin sırası; tarihsiz bir kaydın işi büyük olasılıkla
    kendinden önce girilen kaydın günlerinde yapıldı. **OPU ve transfer
    alanlarına yazılmıyor** -- tedavinin sırası ve olayların günü için
    `tarih` kullanılıyor, not "yaklaşık" diyor. İlk kayıt tarihsizse
    ardından gelenin tarihi alınıyor.
    """
    sirali = sorted(satirlar, key=lambda r: int(r["kimlik"] or 0))
    for i, r in enumerate(sirali):
        if r["tarih"]:
            continue
        onceki = next((o["tarih"] for o in reversed(sirali[:i]) if o["tarih"]
                       and not o["tarih_yaklasik"]), None)
        sonraki = next((o["tarih"] for o in sirali[i + 1:] if o["tarih"]), None)
        if onceki or sonraki:
            r["tarih"] = onceki or sonraki
            r["tarih_yaklasik"] = True


def bos_kopyalari_ayikla(satirlar) -> list:
    """Access'te aynı tedavinin boş kopyası -- atlanır. Döner: atlananlar.

    Bir şubat satırı öbürünün birebir boş kopyası: aynı dosya no, aynı OPU
    günü, hiçbir sayı ve not yok. Aktarılsaydı hastanın kartında içi boş
    ikinci bir tedavi açılırdı. Boşluk ölçüsü dar: kopyanın hiçbir sayısı,
    notu ve transferi olmamalı, aynı gün aynı hastanın DOLU bir satırı
    olmalı.
    """
    sayilar = ("toplanan", "mii", "immatur", "empty_zona", "dejenere",
               "atretik", "islenen", "iki_pn", "intakt", "anormal_fert",
               "islem_dejenere", "transfer_adet", "dondurulan", "cozulen")

    def bos(r):
        return (not any(r[k] for k in sayilar) and not r["notlar"]
                and not r["transfer"])
    atlanan = []
    for r in satirlar:
        if bos(r) and r["tarih"] and any(
                o is not r and o["dosya_no"] == r["dosya_no"]
                and o["tarih"] == r["tarih"] and not bos(o) for o in satirlar):
            atlanan.append(r)
    for r in atlanan:
        satirlar.remove(r)
    return atlanan


def _islem_gunu(r) -> str:
    """Olayların günü: OPU, yoksa transfer, yoksa (tarihsiz satırda) yaklaşık
    tarih. Yumurta Çözme'nin çözme günü ayrı: `_cozme_gunu()`."""
    return r["opu"] or r["transfer"] or r["tarih"]


def _cozme_gunu(r) -> str:
    """FET ve Yumurta Çözme'de çözmenin günü.

    FET'te kaynak kayıt çözmenin gününü yazmıyor; v6.130'dan beri çözme
    transfer günü sayılıyor (aynı gün çözülüp transfer ediliyor). Yumurta
    Çözme'de ise yumurta ICSI günü çözülüyor ve embriyo günler sonra
    transfer ediliyor: çözme = transfer günü − transfer aşaması ("3,GÜN"
    -> üç gün önce). Tarihsiz satırda yaklaşık tarih.
    """
    if _db.cozulen_yumurta_islenir(r["tip"]) and r["transfer"]:
        return _gun_ekle(r["transfer"], -(_asama_gunu(r["transfer_asama"]) or 3))
    return r["transfer"] or r["tarih"]


# ------------------------------------------------------------------- yazma

ISARET = "[Access kaydı {}#{}]"     # aynı satır iki kez girmesin diye

# Kaynak dosyanın etiketi (`kaynak=TEMMUZ`). Boşken işaret v6.130'daki
# haliyle basılıyor -- ağustos aktarımı bu yüzden bozulmuyor.
#
# Neden gerekli: her Access dosyası KENDİ kayıtlarını 1'den numaralandırıyor.
# Ağustos dosyasının #1..#20'si programda dururken temmuz dosyası
# aktarılsaydı onun ilk 20 satırı "zaten aktarılmış" sanılıp SESSİZCE
# atlanırdı. Etiket numarayı dosyasına bağlıyor: `[Access kaydı TEMMUZ#5]`
# ile `[Access kaydı #5]` birbirini bulmuyor (kapanış `]` sayesinde
# `#1]` deseni `#10]`'u da yakalamıyor).
KAYNAK = ""


def _isaret(kimlik) -> str:
    return ISARET.format(KAYNAK, kimlik)


def _kaynak_ayikla(deger: str) -> str:
    """`kaynak=` değerini işarete yazılabilir hale getirir.

    Yalnızca harf/rakam: işaret SQL'de `LIKE` deseni olarak kullanılıyor ve
    `_` ile `%` orada joker. Türkçe harfler de düşüyor -- işaret protokol
    notunda, yani resmî formun NOTLAR kutusunda görünüyor.
    """
    # `tr_buyuk()` DEĞİL `_sade()`: ilki 'i'yi 'İ' yapıyor ve ASCII süzgeci
    # onu düşürüyor ("nisan" -> "NSAN"). `_sade()` Türkçe harfleri ASCII
    # karşılığına katlıyor ("ağustos" -> "AGUSTOS").
    ad = "".join(k for k in _sade(deger) if k.isascii() and k.isalnum())
    if not ad:
        sys.exit(f"Gecersiz kaynak adi: {deger!r} (yalnizca harf ve rakam)")
    return ad


def _kullanici_id() -> int:
    """Kayıtları "kimin girdiği". `olay.kullanici_id` NOT NULL.

    Aktarımı yapan yönetici seçiliyor. Bu "kim yaptı" değil "kim girdi" --
    işlemi yapan embriyolog ayrı, `islem_yapan.yapan_ad`'a yazılıyor
    (CLAUDE.md'nin ayrımı).
    """
    for kosul in ("AND rol='yonetici'", ""):
        r = _db.tek(f"SELECT id FROM kullanici WHERE lab_id=? AND aktif_mi=1 "
                    f"{kosul} ORDER BY id LIMIT 1", (_db.LAB_ID,))
        if r:
            return r["id"]
    sys.exit("Aktif kullanici yok -- once bir kullanici ac (kullanici.py).")


def _lab_no(b, yil: str) -> str:
    """Bir sonraki tedavi numarası. `app.sonraki_lab_no()`'nun kopyası.

    Tek fark: yıl öneki **tedavinin kendi yılından** geliyor (aktarım
    gelecek yıl çalıştırılsa bile ağustos 2026 kaydı 2026-xxxx olsun diye).
    Aynı işlem içinde okuyup yazıyor -- tuzak #7.
    """
    onek = yil if _db.ayar("lab_no_yillik_sifirla", "1") == "1" \
        else _db.ayar("lab_no_onek", yil)
    basamak = int(_db.ayar("lab_no_basamak", "4") or 4)
    bosluk_doldur = _db.ayar("lab_no_bosluk_doldur", "1") == "1"
    kalip = re.compile(rf"^{re.escape(onek)}-(\d+)$")
    kullanilan = set()
    for (no,) in b.execute("SELECT cycle_no FROM cycle WHERE lab_id=?",
                           (_db.LAB_ID,)).fetchall():
        m = kalip.match(no or "")
        if m:
            kullanilan.add(int(m.group(1)))
    if bosluk_doldur:
        sira = 1
        while sira in kullanilan:
            sira += 1
    else:
        sira = (max(kullanilan) + 1) if kullanilan else 1
    return f"{onek}-{sira:0{basamak}d}"


def _gun_ekle(iso: str, gun: int) -> str:
    return (_dt.date.fromisoformat(iso) + _dt.timedelta(days=gun)).isoformat()


def _asama_gunu(metin: str):
    """"5,GÜN" / "3.GÜN" -> 5 / 3. Tanınmazsa None."""
    m = re.match(r"\s*(\d+)", _m(metin))
    return int(m.group(1)) if m else None


# İptal sebebi kaynak kaydın NOTLAR metninden okunuyor. **Serbest metinden
# klinik karar çıkarmak riskli**, o yüzden iki kademeli: metin önce açıkça
# "iptal edildi" / "uygulanmadı" demeli; ancak ondan sonra hangi ayrıntılı
# sebep olduğuna bakılıyor, tanınmazsa genel "iptal" kalıyor (CLAUDE.md:
# genel İptal listede olmayan sebepler için duruyor). `liste` kipi hangi
# satıra hangi sebebin yazılacağını tek tek basıyor -- aktarmadan önce oku.
_IPTAL_SOZU = ("IPTAL", "UYGULANMADI")
_IPTAL_AYRINTI = (
    ("fert_olmadi", ("FERTILIZASYON OLMADI",)),
    # "D2 EMBRİYO ARRESTİ", "KLİVAJ ARRESTİ", "D3 ARRESTİ" (v6.148: ocak-haziran
    # notları günü "D2"/"D3" diye, cleavage'ı "KLİVAJ" diye yazmış).
    ("cleavage_arrest", ("2. GUN EMBRIYO ARRE", "3. GUN EMBRIYO ARRE",
                         "2.GUN EMBRIYO ARRE", "3.GUN EMBRIYO ARRE",
                         "D2 EMBRIYO ARRE", "D3 EMBRIYO ARRE",
                         "D2 ARRE", "D3 ARRE", "KLIVAJ ARRE",
                         "KLIVAJ ASAMASINDA EMBRIYO ARRE")),
    ("gun5_arrest", ("5. GUN EMBRIYO ARRE", "5.GUN EMBRIYO ARRE",
                     "D5 EMBRIYO ARRE", "D5 ARRE", "BLASTOKIST ARRE")),
    # v6.149 (mayıs): "OPUDA OOSİT ÇIKMADI", "İNMATÜR OOSİT SEBEBİYLE" --
    # programdaki sebeplerin (v6.103) adıyla birebir aynı söz, yorum değil.
    # Arrest/fertilizasyon kalıplarından SONRA: iki sebep birden yazıyorsa
    # işlemin daha ileri aşamadaki sonu kazanır.
    ("yumurta_cikmadi", ("OOSIT CIKMA", "YUMURTA CIKMA",
                         "OOSIT ELDE EDILEME", "YUMURTA ELDE EDILEME")),
    ("immatur_yumurta", ("IMMATUR OOSIT SEBEB", "INMATUR OOSIT SEBEB",
                         "IMMATUR YUMURTA SEBEB", "INMATUR YUMURTA SEBEB",
                         "IMMATUR OLDUG", "INMATUR OLDUG")),
)


# Dondurma cümlesinin fiili. Sayı alanı boş olan yumurta dondurmada
# tedavinin nasıl bittiğini yalnızca not söylüyor.
#
# v6.148'de genişledi: kaynak kayıt aynı işi çok farklı yazmış --
# "DONDURULARAK SAKLANDI", "DONDURULDU", "DONDURULMUŞTUR", "DONDURULARAK
# KORUNMUŞTUR", "DONDURULARAK SAKLANMIŞTIR", FET'te "REFREEZE EDİLDİ" /
# "REFREEZ EDİLDİ" / "REFREEZE EDİLEREK SAKLANDI", yazım hatalarıyla
# "DONDURULRAK", "DONDURULARK", "DONDURULAK". v6.147'ye kadar yalnızca ilk
# ikisi tanınıyordu: ocak-haziranda altmışa yakın dondurma (yedi tüplük bir
# dondurma dahil) hiç yazılmayacaktı, temmuzda bir yeniden dondurma
# yazılmamıştı.
#
# "DONDURULMUŞ EMBRİYOSU KALDI" (önceki tedaviden artan) ve "DONDURULMUŞ
# ŞEKİLDE SAKLANDI" (sperm tüpü) bilerek eşleşmiyor: fiil "dondurulmak"
# değil, "dondurulmuş halde durmak".
#
# Üç yazılış biçimi var, dondurulanın NEREDE yazdığı biçime göre değişiyor:
# - bitmiş fiil ("(1CC) ŞEKLİNDE REFREEZE EDİLDİ"): skorlar fiilden ÖNCE;
# - sıfat ("REFREEZ EDİLEN (4CC) İLE BİRLİKTE ... KALDI", "REFREEZE (KAVG1)
#   KALDI"): skorlar fiilden SONRA (`sonra` grubu);
# - örtük ("KÜLTÜRE EDİLEN 2 ADET D5 EMBRİYOSU (3CB) (2CC) İLE BİRLİKTE
#   TOPLAMDA 3 TÜPTE 6 ADET EMBRİYOSU KALDI"): fiil hiç yok ama embriyolar
#   "kalanlar arasında" sayılıyor, yani dondurulmuşlar (`ortuk` grubu).
#   Temmuzdaki bir FET o (3CB)'yi transfer ediyor -- gerçekten tanktaydı.
# "REFREEZE YAPILAMADI" (arrest yüzünden dondurulamadı) bir dondurma değil.
# Parantez içindeki "(REFREEZE)" da fiil değil, etiket (v6.149, mayıs: "(1CB)
# ŞEKLİNDE (REFREEZE) DONDURULARAK SAKLANDI") -- fiil sayılsaydı skor fiilin
# ARKASINDA aranıyor, (1CB) kaçıyor ve "(REFREEZE)" tüp sanılıyordu.
# FET'te bunların çoğu stok cümlesi; ayırt eden `_dondurma_coz()`'ün
# "fazla" kuralı (çözülen − transfer edilen).
_DONDURMA_FIILI = re.compile(
    r"DONDUR\w*\s+(?:SAKLAN|KORUN)\w*|DONDURULDU\b|DONDURULMUSTUR\b"
    r"|REFREEZ\w*\s+EDIL(?!EN\b)\w*"
    r"|(?P<sonra>REFREEZ\w*\s+EDILEN\b"
    r"|(?<!\()REFREEZE?\b(?!\s*\))(?!\s+(?:EDIL|YAPILA?MA|YAPILMA)))"
    r"|(?P<ortuk>KULTURE?\s+EDILEN\b)(?=[^.]*\bILE\s+BIR\w*[^.]*\bKALDI)")



def _iptal_sebebi(notlar: str):
    n = _sade(notlar)
    if not any(s in n for s in _IPTAL_SOZU):
        return None
    for kod, kaliplar in _IPTAL_AYRINTI:
        if any(k in n for k in kaliplar):
            return kod
    return "iptal"


_ENDIKASYON = (("AOR", "azalmis_over_rezervi"),
               ("AZALMIS OVER", "azalmis_over_rezervi"),
               ("ERKEK FAKTOR", "erkek_faktoru"))


def _gizli_notu_coz(metin: str) -> tuple:
    """NOTLAR CONFIDENTIAL -> (telefon, endikasyon kodu, kalan metin).

    O kolon telefon numarası ve parantez içinde endikasyon taşıyor. İkisi
    de programda kendi alanına gidiyor; **protokol notuna yazılmıyor**,
    çünkü protokol notu resmî formun NOTLAR kutusuna basılıyor (v6.102) --
    hasta telefonu orada işi yok.
    """
    ham = _m(metin)
    if not ham:
        return None, None, ""
    tel = None
    m = re.search(r"[\d][\d ]{8,}", ham)
    if m and len(re.sub(r"\D", "", m.group(0))) >= 10:
        tel = re.sub(r"\s+", " ", m.group(0)).strip()
        ham = ham.replace(m.group(0), " ")
    sade = _sade(ham)
    endikasyon = next((kod for anahtar, kod in _ENDIKASYON if anahtar in sade), None)
    # Tanınan endikasyon `cycle.endikasyon`a gidiyor; aynı kelimeyi bir de
    # hasta notuna yazmak gereksiz tekrar olurdu ("Not: AOR"). Silme
    # **katlanmış kopyanın üstünden** yürüyor ("ERKEK FAKTÖR" ham metinde
    # Türkçe harfli, kalıplar ASCII) ama karakter karakter hizalı kalsın
    # diye boşluk sıkıştırılmıyor -- `_sade()` sıkıştırdığı için burada
    # kullanılamaz.
    hizali = ham.upper().translate(_KATLA)
    for anahtar, _kod in _ENDIKASYON:
        yer = hizali.find(anahtar)
        while yer >= 0:
            bosluk = " " * len(anahtar)
            ham = ham[:yer] + bosluk + ham[yer + len(anahtar):]
            hizali = hizali[:yer] + bosluk + hizali[yer + len(anahtar):]
            yer = hizali.find(anahtar)
    kalan = re.sub(r"[\s()+]+", " ", ham).strip()
    return tel, endikasyon, kalan


# --------------------------------------------- dondurma notunun çözümlenmesi
#
# Kaynak kayıt dondurulan örneğin **skorunu yalnızca serbest NOTLAR metninde**
# tutuyor ("1 ADET D5 EMBRİYO (4BB HATCHED) ... DONDURULARAK SAKLANDI").
# Kullanıcının isteği (2026-09-22): "4BB blastokist dondurulmuş yazıyor ise
# blastokist bölümüne fotoğrafsız 4BB embriyo kaydet".
#
# Bu, serbest metinden **klinik veri** çıkarmak -- normalde kaçınılan şey. İki
# gerekçeyle yapılıyor: (1) yazım programın kendi skor biçiminin birebir aynısı
# (`app.blast_skor()` de "4BB", "KAV2" üretiyor), yani eşleme yorum değil
# çeviri; (2) tanınmayan her parça **olduğu gibi olayın notuna** yazılıyor ve
# `liste` kipi yazmadan önce hepsini tek tek basıyor.
#
# Tanınan yazımlar (hepsi gerçek kayıtlardan):
#   3AA, 4BB HATCHED      -> blastokist: genişleme + ICM + TE
#   KAVG2, MORG1          -> kavitasyon/morula + derece 2   (M/EM/ARR aynı desen)
#   4HG2, 3HG2, 8G2       -> cleavage: hücre sayısı + G skoru
#   2*M2, 5M2, 1*M1       -> dondurulan YUMURTA grubu (adet + olgunluk, v6.148:
#                            yıldızsız yazım ve MI yumurta da)
#   BB, BİRLEŞME G1       -> skoru bilinmeyen embriyo (v6.148): D3 listelerinde
#                            bir embriyonun yerini tutuyor, sayılıyor ama
#                            değerlendirmesi yazılmıyor, ham hali notta
_OOSIT_GRUBU = re.compile(r"^(\d+)\s*\*?\s*M\s*(2|II|1|I)$")
_TEK_OOSIT = re.compile(r"^M\s*(2|II|1|I)$")        # "(M2)" -- yalnız yumurta notunda
_CLEAVAGE = re.compile(r"^(\d+)\s*(?:H\s*G?|G)\s*([1-4])")
_BLAST = re.compile(r"^([1-6])\s*([ABC])\s*([ABC])")
_BLAST_DISI = re.compile(r"^(KAV|EM|ARR|MOR|M)\s*G?\s*([1-3])?(?![A-Z0-9])")
_YUVA = re.compile(r"^(?:BB|BIRLESME\w*)$")
# `app.BLAST_KISA`'nın tersi -- oradaki kısaltmalar kâğıda da böyle yazılıyor.
_KISALTMA = {"KAV": "kavitasyon", "M": "morula", "MOR": "morula",
             "EM": "erken_morula", "ARR": "arrest"}


def _skor_coz(parca: str, yumurta: bool = False):
    """Tek bir skor yazısını programın alanlarına çevirir. Tanımazsa None.

    `yumurta`: not bir yumurta dondurmasını anlatıyor. Orada "M2" MII yumurta,
    embriyo notunda "M2" morula derece 2 -- aynı yazı iki anlama geliyor,
    bağlam karar veriyor (v6.148).
    """
    t = _sade(parca).replace("KAVITASYON", "KAV").replace("MORULA", "MOR")
    if not t:
        return None
    m = _OOSIT_GRUBU.match(t) or (_TEK_OOSIT.match(t) if yumurta else None)
    if m:
        adet = int(m.group(1)) if m.re is _OOSIT_GRUBU else 1
        olgunluk = m.group(m.re.groups)
        return {"tur": "oosit", "adet": adet,
                "mat": "mii" if olgunluk in ("2", "II") else "mi",
                "ham": parca.strip()}
    m = _CLEAVAGE.match(t)
    if m:
        return {"tur": "cleavage", "hucre": int(m.group(1)),
                "skor": "G" + m.group(2), "ham": parca.strip()}
    m = _BLAST.match(t)
    if m:
        return {"tur": "blast", "genisleme": m.group(1),
                "icm": m.group(2).lower(), "te": m.group(3).lower(),
                "skor": m.group(1) + m.group(2) + m.group(3), "ham": parca.strip()}
    m = _BLAST_DISI.match(t)
    if m:
        kod = _KISALTMA[m.group(1)]
        derece = m.group(2)
        kisa = "M" if m.group(1) == "MOR" else m.group(1)
        return {"tur": "blast", "genisleme": kod, "derece": derece,
                "skor": kisa + (derece or ""), "ham": parca.strip()}
    return None


def _yuva_coz(parca: str):
    """Skoru bilinmeyen ama bir embriyonun yerini tutan yazım ("BB")."""
    if _YUVA.match(_sade(parca)):
        return {"tur": "embriyo", "ham": parca.strip()}
    return None


def _grup_coz(grup: str, yumurta: bool) -> list:
    """Bir parantez grubunun öğeleri. "-" öğeleri ayırıyor; bazı notlarda
    boşluk ayırıyor ("(3M2 1M1)", "(BB 10HG3 8HG3 8HG2)") -- o zaman boşlukla
    ayrılan her parça tek tek tanınmalı, yoksa parça tek öğe sayılıyor ("4BB
    HATCHED" bir blastokist). Parçanın içinde "(" kalmışsa (kaynaktaki
    "((4CB-1BB)" ya da "D3 (EMBRİYOSU (8HG1-10HG2)" gibi yazım hataları)
    sonuncusundan sonrası alınıyor."""
    ogeler = []
    for parca in grup.split("-"):
        parca = parca.split("(")[-1].strip()
        if not parca:
            continue
        coz = _skor_coz(parca, yumurta)
        if not coz:
            alt = parca.split()
            if len(alt) > 1:
                alt_coz = [_skor_coz(a, yumurta) or _yuva_coz(a) for a in alt]
                if all(alt_coz):
                    ogeler.extend(alt_coz)
                    continue
            coz = _yuva_coz(parca)
        ogeler.append(coz or {"tur": "taninmadi", "ham": parca})
    return ogeler


def _gun_bul(metin: str):
    """"D5", "D 3", "5.GÜN", "3. GÜN", "5,GÜN" -> 5 / 3. Metin `_KATLA`'lı."""
    m = (re.search(r"\bD\s*([1-7])\b", metin)
         or re.search(r"\b([1-7])\s*[.,]?\s*GUN", metin))
    return int(m.group(1)) if m else None


def _dondurma_coz(notlar: str, asama: str = "", tip: str = "",
                  dondurulan=None, fazla=None) -> dict:
    """Dondurma cümlesini çözümler. Dondurma yoksa boş sözlük.

    Yalnızca dondurma fiilinin geçtiği **cümleye** bakıyor (v6.148; önce
    notun başından fiile kadar her şeye bakılıyordu):
    - bir kayıtta fiilden sonra ilgisiz metin geliyor ("SPERM MORFOLOJİSİ
      KÖTÜ, ... MOTİLİTE %0") -- oradaki sayılar skor sanılmamalı;
    - önceki cümle transferi anlatıyorsa ("1ADET (2BC) ŞEKLİNDE TRANSFER
      EDİLDİ. ... (1CC) ŞEKLİNDE REFREEZE EDİLDİ") transfer edilen embriyo
      dondurulmuş sayılmamalı. Aynı cümlede önce transfer geçiyorsa ("(3AB)
      ŞEKLİNDE TAZE TRANSFER SONRASI KALAN 1ADET (1BB) ... DONDURULARAK
      SAKLANDI") son "TRANSFER"den sonrası alınıyor.
    Rakamdan sonra gelen nokta cümle sonu değil ("3. GÜN", "17.01.25").
    Skorların fiilden önce mi sonra mı yazdığı fiilin biçimine bağlı
    (`_DONDURMA_FIILI`'nin açıklaması).

    **FET'te notların çoğu stok cümlesi, dondurma değil** (v6.148): "GERİDE
    8 ADET D5 EMBRİYOSU (...) DONDURULARAK SAKLANMIŞTIR", "REFREEZ EDİLEN
    1 ADET D5 (1BB) EMBRİYOSU KALDI" depoda kalanları anlatıyor. Karar
    yapılandırılmış alanlardan (v6.142'nin dersi): `fazla` = çözülen −
    transfer edilen. Fazla yoksa bu tedavide dondurulacak embriyo da yoktu;
    cümle "GERİDE" diyor ve DONDURULAN sayısı 0 ise yine stok.
    """
    ham = notlar or ""
    hizali = ham.upper().translate(_KATLA)
    if len(hizali) != len(ham):       # upper() nadiren uzunluk değiştirir
        ham = hizali
    m = _DONDURMA_FIILI.search(hizali)
    if not m:
        return {}
    bas = 0
    for b in re.finditer(r"(?<!\d)\.\s*(?=\S)", hizali[:m.start()]):
        bas = b.end()
    son = re.search(r"(?<!\d)\.(?!\d)", hizali[m.end():])
    son = m.end() + son.start() if son else len(hizali)
    tum = re.sub(r"\s+", " ", hizali[bas:son])        # fiilin bütün cümlesi

    fet = tip in FET_TIPLERI and not _db.cozulen_yumurta_islenir(tip)
    if fet:
        if fazla is not None and fazla <= 0:
            return {}
        if ("GERIDE" in tum or "GERIYE" in tum) and not dondurulan:
            return {}

    if m.group("sonra") or m.group("ortuk"):
        # Nesne fiilden sonra: "İLE BİRLİKTE" / "KALDI" / cümle sonuna kadar
        dur = re.search(r"\bILE\s+BIR|\bKALDI", hizali[m.end():son])
        a, z = m.end(), (m.end() + dur.start() if dur else son)
    else:
        a = bas
        t = hizali.rfind("TRANSFER", bas, m.start())
        if t >= 0:
            a = t + len("TRANSFER")
        z = m.start()
    cumle = re.sub(r"\s+", " ", hizali[a:z])
    ham_cumle, cumle_hizali = ham[a:z], hizali[a:z]

    gun = _asama_gunu(asama)
    if gun is None:
        gun = _gun_bul(cumle) or _gun_bul(tum)

    def _ilk(kalip):
        mm = re.search(kalip, cumle)
        return int(mm.group(1)) if mm else None

    # Yumurta mı embriyo mu -- üç işaretten biri yeter (v6.142). Önceden
    # yalnızca nottaki kelimeye bakılıyordu; bir temmuz notu kelimeyi
    # atlamış: "2 TÜPTE 10 ADET (5*M2) (5*M2)". Araç onu embriyo sandı,
    # yumurta dondurma tedavisinde 2PN'li örnek aradı, bulamadı ve
    # 10 yumurtayı HİÇ yazmadı -- Cryo Haritası o iki tüpü göstermedi.
    # (1) Tedavinin tipi: programın kendi kuralı `db.yumurta_mi()`.
    #     Yapılandırılmış veri serbest metinden önce gelir.
    # (2) Nottaki kelime: `ivf_icsi`'de yumurta dondurulmuşsa tek işaret.
    # (3) Her öğe yumurta yazımı ("N*M2"): MII/MI bir olgunluk derecesi,
    #     embriyo için hiç yazılmaz.
    baglam = (_db.yumurta_mi(tip) or "OOSIT" in cumle or "YUMURTA" in cumle)

    # **Bir parantez grubu = bir tüp.** Kaynak kayıt tüp sayısını bazen ayrıca
    # yazıyor ("2 TÜPTE"), bazen yazmıyor; ama yazdığı her satırda grup sayısı
    # o sayıyla birebir tutuyor (doğrulandı, 7 notun 3'ünde açık sayı var):
    #   "6 ADET OOSİT 2 TÜPTE (3*M2) (3*M2)"        -> 2 grup, 2 tüp
    #   "1TÜPTE 3 ADET D3 EMBRİYOSU (4HG2-4HG2-3HG2)" -> 1 grup, 1 tüp
    # Grup içinde "-" örnekleri ayırıyor, "N*M2" ise N yumurta demek.
    # "6 ADET (M2) OOSİT (3*M2) (3*M2)": "ADET"ten hemen sonraki yalın "(M2)"
    # tüp değil, sayının niteliği -- tüp sayılsaydı 6 yumurta 3 tüpe (1+3+2)
    # dağılırdı. Tek grup oysa zaten tek örnek kuralına düşüyor, sonuç aynı.
    gruplar = []
    for gm in re.finditer(r"\(([^)]*)\)", ham_cumle):
        if re.fullmatch(r"REFREEZ\w*", _sade(gm.group(1))):
            continue                    # "(REFREEZE)" etiket, tüp değil
        if (baglam and _TEK_OOSIT.match(_sade(gm.group(1)))
                and cumle_hizali[:gm.start()].rstrip().endswith("ADET")):
            continue
        g = _grup_coz(gm.group(1), baglam)
        if g:
            gruplar.append(g)
    ogeler = [o for g in gruplar for o in g]      # düz liste
    adet = _ilk(r"(\d+)\s*ADET")
    if not gruplar and (adet == 1 or (adet is None and fazla == 1)):
        # Parantezsiz tek örnek (v6.148): "1 ADET M2 OOSİT DONDURULARAK
        # SAKLANDI" -- bir örnek ancak bir tüpte olabilir. FET'te sayı hiç
        # yazmıyorsa ("REFREEZ EDİLEN EMBRİYO İLE BİRLİKTE ... KALDI") tek
        # fazla embriyo o. Birden çok örnekte tüplere dağılım bilinmiyor,
        # orada uydurulmuyor (uyarı çıkıyor).
        if baglam:
            tek = {"tur": "oosit", "adet": 1,
                   "mat": "mi" if re.search(r"\bM\s*(1|I)\b", cumle) else "mii",
                   "ham": ham_cumle.strip()}
        else:
            tek = {"tur": "embriyo", "ham": ham_cumle.strip() or "skorsuz"}
        gruplar, ogeler = [[tek]], [tek]
    sayilan = [o for o in ogeler if o["tur"] != "taninmadi"]
    return {
        "gun": gun,
        "oosit_mi": baglam or (bool(sayilan)
                               and all(o["tur"] == "oosit" for o in sayilan)),
        "adet": adet,
        "tup": _ilk(r"(\d+)\s*TUPTE"),
        "gruplar": gruplar,
        "ogeler": ogeler,
        # Fiilsiz dondurma: `liste` ve rapor bunu ayrıca söylüyor
        "ortuk": bool(m.group("ortuk")),
    }


def _cozulen_sayisi(r) -> int:
    """FET'te çözülen embriyo sayısı. Kaynağın ÇÖZDÜRÜLEN alanı bazen eksik:
    bir satırda 1 çözüldü, 1 transfer, 3 yeniden dondurma yazıyor -- en az 4
    çözülmüş olmalı. Transfer + dondurma alttan sınır (v6.148)."""
    return max(r["cozulen"] or 0,
               (r["transfer_adet"] or 0) + (r["dondurulan"] or 0))


def _satir_dondurmasi(r) -> dict:
    """Satırın dondurması -- `_dondurma_coz()`'ün satırdan beslenen hali.
    FET'te "fazla" (çözülen − transfer edilen) oradaki stok kuralına gidiyor.
    Bütün çağıranlar bunu kullanmalı: kural tek yerde kalsın."""
    fazla = None
    if r["tip"] in FET_TIPLERI and not _db.cozulen_yumurta_islenir(r["tip"]):
        fazla = _cozulen_sayisi(r) - (r["transfer_adet"] or 0)
    return _dondurma_coz(r["notlar"], r["dondurma_asama"], r["tip"],
                         r["dondurulan"], fazla)


def _not_kur(r: dict) -> str:
    """Tedavinin protokol notu -- ekranda **ve resmî formda** görünen metin.

    **Kısa tutuluyor, bilerek.** Bu metin Embriyoloji Özet formunun NOTLAR
    kutusuna basılıyor (v6.102) ve o kutu `white-space: pre` -- uzun satır
    sarmıyor, kutunun dışında kesiliyor. İlk yazışta aktarımın bütün
    ayrıntıları (empty zona sayısı, taşıyıcı yok, MI/GV ayrımı...) buraya
    yazılmıştı ve formda kesik görünüyordu. O ayrıntılar zaten verinin
    kendisinde duruyor (maturasyon olayı olmayan oosit, taşıyıcısız
    vitrifikasyon kaydı); burada yalnızca kaynağın kendi metni, tek cümlelik
    uyarı ve işaret kalıyor. Satırlar 68 karakterde elle sarılıyor.

    Yeni bir satır eklersen formu açıp bak (tuzak #5). Bugünkü en uzun
    not sekiz satır (protokol + kaynağın notu + aktarım cümlesi + işaret +
    v6.104'ün iptal sebebi) ve kutu onu kesmeden basıyor -- ölçüldü,
    `scrollHeight == clientHeight`.
    """
    p = []
    if r["protokol"]:
        p.append(f'Tedavi protokolü (kaynak kayıt): {r["protokol"]}')
    if r["notlar"]:
        p.append(r["notlar"])
    p.append(_aktarim_cumlesi(r["tip"]))
    # Tarih notları (v6.148): kaynakta olmayan ya da yazım hatasıyla
    # düzeltilen tarih ekranda ve resmî formda "gerçek" gibi durmasın.
    if r["tarih_yaklasik"]:
        p.append(f'Tarih kaynak kayıtta yok, yaklaşık: Access\'teki bir önceki '
                 f'kaydın tarihi ({_gg(r["tarih"])}).')
    for alan, eski, yeni in r["duzeltme"]:
        p.append(f"{alan} tarihi Access'te {_gg(eski)} yazıyordu, "
                 f"{_gg(yeni)} olarak düzeltildi.")
    # İşaret KENDİ satırında: cümlenin sonuna eklenirse `textwrap` onu
    # ortasından bölüyor ("[Access kaydı\nTEMMUZ#9]") ve `_zaten_var()`in
    # `LIKE` deseni tutmuyor -- yani aktarım idempotent olmaktan çıkıyor,
    # ikinci çalıştırma aynı tedaviyi bir daha açıyor. Ağustosta işaret
    # kısa olduğu için (etiketsiz) rastgele sığıyordu; `kaynak=TEMMUZ`
    # altı karakter uzatınca 86 satırın 60'ında bölündü. Tek başına bir
    # satır olarak 68'in çok altında, hiçbir etiketle bölünemez.
    p.append(_isaret(r["kimlik"]))
    return "\n".join(textwrap.fill(satir, 68) for satir in p)


def _aktarim_cumlesi(tip: str, kaynak: str = None) -> str:
    """Protokol notunun "nereden geldi" cümlesi.

    FET'te çözülen embriyonun dondurulduğu tedavi programda yoksa bunu
    söylüyor (v6.130). `_kaynaga_bagla()` o tedaviyi programda bulursa
    (v6.148) cümle o tedavinin numarasıyla yeniden kuruluyor (`kaynak`:
    "2026-0012 tedavisinde") -- iki hâl de
    buradan, not sonradan metin içinde değiştirilebilsin diye (`textwrap`
    ile sarılmış paragrafı birebir yeniden üretmek gerekiyor, goc_044'ün
    dersi).
    """
    if tip in FET_TIPLERI:
        ne = "yumurta" if _db.cozulen_yumurta_islenir(tip) else "embriyo"
        cumle = ("Program öncesi Access kaydından aktarıldı; " +
                 (f"çözülen {ne}lar {kaynak} dondurulmuştu."
                  if kaynak else
                  f"çözülen {ne}ların dondurulduğu tedavi programda yok."))
        if _db.cozulen_yumurta_islenir(tip):
            cumle += (" ICSI ve sonrası toplam sayılardan üretildi, tek tek "
                      "gözlem değildir.")
        return cumle
    return ("Program öncesi Access kaydından aktarıldı; yumurta kayıtları "
            "toplam sayılardan üretildi, tek tek gözlem değildir.")


def _olay(b, kid, specimen_id, cycle_id, tip, zaman, **alanlar):
    alanlar = {k: v for k, v in alanlar.items() if v is not None}
    kolonlar = ["lab_id", "specimen_id", "cycle_id", "tip", "zaman",
                "kullanici_id", "olusturma_zamani"] + list(alanlar)
    degerler = [_db.LAB_ID, specimen_id, cycle_id, tip, zaman, kid,
                zaman] + list(alanlar.values())
    b.execute(f"INSERT INTO olay ({','.join(kolonlar)}) "
              f"VALUES ({','.join('?' * len(kolonlar))})", degerler)


def _durum_yaz(b, sid, durum):
    b.execute("UPDATE specimen SET durum=? WHERE id=?", (durum, sid))


def _hastayi_bul_veya_ac(b, r, rapor) -> int:
    """Dosya numarasına göre hasta. Varsa **üzerine yazmaz**, boşları doldurur."""
    tel, _endikasyon, kalan = _gizli_notu_coz(r["gizli_not"])
    h = b.execute("SELECT * FROM hasta WHERE lab_id=? AND dosya_no=?",
                  (_db.LAB_ID, r["dosya_no"])).fetchone()
    if h:
        bos = {}
        for kolon, deger in (("es_adi", r["es_adi"]),
                             ("dogum_tarihi", r["dogum_tarihi"]),
                             ("telefon", tel), ("notlar", kalan or None)):
            if deger and not h[kolon]:
                bos[kolon] = deger
        if bos:
            b.execute("UPDATE hasta SET " + ",".join(f"{k}=?" for k in bos) +
                      " WHERE id=?", list(bos.values()) + [h["id"]])
            rapor.append(f'    hasta {r["dosya_no"]}: boş alanlar dolduruldu '
                         f'({", ".join(bos)})')
        else:
            rapor.append(f'    hasta {r["dosya_no"]}: zaten kayıtlı')
        if r["ad_soyad"] and h["ad_soyad"] != r["ad_soyad"]:
            # Eşleşme yine dosya numarasıyla (CLAUDE.md: isimle eşleştirme
            # yok) -- ama ad farklıysa söylenmeli, yanlış hasta bu işin en
            # pahalı hatası. Ocak-ağustos dosyalarında 11 dosya numarası
            # farklı yazılmış adla geçiyor; hepsi aynı kişi (bir harf, yer
            # değiştiren ad, aynı doğum tarihi). Ad rapora YAZILMIYOR.
            rapor.append("    DİKKAT: Access'teki ad programdakinden farklı "
                         "yazılmış -- programdaki korundu, hastayı kontrol et")
        return h["id"]

    # `olusturma_zamani` tedavinin tarihine çekiliyor: kayıt bugün açılıyor
    # ama iş ağustosta yapıldı. Ay listeleri ve `/istatistik`'in ay süzgeci
    # bu alana düşüyor (FET'te opu_zamani yok), "Son kayıtlar" da öyle --
    # aktarılan eski kayıt "bu haftanın işi" gibi görünmemeli (v6.124).
    b.execute("INSERT INTO hasta (lab_id, dosya_no, ad_soyad, dogum_tarihi, "
              "es_adi, telefon, notlar, durum, olusturma_zamani) "
              "VALUES (?,?,?,?,?,?,?,'aktif',?)",
              (_db.LAB_ID, r["dosya_no"], r["ad_soyad"], r["dogum_tarihi"],
               r["es_adi"], tel, kalan or None, _zaman(r["tarih"], "08:00:00")))
    rapor.append(f'    hasta {r["dosya_no"]}: YENİ kart açıldı')
    return b.execute("SELECT last_insert_rowid()").fetchone()[0]


def _dondurma_zamani(r, coz) -> tuple:
    """(dondurma anı, değerlendirme anı), ISO metin -- tarih yoksa (None, None).

    Saatler program öncesi kayıtların bütün saatleri gibi yaklaşık (v6.130),
    gün ise kaynağın söylediği:
    - yumurta dondurma OPU günü, denüdasyondan sonra;
    - embriyo dondurma OPU + nottaki gün ("5,GÜN", "D3");
    - FET'te yeniden dondurma çözme (= transfer) günü, transferden sonra.
      Transfersiz kültürde (PGT satırları) çözülen gün 3 embriyosu notun
      gününe kadar kültürde kalıyor: çözme + (gün − 3);
    - Yumurta Çözme'de embriyo dondurma çözme + nottaki gün.
    Değerlendirme dondurmadan önce: çözmeden (09:00) SONRA olmalı, yoksa
    `db.olay_tedavisi()` onu kaynak tedaviye yazar.
    """
    tip, gun = r["tip"], coz.get("gun")
    if tip in FET_TIPLERI:
        cg = _cozme_gunu(r)
        if not cg:
            return None, None
        if _db.cozulen_yumurta_islenir(tip):
            g = _gun_ekle(cg, gun or 3)
            return _zaman(g, "12:00:00"), _zaman(g, "09:30:00")
        if not r["transfer"] and gun and gun > 3:
            cg = _gun_ekle(cg, gun - 3)
        return _zaman(cg, "14:00:00"), _zaman(cg, "13:00:00")
    opu = r["opu"] or r["tarih"]
    if not opu:
        return None, None
    if coz.get("oosit_mi"):
        return _zaman(opu, "14:00:00"), _zaman(opu, "11:30:00")
    g = _gun_ekle(opu, gun or 5)
    return _zaman(g, "12:00:00"), _zaman(g, "09:00:00")


def _cycle_ac(b, r, hasta_id, rapor) -> tuple:
    """Tedaviyi açar. (cycle_id, cycle_no) döner."""
    tarih = r["tarih"]
    yil = tarih[:4] if tarih else str(_dt.date.today().year)
    cycle_no = _lab_no(b, yil)
    sira = (b.execute("SELECT MAX(hasta_cycle_no) FROM cycle WHERE hasta_id=?",
                      (hasta_id,)).fetchone()[0] or 0) + 1
    _tel, endikasyon, _kalan = _gizli_notu_coz(r["gizli_not"])

    sebep = _iptal_sebebi(r["notlar"])
    coz = _satir_dondurmasi(r)
    if sebep:
        durum, bitis = "iptal", sebep
        bitis_zamani = r["transfer"] or _islem_gunu(r)
    elif (r["transfer"] or r["tarih_yaklasik"]) and r["transfer_adet"]:
        durum, bitis = "tamamlandi", "transfer"
        bitis_zamani = r["transfer"] or r["tarih"]
    elif r["dondurulan"] or coz:
        # Yumurta dondurmada sayı alanı boş (embriyo kolonu) ama not açıkça
        # "16 ADET OOSİT ... DONDURULARAK SAKLANDI" diyor -- iptal notunda
        # olduğu gibi, kaynak kaydın kendi cümlesine güveniliyor. FET'in stok
        # cümlesi ("GERİDE ... DONDURULARAK SAKLANMIŞTIR") burada sayılmıyor:
        # `_satir_dondurmasi()` onu dondurma saymıyor (v6.148).
        durum, bitis = "tamamlandi", "dondurma"
        an = _dondurma_zamani(r, coz or {"gun": _asama_gunu(r["dondurma_asama"]),
                                         "oosit_mi": False})[0]
        bitis_zamani = an[:10] if an else None
    else:
        # Kaynak kayıt ne transfer ne dondurma diyor, iptal de demiyor.
        # Uydurulmuyor: tedavi "tamamlandı" olarak kapanıyor (yapılacaklar
        # listesini ağustos işiyle doldurmasın diye) ama sebep boş kalıyor.
        # `cycle_detay.html` bu durumu zaten biliyor: sebep yoksa
        # "Tamamlandı" rozeti basıyor.
        durum, bitis = "tamamlandi", None
        bitis_zamani = r["transfer"] or _islem_gunu(r)

    opu_zamani = _zaman(r["opu"], "09:00:00") if r["tip"] not in FET_TIPLERI else None
    # "Toplanan" OPU'nun kendi sayısı (v6.112). FET tiplerinde yumurta
    # toplanmıyor: Yumurta Çözme satırının TOPLANAN OOSİT'i çözülen yumurta
    # sayısı, OPU sayısı değil -- v6.147'den beri ekran orada "Toplanan"
    # basmıyor, veriye de yazılmıyor (v6.148).
    toplanan = (r["toplanan"] or None) if r["tip"] not in FET_TIPLERI else None
    b.execute(
        "INSERT INTO cycle (lab_id, hasta_id, cycle_no, hasta_cycle_no, "
        " cycle_tipi, endikasyon, protokol_notu, opu_zamani, denudasyon_zamani, "
        " opu_hekim, opu_sag_oosit, durum, bitis_sebebi, bitis_zamani, "
        " olusturma_zamani) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (_db.LAB_ID, hasta_id, cycle_no, sira, r["tip"], endikasyon,
         _not_kur(r), opu_zamani, _zaman(r["opu"], "11:00:00"),
         r["opu_hekim"], toplanan, durum, bitis,
         _zaman(bitis_zamani, "16:00:00"), _zaman(tarih, "08:30:00")))
    cycle_id = b.execute("SELECT last_insert_rowid()").fetchone()[0]
    # `sira` yalnızca geçici: son numarayı satırın sonunda tarih sırası
    # veriyor (`_tedavi_sirasi()`), rapordaki numara oradan.
    rapor.append(f'    tedavi {cycle_no} ({r["tip"]}) — '
                 f'{durum}{" / " + bitis if bitis else ""}')
    return cycle_id, cycle_no


def _tedavi_sirasi(b, hasta_id, cycle_id, rapor):
    """Hastanın tedavilerini tarih sırasıyla numaralar (v6.144).

    Kullanıcının isteği: eski bir tedavi sonradan aktarılırsa araya
    yerleşsin, en eski tedavi 1. olsun. Kural programınki, tek yerde:
    `db.tedavileri_sirala()`. Satırın bütün kayıtları yazıldıktan sonra
    çağrılıyor -- FET'in günü çözme kaydından geliyor.
    """
    degisen = _db.tedavileri_sirala(b, hasta_id)
    no = b.execute("SELECT hasta_cycle_no FROM cycle WHERE id=?",
                   (cycle_id,)).fetchone()[0]
    kayan = [f"{c} {e}.→{y}." for cid, c, e, y in degisen if cid != cycle_id]
    rapor.append(f"    hastanın {no}. tedavisi"
                 + (f" — tarih sırasına göre kayanlar: {', '.join(kayan)}"
                    if kayan else ""))


def _specimen_ac(b, cycle_id, cycle_no, sira, durum, zaman) -> str:
    sid = f"{cycle_no}-{sira:02d}"
    b.execute("INSERT INTO specimen (id, lab_id, cycle_id, cycle_sira_no, "
              "durum, olusturma_zamani) VALUES (?,?,?,?,?,?)",
              (sid, _db.LAB_ID, cycle_id, sira, durum, zaman))
    return sid


def _oositleri_ac(b, r, cycle_id, cycle_no, kid, rapor):
    """Toplanan (ya da çözülen) yumurta kadar kayıt açar, sayılara uyan
    olayları yazar.

    Dağıtım sırası **tek yerde burada**: önce MII, sonra immatür, sonra
    empty zona / dejenere / atretik. ICSI listenin başından veriliyor
    (yani önce MII'lere), fertilizasyon da işlem görenlerin başından.
    Hangi oositin hangisi olduğu kaynak kayıtta yok -- docstring'de yazılı.

    **Yumurta Çözme** (v6.148): aynı dağıtım, ama yumurtalar OPU'da
    toplanmıyor, bu tedavi için çözülüyor. Her yumurtaya `thaw_cycle_id`'si
    bu tedavi olan bir çözme yazılıyor (programın Yumurta Çözme ekranları
    örnekleri oradan buluyor, `db.tedavi_ornekleri()`), olgunluk ICSI
    ekranının sorusu (v6.147). Kaynağın TOPLANAN OOSİT'i burada çözülen
    yumurta sayısı; bazı satırlarda yalnızca MII ya da İŞLEME ALINAN dolu,
    sayı en büyüğünden. Yumurtaların dondurulduğu tüp programdaysa
    `_kaynaga_bagla()` hepsini o tüpün örneklerine taşıyor.
    """
    cozme = _db.cozulen_yumurta_islenir(r["tip"])
    if cozme:
        n = max(r["toplanan"] or 0,
                r["mii"] + r["immatur"] + r["empty_zona"] + r["dejenere"]
                + r["atretik"], r["islenen"] or 0)
        gun = _cozme_gunu(r)
    else:
        n = r["toplanan"] or 0
        gun = r["opu"] or r["tarih"]
    if not n:
        if cozme:
            rapor.append("    çözülen yumurta sayısı kaynak kayıtta yok, "
                         "yumurta kaydı açılmadı")
        return
    if not gun:
        rapor.append("    UYARI: tarih yok, yumurta kaydı açılmadı")
        return
    t_thaw = _zaman(gun, "09:00:00")
    t_denud = _zaman(gun, "11:00:00")
    t_icsi = _zaman(gun, "13:00:00")
    t_fert = _zaman(_gun_ekle(gun, 1), "09:00:00")

    plan = (["mii"] * r["mii"] + ["mi"] * r["immatur"] +
            [None] * r["empty_zona"] + ["degenere"] * r["dejenere"] +
            ["atretik"] * r["atretik"])
    plan = (plan + [None] * n)[:n]        # sayılar tutmazsa kalanı boş geçer
    islenen = min(r["islenen"] or 0, n)

    oositler = []
    for i, mat in enumerate(plan, start=1):
        sid = _specimen_ac(b, cycle_id, cycle_no, i, "oosit",
                           t_thaw if cozme else t_denud)
        oositler.append([sid, mat, None])          # [id, maturasyon, durum]
        if cozme:
            # Çözmeden canlı çıktığı kaynakta yazmıyor; olgunluğu
            # değerlendirilen ya da ICSI'ye alınan yumurta canlıdır.
            canli = mat in ("mii", "mi") or i <= islenen
            _olay(b, kid, sid, cycle_id, "thaw", t_thaw, thaw_cycle_id=cycle_id,
                  thaw_sagkalim="canli" if canli else None)
        if mat:
            # oosit_cryo'da bu soru denüdasyon ekranında soruluyor, ivf_icsi'de
            # ICSI ekranında -- ikisi de aynı olay tipini yazıyor (v6.96).
            _olay(b, kid, sid, cycle_id, "maturasyon_kontrolu", t_denud,
                  mat_deger=mat)

    # --- ICSI: önce MII'ler, yetmezse immatürler (bir satırda işlem sayısı
    #     MII'den fazla: 12 MII / 13 işlem -- kaynak kayıt öyle diyor).
    enjekte = oositler[:islenen]
    # İşlem sonrası dejenere listenin SONUNDAKİLER. Kaynağın toplamı çoğu
    # satırda tutuyor (İŞLEME ALINAN = 2PN + ANORMAL + DEJENERE + INTAKT);
    # ocak-haziranda on iki satırda tutmuyor -- birinde 11 ICSI'nin 10'u
    # dejenere yazılmış ama 5'i 2PN ve ikisi dondurulmuş. Öyle satırda 2PN,
    # anormal ve intakt korunuyor, dejenere kalana kısılıyor: dondurulan ve
    # transfer edilen embriyo 2PN'lerden seçiliyor (v6.148). Tutan satırda
    # dağıtım v6.130'dakiyle birebir aynı.
    fert = (r["iki_pn"] or 0) + (r["intakt"] or 0) + (r["anormal_fert"] or 0)
    n_dej = max(0, min(r["islem_dejenere"] or 0, len(enjekte) - fert))
    if fert + (r["islem_dejenere"] or 0) != len(enjekte) and enjekte:
        rapor.append(f'    kaynakta sayılar tutmuyor: {len(enjekte)} ICSI, '
                     f'2PN+intakt+anormal {fert}, işlem sonrası dejenere '
                     f'{r["islem_dejenere"] or 0} -- dejenere {n_dej} yazıldı')
    dejenere_olan = enjekte[len(enjekte) - n_dej:] if n_dej else []
    for o in enjekte:
        bozuk = o in dejenere_olan
        _olay(b, kid, o[0], cycle_id, "icsi", t_icsi,
              icsi_sonuc="degenere" if bozuk else "basarili")
        o[2] = "degenere" if bozuk else "enjekte"

    # --- Fertilizasyon: dejenere olanlara bakılmıyor (değerlendirilmez)
    kalan = [o for o in enjekte if o not in dejenere_olan]
    sirada = 0
    for _ in range(min(r["iki_pn"] or 0, len(kalan))):
        o = kalan[sirada]; sirada += 1
        _olay(b, kid, o[0], cycle_id, "fertilizasyon_kontrolu", t_fert,
              fert_pn_sayisi="2", fert_sonuc="normal")
        o[2] = "zigot"
    for _ in range(min(r["intakt"] or 0, len(kalan) - sirada)):
        o = kalan[sirada]; sirada += 1
        _olay(b, kid, o[0], cycle_id, "fertilizasyon_kontrolu", t_fert,
              fert_pn_sayisi="0")
        o[2] = "0pn"
    for _ in range(min(r["anormal_fert"] or 0, len(kalan) - sirada)):
        o = kalan[sirada]; sirada += 1
        # PN sayısı kaynak kayıtta yok (1PN mi 3PN mi belli değil) -- boş
        # bırakılıyor, sebebi olayın notuna yazılıyor.
        _olay(b, kid, o[0], cycle_id, "fertilizasyon_kontrolu", t_fert,
              notlar="Anormal fertilizasyon; PN sayısı kaynak kayıtta yok.")
        o[2] = "kontrol_edildi"

    # Dondurulan embriyoların değerlendirmesi `_dondurma_kayitlari()`'nda --
    # skorlar serbest NOTLAR metninden geliyor ve o iş aktarımdan sonra da
    # tek başına çalıştırılabilmeli ("tamamla" kipi).

    for sid, _mat, durum in oositler:
        if durum:
            _durum_yaz(b, sid, durum)
        elif _mat and _mat != "mii":
            _durum_yaz(b, sid, "degenere" if _mat == "degenere" else "immatur")
        elif cozme:
            _durum_yaz(b, sid, "cozuldu")
    rapor.append(f'    {n} yumurta{" çözüldü" if cozme else ""}, {r["mii"]} MII, '
                 f'{islenen} ICSI, {r["iki_pn"]} 2PN'
                 + (" (tarih yaklaşık)" if r["tarih_yaklasik"] else ""))


# Nottan yazılan değerlendirmenin notu bu önekle başlıyor; aktarımın kendi
# yazdığını (onarımda iptal edilebilecek olanı) elle girilenden ayırt eden bu.
_KAYNAK_YAZIMI = "Kaynak kayıttaki yazım"
_DEGERLENDIRMELER = ("cleavage_degerlendirme", "blastokist_degerlendirme")


def _kendi_tedavisi(b, sid) -> int:
    """Örneğin KENDİ tedavisi -- `olay.cycle_id` her zaman bu (CLAUDE.md)."""
    return b.execute("SELECT cycle_id FROM specimen WHERE id=?", (sid,)).fetchone()[0]


def _iptal(b, kid, olay_id, sebep):
    b.execute("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, iptal_zamani=?, "
              "iptal_sebep=? WHERE id=?",
              (kid, _dt.datetime.now().isoformat(" ", "seconds"), sebep, olay_id))


def _degerlendirme_yaz(b, kid, sid, tedavi, tip, gun, zaman, alanlar, ham,
                       onek=_KAYNAK_YAZIMI):
    """Aşama değerlendirmesini yazar; varsa **üzerine yazar**, ikinci kayıt açmaz.

    "tamamla" kipi aktarılmış bir tedaviyi ikinci kez işleyebilsin diye
    idempotent: aynı örneğe aynı tipte, **bu tedavide** yapılmış
    (`db.bu_tedavide()`) iptal edilmemiş bir olay varsa o güncelleniyor.
    Tedavi sınırı v6.148'de geldi: FET'e bağlanan bir embriyonun kaynak
    tedavideki skoru FET'teki yeniden dondurmanın skoruyla ezilmesin.
    `olay.cycle_id` örneğin kendi tedavisi, `tedavi` işlemin yapıldığı.
    """
    notu = f"{onek}: {ham}"
    var = b.execute("SELECT o.id FROM olay o WHERE o.specimen_id=? AND o.tip=? "
                    f"AND o.iptal_mi=0 AND {_db.bu_tedavide(tedavi, 'o')} "
                    "ORDER BY o.id LIMIT 1", (sid, tip)).fetchone()
    if var:
        atama = ", ".join(f"{k}=?" for k in alanlar)
        b.execute(f"UPDATE olay SET {atama}, gun=?, notlar=? WHERE id=?",
                  list(alanlar.values()) + [gun, notu, var[0]])
    else:
        _olay(b, kid, sid, _kendi_tedavisi(b, sid), tip, zaman, gun=gun,
              notlar=notu, **alanlar)


def _oge_alanlari(o, gun=None) -> tuple:
    """Nottan çözümlenen öğe -> (olay tipi, alanlar), değerlendirmesi yoksa None.

    Skorsuz öğe ("BB") gün 2/3 listesinde o embriyonun o günkü
    değerlendirmesinin yazımı: skor alanları boş bir cleavage değerlendirmesi
    yazılıyor, yazım notunda (v6.148). Skor uydurulmuyor; ama embriyo
    değerlendirilmiş ve dondurulmuş, "Cleavage sayısı" onu saymalı. Blastokist
    gününde ya da günü bilinmeyen skorsuz öğede değerlendirme yok.
    """
    if o["tur"] == "embriyo":
        if gun is not None and gun <= 3:
            return "cleavage_degerlendirme", {
                "cl_hucre_sayisi": None, "cl_skor": None, "cl_skor_kaynagi": None}
        return None
    if o["tur"] == "blast":
        return "blastokist_degerlendirme", {
            "bl_genisleme": o["genisleme"], "bl_icm": o.get("icm"),
            "bl_te": o.get("te"), "bl_derece": o.get("derece"),
            "bl_skor": o["skor"], "bl_skor_kaynagi": "elle"}
    if o["tur"] == "cleavage":
        return "cleavage_degerlendirme", {
            "cl_hucre_sayisi": o["hucre"], "cl_skor": o["skor"],
            "cl_skor_kaynagi": "elle"}
    return None


def _oge_anahtari(o):
    """Karşılaştırma anahtarı: blastokistte skor ("4AA", "KAV3", "M1"),
    cleavage'da hücre + skor ("8G2"). Skorsuz öğede None."""
    if o["tur"] == "blast":
        return o["skor"]
    if o["tur"] == "cleavage":
        return f'{o["hucre"]}{o["skor"]}'
    return None


# Gelişim sırası: çözülüp kültüre alınan embriyo ancak İLERİ gider (gün 3
# embriyosu gün 5'te blastokist olarak transfer edilebilir, tersi olmaz).
# `_kaynaga_bagla()` kaynağın skorunu transferinkiyle bu sıraya göre
# karşılaştırıyor.
_EVRE_SIRASI = {"morula": 2, "erken_morula": 2, "kavitasyon": 3}


def _oge_sirasi(o):
    """Öğenin gelişim sırası: cleavage 1, morula 2, kavitasyon 3, blastokist 4;
    skorsuz öğede None."""
    if o["tur"] == "cleavage":
        return 1
    if o["tur"] == "blast":
        return _EVRE_SIRASI.get(o["genisleme"], 4)
    return None


def _degerlendirme_anahtari(b, sid, tedavi):
    """Örneğin bu tedavideki değerlendirmesinin anahtarı (`_oge_anahtari()`
    ile aynı biçim) ve gelişim sırası (`_oge_sirasi()`): ('4AA', 4),
    ('8G2', 1) ya da (None, None)."""
    o = b.execute(
        "SELECT o.tip, o.bl_skor, o.cl_hucre_sayisi, o.cl_skor, o.bl_genisleme "
        "FROM olay o WHERE o.specimen_id=? AND o.iptal_mi=0 AND o.tip IN (?, ?) "
        f"AND {_db.bu_tedavide(tedavi, 'o')} "
        "ORDER BY o.zaman DESC, o.id DESC LIMIT 1",
        (sid,) + _DEGERLENDIRMELER).fetchone()
    if not o:
        return None, None
    if o[0] == "blastokist_degerlendirme":
        return o[1], _EVRE_SIRASI.get(o[4], 4)
    if o[2] is None and not o[3]:
        return None, None       # skorsuz ("BB"): bilinmiyor, her şeyle tutar
    return (f"{o[2]}{o[3]}" if o[2] is not None and o[3] else None), 1


def _olgunluk(b, sid, tedavi):
    """Yumurtanın bu tedavideki olgunluğu, dondurma havuzunun anahtarıyla:
    MII 'mii', MI/GV 'mi', öteki (dejenere, atretik, girilmemiş) None."""
    o = b.execute("SELECT o.mat_deger FROM olay o WHERE o.specimen_id=? "
                  "AND o.tip='maturasyon_kontrolu' AND o.iptal_mi=0 "
                  f"AND {_db.bu_tedavide(tedavi, 'o')} "
                  "ORDER BY o.id DESC LIMIT 1", (sid,)).fetchone()
    mat = o[0] if o else None
    return "mii" if mat == "mii" else ("mi" if mat in ("mi", "gv") else None)


def _aktarim_skorunu_iptal(b, kid, sid, tedavi, sebep):
    """Nottan yazılmış (`_KAYNAK_YAZIMI`) değerlendirmeleri iptal eder --
    yalnızca bu tedavidekileri ve yalnızca aktarımın kendi yazdıklarını;
    elle girilmiş bir skora dokunmaz."""
    for (oid,) in b.execute(
            "SELECT o.id FROM olay o WHERE o.specimen_id=? AND o.iptal_mi=0 "
            f"AND o.tip IN (?, ?) AND o.notlar LIKE ? AND {_db.bu_tedavide(tedavi, 'o')}",
            (sid,) + _DEGERLENDIRMELER + (_KAYNAK_YAZIMI + ": %",)).fetchall():
        _iptal(b, kid, oid, sebep)


def _dondurma_havuzu(b, r, cycle_id, oosit_mi) -> dict:
    """Bu tedavide dondurulabilecek örnekler, örnek sırasıyla.

    Yumurtada iki havuz, olgunluğa göre ('mii', 'mi'); embriyoda tek (None).
    - yumurta: tedavinin kendi yumurtaları, ICSI'ye alınmamış;
    - embriyo (IVF/ICSI): kendi 2PN'leri;
    - Yumurta Çözme: bu tedavi için çözülüp bu tedavide 2PN çıkanlar;
    - FET: bu tedavi için çözülüp dejenere çıkmayanlar (v6.143).
    Transfer edilmiş örnek hiçbirinde yok. Havuz yalnızca YENİ atama için:
    bir tüpte zaten duran örnek eşleştirmede kendi kaydından tanınıyor
    (`_dondurma_kayitlari()`), havuzda olması gerekmiyor.
    """
    bu = _db.bu_tedavide(cycle_id, "o")
    transfersiz = ("NOT EXISTS (SELECT 1 FROM olay tr WHERE tr.specimen_id=s.id "
                   "AND tr.tip='transfer' AND tr.iptal_mi=0)")
    if oosit_mi:
        havuz = {"mii": [], "mi": []}
        for sid, mat in b.execute(
                "SELECT s.id, o.mat_deger FROM specimen s JOIN olay o ON o.specimen_id=s.id "
                f"WHERE s.cycle_id=? AND o.tip='maturasyon_kontrolu' AND o.iptal_mi=0 AND {bu} "
                f"AND {transfersiz} AND NOT EXISTS (SELECT 1 FROM olay i "
                "WHERE i.specimen_id=s.id AND i.tip='icsi' AND i.iptal_mi=0) "
                "GROUP BY s.id ORDER BY s.cycle_sira_no", (cycle_id,)).fetchall():
            anahtar = "mii" if mat == "mii" else ("mi" if mat in ("mi", "gv") else None)
            if anahtar:
                havuz[anahtar].append(sid)
        return havuz
    if r["tip"] in FET_TIPLERI and not _db.cozulen_yumurta_islenir(r["tip"]):
        sorgu = ("SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
                 "WHERE o.tip='thaw' AND o.iptal_mi=0 AND o.thaw_cycle_id=? "
                 "AND COALESCE(o.thaw_sagkalim, '') <> 'degenere' "
                 f"AND {transfersiz} GROUP BY s.id ORDER BY s.cycle_id, s.cycle_sira_no")
    else:
        adaylar = (_db.tedavi_ornekleri(r["tip"], "s"))
        sorgu = ("SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
                 f"WHERE {adaylar} AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
                 f"AND o.fert_pn_sayisi='2' AND {bu} AND {transfersiz} "
                 "GROUP BY s.id ORDER BY s.cycle_id, s.cycle_sira_no")
        return {None: [sid for (sid,) in b.execute(sorgu, (cycle_id,)).fetchall()],
                "yedek": _yedek_embriyolar(b, r, cycle_id)}
    return {None: [sid for (sid,) in b.execute(sorgu, (cycle_id,)).fetchall()]}


def _yedek_embriyolar(b, r, cycle_id) -> list:
    """2PN'i yazılmamış, enjekte edilmiş ve dejenere olmamış yumurtalar.

    Dört satırda kaynağın 2PN sayısı 0 ama not "1 ADET D3 EMBRİYOSU (5HG3)
    ... DONDURULARAK SAKLANDI" diyor; birinde embriyoları sonraki bir FET
    çözüyor -- tüpler gerçekten tankta. Embriyo enjekte edilmiş bir
    yumurtadan geldi, döllenme kaydı kaynakta eksik. 2PN'ler bitince dondurma
    ve transfer bu yumurtalara yazılıyor ve rapor bunu söylüyor: tankta duran
    tüpün programda görünmemesi (v6.142'nin dersi) döllenme sayısının boş
    kalmasından pahalı. 0PN (intakt) ve anormal yazılmış yumurta alınmıyor.
    """
    adaylar = _db.tedavi_ornekleri(r["tip"], "s")
    bu = _db.bu_tedavide(cycle_id, "o")
    return [sid for (sid,) in b.execute(
        "SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
        f"WHERE {adaylar} AND o.tip='icsi' AND o.iptal_mi=0 AND {bu} "
        "AND COALESCE(o.icsi_sonuc, '') <> 'degenere' "
        "AND NOT EXISTS (SELECT 1 FROM olay f WHERE f.specimen_id=s.id "
        "  AND f.tip='fertilizasyon_kontrolu' AND f.iptal_mi=0) "
        "AND NOT EXISTS (SELECT 1 FROM olay v WHERE v.specimen_id=s.id "
        "  AND v.tip IN ('vitrifikasyon', 'transfer') AND v.iptal_mi=0) "
        "GROUP BY s.id ORDER BY s.cycle_id, s.cycle_sira_no", (cycle_id,)).fetchall()]


def _mevcut_tupler(b, cycle_id) -> list:
    """Bu tedavide yapılmış dondurmaların tüpleri, açılış sırasıyla:
    [(taşıyıcı, etiket, vitrifikasyon anı, [(örnek, olay), ...]), ...]."""
    tupler = {}
    for tid, etiket, an, sid, oid in b.execute(
            "SELECT o.vit_tasiyici_id, t.etiket, t.vitrifikasyon_zamani, "
            "o.specimen_id, o.id FROM olay o JOIN tasiyici t ON t.id=o.vit_tasiyici_id "
            "WHERE o.tip='vitrifikasyon' AND o.iptal_mi=0 "
            f"AND {_db.vit_tedavisi('o')} = ? ORDER BY o.vit_tasiyici_id, o.id",
            (cycle_id,)).fetchall():
        tupler.setdefault(tid, [etiket, an, []])[2].append((sid, oid))
    return [(tid, e, an, u) for tid, (e, an, u) in sorted(tupler.items())]


def _yerler(grup, oosit_mi) -> list:
    """Bir tüpün (parantez grubunun) örnek yerleri: [(anahtar, öğe), ...].
    Yumurtada "3*M2" üç yer, anahtar olgunluk; embriyoda her öğe bir yer,
    anahtar skoru (skorsuz "BB" yerinde None)."""
    yerler = []
    for o in grup:
        if oosit_mi:
            if o["tur"] == "oosit":
                yerler += [(o["mat"], o)] * o["adet"]
        elif o["tur"] in ("blast", "cleavage", "embriyo"):
            yerler.append((_oge_anahtari(o), o))
    return yerler


def _onceki_durum(b, sid, tedavi) -> str:
    """Tüpten çıkarılan örneğin dondurmadan önceki durumu (onarım için)."""
    if b.execute("SELECT 1 FROM olay WHERE specimen_id=? AND tip='thaw' "
                 "AND iptal_mi=0 AND thaw_cycle_id=?", (sid, tedavi)).fetchone():
        return "cozuldu"
    if b.execute("SELECT 1 FROM olay WHERE specimen_id=? AND iptal_mi=0 "
                 "AND tip='fertilizasyon_kontrolu' AND fert_pn_sayisi='2'",
                 (sid,)).fetchone():
        return "zigot"
    return "oosit"


def _tasiyici_ac(b, kid, cycle_no, zaman):
    """Taşıyıcıyı vitrifikasyon ekranının kendi kalıbıyla açar.

    Etiket **uydurulmuyor**: `vit_ekran()` zaten `onerilen =
    f"{cycle_no}-{HHMM}"` diye bir kod öneriyor ve personel ekranda çoğu
    zaman onu kabul ediyor -- yani etiket tüpten okunan bir ad değil,
    programın ürettiği bir kod. Aktarım da aynı kalıbı kullanıyor
    (kullanıcının isteği: "Vitrifikasyon bölümünde etiket kodu üretiyor,
    onu kullansan").

    Saat, o tüpün vitrifikasyon saati. Aynı tedavide birden çok tüp varsa
    dakika ilerliyor (`UNIQUE(lab_id, etiket)`) -- tüpler zaten arka arkaya
    hazırlanıyor, kod da öyle okunuyor.

    Konum (tank/kanister/goblet/pozisyon) **boş kalıyor**: kaynak kayıtta
    yok ve ekranın kendisi de boş bırakılmasına izin veriyor ("taşıyıcı
    sistemde görünür ama nerede olduğu bilinmez"). Kullanıcı Cryo
    Haritası'ndan konumu sonradan girer.
    """
    t = _dt.datetime.fromisoformat(zaman)
    for _ in range(600):
        etiket = f"{cycle_no}-{t:%H%M}"
        if not b.execute("SELECT id FROM tasiyici WHERE lab_id=? AND etiket=?",
                         (_db.LAB_ID, etiket)).fetchone():
            break
        t += _dt.timedelta(minutes=1)
    else:
        raise RuntimeError(f"{cycle_no} icin bos etiket bulunamadi")
    an = t.isoformat(" ", "seconds")
    b.execute("INSERT INTO tasiyici (lab_id, tip, etiket, konum_id, "
              "vitrifikasyon_zamani, kullanici_id, durum, kategori) "
              "VALUES (?,'cryotop',?,NULL,?,?,'dolu','embriyo')",
              (_db.LAB_ID, etiket, an, kid))
    return b.execute("SELECT last_insert_rowid()").fetchone()[0], etiket, an


def _dondurma_kayitlari(b, r, cycle_id, kid, rapor):
    """Nottan çözümlenen dondurmayı ilgili aşama ekranlarına yazar.

    Kullanıcının isteği (2026-09-22): "4BB blastokist dondurulmuş yazıyor ise
    blastokist bölümüne fotoğrafsız 4BB embriyo kaydedip vitrifikasyonda da
    bunun dondurulduğunu ilgili bölüme yaz."

    Üç şey yazılıyor:
    1. **Değerlendirme** — blastokist yazımı `blastokist_degerlendirme`
       (`bl_genisleme`/`bl_icm`/`bl_te` ya da kavitasyon + derece), cleavage
       yazımı `cleavage_degerlendirme` (`cl_hucre_sayisi`/`cl_skor`). Skorsuz
       yer ("BB") değerlendirmesiz dondurulmuş embriyo.
    2. **Taşıyıcı** — her parantez grubu bir tüp (`_dondurma_coz()`'e bak),
       etiketi `vit_ekran()`'in önerdiği kalıpta.
    3. **Vitrifikasyon olayı** — taşıyıcıya bağlı, yani vitrifikasyon
       ekranının "Dondurulmuş" listesinde ve Cryo Haritası'nda görünüyor.
       FET'te ve Yumurta Çözme'de `vit_cycle_id` bu tedavi: örnek başka bir
       tedaviden geliyor, dondurma bu tedavide yapıldı (v6.143, goc_046).

    **İdempotent, ve var olan tüpü ONARIR** (v6.148). Tüpler zaten varsa
    (önceki bir aktarım ya da "tamamla") notun grupları sırayla o tüplerle
    eşleşiyor: tüpte duran örnek kendi kaydından tanınıyor (skoru, yumurtada
    olgunluğu), notta olup tüpte olmayan yer havuzdan tamamlanıyor, notta
    olmayan örnek tüpten çıkıyor. v6.147'ye kadarki araç "BB" yazımını ve
    MI yumurtayı tanımıyordu -- temmuzun üç tüpünde birer embriyo, üç
    tüpünde birer MI yumurta eksik yazıldı; "tamamla" onları böyle ekliyor.
    **Tüp silinmiyor, etiketi ve konumu değişmiyor**: kullanıcı Cryo
    Haritası'ndan konum girmiş olabilir. Not tüp sayısından azsa fazla tüp
    olduğu gibi kalıyor ve rapor söylüyor.
    """
    coz = _satir_dondurmasi(r)
    if not coz:
        return
    if not coz["gruplar"]:
        # Dondurma cümlesi var ama kaç örnek/tüp olduğu yazmıyor (parantez
        # grubu yok) -- neyin yazılacağı bilinemez. #33'ün dersi (v6.142):
        # dondurulmuş bir örnek tankta durup programda görünmüyorsa bu
        # SÖYLENMELİ.
        rapor.append("    UYARI: notta dondurma var ama kaç örnek/tüp olduğu "
                     "okunamadı -- dondurma kaydı yazılmadı")
        return
    tip = r["tip"]
    baska_tedaviden = tip in FET_TIPLERI       # örnek bu tedavi için çözüldü
    oosit_mi = coz["oosit_mi"]
    t_vit, t_deg = _dondurma_zamani(r, coz)
    if not t_vit:
        rapor.append("    UYARI: tarih yok, dondurma kaydı yazılamadı")
        return
    cycle_no = b.execute("SELECT cycle_no FROM cycle WHERE id=?",
                         (cycle_id,)).fetchone()[0]

    if not baska_tedaviden:
        # v6.131'in ilk yazışındaki taşıyıcısız vitrifikasyon olayları iptal
        # ediliyor: istatistikte "donduruldu" derken ekranda "aday"
        # görünüyorlardı. FET'te öyle kayıt hiç yazılmadı.
        for (oid,) in b.execute(
                "SELECT o.id FROM olay o JOIN specimen s ON s.id=o.specimen_id "
                "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
                "AND o.vit_tasiyici_id IS NULL", (cycle_id,)).fetchall():
            _iptal(b, kid, oid, "Tasiyicili kayitla degistirildi")

    gun = coz["gun"] or 5
    havuz = _dondurma_havuzu(b, r, cycle_id, oosit_mi)
    mevcut = _mevcut_tupler(b, cycle_id)
    kullanilan = {sid for *_x, uyeler in mevcut for sid, _o in uyeler}
    ek_vit = {"vit_cycle_id": cycle_id} if baska_tedaviden else {}
    if tip in FET_TIPLERI and not _db.cozulen_yumurta_islenir(tip):
        vit_notu = ("Kaynak kayıttaki dondurma notundan aktarıldı (çözme sonrası "
                    "yeniden dondurma); konum girilmedi.")
    else:
        vit_notu = "Kaynak kayıttaki dondurma notundan aktarıldı; konum girilmedi."

    yeni_tup, onarilan, yazilan, eksik, yer_sayisi, yedekten = [], [], [], 0, 0, 0
    for i, grup in enumerate(coz["gruplar"]):
        yerler = _yerler(grup, oosit_mi)
        if not yerler:
            continue
        yer_sayisi += len(yerler)
        tid, etiket, an, uyeler = mevcut[i] if i < len(mevcut) else (None, None, None, [])
        tupteki = [sid for sid, _o in uyeler]
        if oosit_mi:
            anahtar = {sid: _olgunluk(b, sid, cycle_id) for sid in tupteki}
        else:
            anahtar = {sid: _degerlendirme_anahtari(b, sid, cycle_id)[0]
                       for sid in tupteki}
        atanan = [None] * len(yerler)
        bosta = list(tupteki)
        # 1) tüpteki örnek kendi skoruyla (yumurtada olgunluğuyla) yerine
        for j, (a, _o) in enumerate(yerler):
            if a is None:
                continue
            sid = next((s for s in bosta if anahtar[s] == a), None)
            if sid:
                atanan[j] = sid
                bosta.remove(sid)
        if not oosit_mi:
            # 2) skorsuz yer ("BB") <- değerlendirmesiz örnek
            for j, (a, _o) in enumerate(yerler):
                if atanan[j] is None and a is None:
                    sid = next((s for s in bosta if anahtar[s] is None), None)
                    if sid:
                        atanan[j] = sid
                        bosta.remove(sid)
            # 3) kalan yer <- tüpte kalan embriyo (skoru nottakiyle yazılacak).
            #    Yumurtada yapılmıyor: MI'nın yerine MII konmaz.
            for j in range(len(yerler)):
                if atanan[j] is None and bosta:
                    atanan[j] = bosta.pop(0)
        # 4) kalan yer <- havuzdan, hiçbir tüpte olmayan yeni örnek; 2PN'ler
        #    bitmişse 2PN'i yazılmamış enjekte yumurta (`_yedek_embriyolar()`)
        for j, (a, _o) in enumerate(yerler):
            if atanan[j]:
                continue
            sid = next((s for s in havuz.get(a if oosit_mi else None, [])
                        if s not in kullanilan), None)
            if sid is None and not oosit_mi:
                sid = next((s for s in havuz.get("yedek", [])
                            if s not in kullanilan), None)
                yedekten += bool(sid)
            if sid is None:
                eksik += 1
                continue
            atanan[j] = sid
            kullanilan.add(sid)

        eklenen = [s for s in atanan if s and s not in tupteki]
        if tid is None:
            if not eklenen:
                continue
            an = (_dt.datetime.fromisoformat(t_vit)
                  + _dt.timedelta(minutes=i)).isoformat(" ", "seconds")
            tid, etiket, an = _tasiyici_ac(b, kid, cycle_no, an)
            yeni_tup.append(f"{etiket} ({len(eklenen)})")
        elif eklenen or bosta:
            onarilan.append(f"{etiket}: " + ", ".join(
                x for x in (f"+{len(eklenen)}" if eklenen else "",
                            f"-{len(bosta)}" if bosta else "") if x))
        for sid in eklenen:
            _olay(b, kid, sid, _kendi_tedavisi(b, sid), "vitrifikasyon", an,
                  vit_tasiyici_id=tid, notlar=vit_notu, **ek_vit)
            _durum_yaz(b, sid, "dondurulmus")
        for sid in bosta:
            # Notta yok: tüpten çıkıyor. Nottan yazılmış skoru da onunla gidiyor.
            _iptal(b, kid, dict(uyeler)[sid],
                   "Kaynak kayittaki dondurma notunda yok (aktarim onarimi)")
            if not oosit_mi:
                _aktarim_skorunu_iptal(b, kid, sid, cycle_id,
                                       "Kaynak kayittaki dondurma notunda yok")
            _durum_yaz(b, sid, _onceki_durum(b, sid, cycle_id))

        if oosit_mi:
            continue
        for (a, o), sid in zip(yerler, atanan):
            if not sid:
                continue
            yazilan.append(o["ham"])
            alan = _oge_alanlari(o, coz["gun"])
            if alan:
                deg_tipi, alanlar = alan
                _degerlendirme_yaz(b, kid, sid, cycle_id, deg_tipi,
                                   max(gun, 4) if o["tur"] == "blast" else min(gun, 3),
                                   t_deg, alanlar, o["ham"])
            else:
                # Skorsuz ve değerlendirmesiz yer: bu örneğe daha önce başka
                # bir yazım atanmışsa o skor gidiyor.
                _aktarim_skorunu_iptal(b, kid, sid, cycle_id,
                                       "Skorsuz embriyo (kaynak kayitta skor yok)")

    if yedekten:
        rapor.append(f"    UYARI: kaynakta 2PN sayısı dondurulandan az -- {yedekten} "
                     "embriyo 2PN kaydı olmayan enjekte yumurtaya yazıldı")
    if eksik:
        rapor.append(f"    UYARI: notta {yer_sayisi} örnek yazıyor ama "
                     f"{yer_sayisi - eksik} uygun kayıt var; fazlası yazılmadı")
    if len(mevcut) > len(coz["gruplar"]):
        rapor.append(f"    UYARI: programda notta olmayan "
                     f"{len(mevcut) - len(coz['gruplar'])} tüp var, dokunulmadı")
    if yazilan:
        rapor.append(f'    skorlar: {", ".join(yazilan)} (gün {gun})')
    if coz.get("ortuk"):
        rapor.append("    not dondurmayı fiilsiz söylüyor (\"... İLE BİRLİKTE "
                     "KALDI\") -- yeniden dondurma sayıldı")
    if yeni_tup:
        rapor.append(f'    dondurma: {len(yeni_tup)} tüp — {", ".join(yeni_tup)} '
                     f'(konum boş, Cryo Haritası\'ndan gir)')
    if onarilan:
        rapor.append(f'    dondurma onarıldı: {"; ".join(onarilan)}')
    if mevcut and not yeni_tup and not onarilan:
        rapor.append("    dondurma zaten girilmiş, tüpler notla tutuyor")


def _kalite_coz(hucre: str, kalite: str):
    """Kaynağın "EMBRİYO1 HÜCRE/AŞAMA" + "KALİTE" kutuları -> öğe (skor sözlüğü).

    Yazım satırdan satıra değişiyor: ("4", "AA") blastokist 4AA, ("8H", "G3")
    ve ("8", "2") gün 3 embriyosu 8 hücre G3/G2, ("KAVİTASYON", "3") KAV3,
    ("MORULA", "1") morula 1, ("", "4BB"), ("2", "BB(%80)"), ("BB", "")
    skorsuz embriyo. Tanınmazsa None (transfer notunda ham hali duruyor).
    """
    h, k = _m(hucre), _m(kalite)
    if not (h or k):
        return None
    birlesik = re.sub(r"\(.*?\)", "", f"{h}{k}").strip()
    coz = _skor_coz(birlesik)
    if coz:
        return coz
    if h.isdigit() and re.fullmatch(r"G?\s*[1-4]", _sade(k)):
        return _skor_coz(f"{h}HG{_sade(k)[-1]}")
    return _yuva_coz(birlesik) or _yuva_coz(h) or _yuva_coz(k)


def _kalite_yazimi(hucre: str, kalite: str) -> str:
    """Transfer notunda ve raporda gösterilen yazım: kaynağın iki kutusu
    birleşince "81" gibi okunmaz bir şey çıkıyordu ("8" hücre + "1" skor);
    tanınan yazım kullanıcının kendi notlarındaki biçimle ("8HG1", "3AA",
    "KAV3"), tanınmayan olduğu gibi."""
    o = _kalite_coz(hucre, kalite)
    if o and o["tur"] == "cleavage":
        return f'{o["hucre"]}HG{o["skor"][-1]}'
    if o and o["tur"] == "blast":
        return o["skor"]
    return f"{_m(hucre)}{_m(kalite)}"


def _transfer_kaliteleri(r) -> list:
    """Transfer edilen embriyoların öğeleri, transfer sırasıyla (tanınmayan
    ya da boş kutu None). Yalnızca TRANSFER EDİLEN sayısı kadar: bir satırda
    ikinci kutuya embriyo değil bir kişinin adı yazılmış."""
    return [_kalite_coz(h, k) for h, k in (r["emb1"], r["emb2"])][:r["transfer_adet"] or 0]


def _taze_transfer(b, r, cycle_id, kid, rapor):
    """IVF/ICSI ve Yumurta Çözme'de bu tedavide yapılan transfer (v6.148).

    v6.147'ye kadar araç yalnızca FET transferini yazıyordu; IVF/ICSI'de
    embriyo aynı tedavide transfer edildiğinde hiçbir şey yazılmıyordu --
    tedavi "transfer ile bitti" diyor, ama transfer ekranı, istatistiğin
    transfer sayısı ve gebelik ekranı boş kalıyordu. Temmuzda bir, ocak-
    haziranda yirmi bir satır böyle.

    Transfer edilen embriyo bu tedavinin (Yumurta Çözme'de bu tedavide
    döllenen) 2PN'lerinden, dondurulmayanlardan seçiliyor -- hangisi olduğu
    kaynak kayıtta yok, docstring'deki dağıtım kuralının aynısı. Kaynağın
    EMBRİYO1/2 kutusundaki skor o embriyonun o günkü değerlendirmesi olarak
    yazılıyor (dondurmadaki kuralın aynısı), olayın notunda ham hali.
    Tedavide zaten bir transfer varsa hiçbir şey yazılmıyor ("tamamla"
    ikinci kez çalışabilsin diye).
    """
    if r["tip"] not in ("ivf_icsi", "yumurta_cozme") or not r["transfer_adet"]:
        return
    gun_tr = r["transfer"] or (r["tarih"] if r["tarih_yaklasik"] else None)
    if not gun_tr:
        rapor.append("    UYARI: transfer tarihi yok, transfer yazılamadı")
        return
    if b.execute("SELECT 1 FROM olay o WHERE o.tip='transfer' AND o.iptal_mi=0 "
                 "AND COALESCE(o.tr_cycle_id, o.cycle_id)=? LIMIT 1",
                 (cycle_id,)).fetchone():
        rapor.append("    transfer zaten girilmiş, dokunulmadı")
        return
    adaylar = _db.tedavi_ornekleri(r["tip"], "s")
    bos = [sid for (sid,) in b.execute(
        "SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
        f"WHERE {adaylar} AND o.tip='fertilizasyon_kontrolu' AND o.iptal_mi=0 "
        f"AND o.fert_pn_sayisi='2' AND {_db.bu_tedavide(cycle_id, 'o')} "
        "AND NOT EXISTS (SELECT 1 FROM olay v WHERE v.specimen_id=s.id "
        "  AND v.tip IN ('vitrifikasyon', 'transfer') AND v.iptal_mi=0) "
        "GROUP BY s.id ORDER BY s.cycle_id, s.cycle_sira_no", (cycle_id,)).fetchall()]
    yedek = [s for s in _yedek_embriyolar(b, r, cycle_id) if s not in bos]
    yedekten = max(0, min(r["transfer_adet"] - len(bos), len(yedek)))
    bos += yedek[:yedekten]
    if yedekten:
        rapor.append(f"    UYARI: kaynakta 2PN sayısı transferden az -- {yedekten} "
                     "embriyo 2PN kaydı olmayan enjekte yumurtaya yazıldı")
    kaliteler = _transfer_kaliteleri(r)
    asama_gunu = _asama_gunu(r["transfer_asama"])
    ham = [_kalite_yazimi(h, k) for h, k in (r["emb1"], r["emb2"])]
    yazilan = []
    for i, sid in enumerate(bos[:r["transfer_adet"]]):
        o = kaliteler[i] if i < len(kaliteler) else None
        gun = asama_gunu or (5 if o and o["tur"] == "blast" else 3)
        alan = _oge_alanlari(o, gun) if o else None
        if alan:
            deg_tipi, alanlar = alan
            _degerlendirme_yaz(b, kid, sid, cycle_id, deg_tipi, gun,
                               _zaman(gun_tr, "09:00:00"), alanlar, o["ham"],
                               onek=_KAYNAK_YAZIMI + " (transfer)")
        _olay(b, kid, sid, _kendi_tedavisi(b, sid), "transfer",
              _zaman(gun_tr, "12:00:00"), tr_cycle_id=cycle_id,
              notlar=(f'Aşama: {r["transfer_asama"]}. ' if r["transfer_asama"] else "")
                     + (f"Embriyo: {ham[i]}" if i < len(ham) and ham[i] else ""))
        _durum_yaz(b, sid, "transfer_edildi")
        yazilan.append(ham[i] if i < len(ham) and ham[i] else "skorsuz")
    if len(yazilan) < r["transfer_adet"]:
        rapor.append(f'    UYARI: {r["transfer_adet"]} transfer yazıyor ama '
                     f"{len(yazilan)} uygun embriyo var (enjekte edilmiş, "
                     "dondurulmamış); fazlası yazılmadı -- transferi elle gir")
    if yazilan:
        rapor.append(f'    taze transfer: {len(yazilan)} embriyo ({", ".join(yazilan)})')


def _fet_embriyolari(b, r, cycle_id, cycle_no, kid, rapor):
    """FET'te çözülen/transfer edilen embriyolar (docstring: "FET" bölümü).

    Embriyolar önce FET'in kendi altında açılıyor (v6.130); dondurulduğu
    tüp programdaysa `_kaynaga_bagla()` onları o tüpün örneklerine taşıyor
    (v6.148).
    """
    adet = _cozulen_sayisi(r)
    if not adet:
        rapor.append("    çözülen/transfer sayısı kaynak kayıtta yok, "
                     "embriyo kaydı açılmadı")
        return
    gun = _cozme_gunu(r)
    if not gun:
        rapor.append("    UYARI: çözme tarihi yok, embriyo kaydı açılmadı")
        return
    t_thaw = _zaman(gun, "09:00:00")
    t_tr = _zaman(r["transfer"] or gun, "12:00:00")
    kaliteler = [_kalite_yazimi(h, k) for h, k in (r["emb1"], r["emb2"]) if h or k]
    tr_adet = r["transfer_adet"] or 0

    # Viabilite geçersizse (100'ü aşan, `satirlari_oku()`) canlılık boş;
    # transfer edilen embriyo her durumda çözmeden canlı çıkmıştır.
    via = r["viabilite"]
    via_notu = (f'Çözme sonrası viabilite kaynak kayıtta "{r["viabilite_ham"]}" '
                "yazılı (100'ü aşıyor, embriyo başına değerler bitişik "
                "yazılmış olabilir); canlılık boş bırakıldı."
                if r["viabilite_ham"] else None)
    embriyolar = []
    for i in range(1, adet + 1):
        sid = _specimen_ac(b, cycle_id, cycle_no, i, "oosit", t_thaw)
        canli = (via or 0) > 0 or i <= tr_adet
        # Transfer edilen embriyo mutlaka çözülmüştür; `thaw_cycle_id` bu
        # tedaviyi gösteriyor (CLAUDE.md: "hangi tedavi için çözüldü").
        _olay(b, kid, sid, cycle_id, "thaw", t_thaw, thaw_cycle_id=cycle_id,
              thaw_sagkalim="canli" if canli else None,
              thaw_canlilik=via, notlar=via_notu)
        _durum_yaz(b, sid, "cozuldu")
        embriyolar.append(sid)

    for i, sid in enumerate(embriyolar[:tr_adet]):
        _olay(b, kid, sid, cycle_id, "transfer", t_tr, tr_cycle_id=cycle_id,
              notlar=(f'Aşama: {r["transfer_asama"]}. ' if r["transfer_asama"] else "")
                     + (f'Embriyo: {kaliteler[i]}' if i < len(kaliteler) else ""))
        _durum_yaz(b, sid, "transfer_edildi")
    rapor.append(f'    {adet} embriyo çözüldü, {tr_adet} transfer edildi'
                 + (" (tarih yaklaşık)" if r["tarih_yaklasik"] and not r["transfer"] else ""))


def _fet_transfer_kalitesi(b, r, cycle_id, kid, rapor):
    """FET'te transfer edilen embriyonun kalitesi, aşama ekranına (v6.154).

    Kullanıcının bildirdiği: "FET tedavileri hâlâ formlara işlenmiyor."
    Kaynağın "EMBRİYO1/2 HÜCRE/AŞAMA" + "KALİTE" kutuları FET'te yalnızca
    transfer olayının notuna yazılıyordu; hiçbir değerlendirme açılmadığı
    için Özet'in EMBRİYO1/2 kutuları, TRANSFER AŞAMASI ve ART Lab'ın "Uterus
    grade"i boş basılıyordu. Taze transferin (`_taze_transfer()`) zaten
    yaptığı şey: kutudaki skor o embriyonun o günkü değerlendirmesi.

    - Embriyolar transfer sırasıyla (`_fet_embriyolari()` onları sırayla
      açıp ilk N'ini transfer ediyor; `_kaynaga_bagla()` taşısa da olayların
      kimlik sırası aynı kalıyor).
    - Saat çözme (09:00) ile transfer (12:00) arasında, 11:00: değerlendirme
      çözmeden sonra olmalı ki FET'in işi sayılsın (`db.olay_tedavisi()`).
    - **Aynı gün, aynı tipte değerlendirmesi olan embriyoya yazılmıyor**:
      tüpüne bağlanmış embriyonun kaynak tedavideki kaydıyla çakışırdı
      (değerlendirme örnek+gün başına tek kayıt, v6.146'nın açık sorunu).
      O embriyonun kalitesi zaten kaynağından görünüyor.
    - **Bu tedavide o tipte değerlendirmesi olan embriyoya dokunulmuyor**
      (ekranda girilmiş ya da elle düzeltilmiş olabilir; `tamamla`'nın
      skoru ezme riski burada yok). Yani ikinci çalıştırma hiçbir şey
      değiştirmez ve rapor da bir şey yazmaz.
    """
    if r["tip"] not in ("fet", "fet_kultur") or not r["transfer_adet"]:
        return
    kaliteler = _transfer_kaliteleri(r)
    if not any(kaliteler):
        return
    trler = b.execute(
        "SELECT o.specimen_id, o.zaman FROM olay o WHERE o.tip='transfer' "
        "AND o.iptal_mi=0 AND o.tr_cycle_id=? ORDER BY o.id",
        (cycle_id,)).fetchall()
    asama_gunu = _asama_gunu(r["transfer_asama"])
    ham = [_kalite_yazimi(h, k) for h, k in (r["emb1"], r["emb2"])]
    yazilan, atlanan = [], []
    for i, tr in enumerate(trler[:len(kaliteler)]):
        o = kaliteler[i]
        if not o:
            continue
        gun = asama_gunu or (5 if o["tur"] == "blast" else 3)
        alan = _oge_alanlari(o, gun)
        if not alan:
            continue
        deg_tipi, alanlar = alan
        sid = tr["specimen_id"]
        baska = b.execute(
            "SELECT 1 FROM olay o WHERE o.specimen_id=? AND o.tip=? AND o.gun=? "
            f"AND o.iptal_mi=0 AND NOT ({_db.bu_tedavide(cycle_id, 'o')}) LIMIT 1",
            (sid, deg_tipi, gun)).fetchone()
        if baska:
            atlanan.append(ham[i] or "?")
            continue
        if b.execute(
                "SELECT 1 FROM olay o WHERE o.specimen_id=? AND o.tip=? "
                f"AND o.iptal_mi=0 AND {_db.bu_tedavide(cycle_id, 'o')} LIMIT 1",
                (sid, deg_tipi)).fetchone():
            continue
        _degerlendirme_yaz(b, kid, sid, cycle_id, deg_tipi, gun,
                           _zaman(tr["zaman"][:10], "11:00:00"), alanlar,
                           o["ham"], onek=_KAYNAK_YAZIMI + " (transfer)")
        yazilan.append(ham[i] or "?")
    if yazilan:
        rapor.append(f'    transfer edilen embriyo kalitesi: {", ".join(yazilan)}')
    if atlanan:
        rapor.append(f'    transfer kalitesi yazılmadı ({", ".join(atlanan)}): '
                     "embriyonun kaynak tedavisinde aynı günün kaydı var")


# Hastanın bir çözmeyle karşılaştırılacak en çok tüp sayısı. Alt kümeler
# tek tek deneniyor (2^N); bu labda bir hastanın en çok 7 tüpü var.
_BAGLA_EN_COK_TUP = 14


def _uyumlu(q, anahtar, sira) -> bool:
    """Transfer edilen embriyonun yazımı (q) tüpteki örnekle tutuyor mu?
    Aynı evrede skor aynı olmalı; tüpteki örnek daha erken evredeyse
    kültürde ilerlemiş olabilir (tutar); daha ileri evredeyse geri dönemez
    (tutmaz). Skoru bilinmeyen taraf ("BB", tanınmayan yazım) sınırlamıyor."""
    if q is None or sira is None:
        return True
    qs = _oge_sirasi(q)
    if qs is None:
        return True
    if sira != qs:
        return sira < qs
    return _oge_anahtari(q) == anahtar


def _eslestir(kaliteler, ornekler):
    """Her transfer yazımına tüplerden ayrı bir örnek bulur. Döner: her
    yazım için `ornekler` içindeki sıra (yazım tanınmıyorsa None), ya da
    eşleşme yoksa None. Yazım en çok iki (EMBRİYO1/2), geri izleme yetiyor."""
    def dene(i, kullanilan):
        if i == len(kaliteler):
            return []
        q = kaliteler[i]
        if q is None:
            devam = dene(i + 1, kullanilan)
            return None if devam is None else [None] + devam
        # Önce skoru birebir tutan örnek denenir, sonra "kültürde ilerlemiş
        # olabilir" diye tutan: aynı tüpte ikisi de varsa birebir olan seçilsin.
        sira_q, anahtar_q = _oge_sirasi(q), _oge_anahtari(q)
        adaylar = sorted(range(len(ornekler)), key=lambda j: not (
            ornekler[j][2] == sira_q and ornekler[j][1] == anahtar_q))
        for j in adaylar:
            _sid, anahtar, sira = ornekler[j]
            if j not in kullanilan and _uyumlu(q, anahtar, sira):
                devam = dene(i + 1, kullanilan | {j})
                if devam is not None:
                    return [j] + devam
        return None
    return dene(0, frozenset())


def _kaynaga_bagla(b, r, cycle_id, kid, rapor) -> str:
    """FET'te ve Yumurta Çözme'de çözülen örnekleri, dondurulduğu tüp
    programdaysa o tüpün örneklerine bağlar (v6.148).

    Kullanıcının kararı: "Bağla, belirsizi listele". v6.130'dan beri çözülen
    embriyo FET'in KENDİ altında açılıyordu, çünkü dondurulduğu tedavi
    programda yoktu. Ocak-haziran aktarılınca çoğu FET'in kaynağı programda:
    Cryo Haritası o tüpleri hâlâ "dolu" gösterirdi, soyağacı ("bu embriyo
    hangi tedaviden") kopuk kalırdı.

    Eşleştirme hastanın **dolu** tüplerinden, çözmeden önce dondurulmuş
    olanlardan: toplam örnek sayısı çözülen sayıya eşit olan tüp kümeleri
    aranıyor (bir tüp bütün olarak çözülür) ve transfer edilen embriyonun
    yazımı (EMBRİYO1/2) kümedeki bir örnekle tutmalı (`_uyumlu()`).
    - Tek küme tutuyorsa bağlanıyor. Aynı tedavinin içeriği birebir aynı iki
      tüpü ("(4AA) (4AA)") ayırt edilemez ve fark etmez: ilki alınıyor.
    - Birden çok farklı küme tutuyorsa (farklı tedavilerin aynı skorlu
      tüpleri de) BELİRSİZ; hiç tutmuyorsa BAĞLANAMADI -- ikisi de yazılmıyor,
      rapor kayıt numarasıyla söylüyor, kullanıcı elle bakıyor.

    Bağlamak: FET'in kendi örneklerinin bütün olayları (çözme, transfer,
    yeniden dondurma, değerlendirme) tüpteki örneğe taşınıyor, `olay.cycle_id`
    o örneğin kendi tedavisi oluyor (CLAUDE.md), çözmeye tüp yazılıyor
    (`thaw_tasiyici_id`), FET'in artık boş kendi örnekleri siliniyor, tüp
    programın kendi çözmesindeki gibi boşaltılıyor. Protokol notunun
    "tedavi programda yok" cümlesi kaynağın numarasıyla yeniden kuruluyor.

    Döner: "bagli", "zaten", "belirsiz", "tutmuyor", "yok" (hastanın uygun
    dolu tüpü yok) ya da "" (çözülen örnek yok).
    """
    tip = r["tip"]
    if tip not in FET_TIPLERI:
        return ""
    yumurta = _db.cozulen_yumurta_islenir(tip)
    ne = "yumurta" if yumurta else "embriyo"
    cozulen = b.execute(
        "SELECT o.specimen_id, s.cycle_id, o.zaman FROM olay o "
        "JOIN specimen s ON s.id=o.specimen_id WHERE o.tip='thaw' AND o.iptal_mi=0 "
        "AND o.thaw_cycle_id=? ORDER BY s.cycle_id, s.cycle_sira_no",
        (cycle_id,)).fetchall()
    if not cozulen:
        return ""
    if any(c[1] != cycle_id for c in cozulen):
        return "zaten"          # bağlanmış (ya da programın kendi çözmesi)
    kendi = [c[0] for c in cozulen]
    n = len(kendi)
    t_cozme = min(c[2] for c in cozulen)
    hasta_id = b.execute("SELECT hasta_id FROM cycle WHERE id=?",
                         (cycle_id,)).fetchone()[0]

    ted = _db.vit_tedavisi("o")
    tupler = {}
    for tid, etiket, konum, sid, dt, dt_no, dt_tip in b.execute(
            f"SELECT t.id, t.etiket, t.konum_id, o.specimen_id, {ted}, dc.cycle_no, "
            "dc.cycle_tipi FROM tasiyici t "
            "JOIN olay o ON o.vit_tasiyici_id=t.id AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
            "JOIN specimen s ON s.id=o.specimen_id "
            "JOIN cycle sc ON sc.id=s.cycle_id "
            f"JOIN cycle dc ON dc.id={ted} "
            "WHERE sc.hasta_id=? AND t.durum='dolu' AND t.kategori='embriyo' "
            f"AND {ted} <> ? AND o.zaman < ? "
            "AND NOT EXISTS (SELECT 1 FROM olay x WHERE x.tip='thaw' AND x.iptal_mi=0 "
            "                AND x.thaw_tasiyici_id=t.id) "
            "ORDER BY t.id, o.id", (hasta_id, cycle_id, t_cozme)).fetchall():
        tup = tupler.setdefault(tid, {"tid": tid, "etiket": etiket, "konum": konum,
                                      "ted": set(), "no": dt_no, "tip": dt_tip,
                                      "ornekler": []})
        tup["ted"].add(dt)
        tup["ornekler"].append(sid)
    # Yalnızca tek tedavinin, doğru türde (yumurta/embriyo) içeriği olan tüpler
    adaylar = []
    for tup in tupler.values():
        if len(tup["ted"]) != 1 or _db.yumurta_mi(tup["tip"]) != yumurta:
            continue
        tup["ted"] = next(iter(tup["ted"]))
        tup["ornekler"] = [
            (sid, *( (None, None) if yumurta else
                     _degerlendirme_anahtari(b, sid, tup["ted"])))
            for sid in tup["ornekler"]]
        adaylar.append(tup)
    if not adaylar:
        rapor.append(f"    çözülen {ne}ların tüpü programda yok "
                     "(dondurma program öncesi)")
        return "yok"
    if len(adaylar) > _BAGLA_EN_COK_TUP:
        rapor.append(f"    BAĞLANAMADI: hastanın {len(adaylar)} dolu tüpü var, "
                     "karşılaştırılamayacak kadar çok -- elle bakılmalı")
        return "tutmuyor"

    kaliteler = [] if yumurta else _transfer_kaliteleri(r)
    gecerli = []
    for k in range(1, len(adaylar) + 1):
        for alt in itertools.combinations(range(len(adaylar)), k):
            ornekler = [o for i in alt for o in adaylar[i]["ornekler"]]
            if len(ornekler) != n:
                continue
            esle = _eslestir(kaliteler, ornekler)
            if esle is not None:
                gecerli.append((alt, esle))

    def sinif(alt):
        return (tuple(sorted({adaylar[i]["ted"] for i in alt})),
                tuple(sorted(tuple(sorted(str(o[1]) for o in adaylar[i]["ornekler"]))
                             for i in alt)))

    def anlat(alt):
        return (f'{adaylar[alt[0]]["no"]}: '
                + " + ".join(adaylar[i]["etiket"] for i in alt))

    def tam(alt, esle):
        """Yazımı skoruyla birebir tutan transfer sayısı. "Kültürde
        ilerlemiş olabilir" diye tutan küme (kavitasyon tüpü, 4CC transferi)
        ancak birebir tutan yoksa aday: yoksa her FET'te bir KAV tüpü
        seçeneği belirsizlik yaratırdı."""
        ornekler = [o for i in alt for o in adaylar[i]["ornekler"]]
        return sum(1 for q, j in zip(kaliteler, esle) if q is not None
                   and j is not None and _oge_sirasi(q) is not None
                   and ornekler[j][2] == _oge_sirasi(q)
                   and ornekler[j][1] == _oge_anahtari(q))
    if gecerli:
        en_iyi = max(tam(a, e) for a, e in gecerli)
        gecerli = [(a, e) for a, e in gecerli if tam(a, e) == en_iyi]
    siniflar = {}
    for alt, esle in gecerli:
        siniflar.setdefault(sinif(alt), (alt, esle))
    if not siniflar:
        ozet = ", ".join(f'{t["etiket"]} ({len(t["ornekler"])})' for t in adaylar)
        rapor.append(f"    BAĞLANAMADI: hastanın dolu tüpleri ({ozet}) çözülen "
                     f"{n} {ne} ve transfer yazımıyla tutmuyor -- elle bakılmalı")
        return "tutmuyor"
    if len(siniflar) > 1:
        rapor.append(f"    BELİRSİZ: çözülen {n} {ne} birden çok tüp seçeneğiyle "
                     f"tutuyor ({' | '.join(anlat(a) for a, _e in siniflar.values())})"
                     " -- bağlanmadı, elle bakılmalı")
        return "belirsiz"
    alt, esle = next(iter(siniflar.values()))

    # Kendi örneklerinde fotoğraf/bulgu varsa (aktarımdan sonra elle
    # eklenmiş) örnek silinemez -- dokunma, söyle.
    for tablo in ("goruntu", "specimen_bulgu", "pgt_sonuc"):
        if not b.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                         (tablo,)).fetchone():
            continue
        if b.execute(f"SELECT 1 FROM {tablo} WHERE specimen_id IN "
                     f"({','.join('?' * n)}) LIMIT 1", kendi).fetchone():
            rapor.append(f"    BAĞLANMADI: çözülen {ne}lara sonradan {tablo} "
                         "kaydı eklenmiş -- elle bakılmalı")
            return "tutmuyor"

    ornekler = [o for i in alt for o in adaylar[i]["ornekler"]]
    tupu = {o[0]: adaylar[i]["tid"] for i in alt for o in adaylar[i]["ornekler"]}
    # Transfer edilen kendi örnekleri, transfer sırasıyla (`_fet_embriyolari()`
    # transferi ilk örneklere veriyor): eşleşen tüp örneğine.
    transferli = [sid for (sid,) in b.execute(
        "SELECT s.id FROM specimen s WHERE s.cycle_id=? AND EXISTS (SELECT 1 FROM "
        "olay t WHERE t.specimen_id=s.id AND t.tip='transfer' AND t.iptal_mi=0) "
        "ORDER BY s.cycle_sira_no", (cycle_id,)).fetchall()]
    eslesme, kullanilan = {}, set()
    for qi, oi in enumerate(esle):
        if oi is not None and qi < len(transferli):
            eslesme[transferli[qi]] = ornekler[oi][0]
            kullanilan.add(oi)
    kalan = [o[0] for j, o in enumerate(ornekler) if j not in kullanilan]
    if yumurta:
        # Yumurtada olgunluğu aynı olanlar birbirine (MI'ya MI)
        olg = {sid: _olgunluk(b, sid, adaylar[alt[0]]["ted"]) for sid in kalan}
        for sid in kendi:
            k = _olgunluk(b, sid, cycle_id)
            es = next((x for x in kalan if olg[x] == k), None) or kalan[0]
            eslesme[sid] = es
            kalan.remove(es)
    else:
        for sid in kendi:
            if sid not in eslesme:
                eslesme[sid] = kalan.pop(0)

    cozme_tupu = _db.cozme_tupu_var()
    for kendi_sid, kaynak_sid in eslesme.items():
        durum = b.execute("SELECT durum FROM specimen WHERE id=?",
                          (kendi_sid,)).fetchone()[0]
        b.execute("UPDATE olay SET specimen_id=?, cycle_id=? WHERE specimen_id=?",
                  (kaynak_sid, _kendi_tedavisi(b, kaynak_sid), kendi_sid))
        if cozme_tupu:
            b.execute("UPDATE olay SET thaw_tasiyici_id=? WHERE specimen_id=? "
                      "AND tip='thaw' AND iptal_mi=0 AND thaw_cycle_id=?",
                      (tupu[kaynak_sid], kaynak_sid, cycle_id))
        b.execute("UPDATE specimen SET durum=? WHERE id=?", (durum, kaynak_sid))
        b.execute("DELETE FROM specimen WHERE id=?", (kendi_sid,))
    for i in alt:
        b.execute("UPDATE tasiyici SET durum='bosaltildi' WHERE id=?",
                  (adaylar[i]["tid"],))
        if adaylar[i]["konum"]:
            b.execute("UPDATE konum SET durum='bos' WHERE id=?", (adaylar[i]["konum"],))

    nolar = sorted({adaylar[i]["no"] for i in alt})
    kaynak_no = (nolar[0] + " tedavisinde" if len(nolar) == 1 else
                 ", ".join(nolar[:-1]) + " ve " + nolar[-1] + " tedavilerinde")
    notu = b.execute("SELECT protokol_notu FROM cycle WHERE id=?",
                     (cycle_id,)).fetchone()[0] or ""
    eski = textwrap.fill(_aktarim_cumlesi(tip), 68)
    yeni = textwrap.fill(_aktarim_cumlesi(tip, kaynak_no), 68)
    if eski in notu:
        b.execute("UPDATE cycle SET protokol_notu=? WHERE id=?",
                  (notu.replace(eski, yeni), cycle_id))
    else:
        rapor.append("    (protokol notu elle değiştirilmiş, kaynak cümlesi "
                     "güncellenmedi)")
    rapor.append(f"    çözme kaynağı: {kaynak_no} dondurulan "
                 f"{len(alt)} tüp ({', '.join(adaylar[i]['etiket'] for i in alt)}) "
                 f"-- {n} {ne} bağlandı, tüp boşaltıldı")
    return "bagli"


def _androloji(b, r, cycle_id, kid):
    """`sperm_ornek` + iki `sperm_analiz` (bazal / hazırlık sonrası).

    Günü OPU; Yumurta Çözme'de sperm ICSI günü, yani çözme günü hazırlanıyor
    (v6.148)."""
    if not (r["sperm_kaynak"] or r["bazal"]["konsantrasyon_milyon_ml"]):
        return
    gun = _cozme_gunu(r) if r["tip"] in FET_TIPLERI else _islem_gunu(r)
    t_al = _zaman(gun, "08:00:00")
    t_haz = _zaman(gun, "10:00:00")
    b.execute("INSERT INTO sperm_ornek (lab_id, cycle_id, alinma_zamani, "
              "alinma_yontemi, hacim_ml, hazirlama_yontemi, hazirlama_zamani, "
              "kullanici_id, notlar, olusturma_zamani) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (_db.LAB_ID, cycle_id, t_al,
               _ALINMA.get(_sade(r["sperm_kaynak"])), r["bazal"]["hacim_ml"],
               _HAZIRLAMA.get(_sade(r["hazirlama"])), t_haz,
               kid,
               f'Kaynak kayıt: {r["sperm_kaynak"]} / {r["hazirlama"]}'.strip(" /"),
               t_al))
    ornek_id = b.execute("SELECT last_insert_rowid()").fetchone()[0]
    for asama, veri, zaman in (("bazal", r["bazal"], t_al),
                               ("hazirlik_sonrasi", r["hazirlik"], t_haz)):
        alanlar = {k: v for k, v in veri.items() if v is not None}
        if not alanlar:
            continue
        kolonlar = ["sperm_ornek_id", "asama", "zaman", "kullanici_id"] + list(alanlar)
        b.execute(f"INSERT INTO sperm_analiz ({','.join(kolonlar)}) "
                  f"VALUES ({','.join('?' * len(kolonlar))})",
                  [ornek_id, asama, zaman, kid] + list(alanlar.values()))


def _islem_yapan(b, r, cycle_id):
    """"İşlemi yapan" -- aşama başına tek kişi (`UNIQUE(cycle_id, asama)`).

    Kaynak kayıttaki ad programdaki personel listesinde olmayabilir; tuzak
    #6'nın gereği olarak `_islem_yapan.html` bilinmeyen değeri listeye
    kendi seçeneği olarak ekliyor, o yüzden ad olduğu gibi yazılıyor.
    """
    gun = _cozme_gunu(r) if r["tip"] in FET_TIPLERI else _islem_gunu(r)
    zamanlar = {"opu": _zaman(r["opu"], "09:00:00"),
                "androloji": _zaman(gun, "10:00:00"),
                "icsi": _zaman(gun, "13:00:00"),
                "transfer": _zaman(r["transfer"], "12:00:00")}
    asamalar = _db.TIP_ASAMALARI.get(r["tip"], ())
    for asama, ad in r["yapan"].items():
        # Tedavinin tipinde olmayan aşamanın "yapan"ı yazılmıyor -- ekranı
        # yok, kimse göremez (Yumurta Çözme'de OPU yok, v6.148).
        if not ad or asama not in asamalar:
            continue
        b.execute("INSERT OR IGNORE INTO islem_yapan (lab_id, cycle_id, asama, "
                  "yapan_ad, zaman) VALUES (?,?,?,?,?)",
                  (_db.LAB_ID, cycle_id, asama, re.sub(r"\s+", " ", ad),
                   zamanlar.get(asama)))


def _zaten_var(kimlik):
    """Bu Access satırı daha önce aktarılmış mı? (işaret protokol notunda)

    Hastanın dosya numarası da dönüyor: `_carpismalar()` "işaret tuttu ama
    BAŞKA hastanın tedavisi" durumunu ondan anlıyor.
    """
    # Satır sonları boşluğa katlanıyor: notu elle düzenleyen ya da daha
    # uzun bir etiket kullanan biri işareti iki satıra bölerse arama yine
    # tutsun. Kemer + askı -- `_not_kur()` işareti zaten kendi satırında
    # yazıyor, ama bu sorgu daha önce yazılmış notları da okuyor.
    return _db.tek("SELECT c.id, c.cycle_no, c.cycle_tipi, h.dosya_no FROM cycle c "
                   "JOIN hasta h ON h.id = c.hasta_id "
                   "WHERE c.lab_id=? AND REPLACE(REPLACE(c.protokol_notu, "
                   "char(13), ' '), char(10), ' ') LIKE ?",
                   (_db.LAB_ID, f"%{_isaret(kimlik)}%"))


def _carpismalar(satirlar) -> list:
    """Kayıt numarası çakışması var mı — işaret tuttu ama başka hasta?

    `kaynak=` unutulursa ikinci dosyanın satırları birincininkiyle aynı
    işareti taşır ve "zaten aktarılmış" sanılıp sessizce atlanır. Sessiz
    veri kaybı, bu projenin tuzak listesinin tam olarak uyardığı şey --
    o yüzden betik durup soruyor, uyarıp devam etmiyor.

    Ölçü hastanın dosya numarası: gerçek bir yeniden çalıştırmada işaret
    aynı hastanın tedavisini bulur, çakışmada başkasınınkini.
    """
    return [(r, var) for r in satirlar
            if (var := _zaten_var(r["kimlik"]))
            and str(var["dosya_no"]) != str(r["dosya_no"])]


def _satiri_yaz(r) -> list:
    """Bir Access satırını tek işlemde yazar. Patlarsa hiçbiri yazılmaz."""
    rapor = []
    kid = _kullanici_id()
    with _db.yazma_islemi() as b:
        hasta_id = _hastayi_bul_veya_ac(b, r, rapor)
        cycle_id, cycle_no = _cycle_ac(b, r, hasta_id, rapor)
        if r["tip"] in ("fet", "fet_kultur"):
            _fet_embriyolari(b, r, cycle_id, cycle_no, kid, rapor)
            # Çözme sonrası yeniden dondurma (v6.143) -- çözme kayıtları bir
            # satır yukarıda, aynı işlemde yazıldı; hedef örnekleri onlar.
            _dondurma_kayitlari(b, r, cycle_id, kid, rapor)
        else:
            # IVF/ICSI, Yumurta Dondurma ve Yumurta Çözme (çözülen yumurtaya
            # ICSI, v6.147): yumurtalar, dondurma, taze transfer, androloji.
            # Dondurma transferden önce: ikisi de 2PN'lerden seçiyor.
            _oositleri_ac(b, r, cycle_id, cycle_no, kid, rapor)
            _dondurma_kayitlari(b, r, cycle_id, kid, rapor)
            _taze_transfer(b, r, cycle_id, kid, rapor)
            _androloji(b, r, cycle_id, kid)
        _islem_yapan(b, r, cycle_id)
        # Çözülen örneği dondurulduğu tüpe bağla (v6.148) -- bütün olaylar
        # yazıldıktan sonra, çünkü onları taşıyor.
        durum = _kaynaga_bagla(b, r, cycle_id, kid, rapor)
        # FET'te transfer edilen embriyonun kalitesi (v6.154) -- bağlamadan
        # SONRA: bağlanan embriyonun kaynaktaki aynı günün kaydıyla
        # çakışmasın diye o kayda bakıyor.
        _fet_transfer_kalitesi(b, r, cycle_id, kid, rapor)
        _tedavi_sirasi(b, hasta_id, cycle_id, rapor)
    return rapor, durum


def _ozet_satiri(r) -> str:
    sebep = _iptal_sebebi(r["notlar"])
    if sebep:
        son = f"İPTAL ({sebep})"
    elif (r["transfer"] or r["tarih_yaklasik"]) and r["transfer_adet"]:
        son = "tamamlandı / transfer"
    elif r["dondurulan"] or _satir_dondurmasi(r):
        son = "tamamlandı / dondurma"
    else:
        son = "tamamlandı (sebep yok — kaynak kayıt söylemiyor)"
    if r["tip"] in ("fet", "fet_kultur"):
        icerik = (f'{_cozulen_sayisi(r)} embriyo çözme, '
                  f'{r["transfer_adet"] or 0} transfer')
    else:
        n = (max(r["toplanan"] or 0, r["mii"] + r["immatur"] + r["empty_zona"]
                 + r["dejenere"] + r["atretik"], r["islenen"] or 0)
             if r["tip"] == "yumurta_cozme" else r["toplanan"])
        icerik = (f'{n} {"çözülen yumurta" if r["tip"] == "yumurta_cozme" else "oosit"}'
                  f' / {r["mii"]} MII / {r["islenen"]} ICSI / {r["iki_pn"]} 2PN / '
                  f'{r["dondurulan"]} dondurma')
    ek = ""
    if r["tarih_yaklasik"]:
        ek += "   [tarih yok: yaklaşık]"
    for alan, eski, yeni in r["duzeltme"]:
        ek += f"   [{alan} {_gg(eski)} → {_gg(yeni)}]"
    return (f'#{r["kimlik"]:>3}  dosya {r["dosya_no"]:<10} {r["tip"]:<14}'
            f'{r["tarih"] or "tarihsiz":<11} {icerik:<52} {son}{ek}')


def onizleme(satirlar, kopyalar=(), tutmayan=()):
    print(f"\nCSV'de {len(satirlar) + len(kopyalar)} satır. Veritabanı: {DB}\n")
    for r in kopyalar:
        print(f'#{r["kimlik"]:>3}  ATLANIR — aynı hastanın aynı günkü dolu '
              "satırının boş kopyası (hiçbir sayı ve not yok)")
    for t in tutmayan:
        print(f"UYARI: tarih düzeltmesi uygulanmadı, Access'teki değer tutmuyor: {t}")
    yeni_hasta, atlanan = 0, 0
    gorulen = set()
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if var:
            atlanan += 1
            print(f'#{r["kimlik"]:>3}  ATLANIR — zaten aktarılmış '
                  f'(tedavi {var["cycle_no"]})')
            continue
        h = _db.tek("SELECT id FROM hasta WHERE lab_id=? AND dosya_no=?",
                    (_db.LAB_ID, r["dosya_no"]))
        if not h and r["dosya_no"] not in gorulen:
            yeni_hasta += 1
        gorulen.add(r["dosya_no"])
        print(_ozet_satiri(r) + ("   [YENİ HASTA]" if not h else ""))
        if r["dosya_no"] < 1000:
            print(f'        DİKKAT: dosya numarası {len(str(r["dosya_no"]))} haneli '
                  "-- Access'te yer tutucu yazılmış olabilir, kontrol et")
        coz = _satir_dondurmasi(r)
        if coz and coz["ogeler"]:
            # Kullanıcının kendi yazımı basılıyor ("4HG2"), çözümlenmiş kod
            # değil -- kendi notunda ne yazdığını tanıyabilmeli.
            ozet = " ".join("(" + "-".join(o["ham"] for o in g) + ")"
                            for g in coz["gruplar"])
            print(f'        dondurulan ({"yumurta" if coz["oosit_mi"] else "embriyo"}'
                  + (f', gün {coz["gun"]}' if coz["gun"] else "")
                  + f', {len(coz["gruplar"])} tüp): {ozet}'
                  + ("   <- çözme sonrası yeniden dondurma"
                     if r["tip"] in ("fet", "fet_kultur") else "")
                  + ("   <- not fiilsiz söylüyor (\"İLE BİRLİKTE KALDI\")"
                     if coz.get("ortuk") else ""))
        elif coz:
            print("        dondurma notu var   <- kaç örnek/tüp olduğu "
                  "okunamadı, YAZILMAYACAK")
        if r["tip"] in ("ivf_icsi", "yumurta_cozme") and r["transfer_adet"]:
            ham = [_kalite_yazimi(h, k) for h, k in (r["emb1"], r["emb2"]) if h or k]
            print(f'        taze transfer: {r["transfer_adet"]} embriyo'
                  + (f' ({", ".join(ham[:r["transfer_adet"]])})' if ham else ""))
        if r["tip"] in FET_TIPLERI:
            print("        çözülen örnekler hastanın programdaki dolu tüpleriyle "
                  "eşleştirilecek")
    print(f'\n{len(satirlar) - atlanan} tedavi yazılacak, {yeni_hasta} yeni '
          f'hasta kartı açılacak, {atlanan + len(kopyalar)} satır atlanacak.')
    print("Yazmak için: python3 aktar_access.py <dosya.csv>\n")


def _bagla_ozeti(sonuclar):
    """Aktarımın sonunda: FET'lerin kaynak tüpe bağlanması. Elle bakılması
    gerekenler kayıt numarasıyla (kullanıcının kararı: "belirsizi listele")."""
    if not sonuclar:
        return
    say = {}
    for _k, d in sonuclar:
        say[d] = say.get(d, 0) + 1
    print(f'\nÇözme kaynağı: {say.get("bagli", 0)} tedavi tüpüne bağlandı, '
          f'{say.get("yok", 0)} tedavinin tüpü programda yok (program öncesi '
          f'dondurma), {say.get("zaten", 0)} zaten bağlıydı.')
    elle = [(k, d) for k, d in sonuclar if d in ("belirsiz", "tutmuyor")]
    if elle:
        print("Elle bakılmalı (yukarıdaki satırlarında ayrıntı var):")
        for k, d in elle:
            print(f'  #{k:>3}  {"birden çok tüp seçeneği" if d == "belirsiz" else "dolu tüpler tutmuyor"}')


def aktar(satirlar):
    toplam = {"tedavi": 0, "atlanan": 0, "hata": 0}
    sonuclar = []
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if var:
            toplam["atlanan"] += 1
            print(f'#{r["kimlik"]:>3}  atlandı (zaten aktarılmış: {var["cycle_no"]})')
            continue
        try:
            rapor, durum = _satiri_yaz(r)
        except Exception as hata:            # bir satır ötekileri durdurmasın
            toplam["hata"] += 1
            print(f'#{r["kimlik"]:>3}  HATA: {hata}')
            continue
        toplam["tedavi"] += 1
        if durum:
            sonuclar.append((r["kimlik"], durum))
        print(f'#{r["kimlik"]:>3}  aktarıldı')
        for satir in rapor:
            print(satir)
    print(f'\nBitti. {toplam["tedavi"]} tedavi aktarıldı, '
          f'{toplam["atlanan"]} atlandı, {toplam["hata"]} hata.')
    _bagla_ozeti(sonuclar)


def _canlilik_duzelt(b, r, cycle_id, rapor):
    """Daha önce aktarılmış FET'te 100'ü aşan viabilite (v6.148'e kadar
    olduğu gibi yazılıyordu, ekranda "%9080") -- boşaltılır, ham hali notta."""
    if not r["viabilite_ham"] or r["tip"] not in FET_TIPLERI:
        return
    notu = (f'Çözme sonrası viabilite kaynak kayıtta "{r["viabilite_ham"]}" '
            "yazılı (100'ü aşıyor, embriyo başına değerler bitişik yazılmış "
            "olabilir); canlılık boş bırakıldı.")
    n = b.execute("UPDATE olay SET thaw_canlilik=NULL, notlar=? WHERE tip='thaw' "
                  "AND iptal_mi=0 AND thaw_cycle_id=? AND thaw_canlilik > 100",
                  (notu, cycle_id)).rowcount
    if n:
        rapor.append(f"    çözme canlılığı düzeltildi ({n} kayıt): "
                     f'"{r["viabilite_ham"]}" geçersiz, boşaltıldı')


def _cozme_tupu_duzelt(b, r, cycle_id, rapor):
    """Çözmenin tüpü, aynı FET'in kendi yeniden dondurma tüpüyse boşaltılır.

    goc_046 eski çözmelere tüpünü geriye dönük yazarken, çözmeden önce
    dondurması olmayan örneğe "herhangi bir tüpünü" yazıyor. Program öncesi
    FET embriyosunun tek tüpü yeniden dondurulduğu tüp olabilir -- göç
    yeniden dondurmadan SONRA çalışmışsa o tüp "çözülmüş" görünür, dondurma
    geri alınamaz, tüp bir sonraki FET'e aday olmaz (prova kopyasında bir
    tüpte oldu, v6.148). Bir FET kendi dondurduğu tüpü çözemez: koşul bu,
    dar ve kesin.
    """
    if r["tip"] not in FET_TIPLERI or not _db.yeniden_dondurma_var():
        return
    n = b.execute(
        "UPDATE olay SET thaw_tasiyici_id=NULL WHERE tip='thaw' AND iptal_mi=0 "
        "AND thaw_cycle_id=? AND thaw_tasiyici_id IN (SELECT v.vit_tasiyici_id "
        "FROM olay v WHERE v.tip='vitrifikasyon' AND v.iptal_mi=0 "
        "AND v.vit_cycle_id=?)", (cycle_id, cycle_id)).rowcount
    if n:
        rapor.append(f"    çözmenin tüpü düzeltildi ({n}): kendi yeniden dondurma "
                     "tüpü yazılmıştı (goc_046)")


def _iptal_sebebi_duzelt(b, r, cycle_id, kid, rapor):
    """Genel "iptal" ile kapanmış tedaviye nottaki ayrıntılı sebebi yazar.

    v6.149'a kadar araç "Yumurta Çıkmadı" / "İmmatür Yumurta" sebeplerini
    tanımıyordu; o notlar genel "İptal"e düştü. **Yalnızca sebep hâlâ genel
    "iptal" ise** değiştiriliyor -- kullanıcı ekrandan başka bir sebep
    seçtiyse (`/cycle/{id}/bitir`) ona dokunulmaz. Değişiklik geçmişine de
    yazılıyor, ekranda elle yapılan değişiklik gibi.
    """
    sebep = _iptal_sebebi(r["notlar"])
    if not sebep or sebep == "iptal":
        return
    c = b.execute("SELECT durum, bitis_sebebi FROM cycle WHERE id=?",
                  (cycle_id,)).fetchone()
    if not c or c["durum"] != "iptal" or c["bitis_sebebi"] != "iptal":
        return
    b.execute("UPDATE cycle SET bitis_sebebi=? WHERE id=?", (sebep, cycle_id))
    # `guvenlik.degisiklikleri_yaz()` kendi bağlantısını açıyor; burası
    # `yazma_islemi()`'nin kilidi içinde, o yüzden aynı bağlantıdan yazılıyor.
    b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
              "eski_deger, yeni_deger, kullanici_id, zaman) "
              "VALUES (?,?,?,?,?,?,?,?)",
              (_db.LAB_ID, "cycle", str(cycle_id), "bitis_sebebi", "iptal",
               sebep, kid,
               _dt.datetime.now().isoformat(" ", "seconds")))
    rapor.append(f"    iptal sebebi: iptal → {sebep}")


def fet_transfer_kalitelerini_yaz(satirlar):
    """Yalnızca FET transfer kalitesi: `tamamla`'nın 6. adımı, tek başına
    (v6.154). `iptal` kipiyle aynı gerekçe: `tamamla` dondurma skorlarını
    nottaki değerle yeniden yazıyor, elle düzeltilmiş skoru ezebilir; bu kip
    yalnızca FET'te transfer edilen, o gün değerlendirmesi olmayan
    embriyolara kaynağın EMBRİYO1/2 kutusunu yazıyor. İkinci çalıştırma
    hiçbir şey değiştirmez."""
    kid = _kullanici_id()
    degisen = 0
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if not var:
            continue
        rapor = []
        if var["cycle_tipi"] != r["tip"]:
            r = dict(r, tip=var["cycle_tipi"])
        with _db.yazma_islemi() as b:
            _fet_transfer_kalitesi(b, r, var["id"], kid, rapor)
        if rapor:
            degisen += 1
            print(f'#{r["kimlik"]:>3}  {var["cycle_no"]}')
            for satir in rapor:
                print(satir)
    print(f"\nBitti. {degisen} FET tedavisine transfer kalitesi yazildi.")


def iptal_sebeplerini_duzelt(satirlar):
    """Yalnızca iptal sebebi: `tamamla`'nın 5. adımı, tek başına (v6.150).

    `tamamla` dondurulan embriyoların değerlendirmesini nottaki değerle
    yeniden yazıyor -- aylar önce aktarılmış bir tedavide ekrandan elle
    düzeltilmiş bir skoru ezer (v6.142). Sebebi onarmak için o riski almaya
    gerek yok: bu kip `cycle.bitis_sebebi` dışında hiçbir şeye dokunmuyor.
    İkinci çalıştırma hiçbir şey değiştirmez.
    """
    kid = _kullanici_id()
    degisen = 0
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if not var:
            continue
        rapor = []
        with _db.yazma_islemi() as b:
            _iptal_sebebi_duzelt(b, r, var["id"], kid, rapor)
        if rapor:
            degisen += 1
            print(f'#{r["kimlik"]:>3}  {var["cycle_no"]}')
            for satir in rapor:
                print(satir)
    print(f"\nBitti. {degisen} tedavinin iptal sebebi guncellendi.")


def tamamla(satirlar):
    """Zaten aktarılmış tedavileri aracın bugünkü kurallarıyla tamamlar.

    Aktarım bir kez yapıldıktan sonra betiğin yeni bir sürümü çıktığında
    baştan almak gerekmesin diye. Her adım idempotent -- ikinci çalıştırma
    hiçbir şey değiştirmez:
    1. dondurma: nottaki tüpler, var olan tüpler onarılarak (v6.148: temmuzun
       "BB" embriyoları ve MI yumurtaları, FET'in yeniden dondurması);
    2. taze transfer (v6.148: araç IVF/ICSI transferini hiç yazmıyordu);
    3. geçersiz çözme canlılığı, çözmeye yanlış yazılmış tüp (goc_046);
    4. çözülen örneği dondurulduğu tüpe bağlama;
    5. iptal sebebi: genel "iptal" kalmış tedavi, not bugün tanınan ayrıntılı
       bir sebep söylüyorsa (v6.150: "OOSİT ÇIKMADI", "İNMATÜR OOSİT");
    6. FET'te transfer edilen embriyonun kalitesi (v6.154).
    **Hemen çalıştır**: değerlendirme nottaki değerle güncelleniyor, aktarılan
    bir skoru ekranda elle düzelttiysen `tamamla` o düzeltmeyi ezer (v6.142).
    """
    kid = _kullanici_id()
    sayac = {"islenen": 0, "atlanan": 0, "hata": 0}
    sonuclar = []
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if not var:
            sayac["atlanan"] += 1
            print(f'#{r["kimlik"]:>3}  aktarılmamış, atlandı')
            continue
        rapor = []
        if var["cycle_tipi"] != r["tip"]:
            # Aktarıldığı günden beri kuralı değişen tip (programda elle
            # değiştirilmiş de olabilir): programdaki geçerli.
            rapor.append(f'    tip: programda {var["cycle_tipi"]}, kaynak '
                         f'{r["tip"]} sayılıyor -- programdaki kullanıldı')
            r = dict(r, tip=var["cycle_tipi"])
        try:
            with _db.yazma_islemi() as b:
                _dondurma_kayitlari(b, r, var["id"], kid, rapor)
                _taze_transfer(b, r, var["id"], kid, rapor)
                _canlilik_duzelt(b, r, var["id"], rapor)
                _cozme_tupu_duzelt(b, r, var["id"], rapor)
                durum = _kaynaga_bagla(b, r, var["id"], kid, rapor)
                _iptal_sebebi_duzelt(b, r, var["id"], kid, rapor)
                _fet_transfer_kalitesi(b, r, var["id"], kid, rapor)
        except Exception as hata:
            sayac["hata"] += 1
            print(f'#{r["kimlik"]:>3}  HATA: {hata}')
            continue
        sayac["islenen"] += 1
        if durum:
            sonuclar.append((r["kimlik"], durum))
        if rapor:
            print(f'#{r["kimlik"]:>3}  {var["cycle_no"]}')
            for satir in rapor:
                print(satir)
    print(f'\nBitti. {sayac["islenen"]} tedavi gözden geçirildi, '
          f'{sayac["atlanan"]} atlandı, {sayac["hata"]} hata.')
    _bagla_ozeti(sonuclar)


def main():
    global KAYNAK
    arg, duzelt = [], None
    for a in sys.argv[1:]:
        if a.lower().startswith("kaynak="):
            KAYNAK = _kaynak_ayikla(a.split("=", 1)[1])
        elif a.lower().startswith("duzelt="):
            duzelt = a.split("=", 1)[1]
        else:
            arg.append(a)
    kip = "aktar"
    if arg and arg[0] in ("liste", "tamamla", "iptal", "transfer"):
        kip, arg = arg[0], arg[1:]
    if not arg:
        sys.exit("Kullanim:\n"
                 "  python3 aktar_access.py liste <dosya.csv>     ne yazilacagini gosterir\n"
                 "  python3 aktar_access.py <dosya.csv>           aktarir\n"
                 "  python3 aktar_access.py tamamla <dosya.csv>   zaten aktarilmis\n"
                 "                                                tedavilere nottaki\n"
                 "                                                skorlari ekler\n"
                 "  python3 aktar_access.py iptal <dosya.csv>     yalnizca iptal\n"
                 "                                                sebeplerini gunceller\n"
                 "  python3 aktar_access.py transfer <dosya.csv>  yalnizca FET'te\n"
                 "                                                transfer edilen\n"
                 "                                                embriyonun kalitesi\n"
                 "\n"
                 "  kaynak=<AD>  ikinci bir Access dosyasi aktarilirken sart:\n"
                 "               her dosya kendi kayitlarini 1'den numaraliyor,\n"
                 "               etiket numarayi dosyasina bagliyor.\n"
                 "               ornek: python3 aktar_access.py kaynak=TEMMUZ temmuz.csv\n"
                 "  duzelt=<dosya>  yazim hatali tarihlerin duzeltmeleri (satir:\n"
                 "               KAYNAK#KAYIT  OPU|TRANSFER  eski-tarih  yeni-tarih)")
    # Dosya yoksa Python'un hata dökümü yerine ne olduğunu söyle: Windows
    # uzantıyı gizlediği için "temmuz" görünen dosya "temmuz_2026.csv" ya da
    # "temmuz.csv.csv" olabiliyor (kullanıcının başına geldi, v6.150).
    for yol, ne in ((arg[0], "CSV dosyasi"), (duzelt, "duzeltme dosyasi")):
        if yol and not os.path.isfile(yol):
            buradakiler = sorted(glob.glob("*.csv")) + sorted(glob.glob("*.txt"))
            sys.exit(f"{ne} bulunamadi: {yol}\n"
                     f"Calisilan klasor: {os.getcwd()}\n"
                     "Bu klasordeki .csv/.txt dosyalari:\n"
                     + ("".join(f"  {a}\n" for a in buradakiler)
                        or "  (hic yok -- dosyalar baska bir klasorde)\n")
                     + "Komutta dosyanin adini yukaridaki gibi yaz; adinda "
                       "bosluk varsa tirnak icine al: \"temmuz 2026.csv\"")
    satirlar = satirlari_oku(arg[0])
    # Önce yazım hatası düzeltmeleri, sonra tarihsiz satırlara yakın kaydın
    # tarihi (düzeltilen tarih komşusuna da doğru geçsin), sonra boş kopyalar.
    tutmayan = (duzeltmeleri_uygula(satirlar, duzeltmeleri_oku(duzelt), KAYNAK)
                if duzelt else [])
    tarihleri_tamamla(satirlar)
    kopyalar = bos_kopyalari_ayikla(satirlar)
    satirlar.sort(key=lambda r: (r["tarih"] or "9999-99-99", int(r["kimlik"] or 0)))
    cakisan = _carpismalar(satirlar)
    if cakisan:
        print(f"\nDUR -- hicbir sey yazilmadi. {len(cakisan)} satirin kayit "
              "numarasi baska bir aktarimin numarasiyla cakisiyor:\n")
        for r, var in cakisan[:5]:
            print(f'  #{r["kimlik"]:>3} dosya {r["dosya_no"]} -> isaret '
                  f'{var["cycle_no"]} tedavisini buluyor (dosya '
                  f'{var["dosya_no"]}, BASKA hasta)')
        if len(cakisan) > 5:
            print(f"  ... ve {len(cakisan) - 5} satir daha")
        print("\nHer Access dosyasi kendi kayitlarini 1'den numaraliyor. Bu "
              "dosyaya\nkendi etiketini ver, yoksa o satirlar 'zaten "
              "aktarilmis' sanilip\nSESSIZCE atlanir:\n\n"
              f'  python3 aktar_access.py kaynak=<AD> {arg[0]}\n')
        sys.exit(1)
    if kip == "liste":
        onizleme(satirlar, kopyalar, tutmayan)
        return
    # Yazmadan önce: araç göçleri kendisi çalıştırmıyor, program açılışta
    # çalıştırıyor (v6.49). `git pull`'dan sonra program yeniden açılmadıysa
    # FET'in yeniden dondurması `vit_cycle_id`'yi (goc_046) yazarken işlemin
    # ortasında patlardı; goc_047 yoksa eski tedavi araya yerleşmez, eski
    # kural gibi "en yüksek + 1" alırdı -- baştan, hiçbir şey yazmadan söyle.
    eksik = [ad for ad, var in (
        ("goc_046", _db.yeniden_dondurma_var()),
        ("goc_047", _db.kolon_var("cycle", "hasta_cycle_no_elle"))) if not var]
    if eksik:
        sys.exit(f"Veritabani guncellemesi eksik ({', '.join(eksik)}). Programi "
                 "bir kez kapatip ac -- guncellemeler acilista uygulanir -- ya "
                 "da `python3 goc_hepsi.py` calistir, sonra tekrar dene.")
    if kip == "tamamla":
        tamamla(satirlar)
        return
    if kip == "iptal":
        iptal_sebeplerini_duzelt(satirlar)
        return
    if kip == "transfer":
        fet_transfer_kalitelerini_yaz(satirlar)
        return
    onizleme(satirlar, kopyalar, tutmayan)
    print("Bu, veritabanina YAZAR. Once yedek al (/yedekleme -> Simdi yedekle).")
    if input("Devam etmek icin AKTAR yaz: ").strip() != "AKTAR":
        sys.exit("Vazgecildi, hicbir sey yazilmadi.")
    aktar(satirlar)


if __name__ == "__main__":
    main()
