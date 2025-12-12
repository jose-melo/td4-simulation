#!/bin/bash

# Startup script for Bin Packing Visualizer Flask App

echo "=================================="
echo "Bin Packing Visualizer - Startup"
echo "=================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the Flask server
echo ""
echo "Starting Flask server..."
echo "Access the app at: http://localhost:5001"
echo "Press Ctrl+C to stop"
echo ""

python app.py
