param(
    [string[]]$CH,      # Character names to search
    [string[]]$TH,      # Themes to search
    [string[]]$BE,      # Beats to search
    [string[]]$WO,      # World elements to search
    [string[]]$IN,      # Influences to search
    [string[]]$SL,      # Storylines to search
    [string[]]$search,  # General keyword search
    [switch]$recent,    # Show recent files in root
    [string]$output     # Output file
)

# Ensure we're in the project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Show recent working files (in root)
if ($recent) {
    Write-Host "`nRecent working files (root):" -ForegroundColor Cyan
    Get-ChildItem -Path "." -Filter "*-*.md" -File | 
    Where-Object { $_.Name -match "^(CH|TH|BE|WO|IN|SL)-" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 10 |
    Format-Table Name, LastWriteTime -AutoSize
    exit
}

# Build Python command
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
$outputFile = if ($output) { $output } else { "context\context-$timestamp.md" }

# Ensure context directory exists
if (!(Test-Path "context")) { 
    New-Item -ItemType Directory -Path "context" | Out-Null
}

# Build arguments
$cmd = "python tools\retriever.py"

# Handle different search types
if ($CH -or $TH -or $BE -or $WO -or $IN -or $SL) {
    # Type-specific searches
    $types = @()
    $keywords = @()
    
    if ($CH) { $types += "CH"; $keywords += $CH }
    if ($TH) { $types += "TH"; $keywords += $TH }
    if ($BE) { $types += "BE"; $keywords += $BE }
    if ($WO) { $types += "WO"; $keywords += $WO }
    if ($IN) { $types += "IN"; $keywords += $IN }
    if ($SL) { $types += "SL"; $keywords += $SL }
    
    if ($types) { $cmd += " -t " + ($types -join ",") }
    if ($keywords) { $cmd += " -k " + ($keywords -join ",") }
}
elseif ($search) {
    # General search
    $cmd += " -k " + ($search -join ",")
}
else {
    Write-Host "Please specify what to search for:" -ForegroundColor Yellow
    Write-Host "  -CH dolores         # Search for character"
    Write-Host "  -TH consciousness   # Search for theme"
    Write-Host "  -search 'maze'      # General search"
    Write-Host "  -recent             # Show recent files"
    exit
}

$cmd += " -o `"$outputFile`""

# Run retriever
Write-Host "Searching..." -ForegroundColor Cyan
Invoke-Expression $cmd

# Display result
if (Test-Path $outputFile) {
    Write-Host "`nContext saved to: $outputFile" -ForegroundColor Green
    
    # Show preview
    $content = Get-Content $outputFile -Raw
    $lines = $content -split "`n" | Select-Object -First 30
    $lines -join "`n"
    
    if (($content -split "`n").Count -gt 30) {
        Write-Host "`n... (full context in $outputFile)" -ForegroundColor Gray
    }
}
