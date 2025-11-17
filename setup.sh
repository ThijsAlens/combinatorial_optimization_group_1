#!/bin/bash

echo "Creating a virtual environment..."
python3 -m venv venv
echo "Virtual environment created."
echo "Activating the virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."
echo "Installing required packages..."
pip install -r requirements.txt
echo "Required packages installed."
echo "Setup complete :)"