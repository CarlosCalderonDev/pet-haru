@echo off
setlocal
cd /d "%~dp0.."
python desktop\haru_desktop.py
if errorlevel 1 (
  echo.
  echo No fue posible iniciar Haru. Instala Python y ejecuta: python -m pip install -r requirements.txt
  pause
)
