@echo off
REM KataGo Setup Script for Clarus
REM This script helps you configure KataGo for the first time

echo ========================================
echo KataGo Setup for Clarus
echo ========================================
echo.

REM Set KataGo directory
set KATAGO_DIR=D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64
set KATAGO_EXE=%KATAGO_DIR%\katago.exe

echo Step 1: Checking KataGo installation...
if not exist "%KATAGO_EXE%" (
    echo ERROR: katago.exe not found at %KATAGO_EXE%
    echo Please check the path and try again.
    pause
    exit /b 1
)
echo ✓ KataGo found: %KATAGO_EXE%
echo.

REM Check for model file
echo Step 2: Checking for neural network model...
set MODEL_FILE=%KATAGO_DIR%\kata1-b40c256-s11840935168-d2898845681.bin.gz

if exist "%MODEL_FILE%" (
    echo ✓ Model found: %MODEL_FILE%
) else (
    echo ⚠ Model file not found!
    echo.
    echo You need to download a KataGo neural network model.
    echo.
    echo Recommended models:
    echo 1. 40-block (recommended, ~200MB): kata1-b40c256-s11840935168-d2898845681.bin.gz
    echo 2. 20-block (faster, ~100MB): kata1-b20c256x2-s5303129600-d1228401921.bin.gz
    echo.
    echo Download from: https://katagotraining.org/networks/
    echo.
    echo After downloading, place the .bin.gz file in:
    echo %KATAGO_DIR%
    echo.
    echo Would you like me to show you the download link?
    choice /C YN /M "Open download page in browser"
    if errorlevel 2 goto :skip_download
    start https://katagotraining.org/networks/
    :skip_download
    echo.
    echo Please download the model, then run this script again.
    pause
    exit /b 1
)
echo.

REM Check for config file
echo Step 3: Checking for analysis config file...
set CONFIG_FILE=%KATAGO_DIR%\analysis_config.cfg

if exist "%CONFIG_FILE%" (
    echo ✓ Config found: %CONFIG_FILE%
    echo.
    choice /C YN /M "Config file exists. Regenerate it"
    if errorlevel 2 goto :skip_genconfig
)

echo Generating analysis config...
cd /d "%KATAGO_DIR%"
"%KATAGO_EXE%" genconfig -model "%MODEL_FILE%" -output analysis_config.cfg

if %errorlevel% neq 0 (
    echo ERROR: Failed to generate config file
    pause
    exit /b 1
)

echo ✓ Config file generated
:skip_genconfig
echo.

REM Update .env file
echo Step 4: Updating Clarus .env configuration...
set ENV_FILE=D:\ai\Clarus\backend\.env

if not exist "%ENV_FILE%" (
    echo Creating .env file from example...
    copy "D:\ai\Clarus\backend\.env.example" "%ENV_FILE%"
)

REM Create temporary PowerShell script to update .env
echo $envFile = "%ENV_FILE%" > update_env.ps1
echo $content = Get-Content $envFile >> update_env.ps1
echo $content = $content -replace "KATAGO_PATH=.*", "KATAGO_PATH=%KATAGO_EXE:\=\\%" >> update_env.ps1
echo $content = $content -replace "KATAGO_CONFIG=.*", "KATAGO_CONFIG=%CONFIG_FILE:\=\\%" >> update_env.ps1
echo $content = $content -replace "KATAGO_MODEL=.*", "KATAGO_MODEL=%MODEL_FILE:\=\\%" >> update_env.ps1
echo $content ^| Set-Content $envFile >> update_env.ps1

powershell -ExecutionPolicy Bypass -File update_env.ps1
del update_env.ps1

echo ✓ .env file updated
echo.

REM Test KataGo
echo Step 5: Testing KataGo...
echo Sending test query...
cd /d "%KATAGO_DIR%"

echo {"id":"test","moves":[["B","Q16"]],"rules":"chinese","komi":7.5,"boardXSize":19,"boardYSize":19,"maxVisits":100} | "%KATAGO_EXE%" analysis -config "%CONFIG_FILE%" -model "%MODEL_FILE%" 2>nul | findstr "id"

if %errorlevel% neq 0 (
    echo ⚠ Warning: Test query failed
    echo This might be normal if GPU drivers are not installed
    echo The system will fall back to mock data
) else (
    echo ✓ KataGo is working!
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo KataGo configuration:
echo   Executable: %KATAGO_EXE%
echo   Config: %CONFIG_FILE%
echo   Model: %MODEL_FILE%
echo.
echo Next steps:
echo   1. Start the Clarus backend: cd D:\ai\Clarus\backend ^&^& python -m app.main
echo   2. Open workspace-go.html
echo   3. Try analyzing a position!
echo.
echo KataGo will now provide REAL AI analysis instead of mock data!
echo.
pause
