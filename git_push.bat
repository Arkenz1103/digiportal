@echo off
echo Pushing to Bitbucket...
git push https://kentaxkpel:ATATT3xFfGF0mDCyZCOrESeH8ZmM2fmmWB3BJncAAiZbmsAgXRL6_hNpiCY1IKggtyWkxgdb_GU9ZglDYu3-ozyvn-nhfOSAtscO5nCf0zxIUI9C7OIYquLkA5f2GGBnWvpiDOwZ8hPq1zH-mc6DIs2_JdUYYyGqC9neQfu0jIxhFgRrsMqWaM8=6F7CFF2E@bitbucket.org/digi_port/digiport.git master
if errorlevel 1 (
    echo Push failed!
    pause
    exit /b 1
)
echo Push successful!
pause
