# File: add_large_files_to_gitignore.ps1
# This script finds files larger than 99MB and adds them to .gitignore

# Get the .gitignore file path
$gitignorePath = ".\.gitignore"

# Find all files larger than 99MB
$largeFiles = Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 99MB }

# Check if there are any large files
if ($largeFiles.Count -eq 0) {
    Write-Host "No files larger than 99MB found."
    exit
}

# Check if .gitignore exists, create it if not
if (-not (Test-Path $gitignorePath)) {
    New-Item -Path $gitignorePath -ItemType File
}

# Read the existing .gitignore content
$existingEntries = Get-Content $gitignorePath

# Append large file paths to .gitignore, avoiding duplicates
foreach ($file in $largeFiles) {
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
    if (-not ($existingEntries -contains $relativePath)) {
        Add-Content -Path $gitignorePath -Value $relativePath
        Write-Host "Added $relativePath to .gitignore"
    } else {
        Write-Host "$relativePath already exists in .gitignore"
    }
}

Write-Host "All large files have been processed."
