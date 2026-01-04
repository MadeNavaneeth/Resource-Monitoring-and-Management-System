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
:: Detect IP Address using PowerShell (First non-loopback IPv4)
for /f "delims=" %%i in ('powershell -Command "([System.Net.Dns]::GetHostAddresses([System.Net.Dns]::GetHostName()) | Where-Object {$_.AddressFamily -eq 'InterNetwork'} | Select-Object -First 1).IPAddressToString"') do set LOCAL_IP=%%i

echo.
echo [1/3] Starting Backend Server...
start "SysMonitor Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [2/3] Starting Dashboard...
start "SysMonitor Dashboard" cmd /k "cd /d %~dp0dashboard && npm run dev -- --host"

echo [3/3] Starting Agent (waiting 5s for server)...
:: Use ping for delay (Unix timeout tool conflict workaround)
ping 127.0.0.1 -n 6 > nul
:: Force Agent to use the detected IP
set SERVER_URL=http://%LOCAL_IP%:8000/api/v1
start "SysMonitor Agent" cmd /k "cd /d %~dp0agent && python gui.py"

echo.
echo ========================================================
echo    ALL SERVICES STARTED!
echo ========================================================
echo.
echo    System IP: %LOCAL_IP%
echo.
echo    Backend API:   http://%LOCAL_IP%:8000/docs
echo    Dashboard:     http://%LOCAL_IP%:5173
echo.
echo    Share this IP with friends so they can connect agents!
echo.
echo    Share your IP with friends so they can connect agents!
echo.
pause
