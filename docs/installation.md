# docx-processor Installation Guide

This guide provides comprehensive instructions for installing and configuring the docx-processor package.

> **Version Note**: This guide covers docx-processor v2.0.0-alpha with intelligent chunking features. For legacy v0.1.0 setup, see the archived documentation.

## Prerequisites

- Python 3.8 or higher (verify version: `python --version`)
- pip (Python package manager)
- **Virtual environment** (mandatory for development)

## Critical Requirements

⚠️ **IMPORTANT**: Virtual environment activation is MANDATORY for all development work. Never run Python commands without an activated virtual environment.

## Platform Notes

### Windows (Claude Desktop)
- Use PowerShell or Command Prompt
- Virtual environment activation: `.\docx-processor-env\Scripts\Activate.ps1`
- Native Windows paths: `D:\Users\alexp\dev\docx-processor`

### WSL2 (Claude Code on Ubuntu)
- Project is on Windows D: drive, accessed via mount point
- Use bash terminal
- Virtual environment activation: `source docx-processor-env/bin/activate`
- WSL2 paths: `/mnt/d/Users/alexp/dev/docx-processor`

### Linux/Mac (Native)
- Use terminal
- Virtual environment activation: `source docx-processor-env/bin/activate`
- Standard Unix paths

## Installation Methods

### Method 1: Development Mode Installation (Recommended)

Development mode allows you to modify the code while still being able to use the package from anywhere on your system.

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Create virtual environment (MANDATORY)
python -m venv docx-processor-env

# Activate virtual environment
# Windows:
.\docx-processor-env\Scripts\Activate.ps1
# Linux/Mac:
source docx-processor-env/bin/activate

# VERIFY activation (critical step)
python -c "import sys; print(sys.prefix)"
# Should show path to your virtual environment

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Method 2: Standard Installation

⚠️ **WARNING**: Always use a virtual environment, even for standard installation.

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Create and activate virtual environment (see Method 1)

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

## Verification

After installation, verify the package is correctly installed by running:

```bash
# Check version
docx-processor --version

# Should output
# docx-processor 0.1.0
```

## Running from Any Directory

When installed in development mode, you can run docx-processor from any directory:

```bash
# Navigate to a directory with your DOCX files
cd path/to/your/files

# Process a document
docx-processor input.docx output_directory
```

## Troubleshooting

### Command Not Found Error

If you get a "command not found" error after installation:

1. Ensure pip installed to the active Python environment
2. Check that your PATH includes the Python scripts directory
3. Verify your setup.py contains the correct entry point configuration

### Permission Denied Error

If you see `[Errno 13] Permission denied` when accessing files:

1. Check if the file is locked or in use by another application
2. Ensure you have proper permissions to access the file
3. Try using absolute paths for both input and output files:

```bash
# Windows
docx-processor "D:\full\path\to\input.docx" "D:\full\path\to\output_directory"

# WSL2 (accessing Windows files)
docx-processor "/mnt/d/full/path/to/input.docx" "/mnt/d/full/path/to/output_directory"

# Linux/Mac
docx-processor "/full/path/to/input.docx" "/full/path/to/output_directory"
```

4. If needed, adjust file permissions:

```bash
# Windows (PowerShell, run as Administrator)
icacls "path\to\file.docx" /grant "$(whoami)":F

# Linux/macOS/WSL2
chmod 644 path/to/file.docx
```

### Import Errors

If you encounter import errors:

1. Verify you're running the correct Python environment
2. Reinstall the package in development mode
3. Check for any conflicting packages with similar names

## Alternative Usage Methods

If you prefer not to install the package, you can run it directly from the project directory:

```bash
# Navigate to the project directory
cd path/to/docx-processor

# Run main.py directly with Python
python main.py input.docx output_directory
```

Or using the module syntax:

```bash
# Navigate to the project directory
cd path/to/docx-processor

# Run as a module
python -m src input.docx output_directory
```
