#!/bin/bash

echo "🚨 HEAT Emergency Display - EZ Setup (No Pipes!)"
echo "================================================"

# Get user ID as parameter
if [ -z "$1" ]; then
    echo "❌ Please provide your User ID"
    echo ""
    echo "Usage: ./ez-setup.sh YOUR_USER_ID"
    echo ""
    echo "📱 Get your User ID from the web app dashboard"
    exit 1
fi

USER_ID="$1"
echo "🆔 Setting up for User ID: $USER_ID"

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt update -qq
sudo apt install -y python3-pygame python3-pip python3-requests wget

# Install Python packages
pip3 install pygame requests

# Download emergency display script
echo "📥 Downloading emergency display..."
cd /home/pi

# Remove existing directory if it exists
if [ -d "pocket-doc-emergency-pi" ]; then
    echo "🗑️  Removing existing directory..."
    rm -rf pocket-doc-emergency-pi
fi

# Download fresh copy
echo "📂 Downloading fresh files..."
wget https://raw.githubusercontent.com/Garyxue213/pocket-doc-emergency-pi/main/emergency.py
chmod +x emergency.py

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 Starting Emergency Display..."
echo "   User ID: $USER_ID"
echo "   Touch screen to refresh"
echo "   Press ESC to exit"
echo ""

# Start the emergency display
python3 emergency.py "$USER_ID"
