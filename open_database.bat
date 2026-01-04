@echo off
echo ============================================
echo   Open Database in DB Browser for SQLite
echo ============================================
echo.

set DB_PATH=backend\resource_monitor.db
set DB_BROWSER="C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"

echo Database Location: %DB_PATH%
echo.

REM Check if DB Browser is installed
if exist %DB_BROWSER% (
    echo Opening database in DB Browser...
    start "" %DB_BROWSER% %DB_PATH%
    echo.
    echo ✓ Database opened successfully!
) else (
    echo DB Browser for SQLite not found!
    echo.
    echo Please install it first by running:
    echo   db_browser_sqlite_installer.msi
    echo.
    echo Or manually open the database file:
    echo   %CD%\%DB_PATH%
    echo.
    pause
)

echo.
echo ============================================
echo   Alternative Methods:
echo ============================================
echo.
echo 1. Python Script:
echo    python inspect_db.py
echo.
echo 2. Detailed View:
echo    python view_all_user_data.py
echo.
echo 3. Open this file manually in DB Browser:
echo    %CD%\%DB_PATH%
echo.
pause
