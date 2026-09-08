"""Sıfırdan güncel bir veritabanı kurar.

Yeni bir makinede (veya temiz bir test veritabanı için) tek komutla:
  - güncel şemayı oluşturur (tüm göçler uygulanmış hali)
  - seçim listelerini ve varsayılan ayarları doldurur
  - bir kullanıcı oluşturur ve şifresini sorar
  - bu makineye uygun klasör ayarlarını yazar

Mevcut lab.db varsa DOKUNMAZ — önce yeniden adlandırman gerekir.

Kullanım:  python sifirdan_kur.py      (Mac'te: python3 sifirdan_kur.py)
"""

import getpass
import json
import platform
import sqlite3
import sys
from pathlib import Path

KOK = Path(__file__).parent
DB = KOK / "lab.db"
SEMA = KOK / "sema_guncel.sql"

if DB.exists():
    sys.exit(
        f"lab.db zaten var: {DB}\n"
        "Uzerine yazmamak icin durduruldu. Yeni bir tane istiyorsan once\n"
        "mevcut dosyayi yeniden adlandir (ornek: lab_eski.db)."
    )
if not SEMA.exists():
    sys.exit(f"sema_guncel.sql bulunamadi: {SEMA}")

b = sqlite3.connect(DB)
b.executescript(SEMA.read_text(encoding="utf-8"))
b.commit()
tablo = b.execute(
    "SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
print(f"Sema olusturuldu: {tablo} tablo")

b.execute("INSERT INTO lab (id, ad) VALUES (1, 'Embriyoloji Laboratuvari')")

# ------------------------------------------------------------------ listeler
LISTELER = {
    "maturasyon": [("mii","MII"),("mi","MI"),("gv","GV"),
                   ("degenere","Dejenere"),("atretik","Atretik")],
    "gecis_zorlugu": [("kolay","Kolay"),("normal","Normal"),("zor","Zor")],
    "icsi_sonuc": [("basarili","Başarılı"),("degenere","Dejenere")],
    "fert_sonuc": [("normal","Normal"),("degenere","Dejenere"),("kayip","Kayıp")],
    "pn_sayisi": [("0","0PN"),("1","1PN"),("2","2PN"),("3","3PN"),("4+","4PN ve üzeri")],
    "pn_skoru": [("z1","Z1"),("z2","Z2"),("z3","Z3"),("z4","Z4")],
    "simetri": [("esit","Eşit"),("hafif_esitsiz","Hafif eşitsiz"),("esitsiz","Eşitsiz")],
    "bl_genisleme": [("1","1 - Erken blastosöl"),("2","2 - Blastosöl ≥ yarım"),
                     ("3","3 - Tam blastokist"),("4","4 - Genişlemiş"),
                     ("5","5 - Hatching"),("6","6 - Hatched"),
                     ("erken_morula","Erken morula"),("morula","Morula"),
                     ("kavitasyon","Kavitasyon"),("arrest","Arrest")],
    "bl_derece": [("1","Derece 1"),("2","Derece 2"),("3","Derece 3")],
    "bl_icm": [("a","A"),("b","B"),("c","C")],
    "bl_te": [("a","A"),("b","B"),("c","C")],
    "bulgu_icsi": [
        ("kalin_zona","Kalın zona"),("ince_zona","İnce zona"),
        ("duzensiz_zona","Düzensiz zona"),("granullu_sitoplazma","Granüllü sitoplazma"),
        ("viskoz_sitoplazma","Viskoz sitoplazma"),
        ("merkezi_granulasyon","Merkezi granülasyon"),("vakuol","Vakuol"),
        ("ser_kumesi","SER kümesi"),("refraktil_cisim","Refraktil cisim"),
        ("koyu_sitoplazma","Koyu sitoplazma"),("genis_pvs","Geniş PVS"),
        ("pvs_debris","PVS'de debris"),("fragmente_pb","Fragmente polar cisim"),
        ("buyuk_pb","Büyük polar cisim"),("oval_oosit","Oval oosit"),
        ("duzensiz_form","Düzensiz form")],
    "bulgu_fert": [("halo","Halo"),("pn_hizasiz","PN hizasız"),
                   ("sitoplazmik_granulasyon","Sitoplazmik granülasyon"),
                   ("vakuol","Vakuol")],
    "bulgu_cleavage": [("multinukleasyon","Multinükleasyon"),
                       ("duzensiz_bolunme","Düzensiz bölünme"),("vakuol","Vakuol")],
    "sperm_alinma": [("masturbasyon","Mastürbasyon"),("tese","TESE"),("tesa","TESA"),
                     ("donor","Donör"),("thaw","Çözülmüş örnek")],
    "sperm_hazirlama": [("swim_up","Swim-up"),("gradient","Gradient"),("yikama","Yıkama")],
    "viskozite": [("normal","Normal"),("artmis","Artmış"),("ileri_artmis","İleri artmış")],
    "cycle_tipi": [("ivf_icsi","IVF / ICSI cycle'ı"),
                   ("fet","FET (donmuş embriyo transferi)"),
                   ("oosit_cryo","Oosit dondurma")],
    "protokol_tipi": [("antagonist","Antagonist"),("long_agonist","Long agonist"),
                      ("short_agonist","Short agonist"),("mild","Mild"),
                      ("natural","Natural"),("ppos","PPOS")],
    "trigger_tipi": [("hcg","hCG"),("gnrh_agonist","GnRH agonist"),("dual","Dual trigger")],
    "thaw_sagkalim": [("canli","Canlı"),("degenere","Dejenere"),
                      ("kismi_hasar","Kısmi hasar")],
    "discard_sebep": [("gelisimsel","Gelişimsel"),("genetik","Genetik"),
                      ("hasta_talebi","Hasta talebi"),
                      ("sure_doldu","Saklama süresi doldu"),("diger","Diğer")],
    "pgt_sonuc": [("oploid","Öploid"),("anoploid","Anöploid"),("mozaik","Mozaik"),
                  ("sonuc_yok","Sonuç yok"),("no_call","No-call")],
    "sonlanma": [("canli_dogum","Canlı doğum"),("abortus","Abortus"),
                 ("biyokimyasal","Biyokimyasal gebelik"),("ektopik","Ektopik"),
                 ("devam_ediyor","Devam ediyor"),("takip_kaybi","Takip kaybı")],
    "endikasyon": [
        ("erkek_faktoru","Erkek faktörü"),
        ("siddetli_erkek_faktoru","Şiddetli erkek faktörü"),
        ("azoospermi","Azoospermi"),("tubal_faktor","Tubal faktör"),
        ("endometriozis","Endometriozis"),
        ("ovulatuar_disfonksiyon","Ovulatuar disfonksiyon / PCOS"),
        ("azalmis_over_rezervi","Azalmış over rezervi"),
        ("ileri_anne_yasi","İleri anne yaşı"),("uterin_faktor","Uterin faktör"),
        ("aciklanamayan","Açıklanamayan infertilite"),
        ("tekrarlayan_implantasyon","Tekrarlayan implantasyon başarısızlığı"),
        ("tekrarlayan_gebelik_kaybi","Tekrarlayan gebelik kaybı"),
        ("pgt_endikasyonu","PGT endikasyonu"),
        ("fertilite_koruma","Fertilite koruma"),
        ("donor_oosit","Donör oosit"),("donor_sperm","Donör sperm"),
        ("diger","Diğer")],
    "goruntu_asama": [
        ("denudasyon","Denüdasyon"),("icsi","ICSI"),
        ("fertilizasyon_kontrolu","Fertilizasyon kontrolü"),
        ("gun2","Gün 2"),("gun3","Gün 3"),("blastokist","Blastokist"),
        ("vitrifikasyon_oncesi","Vitrifikasyon öncesi"),
        ("thaw_sonrasi","Thaw sonrası"),("transfer_oncesi","Transfer öncesi"),
        ("diger","Diğer")],
}

sira = 0
for liste, degerler in LISTELER.items():
    for kod, etiket in degerler:
        b.execute("INSERT OR IGNORE INTO liste_degeri "
                  "(lab_id, liste_adi, kod, etiket, sira) VALUES (1,?,?,?,?)",
                  (liste, kod, etiket, sira))
        sira += 1
n = b.execute("SELECT COUNT(*) FROM liste_degeri").fetchone()[0]
print(f"Secim listeleri: {n} deger, {len(LISTELER)} liste")

# ------------------------------------------------------------------ ayarlar
from datetime import datetime
AYARLAR = [
    ("fert_kontrol_saat", "17", "ICSI sonrasi hedef fertilizasyon kontrolu (saat)"),
    ("gun3_kontrol_saat", "68", "ICSI sonrasi gun 3 kontrolu (saat)"),
    ("blast_kontrol_saat", "116", "ICSI sonrasi gun 5 kontrolu (saat)"),
    ("lab_no_onek", str(datetime.now().year), "Lab kayit no oneki"),
    ("lab_no_basamak", "4", "Sira kac basamakli"),
    ("lab_no_bosluk_doldur", "1", "1 = bosalan numara yeniden kullanilir"),
    ("lab_no_yillik_sifirla", "1", "1 = her yil sira 1'den baslar"),
    ("yedek_uyari_gun", "3", "Son yedek bu kadar gunden eskiyse uyar"),
]
for anahtar, deger, aciklama in AYARLAR:
    b.execute("INSERT OR IGNORE INTO ayarlar (lab_id, anahtar, deger, aciklama) "
              "VALUES (1,?,?,?)", (anahtar, deger, aciklama))
b.commit()
b.close()
print(f"Ayarlar: {len(AYARLAR)} kayit")

# ------------------------------------------------------------------ kullanici
import db as _db
import guvenlik

print("\nBir kullanici olusturalim.")
ad = input("  Ad soyad      : ").strip() or "Kullanici"
kod = (input("  Kisa kod (ON) : ").strip() or ad[:2]).upper()
kadi = (input("  Kullanici adi : ").strip() or "onur").lower()
while True:
    s1 = getpass.getpass("  Sifre (min 8) : ")
    s2 = getpass.getpass("  Tekrar        : ")
    if s1 != s2:
        print("  Sifreler ayni degil, tekrar dene.")
    elif len(s1) < 8:
        print("  En az 8 karakter olmali.")
    else:
        break

_db.yaz("INSERT INTO kullanici (lab_id, ad_soyad, kisa_kod, rol, kullanici_adi, "
        "sifre_hash) VALUES (1,?,?,'embriyolog',?,?)",
        (ad, kod, kadi, guvenlik.sifrele(s1)))
print(f"Kullanici olusturuldu: {kadi}")

# ------------------------------------------------------------------ yerel yol
sistem = platform.system()
ev = Path.home()
if sistem == "Windows":
    yerel = {"goruntu_kaynak_klasor": str(ev / "Desktop" / "snapshot"),
             "goruntu_arsiv_klasor": str(KOK / "arsiv"),
             "yedek_klasor": "D:\\lab_yedek"}
else:
    yerel = {"goruntu_kaynak_klasor": str(ev / "Desktop" / "snapshot"),
             "goruntu_arsiv_klasor": str(KOK / "arsiv"),
             "yedek_klasor": str(ev / "lab_yedek")}

hedef = KOK / "yerel_ayar.json"
if not hedef.exists():
    hedef.write_text(json.dumps(yerel, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nyerel_ayar.json yazildi ({sistem}):")
    for k, v in yerel.items():
        print(f"  {k:24s} = {v}")
    print("Yollar yanlissa dosyayi metin editoruyle duzelt.")

print("\nKurulum tamam. Baslatmak icin:")
komut = "python" if sistem == "Windows" else "python3"
print(f"  {komut} -m uvicorn app:uygulama --host 0.0.0.0 --port 8000")
