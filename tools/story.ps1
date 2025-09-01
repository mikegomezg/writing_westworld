param(
    [string]$query = "",
    [string]$types = "",
    [string]$keywords = "",
    [string]$storyline = "",
    [string]$format = "markdown",
    [switch]$list,
    [switch]$storylines,
    [string]$canonize = "",
    [string]$deactivate = "",
    [switch]$recent,
    [int]$days = 7,
    [switch]$generate
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
    } catch {
        Write-Host "Python not found. Please install Python 3.8+" -ForegroundColor Red
        return $false
    }
}

# List storylines
if ($storylines) {
    Write-Host "`nStorylines:" -ForegroundColor Cyan
    Get-ChildItem -Path "canon\storylines" -Filter "SL-*.md" -ErrorAction SilentlyContinue | 
        ForEach-Object {
            Write-Host "  $($_.BaseName)" -ForegroundColor Yellow
            $content = Get-Content $_.FullName | Select-Object -Skip 6 -First 3
            $content | ForEach-Object { Write-Host "    $_" }
        }
    exit
}

# List files by type
if ($list) {
    if ($types) {
        Get-ChildItem -Filter "$types-*.md" -Recurse | 
            Select-Object Name, Directory, LastWriteTime |
            Format-Table -AutoSize
    } else {
        Get-ChildItem -Filter "*.md" -Recurse | 
            Where-Object { $_.Name -match '^(CH|WO|TH|BE|IN|SL)-' } |
            Select-Object @{Name="Type";Expression={$_.Name.Substring(0,2)}}, Name, Directory, LastWriteTime |
            Sort-Object Type, Name |
            Format-Table -AutoSize
    }
    exit
}

# Canonize a file
if ($canonize) {
    if (Test-Path $canonize) {
        $fileName = Split-Path -Leaf $canonize
        
        # Determine target directory
        $targetDir = "canon"
        if ($fileName.StartsWith("SL-")) {
            $targetDir = "canon\storylines"
        }
        
        # Ensure directory exists
        if (!(Test-Path $targetDir)) { 
            New-Item -ItemType Directory -Path $targetDir -Force
        }
        
        # Move file
        Move-Item $canonize "$targetDir\" -Force
        Write-Host "Moved $canonize to $targetDir/" -ForegroundColor Green
        
        # Git commit
        git add .
        git commit -m "canon: $fileName"
    } else {
        Write-Host "File not found: $canonize" -ForegroundColor Red
    }
    exit
}

# Deactivate a file
if ($deactivate) {
    if (Test-Path $deactivate) {
        if (!(Test-Path "inactive")) { 
            New-Item -ItemType Directory -Path "inactive" 
        }
        $fileName = Split-Path -Leaf $deactivate
        Move-Item $deactivate "inactive/" -Force
        Write-Host "Moved $deactivate to inactive/" -ForegroundColor Yellow
        git add .
        git commit -m "inactive: $fileName"
    } else {
        Write-Host "File not found: $deactivate" -ForegroundColor Red
    }
    exit
}

# Show recent changes
if ($recent) {
    Write-Host "`nRecent commits (last $days days):" -ForegroundColor Cyan
    git log --oneline --since="$days days ago" | Select-Object -First 10
    
    Write-Host "`nRecently modified files:" -ForegroundColor Cyan
    Get-ChildItem -Filter "*.md" -Recurse | 
        Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-$days) } |
        Select-Object Name, Directory, LastWriteTime |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 10 |
        Format-Table -AutoSize
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
    $outputFile = "context\context-$timestamp.md"
    
    $pythonArgs = @()
    if ($query) { $pythonArgs += "-q", "`"$query`"" }
    if ($types) { $pythonArgs += "-t", $types }
    if ($keywords) { $pythonArgs += "-k", "`"$keywords`"" }
    if ($storyline) { $pythonArgs += "-s", $storyline }
    $pythonArgs += "-f", $format
    $pythonArgs += "-o", $outputFile
    
    # Run retriever
    Write-Host "Retrieving context..." -ForegroundColor Cyan
    $cmd = "python tools\retriever.py $($pythonArgs -join ' ')"
    Invoke-Expression $cmd
    
    # Display result
    if (Test-Path $outputFile) {
        Write-Host "`nContext saved to: $outputFile" -ForegroundColor Green
        
        if ($generate) {
            Write-Host "`nContext retrieved. Copied to clipboard for AI tool." -ForegroundColor Yellow
            Get-Content $outputFile | Set-Clipboard
            Write-Host "Ready to paste into AI!" -ForegroundColor Green
        } else {
            # Show preview
            Get-Content $outputFile | Select-Object -First 30
            Write-Host "`n... (preview - full context in $outputFile)" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "Please install Python to use context retrieval" -ForegroundColor Red
}
