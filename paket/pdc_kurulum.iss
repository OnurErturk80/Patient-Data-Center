; Patient Data Center — Windows kurulum dosyası (Inno Setup)
;
; DENENMEDI: bu betik henüz bir Windows makinesinde çalıştırılmadı.
; İlk kurulumda birlikte gözden geçirilecek (bkz. PAKETLEME.md).
;
; Önce paketi üret, sonra bunu derle:
;     pyinstaller paket\pdc.spec
;     ISCC.exe paket\pdc_kurulum.iss
;
; Veri klasörü bilerek Program Files'ın DIŞINDA: paketin içi salt okunur ve
; program güncellenince üzerine yazılıyor -- veri orada olsaydı silinirdi
; (bkz. db.py "iki kök"). db.py Windows'ta %PROGRAMDATA% altına bakıyor,
; buradaki yol onunla aynı olmalı.

#define Ad         "Patient Data Center"
#define Surum      "6.50"
#define Yayinci    "Patient Data Center"
#define CalisanAd  "PatientDataCenter.exe"
#define Port       "8000"

[Setup]
AppId={{8F3C2A41-6D5B-4E28-9C17-PDC0000LAB01}
AppName={#Ad}
AppVersion={#Surum}
AppPublisher={#Yayinci}
DefaultDirName={autopf}\{#Ad}
DefaultGroupName={#Ad}
OutputBaseFilename=PatientDataCenter-Kurulum-{#Surum}
Compression=lzma2
SolidCompression=yes
; Görev Zamanlayıcı görevi ve güvenlik duvarı kuralı yönetici hakkı istiyor.
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
WizardStyle=modern

[Languages]
Name: "tr"; MessagesFile: "compiler:Languages\Turkish.isl"

[Files]
; PyInstaller çıktısının tamamı: çalıştırılabilir dosya + _internal klasörü.
Source: "..\dist\PatientDataCenter\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
; Veri klasörü. Program SYSTEM olarak çalışacağı için yazma izni gerekiyor.
Name: "{commonappdata}\PatientDataCenter"; Permissions: users-modify

[Icons]
; Kısayol programı başlatmıyor -- program zaten arka planda çalışıyor.
; Tarayıcıyı açıyor.
Name: "{group}\{#Ad}"; Filename: "http://localhost:{#Port}/"
Name: "{group}\Veri klasoru"; Filename: "{commonappdata}\PatientDataCenter"
Name: "{group}\{#Ad} kaldir"; Filename: "{uninstallexe}"

[Run]
; 1) Açılışta başlat. Servis yerine Görev Zamanlayıcı: servis kurmak için
;    ek bir araç paketlemek gerekirdi, bu Windows'un kendi parçası.
Filename: "schtasks.exe"; Parameters: "/Create /F /TN ""PatientDataCenter"" \
    /TR ""\""{app}\{#CalisanAd}\"""" /SC ONSTART /RU SYSTEM /RL HIGHEST"; \
    Flags: runhidden; StatusMsg: "Acilista baslatma ayarlaniyor..."

; 2) Yerel ağdan erişim. Kural bilerek yalnızca yerel ağ (LocalSubnet):
;    program dışarıya açılmamalı, HTTPS yok.
Filename: "netsh.exe"; Parameters: "advfirewall firewall add rule \
    name=""Patient Data Center"" dir=in action=allow protocol=TCP \
    localport={#Port} remoteip=LocalSubnet"; \
    Flags: runhidden; StatusMsg: "Guvenlik duvari kurali ekleniyor..."

; 3) Şimdi başlat (yeniden başlatmayı beklemesin).
Filename: "schtasks.exe"; Parameters: "/Run /TN ""PatientDataCenter"""; \
    Flags: runhidden; StatusMsg: "Program baslatiliyor..."

; 4) Kurulum bitince tarayıcıda aç.
Filename: "http://localhost:{#Port}/"; Flags: shellexec postinstall nowait; \
    Description: "Programi simdi ac"

[UninstallRun]
Filename: "schtasks.exe"; Parameters: "/End /TN ""PatientDataCenter"""; \
    Flags: runhidden; RunOnceId: "durdur"
Filename: "schtasks.exe"; Parameters: "/Delete /F /TN ""PatientDataCenter"""; \
    Flags: runhidden; RunOnceId: "gorevsil"
Filename: "netsh.exe"; Parameters: "advfirewall firewall delete rule \
    name=""Patient Data Center"""; Flags: runhidden; RunOnceId: "duvarsil"

[UninstallDelete]
; Veri KALIYOR. Hasta kaydı kaldırma sırasında silinmez -- silinmesi
; gerekiyorsa kullanıcı klasörü kendi siler.
Type: filesandordirs; Name: "{app}\_internal"
