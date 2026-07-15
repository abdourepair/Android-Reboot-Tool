@echo off
setlocal

echo ============================================
echo   Android Multitool - launcher
echo ============================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] Python was not found on this PC.
        echo     Download and install it from https://www.python.org/downloads/
        echo     During install, make sure to check "Add Python to PATH".
        echo.
        pause
        exit /b 1
    ) else (
        set PYCMD=py
    )
) else (
    set PYCMD=python
)

echo [*] Using: %PYCMD%
echo [*] Checking dependencies...
%PYCMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check

echo [*] Starting Android Multitool...
echo.
%PYCMD% src\main.py

echo.
pause
