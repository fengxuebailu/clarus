@echo off
REM 设置 Python 使用 UTF-8 编码
SET PYTHONIOENCODING=utf-8
SET PYTHONUTF8=1

echo ========================================
echo Clarus Backend - FastAPI Server (UTF-8)
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server with UTF-8 encoding...
echo API Documentation: http://localhost:8000/api/docs
echo Health Check: http://localhost:8000/api/go/health
echo.

python -m app.main

pause
