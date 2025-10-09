#!/bin/bash

# RAG Assistant Setup Script for Fedora
# This script installs dependencies and sets up the project

set -e  # Exit on any error

echo "🤖 RAG Assistant Setup for Fedora"
echo "================================"

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo dnf install -y python3
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION is too old. Need 3.8+"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION"

# Install Tesseract OCR
echo "Installing Tesseract OCR..."
sudo dnf install -y tesseract tesseract-langpack-eng tesseract-langpack-fra tesseract-langpack-ara

# Verify Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract installation failed"
    exit 1
fi
echo "✅ Tesseract installed"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate and install dependencies
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
echo "================================"
echo "✅ Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python engine.py"
echo "================================"