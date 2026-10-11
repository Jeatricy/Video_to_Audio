$ErrorActionPreference = 'Stop'
$instanceFile = Join-Path $PSScriptRoot '.runtime\server.json'
if (-not (Test-Path -LiteralPath $instanceFile)) { exit 0 }
$instance = Get-Content -LiteralPath $instanceFile -Raw | ConvertFrom-Json
try {
    $appInfo = Invoke-RestMethod -Uri ($instance.url + '/api/bootstrap') -TimeoutSec 3
    if ($appInfo.app_id -eq 'audiodrop') {
        Invoke-RestMethod -Uri ($instance.url + '/api/shutdown') -Method Post -Headers @{ 'X-App-Token' = $appInfo.token } -Body '{}' -ContentType 'application/json' -TimeoutSec 5 | Out-Null
        exit 0
    }
} catch { }
$service = Get-CimInstance Win32_Process -Filter ("ProcessId = " + [int]$instance.pid)
$expectedScript = Join-Path $PSScriptRoot 'server.py'
if ($service -and $service.CommandLine -and $service.CommandLine.Contains($expectedScript)) {
    # Stop only FFmpeg children of this project service, then this service.
    Get-CimInstance Win32_Process -Filter ("ParentProcessId = " + [int]$instance.pid) | Where-Object { $_.Name -eq 'ffmpeg.exe' -and $_.CommandLine.Contains($PSScriptRoot) } | ForEach-Object { Stop-Process -Id $_.ProcessId -ErrorAction SilentlyContinue }
    Stop-Process -Id ([int]$instance.pid) -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $instanceFile -ErrorAction SilentlyContinue
}
