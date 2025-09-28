#!/usr/bin/env python3
"""
Simple test script to verify the emergency display works
Creates mock data and displays it on screen
"""

import pygame
import json
from datetime import datetime

# Mock emergency data for testing
MOCK_DATA = {
    'criticalAllergies': [
        {
            'name': 'Peanuts',
            'severity': 'life-threatening',
            'reaction': 'Anaphylaxis'
        },
        {
            'name': 'Shellfish', 
            'severity': 'severe',
            'reaction': 'Hives, swelling'
        }
    ],
    'criticalMedications': [
        {
            'name': 'Lisinopril',
            'dosage': '10mg',
            'frequency': 'Daily',
            'active': True
        },
        {
            'name': 'Metformin',
            'dosage': '500mg',
            'frequency': 'Twice daily',
            'active': True
        }
    ],
    'emergencyContacts': [
        {
            'name': 'Jane Doe',
            'relationship': 'Spouse',
            'phone': '(555) 123-4567',
            'isPrimary': True
        }
    ],
    'bloodType': 'O+',
    'fullName': 'John Doe',
    'dateOfBirth': '1985-03-15'
}

# Display Configuration for 480x320
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FONT_SIZE_LARGE = 28
FONT_SIZE_MEDIUM = 20
FONT_SIZE_SMALL = 16

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 53, 69)
BLUE = (0, 123, 255)
GREEN = (40, 167, 69)
YELLOW = (255, 193, 7)
GRAY = (108, 117, 125)
BG_COLOR = (248, 249, 250)

class TestEmergencyDisplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Emergency Medical Information - TEST")
        
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.emergency_mode = True  # Start in emergency mode for demo
        
    def draw_header(self):
        """Draw emergency header"""
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(self.screen, RED, header_rect)
        
        title = self.font_medium.render("🚨 EMERGENCY MEDICAL INFO", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 25))
        self.screen.blit(title, title_rect)
    
    def draw_patient_info(self, y_start):
        """Draw patient basic info"""
        y = y_start
        
        # Patient name and blood type
        name_text = self.font_medium.render(f"PATIENT: {MOCK_DATA['fullName']}", True, BLACK)
        self.screen.blit(name_text, (10, y))
        
        if MOCK_DATA['bloodType']:
            blood_text = self.font_large.render(f"BLOOD: {MOCK_DATA['bloodType']}", True, RED)
            blood_rect = blood_text.get_rect(right=SCREEN_WIDTH - 10, y=y)
            self.screen.blit(blood_text, blood_rect)
        
        return y + 35
    
    def draw_allergies(self, y_start):
        """Draw critical allergies"""
        y = y_start
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (255, 220, 220), header_rect)
        pygame.draw.rect(self.screen, RED, header_rect, 2)
        
        title = self.font_small.render("⚠️ CRITICAL ALLERGIES", True, RED)
        self.screen.blit(title, (10, y + 5))
        y += 30
        
        # Allergies list
        for allergy in MOCK_DATA['criticalAllergies'][:2]:  # Show top 2 for space
            allergy_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 25)
            pygame.draw.rect(self.screen, (255, 240, 240), allergy_rect)
            pygame.draw.rect(self.screen, RED, allergy_rect, 1)
            
            text = f"{allergy['name']} - {allergy['severity'].upper()}"
            allergy_text = self.font_small.render(text, True, BLACK)
            self.screen.blit(allergy_text, (15, y + 5))
            y += 30
        
        return y + 5
    
    def draw_medications(self, y_start):
        """Draw current medications"""
        y = y_start
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (220, 240, 255), header_rect)
        pygame.draw.rect(self.screen, BLUE, header_rect, 2)
        
        title = self.font_small.render("💊 CURRENT MEDICATIONS", True, BLUE)
        self.screen.blit(title, (10, y + 5))
        y += 30
        
        # Medications list
        for med in MOCK_DATA['criticalMedications'][:2]:  # Show top 2
            med_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 25)
            pygame.draw.rect(self.screen, (240, 248, 255), med_rect)
            pygame.draw.rect(self.screen, BLUE, med_rect, 1)
            
            text = f"{med['name']} - {med['dosage']} ({med['frequency']})"
            med_text = self.font_small.render(text, True, BLACK)
            self.screen.blit(med_text, (15, y + 5))
            y += 30
        
        return y + 5
    
    def draw_emergency_contact(self, y_start):
        """Draw primary emergency contact"""
        y = y_start
        
        contact = MOCK_DATA['emergencyContacts'][0]  # Primary contact
        
        # Section header
        header_rect = pygame.Rect(5, y, SCREEN_WIDTH - 10, 25)
        pygame.draw.rect(self.screen, (220, 255, 220), header_rect)
        pygame.draw.rect(self.screen, GREEN, header_rect, 2)
        
        title = self.font_small.render("📞 EMERGENCY CONTACT", True, GREEN)
        self.screen.blit(title, (10, y + 5))
        y += 30
        
        # Contact info
        contact_rect = pygame.Rect(10, y, SCREEN_WIDTH - 20, 40)
        pygame.draw.rect(self.screen, (240, 255, 240), contact_rect)
        pygame.draw.rect(self.screen, GREEN, contact_rect, 2)
        
        name_text = self.font_small.render(f"{contact['name']} ({contact['relationship']})", True, BLACK)
        self.screen.blit(name_text, (15, y + 5))
        
        phone_text = self.font_medium.render(contact['phone'], True, BLACK)
        self.screen.blit(phone_text, (15, y + 22))
        
        return y + 45
    
    def draw_instructions(self, y_start):
        """Draw usage instructions"""
        y = y_start
        
        instructions = [
            "TOUCH SCREEN TO REFRESH",
            "SPACE = Emergency Mode",
            "R = Refresh Data"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 18
    
    def draw_main_screen(self):
        """Draw the complete emergency display"""
        self.screen.fill(BG_COLOR)
        
        # Draw all sections
        y = 0
        y = self.draw_header()
        y = self.draw_patient_info(y + 10)
        y = self.draw_allergies(y + 5)
        y = self.draw_medications(y + 5)
        y = self.draw_emergency_contact(y + 5)
        
        # Instructions at bottom
        if y < SCREEN_HEIGHT - 60:
            self.draw_instructions(SCREEN_HEIGHT - 55)
    
    def run(self):
        """Main display loop"""
        print("Emergency Display Test - Using Mock Data")
        print("Press ESC to exit, SPACE for emergency mode, R to refresh")
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.emergency_mode = not self.emergency_mode
                        print(f"Emergency mode: {self.emergency_mode}")
                    elif event.key == pygame.K_r:
                        print("Refreshing data...")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Touch interaction
                    self.emergency_mode = not self.emergency_mode
                    print(f"Touch - Emergency mode: {self.emergency_mode}")
            
            # Draw screen
            self.draw_main_screen()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    print("Starting Emergency Display Test")
    print("This will show mock emergency data on a 480x320 display")
    
    display = TestEmergencyDisplay()
    display.run()
