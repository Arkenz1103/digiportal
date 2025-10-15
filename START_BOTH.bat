@echo off
cls
echo ========================================
echo   Starting DigiPortal Frontend
echo ========================================
echo.
echo Starting Vue Frontend on localhost:5173...
echo.

REM Start Vite frontend only
npm run dev

echo.
echo Frontend server is running!
echo Visit: http://localhost:5173
