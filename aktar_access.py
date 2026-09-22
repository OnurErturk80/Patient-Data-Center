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
  - Dondurulanlar için o kadarı kaydediliyor: gün ≥ 5 blastokist, öncesi
    cleavage değerlendirmesi, skor alanları boş. Yani bu sayılar "en az"
    demek -- gün 5'e ulaşıp dondurulmayan embriyo kaynakta hiç görünmüyor.
    `/istatistik`'in blastokist oranı bu yüzden olduğundan düşük çıkar;
    ağustos için "ölçülmedi" demek daha doğru olurdu ama programda o ayrım
    yok.
  - FET'te transfer edilen embriyo için **yazılmıyor**: o embriyo bu
    tedavide gelişmedi, programda hiç olmayan bir önceki tedavide gelişti.
    Aşaması ve kalitesi transfer olayının notunda duruyor ("5. gün", "3AA").
- **Dondurulan embriyonun taşıyıcısı ve yeri**: kaynakta yok.
  `vitrifikasyon` olayı `vit_tasiyici_id` olmadan yazılıyor -- sayı doğru
  çıkar ama Cryo Haritası'nda görünmez. Taşıyıcı/konum uydurmak, geri
  alınan v6.127'nin hatasıydı.
- **Dondurulan YUMURTA (oosit_cryo)**: kaynağın "DONDURULAN EMBRİYO
  SAYISI" alanı embriyo için, yumurta dondurmada boş. Kaç yumurtanın
  dondurulduğu yalnızca serbest NOTLAR metninde yazıyor ("16 ADET OOSİT
  4 TÜPTE..."). Serbest metinden sayı çıkarmak kırılgan olurdu; o tedaviler
  için vitrifikasyon olayı **yazılmıyor**, not olduğu gibi aktarılıyor.
  Kullanıcı isterse vitrifikasyon ekranından elle girer.
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
"""


import csv
import datetime as _dt
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
        return "fet"
    if "CRYO" in p or "KRIYO" in p:
        return "oosit_cryo"
    return "ivf_icsi"


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
        tip = cycle_tipi(v("TEDAVİ PROTOKOLÜ"))
        opu = _tarih(v("OPU TARİHİ"))
        transfer = _tarih(v("TRANSFER TARİHİ"))
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
            "viabilite": _ondalik(v("ÇÖZDÜRME SONRASI VİABİLİTE")),
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
    ("cleavage_arrest", ("2. GUN EMBRIYO ARRE", "3. GUN EMBRIYO ARRE",
                         "2.GUN EMBRIYO ARRE", "3.GUN EMBRIYO ARRE",
                         "KLIVAJ ASAMASINDA EMBRIYO ARRE")),
    ("gun5_arrest", ("5. GUN EMBRIYO ARRE", "5.GUN EMBRIYO ARRE",
                     "BLASTOKIST ARRE")),
)


# "Dondurularak saklandı" cümlesi: sayı alanı boş olan yumurta dondurmada
# tedavinin nasıl bittiğini yalnızca not söylüyor. "DONDURULMUŞ EMBRİYOSU
# KALDI" (önceki tedaviden artan) bilerek eşleşmiyor.
_DONDURMA_SOZU = ("DONDURULARAK SAKLAND", "DONDURULDU")


def _dondurma_sozu(notlar: str) -> bool:
    n = _sade(notlar)
    return any(s in n for s in _DONDURMA_SOZU)


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
#   KAVG2                 -> kavitasyon + derece 2   (M/EM/ARR aynı desen)
#   4HG2, 3HG2            -> cleavage: hücre sayısı + G skoru
#   2*M2, 3*M2            -> dondurulan OOSİT grubu (tüp başına adet)
_OOSIT_GRUBU = re.compile(r"^(\d+)\s*\*\s*M\s*(?:2|II)$")
_CLEAVAGE = re.compile(r"^(\d+)\s*H\s*G?\s*([1-4])")
_BLAST = re.compile(r"^([1-6])\s*([ABC])\s*([ABC])")
_BLAST_DISI = re.compile(r"^(KAV|EM|ARR|M)\s*G?\s*([1-3])?(?![A-Z0-9])")
# `app.BLAST_KISA`'nın tersi -- oradaki kısaltmalar kâğıda da böyle yazılıyor.
_KISALTMA = {"KAV": "kavitasyon", "M": "morula", "EM": "erken_morula",
             "ARR": "arrest"}


def _skor_coz(parca: str):
    """Tek bir skor yazısını programın alanlarına çevirir. Tanımazsa None."""
    t = _sade(parca)
    if not t:
        return None
    m = _OOSIT_GRUBU.match(t)
    if m:
        return {"tur": "oosit", "adet": int(m.group(1)), "ham": parca.strip()}
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
        return {"tur": "blast", "genisleme": kod, "derece": derece,
                "skor": m.group(1) + (derece or ""), "ham": parca.strip()}
    return None


def _dondurma_coz(notlar: str, asama: str = "", tip: str = "") -> dict:
    """Dondurma cümlesini çözümler. Dondurma yoksa boş sözlük.

    Yalnızca "... DONDURULARAK SAKLANDI" cümlesinin **öncesine** bakıyor:
    bir kayıtta o cümleden sonra ilgisiz metin geliyor ("SPERM MORFOLOJİSİ
    KÖTÜ, ... MOTİLİTE %0") ve oradaki sayılar skor sanılmamalı.
    """
    sade = _sade(notlar)
    kesim = len(sade)
    for soz in _DONDURMA_SOZU:
        yer = sade.find(soz)
        if yer >= 0:
            kesim = min(kesim, yer)
    if kesim == len(sade):
        return {}
    cumle = sade[:kesim]
    ham_cumle = notlar[:kesim] if len(notlar) >= kesim else notlar

    gun = _asama_gunu(asama)
    if gun is None:
        m = re.search(r"\bD\s*([1-7])\b", cumle)
        gun = int(m.group(1)) if m else None

    def _ilk(kalip):
        m = re.search(kalip, cumle)
        return int(m.group(1)) if m else None

    # **Bir parantez grubu = bir tüp.** Kaynak kayıt tüp sayısını bazen ayrıca
    # yazıyor ("2 TÜPTE"), bazen yazmıyor; ama yazdığı her satırda grup sayısı
    # o sayıyla birebir tutuyor (doğrulandı, 7 notun 3'ünde açık sayı var):
    #   "6 ADET OOSİT 2 TÜPTE (3*M2) (3*M2)"        -> 2 grup, 2 tüp
    #   "1TÜPTE 3 ADET D3 EMBRİYOSU (4HG2-4HG2-3HG2)" -> 1 grup, 1 tüp
    # Grup içinde "-" örnekleri ayırıyor, "N*M2" ise N yumurta demek.
    # Açık sayı olmayan satırlarda tüp sayısı bu yapıdan okunuyor.
    gruplar = []
    for grup in re.findall(r"\(([^)]*)\)", ham_cumle):
        icerik = []
        for parca in grup.split("-"):
            coz = _skor_coz(parca)
            if coz:
                icerik.append(coz)
            elif parca.strip():
                icerik.append({"tur": "taninmadi", "ham": parca.strip()})
        if icerik:
            gruplar.append(icerik)
    ogeler = [o for g in gruplar for o in g]      # düz liste
    return {
        "gun": gun,
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
        "oosit_mi": (_db.yumurta_mi(tip)
                     or "OOSIT" in cumle or "YUMURTA" in cumle
                     or (bool(ogeler)
                         and all(o["tur"] == "oosit" for o in ogeler))),
        "adet": _ilk(r"(\d+)\s*ADET"),
        "tup": _ilk(r"(\d+)\s*TUPTE"),
        "gruplar": gruplar,
        "ogeler": ogeler,
    }


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
    if r["tip"] in FET_TIPLERI:
        p.append("Program öncesi Access kaydından aktarıldı; çözülen "
                 "embriyoların dondurulduğu tedavi programda yok.")
    else:
        p.append("Program öncesi Access kaydından aktarıldı; yumurta kayıtları "
                 "toplam sayılardan üretildi, tek tek gözlem değildir.")
    # İşaret KENDİ satırında: cümlenin sonuna eklenirse `textwrap` onu
    # ortasından bölüyor ("[Access kaydı\nTEMMUZ#9]") ve `_zaten_var()`in
    # `LIKE` deseni tutmuyor -- yani aktarım idempotent olmaktan çıkıyor,
    # ikinci çalıştırma aynı tedaviyi bir daha açıyor. Ağustosta işaret
    # kısa olduğu için (etiketsiz) rastgele sığıyordu; `kaynak=TEMMUZ`
    # altı karakter uzatınca 86 satırın 60'ında bölündü. Tek başına bir
    # satır olarak 68'in çok altında, hiçbir etiketle bölünemez.
    p.append(_isaret(r["kimlik"]))
    return "\n".join(textwrap.fill(satir, 68) for satir in p)


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


def _cycle_ac(b, r, hasta_id, rapor) -> tuple:
    """Tedaviyi açar. (cycle_id, cycle_no) döner."""
    tarih = r["tarih"]
    yil = tarih[:4] if tarih else str(_dt.date.today().year)
    cycle_no = _lab_no(b, yil)
    sira = (b.execute("SELECT MAX(hasta_cycle_no) FROM cycle WHERE hasta_id=?",
                      (hasta_id,)).fetchone()[0] or 0) + 1
    _tel, endikasyon, _kalan = _gizli_notu_coz(r["gizli_not"])

    sebep = _iptal_sebebi(r["notlar"])
    if sebep:
        durum, bitis = "iptal", sebep
        bitis_zamani = r["transfer"] or r["opu"]
    elif r["transfer"] and r["transfer_adet"]:
        durum, bitis, bitis_zamani = "tamamlandi", "transfer", r["transfer"]
    elif r["dondurulan"] or _dondurma_sozu(r["notlar"]):
        # Yumurta dondurmada sayı alanı boş (embriyo kolonu) ama not açıkça
        # "16 ADET OOSİT ... DONDURULARAK SAKLANDI" diyor -- iptal notunda
        # olduğu gibi, kaynak kaydın kendi cümlesine güveniliyor.
        gun = _asama_gunu(r["dondurma_asama"]) or 0
        durum, bitis = "tamamlandi", "dondurma"
        bitis_zamani = _gun_ekle(r["opu"], gun) if r["opu"] else None
    else:
        # Kaynak kayıt ne transfer ne dondurma diyor, iptal de demiyor.
        # Uydurulmuyor: tedavi "tamamlandı" olarak kapanıyor (yapılacaklar
        # listesini ağustos işiyle doldurmasın diye) ama sebep boş kalıyor.
        # `cycle_detay.html` bu durumu zaten biliyor: sebep yoksa
        # "Tamamlandı" rozeti basıyor.
        durum, bitis = "tamamlandi", None
        bitis_zamani = r["transfer"] or r["opu"]

    opu_zamani = _zaman(r["opu"], "09:00:00") if r["tip"] not in FET_TIPLERI else None
    b.execute(
        "INSERT INTO cycle (lab_id, hasta_id, cycle_no, hasta_cycle_no, "
        " cycle_tipi, endikasyon, protokol_notu, opu_zamani, denudasyon_zamani, "
        " opu_hekim, opu_sag_oosit, durum, bitis_sebebi, bitis_zamani, "
        " olusturma_zamani) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (_db.LAB_ID, hasta_id, cycle_no, sira, r["tip"], endikasyon,
         _not_kur(r), opu_zamani, _zaman(r["opu"], "11:00:00"),
         r["opu_hekim"], r["toplanan"] or None, durum, bitis,
         _zaman(bitis_zamani, "16:00:00"), _zaman(tarih, "08:30:00")))
    cycle_id = b.execute("SELECT last_insert_rowid()").fetchone()[0]
    rapor.append(f'    tedavi {cycle_no} ({sira}. tedavi, {r["tip"]}) — '
                 f'{durum}{" / " + bitis if bitis else ""}')
    return cycle_id, cycle_no


def _specimen_ac(b, cycle_id, cycle_no, sira, durum, zaman) -> str:
    sid = f"{cycle_no}-{sira:02d}"
    b.execute("INSERT INTO specimen (id, lab_id, cycle_id, cycle_sira_no, "
              "durum, olusturma_zamani) VALUES (?,?,?,?,?,?)",
              (sid, _db.LAB_ID, cycle_id, sira, durum, zaman))
    return sid


def _oositleri_ac(b, r, cycle_id, cycle_no, kid, rapor):
    """Toplanan oosit kadar kayıt açar, sayılara uyan olayları yazar.

    Dağıtım sırası **tek yerde burada**: önce MII, sonra immatür, sonra
    empty zona / dejenere / atretik. ICSI listenin başından veriliyor
    (yani önce MII'lere), fertilizasyon da işlem görenlerin başından.
    Hangi oositin hangisi olduğu kaynak kayıtta yok -- docstring'de yazılı.
    """
    n = r["toplanan"] or 0
    if not n:
        return
    opu = r["opu"]
    t_denud = _zaman(opu, "11:00:00")
    t_icsi = _zaman(opu, "13:00:00")
    t_fert = _zaman(_gun_ekle(opu, 1), "09:00:00") if opu else t_icsi

    plan = (["mii"] * r["mii"] + ["mi"] * r["immatur"] +
            [None] * r["empty_zona"] + ["degenere"] * r["dejenere"] +
            ["atretik"] * r["atretik"])
    plan = (plan + [None] * n)[:n]        # sayılar tutmazsa kalanı boş geçer

    oositler = []
    for i, mat in enumerate(plan, start=1):
        sid = _specimen_ac(b, cycle_id, cycle_no, i, "oosit", t_denud)
        oositler.append([sid, mat, None])          # [id, maturasyon, durum]
        if mat:
            # oosit_cryo'da bu soru denüdasyon ekranında soruluyor, ivf_icsi'de
            # ICSI ekranında -- ikisi de aynı olay tipini yazıyor (v6.96).
            _olay(b, kid, sid, cycle_id, "maturasyon_kontrolu", t_denud,
                  mat_deger=mat)

    # --- ICSI: önce MII'ler, yetmezse immatürler (bir satırda işlem sayısı
    #     MII'den fazla: 12 MII / 13 işlem -- kaynak kayıt öyle diyor).
    islenen = min(r["islenen"] or 0, n)
    enjekte = oositler[:islenen]
    dejenere_olan = enjekte[len(enjekte) - (r["islem_dejenere"] or 0):] \
        if r["islem_dejenere"] else []
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
    rapor.append(f'    {n} oosit, {r["mii"]} MII, {islenen} ICSI, '
                 f'{r["iki_pn"]} 2PN')


def _degerlendirme_yaz(b, kid, sid, cycle_id, tip, gun, zaman, alanlar, ham):
    """Aşama değerlendirmesini yazar; varsa **üzerine yazar**, ikinci kayıt açmaz.

    "tamamla" kipi aktarılmış bir tedaviyi ikinci kez işleyebilsin diye
    idempotent: aynı örneğe aynı tipte iptal edilmemiş bir olay varsa o
    güncelleniyor.
    """
    notu = f"Kaynak kayıttaki yazım: {ham}"
    var = b.execute("SELECT id FROM olay WHERE specimen_id=? AND tip=? "
                    "AND iptal_mi=0 ORDER BY id LIMIT 1", (sid, tip)).fetchone()
    if var:
        atama = ", ".join(f"{k}=?" for k in alanlar)
        b.execute(f"UPDATE olay SET {atama}, gun=?, notlar=? WHERE id=?",
                  list(alanlar.values()) + [gun, notu, var[0]])
    else:
        _olay(b, kid, sid, cycle_id, tip, zaman, gun=gun, notlar=notu, **alanlar)


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


def _vitrifikasyon_var(b, cycle_id) -> bool:
    """Bu tedavide taşıyıcıya bağlı, iptal edilmemiş bir dondurma var mı?"""
    return bool(b.execute(
        "SELECT 1 FROM olay o JOIN specimen s ON s.id=o.specimen_id "
        "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
        "AND o.vit_tasiyici_id IS NOT NULL LIMIT 1", (cycle_id,)).fetchone())


# Blastokist dışı kodların `specimen.durum` karşılığı -- `app.blast_kaydet()`
# ile aynı eşleme. Blastokist (sayı) genişlemelerde durum "blastokist".
_BLAST_DURUM = {"kavitasyon": "kavitasyon", "arrest": "arrest",
                "morula": "morula", "erken_morula": "morula"}


def _dondurma_kayitlari(b, r, cycle_id, kid, rapor):
    """Nottan çözümlenen dondurmayı ilgili aşama ekranlarına yazar.

    Kullanıcının isteği (2026-09-22): "4BB blastokist dondurulmuş yazıyor ise
    blastokist bölümüne fotoğrafsız 4BB embriyo kaydedip vitrifikasyonda da
    bunun dondurulduğunu ilgili bölüme yaz."

    Üç şey yazılıyor:
    1. **Değerlendirme** — gün 5 ve sonrası `blastokist_degerlendirme`
       (`bl_genisleme`/`bl_icm`/`bl_te` ya da kavitasyon + derece), öncesi
       `cleavage_degerlendirme` (`cl_hucre_sayisi`/`cl_skor`).
    2. **Taşıyıcı** — her parantez grubu bir tüp (`_dondurma_coz()`'e bak),
       etiketi `vit_ekran()`'in önerdiği kalıpta.
    3. **Vitrifikasyon olayı** — taşıyıcıya bağlı, yani vitrifikasyon
       ekranının "Dondurulmuş" listesinde ve Cryo Haritası'nda görünüyor.

    **İdempotent**: hem taze aktarımda hem "tamamla" kipinde çağrılıyor.
    Değerlendirme varsa güncelleniyor; taşıyıcıya bağlı bir dondurma zaten
    varsa dondurma kısmına hiç dokunulmuyor (kullanıcı konumu elle girmiş
    olabilir, üzerine yazmak onu silerdi).
    """
    coz = _dondurma_coz(r["notlar"], r["dondurma_asama"], r["tip"])
    if not coz:
        return
    if not coz["gruplar"]:
        # Dondurma cümlesi var ama kaç örnek/tüp olduğu yazmıyor (parantez
        # grubu yok) -- neyin yazılacağı bilinemez. Önceden burada da
        # sessizce dönülüyordu; #33'ün dersi (v6.142): dondurulmuş bir
        # örnek tankta durup programda görünmüyorsa bu SÖYLENMELİ.
        # Temmuz ve ağustos dosyalarında böyle satır yok (ölçüldü).
        rapor.append("    UYARI: notta dondurma var ama kaç örnek/tüp olduğu "
                     "okunamadı -- dondurma kaydı yazılmadı")
        return
    cycle_no = b.execute("SELECT cycle_no FROM cycle WHERE id=?",
                         (cycle_id,)).fetchone()[0]
    # FET'te çözme SONRASI yeniden dondurma (v6.143, kullanıcının isteği:
    # "Çözülen embriyo aynı FET tedavisinde yeniden dondurulabilsin ve tüp
    # Cryo Haritası'na girsin"). Temmuzda bir FET notu: "KÜLTÜRE EDİLEN
    # TRANSFER FAZLASI 1 ADET D5 EMBRİYOSU (1CC) ŞEKLİNDE DONDURULARAK
    # SAKLANDI". v6.142 bunu yazmıyor, uyarıyordu; program artık destekliyor
    # (`vit_cycle_id`, goc_046). Farkları aşağıda: hedef örnekler, tarih ve
    # dondurmanın hangi tedavide yapıldığı.
    fet = r["tip"] in FET_TIPLERI

    if not fet:
        # v6.131'in ilk yazışındaki taşıyıcısız vitrifikasyon olayları iptal
        # ediliyor: istatistikte "donduruldu" derken ekranda "aday"
        # görünüyorlardı. FET'te öyle kayıt hiç yazılmadı.
        eski = b.execute(
            "SELECT o.id FROM olay o JOIN specimen s ON s.id=o.specimen_id "
            "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
            "AND o.vit_tasiyici_id IS NULL", (cycle_id,)).fetchall()
        for (oid,) in eski:
            b.execute("UPDATE olay SET iptal_mi=1, iptal_kullanici_id=?, "
                      "iptal_zamani=?, iptal_sebep=? WHERE id=?",
                      (kid, _dt.datetime.now().isoformat(" ", "seconds"),
                       "Tasiyicili kayitla degistirildi", oid))

    gun = coz["gun"] or 5
    oosit_mi = coz["oosit_mi"]
    if fet:
        # FET'te OPU yok. Kaynak kayıtta yalnızca transfer günü var; kültürün
        # kaçıncı güne sürdüğü yazmıyor -- değerlendirme ve dondurma o güne,
        # transferden (12:00) sonraya yazılıyor. Program öncesi kayıtların
        # bütün saatleri gibi yaklaşık (v6.130); gün ise nottaki ("D5").
        temel = _zaman(r["transfer"], "14:00:00") if r["transfer"] else None
        t_deg = _zaman(r["transfer"], "13:00:00") if r["transfer"] else None
        eksik_tarih = "transfer"
    else:
        # Yumurta dondurma OPU günü, denüdasyondan sonra; embriyo dondurma
        # kaynak kaydın söylediği gün ("5,GÜN" / "3.GÜN").
        temel = (_zaman(r["opu"], "14:00:00") if oosit_mi
                 else _zaman(_gun_ekle(r["opu"], gun), "12:00:00")) if r["opu"] else None
        t_deg = _zaman(_gun_ekle(r["opu"], gun), "09:00:00") if r["opu"] else None
        eksik_tarih = "OPU"
    if not temel:
        rapor.append(f"    UYARI: {eksik_tarih} tarihi yok, dondurma kaydı "
                     "yazılamadı")
        return

    # Hedef örnekler: yumurtada MII olanlar, embriyoda 2PN olanlar; FET'te bu
    # tedavide çözülüp canlı/kısmi hasarlı çıkan ve transfer edilmeyenler
    # (FET'in embriyoları FET'in kendi altında, v6.130). Hepsinde daha önce
    # dondurulmuş işaretlenenler öne alınıyor ki "tamamla" aynı örneklere
    # denk gelsin.
    secili, gorulen = [], set()
    sorgular = ["SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
                "WHERE s.cycle_id=? AND o.tip='vitrifikasyon' "
                "GROUP BY s.id ORDER BY s.cycle_sira_no"]
    if fet:
        sorgular.append(
            "SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
            "WHERE s.cycle_id=? AND o.iptal_mi=0 AND o.tip='thaw' "
            "AND COALESCE(o.thaw_sagkalim, '') <> 'degenere' "
            "AND NOT EXISTS (SELECT 1 FROM olay tr WHERE tr.specimen_id=s.id "
            "                AND tr.tip='transfer' AND tr.iptal_mi=0) "
            "GROUP BY s.id ORDER BY s.cycle_sira_no")
    else:
        sorgular.append(
            "SELECT s.id FROM specimen s JOIN olay o ON o.specimen_id=s.id "
            "WHERE s.cycle_id=? AND o.iptal_mi=0 AND " +
            ("o.tip='maturasyon_kontrolu' AND o.mat_deger='mii'" if oosit_mi else
             "o.tip='fertilizasyon_kontrolu' AND o.fert_pn_sayisi='2'") +
            " GROUP BY s.id ORDER BY s.cycle_sira_no")
    for sorgu in sorgular:
        for (sid,) in b.execute(sorgu, (cycle_id,)).fetchall():
            if sid not in gorulen:
                gorulen.add(sid)
                secili.append(sid)

    zaten = _vitrifikasyon_var(b, cycle_id)
    # Yeniden dondurmada dondurmanın yapıldığı tedavi bu FET (`vit_cycle_id`,
    # goc_046) -- programın kendi FET vitrifikasyon ekranının yazdığıyla aynı.
    ek_vit = {"vit_cycle_id": cycle_id} if fet else {}
    vit_notu = ("Kaynak kayıttaki dondurma notundan aktarıldı (çözme sonrası "
                "yeniden dondurma); konum girilmedi." if fet else
                "Kaynak kayıttaki dondurma notundan aktarıldı; konum girilmedi.")
    sira, tup_no, yazilan, tupler = 0, 0, [], []
    for grup in coz["gruplar"]:
        ogeler = [o for o in grup if o["tur"] in ("blast", "cleavage", "oosit")]
        if not ogeler:
            continue
        adet = (sum(o["adet"] for o in ogeler) if oosit_mi else len(ogeler))
        payi = secili[sira:sira + adet]
        sira += adet
        if not payi:
            break

        tid = etiket = None
        if not zaten:
            an = (_dt.datetime.fromisoformat(temel)
                  + _dt.timedelta(minutes=tup_no)).isoformat(" ", "seconds")
            tid, etiket, an = _tasiyici_ac(b, kid, cycle_no, an)
            tupler.append(f"{etiket} ({len(payi)})")
        tup_no += 1

        for i, sid in enumerate(payi):
            if not oosit_mi:
                o = ogeler[i]
                if o["tur"] == "blast":
                    alanlar = {"bl_genisleme": o["genisleme"], "bl_icm": o.get("icm"),
                               "bl_te": o.get("te"), "bl_derece": o.get("derece"),
                               "bl_skor": o["skor"], "bl_skor_kaynagi": "elle"}
                    _degerlendirme_yaz(b, kid, sid, cycle_id,
                                       "blastokist_degerlendirme", max(gun, 4),
                                       t_deg, alanlar, o["ham"])
                else:
                    alanlar = {"cl_hucre_sayisi": o["hucre"], "cl_skor": o["skor"],
                               "cl_skor_kaynagi": "elle"}
                    _degerlendirme_yaz(b, kid, sid, cycle_id,
                                       "cleavage_degerlendirme", min(gun, 3),
                                       t_deg, alanlar, o["ham"])
                yazilan.append(o["ham"])
            if tid:
                _olay(b, kid, sid, cycle_id, "vitrifikasyon", an,
                      vit_tasiyici_id=tid, notlar=vit_notu, **ek_vit)
                _durum_yaz(b, sid, "dondurulmus")

    if sira > len(secili):
        rapor.append(f"    UYARI: notta {sira} örnek yazıyor ama {len(secili)} "
                     f"uygun kayıt var; fazlası yazılmadı")
    taninmayan = [o["ham"] for g in coz["gruplar"] for o in g
                  if o["tur"] == "taninmadi"]
    if yazilan:
        rapor.append(f'    skorlar: {", ".join(yazilan)} (gün {gun})'
                     + (f' — tanınmayan: {", ".join(taninmayan)}' if taninmayan else ""))
    if tupler:
        rapor.append(f'    dondurma: {len(tupler)} tüp — {", ".join(tupler)} '
                     f'(konum boş, Cryo Haritası\'ndan gir)')
    elif zaten:
        rapor.append("    dondurma zaten girilmiş, dokunulmadı")


def _fet_embriyolari(b, r, cycle_id, cycle_no, kid, rapor):
    """FET'te çözülen/transfer edilen embriyolar (docstring: "FET" bölümü)."""
    adet = max(r["cozulen"] or 0, r["transfer_adet"] or 0)
    if not adet:
        rapor.append("    çözülen/transfer sayısı kaynak kayıtta yok, "
                     "embriyo kaydı açılmadı")
        return
    t_thaw = _zaman(r["transfer"], "09:00:00")
    t_tr = _zaman(r["transfer"], "12:00:00")
    kaliteler = [f"{h}{k}" for h, k in (r["emb1"], r["emb2"]) if h or k]

    embriyolar = []
    for i in range(1, adet + 1):
        sid = _specimen_ac(b, cycle_id, cycle_no, i, "oosit", t_thaw)
        # Transfer edilen embriyo mutlaka çözülmüştür; `thaw_cycle_id` bu
        # tedaviyi gösteriyor (CLAUDE.md: "hangi tedavi için çözüldü").
        _olay(b, kid, sid, cycle_id, "thaw", t_thaw, thaw_cycle_id=cycle_id,
              thaw_sagkalim="canli" if (r["viabilite"] or 0) > 0 else None,
              thaw_canlilik=r["viabilite"])
        _durum_yaz(b, sid, "cozuldu")
        embriyolar.append(sid)

    for i, sid in enumerate(embriyolar[:r["transfer_adet"] or 0]):
        _olay(b, kid, sid, cycle_id, "transfer", t_tr, tr_cycle_id=cycle_id,
              notlar=(f'Aşama: {r["transfer_asama"]}. ' if r["transfer_asama"] else "")
                     + (f'Embriyo: {kaliteler[i]}' if i < len(kaliteler) else ""))
        _durum_yaz(b, sid, "transfer_edildi")
    rapor.append(f'    {adet} embriyo çözüldü, {r["transfer_adet"] or 0} '
                 f'transfer edildi')


def _androloji(b, r, cycle_id, kid):
    """`sperm_ornek` + iki `sperm_analiz` (bazal / hazırlık sonrası)."""
    if not (r["sperm_kaynak"] or r["bazal"]["konsantrasyon_milyon_ml"]):
        return
    t_al = _zaman(r["opu"], "08:00:00")
    b.execute("INSERT INTO sperm_ornek (lab_id, cycle_id, alinma_zamani, "
              "alinma_yontemi, hacim_ml, hazirlama_yontemi, hazirlama_zamani, "
              "kullanici_id, notlar, olusturma_zamani) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (_db.LAB_ID, cycle_id, t_al,
               _ALINMA.get(_sade(r["sperm_kaynak"])), r["bazal"]["hacim_ml"],
               _HAZIRLAMA.get(_sade(r["hazirlama"])), _zaman(r["opu"], "10:00:00"),
               kid,
               f'Kaynak kayıt: {r["sperm_kaynak"]} / {r["hazirlama"]}'.strip(" /"),
               t_al))
    ornek_id = b.execute("SELECT last_insert_rowid()").fetchone()[0]
    for asama, veri, zaman in (("bazal", r["bazal"], t_al),
                               ("hazirlik_sonrasi", r["hazirlik"],
                                _zaman(r["opu"], "10:00:00"))):
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
    zamanlar = {"opu": _zaman(r["opu"], "09:00:00"),
                "androloji": _zaman(r["opu"], "10:00:00"),
                "icsi": _zaman(r["opu"], "13:00:00"),
                "transfer": _zaman(r["transfer"], "12:00:00")}
    for asama, ad in r["yapan"].items():
        if not ad:
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
    return _db.tek("SELECT c.id, c.cycle_no, h.dosya_no FROM cycle c "
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
        if r["tip"] in FET_TIPLERI:
            _fet_embriyolari(b, r, cycle_id, cycle_no, kid, rapor)
            # Çözme sonrası yeniden dondurma (v6.143) -- çözme kayıtları bir
            # satır yukarıda, aynı işlemde yazıldı; hedef örnekleri onlar.
            _dondurma_kayitlari(b, r, cycle_id, kid, rapor)
        else:
            _oositleri_ac(b, r, cycle_id, cycle_no, kid, rapor)
            _dondurma_kayitlari(b, r, cycle_id, kid, rapor)
            _androloji(b, r, cycle_id, kid)
        _islem_yapan(b, r, cycle_id)
    return rapor


def _ozet_satiri(r) -> str:
    sebep = _iptal_sebebi(r["notlar"])
    if sebep:
        son = f"İPTAL ({sebep})"
    elif r["transfer"] and r["transfer_adet"]:
        son = "tamamlandı / transfer"
    elif r["dondurulan"] or _dondurma_sozu(r["notlar"]):
        son = "tamamlandı / dondurma"
    else:
        son = "tamamlandı (sebep yok — kaynak kayıt söylemiyor)"
    if r["tip"] in FET_TIPLERI:
        icerik = (f'{max(r["cozulen"] or 0, r["transfer_adet"] or 0)} embriyo '
                  f'çözme, {r["transfer_adet"] or 0} transfer')
    else:
        icerik = (f'{r["toplanan"]} oosit / {r["mii"]} MII / '
                  f'{r["islenen"]} ICSI / {r["iki_pn"]} 2PN / '
                  f'{r["dondurulan"]} dondurma')
    return (f'#{r["kimlik"]:>3}  dosya {r["dosya_no"]:<10} {r["tip"]:<11}'
            f'{r["tarih"] or "tarihsiz":<11} {icerik:<52} {son}')


def onizleme(satirlar):
    print(f"\nCSV'de {len(satirlar)} satır. Veritabanı: {DB}\n")
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
        coz = _dondurma_coz(r["notlar"], r["dondurma_asama"], r["tip"])
        if coz and coz["ogeler"]:
            # Kullanıcının kendi yazımı basılıyor ("4HG2"), çözümlenmiş kod
            # değil -- kendi notunda ne yazdığını tanıyabilmeli.
            ozet = ", ".join(o["ham"] for o in coz["ogeler"])
            print(f'        dondurulan ({"yumurta" if coz["oosit_mi"] else "embriyo"}'
                  + (f', gün {coz["gun"]}' if coz["gun"] else "") + f'): {ozet}'
                  + ("   <- çözme sonrası yeniden dondurma"
                     if r["tip"] in FET_TIPLERI else ""))
        elif coz:
            print("        dondurma notu var   <- kaç örnek/tüp olduğu "
                  "okunamadı, YAZILMAYACAK")
    print(f'\n{len(satirlar) - atlanan} tedavi yazılacak, {yeni_hasta} yeni '
          f'hasta kartı açılacak, {atlanan} satır atlanacak.')
    print("Yazmak için: python3 aktar_access.py <dosya.csv>\n")


def aktar(satirlar):
    toplam = {"tedavi": 0, "atlanan": 0, "hata": 0}
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if var:
            toplam["atlanan"] += 1
            print(f'#{r["kimlik"]:>3}  atlandı (zaten aktarılmış: {var["cycle_no"]})')
            continue
        try:
            rapor = _satiri_yaz(r)
        except Exception as hata:            # bir satır ötekileri durdurmasın
            toplam["hata"] += 1
            print(f'#{r["kimlik"]:>3}  HATA: {hata}')
            continue
        toplam["tedavi"] += 1
        print(f'#{r["kimlik"]:>3}  aktarıldı')
        for satir in rapor:
            print(satir)
    print(f'\nBitti. {toplam["tedavi"]} tedavi aktarıldı, '
          f'{toplam["atlanan"]} atlandı, {toplam["hata"]} hata.')


def tamamla(satirlar):
    """Zaten aktarılmış tedavilere nottan çözümlenen skorları ekler.

    Aktarım bir kez yapıldıktan sonra betiğin yeni bir sürümü çıktığında
    baştan almak gerekmesin diye: `_dondurma_kayitlari()` idempotent olduğu
    için var olan kayıtların üzerine yazıyor, yeni satır açmıyor.
    """
    kid = _kullanici_id()
    sayac = {"islenen": 0, "atlanan": 0, "hata": 0}
    for r in satirlar:
        var = _zaten_var(r["kimlik"])
        if not var:
            sayac["atlanan"] += 1
            print(f'#{r["kimlik"]:>3}  aktarılmamış, atlandı')
            continue
        rapor = []
        try:
            with _db.yazma_islemi() as b:
                _dondurma_kayitlari(b, r, var["id"], kid, rapor)
        except Exception as hata:
            sayac["hata"] += 1
            print(f'#{r["kimlik"]:>3}  HATA: {hata}')
            continue
        sayac["islenen"] += 1
        if rapor:
            print(f'#{r["kimlik"]:>3}  {var["cycle_no"]}')
            for satir in rapor:
                print(satir)
    print(f'\nBitti. {sayac["islenen"]} tedavi gözden geçirildi, '
          f'{sayac["atlanan"]} atlandı, {sayac["hata"]} hata.')


def main():
    global KAYNAK
    arg = [a for a in sys.argv[1:] if not a.lower().startswith("kaynak=")]
    for a in sys.argv[1:]:
        if a.lower().startswith("kaynak="):
            KAYNAK = _kaynak_ayikla(a.split("=", 1)[1])
    kip = "aktar"
    if arg and arg[0] in ("liste", "tamamla"):
        kip, arg = arg[0], arg[1:]
    if not arg:
        sys.exit("Kullanim:\n"
                 "  python3 aktar_access.py liste <dosya.csv>     ne yazilacagini gosterir\n"
                 "  python3 aktar_access.py <dosya.csv>           aktarir\n"
                 "  python3 aktar_access.py tamamla <dosya.csv>   zaten aktarilmis\n"
                 "                                                tedavilere nottaki\n"
                 "                                                skorlari ekler\n"
                 "\n"
                 "  kaynak=<AD>  ikinci bir Access dosyasi aktarilirken sart:\n"
                 "               her dosya kendi kayitlarini 1'den numaraliyor,\n"
                 "               etiket numarayi dosyasina bagliyor.\n"
                 "               ornek: python3 aktar_access.py kaynak=TEMMUZ temmuz.csv")
    satirlar = satirlari_oku(arg[0])
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
        onizleme(satirlar)
        return
    # Yazmadan önce: araç göçleri kendisi çalıştırmıyor, program açılışta
    # çalıştırıyor (v6.49). `git pull`'dan sonra program yeniden açılmadıysa
    # FET'in yeniden dondurması `vit_cycle_id`'yi (goc_046) yazarken işlemin
    # ortasında patlardı -- baştan, hiçbir şey yazmadan söyle.
    if not _db.yeniden_dondurma_var():
        sys.exit("Veritabani guncellemesi eksik (goc_046). Programi bir kez "
                 "kapatip ac -- guncellemeler acilista uygulanir -- ya da "
                 "`python3 goc_hepsi.py` calistir, sonra tekrar dene.")
    if kip == "tamamla":
        tamamla(satirlar)
        return
    onizleme(satirlar)
    print("Bu, veritabanina YAZAR. Once yedek al (/yedekleme -> Simdi yedekle).")
    if input("Devam etmek icin AKTAR yaz: ").strip() != "AKTAR":
        sys.exit("Vazgecildi, hicbir sey yazilmadi.")
    aktar(satirlar)


if __name__ == "__main__":
    main()
