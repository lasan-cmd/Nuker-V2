@echo off
setlocal enabledelayedexpansion

goto :main

:center
cls
echo.
echo     █████                  █████████                          ██████   █████            █████
echo     ▒▒███                  ███▒▒▒▒▒███                        ▒▒██████ ▒▒███            ▒▒███
echo      ▒███         ██████  ▒███    ▒▒▒   ██████   ████████      ▒███▒███ ▒███  █████ ████ ▒███ █████  ██████  ████████
echo      ▒███        ▒▒▒▒▒███ ▒▒█████████  ▒▒▒▒▒███ ▒▒███▒▒███     ▒███▒▒███▒███ ▒▒███ ▒███  ▒███▒▒███  ███▒▒███▒▒███▒▒███
echo      ▒███         ███████  ▒▒▒▒▒▒▒▒███  ███████  ▒███ ▒███     ▒███ ▒▒██████  ▒███ ▒███  ▒██████▒  ▒███████  ▒███ ▒▒▒
echo      ▒███      █ ███▒▒███  ███    ▒███ ███▒▒███  ▒███ ▒███     ▒███  ▒▒█████  ▒███ ▒███  ▒███▒▒███ ▒███▒▒▒   ▒███
echo     ███████████▒▒████████▒▒█████████ ▒▒████████ ████ █████    █████  ▒▒█████ ▒▒████████ ████ █████▒▒██████  █████
echo     ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒ ▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒    ▒▒▒▒▒   ▒▒▒▒▒▒▒▒ ▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒  ▒▒▒▒▒
echo.
goto :eof

:section
cls
echo.
echo   %~1
echo   =============================================
echo.
goto :eof

:main
call :center

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [ERROR] Python is not installed!
    echo.
    echo   Death Hub requires Python 3.12
    echo.
    echo   Press ENTER to install Python 3.12...
    echo.
    pause >nul

    call :section "Downloading Python 3.12"
    echo   Please wait...
    echo.

    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python312-installer.exe'"

    call :section "Installing Python"
    echo   Please wait...
    echo.

    start /wait python312-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python312-installer.exe 2>nul
)

call :section "Checking Python"
python --version
echo.

call :section "Installing Dependencies"
echo.

python -m pip install --upgrade pip >nul 2>&1
echo   [OK] Upgraded pip

python -m pip uninstall discord -y >nul 2>&1
python -m pip uninstall discord.py -y >nul 2>&1
echo   [OK] Cleaned old packages

python -m pip install --no-cache-dir discord.py aiohttp >nul 2>&1
echo   [OK] Installed discord.py ^& aiohttp
echo.

call :section "Installation Complete"
echo   Run Death Hub using: start.bat
echo.
timeout /t 5 /nobreak >nul