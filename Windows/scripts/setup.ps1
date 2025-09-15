# RAG Assistant Setup for Windows PowerShell
Write-Host "🤖 RAG Assistant Setup for Windows" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if (-not $pythonVersion) {
    Write-Host "❌ Python not found. Install from https://python.org" -ForegroundColor Red
    exit
}

Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Install Tesseract via Chocolatey
Write-Host "Installing Tesseract OCR..." -ForegroundColor Yellow
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

choco install tesseract -y --no-progress

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Setup API key
$apiKey = Read-Host "Enter your Groq API key (or press Enter to skip)"
if ($apiKey) {
    $apiKey | Out-File -FilePath "groq_API.txt" -Encoding utf8
    Write-Host "✅ API key saved to groq_API.txt" -ForegroundColor Green
} else {
    Write-Host "⚠️  No API key provided. Create groq_API.txt manually later." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host "Run: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "Then: python engine.py" -ForegroundColor White
Write-Host "==================================" -ForegroundColor Green