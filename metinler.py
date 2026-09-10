"""Arayüz metinleri — iki dil, tek sözlük.

Neden gettext/babel değil: bu projede framework yok, build adımı yok.
`.po` dosyası derlemek yeni bir kurulum adımı demek olurdu. Düz bir sözlük
hem yeterli hem de kullanıcının kendi düzeltebileceği bir şey.

**Dil lab başına tektir**, kullanıcı başına değil. Yönetici bir kez seçer,
bütün program o dile geçer (karar: CLAUDE.md bekleyen iş 8).

Kullanım:
    şablonda   {{ t("kaydet") }}
    app.py'de  metinler.t("kaydet")

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
