@echo off
echo ========================================
echo  Building VoiceScribe CLI
echo ========================================

pyinstaller ^
    --onefile ^
    --name voicescribe ^
    --add-data "voicescribe/core;voicescribe/core" ^
    --hidden-import=faster_whisper ^
    --hidden-import=watchdog ^
    --hidden-import=PyYAML ^
    voicescribe/cli.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)