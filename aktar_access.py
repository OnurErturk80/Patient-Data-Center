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

**Yalnızca eksik tüp: `dondurma`** (v6.161). Aracın okuyamadığı için hiç
tüpü yazılmamış dondurmayı yazar ("2 ADET M2 OOSİT DONDURULARAK SAKLANDI"
artık tek tüp); tüpü olan tedaviye dokunmaz:

    python3 aktar_access.py dondurma kaynak=OCAK duzelt=tarih_duzeltme.txt ocak.csv

**FET'leri tüpüne bağlama: `bagla`** (v6.160, v6.163'ten beri dosyasız).
Daha eski bir ay sonradan aktarıldıysa (2026 aktarılmışken 2025) önceki
FET'ler o tüplere ancak şimdi bağlanabilir. **Her aktarımın sonunda bu
kendiliğinden yapılıyor**; bir kez elle de çalıştırılabilir, veritabanındaki
bütün aktarılmış FET'lere bakar, dosya istemez:

    python3 aktar_access.py bagla

**Arada aktarılmamış ay varsa bağlanmaz, ertelenir** (v6.164). Tutan tüp
ile çözme arasında programda hiç tedavisi olmayan bir ay varsa (dosyası
henüz gelmemiş), gerçek tüp o ayda olabilir; o gün tek seçenek görünen tüpe
bağlamak yanlış tüpü boşaltırdı. Rapor "ertelendi" der ve ayları yazar; ay
aktarılınca her aktarımın sonundaki deneme kendiliğinden bağlar. Daha önce
bağlanmış bir FET'e sonradan gelen bir tüp de tutuyorsa bağ çözülmez, rapor
"Bağlı ama artık kesin değil" diye iki tüpü yazar -- elle bakılır.

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
    # Yazım hatası da (v6.167): "OOSİT CRTYO" (ağustos 2025), "OOSİT CRRYO"
    # (mart 2024) IVF/ICSI sayılıyordu -- ICSI'siz, yalnızca yumurta
    # donduran tedavi IVF/ICSI ekranlarıyla açıldı, tüpleri "embriyo" dedi.
    # C/K + R + en çok iki harf + YO; 30 farklı protokol adında başka hiçbiri
    # tutmuyor (ölçüldü).
    if "CRYO" in p or "KRIYO" in p or re.search(r"\b[CK]R\w{0,2}YO\b", p):
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
#
# Aynı dosyada **atlanacak kayıt** da (v6.167): aynı hastanın aynı günkü iki
# farklı kaydından hangisinin doğru olduğunu kullanıcı söylüyor, öteki
# aktarılmıyor (`ikizleri_ayikla()`):
#
#     MAYIS2024#13    ATLA
#
# ve yazım hatalı ICSI sayısı (v6.167; mayıs 2024'te 13 yumurtanın satırında
# İŞLEME ALINAN "94"):
#
#     MAYIS2024#30    ICSI      94           9
#
# ve yer tutucu yazılmış dosya numarası (v6.170; haziran 2023'te bir FET'in
# DOSYA NO'su "41", kaydın kendi sıra numarası). Doğru numarayı kullanıcı
# söylüyor -- araç hastayı adından ya da doğum tarihinden eşleştirmiyor
# (v6.125'in kuralı), yanlış hasta bu işin en pahalı hatası:
#
#     HAZIRAN2023#41  DOSYA     41           12345678
_DUZELTILEBILIR = {"OPU": "opu", "TRANSFER": "transfer", "ICSI": "islenen",
                   "DOSYA": "dosya_no"}
_SAYI_ALANI = ("ICSI", "DOSYA")


def duzeltmeleri_oku(yol: str) -> list:
    satirlar = []
    with open(yol, encoding="utf-8-sig") as f:
        for no, satir in enumerate(f, start=1):
            satir = satir.split("#", 1)[0] if satir.lstrip().startswith("#") else satir
            parca = satir.split()
            if not parca:
                continue
            if len(parca) == 2 and "#" in parca[0] and parca[1].upper() == "ATLA":
                kaynak, kimlik = parca[0].split("#", 1)
                satirlar.append((_kaynak_ayikla(kaynak) if kaynak else "", kimlik,
                                 "ATLA", None, None))
                continue
            alan = parca[1].upper() if len(parca) > 1 else ""
            sayi = alan in _SAYI_ALANI
            if len(parca) != 4 or "#" not in parca[0] \
                    or alan not in _DUZELTILEBILIR \
                    or not all((p.isdigit() if sayi else _tarih(p) == p)
                               for p in parca[2:]):
                sys.exit(f"{yol}:{no}: anlaşılmadı -- beklenen: "
                         "KAYNAK#KAYIT  OPU|TRANSFER  eski-tarih  yeni-tarih\n"
                         "ya da: KAYNAK#KAYIT  ICSI  eski-sayi  yeni-sayi\n"
                         "ya da: KAYNAK#KAYIT  DOSYA  eski-no  yeni-no\n"
                         "ya da: KAYNAK#KAYIT  ATLA")
            kaynak, kimlik = parca[0].split("#", 1)
            eski, yeni = ((int(parca[2]), int(parca[3])) if sayi
                          else (parca[2], parca[3]))
            satirlar.append((_kaynak_ayikla(kaynak) if kaynak else "", kimlik,
                             alan, eski, yeni))
    return satirlar


def duzeltmeleri_uygula(satirlar, duzeltmeler, kaynak) -> list:
    """Bu dosyanın (`kaynak`) düzeltmelerini uygular. Döner: uygulanamayanlar.
    ATLA satırları burada değil, `atla_satirlarini_ayikla()`'da."""
    kimlige = {r["kimlik"]: r for r in satirlar}
    tutmayan = []
    for k, kimlik, alan, eski, yeni in duzeltmeler:
        if k != kaynak or alan == "ATLA":
            continue
        r = kimlige.get(kimlik)
        anahtar = _DUZELTILEBILIR[alan]
        if not r or r[anahtar] != eski:
            tutmayan.append(f"{k}#{kimlik} {alan} {eski}")
            continue
        r[anahtar] = yeni
        if alan not in _SAYI_ALANI:
            r["tarih"] = r["opu"] or r["transfer"]
        r["duzeltme"].append((alan, eski, yeni))
    return tutmayan


def atla_satirlarini_ayikla(satirlar, duzeltmeler, kaynak) -> tuple:
    """Düzeltme dosyasında ATLA yazan satırlar aktarılmaz (v6.167).
    Döner: (atlananlar, bulunamayan ATLA satırları)."""
    istenen = {kimlik for k, kimlik, alan, _e, _y in duzeltmeler
               if k == kaynak and alan == "ATLA"}
    atlanan = [r for r in satirlar if r["kimlik"] in istenen]
    for r in atlanan:
        satirlar.remove(r)
    bulunan = {r["kimlik"] for r in atlanan}
    return atlanan, [f"{kaynak}#{k} ATLA" for k in sorted(istenen - bulunan)]


# İki satırı karşılaştırırken bakılmayan alanlar: Access kayıt numarası,
# ad (hasta kartına gidiyor, tedaviye değil; eşleşme dosya numarasıyla) ve
# araçların satıra sonradan eklediği türetilmiş işaretler.
_IKIZ_DISI = ("kimlik", "duzeltme", "tarih_yaklasik", "ad_soyad", "es_adi",
              "olgunluk_duzeltme", "icsi_duzeltme", "icsi_hatali", "tip_duzeltme",
              "yumurta_fazla")
_ALAN_ADI = {"toplanan": "toplanan", "mii": "MII", "immatur": "immatür",
             "empty_zona": "empty zona", "dejenere": "dejenere",
             "atretik": "atretik", "islenen": "ICSI", "iki_pn": "2PN",
             "notlar": "not", "gizli_not": "gizli not", "bazal": "sperm",
             "hazirlik": "sperm", "hazirlama": "sperm", "sperm_kaynak": "sperm",
             "dondurulan": "dondurulan", "transfer_adet": "transfer",
             "cozulen": "çözülen", "emb1": "embriyo 1", "emb2": "embriyo 2"}


def _ikiz_farki(x, y) -> list:
    """İki satırın farklı alanları. Notta boşluk, noktalama ve büyük/küçük
    harf farkı sayılmıyor ("İPTAL EDİLDİ." / "İPTAL.")."""
    fark = []
    for k in x:
        if k in _IKIZ_DISI:
            continue
        a, b = x.get(k), y.get(k)
        if k in ("notlar", "gizli_not"):
            a, b = (re.sub(r"[\s.,;:]+", " ", _sade(v or "")).strip() for v in (a, b))
        if a != b:
            fark.append(k)
    return fark


def ikizleri_ayikla(satirlar) -> list:
    """Aynı hastanın aynı günkü, aynı tipteki iki DOLU kaydı (v6.167).

    Mayıs 2024'te bir hastanın aynı OPU'su iki kez girilmiş: toplanan ve MII
    aynı, immatür/empty zona ve sperm sayıları farklı. İkisi de aktarılsaydı
    hastanın kartında aynı gün iki tedavi açılır, aynı 16 yumurta iki kez
    dondurulmuş görünürdü (Cryo Haritası'nda sekiz tüp). Daha önceki üç ayda
    da (haziran, temmuz, aralık 2025) birer çift böyle aktarıldı -- hepsi
    iptal edilmiş tedaviler, yalnızca notun yazımı farklıydı.
    - **Birebir aynıysa** (`_ikiz_farki()` boş) ilki aktarılıyor, öteki
      atlanıyor ve söyleniyor.
    - **Farklıysa** hangisinin doğru olduğu bilinemez, ikisi de atlanıyor:
      kullanıcı doğru olmayanı düzeltme dosyasına `KAYNAK#KAYIT ATLA` diye
      yazıp dosyayı yeniden aktarıyor (öteki "zaten aktarılmış" sayılmaz,
      hiç yazılmamıştı). Çiftten biri zaten aktarılmışsa öteki atlanıyor.
    Tarihi yaklaşık olan satır (`tarihleri_tamamla()`) sayılmıyor: günü
    komşusundan, ikiz olduğu söylenemez. Boş kopyalar zaten ayıklandı
    (`bos_kopyalari_ayikla()`).
    Döner: [(satır, çiftin öteki satırları, farklı alanlar, "birebir" |
    "farkli" | "aktarilmis")]; dönen satırlar listeden çıkarılır."""
    gruplar = {}
    for r in satirlar:
        if r["tarih"] and not r["tarih_yaklasik"]:
            gruplar.setdefault((r["dosya_no"], r["tarih"], r["tip"]), []).append(r)
    cikan = []
    for grup in gruplar.values():
        if len(grup) < 2:
            continue
        grup.sort(key=lambda r: int(r["kimlik"] or 0))
        aktarilmis = [r for r in grup if _zaten_var(r["kimlik"])]
        farklar = sorted({k for r in grup[1:] for k in _ikiz_farki(grup[0], r)})
        for r in grup:
            oteki = [o for o in grup if o is not r]
            if r in aktarilmis:
                continue
            if aktarilmis:
                cikan.append((r, aktarilmis, farklar, "aktarilmis"))
            elif not farklar:
                if r is not grup[0]:
                    cikan.append((r, [grup[0]], farklar, "birebir"))
            else:
                cikan.append((r, oteki, farklar, "farkli"))
    for r, *_x in cikan:
        satirlar.remove(r)
    return cikan


