#!/bin/bash

# Raspberry Pi Emergency Display Setup Script
# For use with 480x320 touchscreen display

echo "Setting up Emergency Display System..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python dependencies
sudo apt-get install -y python3-pip python3-pygame python3-dev

# Install GPIO library
sudo apt-get install -y python3-rpi.gpio

# Install Python packages
pip3 install -r requirements.txt

# Create cache directory
mkdir -p ~/.emergency_cache

# Set up autostart (optional)
read -p "Do you want to set up autostart on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Get user ID
    read -p "Enter your Firebase User ID: " USER_ID
    read -p "Enter your 4-digit PIN: " PIN
    
    # Create autostart script
    cat > ~/emergency_autostart.sh <<EOF
#!/bin/bash
sleep 10
cd /home/pi/emergency-display
python3 emergency_display.py $USER_ID $PIN
EOF
    
    chmod +x ~/emergency_autostart.sh
    
    # Add to rc.local
    sudo sed -i -e '$i /home/pi/emergency_autostart.sh &\n' /etc/rc.local
    
    echo "Autostart configured!"
fi

# Set permissions
chmod +x emergency_display.py

echo "Setup complete!"
echo ""
echo "To run the emergency display:"
echo "  python3 emergency_display.py <user_id> [pin]"
echo ""
echo "Connect emergency button to GPIO pin 17 (BCM)"
echo "Display should be connected via HDMI or DSI"
