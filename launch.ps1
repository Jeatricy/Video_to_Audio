param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$runtimeDir = Join-Path $projectRoot '.runtime'
$instanceFile = Join-Path $runtimeDir 'server.json'

if (Test-Path -LiteralPath $instanceFile) {
    try {
        $instance = Get-Content -LiteralPath $instanceFile -Raw | ConvertFrom-Json
        $existing = Invoke-RestMethod -Uri ($instance.url + '/api/bootstrap') -TimeoutSec 3
        if ($existing.app_id -eq 'audiodrop') {
            if (-not $NoBrowser) { Start-Process $instance.url }
            exit 0
        }
    } catch { }
}

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
$usePyLauncher = $false
if (-not $pythonCommand -or $pythonCommand.Source -like '*WindowsApps*') {
    $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
    $usePyLauncher = $true
}
if (-not $pythonCommand) {
    Write-Host 'Python 3.10 or newer is required. Install Python, then run start.bat again.'
    exit 1
}

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
$serverPath = Join-Path $projectRoot 'server.py'
$serverArguments = '"' + $serverPath + '" --no-browser'
if ($usePyLauncher) { $serverArguments = '-3 ' + $serverArguments }
$env:PYTHONIOENCODING = 'utf-8'
$serviceProcess = Start-Process -FilePath $pythonCommand.Source -ArgumentList $serverArguments -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtimeDir 'server.stdout.log') -RedirectStandardError (Join-Path $runtimeDir 'server.stderr.log')

for ($attempt = 0; $attempt -lt 80; $attempt++) {
    Start-Sleep -Milliseconds 250
    if ($serviceProcess.HasExited) {
        Write-Host 'AudioDrop could not start. See .runtime/server.stderr.log.'
        Get-Content -LiteralPath (Join-Path $runtimeDir 'server.stderr.log') -ErrorAction SilentlyContinue
        exit 1
    }
    if (Test-Path -LiteralPath $instanceFile) {
        try {
            $instance = Get-Content -LiteralPath $instanceFile -Raw | ConvertFrom-Json
            $response = Invoke-RestMethod -Uri ($instance.url + '/api/bootstrap') -TimeoutSec 2
            if ($response.app_id -eq 'audiodrop') {
                if (-not $NoBrowser) { Start-Process $instance.url }
                exit 0
            }
        } catch { }
    }
}
Write-Host 'Startup is taking longer than expected. See .runtime/server.stderr.log.'
exit 1
