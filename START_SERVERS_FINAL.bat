@echo off
cls
echo ========================================
echo   DigiPortal - Django + Vue.js
echo ========================================
echo.
echo Starting both servers...
echo.

REM Kill any existing processes on ports 8000 and 5173
echo Checking for existing servers...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do taskkill /F /PID %%a >nul 2>&1

timeout /t 2 /nobreak >nul

REM Start Django Backend
echo [1/2] Starting Django Backend...
start "Django Backend - Port 8000" cmd /k "cd /d %~dp0.be && py manage.py runserver"

REM Wait for Django to start
timeout /t 5 /nobreak >nul

REM Start Vue Frontend
echo [2/2] Starting Vue.js Frontend...
start "Vue Frontend - Port 5173" cmd /k "cd /d %~dp0 && npm run dev"

echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo.
echo Two windows will open:
echo   [1] Django Backend  - http://localhost:8000
echo   [2] Vue Frontend    - http://localhost:5173
echo.
echo Wait 10 seconds, then visit:
echo   http://localhost:5173
echo.
echo Press any key to close this window...
pause >nul
