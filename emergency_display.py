#!/usr/bin/env python3
"""
Raspberry Pi Emergency Display Script
For 480x320 touchscreen display
Fetches encrypted emergency data from Firebase and displays it
"""

import os
import sys
import time
import json
import hashlib
import base64
from datetime import datetime
from typing import Dict, Optional, List
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *

# Configuration
FIREBASE_PROJECT_ID = "heat-2cc8c"
FIREBASE_API_KEY = "AIzaSyCVtFLAmaOUdojGu8yyMy0H-KtW1ugLoag"
USER_ID = ""  # Set this to the user's ID
EMERGENCY_PIN = "1234"  # Default PIN, should be configured

# Display Configuration for 480x320
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# GPIO Configuration for emergency button
EMERGENCY_BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(EMERGENCY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 53, 69)
BLUE = (0, 123, 255)
GREEN = (40, 167, 69)
YELLOW = (255, 193, 7)
GRAY = (108, 117, 125)
BG_COLOR = (248, 249, 250)

class EmergencyDisplay:
    def __init__(self):
        """Initialize the emergency display system"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Emergency Medical Information")
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.emergency_mode = False
        self.emergency_data = None
        self.last_update = None
        self.offline_cache = self.load_offline_cache()
        
    def load_offline_cache(self) -> Optional[Dict]:
        """Load cached emergency data for offline use"""
        cache_file = "/home/pi/.emergency_cache.json"
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
        return None
    
    def save_offline_cache(self, data: Dict):
        """Save emergency data to offline cache"""
        cache_file = "/home/pi/.emergency_cache.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def decrypt_data(self, encrypted_data: str, pin: str) -> Optional[Dict]:
        """Decrypt emergency data using PIN"""
        try:
            # Decode base64
            combined = base64.b64decode(encrypted_data)
            
            # Extract components (matching the TypeScript implementation)
            salt_length = 64
            iv_length = 12
            tag_length = 16
            
            salt = combined[:salt_length]
            iv = combined[salt_length:salt_length + iv_length]
            tag = combined[salt_length + iv_length:salt_length + iv_length + tag_length]
            encrypted = combined[salt_length + iv_length + tag_length:]
            
            # Derive key from PIN
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(pin.encode())
            
            # Decrypt
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(iv, encrypted + tag, None)
            
            return json.loads(decrypted.decode('utf-8'))
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def fetch_emergency_data(self) -> Optional[Dict]:
        """Fetch emergency data from Firebase"""
        try:
            # Try to get medical info first (more likely to exist)
            medical_url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/medicalInfo/{USER_ID}?key={FIREBASE_API_KEY}"
            
            response = requests.get(medical_url, timeout=10)
            if response.status_code == 200:
                doc = response.json()
                fields = doc.get('fields', {})
                
                # Parse medical info and create emergency data
                emergency_data = {
                    'criticalAllergies': self.parse_array_field(fields.get('allergies')),
                    'criticalMedications': self.parse_array_field(fields.get('medications')),
                    'emergencyContacts': self.parse_array_field(fields.get('emergencyContacts')),
                    'bloodType': fields.get('bloodType', {}).get('stringValue', ''),
                    'lastUpdated': fields.get('lastUpdated', {}).get('timestampValue')
                }
                
                # Filter for critical items only
                if emergency_data['criticalAllergies']:
                    emergency_data['criticalAllergies'] = [
                        a for a in emergency_data['criticalAllergies'] 
                        if a.get('severity') in ['severe', 'life-threatening']
                    ]
                
                if emergency_data['criticalMedications']:
                    emergency_data['criticalMedications'] = [
                        m for m in emergency_data['criticalMedications'] 
                        if m.get('active') == True
                    ]
                
                # Save to cache for offline use
                self.save_offline_cache(emergency_data)
                self.last_update = datetime.now()
                
                return emergency_data
            else:
                print(f"Medical info not found, status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        # Fall back to offline cache
        print("Using offline cache")
        return self.offline_cache
    
    def parse_array_field(self, field_data):
        """Parse Firestore array field"""
        if not field_data or 'arrayValue' not in field_data:
            return []
        
        values = field_data['arrayValue'].get('values', [])
        result = []
        
        for value in values:
            if 'mapValue' in value:
                item = {}
                fields = value['mapValue'].get('fields', {})
                for key, val in fields.items():
                    if 'stringValue' in val:
                        item[key] = val['stringValue']
                    elif 'booleanValue' in val:
                        item[key] = val['booleanValue']
                result.append(item)
        
        return result
    
    def draw_header(self):
        """Draw the header section"""
        # Emergency header background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, RED if self.emergency_mode else BLUE, header_rect)
        
        # Title
        title = "🚨 EMERGENCY INFO" if self.emergency_mode else "Medical Information"
        title_surface = self.font_medium.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title_surface, title_rect)
        
        # Status indicator
        status_color = GREEN if self.last_update and (datetime.now() - self.last_update).seconds < 300 else YELLOW
        pygame.draw.circle(self.screen, status_color, (SCREEN_WIDTH - 20, 30), 8)
    
    def draw_allergy_section(self, y_offset):
        """Draw critical allergies section"""
        y = y_offset
        
        # Section title
        title = self.font_small.render("⚠️ CRITICAL ALLERGIES", True, RED)
        self.screen.blit(title, (10, y))
        y += 25
        
        if self.emergency_data and self.emergency_data.get('criticalAllergies'):
            for allergy in self.emergency_data['criticalAllergies'][:3]:  # Show top 3
                # Allergy box
                allergy_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 30)
                pygame.draw.rect(self.screen, (255, 230, 230), allergy_rect)
                pygame.draw.rect(self.screen, RED, allergy_rect, 2)
                
                # Allergy text
                text = f"{allergy.get('name', 'Unknown')} - {allergy.get('severity', '').upper()}"
                allergy_text = self.font_small.render(text[:40], True, BLACK)
                self.screen.blit(allergy_text, (15, y + 5))
                y += 35
        else:
            no_allergy = self.font_small.render("No critical allergies", True, GRAY)
            self.screen.blit(no_allergy, (15, y))
            y += 30
        
        return y
    
    def draw_medication_section(self, y_offset):
        """Draw current medications section"""
        y = y_offset
        
        # Section title
        title = self.font_small.render("💊 CURRENT MEDICATIONS", True, BLUE)
        self.screen.blit(title, (10, y))
        y += 25
        
        if self.emergency_data and self.emergency_data.get('criticalMedications'):
            for med in self.emergency_data['criticalMedications'][:2]:  # Show top 2
                # Medication box
                med_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 30)
                pygame.draw.rect(self.screen, (230, 240, 255), med_rect)
                pygame.draw.rect(self.screen, BLUE, med_rect, 1)
                
                # Medication text
                text = f"{med.get('name', 'Unknown')} - {med.get('dosage', '')} ({med.get('frequency', '')})"
                med_text = self.font_small.render(text[:45], True, BLACK)
                self.screen.blit(med_text, (15, y + 5))
                y += 35
        else:
            no_med = self.font_small.render("No active medications", True, GRAY)
            self.screen.blit(no_med, (15, y))
            y += 30
        
        return y
    
    def draw_contact_section(self, y_offset):
        """Draw emergency contacts section"""
        y = y_offset
        
        # Section title
        title = self.font_small.render("📞 EMERGENCY CONTACTS", True, GREEN)
        self.screen.blit(title, (10, y))
        y += 25
        
        if self.emergency_data and self.emergency_data.get('emergencyContacts'):
            primary_contact = None
            for contact in self.emergency_data['emergencyContacts']:
                if contact.get('isPrimary'):
                    primary_contact = contact
                    break
            
            if not primary_contact and self.emergency_data['emergencyContacts']:
                primary_contact = self.emergency_data['emergencyContacts'][0]
            
            if primary_contact:
                # Contact box
                contact_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 45)
                pygame.draw.rect(self.screen, (230, 255, 230), contact_rect)
                pygame.draw.rect(self.screen, GREEN, contact_rect, 2)
                
                # Contact info
                name_text = self.font_small.render(
                    f"{primary_contact.get('name', 'Unknown')} ({primary_contact.get('relationship', '')})",
                    True, BLACK
                )
                self.screen.blit(name_text, (15, y + 5))
                
                phone_text = self.font_medium.render(
                    primary_contact.get('phone', 'No phone'),
                    True, BLACK
                )
                self.screen.blit(phone_text, (15, y + 23))
        else:
            no_contact = self.font_small.render("No emergency contacts", True, GRAY)
            self.screen.blit(no_contact, (15, y))
        
        return y + 50
    
    def draw_main_screen(self):
        """Draw the main display screen"""
        self.screen.fill(BG_COLOR)
        
        # Draw header
        self.draw_header()
        
        # Draw content sections
        y = 70
        y = self.draw_allergy_section(y)
        y = self.draw_medication_section(y + 10)
        y = self.draw_contact_section(y + 10)
        
        # Draw footer with last update
        footer_y = SCREEN_HEIGHT - 20
        if self.last_update:
            update_text = f"Updated: {self.last_update.strftime('%H:%M:%S')}"
        else:
            update_text = "Offline Mode"
        
        footer = self.font_small.render(update_text, True, GRAY)
        footer_rect = footer.get_rect(center=(SCREEN_WIDTH // 2, footer_y))
        self.screen.blit(footer, footer_rect)
    
    def handle_emergency_button(self):
        """Handle physical emergency button press"""
        if GPIO.input(EMERGENCY_BUTTON_PIN) == GPIO.LOW:
            self.emergency_mode = True
            # Trigger emergency actions
            self.screen.fill(RED)
            emergency_text = self.font_large.render("EMERGENCY ACTIVATED", True, WHITE)
            text_rect = emergency_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(emergency_text, text_rect)
            pygame.display.flip()
            time.sleep(2)
    
    def run(self):
        """Main display loop"""
        # Initial data fetch
        self.emergency_data = self.fetch_emergency_data()
        
        # Set up refresh timer
        REFRESH_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(REFRESH_EVENT, 60000)  # Refresh every minute
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_SPACE:
                        # Manual emergency activation
                        self.emergency_mode = not self.emergency_mode
                    elif event.key == K_r:
                        # Manual refresh
                        self.emergency_data = self.fetch_emergency_data()
                elif event.type == REFRESH_EVENT:
                    # Auto-refresh data
                    self.emergency_data = self.fetch_emergency_data()
                elif event.type == MOUSEBUTTONDOWN:
                    # Touch screen interaction
                    x, y = event.pos
                    if y < 60:  # Header area - toggle emergency mode
                        self.emergency_mode = not self.emergency_mode
            
            # Check physical button
            self.handle_emergency_button()
            
            # Draw screen
            self.draw_main_screen()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS
        
        # Cleanup
        pygame.quit()
        GPIO.cleanup()

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        global USER_ID
        USER_ID = sys.argv[1]
    else:
        print("Usage: python3 emergency_display.py <user_id> [pin]")
        print("Please provide the user ID as an argument")
        sys.exit(1)
    
    if len(sys.argv) > 2:
        global EMERGENCY_PIN
        EMERGENCY_PIN = sys.argv[2]
    
    print(f"Starting Emergency Display for user: {USER_ID}")
    print("Press ESC to exit, SPACE to toggle emergency mode, R to refresh")
    
    display = EmergencyDisplay()
    display.run()

if __name__ == "__main__":
    main()
