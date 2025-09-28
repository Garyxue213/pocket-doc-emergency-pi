# Complete Raspberry Pi Setup for Emergency Display

## 🥧 **Starting from Scratch - Raspberry Pi Setup**

### **Step 1: Prepare Your Raspberry Pi**

1. **Flash Raspberry Pi OS:**
   - Download [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
   - Flash "Raspberry Pi OS (32-bit)" to SD card
   - Enable SSH and set username/password in advanced options

2. **Boot Your Pi:**
   - Insert SD card and boot
   - Connect to Wi-Fi
   - Enable SSH: `sudo systemctl enable ssh`

### **Step 2: Install Hosyond Display Driver**

Your [Hosyond 3.5" 480x320 display](https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3) needs specific drivers:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install git if not present
sudo apt install git -y

# Download Hosyond LCD driver
git clone https://github.com/hosyond/LCD-show
cd LCD-show/

# Make executable and install 3.5" driver
chmod +x LCD35-show
sudo ./LCD35-show

# Pi will reboot automatically
```

**After reboot, your 480x320 touchscreen should be working!**

### **Step 3: Clone Your Health App**

```bash
# Clone your project
git clone https://github.com/YOUR_USERNAME/hackgtmergency-2.git
cd hackgtmergency-2/pi-display

# OR if you don't have GitHub, create manually:
mkdir -p ~/emergency-display
cd ~/emergency-display

# Copy the Python files (you'll need to transfer these)
```

### **Step 4: Install Python Dependencies**

```bash
# Install required packages
sudo apt install python3-pygame python3-pip python3-requests -y

# Install Python packages
pip3 install pygame requests
```

### **Step 5: Get Your User ID**

From your web app (running on your computer):

1. Go to: `http://YOUR_COMPUTER_IP:3003/dashboard/emergency`
2. Copy the **User ID** from the emergency access section
3. Note it down (looks like: `abc123def456ghi789`)

### **Step 6: Test the Display**

```bash
# Test with your actual user ID
python3 hosyond_emergency.py YOUR_USER_ID

# Example:
python3 hosyond_emergency.py abc123def456ghi789
```

## 📂 **If You Don't Have Git Access**

Create the files manually on your Pi:

### **Create the main script:**
```bash
nano ~/emergency_display.py
```

Then copy the content from `hosyond_emergency.py` into this file.

### **Or use wget to download:**
```bash
# If you put files on GitHub or a server
wget https://raw.githubusercontent.com/YOUR_REPO/pi-display/hosyond_emergency.py
```

## 🔧 **Manual File Transfer Methods**

### **Option 1: SCP (if SSH enabled)**
From your computer:
```bash
scp pi-display/hosyond_emergency.py pi@YOUR_PI_IP:~/
```

### **Option 2: USB Drive**
1. Copy `hosyond_emergency.py` to USB drive
2. Insert USB into Pi
3. Copy file: `cp /media/pi/USB_DRIVE/hosyond_emergency.py ~/`

### **Option 3: Direct Copy-Paste**
1. SSH into Pi: `ssh pi@YOUR_PI_IP`
2. Create file: `nano ~/emergency_display.py`
3. Copy-paste the Python code
4. Save: `Ctrl+X, Y, Enter`

## 🖥️ **Hosyond Display Configuration**

Your display should work with these settings:
- **Resolution:** 480x320 (handled automatically)
- **Touch:** Resistive (calibrated in script)
- **Orientation:** Landscape
- **Interface:** SPI via GPIO

## 🚀 **Auto-Start Setup**

To start automatically when Pi boots:

```bash
# Create startup script
nano ~/start_emergency.sh
```

Content:
```bash
#!/bin/bash
sleep 30  # Wait for network
cd ~/emergency-display
python3 hosyond_emergency.py YOUR_USER_ID
```

```bash
# Make executable
chmod +x ~/start_emergency.sh

# Add to startup
echo "/home/pi/start_emergency.sh &" | sudo tee -a /etc/rc.local
```

## 🎯 **Expected Result**

Your Hosyond 480x320 display will show:
- 🩸 **Blood Type** in large red text
- ⚠️ **Critical Allergies** with severity levels
- 💊 **Active Medications** with dosages
- 📞 **Emergency Contact** with phone number
- **Touch to refresh** functionality

## 🔍 **Troubleshooting**

### **Display Not Working:**
```bash
# Check if display driver installed
ls /dev/fb1

# Test basic display
sudo fbi -T 1 -d /dev/fb1 /opt/vc/src/hello_pi/hello_fft/hello_fft
```

### **No Medical Data:**
1. Ensure you've added medical info in web app
2. Check internet connection on Pi
3. Verify User ID is correct

### **Touch Not Responding:**
```bash
# Check touch device
sudo apt install evtest
sudo evtest
# Test touch input
```

Your Hosyond display is perfect for this emergency medical application! 🏥
