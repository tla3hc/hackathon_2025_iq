@echo off
REM Quick start script for Mock Server

echo ============================================================
echo Mock Server Quick Start
echo ============================================================
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing...
    pip install flask
    echo.
)

echo Starting Mock Server...
echo Server will run at: http://127.0.0.1:5000
echo Password: dummy_password
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python mock_server.py
