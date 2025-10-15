@echo off
echo ========================================
echo Laravel/PHP Files Backup and Cleanup
echo ========================================
echo.
echo This script will:
echo 1. Create a backup folder: laravel_backup/
echo 2. Move Laravel/PHP files to the backup folder
echo 3. Keep your Django backend and Vue.js frontend intact
echo.
echo You can delete the backup folder later if everything works fine.
echo.
set /p confirm="Continue? (yes/no): "

if /i not "%confirm%"=="yes" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Creating backup folder...
if not exist laravel_backup\ mkdir laravel_backup

echo Moving Laravel files to backup...

REM Move Laravel directories
if exist app\ (
    echo Moving app/...
    move app laravel_backup\ >nul 2>&1
)

if exist bootstrap\ (
    echo Moving bootstrap/...
    move bootstrap laravel_backup\ >nul 2>&1
)

if exist config\ (
    echo Moving config/...
    move config laravel_backup\ >nul 2>&1
)

if exist database\ (
    echo Moving database/...
    move database laravel_backup\ >nul 2>&1
)

if exist routes\ (
    echo Moving routes/...
    move routes laravel_backup\ >nul 2>&1
)

if exist storage\ (
    echo Moving storage/...
    move storage laravel_backup\ >nul 2>&1
)

if exist tests\ (
    echo Moving tests/...
    move tests laravel_backup\ >nul 2>&1
)

if exist vendor\ (
    echo Moving vendor/...
    move vendor laravel_backup\ >nul 2>&1
)

if exist backend\ (
    echo Moving backend/ (old backend folder)...
    move backend laravel_backup\ >nul 2>&1
)

REM Move Laravel files
if exist artisan (
    echo Moving artisan...
    move artisan laravel_backup\ >nul 2>&1
)

if exist composer.json (
    echo Moving composer.json...
    move composer.json laravel_backup\ >nul 2>&1
)

if exist composer.lock (
    echo Moving composer.lock...
    move composer.lock laravel_backup\ >nul 2>&1
)

if exist phpunit.xml (
    echo Moving phpunit.xml...
    move phpunit.xml laravel_backup\ >nul 2>&1
)

if exist .env (
    echo Moving .env (Laravel)...
    move .env laravel_backup\ >nul 2>&1
)

if exist .env.example (
    echo Moving .env.example (Laravel)...
    move .env.example laravel_backup\ >nul 2>&1
)

echo.
echo ========================================
echo Backup Complete!
echo ========================================
echo.
echo All Laravel files have been moved to: laravel_backup/
echo.
echo Your project structure is now clean:
echo   ✓ .be/ - Django backend
echo   ✓ resources/ - Vue.js frontend
echo   ✓ public/ - Public assets
echo   ✓ node_modules/ - Node dependencies
echo   ✓ Documentation files
echo.
echo If everything works fine, you can delete the laravel_backup/ folder.
echo.
pause
