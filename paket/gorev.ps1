# Patient Data Center -- Windows açılışında programı başlatan Görev Zamanlayıcı
# görevini kurar (v6.204). Kurulum dosyası çağırıyor (paket\pdc_kurulum.iss):
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File gorev.ps1 -Program "<exe>"
#
# schtasks.exe yerine PowerShell, çünkü schtasks'ın kurduğu görev "3 günden uzun
# sürerse durdur" ayarıyla geliyor: sunucu üç günde bir kapanır, bilgisayar
# yeniden açılana kadar kapalı kalırdı. Görev bilgisayar açılınca, kimse oturum
# açmadan SYSTEM olarak başlıyor; program --servis ile açılıyor (tarayıcı ve
# pencere yok, bkz. baslat.py). Öncelik normal: Görev Zamanlayıcı'nın varsayılanı
# (7) "normalin altı" -- sunucu yavaş cevap verirdi.
#
# Dosya UTF-8 (BOM'lu): Windows PowerShell 5.1 BOM'suz dosyayı ANSI okuyup
# Türkçe harfleri bozar.
param(
    [Parameter(Mandatory = $true)][string]$Program,
    [string]$Ad = 'PatientDataCenter'
)
$ErrorActionPreference = 'Stop'

$eylem = New-ScheduledTaskAction -Execute $Program -Argument '--servis' `
    -WorkingDirectory (Split-Path -Parent $Program)
$tetik = New-ScheduledTaskTrigger -AtStartup
$ayar = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable `
    -MultipleInstances IgnoreNew -Priority 4 `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$kim = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName $Ad -Action $eylem -Trigger $tetik -Settings $ayar `
    -Principal $kim -Force `
    -Description 'Patient Data Center: bilgisayar açılınca programı başlatır.' | Out-Null
exit 0
