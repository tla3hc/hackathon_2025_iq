#!/bin/bash
# Quick start script for Mock Server

echo "============================================================"
echo "Mock Server Quick Start"
echo "============================================================"
echo ""

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Flask not found. Installing..."
    pip3 install flask
    echo ""
fi

echo "Starting Mock Server..."
echo "Server will run at: http://127.0.0.1:5000"
echo "Password: dummy_password"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 mock_server.py
