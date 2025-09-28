#!/bin/bash

echo "🚨 HEAT Emergency Display - Super Quick Start"
echo "============================================="

# Check if we're on a Pi
if ! command -v gpio &> /dev/null; then
    echo "⚠️  Warning: This doesn't look like a Raspberry Pi"
    echo "   Continuing anyway for testing..."
fi

# Get user ID as parameter
if [ -z "$1" ]; then
    echo "❌ Please provide your User ID"
    echo ""
    echo "Usage: ./quick-start.sh YOUR_USER_ID"
    echo ""
    echo "📱 Get your User ID from:"
    echo "   http://YOUR_COMPUTER_IP:3003/dashboard"
    echo "   (Click 'Copy' in Raspberry Pi Setup card)"
    exit 1
fi

USER_ID="$1"
echo "🆔 Using User ID: $USER_ID"

# Quick install if needed
if ! command -v python3 &> /dev/null || ! python3 -c "import pygame" &> /dev/null; then
    echo "📦 Installing dependencies..."
    sudo apt update -qq
    sudo apt install -y python3-pygame python3-pip python3-requests
    pip3 install pygame requests
fi

# Download latest emergency display
echo "📥 Getting latest emergency display..."
cd /home/pi

# Remove old version
rm -rf emergency-display 2>/dev/null

# Download fresh copy
wget -q https://raw.githubusercontent.com/Garyxue213/pocket-doc-emergency-pi/main/emergency.py -O emergency.py
chmod +x emergency.py

echo "✅ Setup complete!"
echo ""
echo "🚀 Starting emergency display..."
echo "   Touch screen to refresh data"
echo "   Press ESC to exit"
echo ""

# Run the emergency display
python3 emergency.py "$USER_ID"
