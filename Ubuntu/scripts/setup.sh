#!/bin/bash

# RAG Assistant Setup for Ubuntu/Debian
set -e

echo "🤖 RAG Assistant Setup for Ubuntu/Debian"
echo "========================================"

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-venv
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    echo "❌ Python $PYTHON_VERSION is too old. Need 3.8+"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION"

# Install Tesseract OCR
echo "Installing Tesseract OCR..."
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-ara

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup API key
echo "Setting up API key..."
read -p "Enter your Groq API key (or press Enter to skip): " API_KEY
if [ -n "$API_KEY" ]; then
    echo "$API_KEY" | sudo tee /etc/groq_API.txt > /dev/null
    sudo chmod 600 /etc/groq_API.txt
    echo "✅ API key saved to /etc/groq_API.txt"
else
    echo "⚠️  No API key provided. Create /etc/groq_API.txt manually later."
fi

echo ""
echo "========================================"
echo "✅ Setup completed successfully!"
echo "Run: source venv/bin/activate && python engine.py"
echo "========================================"