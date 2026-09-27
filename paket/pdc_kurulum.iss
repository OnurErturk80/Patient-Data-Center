; Patient Data Center — Windows kurulum dosyası (Inno Setup 6), v6.204
;
; GitHub Actions her derlemede bunu derleyip sessizce kuruyor, güncelliyor ve
; kaldırıyor (.github/workflows/paket.yml, PAKETLEME.md). Elle:
;     pyinstaller --noconfirm paket\pdc.spec
;     ISCC.exe /DSurum=6.204 paket\pdc_kurulum.iss
; Çıktı: dist\PatientDataCenter-Kurulum-<sürüm>.exe
;
; Veri klasörü bilerek Program Files'ın DIŞINDA: paketin içi salt okunur ve
; program güncellenince üzerine yazılıyor -- veri orada olsaydı silinirdi
; (bkz. db.py "iki kök"). db.py Windows'ta %PROGRAMDATA% altına bakıyor,
; buradaki yol onunla aynı olmalı. Kaldırınca veri KALIYOR.
;
; Dosya UTF-8 (BOM'lu): Inno Setup BOM'suz dosyayı ANSI okur, Türkçe bozulur.

#ifndef Surum
  #define Surum "0.0"
#endif
#define Ad         "Patient Data Center"
#define Yayinci    "Patient Data Center"
#define CalisanAd  "PatientDataCenter.exe"
#define GorevAdi   "PatientDataCenter"
#define VeriAdi    "PatientDataCenter"
#define Port       "8000"
#define HttpsPort  "8443"
#define Simge      "..\build\paket\pdc.ico"

[Setup]
; AppId değişirse güncelleme eskisinin üzerine kurulmaz, ikinci bir kurulum olur.
AppId={{8F3C2A41-6D5B-4E28-9C17-5D3C0A1B6E01}
AppName={#Ad}
AppVersion={#Surum}
AppVerName={#Ad} {#Surum}
AppPublisher={#Yayinci}
VersionInfoVersion={#Surum}
DefaultDirName={autopf}\{#Ad}
DefaultGroupName={#Ad}
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=PatientDataCenter-Kurulum-{#Surum}
Compression=lzma2
SolidCompression=yes
; Görev Zamanlayıcı ve güvenlik duvarı yönetici hakkı istiyor.
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
; Çalışan programı kurulum kendisi durduruyor (PrepareToInstall).
CloseApplications=no
UninstallDisplayIcon={app}\{#CalisanAd}
UninstallDisplayName={#Ad}
#if FileExists(AddBackslash(SourcePath) + Simge)
SetupIconFile={#Simge}
#endif

[Languages]
Name: "tr"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "masaustu"; Description: "Masaüstüne kısayol koy"; GroupDescription: "Kısayollar:"

[InstallDelete]
; PyInstaller'ın klasörü her sürümde baştan: eski sürümden kalan bir dosya
; yenisine karışmasın.
Type: filesandordirs; Name: "{app}\_internal"

[Files]
; PyInstaller çıktısının tamamı: çalıştırılabilir dosya + _internal klasörü.
Source: "..\dist\PatientDataCenter\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gorev.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; Veri klasörü. Program SYSTEM olarak çalışıyor; kullanıcılar da yazabilsin
; (programa çift tıklayan kullanıcının açtığı program aynı klasörü kullanıyor).
Name: "{commonappdata}\{#VeriAdi}"; Permissions: users-modify; Flags: uninsneveruninstall

[Icons]
; Kısayollar programı başlatmıyor -- program zaten arka planda çalışıyor.
; Tarayıcıyı programın adresinde açıyorlar.
Name: "{group}\{#Ad}"; Filename: "http://localhost:{#Port}/"; IconFilename: "{app}\{#CalisanAd}"
Name: "{group}\Veri klasörü"; Filename: "{commonappdata}\{#VeriAdi}"
Name: "{group}\Program günlüğü"; Filename: "{commonappdata}\{#VeriAdi}\program.log"
Name: "{group}\{#Ad} kaldır"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Ad}"; Filename: "http://localhost:{#Port}/"; \
    IconFilename: "{app}\{#CalisanAd}"; Tasks: masaustu

[Run]
; 1) Açılışta başlat: Görev Zamanlayıcı, SYSTEM, kimse oturum açmadan. Servis
;    yerine görev: servis kurmak için ek bir araç paketlemek gerekirdi.
;    Görevi PowerShell kuruyor, schtasks değil -- gorev.ps1'in başına bak.
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; \
    Parameters: "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""{app}\gorev.ps1"" -Program ""{app}\{#CalisanAd}"" -Ad ""{#GorevAdi}"""; \
    Flags: runhidden waituntilterminated; StatusMsg: "Açılışta başlatma ayarlanıyor..."; \
    AfterInstall: GorevDenetle

; 2) Güvenlik duvarı: 8000 ve 8443 (güvenli bağlantı, v6.196) yalnızca yerel
;    ağdan. Eski kural önce siliniyor: güncellemede ikinci kural olmasın.
;    Program ayrıca kendi "ağ erişimi" ayarıyla yeni kurulumda ağa kapalı
;    başlıyor (v6.203); telefonlar yönetici açınca bağlanıyor.
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall delete rule name=""{#Ad}"""; \
    Flags: runhidden waituntilterminated
Filename: "{sys}\netsh.exe"; \
    Parameters: "advfirewall firewall add rule name=""{#Ad}"" dir=in action=allow protocol=TCP localport={#Port},{#HttpsPort} remoteip=localsubnet profile=any"; \
    Flags: runhidden waituntilterminated; StatusMsg: "Güvenlik duvarı kuralı ekleniyor..."

; 3) Şimdi başlat (bilgisayarın yeniden açılmasını beklemesin).
Filename: "{sys}\schtasks.exe"; Parameters: "/Run /TN ""{#GorevAdi}"""; \
    Flags: runhidden waituntilterminated; StatusMsg: "Program başlatılıyor..."

; 4) Kurulum bitince tarayıcıda aç -- program cevap verince (ilk açılışta göçler
;    ve güvenli bağlantının sertifikası birkaç saniye sürüyor).
Filename: "http://localhost:{#Port}/"; Description: "Programı şimdi aç"; \
    Flags: shellexec postinstall nowait skipifsilent; BeforeInstall: ProgramiBekle

[UninstallDelete]
Type: filesandordirs; Name: "{app}\_internal"

[Code]
const
  GorevAdi = '{#GorevAdi}';

function Calistir(Dosya, Parametreler: String): Integer;
var
  Sonuc: Integer;
begin
  if not Exec(ExpandConstant('{sys}\') + Dosya, Parametreler, '', SW_HIDE,
              ewWaitUntilTerminated, Sonuc) then
    Sonuc := -1;
  Result := Sonuc;
end;

// Çalışan programı durdur: güncellemede dosyaları değiştirebilmek, kaldırırken
// silebilmek için. Önce görev, sonra elle açılmış bir kopya kalmışsa o.
procedure ProgramiDurdur();
begin
  Calistir('schtasks.exe', '/End /TN "' + GorevAdi + '"');
  Calistir('taskkill.exe', '/F /IM {#CalisanAd}');
  Sleep(1500);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  ProgramiDurdur();
  Result := '';
end;

procedure GorevDenetle();
begin
  if Calistir('schtasks.exe', '/Query /TN "' + GorevAdi + '"') <> 0 then
  begin
    Log('Gorev Zamanlayici gorevi kurulamadi.');
    SuppressibleMsgBox('Programın bilgisayar açılınca kendiliğinden başlaması ' +
      'ayarlanamadı (Görev Zamanlayıcı). Kurulum dosyasını yönetici olarak ' +
      'yeniden çalıştırın.', mbError, MB_OK, IDOK);
  end;
end;

function ProgramCevapVeriyor(): Boolean;
var
  Istek: Variant;
begin
  Result := False;
  try
    Istek := CreateOleObject('WinHttp.WinHttpRequest.5.1');
    Istek.SetProxy(1);
    Istek.SetTimeouts(2000, 2000, 2000, 2000);
    Istek.Open('GET', 'http://127.0.0.1:{#Port}/__pdc', False);
    Istek.Send('');
    Result := (Istek.Status = 200);
  except
    Result := False;
  end;
end;

// Tarayıcı açılmadan önce program hazır olsun. En çok bir dakika.
procedure ProgramiBekle();
var
  I: Integer;
begin
  for I := 1 to 120 do
  begin
    if ProgramCevapVeriyor() then
      Exit;
    Sleep(500);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    ProgramiDurdur();
    Calistir('schtasks.exe', '/Delete /F /TN "' + GorevAdi + '"');
    Calistir('netsh.exe', 'advfirewall firewall delete rule name="{#Ad}"');
  end;
end;
