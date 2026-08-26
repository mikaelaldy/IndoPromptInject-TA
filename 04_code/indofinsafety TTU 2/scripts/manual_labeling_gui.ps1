$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$samplePath = Join-Path $root "outputs\manual_validation_stratified_sample.csv"
$metricsScript = Join-Path $root "scripts\calculate_manual_validation_metrics.ps1"
$augmentedPromptPath = Join-Path $root "data\augmented_prompts_v1_200.json"

if (-not (Test-Path -LiteralPath $samplePath)) {
    [System.Windows.Forms.MessageBox]::Show("Missing sample file:`n$samplePath", "File not found", "OK", "Error") | Out-Null
    exit 1
}

$script:rows = @(Import-Csv -LiteralPath $samplePath)
$script:promptById = @{}
if (Test-Path -LiteralPath $augmentedPromptPath) {
    $augmentedPrompts = Get-Content -LiteralPath $augmentedPromptPath -Raw | ConvertFrom-Json
    foreach ($item in $augmentedPrompts) {
        $script:promptById[[string]$item.id] = [string]$item.prompt
    }
}
$script:filtered = @()
$script:position = 0
$script:currentIndex = $null
$script:fieldNames = @(
    "review_id", "model", "id", "source", "category", "attack_type", "prompt", "response",
    "judge_label", "judge_reason", "judge_confidence", "manual_label", "manual_notes", "manual_is_valid"
)

function Save-AllRows {
    $script:rows | Select-Object $script:fieldNames | Export-Csv -LiteralPath $samplePath -NoTypeInformation -Encoding UTF8
    Update-Status "Saved"
}

function Save-CurrentRow {
    if ($null -eq $script:currentIndex) { return }
    Store-Current
    $row = $script:rows[$script:currentIndex]
    if ($row.manual_label -eq "safe" -or $row.manual_label -eq "unsafe") {
        $row.manual_is_valid = "True"
    }
    Save-AllRows
}

function Store-Current {
    if ($null -eq $script:currentIndex) { return }
    $row = $script:rows[$script:currentIndex]
    if ($radioSafe.Checked) {
        $row.manual_label = "safe"
    } elseif ($radioUnsafe.Checked) {
        $row.manual_label = "unsafe"
    } else {
        $row.manual_label = ""
    }
    $row.manual_notes = $notesBox.Text.Trim()
}

function Get-ProgressText {
    $reviewed = @($script:rows | Where-Object { $_.manual_is_valid -eq "True" }).Count
    $total = @($script:rows).Count
    $shown = @($script:filtered).Count
    $pos = if ($shown -gt 0) { $script:position + 1 } else { 0 }
    return "Reviewed $reviewed/$total | Showing $pos/$shown"
}

function Update-Status {
    param([string]$suffix = "")
    $text = Get-ProgressText
    if ($suffix) { $text = "$text | $suffix" }
    $statusLabel.Text = $text
}

function Set-TextBox {
    param(
        $Box,
        [string]$Text
    )
    $Box.Text = if ($Text) { $Text } else { "" }
    $Box.SelectionStart = 0
    $Box.SelectionLength = 0
    $Box.ScrollToCaret()
}

function Get-AttackPrompt {
    param($Row)
    $id = [string]$Row.id
    if ($script:promptById.ContainsKey($id) -and $script:promptById[$id]) {
        return $script:promptById[$id]
    }
    return [string]$Row.prompt
}

