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
