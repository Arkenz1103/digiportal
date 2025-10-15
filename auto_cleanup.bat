@echo off
echo ========================================
echo Auto Cleanup - Moving Laravel files...
echo ========================================
echo.

REM Create backup folder
if not exist laravel_backup\ mkdir laravel_backup

echo Moving Laravel files to laravel_backup/...
echo.

REM Move Laravel directories
if exist app\ (
    echo [1/15] Moving app/...
    move app laravel_backup\ >nul 2>&1
)

if exist bootstrap\ (
    echo [2/15] Moving bootstrap/...
    move bootstrap laravel_backup\ >nul 2>&1
)

if exist config\ (
    echo [3/15] Moving config/...
    move config laravel_backup\ >nul 2>&1
)

if exist database\ (
    echo [4/15] Moving database/...
    move database laravel_backup\ >nul 2>&1
)

if exist routes\ (
    echo [5/15] Moving routes/...
    move routes laravel_backup\ >nul 2>&1
)

if exist storage\ (
    echo [6/15] Moving storage/...
    move storage laravel_backup\ >nul 2>&1
)

if exist tests\ (
    echo [7/15] Moving tests/...
    move tests laravel_backup\ >nul 2>&1
)

if exist vendor\ (
    echo [8/15] Moving vendor/...
    move vendor laravel_backup\ >nul 2>&1
)

if exist backend\ (
    echo [9/15] Moving backend/...
    move backend laravel_backup\ >nul 2>&1
)

REM Move Laravel files
if exist artisan (
    echo [10/15] Moving artisan...
    move artisan laravel_backup\ >nul 2>&1
)

if exist composer.json (
    echo [11/15] Moving composer.json...
    move composer.json laravel_backup\ >nul 2>&1
)

if exist composer.lock (
    echo [12/15] Moving composer.lock...
    move composer.lock laravel_backup\ >nul 2>&1
)

if exist phpunit.xml (
    echo [13/15] Moving phpunit.xml...
    move phpunit.xml laravel_backup\ >nul 2>&1
)

if exist .env (
    echo [14/15] Moving .env...
    move .env laravel_backup\ >nul 2>&1
)

if exist .env.example (
    echo [15/15] Moving .env.example...
    move .env.example laravel_backup\ >nul 2>&1
)

echo.
echo ========================================
echo ✅ Cleanup Complete!
echo ========================================
echo.
echo All Laravel files moved to: laravel_backup/
echo.
echo Your clean project structure:
echo   ✓ .be/ - Django backend
echo   ✓ resources/ - Vue.js frontend  
echo   ✓ public/ - Public assets
echo   ✓ Documentation files
echo.
echo Next: Test your Django backend!
echo   cd .be
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
