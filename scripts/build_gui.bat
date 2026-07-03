@echo off
echo ========================================
echo  Building VoiceScribe GUI
echo ========================================

pyinstaller ^
    --onefile ^
    --windowed ^
    --name voicescribe-gui ^
    --add-data "voicescribe/core;voicescribe/core" ^
    --hidden-import=faster_whisper ^
    --hidden-import=tkinterdnd2 ^
    --collect-all tkinterdnd2 ^
    voicescribe/gui.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe-gui.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)