#!/usr/bin/env python3
"""
Simplified Emergency Display for Raspberry Pi
Displays emergency medical information in a clear, readable format
Optimized for 480x320 touchscreen
"""

import sys
import json
import requests
from datetime import datetime

# Configuration - Update these values
FIREBASE_PROJECT_ID = "heat-2cc8c"
FIREBASE_API_KEY = "AIzaSyCVtFLAmaOUdojGu8yyMy0H-KtW1ugLoag"

def fetch_user_data(user_id):
    """Fetch user medical data from Firebase"""
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/medicalInfo/{user_id}?key={FIREBASE_API_KEY}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            doc = response.json()
            fields = doc.get('fields', {})
            
            # Parse the Firestore data
            def parse_array(field_data):
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
                        result.append(item)
                
                return result
            
            # Extract medical information
            allergies = parse_array(fields.get('allergies', {}))
            medications = parse_array(fields.get('medications', {}))
            contacts = parse_array(fields.get('emergencyContacts', {}))
            blood_type = fields.get('bloodType', {}).get('stringValue', '')
            
            # Filter for critical items
            critical_allergies = [a for a in allergies if a.get('severity') in ['severe', 'life-threatening']]
            active_meds = [m for m in medications if m.get('active') == True]
            
            return {
                'success': True,
                'data': {
                    'bloodType': blood_type,
                    'criticalAllergies': critical_allergies,
                    'activeMedications': active_meds,
                    'emergencyContacts': contacts,
                    'lastUpdated': datetime.now().isoformat()
                }
            }
        else:
            return {'success': False, 'error': f'User data not found (Status: {response.status_code})'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def display_emergency_info(user_id):
    """Display emergency information in terminal format"""
    print("\n" + "="*60)
    print("🚨 EMERGENCY MEDICAL INFORMATION DISPLAY")
    print("="*60)
    
    # Fetch data
    print(f"\n📡 Fetching data for user: {user_id}")
    result = fetch_user_data(user_id)
    
    if not result['success']:
        print(f"\n❌ ERROR: {result['error']}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure you've added medical info in the web app")
        print("2. Check that Firestore is enabled in Firebase Console")
        print("3. Verify the user ID is correct")
        return
    
    data = result['data']
    print("✅ Data loaded successfully!")
    
    # Display patient info
    print(f"\n👤 PATIENT INFORMATION")
    print("-" * 30)
    if data['bloodType']:
        print(f"🩸 BLOOD TYPE: {data['bloodType']}")
    else:
        print("🩸 BLOOD TYPE: Not specified")
    
    # Critical Allergies
    print(f"\n⚠️  CRITICAL ALLERGIES")
    print("-" * 30)
    if data['criticalAllergies']:
        for allergy in data['criticalAllergies']:
            severity = allergy.get('severity', 'unknown').upper()
            reaction = allergy.get('reaction', '')
            print(f"🔴 {allergy['name']} - {severity}")
            if reaction:
                print(f"   Reaction: {reaction}")
    else:
        print("✅ No critical allergies reported")
    
    # Active Medications
    print(f"\n💊 CURRENT MEDICATIONS")
    print("-" * 30)
    if data['activeMedications']:
        for med in data['activeMedications']:
            dosage = med.get('dosage', '')
            frequency = med.get('frequency', '')
            print(f"🔵 {med['name']}")
            if dosage and frequency:
                print(f"   {dosage} - {frequency}")
    else:
        print("ℹ️  No active medications")
    
    # Emergency Contacts
    print(f"\n📞 EMERGENCY CONTACTS")
    print("-" * 30)
    if data['emergencyContacts']:
        for contact in data['emergencyContacts']:
            primary = " (PRIMARY)" if contact.get('isPrimary') else ""
            print(f"🟢 {contact['name']}{primary}")
            print(f"   {contact.get('relationship', 'Contact')}: {contact['phone']}")
    else:
        print("⚠️  No emergency contacts available")
    
    # Footer
    print(f"\n📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\n💡 This is what will display on your Raspberry Pi screen")
    print("🖥️  Optimized for 480x320 touchscreen display")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("❌ Usage: python3 simple_emergency.py <user_id>")
        print("\n📋 To get your user ID:")
        print("1. Login to your web app")
        print("2. Go to Emergency page")
        print("3. Copy the User ID from the emergency access section")
        print("\n🌐 Web app: http://localhost:3003")
        sys.exit(1)
    
    user_id = sys.argv[1]
    print(f"🚀 Emergency Display System")
    print(f"📱 Fetching data for: {user_id}")
    
    display_emergency_info(user_id)
    
    print(f"\n🔄 To run on actual Pi display:")
    print(f"   python3 emergency_display.py {user_id} 1234")

if __name__ == "__main__":
    main()