function Apply-Filter {
    Store-Current
    $mode = [string]$filterBox.SelectedItem
    $query = $searchBox.Text.Trim().ToLowerInvariant()
    $indices = New-Object System.Collections.Generic.List[int]

    for ($i = 0; $i -lt $script:rows.Count; $i++) {
        $row = $script:rows[$i]
        $manualValid = ([string]$row.manual_is_valid).Trim().ToLowerInvariant() -eq "true"
        $judgeValue = ([string]$row.judge_label).Trim().ToLowerInvariant()
        $manualLabel = ([string]$row.manual_label).Trim().ToLowerInvariant()

        if ($mode -eq "Unreviewed" -and $manualValid) { continue }
        if ($mode -eq "Reviewed" -and -not $manualValid) { continue }
        if ($mode -eq "Judge safe" -and $judgeValue -ne "safe") { continue }
        if ($mode -eq "Judge unsafe" -and $judgeValue -ne "unsafe") { continue }
        if ($mode -eq "Disagreements" -and (-not $manualValid -or $judgeValue -eq $manualLabel)) { continue }

        $haystack = @(
            $row.review_id, $row.model, $row.id, $row.category, $row.attack_type, $row.prompt, $row.response
        ) -join " "
        if ($query -and -not $haystack.ToLowerInvariant().Contains($query)) { continue }
        $indices.Add($i)
    }

    $script:filtered = @($indices)
    $script:position = 0
    Show-Current
}

function Show-Current {
    if (@($script:filtered).Count -eq 0) {
        $script:currentIndex = $null
        $metaLabel.Text = "No rows match the current filter."
        $judgeStatusLabel.Text = ""
        Set-TextBox $promptBox ""
        Set-TextBox $responseBox ""
        Set-TextBox $judgeReasonBox ""
        $notesBox.Text = ""
        $radioSafe.Checked = $false
        $radioUnsafe.Checked = $false
        $radioUnlabeled.Checked = $true
        Update-Status
        return
    }

    if ($script:position -lt 0) { $script:position = 0 }
    if ($script:position -ge $script:filtered.Count) { $script:position = $script:filtered.Count - 1 }

    $script:currentIndex = $script:filtered[$script:position]
    $row = $script:rows[$script:currentIndex]

    $attackPrompt = Get-AttackPrompt $row
    $metaLabel.Text = "$($row.review_id) | $($row.model) | $($row.id) | $($row.category) | $($row.attack_type)"
    $judgeStatusLabel.Text = "Judge: $($row.judge_label) | confidence: $($row.judge_confidence) | Manual: $(if ($row.manual_label) { $row.manual_label } else { '-' }) | valid: $($row.manual_is_valid)"

    $promptPreviewLabel.Text = "Attack prompt: $attackPrompt"
    Set-TextBox $promptBox $attackPrompt
    Set-TextBox $responseBox $row.response
    Set-TextBox $judgeReasonBox $row.judge_reason
    $notesBox.Text = if ($row.manual_notes) { $row.manual_notes } else { "" }

    $radioSafe.Checked = $false
    $radioUnsafe.Checked = $false
    $radioUnlabeled.Checked = $false
    switch (([string]$row.manual_label).Trim().ToLowerInvariant()) {
        "safe" { $radioSafe.Checked = $true }
        "unsafe" { $radioUnsafe.Checked = $true }
        default { $radioUnlabeled.Checked = $true }
    }

    Update-Status
}

function Move-Next {
    Store-Current
    if ($script:position -lt @($script:filtered).Count - 1) {
        $script:position++
    }
    Show-Current
}

function Advance-AfterLabel {
    if ($script:position -lt @($script:filtered).Count - 1) {
        $script:position++
    }
    Show-Current
}

function Move-Prev {
    Store-Current
    if ($script:position -gt 0) {
        $script:position--
    }
    Show-Current
}

function Label-Current {
    param([string]$Label)
    if ($null -eq $script:currentIndex) { return }
    $row = $script:rows[$script:currentIndex]
    $row.manual_label = $Label
    $row.manual_notes = $notesBox.Text.Trim()
    $row.manual_is_valid = "True"
    Save-AllRows
    Advance-AfterLabel
}

function Skip-Current {
    if ($null -eq $script:currentIndex) { return }
    Store-Current
    Save-AllRows
    Move-Next
}

function Get-CurrentAttackPrompt {
    if ($null -eq $script:currentIndex) { return "" }
    return Get-AttackPrompt $script:rows[$script:currentIndex]
}

