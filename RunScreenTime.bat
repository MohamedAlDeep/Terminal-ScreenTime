@echo off
chcp 65001 >nul 2>&1
title Screen Time Tracker
cd /d "%~dp0"

REM Check if executable exists
if not exist "dist\ScreenTimeTracker.exe" (
    echo Error: ScreenTimeTracker.exe not found in dist folder
    pause
    exit /b 1
)

REM Run the executable with passed arguments
dist\ScreenTimeTracker.exe %*
