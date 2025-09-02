param(
    [Parameter(Mandatory = $true)]
    [string]$file
)

$content = Get-Content $file -Raw

# Simple logic to suggest type based on content
$suggestions = @()

if ($content -match "character|personality|traits|goals") {
    $suggestions += "CH-"
}
if ($content -match "consciousness|reality|theme|concept") {
    $suggestions += "TH-"
}
if ($content -match "scene|moment|happens|event") {
    $suggestions += "BE-"
}
if ($content -match "world|setting|location|place") {
    $suggestions += "WO-"
}
if ($content -match "influence|inspiration|reference|source") {
    $suggestions += "IN-"
}
if ($content -match "storyline|arc|journey|path") {
    $suggestions += "SL-"
}

# Skip frontmatter and find first header
$lines = $content -split "`n"
$header = ""
foreach ($line in $lines) {
    if ($line -match "^#\s+(.+)$") {
        $header = $matches[1]
        break
    }
}

if ($header) {
    $title = $header.ToLower() -replace '\s+', '-'
    foreach ($prefix in $suggestions) {
        Write-Host "$prefix$title.md"
    }
}
else {
    # Fallback: suggest based on content keywords
    $words = $content -split '\s+' | Where-Object { $_.Length -gt 3 } | Select-Object -First 3
    $name = ($words -join '-').ToLower()
    foreach ($prefix in $suggestions) {
        Write-Host "$prefix$name.md"
    }
}
