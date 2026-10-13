@echo off
setlocal
cd /d "%~dp0.."

set "HARU_PYTHON="
set "CODEX_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "CODEX_PYTHONW=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe"
if exist "%CODEX_PYTHONW%" set "HARU_PYTHON=""%CODEX_PYTHONW%""
if not defined HARU_PYTHON if exist "%CODEX_PYTHON%" set "HARU_PYTHON=""%CODEX_PYTHON%""

if not defined HARU_PYTHON (
  where py.exe >nul 2>nul
  if not errorlevel 1 set "HARU_PYTHON=py -3"
)

if not defined HARU_PYTHON (
  where python.exe >nul 2>nul
  if not errorlevel 1 set "HARU_PYTHON=python"
)

if not defined HARU_PYTHON (
  echo.
  echo No se encontro un runtime compatible de Python en este equipo.
  echo Haru necesita Python 3 con Pillow y Tkinter.
  pause
  exit /b 1
)

%HARU_PYTHON% desktop\haru_desktop.py
if errorlevel 1 (
  echo.
  echo Haru no pudo iniciar. Revisa el mensaje de error mostrado arriba.
  pause
)
