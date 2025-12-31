#!/bin/bash
# Start MareArts ANPR Management Server
# This script will automatically load credentials from ~/.marearts/.marearts_env

cd "$(dirname "$0")"

echo "========================================================================"
echo "Starting MareArts ANPR Management Server"
echo "========================================================================"
echo ""

# Check if config file exists
if [ -f "$HOME/.marearts/.marearts_env" ]; then
    echo "✅ Found credentials in ~/.marearts/.marearts_env"
    # Source the credentials
    source "$HOME/.marearts/.marearts_env"
    echo "✅ Credentials loaded"
else
    echo "⚠️  Credentials file not found: ~/.marearts/.marearts_env"
    echo "   Run: ma-anpr config"
fi

echo ""

# Start server
python server.py

