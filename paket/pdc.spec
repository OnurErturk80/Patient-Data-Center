# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller tarifi — Windows ve Mac paketleri bunu kullanıyor.

    pip install pyinstaller
    pyinstaller paket/pdc.spec          # proje kökünde çalıştır

Çıktı: `dist/PatientDataCenter/` klasörü (Windows'ta `.exe`, Mac'te `.app`).

İki şeye dikkat, ikisi de sessizce bozulur:

1. **Şablonlar ve `static/` veri olarak eklenmeli.** PyInstaller yalnızca
   `import` edilenleri toplar; Jinja şablonlarını ve CSS'i göremez. Eksik
   kalırsa program açılır ama her ekran hata verir.

2. **Göç betikleri `import` edilmiyor, adıyla çağrılıyor**
   (`importlib.import_module("goc_029")`). PyInstaller bunu göremez, o
   yüzden `hiddenimports`'a tek tek yazılıyor. Eksik kalırsa veritabanı
   güncellemeleri sessizce çalışmaz -- en pahalı hata bu olurdu.
   Ayrıca dosyaların kendisi de veri olarak ekleniyor: `goc.py` önce
   dosyalara bakıyor, bulamazsa modül listesine düşüyor; ikisi de çalışsın.
"""
import glob
import os
import re

from PyInstaller.utils.hooks import collect_submodules

KOK = os.path.abspath(os.getcwd())

gocler = sorted(
    os.path.splitext(os.path.basename(p))[0]
    for p in glob.glob(os.path.join(KOK, "goc_*.py"))
    if re.match(r"^goc_\d+\.py$", os.path.basename(p)))

veriler = [
    (os.path.join(KOK, "templates"), "templates"),
    (os.path.join(KOK, "static"), "static"),
    (os.path.join(KOK, "sema_guncel.sql"), "."),
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
    console=True,          # Windows'ta servis olarak çalışacak; konsol günlüğü
    icon=None,
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False, upx=False,
    name="PatientDataCenter",
)
