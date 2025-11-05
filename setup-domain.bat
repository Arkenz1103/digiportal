@echo off
echo ========================================
echo DigiPortal - Custom Domain Setup
echo ========================================
echo.
echo This script will add 'digiportal.local' to your hosts file
echo You need to run this as Administrator
echo.
pause

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo Adding digiport.ph to hosts file...
echo.

REM Backup hosts file first
copy C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.backup

REM Check if entry already exists
findstr /C:"digiport.ph" C:\Windows\System32\drivers\etc\hosts >nul
if %errorLevel% equ 0 (
    echo digiport.ph already exists in hosts file!
    echo Skipping...
) else (
    REM Add the entry
    echo 127.0.0.1    digiport.ph >> C:\Windows\System32\drivers\etc\hosts
    echo 127.0.0.1    www.digiport.ph >> C:\Windows\System32\drivers\etc\hosts
    echo 127.0.0.1    api.digiport.ph >> C:\Windows\System32\drivers\etc\hosts
    echo.
    echo SUCCESS! Added digiport.ph to hosts file
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now access DigiPortal at:
echo   http://digiport.ph:5173
echo.
echo Make sure to restart your dev server:
echo   1. Stop current server (Ctrl+C)
echo   2. Run: npm run dev
echo   3. Open: http://digiport.ph:5173
echo.
pause
