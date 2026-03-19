@echo off
echo ========================================
echo Clarus Backend - FastAPI Server
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and configure:
    echo   - GEMINI_API_KEY
    echo   - KATAGO_API_URL
    echo   - DATABASE_URL
    echo   - SECRET_KEY
    echo.
    pause
)

echo.
echo Starting FastAPI server...
echo API Documentation: http://localhost:8000/api/docs
echo Health Check: http://localhost:8000/api/go/health
echo.

python -m app.main

pause