function Show-FullPrompt {
    $attackPrompt = Get-CurrentAttackPrompt
    if (-not $attackPrompt) { return }
    [System.Windows.Forms.MessageBox]::Show($attackPrompt, "Full Attack Prompt", "OK", "Information") | Out-Null
}

function Copy-FullPrompt {
    $attackPrompt = Get-CurrentAttackPrompt
    if (-not $attackPrompt) { return }
    [System.Windows.Forms.Clipboard]::SetText($attackPrompt)
    Update-Status "Prompt copied"
}

function Run-Metrics {
    Save-AllRows
    if (-not (Test-Path -LiteralPath $metricsScript)) {
        [System.Windows.Forms.MessageBox]::Show("Missing metrics script:`n$metricsScript", "Metrics", "OK", "Warning") | Out-Null
        return
    }
    $output = & powershell -NoProfile -ExecutionPolicy Bypass -File $metricsScript 2>&1
    [System.Windows.Forms.MessageBox]::Show(($output -join "`n"), "Saved + Metrics", "OK", "Information") | Out-Null
}

$form = New-Object System.Windows.Forms.Form
$form.Text = "IndoFinSafety Manual Validation"
$form.Size = New-Object System.Drawing.Size(1180, 780)
$form.MinimumSize = New-Object System.Drawing.Size(980, 640)
$form.StartPosition = "CenterScreen"
$form.KeyPreview = $true

$topPanel = New-Object System.Windows.Forms.Panel
$topPanel.Dock = "Top"
$topPanel.Height = 54
$form.Controls.Add($topPanel)

$filterLabel = New-Object System.Windows.Forms.Label
$filterLabel.Text = "Filter"
$filterLabel.Location = New-Object System.Drawing.Point(12, 18)
$filterLabel.AutoSize = $true
$topPanel.Controls.Add($filterLabel)

$filterBox = New-Object System.Windows.Forms.ComboBox
$filterBox.DropDownStyle = "DropDownList"
$filterBox.Items.AddRange(@("All", "Unreviewed", "Reviewed", "Judge safe", "Judge unsafe", "Disagreements"))
$filterBox.SelectedItem = "Unreviewed"
$filterBox.Location = New-Object System.Drawing.Point(52, 14)
$filterBox.Width = 150
$topPanel.Controls.Add($filterBox)

$searchLabel = New-Object System.Windows.Forms.Label
$searchLabel.Text = "Search"
$searchLabel.Location = New-Object System.Drawing.Point(218, 18)
$searchLabel.AutoSize = $true
$topPanel.Controls.Add($searchLabel)

$searchBox = New-Object System.Windows.Forms.TextBox
$searchBox.Location = New-Object System.Drawing.Point(268, 14)
$searchBox.Width = 220
$topPanel.Controls.Add($searchBox)

$applyButton = New-Object System.Windows.Forms.Button
$applyButton.Text = "Apply"
$applyButton.Location = New-Object System.Drawing.Point(498, 12)
$applyButton.Width = 70
$topPanel.Controls.Add($applyButton)

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Anchor = "Top,Right"
$statusLabel.TextAlign = "MiddleRight"
$statusLabel.Location = New-Object System.Drawing.Point(790, 18)
$statusLabel.Size = New-Object System.Drawing.Size(360, 20)
$topPanel.Controls.Add($statusLabel)

$metaPanel = New-Object System.Windows.Forms.Panel
$metaPanel.Dock = "Top"
$metaPanel.Height = 104
$form.Controls.Add($metaPanel)

$metaLabel = New-Object System.Windows.Forms.Label
$metaLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$metaLabel.Location = New-Object System.Drawing.Point(12, 6)
$metaLabel.Size = New-Object System.Drawing.Size(1120, 22)
$metaPanel.Controls.Add($metaLabel)

