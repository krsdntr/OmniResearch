# OmniResearch Universal Installer for Windows PowerShell
# Usage:
#   irm https://raw.githubusercontent.com/krsdntr/OmniResearch/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/krsdntr/OmniResearch.git"
$GlobalDir = Join-Path $env:USERPROFILE ".gemini\config\skills\research-scientist"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "    OmniResearch Scientist Workbench Installer (Windows)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$TargetDir = $GlobalDir
if ($args -contains "--local") {
    $TargetDir = Join-Path (Get-Location) ".agents\skills\research-scientist"
    Write-Host "[+] Installing in Local Workspace: $TargetDir" -ForegroundColor Yellow
} else {
    Write-Host "[+] Installing Globally for Google Antigravity: $TargetDir" -ForegroundColor Green
}

$TempDir = Join-Path $env:TEMP ("omni_install_" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

try {
    Write-Host "[+] Fetching latest OmniResearch Skill..." -ForegroundColor Gray
    git clone --depth 1 $RepoUrl "$TempDir\omni" | Out-Null

    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }

    Copy-Item -Path "$TempDir\omni\.agents\skills\research-scientist\*" -Destination $TargetDir -Recurse -Force

    if ($args -contains "--local") {
        Copy-Item -Path "$TempDir\omni\GEMINI.md" -Destination "." -Force -ErrorAction SilentlyContinue
        Copy-Item -Path "$TempDir\omni\CLAUDE.md" -Destination "." -Force -ErrorAction SilentlyContinue
        Copy-Item -Path "$TempDir\omni\AGENTS.md" -Destination "." -Force -ErrorAction SilentlyContinue
        Copy-Item -Path "$TempDir\omni\.cursorrules" -Destination "." -Force -ErrorAction SilentlyContinue
    }

    Write-Host "[OK] OmniResearch successfully installed to: $TargetDir" -ForegroundColor Green
    Write-Host ""
    Write-Host "How to use in Google Antigravity:" -ForegroundColor White
    Write-Host "  - Simply open any research workspace and ask:" -ForegroundColor White
    Write-Host "    'Initialize an OmniResearch scientific study for my project.'" -ForegroundColor Cyan
}
finally {
    Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "========================================================" -ForegroundColor Cyan
