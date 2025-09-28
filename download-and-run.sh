#!/bin/bash

echo "🚨 HEAT Emergency Display - Quick Setup"
echo "========================================"

# Update system
echo "📦 Updating system packages..."
sudo apt update -qq

# Install required packages
echo "🐍 Installing Python dependencies..."
sudo apt install -y python3-pygame python3-pip python3-requests git

# Install Python packages
echo "📚 Installing Python libraries..."
pip3 install pygame requests --quiet

# Download emergency display files
echo "📥 Downloading emergency display system..."

# Remove existing directory if it exists
if [ -d "/home/pi/emergency-display" ]; then
    echo "🗑️  Removing existing directory..."
    rm -rf /home/pi/emergency-display
fi

# Create fresh directory and clone
echo "📂 Creating fresh installation..."
mkdir -p /home/pi/emergency-display
cd /home/pi

# Clone with force
git clone https://github.com/Garyxue213/pocket-doc-emergency-pi.git emergency-display 2>/dev/null || {
    echo "📥 Updating existing repository..."
    cd emergency-display
    git fetch origin
    git reset --hard origin/main
    cd ..
}

# Make scripts executable
chmod +x /home/pi/emergency-display/*.py

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🎯 To start emergency display:"
echo "   cd /home/pi/emergency-display"
echo "   python3 emergency.py YOUR_USER_ID"
echo ""
echo "📱 Get your User ID from:"
echo "   http://YOUR_COMPUTER_IP:3003/dashboard"
echo "   (Look for 'Raspberry Pi Setup' card)"
echo ""
echo "🖥️  Optimized for Hosyond 3.5\" 480x320 touchscreen"
echo "👆 Touch screen to refresh data"
echo ""
