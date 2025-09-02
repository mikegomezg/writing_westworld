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

# Build combined search - accumulate all searches
$allTypes = @()
$allKeywords = @()

# Collect all specified searches
if ($CH) { 
    $allTypes += "CH"
    $allKeywords += $CH
}
if ($TH) { 
    $allTypes += "TH"
    $allKeywords += $TH
}
if ($BE) { 
    $allTypes += "BE"
    $allKeywords += $BE
}
if ($WO) { 
    $allTypes += "WO"
    $allKeywords += $WO
}
if ($IN) { 
    $allTypes += "IN"
    $allKeywords += $IN
}
if ($SL) { 
    $allTypes += "SL"
    $allKeywords += $SL
}

# Add general search keywords
if ($search) {
    $allKeywords += $search
}

# Build command
$cmd = "python tools\retriever.py"

# Add parameters if we have any searches
if ($allTypes.Count -gt 0 -or $allKeywords.Count -gt 0) {
    if ($allTypes.Count -gt 0) {
        $cmd += " -t `"$($allTypes -join ',')`""
    }
    if ($allKeywords.Count -gt 0) {
        $cmd += " -k `"$($allKeywords -join ',')`""
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
}
else {
    Write-Host "Please specify what to search for:" -ForegroundColor Yellow
    Write-Host "  -CH dolores bernard    # Search for characters"
    Write-Host "  -TH consciousness      # Search for themes"
    Write-Host "  -BE awakening          # Search for beats"
    Write-Host "  -search 'maze'         # General search"
    Write-Host "  -recent                # Show recent files"
    Write-Host ""
    Write-Host "You can combine searches:" -ForegroundColor Cyan
    Write-Host "  .\tools\story.ps1 -CH dolores -TH consciousness -BE fly"
}
