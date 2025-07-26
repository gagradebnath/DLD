#!/bin/bash

echo ""
echo "==================================================="
echo " Digital Logic Design IC Library - Web Frontend"
echo "==================================================="
echo ""
echo "Starting web server..."
echo ""
echo "Open your browser to: http://localhost:5000"
echo ""
echo "Features available:"
echo "  - Interactive IC Simulator"
echo "  - Circuit Designer"
echo "  - Real-time Logic Testing"
echo "  - IC Documentation"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 web_frontend/app.py
