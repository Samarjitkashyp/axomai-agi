@echo off
title AxomAI AGI - Z1 Alpha Intelligence Panel
cd /d "%~dp0"
set PYTHONPATH=src
echo ========================================================
echo   AxomAI AGI - Z1 Alpha File Intelligence Panel
echo   Opening on: http://127.0.0.1:8080
echo ========================================================
.venv\Scripts\python.exe run_panel.py --port 8080
pause

