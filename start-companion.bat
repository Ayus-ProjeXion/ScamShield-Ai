@echo off
title ∀VITR AI — Windows Desktop Shield Companion
echo ========================================================
echo   ∀VITR AI — Windows Real-Time Scam Shield Companion
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python desktop_companion.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py desktop_companion.py
    goto end
)

echo [ERROR] Python was not found in your system PATH.
echo Please install Python 3.8+ from https://www.python.org/
echo (Check the box "Add Python to PATH" during installation).
echo.
pause
exit /b 1

:end
pause