$judgeStatusLabel = New-Object System.Windows.Forms.Label
$judgeStatusLabel.Location = New-Object System.Drawing.Point(12, 32)
$judgeStatusLabel.Size = New-Object System.Drawing.Size(1120, 20)
$metaPanel.Controls.Add($judgeStatusLabel)

$promptPreviewLabel = New-Object System.Windows.Forms.Label
$promptPreviewLabel.Location = New-Object System.Drawing.Point(12, 56)
$promptPreviewLabel.Size = New-Object System.Drawing.Size(1120, 44)
$promptPreviewLabel.AutoEllipsis = $false
$promptPreviewLabel.ForeColor = [System.Drawing.Color]::DarkRed
$metaPanel.Controls.Add($promptPreviewLabel)

$mainSplit = New-Object System.Windows.Forms.SplitContainer
$mainSplit.Dock = "Fill"
$mainSplit.SplitterDistance = 570
$mainSplit.Panel1.Padding = New-Object System.Windows.Forms.Padding(12, 0, 6, 8)
$mainSplit.Panel2.Padding = New-Object System.Windows.Forms.Padding(6, 0, 12, 8)
$form.Controls.Add($mainSplit)

function New-LabeledTextBox {
    param(
        [string]$Title,
        [bool]$ReadOnly = $true,
        [bool]$Rich = $false
    )
    $group = New-Object System.Windows.Forms.GroupBox
    $group.Text = $Title
    $group.Dock = "Fill"
    $group.Padding = New-Object System.Windows.Forms.Padding(8)

    if ($Rich) {
        $box = New-Object System.Windows.Forms.RichTextBox
        $box.BorderStyle = "FixedSingle"
        $box.DetectUrls = $false
    } else {
        $box = New-Object System.Windows.Forms.TextBox
        $box.Multiline = $true
    }
    $box.ScrollBars = "Vertical"
    $box.WordWrap = $true
    $box.ReadOnly = $ReadOnly
    $box.Dock = "Fill"
    $box.Font = New-Object System.Drawing.Font("Segoe UI", 10)
    $group.Controls.Add($box)

    return @($group, $box)
}

$leftLayout = New-Object System.Windows.Forms.TableLayoutPanel
$leftLayout.Dock = "Fill"
$leftLayout.RowCount = 2
$leftLayout.ColumnCount = 1
$leftLayout.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 24))) | Out-Null
$leftLayout.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 76))) | Out-Null
$mainSplit.Panel1.Controls.Add($leftLayout)

$promptControls = New-LabeledTextBox "Attack Prompt Sent to Model" $true $true
$promptBox = $promptControls[1]
$promptBox.BackColor = [System.Drawing.Color]::FromArgb(255, 252, 232)
$promptBox.ForeColor = [System.Drawing.Color]::Black
$promptBox.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$leftLayout.Controls.Add($promptControls[0], 0, 0)

$responseControls = New-LabeledTextBox "Model Response" $true
$responseBox = $responseControls[1]
$leftLayout.Controls.Add($responseControls[0], 0, 1)

$rightLayout = New-Object System.Windows.Forms.TableLayoutPanel
$rightLayout.Dock = "Fill"
$rightLayout.RowCount = 3
$rightLayout.ColumnCount = 1
$rightLayout.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 38))) | Out-Null
$rightLayout.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 42))) | Out-Null
$rightLayout.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Absolute, 88))) | Out-Null
$mainSplit.Panel2.Controls.Add($rightLayout)

$judgeControls = New-LabeledTextBox "Judge Reason" $true
$judgeReasonBox = $judgeControls[1]
$rightLayout.Controls.Add($judgeControls[0], 0, 0)

$notesControls = New-LabeledTextBox "Manual Notes" $false
$notesBox = $notesControls[1]
$rightLayout.Controls.Add($notesControls[0], 0, 1)

$decisionGroup = New-Object System.Windows.Forms.GroupBox
$decisionGroup.Text = "Manual Label"
$decisionGroup.Dock = "Fill"
$rightLayout.Controls.Add($decisionGroup, 0, 2)

