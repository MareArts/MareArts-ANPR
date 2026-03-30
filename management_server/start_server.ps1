# Start MareArts ANPR Management Server (Windows)
# This script will automatically load credentials from ~/.marearts/.marearts_env

# Fix UTF-8 output for emoji characters
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location $PSScriptRoot

Write-Host "========================================================================"
Write-Host "Starting MareArts ANPR Management Server"
Write-Host "========================================================================"
Write-Host ""

# Check if config file exists and load credentials
$envFile = Join-Path $env:USERPROFILE ".marearts\.marearts_env"
if (Test-Path $envFile) {
    Write-Host "Found credentials in $envFile"
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -match '^\s*export\s+(\w+)=(.*)') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2].Trim('"').Trim("'"))
        }
        elseif ($line -match '^\s*(\w+)=(.*)' -and $line -notmatch '^\s*#') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2].Trim('"').Trim("'"))
        }
    }
    Write-Host "Credentials loaded"
} else {
    Write-Host "Credentials file not found: $envFile"
    Write-Host "   Run: ma-anpr config"
}

Write-Host ""

# Start server
python server.py
