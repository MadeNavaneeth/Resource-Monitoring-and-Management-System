@echo off
title Kill SysMonitor Processes
color 0C

echo ========================================================
echo       KILLING STUCK SERVERS (Zombie Clean-up) 🧟‍♂️
echo ========================================================
echo.

echo [*] Asking Python processes to stop...
taskkill /F /IM python.exe /T
echo.

echo [*] Asking Node.js (Dashboard) to stop...
taskkill /F /IM node.exe /T
echo.

echo ========================================================
echo       CLEANUP COMPLETE!
echo ========================================================
echo.
echo Now you can run "run_all.bat" freshly.
echo.
pause
