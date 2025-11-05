@echo off
echo ========================================
echo Git Push Helper - Using API Token
echo ========================================
echo.
echo This script will help you push to Bitbucket using an API token
echo.
echo First, create a Repository Access Token:
echo 1. Go to: https://bitbucket.org/digi_port/digiport/admin/access-tokens
echo 2. Click "Create Repository Access Token"
echo 3. Name: "Git Push Token"
echo 4. Permissions: Select "Write"
echo 5. Copy the token
echo.
set /p token="Paste your Repository Access Token here: "
echo.
echo Pushing to Bitbucket...
git push https://x-token-auth:%token%@bitbucket.org/digi_port/digiport.git master
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Your commits are now on Bitbucket!
    echo ========================================
) else (
    echo ========================================
    echo FAILED! Please check your token and try again.
    echo ========================================
)
echo.
pause
