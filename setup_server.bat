@echo off
title SysMonitor Server Setup
color 0E

echo ========================================================
echo       SYSMONITOR - SERVER SETUP (Run as Admin)
echo ========================================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run this script as Administrator!
    echo.
    echo Right-click on this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [1/2] Opening Windows Firewall port 8000...
netsh advfirewall firewall delete rule name="SysMonitor Backend" >nul 2>&1
netsh advfirewall firewall add rule name="SysMonitor Backend" dir=in action=allow protocol=TCP localport=8000
if %errorLevel% equ 0 (
    echo       [OK] Firewall rule added successfully!
) else (
    echo       [FAIL] Could not add firewall rule
)

echo.
echo [2/2] Opening Windows Firewall for UDP Discovery (port 9999)...
netsh advfirewall firewall delete rule name="SysMonitor Discovery" >nul 2>&1
netsh advfirewall firewall add rule name="SysMonitor Discovery" dir=in action=allow protocol=UDP localport=9999
if %errorLevel% equ 0 (
    echo       [OK] Discovery firewall rule added!
) else (
    echo       [FAIL] Could not add discovery rule
)

echo.
echo ========================================================
echo                   SETUP COMPLETE!
echo ========================================================
echo.
echo Your PC is now ready to be a SysMonitor Server.
echo.
echo Other PCs on your network can now:
echo   1. Connect agents to your IP address
echo   2. Auto-discover your server via UDP broadcast
echo.
echo To find your IP address, run: ipconfig
echo.
pause
