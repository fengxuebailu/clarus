@echo off
REM KataGo Analysis Engine Launcher for Clarus
REM This script starts KataGo in Analysis mode for the Clarus backend

echo ========================================
echo KataGo Analysis Engine Launcher
echo ========================================
echo.

REM Check if KataGo path is set
if "%KATAGO_PATH%"=="" (
    echo ERROR: KATAGO_PATH environment variable not set
    echo.
    echo Please set the following environment variables:
    echo   KATAGO_PATH=C:\path\to\katago.exe
    echo   KATAGO_CONFIG=C:\path\to\analysis_config.cfg
    echo   KATAGO_MODEL=C:\path\to\model.bin.gz
    echo.
    echo Or edit this script to set them directly.
    echo.
    pause
    exit /b 1
)

REM Default paths (edit these if not using environment variables)
if "%KATAGO_PATH%"=="" set KATAGO_PATH=C:\katago\katago.exe
if "%KATAGO_CONFIG%"=="" set KATAGO_CONFIG=C:\katago\analysis_config.cfg
if "%KATAGO_MODEL%"=="" set KATAGO_MODEL=C:\katago\kata1-b40c256-s11840935168-d2898845681.bin.gz

echo KataGo Path: %KATAGO_PATH%
echo Config: %KATAGO_CONFIG%
echo Model: %KATAGO_MODEL%
echo.

REM Check if files exist
if not exist "%KATAGO_PATH%" (
    echo ERROR: KataGo executable not found at %KATAGO_PATH%
    echo Please download KataGo from https://github.com/lightvector/KataGo/releases
    pause
    exit /b 1
)

if not exist "%KATAGO_CONFIG%" (
    echo ERROR: Config file not found at %KATAGO_CONFIG%
    echo Please run: katago genconfig -model %KATAGO_MODEL% -output %KATAGO_CONFIG%
    pause
    exit /b 1
)

if not exist "%KATAGO_MODEL%" (
    echo ERROR: Model file not found at %KATAGO_MODEL%
    echo Please download a model from https://katagotraining.org/networks/
    pause
    exit /b 1
)

echo.
echo Starting KataGo Analysis Engine...
echo Press Ctrl+C to stop
echo.

REM Start KataGo
"%KATAGO_PATH%" analysis -config "%KATAGO_CONFIG%" -model "%KATAGO_MODEL%"

pause
