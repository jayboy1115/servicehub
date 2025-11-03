#!/usr/bin/env python3
"""
MongoDB SSL Connection Test Script - Fixed Version
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
    # Remove deprecated insecure flags from test configurations
    # - Removed tlsAllowInvalidCertificates and tlsInsecure
    # - Removed ssl=false and tls=false URL parameters
    # - Use default secure configuration with sensible timeouts
    
    test_configs = [
        {
            "name": "Standard MongoDB+SRV (default SSL)",
            "url": f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=ServiceHub",
            "params": {"serverSelectionTimeoutMS": 15000}
        },
        {
            "name": "Connection with longer timeout",
            "url": f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=ServiceHub",
            "params": {"serverSelectionTimeoutMS": 30000, "connectTimeoutMS": 30000}
        }
    ]
    
    working_config = None
    
    for config in test_configs:
        print(f"\n🔍 Testing: {config['name']}")
        print(f"   Timeout: {config['params'].get('serverSelectionTimeoutMS', 'default')}ms")
        
        try:
            client = AsyncIOMotorClient(config['url'], **config['params'])
            
            # Test connection with timeout
            await asyncio.wait_for(client.admin.command('ping'), timeout=15)
            
            # Test database access
            db = client['ServiceHub']
            collections = await db.list_collection_names()
            
            print(f"✅ SUCCESS! Connection established")
            print(f"   Database: ServiceHub")
            print(f"   Collections found: {len(collections)}")
            if collections:
                print(f"   Sample collections: {collections[:5]}")
            
            working_config = config
            client.close()
            break
            
        except asyncio.TimeoutError:
            print(f"❌ TIMEOUT: Connection timed out")
        except Exception as e:
            error_msg = str(e)
            if "SSL" in error_msg or "TLS" in error_msg:
                print(f"❌ SSL/TLS ERROR: {error_msg[:150]}...")
            elif "authentication" in error_msg.lower():
                print(f"❌ AUTH ERROR: {error_msg[:150]}...")
            elif "ServerSelectionTimeoutError" in str(type(e)):
                print(f"❌ SERVER SELECTION TIMEOUT: Cannot reach MongoDB servers")
            else:
                print(f"❌ OTHER ERROR: {error_msg[:150]}...")
        
        try:
            client.close()
        except:
            pass
    
    return working_config

async def test_basic_connectivity():
    """Test basic network connectivity to MongoDB Atlas"""
    print("\n🌐 Testing basic connectivity...")
    
    import socket
    
    hosts = [
        ("servicehub.fh5tlnn.mongodb.net", 27017),
        ("ac-r7lfn1n-shard-00-00.fh5tlnn.mongodb.net", 27017),
        ("ac-r7lfn1n-shard-00-01.fh5tlnn.mongodb.net", 27017),
        ("ac-r7lfn1n-shard-00-02.fh5tlnn.mongodb.net", 27017)
    ]
    
    for host, port in hosts:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print(f"✅ Can reach {host}:{port}")
        except Exception as e:
            print(f"❌ Cannot reach {host}:{port} - {e}")

async def main():
    print("🔧 MongoDB SSL Connection Diagnostics - Fixed Version")
    print("=" * 60)
    
    # Test basic connectivity first
    await test_basic_connectivity()
    
    # Test SSL configurations
    working_config = await test_ssl_configs()
    
    if working_config:
        print(f"\n🎉 SOLUTION FOUND!")
        print(f"Working configuration: {working_config['name']}")
        print(f"Parameters: {working_config['params']}")
        print(f"\n📝 To fix your scripts, use these connection parameters:")
        print(f"   URL: {working_config['url']}")
        print(f"   Additional params: {working_config['params']}")
        
        # Generate fixed database.py code
        print(f"\n🔧 Updated database.py connection code:")
        print(f"```python")
        print(f"self.client = AsyncIOMotorClient(mongo_url, **{working_config['params']})")
        print(f"```")
        
    else:
        print(f"\n❌ NO WORKING CONFIGURATION FOUND")
        print(f"This indicates a fundamental connectivity issue:")
        print(f"1. Check your internet connection")
        print(f"2. Verify MongoDB Atlas cluster is running")
        print(f"3. Check if your IP is whitelisted in MongoDB Atlas")
        print(f"4. Verify credentials are correct")
        print(f"5. Check for corporate firewall blocking MongoDB ports")

if __name__ == "__main__":
    asyncio.run(main())