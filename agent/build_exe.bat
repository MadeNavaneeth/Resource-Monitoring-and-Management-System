@echo off
title Build SysMonitor Agent
color 0A

echo ========================================================
echo       SYSMONITOR AGENT - BUILD SYSTEM
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b
)

echo.
echo [2/4] Installing Build Dependencies...
pip install pyinstaller psutil requests python-dotenv

echo.
echo [3/4] Building Executable...
echo       This may take a minute...
pyinstaller --noconfirm --log-level=WARN SysMonitorAgent.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build Failed!
    pause
    exit /b
)

echo.
echo [4/4] verifying...
if exist "dist\SysMonitorAgent.exe" (
    echo.
    echo ========================================================
    echo    BUILD SUCCESSFUL!
    echo ========================================================
    echo    Executable: agent\dist\SysMonitorAgent.exe
    echo.
    echo    You can now copy 'agent\dist' folder to other PCs.
    echo    Remember to configure .env or user input on first run.
    echo.
) else (
    echo [ERROR] SysMonitorAgent.exe not found in dist/
)

pause
