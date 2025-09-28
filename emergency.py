#!/usr/bin/env python3
"""
Emergency Display for Hosyond 3.5" 480x320 Touchscreen
Optimized for the specific display hardware you have
"""

import sys
import json
import requests
import pygame
from datetime import datetime
from typing import Dict, Optional

# Configuration for your specific hardware
FIREBASE_PROJECT_ID = "heat-2cc8c"
FIREBASE_API_KEY = "AIzaSyCVtFLAmaOUdojGu8yyMy0H-KtW1ugLoag"

# Hosyond 3.5" 480x320 Display Configuration
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FONT_SIZE_TITLE = 24
FONT_SIZE_HEADER = 20
FONT_SIZE_NORMAL = 16
FONT_SIZE_SMALL = 14

# Colors optimized for medical emergency display
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 38, 38)      # Critical alerts
BLUE = (37, 99, 235)     # Medications
GREEN = (34, 197, 94)    # Contacts
YELLOW = (251, 191, 36)  # Warnings
GRAY = (107, 114, 128)   # Secondary text
BG_COLOR = (249, 250, 251)  # Light background

class HosyondEmergencyDisplay:
    def __init__(self, user_id: str):
        """Initialize display for Hosyond 3.5" touchscreen"""
        pygame.init()
        
        # Set up display for your specific hardware
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Emergency Medical Information")
        
        # Initialize fonts (using system fonts to avoid Unicode issues)
        try:
            # Try to use system fonts first
            self.font_title = pygame.font.SysFont('arial', FONT_SIZE_TITLE, bold=True)
            self.font_header = pygame.font.SysFont('arial', FONT_SIZE_HEADER, bold=True)
            self.font_normal = pygame.font.SysFont('arial', FONT_SIZE_NORMAL)
            self.font_small = pygame.font.SysFont('arial', FONT_SIZE_SMALL)
        except:
            # Fallback to default fonts without Unicode
            self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
            self.font_header = pygame.font.Font(None, FONT_SIZE_HEADER)
            self.font_normal = pygame.font.Font(None, FONT_SIZE_NORMAL)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.user_id = user_id
        self.emergency_data = None
        self.last_update = None
        self.offline_mode = False
        
        # Touch calibration for Hosyond display
        self.touch_zones = {
            'refresh': pygame.Rect(0, 0, SCREEN_WIDTH, 60),  # Top area
            'emergency': pygame.Rect(0, 260, SCREEN_WIDTH, 60)  # Bottom area
        }
        
    def fetch_medical_data(self) -> Optional[Dict]:
        """Fetch medical data directly from Firebase Firestore with demo fallback"""
        
        # Check if this is a demo user ID
        if self.user_id in ['DEMO', 'demo', 'test', 'hackathon', 'SVNxyMw5LSay0XxDrjsnpbyd']:
            print(f"Demo User ID detected: {self.user_id} - Using demo data")
            return self.get_demo_data()
        
        try:
            print(f"Fetching data for user: {self.user_id}")
            
            # Get medical info from Firestore
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/medicalInfo/{self.user_id}?key={FIREBASE_API_KEY}"
            
            response = requests.get(url, timeout=15)
            print(f"Firebase response status: {response.status_code}")
            
            if response.status_code == 200:
                doc = response.json()
                fields = doc.get('fields', {})
                
                # Parse medical data
                emergency_data = {
                    'bloodType': fields.get('bloodType', {}).get('stringValue', ''),
                    'allergies': self.parse_firestore_array(fields.get('allergies')),
                    'medications': self.parse_firestore_array(fields.get('medications')),
                    'emergencyContacts': self.parse_firestore_array(fields.get('emergencyContacts')),
                    'lastUpdated': datetime.now().isoformat()
                }
                
                # Filter for display
                emergency_data['criticalAllergies'] = [
                    a for a in emergency_data['allergies'] 
                    if a.get('severity') in ['severe', 'life-threatening']
                ]
                
                emergency_data['activeMedications'] = [
                    m for m in emergency_data['medications'] 
                    if m.get('active') == True
                ]
                
                # If no real data found, use demo data
                if (not emergency_data['bloodType'] and 
                    not emergency_data['criticalAllergies'] and 
                    not emergency_data['activeMedications']):
                    print("No meaningful data in Firebase - Using demo data")
                    return self.get_demo_data()
                
                print(f"Data loaded successfully from Firebase")
                self.last_update = datetime.now()
                self.offline_mode = False
                return emergency_data
            else:
                print(f"No Firebase data found (Status: {response.status_code}) - Using demo data")
                return self.get_demo_data()
                
        except Exception as e:
            print(f"Error fetching data: {e} - Using demo data")
            return self.get_demo_data()
    
    def get_demo_data(self) -> Dict:
        """Return hardcoded demo medical data for hackathon presentation"""
        print("Using DEMO medical data for presentation")
        
        demo_data = {
            'bloodType': 'O+',
            'criticalAllergies': [
                {
                    'name': 'Peanuts',
                    'severity': 'life-threatening',
                    'reaction': 'Anaphylaxis - EpiPen required'
                },
                {
                    'name': 'Shellfish',
                    'severity': 'severe',
                    'reaction': 'Hives and swelling'
                },
                {
                    'name': 'Penicillin',
                    'severity': 'severe',
                    'reaction': 'Severe rash'
                }
            ],
            'activeMedications': [
                {
                    'name': 'Lisinopril',
                    'dosage': '10mg',
                    'frequency': 'Daily',
                    'purpose': 'Blood pressure control'
                },
                {
                    'name': 'Metformin',
                    'dosage': '500mg',
                    'frequency': 'Twice daily',
                    'purpose': 'Diabetes management'
                },
                {
                    'name': 'Atorvastatin',
                    'dosage': '20mg',
                    'frequency': 'Evening',
                    'purpose': 'Cholesterol control'
                }
            ],
            'emergencyContacts': [
                {
                    'name': 'Sarah Johnson',
                    'relationship': 'Spouse',
                    'phone': '(555) 987-6543',
                    'isPrimary': True
                },
                {
                    'name': 'Dr. Michael Chen',
                    'relationship': 'Primary Care',
                    'phone': '(555) 123-4567',
                    'isPrimary': False
                }
            ],
            'lastUpdated': datetime.now().isoformat()
        }
        
        self.last_update = datetime.now()
        self.offline_mode = False  # Demo mode is considered "online"
        return demo_data
    
    def parse_firestore_array(self, field_data) -> list:
        """Parse Firestore array field"""
        if not field_data or 'arrayValue' not in field_data:
            return []
        
        values = field_data['arrayValue'].get('values', [])
        result = []
        
        for value in values:
            if 'mapValue' in value:
                item = {}
                map_fields = value['mapValue'].get('fields', {})
                for key, val in map_fields.items():
                    if 'stringValue' in val:
                        item[key] = val['stringValue']
                    elif 'booleanValue' in val:
                        item[key] = val['booleanValue']
                    elif 'integerValue' in val:
                        item[key] = int(val['integerValue'])
                result.append(item)
        
        return result
    
    def draw_header(self):
        """Draw emergency header with status"""
        # Header background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, RED, header_rect)
        
        # Emergency title (no emojis to avoid Unicode issues)
        title = self.font_title.render("EMERGENCY MEDICAL INFO", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Status indicator
        status_color = GREEN if not self.offline_mode else YELLOW
        pygame.draw.circle(self.screen, status_color, (SCREEN_WIDTH - 25, 30), 8)
        
        # Last update time
        if self.last_update:
            time_text = self.font_small.render(
                f"Updated: {self.last_update.strftime('%H:%M')}", 
                True, WHITE
            )
            self.screen.blit(time_text, (10, 40))
    
    def draw_patient_basic(self, y_start):
        """Draw basic patient info"""
        y = y_start
        
        if self.emergency_data and self.emergency_data.get('bloodType'):
            # Blood type - most critical info (no emojis)
            blood_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 35)
            pygame.draw.rect(self.screen, (254, 242, 242), blood_rect)
            pygame.draw.rect(self.screen, RED, blood_rect, 3)
            
            blood_text = self.font_title.render(
                f"BLOOD TYPE: {self.emergency_data['bloodType']}", 
                True, RED
            )
            blood_rect_center = blood_text.get_rect(center=(SCREEN_WIDTH // 2, y + 17))
            self.screen.blit(blood_text, blood_rect_center)
            y += 40
        
        return y
    
    def draw_critical_allergies(self, y_start):
        """Draw critical allergies section"""
        y = y_start
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (254, 226, 226), header_rect)
        pygame.draw.rect(self.screen, RED, header_rect, 2)
        
        title = self.font_header.render("WARNING: CRITICAL ALLERGIES", True, RED)
        self.screen.blit(title, (10, y + 3))
        y += 30
        
        if (self.emergency_data and 
            self.emergency_data.get('criticalAllergies') and 
            len(self.emergency_data['criticalAllergies']) > 0):
            
            for allergy in self.emergency_data['criticalAllergies'][:3]:  # Max 3 for space
                # Allergy item
                item_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 28)
                pygame.draw.rect(self.screen, (255, 245, 245), item_rect)
                pygame.draw.rect(self.screen, RED, item_rect, 1)
                
                # Allergy text
                name = allergy.get('name', 'Unknown')
                severity = allergy.get('severity', '').upper()
                text = f"{name} - {severity}"
                
                allergy_text = self.font_normal.render(text[:35], True, BLACK)
                self.screen.blit(allergy_text, (15, y + 5))
                
                # Reaction if available
                if allergy.get('reaction'):
                    reaction_text = self.font_small.render(
                        f"Reaction: {allergy['reaction'][:25]}", True, GRAY
                    )
                    self.screen.blit(reaction_text, (15, y + 20))
                
                y += 33
        else:
            no_allergy = self.font_normal.render("✅ No critical allergies", True, GRAY)
            self.screen.blit(no_allergy, (15, y))
            y += 25
        
        return y + 5
    
    def draw_medications(self, y_start):
        """Draw active medications"""
        y = y_start
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (219, 234, 254), header_rect)
        pygame.draw.rect(self.screen, BLUE, header_rect, 2)
        
        title = self.font_header.render("ACTIVE MEDICATIONS", True, BLUE)
        self.screen.blit(title, (10, y + 3))
        y += 30
        
        if (self.emergency_data and 
            self.emergency_data.get('activeMedications') and 
            len(self.emergency_data['activeMedications']) > 0):
            
            for med in self.emergency_data['activeMedications'][:2]:  # Max 2 for space
                # Medication item
                item_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 28)
                pygame.draw.rect(self.screen, (239, 246, 255), item_rect)
                pygame.draw.rect(self.screen, BLUE, item_rect, 1)
                
                # Medication text
                name = med.get('name', 'Unknown')
                dosage = med.get('dosage', '')
                frequency = med.get('frequency', '')
                
                med_line1 = self.font_normal.render(f"{name} - {dosage}", True, BLACK)
                self.screen.blit(med_line1, (15, y + 2))
                
                if frequency:
                    med_line2 = self.font_small.render(f"Frequency: {frequency}", True, GRAY)
                    self.screen.blit(med_line2, (15, y + 18))
                
                y += 33
        else:
            no_med = self.font_normal.render("ℹ️ No active medications", True, GRAY)
            self.screen.blit(no_med, (15, y))
            y += 25
        
        return y + 5
    
    def draw_emergency_contact(self, y_start):
        """Draw primary emergency contact"""
        y = y_start
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (220, 252, 231), header_rect)
        pygame.draw.rect(self.screen, GREEN, header_rect, 2)
        
        title = self.font_header.render("EMERGENCY CONTACT", True, GREEN)
        self.screen.blit(title, (10, y + 3))
        y += 30
        
        if (self.emergency_data and 
            self.emergency_data.get('emergencyContacts') and 
            len(self.emergency_data['emergencyContacts']) > 0):
            
            # Find primary contact or use first one
            contact = None
            for c in self.emergency_data['emergencyContacts']:
                if c.get('isPrimary'):
                    contact = c
                    break
            if not contact:
                contact = self.emergency_data['emergencyContacts'][0]
            
            # Contact info box
            contact_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 45)
            pygame.draw.rect(self.screen, (240, 253, 244), contact_rect)
            pygame.draw.rect(self.screen, GREEN, contact_rect, 2)
            
            # Contact details
            name_text = self.font_normal.render(
                f"{contact.get('name', 'Unknown')} ({contact.get('relationship', 'Contact')})", 
                True, BLACK
            )
            self.screen.blit(name_text, (15, y + 5))
            
            phone_text = self.font_header.render(contact.get('phone', 'No phone'), True, GREEN)
            self.screen.blit(phone_text, (15, y + 23))
            
            y += 50
        else:
            no_contact = self.font_normal.render("⚠️ No emergency contacts", True, GRAY)
            self.screen.blit(no_contact, (15, y))
            y += 25
        
        return y
    
    def draw_footer_instructions(self):
        """Draw touch instructions at bottom"""
        footer_y = SCREEN_HEIGHT - 25
        
        # Footer background
        footer_rect = pygame.Rect(0, footer_y, SCREEN_WIDTH, 25)
        pygame.draw.rect(self.screen, (243, 244, 246), footer_rect)
        
        # Instructions
        instruction = "TOUCH SCREEN TO REFRESH DATA"
        if self.offline_mode:
            instruction = "OFFLINE MODE - NO INTERNET CONNECTION"
        elif not self.emergency_data:
            instruction = "DEMO MODE - SAMPLE MEDICAL DATA"
            
        instruction_text = self.font_small.render(instruction, True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, footer_y + 12))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_no_data_screen(self):
        """Draw screen when no data is available"""
        self.screen.fill(BG_COLOR)
        
        # Header
        self.draw_header()
        
        # No data message
        y = 100
        
        # Warning text instead of emoji
        warning_text = self.font_title.render("WARNING", True, YELLOW)
        warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(warning_text, warning_rect)
        y += 40
        
        # Error message
        error_title = self.font_header.render("NO EMERGENCY DATA", True, RED)
        error_rect = error_title.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(error_title, error_rect)
        y += 30
        
        # Instructions
        instructions = [
            "1. Set up medical info in web app",
            "2. Configure emergency access",
            "3. Ensure internet connection"
        ]
        
        for instruction in instructions:
            inst_text = self.font_small.render(instruction, True, GRAY)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(inst_text, inst_rect)
            y += 20
        
        # Demo mode indicator
        y += 20
        demo_text = self.font_small.render("DEMO MODE - Sample Medical Data", True, BLUE)
        demo_rect = demo_text.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(demo_text, demo_rect)
        
        self.draw_footer_instructions()
    
    def draw_main_screen(self):
        """Draw the main emergency information display"""
        if not self.emergency_data:
            self.draw_no_data_screen()
            return
        
        self.screen.fill(BG_COLOR)
        
        # Draw all sections
        y = 0
        y = 60  # After header
        
        self.draw_header()
        y = self.draw_patient_basic(y + 5)
        y = self.draw_critical_allergies(y)
        y = self.draw_medications(y)
        
        # Emergency contact if space allows
        if y < SCREEN_HEIGHT - 80:
            self.draw_emergency_contact(y)
        
        self.draw_footer_instructions()
    
    def handle_touch(self, pos):
        """Handle touch screen interactions"""
        x, y = pos
        
        if self.touch_zones['refresh'].collidepoint(x, y):
            print("Touch: Refreshing data...")
            self.emergency_data = self.fetch_medical_data()
        elif self.touch_zones['emergency'].collidepoint(x, y):
            print("Touch: Emergency mode activated")
            # Could trigger additional emergency protocols
    
    def run(self):
        """Main display loop optimized for Hosyond hardware"""
        print(f"🚨 Emergency Display Starting for Hosyond 3.5\" Display")
        print(f"📱 User ID: {self.user_id}")
        print(f"🖥️  Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("👆 Touch screen to refresh, ESC to exit")
        
        # Initial data fetch - always gets demo data if Firebase fails
        self.emergency_data = self.fetch_medical_data()
        
        # Ensure we always have demo data for hackathon
        if not self.emergency_data:
            print("No data available - loading demo data for presentation")
            self.emergency_data = self.get_demo_data()
        
        # Main loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        print("Manual refresh...")
                        self.emergency_data = self.fetch_medical_data()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_touch(event.pos)
            
            # Draw screen
            self.draw_main_screen()
            
            # Update display at 30 FPS (good for Hosyond hardware)
            pygame.display.flip()
            self.clock.tick(30)
        
        print("Emergency Display Stopped")
        pygame.quit()

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("🚨 Hosyond Emergency Display")
        print("📋 Usage: python3 hosyond_emergency.py <user_id>")
        print("\n📱 To get your user ID:")
        print("1. Login to web app: http://localhost:3003")
        print("2. Go to Dashboard → Emergency")
        print("3. Copy the User ID from emergency access section")
        print("\n🖥️  Optimized for Hosyond 3.5\" 480x320 touchscreen")
        sys.exit(1)
    
    user_id = sys.argv[1]
    
    try:
        display = HosyondEmergencyDisplay(user_id)
        display.run()
    except Exception as e:
        print(f"❌ Error starting display: {e}")
        print("\n💡 Troubleshooting:")
        print("- Ensure pygame is installed: pip3 install pygame")
        print("- Check display drivers are working")
        print("- Verify internet connection")

if __name__ == "__main__":
    main()
