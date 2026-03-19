@echo off
REM Quick KataGo Test Script

echo ========================================
echo Testing KataGo Installation
echo ========================================
echo.

set KATAGO_DIR=D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64
set KATAGO_EXE=%KATAGO_DIR%\katago.exe
set CONFIG_FILE=%KATAGO_DIR%\analysis_config.cfg
set MODEL_FILE=%KATAGO_DIR%\kata1-b40c256-s11840935168-d2898845681.bin.gz

echo Checking files...
if not exist "%KATAGO_EXE%" (
    echo ✗ katago.exe not found
    goto :error
)
echo ✓ katago.exe found

if not exist "%MODEL_FILE%" (
    echo ✗ Model file not found
    echo Please download: kata1-b40c256-s11840935168-d2898845681.bin.gz
    goto :error
)
echo ✓ Model file found

if not exist "%CONFIG_FILE%" (
    echo ⚠ Config file not found, generating...
    cd /d "%KATAGO_DIR%"
    "%KATAGO_EXE%" genconfig -model "%MODEL_FILE%" -output analysis_config.cfg
    if %errorlevel% neq 0 goto :error
    echo ✓ Config file generated
) else (
    echo ✓ Config file found
)

echo.
echo Sending test analysis request...
echo.

cd /d "%KATAGO_DIR%"
echo {"id":"test","moves":[["B","Q16"]],"rules":"chinese","komi":7.5,"boardXSize":19,"boardYSize":19,"maxVisits":100} | "%KATAGO_EXE%" analysis -config "%CONFIG_FILE%" -model "%MODEL_FILE%"

echo.
echo ========================================
echo If you see JSON output above, KataGo is working!
echo ========================================
goto :end

:error
echo.
echo ========================================
echo ERROR: Setup incomplete
echo ========================================
echo Please run: setup_katago.bat
echo.

:end
pause
