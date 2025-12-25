@echo off
title SysMonitor Launcher
color 0A

echo ========================================================
echo       RESOURCE MONITORING SYSTEM - LAUNCHER
echo ========================================================
echo.

:: Check if firewall rule already exists
netsh advfirewall firewall show rule name="SysMonitor Backend" >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Firewall already configured
    goto :start_services
)

:: Firewall rule doesn't exist - check if we're admin
net session >nul 2>&1
if %errorLevel% equ 0 (
    :: We ARE admin - add the rules
    echo [*] Adding firewall rules...
    netsh advfirewall firewall add rule name="SysMonitor Backend" dir=in action=allow protocol=TCP localport=8000 >nul
    netsh advfirewall firewall add rule name="SysMonitor Discovery" dir=in action=allow protocol=UDP localport=9999 >nul
    echo [OK] Firewall configured!
    goto :start_services
)

:: Not admin and no firewall rule - need to elevate
echo [!] First-time setup - need Administrator to open firewall
echo [*] Requesting elevation...
powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
exit /b

:start_services
echo.
echo [1/3] Starting Backend Server...
start "SysMonitor Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [2/3] Starting Dashboard...
start "SysMonitor Dashboard" cmd /k "cd /d %~dp0dashboard && npm run dev"

echo [3/3] Starting Agent (waiting 5s for server)...
timeout /t 5 /nobreak >nul
start "SysMonitor Agent" cmd /k "cd /d %~dp0agent && python gui.py"

echo.
echo ========================================================
echo    ALL SERVICES STARTED!
echo ========================================================
echo.

:: Get and display the server's IP address
echo    Your Server IP Addresses:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    echo      %%a
)
echo.
echo    Backend API:   http://localhost:8000/docs
echo    Dashboard:     http://localhost:5173
echo.
echo    Share your IP with friends so they can connect agents!
echo.
pause
