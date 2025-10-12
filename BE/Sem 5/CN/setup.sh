#!/bin/bash

# Setup script for Error Detection Methods Project (Practical 5)
# This script installs dependencies in the global virtual environment

echo "Setting up Error Detection Methods Project (Practical 5)..."
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "error_detection.py" ]; then
    echo "Error: Please run this script from the Practical5-ErrorDetection directory"
    exit 1
fi

# Check if global virtual environment exists
if [ -d "../venv" ]; then
    echo "Global virtual environment found."
    echo "Activating global virtual environment..."
    source ../venv/bin/activate
else
    echo "Global virtual environment not found. Creating one..."
    cd ..
    python3 -m venv venv
    source venv/bin/activate
    cd Practical5-ErrorDetection
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo "==============="
echo ""
echo "To activate the global virtual environment, run:"
echo "  source ../venv/bin/activate"
echo ""
echo "To run the main program:"
echo "  python error_detection.py"
echo ""
echo "To run tests:"
echo "  python test_error_detection.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
