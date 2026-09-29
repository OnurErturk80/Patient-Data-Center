"""Arayüz metinleri — iki dil, tek sözlük.

Neden gettext/babel değil: bu projede framework yok, build adımı yok.
`.po` dosyası derlemek yeni bir kurulum adımı demek olurdu. Düz bir sözlük
hem yeterli hem de kullanıcının kendi düzeltebileceği bir şey.

**Dil lab başına tektir**, kullanıcı başına değil. Yönetici bir kez seçer,
bütün program o dile geçer (karar: CLAUDE.md bekleyen iş 8).

Kullanım:
    şablonda   {{ metin("kaydet") }}
    app.py'de  metinler.t("kaydet")

Şablondaki adı bilerek `t` değil: on iki şablon `{% for t in ... %}` diye
döngü değişkeni olarak `t` kullanıyor ve döngünün içinde `t(...)` çağrısı
sessizce patlardı. `metin` çakışmıyor ve projenin Türkçe adlandırmasına uyuyor.

Anahtar bulunamazsa anahtarın kendisi döner — ekranda `kaydet` diye çıplak
görünür, yani eksik çeviri gözden kaçmaz.

**Klinik terimler çevrilmez** (blastocyst, ICSI, PN, ICM, TE, FET, MII…) —
iki dilde de aynı kalır. Açılır menülerdeki seçenekler burada değil,
veritabanındaki `liste_degeri` tablosunda.
"""

import contextvars

DILLER = [("tr", "Türkçe"), ("en", "English")]
VARSAYILAN = "tr"

# İstek başına geçerli dil. Middleware başta bir kez ayarlar; `t()` buradan
# okur. Giriş yapılmamış sayfalarda da geçerli olmalı — giriş ekranı da
# çevriliyor.
_DIL = contextvars.ContextVar("dil", default=VARSAYILAN)


def dil_ayarla(kod: str):
    """Bu istek için dili ayarla. Geri alma jetonu döndürür."""
    return _DIL.set(kod if kod in dict(DILLER) else VARSAYILAN)


def dil_sifirla(jeton) -> None:
    _DIL.reset(jeton)


def dil() -> str:
    return _DIL.get()


def t(anahtar: str) -> str:
    """Anahtarın geçerli dildeki karşılığı."""
    kayit = METINLER.get(anahtar)
    if kayit is None:
        return anahtar
    return kayit.get(dil()) or kayit.get(VARSAYILAN) or anahtar


def say(anahtar: str, n) -> str:
    """Sayılı metin: "3 embriyo" / "3 embryos", "1 embriyo" / "1 embryo".

    İngilizce 1 için tekil biçim ister; Türkçede sayıdan sonra çoğul eki
    kullanılmaz, tek biçim yeter. n == 1 iken `<anahtar>_tekil` varsa o
    kullanılır, yoksa normal biçime düşülür — tekil biçim tanımlamak
    isteğe bağlı.
    """
    if n == 1 and (anahtar + "_tekil") in METINLER:
        return t(anahtar + "_tekil").format(n=n)
    return t(anahtar).format(n=n)


def yuzde(deger) -> str:
    """Yüzde işareti dile göre yer değiştirir: Türkçe %90, İngilizce 90%.

    Kolon REAL olduğu için 10 değeri 10.0 diye okunuyor; tam sayıysa ondalık
    kısım yazılmaz — ekranda "%10.0" değil "%10" görünsün.
    """
    if deger is None:
        return ""
    if isinstance(deger, float) and deger.is_integer():
        deger = int(deger)
    return f"%{deger}" if dil() == "tr" else f"{deger}%"


