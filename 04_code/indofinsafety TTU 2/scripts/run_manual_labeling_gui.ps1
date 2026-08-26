$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$gui = Join-Path $root "scripts\manual_labeling_gui.ps1"
if (-not (Test-Path -LiteralPath $gui)) {
    throw "GUI script not found: $gui"
}

& powershell -NoProfile -ExecutionPolicy Bypass -File $gui
