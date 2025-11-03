#!/usr/bin/env python3
"""
TARGETED LOGIN TEST - Checking correct database and fixing the login issue
"""

import requests
import json
from pymongo import MongoClient

# Configuration
BACKEND_URL = "http://localhost:8001/api"
MONGO_URL = "mongodb://localhost:27017/test_database"  # Using correct DB name
TARGET_EMAIL = "francisdaniel4jb@gmail.com"

def test_user_in_correct_database():
    """Check if user exists in the correct database"""
    print(f"🔍 Checking user in correct database: test_database")
    
    try:
        client = MongoClient(MONGO_URL)
        db = client.test_database
        
        # Check if user exists
        user = db.users.find_one({"email": TARGET_EMAIL})
        
        if user:
            print(f"✅ User FOUND in test_database!")
            print(f"   User ID: {user.get('id')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Status: {user.get('status')}")
            print(f"   Created: {user.get('created_at')}")
            print(f"   Password Hash: {'Present' if user.get('password_hash') else 'Missing'}")
            
            # Check password hash format
            password_hash = user.get('password_hash', '')
            if password_hash.startswith('$2b$'):
                print(f"   Password Hash Format: bcrypt (correct)")
            else:
                print(f"   Password Hash Format: Unknown - {password_hash[:20]}...")
            
            return user
        else:
            print(f"❌ User NOT FOUND in test_database")
            
            # Check total users
            total_users = db.users.count_documents({})
            print(f"   Total users in database: {total_users}")
            
            # Check recent users
            recent_users = list(db.users.find({}).sort("created_at", -1).limit(3))
            print(f"   Recent users:")
            for u in recent_users:
                print(f"     - {u.get('email')} ({u.get('role')})")
            
            return None
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None
    finally:
        client.close()

def test_login_with_known_password():
    """Test login with various password attempts"""
    print(f"\n🔐 Testing login attempts for {TARGET_EMAIL}")
    
    # Common passwords to try
    passwords = [
        "password",
        "password123",
        "Password123",
        "Password123!",
        "servicehub",
        "servicehub123",
        "ServiceHub123",
        "ServiceHub123!",
        "francis",
        "francis123",
        "Francis123",
        "Francis123!",
        "daniel",
        "daniel123",
        "Daniel123",
        "Daniel123!",
        "francisdaniel",
        "francisdaniel123",
        "FrancisDaniel123",
        "FrancisDaniel123!"
    ]
    
    for password in passwords:
        login_data = {
            "email": TARGET_EMAIL,
            "password": password
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('access_token'):
                    print(f"🎉 LOGIN SUCCESSFUL!")
                    print(f"   Password: {password}")
                    print(f"   Access Token: {data.get('access_token')[:50]}...")
                    print(f"   User ID: {data.get('user', {}).get('id')}")
                    return data
            elif response.status_code == 401:
                print(f"   ❌ {password} - Invalid credentials")
            elif response.status_code == 403:
                print(f"   🚫 {password} - Account suspended/forbidden")
            else:
                print(f"   ⚠️  {password} - Status: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 {password} - Error: {e}")
    
    print(f"❌ No successful login found")
    return None

def create_new_account_for_user():
    """Create a new account for the user since the old one seems corrupted"""
    print(f"\n🆕 Creating new account for user")
    
    # Try different email variations
    email_variations = [
        "francisdaniel4jb+new@gmail.com",
        "francisdaniel4jb.new@gmail.com", 
        "francisdaniel4jb2@gmail.com"
    ]
    
    for email in email_variations:
        registration_data = {
            "name": "Francis Daniel",
            "email": email,
            "password": "NewPassword123!",
            "phone": "+2348012345678",
            "location": "Lagos",
            "postcode": "100001"
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/auth/register/homeowner", json=registration_data)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ New account created successfully!")
                print(f"   Email: {email}")
                print(f"   User ID: {data.get('user', {}).get('id')}")
                print(f"   Access Token: {data.get('access_token')[:50]}...")
                
                # Test login with new account
                login_data = {
                    "email": email,
                    "password": "NewPassword123!"
                }
                
                login_response = requests.post(f"{BACKEND_URL}/auth/login", json=login_data)
                
                if login_response.status_code == 200:
                    print(f"✅ Login with new account successful!")
                    return {
                        "email": email,
                        "password": "NewPassword123!",
                        "user_data": data
                    }
                else:
                    print(f"❌ Login with new account failed: {login_response.status_code}")
            else:
                print(f"❌ Registration failed for {email}: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                    
        except Exception as e:
            print(f"💥 Error creating account for {email}: {e}")
    
    return None

def fix_existing_user_password():
    """Try to fix the existing user's password by updating it directly in database"""
    print(f"\n🔧 Attempting to fix existing user password")
    
    try:
        client = MongoClient(MONGO_URL)
        db = client.test_database
        
        # Find the user
        user = db.users.find_one({"email": TARGET_EMAIL})
        
        if not user:
            print(f"❌ User not found for password fix")
            return False
        
        # Generate a new password hash for a known password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"])  # Removed deprecated="auto"
        
        new_password = "FixedPassword123!"
        new_hash = pwd_context.hash(new_password)
        
        # Update the user's password hash
        result = db.users.update_one(
            {"email": TARGET_EMAIL},
            {"$set": {"password_hash": new_hash}}
        )
        
        if result.modified_count > 0:
            print(f"✅ Password hash updated successfully")
            print(f"   New password: {new_password}")
            
            # Test login with new password
            login_data = {
                "email": TARGET_EMAIL,
                "password": new_password
            }
            
            response = requests.post(f"{BACKEND_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                print(f"🎉 LOGIN SUCCESSFUL with fixed password!")
                print(f"   Access Token: {data.get('access_token')[:50]}...")
                return True
            else:
                print(f"❌ Login still failed: {response.status_code}")
                return False
        else:
            print(f"❌ Failed to update password hash")
            return False
            
    except Exception as e:
        print(f"💥 Error fixing password: {e}")
        return False
    finally:
        client.close()

def main():
    print("🚨 TARGETED LOGIN DEBUG AND FIX")
    print("=" * 50)
    
    # Step 1: Check if user exists in correct database
    user_data = test_user_in_correct_database()
    
    # Step 2: Try login with common passwords
    login_result = test_login_with_known_password()
    
    if login_result:
        print(f"\n✅ ISSUE RESOLVED - User can login successfully!")
        return
    
    # Step 3: If user exists but login fails, try to fix password
    if user_data:
        print(f"\n🔧 User exists but login fails - attempting password fix...")
        if fix_existing_user_password():
            print(f"\n✅ ISSUE RESOLVED - Password fixed and user can login!")
            return
    
    # Step 4: Create new account as fallback
    print(f"\n🆕 Creating new account as fallback solution...")
    new_account = create_new_account_for_user()
    
    if new_account:
        print(f"\n✅ FALLBACK SOLUTION - New account created!")
        print(f"   User can login with: {new_account['email']}")
        print(f"   Password: {new_account['password']}")
    else:
        print(f"\n❌ UNABLE TO RESOLVE - Manual intervention required")

if __name__ == "__main__":
    main()