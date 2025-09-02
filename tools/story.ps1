param(
    [string[]]$CH,      # Character names to search
    [string[]]$TH,      # Themes to search
    [string[]]$BE,      # Beats to search
    [string[]]$WO,      # World elements to search
    [string[]]$IN,      # Influences to search
    [string[]]$SL,      # Storylines to search
    [string[]]$search,  # General keyword search
    [switch]$recent,    # Show recent working files
    [string]$output     # Output file
)

# Ensure we're in the project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Helper function to ensure Python is available
function Test-Python {
    try {
        python --version | Out-Null
        return $true
    }
    catch {
        Write-Host "Python not found. Please install Python 3.8+" -ForegroundColor Red
        return $false
    }
}

# Show recent working files
if ($recent) {
    Write-Host "`nRecent working files:" -ForegroundColor Cyan
    Get-ChildItem -Path "." -Filter "*.md" | 
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 10 |
    Format-Table Name, LastWriteTime -AutoSize
    exit
}

# Run context retrieval
if (Test-Python) {
    # Ensure context directory exists
    if (!(Test-Path "context")) { 
        New-Item -ItemType Directory -Path "context" 
    }
    
    # Build Python command
    $timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
    $outputFile = if ($output) { $output } else { "context\context-$timestamp.md" }
    
    $pythonArgs = @()
    
    # Add type-specific searches
    if ($CH) { $pythonArgs += "-t", "CH", "-k", ($CH -join ",") }
    if ($TH) { $pythonArgs += "-t", "TH", "-k", ($TH -join ",") }
    if ($BE) { $pythonArgs += "-t", "BE", "-k", ($BE -join ",") }
    if ($WO) { $pythonArgs += "-t", "WO", "-k", ($WO -join ",") }
    if ($IN) { $pythonArgs += "-t", "IN", "-k", ($IN -join ",") }
    if ($SL) { $pythonArgs += "-t", "SL", "-k", ($SL -join ",") }
    
    # Or general search
    if ($search) { $pythonArgs += "-k", ($search -join ",") }
    
    $pythonArgs += "-o", $outputFile
    
    # Run retriever
    Write-Host "Retrieving context..." -ForegroundColor Cyan
    $cmd = "python tools\retriever.py $($pythonArgs -join ' ')"
    Invoke-Expression $cmd
    
    # Display result
    if (Test-Path $outputFile) {
        Write-Host "`nContext saved to: $outputFile" -ForegroundColor Green
        
        # Show preview
        Get-Content $outputFile | Select-Object -First 30
        Write-Host "`n... (preview - full context in $outputFile)" -ForegroundColor Gray
    }
}
else {
    Write-Host "Please install Python to use context retrieval" -ForegroundColor Red
}
