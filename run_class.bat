@echo off
REM 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
setlocal
if "%~1"=="" (
  echo Usage: run_class.bat class001
  exit /b 1
)
set CLASS_ID=%~1
set PY_FILE=%~dp0%CLASS_ID%\%CLASS_ID%.py
if not exist "%PY_FILE%" (
  echo Class file not found: %PY_FILE%
  exit /b 1
)
python "%PY_FILE%"
endlocal
