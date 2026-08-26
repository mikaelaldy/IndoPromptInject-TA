param(
    [int]$PerLabelPerStratum = 2,
    [int]$Seed = 42
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$outputDir = Join-Path $root "outputs"
$samplePath = Join-Path $outputDir "manual_validation_stratified_sample.csv"
$summaryPath = Join-Path $outputDir "manual_validation_stratified_summary.csv"

$models = @("gpt-5.2", "gemini-3-flash", "qwen3.6-plus")
$allRows = New-Object System.Collections.Generic.List[object]

foreach ($model in $models) {
    $path = Join-Path $outputDir ("final_labels_{0}.csv" -f $model)
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing final labels file: $path"
    }

    Import-Csv -LiteralPath $path | ForEach-Object {
        $_ | Add-Member -NotePropertyName model -NotePropertyValue $model -Force
        $allRows.Add($_)
    }
}

function Get-StableScore {
    param(
        [string]$Text,
        [int]$Seed
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes("$Seed|$Text")
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hash = $sha.ComputeHash($bytes)
    return [BitConverter]::ToString($hash).Replace("-", "")
}

$sampled = New-Object System.Collections.Generic.List[object]
$groups = $allRows | Group-Object model, category, attack_type, final_label

foreach ($group in $groups) {
    $picked = $group.Group |
        Sort-Object @{Expression = { Get-StableScore -Text ("{0}|{1}|{2}|{3}" -f $_.model, $_.id, $_.category, $_.attack_type) -Seed $Seed }} |
        Select-Object -First $PerLabelPerStratum

    foreach ($row in $picked) {
        $sampled.Add($row)
    }
}

$ordered = $sampled |
    Sort-Object model, category, attack_type, final_label, id |
    ForEach-Object -Begin { $i = 1 } -Process {
        [pscustomobject]@{
            review_id = "MV{0:D3}" -f $i
            model = $_.model
            id = $_.id
            source = $_.source
            category = $_.category
            attack_type = $_.attack_type
            prompt = $_.prompt
            response = $_.response
            judge_label = $_.judge_label
            judge_reason = $_.judge_reason
            judge_confidence = $_.judge_confidence
            manual_label = ""
            manual_notes = ""
            manual_is_valid = "False"
        }
        $i++
    }

$ordered | Export-Csv -LiteralPath $samplePath -NoTypeInformation -Encoding UTF8

$summary = $ordered |
    Group-Object model, category, attack_type, judge_label |
    Sort-Object Name |
    ForEach-Object {
        $parts = $_.Name -split ", "
        [pscustomobject]@{
            model = $parts[0]
            category = $parts[1]
            attack_type = $parts[2]
            judge_label = $parts[3]
            sampled_n = $_.Count
        }
    }

$summary | Export-Csv -LiteralPath $summaryPath -NoTypeInformation -Encoding UTF8

Write-Output "Created: $samplePath"
Write-Output "Created: $summaryPath"
Write-Output ("Sample rows: {0}" -f @($ordered).Count)
