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
    "es_adi": {"tr": "Eş adı", "en": "Partner name"},
    "es_dogum_tarihi": {"tr": "Eş doğum tarihi", "en": "Partner date of birth"},
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
    "cryo_ara_ipucu": {"tr": "Etiket, konum, dosya no veya hasta adı",
                       "en": "Label, location, file no or patient name"},
    "tanklar": {"tr": "Tanklar", "en": "Tanks"},
    "n_tasiyici": {"tr": "{n} taşıyıcı", "en": "{n} carriers"},
    "n_tasiyici_tekil": {"tr": "{n} taşıyıcı", "en": "{n} carrier"},
    "n_embriyo": {"tr": "{n} embriyo", "en": "{n} embryos"},
    "n_embriyo_tekil": {"tr": "{n} embriyo", "en": "{n} embryo"},
    "dolu_tasiyicilar": {"tr": "Dolu taşıyıcılar", "en": "Occupied carriers"},
    "konum_girilmemis": {"tr": "konum girilmemiş", "en": "location not entered"},
    "aramaya_uyan_tasiyici_yok": {"tr": "Bu aramaya uyan taşıyıcı yok.",
                                  "en": "No carriers match this search."},
    "henuz_dondurulmus_yok": {"tr": "Henüz dondurulmuş embriyo yok.",
                              "en": "No frozen embryos yet."},

    # ---- cycle formu ----
    "cycle_duzenle": {"tr": "Cycle düzenle", "en": "Edit cycle"},
    "yeni_cycle": {"tr": "Yeni cycle", "en": "New cycle"},
    "cycle_i_kaydet": {"tr": "Cycle'ı kaydet", "en": "Save cycle"},
    "lab_kayit_no": {"tr": "Lab kayıt no", "en": "Lab record no"},
    "kacinci_cycle": {"tr": "Kaçıncı cycle", "en": "Patient's cycle no"},
    "cycle_no_ipucu": {
        "tr": "Lab kayıt no otomatik atandı; gerekirse değiştirebilirsin. "
              "Kaçıncı cycle hastanın denemesidir — başka merkezdeki "
              "tedavileri de sayıyorsan elle değiştir.",
        "en": "The lab record no was assigned automatically; change it if you "
              "need to. The patient's cycle no counts this patient's attempts "
              "— edit it by hand if you also count treatments at another "
              "centre."},
    "tedavi_tipi": {"tr": "Tedavi tipi", "en": "Treatment type"},
    "fet_ipucu": {
        "tr": "FET seçilirse laboratuvar aşamaları gösterilmez; doğrudan "
              "çözme ve transferle başlanır.",
        "en": "If FET is selected the laboratory stages are hidden; the cycle "
              "starts directly with thaw and transfer."},
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
    "opu_oosit_sayilari": {"tr": "OPU'da toplanan oosit sayıları",
                           "en": "Oocytes collected at OPU"},
    "sag_overden": {"tr": "Sağ overden toplanan",
                    "en": "Collected from right ovary"},
    "sol_overden": {"tr": "Sol overden toplanan",
                    "en": "Collected from left ovary"},
    "sag_overden_oosit": {"tr": "Sağ overden toplanan oosit",
                          "en": "Oocytes collected from right ovary"},
    "sol_overden_oosit": {"tr": "Sol overden toplanan oosit",
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
    "oosit_ad": {"tr": "Oosit", "en": "Oocyte"},
    "zigot_ad": {"tr": "Zigot", "en": "Zygote"},
    "cleavage_ad": {"tr": "Cleavage", "en": "Cleavage"},
    "blastokist_ad": {"tr": "Blastokist", "en": "Blastocyst"},
    "embriyo_ad": {"tr": "Embriyo", "en": "Embryo"},

    # ---- büyüteç / kare şeridi (paylaşılan parçalar) ----
    "kapat": {"tr": "Kapat", "en": "Close"},
    "onceki_kare": {"tr": "Önceki kare", "en": "Previous frame"},
    "sonraki_kare": {"tr": "Sonraki kare", "en": "Next frame"},
    "yakinlastir": {"tr": "Yakınlaştır", "en": "Zoom in"},
    "sigdir": {"tr": "Sığdır", "en": "Fit"},
    "kare_n": {"tr": "Kare {n}", "en": "Frame {n}"},
    "bu_kareyi_sil": {"tr": "Bu kareyi sil", "en": "Delete this frame"},
    "bekleyen_kare": {"tr": "Bekleyen kare", "en": "Waiting frame"},
    "buyut": {"tr": "büyüt", "en": "enlarge"},

    # ---- vitrifikasyon ----
    "dondurulmus": {"tr": "Dondurulmuş", "en": "Frozen"},
    "coz": {"tr": "çöz", "en": "thaw"},
    "kaydi_geri_al": {"tr": "kaydı geri al", "en": "undo record"},
    "dondurulacak_kalmadi": {"tr": "Dondurulacak embriyo kalmadı.",
                             "en": "No embryos left to freeze."},
    "dondurulacak_embriyolar": {"tr": "Dondurulacak embriyolar",
                                "en": "Embryos to freeze"},
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
    "cozme_ekrani": {"tr": "Çözme ekranı", "en": "Thaw screen"},

    # ---- transfer ----
    "bu_cyclede_transfer": {"tr": "Bu cycle'da transfer edilenler",
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
        "tr": "Hastanın tüm cycle'larından uygun embriyolar listelenir. "
              "Çözülmüş embriyolar \"donmuş transfer\", diğerleri \"taze\" "
              "olarak kaydedilir.",
        "en": "Eligible embryos from all of this patient's cycles are listed. "
              "Thawed embryos are recorded as \"frozen transfer\", the rest "
              "as \"fresh\"."},
    "transfer_saati": {"tr": "Transfer saati", "en": "Transfer time"},
    "transferi_kaydet": {"tr": "Transferi kaydet", "en": "Save transfer"},
    "cycle_kartina_don": {"tr": "Cycle kartına dön", "en": "Back to cycle card"},

    # ---- taşıyıcı ----
    "girilmemis": {"tr": "girilmemiş", "en": "not entered"},
    "icerik": {"tr": "İçerik", "en": "Contents"},
    "canli": {"tr": "Canlı", "en": "Surviving"},
    "sagkalim": {"tr": "Sağkalım", "en": "Survival"},
    "ort_canlilik": {"tr": "Ort. canlılık", "en": "Avg. viability"},
    "tasiyicida_n_embriyo": {
        "tr": "Bu taşıyıcıda {n} embriyo var. Çözüldüğünde hepsi etkilenir.",
        "en": "This carrier holds {n} embryos. Thawing affects all of them."},
    "icindeki_embriyolar": {"tr": "İçindeki embriyolar",
                            "en": "Embryos on this carrier"},
    "cyclei_ac": {"tr": "cycle'ı aç", "en": "open cycle"},
    "tasiyici_bosaltilmis": {"tr": "Bu taşıyıcı boşaltılmış.",
                             "en": "This carrier has been emptied."},
    "bu_tasiyiciyi_coz": {"tr": "Bu taşıyıcıyı çöz", "en": "Thaw this carrier"},
    "tasiyici_bosaltildi": {"tr": "boşaltıldı", "en": "emptied"},

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
        "tr": "Çözme bu cycle'ın kaydına yazılır. Embriyo canlı çıkmasa da o "
              "tedavide çözüldüğü görünür.",
        "en": "The thaw is recorded against this cycle. Even if the embryo "
              "does not survive, it still shows as thawed for that treatment."},
    "cozme_saati": {"tr": "Çözme saati", "en": "Thaw time"},
    "ikinci_kontrol_saati": {"tr": "İkinci kontrol saati",
                             "en": "Second check time"},
    "ikinci_kontrol_ipucu": {
        "tr": "Re-expansion değerlendirmesinin yapıldığı saat. Henüz "
              "yapılmadıysa boş bırak, sonra doldur.",
        "en": "The time the re-expansion assessment was made. Leave it empty "
              "if it has not been done yet and fill it in later."},
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
    "donduruldugu_cycle": {"tr": "dondurulduğu cycle", "en": "frozen in cycle"},
    "icerigi_gor": {"tr": "içeriği gör", "en": "view contents"},
    "coz_dugme": {"tr": "Çöz", "en": "Thaw"},
    "fet_tasiyici_yok": {"tr": "Bu hastanın tankta duran taşıyıcısı yok.",
                         "en": "This patient has no carriers in the tank."},
    "cycle_tasiyici_yok": {"tr": "Bu cycle'a ait tankta duran taşıyıcı yok.",
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
        "tr": "Bu cycle'da henüz oosit yok.",
        "en": "There are no oocytes in this cycle yet."},
    "once_denudasyon": {"tr": "Önce denüdasyon ekranından oositleri oluştur.",
                        "en": "Create the oocytes from the denudation screen first."},
    "denudasyon_ekrani": {"tr": "Denüdasyon ekranı", "en": "Denudation screen"},
    "n_m_kaydedildi": {"tr": "{n} / {m} kaydedildi", "en": "{n} / {m} recorded"},
    "bu_fotografi_sil_uzun": {"tr": "Bu fotoğrafı sil", "en": "Delete this photo"},
    "bu_asamada_fotograf_yok": {"tr": "Bu aşamaya ait fotoğraf yok.",
                                "en": "No photo for this stage."},
    "maturasyon": {"tr": "Maturasyon", "en": "Maturation"},
    "oosit_bulgulari": {"tr": "Oosit bulguları", "en": "Oocyte findings"},
    "bulgu_yok": {"tr": "Bulgu yok", "en": "No findings"},
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
    "kaydet_sonraki_oosit": {"tr": "Kaydet ve sonraki oosit",
                             "en": "Save and next oocyte"},
    "zaman_operator_otomatik": {
        "tr": "Zaman ve operatör otomatik kaydedilir.",
        "en": "Time and operator are recorded automatically."},
    "oosit_n_fotograf_ekle": {"tr": "Oosit {n} için fotoğraf ekle",
                              "en": "Add a photo for oocyte {n}"},
    "secimleri_geri_al": {"tr": "Seçimleri geri al", "en": "Reset selections"},
    "bu_oositin_kaydini_sil": {"tr": "Bu oositin kaydını sil",
                               "en": "Delete this oocyte's record"},

    # ---- snapshot / eşleştirme ----
    "n_kare_bekliyor": {"tr": "Kamera klasöründe {n} kare bekliyor",
                        "en": "{n} frames waiting in the camera folder"},
    "n_kare_bekliyor_tekil": {"tr": "Kamera klasöründe {n} kare bekliyor",
                              "en": "{n} frame waiting in the camera folder"},
    "kareyi_oosite_ekle": {"tr": "Bu kareyi oosit {n}'e ekle",
                           "en": "Add this frame to oocyte {n}"},
    "n_karenin_hepsini_ekle": {"tr": "{n} karenin hepsini ekle",
                               "en": "Add all {n} frames"},
    "oositlere_dagit": {"tr": "oositlere tek tek dağıt ({n} kare)",
                        "en": "distribute to oocytes one by one ({n} frames)"},
    "oositlere_dagit_tekil": {"tr": "oositlere tek tek dağıt ({n} kare)",
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
    "icsi_kaydi_yok": {"tr": "Bu oosite ICSI kaydı yok",
                       "en": "There is no ICSI record for this oocyte"},
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
    "gun_n_degerlendirme": {"tr": "Gün {n} değerlendirme", "en": "Day {n} assessment"},
    "gun_n_buyuk": {"tr": "Gün {n}", "en": "Day {n}"},
    "fert_kontrolunde_npn": {
        "tr": "Bu oosit fertilizasyon kontrolünde {n}PN idi.",
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
    "gun_n_kaydini_sil": {"tr": "Bu oositin gün {n} kaydını sil",
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
    "henuz_oosit_yok_kisa": {"tr": "Bu cycle'da henüz oosit yok.",
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
    "bu_cyclede_transfer_edilen": {"tr": "Bu cycle'da transfer edilen",
                                   "en": "Transferred in this cycle"},
    "transfer_kaydi_yok_uyari": {
        "tr": "Bu cycle'da transfer kaydı yok. Sonuç yine de girilebilir, ama "
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
    "sonucu_kaydet": {"tr": "Sonucu kaydet", "en": "Save outcome"},
    "son_guncelleme": {"tr": "Son güncelleme:", "en": "Last updated:"},

    # ---- fotoğraf ekleme / görüntü silme ----
    "hangi_oosite": {"tr": "Hangi oosite", "en": "To which oocyte"},
    "her_dosya_ayri_oosit": {"tr": "Her dosya ayrı oosit olsun (yeni numaralar)",
                             "en": "Each file its own oocyte (new numbers)"},
    "oosite_baglama": {"tr": "Oosite bağlama — cycle arşivine koy",
                       "en": "Do not link to an oocyte — put in the cycle archive"},
    "asama": {"tr": "Aşama", "en": "Stage"},
    "dosyalar": {"tr": "Dosyalar", "en": "Files"},
    "foto_ekle_ipucu": {
        "tr": "Birden fazla seçebilirsin. \"Her dosya ayrı oosit\" seçiliyse her "
              "dosya kendi oosit numarasını alır; belirli bir oosit seçiliyse "
              "hepsi ona eklenir. En fazla 25 MB, jpg/png/tif/bmp/webp.",
        "en": "You can select more than one. With \"each file its own oocyte\" "
              "every file gets its own oocyte number; if a specific oocyte is "
              "selected they are all added to it. Max 25 MB, "
              "jpg/png/tif/bmp/webp."},
    "yukle": {"tr": "Yükle", "en": "Upload"},
    "goruntuyu_sil": {"tr": "Görüntüyü sil", "en": "Delete image"},
    "goruntu_kalici_silinecek": {
        "tr": "<strong>Bu görüntü kalıcı olarak silinecek.</strong><br>Oosit "
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
    "ornege_bagli_degil": {"tr": "örneğe bağlı değil (cycle arşivi)",
                           "en": "not linked to a sample (cycle archive)"},
    "kaynak_alan": {"tr": "Kaynak", "en": "Source"},
    "mikroskop_kamerasi": {"tr": "Mikroskop kamerası", "en": "Microscope camera"},
    "elle_yuklendi": {"tr": "Elle yüklendi", "en": "Uploaded manually"},
    "zaman": {"tr": "Zaman", "en": "Time"},

    # ---- silme ekranları (ortak) ----
    "geri_don": {"tr": "Geri dön", "en": "Go back"},
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
    "oositi_sil": {"tr": "Oositi sil", "en": "Delete oocyte"},
    "ornek_n": {"tr": "Örnek {n}", "en": "Sample {n}"},
    "oosit_silinemez": {"tr": "<strong>Bu oosit silinemez.</strong>",
                        "en": "<strong>This oocyte cannot be deleted.</strong>"},
    "oosit_silinemez_sebep": {
        "tr": "{n} işlem kaydı bağlı (maturasyon, ICSI, fertilizasyon gibi). "
              "Klinik işlem kaydı olan bir oosit silinmez. Önce ilgili işlem "
              "kayıtları iptal edilmeli.",
        "en": "{n} procedure records are linked (maturation, ICSI, "
              "fertilization and the like). An oocyte with clinical procedure "
              "records is not deleted. Cancel those records first."},
    "oosit_kalici_silinecek": {
        "tr": "<strong>Bu oosit kalıcı olarak silinecek.</strong>",
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
        "tr": "Numara boşluğu oluşabilir: 1, 2, 4 gibi. Verilen oosit "
              "kimlikleri kalıcıdır, geriye dönük numaralandırma yapılmaz.",
        "en": "A gap in the numbering may appear: 1, 2, 4 and so on. Oocyte "
              "identifiers once assigned are permanent; they are never "
              "renumbered."},

    # ---- ICSI kaydı silme ----
    "icsi_kaydini_sil": {"tr": "ICSI kaydını sil", "en": "Delete ICSI record"},
    "icsi_kaydi_bulunamadi": {
        "tr": "Bu oosite ait kaydedilmiş bir ICSI kaydı yok.",
        "en": "There is no saved ICSI record for this oocyte."},
    "kaydete_basilmamis": {
        "tr": "Ekranda seçim yaptıysan Kaydet'e basılmamış demektir;",
        "en": "If you made selections on the screen, Save was not pressed;"},
    "secimleri_geri_al_ipucu": {
        "tr": "geri dönüp \"Seçimleri geri al\" ile temizleyebilirsin.",
        "en": "go back and clear them with \"Reset selections\"."},
    "icsi_kaydi_temizlenecek": {
        "tr": "<strong>Bu oositin ICSI kaydı temizlenecek.</strong>",
        "en": "<strong>The ICSI record for this oocyte will be cleared.</strong>"},
    "oosit_fotograf_durur": {
        "tr": "Oosit ve fotoğrafları durur, yalnızca aşağıdaki değerlendirme "
              "silinir. Oositi yeniden değerlendirebilirsin.",
        "en": "The oocyte and its photos remain; only the assessment below is "
              "deleted. You can assess the oocyte again."},

    # ---- aşama kaydı silme ekranları ----
    "fert_kaydini_sil": {"tr": "Fertilizasyon kaydını sil",
                         "en": "Delete fertilization record"},
    "fert_kaydi_bulunamadi": {
        "tr": "Bu oosite ait kaydedilmiş fertilizasyon kaydı yok.",
        "en": "There is no saved fertilization record for this oocyte."},
    "kaydete_basilmamis_kisa": {
        "tr": "Ekranda seçim yaptıysan Kaydet'e basılmamış demektir.",
        "en": "If you made selections on the screen, Save was not pressed."},
    "fert_kaydi_temizlenecek": {
        "tr": "<strong>Bu oositin fertilizasyon kaydı temizlenecek.</strong>",
        "en": "<strong>The fertilization record for this oocyte will be "
              "cleared.</strong>"},
    "fert_sil_aciklama": {
        "tr": "Oosit, fotoğrafları ve ICSI kaydı durur. Yalnızca aşağıdaki "
              "değerlendirme silinir.",
        "en": "The oocyte, its photos and the ICSI record remain. Only the "
              "assessment below is deleted."},
    "pn_sayisi": {"tr": "PN sayısı", "en": "PN count"},
    "pn_skoru": {"tr": "PN skoru", "en": "PN score"},
    "gun_n_kaydini_sil_baslik": {"tr": "Gün {n} kaydını sil",
                                 "en": "Delete day {n} record"},
    "gun_n_kaydi_bulunamadi": {"tr": "Bu oosite ait kaydedilmiş gün {n} kaydı yok.",
                               "en": "There is no saved day {n} record for this "
                                     "oocyte."},
    "gun_n_degerlendirme_temizlenecek": {
        "tr": "<strong>Gün {n} değerlendirmesi temizlenecek.</strong>",
        "en": "<strong>The day {n} assessment will be cleared.</strong>"},
    "diger_asamalar_durur": {
        "tr": "Oosit, fotoğrafları ve diğer aşamaların kayıtları durur.",
        "en": "The oocyte, its photos and the records of the other stages "
              "remain."},
    "blast_kaydini_sil": {"tr": "Blastokist kaydını sil",
                          "en": "Delete blastocyst record"},
    "blast_kaydi_bulunamadi": {
        "tr": "Bu oosite ait gün {n} blastokist kaydı yok.",
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
        "tr": "İlk oosit kaydedildiğinde otomatik dolar. Gerekirse düzelt.",
        "en": "Filled in automatically when the first oocyte is recorded. "
              "Correct it if needed."},
    "toplandigi_over": {"tr": "Toplandığı over", "en": "Ovary collected from"},
    "belirtme": {"tr": "Belirtme", "en": "Unspecified"},
    "taraf_ipucu": {
        "tr": "Bundan sonra oluşturulan oositlere bu taraf yazılır. Sağ overi "
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
    "oosit_n": {"tr": "Oosit {n}", "en": "Oocyte {n}"},
    "siradaki_goruntu": {"tr": "Sıradaki görüntü", "en": "Next image"},
    "kaydet_oosit_n": {"tr": "Kaydet → oosit {n}", "en": "Save → oocyte {n}"},
    "ayni_oosite_ekle": {"tr": "Aynı oosite ekle", "en": "Add to the same oocyte"},
    "atla": {"tr": "Atla", "en": "Skip"},
    "fotografsiz_oosit": {"tr": "Fotoğrafsız oosit", "en": "Oocyte without photo"},
    "fotografsiz_oosit_ekle": {"tr": "Fotoğrafsız oosit ekle",
                               "en": "Add oocyte without photo"},
    "bekleyen_kalmadi": {"tr": "Bekleyen görüntü kalmadı.",
                         "en": "No images left waiting."},
    "n_oosit_kaydedildi": {"tr": "{n} oosit kaydedildi.",
                           "en": "{n} oocytes recorded."},
    "n_oosit_kaydedildi_tekil": {"tr": "{n} oosit kaydedildi.", "en": "{n} oocyte recorded."},
    "klasorde_yeni_yok": {"tr": "Klasörde yeni görüntü yok.",
                          "en": "No new images in the folder."},
    "kameradan_kare_al": {"tr": "Kameradan kare alıp sayfayı yenile.",
                          "en": "Take a frame from the camera and refresh the page."},
    "yenile": {"tr": "Yenile", "en": "Refresh"},
    "son_kaydi_geri_al": {"tr": "Son kaydı geri al", "en": "Undo last record"},
    "elle_fotograf_ekle": {"tr": "Elle fotoğraf ekle", "en": "Add photo manually"},
    "kaydedilen_oositler": {"tr": "Kaydedilen oositler", "en": "Recorded oocytes"},
    "henuz_oosit_kaydedilmedi": {"tr": "Henüz oosit kaydedilmedi.",
                                 "en": "No oocytes recorded yet."},

    # ---- cycle detay ----
    "toplanan_oosit": {"tr": "Toplanan oosit", "en": "Oocytes collected"},
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
    "oositler": {"tr": "Oositler", "en": "Oocytes"},
    "henuz_oosit_yok": {"tr": "Henüz oosit kaydı yok.",
                        "en": "No oocytes recorded yet."},
    "denudasyondan_ekle": {"tr": "Denüdasyon ekranından ekleyebilirsin.",
                           "en": "You can add them from the denudation screen."},
    "cycle_arsivi": {"tr": "Cycle arşivi", "en": "Cycle archive"},
    "oosite_baglanmamis": {"tr": "Oosite bağlanmamış fotoğraflar.",
                           "en": "Photos not linked to an oocyte."},
    "arsivi_temizle": {"tr": "arşivi temizle", "en": "clear archive"},
    "fotograf_ekle": {"tr": "Fotoğraf ekle", "en": "Add photo"},
    "iptali_geri_al": {"tr": "İptali geri al", "en": "Undo cancellation"},
    "iptal_et_veya_sil": {"tr": "İptal et veya sil", "en": "Cancel or delete"},

    # ---- aşama adları (app.py ASAMA_SIRASI) ----
    # Klinik terimler iki dilde de aynı: OPU, ICSI, Transfer.
    "asama_opu": {"tr": "OPU", "en": "OPU"},
    "asama_androloji": {"tr": "Androloji", "en": "Andrology"},
    "asama_denudasyon": {"tr": "Denüdasyon", "en": "Denudation"},
    "asama_icsi": {"tr": "ICSI", "en": "ICSI"},
    "asama_fert": {"tr": "Fertilizasyon", "en": "Fertilization"},
    "asama_cleavage": {"tr": "Gün 2 / 3", "en": "Day 2 / 3"},
    "asama_blast": {"tr": "Blastokist", "en": "Blastocyst"},
    "asama_vitrifikasyon": {"tr": "Vitrifikasyon", "en": "Vitrification"},
    "asama_thaw": {"tr": "Çözme", "en": "Thaw"},
    "asama_transfer": {"tr": "Transfer", "en": "Transfer"},
    "asama_gebelik": {"tr": "Gebelik sonucu", "en": "Pregnancy outcome"},

    # ---- tedavi tipi (app.py TIP_KISA) ----
    "tip_ivf_icsi": {"tr": "IVF/ICSI", "en": "IVF/ICSI"},
    "tip_fet": {"tr": "FET", "en": "FET"},
    "tip_oosit_cryo": {"tr": "Oosit cryo", "en": "Oocyte cryo"},
    "tip_taze": {"tr": "IVF/ICSI", "en": "IVF/ICSI"},

    # ---- işlemi yapan (paylaşılan parça) ----
    "islem_yapan": {"tr": "İşlemi yapan", "en": "Performed by"},
    "islem_yapan_ipucu": {
        "tr": "Bu aşamayı fiilen yapan kişi. Kaydı giren kişiden farklı olabilir.",
        "en": "The person who actually did this step. May differ from the "
              "person entering the record."},
    "ad_soyad": {"tr": "Ad soyad", "en": "Full name"},
    "opu_embriyologu": {"tr": "OPU Embriyoloğu", "en": "OPU Embryologist"},
    "opu_hekimi": {"tr": "OPU Hekimi", "en": "OPU Physician"},

    # ---- örnek ızgarası ve bilgi kartı (her aşamada aynı düzen) ----
    "oosit_ekle": {"tr": "Oosit ekle", "en": "Add oocyte"},
    "fotografsiz": {"tr": "fotoğrafsız", "en": "no photo"},
    "buyuk_goster": {"tr": "Büyük göster", "en": "Show larger"},
    "tam_ekran": {"tr": "Tam ekran", "en": "Full screen"},
    "numara": {"tr": "Numara", "en": "Number"},
    # Embriyo cycle değiştirmez; transferde "hangi cycle'dan geldi" sorusunun
    # cevabı specimen.cycle_id (bkz. CLAUDE.md "üç alan üç soruyu yanıtlar").
    "geldigi_cycle": {"tr": "Geldiği cycle", "en": "Origin cycle"},
    "cozme_saati_kisa": {"tr": "Çözme saati", "en": "Thaw time"},
    "sagkalim": {"tr": "Sağkalım", "en": "Survival"},
    "canlilik": {"tr": "Canlılık oranı", "en": "Viability"},
    "transfer_durumu": {"tr": "Transfer", "en": "Transfer"},
    "kaynak_cycle": {"tr": "Kaynak cycle", "en": "Source cycle"},
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
    "hasta_kayitlari": {"tr": "Hasta kayıtları", "en": "Patient records"},
    "aktif_hasta": {"tr": "Aktif hasta", "en": "Active patients"},
    "aktif_cycle": {"tr": "Aktif cycle", "en": "Active cycles"},
    "bekleyen_kare": {"tr": "Bekleyen kare", "en": "Pending frames"},
    "dondurulmus": {"tr": "Dondurulmuş", "en": "Frozen"},
    "durum_ozeti": {"tr": "Durum", "en": "Status"},
    "ana_ekran_ipucu": {
        "tr": "Hasta adları bu ekranda görünmez; listeye girince görünür.",
        "en": "Patient names are not shown here; they appear once you open "
              "the list."},
    "aramayi_temizle": {"tr": "Aramayı temizle", "en": "Clear search"},
    "asamalar": {"tr": "Aşamalar", "en": "Stages"},

    # ---- hasta listesi ----
    "hastalar": {"tr": "Hastalar", "en": "Patients"},
    "hasta": {"tr": "Hasta", "en": "Patient"},
    "cycle": {"tr": "Cycle", "en": "Cycle"},
    "cycleler": {"tr": "Cycle'lar", "en": "Cycles"},
    "yetkisiz_ekran": {
        "tr": "ekranına erişim iznin yok. Gerekiyorsa yöneticiye söyle.",
        "en": "— you do not have access to this screen. Ask an administrator "
              "if you need it."},
    "ara_ipucu": {"tr": "Dosya no veya ad ara", "en": "Search file no or name"},
    "aktif_hastalara_don": {"tr": "Aktif hastalara dön",
                            "en": "Back to active patients"},
    "yeni_hasta": {"tr": "Yeni hasta", "en": "New patient"},
    "cryo_haritasi": {"tr": "Cryo haritası", "en": "Cryo map"},
    "yonetim": {"tr": "Yönetici", "en": "Administrator"},
    "arsiv": {"tr": "Arşiv", "en": "Archive"},
    "arsivde": {"tr": "arşivde", "en": "archived"},
    "arama_sonucu": {"tr": "Arama sonucu", "en": "Search results"},
    "son_kayitlar": {"tr": "Son kayıtlar", "en": "Recent records"},
    "es": {"tr": "Eş", "en": "Partner"},
    "n_cycle": {"tr": "{n} cycle", "en": "{n} cycles"},
    "n_cycle_tekil": {"tr": "{n} cycle", "en": "{n} cycle"},
    "n_cycle_sirali": {"tr": "{n}. cycle", "en": "Cycle {n}"},
    "aramaya_uyan_yok": {"tr": "Bu aramaya uyan kayıt yok.",
                         "en": "No records match this search."},
    "henuz_hasta_yok": {"tr": "Henüz hasta kaydı yok.",
                        "en": "No patients recorded yet."},

    # ---- hasta detay ----
    "duzenle": {"tr": "Düzenle", "en": "Edit"},
    "dogum_tarihi_kisa": {"tr": "D.T.", "en": "DOB"},
    "yeni_cycle_ac": {"tr": "Yeni cycle aç", "en": "Open new cycle"},
    "oosit_kucuk": {"tr": "oosit", "en": "oocytes"},
    "bu_hastada_cycle_yok": {"tr": "Bu hastada henüz cycle yok.",
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
}
