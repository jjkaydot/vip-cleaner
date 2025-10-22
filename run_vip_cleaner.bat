@echo off
:: VIP System Cleaner - Run as Administrator
:: Premium Edition with Golden Theme

echo ================================================
echo   💎 VIP System Cleaner - Premium Edition 💎
echo ================================================
echo.
echo Starting VIP application with administrator rights...
echo.

:: Check for Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Run the Python script with admin privileges
powershell -Command "Start-Process python -ArgumentList '%~dp0vip_system_cleaner.py' -Verb RunAs"

exit