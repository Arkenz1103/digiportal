# PowerShell Cleanup Script for Laravel Files
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Laravel/PHP Files Cleanup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create backup folder
$backupFolder = "laravel_backup"
if (-not (Test-Path $backupFolder)) {
    New-Item -ItemType Directory -Path $backupFolder | Out-Null
    Write-Host "✓ Created backup folder: $backupFolder" -ForegroundColor Green
}

# List of folders to move
$foldersToMove = @(
    "app",
    "bootstrap", 
    "config",
    "database",
    "routes",
    "storage",
    "tests",
    "vendor",
    "backend"
)

# List of files to move
$filesToMove = @(
    "artisan",
    "composer.json",
    "composer.lock",
    "phpunit.xml",
    ".env",
    ".env.example"
)

Write-Host "Moving Laravel folders..." -ForegroundColor Yellow
$count = 0
foreach ($folder in $foldersToMove) {
    if (Test-Path $folder) {
        $count++
        Write-Host "  [$count/$($foldersToMove.Count)] Moving $folder/" -ForegroundColor White
        Move-Item -Path $folder -Destination "$backupFolder\" -Force
    }
}

Write-Host ""
Write-Host "Moving Laravel files..." -ForegroundColor Yellow
$count = 0
foreach ($file in $filesToMove) {
    if (Test-Path $file) {
        $count++
        Write-Host "  [$count/$($filesToMove.Count)] Moving $file" -ForegroundColor White
        Move-Item -Path $file -Destination "$backupFolder\" -Force
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Cleanup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "All Laravel files moved to: $backupFolder/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your clean project structure:" -ForegroundColor White
Write-Host "  ✓ .be/ - Django backend" -ForegroundColor Green
Write-Host "  ✓ resources/ - Vue.js frontend" -ForegroundColor Green
Write-Host "  ✓ public/ - Public assets" -ForegroundColor Green
Write-Host "  ✓ Documentation files" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. cd .be" -ForegroundColor White
Write-Host "  2. venv\Scripts\activate" -ForegroundColor White
Write-Host "  3. python manage.py runserver" -ForegroundColor White
Write-Host ""
