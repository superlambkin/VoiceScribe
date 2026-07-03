@echo off
echo ========================================
echo  Building VoiceScribe CLI
echo ========================================

REM Use voicescribe/__main__.py as entry to support relative imports
REM --paths . 让 PyInstaller 找到 voicescribe 包
pyinstaller ^
    --onefile ^
    --name voicescribe ^
    --paths . ^
    --hidden-import=faster_whisper ^
    --hidden-import=watchdog ^
    --hidden-import=PyYAML ^
    voicescribe\__main__.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe.exe
    echo  Size:  ~400 MB (含 faster-whisper 全依赖)
    echo ========================================
    echo.
    echo  Test: dist\voicescribe.exe --version
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)