#!/usr/bin/env python3
"""
MongoDB SSL Connection Test Script
Diagnose and fix SSL connection issues with MongoDB Atlas
"""

import os
import asyncio
import ssl
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

async def test_ssl_configs():
    """Test different SSL configurations to find working solution"""
    
    # MongoDB connection details
    username = "servicehub9ja_db_user"
    password = "4g1AuCgVnJB2VR5s"
    cluster = "servicehub.fh5tlnn.mongodb.net"
    
    # Try different URL formats and SSL configurations
    # Remove deprecated/insecure flags from SSL test configurations
    # - Removed tlsAllowInvalidCertificates and tlsInsecure
    # - Removed ssl=false URL parameters
    # - Keep secure defaults with timeouts
    
    test_configs = [
        {
            "name": "Standard MongoDB+SRV (default SSL)",
            "url": f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=ServiceHub",
            "params": {"serverSelectionTimeoutMS": 15000}
        },
        {
            "name": "Connection with longer timeout",
            "url": f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster}/?retryWrites=true&w=majority&appName=ServiceHub",
            "params": {"serverSelectionTimeoutMS": 30000, "connectTimeoutMS": 30000}
        }
    ]
    
    working_config = None
    
    for config in test_configs:
        print(f"\n🔍 Testing: {config['name']}")
        print(f"   URL: {config['url'][:80]}...")
        
        try:
            client = AsyncIOMotorClient(config['url'], **config['params'])
            
            # Test connection with timeout
            await asyncio.wait_for(client.admin.command('ping'), timeout=10)
            
            # Test database access
            db = client['ServiceHub']
            collections = await db.list_collection_names()
            
            print(f"✅ SUCCESS! Connection established")
            print(f"   Database: ServiceHub")
            print(f"   Collections found: {len(collections)}")
            print(f"   Sample collections: {collections[:5]}")
            
            working_config = config
            client.close()
            break
            
        except asyncio.TimeoutError:
            print(f"❌ TIMEOUT: Connection timed out after 10 seconds")
        except Exception as e:
            error_msg = str(e)
            if "SSL" in error_msg or "TLS" in error_msg:
                print(f"❌ SSL/TLS ERROR: {error_msg[:100]}...")
            elif "authentication" in error_msg.lower():
                print(f"❌ AUTH ERROR: {error_msg[:100]}...")
            else:
                print(f"❌ OTHER ERROR: {error_msg[:100]}...")
        
        try:
            client.close()
        except:
            pass
    
    return working_config

async def main():
    print("🔧 MongoDB SSL Connection Diagnostics")
    print("=" * 50)
    
    working_config = await test_ssl_configs()
    
    if working_config:
        print(f"\n🎉 SOLUTION FOUND!")
        print(f"Working configuration: {working_config['name']}")
        print(f"Parameters: {working_config['params']}")
        print(f"\n📝 To fix your scripts, use these connection parameters:")
        print(f"   URL: {working_config['url']}")
        print(f"   Additional params: {working_config['params']}")
    else:
        print(f"\n❌ NO WORKING CONFIGURATION FOUND")
        print(f"All SSL configurations failed. This might indicate:")
        print(f"1. Network connectivity issues")
        print(f"2. Firewall blocking MongoDB ports")
        print(f"3. Invalid credentials")
        print(f"4. MongoDB Atlas cluster issues")

if __name__ == "__main__":
    asyncio.run(main())