#!/bin/bash

# RAG Assistant Setup Script
# This script installs system dependencies for the RAG Assistant project

set -e  # Exit on any error

echo "🤖 RAG Assistant Dependency Installer"
echo "======================================"

# Check if Python is installed and meets version requirement
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo "✅ Python version $PYTHON_VERSION is compatible"
else
    echo "❌ Python version $PYTHON_VERSION is too old. Please install Python 3.8 or higher."
    exit 1
fi

# Update package list
echo "Updating package list..."
sudo apt update

# Install Tesseract OCR and language packs
echo "Installing Tesseract OCR and language packs..."
sudo apt install -y tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-fra \
    tesseract-ocr-eng

# Verify Tesseract installation
echo "Verifying Tesseract installation..."
TESSERACT_VERSION=$(tesseract --version | head -n1)
if [ $? -eq 0 ]; then
    echo "✅ Tesseract installed: $TESSERACT_VERSION"
else
    echo "❌ Tesseract installation failed"
    exit 1
fi

# Verify language packs are installed
echo "Checking installed Tesseract languages..."
INSTALLED_LANGS=$(tesseract --list-langs)
for lang in ara fra eng; do
    if echo "$INSTALLED_LANGS" | grep -q "$lang"; then
        echo "✅ $lang language pack installed"
    else
        echo "❌ $lang language pack not found"
    fi
done

echo ""
echo "======================================"
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Create a virtual environment:"
echo "   python3 -m venv venv"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Install Python dependencies:"
echo "   pip install -r requirements.txt"
echo "4. Set up your Groq API key:"
echo "   echo 'your_api_key_here' | sudo tee /etc/groq_API.txt"
echo "   sudo chmod 600 /etc/groq_API.txt"
echo "5. Run the application:"
echo "   python engine.py"
echo "======================================"
