@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
.venv\Scripts\python.exe screentime_cli.py %*
