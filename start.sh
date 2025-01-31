#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y ffmpeg
    elif [ -f /etc/arch-release ]; then
        sudo pacman -S ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "Please install ffmpeg manually for your system"
        exit 1
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip3 install -r requirements.txt
fi

# Run the WebUI
echo "Starting WebUI..."
python3 webui.py
