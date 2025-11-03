#!/usr/bin/env python3
"""
Test script to verify the Nigerian phone number validation fix.
This tests the specific case that was failing: +23408140120508
"""

import requests
import json
import uuid

def test_phone_validation():
    """Test the phone number validation with the problematic number"""
    
    # Backend URL
    base_url = "http://localhost:8001/api"
    
    # Generate unique test data
    unique_id = uuid.uuid4().hex[:8]
    
    # Test data with the problematic phone number
    test_data = {
        "name": f"Test User {unique_id}",
        "email": f"test.{unique_id}@example.com",
        "password": "TestPassword123!",
        "phone": "+23408140120508",  # This was failing before
        "location": "Lagos",
        "postcode": "100001",
        "trade_categories": ["Plumbing"],
        "experience_years": 2,
        "company_name": f"Test Company {unique_id}",
        "description": "This is a comprehensive test description for phone validation fix that meets the minimum 50 character requirement for tradesperson registration."
    }
    
    print("=== Testing Nigerian Phone Number Validation Fix ===")
    print(f"Testing phone number: {test_data['phone']}")
    print(f"Expected: Should be accepted and formatted to +2348140120508")
    
    try:
        # Make registration request
        response = requests.post(
            f"{base_url}/auth/register/tradesperson",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registration successful!")
            
            # Check for phone in user object
            user_data = data.get('user', {})
            formatted_phone = user_data.get('phone', 'Not returned')
            print(f"Formatted phone: {formatted_phone}")
            
            # Verify the phone was formatted correctly
            expected_phone = "+2348140120508"
            if formatted_phone == expected_phone:
                print(f"✅ Phone number correctly formatted to: {expected_phone}")
            else:
                print(f"⚠️ Phone formatting issue: expected '{expected_phone}', got '{formatted_phone}'")
                
        elif response.status_code == 400:
            try:
                error_data = response.json()
                print(f"❌ Registration failed: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"❌ Registration failed with status 400")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    # Test additional phone number formats
    print("\n=== Testing Additional Phone Number Formats ===")
    
    test_cases = [
        ("+2348140120508", "Correct format"),
        ("08140120508", "Nigerian local format"),
        ("8140120508", "10-digit format"),
        ("+234 814 012 0508", "With spaces"),
    ]
    
    for phone, description in test_cases:
        unique_id = uuid.uuid4().hex[:8]
        test_data_variant = test_data.copy()
        test_data_variant["name"] = f"Test User {unique_id}"
        test_data_variant["email"] = f"test.{unique_id}@example.com"
        test_data_variant["phone"] = phone
        
        print(f"\nTesting: {phone} ({description})")
        
        try:
            response = requests.post(
                f"{base_url}/auth/register/tradesperson",
                json=test_data_variant,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('user', {})
                formatted_phone = user_data.get('phone', 'Not returned')
                print(f"✅ Accepted, formatted to: {formatted_phone}")
            else:
                try:
                    error_data = response.json()
                    print(f"❌ Rejected: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"❌ Rejected with status {response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_phone_validation()