#!/bin/bash
# Bash setup script for docx-processor development environment
# Run from project root: ./scripts/setup.sh

echo -e "\033[32mSetting up docx-processor development environment...\033[0m"

# Check if we're in the project root
if [ ! -f "./main.py" ]; then
    echo -e "\033[31mError: Please run this script from the project root directory\033[0m"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "./docx-processor-env" ]; then
    echo -e "\033[33mCreating virtual environment...\033[0m"
    python3 -m venv docx-processor-env
    if [ $? -ne 0 ]; then
        echo -e "\033[31mError: Failed to create virtual environment\033[0m"
        exit 1
    fi
else
    echo -e "\033[36mVirtual environment already exists\033[0m"
fi

# Activate virtual environment
echo -e "\033[33mActivating virtual environment...\033[0m"
source ./docx-processor-env/bin/activate

# Upgrade pip
echo -e "\033[33mUpgrading pip...\033[0m"
python -m pip install --upgrade pip

# Install dependencies
echo -e "\033[33mInstalling dependencies...\033[0m"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "\033[31mError: Failed to install dependencies\033[0m"
    exit 1
fi

# Install package in editable mode
echo -e "\033[33mInstalling package in editable mode...\033[0m"
pip install -e .
if [ $? -ne 0 ]; then
    echo -e "\033[33mWarning: Failed to install package in editable mode\033[0m"
fi

# Create necessary directories if they don't exist
directories=("tests/test_data" "tests/test_data/fixtures" "examples" "archive")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "\033[32mCreated directory: $dir\033[0m"
    fi
done

echo -e "\n\033[32mSetup complete!\033[0m"
echo -e "\033[36mVirtual environment is activated. You can now run:\033[0m"
echo -e "  python main.py <input.docx> <output_dir>"
echo -e "\n\033[90mTo deactivate the virtual environment, run: deactivate\033[0m"

# Make the script executable
chmod +x ./scripts/setup.sh