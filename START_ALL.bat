@echo off
echo ========================================
echo DigiPortal - Starting All Servers
echo ========================================
echo.

REM Start Django Backend in new window
echo Starting Django Backend...
start "Django Backend" cmd /k "cd .be && py manage.py migrate && py manage.py runserver"

REM Wait a bit for Django to start
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo Starting Vue.js Frontend...
start "Vue Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Django Backend: http://localhost:8000
echo Vue Frontend: http://localhost:5173
echo.
echo Two new windows will open:
echo   1. Django Backend (black window)
echo   2. Vue Frontend (black window)
echo.
echo Wait for both to finish starting, then visit:
echo http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
