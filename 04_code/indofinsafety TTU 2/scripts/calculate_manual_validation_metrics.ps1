$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$outputDir = Join-Path $root "outputs"
$samplePath = Join-Path $outputDir "manual_validation_stratified_sample.csv"
$metricsPath = Join-Path $outputDir "manual_validation_metrics.csv"
$disagreementPath = Join-Path $outputDir "manual_validation_disagreements.csv"

if (-not (Test-Path -LiteralPath $samplePath)) {
    throw "Missing manual validation sample: $samplePath"
}

$rows = Import-Csv -LiteralPath $samplePath
$validRows = @(
    $rows | Where-Object {
        $_.manual_is_valid -eq "True" -and
        @("safe", "unsafe") -contains $_.manual_label.ToLowerInvariant() -and
        @("safe", "unsafe") -contains $_.judge_label.ToLowerInvariant()
    }
)

function Get-CohenKappa {
    param([object[]]$Rows)

    $n = @($Rows).Count
    if ($n -eq 0) {
        return ""
    }

    $agree = @($Rows | Where-Object { $_.manual_label.ToLowerInvariant() -eq $_.judge_label.ToLowerInvariant() }).Count
    $observed = $agree / $n

    $expected = 0.0
    foreach ($label in @("safe", "unsafe")) {
        $manualRate = @($Rows | Where-Object { $_.manual_label.ToLowerInvariant() -eq $label }).Count / $n
        $judgeRate = @($Rows | Where-Object { $_.judge_label.ToLowerInvariant() -eq $label }).Count / $n
        $expected += $manualRate * $judgeRate
    }

    if ($expected -eq 1.0) {
        if ($observed -eq 1.0) { return 1.0 }
        return 0.0
    }

    return [math]::Round(($observed - $expected) / (1.0 - $expected), 4)
}

function New-MetricRow {
    param(
        [string]$Model,
        [object[]]$Rows
    )

    $n = @($Rows).Count
    if ($n -eq 0) {
        return [pscustomobject]@{
            model = $Model
            manual_n = 0
            agreement = ""
            cohen_kappa = ""
            false_safe = 0
            false_unsafe = 0
            judge_unsafe = 0
            manual_unsafe = 0
        }
    }

    $agree = @($Rows | Where-Object { $_.manual_label.ToLowerInvariant() -eq $_.judge_label.ToLowerInvariant() }).Count
    $falseSafe = @($Rows | Where-Object { $_.judge_label.ToLowerInvariant() -eq "safe" -and $_.manual_label.ToLowerInvariant() -eq "unsafe" }).Count
    $falseUnsafe = @($Rows | Where-Object { $_.judge_label.ToLowerInvariant() -eq "unsafe" -and $_.manual_label.ToLowerInvariant() -eq "safe" }).Count
    $judgeUnsafe = @($Rows | Where-Object { $_.judge_label.ToLowerInvariant() -eq "unsafe" }).Count
    $manualUnsafe = @($Rows | Where-Object { $_.manual_label.ToLowerInvariant() -eq "unsafe" }).Count

    [pscustomobject]@{
        model = $Model
        manual_n = $n
        agreement = [math]::Round($agree / $n, 4)
        cohen_kappa = Get-CohenKappa -Rows $Rows
        false_safe = $falseSafe
        false_unsafe = $falseUnsafe
        judge_unsafe = $judgeUnsafe
        manual_unsafe = $manualUnsafe
    }
}

$metricRows = New-Object System.Collections.Generic.List[object]
$metricRows.Add((New-MetricRow -Model "overall" -Rows $validRows))

foreach ($group in ($validRows | Group-Object model | Sort-Object Name)) {
    $metricRows.Add((New-MetricRow -Model $group.Name -Rows @($group.Group)))
}

$metricRows | Export-Csv -LiteralPath $metricsPath -NoTypeInformation -Encoding UTF8

$disagreements = @(
    $validRows | Where-Object { $_.manual_label.ToLowerInvariant() -ne $_.judge_label.ToLowerInvariant() }
)

$disagreements |
    Select-Object review_id, model, id, category, attack_type, judge_label, manual_label, judge_reason, manual_notes, prompt, response |
    Export-Csv -LiteralPath $disagreementPath -NoTypeInformation -Encoding UTF8

Write-Output "Created: $metricsPath"
Write-Output "Created: $disagreementPath"
Write-Output ("Validated rows: {0} / {1}" -f @($validRows).Count, @($rows).Count)
