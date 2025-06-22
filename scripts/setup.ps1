# PowerShell setup script for docx-processor development environment
# Run from project root: .\scripts\setup.ps1

Write-Host "Setting up docx-processor development environment..." -ForegroundColor Green

# Check if we're in the project root
if (-not (Test-Path ".\main.py")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".\docx-processor-env")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv docx-processor-env
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Cyan
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\docx-processor-env\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install package in editable mode
Write-Host "Installing package in editable mode..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Failed to install package in editable mode" -ForegroundColor Yellow
}

# Create necessary directories if they don't exist
$directories = @("tests\test_data", "tests\test_data\fixtures", "examples", "archive")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "Virtual environment is activated. You can now run:" -ForegroundColor Cyan
Write-Host "  python main.py <input.docx> <output_dir>" -ForegroundColor White
Write-Host "`nTo deactivate the virtual environment, run: deactivate" -ForegroundColor Gray
