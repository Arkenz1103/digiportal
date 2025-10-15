@echo off
echo ========================================
echo Laravel/PHP Files Cleanup Script
echo ========================================
echo.
echo This will DELETE the following Laravel/PHP files and folders:
echo.
echo FOLDERS:
echo   - app/
echo   - bootstrap/
echo   - config/
echo   - database/
echo   - routes/
echo   - storage/
echo   - tests/
echo   - vendor/
echo   - backend/ (old backend folder)
echo.
echo FILES:
echo   - artisan
echo   - composer.json
echo   - composer.lock
echo   - phpunit.xml
echo   - .env (Laravel env file)
echo   - .env.example (Laravel env example)
echo.
echo KEEPING:
echo   - .be/ (Django backend)
echo   - resources/ (Vue.js frontend)
echo   - public/ (public assets)
echo   - node_modules/
echo   - package.json
echo   - vite.config.js
echo   - tailwind.config.js
echo   - All documentation files
echo.
echo ========================================
set /p confirm="Are you sure you want to continue? (yes/no): "

if /i not "%confirm%"=="yes" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup...
echo.

REM Remove Laravel directories
if exist app\ (
    echo Removing app/...
    rmdir /s /q app
)

if exist bootstrap\ (
    echo Removing bootstrap/...
    rmdir /s /q bootstrap
)

if exist config\ (
    echo Removing config/...
    rmdir /s /q config
)

if exist database\ (
    echo Removing database/...
    rmdir /s /q database
)

if exist routes\ (
    echo Removing routes/...
    rmdir /s /q routes
)

if exist storage\ (
    echo Removing storage/...
    rmdir /s /q storage
)

if exist tests\ (
    echo Removing tests/...
    rmdir /s /q tests
)

if exist vendor\ (
    echo Removing vendor/...
    rmdir /s /q vendor
)

if exist backend\ (
    echo Removing backend/ (old backend folder)...
    rmdir /s /q backend
)

REM Remove Laravel files
if exist artisan (
    echo Removing artisan...
    del /q artisan
)

if exist composer.json (
    echo Removing composer.json...
    del /q composer.json
)

if exist composer.lock (
    echo Removing composer.lock...
    del /q composer.lock
)

if exist phpunit.xml (
    echo Removing phpunit.xml...
    del /q phpunit.xml
)

if exist .env (
    echo Removing .env (Laravel)...
    del /q .env
)

if exist .env.example (
    echo Removing .env.example (Laravel)...
    del /q .env.example
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Removed Laravel/PHP files successfully.
echo Your Django backend is in the .be/ folder.
echo.
echo Next steps:
echo 1. cd .be
echo 2. venv\Scripts\activate
echo 3. python manage.py runserver
echo.
pause