def ikiz_satirlari(cikan) -> list:
    """`ikizleri_ayikla()`'nın sonucu için rapor satırları. Farklı çift tek
    satırda: ikisi de atlandı, hangisinin atlanacağını kullanıcı seçiyor."""
    satirlar, gorulen = [], set()
    for r, oteki, farklar, durum in cikan:
        if r["kimlik"] in gorulen:
            continue
        if durum == "birebir":
            satirlar.append(f'#{r["kimlik"]:>3}  ATLANIR — #{oteki[0]["kimlik"]} ile '
                            "birebir aynı kayıt (aynı hasta, aynı gün, aynı tip)")
        elif durum == "aktarilmis":
            satirlar.append(f'#{r["kimlik"]:>3}  ATLANIR — aynı hastanın aynı günkü '
                            f'kaydı #{oteki[0]["kimlik"]} zaten aktarılmış')
        else:
            cift = [r] + oteki
            gorulen.update(o["kimlik"] for o in cift)
            ne = ", ".join(sorted({_ALAN_ADI.get(k, k) for k in farklar}))
            numara = " ve ".join(f'#{o["kimlik"]}' for o in cift)
            satirlar.append(
                f"{numara}  ATLANIR — aynı hastanın aynı günkü İKİ FARKLI kaydı "
                f"(farklı: {ne}). Hangisi doğruysa ÖTEKİNİ düzeltme dosyasına "
                "yazıp bu dosyayı yeniden aktar, ör.: "
                f'{KAYNAK}#{cift[-1]["kimlik"]}  ATLA')
    return satirlar


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
# "REFREEZ YAPILARAK" / "REFREEZ YAPILAN" da fiil değil (v6.164, temmuz 2025:
# "1 ADET D5 EMBRİYOSU (1BB) REFREEZ YAPILARAK DONDURULDU"): asıl fiil
# arkasından geliyor, skor ondan ÖNCE. Fiil sayılınca skor arkada aranıyor,
# bulunamıyor ve tüp hiç yazılmıyordu.
# FET'te bunların çoğu stok cümlesi; ayırt eden `_dondurma_coz()`'ün
# "fazla" kuralı (çözülen − transfer edilen).
_DONDURMA_FIILI = re.compile(
    r"DONDUR\w*\s+(?:SAKLAN|KORUN)\w*|DONDURULDU\b|DONDURULMUSTUR\b"
    r"|REFREEZ\w*\s+EDIL(?!EN\b)\w*|REFREEZ\w*\s+YAPILDI\b"
    r"|(?P<sonra>REFREEZ\w*\s+EDILEN\b"
    r"|(?<!\()REFREEZE?\b(?!\s*\))"
    r"(?!\s+(?:EDIL|YAPILA?MA|YAPILMA|YAPILAN\b|YAPILARAK\b)))"
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
#   BB, BİRLEŞME G1       -> birleşme (v6.157; kullanıcı: "BB birleşme
#                            başlangıcı demek"): hücre sayısı yok, grade
#                            yazılıysa o. v6.148-v6.156 arası skorsuz
#                            embriyo diye yazılıyordu, goc_048 düzeltiyor
_OOSIT_GRUBU = re.compile(r"^(\d+)\s*\*?\s*M\s*(2|II|1|I)$")
_TEK_OOSIT = re.compile(r"^M\s*(2|II|1|I)$")        # "(M2)" -- yalnız yumurta notunda
# Yumurta yazımının iki yazım hatası (v6.164, haziran/ekim 2025): "1*1"
# ("M" düşmüş, 1 MI) ve "1M*1" (yıldız yer değiştirmiş, 1 MI). Yalnız yumurta
# notunda; tanınmayınca o yumurta tüpe hiç yazılmıyordu, uyarısız.
_OOSIT_YAZIM_HATASI = re.compile(r"^(\d+)\s*(?:\*|M\s*\*)\s*(2|II|1|I)$")
_CLEAVAGE = re.compile(r"^(\d+)\s*(?:H\s*G?|G)\s*([1-4])")
_BLAST = re.compile(r"^([1-6])\s*([ABC])\s*([ABC])")
_BLAST_DISI = re.compile(r"^(KAV|EM|ARR|MOR|M)\s*G?\s*([1-3])?(?![A-Z0-9])")
# "BBG1" / "BB G2" (v6.165, kasım 2025, ocak 2024): BB'nin grade'li yazımı;
# "BİRG1" (mart 2024): BİRLEŞME'nin kısaltması. İkisi de tanınmıyordu, o
# embriyo tüpe hiç yazılmıyordu (uyarıyla). "BİR" tek başına değil, yalnızca
# grade'iyle: Türkçede "bir" sayı da.
_YUVA = re.compile(r"^(?:BB\s*G?\s*([1-4])?|BIR\s*G\s*([1-4])"
                   r"|BIRLESME(?:\s*BASLANGICI)?\s*G?\s*([1-4])|BIRLESME\w*)$")
# `app.BLAST_KISA`'nın tersi -- oradaki kısaltmalar kâğıda da böyle yazılıyor.
_KISALTMA = {"KAV": "kavitasyon", "M": "morula", "MOR": "morula",
             "EM": "erken_morula", "ARR": "arrest"}


def _skor_metni(parca: str) -> str:
    """Skor yazısının katlanmış hali; kısaltmalar ve bilinen yazım hataları
    (v6.168): "KAVVİTASYONG3" (V iki kez, ocak 2023) ve "KACG1" (klavyede C,
    V'nin yanında; kasım 2024, ocak 2025). "KAC" yalnızca arkasından derece
    geliyorsa KAV sayılıyor."""
    t = re.sub(r"KAV+ITASYON", "KAV", _sade(parca)).replace("MORULA", "MOR")
    return re.sub(r"^KAC(?=\s*G?\s*[1-3](?![A-Z0-9]))", "KAV", t)


def _skor_coz(parca: str, yumurta: bool = False):
    """Tek bir skor yazısını programın alanlarına çevirir. Tanımazsa None.

    `yumurta`: not bir yumurta dondurmasını anlatıyor. Orada "M2" MII yumurta,
    embriyo notunda "M2" morula derece 2 -- aynı yazı iki anlama geliyor,
    bağlam karar veriyor (v6.148).
    """
    t = _skor_metni(parca)
    if not t:
        return None
    m = (_OOSIT_GRUBU.match(t)
         or (_TEK_OOSIT.match(t) or _OOSIT_YAZIM_HATASI.match(t) if yumurta else None))
    if m:
        adet = int(m.group(1)) if m.re is not _TEK_OOSIT else 1
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
    """Hücre sayısı olmayan embriyo yazımı: "BB" / "BİRLEŞME G1" -- birleşme
    başlangıcı (v6.157, kullanıcının cevabı). Grade yazılıysa `skor`."""
    m = _YUVA.match(_sade(parca))
    if m:
        grade = next((g for g in m.groups() if g), None)
        return {"tur": "embriyo", "birlesme": True, "ham": parca.strip(),
                "skor": f"G{grade}" if grade else None}
    return None


def _bitisik_ayir(parca: str):
    """Ayırıcısız yazılmış birden çok embriyo skoru (v6.165): "10HG28HG2"
    ("10HG2" + "8HG2", ocak 2024), "8HG2 8HG2 8HG2 6HG3" (şubat 2026).

    `_skor_coz()` baştaki skoru tanıyıp arkasına bakmıyor; bu yazımlarda
    arkadaki embriyolar tüpe hiç yazılmıyordu, uyarısız -- şubat 2026'nın bir
    tüpüne 4 yerine 1 embriyo girdi. Arkası rakamla başlıyor ve kendisi de
    skor olarak okunuyorsa ayrı embriyo. Değilse None, eski okuma kalıyor:
    "8HG1BB", "4BA TA", "10HG1OVAL" -- arkası bir niteleme, embriyo değil.
    Yalnızca embriyo notunda.
    """
    t = _skor_metni(parca)
    m = _CLEAVAGE.match(t) or _BLAST.match(t)
    if not m:
        return None
    kalan = t[m.end():].strip()
    if not re.match(r"\d", kalan):
        return None
    ilk = _skor_coz(t[:m.end()])
    devam = _bitisik_ayir(kalan) or (
        [_skor_coz(kalan)] if _skor_coz(kalan) else None)
    return [ilk] + devam if ilk and devam else None


def _grup_coz(grup: str, yumurta: bool) -> list:
    """Bir parantez grubunun öğeleri. "-" öğeleri ayırıyor; bazı notlarda
    boşluk ayırıyor ("(3M2 1M1)", "(BB 10HG3 8HG3 8HG2)") -- o zaman boşlukla
    ayrılan her parça tek tek tanınmalı, yoksa parça tek öğe sayılıyor ("4BB
    HATCHED" bir blastokist). Parçanın içinde "(" kalmışsa (kaynaktaki
    "((4CB-1BB)" ya da "D3 (EMBRİYOSU (8HG1-10HG2)" gibi yazım hataları)
    sonuncusundan sonrası alınıyor."""
    ogeler = []
    parcalar = [p.split("(")[-1].strip() for p in grup.split("-")]
    parcalar = [p for p in parcalar if p]
    if yumurta:
        # "(4-M2)": sayı ile olgunluk tireyle ayrılmış (v6.164, ekim 2025) --
        # "4*M2". Ayrı okununca "4" tanınmıyor, tüpe 4 yerine 1 yumurta
        # yazılıyordu.
        birlesik = []
        for p in parcalar:
            if (birlesik and re.fullmatch(r"\d+", birlesik[-1])
                    and _TEK_OOSIT.match(_sade(p))):
                birlesik[-1] = f"{birlesik[-1]}*{p}"
            else:
                birlesik.append(p)
        parcalar = birlesik
    for parca in parcalar:
        bitisik = None if yumurta else _bitisik_ayir(parca)
        if bitisik:
            ogeler.extend(bitisik)
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
        if not coz and not yumurta and re.match(r"\d", parca):
            # Rakamla başlayan ama okunamayan embriyo yazımı (v6.164, eylül
            # 2025: "(8HGT1-6HG3-8HG3)"). Embriyo o tüpte; atılırsa tüpe bir
            # eksik yazılıyordu, sessizce. Skor uydurulmuyor: skorsuz embriyo,
            # yazımı değerlendirmenin notunda -- ekrandan düzeltilebilir.
            coz = {"tur": "embriyo", "ham": parca, "okunamadi": True}
        ogeler.append(coz or {"tur": "taninmadi", "ham": parca})
    return ogeler


def _gun_bul(metin: str):
    """"D5", "D 3", "5.GÜN", "3. GÜN", "5,GÜN" -> 5 / 3. Metin `_KATLA`'lı."""
    m = (re.search(r"\bD\s*([1-7])\b", metin)
         or re.search(r"\b([1-7])\s*[.,]?\s*GUN", metin))
    return int(m.group(1)) if m else None


def _son_gun(metin: str):
    """Metindeki SON gün işareti: "KÜLTÜRE EDİLEN D3 EMBRİYOLARI ... D5
    EMBRİYOSU OLARAK (4CB)" -> 5. `_gun_bul()` ilkini buluyor; bir parantez
    grubunun günü ona en yakın, yani önündeki son işaret (v6.164)."""
    son = None
    for m in re.finditer(r"\bD\s*([1-7])\b|\b([1-7])\s*[.,]?\s*GUN", metin):
        son = int(m.group(1) or m.group(2))
    return son


def _tek_tup(cumle: str) -> bool:
    """Cümle tüp sayısını 1 diye yazıyor mu: "1 TÜPTE", "1TÜPTE", "TEK TÜPTE".
    Metin `_KATLA`'lı."""
    return bool(re.search(r"(?<!\d)1\s*TUPTE|\bTEK\s+TUPTE", cumle))


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
    # "1 TÜPTE84*M2)" (v6.165, mart 2024, üç satır): "(" yerine shift'siz
    # "8" basılmış -- Türkçe klavyede "(" Shift+8. Grup açılmadığı için o
    # tüpün yumurtaları hiç yazılmıyordu. Yalnızca "TÜPTE"den hemen sonra,
    # ardından rakam ve "(" açmadan kapanan ")" geliyorsa.
    for mm in re.finditer(r"TUPTE8(?=\d[^()]*\))", hizali):
        i = mm.end() - 1
        ham, hizali = ham[:i] + "(" + ham[i + 1:], hizali[:i] + "(" + hizali[i + 1:]
    m = _DONDURMA_FIILI.search(hizali)
    if not m:
        return {}

    def _cumle_bas(fiil):
        bas_ = 0
        for b_ in re.finditer(r"(?<!\d)\.\s*(?=\S)", hizali[:fiil.start()]):
            bas_ = b_.end()
        return bas_

    # İlk dondurma cümlesinde tüp yoksa ve sonraki bir dondurma cümlesinde
    # varsa o (v6.168, ocak 2023): "ÇÖZÜLEN 3 ADET OOSİTTEN 2 TANE M2 OOSİT
    # REFREEZE YAPILDI. OPUDA TOPLANAN 2 ADET M2 OOSİTLE BİRLİKTE TOPLAM 1
    # TÜPTE(4*M2) ... DONDURULARAK SAKLANDI." İlk cümle tüpü söylemiyor, araç
    # "okunamadı" deyip tüpü hiç yazmıyordu. İlk cümlede parantez varsa ya da
    # hiçbirinde yoksa eski okuma.
    for aday in _DONDURMA_FIILI.finditer(hizali):
        son_ = re.search(r"(?<!\d)\.(?!\d)", hizali[aday.end():])
        son_ = aday.end() + son_.start() if son_ else len(hizali)
        if "(" in hizali[_cumle_bas(aday):son_]:
            m = aday
            break
    bas = _cumle_bas(m)
    son = re.search(r"(?<!\d)\.(?!\d)", hizali[m.end():])
    son = m.end() + son.start() if son else len(hizali)
    tum = re.sub(r"\s+", " ", hizali[bas:son])        # fiilin bütün cümlesi

    fet = tip in FET_TIPLERI and not _db.cozulen_yumurta_islenir(tip)
    if fet:
        if fazla is not None and fazla <= 0:
            return {}
        # "GERİYE 1 ADET REFREEZ YAPILAN D5 EMBRİYOSU (KAVG2) ŞEKLİNDE
        # DONDURULDU" stok değil (v6.164, ağustos 2025): cümle REFREEZ diyor
        # ve fiili bitmiş ("DONDURULDU", "SAKLANDI", "EDİLDİ") -- bu tedavide
        # çözülüp transfer edilmeyen embriyo yeniden donduruldu, DONDURULAN
        # alanı boş bırakılmış. Stok cümlesi "SAKLANMIŞTIR" / "KALDI" der.
        yeniden = ("REFREEZ" in tum
                   and re.search(r"DONDURULDU\b|SAKLANDI\b|EDILDI\b", m.group(0)))
        if ("GERIDE" in tum or "GERIYE" in tum) and not dondurulan and not yeniden:
            return {}

    if m.group("sonra") or m.group("ortuk"):
        # Nesne fiilden sonra: "İLE BİRLİKTE" / "KALDI" / cümle sonuna kadar.
        # "İLE TOPLAM 6 TÜPTE 20 ADET EMBRİYOSU KALDI" (v6.165) aynı kuruluş:
        # arkası hastanın bütün stoku -- 20 dondurulan sayısı sanılmamalı.
        dur = re.search(r"\bILE\s+(?:BIR|TOPLAM)|\bKALDI", hizali[m.end():son])
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
    # Grubun günü (v6.164): tek not iki ayrı gün dondurabiliyor -- "2 ADET D3
    # EMBRİYOSU (8HG3-10HG2) 2 ADET D5 EMBRİYOSU (3CC-1CC) ŞEKLİNDE
    # DONDURULARAK SAKLANDI". Her grubun günü önündeki son işaret; işareti
    # olmayan grup bir öncekinin gününde ("2 ADET D5 EMBRİYOSU (1CC) (1BC)").
    def _tam_okunan(metin):
        """Metin bütün öğeleri tanınan bir grupsa öğeleri, değilse None."""
        g = _grup_coz(metin, baglam)
        return g if g and all(o["tur"] != "taninmadi" and not o.get("okunamadi")
                              for o in g) else None

    gruplar, grup_gunleri = [], []
    onceki, son_isaret = 0, None
    # Her ")" bir grubu kapatıyor; grup, önceki ")"den sonraki ilk "(" ile
    # başlıyor (v6.164'e kadarki `\(([^)]*)\)` ile aynı gruplar). v6.165:
    # parantezi eksik iki yazım da okunuyor -- aşağıda.
    for sm in re.finditer(r"[^)]*\)", cumle_hizali):
        parca = cumle_hizali[sm.start():sm.end() - 1]
        if "(" in parca:
            ac = sm.start() + parca.index("(")
            metin = ham_cumle[ac + 1:sm.end() - 1]
        else:
            # Açılmamış grup (aralık 2025): "(4AA-4AA) 4AA-3AA) (1AA-3BC)",
            # "24 ADET D3 EMBRİYOSU 5HG2-8HG1-6HG2-8HG1) (...". ")"den hemen
            # önce tireyle bağlı skorlar -- bütün öğeleri tanınıyorsa bir
            # tüp; tanınmıyorsa eskisi gibi alınmıyor.
            y = re.search(r"[0-9A-Z*]+(?:\s*-\s*[0-9A-Z*]+)*\s*$", parca)
            if not y or not _tam_okunan(ham_cumle[sm.start() + y.start():sm.end() - 1]):
                continue
            ac = sm.start() + y.start()
            metin = ham_cumle[ac:sm.end() - 1]
        son_isaret = _son_gun(cumle_hizali[onceki:ac]) or son_isaret
        onceki = sm.end()
        # Kapanmamış grup (kasım 2025): "(3AB) (3BB (3BC) (3BA)" -- "3BB" ayrı
        # bir tüp, ")"si unutulmuş. Önceki parça boşsa ("((4CB-1BB)"), skor
        # değilse ("D3 (EMBRİYOSU (8HG1-10HG2)") ya da tireyle bitiyorsa
        # (aynı grubun devamı) `_grup_coz()` eskisi gibi son "("den sonrasını
        # alıyor.
        parcalar = metin.split("(")
        kes = 0
        while kes < len(parcalar) - 1:
            onu = parcalar[kes]
            g = (_tam_okunan(onu) if onu.strip() and not onu.rstrip().endswith("-")
                 else None)
            if not g:
                break
            gruplar.append(g)
            grup_gunleri.append(son_isaret)
            kes += 1
        metin = "(".join(parcalar[kes:])
        if re.fullmatch(r"REFREEZ\w*", _sade(metin)):
            continue                    # "(REFREEZE)" etiket, tüp değil
        if re.search(r"VIABIL|^\s*%\s*\d", _sade(metin)):
            continue                    # "(%80 VİABİLİTE)" çözmenin notu (v6.168)
        if (baglam and _TEK_OOSIT.match(_sade(metin))
                and cumle_hizali[:ac].rstrip().endswith("ADET")):
            continue
        g = _grup_coz(metin, baglam)
        if g:
            gruplar.append(g)
            grup_gunleri.append(son_isaret)
    adet = _ilk(r"(\d+)\s*ADET")
    # Aynı tüp iki kez yazılmış (v6.164, ekim 2025: "19 ADET D3 EMBRİYOSU"
    # ve DONDURULAN 19, ama beş grup 24 embriyo tutuyor; ikinci ve dördüncü
    # grup birebir aynı -- kopyala-yapıştır). İki bağımsız sayı (notun ADET'i
    # ve DONDURULAN alanı) tekrarı çıkarınca tam tutuyorsa tekrar düşüyor;
    # yoksa tankta olmayan bir tüp yazılırdı. Aynı içerikli iki tüp olağan
    # ("(4AA) (4AA)"): sayılar tutuyorsa hiçbir şey değişmiyor. Yalnızca
    # embriyoda -- yumurta satırlarında DONDURULAN embriyo sayısı, ikinci
    # sayı yok.
    tekrar_grup = None
    if (gruplar and not baglam and adet and dondurulan == adet
            and sum(len(g) for g in gruplar) > adet):
        yazim = ["-".join(o["ham"] for o in g) for g in gruplar]
        for j in range(1, len(gruplar)):
            if (yazim[j] in yazim[:j]
                    and sum(len(g) for g in gruplar) - len(gruplar[j]) == adet):
                tekrar_grup = yazim[j]
                del gruplar[j], grup_gunleri[j]
                break
    ogeler = [o for g in gruplar for o in g]      # düz liste
    farkli_gun = not baglam and len({g for g in grup_gunleri if g}) > 1
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
    elif (not gruplar and adet and adet > 1
          and (_tek_tup(cumle) or (baglam and _ilk(r"(\d+)\s*TUPTE") is None))
          and not (re.search(r"\bM\s*(1|I)\b", cumle)
                   and re.search(r"\bM\s*(2|II)\b", cumle))):
        # Parantezsiz ama tüp sayısı 1 (v6.160): "5 ADET M2 OOSİT 1 TÜPTE
        # DONDURULARAK SAKLANDI" -- dağılım bilinmiyor değil, hepsi o tüpte.
        # Yumurtada tüp sayısı HİÇ yazmıyorsa da tek tüp (v6.161,
        # kullanıcının cevabı: "2 ADET M2 OOSİT DONDURULARAK SAKLANDI tek
        # tüptür"). Embriyoda bu varsayılmıyor; "2 TÜPTE 4 ADET" gibi birden
        # çok tüpün dağılımı da hâlâ bilinmiyor.
        # Olgunluk karışıksa ("M1" ve "M2" birlikte, sayısı yazmıyor) hangi
        # yumurtanın hangisi olduğu bilinmez, uydurulmuyor (uyarı çıkıyor).
        if baglam:
            tek = [{"tur": "oosit", "adet": adet,
                    "mat": "mi" if re.search(r"\bM\s*(1|I)\b", cumle) else "mii",
                    "ham": ham_cumle.strip()}]
        else:
            tek = [{"tur": "embriyo", "ham": ham_cumle.strip() or "skorsuz"}
                   for _ in range(adet)]
        gruplar, ogeler = [tek], list(tek)
    sayilan =[o for o in ogeler if o["tur"] != "taninmadi"]
    oosit_mi = baglam or (bool(sayilan) and all(o["tur"] == "oosit" for o in sayilan))
    # Kaynağın kendi sayısı tüplerden çoksa (v6.165): "10 ADET D5 EMBRİYOSU
    # (4AA) (4AA) (3AA-2BB) (KAVG1-KAVG1) (KAVG1-KAVG1)" ve DONDURULAN 10,
    # ama tüplerde 8 embriyo. Eksik ikisinin tüpü ve skoru bilinmiyor,
    # uydurulmuyor -- ama tankta duran embriyo programda görünmeyecek, bu
    # SÖYLENMELİ (v6.142'nin kuralı). Tanınmayan öğe sayılmış sayılıyor: onu
    # ayrı uyarı söylüyor. Embriyoda iki sayının büyüğü (günü karışık notta
    # ADET yalnızca ilk günün sayısı); yumurtada yalnızca notun ADET'i --
    # DONDURULAN kolonu embriyo sayısı.
    okunan = sum(o.get("adet", 1) if o["tur"] == "oosit" else 1 for o in ogeler)
    # Embriyoda önce DONDURULAN (v6.167; v6.165'te iki sayının büyüğüydü):
    # yapılandırılmış alan serbest metinden önce gelir (v6.142). Haziran
    # 2024'te not "16 ADET D3 EMBRİYOSU" diyor, DONDURULAN 15 ve dört tüpte
    # 15 embriyo -- büyüğü almak tutan bir tüpe "1 embriyo eksik" dedirtiyordu.
    # Günü karışık notta ADET ilk günün sayısı, DONDURULAN hepsi: yine doğru.
    beklenen = (adet or 0) if oosit_mi else (dondurulan or adet or 0)
    # Grup grup tür (v6.167, haziran 2024): bir Yumurta Dondurma notu "1 ADET
    # 5,GÜN EMBRİYOSU 1 TÜPTE(1CB) GERİYE KALAN 16 ADET OOSİT 1 TÜPTE(6*M2)
    # ..." -- beş yumurtaya ICSI yapılmış, blastokisti ayrı tüpte. Not bütün
    # olarak yumurta sayılıyordu; blastokistin tüpü yumurta aranıp
    # bulunmadığı için SESSİZCE yazılmıyordu. Grup, öğeleri yumurtaysa
    # yumurta, embriyo yazımıysa (blastokist, cleavage, "BB") embriyo; hiçbiri
    # tanınmıyorsa notun türünde.
    embriyo_turleri = ("blast", "cleavage", "embriyo")
    grup_yumurta = []
    for g in gruplar:
        yum = any(o["tur"] == "oosit" for o in g)
        emb = any(o["tur"] in embriyo_turleri for o in g)
        grup_yumurta.append(oosit_mi if yum == emb else yum)
    return {
        "gun": gun,
        # Gruplar farklı günlerde dondurulduysa grup grup gün (işaretsiz
        # grup notun gününde); öyle değilse None -- herkes `gun`'u kullanır.
        "grup_gunleri": ([g or gun for g in grup_gunleri]
                         if farkli_gun and len(grup_gunleri) == len(gruplar) else None),
        "oosit_mi": oosit_mi,
        # Grup grup yumurta mı (yukarıya bak); notun türü `oosit_mi`
        "grup_yumurta": grup_yumurta,
        "karisik": len(set(grup_yumurta)) > 1,
        "adet": adet,
        # Kaynağın sayısına göre tüplerde eksik kalan örnek (yukarıya bak)
        "eksik_not": (beklenen - okunan) if gruplar and beklenen > okunan else 0,
        "beklenen": beklenen,
        "tup": _ilk(r"(\d+)\s*TUPTE"),
        "gruplar": gruplar,
        "ogeler": ogeler,
        # Fiilsiz dondurma: `liste` ve rapor bunu ayrıca söylüyor
        "ortuk": bool(m.group("ortuk")),
        "tekrar_grup": tekrar_grup,
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


def olgunlugu_nottan_duzelt(satirlar) -> None:
    """Dondurma notu MII/immatür sayısıyla çelişiyorsa not kazanır (v6.161;
    ters yönü -- not M1 donduruyor, kutu MII diyor -- v6.168).

    Kullanıcının cevabı: iki satırda MII/İMMATÜR kutuları notla tutmuyordu
    (MII 4 / immatür 3, not 6 M2 + 1 M1 donduruyor; MII 3, not "(3*M2-2M2)"),
    "bunlar yanlış yazılmıştır, en son yazılanı kullan" -- en son yazılan
    dondurma notu. Fark immatürden MII'ye geçiyor, toplam değişmiyor;
    immatür yetmezse kalan eksik kalıyor ve dondurma uyarısı çıkıyor
    (uydurulacak yumurta yok). Yalnızca yumurtanın bu tedavide toplandığı
    tipler: FET/Yumurta Çözme'de dondurulan yumurta başka tedavinin.
    Not "MII Access'te N yazıyordu" diyor (`_not_kur()`)."""
    for r in satirlar:
        r["olgunluk_duzeltme"] = None
        if r["tip"] in FET_TIPLERI:
            continue
        coz = _satir_dondurmasi(r)
        if not coz or not coz.get("oosit_mi"):
            continue
        oositler = [o for o in coz["ogeler"] if o["tur"] == "oosit"]
        m2 = sum(o["adet"] for o in oositler if o["mat"] == "mii")
        m1 = sum(o["adet"] for o in oositler if o["mat"] != "mii")
        once = (r["mii"], r["immatur"])
        fark = min(m2 - r["mii"], r["immatur"])
        if fark > 0:
            r["mii"] += fark
            r["immatur"] -= fark
        # Ters yönü (v6.168): kasım 2024'te MII 1, immatür 0, not "(1*M1)"
        # donduruyor. Aynı kural -- not kazanır, fark MII'den immatüre.
        fark = min(m1 - r["immatur"], r["mii"] - m2)
        if fark > 0:
            r["mii"] -= fark
            r["immatur"] += fark
        if (r["mii"], r["immatur"]) != once:
            r["olgunluk_duzeltme"] = once


def _yumurta_sayisi(r, icsi=True) -> int:
    """Açılacak yumurta kaydı: TOPLANAN, olgunluk sayılarının toplamı (MII +
    immatür + empty zona + dejenere + atretik) ve ICSI sayısının en büyüğü.

    Yumurta Çözme'de v6.148'den beri böyle (çözülen sayı kimi satırda
    yalnızca MII ya da İŞLEME ALINAN kutusunda). v6.167'den beri OPU'lu
    tiplerde de: mayıs 2024'te bir Yumurta Dondurma satırında TOPLANAN boş,
    MII 1 ve not o yumurtayı donduruyor -- kayıt açılmadığı için dondurma
    yazılamıyordu; ağustos 2024'te TOPLANAN 6, olgunluk sayıları 7 (bir
    dejenere düşüyordu). "Toplanan" kutusu (OPU'nun kendi sayısı, v6.112)
    Access'teki değeri tutmaya devam ediyor. `icsi=False`: ICSI sayısını
    sınamak için (`icsi_sayisini_tamamla()`), onu katmadan."""
    return max(r["toplanan"] or 0,
               r["mii"] + r["immatur"] + r["empty_zona"] + r["dejenere"]
               + r["atretik"], (r["islenen"] or 0) if icsi else 0)


def yumurta_sayisini_isaretle(satirlar) -> None:
    """Açılacak yumurta TOPLANAN'dan fazlaysa (`_yumurta_sayisi()`) not
    söylesin: `r["yumurta_fazla"]` (v6.167). Yalnızca OPU'lu tipler --
    Yumurta Çözme'de sayı v6.148'den beri böyle ve TOPLANAN orada çözülen
    sayı, OPU sayısı değil."""
    for r in satirlar:
        n = _yumurta_sayisi(r)
        r["yumurta_fazla"] = (n if r["tip"] not in FET_TIPLERI
                              and n > (r["toplanan"] or 0) else None)


def icsi_sayisini_tamamla(satirlar) -> None:
    """ICSI sayısı boş ama döllenme sonuçları dolu: sayı sonuçlardan (v6.164).

    Temmuz 2025'te bir satır: yöntem "ICSI", MII 8, 2PN 7, intakt 1, İŞLEME
    ALINAN boş. Araç ICSI'yi hiç yazmıyordu, 2PN'ler de ICSI'den türediği
    için hiç embriyo açılmıyor ve dondurulan 6 embriyonun 4 tüpü Cryo
    Haritası'na girmiyordu. 2PN, intakt, anormal ve işlem sonrası dejenere
    enjeksiyonun SONUÇLARI -- toplamları enjekte edilen yumurta sayısının
    kendisi, uydurma değil (v6.148'in "ICSI toplamı tutmuyorsa 2PN
    korunuyor" kuralının boş hali). Döllenme sonucu da yoksa ICSI yine
    yazılmıyor. Yalnızca ICSI aşaması olan tiplerde; not "Access'te boş"
    diyor (`_not_kur()`)."""
    for r in satirlar:
        r["icsi_duzeltme"] = None
        r["icsi_hatali"] = None
        if "icsi" not in _db.TIP_ASAMALARI.get(r["tip"], ()):
            continue
        # Yumurtadan fazla ICSI yazım hatası (v6.167, mayıs 2024: 13 yumurta,
        # 9 MII, İŞLEME ALINAN 94). Araç sayıyı yumurta sayısına kısıyor ve
        # empty zona yumurtalara da ICSI yazıyordu. Sayı boş sayılıyor (aşağıdaki
        # kural), Access'teki değer notta; doğrusu biliniyorsa düzeltme
        # dosyasına `KAYNAK#KAYIT ICSI eski yeni`. Yumurta Çözme'de değil:
        # orada çözülen yumurta sayısı çoğu zaman yalnızca bu kutuda.
        if (r["islenen"] and r["tip"] not in FET_TIPLERI
                and r["islenen"] > _yumurta_sayisi(r, icsi=False)):
            r["icsi_hatali"], r["islenen"] = r["islenen"], 0
        if r["islenen"]:
            continue
        sonuc = ((r["iki_pn"] or 0) + (r["intakt"] or 0) + (r["anormal_fert"] or 0)
                 + (r["islem_dejenere"] or 0))
        if sonuc:
            r["islenen"] = sonuc
            r["icsi_duzeltme"] = sonuc


def tipi_veriden_duzelt(satirlar) -> None:
    """IVF/ICSI sayılan satır ICSI'siz ve yalnızca yumurta donduruyorsa
    Yumurta Dondurma (v6.167). `r["tip_duzeltme"]`: eski tip, raporda.

    Protokol adı yalnızca ilaç olabiliyor ("GONAPEPTLY"): üç satırda ICSI,
    2PN ve transfer yok, not "11 ADET OOSİT ... (3*M2-1M1)" diye yalnızca
    yumurta donduruyor. IVF/ICSI açılınca tedavi ekranı boş ICSI/döllenme
    aşamaları gösteriyor, resmî formun "fertilizasyon yöntemi" kutusu
    "IVF/ICSI" basıyordu. Tip veriden (v6.142'nin dersi: yapılandırılmış veri
    serbest metinden önce): ICSI sayısı (`icsi_sayisini_tamamla()`'dan
    sonra), 2PN, transfer ve DONDURULAN embriyo sayısının hepsi boş, dondurma
    notunun bütün tüpleri yumurta. Kısmi ICSI'li satır (birkaç yumurtaya ICSI,
    kalanı dondurulmuş) IVF/ICSI kalıyor -- tüpleri yine yumurta
    (`db.dondurulan_yumurta_sql()`)."""
    for r in satirlar:
        r["tip_duzeltme"] = None
        if (r["tip"] != "ivf_icsi" or r["islenen"] or r["iki_pn"]
                or r["transfer_adet"] or r["dondurulan"]):
            continue
        coz = _satir_dondurmasi(r)
        if (coz and coz.get("oosit_mi") and coz["ogeler"]
                and all(o["tur"] == "oosit" for o in coz["ogeler"])):
            r["tip_duzeltme"] = r["tip"]
            r["tip"] = "oosit_cryo"


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
        if alan == "DOSYA":
            p.append(f"Dosya numarası Access'te {eski} yazıyordu, {yeni} "
                     "olarak düzeltildi.")
            continue
        if alan in _SAYI_ALANI:
            p.append(f"{alan} sayısı Access'te {eski} yazıyordu, {yeni} olarak "
                     "düzeltildi.")
            continue
        p.append(f"{alan} tarihi Access'te {_gg(eski)} yazıyordu, "
                 f"{_gg(yeni)} olarak düzeltildi.")
    if r.get("olgunluk_duzeltme"):
        mii, imm = r["olgunluk_duzeltme"]
        p.append(f"Access'te MII {mii}, immatür {imm} yazıyordu; dondurma "
                 f"notuna göre MII {r['mii']}, immatür {r['immatur']} alındı.")
    if r.get("icsi_hatali"):
        p.append(f"ICSI sayısı Access'te {r['icsi_hatali']}, yumurta sayısından "
                 "fazla; " + (f"döllenme sonuçlarının toplamı ({r['icsi_duzeltme']}) "
                              "alındı." if r.get("icsi_duzeltme") else "yazılmadı."))
    elif r.get("icsi_duzeltme"):
        p.append(f"ICSI sayısı Access'te boş; döllenme sonuçlarının toplamı "
                 f"({r['icsi_duzeltme']}) alındı.")
    if r.get("yumurta_fazla"):
        p.append(f"Toplanan yumurta Access'te {r['toplanan'] or 0}; olgunluk "
                 f"sayılarının toplamı {r['yumurta_fazla']} -- o kadar yumurta "
                 "kaydı açıldı.")
    coz = _satir_dondurmasi(r)
    if coz.get("tekrar_grup"):
        p.append(f"Dondurma notunda aynı tüp iki kez yazılmış "
                 f"({coz['tekrar_grup']}); {coz['adet']} embriyo, "
                 f"{len(coz['gruplar'])} tüp alındı.")
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


def _grup_zamanlari(r, coz) -> list:
    """Her tüpün (parantez grubunun) (dondurma anı, değerlendirme anı).

    Grubun günü (v6.164, `grup_gunleri`) ve türü (v6.167, `grup_yumurta`):
    yumurta OPU günü, embriyo OPU + gün -- aynı notta ikisi de olabiliyor
    ("1 ADET 5,GÜN EMBRİYOSU (1CB) ... 16 ADET OOSİT (6*M2) ..."). Grubu
    olmayan notta tek bir an, notun gününden ve türünden."""
    n = max(len(coz.get("gruplar") or ()), 1)
    gunler = coz.get("grup_gunleri") or [coz.get("gun")] * n
    turler = coz.get("grup_yumurta")
    if not turler or len(turler) != n:
        turler = [coz.get("oosit_mi")] * n
    return [_dondurma_zamani(r, dict(coz, gun=g, oosit_mi=y))
            for g, y in zip(gunler, turler)]


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
        # Gruplar farklı günlerdeyse (v6.164) ya da notta yumurta ve embriyo
        # tüpü birlikteyse (v6.167) tedavi son dondurmayla biter.
        an = max((t or "" for t, _d in _grup_zamanlari(r, coz)), default="") \
            if coz else _dondurma_zamani(r, {"gun": _asama_gunu(r["dondurma_asama"]),
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
    if r.get("tip_duzeltme"):
        rapor.append(f'    tip: Yumurta Dondurma -- protokol "{r["protokol"]}" ama ICSI, '
                     "2PN ve transfer yok, yalnızca yumurta dondurulmuş")
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
    """Toplanan (ya da çözülen) yumurta kadar kayıt açar -- sayı
    `_yumurta_sayisi()`'nden (v6.167) -- ve sayılara uyan olayları yazar.

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
    n = _yumurta_sayisi(r)
    if cozme:
        gun = _cozme_gunu(r)
    else:
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
            # Birleşme (v6.157): hücre sayısı yok, grade yazılıysa o. Göç
            # (goc_048) yoksa kolon yazılmıyor -- eski davranış, skorsuz.
            alan = {"cl_hucre_sayisi": None, "cl_skor": o.get("skor"),
                    "cl_skor_kaynagi": "elle" if o.get("skor") else None}
            if o.get("birlesme") and _db.kolon_var("olay", "cl_birlesme"):
                alan["cl_birlesme"] = 1
            return "cleavage_degerlendirme", alan
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
    if o[2] is None:
        # Hücre sayısı yok ("BB", birleşme -- grade'i olsa da, v6.157):
        # anahtarı bilinmiyor, her şeyle tutar. v6.148'deki davranış.
        return None, None
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
        # Olgunluğu kaynakta HİÇ sayılmamış yumurta (v6.160): "1 ADET OOSİT
        # DONDURULARAK SAKLANDI", MII/İMMATÜR kutuları boş. Tankta duruyor;
        # olgunluk boş kalıyor, uydurulmuyor. Yalnızca kaynağın sayılarının
        # (MII + immatür + empty zona + dejenere + atretik) ÖTESİNDEKİ
        # yumurtalar: empty zona da maturasyon kaydı olmadan açılıyor
        # (`_oositleri_ac()`), ama içinde yumurta yok -- dondurulamaz.
        sayilan = (r["mii"] + r["immatur"] + r["empty_zona"] + r["dejenere"]
                   + r["atretik"])
        havuz["olcusuz"] = [sid for (sid,) in b.execute(
            "SELECT s.id FROM specimen s WHERE s.cycle_id=? AND s.cycle_sira_no > ? "
            f"AND {transfersiz} AND NOT EXISTS (SELECT 1 FROM olay m "
            "WHERE m.specimen_id=s.id AND m.tip IN ('maturasyon_kontrolu', 'icsi') "
            "AND m.iptal_mi=0) ORDER BY s.cycle_sira_no",
            (cycle_id, sayilan)).fetchall()]
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


def _tupte_yumurta_mi(b, uyeler) -> bool:
    """Var olan tüpte yumurta mı var -- içerikten (v6.167,
    `db.dondurulan_yumurta_sql()`), tüpün ilk dondurma olayından.
    `uyeler`: `_mevcut_tupler()`'in [(örnek, olay), ...] listesi."""
    return b.execute(f"SELECT {_db.dondurulan_yumurta_sql('o')} FROM olay o "
                     "WHERE o.id=?", (uyeler[0][1],)).fetchone()[0] == 1


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


def _dondurma_kayitlari(b, r, cycle_id, kid, rapor, yalnizca_ekle=False):
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

    `yalnizca_ekle` (v6.165, `dondurma` kipi): yalnızca EKSİK olan yazılıyor
    -- notta olup tüpte olmayan yer yeni örnekle tamamlanıyor, eksik tüp
    açılıyor. Tüpte duran örneğe, skoruna ve durumuna hiç dokunulmuyor, notta
    olmayan örnek tüpten çıkmıyor: elle düzeltilmiş bir skor ezilmesin
    (`tamamla`'nın riski, v6.142). Döner: bir şey yazıldı mı.
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
    # Grup grup tür (v6.167): notta yumurta ve embriyo tüpü birlikte olabilir
    # (`_dondurma_coz()`'ün `grup_yumurta`'sı). Tek türlü notta hepsi aynı.
    grup_yumurta = coz.get("grup_yumurta") or [oosit_mi] * len(coz["gruplar"])
    # Grup grup gün (v6.164): "D3 (..) D5 (..)" notunda D5 tüpü OPU + 5'te
    # dondurulmuş, blastokistleri 5. gün değerlendirmesi -- v6.163'e kadar
    # bütün tüpler notun ilk gününe (3) yazılıyordu, blastokist 4. güne.
    grup_gunleri = coz.get("grup_gunleri") or [coz["gun"]] * len(coz["gruplar"])
    zamanlar = _grup_zamanlari(r, coz)
    if not all(t for t, _d in zamanlar):
        rapor.append("    UYARI: tarih yok, dondurma kaydı yazılamadı")
        return
    cycle_no = b.execute("SELECT cycle_no FROM cycle WHERE id=?",
                         (cycle_id,)).fetchone()[0]

    if not baska_tedaviden and not yalnizca_ekle:
        # v6.131'in ilk yazışındaki taşıyıcısız vitrifikasyon olayları iptal
        # ediliyor: istatistikte "donduruldu" derken ekranda "aday"
        # görünüyorlardı. FET'te öyle kayıt hiç yazılmadı.
        for (oid,) in b.execute(
                "SELECT o.id FROM olay o JOIN specimen s ON s.id=o.specimen_id "
                "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
                "AND o.vit_tasiyici_id IS NULL", (cycle_id,)).fetchall():
            _iptal(b, kid, oid, "Tasiyicili kayitla degistirildi")

    gun = coz["gun"] or 5
    havuzlar = {}

    def havuz(yumurta):
        if yumurta not in havuzlar:
            havuzlar[yumurta] = _dondurma_havuzu(b, r, cycle_id, yumurta)
        return havuzlar[yumurta]
    mevcut = _mevcut_tupler(b, cycle_id)
    kullanilan = {sid for *_x, uyeler in mevcut for sid, _o in uyeler}
    # Var olan tüp notun AYNI türdeki grubuyla sırasıyla eşleşiyor (v6.167):
    # karışık notta (bir embriyo tüpü + üç yumurta tüpü) sıra türün içinde.
    # Öğesi hiç tanınmayan grup (yer yok) sıra almıyor: tüpü de açılmamıştı.
    mevcut_tur = {True: [], False: []}
    for m in mevcut:
        mevcut_tur[_tupte_yumurta_mi(b, m[3])].append(m)
    tur_sira = {True: 0, False: 0}
    ek_vit = {"vit_cycle_id": cycle_id} if baska_tedaviden else {}
    if tip in FET_TIPLERI and not _db.cozulen_yumurta_islenir(tip):
        vit_notu = (_db.KAYNAK_DONDURMA_NOTU + " (çözme sonrası "
                    "yeniden dondurma); konum girilmedi.")
    else:
        vit_notu = _db.KAYNAK_DONDURMA_NOTU + "; konum girilmedi."

    yeni_tup, onarilan, yazilan, eksik, yer_sayisi, yedekten = [], [], [], 0, 0, 0
    olcusuzden = 0
    for i, grup in enumerate(coz["gruplar"]):
        g_oosit = grup_yumurta[i]
        yerler = _yerler(grup, g_oosit)
        if not yerler:
            continue
        yer_sayisi += len(yerler)
        sira_t = tur_sira[g_oosit]
        tur_sira[g_oosit] += 1
        tid, etiket, an, uyeler = (mevcut_tur[g_oosit][sira_t]
                                   if sira_t < len(mevcut_tur[g_oosit])
                                   else (None, None, None, []))
        tupteki = [sid for sid, _o in uyeler]
        if g_oosit:
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
        if not g_oosit:
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
            sid = next((s for s in havuz(g_oosit).get(a if g_oosit else None, [])
                        if s not in kullanilan), None)
            if sid is None and not g_oosit:
                sid = next((s for s in havuz(False).get("yedek", [])
                            if s not in kullanilan), None)
                yedekten += bool(sid)
            if sid is None and g_oosit:
                sid = next((s for s in havuz(True).get("olcusuz", [])
                            if s not in kullanilan), None)
                olcusuzden += bool(sid)
            if sid is None:
                eksik += 1
                continue
            atanan[j] = sid
            kullanilan.add(sid)

        eklenen = [s for s in atanan if s and s not in tupteki]
        if yalnizca_ekle:
            bosta = []                  # notta olmayan örnek tüpte kalıyor
        g_vit, g_deg = zamanlar[i]
        if tid is None:
            if not eklenen:
                continue
            an = (_dt.datetime.fromisoformat(g_vit)
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
            if not g_oosit:
                _aktarim_skorunu_iptal(b, kid, sid, cycle_id,
                                       "Kaynak kayittaki dondurma notunda yok")
            _durum_yaz(b, sid, _onceki_durum(b, sid, cycle_id))

        if g_oosit:
            continue
        g_gun = grup_gunleri[i]
        for (a, o), sid in zip(yerler, atanan):
            if not sid or (yalnizca_ekle and sid not in eklenen):
                continue
            yazilan.append(o["ham"])
            alan = _oge_alanlari(o, g_gun)
            if alan:
                deg_tipi, alanlar = alan
                gg = g_gun or gun
                _degerlendirme_yaz(b, kid, sid, cycle_id, deg_tipi,
                                   max(gg, 4) if o["tur"] == "blast" else min(gg, 3),
                                   g_deg, alanlar, o["ham"])
            else:
                # Skorsuz ve değerlendirmesiz yer: bu örneğe daha önce başka
                # bir yazım atanmışsa o skor gidiyor.
                _aktarim_skorunu_iptal(b, kid, sid, cycle_id,
                                       "Skorsuz embriyo (kaynak kayitta skor yok)")

    if yedekten:
        rapor.append(f"    UYARI: kaynakta 2PN sayısı dondurulandan az -- {yedekten} "
                     "embriyo 2PN kaydı olmayan enjekte yumurtaya yazıldı")
    if olcusuzden:
        rapor.append(f"    UYARI: kaynakta olgunluğu yazılmamış {olcusuzden} yumurta "
                     "dondurulmuş yazıldı (olgunluk boş)")
    if eksik:
        rapor.append(f"    UYARI: notta {yer_sayisi} örnek yazıyor ama "
                     f"{yer_sayisi - eksik} uygun kayıt var; fazlası yazılmadı")
    fazla_tup = sum(max(len(mevcut_tur[y]) - tur_sira[y], 0) for y in (True, False))
    if fazla_tup:
        rapor.append(f"    UYARI: programda notta olmayan {fazla_tup} tüp var, "
                     "dokunulmadı")
    # Aynı tüpte yumurta da embriyo da yazılmış (v6.167): tür grubun
    # çoğunluğundan değil, ikisi birden varsa notun türünden -- öteki öğe
    # hiçbir tüpe yazılmıyor, sessiz kalmasın.
    uyusmayan = [o["ham"] for g, y in zip(coz["gruplar"], grup_yumurta) for o in g
                 if o["tur"] != "taninmadi" and (o["tur"] == "oosit") != y]
    if uyusmayan:
        rapor.append("    UYARI: aynı tüpte yumurta ve embriyo yazılmış: "
                     + ", ".join(f"'{h}'" for h in uyusmayan) + " -- yazılmadı")
    # Tanınmayan öğe sessizce düşmesin (v6.164): tüpe eksik yazılıyor demek.
    atilan = [o["ham"] for o in coz["ogeler"] if o["tur"] == "taninmadi"]
    if atilan:
        rapor.append("    UYARI: notta tanınmayan yazım: "
                     + ", ".join(f"'{h}'" for h in atilan) + " -- o örnek yazılmadı")
    if coz.get("eksik_not"):
        rapor.append(f'    UYARI: kaynakta {coz["beklenen"]} '
                     f'{"yumurta" if oosit_mi else "embriyo"} dondurulmuş (notun '
                     f'ADET\'i {coz["adet"] or "-"}'
                     + ("" if oosit_mi else f', DONDURULAN {r["dondurulan"] or "-"}')
                     + f') ama tüplerde {coz["beklenen"] - coz["eksik_not"]} yazıyor '
                     f'-- {coz["eksik_not"]} {"yumurtanın" if oosit_mi else "embriyonun"} '
                     "tüpü bilinmiyor, yazılmadı")
    okunamayan = [o["ham"] for o in coz["ogeler"] if o.get("okunamadi")]
    if okunamayan:
        rapor.append("    skoru okunamayan embriyo skorsuz yazıldı: "
                     + ", ".join(f"'{h}'" for h in okunamayan) + " (ekrandan düzelt)")
    if coz.get("tekrar_grup"):
        rapor.append(f'    notta aynı tüp iki kez yazılmış ({coz["tekrar_grup"]}) -- '
                     f'notun {coz["adet"]} ADET\'i ve DONDURULAN {r["dondurulan"]} '
                     f'ile tutan {len(coz["gruplar"])} tüp yazıldı')
    if yazilan:
        gunler = sorted({g for g in grup_gunleri if g}) if coz.get("grup_gunleri") else [gun]
        rapor.append(f'    skorlar: {", ".join(yazilan)} '
                     f'(gün {"/".join(str(g) for g in gunler)})')
    if coz.get("ortuk"):
        rapor.append("    not dondurmayı fiilsiz söylüyor (\"... İLE BİRLİKTE "
                     "KALDI\") -- yeniden dondurma sayıldı")
    if yeni_tup:
        rapor.append(f'    dondurma: {len(yeni_tup)} tüp — {", ".join(yeni_tup)} '
                     f'(konum boş, Cryo Haritası\'ndan gir)')
    if onarilan:
        rapor.append(f'    dondurma onarıldı: {"; ".join(onarilan)}')
    if mevcut and not yeni_tup and not onarilan and not eksik and not coz.get("eksik_not"):
        # Eksik varken "tutuyor" demek yukarıdaki UYARI'yla çelişirdi (v6.166)
        rapor.append("    dondurma zaten girilmiş, tüpler notla tutuyor")
    return bool(yeni_tup or onarilan)


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


def _bag_siniflari(b, hasta_id, cycle_id, t_cozme, n, yumurta, kaliteler, dahil=()):
    """Çözülen `n` örneğin tutabileceği tüp kümeleri -- `_kaynaga_bagla()`'nın
    arama kısmı (v6.164'te ayrıldı: var olan bağlantı da aynı kuralla yeniden
    sınanabilsin, `_baglantilari_yeniden_sina()`).

    Adaylar hastanın **dolu**, çözülmemiş, çözmeden önce dondurulmuş, tek
    tedavinin ve doğru türün (yumurta/embriyo) tüpleri; `dahil` bunlara
    boşaltılmış olsa da katılacak tüpler (bağlantının kendi tüpleri).
    Döner: (durum, adaylar, sınıflar). durum "yok" (aday yok), "cok"
    (karşılaştırılamayacak kadar çok) ya da "". Sınıf: {anahtar: (küme,
    eşleşme)}; aynı tedavinin içeriği birebir aynı kümeleri tek sınıf."""
    ted = _db.vit_tedavisi("o")
    dahil = tuple(dahil)
    ek = (f" OR t.id IN ({','.join('?' * len(dahil))})") if dahil else ""
    tupler = {}
    for tid, etiket, konum, sid, dt, dt_no, dt_tip, zaman, yum in b.execute(
            f"SELECT t.id, t.etiket, t.konum_id, o.specimen_id, {ted}, dc.cycle_no, "
            f"dc.cycle_tipi, o.zaman, {_db.dondurulan_yumurta_sql('o')} FROM tasiyici t "
            "JOIN olay o ON o.vit_tasiyici_id=t.id AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
            "JOIN specimen s ON s.id=o.specimen_id "
            "JOIN cycle sc ON sc.id=s.cycle_id "
            f"JOIN cycle dc ON dc.id={ted} "
            "WHERE sc.hasta_id=? AND t.kategori='embriyo' "
            f"AND {ted} <> ? AND o.zaman < ? "
            "AND ((t.durum='dolu' AND NOT EXISTS (SELECT 1 FROM olay x WHERE "
            "      x.tip='thaw' AND x.iptal_mi=0 AND x.thaw_tasiyici_id=t.id))"
            f"{ek}) "
            "ORDER BY t.id, o.id", (hasta_id, cycle_id, t_cozme, *dahil)).fetchall():
        tup = tupler.setdefault(tid, {"tid": tid, "etiket": etiket, "konum": konum,
                                      "ted": set(), "no": dt_no, "tip": dt_tip,
                                      "ornekler": [], "zaman": zaman, "yum": set()})
        tup["ted"].add(dt)
        tup["yum"].add(yum)
        tup["ornekler"].append(sid)
        tup["zaman"] = min(tup["zaman"], zaman)
    # Yalnızca tek tedavinin, doğru türde (yumurta/embriyo) içeriği olan tüpler.
    # Tür içerikten (v6.167, `db.dondurulan_yumurta_sql()`): IVF/ICSI'de
    # dondurulmuş aktarılmış yumurta tüpü tipe bakınca "embriyo" sayılıyordu --
    # skoru olmayan örnek her transfer yazımıyla tuttuğu için bir FET'in
    # çözdüğü embriyolar yumurta tüpüne bağlanabilirdi, Yumurta Çözme ise o
    # tüpü hiç bulamazdı.
    adaylar = []
    for tup in tupler.values():
        if len(tup["ted"]) != 1 or tup["yum"] != {1 if yumurta else 0}:
            continue
        tup["ted"] = next(iter(tup["ted"]))
        tup["ornekler"] = [
            (sid, *( (None, None) if yumurta else
                     _degerlendirme_anahtari(b, sid, tup["ted"])))
            for sid in tup["ornekler"]]
        adaylar.append(tup)
    if not adaylar:
        return "yok", adaylar, {}
    if len(adaylar) > _BAGLA_EN_COK_TUP:
        return "cok", adaylar, {}

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
        return _sinif_anahtari(adaylar, alt)

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
    return "", adaylar, siniflar


def _sinif_anahtari(adaylar, alt) -> tuple:
    """Tüp kümesinin ayırt edilebilirlik anahtarı: tedavileri + içerikleri.
    Aynı tedavinin birebir aynı tüpleri ("(4AA) (4AA)") aynı anahtar."""
    return (tuple(sorted({adaylar[i]["ted"] for i in alt})),
            tuple(sorted(tuple(sorted(str(o[1]) for o in adaylar[i]["ornekler"]))
                         for i in alt)))


def _tup_anlat(adaylar, alt) -> str:
    return (f'{adaylar[alt[0]]["no"]}: '
            + " + ".join(adaylar[i]["etiket"] for i in alt))


def _baglantilari_yeniden_sina() -> list:
    """Tüpüne BAĞLANMIŞ aktarılmış FET'ler bugünkü tüplerle hâlâ tek seçenek
    mi? (v6.164) Döner: [(Access işareti, bağlı tüpler, öteki seçenekler)].

    Bir FET o gün tek tutan tüpe bağlanıyor; sonradan aktarılan bir ay aynı
    hastaya aynı içerikte başka bir tüp getirirse seçim artık kesin değil --
    tarih sırasıyla aktarılsaydı "belirsiz" denirdi. Bağ çözülmüyor (FET'in
    kendi örnekleri silindi, tüpün yeri elle girilmiş olabilir); yalnızca
    söyleniyor, kullanıcı kâğıttan bakıyor ("belirsizi listele", v6.148).
    Hiçbir şey yazmıyor."""
    yer = ",".join("?" * len(FET_TIPLERI))
    b = _db.baglan()
    try:
        fetler = b.execute(
            "SELECT c.id, c.cycle_no, c.cycle_tipi, c.protokol_notu, c.hasta_id, "
            "MIN(o.zaman) FROM cycle c JOIN olay o ON o.thaw_cycle_id=c.id "
            "AND o.tip='thaw' AND o.iptal_mi=0 JOIN specimen s ON s.id=o.specimen_id "
            f"WHERE c.lab_id=? AND c.cycle_tipi IN ({yer}) "
            "AND c.protokol_notu LIKE '%[Access kayd%' "
            "GROUP BY c.id HAVING SUM(s.cycle_id = c.id) = 0 "
            "AND SUM(o.thaw_tasiyici_id IS NULL) = 0 ORDER BY 6, c.id",
            (_db.LAB_ID, *FET_TIPLERI)).fetchall()
        sonuc = []
        for cid, cno, tip, notu, hasta_id, t_cozme in fetler:
            cozulen = b.execute(
                "SELECT DISTINCT specimen_id, thaw_tasiyici_id FROM olay WHERE "
                "tip='thaw' AND iptal_mi=0 AND thaw_cycle_id=?", (cid,)).fetchall()
            dahil = sorted({t for _s, t in cozulen})
            yumurta = _db.cozulen_yumurta_islenir(tip)
            kaliteler = [] if yumurta else _transfer_kaliteleri(_vt_satiri(b, cid, tip))
            durum, adaylar, siniflar = _bag_siniflari(
                b, hasta_id, cid, t_cozme, len({s for s, _t in cozulen}),
                yumurta, kaliteler, dahil)
            if durum or not siniflar:
                continue
            bagli = tuple(i for i, t in enumerate(adaylar) if t["tid"] in dahil)
            if len(bagli) != len(dahil):
                continue
            anahtar = _sinif_anahtari(adaylar, bagli)
            obur = [alt for k, (alt, _e) in siniflar.items() if k != anahtar]
            if obur:
                m = re.search(r"\[Access kaydı\s+([^\]]+)\]", (notu or "").replace("\n", " "))
                sonuc.append((m.group(1) if m else cno, _tup_anlat(adaylar, bagli),
                              [_tup_anlat(adaylar, a) for a in obur]))
        return sonuc
    finally:
        b.close()


def _aktarilmamis_aylar(b, bas, son) -> list:
    """`bas` ile `son` arasındaki (ikisi de hariç) ve programda HİÇ kaydı
    olmayan aylar, "2025-11" biçiminde (v6.164).

    Bir laboratuvarın bir ay boyunca hiç tedavisi olmaz; o ayda başlayan hiç
    tedavi yoksa ay henüz aktarılmamış demektir. Çözülen embriyonun gerçek
    tüpü o ayda dondurulmuş olabilir -- o gün tek tutan tüpe bağlamak yanlış
    tüpü boşaltabilirdi (v6.163'ün bilinen sınırı; kullanıcının makinesinde
    asıl durum buydu: 2026 aktarılmışken 2025 ay ay geliyor).
    Ölçü tedavinin günü (`db.tedavi_tarihi()`: OPU, çözme/transfer, ...),
    olayların günü DEĞİL: ekimin son OPU'larının 5. gün dondurmaları ve
    transferleri kasıma düşüyor, kasım dosyası gelmeden ay dolu görünürdü.
    Bir iki tedavi de ayı doldurmuyor (`_AY_EN_AZ_TEDAVI`): kullanıcının
    veritabanında programdan girilmiş iki tedavi, dosyası hiç gelmemiş bir
    ayı "dolu" gösteriyordu; aktarılan aylar 20 ile 130 tedavi arası."""
    y1, a1 = int(bas[:4]), int(bas[5:7])
    y2, a2 = int(son[:4]), int(son[5:7])
    aylar = []
    y, a = y1, a1 + 1
    while (y, a) < (y2, a2):
        if a > 12:
            y, a = y + 1, 1
            continue
        aylar.append(f"{y:04d}-{a:02d}")
        a += 1
    if not aylar:
        return []
    sayi = _tedavi_aylari(b)
    return [ay for ay in aylar if sayi.get(ay, 0) < _AY_EN_AZ_TEDAVI]


_AY_EN_AZ_TEDAVI = 10
_AY_ONBELLEK = {"anahtar": None, "aylar": {}}


def _tedavi_aylari(b) -> dict:
    """{"2025-06": tedavi sayısı, ...}. Sorgu yarım saniye sürüyor ve her
    FET için soruluyor; tedavi eklenmedikçe (sayı ve en büyük kimlik aynı)
    öncekini döndürüyor."""
    anahtar = tuple(b.execute("SELECT COUNT(*), MAX(id) FROM cycle").fetchone())
    if _AY_ONBELLEK["anahtar"] != anahtar:
        _AY_ONBELLEK["aylar"] = {ay: n for ay, n in b.execute(
            f"SELECT substr({_db.tedavi_tarihi(b, 'c')}, 1, 7), COUNT(*) FROM cycle c "
            "WHERE c.lab_id=? GROUP BY 1", (_db.LAB_ID,))}
        _AY_ONBELLEK["anahtar"] = anahtar
    return _AY_ONBELLEK["aylar"]


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
    dolu tüpü yok), "ertelendi" (tek tutan tüp var ama arada aktarılmamış
    ay var, v6.164) ya da "" (çözülen örnek yok).
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

    kaliteler = [] if yumurta else _transfer_kaliteleri(r)
    durum, adaylar, siniflar = _bag_siniflari(b, hasta_id, cycle_id, t_cozme, n,
                                              yumurta, kaliteler)
    if durum == "yok":
        rapor.append(f"    çözülen {ne}ların tüpü programda yok "
                     "(dondurma program öncesi)")
        return "yok"
    if durum == "cok":
        rapor.append(f"    BAĞLANAMADI: hastanın {len(adaylar)} dolu tüpü var, "
                     "karşılaştırılamayacak kadar çok -- elle bakılmalı")
        return "tutmuyor"

    def anlat(alt):
        return _tup_anlat(adaylar, alt)
    if not siniflar:
        # Hastanın tüpleri tutmuyor, ama aralarında aktarılmamış ay varsa
        # gerçek tüp o ayda olabilir (v6.164): "elle bak" değil, bekle.
        bosluk = _aktarilmamis_aylar(b, min(t["zaman"] for t in adaylar), t_cozme)
        if bosluk:
            rapor.append(f"    ERTELENDİ: hastanın dolu tüpleri tutmuyor, ama arada "
                         f"programda hiç kaydı olmayan ay var ({', '.join(bosluk)}) "
                         "-- gerçek tüp o aylarda olabilir, aktarılınca yeniden "
                         "denenecek")
            return "ertelendi"
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
    # Tüp ile çözme arasında aktarılmamış ay varsa bekle (v6.164): gerçek tüp
    # o ayda olabilir. Ay gelince her aktarımın sonundaki `butun_fetleri_bagla()`
    # yeniden dener -- o gün tek seçenek kalıyorsa bağlar.
    bosluk = _aktarilmamis_aylar(b, min(adaylar[i]["zaman"] for i in alt), t_cozme)
    if bosluk:
        rapor.append(f"    ERTELENDİ: tutan tüp ({anlat(alt)}) ile çözme arasında "
                     f"programda hiç kaydı olmayan ay var ({', '.join(bosluk)}) -- "
                     "o aylar aktarılınca yeniden denenecek")
        return "ertelendi"

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
    # Taşınan örneklerde FET'in transfer günü değerlendirmesi (v6.154, nottan)
    # kaynağın AYNI tip ve gündeki kaydıyla çakışıyorsa FET'inki iptal
    # (v6.163). `_fet_transfer_kalitesi()` bağlı embriyoya zaten yazmıyor;
    # önce yazılıp sonra bağlanan (2026 aktarılmışken 2025 gelince) aynı
    # kurala getiriliyor -- değerlendirme örnek+gün başına tek (v6.146).
    for kaynak_sid in eslesme.values():
        for oid, dtip, dgun in b.execute(
                "SELECT o.id, o.tip, o.gun FROM olay o WHERE o.specimen_id=? "
                "AND o.iptal_mi=0 AND o.notlar LIKE ? AND o.tip IN (?, ?)",
                (kaynak_sid, _KAYNAK_YAZIMI + " (transfer):%")
                + _DEGERLENDIRMELER).fetchall():
            if b.execute(
                    "SELECT 1 FROM olay o WHERE o.specimen_id=? AND o.tip=? "
                    "AND o.gun=? AND o.iptal_mi=0 AND o.id<>? "
                    f"AND NOT ({_db.bu_tedavide(cycle_id, 'o')}) LIMIT 1",
                    (kaynak_sid, dtip, dgun, oid)).fetchone():
                _iptal(b, kid, oid, "Kaynak tedavide ayni gunun kaydi var "
                                    "(tupune baglandi)")
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
        n = _yumurta_sayisi(r)
        icerik = (f'{n} {"çözülen yumurta" if r["tip"] == "yumurta_cozme" else "oosit"}'
                  f' / {r["mii"]} MII / {r["islenen"]} ICSI / {r["iki_pn"]} 2PN / '
                  f'{r["dondurulan"]} dondurma')
    ek = ""
    if r["tarih_yaklasik"]:
        ek += "   [tarih yok: yaklaşık]"
    for alan, eski, yeni in r["duzeltme"]:
        ek += (f"   [{alan} {eski} → {yeni}]" if alan in _SAYI_ALANI
               else f"   [{alan} {_gg(eski)} → {_gg(yeni)}]")
    if r.get("olgunluk_duzeltme"):
        ek += f'   [MII {r["olgunluk_duzeltme"][0]} → {r["mii"]}, nottan]'
    if r.get("icsi_hatali"):
        ek += (f'   [ICSI {r["icsi_hatali"]} yumurtadan fazla → '
               f'{r["icsi_duzeltme"] or "yazılmadı"}'
               + (", döllenme sonuçlarından]" if r.get("icsi_duzeltme") else "]"))
    elif r.get("icsi_duzeltme"):
        ek += f'   [ICSI boş → {r["icsi_duzeltme"]}, döllenme sonuçlarından]'
    if r.get("yumurta_fazla"):
        ek += f'   [toplanan {r["toplanan"] or 0} → {r["yumurta_fazla"]}, olgunluk sayılarından]'

    return (f'#{r["kimlik"]:>3}  dosya {r["dosya_no"]:<10} {r["tip"]:<14}'
            f'{r["tarih"] or "tarihsiz":<11} {icerik:<52} {son}{ek}')


def onizleme(satirlar, kopyalar=(), tutmayan=(), atla=(), ikizler=()):
    print(f"\nCSV'de {len(satirlar) + len(kopyalar) + len(atla) + len(ikizler)} "
          f"satır. Veritabanı: {DB}\n")
    for r in kopyalar:
        print(f'#{r["kimlik"]:>3}  ATLANIR — aynı hastanın aynı günkü dolu '
              "satırının boş kopyası (hiçbir sayı ve not yok)")
    for r in atla:
        print(f'#{r["kimlik"]:>3}  ATLANIR — düzeltme dosyasında ATLA yazıyor')
    for satir in ikiz_satirlari(ikizler):
        print(satir)
    for t in tutmayan:
        print(f"UYARI: düzeltme satırı uygulanmadı, Access'teki değer tutmuyor: {t}")
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
        if r.get("tip_duzeltme"):
            print(f'        tip: Yumurta Dondurma -- protokol "{r["protokol"]}" ama '
                  "ICSI, 2PN ve transfer yok, yalnızca yumurta dondurulmuş")
        if r["dosya_no"] < 1000:
            print(f'        DİKKAT: dosya numarası {len(str(r["dosya_no"]))} haneli '
                  "-- Access'te yer tutucu yazılmış olabilir, kontrol et")
        coz = _satir_dondurmasi(r)
        if coz and coz["ogeler"]:
            # Kullanıcının kendi yazımı basılıyor ("4HG2"), çözümlenmiş kod
            # değil -- kendi notunda ne yazdığını tanıyabilmeli.
            ozet = " ".join("(" + "-".join(o["ham"] for o in g) + ")"
                            for g in coz["gruplar"])
            gunler = ("/".join(str(g) for g in coz["grup_gunleri"])
                      if coz.get("grup_gunleri") else coz["gun"])
            atilan = [o["ham"] for o in coz["ogeler"] if o["tur"] == "taninmadi"]
            okunamayan = [o["ham"] for o in coz["ogeler"] if o.get("okunamadi")]
            print(f'        dondurulan ({"yumurta + embriyo" if coz.get("karisik") else "yumurta" if coz["oosit_mi"] else "embriyo"}'
                  + (f', gün {gunler}' if gunler else "")
                  + f', {len(coz["gruplar"])} tüp): {ozet}'
                  + ("   <- çözme sonrası yeniden dondurma"
                     if r["tip"] in ("fet", "fet_kultur") else "")
                  + ("   <- not fiilsiz söylüyor (\"İLE BİRLİKTE KALDI\")"
                     if coz.get("ortuk") else "")
                  + (f'   <- aynı tüp iki kez yazılmış, biri alınmadı '
                     f'({coz["tekrar_grup"]})' if coz.get("tekrar_grup") else "")
                  + (f'   <- skoru okunamadı, skorsuz: {", ".join(okunamayan)}'
                     if okunamayan else "")
                  + (f'   <- kaynak {coz["beklenen"]} diyor, tüplerde '
                     f'{coz["beklenen"] - coz["eksik_not"]}: {coz["eksik_not"]} '
                     "yazılmayacak" if coz.get("eksik_not") else "")
                  + (f'   <- TANINMADI, yazılmayacak: {", ".join(atilan)}'
                     if atilan else ""))
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
          f'hasta kartı açılacak, {atlanan + len(kopyalar) + len(atla) + len(ikizler)} '
          'satır atlanacak.')
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
    if say.get("ertelendi"):
        print(f'{say["ertelendi"]} tedavi ertelendi: tüp ile çözme arasında '
              "aktarılmamış ay var; o ay aktarılınca kendiliğinden denenecek.")
    elle = [(k, d) for k, d in sonuclar if d in ("belirsiz", "tutmuyor")]
    if elle:
        print("Elle bakılmalı (yukarıdaki satırlarında ayrıntı var):")
        for k, d in elle:
            print(f'  #{k:>3}  {"birden çok tüp seçeneği" if d == "belirsiz" else "dolu tüpler tutmuyor"}')


def aktar(satirlar, ikizler=()):
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
    farkli = [x for x in ikizler if x[3] == "farkli"]
    if farkli:
        # Uzun çıktının başında kalmasın (v6.167): karar kullanıcının.
        print("\nAynı gün iki farklı kaydı olan hasta -- ikisi de AKTARILMADI:")
        for satir in ikiz_satirlari(farkli):
            print("  " + satir)
    _bagla_ozeti(sonuclar)
    # Daha önce aktarılmış FET'ler: çözdükleri tüp bu dosyayla gelmiş
    # olabilir (v6.163). Bu dosyanın FET'leri zaten yukarıda denendi.
    print("\nDaha önce aktarılmış FET'ler yeni gelen tüplerle eşleştiriliyor...")
    butun_fetleri_bagla(yalnizca_ozet=True)


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


def _vt_satiri(b, cycle_id, tip) -> dict:
    """Aktarılmış bir FET'in `_kaynaga_bagla()`'nın istediği bilgisi,
    CSV'siz: veritabanından (v6.163). Gereken yalnızca tip, transfer sayısı
    ve transfer edilen embriyoların yazımı -- yazım transfer olayının
    notunda ("Embriyo: 3AA", `_fet_embriyolari()`), `_kalite_yazimi()`'nin
    biçiminde, yani `_kalite_coz()` onu yeniden tanıyor."""
    yazimlar = []
    for (notu,) in b.execute(
            "SELECT o.notlar FROM olay o JOIN specimen s ON s.id=o.specimen_id "
            "WHERE o.tip='transfer' AND o.iptal_mi=0 AND o.tr_cycle_id=? "
            "ORDER BY s.cycle_sira_no, o.id", (cycle_id,)).fetchall():
        m = re.search(r"Embriyo:\s*(.+)$", notu or "")
        yazimlar.append(m.group(1).strip() if m else "")
    emb = [("", y) for y in yazimlar[:2]] + [("", "")] * 2
    return {"tip": tip, "emb1": emb[0], "emb2": emb[1],
            "transfer_adet": len(yazimlar)}


def butun_fetleri_bagla(yalnizca_ozet=False):
    """Veritabanındaki BÜTÜN aktarılmış FET'leri tüpüne bağlamayı dener
    (v6.163, kullanıcının isteği: "aktardığım bütün tedavileri birbirine
    bağla ... her yeni aktarım yaptığımda eski kayıtlardan bağlantılı hasta
    varsa tedavileri bağla").

    Aylar karışık sırayla aktarılıyor (2026 önce, 2025 sonra): bir FET
    aktarıldığı gün çözdüğü tüp programda yoktu, sonradan geldi. Bu işlev
    CSV'ye bakmıyor -- hâlâ kendi embriyolarını taşıyan (bağlanmamış) her
    aktarılmış FET'i **çözme tarihi sırasıyla** `_kaynaga_bagla()`'dan
    geçiriyor: aynı tüpü isteyebilecek iki FET'ten önce çözen önce alır.
    Kurallar aynı: tek eşleşme bağlanır, belirsiz ve tutmayan listelenir.
    Her aktarımın sonunda kendiliğinden çalışıyor (`aktar()`); ayrıca
    `bagla` kipi. Bağlı olana dokunmuyor, ikinci çalıştırma hiçbir şey
    değiştirmez."""
    kid = _kullanici_id()
    yer = ",".join("?" * len(FET_TIPLERI))
    fetler = _db.sorgu(
        "SELECT c.id, c.cycle_no, c.cycle_tipi, c.protokol_notu, MIN(o.zaman) t "
        "FROM cycle c JOIN olay o ON o.thaw_cycle_id=c.id AND o.tip='thaw' "
        "AND o.iptal_mi=0 JOIN specimen s ON s.id=o.specimen_id AND s.cycle_id=c.id "
        f"WHERE c.lab_id=? AND c.cycle_tipi IN ({yer}) "
        "AND c.protokol_notu LIKE '%[Access kayd%' "
        "GROUP BY c.id ORDER BY t, c.id", (_db.LAB_ID, *FET_TIPLERI))
    sonuclar, eksik_aylar = [], []
    for f in fetler:
        m = re.search(r"\[Access kaydı\s+([^\]]+)\]",
                      (f["protokol_notu"] or "").replace("\n", " "))
        etiket = m.group(1) if m else f["cycle_no"]
        rapor = []
        try:
            with _db.yazma_islemi() as b:
                durum = _kaynaga_bagla(b, _vt_satiri(b, f["id"], f["cycle_tipi"]),
                                       f["id"], kid, rapor)
        except Exception as hata:            # biri ötekileri durdurmasın
            print(f'{f["cycle_no"]} ({etiket})  HATA: {hata}')
            continue
        if durum:
            sonuclar.append((etiket, durum))
        if durum == "ertelendi":
            for satir in rapor:
                mm = re.search(r"kaydı olmayan ay var \(([^)]*)\)", satir)
                if mm:
                    eksik_aylar.append(mm.group(1).split(", "))
        if durum in ("bagli", "belirsiz", "tutmuyor") and not (
                yalnizca_ozet and durum != "bagli"):
            print(f'{f["cycle_no"]} ({etiket})')
            for satir in rapor:
                print(satir)
    bagli = sum(1 for _k, d in sonuclar if d == "bagli")
    elle = [(k, d) for k, d in sonuclar if d in ("belirsiz", "tutmuyor")]
    print(f"\nBütün aktarılmış FET'ler: {len(fetler)} tanesi henüz tüpüne "
          f"bağlı değildi, {bagli} tanesi şimdi bağlandı, "
          f"{sum(1 for _k, d in sonuclar if d == 'yok')} tanesinin tüpü "
          f"programda yok (dondurma program öncesi).")
    ertelenen = sum(1 for _k, d in sonuclar if d == "ertelendi")
    if ertelenen:
        aylar = sorted({ay for a in eksik_aylar for ay in a})
        print(f"{ertelenen} tanesi ertelendi: tüp ile çözme arasında "
              f"aktarılmamış ay var ({', '.join(aylar)}); o aylar aktarılınca "
              "kendiliğinden yeniden denenir.")
    if elle:
        print("Elle bakılmalı (Access kaydı):")
        for k, d in elle:
            print(f'  {k}  {"birden çok tüp seçeneği" if d == "belirsiz" else "dolu tüpler tutmuyor"}')
    # Önceden bağlanmış olanlar yeni gelen tüplerle hâlâ tek seçenek mi (v6.164)
    simdi_belirsiz = _baglantilari_yeniden_sina()
    if simdi_belirsiz:
        print("Bağlı ama artık kesin değil -- sonradan gelen bir tüp de tutuyor, "
              "elle bakılmalı (Access kaydı: bağlı tüp | öteki seçenek):")
        for k, bagli_tup, obur in simdi_belirsiz:
            print(f'  {k}  {bagli_tup}  |  {" | ".join(obur)}')


def eksik_dondurmalari_yaz(satirlar):
    """Yalnızca EKSİK dondurma: `tamamla`'nın 1. adımı, dar halde (v6.161,
    v6.165).

    Araç bir dondurma notunu okuyamadığında tüp açmıyor, uyarıyordu
    ("2 ADET M2 OOSİT DONDURULARAK SAKLANDI": kullanıcının cevabı "tek
    tüptür"). Kural sonradan değişince o tedavinin tüpü ancak `tamamla` ile
    yazılır, `tamamla` ise öteki tedavilerde elle düzeltilmiş skorları
    nottaki değerle ezer (v6.142). Bu kip:
    - hiç tüpü olmayan tedaviye dondurmayı baştan yazıyor (v6.161);
    - tüpü olan tedavide yalnızca eksiği ekliyor (v6.165): v6.164'e kadar
      araç "(8HG2 8HG2 8HG2 6HG3)" gibi ayırıcısız skorların yalnızca ilkini
      okuyordu, şubat 2026'nın bir tüpüne 4 yerine 1 embriyo girdi. Tüpteki
      örneğe, skoruna ve durumuna dokunulmuyor, hiçbir şey çıkarılmıyor
      (`_dondurma_kayitlari(yalnizca_ekle=True)`).
    Bir şey yazılan ya da UYARI veren tedavi basılıyor: tüpte eksik olup
    eklenemeyen örnek (havuz boş, not tutmuyor) sessiz kalmasın (v6.166).
    Son satır kaç aktarılmış tedaviye bakıldığını söylüyor; hiçbiri
    bulunamadıysa `kaynak=` etiketi aktarımdakiyle aynı değildir. İkinci
    çalıştırma hiçbir şey değiştirmez."""
    kid = _kullanici_id()
    yazilan = bakilan = 0
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if not var:
            continue
        bakilan += 1
        if var["cycle_tipi"] != r["tip"]:
            r = dict(r, tip=var["cycle_tipi"])
        coz = _satir_dondurmasi(r)
        if not coz or not coz["gruplar"]:
            continue
        with _db.yazma_islemi() as b:
            tupu_var = bool(b.execute(
                "SELECT 1 FROM olay o JOIN specimen s ON s.id=o.specimen_id "
                "WHERE o.tip='vitrifikasyon' AND o.iptal_mi=0 "
                f"AND o.vit_tasiyici_id IS NOT NULL AND {_db.vit_tedavisi('o')} = ?",
                (var["id"],)).fetchone())
            rapor = []
            yazdi = _dondurma_kayitlari(b, r, var["id"], kid, rapor,
                                        yalnizca_ekle=tupu_var)
        if yazdi or any("UYARI" in satir for satir in rapor):
            yazilan += bool(yazdi)
            print(f'#{r["kimlik"]:>3}  {var["cycle_no"]}')
            for satir in rapor:
                print(satir)
    print(f"\nBitti. {yazilan} tedaviye eksik dondurma yazildi "
          f"({bakilan} aktarilmis tedavi gozden gecirildi).")
    if satirlar and not bakilan:
        print("Bu dosyanin hicbir satiri programda bulunamadi: kaynak= etiketi "
              "aktarimdakiyle ayni mi? (ornek: subat 2026 icin kaynak=SUBAT)")


def tipleri_duzelt():
    """Aktarılmış, ICSI'siz ve yalnızca yumurta donduran IVF/ICSI tedavisini
    Yumurta Dondurma yapar (v6.167) -- `tipi_veriden_duzelt()`'in onarım yolu.

    CSV'siz, bütün veritabanı (`bagla` gibi): ölçü aktarılmış tedavinin
    kendi kayıtları, satırın kuralının aynısı -- hiçbir örneğinde ICSI,
    döllenme, cleavage/blastokist değerlendirmesi ya da transfer yok, bu
    tedavide çözme yok, en az bir dondurması var ve hepsi yumurta
    (`db.dondurulan_yumurta_sql()`), tedaviye bağlanmış dondurulmuş sperm yok.
    Değişen yalnızca `cycle.cycle_tipi` (değişiklik geçmişine yazılıyor) ve
    Yumurta Dondurma'da olmayan aşamaların "İşlemi yapan"ı (`islem_yapan`:
    aynı satır bugün aktarılsa yazılmazdı; ICSI embriyoloğu resmî formda
    "fertilizasyon embriyoloğu" diye basılıyordu). İkinci çalıştırma hiçbir
    şey değiştirmez."""
    vt = _db.vit_tedavisi("v")
    izler = ("'icsi', 'fertilizasyon_kontrolu', 'cleavage_degerlendirme', "
             "'blastokist_degerlendirme', 'transfer'")
    sperm = ("AND NOT EXISTS (SELECT 1 FROM sperm_dondurma sd "
             "WHERE sd.kullanim_cycle_id = c.id) "
             if _db.kolon_var("sperm_dondurma", "kullanim_cycle_id") else "")
    b = _db.baglan()
    try:
        adaylar = b.execute(
            "SELECT c.id, c.cycle_no, c.protokol_notu FROM cycle c "
            "WHERE c.lab_id=? AND c.cycle_tipi='ivf_icsi' "
            "AND c.protokol_notu LIKE '%[Access kaydı%' "
            f"AND EXISTS (SELECT 1 FROM olay v WHERE v.tip='vitrifikasyon' "
            f"  AND v.iptal_mi=0 AND {vt} = c.id) "
            f"AND NOT EXISTS (SELECT 1 FROM olay v WHERE v.tip='vitrifikasyon' "
            f"  AND v.iptal_mi=0 AND {vt} = c.id "
            f"  AND {_db.dondurulan_yumurta_sql('v')} = 0) "
            "AND NOT EXISTS (SELECT 1 FROM olay e JOIN specimen s ON s.id=e.specimen_id "
            f"  WHERE s.cycle_id=c.id AND e.iptal_mi=0 AND e.tip IN ({izler})) "
            "AND NOT EXISTS (SELECT 1 FROM olay t WHERE t.iptal_mi=0 "
            "  AND (t.tr_cycle_id=c.id OR t.thaw_cycle_id=c.id)) "
            f"{sperm}ORDER BY c.cycle_no", (_db.LAB_ID,)).fetchall()
    finally:
        b.close()
    kid = _kullanici_id()
    kalan = tuple(_db.TIP_ASAMALARI["oosit_cryo"])
    yer = ",".join("?" * len(kalan))
    for cid, cycle_no, notu in adaylar:
        isaret = re.search(r"\[Access kaydı ([^\]]+)\]",
                           re.sub(r"\s+", " ", notu or ""))
        with _db.yazma_islemi() as b:
            b.execute("UPDATE cycle SET cycle_tipi='oosit_cryo' WHERE id=? "
                      "AND cycle_tipi='ivf_icsi'", (cid,))
            b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
                      "eski_deger, yeni_deger, kullanici_id, zaman) "
                      "VALUES (?,?,?,?,?,?,?,?)",
                      (_db.LAB_ID, "cycle", str(cid), "cycle_tipi", "ivf_icsi",
                       "oosit_cryo", kid,
                       _dt.datetime.now().isoformat(" ", "seconds")))
            silinen = b.execute(f"DELETE FROM islem_yapan WHERE cycle_id=? "
                                f"AND asama NOT IN ({yer})", (cid, *kalan)).rowcount
        print(f'  {isaret.group(1) if isaret else "?":<16} {cycle_no}: IVF/ICSI -> '
              "Yumurta Dondurma"
              + (f" ({silinen} aşamanın 'işlemi yapan'ı kaldırıldı)" if silinen else ""))
    print(f"\nBitti. {len(adaylar)} tedavinin tipi Yumurta Dondurma yapıldı "
          "(ICSI'siz, yalnızca yumurta donduran aktarılmış IVF/ICSI tedavileri).")


def ikizleri_listele():
    """Aynı hastanın aynı gün aynı tipte iki AKTARILMIŞ tedavisi (v6.167) --
    listeler, hiçbir şey yazmaz.

    `ikizleri_ayikla()` v6.167'de geldi; öncesinde Access'te iki kez girilmiş
    bir kayıt iki tedavi olarak aktarıldı (haziran, temmuz ve aralık 2025'te
    birer çift: hepsi iptal edilmiş IVF/ICSI, notun yazımından başka farkları
    yok). Hangisinin fazla olduğuna kullanıcı karar veriyor ve fazlasını
    ekrandan kalıcı siliyor; araç silmiyor. Gün `db.tedavi_tarihi()`."""
    b = _db.baglan()
    try:
        gun = _db.tedavi_tarihi(b, "c")
        satirlar = b.execute(
            f"SELECT c.id, c.cycle_no, c.cycle_tipi, c.durum, c.hasta_id, "
            f"h.dosya_no, {gun} AS gun, c.protokol_notu, "
            "EXISTS (SELECT 1 FROM olay t WHERE t.tip='transfer' AND t.iptal_mi=0 "
            "  AND COALESCE(t.tr_cycle_id, t.cycle_id) = c.id) AS transferli "
            "FROM cycle c JOIN hasta h ON h.id = c.hasta_id "
            "WHERE c.lab_id=? AND c.protokol_notu LIKE '%[Access kaydı%' "
            "ORDER BY c.hasta_id, gun, c.id", (_db.LAB_ID,)).fetchall()
    finally:
        b.close()
    gruplar = {}
    for c in satirlar:
        if c["gun"]:
            gruplar.setdefault((c["hasta_id"], c["gun"], c["cycle_tipi"]), []).append(c)
    ciftler = [g for g in gruplar.values() if len(g) > 1]
    for g in ciftler:
        print(f'dosya {g[0]["dosya_no"]}, {_gg(g[0]["gun"])}, {g[0]["cycle_tipi"]}:')
        for c in g:
            isaret = re.search(r"\[Access kaydı ([^\]]+)\]",
                               re.sub(r"\s+", " ", c["protokol_notu"] or ""))
            print(f'   {c["cycle_no"]}  {isaret.group(1) if isaret else "?":<16} '
                  f'{c["durum"]}'
                  + ("  (transferi var -- kalıcı silinemez)" if c["transferli"] else ""))
    print(f"\nBitti. {len(ciftler)} hastada aynı gün aynı tipte iki aktarılmış tedavi. "
          "Hiçbir şey değiştirilmedi.")
    if ciftler:
        print("Fazla olanı hasta kartından aç -> Sil -> kalıcı silme (dosya no + SIL).")


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
    if arg and arg[0] in ("liste", "tamamla", "iptal", "transfer", "bagla", "dondurma",
                          "tip", "ikiz"):
        kip, arg = arg[0], arg[1:]
    if kip == "ikiz":
        ikizleri_listele()              # v6.167: hiçbir şey yazmaz
        return
    if kip == "tip":
        # v6.167: CSV'ye bakmıyor, veritabanındaki aktarılmış bütün tedaviler.
        if not _db.kolon_var("cycle", "hasta_cycle_no_elle"):
            sys.exit("Veritabani guncellemesi eksik. Programi bir kez kapatip ac, "
                     "sonra tekrar dene.")
        tipleri_duzelt()
        return
    if kip == "bagla":
        # v6.163: CSV'ye bakmıyor, veritabanındaki bütün aktarılmış FET'ler.
        # Eski yazım (`bagla kaynak=X dosya.csv`) da çalışsın: dosya yok sayılır.
        if not _db.kolon_var("cycle", "hasta_cycle_no_elle"):
            sys.exit("Veritabani guncellemesi eksik. Programi bir kez kapatip ac, "
                     "sonra tekrar dene.")
        butun_fetleri_bagla()
        return
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
                 "  python3 aktar_access.py dondurma <dosya.csv>  yalnizca eksik\n"
                 "                                                dondurma (tupteki\n"
                 "                                                ornege dokunmaz)\n"
                 "  python3 aktar_access.py bagla                 aktarilmis butun\n"
                 "                                                FET'leri tupune\n"
                 "                                                baglar (dosya gerekmez)\n"
                 "  python3 aktar_access.py tip                   ICSI'siz, yalnizca\n"
                 "                                                yumurta donduran\n"
                 "                                                IVF/ICSI tedavisini\n"
                 "                                                Yumurta Dondurma yapar\n"
                 "                                                (dosya gerekmez)\n"
                 "  python3 aktar_access.py ikiz                  ayni hastanin ayni gun\n"
                 "                                                iki kez aktarilmis\n"
                 "                                                tedavileri listeler\n"
                 "                                                (hicbir sey yazmaz)\n"
                 "\n"
                 "  kaynak=<AD>  ikinci bir Access dosyasi aktarilirken sart:\n"
                 "               her dosya kendi kayitlarini 1'den numaraliyor,\n"
                 "               etiket numarayi dosyasina bagliyor.\n"
                 "               ornek: python3 aktar_access.py kaynak=TEMMUZ temmuz.csv\n"
                 "  duzelt=<dosya>  yazim hatali tarihlerin duzeltmeleri (satir:\n"
                 "               KAYNAK#KAYIT  OPU|TRANSFER  eski-tarih  yeni-tarih)\n"
                 "               ve aktarilmayacak kayitlar (KAYNAK#KAYIT  ATLA),\n"
                 "               yer tutucu dosya no (KAYNAK#KAYIT  DOSYA  eski  yeni)")
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
    duzeltmeler = duzeltmeleri_oku(duzelt) if duzelt else []
    tutmayan = duzeltmeleri_uygula(satirlar, duzeltmeler, KAYNAK)
    tarihleri_tamamla(satirlar)
    olgunlugu_nottan_duzelt(satirlar)
    icsi_sayisini_tamamla(satirlar)
    yumurta_sayisini_isaretle(satirlar)
    tipi_veriden_duzelt(satirlar)
    kopyalar = bos_kopyalari_ayikla(satirlar)
    # Atlanacak kayıtlar ve aynı gün iki kez girilmiş kayıtlar (v6.167) --
    # yalnızca yeni aktarımda: onarım kipleri zaten aktarılmış tedavilere
    # işaretleriyle ulaşıyor, aktarılmamış satıra dokunmuyor.
    atla, ikizler = [], []
    if kip in ("liste", "aktar"):
        atla, atla_tutmayan = atla_satirlarini_ayikla(satirlar, duzeltmeler, KAYNAK)
        tutmayan += [f"{t} (bu dosyada böyle bir kayıt yok)" for t in atla_tutmayan]
        ikizler = ikizleri_ayikla(satirlar)
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
        onizleme(satirlar, kopyalar, tutmayan, atla, ikizler)
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
    if kip == "dondurma":
        eksik_dondurmalari_yaz(satirlar)
        return
    onizleme(satirlar, kopyalar, tutmayan, atla, ikizler)
    print("Bu, veritabanina YAZAR. Once yedek al (/yedekleme -> Simdi yedekle).")
    if input("Devam etmek icin AKTAR yaz: ").strip() != "AKTAR":
        sys.exit("Vazgecildi, hicbir sey yazilmadi.")
    aktar(satirlar, ikizler)


if __name__ == "__main__":
    main()
