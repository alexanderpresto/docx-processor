# docx-processor Installation Guide

This guide provides comprehensive instructions for installing and configuring the docx-processor package.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation Methods

### Method 1: Standard Installation

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

### Method 2: Development Mode Installation (Recommended)

Development mode allows you to modify the code while still being able to use the package from anywhere on your system.

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Install in development mode
pip install -e .
```

This creates a special link in your Python environment that points to your project folder, making the package accessible from anywhere while allowing you to edit the code.

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
docx-processor "C:\full\path\to\input.docx" "C:\full\path\to\output_directory"
```

4. If needed, adjust file permissions:

```bash
# Windows (PowerShell, run as Administrator)
icacls "path\to\file.docx" /grant "$(whoami)":F

# Linux/macOS
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
