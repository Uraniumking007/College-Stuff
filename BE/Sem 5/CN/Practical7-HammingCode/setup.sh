#!/bin/bash

# Setup script for Hamming Code Error Correction Methods Project (Practical 7)
# This script sets up the project and installs dependencies in the global virtual environment

echo "Setting up Hamming Code Error Correction Methods Project (Practical 7)..."
echo "======================================================================="

# Check if we're in the right directory
if [ ! -f "hamming_code.py" ]; then
    echo "Error: Please run this script from the Practical7-HammingCode directory"
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
    cd Practical7-HammingCode
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from global requirements
echo "Installing dependencies from global requirements..."
pip install -r ../requirements.txt

echo ""
echo "Setup complete!"
echo "==============="
echo ""
echo "Hamming Code implementation uses only Python standard library."
echo "No external dependencies required."
echo ""
echo "To activate the global virtual environment, run:"
echo "  source ../venv/bin/activate"
echo ""
echo "To run the main program:"
echo "  python hamming_code.py"
echo ""
echo "To run tests:"
echo "  python test_hamming_code.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
