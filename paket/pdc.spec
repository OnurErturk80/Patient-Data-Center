# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller tarifi — Windows ve Mac paketleri bunu kullanıyor.

    pip install pyinstaller pillow
    pyinstaller --noconfirm paket/pdc.spec      # proje kökünde çalıştır

Çıktı:
    Windows  dist/PatientDataCenter/PatientDataCenter.exe (+ _internal/)
             -> paket/pdc_kurulum.iss bunu kurulum dosyasına koyuyor
    Mac      dist/Patient Data Center.app
             -> .github/workflows/paket.yml bunu .dmg'ye koyuyor
    ayrıca   build/paket/paket_bilgisi.json (sürüm, derleme kimliği) ve simgeler

GitHub Actions her derlemede bunu çalıştırıp programı deniyor (PAKETLEME.md).

Dikkat, hepsi sessizce bozulur:

1. **Şablonlar ve `static/` veri olarak eklenmeli.** PyInstaller yalnızca
   `import` edilenleri toplar; Jinja şablonlarını ve CSS'i göremez. Eksik
   kalırsa program açılır ama her ekran hata verir.

2. **Göç betikleri `import` edilmiyor, adıyla çağrılıyor**
   (`importlib.import_module("goc_029")`). PyInstaller bunu göremez, o
   yüzden `hiddenimports`'a tek tek yazılıyor. Eksik kalırsa veritabanı
   güncellemeleri sessizce çalışmaz -- en pahalı hata bu olurdu.
   Ayrıca dosyaların kendisi de veri olarak ekleniyor: `goc.py` önce
   dosyalara bakıyor, bulamazsa modül listesine düşüyor; ikisi de çalışsın.

3. **README.md pakete giriyor** (v6.204): çalışan sürüm oradan okunuyor
   (`app.kod_surumu()`, Yönetici panelinin sürüm kartı).

4. **`paket_bilgisi.json`** (v6.204): derlemenin kimliği (sürüm + commit +
   tarih). Mac'te yenilenmiş uygulama çalışan eski derlemeyi bununla tanıyıp
   kapatıyor (`baslat.py`); kimlik her derlemede farklı olmalı.

5. **Program pencereli** (konsolsuz, v6.204): Windows'ta Görev Zamanlayıcı
   onu SYSTEM olarak başlatıyor, çift tıklayınca kara pencere açılmasın;
   Mac'te uygulama. Günlük `program.log`'da (`baslat.py`).
"""
import datetime
import glob
import json
import os
import re
import subprocess
import sys

from PyInstaller.utils.hooks import collect_submodules

KOK = os.path.abspath(os.getcwd())
YAPI = os.path.join(KOK, "build", "paket")        # tarifin ürettiği ara dosyalar
os.makedirs(YAPI, exist_ok=True)

# Mac'te uygulamanın kimliği; `baslat.MAC_ETIKETI` ile aynı olmalı
# (oturum açılışında başlatan LaunchAgent'ın adı).
MAC_KIMLIGI = "com.patientdatacenter.pdc"


def _surum():
    """README'deki en büyük "# v6.xxx" başlığı -- `app.kod_surumu()`'nün
    kuralı. Tarif `app`'i import edemez (veritabanına, veri klasörüne dokunur)."""
    with open(os.path.join(KOK, "README.md"), encoding="utf-8") as f:
        metin = f.read()
    surumler = [tuple(int(x) for x in m.groups())
                for m in re.finditer(r"^# v(\d+)\.(\d+)\b", metin, re.M)]
    return "%d.%d" % max(surumler) if surumler else "0.0"


def _commit():
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        return sha[:7]
    try:
        cikti = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=KOK,
                               capture_output=True, text=True, timeout=10)
        return cikti.stdout.strip() or "yerel"
    except Exception:
        return "yerel"


