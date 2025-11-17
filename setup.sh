#!/bin/bash

# --- 1. Find the correct Python command ---
# Default to python3
PY_CMD="python3"

# Check if python3 exists
if ! command -v python3 &> /dev/null; then
    # If not, check for python
    if command -v python &> /dev/null; then
        echo "python3 not found, falling back to 'python'."
        PY_CMD="python"
    else
        # If neither exists, error out
        echo "Error: Python not found."
        echo "Please install Python 3. After installation, run this script again."
        exit 1
    fi
fi

# Check version
echo "Using Python: $($PY_CMD --version)"

# --- 2. Create the virtual environment ---
echo "Creating virtual environment 'venv'..."
$PY_CMD -m venv venv

# --- 3. Activate based on OS ---
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    # For macOS and Linux
    source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # For Windows (Git Bash)
    # Note: Git Bash (msys) uses the "Scripts" folder
    source venv/Scripts/activate
else
    echo "Unsupported OS: $OSTYPE"
    echo "Please activate the environment called \"venv\" manually. After it is activated, run: \"pip install -r requirements.txt\""
    exit 1
fi

# --- 4. Install requirements ---
echo "Installing requirements..."
pip install -r requirements.txt

echo "---"
echo "Setup complete :)."
echo "---"