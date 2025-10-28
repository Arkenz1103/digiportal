@echo off
echo ============================================================
echo SETTING UP STUDENT DATA SYSTEM
echo ============================================================
echo.

echo Step 1: Running migration to create students table...
py manage.py migrate api 0034
if %errorlevel% neq 0 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Populating student data (360 students)...
py test_and_populate.py
if %errorlevel% neq 0 (
    echo ERROR: Population failed!
    pause
    exit /b 1
)
echo.

echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
pause