$radioSafe = New-Object System.Windows.Forms.RadioButton
$radioSafe.Text = "Safe"
$radioSafe.Location = New-Object System.Drawing.Point(14, 30)
$decisionGroup.Controls.Add($radioSafe)

$radioUnsafe = New-Object System.Windows.Forms.RadioButton
$radioUnsafe.Text = "Unsafe"
$radioUnsafe.Location = New-Object System.Drawing.Point(118, 30)
$decisionGroup.Controls.Add($radioUnsafe)

$radioUnlabeled = New-Object System.Windows.Forms.RadioButton
$radioUnlabeled.Text = "Unlabeled"
$radioUnlabeled.Location = New-Object System.Drawing.Point(240, 30)
$decisionGroup.Controls.Add($radioUnlabeled)

$bottomPanel = New-Object System.Windows.Forms.Panel
$bottomPanel.Dock = "Bottom"
$bottomPanel.Height = 58
$form.Controls.Add($bottomPanel)

$script:x = 12
function Add-BottomButton {
    param(
        [string]$Text,
        [scriptblock]$Action,
        [int]$Width = 86
    )
    $button = New-Object System.Windows.Forms.Button
    $button.Text = $Text
    $button.Location = New-Object System.Drawing.Point($script:x, 14)
    $button.Width = $Width
    $button.Add_Click($Action)
    $bottomPanel.Controls.Add($button)
    $script:x += $Width + 8
}

Add-BottomButton "Prev" { Move-Prev } 72
Add-BottomButton "Next" { Move-Next } 72
Add-BottomButton "Safe" { Label-Current "safe" } 76
Add-BottomButton "Unsafe" { Label-Current "unsafe" } 82
Add-BottomButton "Skip" { Skip-Current } 76
Add-BottomButton "Save" { Save-CurrentRow } 76
Add-BottomButton "Show Prompt" { Show-FullPrompt } 104
Add-BottomButton "Copy Prompt" { Copy-FullPrompt } 104
Add-BottomButton "Save + Metrics" { Run-Metrics } 118
Add-BottomButton "Open CSV Folder" { Start-Process explorer.exe (Split-Path -Parent $samplePath) } 130

$shortcutLabel = New-Object System.Windows.Forms.Label
$shortcutLabel.Anchor = "Top,Right"
$shortcutLabel.Text = "Shortcuts: S safe, U unsafe, K skip, Ctrl+S save, Left/Right navigate"
$shortcutLabel.TextAlign = "MiddleRight"
$shortcutLabel.Location = New-Object System.Drawing.Point(760, 20)
$shortcutLabel.Size = New-Object System.Drawing.Size(390, 20)
$bottomPanel.Controls.Add($shortcutLabel)

$applyButton.Add_Click({ Apply-Filter })
$filterBox.Add_SelectedIndexChanged({ Apply-Filter })
$searchBox.Add_KeyDown({
    param($sender, $e)
    if ($e.KeyCode -eq "Enter") {
        Apply-Filter
        $e.SuppressKeyPress = $true
    }
})

$form.Add_KeyDown({
    param($sender, $e)
    if ($e.Control -and $e.KeyCode -eq "S") {
        Save-AllRows
        $e.SuppressKeyPress = $true
        return
    }
    if ($notesBox.Focused -or $searchBox.Focused) { return }
    switch ($e.KeyCode) {
        "S" { Label-Current "safe"; $e.SuppressKeyPress = $true }
        "U" { Label-Current "unsafe"; $e.SuppressKeyPress = $true }
        "K" { Skip-Current; $e.SuppressKeyPress = $true }
        "Left" { Move-Prev; $e.SuppressKeyPress = $true }
        "Right" { Move-Next; $e.SuppressKeyPress = $true }
    }
})

$form.Add_FormClosing({
    Store-Current
    Save-AllRows
})

Apply-Filter
[void]$form.ShowDialog()
