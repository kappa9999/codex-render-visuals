param(
    [string]$CodexHome = $env:CODEX_HOME,
    [switch]$Force
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = Join-Path $HOME ".codex"
}

$skillsRoot = Join-Path $CodexHome "skills"
$destination = Join-Path $skillsRoot "codex-visuals"

New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null

if (Test-Path $destination) {
    if (-not $Force) {
        Write-Error "Destination already exists: $destination . Re-run with -Force to replace it."
        exit 1
    }
    Remove-Item -Recurse -Force $destination
}

Copy-Item -Recurse -Force $skillRoot $destination

Write-Host "Installed codex-visuals to $destination"
Write-Host "Restart Codex to pick up the updated skill."
