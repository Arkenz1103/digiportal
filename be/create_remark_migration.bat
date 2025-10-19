@echo off
cd /d "%~dp0"
echo Creating migrations for Remark model with is_read field...
python manage.py makemigrations
echo.
echo Applying migrations...
python manage.py migrate
echo.
echo Migration completed successfully!
echo.
pause
