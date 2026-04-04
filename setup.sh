#!/bin/bash

# DpForge Setup Script
# Run this script to set up DpForge on your system

set -e

echo "======================================"
echo "  DpForge - Display Picture Forge"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

echo "[1/4] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed."
    exit 1
fi

# Install Python dependencies
echo ""
echo "[2/4] Installing Python dependencies..."
pip3 install -r requirements.txt
echo "  Dependencies installed!"

# Check Ollama
echo ""
echo "[3/4] Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "  Ollama is installed!"
    
    # Pull recommended model
    echo ""
    echo "[4/4] Pulling image generation model..."
    echo "  This may take a few minutes..."
    ollama pull sdxl-turbo 2>/dev/null || echo "  (Model may already exist)"
    echo "  Model ready!"
else
    echo "  Ollama not found!"
    echo ""
    echo "  Please install Ollama:"
    echo "  - macOS/Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  - Windows: Download from https://ollama.ai/download"
    echo ""
    echo "  After installing, run this script again."
fi

echo ""
echo "======================================"
echo "  Setup complete!"
echo "======================================"
echo ""
echo "To start DpForge:"
echo "  1. Make sure Ollama is running: ollama serve"
echo "  2. Run: python3 server.py"
echo "  3. Open: http://localhost:8000"
echo ""
