@echo off
echo ========================================
echo Starting Vue.js Frontend
echo ========================================
echo.

echo Checking node_modules...
if not exist node_modules\ (
    echo Installing dependencies...
    npm install
)

echo.
echo ========================================
echo Starting Vite Development Server
echo ========================================
echo.
echo Server will run at: http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev
