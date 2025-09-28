# 🚨 Simple Raspberry Pi Emergency Display Commands

## 🎯 **SUPER EASY - Multiple Options!**

### **Step 1: Get Your User ID**
1. Go to your web app: http://localhost:3003/dashboard
2. Look for the **"Raspberry Pi Setup"** card
3. Click **"Copy"** button to copy your User ID

### **Step 2: Choose Your Setup Method**

#### **🚀 Option A: One Command (with pipe)**
```bash
curl -sSL https://raw.githubusercontent.com/Garyxue213/pocket-doc-emergency-pi/main/quick-start.sh | bash -s YOUR_USER_ID
```

#### **⚡ Option B: No Pipes Needed**
```bash
# Download and run (no pipe character needed):
wget https://raw.githubusercontent.com/Garyxue213/pocket-doc-emergency-pi/main/ez-setup.sh
chmod +x ez-setup.sh
./ez-setup.sh YOUR_USER_ID
```

#### **📋 Option C: Manual Steps**
```bash
# Step by step:
wget https://raw.githubusercontent.com/Garyxue213/pocket-doc-emergency-pi/main/emergency.py
sudo apt install python3-pygame python3-requests -y
python3 emergency.py YOUR_USER_ID
```

**All methods do the same thing - choose what's easiest for you! 🎉**

---

## 📋 **Example with Real User ID**

If your User ID is: `abc123def456ghi789`

```bash
# Your exact command:
python3 hosyond_emergency.py abc123def456ghi789
```

---

## 🖥️ **What You'll See on Your Hosyond Display**

```
┌─────────────────────────────────────────────┐
│    🚨 EMERGENCY MEDICAL INFO        ●       │
├─────────────────────────────────────────────┤
│        🩸 BLOOD TYPE: O+                    │
├─────────────────────────────────────────────┤
│ ⚠️ CRITICAL ALLERGIES                       │
│ │ Peanuts - LIFE-THREATENING             │ │
├─────────────────────────────────────────────┤
│ 💊 ACTIVE MEDICATIONS                       │
│ │ Lisinopril - 10mg Daily               │ │
├─────────────────────────────────────────────┤
│ 📞 EMERGENCY CONTACT                        │
│ │ Jane Doe (555) 123-4567                │ │
├─────────────────────────────────────────────┤
│        TOUCH SCREEN TO REFRESH             │
└─────────────────────────────────────────────┘
```

---

## 🔧 **Troubleshooting**

### **No Data Showing?**
1. Make sure you added medical info in the web app
2. Check your User ID is correct (copy from dashboard)
3. Ensure Pi has internet connection

### **Display Not Working?**
```bash
# Install display driver for Hosyond screen:
git clone https://github.com/hosyond/LCD-show
cd LCD-show && sudo ./LCD35-show
```

### **Touch Not Working?**
```bash
# Test touch:
sudo apt install evtest
sudo evtest
# Select your touch device
```

---

## 🎯 **For Hackathon Demo**

1. **Show Web App** - Complete health management
2. **Copy User ID** - One-click copy from dashboard
3. **Run Pi Command** - Simple paste and run
4. **Live Display** - Real emergency information
5. **Touch Demo** - Interactive refresh

**Perfect for impressing judges with real hardware integration! 🏆**
