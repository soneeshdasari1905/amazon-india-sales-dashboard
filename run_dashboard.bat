@echo off
setlocal
echo =====================================================================
echo    Amazon India Sales Analytics Dashboard - One-Click Launcher
echo =====================================================================
echo.

set PYTHON_EXE=
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo [INFO] Python Executable: %PYTHON_EXE%
echo [INFO] Starting Streamlit Dashboard on http://localhost:8501 ...
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.port=8501 --server.headless=false

pause
