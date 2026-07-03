@echo off
echo ========================================
echo  Building VoiceScribe GUI
echo ========================================

REM --windowed 隐藏控制台窗口（GUI 程序无 stdout/stderr）
REM --collect-all tkinterdnd2 强制打包 Tk 扩展二进制
REM --collect-all numpy numpy.libs DLL
pyinstaller ^
    --onefile ^
    --windowed ^
    --name voicescribe-gui ^
    --paths . ^
    --hidden-import=faster_whisper ^
    --hidden-import=tkinterdnd2 ^
    --collect-all tkinterdnd2 ^
    --collect-all numpy ^
    voicescribe\gui.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe-gui.exe
    echo  Size:  ~380 MB
    echo ========================================
    echo.
    echo  Test: 双击 dist\voicescribe-gui.exe
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)