@echo off
title SalesTrack AI - Server
cd /d "%~dp0"
echo Starting SalesTrack AI...
echo Opening in browser: http://127.0.0.1:8000
echo.
.\venv\Scripts\python.exe run.py
pause