SURUM = _surum()
KIMLIK = "v%s · %s · %s" % (SURUM, _commit(),
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
PAKET_BILGISI = os.path.join(YAPI, "paket_bilgisi.json")
with open(PAKET_BILGISI, "w", encoding="utf-8") as f:
    json.dump({"surum": "v" + SURUM, "kimlik": KIMLIK, "sistem": sys.platform},
              f, ensure_ascii=False)
print("Paket:", KIMLIK)


def _simgeler():
    """Program simgesi `static/ikon_512.png`'den (telefondaki simgenin aynısı).

    Windows'a olduğu gibi (.ico), Mac'e köşeleri yuvarlatılıp Apple'ın
    ızgarasına göre küçültülmüş hali (1024'lük tuvalin ortadaki 824'ü, .icns):
    düz kare Mac'te öteki simgelerden büyük ve köşeli durur. Pillow yalnızca
    derlemede gerekiyor, programın bağımlılığı değil; yoksa simgesiz derlenir.
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("UYARI: Pillow yok, program simgesiz derleniyor (pip install pillow)")
        return None, None
    kaynak = Image.open(os.path.join(KOK, "static", "ikon_512.png")).convert("RGBA")
    ico = os.path.join(YAPI, "pdc.ico")
    kaynak.save(ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                            (128, 128), (256, 256)])
    tuval = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    maske = Image.new("L", (824, 824), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, 823, 823), radius=185, fill=255)
    tuval.paste(kaynak.resize((824, 824), Image.LANCZOS), (100, 100), maske)
    icns = os.path.join(YAPI, "pdc.icns")
    tuval.save(icns, format="ICNS")
    return ico, icns


ICO, ICNS = _simgeler()

gocler = sorted(
    os.path.splitext(os.path.basename(p))[0]
    for p in glob.glob(os.path.join(KOK, "goc_*.py"))
    if re.match(r"^goc_\d+\.py$", os.path.basename(p)))

veriler = [
    (os.path.join(KOK, "templates"), "templates"),
    (os.path.join(KOK, "static"), "static"),
    (os.path.join(KOK, "sema_guncel.sql"), "."),
    (os.path.join(KOK, "README.md"), "."),
    (PAKET_BILGISI, "."),
]
# Gömülü resmî formlar: ticari dağıtımda silinecekler, o yüzden varsa ekle
# (bkz. CLAUDE.md "Ticari dağıtımda gömülü form olmayacak").
for ek in ("form_kalip.json",):
    if os.path.exists(os.path.join(KOK, ek)):
        veriler.append((os.path.join(KOK, ek), "."))
veriler += [(p, ".") for p in glob.glob(os.path.join(KOK, "goc_*.py"))]

gizli = gocler + collect_submodules("uvicorn") + [
    "goc", "goc_hepsi",
    # uvicorn bunları adıyla yüklüyor; toplayıcı bazı sürümlerde kaçırıyor.
    "uvicorn.loops.auto", "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets.auto", "uvicorn.lifespan.on",
]

a = Analysis(
    [os.path.join(KOK, "baslat.py")],
    pathex=[KOK],
    binaries=[],
    datas=veriler,
    hiddenimports=gizli,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "PIL", "numpy", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="PatientDataCenter",
    debug=False,
    strip=False,
    upx=False,
    console=False,         # pencereli: bkz. belgenin 5. maddesi
    icon=ICO if sys.platform == "win32" else None,
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False, upx=False,
    name="PatientDataCenter",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="Patient Data Center.app",
        icon=ICNS,
        bundle_identifier=MAC_KIMLIGI,
        version=SURUM,
        info_plist={
            "CFBundleName": "Patient Data Center",
            "CFBundleDisplayName": "Patient Data Center",
            "CFBundleShortVersionString": SURUM,
            "CFBundleVersion": SURUM,
            # Dock'ta simge yok: arka planda çalışan bir sunucu, ekranı
            # tarayıcıda. Uygulamaya yeniden çift tıklamak tarayıcıyı açar.
            "LSUIElement": True,
            "NSHighResolutionCapable": True,
            "LSApplicationCategoryType": "public.app-category.medical",
            # macOS 15'in "yerel ağ" izni: sorarsa telefonların bağlanması için.
            "NSLocalNetworkUsageDescription":
                "Telefonlar ve öteki bilgisayarlar programa iç ağdan bağlansın diye.",
        },
    )
