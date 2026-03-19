@echo off
echo ========================================
echo Clarus Backend - Setup Script
echo ========================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example to .env
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and configure your API keys
echo 2. Run start.bat to start the server
echo.
pause
