# Hosyond 3.5" Emergency Display Setup

This guide is specifically for your [Hosyond 3.5 Inch 480x320 Touch Screen](https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3).

## 🖥️ Your Hardware Specs:
- **Resolution:** 480x320 pixels
- **Interface:** SPI (Fmax: 32MHz)
- **Touch:** Resistive touch control
- **Compatibility:** Pi A, B, A+, B+, 2B, 3B, 3B+, 4B, 5
- **Connection:** GPIO direct plug

## 🚀 Quick Start

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install python3-pygame python3-pip python3-requests -y
pip3 install pygame requests
```

### 2. Set Up Display Driver
```bash
# Download Hosyond driver (if not already installed)
git clone https://github.com/hosyond/LCD-show
cd LCD-show/
chmod +x LCD35-show
sudo ./LCD35-show
```

### 3. Run Emergency Display
```bash
# Get your user ID from the web app first
python3 hosyond_emergency.py YOUR_USER_ID
```

## 📱 Getting Your User ID

1. Open web app: http://localhost:3003 (or your network IP)
2. Login and go to Dashboard → Emergency
3. Copy the User ID from the emergency access section
4. Use it in the Pi command

## 🎯 Display Layout (480x320)

```
┌─────────────────────────────────────────────┐
│    🚨 EMERGENCY MEDICAL INFO        ●       │ ← Header (60px)
├─────────────────────────────────────────────┤
│        🩸 BLOOD TYPE: O+                    │ ← Blood Type (35px)
├─────────────────────────────────────────────┤
│ ⚠️ CRITICAL ALLERGIES                       │
│ ┌─────────────────────────────────────────┐ │
│ │ Peanuts - LIFE-THREATENING             │ │ ← Allergies
│ │ Reaction: Anaphylaxis                  │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 💊 ACTIVE MEDICATIONS                       │
│ ┌─────────────────────────────────────────┐ │
│ │ Lisinopril - 10mg                      │ │ ← Medications
│ │ Frequency: Daily                       │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 📞 EMERGENCY CONTACT                        │
│ ┌─────────────────────────────────────────┐ │
│ │ Jane Doe (Spouse)                      │ │ ← Primary Contact
│ │ (555) 123-4567                         │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│        TOUCH SCREEN TO REFRESH DATA         │ ← Instructions (25px)
└─────────────────────────────────────────────┘
```

## 🎮 Controls

- **Touch Screen:** Refresh data from Firebase
- **ESC Key:** Exit application
- **R Key:** Manual data refresh

## 🔧 Hosyond-Specific Features

### Touch Calibration
The script is calibrated for resistive touch:
- **Top area touch:** Refreshes data
- **Bottom area touch:** Emergency mode (future feature)

### Display Optimization
- **30 FPS refresh rate** (optimal for Hosyond hardware)
- **Large fonts** for emergency visibility
- **High contrast colors** for medical urgency
- **Efficient rendering** for smooth performance

## 🛠️ Troubleshooting

### Display Issues
```bash
# Check if display is detected
sudo dmesg | grep -i spi

# Test display
sudo apt install fbi
sudo fbi -T 1 -d /dev/fb1 test_image.jpg
```

### Touch Not Working
```bash
# Check touch device
sudo apt install evtest
sudo evtest
# Select your touch device and test
```

### No Data Displayed
```bash
# Test network connection
ping google.com

# Test Firebase connection
curl "https://firestore.googleapis.com/v1/projects/heat-2cc8c/databases/(default)/documents/test"

# Check user has medical data in web app
```

## 🔄 Auto-Start on Boot

Create startup script:
```bash
nano ~/emergency_start.sh
```

Content:
```bash
#!/bin/bash
sleep 30  # Wait for network
cd /home/pi/hackgtmergency-2/pi-display
python3 hosyond_emergency.py YOUR_USER_ID
```

Make executable and add to startup:
```bash
chmod +x ~/emergency_start.sh
echo "/home/pi/emergency_start.sh &" | sudo tee -a /etc/rc.local
```

## 📊 Performance Tips

For best performance on your Hosyond display:

1. **Resolution:** Already optimized for 480x320
2. **Frame Rate:** 30 FPS for smooth touch response
3. **Memory:** Efficient font loading and caching
4. **Network:** 15-second timeout for Firebase requests

## 🎯 Emergency Features

- **Offline Mode:** Caches last known data
- **Touch Refresh:** Simple tap to update
- **High Visibility:** Large fonts, red/green color coding
- **Critical Priority:** Shows most important info first

Perfect for first responders using your [Hosyond touchscreen display](https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3)!
