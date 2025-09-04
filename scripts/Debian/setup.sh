#!/bin/bash

# RAG Assistant Setup Script for Fedora
# This script sets up the project from within the project directory

set -e  # Exit on any error

echo "🤖 RAG Assistant Setup Script for Fedora"
echo "========================================"
echo "Running from: $(pwd)"
echo "========================================"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed and meets version requirement
echo "Checking Python version..."
if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Installing Python 3..."
    sudo dnf install -y python3
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo "✅ Python version $PYTHON_VERSION is compatible"
else
    echo "❌ Python version $PYTHON_VERSION is too old. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Setup Groq API key
echo "Setting up Groq API key..."
read -p "Enter your Groq API key: " API_KEY
if [ -z "$API_KEY" ]; then
    echo "⚠️  No API key provided. You'll need to set this up manually later."
else
    echo "$API_KEY" | sudo tee /etc/groq_API.txt > /dev/null
    sudo chmod 600 /etc/groq_API.txt
    echo "✅ API key saved to /etc/groq_API.txt"
fi

# Final setup
echo ""
echo "========================================"
echo "✅ Fedora setup completed successfully!"
echo ""
echo "Virtual environment: venv/"
echo "Project ready in: $(pwd)"
echo ""
echo "To activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "To run the application:"
echo "   python engine.py"
echo ""
echo "Note: If you didn't provide an API key, make sure to:"
echo "   echo 'your_api_key' | sudo tee /etc/groq_API.txt"
echo "   sudo chmod 600 /etc/groq_API.txt"
echo "========================================"
