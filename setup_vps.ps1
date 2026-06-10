# ==========================================
# IB Gateway & IBC Auto-Downloader for VPS
# ==========================================

$ErrorActionPreference = "Stop"

Write-Host "1. Downloading IB Gateway Offline Installer..." -ForegroundColor Cyan
$ibgUrl = "https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-windows-x64.exe"
$ibgDest = "$env:USERPROFILE\Desktop\ibgateway-installer.exe"
Invoke-WebRequest -Uri $ibgUrl -OutFile $ibgDest
Write-Host "-> IB Gateway downloaded to your Desktop: $ibgDest" -ForegroundColor Green

Write-Host "`n2. Finding the latest IBC release on GitHub..." -ForegroundColor Cyan
# Fetch latest release info from GitHub
$releaseInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/IbcAlpha/IBC/releases/latest"
# Find the Windows zip asset
$winAsset = $releaseInfo.assets | Where-Object { $_.name -match "IBCWin.*\.zip" }

if ($winAsset) {
    $ibcUrl = $winAsset.browser_download_url
    $ibcDestZip = "$env:USERPROFILE\Desktop\$($winAsset.name)"
    
    Write-Host "-> Found latest IBC version: $($releaseInfo.tag_name). Downloading..."
    Invoke-WebRequest -Uri $ibcUrl -OutFile $ibcDestZip
    
    Write-Host "-> Extracting IBC to C:\IBC..."
    $extractPath = "C:\IBC"
    if (!(Test-Path $extractPath)) {
        New-Item -ItemType Directory -Path $extractPath | Out-Null
    }
    Expand-Archive -Path $ibcDestZip -DestinationPath $extractPath -Force
    
    Write-Host "-> IBC successfully extracted to C:\IBC!" -ForegroundColor Green
    Write-Host "-> Cleaning up IBC zip file..."
    Remove-Item $ibcDestZip
} else {
    Write-Host "-> Could not find the Windows IBC zip in the latest release." -ForegroundColor Red
}

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "DOWNLOAD COMPLETE!" -ForegroundColor Green
Write-Host "Please go to your Desktop and run 'ibgateway-installer.exe' to install the Gateway."
Write-Host "After installation, your IBC configuration will be ready at C:\IBC\config.ini"
Write-Host "==========================================" -ForegroundColor Green
