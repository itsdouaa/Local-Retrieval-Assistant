@echo off
echo 🤖 RAG Assistant Setup for Windows
echo ==================================

:: Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Install from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python version %%i

:: Install Tesseract via Chocolatey
echo Installing Tesseract OCR...
where choco >nul 2>&1
if errorlevel 1 (
    echo Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
)

choco install tesseract -y --no-progress

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

:: Setup API key
set /p apiKey="Enter your Groq API key (or press Enter to skip): "
if not "%apiKey%"=="" (
    echo %apiKey% > groq_API.txt
    echo ✅ API key saved to groq_API.txt
) else (
    echo ⚠️  No API key provided. Create groq_API.txt manually later.
)

echo.
echo ==================================
echo ✅ Setup completed successfully!
echo.
echo Run: venv\Scripts\activate.bat
echo Then: python engine.py
echo ==================================
pause