METINLER = {
    # ---- program ve genel ----
    "program_adi": {"tr": "Patient Data Center", "en": "Patient Data Center"},
    "giris_aciklama": {
        "tr": "IVF laboratuvarının hasta, tedavi ve yumurta kayıtlarını tuttuğu "
              "program. Klinik içi ağda çalışır, veriler bu cihazın dışına "
              "çıkmaz.",
        "en": "Keeps this IVF lab's patient, cycle and oocyte records. Runs "
              "on the clinic's own network — data never leaves this device."},
    "kaydet": {"tr": "Kaydet", "en": "Save"},
    "iptal": {"tr": "İptal", "en": "Cancel"},
    # Durum rozeti — düğme değil. Ayrıca Türkçe "İptal"i küçültmek
    # "i" + ayrı nokta üretiyor (i̇ptal), o yüzden hazır küçük yazılı.
    "iptal_rozet": {"tr": "iptal", "en": "cancelled"},
    "geri": {"tr": "Geri", "en": "Back"},
    "sil": {"tr": "Sil", "en": "Delete"},
    "evet": {"tr": "Evet", "en": "Yes"},
    "hayir": {"tr": "Hayır", "en": "No"},
    "girilmedi": {"tr": "girilmedi", "en": "not entered"},
    "aktif": {"tr": "aktif", "en": "active"},
    "pasif": {"tr": "PASİF", "en": "INACTIVE"},

    # ---- giriş ----
    "giris": {"tr": "Giriş", "en": "Sign in"},
    "giris_yap": {"tr": "Giriş yap", "en": "Sign in"},
    "cikis": {"tr": "Çıkış", "en": "Sign out"},
    "kullanici_adi": {"tr": "Kullanıcı adı", "en": "Username"},
    "sifre": {"tr": "Şifre", "en": "Password"},
    "giris_hatali": {"tr": "Kullanıcı adı veya şifre hatalı.",
                     "en": "Incorrect username or password."},
    "sifre_degisti_gir": {"tr": "Şifre değiştirildi. Yeni şifrenle giriş yap.",
                          "en": "Password changed. Sign in with your new password."},

    # ---- şifre değiştirme ----
    "sifre_degistir": {"tr": "Şifre değiştir", "en": "Change password"},
    "mevcut_sifre": {"tr": "Mevcut şifre", "en": "Current password"},
    "sifreyi_degistir": {"tr": "Şifreyi değiştir", "en": "Change password"},
    "yeni_sifre": {"tr": "Yeni şifre", "en": "New password"},
    "yeni_sifre_tekrar": {"tr": "Yeni şifre (tekrar)", "en": "New password (repeat)"},
    "tekrar": {"tr": "Tekrar", "en": "Repeat"},
    "kullanici": {"tr": "Kullanıcı", "en": "User"},
    "en_az_n_karakter": {"tr": "En az {n} karakter.",
                         "en": "At least {n} characters."},
    "sifre_oturum_uyari": {
        "tr": "Şifre değişince bu hesabın <b>açık oturumları kapatılır</b> — "
              "telefonunda veya başka bir bilgisayarda açık kalan sayfalar "
              "dahil. Yeniden giriş yapman gerekecek.",
        "en": "Changing the password <b>signs this account out everywhere</b> — "
              "including pages left open on a phone or another computer. "
              "You will need to sign in again."},
    "sifre_bilmiyorsan": {
        "tr": "Mevcut şifreni bilmiyorsan bu ekran işe yaramaz —",
        "en": "This screen is no use if you do not know your current password —"},

    # ---- şifremi unuttum ----
    "sifremi_unuttum": {"tr": "Şifremi unuttum", "en": "Forgot password"},
    "sifre_nasil_sifirlanir": {"tr": "Şifre nasıl sıfırlanır",
                               "en": "How to reset a password"},
    "sifre_sifirlama_metin": {
        "tr": "Şifreler geri okunamayacak şekilde saklanıyor — kimse mevcut "
              "şifreni göremez, ancak <b>yenisiyle değiştirilebilir</b>."
              "<br><br><b>Laboratuvarın yöneticisine başvur.</b> Yönetici, "
              "kullanıcı yönetimi ekranından sana yeni bir şifre verebilir.",
        "en": "Passwords are stored so that they cannot be read back — nobody "
              "can see your current password, but it <b>can be replaced</b>."
              "<br><br><b>Ask your laboratory administrator.</b> They can set "
              "a new password for you from the user management screen."},
    "sifre_sifirlama_ipucu": {
        "tr": "Bu ekran şifre sıfırlamaz. Sistemde e-posta veya SMS doğrulaması "
              "olmadığı için, kim olduğunu doğrulamadan şifre değiştirmek "
              "programı ağdaki herkese açık hale getirirdi.<br><br>"
              "Yönetici de giriş yapamıyorsa, programın kurulu olduğu "
              "bilgisayarda terminalden "
              "<code>python3 kullanici.py sifre &lt;kullanıcı adı&gt;</code> "
              "komutu çalıştırılmalı.",
        "en": "This screen does not reset anything. There is no e-mail or SMS "
              "verification in this system, so changing a password without "
              "proving who you are would open the program to everyone on the "
              "network.<br><br>If the administrator is locked out too, run "
              "<code>python3 kullanici.py sifre &lt;username&gt;</code> in a "
              "terminal on the computer where the program is installed."},
    "giris_ekranina_don": {"tr": "Giriş ekranına dön", "en": "Back to sign in"},

    # ---- hasta formu ----
    "dosya_no": {"tr": "Dosya no", "en": "File no"},
    "dosya_no_tek": {"tr": "Aynı dosya no ikinci kez kaydedilemez.",
                     "en": "The same file no cannot be recorded twice."},
    "dogum_tarihi": {"tr": "Doğum tarihi", "en": "Date of birth"},
    "yas_hesaplanir": {"tr": "Yaş bundan hesaplanır, ayrıca girilmez.",
                       "en": "Age is calculated from this; do not enter it "
                             "separately."},
    "telefon": {"tr": "Telefon", "en": "Phone"},
    "es_adi": {"tr": "Eş adı", "en": "Partner name"},
    "es_dogum_tarihi": {"tr": "Eş doğum tarihi", "en": "Partner date of birth"},
    "es_telefon": {"tr": "Eş telefonu", "en": "Partner phone"},
    # Eşin kendi dosya numarası (v6.139). v6.125'in kapsamadığı durum:
    # erkek hasta çiftin dosyasından bağımsız bir numarayla kayıtlı.
    "es_dosya_no": {"tr": "Eşin dosya numarası", "en": "Partner file no"},
    "es_dosya_no_ipucu": {
        "tr": "Eşin kendi hasta kaydı varsa (örn. onkoloji öncesi sperm "
              "dondurma) numarasını yaz — dondurulmuş spermi hasta kartında "
              "görünür ve tedaviye bağlanabilir.",
        "en": "If the partner has his own patient record (e.g. sperm frozen "
              "before oncology treatment), enter his file number — his frozen "
              "sperm then appears on this card and can be linked to a cycle."},
    "hastayi_kaydet": {"tr": "Hastayı kaydet", "en": "Save patient"},
    "mukerrer_dosya_no": {"tr": "Bu dosya no zaten kayıtlı:",
                          "en": "This file no is already registered:"},
    "kaydi_ac": {"tr": "kaydı aç", "en": "open the record"},

    # ---- hasta düzenleme ----
    "hastayi_duzenle": {"tr": "Hastayı düzenle", "en": "Edit patient"},
    "dosya_no_degismez": {
        "tr": "Dosya no değiştirilemez. Yanlışsa kayıt silinip yeniden açılmalı.",
        "en": "The file no cannot be changed. If it is wrong, the record must "
              "be deleted and created again."},
    "degisiklikleri_kaydet": {"tr": "Değişiklikleri kaydet", "en": "Save changes"},
    "vazgec": {"tr": "Vazgeç", "en": "Discard"},

    # ---- değişiklik geçmişi ----
    "kayitli_degisiklikler": {"tr": "Kayıtlı değişiklikler",
                              "en": "Recorded changes"},
    "henuz_degisiklik_yok": {"tr": "Bu kayıtta henüz değişiklik yapılmamış.",
                             "en": "No changes have been made to this record yet."},

    # ---- cryo haritası ----
    "cryo_ara_ipucu": {"tr": "Etiket, konum, dosya no, hasta adı veya örnek kodu",
                       "en": "Label, location, file no, patient name or sample code"},
    "tanklar": {"tr": "Tanklar", "en": "Tanks"},
    "n_tasiyici": {"tr": "{n} taşıyıcı", "en": "{n} carriers"},
    "n_tasiyici_tekil": {"tr": "{n} taşıyıcı", "en": "{n} carrier"},
    "n_embriyo": {"tr": "{n} embriyo", "en": "{n} embryos"},
    # Sperm Dondurma haritası (v6.180): tank -> kanister -> goblet.
    "n_tup": {"tr": "{n} tüp", "en": "{n} tubes"},
    "kanister": {"tr": "Kanister", "en": "Canister"},
    "goblet": {"tr": "Goblet", "en": "Goblet"},
    # Erkeğin kartından eşin kaydını bağlama (v6.180).
    "esinin_kaydi": {"tr": "Eşinin tüp bebek kaydı", "en": "Partner's IVF record"},
    "es_bag_dosya_no": {"tr": "Eşinin dosya numarası", "en": "Partner's file no"},
    "es_bagla": {"tr": "Eşine bağla", "en": "Link to partner"},
    "es_bagi_kaldir": {"tr": "Bağı kaldır", "en": "Remove link"},
    "es_bagi_kaldir_onay": {"tr": "Eşle bağ kaldırılsın mı?",
                            "en": "Remove the link to this partner?"},
    "esin_kaydindan_baglanir": {
        "tr": "Tedaviye eşinin kaydından bağlanır (aşağıdan eşine bağlayın).",
        "en": "Linked to a treatment from the partner's record (link the partner below)."},
    "es_bagla_ipucu": {
        "tr": "Eşinin kaydına bu hastanın dosya numarası yazılır; dondurulmuş sperm "
              "orada görünür ve tedaviye oradan bağlanır.",
        "en": "This patient's file no is written into the partner's record; the "
              "frozen sperm appears there and is linked to a treatment from there."},
    "sperm_harita_ipucu": {"tr": "Tank → kanister → goblet",
                           "en": "Tank → canister → goblet"},
    "n_embriyo_tekil": {"tr": "{n} embriyo", "en": "{n} embryo"},
    # Yumurta dondurmada taşıyıcının içindekiler embriyo değil (v6.133,
    # kullanıcının isteği: "Yumurta donduruluyorsa Yumurta, Embriyo
    # donduruluyorsa Embriyo yazsın"). Seçimi `yumurta_mi()` yapıyor.
    "n_yumurta": {"tr": "{n} yumurta", "en": "{n} oocytes"},
    "n_yumurta_tekil": {"tr": "{n} yumurta", "en": "{n} oocyte"},
    "dolu_tasiyicilar": {"tr": "Dolu taşıyıcılar", "en": "Occupied carriers"},
    "konum_girilmemis": {"tr": "konum girilmemiş", "en": "location not entered"},
    "aramaya_uyan_tasiyici_yok": {"tr": "Bu aramaya uyan taşıyıcı yok.",
                                  "en": "No carriers match this search."},
    "henuz_dondurulmus_yok": {"tr": "Henüz dondurulmuş embriyo yok.",
                              "en": "No frozen embryos yet."},

    # ---- tank düzeni ve Excel kaydı (v6.189) ----
    "tank_duzeni_ipucu": {"tr": "Tank → kanister → goblet (her goblet 4 straw)",
                          "en": "Tank → canister → goblet (4 straws per goblet)"},
    "n_goblet": {"tr": "{n} goblet", "en": "{n} goblets"},
    "n_goblet_tekil": {"tr": "{n} goblet", "en": "{n} goblet"},
    "n_bos_yuva": {"tr": "{n} boş yuva", "en": "{n} free slots"},
    "n_bos_yuva_tekil": {"tr": "{n} boş yuva", "en": "{n} free slot"},
    "n_excel_kaydi": {"tr": "{n} Excel kaydı", "en": "{n} Excel records"},
    "n_excel_kaydi_tekil": {"tr": "{n} Excel kaydı", "en": "{n} Excel record"},
    "n_yeri_belirsiz": {"tr": "{n} gobleti belirsiz", "en": "{n} without goblet"},
    "ust_kati_var": {"tr": "üst katı var", "en": "has upper level"},
    # Yedek goblet (v6.192): Excel'de numarasız, "yer biterse diye" hazırlanmış kat.
    "ust_kati_yedek": {"tr": "üst katı yedek", "en": "upper level is reserve"},
    "alt_kat": {"tr": "Alt kat", "en": "Lower level"},
    "ust_kat": {"tr": "Üst kat", "en": "Upper level"},
    "ust_kat_yedek": {
        "tr": "Üst kat · yedek (yer biterse diye hazırlandı)",
        "en": "Upper level · reserve (prepared for when space runs out)"},
    "bos_yuva": {"tr": "boş yuva", "en": "free slot"},
    "goblet_bos": {"tr": "Excel'de satırı yok", "en": "No rows in the Excel"},
    "kapasite_bilinmiyor": {"tr": "kaç straw aldığı bilinmiyor",
                            "en": "capacity unknown"},
    "gobleti_belirsiz": {"tr": "Gobleti belirsiz", "en": "Goblet unknown"},
    "gobleti_belirsiz_ipucu": {
        "tr": "Bu kanisterde, ama yazılan goblet tank düzeninde yok ya da hiç "
              "yazılmamış.",
        "en": "In this canister, but the goblet written is not in the tank "
              "layout or was not written at all."},
    "yeri_belirsizler": {"tr": "Haritada yeri belirsiz", "en": "Location unknown"},
    "konumu_girilmemis_tupler": {"tr": "Konumu girilmemiş tüpler",
                                 "en": "Tubes without a location"},
    "konumu_girilmemis_ipucu": {
        "tr": "Tankta duruyor, yeri programda yok. Excel'le eşleşmeyen tüpler "
              "çoğunlukla bunlar: gobletinde duran Excel kaydından bağlanabilir.",
        "en": "In the tank, location not recorded. Usually the tubes that did "
              "not match the Excel: link them from the Excel record in their goblet."},
    "duzende_olmayan_konum": {"tr": "Tank düzeninde olmayan konum",
                              "en": "Location not in the tank layout"},
    "duzende_olmayan_konum_ipucu": {
        "tr": "Girilen yer (Tank / Kanister / Goblet) düzendeki hiçbir gobletle "
              "tutmuyor.",
        "en": "The location entered (tank / canister / goblet) matches no "
              "goblet in the layout."},
    "girilen_konum": {"tr": "Girilen konum", "en": "Location entered"},
    "excel_kaydi": {"tr": "Excel kaydı", "en": "Excel record"},
    "excel_kayitlari": {"tr": "Excel kayıtları", "en": "Excel records"},
    "excel_kaydi_ipucu": {
        "tr": "Cryo Haritası Excel'inde duran, programda tüpü bulunamamış satırlar",
        "en": "Rows of the cryo map Excel with no matching tube in the program"},
    "excel_kaydi_aciklama": {
        "tr": "Cryo Haritası Excel'inde bu gobletde duran ama programda karşılığı "
              "olan tüp bulunamayan bir straw. Excel'deki yazısıyla duruyor; yuvası "
              "dolu sayılıyor.",
        "en": "A straw listed in this goblet of the cryo map Excel with no "
              "matching tube in the program. Shown as written in the Excel; its "
              "slot counts as occupied."},
    "excel_kaydi_kaldirildi": {"tr": "Tanktan çıkarıldı", "en": "Removed from tank"},
    "excel_kaydi_baglandi": {"tr": "Tüpe bağlandı", "en": "Linked to a tube"},
    "excel_soyad_ad": {"tr": "Soyad, ad (Excel)", "en": "Surname, name (Excel)"},
    "excel_hucre": {"tr": "Hücre (Excel)", "en": "Cells (Excel)"},
    "excel_vial": {"tr": "VİAL (Excel)", "en": "VIAL (Excel)"},
    "excel_kaynak": {"tr": "Excel'deki yeri", "en": "Place in the Excel"},
    "satir_n": {"tr": "satır {n}", "en": "row {n}"},
    "tarih": {"tr": "Tarih", "en": "Date"},
    "notlar": {"tr": "Notlar", "en": "Notes"},
    "isaretleyen": {"tr": "İşaretleyen", "en": "Marked by"},
    "eslesmeme_sebebi": {"tr": "Neden tüp değil", "en": "Why not a tube"},
    "eslesmeme_hasta_yok": {"tr": "Excel'deki hasta programda yok",
                            "en": "The patient in the Excel is not in the program"},
    "eslesmeme_hasta_cok": {"tr": "Aynı adlı birden çok hasta var, hangisi olduğu "
                                  "ayırt edilemedi",
                            "en": "Several patients share the name; not resolved"},
    "eslesmeme_gun_yok": {"tr": "Hasta programda var ama o gün dondurulmuş tüpü yok",
                          "en": "Patient found, but no tube frozen that day"},
    "eslesmeme_tup_yok": {"tr": "Hasta programda var ama hiç dondurma tüpü yok",
                          "en": "Patient found, but no frozen tubes at all"},
    "eslesmeme_tutmuyor": {"tr": "O gün tüp var ama içerik tutmuyor",
                           "en": "A tube exists that day but the contents differ"},
    "eslesmeme_es_tutmuyor": {"tr": "Ad tutuyor, eş adı tutmuyor",
                              "en": "Name matches, partner's name does not"},
    "eslesmeme_cakisma": {"tr": "İki Excel satırı aynı tüpü istiyor",
                          "en": "Two Excel rows claim the same tube"},
    "eslesmeme_bosaltilmis": {
        "tr": "Tüp programda çözülmüş/boşaltılmış görünüyor, Excel tankta diyor",
        "en": "The tube is thawed/emptied in the program; the Excel says in tank"},
    "eslesmeme_farkli_konum": {"tr": "Tüp programda başka bir konumda",
                               "en": "The tube is at another location in the program"},
    "eslesmeme_tarihsiz": {"tr": "Excel'de tarih yok ya da okunamadı",
                           "en": "No readable date in the Excel"},
    "eslesmeme_bilgisiz": {"tr": "Excel'de yalnızca ad yazılı (tarih, hücre, VİAL yok)",
                           "en": "Only a name in the Excel (no date, cells, vial)"},
    "eslesmeme_gobletsiz": {"tr": "Excel'de gobleti (NO) yazmıyor",
                            "en": "No goblet (NO) in the Excel"},
    "eslesmeme_sperm_tarih_yok": {"tr": "Sperm: tarih yok ya da okunamadı",
                                  "en": "Sperm: no readable date"},
    "eslesmeme_sperm_tarih_ileri": {"tr": "Sperm: tarih bugünden ileri (yazım hatası)",
                                    "en": "Sperm: date in the future (typo)"},
    "eslesmeme_sperm_ayni_ad": {"tr": "Sperm: aynı adla birden çok kayıt",
                                "en": "Sperm: several records with the name"},
    "eslesmeme_sperm_es_belirsiz": {
        "tr": "Sperm: aynı adla iki farklı eş, bu satırda eş yazmıyor",
        "en": "Sperm: two partners with the name, none on this row"},
    "eslesmeme_sperm_baska_konum": {
        "tr": "Sperm: programda o gün kaydı var, konumu farklı",
        "en": "Sperm: a record that day exists at another location"},
    "tupe_bagla": {"tr": "Tüpe bağla", "en": "Link to a tube"},
    "tupe_bagla_ipucu": {
        "tr": "Straw programdaki bir tüpse bağlayın: tüp bu gobletin konumunu alır, "
              "Excel kaydı onunla birleşir. Aynı gün dondurulmuş tüpler:",
        "en": "If the straw is a tube in the program, link it: the tube takes this "
              "goblet's location and the Excel record merges into it. Tubes frozen "
              "the same day:"},
    "bu_tupe_bagla": {"tr": "Bu tüp", "en": "This tube"},
    "tupe_bagla_onay": {"tr": "Excel kaydı {etiket} tüpüne bağlanacak; tüp bu "
                              "gobletin konumunu alacak. Devam edilsin mi?",
                        "en": "The Excel record will be linked to tube {etiket}; "
                              "the tube takes this goblet's location. Continue?"},
    "tupe_bagla_onay_elle": {"tr": "Excel kaydı yazılan etiketteki tüpe bağlanacak; "
                                   "tüp bu gobletin konumunu alacak. Devam edilsin mi?",
                             "en": "The Excel record will be linked to the tube with "
                                   "this label; the tube takes this goblet's location. "
                                   "Continue?"},
    "tup_etiketi": {"tr": "Tüp etiketi", "en": "Tube label"},
    "ayni_gun_tup_yok": {"tr": "Aynı gün dondurulmuş dolu tüp yok.",
                         "en": "No occupied tube frozen that day."},
    "excel_bagla_tup_yok": {"tr": "Bu etiketle bir tüp yok",
                            "en": "No tube with this label"},
    "excel_bagla_tup_dolu_degil": {"tr": "Tüp dolu değil (çözülmüş ya da taşınmış)",
                                   "en": "The tube is not occupied (thawed or moved)"},
    "excel_bagla_kategori": {"tr": "Tüp başka türden (embriyo / sperm)",
                             "en": "The tube is of another kind (embryo / sperm)"},
    "excel_kaldir_tarih": {"tr": "Tarih girilmeli.", "en": "A date is required."},
    "excel_bagi_coz": {"tr": "Bağı çöz", "en": "Unlink"},
    "excel_bagi_coz_onay": {"tr": "Bağ çözülecek; tüp bağlamadan önceki konumuna döner. "
                                  "Devam edilsin mi?",
                            "en": "The link will be removed; the tube returns to its "
                                  "previous location. Continue?"},
    "tanktan_cikarildi": {"tr": "Tanktan çıkarıldı olarak işaretle",
                          "en": "Mark as removed from the tank"},
    "tanktan_cikarildi_ipucu": {
        "tr": "Straw çözüldü, atıldı ya da başka yere taşındıysa. Yuva boşalır; "
              "kayıt silinmez, geri alınabilir.",
        "en": "If the straw was thawed, discarded or moved. The slot is freed; the "
              "record is kept and can be restored."},
    "tanktan_cikarildi_ornek": {"tr": "Örn. çözüldü, atıldı, başka merkeze gitti",
                                "en": "E.g. thawed, discarded, sent elsewhere"},
    "tanktan_cikarildi_onay": {"tr": "Straw tanktan çıkarıldı olarak işaretlenecek. "
                                     "Devam edilsin mi?",
                               "en": "The straw will be marked as removed. Continue?"},
    "tanktan_cikarildi_kaydet": {"tr": "Tanktan çıkarıldı", "en": "Removed"},
    "tanka_don": {"tr": "Tanka geri koy", "en": "Put back in the tank"},
    "tanka_don_onay": {"tr": "Straw yeniden tankta sayılacak. Devam edilsin mi?",
                       "en": "The straw will count as in the tank again. Continue?"},
    "excel_bagla_tup_bagli": {"tr": "Bu tüp başka bir Excel kaydının straw'ı",
                              "en": "This tube is another Excel record's straw"},
    "baska_kayda_bagli": {"tr": "başka bir Excel kaydının straw'ı",
                          "en": "another Excel record's straw"},

    # ---- Excel kaydını hastaya bağla (v6.213) ----
    "hastaya_bagla": {"tr": "Hastaya bağla", "en": "Link to a patient"},
    "hastaya_bagla_ipucu": {
        "tr": "Straw'ın tüpü programda yoksa: hastayı dosya numarası ya da adıyla "
              "bulun. Program o hastaya bu straw'ın tüpünü açar ve bu gobletde "
              "gösterir; Excel kaydı onunla birleşir. Yalnızca dondurma bilgisi "
              "yazılır -- OPU, ICSI ve döllenme kaydı uydurulmaz.",
        "en": "If the straw's tube is not in the program: find the patient by file "
              "number or name. The program opens this straw's tube for that "
              "patient in this goblet and merges the Excel record into it. Only "
              "the freezing is recorded -- no OPU, ICSI or fertilisation is made up."},
    "excel_sperm_hastaya_bagla_ipucu": {
        "tr": "Straw'ın tüpü programda yoksa: hastayı dosya numarası ya da adıyla "
              "bulun. Program o hastaya bir sperm dondurma kaydı açar, tüpü bu "
              "gobletde gösterir; Excel kaydı onunla birleşir.",
        "en": "If the straw's tube is not in the program: find the patient by file "
              "number or name. The program opens a sperm freezing record for that "
              "patient in this goblet and merges the Excel record into it."},
    "hastaya_bagla_ara_ipucu": {"tr": "Dosya no ya da ad (sıra önemsiz)",
                                "en": "File no or name (any order)"},
    "excel_adiyla_ara": {"tr": "Excel'deki adla ara", "en": "Search the Excel's name"},
    "hastaya_bagla_hasta_yok": {
        "tr": "Bu aramayla hasta bulunamadı. Hasta programda yoksa önce "
              "\"Yeni hasta\" ile açın, sonra buradan bağlayın.",
        "en": "No patient found. If the patient is not in the program, open them "
              "with \"New patient\" first, then link here."},
    "secilen_hasta": {"tr": "Seçilen hasta", "en": "Selected patient"},
    "excel_ad_ayni": {"tr": "Excel'deki ad bu hastanınkiyle aynı.",
                      "en": "The name in the Excel is this patient's."},
    "excel_ad_es": {"tr": "Excel'deki ad bu kaydın eşinin adı.",
                    "en": "The name in the Excel is this record's partner."},
    "excel_ad_farkli": {
        "tr": "Excel'deki ad ({excel}) bu hastanınkinden farklı yazılmış: doğru "
              "hasta olduğundan emin olun.",
        "en": "The name in the Excel ({excel}) differs from this patient's: make "
              "sure this is the right patient."},
    "excel_es_farkli": {"tr": "Excel'deki eş adı ({excel}) bu hastanın eşininkinden farklı.",
                        "en": "The partner in the Excel ({excel}) differs from this "
                              "patient's."},
    "hastanin_tupleri": {"tr": "Hastanın tanktaki tüpleri",
                         "en": "The patient's tubes in the tank"},
    "hastanin_tupleri_ipucu": {
        "tr": "Straw bunlardan biriyse (Excel'deki tarih yanlış yazılmış olabilir) "
              "o tüpe bağlayın, yeni tüp açmayın.",
        "en": "If the straw is one of these (the Excel date may be wrong), link to "
              "that tube instead of opening a new one."},
    "hastanin_tupu_yok": {"tr": "Tankta tüpü yok.", "en": "No tubes in the tank."},
    "acilacak_tup": {"tr": "Bu hastaya açılacak tüp", "en": "Tube to open for this patient"},
    "tup": {"tr": "Tüp", "en": "Tube"},
    "dondurma_gunu": {"tr": "Dondurma günü", "en": "Freezing day"},
    "dondurma_gunu_excel": {"tr": "Excel'deki tarih: {t}", "en": "Date in the Excel: {t}"},
    "dondurma_gunu_degistir": {"tr": "Dondurma gününü değiştir",
                               "en": "Change the freezing day"},
    "dondurma_gunu_uygula": {"tr": "Bu günle göster", "en": "Show with this day"},
    "opu_gunu": {"tr": "OPU günü", "en": "OPU day"},
    "opu_gunu_bilinmiyor": {"tr": "bilinmiyor (HÜCRE günü yazmıyor)",
                            "en": "unknown (the cells column gives no day)"},
    "acilacak_kayit": {"tr": "Kayıt", "en": "Record"},
    "acilacak_tedavi_yeni": {
        "tr": "Yeni bir Cryo Excel tedavisi ({tip}): yalnızca dondurma bilgisi, "
              "istatistiğe girmez",
        "en": "A new Cryo Excel treatment ({tip}): freezing only, not in the "
              "statistics"},
    "acilacak_tedavi_var": {
        "tr": "Hastanın aynı güne açılmış Cryo Excel tedavisine eklenir: {no}",
        "en": "Added to the patient's Cryo Excel treatment of the same day: {no}"},
    "acilacak_sperm": {"tr": "Yeni bir sperm dondurma kaydı (Cryo Excel)",
                       "en": "A new sperm freezing record (Cryo Excel)"},
    "acilis_taninmayan": {"tr": "Okunamayan parça: {p} -- skorsuz embriyo olarak açılır.",
                          "en": "Unreadable part: {p} -- opened as an embryo without "
                                "a score."},
    "acilis_ayni_gun": {
        "tr": "Bu hastanın o gün programda başka bir tedavisi var: {liste}. Straw o "
              "tedavinin tüpü olabilir -- öyleyse yukarıdaki listeden o tüpe bağlayın.",
        "en": "This patient has another treatment that day: {liste}. The straw may be "
              "its tube -- if so, link to that tube in the list above."},
    "acilis_ayni_gun_sperm": {
        "tr": "Bu hastanın o gün bir sperm dondurması var: {liste}. Straw o tüp "
              "olabilir -- öyleyse yukarıdaki listeden bağlayın.",
        "en": "This patient has a sperm freezing that day: {liste}. The straw may be "
              "that tube -- if so, link to it above."},
    "hastaya_ac": {"tr": "Bu hastaya tüp olarak aç", "en": "Open as this patient's tube"},
    "hastaya_ac_onay": {"tr": "{ad} ({dosya}) hastasına bu straw'ın tüpü açılacak. "
                              "Devam edilsin mi?",
                        "en": "This straw's tube will be opened for {ad} ({dosya}). "
                              "Continue?"},
    "excel_acilis_tarih_yok": {
        "tr": "Dondurma günü girilmeli: Excel'deki tarih yok, okunamadı ya da "
              "bugünden ileri.",
        "en": "A freezing day is required: the Excel's date is missing, unreadable "
              "or in the future."},
    "excel_acilis_tarih_ileri": {"tr": "Dondurma günü bugünden ileri olamaz.",
                                 "en": "The freezing day cannot be in the future."},
    "excel_acilis_tarih_bozuk": {"tr": "Yazılan gün okunamadı.",
                                 "en": "The day entered could not be read."},
    "excel_acilis_icerik_okunamadi": {
        "tr": "Excel'deki HÜCRE okunamadı: tüpün içeriği bilinmiyor, tüp açılamaz. "
              "Straw programda bir tüpse ona bağlayın.",
        "en": "The Excel's cells column could not be read: the tube's content is "
              "unknown, no tube can be opened. If the straw is a tube in the "
              "program, link to it."},
    "excel_acilis_cok_tup": {
        "tr": "Excel'deki yazıda birden çok tüp var (her parantez bir tüp): bu "
              "kayıttan tek tüp açılabiliyor, açılmadı.",
        "en": "The Excel text lists several tubes (one per bracket): only one tube "
              "can be opened from a record, nothing was opened."},
    "excel_acilis_durum": {"tr": "Excel kaydı artık tankta değil (bu arada bağlanmış "
                                 "ya da çıkarılmış).",
                           "en": "The Excel record is no longer in the tank (linked or "
                                 "removed meanwhile)."},
    "excel_kaydi_acildi": {"tr": "Straw hastaya bağlandı: tüpü açıldı.",
                           "en": "The straw was linked to the patient: its tube was opened."},
    "excel_kaydi_geri_alindi": {"tr": "Açılan tüp geri alındı; Excel kaydı yeniden tankta.",
                                "en": "The opened tube was undone; the Excel record is "
                                      "in the tank again."},
    "excel_kaydi_hastaya_acildi": {"tr": "Hastaya bağlandı", "en": "Linked to a patient"},
    "acilan_aciklama": {
        "tr": "Bu straw'ın tüpü bu kayıttan hastaya açıldı (yalnızca dondurma "
              "bilgisiyle).",
        "en": "This straw's tube was opened for the patient from this record "
              "(freezing only)."},
    "acilan_tedavi": {"tr": "Açılan tedavi", "en": "Treatment opened"},
    "acilan_tedavi_ipucu": {"tr": "Yalnızca dondurma bilgisi olan Cryo Excel tedavisi",
                            "en": "Cryo Excel treatment with the freezing only"},
    "acilan_sperm_kaydi": {"tr": "Açılan sperm dondurma kaydı",
                           "en": "Sperm freezing record opened"},
    "acilan_sperm_ipucu": {"tr": "Sayfasında dondurma sebebi ve İşlemi Yapan girilebilir",
                           "en": "The reason and the person can be entered on its page"},
    "acilani_geri_al": {"tr": "Açılan tüpü geri al", "en": "Undo the opened tube"},
    "acilani_geri_al_ipucu": {
        "tr": "Yanlış hastaya açıldıysa: tüp (tedavisi boş kalırsa o da) silinir, "
              "Excel kaydı yeniden tankta görünür. Tüpe sonradan işlem yapıldıysa "
              "(çözme, taşıma) geri alınamaz.",
        "en": "If opened for the wrong patient: the tube (and its treatment, if left "
              "empty) is deleted and the Excel record is in the tank again. Not "
              "possible after further work on the tube (thaw, move)."},
    "acilani_geri_al_onay": {
        "tr": "Bu kayıttan açılan tüp silinecek (tedavisi boş kalırsa o da); Excel "
              "kaydı yeniden tankta görünecek. Devam edilsin mi?",
        "en": "The tube opened from this record will be deleted (and its treatment, "
              "if left empty); the Excel record will be in the tank again. Continue?"},
    "excel_acilan_degil": {"tr": "Bu kayıt hastaya açılan bir tüpe bağlı değil.",
                           "en": "This record is not linked to a tube opened for a patient."},
    "excel_acilan_kullanildi": {
        "tr": "Açılan tüp artık tankta değil (çözülmüş, kullanılmış ya da başka "
              "merkeze taşınmış): geri alınamaz. Önce o işlemi geri alın.",
        "en": "The opened tube is no longer in the tank (thawed, used or moved "
              "elsewhere): cannot be undone. Undo that step first."},
    "excel_acilan_tasindi": {
        "tr": "Açılan tüp başka bir gobletde: geri alınamaz. Önce tüpü bu gobletde "
              "gösterin.",
        "en": "The opened tube is in another goblet: cannot be undone. Put it back "
              "in this goblet first."},
    "excel_acilan_baska_kayit": {"tr": "Açılan tüpe başka bir Excel kaydı da bağlı: "
                                       "geri alınamaz.",
                                 "en": "Another Excel record is linked to the opened "
                                       "tube: cannot be undone."},
    "excel_acilan_islem_var": {
        "tr": "Açılan tüpe sonradan kayıt eklenmiş (dondurma ve değerlendirme "
              "dışında bir işlem, fotoğraf, onam, tedaviye bağlama): geri alınamaz.",
        "en": "Records were added to the opened tube later (other than freezing and "
              "grading: a procedure, photo, consent, link to a treatment): cannot be "
              "undone."},

    # ---- haritadan yer tamamla (v6.214) ----
    "yer_tamamla": {"tr": "Haritadan yer tamamla", "en": "Complete locations from the map"},
    "yer_tamamla_ipucu": {
        "tr": "Access kayıtlarında konum yoktu. Konumlar Cryo Haritası Excel'inden, "
              "ad, dondurma günü ve içerik birebir tutunca yazıldı. Bu tüplerde "
              "biri tutmadı (ad farklı yazılmış, Excel'deki tarih bir iki gün kayık, "
              "skor farklı yazılmış) -- straw haritada gobletinde duruyor, tüp "
              "\"konum girilmemiş\". Program kendisi bağlamıyor: doğru olanları "
              "işaretleyin, tüp straw'ın gobletine geçer. Yanlış bağlanan, haritadaki "
              "kaydın sayfasında \"Bağı çöz\" ile geri alınır.",
        "en": "The Access records had no location. Locations were written from the "
              "Cryo Map Excel when name, freezing day and content matched exactly. "
              "One of them did not match for these tubes (name spelt differently, "
              "Excel date off by a day or two, grade written differently) -- the straw "
              "is in its goblet on the map, the tube says \"location not entered\". "
              "The program does not link them itself: tick the right ones and the "
              "tube moves to the straw's goblet. A wrong link is undone with "
              "\"Unlink\" on the map record's page."},
    "yer_tamamla_ozet": {"tr": "Konumu girilmemiş tüp: {n} · haritada olası yeri olan: {m}",
                         "en": "Tubes without a location: {n} · with a possible place "
                               "on the map: {m}"},
    "yer_tamamla_sirali": {
        "tr": "Bu hastanın aynı içerikli tüpleri programda birbirinden ayırt "
              "edilmiyor: her tüpe ayrı bir straw, sırayla önerildi.",
        "en": "This patient's tubes with the same content cannot be told apart in "
              "the program: each tube gets its own straw, in order."},
    "yer_tamamla_hasta_sec": {"tr": "Bu hastanınkileri seç", "en": "Select this patient's"},
    "yer_tamamla_kesin": {"tr": "Programın kuralıyla da tutuyor (ad, gün, içerik)",
                          "en": "Also matches the program's rule (name, day, content)"},
    "yer_tamamla_onerisiz": {
        "tr": "Olası yeri bu hastanın aynı içerikli başka tüpüne önerildi; haritada "
              "ikinci bir straw yok.",
        "en": "Its possible place was suggested for another tube of this patient "
              "with the same content; no second straw on the map."},
    "yer_tamamla_baska_aday": {"tr": "Başka olası yer: {n} (tüpün sayfası)",
                               "en": "Other possible places: {n} (tube page)"},
    "yer_tamamla_bagla": {"tr": "Seçilenleri bağla", "en": "Link selected"},
    "yer_tamamla_onay": {
        "tr": "Seçilen {n} tüp, haritadaki straw'ın gobletine yazılacak. Emin misiniz?",
        "en": "The {n} selected tubes will be written to their straws' goblets. "
              "Are you sure?"},
    "yer_tamamla_baglandi": {"tr": "{n} tüpün yeri haritadan yazıldı.",
                             "en": "Location written from the map for {n} tubes."},
    "yer_tamamla_atlanan": {
        "tr": "{n} seçim yazılmadı: tüp ya da haritadaki kayıt bu arada değişmiş "
              "(çözülmüş, başka bir tüpe bağlanmış) ya da aynı straw iki tüpe seçilmiş.",
        "en": "{n} selections were not written: the tube or the map record changed "
              "meanwhile (thawed, linked to another tube) or the same straw was "
              "chosen for two tubes."},
    "yer_tamamla_yok": {"tr": "Konumu girilmemiş tüplerin haritada olası yeri yok.",
                        "en": "No possible place on the map for tubes without a location."},
    "yer_tamamla_n_oneri": {"tr": "{n} tüp için haritada olası yer var",
                            "en": "A possible place on the map for {n} tubes"},
    "haritada_olasi_yer": {"tr": "Haritada olası yeri", "en": "Possible place on the map"},
    "haritada_olasi_yer_ipucu": {
        "tr": "Cryo Haritası'nda bu tüpe uyan bir straw duruyor, ama ad, gün ya da "
              "içerikten biri birebir tutmadığı için program kendisi bağlamadı. "
              "Doğruysa bağlayın: tüp straw'ın gobletine geçer.",
        "en": "A straw on the Cryo Map fits this tube, but name, day or content did "
              "not match exactly, so the program did not link it. If it is right, "
              "link it: the tube moves to the straw's goblet."},
    "bu_yere_bagla": {"tr": "Bu yere bağla", "en": "Link here"},
    "programdaki_hasta": {"tr": "Programdaki hasta", "en": "Patient in the program"},
    "bu_yere_bagla_onay": {"tr": "Tüp {yer} gobletine yazılacak. Emin misiniz?",
                           "en": "The tube will be written to goblet {yer}. Are you sure?"},
    "konum_neden_aktarim": {
        "tr": "Access kayıtlarında konum yoktu; konum Cryo Haritası Excel'inden, ad, "
              "dondurma günü ve içerik birebir tutunca yazıldı. Bu tüpte biri tutmadı.",
        "en": "The Access records had no location; it was written from the Cryo Map "
              "Excel when name, freezing day and content matched exactly. One of them "
              "did not match for this tube."},
    "konum_neden_ekran": {"tr": "Dondurulurken konum yazılmamış.",
                          "en": "No location was written at freezing."},
    "yer_haritadan_yazildi": {
        "tr": "Yer haritadan yazıldı. Yanlışsa haritadaki kaydın sayfasında "
              "\"Bağı çöz\" geri alır.",
        "en": "Location written from the map. If wrong, \"Unlink\" on the map "
              "record's page undoes it."},
    "yer_yazilmadi": {"tr": "Yazılmadı: tüp ya da haritadaki kayıt bu arada değişmiş.",
                      "en": "Not written: the tube or the map record changed meanwhile."},
    "harita_kaydina_bagli": {"tr": "Cryo Haritası'ndaki Excel kaydı",
                             "en": "Excel record on the Cryo Map"},
    "kanit_tutan": {"tr": "Tutan", "en": "Matches"},
    "kanit_farkli": {"tr": "Farklı", "en": "Differs"},
    "kanit_ad": {"tr": "ad", "en": "name"},
    "kanit_ad_yazim": {"tr": "ad farklı yazılmış", "en": "name spelt differently"},
    "kanit_ad_eksik_kelime": {"tr": "adın bir kısmı eksik (ikinci ad, soyadı)",
                              "en": "part of the name missing (middle name, surname)"},
    "kanit_ad_kelime_farkli": {"tr": "adın bir kelimesi farklı",
                               "en": "one word of the name differs"},
    "kanit_ad_yok": {"tr": "ad tutmuyor", "en": "name does not match"},
    "kanit_gun": {"tr": "dondurma günü", "en": "freezing day"},
    "kanit_gun_opu": {"tr": "OPU günü (Excel'deki gün OPU'dan)",
                      "en": "OPU day (Excel day counted from OPU)"},
    "kanit_gun_sonra": {"tr": "Excel'deki tarih {n} gün sonra",
                        "en": "Excel date {n} days later"},
    "kanit_gun_once": {"tr": "Excel'deki tarih {n} gün önce",
                       "en": "Excel date {n} days earlier"},
    "kanit_gun_yok": {"tr": "Excel'de tarih yok", "en": "no date in Excel"},
    "kanit_icerik": {"tr": "içerik", "en": "content"},
    "kanit_icerik_sayi": {"tr": "skor farklı yazılmış (sayı aynı)",
                          "en": "grade written differently (same count)"},
    "kanit_es": {"tr": "eş adı", "en": "partner's name"},
    "kanit_es_farkli": {"tr": "eş adı farklı", "en": "partner's name differs"},
    "kanit_ad_baska_hasta": {"tr": "bu ad programda başka bir hastada da var",
                             "en": "another patient in the program has this name"},
    "kanit_baska_tup": {"tr": "hastanın aynı içerikli başka tüpüne de uyuyor",
                        "en": "also fits another tube of this patient with the same content"},

    # ---- boş yer önerisi (v6.190) ----
    "oneri_baslik": {"tr": "Boş yer önerisi", "en": "Free slot suggestion"},
    "oneri_kac": {"tr": "Bugün kaç straw:", "en": "Straws today:"},
    "n_renksiz": {"tr": "{n} straw'ın rengi yazılmamış",
                  "en": "{n} straws without a colour"},
    "n_renksiz_tekil": {"tr": "{n} straw'ın rengi yazılmamış",
                        "en": "{n} straw without a colour"},
    "oneri_bugun": {"tr": "Bu hastanın bugünkü straw'ı burada",
                    "en": "This patient's straw from today is here"},
    "oneri_hasta": {"tr": "Bu hastanın başka straw'ları burada",
                    "en": "This patient's other straws are here"},
    "oneri_yakin": {"tr": "Bu hastanın straw'larına yakın",
                    "en": "Near this patient's straws"},
    "oneri_yedek": {"tr": "Yedek kat (olağan yerler yetmiyor)",
                    "en": "Reserve level (regular places do not fit)"},
    "oneri_gobletde": {"tr": "gobletde", "en": "in goblet"},
    "oneri_goblet_bos": {"tr": "goblet boş", "en": "goblet empty"},
    "oneri_renk": {"tr": "önerilen renk", "en": "suggested colour"},
    "oneri_yok": {"tr": "Boş yuvası olan goblet bulunamadı.",
                  "en": "No goblet with a free slot."},
    # Tank / kanister sorgusu (v6.202).
    "oneri_tank": {"tr": "Tank", "en": "Tank"},
    "oneri_butun_tanklar": {"tr": "Bütün tanklar (otomatik)", "en": "All tanks (automatic)"},
    "oneri_butun_kanisterler": {"tr": "Bütün kanisterler", "en": "All canisters"},
    "oneri_yok_burada": {"tr": "Seçilen yerde boş yuvası olan goblet bulunamadı.",
                         "en": "No goblet with a free slot in the selected place."},
    "n_yedek_yuva": {"tr": "{n} yedek yuva", "en": "{n} reserve slots"},
    "n_yedek_yuva_tekil": {"tr": "{n} yedek yuva", "en": "{n} reserve slot"},
    "n_oneri_daha": {"tr": "{n} öneri daha göster", "en": "Show {n} more suggestions"},
    "n_oneri_daha_tekil": {"tr": "{n} öneri daha göster", "en": "Show {n} more suggestion"},
    "yer_bilgi": {"tr": "Seçilen goblet: {dolu} / {kapasite} straw",
                  "en": "Selected goblet: {dolu} / {kapasite} straws"},
    "yer_bilgi_kapasitesiz": {"tr": "Seçilen goblet: {dolu} straw",
                              "en": "Selected goblet: {dolu} straws"},
    "yer_duzende_yok": {"tr": "Bu goblet tank düzeninde yok (yazım hatası olabilir).",
                        "en": "This goblet is not in the tank layout (typo?)."},
    "yer_kapasite_yok": {"tr": "Bu yerin kaç straw aldığı bilinmiyor.",
                         "en": "The capacity of this place is unknown."},
    "yer_dolu": {"tr": "Bu gobletde boş yuva yok ({dolu}/{kapasite}).",
                 "en": "No free slot in this goblet ({dolu}/{kapasite})."},
    "yer_renk_var": {"tr": "Bu gobletde zaten {renk} straw var.",
                     "en": "This goblet already has a {renk} straw."},
    "yer_onay": {"tr": "Biliyorum, yine de bu yere kaydet",
                 "en": "I know, save to this place anyway"},
    "yer_onay_gerekli": {"tr": "Yine de bu yere kaydetmek için onay kutusunu işaretleyin.",
                         "en": "Tick the confirmation box to save to this place anyway."},

    # ---- sperm dondurma (v6.84) ----
    "sperm_dondurma": {"tr": "Sperm Dondurma", "en": "Sperm Freezing"},
    "yeni_sperm_dondurma": {"tr": "Yeni Sperm Dondurma", "en": "New Sperm Freezing"},
    "sperm_dondurma_hastasi": {"tr": "Sperm Dondurma", "en": "Sperm Freezing"},
    "sperm_dondurma_ara_ipucu": {
        "tr": "Etiket, konum, dosya no veya hasta adı",
        "en": "Label, location, file no or patient name"},
    "dondurulmus_sperm_yok": {"tr": "Henüz dondurulmuş sperm yok.",
                              "en": "No frozen sperm yet."},
    "aramaya_uyan_sperm_yok": {"tr": "Bu aramaya uyan sperm kaydı yok.",
                               "en": "No sperm records match this search."},
    "dondurma_saati": {"tr": "Dondurma saati", "en": "Freeze time"},
    "sperm_dondurmayi_kaydet": {"tr": "Sperm dondurmayı kaydet",
                                "en": "Save sperm freezing"},
    "sperm_dondurma_kaydini_sil": {"tr": "Sperm dondurma kaydını sil",
                                   "en": "Delete sperm freezing record"},
    "sperm_kaydi_yok": {"tr": "Bu kayıt bulunamadı.",
                        "en": "This record was not found."},
    "sperm_dondurma_silinecek": {
        "tr": "Bu kayıt ve bağlı olduğu taşıyıcı kalıcı olarak silinecek.",
        "en": "This record and its carrier will be permanently deleted."},
    "kaydi_sil_dugme": {"tr": "Kaydı sil", "en": "Delete record"},
    "semen_analizi": {"tr": "Dondurma öncesi semen analizi",
                      "en": "Pre-freeze semen analysis"},
    "yeni_sperm_hasta": {"tr": "Yeni hasta kaydı (Sperm Dondurma)",
                         "en": "New patient (Sperm Freezing)"},
    "hasta_ve_sperm_dondurmayi_kaydet": {
        "tr": "Hastayı ve sperm dondurmayı kaydet",
        "en": "Save patient and sperm freezing"},
    "onamlar": {"tr": "Onamlar", "en": "Consent forms"},
    "onam_yok": {"tr": "Henüz onam eklenmedi.", "en": "No consent form added yet."},
    "onam_ipucu": {
        "tr": "Fotoğraf veya PDF ekleyebilirsin (imzalı onam formu gibi).",
        "en": "You can add a photo or PDF (a signed consent form, etc.)."},
    "onam_sil": {"tr": "Onamı sil", "en": "Delete consent form"},
    "onam_kalici_silinecek": {
        "tr": "Bu onam eki kalıcı olarak silinecek.",
        "en": "This consent form attachment will be permanently deleted."},
    "dondurma_sebebi": {"tr": "Dondurma sebebi", "en": "Freeze reason"},
    "dondurma_sebebi_ipucu": {
        "tr": "Listeden seçebilir ya da kendi sebebinizi yazabilirsiniz.",
        "en": "Pick from the list or type your own reason."},
    "kullanildigi_tedavi": {"tr": "Kullanıldığı tedavi", "en": "Used in treatment"},
    # ---- dosya numarasından eşleşme (v6.125) ----
    "mukerrer_tedavi_var": {"tr": "{n} tüp bebek tedavisi var",
                            "en": "{n} IVF treatment(s) on record"},
    "mukerrer_sperm_var": {"tr": "{n} dondurulmuş sperm kaydı var",
                           "en": "{n} frozen sperm record(s)"},
    "mukerrer_es": {"tr": "eşi: {ad}", "en": "spouse: {ad}"},
    "dondurulmus_sperm": {"tr": "Dondurulmuş sperm", "en": "Frozen sperm"},
    # Tedavinin bulaş hastalığı kaydı (v6.219): tedavi formu, tedavi ekranı,
    # kimlik bandının uyarısı. `bulas_<kişi>` anahtarı `db.BULAS_KISILER`'den.
    "bulas_hastaligi": {"tr": "Bulaş hastalığı", "en": "Infectious disease"},
    "bulas_kadin": {"tr": "Kadın", "en": "Female"},
    "bulas_erkek": {"tr": "Erkek", "en": "Male"},
    "bulas_yok": {"tr": "Yok", "en": "None"},
    "bulas_diger": {"tr": "Diğer (elle yazın)", "en": "Other (type it)"},
    "bulas_ipucu": {
        "tr": "Hiçbiri seçilmezse girilmedi sayılır. Seçilen hastalık bu "
              "tedavinin bütün ekranlarında, en üstte hastanın adının altında "
              "kırmızı uyarıyla görünür.",
        "en": "Nothing selected means not entered. A selected disease shows as "
              "a red warning under the patient's name on every screen of this "
              "cycle."},
    "bulas_onceki": {
        "tr": "Hastanın önceki tedavisinden ({no}) geldi; tahlil değiştiyse düzeltin.",
        "en": "Carried over from the patient's previous cycle ({no}); correct it "
              "if the test result changed."},
    "bulas_tedavisinde": {"tr": "{no} tedavisinde", "en": "in cycle {no}"},
    # Hasta kartının "Dondurulmuş örnekler" bölümü (v6.217).
    "dondurulmus_ornekler": {"tr": "Dondurulmuş örnekler", "en": "Frozen samples"},
    "tankta_embriyo_yok": {"tr": "Tankta embriyo ya da yumurta tüpü yok.",
                           "en": "No embryo or oocyte straw in the tank."},
    "coz_acik": {"tr": "Çöz · {no} ({tip}) için", "en": "Thaw · for {no} ({tip})"},
    "coz_yeni": {"tr": "Çöz · yeni {tip}", "en": "Thaw · new {tip}"},
    "coz_yeni_onay": {
        "tr": "Bu tüp için yeni bir {tip} tedavisi açılacak ve çözme ekranına "
              "geçilecek. Devam edilsin mi?",
        "en": "A new {tip} cycle will be opened for this straw and the thaw "
              "screen will open. Continue?"},
    "coz_ekrani": {"tr": "Çözme ekranı", "en": "Thaw screen"},
    "tasima_git": {"tr": "Başka merkeze taşı", "en": "Move to another centre"},
    "dondurulmus_excel_baslik": {
        "tr": "Cryo Haritası'nda adı benzeyen Excel kayıtları",
        "en": "Cryo map Excel records with a similar name"},
    "dondurulmus_excel_ipucu": {
        "tr": "Programda tüpü olmayan straw'lar. Hastaya bağlı değiller (ad tek "
              "başına kanıt değil), buradan çözülemez: kaydı açıp hastaya "
              "bağlayınca tüp yukarıdaki listeye gelir.",
        "en": "Straws with no straw record in the program. They are not linked "
              "to the patient (a name alone is not proof) and cannot be thawed "
              "from here: open the record and link it to the patient, the straw "
              "then appears in the list above."},
    "sperm_dosya_esleme_ipucu": {
        "tr": "Bu kayıtlar dosya numarasıyla eşleşiyor — aynı dosya no, aynı "
              "hasta kaydı.",
        "en": "These records match by file number — same file number, same "
              "patient record."},
    "sperm_bagli_degil": {"tr": "Henüz bir tedaviye bağlanmadı",
                          "en": "Not linked to a treatment yet"},
    "sperm_dosyada_bekliyor": {
        "tr": "Bu dosya numarasına ait, henüz hiçbir tedaviye bağlanmamış "
              "{n} dondurulmuş sperm kaydı var.",
        "en": "This file number has {n} frozen sperm record(s) not yet linked "
              "to any treatment."},
    "dondurulmus_sperm_bagla": {"tr": "Dondurulmuş sperm bağla",
                                "en": "Link frozen sperm"},
    "sperm_bagli_yok": {"tr": "Bu tedaviye bağlı dondurulmuş sperm yok.",
                        "en": "No frozen sperm linked to this treatment."},
    "sperm_baglantisini_kaldir": {"tr": "Bağlantıyı kaldır", "en": "Remove link"},
    # Hasta kartından tedaviye bağlama (v6.139)
    "esin_dondurulmus_spermi": {"tr": "Eşin dondurulmuş spermi",
                                "en": "Partner's frozen sperm"},
    "es_kayitli_degil": {
        "tr": "Bu dosya numarasıyla kayıtlı bir hasta yok.",
        "en": "No patient is registered with this file number."},
    "es_sperm_uyari": {
        "tr": "Eşin kendi dosya numarasında {n} dondurulmuş sperm kaydı var.",
        "en": "The partner's own file number has {n} frozen sperm record(s)."},
    "tedaviye_bagla": {"tr": "Tedaviye bağla", "en": "Link to treatment"},
    "tedavi_sec": {"tr": "Tedavi seç", "en": "Choose treatment"},
    "baglanacak_tedavi_yok": {
        "tr": "Bağlamak için önce bu hastaya bir tedavi açılmalı.",
        "en": "Open a treatment for this patient first, then link."},
    "sperm_baglama_ipucu": {
        "tr": "Başka bir hastaya ait, daha önce dondurulmuş bir sperm "
              "örneğini bu tedaviyle ilişkilendir — örn. eşi için "
              "onkoloji tedavisi öncesi dondurma yaptırmış bir hasta.",
        "en": "Link a previously frozen sperm sample belonging to another "
              "patient to this treatment — e.g. a patient who froze sperm "
              "before oncology treatment, for his spouse's IVF cycle."},
    "bagla": {"tr": "Bağla", "en": "Link"},

    # ---- cycle formu ----
    "cycle_duzenle": {"tr": "Tedaviyi düzenle", "en": "Edit cycle"},
    "yeni_cycle": {"tr": "Yeni tedavi", "en": "New cycle"},
    "cycle_i_kaydet": {"tr": "Tedaviyi kaydet", "en": "Save cycle"},
    "lab_kayit_no": {"tr": "Lab kayıt no", "en": "Lab record no"},
    "kacinci_cycle": {"tr": "Kaçıncı tedavi", "en": "Patient's cycle no"},
    "cycle_no_ipucu": {
        "tr": "Lab kayıt no otomatik atandı; gerekirse değiştirebilirsin. "
              "Kaçıncı tedavi tarih sırasından verilir: en eski tedavi 1. "
              "Hasta başka merkezde de tedavi gördüyse gerçek deneme sayısını "
              "yaz — elle yazdığın numara korunur, sonraki tedaviler ondan "
              "devam eder.",
        "en": "The lab record no was assigned automatically; change it if you "
              "need to. The patient's cycle no follows the date order: the "
              "oldest cycle is 1. If the patient was also treated at another "
              "centre, type the real attempt number — a number you type is "
              "kept and later cycles continue from it."},
    "kacinci_elle": {
        "tr": "Elle yazılan numara: {n}. Kutuyu boşaltırsan numarayı tarih "
              "sırası verir.",
        "en": "Number typed by hand: {n}. Clear the box to let the date order "
              "set it."},
    "tedavi_tipi": {"tr": "Tedavi tipi", "en": "Treatment type"},
    "fet_ipucu": {
        "tr": "FET seçilirse laboratuvar aşamaları gösterilmez; doğrudan "
              "çözme ve transferle başlanır. FET (3→5) seçilirse çözme ile "
              "transfer arasına blastokist değerlendirmesi eklenir — gün 2/3 "
              "embriyosu çözülüp gün 5'e kadar kültürlenir. Yumurta Çözme "
              "seçilirse yalnızca çözme aşaması gösterilir — daha önce "
              "dondurulmuş bir yumurtanın bu tedavide çözülmesi.",
        "en": "If FET is selected the laboratory stages are hidden; the cycle "
              "starts directly with thaw and transfer. If FET (D3→5) is "
              "selected, a blastocyst assessment stage is added between thaw "
              "and transfer — a day 2/3 embryo is thawed and cultured to "
              "day 5. If Egg Thaw is selected, only the thaw stage is shown "
              "— a previously frozen egg is thawed in this treatment."},
    "endikasyon": {"tr": "Endikasyon", "en": "Indication"},
    "klinik_protokol": {"tr": "Klinik protokol", "en": "Clinical protocol"},
    "gonadotropin": {"tr": "Gonadotropin", "en": "Gonadotropin"},
    "baslangic_doz": {"tr": "Başlangıç doz", "en": "Starting dose"},
    "trigger": {"tr": "Trigger", "en": "Trigger"},
    "hcg_gunu_e2_alan": {"tr": "hCG günü E2", "en": "E2 on hCG day"},
    "endometrium_mm": {"tr": "Endometrium (mm)", "en": "Endometrium (mm)"},
    "folikul_sayisi": {"tr": "Folikül sayısı", "en": "Follicle count"},
    "amh": {"tr": "AMH", "en": "AMH"},
    "protokol_notu_ipucu": {"tr": "Arşiv amaçlı. İstatistikte kullanılmaz.",
                            "en": "For the record only. Not used in statistics."},
    "zamanlar_ve_opu": {"tr": "Zamanlar ve OPU", "en": "Times and OPU"},
    "hcg_zamani": {"tr": "hCG zamanı", "en": "hCG time"},
    "hcg_zamani_ipucu": {
        "tr": "Saat dahil girilmeli — OPU ve ICSI aralıkları buna göre "
              "hesaplanır.",
        "en": "Enter the time of day as well — the OPU and ICSI intervals are "
              "calculated from it."},
    "opu_zamani": {"tr": "OPU zamanı", "en": "OPU time"},
    "opu_oosit_sayilari": {"tr": "OPU'da toplanan yumurta sayıları",
                           "en": "Oocytes collected at OPU"},
    "sag_overden": {"tr": "Sağ overden toplanan",
                    "en": "Collected from right ovary"},
    "sol_overden": {"tr": "Sol overden toplanan",
                    "en": "Collected from left ovary"},
    "sag_overden_oosit": {"tr": "Sağ overden toplanan yumurta",
                          "en": "Oocytes collected from right ovary"},
    "sol_overden_oosit": {"tr": "Sol overden toplanan yumurta",
                          "en": "Oocytes collected from left ovary"},
    "bos_birakilirsa_null": {
        "tr": "Boş bırakılırsa \"girilmedi\" olarak kalır, sıfır yazılmaz.",
        "en": "If left empty it stays \"not entered\"; zero is not recorded."},
    "varsayilan_su_an": {
        "tr": "Varsayılan şu an. İşlem sonradan kaydediliyorsa değiştir.",
        "en": "Defaults to now. Change it if the step is being recorded later."},
    "ozet": {"tr": "Özet", "en": "Summary"},
    "opu_goc_gerekli": {
        "tr": "OPU'yu yapan hekim henüz kaydedilmiyor. Terminalde "
              "<code>python goc_025.py</code> çalıştır.",
        "en": "The physician who performed the OPU is not recorded yet. Run "
              "<code>python goc_025.py</code> in a terminal."},

    # ---- örnek adları (app.py ASAMA_ORNEK_ADI) ----
    # Oosit → zigot → embriyo aynı örnektir, kod değişmez; değişen sadece
    # ekrandaki isim (CLAUDE.md). O isim buradan geliyor.
    "ornek_ad": {"tr": "Örnek", "en": "Sample"},
    "oosit_ad": {"tr": "Yumurta", "en": "Oocyte"},
    "zigot_ad": {"tr": "Zigot", "en": "Zygote"},
    "cleavage_ad": {"tr": "Cleavage", "en": "Cleavage"},
    "blastokist_ad": {"tr": "Blastokist", "en": "Blastocyst"},
    "embriyo_ad": {"tr": "Embriyo", "en": "Embryo"},

    # ---- büyüteç / kare şeridi (paylaşılan parçalar) ----
    "kapat": {"tr": "Kapat", "en": "Close"},
    "onceki_kare": {"tr": "Önceki kare", "en": "Previous frame"},
    "sonraki_kare": {"tr": "Sonraki kare", "en": "Next frame"},
    "yakinlastir": {"tr": "Yakınlaştır", "en": "Zoom in"},
    "uzaklastir": {"tr": "Uzaklaştır", "en": "Zoom out"},
    "sigdir": {"tr": "Sığdır", "en": "Fit"},
    "kare_n": {"tr": "Kare {n}", "en": "Frame {n}"},
    "bu_kareyi_sil": {"tr": "Bu kareyi sil", "en": "Delete this frame"},
    "buyut": {"tr": "büyüt", "en": "enlarge"},

    # ---- vitrifikasyon ----
    "coz": {"tr": "çöz", "en": "thaw"},
    "kaydi_geri_al": {"tr": "kaydı geri al", "en": "undo record"},
    "dondurulacak_kalmadi": {"tr": "Dondurulacak embriyo kalmadı.",
                             "en": "No embryos left to freeze."},
    "dondurulacak_embriyolar": {"tr": "Dondurulacak embriyolar",
                                "en": "Embryos to freeze"},
    # Vitrifikasyon ekranı `oosit_cryo` ile paylaşılıyor; orada dondurulan
    # şey embriyo değil yumurta (v6.137). Şablon `yumurta_mi()` ile seçiyor.
    "dondurulacak_yumurta_kalmadi": {"tr": "Dondurulacak yumurta kalmadı.",
                                     "en": "No oocytes left to freeze."},
    "dondurulacak_yumurtalar": {"tr": "Dondurulacak yumurtalar",
                                "en": "Oocytes to freeze"},
    # FET'te yeniden dondurma (v6.143): liste bu tedavi için çözülüp transfer
    # edilmeyen embriyolar -- "kalmadı" yerine neden boş olduğunu söyle.
    "fet_dondurulacak_yok": {
        "tr": "Bu tedavide çözülüp transfer edilmeyen embriyo yok. Yeniden "
              "dondurulacak embriyo önce Çözme ekranından bu tedavi için "
              "çözülmüş olmalı.",
        "en": "No embryo was thawed and left untransferred in this cycle. An "
              "embryo to re-freeze must first be thawed for this cycle on "
              "the Thaw screen."},
    # Yumurta Çözme (v6.147): dondurulan, bu tedavide çözülen yumurtadan
    # ICSI ile gelişen embriyo -- FET'in "yeniden dondurma" metni ona uymuyor.
    "yumurtadan_dondurulacak_yok": {
        "tr": "Dondurulacak embriyo yok. Bu tedavide çözülen yumurtalardan "
              "gelişen embriyolar cleavage ya da blastokist ekranında "
              "değerlendirildikten sonra burada listelenir.",
        "en": "No embryos to freeze. Embryos developed from the oocytes thawed "
              "in this cycle are listed here once assessed on the cleavage or "
              "blastocyst screen."},
    "yumurtadan_dondurma_ipucu": {
        "tr": "Bu tedavide çözülen yumurtalardan gelişen, transfer edilmeyen "
              "embriyolar. Dondurulan embriyo yeni bir taşıyıcıya girer; "
              "yumurtanın ilk taşıyıcısının kaydı geçmiş olarak kalır.",
        "en": "Embryos developed from the oocytes thawed in this cycle and not "
              "transferred. A frozen embryo goes into a new carrier; the "
              "oocyte's first carrier record stays as history."},
    "yeniden_dondurma_ipucu": {
        "tr": "Bu tedavi için çözülüp transfer edilmeyen embriyolar. "
              "Dondurulan embriyo yeni bir taşıyıcıya girer; ilk taşıyıcının "
              "kaydı geçmiş olarak kalır.",
        "en": "Embryos thawed for this cycle and not transferred. A re-frozen "
              "embryo goes into a new carrier; the first carrier's record "
              "stays as history."},
    "yeniden_dondurma_goc_gerekli": {
        "tr": "Çözülen embriyonun yeniden dondurulması için veritabanı "
              "güncellemesi (goc_046) henüz uygulanmamış. Programı kapatıp "
              "yeniden aç; güncellemeler açılışta kendiliğinden uygulanır.",
        "en": "The database update needed to re-freeze a thawed embryo "
              "(goc_046) has not been applied yet. Close and reopen the "
              "program; updates are applied automatically at start-up."},
    # Geri alma sırası (v6.143): önce en son adım.
    "vit_geri_alma_cozulmus": {
        "tr": "Bu taşıyıcı çözülmüş. Dondurma kaydını silmek \"hiç "
              "dondurulmadı\" demek olurdu ama çözme kaydı duruyor. Önce "
              "çözme kaydını geri al.",
        "en": "This carrier has been thawed. Deleting the freezing record "
              "would mean it was never frozen, but the thaw record remains. "
              "Undo the thaw record first."},
    # v6.147: çözmeden sonra girilmiş başka bir kayıt (ICSI, değerlendirme,
    # transfer) varsa çözme geri alınmıyor -- önce en son adım.
    "thaw_geri_alma_sonraki_kayit": {
        "tr": "Bu çözmeden sonra bu örneğe başka kayıtlar girilmiş (ICSI, "
              "değerlendirme ya da transfer). Önce onları geri al.",
        "en": "Other records were entered for this sample after this thaw (ICSI, "
              "assessment or transfer). Undo those first."},
    "thaw_geri_alma_yeniden_dondurulmus": {
        "tr": "Bu embriyo çözüldükten sonra yeniden dondurulmuş. Önce yeniden "
              "dondurma kaydını geri al.",
        "en": "This embryo was re-frozen after this thaw. Undo the re-freezing "
              "record first."},
    "tasiyiciya_git": {"tr": "Taşıyıcıya git", "en": "Go to carrier"},
    # Taşıyıcı detayında: bu tüpten çözülüp sonra başka tüpe dondurulan örnek.
    "yeniden_donduruldu": {"tr": "Yeniden donduruldu", "en": "Re-frozen"},
    # Hasta kartının tedavi satırı (v6.151): bu tedavide yeniden dondurma
    # yapıldı / bu tedavide çözülen tüp daha önce yeniden dondurulmuştu.
    "yeniden_dondurma_rozet": {"tr": "Yeniden dondurma", "en": "Re-freeze"},
    "tup_etiketli": {"tr": "tüp {n}", "en": "tube {n}"},
    "n_tedavide_cozuldu": {"tr": "{n}. tedavide çözüldü",
                           "en": "thawed in cycle {n}"},
    "yeniden_dondurulmus_tup_cozuldu": {
        "tr": "Yeniden dondurulmuş tüp çözüldü",
        "en": "Thawed a re-frozen tube"},
    "n_tedaviden": {"tr": "{n}. tedaviden", "en": "from cycle {n}"},
    "degerlendirilmemis": {"tr": "değerlendirilmemiş", "en": "not assessed"},
    "gun_n": {"tr": "gün {n}", "en": "day {n}"},
    "ayni_tasiyici_ipucu": {
        "tr": "Aynı taşıyıcıya konacakları birlikte seç. Farklı taşıyıcılara "
              "koyacaksan ayrı ayrı kaydet.",
        "en": "Select together the ones going onto the same carrier. Record "
              "them separately if they go onto different carriers."},
    "tasiyici": {"tr": "Taşıyıcı", "en": "Carrier"},
    "etiket": {"tr": "Etiket", "en": "Label"},
    "etiket_benzersiz": {"tr": "Laboratuvar geneli benzersiz olmalı.",
                         "en": "Must be unique across the laboratory."},
    # Etiket araması (v6.138). İki ekran basıyor: vitrifikasyon ve hasta
    # kayıtları -- aynı anahtarları kullanıyorlar ki aynı şey aynı görünsün.
    "etiket_ara": {"tr": "Etiket kodu ile ara", "en": "Search by label code"},
    "etiket_ara_ipucu": {"tr": "Tüpün üstündeki etiket kodu",
                         "en": "Label code written on the tube"},
    "etiket_sonucu": {"tr": "Taşıyıcı etiketi", "en": "Carrier label"},
    "etiket_bulunamadi": {"tr": "Bu etikete uyan taşıyıcı yok.",
                          "en": "No carrier matches this label."},
    "renk": {"tr": "Renk", "en": "Colour"},
    "konum": {"tr": "Konum", "en": "Location"},
    "konum_ipucu": {
        "tr": "Tank haritasındaki yeri. Boş bırakılırsa konum kaydedilmez — "
              "taşıyıcı sistemde görünür ama nerede olduğu bilinmez.",
        "en": "Its place on the tank map. If left empty no location is "
              "recorded — the carrier appears in the system but where it sits "
              "is unknown."},
    "vitrifikasyon_saati": {"tr": "Vitrifikasyon saati", "en": "Vitrification time"},
    "vitrifikasyonu_kaydet": {"tr": "Vitrifikasyonu kaydet",
                              "en": "Save vitrification"},
    "vit_kaydedildi": {"tr": "Kaydedildi: {icerik}, taşıyıcı {etiket}.",
                       "en": "Saved: {icerik}, carrier {etiket}."},
    "cozme_ekrani": {"tr": "Çözme ekranı", "en": "Thaw screen"},
    # Çözme kaydı tedavinin çözme ekranına dönüyor (v6.208).
    "cozme_kaydedildi": {"tr": "Kaydedildi: taşıyıcı {etiket} çözüldü, {icerik} ({sagkalim}).",
                         "en": "Saved: carrier {etiket} thawed, {icerik} ({sagkalim})."},
    "cozme_kalan_tup": {"tr": "Tankta {n} taşıyıcı daha var, aşağıdan çözebilirsiniz.",
                        "en": "{n} more carriers in the tank, thaw them below."},
    "asamaya_gec": {"tr": "{ad} ekranına geç", "en": "Go to {ad}"},

    # ---- transfer ----
    "bu_cyclede_transfer": {"tr": "Bu tedavide transfer edilenler",
                            "en": "Transferred in this cycle"},
    "donmus": {"tr": "donmuş", "en": "frozen"},
    "taze": {"tr": "taze", "en": "fresh"},
    "cozulmus": {"tr": "çözülmüş", "en": "thawed"},
    "transfer_edilebilir_yok": {"tr": "Transfer edilebilir embriyo yok.",
                                "en": "No embryos available for transfer."},
    "transfer_aday_ipucu": {
        "tr": "Taze embriyolar blastokist/gün 3 aşamasında, dondurulmuşlar "
              "çözüldükten sonra listelenir.",
        "en": "Fresh embryos are listed at the blastocyst / day 3 stage; "
              "frozen ones after they have been thawed."},
    "transfer_edilecek_embriyolar": {"tr": "Transfer edilecek embriyolar",
                                     "en": "Embryos to transfer"},
    "transfer_ipucu": {
        "tr": "Hastanın tüm tedavilerinden uygun embriyolar listelenir. "
              "Çözülmüş embriyolar \"donmuş transfer\", diğerleri \"taze\" "
              "olarak kaydedilir.",
        "en": "Eligible embryos from all of this patient's cycles are listed. "
              "Thawed embryos are recorded as \"frozen transfer\", the rest "
              "as \"fresh\"."},
    "transfer_saati": {"tr": "Transfer saati", "en": "Transfer time"},
    "transferi_kaydet": {"tr": "Transferi kaydet", "en": "Save transfer"},
    "cycle_kartina_don": {"tr": "Tedavi kartına dön", "en": "Back to cycle card"},

    # ---- taşıyıcı ----
    "girilmemis": {"tr": "girilmemiş", "en": "not entered"},
    "icerik": {"tr": "İçerik", "en": "Contents"},
    "canli": {"tr": "Canlı", "en": "Surviving"},
    "ort_canlilik": {"tr": "Ort. canlılık", "en": "Avg. viability"},
    "tasiyicida_n_embriyo": {
        "tr": "Bu taşıyıcıda {n} embriyo var. Çözüldüğünde hepsi etkilenir.",
        "en": "This carrier holds {n} embryos. Thawing affects all of them."},
    "tasiyicida_n_yumurta": {
        "tr": "Bu taşıyıcıda {n} yumurta var. Çözüldüğünde hepsi etkilenir.",
        "en": "This carrier holds {n} oocytes. Thawing affects all of them."},
    "icindeki_embriyolar": {"tr": "İçindeki embriyolar",
                            "en": "Embryos on this carrier"},
    "icindeki_yumurtalar": {"tr": "İçindeki yumurtalar",
                            "en": "Oocytes on this carrier"},
    "cyclei_ac": {"tr": "tedaviyi aç", "en": "open cycle"},
    "tasiyici_bosaltilmis": {"tr": "Bu taşıyıcı boşaltılmış.",
                             "en": "This carrier has been emptied."},
    "bu_tasiyiciyi_coz": {"tr": "Bu taşıyıcıyı çöz", "en": "Thaw this carrier"},
    "tasiyici_bosaltildi": {"tr": "boşaltıldı", "en": "emptied"},
    "tasiyici_kullanildi": {"tr": "kullanıldı", "en": "used"},
    # Başka merkeze taşınan tüp (v6.182)
    "tasiyici_gonderildi": {"tr": "başka merkeze taşındı", "en": "moved to another centre"},
    "gonderim_baslik": {"tr": "Başka merkeze taşındı", "en": "Moved to another centre"},
    "gonderim_ac": {"tr": "Başka merkeze taşındı olarak işaretle",
                    "en": "Mark as moved to another centre"},
    "gonderim_ipucu": {
        "tr": "Hasta embriyolarını başka bir tüp bebek ünitesine taşıttıysa. "
              "Tüp Cryo Haritası'ndan ve formların \"Kalan dondurulmuş\" "
              "satırından çıkar; kayıt silinmez, geri alınabilir. Notlara "
              "\"1 tüp 12.03.2025 tarihinde ... taşındı\" diye yazılır.",
        "en": "If the patient had the embryos moved to another IVF unit. The "
              "straw leaves the cryo map and the forms' remaining list; the "
              "record is kept and can be restored."},
    "gonderim_tarihi": {"tr": "Taşındığı gün", "en": "Date moved"},
    "gonderim_yeri": {"tr": "Nereye taşındı", "en": "Moved to"},
    "gonderim_yeri_ornek": {"tr": "ör. Memorial Hastanesi'ne", "en": "e.g. Memorial Hospital"},
    "gonderim_notu": {"tr": "Not", "en": "Note"},
    "gonderim_kaydet": {"tr": "Taşındı olarak kaydet", "en": "Save as moved"},
    "gonderim_onay": {"tr": "Bu tüp başka merkeze taşındı olarak işaretlenecek. Emin misiniz?",
                      "en": "This straw will be marked as moved to another centre. Are you sure?"},
    "gonderim_cumlesi": {"tr": "{tarih} tarihinde {yer} taşındı.",
                         "en": "Moved on {tarih} to {yer}."},
    "gonderim_baska_merkeze": {"tr": "başka merkeze", "en": "another centre"},
    "gonderimi_geri_al": {"tr": "Taşındı işaretini kaldır", "en": "Undo moved"},
    "gonderimi_geri_al_onay": {"tr": "Tüp yeniden tankta (dolu) sayılacak. Emin misiniz?",
                               "en": "The straw will count as in the tank again. Are you sure?"},
    "gonderim_tarih_yok": {"tr": "Taşındığı günü yazın.", "en": "Enter the date."},
    "gonderim_tarih_hatali": {"tr": "Tarih okunamadı ya da yılı hatalı.",
                              "en": "Invalid date."},
    "gonderim_tarih_ileri": {"tr": "Taşındığı gün bugünden sonra olamaz.",
                             "en": "The date cannot be in the future."},
    "gonderim_tarih_once": {"tr": "Taşındığı gün tüpün dondurulmasından önce olamaz.",
                            "en": "The date cannot be before the freezing."},
    "gonderim_dolu_degil": {"tr": "Yalnızca içinde örnek olan dolu tüp taşındı "
                                  "olarak işaretlenebilir.",
                            "en": "Only a full straw can be marked as moved."},
    "tasinan_tupler": {"tr": "Başka merkeze taşınan tüpler", "en": "Straws moved to another centre"},
    # Taşınma bölümü (v6.205): hastanın örnekleri tek ekranda başka merkeze.
    "tasima": {"tr": "Taşınma", "en": "Transfers out"},
    "tasima_aciklama": {"tr": "Başka üniteye taşınan embriyo, yumurta ve sperm",
                        "en": "Embryos, oocytes and sperm moved to another unit"},
    "tasima_ozeti": {"tr": "{tup} tüp taşındı · son taşıma {tarih}",
                     "en": "{tup} straws moved · last on {tarih}"},
    "tasima_dugmesi": {"tr": "Başka merkeze taşıma", "en": "Move to another centre"},
    "tasima_kaydet_baslik": {"tr": "Taşıma kaydet", "en": "Record a transfer"},
    "tasima_ara_ipucu": {"tr": "Dosya no, hasta ya da eş adı",
                         "en": "File no, patient or partner name"},
    "tasima_ara_aciklama": {
        "tr": "Hastayı bulun, tanktaki tüplerinden taşınanları seçip günü ve yeri "
              "yazın. Örnekler Cryo Haritası'ndan çıkar; kayıt silinmez, hasta "
              "kartında görünür ve geri alınabilir.",
        "en": "Find the patient, select the straws that were moved and enter the "
              "date and place. They leave the cryo map; the record is kept, shown "
              "on the patient card and can be restored."},
    "tasima_hasta_yok": {"tr": "Aramaya uyan, tankta ya da taşınmış örneği olan hasta yok.",
                         "en": "No patient with stored or moved samples matches."},
    "tasima_tankta": {"tr": "Tankta", "en": "In tank"},
    "tasima_tasinan": {"tr": "Taşınan", "en": "Moved"},
    "tasinanlar": {"tr": "Taşınanlar", "en": "Moved out"},
    "tasinan_yok": {"tr": "Henüz başka merkeze taşınan örnek yok.",
                    "en": "Nothing has been moved to another centre yet."},
    "n_sperm_tupu": {"tr": "{n} sperm tüpü", "en": "{n} sperm tubes"},
    "n_sperm_tupu_tekil": {"tr": "{n} sperm tüpü", "en": "{n} sperm tube"},
    "tanktaki_ornekler": {"tr": "Tanktaki örnekler", "en": "Samples in the tank"},
    "tanktaki_ornek_yok": {"tr": "Bu hastanın tankta örneği yok.",
                           "en": "This patient has no samples in the tank."},
    "tasima_secim_ipucu": {
        "tr": "İşaretli tüpler taşınmış sayılır; taşınmayanın işaretini kaldırın.",
        "en": "Ticked straws count as moved; untick the ones that stay."},
    "tasima_onay": {"tr": "Seçilen örnekler başka merkeze taşındı olarak işaretlenecek "
                          "ve Cryo Haritası'ndan çıkacak. Emin misiniz?",
                    "en": "The selected samples will be marked as moved and leave the "
                          "cryo map. Are you sure?"},
    "tasima_kaydedildi": {"tr": "{n} örnek başka merkeze taşındı olarak kaydedildi; "
                                "Cryo Haritası'ndan çıktı.",
                          "en": "{n} samples recorded as moved; they left the cryo map."},
    "tasima_geri_alindi": {"tr": "{n} tüp yeniden tankta sayılıyor.",
                           "en": "{n} straws count as in the tank again."},
    "tasima_geri_al": {"tr": "Bu taşımayı geri al", "en": "Undo this transfer"},
    "tasima_geri_al_onay": {"tr": "Bu taşımanın tüpleri yeniden tankta (dolu) sayılacak. "
                                  "Emin misiniz?",
                            "en": "These straws will count as in the tank again. Are you sure?"},
    "tasima_secim_yok": {"tr": "Taşınan en az bir örnek seçin.",
                         "en": "Select at least one sample."},
    "tasima_gecersiz": {"tr": "Seçilenlerden biri artık tankta değil (bu arada çözülmüş "
                              "ya da taşınmış olabilir). Hiçbir şey yazılmadı; güncel "
                              "listeden yeniden seçin.",
                        "en": "One of the selected samples is no longer in the tank. "
                              "Nothing was saved; select again from the current list."},
    "tasima_tarih_once": {"tr": "Taşındığı gün seçilen örneklerden birinin "
                                "dondurulmasından önce olamaz.",
                          "en": "The date cannot be before one of the selected freezings."},
    "tasima_excel_baslik": {"tr": "Adı bu hastaya benzeyen Excel kayıtları",
                            "en": "Excel records with this patient's name"},
    "tasima_excel_ipucu": {
        "tr": "Cryo Excel'inde duran ama programda tüpü bulunamamış satırlar. Ad tek "
              "başına kesin değildir: tarihe, içeriğe ve eşin adına bakın. Bu "
              "hastanınsa işaretleyin; tanktan çıkarılır.",
        "en": "Rows of the cryo map Excel with no tube in the program. A name alone "
              "is not proof: check the date, content and partner. Tick it if it "
              "belongs to this patient; it is removed from the tank."},
    "tasima_excel_arama_ipucu": {
        "tr": "Programda tüpü olmayan Excel satırları: hastanın taşıma ekranında ya da "
              "kendi sayfasından \"Tanktan çıkarıldı\" ile işaretlenir.",
        "en": "Excel rows with no tube in the program: marked on the patient's "
              "transfer screen or on their own page."},
    "tasima_excel_geri_ipucu": {
        "tr": "Geri almak için kaydı açıp \"Tanka geri koy\"a basın; \"Bu taşımayı "
              "geri al\" yalnızca programdaki tüpleri geri koyar.",
        "en": "To undo, open the record and choose \"Put back in the tank\"; "
              "\"Undo this transfer\" restores only the program's straws."},
    "tasima_esin_dosyasi": {"tr": "Eşin ayrı dosyasındaki örnekler",
                            "en": "Samples in the partner's own file"},
    "tasima_hasta_baglanti": {"tr": "Hastanın bütün örnekleri için: Taşınma",
                              "en": "For all of the patient's samples: Transfers out"},
    "tasindi_rozet": {"tr": "Taşındı", "en": "Moved"},

    # ---- çözme (thaw) ----
    "konum_girilmemis_uzun": {"tr": "konum girilmemiş",
                              "en": "location not entered"},
    "tasiyici_cozme_uyari": {
        "tr": "Bu taşıyıcıda <strong>{n} embriyo</strong> var. Taşıyıcı "
              "çözüldüğünde hepsi etkilenir; her biri için sağkalım girilmeli.",
        "en": "This carrier holds <strong>{n} embryos</strong>. Thawing the "
              "carrier affects all of them; survival must be entered for each."},
    "cozme_hangi_tedavi": {"tr": "Bu çözme hangi tedavi için?",
                           "en": "Which treatment is this thaw for?"},
    "thaw_cycle_ipucu": {
        "tr": "Çözme bu tedavinin kaydına yazılır. Embriyo canlı çıkmasa da o "
              "tedavide çözüldüğü görünür.",
        "en": "The thaw is recorded against this cycle. Even if the embryo "
              "does not survive, it still shows as thawed for that treatment."},
    # v6.155: çözme yalnızca ayrı bir FET / Yumurta Çözme tedavisi için.
    "cozme_tedavisi_sec": {
        "tr": "Bu çözme hangi tedavi için? Listeden seç ya da yeni bir tedavi "
              "başlat. Çözme, embriyonun dondurulduğu tedaviye yazılmaz.",
        "en": "Which treatment is this thaw for? Choose one or start a new "
              "treatment. A thaw is not recorded against the freezing cycle."},
    "cozme_tedavi_yok": {
        "tr": "Bu hastanın çözme yapılabilecek bir tedavisi yok. Çözmeden önce "
              "yeni bir tedavi başlat:",
        "en": "This patient has no treatment a thaw can be recorded for. "
              "Start one first:"},
    "cozme_yeni_tedavi_ipucu": {
        "tr": "Çözme ayrı bir tedavidir; embriyonun dondurulduğu IVF/ICSI "
              "tedavisine yazılmaz. Yeni tedavi açılır, lab kayıt numarası "
              "program tarafından verilir.",
        "en": "A thaw is a separate treatment. A new cycle is opened and "
              "numbered by the program."},
    "fet_kultur_yalniz_cleavage": {
        "tr": "FET (3→5)'te yalnızca cleavage embriyosu çözülür; bu tüpte "
              "blastokist var.",
        "en": "FET (3→5) thaws cleavage embryos only; this straw holds a "
              "blastocyst."},
    "blastokist_tupu": {"tr": "Blastokist", "en": "Blastocyst"},
    # Cleavage'da birleşme (v6.157) -- kalite "Birleşme G2". Kısası numara
    # şeridinde ("3-Bir."), "8H"nin yerinde.
    "birlesme": {"tr": "Birleşme", "en": "Compaction"},
    "birlesme_kisa": {"tr": "Bir.", "en": "Comp."},
    "yeni_tedavi_baslat": {"tr": "Yeni tedavi başlat: {n}",
                           "en": "Start new cycle: {n}"},
    "tedavi_seciniz": {"tr": "— Tedavi seç —", "en": "— Choose a cycle —"},
    "yeni_tedavi_acilamadi": {
        "tr": "Yeni tedavi açılamadı (lab kayıt numarası çakıştı). Tekrar dene.",
        "en": "Could not open a new cycle (number clash). Try again."},
    "cozme_saati": {"tr": "Çözme saati", "en": "Thaw time"},
    "ikinci_kontrol_saati": {"tr": "İkinci kontrol saati",
                             "en": "Second check time"},
    "ikinci_kontrol_ipucu": {
        "tr": "Re-expansion değerlendirmesinin yapıldığı saat. Henüz "
              "yapılmadıysa boş bırak, sonra doldur.",
        "en": "The time the re-expansion assessment was made. Leave it empty "
              "if it has not been done yet and fill it in later."},
    "cozme_notu": {"tr": "Not", "en": "Note"},
    "cozme_notu_ipucu": {
        "tr": "Embriyoloji Özet formunun NOTLAR kutusuna, protokol notunun "
              "altına eklenir.",
        "en": "Added to the Embryology Summary form's NOTES box, below the "
              "protocol note."},
    "cozme_sonrasi": {"tr": "Çözme sonrası", "en": "After thaw"},
    "ikinci_kontrol": {"tr": "İkinci kontrol", "en": "Second check"},
    "fotograf_n": {"tr": "fotoğraf {n}", "en": "photo {n}"},
    "bu_fotografi_sil": {"tr": "Bu fotoğrafı sil", "en": "Delete this photo"},
    "fotograf_ekle_kucuk": {"tr": "fotoğraf ekle", "en": "add photo"},
    "arti_ekle": {"tr": "+ ekle", "en": "+ add"},
    "canlilik_orani": {"tr": "Canlılık oranı (%)", "en": "Viability (%)"},
    "re_expansion": {"tr": "Re-expansion (%)", "en": "Re-expansion (%)"},
    "canlilik_reexp_ipucu": {
        "tr": "Canlılık: çözme anında canlı kalan hücre oranı. Re-expansion: "
              "ikinci kontroldeki yeniden genişleme.",
        "en": "Viability: the proportion of cells still alive at the moment of "
              "thaw. Re-expansion: the re-expansion seen at the second check."},
    "tasiyici_bos": {"tr": "Bu taşıyıcı boş.", "en": "This carrier is empty."},
    "cozme_bosaltma_uyari": {
        "tr": "Kaydedince taşıyıcı <strong>boşaltıldı</strong> işaretlenir ve "
              "konumu haritada boşa düşer.",
        "en": "On save the carrier is marked <strong>emptied</strong> and its "
              "location is freed on the map."},
    "cozmeyi_kaydet": {"tr": "Çözmeyi kaydet", "en": "Save thaw"},

    # ---- cycle çözme ekranı ----
    "cozme_thaw": {"tr": "Çözme (thaw)", "en": "Thaw"},
    "thaw_goc_gerekli": {
        "tr": "Çözmelerin hangi tedavi için yapıldığı henüz kaydedilmiyor. "
              "Terminalde <code>python goc_024.py</code> çalıştır.",
        "en": "Which treatment each thaw was done for is not recorded yet. "
              "Run <code>python goc_024.py</code> in a terminal."},
    "tankta_duran_tasiyicilar": {"tr": "Tankta duran taşıyıcılar",
                                 "en": "Carriers still in the tank"},
    "fet_tum_tasiyicilar": {
        "tr": "Hastanın tüm tedavilerindeki taşıyıcılar listelenir.",
        "en": "Carriers from all of this patient's treatments are listed."},
    "donduruldugu_cycle": {"tr": "dondurulduğu tedavi", "en": "frozen in cycle"},
    "icerigi_gor": {"tr": "içeriği gör", "en": "view contents"},
    "coz_dugme": {"tr": "Çöz", "en": "Thaw"},
    "fet_tasiyici_yok": {"tr": "Bu hastanın tankta duran taşıyıcısı yok.",
                         "en": "This patient has no carriers in the tank."},
    "cycle_tasiyici_yok": {"tr": "Bu tedaviye ait tankta duran taşıyıcı yok.",
                           "en": "No carriers from this cycle are in the tank."},
    "bu_tedavide_cozulenler": {"tr": "Bu tedavide çözülenler",
                               "en": "Thawed in this treatment"},
    "transfer_edilen": {"tr": "transfer edilen", "en": "transferred"},
    "canlilik_kucuk": {"tr": "canlılık", "en": "viability"},
    "kaynak": {"tr": "kaynak", "en": "source"},
    "transfer_edildi": {"tr": "transfer edildi", "en": "transferred"},
    "transfer_edilmedi": {"tr": "transfer edilmedi", "en": "not transferred"},
    "cozulmus_tasiyicilar": {"tr": "Çözülmüş taşıyıcılar",
                             "en": "Thawed carriers"},
    "n_cozme_kaydi": {"tr": "{n} çözme kaydı", "en": "{n} thaw records"},
    "n_cozme_kaydi_tekil": {"tr": "{n} çözme kaydı", "en": "{n} thaw record"},
    "vitrifikasyon_ekrani": {"tr": "Vitrifikasyon ekranı",
                             "en": "Vitrification screen"},

    # ---- ICSI ----
    "henuz_oosit_yok_icsi": {
        "tr": "Bu tedavide henüz yumurta yok.",
        "en": "There are no oocytes in this cycle yet."},
    "once_denudasyon": {"tr": "Önce denüdasyon ekranından yumurtaları oluştur.",
                        "en": "Create the oocytes from the denudation screen first."},
    "denudasyon_ekrani": {"tr": "Denüdasyon ekranı", "en": "Denudation screen"},
    # Yumurta Çözme (v6.147): ICSI/fertilizasyon/cleavage ekranlarının
    # yumurtaları bu tedavi için çözülenler.
    "henuz_cozulen_yumurta_yok": {
        "tr": "Bu tedavide henüz çözülen yumurta yok.",
        "en": "No oocytes have been thawed in this cycle yet."},
    "once_cozme": {"tr": "Önce çözme ekranından yumurtaları çöz.",
                   "en": "Thaw the oocytes from the thaw screen first."},
    "cozmede_dejenere_uyari": {
        "tr": "Bu yumurta çözmede dejenere çıktı.",
        "en": "This oocyte was degenerate at thaw."},
    "cozmede_dejenere_form_yok": {
        "tr": "Çözmede dejenere çıktığı için bu yumurtaya ICSI kaydı girilmiyor.",
        "en": "No ICSI record is entered for this oocyte because it was "
              "degenerate at thaw."},
    "hata_cozmeden_once": {
        "tr": "İşlem saati bu tedavideki çözmeden ({z}) önce olamaz. Saati "
              "düzeltip yeniden kaydet.",
        "en": "The procedure time cannot be before the thaw in this cycle "
              "({z}). Correct the time and save again."},
    "n_m_kaydedildi": {"tr": "{n} / {m} kaydedildi", "en": "{n} / {m} recorded"},
    "bu_fotografi_sil_uzun": {"tr": "Bu fotoğrafı sil", "en": "Delete this photo"},
    # v6.35'ten beri hiçbir şablon çağırmıyor: fotoğrafsız örneğin yerini
    # artık _kareler.html `yer()` kutusu tutuyor. Anahtar duruyor, çeviri
    # dosyasından silmenin faydası yok.
    "bu_asamada_fotograf_yok": {"tr": "Bu aşamaya ait fotoğraf yok.",
                                "en": "No photo for this stage."},
    "maturasyon": {"tr": "Maturasyon", "en": "Maturation"},
    "oosit_bulgulari": {"tr": "Yumurta bulguları", "en": "Oocyte findings"},
    "bulgu_yok": {"tr": "Bulgu yok", "en": "No findings"},
    # ICSI'nin genel bulguları (v6.200): yumurtanın değil tedavinin.
    "genel_bulgular": {"tr": "Genel bulgular", "en": "General findings"},
    "genel_bulgular_ipucu": {
        "tr": "Bütün tedavi için. ART Lab formunun en altındaki Yorum satırına yazılır.",
        "en": "For the whole treatment. Printed on the Comment line at the bottom of the ART Lab form."},
    "genel_bulgu_yumurta": {"tr": "Yumurta", "en": "Oocyte"},
    "genel_bulgu_sperm": {"tr": "Sperm", "en": "Sperm"},
    "genel_bulgu_diger": {"tr": "Diğer", "en": "Other"},
    "genel_bulgu_diger_ipucu": {"tr": "Listede olmayan bir bulgu varsa buraya yazın.",
                                "en": "Type a finding that is not in the list."},
    "oosit_degerlendirmesi": {"tr": "Yumurta değerlendirmesi",
                              "en": "Oocyte assessment"},
    "temizle": {"tr": "Temizle", "en": "Clear"},
    "tamam": {"tr": "Tamam", "en": "Done"},
    "enjeksiyon": {"tr": "Enjeksiyon", "en": "Injection"},
    "yapildi": {"tr": "Yapıldı", "en": "Performed"},
    "yapilmadi": {"tr": "Yapılmadı", "en": "Not performed"},
    # Karşılığı kullanıcıya (embriyolog) soruldu ve 2026-09-10'da onaylandı:
    # "Penetration difficulty". Oolemma breakage / zona penetration değil.
    "gecis_zorlugu": {"tr": "Geçiş zorluğu", "en": "Penetration difficulty"},
    "enjeksiyon_sonucu": {"tr": "Enjeksiyon sonucu", "en": "Injection outcome"},
    "basarili": {"tr": "Başarılı", "en": "Successful"},
    "dejenere": {"tr": "Dejenere", "en": "Degenerate"},
    "islem_saati": {"tr": "İşlem saati", "en": "Procedure time"},
    "islem_saati_ipucu": {
        "tr": "Şu an dolu geliyor. Geriye dönük kayıt giriyorsan değiştir.",
        "en": "Prefilled with the current time. Change it if you are entering "
              "a record after the fact."},
    "kaydet_sonraki_oosit": {"tr": "Kaydet ve sonraki yumurta",
                             "en": "Save and next oocyte"},
    "zaman_operator_otomatik": {
        "tr": "Zaman ve operatör otomatik kaydedilir.",
        "en": "Time and operator are recorded automatically."},
    "oosit_n_fotograf_ekle": {"tr": "Yumurta {n} için fotoğraf ekle",
                              "en": "Add a photo for oocyte {n}"},
    "secimleri_geri_al": {"tr": "Seçimleri geri al", "en": "Reset selections"},
    "bu_oositin_kaydini_sil": {"tr": "Bu yumurtanın kaydını sil",
                               "en": "Delete this oocyte's record"},

    # ---- snapshot / eşleştirme ----
    "n_kare_bekliyor": {"tr": "Kamera klasöründe {n} kare bekliyor",
                        "en": "{n} frames waiting in the camera folder"},
    "n_kare_bekliyor_tekil": {"tr": "Kamera klasöründe {n} kare bekliyor",
                              "en": "{n} frame waiting in the camera folder"},
    "kareyi_oosite_ekle": {"tr": "Bu kareyi yumurta {n}'e ekle",
                           "en": "Add this frame to oocyte {n}"},
    "n_karenin_hepsini_ekle": {"tr": "{n} karenin hepsini ekle",
                               "en": "Add all {n} frames"},
    "oositlere_dagit": {"tr": "yumurtalara tek tek dağıt ({n} kare)",
                        "en": "distribute to oocytes one by one ({n} frames)"},
    "oositlere_dagit_tekil": {"tr": "yumurtalara tek tek dağıt ({n} kare)",
                              "en": "distribute to oocytes one by one ({n} frame)"},
    "goruntu_eslestirme": {"tr": "Görüntü eşleştirme", "en": "Match images"},

    # ---- fertilizasyon ----
    "fertilizasyon_kontrolu": {"tr": "Fertilizasyon kontrolü",
                               "en": "Fertilization check"},
    "icsiden_bu_yana": {
        "tr": "ICSI'den bu yana <strong>{n} saat</strong> · hedef {h} saat",
        "en": "<strong>{n} hours</strong> since ICSI · target {h} hours"},
    "icsiden_bu_yana_tekil": {
        "tr": "ICSI'den bu yana <strong>{n} saat</strong> · hedef {h} saat",
        "en": "<strong>{n} hour</strong> since ICSI · target {h} hours"},
    "icsi_kaydi_yok": {"tr": "Bu yumurtaya ICSI kaydı yok",
                       "en": "There is no ICSI record for this oocyte"},
    "icsi_yapilmadi": {"tr": "ICSI yapılmadı", "en": "ICSI was not performed"},
    "icsi_yapilmadi_fert_form_yok": {
        "tr": "ICSI yapılmadığı için bu yumurtaya fertilizasyon kaydı girilmiyor.",
        "en": "No fertilization record is entered for this oocyte because "
              "ICSI was not performed."},
    # Dejenere / maturasyon kısaltmaları (v6.139). Numara şeridindeki
    # kutucuk dar; yalnızca uzun iki etiketin kısaltması var, MII/MI/GV
    # kendi `liste_degeri` etiketiyle basılıyor (app._mat_kisa).
    "mat_kisa_degenere": {"tr": "Dej.", "en": "Deg."},
    "mat_kisa_atretik": {"tr": "Atr.", "en": "Atr."},
    "dejenere_uyari": {
        "tr": "Bu yumurta dejenere olarak işaretlendi.",
        "en": "This oocyte was marked as degenerate."},
    "dejenere_form_yok": {
        "tr": "Dejenere olduğu için bu yumurtaya embriyo kaydı girilmiyor.",
        "en": "No embryo record is entered for this oocyte because it is "
              "degenerate."},
    "maturasyon_kucuk": {"tr": "maturasyon", "en": "maturation"},
    "yine_de_fert_girilebilir": {
        "tr": "Yine de fertilizasyon kaydı girebilirsin.",
        "en": "You can still enter a fertilization record."},
    "sonuc": {"tr": "Sonuç", "en": "Outcome"},
    "pronukleus_sayisi": {"tr": "Pronükleus sayısı", "en": "Number of pronuclei"},
    "pn_skoru_z": {"tr": "PN skoru (Z)", "en": "PN score (Z)"},
    "z_sadece_2pn": {"tr": "Z sınıflaması yalnız 2PN için tanımlıdır.",
                     "en": "The Z classification is defined for 2PN only."},
    "zigot_bulgulari": {"tr": "Zigot bulguları", "en": "Zygote findings"},

    # ---- gün 2/3 (cleavage) ----
    # Kardes ekranin kalibi: "Blastokist · Gün 5". Menu "Cleavage" derken
    # ekranin basligi aşama adini hiç taşımıyordu (v6.60).
    "gun_n_degerlendirme": {"tr": "Cleavage · Gün {n}", "en": "Cleavage · Day {n}"},
    "gun_n_buyuk": {"tr": "Gün {n}", "en": "Day {n}"},
    "fert_kontrolunde_npn": {
        "tr": "Bu yumurta fertilizasyon kontrolünde {n}PN idi.",
        "en": "This oocyte was {n}PN at the fertilization check."},
    "hucre_sayisi": {"tr": "Hücre sayısı", "en": "Cell count"},
    "fragmentasyon": {"tr": "Fragmentasyon (%)", "en": "Fragmentation (%)"},
    # Bilgi kartında değer zaten "%10" diye yazılıyor; başlıkta ikinci bir
    # yüzde işareti olmasın.
    "fragmentasyon_kisa": {"tr": "Fragmentasyon", "en": "Fragmentation"},
    "simetri": {"tr": "Simetri", "en": "Symmetry"},
    "bulgular": {"tr": "Bulgular", "en": "Findings"},
    "gun_n_bulgulari": {"tr": "Gün {n} bulguları", "en": "Day {n} findings"},
    "skor": {"tr": "Skor", "en": "Score"},
    "otomatik_hesaplanir": {"tr": "otomatik hesaplanır",
                            "en": "calculated automatically"},
    "skor_ipucu": {
        "tr": "Boş bırakırsan hücre sayısı, simetri ve fragmentasyondan "
              "hesaplanır.",
        "en": "If you leave it empty it is calculated from the cell count, "
              "symmetry and fragmentation."},
    "su_anki_kayit": {"tr": "Şu anki kayıt:", "en": "Current record:"},
    "elle_girildi": {"tr": "elle girildi", "en": "entered manually"},
    "otomatik": {"tr": "otomatik", "en": "automatic"},
    "gun_n_kaydini_sil": {"tr": "Bu yumurtanın gün {n} kaydını sil",
                          "en": "Delete this oocyte's day {n} record"},

    # ---- blastokist ----
    "blastokist_gun_n": {"tr": "Blastokist · Gün {n}", "en": "Blastocyst · Day {n}"},
    "blast_goc_gerekli": {
        "tr": "<strong>Veritabanı güncellenmemiş.</strong><br>Kavitasyon "
              "seçeneği veya derece alanı eksik. Uygulamayı durdurup "
              "<code>python goc_010.py</code> ve <code>python goc_011.py</code> "
              "çalıştır.",
        "en": "<strong>The database has not been updated.</strong><br>The "
              "cavitation option or the grade field is missing. Stop the "
              "application and run <code>python goc_010.py</code> and "
              "<code>python goc_011.py</code>."},
    "henuz_oosit_yok_kisa": {"tr": "Bu tedavide henüz yumurta yok.",
                             "en": "There are no oocytes in this cycle yet."},
    "genisleme": {"tr": "Genişleme", "en": "Expansion"},
    "genisleme_ipucu": {
        "tr": "1 erken blastosöl · 2 yarım · 3 tam · 4 genişlemiş · "
              "5 hatching · 6 hatched",
        "en": "1 early blastocoel · 2 half · 3 full · 4 expanded · "
              "5 hatching · 6 hatched"},
    "derece": {"tr": "Derece", "en": "Grade"},
    "derece_ipucu": {
        "tr": "Morula, erken morula ve kavitasyon için. Arrest derecelendirilmez.",
        "en": "For morula, early morula and cavitation. Arrest is not graded."},
    "icm": {"tr": "ICM", "en": "ICM"},
    "trofektoderm": {"tr": "Trofektoderm", "en": "Trophectoderm"},
    "otomatik_birlestirilir": {"tr": "otomatik birleştirilir",
                               "en": "combined automatically"},
    "blast_skor_ipucu": {
        "tr": "Boş bırakırsan genişleme + ICM + TE birleştirilir (4AA gibi).",
        "en": "If you leave it empty, expansion + ICM + TE are combined "
              "(like 4AA)."},

    # ---- androloji (WHO semen analizi terimleri) ----
    "sperm_ornegi": {"tr": "Sperm örneği", "en": "Semen sample"},
    "yeni_artı": {"tr": "+ Yeni", "en": "+ New"},
    "sperm_ornek_ipucu": {
        "tr": "Genelde tek örnek. Yedek / ikinci örnek gerekiyorsa \"+ Yeni\".",
        "en": "Usually a single sample. Use \"+ New\" if a back-up or second "
              "sample is needed."},
    "ornek_bilgisi": {"tr": "Örnek bilgisi", "en": "Sample details"},
    "alinma_zamani": {"tr": "Alınma zamanı", "en": "Collection time"},
    "abstinans_gun": {"tr": "Abstinans (gün)", "en": "Abstinence (days)"},
    "alinma_yontemi": {"tr": "Alınma yöntemi", "en": "Collection method"},
    "likefaksiyon_zamani": {"tr": "Likefaksiyon zamanı", "en": "Liquefaction time"},
    "likefaksiyon_ipucu": {"tr": "Likefaksiyonun tamamlandığı saat.",
                           "en": "The time liquefaction was complete."},
    "hazirlama_yontemi": {"tr": "Hazırlama yöntemi", "en": "Preparation method"},
    "hazirlama_zamani": {"tr": "Hazırlama zamanı", "en": "Preparation time"},
    "ornek_notu": {"tr": "Örnek notu", "en": "Sample note"},
    "makroskopik": {"tr": "Makroskopik", "en": "Macroscopic"},
    "hacim_ml": {"tr": "Hacim (mL)", "en": "Volume (mL)"},
    "ph": {"tr": "pH", "en": "pH"},
    "gorunum_renk": {"tr": "Görünüm / renk", "en": "Appearance / colour"},
    "viskozite": {"tr": "Viskozite", "en": "Viscosity"},
    "bazal_analiz": {"tr": "Bazal analiz — hazırlık öncesi",
                     "en": "Baseline analysis — before preparation"},
    "analiz_zamani": {"tr": "Analiz zamanı", "en": "Analysis time"},
    "konsantrasyon": {"tr": "Konsantrasyon (milyon/mL)",
                      "en": "Concentration (million/mL)"},
    "total_motilite": {"tr": "Total motilite (%)", "en": "Total motility (%)"},
    "ilerleyen_pr": {"tr": "İlerleyen — PR (%)", "en": "Progressive — PR (%)"},
    "ilerlemeyen_np": {"tr": "İlerlemeyen — NP (%)",
                       "en": "Non-progressive — NP (%)"},
    "hareketsiz_im": {"tr": "Hareketsiz — IM (%)", "en": "Immotile — IM (%)"},
    "normal_morfoloji": {"tr": "Normal morfoloji (%)", "en": "Normal morphology (%)"},
    "vitalite": {"tr": "Vitalite (%)", "en": "Vitality (%)"},
    "tmsc": {"tr": "TMSC (milyon)", "en": "TMSC (million)"},
    "yuvarlak_hucre": {"tr": "Yuvarlak hücre (milyon/mL)",
                       "en": "Round cells (million/mL)"},
    "lokosit": {"tr": "Lökosit (milyon/mL)", "en": "Leukocytes (million/mL)"},
    "aglutinasyon": {"tr": "Aglütinasyon", "en": "Agglutination"},
    "bazal_analiz_notu": {"tr": "Bazal analiz notu", "en": "Baseline analysis note"},
    "tmsc_ipucu": {
        "tr": "TMSC ≈ hacim × konsantrasyon × motilite/100. Boş bırakılan alan "
              "\"girilmedi\" olarak saklanır.",
        "en": "TMSC ≈ volume × concentration × motility/100. A field left empty "
              "is stored as \"not entered\"."},
    "hazirlik_sonrasi_analiz": {"tr": "Hazırlık sonrası analiz",
                                "en": "Post-preparation analysis"},
    "hazirlik_hacmi": {"tr": "Hazırlık hacmi (mL)", "en": "Preparation volume (mL)"},
    "hazirlik_sonrasi_not": {"tr": "Hazırlık sonrası not",
                             "en": "Post-preparation note"},

    # ---- gebelik sonucu ----
    "bu_cyclede_transfer_edilen": {"tr": "Bu tedavide transfer edilen",
                                   "en": "Transferred in this cycle"},
    "transfer_kaydi_yok_uyari": {
        "tr": "Bu tedavide transfer kaydı yok. Sonuç yine de girilebilir, ama "
              "transferi önce kaydetmek kayıtları birbirine bağlar.",
        "en": "There is no transfer record in this cycle. The outcome can "
              "still be entered, but recording the transfer first links the "
              "records together."},
    "beta_hcg": {"tr": "Beta hCG", "en": "Beta hCG"},
    "artis_kat": {"tr": "{h} saatte {k} kat", "en": "{k}-fold in {h} hours"},
    "beta_girilmedi": {"tr": "Henüz beta hCG değeri girilmedi.",
                       "en": "No beta hCG value entered yet."},
    "olcum_zamani": {"tr": "Ölçüm zamanı", "en": "Measurement time"},
    "beta_ekle": {"tr": "Beta ekle", "en": "Add beta"},
    "beta_ipucu": {
        "tr": "Değer sayı olarak saklanır; pozitif/negatif eşiği sonradan "
              "istediğin gibi uygulanır. Birden fazla ölçüm girersen artış "
              "hızı hesaplanır.",
        "en": "The value is stored as a number; you can apply the "
              "positive/negative threshold however you like later. If you "
              "enter more than one measurement the rate of rise is calculated."},
    "klinik_gebelik": {"tr": "Klinik gebelik", "en": "Clinical pregnancy"},
    "var": {"tr": "Var", "en": "Present"},
    "yok": {"tr": "Yok", "en": "Absent"},
    "bilinmiyor": {"tr": "Bilinmiyor", "en": "Unknown"},
    "gebelik_kesesi_sayisi": {"tr": "Gebelik kesesi sayısı",
                              "en": "Number of gestational sacs"},
    "fetal_kalp_atimi": {"tr": "Fetal kalp atımı", "en": "Fetal heartbeat"},
    "pozitif": {"tr": "Pozitif", "en": "Positive"},
    "negatif": {"tr": "Negatif", "en": "Negative"},
    "kontrol_zamani": {"tr": "Kontrol zamanı", "en": "Check time"},
    # Kullanıcının kararı (2026-09-10): "Pregnancy status".
    # Önce "Termination" denendi, geri alındı — İngilizcede klinik
    # dilde gebelik sonlandırma demek, oysa liste "Devam ediyor" ve
    # "Canlı doğum" da içeriyor.
    "sonlanma": {"tr": "Sonlanma", "en": "Pregnancy status"},
    "henuz_belli_degil": {"tr": "— henüz belli değil", "en": "— not yet known"},
    "sonlanma_ipucu": {
        "tr": "Zamanla değişir: önce \"devam ediyor\", doğumdan sonra \"canlı "
              "doğum\". Ulaşılamayan hasta için \"takip kaybı\" — bu, sonuç "
              "oranlarının doğru çıkması için önemli.",
        "en": "This changes over time: first \"ongoing\", then \"live birth\" "
              "after delivery. Use \"lost to follow-up\" for a patient who "
              "cannot be reached — that matters for the outcome rates to come "
              "out right."},
    "dogum_zamani": {"tr": "Doğum zamanı", "en": "Delivery time"},
    "bebek_sayisi": {"tr": "Bebek sayısı", "en": "Number of babies"},
    "dogum_haftasi": {"tr": "Doğum haftası", "en": "Gestational week"},
    "sonucu_kaydet": {"tr": "Sonucu kaydet", "en": "Save outcome"},
    "son_guncelleme": {"tr": "Son güncelleme:", "en": "Last updated:"},
    "bebekler": {"tr": "Bebekler", "en": "Babies"},
    "n_bebek": {"tr": "{n}. bebek", "en": "Baby {n}"},
    "kiz": {"tr": "Kız", "en": "Girl"},
    "erkek": {"tr": "Erkek", "en": "Boy"},
    "dogum_kilosu": {"tr": "Doğum kilosu (kg)", "en": "Birth weight (kg)"},

    # ---- fotoğraf ekleme / görüntü silme ----
    "hangi_oosite": {"tr": "Hangi yumurtaya", "en": "To which oocyte"},
    "her_dosya_ayri_oosit": {"tr": "Her dosya ayrı yumurta olsun (yeni numaralar)",
                             "en": "Each file its own oocyte (new numbers)"},
    "oosite_baglama": {"tr": "Yumurtaya bağlama — tedavi arşivine koy",
                       "en": "Do not link to an oocyte — put in the cycle archive"},
    "asama": {"tr": "Aşama", "en": "Stage"},
    "dosyalar": {"tr": "Dosyalar", "en": "Files"},
    "foto_ekle_ipucu": {
        "tr": "Birden fazla seçebilirsin. \"Her dosya ayrı yumurta\" seçiliyse her "
              "dosya kendi yumurta numarasını alır; belirli bir yumurta seçiliyse "
              "hepsi ona eklenir. En fazla 25 MB, jpg/png/tif/bmp/webp.",
        "en": "You can select more than one. With \"each file its own oocyte\" "
              "every file gets its own oocyte number; if a specific oocyte is "
              "selected they are all added to it. Max 25 MB, "
              "jpg/png/tif/bmp/webp."},
    "yukle": {"tr": "Yükle", "en": "Upload"},
    "goruntuyu_sil": {"tr": "Görüntüyü sil", "en": "Delete image"},
    "goruntu_kalici_silinecek": {
        "tr": "<strong>Bu görüntü kalıcı olarak silinecek.</strong><br>Yumurta "
              "kaydı silinmez, yalnızca bu fotoğraf.",
        "en": "<strong>This image will be permanently deleted.</strong><br>The "
              "oocyte record is not deleted, only this photo."},
    "kamera_orijinali_kalir": {
        "tr": "Kamera klasöründeki orijinal dosyaya dokunulmaz; dosya tekrar "
              "eşleştirilebilir hale gelir.",
        "en": "The original file in the camera folder is untouched; it becomes "
              "available for matching again."},
    "silinecek_goruntu": {"tr": "Silinecek görüntü", "en": "Image to be deleted"},
    "ornek_kodu_alan": {"tr": "Örnek kodu", "en": "Sample code"},
    "ornege_bagli_degil": {"tr": "örneğe bağlı değil (tedavi arşivi)",
                           "en": "not linked to a sample (cycle archive)"},
    "kaynak_alan": {"tr": "Kaynak", "en": "Source"},
    "mikroskop_kamerasi": {"tr": "Mikroskop kamerası", "en": "Microscope camera"},
    "elle_yuklendi": {"tr": "Elle yüklendi", "en": "Uploaded manually"},
    "zaman": {"tr": "Zaman", "en": "Time"},

    # ---- silme ekranları (ortak) ----
    "yok_kucuk": {"tr": "yok", "en": "none"},
    "bagli_kayitlar": {"tr": "Bağlı kayıtlar", "en": "Linked records"},
    "silinecek_kayit": {"tr": "Silinecek kayıt", "en": "Record to be deleted"},
    "fotograf": {"tr": "Fotoğraf", "en": "Photo"},
    "islem_kaydi": {"tr": "İşlem kaydı", "en": "Procedure record"},
    "bulgu": {"tr": "Bulgu", "en": "Finding"},
    "kaydedilme": {"tr": "Kaydedilme", "en": "Recorded at"},
    "iptal_isaretlenir": {
        "tr": "İşlem kayıtları veritabanından silinmez, \"iptal\" işaretlenir. "
              "Değişiklik geçmişinde kim ne zaman temizlemiş görünür.",
        "en": "Procedure records are not removed from the database, they are "
              "marked \"cancelled\". The change history shows who cleared them "
              "and when."},

    # ---- oosit silme ----
    "oositi_sil": {"tr": "Yumurtayı sil", "en": "Delete oocyte"},
    "ornek_n": {"tr": "Örnek {n}", "en": "Sample {n}"},
    "oosit_silinemez": {"tr": "<strong>Bu yumurta silinemez.</strong>",
                        "en": "<strong>This oocyte cannot be deleted.</strong>"},
    "oosit_silinemez_sebep": {
        "tr": "{n} işlem kaydı bağlı (maturasyon, ICSI, fertilizasyon gibi). "
              "Klinik işlem kaydı olan bir yumurta silinmez. Önce ilgili işlem "
              "kayıtları iptal edilmeli.",
        "en": "{n} procedure records are linked (maturation, ICSI, "
              "fertilization and the like). An oocyte with clinical procedure "
              "records is not deleted. Cancel those records first."},
    "oosit_kalici_silinecek": {
        "tr": "<strong>Bu yumurta kalıcı olarak silinecek.</strong>",
        "en": "<strong>This oocyte will be permanently deleted.</strong>"},
    "bagli_n_fotograf_silinir": {
        "tr": "Bağlı {n} fotoğraf da silinir. Kameradan gelenler denüdasyon "
              "kuyruğuna geri döner, kamera klasöründeki orijinallere "
              "dokunulmaz.",
        "en": "The {n} linked photos are deleted too. Those that came from the "
              "camera return to the denudation queue; the originals in the "
              "camera folder are untouched."},
    "bagli_fotograf_yok": {"tr": "Bağlı fotoğraf yok.", "en": "No linked photos."},
    "numara_boslugu": {
        "tr": "Numara boşluğu oluşabilir: 1, 2, 4 gibi. Verilen yumurta "
              "kimlikleri kalıcıdır, geriye dönük numaralandırma yapılmaz.",
        "en": "A gap in the numbering may appear: 1, 2, 4 and so on. Oocyte "
              "identifiers once assigned are permanent; they are never "
              "renumbered."},

    # ---- ICSI kaydı silme ----
    "icsi_kaydini_sil": {"tr": "ICSI kaydını sil", "en": "Delete ICSI record"},
    "icsi_kaydi_bulunamadi": {
        "tr": "Bu yumurtaya ait kaydedilmiş bir ICSI kaydı yok.",
        "en": "There is no saved ICSI record for this oocyte."},
    "kaydete_basilmamis": {
        "tr": "Ekranda seçim yaptıysan Kaydet'e basılmamış demektir;",
        "en": "If you made selections on the screen, Save was not pressed;"},
    "secimleri_geri_al_ipucu": {
        "tr": "geri dönüp \"Seçimleri geri al\" ile temizleyebilirsin.",
        "en": "go back and clear them with \"Reset selections\"."},
    "icsi_kaydi_temizlenecek": {
        "tr": "<strong>Bu yumurtanın ICSI kaydı temizlenecek.</strong>",
        "en": "<strong>The ICSI record for this oocyte will be cleared.</strong>"},
    "oosit_fotograf_durur": {
        "tr": "Yumurta ve fotoğrafları durur, yalnızca aşağıdaki değerlendirme "
              "silinir. Yumurtayı yeniden değerlendirebilirsin.",
        "en": "The oocyte and its photos remain; only the assessment below is "
              "deleted. You can assess the oocyte again."},

    # ---- aşama kaydı silme ekranları ----
    "fert_kaydini_sil": {"tr": "Fertilizasyon kaydını sil",
                         "en": "Delete fertilization record"},
    "fert_kaydi_bulunamadi": {
        "tr": "Bu yumurtaya ait kaydedilmiş fertilizasyon kaydı yok.",
        "en": "There is no saved fertilization record for this oocyte."},
    "kaydete_basilmamis_kisa": {
        "tr": "Ekranda seçim yaptıysan Kaydet'e basılmamış demektir.",
        "en": "If you made selections on the screen, Save was not pressed."},
    "fert_kaydi_temizlenecek": {
        "tr": "<strong>Bu yumurtanın fertilizasyon kaydı temizlenecek.</strong>",
        "en": "<strong>The fertilization record for this oocyte will be "
              "cleared.</strong>"},
    "fert_sil_aciklama": {
        "tr": "Yumurta, fotoğrafları ve ICSI kaydı durur. Yalnızca aşağıdaki "
              "değerlendirme silinir.",
        "en": "The oocyte, its photos and the ICSI record remain. Only the "
              "assessment below is deleted."},
    "pn_sayisi": {"tr": "PN sayısı", "en": "PN count"},
    "pn_skoru": {"tr": "PN skoru", "en": "PN score"},
    "gun_n_kaydini_sil_baslik": {"tr": "Gün {n} kaydını sil",
                                 "en": "Delete day {n} record"},
    "gun_n_kaydi_bulunamadi": {"tr": "Bu yumurtaya ait kaydedilmiş gün {n} kaydı yok.",
                               "en": "There is no saved day {n} record for this "
                                     "oocyte."},
    "gun_n_degerlendirme_temizlenecek": {
        "tr": "<strong>Gün {n} değerlendirmesi temizlenecek.</strong>",
        "en": "<strong>The day {n} assessment will be cleared.</strong>"},
    "diger_asamalar_durur": {
        "tr": "Yumurta, fotoğrafları ve diğer aşamaların kayıtları durur.",
        "en": "The oocyte, its photos and the records of the other stages "
              "remain."},
    "blast_kaydini_sil": {"tr": "Blastokist kaydını sil",
                          "en": "Delete blastocyst record"},
    "blast_kaydi_bulunamadi": {
        "tr": "Bu yumurtaya ait gün {n} blastokist kaydı yok.",
        "en": "There is no day {n} blastocyst record for this oocyte."},
    "blast_degerlendirme_temizlenecek": {
        "tr": "<strong>Gün {n} blastokist değerlendirmesi temizlenecek.</strong>",
        "en": "<strong>The day {n} blastocyst assessment will be cleared."
              "</strong>"},
    "vit_kaydini_sil": {"tr": "Vitrifikasyon kaydını sil",
                        "en": "Delete vitrification record"},
    "vit_kaydi_yok": {"tr": "Bu embriyonun vitrifikasyon kaydı yok.",
                      "en": "This embryo has no vitrification record."},
    "vit_geri_alinacak": {"tr": "<strong>Vitrifikasyon kaydı geri alınacak.</strong>",
                          "en": "<strong>The vitrification record will be "
                                "undone.</strong>"},
    "vit_geri_alma_uyari": {
        "tr": "Embriyo \"dondurulmuş\" durumundan çıkar. Bu yalnızca "
              "<em>yanlış girilmiş bir kayıt</em> için kullanılmalı — gerçekten "
              "çözülen embriyo için thaw kaydı girilir.",
        "en": "The embryo leaves the \"frozen\" state. Use this only for a "
              "<em>record entered by mistake</em> — for an embryo that was "
              "really thawed, enter a thaw record instead."},
    "vit_kardes_var": {
        "tr": "Bu taşıyıcıda {n} embriyo var. Yalnızca bu embriyonun kaydı geri "
              "alınır, taşıyıcı ve diğerleri yerinde kalır.",
        "en": "This carrier holds {n} embryos. Only this embryo's record is "
              "undone; the carrier and the others stay where they are."},
    "vit_tek_embriyo": {
        "tr": "Bu taşıyıcıdaki tek embriyo. Kayıt geri alınınca taşıyıcı "
              "boşaltılmış işaretlenir ve konumu boşa düşer.",
        "en": "This is the only embryo on the carrier. When the record is "
              "undone the carrier is marked emptied and its location is freed."},
    "kaydi_geri_al_dugme": {"tr": "Kaydı geri al", "en": "Undo record"},

    # ---- denüdasyon ----
    "kamera_klasoru_yok": {"tr": "Kamera klasörü bulunamadı:",
                           "en": "Camera folder not found:"},
    "ayarlardan_duzelt": {"tr": "Ayarlardan düzeltilmeli.",
                          "en": "It must be corrected in the settings."},
    "denudasyon_zamani": {"tr": "Denüdasyon zamanı", "en": "Denudation time"},
    "denudasyon_zamani_ipucu": {
        "tr": "İlk yumurta kaydedildiğinde otomatik dolar. Gerekirse düzelt.",
        "en": "Filled in automatically when the first oocyte is recorded. "
              "Correct it if needed."},
    "toplandigi_over": {"tr": "Toplandığı over", "en": "Ovary collected from"},
    "belirtme": {"tr": "Belirtme", "en": "Unspecified"},
    "taraf_ipucu": {
        "tr": "Bundan sonra oluşturulan yumurtalara bu taraf yazılır. Sağ overi "
              "bitirip sola geçerken değiştir.",
        "en": "Oocytes created from now on are recorded with this side. "
              "Change it when you finish the right ovary and move to the left."},
    "bos_dosya_uyari": {"tr": "{n} dosya boş (0 bayt), atlandı:",
                        "en": "{n} file(s) empty (0 bytes), skipped:"},
    "kopyalama_yarim": {
        "tr": "Kopyalama yarım kalmış olabilir. Kaynağından yeniden kopyala.",
        "en": "The copy may be incomplete. Copy them again from the source."},
    "n_goruntu_bekliyor": {"tr": "{n} görüntü bekliyor", "en": "{n} images waiting"},
    "n_goruntu_bekliyor_tekil": {"tr": "{n} görüntü bekliyor", "en": "{n} image waiting"},
    "oosit_n": {"tr": "Yumurta {n}", "en": "Oocyte {n}"},
    "siradaki_goruntu": {"tr": "Sıradaki görüntü", "en": "Next image"},
    "kaydet_oosit_n": {"tr": "Kaydet → yumurta {n}", "en": "Save → oocyte {n}"},
    "ayni_oosite_ekle": {"tr": "Aynı yumurtaya ekle", "en": "Add to the same oocyte"},
    "atla": {"tr": "Atla", "en": "Skip"},
    "fotografsiz_oosit": {"tr": "Fotoğrafsız yumurta", "en": "Oocyte without photo"},
    "fotografsiz_oosit_ekle": {"tr": "Fotoğrafsız yumurta ekle",
                               "en": "Add oocyte without photo"},
    "bekleyen_kalmadi": {"tr": "Bekleyen görüntü kalmadı.",
                         "en": "No images left waiting."},
    "n_oosit_kaydedildi": {"tr": "{n} yumurta kaydedildi.",
                           "en": "{n} oocytes recorded."},
    "n_oosit_kaydedildi_tekil": {"tr": "{n} yumurta kaydedildi.", "en": "{n} oocyte recorded."},
    "klasorde_yeni_yok": {"tr": "Klasörde yeni görüntü yok.",
                          "en": "No new images in the folder."},
    "kameradan_kare_al": {"tr": "Kameradan kare alıp sayfayı yenile.",
                          "en": "Take a frame from the camera and refresh the page."},
    "yenile": {"tr": "Yenile", "en": "Refresh"},
    "son_kaydi_geri_al": {"tr": "Son kaydı geri al", "en": "Undo last record"},
    "elle_fotograf_ekle": {"tr": "Elle fotoğraf ekle", "en": "Add photo manually"},
    "kaydedilen_oositler": {"tr": "Kaydedilen yumurtalar", "en": "Recorded oocytes"},
    "henuz_oosit_kaydedilmedi": {"tr": "Henüz yumurta kaydedilmedi.",
                                 "en": "No oocytes recorded yet."},
    "n_oosit_hazirla": {"tr": "{n} yumurta için kayıt hazırla",
                        "en": "Prepare {n} oocyte records"},
    "n_oosit_hazirla_tekil": {"tr": "{n} yumurta için kayıt hazırla",
                              "en": "Prepare {n} oocyte record"},
    "oosit_hazirla_ipucu": {
        "tr": "OPU'da toplanan sayı kadar, fotoğrafsız yumurta kaydı açar "
              "(Yumurta 1, Yumurta 2, ...). Fotoğrafı sonra tek tek ekleyebilirsin.",
        "en": "Opens as many photo-less oocyte records as OPU collected "
              "(Oocyte 1, Oocyte 2, ...). You can add photos to each one later."},

    # ---- cycle detay ----
    "toplanan_oosit": {"tr": "Toplanan yumurta", "en": "Oocytes collected"},
    "sag": {"tr": "sağ", "en": "right"},
    # Rozet/etiket biçimi: cümle başı gibi büyük harfle. `sag`/`sol` küçük
    # harfli, cümle içinde geçtiği için ("sağ 5 · sol 4").
    "sag_rozet": {"tr": "Sağ", "en": "Right"},
    "sol_rozet": {"tr": "Sol", "en": "Left"},
    "sol": {"tr": "sol", "en": "left"},
    "kayitli": {"tr": "Kayıtlı", "en": "Recorded"},
    "folikul": {"tr": "Folikül", "en": "Follicles"},
    "zamanlar": {"tr": "Zamanlar", "en": "Times"},
    "protokol": {"tr": "Protokol", "en": "Protocol"},
    "protokol_notu": {"tr": "Protokol notu", "en": "Protocol note"},
    "tip": {"tr": "Tip", "en": "Type"},
    "toplam_doz": {"tr": "Toplam doz", "en": "Total dose"},
    "stim_gun": {"tr": "Stim. gün", "en": "Stim. days"},
    "e2_hcg_gunu": {"tr": "E2 (hCG günü)", "en": "E2 (hCG day)"},
    "endometrium": {"tr": "Endometrium", "en": "Endometrium"},
    # v6.110: "Oositler" listesinin yerini alan embriyoloji özeti; v6.112'de
    # üstteki Folikül/Toplanan kutusuyla birleşti, tek kutu oldu.
    "embriyoloji_ozeti": {"tr": "Embriyoloji özeti", "en": "Embryology summary"},
    "ozet_folikul": {"tr": "Folikül sayısı", "en": "Follicle count"},
    "ozet_toplanan": {"tr": "Toplanan yumurta sayısı", "en": "Oocytes collected"},
    # Yumurta Çözme'de "Toplanan"ın yerinde (v6.147).
    "ozet_cozulen": {"tr": "Çözülen yumurta sayısı", "en": "Oocytes thawed"},
    "ozet_m2": {"tr": "M2 (olgun) yumurta sayısı", "en": "M2 (mature) oocyte count"},
    "ozet_dollenen": {"tr": "Döllenen yumurta (2PN) sayısı",
                      "en": "Fertilized oocytes (2PN) count"},
    "ozet_cleavage": {"tr": "Cleavage sayısı", "en": "Cleavage count"},
    "ozet_blastokist": {"tr": "Blastokist sayısı", "en": "Blastocyst count"},
    "cycle_arsivi": {"tr": "Tedavi arşivi", "en": "Cycle archive"},
    "oosite_baglanmamis": {"tr": "Yumurtaya bağlanmamış fotoğraflar.",
                           "en": "Photos not linked to an oocyte."},
    "arsivi_temizle": {"tr": "arşivi temizle", "en": "clear archive"},
    "fotograf_ekle": {"tr": "Fotoğraf ekle", "en": "Add photo"},
    "doktor_notu": {"tr": "Doktor Notu", "en": "Doctor's Note"},
    "doktor_notu_yok": {"tr": "Henüz doktor notu eklenmedi.",
                        "en": "No doctor's note added yet."},
    "doktor_notu_ipucu": {
        "tr": "Fotoğraf veya PDF ekleyebilirsin (rapor, konsültasyon yazısı gibi).",
        "en": "You can add a photo or PDF (a report, a consult letter, etc.)."},
    "iptali_geri_al": {"tr": "İptali geri al", "en": "Undo cancellation"},
    "iptal_et_veya_sil": {"tr": "İptal et veya sil", "en": "Cancel or delete"},

    # ---- aşama adları (app.py ASAMA_SIRASI) ----
    # Klinik terimler iki dilde de aynı: OPU, ICSI, Transfer.
    "asama_opu": {"tr": "OPU", "en": "OPU"},
    "asama_androloji": {"tr": "Androloji", "en": "Andrology"},
    "asama_denudasyon": {"tr": "Denüdasyon", "en": "Denudation"},
    "asama_icsi": {"tr": "ICSI", "en": "ICSI"},
    "asama_fert": {"tr": "Fertilizasyon", "en": "Fertilization"},
    # Klinik terim, iki dilde de İngilizce kalır -- gün numarası değil,
    # embriyonun o andaki evresi (kullanıcının kararı, 2026-09-12).
    "asama_cleavage": {"tr": "Cleavage", "en": "Cleavage"},
    "asama_blast": {"tr": "Blastokist", "en": "Blastocyst"},
    "asama_vitrifikasyon": {"tr": "Vitrifikasyon", "en": "Vitrification"},
    "asama_thaw": {"tr": "Çözme", "en": "Thaw"},
    "asama_transfer": {"tr": "Transfer", "en": "Transfer"},
    "asama_gebelik": {"tr": "Gebelik sonucu", "en": "Pregnancy outcome"},

    # ---- tedavi tipi (app.py TIP_KISA) ----
    "tip_ivf_icsi": {"tr": "IVF/ICSI", "en": "IVF/ICSI"},
    "tip_fet": {"tr": "FET", "en": "FET"},
    "tip_fet_kultur": {"tr": "FET (3→5)", "en": "FET (D3→5)"},
    "tip_oosit_cryo": {"tr": "Yumurta Dondurma", "en": "Oocyte cryo"},
    "tip_yumurta_cozme": {"tr": "Yumurta Çözme", "en": "Egg Thaw"},
    "tip_taze": {"tr": "IVF/ICSI", "en": "IVF/ICSI"},

    # ---- işlemi yapan (paylaşılan parça) ----
    "islem_yapan": {"tr": "İşlemi yapan", "en": "Performed by"},
    "islem_yapan_ipucu": {
        "tr": "Bu aşamayı fiilen yapan kişi. Kaydı giren kişiden farklı olabilir.",
        "en": "The person who actually did this step. May differ from the "
              "person entering the record."},
    "ad_soyad": {"tr": "Ad soyad", "en": "Full name"},
    "opu_embriyologu": {"tr": "OPU Embriyoloğu", "en": "OPU Embryologist"},
    # Seçici seçilince kendisi kaydediyor (v6.208).
    "iy_kaydedildi": {"tr": "Kaydedildi: {ad}.", "en": "Saved: {ad}."},
    "iy_kaydedilemedi": {"tr": "Kaydedilemedi. Kaydet düğmesine basın.",
                         "en": "Could not save. Press Save."},
    "opu_hekimi": {"tr": "OPU Hekimi", "en": "OPU Physician"},

    # ---- örnek ızgarası ve bilgi kartı (her aşamada aynı düzen) ----
    "oosit_ekle": {"tr": "Yumurta ekle", "en": "Add oocyte"},
    "fotografsiz": {"tr": "fotoğrafsız", "en": "no photo"},
    "buyuk_goster": {"tr": "Büyük göster", "en": "Show larger"},
    "tam_ekran": {"tr": "Tam ekran", "en": "Full screen"},
    "numara": {"tr": "Numara", "en": "Number"},
    # Embriyo cycle değiştirmez; transferde "hangi cycle'dan geldi" sorusunun
    # cevabı specimen.cycle_id (bkz. CLAUDE.md "üç alan üç soruyu yanıtlar").
    "geldigi_cycle": {"tr": "Geldiği tedavi", "en": "Origin cycle"},
    "cozme_saati_kisa": {"tr": "Çözme saati", "en": "Thaw time"},
    "sagkalim": {"tr": "Sağkalım", "en": "Survival"},
    "canlilik": {"tr": "Canlılık oranı", "en": "Viability"},
    "transfer_durumu": {"tr": "Transfer", "en": "Transfer"},
    "kaynak_cycle": {"tr": "Kaynak tedavi", "en": "Source cycle"},
    "cozulen_embriyolar": {"tr": "Çözülen embriyolar", "en": "Thawed embryos"},
    "ornek_kodu_baslik": {"tr": "Örnek kodu", "en": "Specimen code"},
    "saat": {"tr": "Saat", "en": "Time"},
    "bitir": {"tr": "Bitir", "en": "Done"},
    "kare_sayisi": {"tr": "Kare", "en": "Frames"},
    "bu_ornege_ait_fotograf_yok": {
        "tr": "Bu kayda ait fotoğraf yok.",
        "en": "No photo for this record."},
    "duzenle_kaydi": {"tr": "Düzenle", "en": "Edit"},
    "henuz_kaydedilmedi": {"tr": "Henüz kaydedilmedi.", "en": "Not recorded yet."},
    "kaydedildi_rozet": {"tr": "Kaydedildi", "en": "Recorded"},
    "vazgec_duzenleme": {"tr": "Vazgeç", "en": "Cancel"},

    # ---- denüdasyon: kare bağlanamadı ----
    "kare_zaten_kaydedilmis": {
        "tr": "Bu kare zaten kaydedilmiş. Yeni kayıt oluşturulmadı.",
        "en": "This frame was already saved. No new record was created."},
    "kare_bulunamadi": {
        "tr": "Kare kaynak klasörde bulunamadı — taşınmış veya silinmiş "
              "olabilir. Yeni kayıt oluşturulmadı.",
        "en": "The frame was not found in the source folder — it may have "
              "been moved or deleted. No new record was created."},

    # ---- ana ekran ----
    # Hasta adlari bu ekranda YOK: program acikken ekrana bakan herkes
    # (hasta, hasta yakini, teknik servis) hasta listesini gormesin diye.
    # Adlar ancak /hastalar'a girilince gorunur.
    "ana_ekran": {"tr": "Ana ekran", "en": "Home"},
    "ana_menu": {"tr": "Ana menü", "en": "Main menu"},
    "menu": {"tr": "Menü", "en": "Menu"},

    # Ekran kendini tazeleme (v6.54). "yenile" zaten yukarida var.
    "yeni_kayit_var": {"tr": "Başka bir cihazdan yeni kayıt girildi.",
                       "en": "New data was entered from another device."},
    "yazdiklarin_gider": {"tr": "Yazdıkların kaybolur — önce kaydet.",
                          "en": "You will lose what you typed - save first."},

    # Ayni kaydi iki kisi duzenliyor (v6.55)
    "birlikte_duzenleme": {
        "tr": "Bu kaydı şu anda {kim} da düzenliyor.",
        "en": "{kim} is editing this record right now."},
    "birlikte_uyari": {
        "tr": "Aynı anda kaydederseniz biri ötekinin yazdığını siler.",
        "en": "If you both save, one will overwrite the other."},

    # ---- yapilacaklar listesi (v6.28): kagit klasorun karsiligi ----
    "yapilacaklar": {"tr": "Devam Eden Tedaviler", "en": "Ongoing Treatments"},
    "bugun_bitenler": {"tr": "Bugün Biten Tedaviler", "en": "Treatments Completed Today"},
    "bugun_biten_yok": {"tr": "Bugün biten işlem yok.",
                        "en": "Nothing finished today."},
    "tumu": {"tr": "Tümü", "en": "All"},
    "bu_ay": {"tr": "Bu ay", "en": "This month"},
    "ay": {"tr": "Ay", "en": "Month"},
    "yil": {"tr": "Yıl", "en": "Year"},
    "goster": {"tr": "Göster", "en": "Show"},

    # ---- takvim (v6.33) ----
    "takvim": {"tr": "Takvim", "en": "Calendar"},
    "yaklasanlar": {"tr": "Yaklaşan Tedaviler", "en": "Upcoming Treatments"},
    "yaklasan_yok": {"tr": "Önümüzdeki {n} günde planlanmış iş yok.",
                     "en": "Nothing planned in the next {n} days."},
    "planlanan_tarih": {"tr": "Planlanan tarih", "en": "Planned date"},
    "planlanan_tarih_ipucu": {
        "tr": "İleri tarihli iş için doldur. O tarihe kadar tedavi ana "
              "ekrandaki Yapılacaklar listesinde görünmez, takvimde durur.",
        "en": "Fill in for work planned ahead. Until that date the cycle "
              "stays off the home to-do list and sits in the calendar."},
    "planlandi_rozet": {"tr": "Planlandı", "en": "Planned"},
    "ayda_plan_yok": {"tr": "Bu ayda planlanmış iş yok.",
                      "en": "Nothing planned this month."},
    "n_planli_is": {"tr": "{n} planlanmış iş", "en": "{n} planned"},
    "n_planli_is_tekil": {"tr": "{n} planlanmış iş", "en": "{n} planned"},
    "bugun_rozet": {"tr": "Bugün", "en": "Today"},
    "takvim_goc_gerekli": {
        "tr": "Takvim için veritabanı güncel değil. Terminalde "
              "goc_hepsi.py çalıştır, sonra programı yeniden başlat.",
        "en": "The database is not up to date for the calendar. Run "
              "goc_hepsi.py in the terminal, then restart."},
    # Gun adlari -- ISO sirasi: 1 Pazartesi ... 7 Pazar
    "gun_1": {"tr": "Pazartesi", "en": "Monday"},
    "gun_2": {"tr": "Salı", "en": "Tuesday"},
    "gun_3": {"tr": "Çarşamba", "en": "Wednesday"},
    "gun_4": {"tr": "Perşembe", "en": "Thursday"},
    "gun_5": {"tr": "Cuma", "en": "Friday"},
    "gun_6": {"tr": "Cumartesi", "en": "Saturday"},
    "gun_7": {"tr": "Pazar", "en": "Sunday"},
    "onceki_ay": {"tr": "Önceki ay", "en": "Previous month"},
    "sonraki_ay": {"tr": "Sonraki ay", "en": "Next month"},
    "sayfalar": {"tr": "Sayfalar", "en": "Pages"},
    "onceki_sayfa": {"tr": "Önceki sayfa", "en": "Previous page"},
    "sonraki_sayfa": {"tr": "Sonraki sayfa", "en": "Next page"},
    "sayfa_x_y": {"tr": "Sayfa {x} / {y}", "en": "Page {x} / {y}"},
    "n_cycle_ayda": {"tr": "{n} tedavi", "en": "{n} cycles"},
    "n_cycle_ayda_tekil": {"tr": "{n} tedavi", "en": "{n} cycle"},
    "ayda_islem_yok": {"tr": "Bu ayda işlem yapılmış tedavi yok.",
                       "en": "No cycles worked on in this month."},
    # Ay adlari -- `ay_adi(yil, ay)` Jinja global'i bunlari okuyor
    "ay_1": {"tr": "Ocak", "en": "January"},
    "ay_2": {"tr": "Şubat", "en": "February"},
    "ay_3": {"tr": "Mart", "en": "March"},
    "ay_4": {"tr": "Nisan", "en": "April"},
    "ay_5": {"tr": "Mayıs", "en": "May"},
    "ay_6": {"tr": "Haziran", "en": "June"},
    "ay_7": {"tr": "Temmuz", "en": "July"},
    "ay_8": {"tr": "Ağustos", "en": "August"},
    "ay_9": {"tr": "Eylül", "en": "September"},
    "ay_10": {"tr": "Ekim", "en": "October"},
    "ay_11": {"tr": "Kasım", "en": "November"},
    "ay_12": {"tr": "Aralık", "en": "December"},
    # "vazgec" anahtari İngilizcede "Discard" diyor; bu ekranda embriyo
    # dondurmanin yaninda durdugu icin klinik "discard" ile karisirdi.
    "geri_don": {"tr": "Geri dön", "en": "Go back"},
    "yapilacak_yok": {
        "tr": "Laboratuvarda işi süren tedavi yok.",
        "en": "No cycles in progress in the lab."},
    "n_devam_eden": {"tr": "{n} devam eden tedavi", "en": "{n} ongoing treatments"},
    "n_devam_eden_tekil": {"tr": "{n} devam eden tedavi",
                           "en": "{n} ongoing treatment"},
    "biten_islemler": {"tr": "Biten işlemler", "en": "Completed"},
    "n_biten": {"tr": "{n} biten işlem", "en": "{n} completed"},
    "n_biten_tekil": {"tr": "{n} biten işlem", "en": "{n} completed"},
    "biten_yok": {"tr": "Henüz biten işlem yok.", "en": "Nothing completed yet."},
    "opu_gunu_n": {"tr": "OPU günü {n}", "en": "OPU day {n}"},
    "son_islem": {"tr": "Son işlem", "en": "Last step"},
    "henuz_islem_yok": {"tr": "işlem girilmedi", "en": "no steps recorded"},

    # Olay tipleri — `olay.tip` CHECK ile sinirli, kapali bir kume
    "olay_denudasyon": {"tr": "Denüdasyon", "en": "Denudation"},
    "olay_maturasyon_kontrolu": {"tr": "Matürasyon kontrolü",
                                 "en": "Maturity check"},
    "olay_icsi": {"tr": "ICSI", "en": "ICSI"},
    "olay_fertilizasyon_kontrolu": {"tr": "Fertilizasyon kontrolü",
                                    "en": "Fertilisation check"},
    "olay_cleavage_degerlendirme": {"tr": "Cleavage değerlendirme",
                                    "en": "Cleavage assessment"},
    "olay_blastokist_degerlendirme": {"tr": "Blastokist değerlendirme",
                                      "en": "Blastocyst assessment"},
    "olay_biyopsi": {"tr": "Biyopsi", "en": "Biopsy"},
    "olay_vitrifikasyon": {"tr": "Vitrifikasyon", "en": "Vitrification"},
    "olay_thaw": {"tr": "Çözme", "en": "Thaw"},
    "olay_transfer": {"tr": "Transfer", "en": "Transfer"},
    "olay_discard": {"tr": "Discard", "en": "Discard"},

    # ---- cycle bitisi ----
    "islemi_bitir": {"tr": "İşlemi bitir", "en": "Finish treatment"},
    "islemi_bitir_ipucu": {
        "tr": "Laboratuvar işi bitince tedavi yapılacaklar listesinden düşer. "
              "Kayıtlar silinmez, hasta ekranından görünmeye devam eder.",
        "en": "When lab work is done the cycle leaves the to-do list. "
              "Nothing is deleted; it stays on the patient's screen."},
    "bitis_sebebi": {"tr": "Nasıl bitti?", "en": "How did it end?"},
    "bitis_saati": {"tr": "Bitiş saati", "en": "Finish time"},
    "secili_rozet": {"tr": "Seçili", "en": "Current"},
    "hasta_kaydi": {"tr": "Hasta kartı", "en": "Patient card"},
    "bitis_dondurma": {"tr": "Dondurma tamamlandı", "en": "Freezing completed"},
    "bitis_dondurma_ipucu": {
        "tr": "Embriyolar / yumurtalar donduruldu, taze transfer yok.",
        "en": "Embryos / oocytes frozen, no fresh transfer."},
    "bitis_transfer": {"tr": "Transfer yapıldı", "en": "Transfer done"},
    "bitis_transfer_ipucu": {
        "tr": "Transfer tamamlandı, laboratuvarda yapılacak iş kalmadı.",
        "en": "Transfer completed, no lab work left."},
    "bitis_iptal": {"tr": "İptal", "en": "Cancelled"},
    "bitis_iptal_ipucu": {
        "tr": "Tedavi yarıda kaldı, iptal olarak işaretlenir.",
        "en": "Treatment stopped. The cycle is marked cancelled."},
    "iptal_detay_baslik": {
        "tr": "Listede yoksa yukarıdaki genel İptal'i kullan.",
        "en": "If not listed, use the general Cancelled option above."},
    "bitis_yumurta_cikmadi": {"tr": "Yumurta Çıkmadı İptal",
                              "en": "Cancelled — No Oocytes Retrieved"},
    "bitis_immatur_yumurta": {"tr": "İmmatür Yumurta İptal",
                              "en": "Cancelled — Immature Oocytes"},
    "bitis_fert_olmadi": {"tr": "Fertilizasyon Olmadı İptal",
                          "en": "Cancelled — No Fertilization"},
    "bitis_pn_arrest": {"tr": "PN Arrest İptal", "en": "Cancelled — PN Arrest"},
    "bitis_cleavage_arrest": {"tr": "Cleavage Arrest İptal",
                              "en": "Cancelled — Cleavage Arrest"},
    "bitis_gun5_arrest": {"tr": "5. Gün Arrest İptal",
                          "en": "Cancelled — Day 5 Arrest"},
    "tamamlandi_rozet": {"tr": "Tamamlandı", "en": "Completed"},
    "bitisi_geri_al": {"tr": "Listeye geri al", "en": "Reopen"},
    "bitirildi_n": {"tr": "{n} tarihinde bitirildi", "en": "Finished on {n}"},
    "bitis_sebebi_secilmedi": {
        "tr": "Bitiş sebebi seçilmedi.", "en": "No reason selected."},
    "goc_gerekli_kisa": {
        "tr": "Veritabanı güncel değil: goc_hepsi.py çalıştırılmalı.",
        "en": "Database not up to date: run goc_hepsi.py."},
    "goc_gerekli_uzun": {
        "tr": "Veritabanında bitiş kolonları yok. Terminalde "
              "goc_hepsi.py çalıştır, sonra programı yeniden başlat.",
        "en": "The finish columns are missing. Run goc_hepsi.py in the "
              "terminal, then restart the program."},
    "hasta_kayitlari": {"tr": "Hasta kayıtları", "en": "Patient records"},
    "aktif_hasta": {"tr": "Aktif hasta", "en": "Active patients"},
    "aktif_cycle": {"tr": "Aktif tedavi", "en": "Active cycles"},
    "bekleyen_kare": {"tr": "Bekleyen kare", "en": "Pending frames"},
    "dondurulmus": {"tr": "Dondurulmuş", "en": "Frozen"},
    "durum_ozeti": {"tr": "Durum", "en": "Status"},
    # v6.28'de degisti: ekranda artik hasta adi var, eski ipucu yalan
    # soyluyordu. Yerine listenin nasil bosaldigi anlatiliyor.
    "ana_ekran_ipucu": {
        "tr": "Listede laboratuvarda işi süren tedaviler var. İş bitince "
              "tedavi ekranındaki \u201cİşlemi bitir\u201d ile listeden düşer.",
        "en": "The list holds cycles still being worked on. Close one with "
              "\u201cFinish treatment\u201d on the cycle screen."},
    "aramayi_temizle": {"tr": "Aramayı temizle", "en": "Clear search"},
    "asamalar": {"tr": "Aşamalar", "en": "Stages"},

    # ---- hasta listesi ----
    "hastalar": {"tr": "Hastalar", "en": "Patients"},
    "hasta": {"tr": "Hasta", "en": "Patient"},
    "cycle": {"tr": "Tedavi", "en": "Cycle"},
    "cycleler": {"tr": "Tedaviler", "en": "Cycles"},
    "yetkisiz_ekran": {
        "tr": "ekranına erişim iznin yok. Gerekiyorsa yöneticiye söyle.",
        "en": "— you do not have access to this screen. Ask an administrator "
              "if you need it."},
    "ara_ipucu": {"tr": "Dosya no, ad, örnek kodu veya etiket",
                  "en": "File no, name, sample code or label"},
    "ornek_kodu_sonucu": {"tr": "Örnek kodu", "en": "Sample code"},
    "durum_aktif": {"tr": "Aktif", "en": "Active"},
    "excel_cikti": {"tr": "Excel çıktısı", "en": "Excel export"},
    # ---- istatistikler ----
    "istatistikler": {"tr": "İstatistikler", "en": "Statistics"},
    "genel_toplam": {"tr": "Genel toplam", "en": "Overall"},
    "oranlar": {"tr": "Oranlar", "en": "Rates"},
    "oran_mii": {"tr": "M2 oranı (MII / kayıtlı yumurta)",
                 "en": "M2 rate (MII / recorded oocytes)"},
    "oran_fert": {"tr": "Fertilizasyon oranı (2PN / ICSI)",
                  "en": "Fertilization rate (2PN / ICSI)"},
    "oran_blast": {"tr": "Blastokist oranı (blastokist / 2PN)",
                   "en": "Blastocyst rate (blastocyst / 2PN)"},
    "oran_gebelik": {"tr": "Klinik gebelik oranı (transfer başına)",
                     "en": "Clinical pregnancy rate (per transfer)"},
    "aylara_gore": {"tr": "Aylara göre", "en": "By month"},
    "tum_zamanlar": {"tr": "Tüm zamanlar", "en": "All time"},
    "gebelik_kisa": {"tr": "Gebelik", "en": "Pregnancy"},
    "aylik_oran_ipucu": {
        "tr": "Sütunlar yüzde oranıdır. Bir ayın sayılarını görmek için "
              "ayın adına dokunun.",
        "en": "The columns are percentages. Tap a month's name to see its "
              "counts."},
    "istatistik_ay_bos": {
        "tr": "Bu ayda kayıt yok.",
        "en": "No records in this month."},
    "istatistik_yil_bos": {
        "tr": "Bu yılda kayıt yok.",
        "en": "No records in this year."},
    "kayit_hasta": {"tr": "Yeni hasta", "en": "New patient"},
    "kayit_cycle": {"tr": "Yeni tedavi", "en": "New cycle"},
    "kayit_olay": {"tr": "İşlem", "en": "Procedure"},
    "istatistik_bos": {"tr": "Henüz kayıt yok.", "en": "No records yet."},
    "excele_aktar_istatistik": {"tr": "İstatistikleri Excel'e aktar",
                                "en": "Export statistics to Excel"},
    "istatistik_ipucu": {
        "tr": "Sayılar her açılışta kayıtlardan hesaplanıyor; ayrı bir sayaç "
              "tutulmuyor. Böylece hiçbir zaman gerçek kayıtlardan ayrı "
              "düşmüyorlar.",
        "en": "The numbers are computed from the records on every visit; no "
              "separate counter is kept, so they can never drift from the "
              "actual data."},
    # ---- Sağlık Bakanlığı aylık verileri (v6.201) ----
    # Sütun adları bakanlığın formundan, `disari.BAKANLIK_SUTUNLARI`'nda.
    "bakanlik_verileri": {"tr": "Sağlık Bakanlığı Aylık Verileri",
                          "en": "Ministry of Health Monthly Data"},
    "bakanlik_kisa": {"tr": "Bakanlık verileri", "en": "Ministry data"},
    "toplam": {"tr": "Toplam", "en": "Total"},
    "onceki_yil": {"tr": "Önceki yıl", "en": "Previous year"},
    "sonraki_yil": {"tr": "Sonraki yıl", "en": "Next year"},
    "bakanlik_ay_suruyor": {"tr": "ay bitmedi", "en": "month in progress"},
    "bakanlik_ipucu": {
        "tr": "Sayılar her açılışta kayıtlardan hesaplanıyor, saklanmıyor: "
              "geçmiş bir ayın kaydı sonradan düzeltilirse o ayın sayısı da "
              "düzelir. IUI ve embriyo imha programda tutulmuyor, tabloda yok.",
        "en": "The numbers are computed from the records on every visit; "
              "correcting an old record corrects that month too. IUI and "
              "embryo disposal are not kept in the program."},
    "bakanlik_tanimlar": {"tr": "Nasıl sayılıyor", "en": "How they are counted"},
    "bakanlik_tanim_opu": {
        "tr": "OPU'su yapılan tedavi, OPU gününün ayına.",
        "en": "Treatments with an OPU, in the month of the OPU."},
    "bakanlik_tanim_oosit": {
        "tr": "Yumurta dondurma işlemi: o ay yumurtası dondurulan tedavi "
              "(dondurulan yumurtanın adedi değil).",
        "en": "Oocyte freezing procedures: treatments whose oocytes were "
              "frozen that month (not the number of oocytes)."},
    "bakanlik_tanim_tese": {
        "tr": "Bütün cerrahi alımlar (TESE, mikroTESE, TESA, PESA, MESA): "
              "androlojideki alınma yöntemi ve sperm dondurmanın sebebi. Aynı "
              "kişi aynı gün bir kez.",
        "en": "All surgical retrievals (TESE, microTESE, TESA, PESA, MESA), "
              "from andrology and sperm freezing. Once per person per day."},
    "bakanlik_tanim_sperm": {
        "tr": "Sperm dondurma işlemi: aynı kişinin aynı gün dondurulan "
              "tüpleri bir sayılır.",
        "en": "Sperm freezing procedures: one per person per day, whatever "
              "the number of vials."},
    "bakanlik_tanim_siklus": {
        "tr": "Bütün tedaviler (IVF/ICSI, FET, FET (3→5), Yumurta Dondurma, "
              "Yumurta Çözme; iptal edilenler de), tedavinin gününün ayına: "
              "OPU, yoksa hCG; FET'te çözme ya da transfer; hiçbiri yoksa "
              "planlanan tarih ya da açılış.",
        "en": "All treatments of every type (cancelled ones too), in the "
              "month of the treatment day."},
    "bakanlik_tanim_transfer": {
        "tr": "Transfer işlemi: o ay transfer yapılan tedavi (taze ve donmuş); "
              "iki embriyo transfer edilen tedavi bir.",
        "en": "Transfer procedures (fresh and frozen): one per treatment, "
              "whatever the number of embryos."},
    "bakanlik_tanim_gebelik": {
        "tr": "Klinik gebelik, gebelik ekranındaki kontrol zamanının ayına. "
              "Kontrol zamanı girilmemiş gebelik sayılmaz.",
        "en": "Clinical pregnancies, in the month of the check on the "
              "pregnancy screen. Without a check time it is not counted."},
    "bakanlik_tanim_dogum": {
        "tr": "Sonucu \"Canlı doğum\" olan gebelik, doğum zamanının ayına; "
              "ikiz doğum bir. Doğum zamanı girilmemişse sayılmaz.",
        "en": "Pregnancies ending in a live birth, in the month of delivery; "
              "twins count once."},
    "bakanlik_tanim_hasta": {
        "tr": "O ay yeni kaydedilen hasta: hastanın ilk kaydının (kartın "
              "açılışı, ilk tedavisi ya da ilk sperm dondurması) ayı. "
              "Access'ten aktarılan hasta ilk tedavisinin ayında.",
        "en": "New patients: the month of the patient's first record (card, "
              "first treatment or first sperm freezing)."},
    "bakanlik_eksik_gebelik": {
        "tr": "Kontrol zamanı girilmemiş klinik gebelik ({n}) — GEBELİK "
              "SAYISI'na girmedi:",
        "en": "Clinical pregnancies without a check time ({n}), not counted:"},
    "bakanlik_eksik_dogum": {
        "tr": "Doğum zamanı girilmemiş canlı doğum ({n}) — CANLI DOĞUM "
              "SAYISI'na girmedi:",
        "en": "Live births without a delivery time ({n}), not counted:"},
    "excele_aktar_bakanlik": {"tr": "Bakanlık verilerini Excel'e aktar",
                              "en": "Export ministry data to Excel"},
    # ---- resmî formlar ----
    "formlar": {"tr": "Formlar", "en": "Forms"},
    "form_ozet": {"tr": "Embriyoloji Özet Formu",
                  "en": "Embryology Summary Form"},
    "form_artlab": {"tr": "ART Lab. Raporu", "en": "ART Lab. Report"},

    # Laboratuvarın kendi yüklediği formlar (v6.40)
    "lab_formlari": {"tr": "Laboratuvar formları", "en": "Laboratory forms"},
    "lab_formu_ipucu": {
        "tr": "Kendi formunuzu Excel'de açıp kutuların içine etiket yazın "
              "(örnek: {{dosya_no}}), .xlsx olarak kaydedip buraya yükleyin. "
              "Program etiketleri o tedavinin verisiyle değiştirip formu "
              "kâğıdınızın düzeninde basar.",
        "en": "Open your own form in Excel, type a label inside a box "
              "(for example {{dosya_no}}), save it as .xlsx and upload it "
              "here. The program replaces the labels with that cycle's data "
              "and prints the form in your own layout."},
    "form_yukle": {"tr": "Form yükle", "en": "Upload form"},
    "form_adi": {"tr": "Formun adı", "en": "Form name"},
    "form_adi_ipucu": {"tr": "Boş bırakılırsa dosyanın adı kullanılır",
                       "en": "Left empty, the file name is used"},
    "form_dosyasi": {"tr": "Excel dosyası (.xlsx)", "en": "Excel file (.xlsx)"},
    # Elindeki form .xls ise: yukleme kutusunun altinda adim adim anlatiliyor.
    # Ek bir kurulum gerekmesin diye Excel'in kendi "Farkli Kaydet"i kullaniliyor
    # -- .xls okumak programa kutuphane eklemek demekti (CLAUDE.md v6.40).
    "form_xls_baslik": {
        "tr": "Formum .xls ile bitiyor, ne yapmalıyım?",
        "en": "My form ends with .xls — what do I do?"},
    "form_xls_1": {"tr": "Formunuzu Excel'de açın.",
                   "en": "Open your form in Excel."},
    "form_xls_2": {"tr": "Dosya menüsünden Farklı Kaydet'i seçin.",
                   "en": "In the File menu choose Save As."},
    "form_xls_3": {
        "tr": "Dosya adının altındaki biçim kutusunu açın ve "
              "Excel Çalışma Kitabı (.xlsx) seçeneğine tıklayın.",
        "en": "Open the format box under the file name and click "
              "Excel Workbook (.xlsx)."},
    "form_xls_4": {"tr": "Kaydet'e basın.", "en": "Click Save."},
    "form_xls_5": {
        "tr": "Aynı klasörde sonu .xlsx olan yeni bir dosya belirir. "
              "Buraya yükleyeceğiniz dosya odur.",
        "en": "A new file ending in .xlsx appears in the same folder. "
              "That is the one you upload here."},
    "form_xls_mac": {
        "tr": "Mac'te o kutunun adı \"Dosya Biçimi\"dir; seçenek yine "
              "Excel Çalışma Kitabı (.xlsx).",
        "en": "On a Mac the box is called \"File Format\"; the option is "
              "again Excel Workbook (.xlsx)."},
    "form_xls_son": {
        "tr": "Formun görünümü değişmez: çizgiler, yazılar ve logo aynı kalır. "
              "Eski .xls dosyanız da yerinde durur.",
        "en": "The form itself does not change: lines, text and logo stay the "
              "same. Your old .xls file also stays where it is."},
    "form_etiketleri": {"tr": "Yazılabilecek etiketler",
                        "en": "Labels you can use"},
    "form_etiket_ipucu": {
        "tr": "Bu etiketleri formunuzdaki kutuların içine yazın. Kutuda başka "
              "yazı da olabilir: \"Dosya No: {{dosya_no}}\" gibi. Programda "
              "karşılığı olmayan bir etiket yazarsanız formda olduğu gibi "
              "görünür — yazım hatası gözden kaçmasın diye.",
        "en": "Type these labels inside the boxes of your form. A box may "
              "contain other text too, such as \"File no: {{dosya_no}}\". "
              "A label the program does not know is printed as it is, so a "
              "typo cannot slip through."},
    # Bu makinenin klasörleri (v6.41). Değer `yerel_ayar.json`'da, makine
    # adına göre bölümlü -- `lab.db` USB ile taşınıyor.
    "klasorler": {"tr": "Klasörler", "en": "Folders"},
    "klasorler_makine": {"tr": "Bu bilgisayar", "en": "This computer"},
    "klasorler_ipucu": {
        "tr": "Bu ayarlar yalnızca bu bilgisayara aittir. Program iki makinede "
              "kuruluysa her biri kendi klasörlerini kullanır; veritabanını "
              "USB ile taşımak bu yolları değiştirmez.",
        "en": "These settings belong to this computer only. If the program is "
              "installed on two machines each uses its own folders; carrying "
              "the database on a USB stick does not change these paths."},
    "goruntu_kaynak_klasor": {"tr": "Kamera klasörü",
                              "en": "Camera folder"},
    "goruntu_kaynak_klasor_ipucu": {
        "tr": "Mikroskop kamerasının fotoğrafı kaydettiği klasör. Program bu "
              "klasörü yalnızca okur, içine bir şey yazmaz. Var olmayan bir "
              "yol kabul edilmiyor: yazım hatası olursa kamera kuyruğu hep "
              "boş görünürdü.",
        "en": "The folder where the microscope camera saves its photos. The "
              "program only reads this folder, it never writes into it. A "
              "path that does not exist is refused: with a typo the camera "
              "queue would always look empty."},
    "goruntu_arsiv_klasor": {"tr": "Arşiv klasörü", "en": "Archive folder"},
    "goruntu_arsiv_klasor_ipucu": {
        "tr": "Program fotoğrafları buraya kopyalar ve ekranda buradan "
              "gösterir; kamera klasörü boşaltılsa da görüntüler durur. "
              "Yoksa oluşturulur.",
        "en": "The program copies the photos here and shows them from here, "
              "so images survive the camera folder being emptied. Created if "
              "it does not exist."},
    "yedek_klasor": {"tr": "Yedek klasörü", "en": "Backup folder"},
    "yedek_klasor_ipucu": {
        "tr": "Yedeğin yazılacağı yer — <b>başka bir diskte</b> olmalı, yoksa "
              "disk bozulduğunda yedek de gider. Takılı olmayan bir disk "
              "(örneğin E:) yazılabilir; oluşturulmaz, yedek alınırken "
              "aranır. Cryo Haritası değişince program buraya yedeği "
              "kendisi de alır (Yedekleme ekranı).",
        "en": "Where backups are written — it must be on <b>a different "
              "disk</b>, otherwise a disk failure takes the backup with it. A "
              "disk that is not plugged in (E: for example) may be entered; "
              "it is not created, it is looked for when a backup runs. When "
              "the Cryo map changes the program also backs up here by itself "
              "(Backup screen)."},
    "cryo_harita_klasor": {"tr": "Cryo haritası (Excel)", "en": "Cryo map (Excel)"},
    "cryo_harita_klasor_ipucu": {
        "tr": "Programın her değişiklikte yazdığı Cryo Haritası Excel'i "
              "(Cryo_Haritasi.xlsx ve son 30 günün kopyaları) buraya yazılır. "
              "Her gün 14:00'te \"Tüm veriler\" Excel'i de buraya yazılır "
              "(Tum_Veriler_<gün>.xlsx, son 30 gün) -- <b>bütün hasta "
              "kayıtlarını taşır</b>, klasörü buna göre seçin. Varsayılanı "
              "programın veri klasörü. Yoksa oluşturulur. Değişince dosya en "
              "geç bir dakika içinde yeni klasöre yazılır; eski klasördekiler "
              "silinmez.",
        "en": "The Cryo map Excel the program writes after every change "
              "(Cryo_Haritasi.xlsx and copies of the last 30 days) goes here. "
              "Every day at 14:00 the \"All data\" Excel is written here too "
              "(Tum_Veriler_<day>.xlsx, last 30 days) -- <b>it carries every "
              "patient record</b>, choose the folder accordingly. The default "
              "is the program's data folder. Created if it does not exist. "
              "After a change the file is written to the new folder within a "
              "minute; files in the old folder are not deleted."},
    # Elle yedekleme (v6.119, kullanıcının isteği: "Elle yedekleme olsun").
    # `/klasorler`'de, yedek klasörü ayarının hemen altında -- panel yine
    # `/yonetim` DEĞİL, o salt okunur kalıyor (v6.12).
    "yedekleme": {"tr": "Yedekleme", "en": "Backup"},
    "son_yedek": {"tr": "Son yedek", "en": "Last backup"},
    "hic_yedek_yok": {"tr": "Henüz hiç yedek alınmadı.",
                      "en": "No backup has been taken yet."},
    "simdi_yedekle": {"tr": "Şimdi yedekle", "en": "Back up now"},
    "yedekleniyor_uyari": {
        "tr": "Yedekleme sürerken sayfadan ayrılma; büyük arşivlerde birkaç "
              "dakika sürebilir.",
        "en": "Do not leave this page while backing up; it can take a few "
              "minutes for a large archive."},
    "yedek_alindi": {"tr": "Yedekleme tamamlandı.",
                     "en": "Backup completed."},
    "yedek_klasoru_yok_hata": {
        "tr": "Yedek klasörü ayarlanmamış. Önce yukarıdan kaydet.",
        "en": "Backup folder is not set. Save it above first."},
    "yedek_klasoru_yanlis_makine": {
        "tr": "'{yol}' bu işletim sisteminin yolu değil, yedek alınamadı.",
        "en": "'{yol}' is not a path for this operating system, backup not "
              "taken."},
    "yedekleme_basarisiz": {"tr": "Yedekleme başarısız",
                            "en": "Backup failed"},
    "yedekleme_ipucu": {
        "tr": "Veritabanının anlık bir kopyasını alır, doğrular; arşivdeki "
              "yeni fotoğrafları ve Cryo Haritası Excel'ini yedek klasörüne "
              "(Klasörler ekranı) kopyalar -- terminalden "
              "<code>python3 yedek.py</code> çalıştırmakla aynı iş. "
              "Saklanan: son 24 saatin bütün yedekleri, 14 güne kadar her "
              "günün sonuncusu, daha eskide her ayın ilki.",
        "en": "Takes a consistent snapshot of the database, verifies it, "
              "and copies new archive photos and the Cryo map Excel into the "
              "backup folder (Folders screen) -- the same work as running "
              "<code>python3 yedek.py</code> from a terminal. Kept: every "
              "backup of the last 24 hours, the last one of each day up to "
              "14 days, and the first one of each month after that."},
    # Cryo Haritası değişince alınan yedek (v6.216, `oto_yedek.py`).
    "oto_yedek": {"tr": "Otomatik yedek", "en": "Automatic backup"},
    "oto_yedek_ipucu": {
        "tr": "Cryo Haritası'nda bir değişiklik olunca (dondurma, çözme, "
              "taşıma, yer) program yedeği kendisi alır: değişiklikler "
              "bittikten bir iki dakika sonra, sürüp gidiyorsa en geç on "
              "dakikada. \"Şimdi yedekle\"nin aynısı. Program kapalıyken "
              "alınamaz; kapalıyken değişen harita açılınca yedeklenir. Cryo "
              "Haritası'nın değişmediği günlerde otomatik yedek alınmaz.",
        "en": "When the Cryo map changes (freezing, thawing, transfer, "
              "location) the program backs up by itself: a minute or two "
              "after the changes stop, at most ten minutes if they go on. "
              "Same as \"Back up now\". Nothing is backed up while the "
              "program is closed; a map that changed meanwhile is backed up "
              "when it opens. No automatic backup on days the Cryo map does "
              "not change."},
    "oto_yedek_guncel": {
        "tr": "Cryo Haritası'nın şu anki hali yedekli: {zaman} ({dosya}).",
        "en": "The Cryo map as it is now is backed up: {zaman} ({dosya})."},
    "oto_yedek_bekliyor": {
        "tr": "Yedeklenmemiş bir Cryo Haritası değişikliği var; değişiklikler "
              "bitince birkaç dakika içinde yedek alınacak.",
        "en": "There is a Cryo map change not backed up yet; it will be "
              "backed up within minutes once the changes stop."},
    "oto_yedek_henuz": {
        "tr": "Program açıldıktan sonraki ilk dakikada bakılıyor.",
        "en": "Checked within the first minute after the program starts."},
    "oto_yedek_ayarsiz": {
        "tr": "Otomatik yedek alınamıyor: yedek klasörü ayarlanmamış "
              "(Klasörler ekranı).",
        "en": "No automatic backup: the backup folder is not set (Folders "
              "screen)."},
    "oto_yedek_yanlis_makine": {
        "tr": "Otomatik yedek alınamıyor: yedek klasörü ({yol}) bu "
              "bilgisayarın yolu değil (Klasörler ekranı).",
        "en": "No automatic backup: the backup folder ({yol}) is not a path "
              "of this computer (Folders screen)."},
    "oto_yedek_klasor_yok": {
        "tr": "Otomatik yedek alınamıyor: yedek klasörü yok ({yol}). Disk "
              "takılı değilse takın, takılınca yedek alınır. Hiç yedek "
              "alınmadıysa bir kez \"Şimdi yedekle\"ye basın: klasörü o açar.",
        "en": "No automatic backup: the backup folder does not exist ({yol}). "
              "If the disk is not plugged in, plug it in and the backup runs. "
              "If no backup was ever taken, press \"Back up now\" once: it "
              "creates the folder."},
    "oto_yedek_hata": {
        "tr": "Son otomatik yedek alınamadı ({zaman}): {hata}. {dk} dakika "
              "sonra yeniden denenecek; ayrıntısı yedek.log'da.",
        "en": "The last automatic backup failed ({zaman}): {hata}. It is "
              "retried in {dk} minutes; details in yedek.log."},
    "oto_yedek_kisa": {
        "tr": "Her Cryo Haritası değişikliğinden sonra",
        "en": "After every Cryo map change"},
    # Her gün 14:00'te "Tüm veriler" (v6.216): Cryo haritası klasörüne.
    "tum_veri_cryo": {
        "tr": "Her gün {saat}'te \"Tüm veriler\" Excel'i de bu klasöre "
              "yazılır (Tum_Veriler_<gün>.xlsx, son {gun} gün): yönetici "
              "panelindeki \"Tüm veriyi Excel'e aktar\"ın aynısı, bütün "
              "hasta kayıtları.",
        "en": "Every day at {saat} the \"All data\" Excel is also written to "
              "this folder (Tum_Veriler_<day>.xlsx, last {gun} days): the same "
              "as \"Export all data to Excel\" in the admin panel, every "
              "patient record."},
    "tum_veri_son": {"tr": "Son: {ad} ({zaman})", "en": "Last: {ad} ({zaman})"},
    "tum_veri_yazilamadi": {
        "tr": "\"Tüm veriler\" yazılamadı ({zaman}): {hata}. On dakika sonra "
              "yeniden denenecek.",
        "en": "\"All data\" could not be written ({zaman}): {hata}. Retried "
              "in ten minutes."},

    # Yedekten geri yükleme (v6.120, kullanıcının isteği: "Yönetici isterse
    # yedekten geri çağırsın... Yönetici panelinden hepsini yapabilsin").
    # `geri_yukle.html`, `hasta_sil.html`'in iki kademeli yazılı onay +
    # tarayıcı confirm() deseninin aynısı. **Onay için yazılması gereken
    # metin ("GERİ YÜKLE") her iki dilde de sabit** -- sunucu tarafındaki
    # kontrol (`app.py` `klasorler_geri_yukle()`) dile bakmadan aynı
    # sabit stringi arıyor, o yüzden ekrandaki yönerge de dilden bağımsız
    # aynı kelimeyi göstermeli, yoksa İngilizce arayüzde kullanıcı ekranın
    # söylediğini yazar ama sunucu reddeder.
    "yedekten_geri_yukle": {"tr": "Yedekten geri yükle",
                            "en": "Restore from backup"},
    "geri_yukle_uyari_baslik": {
        "tr": "Bu işlem geri alınamaz şekilde risklidir.",
        "en": "This operation is irreversibly risky."},
    "geri_yukle_uyari_govde": {
        "tr": "Seçtiğin yedek, o yedeğin alındığı andan bu yana girilmiş "
              "TÜM hasta, tedavi, yumurta ve işlem kayıtlarının üzerine "
              "yazar. Devam etmeden önce mevcut veritabanının bir güvenlik "
              "kopyası otomatik alınır (yedek klasörüne "
              "<code>lab_ONCEKI_...</code> adıyla) -- yanlış yedek "
              "seçersen o kopyadan geri dönülebilir. Arşivdeki fotoğraflar "
              "bu işlemden etkilenmez, onlar ayrı bir yerde ve hiç "
              "silinmeden birikiyor.",
        "en": "The backup you pick overwrites ALL patient, treatment, "
              "oocyte and procedure records entered since that backup was "
              "taken. Before proceeding, a safety copy of the current "
              "database is taken automatically (named "
              "<code>lab_ONCEKI_...</code> in the backup folder) -- if you "
              "pick the wrong backup you can recover from that copy. "
              "Archive photos are not affected by this operation, they "
              "live separately and are never deleted."},
    "geri_yukle_hangi_yedek": {"tr": "Hangi yedek geri yüklensin?",
                               "en": "Which backup should be restored?"},
    "geri_yukle_onceki_hal": {"tr": "önceki hâlin güvenlik kopyası",
                              "en": "safety copy of a previous state"},
    "geri_yukle_onay1_etiket": {
        "tr": "1. Seçtiğin yedeğin dosya adını yaz",
        "en": "1. Type the filename of the backup you selected"},
    "geri_yukle_onay2_etiket": {
        "tr": "2. Onaylamak için <strong>GERİ YÜKLE</strong> yaz",
        "en": "2. Type <strong>GERİ YÜKLE</strong> to confirm"},
    "geri_yukle_confirm": {
        "tr": "{ad} geri yüklenecek. Bu işlem geri alınamaz. Devam edilsin mi?",
        "en": "{ad} will be restored. This cannot be undone. Continue?"},
    "geri_yukle_yedek_yok": {
        "tr": "Yedek klasöründe geri yüklenebilecek bir dosya bulunamadı.",
        "en": "No restorable file was found in the backup folder."},
    "geri_yukle_secim_yok": {"tr": "Bir yedek seçilmedi.",
                             "en": "No backup was selected."},
    "geri_yukle_dosya_yanlis": {"tr": "Dosya adı doğru yazılmadı.",
                                "en": "The filename was not typed correctly."},
    "geri_yukle_onay_yanlis": {
        "tr": "Onaylamak için 'GERİ YÜKLE' yazılmalı.",
        "en": "Type 'GERİ YÜKLE' to confirm."},
    "geri_yukleme_basarisiz": {"tr": "Geri yükleme başarısız",
                               "en": "Restore failed"},
    "geri_yuklendi_ozet": {
        "tr": "Geri yüklendi: {hasta} hasta, {cycle} tedavi, {specimen} "
              "örnek, {goruntu} fotoğraf kaydı.",
        "en": "Restored: {hasta} patients, {cycle} treatments, {specimen} "
              "specimens, {goruntu} photo records."},
    # v6.145, kullanıcının isteği: "Geri yüklemeden sonra da kendisi yapsın."
    "geri_yukleme_goc_uygulandi": {
        "tr": "Yedek eski bir sürümdendi: {n} veritabanı güncellemesi hemen "
              "uygulandı, programı yeniden açmana gerek yok.",
        "en": "The backup was from an older version: {n} database update(s) "
              "were applied right away, no restart needed."},
    "geri_yukleme_goc_hata": {
        "tr": "Bir veritabanı güncellemesi uygulanamadı ({ad}); ayrıntısı "
              "Yönetici panelinde. Bazı ekranlar eksik davranabilir.",
        "en": "A database update could not be applied ({ad}); details are on "
              "the admin panel. Some screens may behave incompletely."},

    # v6.121, kullanıcının isteği: "Yedekleme bölümünde Yedekleme olsun.
    # Klasörlerin altında zor bulunuyor." -- eylemler `/klasorler`'den
    # kendi ekranına (`/yedekleme`) taşındı.
    "geri_yukle_kisa_ipucu": {
        "tr": "Bir yedek seçip geri yükleyerek hastaları, tedavileri ve "
              "işlem kayıtlarını o yedeğin alındığı ana döndürebilirsin.",
        "en": "Pick a backup and restore it to return patients, treatments "
              "and procedure records to the moment that backup was taken."},
    "yedek_klasoru_degistir_ipucu": {
        "tr": "Yedeğin yazılacağı klasörü değiştirmek için "
              "<a href=\"/klasorler\">Klasörler</a> ekranı.",
        "en": "To change the folder backups are written to, see the "
              "<a href=\"/klasorler\">Folders</a> screen."},
    "yedekleme_yonetim_ipucu": {
        "tr": "Elle yedekleme ve yedekten geri yükleme için",
        "en": "For manual backup and restore, see"},

    "klasor_var": {"tr": "klasör bulundu", "en": "folder found"},
    "klasor_yok": {"tr": "klasör bulunamadı", "en": "folder not found"},
    # Klasör gezgini (v6.43). Tarayıcı sayfaya gerçek yolu vermediği için
    # gezilen klasörler **sunucunun** klasörleri.
    "gozat": {"tr": "Gözat", "en": "Browse"},
    "bu_klasoru_sec": {"tr": "Bu klasörü seç", "en": "Use this folder"},
    "ust_klasor": {"tr": "Üst klasör", "en": "Parent folder"},
    "en_ust": {"tr": "En üst", "en": "Top"},
    "alt_klasor_yok": {"tr": "İçinde klasör yok.", "en": "No folders inside."},
    "n_fotograf": {"tr": "Bu klasörde {n} fotoğraf var.",
                   "en": "{n} photos in this folder."},
    "klasor_okunamadi": {"tr": "Klasör okunamadı.",
                         "en": "The folder could not be read."},
    "yukleniyor": {"tr": "Yükleniyor…", "en": "Loading…"},
    # İşletim sisteminin kendi penceresi + arama (v6.44). Tarayıcı seçilen
    # klasörün yerini vermediği için program onu bu makinede arıyor.
    # Telefonun ana ekranına ekleme + karekod (v6.45).
    # Ana ekrandaki simgenin altında yazan ad (kullanıcının isteği: tam ad).
    # Telefon uzun adı kısaltıp "..." koyuyor; kısaltma istenirse buradan.
    "kisa_ad": {"tr": "Patient Data Center", "en": "Patient Data Center"},
    # Açılışta çalışan göçlerin durumu (v6.49).
    "goc_durumu": {"tr": "Veritabanı güncellemeleri", "en": "Database updates"},
    "goc_guncel": {"tr": "Veritabanı güncel.", "en": "The database is up to date."},
    "program_surumu": {"tr": "Program sürümü", "en": "Program version"},
    "calisan_surum": {"tr": "Çalışan", "en": "Running"},
    # Kurulum dosyasının derlemesi (v6.204): sürüm, commit, tarih.
    "paket_derleme": {"tr": "Kurulum dosyası", "en": "Installer build"},
    "diskteki_surum": {"tr": "Güncellenen (diskte)", "en": "Updated (on disk)"},
    "surum_yeniden_baslat": {
        "tr": "Program güncellendi ama yeniden başlatılmadı: yeni kod çalışmıyor. "
              "Programı kapatıp açın.",
        "en": "The program was updated but not restarted: the new code is not "
              "running. Close and reopen the program."},
    "goc_uygulandi": {"tr": "Bu açılışta {n} güncelleme uygulandı.",
                      "en": "{n} update(s) applied at this start."},
    # v6.145: geri yükleme de göçleri çalıştırıyor, kart en son çalışmayı
    # gösteriyor.
    "goc_uygulandi_geri_yukleme": {
        "tr": "Son geri yüklemede {n} güncelleme uygulandı.",
        "en": "{n} update(s) applied at the last restore."},
    "goc_hata": {
        "tr": "Bir güncelleme uygulanamadı. Program çalışmaya devam ediyor "
              "ama bazı ekranlar eksik davranabilir; aşağıdaki adı not alıp "
              "bildirin.",
        "en": "An update could not be applied. The program keeps running but "
              "some screens may behave incompletely; note the name below and "
              "report it."},
    "goc_elle": {
        "tr": "Şu güncelleme soru sorduğu için elle çalıştırılmalı:",
        "en": "This update asks a question, so it must be run by hand:"},
    "goc_veritabani_yok": {"tr": "Veritabanı bulunamadı.",
                           "en": "The database was not found."},
    "baglan": {"tr": "Telefona ekle", "en": "Add to a phone"},
    # ---- ilk kurulum (v6.204) ----
    "kisa_kod": {"tr": "Kısa kod", "en": "Short code"},
    "sifre_tekrar": {"tr": "Şifre (tekrar)", "en": "Password (repeat)"},
    "kurulum_baslik": {"tr": "İlk kurulum", "en": "First-time setup"},
    "kurulum_aciklama": {
        "tr": "Bu bilgisayarda henüz programın veritabanı yok. Eski bilgisayardaki verileri alın ya da yeni bir laboratuvar kurun. Veri klasörü:",
        "en": "There is no database on this computer yet. Bring the data from the old computer or set up a new laboratory. Data folder:"},
    "kurulum_tasi_baslik": {"tr": "Eski bilgisayardan taşı", "en": "Move from the old computer"},
    "kurulum_tasi_ipucu": {
        "tr": "Eski bilgisayarda <code>python3 tasi.py disari &lt;usb&gt; sertifika</code> ile hazırlanan USB klasörünü (<code>lab_tasima</code>), eski programın klasörünü ya da yedek klasörünü seçin. Veritabanı, fotoğraf arşivi ve telefonların sertifikası buradan alınır.",
        "en": "Choose the USB folder prepared on the old computer with <code>python3 tasi.py disari &lt;usb&gt; sertifika</code> (<code>lab_tasima</code>), the old program's folder or a backup folder. The database, the photo archive and the phones' certificate are taken from there."},
    "kurulum_klasor": {"tr": "Klasör", "en": "Folder"},
    "kurulum_bak": {"tr": "Klasöre bak", "en": "Look in folder"},
    "kurulum_klasor_yok": {"tr": "Bu klasör bu bilgisayarda bulunamadı.", "en": "This folder was not found on this computer."},
    "kurulum_veritabani_sec": {"tr": "Alınacak veritabanı", "en": "Database to take"},
    "kurulum_veritabani_yok": {"tr": "Bu klasörde programın veritabanı bulunamadı (lab.db ya da yedek dosyası).",
                               "en": "No program database (lab.db or a backup file) in this folder."},
    "kurulum_dosya_sec": {"tr": "Listeden bir veritabanı seçin.", "en": "Choose a database from the list."},
    "kurulum_son_kayit": {"tr": "son kayıt", "en": "last record"},
    "kurulum_arsiv_al": {"tr": "Fotoğraf arşivini de al ({n} dosya)", "en": "Also take the photo archive ({n} files)"},
    "kurulum_sertifika_al": {"tr": "Telefonların sertifikasını da al", "en": "Also take the phones' certificate"},
    "kurulum_sertifika_silinir": {
        "tr": "Android telefonlara sertifika yeniden yüklenmez. USB'deki kopya alındıktan sonra silinir.",
        "en": "Android phones do not need the certificate again. The copy on the USB is deleted afterwards."},
    "kurulum_sertifika_kalir": {
        "tr": "Android telefonlara sertifika yeniden yüklenmez. Eski programın klasöründeki sertifikaya dokunulmaz.",
        "en": "Android phones do not need the certificate again. The certificate in the old program's folder is left as it is."},
    "kurulum_uzun_surebilir": {
        "tr": "Fotoğraf arşivi büyükse birkaç dakika sürebilir; sayfayı kapatmayın.",
        "en": "With a large photo archive this can take a few minutes; do not close the page."},
    "kurulum_veriyi_al": {"tr": "Veriyi al", "en": "Take the data"},
    "kurulum_yeni_baslik": {"tr": "Yeni laboratuvar", "en": "New laboratory"},
    "kurulum_yeni_ipucu": {
        "tr": "Boş bir veritabanı kurulur. Bu hesap yönetici olur; öteki personeli sonra Yönetici → Kullanıcılar'dan eklersiniz.",
        "en": "An empty database is set up. This account becomes the administrator; add the other staff later under Administration → Users."},
    "kurulum_lab_adi": {"tr": "Laboratuvarın adı", "en": "Laboratory name"},
    "kurulum_yeni_kur": {"tr": "Laboratuvarı kur", "en": "Set up the laboratory"},
    "kurulum_tamam_yeni": {"tr": "Laboratuvar kuruldu.", "en": "The laboratory is set up."},
    "kurulum_tamam_tasi": {"tr": "Veriler bu bilgisayara alındı.", "en": "The data is on this computer now."},
    "kurulum_alinan": {"tr": "Alınan", "en": "Taken"},
    "kurulum_arsiv": {"tr": "Fotoğraf arşivi", "en": "Photo archive"},
    "kurulum_arsiv_sonuc": {"tr": "{yeni} dosya kopyalandı, {guncel} zaten vardı", "en": "{yeni} files copied, {guncel} already there"},
    "kurulum_sertifika": {"tr": "Sertifika", "en": "Certificate"},
    "kurulum_sertifika_alindi": {"tr": "Alındı: telefonlara yeniden yüklemek gerekmiyor.", "en": "Taken: phones do not need it again."},
    "kurulum_goc_hatasi": {"tr": "{n} güncelleme uygulanamadı; ayrıntısı Yönetici panelinde.", "en": "{n} updates could not be applied; details on the admin panel."},
    "kurulum_ag_kapali": {
        "tr": "Program şimdilik yalnızca bu bilgisayardan açılıyor. Telefonların bağlanması için girişten sonra Yönetici → Ağ erişimi → İç ağa açık.",
        "en": "For now the program opens only on this computer. For phones to connect: after signing in, Administration → Network access → Open to the local network."},
    "kurulum_girise_git": {"tr": "Giriş ekranına git", "en": "Go to sign-in"},
    "kurulum_uzak_baslik": {"tr": "Program henüz kurulmadı", "en": "The program is not set up yet"},
    "kurulum_uzak_metin": {
        "tr": "Patient Data Center bu bilgisayarda henüz kurulmadı. İlk kurulum yalnızca programın kurulu olduğu bilgisayardan yapılır.",
        "en": "Patient Data Center is not set up yet. The first-time setup can be done only on the computer the program is installed on."},
    "kurulum_suruyor_baslik": {"tr": "Kurulum sürüyor", "en": "Setup in progress"},
    "kurulum_suruyor_metin": {"tr": "Veriler yerleştiriliyor, birazdan hazır. Sayfa kendini yenileyecek.",
                              "en": "The data is being put in place, ready shortly. The page will refresh itself."},
    # ---- ağ erişimi (v6.203) ----
    "ag_erisimi": {"tr": "Ağ erişimi", "en": "Network access"},
    "ag_yerel": {"tr": "Yalnızca bu bilgisayar", "en": "This computer only"},
    "ag_yerel_aciklama": {
        "tr": "Program yalnızca kurulu olduğu bilgisayardan açılır. Telefonlar ve öteki bilgisayarlar bağlanamaz.",
        "en": "The program opens only on the computer it is installed on. Phones and other computers cannot connect."},
    "ag_acik": {"tr": "İç ağa açık", "en": "Open to the local network"},
    "ag_acik_aciklama": {
        "tr": "Aynı ağdaki telefonlar ve bilgisayarlar giriş şifresiyle bağlanabilir.",
        "en": "Phones and computers on the same network can connect with their password."},
    "ag_simdiki": {"tr": "şu an", "en": "current"},
    "ag_uzaktan_uyari": {
        "tr": "Şu an bu bilgisayardan değil, ağ üzerinden bağlısınız. “Yalnızca bu bilgisayar”ı seçerseniz bu cihazdan da giremezsiniz; yeniden açmak için programın kurulu olduğu bilgisayara gitmek gerekir.",
        "en": "You are connected over the network, not from this computer. If you choose “This computer only” you will lose access from this device; to open it again you must use the computer the program is installed on."},
    "ag_uzaktan_onay": {
        "tr": "Bu cihazın bağlantısı kesilecek. Yeniden açmak için programın kurulu olduğu bilgisayara gitmeniz gerekecek. Devam edilsin mi?",
        "en": "This device will be disconnected. To open it again you will need the computer the program is installed on. Continue?"},
    "ag_kaydedildi_yerel": {"tr": "Ağ erişimi kapatıldı: program artık yalnızca bu bilgisayardan açılıyor.",
                            "en": "Network access closed: the program now opens only on this computer."},
    "ag_kaydedildi_acik": {"tr": "Ağ erişimi açıldı: aynı ağdaki telefonlar ve bilgisayarlar bağlanabilir.",
                           "en": "Network access opened: phones and computers on the same network can connect."},
    "ag_yazilamadi": {"tr": "Ayar kaydedilemedi: veri klasörüne yazılamıyor.",
                      "en": "The setting could not be saved: the data folder is not writable."},
    "ag_adresler": {"tr": "Adresler", "en": "Addresses"},
    "ag_bu_bilgisayarda": {"tr": "Bu bilgisayarda", "en": "On this computer"},
    "ag_telefonlarda": {"tr": "Telefonlarda ve öteki bilgisayarlarda (ağ açıkken)",
                        "en": "On phones and other computers (when open)"},
    "ag_telefon_ipucu": {"tr": "Telefona eklemek için karekod:", "en": "QR code for phones:"},
    # Yakalanmamış hata (v6.206): düz "Internal Server Error" yerine.
    "hata_baslik": {"tr": "Beklenmeyen bir hata oluştu", "en": "An unexpected error occurred"},
    "hata_metin": {
        "tr": "Bu ekran açılamadı. Aşağıdaki kutuyu (ya da bu sayfanın ekran "
              "görüntüsünü) programı yazana iletin; ayrıntısı veri klasöründeki "
              "program.log dosyasında.",
        "en": "This screen could not be opened. Send the box below (or a screenshot "
              "of this page) to the developer; details are in program.log in the "
              "data folder."},
    "ag_kapali_baslik": {"tr": "Program yalnızca kurulu olduğu bilgisayarda açık",
                         "en": "The program is open only on its own computer"},
    "ag_kapali_metin": {
        "tr": "Patient Data Center şu anda yalnızca kurulu olduğu bilgisayardan kullanılabiliyor. Telefonların ve öteki bilgisayarların bağlanması için yönetici o bilgisayarda Yönetici → Ağ erişimi ekranından ağı açmalı.",
        "en": "Patient Data Center can currently be used only on the computer it is installed on. For phones and other computers to connect, an administrator must open the network on that computer under Administration → Network access."},
    "ag_kapali_baglan": {
        "tr": "Ağ erişimi kapalı: telefonlar şu anda bağlanamaz. Önce Ağ erişimi ekranından açın.",
        "en": "Network access is closed: phones cannot connect now. Open it first under Network access."},
    "ag_durum_yerel": {"tr": "yalnızca bu bilgisayar", "en": "this computer only"},
    "ag_durum_acik": {"tr": "iç ağa açık", "en": "open to the network"},
    "ekle_baslik": {"tr": "Ana ekrana ekle", "en": "Add to home screen"},
    "ekle_giris": {
        "tr": "Programı telefonunuzun ana ekranına ekleyin — sonra tek "
              "dokunuşla açılır, her seferinde adres yazmanız gerekmez.",
        "en": "Add the program to your phone's home screen — then it opens "
              "with one tap and you never type the address again."},
    "ekle_dugme": {"tr": "Ana ekrana ekle", "en": "Add to home screen"},
    "ekle_eklendi": {"tr": "Eklendi. Ana ekranınıza bakın.",
                     "en": "Added. Look at your home screen."},
    "ekle_programa_git": {"tr": "Giriş ekranına dön",
                          "en": "Back to the login screen"},
    "ekle_masaustu": {
        "tr": "Bu sayfa telefon içindir. Bilgisayarda programı yer imlerine "
              "ekleyebilirsiniz.",
        "en": "This page is for phones. On a computer you can bookmark the "
              "program instead."},
    "baglan_adres": {"tr": "Programın adresi", "en": "The program's address"},
    # ---- HTTPS: telefona kök sertifika (v6.196) ----
    "sertifika_baslik": {"tr": "Güvenlik sertifikası", "en": "Security certificate"},
    "sertifika_kapali": {
        "tr": "Bu bilgisayarda güvenli bağlantı (HTTPS) açık değil. Program "
              "\u201cpython3 baslat.py\u201d ile başlatılınca kendiliğinden açılır.",
        "en": "Secure connection (HTTPS) is not on for this computer. It turns "
              "on by itself when the program is started with \u201cpython3 baslat.py\u201d."},
    "sertifika_giris": {
        "tr": "Telefonun programı uygulama gibi (adres çubuğu olmadan, kendi "
              "penceresinde) açabilmesi için laboratuvar bilgisayarının "
              "sertifikasını <b>bir kez</b> yükleyin. Sertifika yalnızca bu "
              "bilgisayarın bağlantısını tanıtır; telefondaki başka hiçbir şeyi "
              "değiştirmez.",
        "en": "Install the laboratory computer's certificate <b>once</b> so the "
              "phone can open the program like an app (no address bar, its own "
              "window). It only identifies this computer's connection; nothing "
              "else on the phone changes."},
    "sertifika_indir": {"tr": "1. Sertifikayı indir", "en": "1. Download the certificate"},
    "sertifika_tamam": {
        "tr": "Sertifika bu telefonda yüklü ve güvenilir. Aşağıdaki "
              "\u201cGüvenli adresi aç\u201d ile devam edin.",
        "en": "The certificate is installed and trusted on this phone. Continue "
              "with \u201cOpen the secure address\u201d below."},
    "sertifika_android_1": {
        "tr": "Yukarıdaki düğmeye dokunun; dosya (PDC-sertifika.crt) indirilir. "
              "Açmaya çalışmayın.",
        "en": "Tap the button above; the file (PDC-sertifika.crt) downloads. "
              "Don't try to open it."},
    "sertifika_android_2": {
        "tr": "Telefonun Ayarlar'ını açın, en üstteki arama kutusuna "
              "\u201csertifika\u201d yazın.",
        "en": "Open the phone's Settings and type \u201ccertificate\u201d in the "
              "search box at the top."},
    "sertifika_android_3": {
        "tr": "\u201cCA sertifikası\u201d seçeneğine dokunun (uyarı çıkarsa "
              "\u201cYine de yükle\u201d), telefon kilit şifresini girin.",
        "en": "Tap \u201cCA certificate\u201d (if warned, \u201cInstall anyway\u201d) "
              "and enter the phone's lock code."},
    "sertifika_android_4": {
        "tr": "İndirilenler'den PDC-sertifika.crt dosyasını seçin.",
        "en": "Pick PDC-sertifika.crt from Downloads."},
    "sertifika_android_ipucu": {
        "tr": "Arama sonuç vermezse: Ayarlar \u2192 Güvenlik (ya da Güvenlik ve "
              "gizlilik) \u2192 Diğer güvenlik ayarları / Şifreleme ve kimlik "
              "bilgileri \u2192 Sertifika yükle \u2192 CA sertifikası. Yol "
              "telefonun markasına göre biraz değişir.",
        "en": "If search finds nothing: Settings \u2192 Security (or Security and "
              "privacy) \u2192 More security settings / Encryption & credentials "
              "\u2192 Install a certificate \u2192 CA certificate. The path varies "
              "a little by brand."},
    "sertifika_ios_1": {
        "tr": "Yukarıdaki düğmeye dokunun, \u201cİzin Ver\u201d deyin: "
              "\u201cProfil indirildi\u201d yazar.",
        "en": "Tap the button above and choose \u201cAllow\u201d: it says "
              "\u201cProfile Downloaded\u201d."},
    "sertifika_ios_2": {
        "tr": "Ayarlar'ı açın; en üstte \u201cProfil İndirildi\u201d satırına "
              "dokunun, \u201cYükle\u201d deyin (iki kez) ve telefon şifresini girin.",
        "en": "Open Settings, tap \u201cProfile Downloaded\u201d at the top, then "
              "\u201cInstall\u201d (twice) and enter the passcode."},
    "sertifika_ios_3": {
        "tr": "Ayarlar \u2192 Genel \u2192 Hakkında \u2192 en altta Sertifika Güven "
              "Ayarları: \u201cPatient Data Center Yerel Kok\u201d anahtarını açın.",
        "en": "Settings \u2192 General \u2192 About \u2192 at the bottom Certificate "
              "Trust Settings: turn on \u201cPatient Data Center Yerel Kok\u201d."},
    "sertifika_ios_ipucu": {
        "tr": "iPhone programı sertifikasız da uygulama gibi açıyor; bu adım "
              "isteğe bağlı.",
        "en": "The iPhone opens the program like an app without it too; this "
              "step is optional."},
    "sertifika_sonra": {"tr": "2. Uygulamayı ekleyin", "en": "2. Add the app"},
    "sertifika_sonra_1": {
        "tr": "Aşağıdaki \u201cGüvenli adresi aç\u201d düğmesine dokunun ve "
              "giriş yapın.",
        "en": "Tap \u201cOpen the secure address\u201d below and sign in."},
    "sertifika_sonra_2": {
        "tr": "Chrome'da sağ üstteki üç noktaya (\u22ee) dokunun.",
        "en": "In Chrome tap the three dots (\u22ee) at the top right."},
    "sertifika_sonra_3": {
        "tr": "\u201cUygulamayı yükle\u201d ya da \u201cAna ekrana ekle\u201d "
              "seçeneğine dokunun. Eski simge varsa silin.",
        "en": "Tap \u201cInstall app\u201d or \u201cAdd to Home screen\u201d. "
              "Delete the old icon if there is one."},
    "sertifika_guvenli_ac": {"tr": "Güvenli adresi aç", "en": "Open the secure address"},
    "sertifika_parmak_izi": {
        "tr": "Sertifikanın parmak izi (telefonda sertifika ayrıntısında "
              "görünenle aynı olmalı):",
        "en": "Certificate fingerprint (should match the one shown in the "
              "certificate details on the phone):"},
    "baglan_android_sertifika": {
        "tr": "Android'de programı uygulama gibi açmak için önce bu karekodu "
              "okutun: sayfa telefona sertifikayı yükletip güvenli adrese "
              "geçiriyor. Her telefonda bir kez.",
        "en": "To open the program like an app on Android, scan this code "
              "first: the page installs the certificate on the phone and moves "
              "to the secure address. Once per phone."},
    "baglan_guvenli": {"tr": "Güvenli adres:", "en": "Secure address:"},
    "baglan_sertifika_bitis": {"tr": "Sertifika geçerliliği:", "en": "Certificate valid until:"},
    "ekle_android_sertifika": {
        "tr": "Android'de programın uygulama gibi açılması için önce "
              "sertifikayı yükleyin.",
        "en": "On Android, install the certificate first so the program opens "
              "like an app."},
    "baglan_makine": {"tr": "Bu bilgisayarın adı:", "en": "This computer's name:"},
    "baglan_ipucu": {
        "tr": "Telefon <b>kliniğin kablosuz ağına bağlı</b> olmalı; program "
              "dışarıya açık değil. Bu sayfayı yazdırıp laboratuvara asın, "
              "yeni gelen personel karekodu okutup kendi telefonuna eklesin.",
        "en": "The phone must be <b>on the clinic's wireless network</b>; the "
              "program is not open to the outside. Print this page and put it "
              "up in the laboratory so new staff can scan it and add it to "
              "their own phone."},
    "baglan_ios": {"tr": "iPhone / iPad", "en": "iPhone / iPad"},
    "baglan_ios_1": {
        "tr": "Karekodu telefonun kamerasıyla okutun, çıkan bağlantıya dokunun.",
        "en": "Scan the code with the phone's camera and tap the link."},
    "baglan_ios_2": {
        "tr": "Safari'de paylaşma simgesine dokunun (kutudan çıkan ok; yeni "
              "iOS'ta önce alttaki \u2022\u2022\u2022 düğmesine).",
        "en": "In Safari tap the share icon at the bottom (the box with an "
              "arrow)."},
    "baglan_ios_3": {"tr": "\u201cAna Ekrana Ekle\u201d seçeneğine dokunun.",
                     "en": "Tap \u201cAdd to Home Screen\u201d."},
    "baglan_ios_4": {"tr": "Sağ üstteki Ekle'ye dokunun.",
                     "en": "Tap Add at the top right."},
    "baglan_android": {"tr": "Android", "en": "Android"},
    "baglan_android_1": {
        "tr": "Karekodu telefonun kamerasıyla okutun, çıkan bağlantıya dokunun.",
        "en": "Scan the code with the phone's camera and tap the link."},
    "baglan_android_2": {
        "tr": "Chrome'da sağ üstteki üç noktaya dokunun.",
        "en": "In Chrome tap the three dots at the top right."},
    "baglan_android_3": {
        "tr": "\u201cUygulamayı yükle\u201d ya da \u201cAna ekrana ekle\u201d "
              "seçeneğine dokunun.",
        "en": "Tap \u201cInstall app\u201d or \u201cAdd to Home screen\u201d."},
    "listeden_sec": {"tr": "Listeden seç", "en": "Pick from list"},
    "klasor_araniyor": {"tr": "\u201c{ad}\u201d bu bilgisayarda aranıyor…",
                        "en": "Looking for \u201c{ad}\u201d on this computer…"},
    "klasor_bulundu": {"tr": "Klasör bulundu, yol yukarıya yazıldı.",
                       "en": "Folder found, the path is filled in above."},
    "klasor_cok_aday": {
        "tr": "Bu adda birden çok klasör var. Doğru olanı seçin:",
        "en": "There is more than one folder with this name. Pick the right one:"},
    "klasor_bulunamadi": {
        "tr": "\u201c{ad}\u201d bu bilgisayarda bulunamadı. Program yalnızca "
              "kendi çalıştığı bilgisayara bakabiliyor — klasör başka bir "
              "makinedeyse aşağıdaki listeden seçin.",
        "en": "\u201c{ad}\u201d was not found on this computer. The program can "
              "only look at the computer it runs on — if the folder is on "
              "another machine, pick it from the list below."},
    "klasor_bos_secildi": {
        "tr": "Seçilen klasörde dosya yok; program onu bu bilgisayarda "
              "arayamıyor. Aşağıdaki listeden seçin.",
        "en": "The selected folder has no files, so the program cannot find "
              "it on this computer. Pick it from the list below."},
    "klasorleri_kaydet": {"tr": "Klasörleri kaydet", "en": "Save folders"},
    "klasor_kaydedildi": {"tr": "Klasörler kaydedildi.", "en": "Folders saved."},
    "klasor_hata_kamera": {
        "tr": "Kamera klasörü bulunamadı. Yolu olduğu gibi yazın; klasörün "
              "bu bilgisayarda var olması gerekir.",
        "en": "The camera folder was not found. Type the path exactly; the "
              "folder must exist on this computer."},
    "klasor_hata_cryo": {
        "tr": "Cryo haritası klasörü oluşturulamadı. Yolu ve yazma iznini kontrol edin.",
        "en": "The cryo map folder could not be created. Check the path and "
              "the write permission."},
    "klasor_hata_arsiv": {
        "tr": "Arşiv klasörü oluşturulamadı. Yolu ve yazma iznini kontrol edin.",
        "en": "The archive folder could not be created. Check the path and "
              "the write permission."},
    "klasor_arsiv_uyari": {
        "tr": "<b>Arşiv klasörünü taşımadan değiştirmeyin.</b> Veritabanı "
              "görüntüleri bu klasöre göre saklıyor; yol değişirse eski "
              "fotoğraflar yeni klasörde aranır ve bulunamaz. Önce klasörün "
              "içindekileri yeni yere kopyalayın, sonra burayı değiştirin.",
        "en": "<b>Do not change the archive folder without moving it.</b> The "
              "database stores images relative to this folder; if the path "
              "changes, old photos are looked for in the new folder and are "
              "not found. Copy the contents to the new place first, then "
              "change this."},
    "gomulu_formlar": {"tr": "Programla gelen formlar",
                       "en": "Forms that came with the program"},
    "gomulu_form_ipucu": {
        "tr": "Bu formlar programı yazan laboratuvarın kurum belgeleri. "
              "Sizin kurumunuzun formu değilse gizleyin — yanlışlıkla "
              "basılırsa başka bir kurumun belgesinde hastanızın verisi "
              "görünür. Gizlemek silmez, istediğinizde geri açarsınız.",
        "en": "These forms are the institutional documents of the laboratory "
              "that wrote the program. If they are not your institution's "
              "forms, hide them — printed by mistake, your patient's data "
              "would appear on another institution's document. Hiding does "
              "not delete; you can show them again at any time."},
    "form_yuklenenler": {"tr": "Yüklenen formlar", "en": "Uploaded forms"},
    "form_yok": {"tr": "Henüz form yüklenmedi.", "en": "No form uploaded yet."},
    "form_gizle": {"tr": "Gizle", "en": "Hide"},
    "form_goster": {"tr": "Göster", "en": "Show"},
    "form_gizli": {"tr": "Gizli", "en": "Hidden"},
    "form_kaldir": {"tr": "Sil", "en": "Delete"},
    "form_kaldir_onay": {
        "tr": "Bu form kalıbı silinsin mi? Hasta kaydı etkilenmez, "
              "yalnızca kalıp gider; yeniden yükleyebilirsiniz.",
        "en": "Delete this form template? No patient record is affected, "
              "only the template; you can upload it again."},
    "form_eklendi": {"tr": "Form yüklendi.", "en": "Form uploaded."},
    "form_hata_dosya": {"tr": "Yalnızca .xlsx dosyası yüklenebilir. "
                              "Excel'de \"Farklı Kaydet\" ile .xlsx yapın.",
                        "en": "Only .xlsx files can be uploaded. Use "
                              "\"Save As\" in Excel to make one."},
    "form_hata_okuma": {"tr": "Dosya okunamadı. Excel'de açılıp .xlsx olarak "
                              "kaydedilmiş bir dosya olmalı.",
                        "en": "The file could not be read. It must be a file "
                              "saved as .xlsx from Excel."},
    "form_hata_bos": {"tr": "Dosyanın ilk sayfası boş görünüyor.",
                      "en": "The first sheet of the file looks empty."},
    "form_satir": {"tr": "{n} satır", "en": "{n} rows"},
    "form_bilinmeyen": {
        "tr": "Tanınmayan etiket (formda olduğu gibi basılıyor):",
        "en": "Unknown label (printed as it is on the form):"},
    "yazdir": {"tr": "Yazdır", "en": "Print"},
    "excel_indir": {"tr": "Excel olarak indir", "en": "Download as Excel"},
    "zaman_cizelgesi": {"tr": "Zaman çizelgesi", "en": "Timeline"},
    "onceki_islemden": {"tr": "Önceki işlemden", "en": "Since previous step"},
    "opudan_bu_yana": {"tr": "OPU'dan bu yana", "en": "Since OPU"},
    "n_saat": {"tr": "{n} sa", "en": "{n} h"},
    "cizelge_bos": {"tr": "Henüz saati girilmiş bir işlem yok.",
                    "en": "No step with a recorded time yet."},
    "cizelge_ipucu": {
        "tr": "Saatler aşama ekranlarında girdiğin değerlerden hesaplanıyor; "
              "ayrı bir kayıt tutulmuyor.",
        "en": "Hours are computed from the times you enter on the stage "
              "screens; nothing is stored separately."},
    "excel_ay": {"tr": "Bu ayı Excel'e aktar", "en": "Export this month to Excel"},
    "excel_cycle": {"tr": "Bu tedaviyi Excel'e aktar",
                    "en": "Export this cycle to Excel"},
    "excel_cryo": {"tr": "Tankları Excel'e aktar",
                   "en": "Export the tanks to Excel"},
    # ---- Cryo Haritası'nın Excel'i (v6.191) ----
    "excel_harita": {"tr": "Excel haritası", "en": "Excel map"},
    "excel_harita_ipucu": {
        "tr": "Harita her değiştiğinde program Excel'ini kendiliğinden yeniden "
              "yazar: her tank ayrı sayfa, kanisterler yan yana, her goblet "
              "kapasitesi kadar satır; ayrıca tek bir liste. Her günün son hali "
              "30 gün saklanır.",
        "en": "Whenever the map changes the program rewrites its Excel file: one "
              "sheet per tank, canisters side by side, one row per goblet slot; "
              "plus a single list. Each day's last version is kept for 30 days."},
    "excel_harita_guncel": {"tr": "Son güncelleme: {zaman}",
                            "en": "Last updated: {zaman}"},
    "excel_harita_henuz": {
        "tr": "Henüz yazılmadı; program açıldıktan birkaç saniye sonra yazılır.",
        "en": "Not written yet; it is written a few seconds after the program starts."},
    "excel_harita_yazilamadi": {
        "tr": "Dosya yazılamadı — başka bir programda (Excel) açık olabilir. "
              "Kapatınca program kendiliğinden yeniden dener.",
        "en": "The file could not be written — it may be open in another program "
              "(Excel). The program retries by itself once it is closed."},
    "excel_harita_kurulamadi": {
        "tr": "Excel haritası kurulamadı; ayrıntı program.log'da.",
        "en": "The Excel map could not be built; see program.log."},
    "excel_harita_klasor": {"tr": "Klasör", "en": "Folder"},
    # ---- Laboratuvarın kendi Cryo Haritası Excel'i (v6.199) ----
    "sablon_ipucu": {
        "tr": "Excel çıktıları laboratuvarın kendi Cryo Haritası Excel'inin "
              "biçiminde ({dosya}, {zaman} yüklendi): sayfalar, tablolar ve "
              "yazılar aynen. Straw hâlâ o gobletteyse satırı olduğu gibi kalır; "
              "çözülen, taşınan ya da başka yere konan straw'ın satırı boşalır; "
              "programda dondurulan straw gobletin boş satırına yazılır. Harita "
              "her değiştiğinde dosya veri klasörüne de yazılır, her günün son "
              "hali 30 gün saklanır. Dosyada elle yapılan değişiklik programa girmez.",
        "en": "Excel output uses the lab's own Cryo Map workbook ({dosya}, "
              "uploaded {zaman}): same sheets, tables and wording. A straw still "
              "in its goblet keeps its row as written; the row of a thawed, "
              "transferred or moved straw is emptied; a straw frozen in the "
              "program is written into a free row of its goblet. The file is also "
              "rewritten in the data folder whenever the map changes; each day's "
              "last version is kept for 30 days. Edits made in the file are not "
              "read back."},
    "sablon_ozet": {
        "tr": "Son yazımda {korunan} satır aynen kaldı, {bosalan} satır boşaldı, "
              "{yeni} straw boş satıra yazıldı.",
        "en": "Last write: {korunan} rows unchanged, {bosalan} rows emptied, "
              "{yeni} straws written into free rows."},
    "sablon_bilinmeyen": {
        "tr": "{n} dolu satırın programda hiçbir karşılığı yok (dosya tank düzeni "
              "kurulduktan sonra Excel'de değiştirilmiş olabilir); olduğu gibi "
              "bırakıldı. Programa almak için: python3 cryo_esle.py yerlesim <dosya>",
        "en": "{n} filled rows have no record in the program (the workbook may have "
              "been edited after the tank layout was built); they were left as they "
              "are. To bring them in: python3 cryo_esle.py yerlesim <file>"},
    "sablon_sigmayan": {
        "tr": "{n} straw yazılamadı: gobleti dolu ya da gobleti dosyada yok.",
        "en": "{n} straws could not be written: the goblet is full or not in the file."},
    "sablon_doldurulamadi": {
        "tr": "Laboratuvarın dosyası doldurulamadı, programın düzeni yazıldı; "
              "ayrıntı program.log'da.",
        "en": "The lab's workbook could not be filled; the program's layout was "
              "written instead (see program.log)."},
    "sablon_yuklendi": {
        "tr": "{dosya} yüklendi. Excel çıktıları bundan sonra bu dosyanın biçiminde.",
        "en": "{dosya} uploaded. Excel output now uses this workbook."},
    "sablon_islenemedi": {
        "tr": "Dosya işlenemedi; ayrıntı program.log'da.",
        "en": "The file could not be processed; see program.log."},
    "sablon_yok_ipucu": {
        "tr": "Çıktıyı laboratuvarın kendi Cryo Haritası Excel'inin biçiminde "
              "almak için dosyayı bir kez aşağıdan yükleyin.",
        "en": "Upload the lab's own Cryo Map workbook once below to get the "
              "output in its format."},
    "sablon_yukle_etiket": {"tr": "Laboratuvarın Cryo Haritası Excel'i",
                            "en": "The lab's Cryo Map workbook"},
    "sablon_yukle_ipucu": {
        "tr": "Tank düzeni kurulurken kullanılan dosya (.xlsx). Yenisi yüklenirse "
              "öncekinin yerine geçer.",
        "en": "The workbook the tank layout was built from (.xlsx). A new upload "
              "replaces the previous one."},
    "sablon_yukle": {"tr": "Dosyayı yükle", "en": "Upload the file"},
    "excel_harita_indir": {"tr": "Excel haritasını indir",
                           "en": "Download the Excel map"},
    "excel_tumu": {"tr": "Tüm veriyi Excel'e aktar",
                   "en": "Export all data to Excel"},
    "excel_tumu_ipucu": {
        "tr": "Bütün hastalar, tedaviler, örnekler ve olaylar; her tablo ayrı "
              "sayfada. Dosya bütün hasta adlarını içerir — kime verildiğine "
              "dikkat et. Şifreler ve oturum anahtarları dosyaya girmez. "
              "Program aynı dosyayı her gün 14:00'te Cryo haritası klasörüne "
              "de yazar (Klasörler ekranı; son 30 gün).",
        "en": "All patients, cycles, samples and events; one sheet per table. "
              "The file contains every patient name — mind who receives it. "
              "Passwords and session tokens are not included. The program "
              "also writes the same file to the Cryo map folder every day at "
              "14:00 (Folders screen; last 30 days)."},
    "aktif_hastalara_don": {"tr": "Aktif hastalara dön",
                            "en": "Back to active patients"},
    "yeni_hasta": {"tr": "Yeni hasta", "en": "New patient"},
    # v6.84'te "Embriyo Dondurma" oldu, v6.85'te kullanıcının isteğiyle
    # tekrar "Cryo Haritası" oldu -- Embriyo Dondurma ve Sperm Dondurma artık
    # aynı ekranda yan yana iki modül, ekranın kendisi ikisinin ortak
    # başlığı. Modül başlıkları ayrı anahtarlarda: "embriyo_dondurma",
    # "sperm_dondurma".
    "cryo_haritasi": {"tr": "Cryo Haritası", "en": "Cryo Map"},
    "embriyo_dondurma": {"tr": "Embriyo Dondurma", "en": "Embryo Freezing"},
    "yonetim": {"tr": "Yönetici", "en": "Administrator"},
    "arsiv": {"tr": "Arşiv", "en": "Archive"},
    "arsivde": {"tr": "arşivde", "en": "archived"},
    "arama_sonucu": {"tr": "Arama sonucu", "en": "Search results"},
    "tum_hastalar": {"tr": "Tüm hastalar", "en": "All patients"},
    "son_kayitlar": {"tr": "Son kayıtlar", "en": "Recent records"},
    "son_kayit_gun": {"tr": "Son {gun} gün", "en": "Last {gun} days"},
    "son_kayit_sinir": {"tr": "en yeni {n} kayıt",
                        "en": "{n} most recent records"},
    "son_kayit_bos": {"tr": "Son {gun} günde kayıt yok.",
                      "en": "No records in the last {gun} days."},
    "es": {"tr": "Eş", "en": "Partner"},
    "n_cycle": {"tr": "{n} tedavi", "en": "{n} cycles"},
    "n_cycle_tekil": {"tr": "{n} tedavi", "en": "{n} cycle"},
    "n_cycle_sirali": {"tr": "{n}. tedavi", "en": "Cycle {n}"},
    "n_yas": {"tr": "{n} yaşında", "en": "age {n}"},
    "aramaya_uyan_yok": {"tr": "Bu aramaya uyan kayıt yok.",
                         "en": "No records match this search."},
    "henuz_hasta_yok": {"tr": "Henüz hasta kaydı yok.",
                        "en": "No patients recorded yet."},

    # ---- hasta detay ----
    "duzenle": {"tr": "Düzenle", "en": "Edit"},
    "dogum_tarihi_kisa": {"tr": "D.T.", "en": "DOB"},
    "yeni_cycle_ac": {"tr": "Yeni tedavi aç", "en": "Open new cycle"},
    "oosit_kucuk": {"tr": "yumurta", "en": "oocytes"},
    "bu_hastada_cycle_yok": {"tr": "Bu hastada henüz tedavi yok.",
                             "en": "No cycles for this patient yet."},
    "not": {"tr": "Not", "en": "Note"},
    "degisiklik_gecmisi": {"tr": "Değişiklik geçmişi", "en": "Change history"},
    "arsivden_cikar": {"tr": "Arşivden çıkar", "en": "Remove from archive"},
    "kalici_olarak_sil": {"tr": "Kalıcı olarak sil", "en": "Delete permanently"},
    "arsivle_veya_sil": {"tr": "Arşivle veya sil", "en": "Archive or delete"},

    # ---- dil ----
    "dil": {"tr": "Dil", "en": "Language"},
    "dil_secimi": {"tr": "Dil seçimi", "en": "Language"},
    "dili_degistir": {"tr": "Dili değiştir", "en": "Change language"},
    "dil_lab_geneli": {
        "tr": "Dil <b>laboratuvar geneli</b>dir. Değiştirdiğinde giriş ekranı "
              "dahil bütün program o dile geçer — herkes aynı dili görür.",
        "en": "The language is <b>lab-wide</b>. Changing it switches the whole "
              "program, sign-in screen included — everyone sees the same "
              "language."},
    "dil_klinik_terim": {
        "tr": "Klinik terimler iki dilde de İngilizce kalır (blastocyst, ICSI, "
              "PN, ICM, TE, FET). Açılır menülerdeki seçenekler laboratuvarın "
              "kendi listelerinden gelir; onları "
              "<code>python3 liste_duzenle.py</code> ile düzenlersin.",
        "en": "Clinical terms stay in English in both languages (blastocyst, "
              "ICSI, PN, ICM, TE, FET). Drop-down options come from the "
              "laboratory's own lists; edit them with "
              "<code>python3 liste_duzenle.py</code>."},
    "dil_degisti": {"tr": "Dil değiştirildi.", "en": "Language changed."},

    # ---- şifre değişikliğinde yönetici onayı (v6.61) ----
    "sifre_onay_bekliyor": {
        "tr": "Şifre isteğin <b>yöneticiye gönderildi</b>. Yönetici onaylayana "
              "kadar eski şifren geçerli — onaylandığında oturumların kapanır "
              "ve yeni şifreyle girersin.",
        "en": "Your password request was <b>sent to an administrator</b>. Your "
              "old password stays valid until it is approved; once approved you "
              "are signed out everywhere and sign in with the new one."},
    "sifre_onay_gerekir": {
        "tr": "Şifre değişikliği <b>yönetici onayı</b> ister. İsteğini "
              "gönderdikten sonra eski şifren onaya kadar geçerli kalır.",
        "en": "A password change needs <b>administrator approval</b>. After you "
              "send the request your old password stays valid until it is "
              "approved."},
    "sifre_istekleri": {"tr": "Şifre istekleri", "en": "Password requests"},
    "sifre_istegi_yok": {"tr": "Onay bekleyen istek yok.",
                         "en": "No requests waiting for approval."},
    "bekleyen_sifre_istegi": {"tr": "{n} şifre isteği onay bekliyor.",
                              "en": "{n} password request(s) waiting."},
    "onayla": {"tr": "Onayla", "en": "Approve"},
    "reddet": {"tr": "Reddet", "en": "Reject"},
    "sifre_istegi_aciklama": {
        "tr": "Onaylarsan şifre <b>o anda</b> değişir ve kullanıcının açık "
              "oturumları kapanır. Reddedersen eski şifresi kalır. Yeni şifreyi "
              "burada göremezsin — program şifreleri düz metin tutmaz; "
              "kullanıcının kendi yazdığı şifre geçerli olur.",
        "en": "Approving changes the password <b>at once</b> and signs that "
              "user out everywhere. Rejecting keeps the old one. You cannot see "
              "the new password here — the program never stores passwords in "
              "plain text; what the user typed becomes their password."},
    "istek_zamani": {"tr": "İstek zamanı", "en": "Requested"},
    "sifre_onaylandi": {"tr": "{kim} kullanıcısının şifresi değiştirildi.",
                        "en": "Password changed for {kim}."},
    "sifre_reddedildi": {"tr": "{kim} kullanıcısının isteği reddedildi.",
                         "en": "Request from {kim} rejected."},
}
