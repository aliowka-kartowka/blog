#!/bin/bash
#
# Preview the restored blog locally
# Usage: ./preview.sh
#

echo "=================================================="
echo "  Alexey Vishnevsky Blog - Local Preview"
echo "=================================================="
echo ""
echo "Starting local web server..."
echo ""
echo "📍 URL: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=================================================="
echo ""

cd restored-blog-clean/
python3 -m http.server 8000
