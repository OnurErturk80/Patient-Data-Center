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
    "n_embriyo": {"tr": "{n} embriyo", "en": "{n} embryos"},
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
    "yonetim": {"tr": "Yönetim", "en": "Administration"},
    "arsiv": {"tr": "Arşiv", "en": "Archive"},
    "arsivde": {"tr": "arşivde", "en": "archived"},
    "arama_sonucu": {"tr": "Arama sonucu", "en": "Search results"},
    "son_kayitlar": {"tr": "Son kayıtlar", "en": "Recent records"},
    "es": {"tr": "Eş", "en": "Partner"},
    "n_cycle": {"tr": "{n} cycle", "en": "{n} cycles"},
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
