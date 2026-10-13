@echo off
setlocal

set "HARU_SCRIPT=%~dp0haru_desktop.py"
set "CODEX_RUNTIME=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python"

if not exist "%HARU_SCRIPT%" (
  echo.
  echo No se encontro el programa de Haru:
  echo %HARU_SCRIPT%
  pause
  exit /b 1
)

if exist "%CODEX_RUNTIME%\pythonw.exe" (
  start "Haru Urara" "%CODEX_RUNTIME%\pythonw.exe" "%HARU_SCRIPT%"
  exit /b 0
)

if exist "%CODEX_RUNTIME%\python.exe" (
  "%CODEX_RUNTIME%\python.exe" "%HARU_SCRIPT%"
  goto :result
)

where py.exe >nul 2>nul
if not errorlevel 1 (
  py -3 "%HARU_SCRIPT%"
  goto :result
)

echo.
echo No se encontro un runtime compatible de Python en este equipo.
echo Haru necesita Python 3 con Pillow y Tkinter.
pause
exit /b 1

:result
if errorlevel 1 (
  echo.
  echo Haru no pudo iniciar. Revisa el mensaje de error mostrado arriba.
  pause
  exit /b 1
)
