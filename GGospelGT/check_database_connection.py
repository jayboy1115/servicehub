#!/usr/bin/env python3
"""
Database Connection Checker

This script checks what databases the ServiceHub application is connected to
and provides detailed connection information.
"""

import asyncio
import motor.motor_asyncio
import os
from urllib.parse import urlparse

async def check_database_connections():
    """Check database connections and provide detailed information"""
    print("🔍 ServiceHub Database Connection Analysis")
    print("=" * 50)
    
    # Get environment variables
    mongo_url = os.environ.get('MONGO_URL', 'Not set')
    db_name = os.environ.get('DB_NAME', 'Not set').strip('"')
    
    print(f"📋 Environment Configuration:")
    print(f"   MONGO_URL: {mongo_url[:50]}...")
    print(f"   DB_NAME: {db_name}")
    print()
    
    # Parse MongoDB URL to get connection details
    if mongo_url and mongo_url != 'Not set':
        try:
            parsed_url = urlparse(mongo_url)
            print(f"🌐 MongoDB Connection Details:")
            print(f"   Host: {parsed_url.hostname}")
            print(f"   Port: {parsed_url.port or 'default (27017)'}")
            print(f"   Username: {parsed_url.username}")
            print(f"   Database from URL: {parsed_url.path.lstrip('/')}")
            print()
        except Exception as e:
            print(f"❌ Failed to parse MongoDB URL: {e}")
    
    # Connect to database
    print("🔗 Connecting to database...")
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Get database
        database = client[db_name]
        print(f"📚 Connected to database: {db_name}")
        
        # List all databases
        db_list = await client.list_database_names()
        print(f"🗃️  Available databases: {', '.join(db_list)}")
        
        # List collections in current database
        collections = await database.list_collection_names()
        print(f"📁 Collections in '{db_name}': {', '.join(collections)}")
        print()
        
        # Get collection counts
        print("📊 Collection Document Counts:")
        for collection_name in collections:
            try:
                count = await database[collection_name].count_documents({})
                print(f"   {collection_name}: {count} documents")
            except Exception as e:
                print(f"   {collection_name}: Error counting - {e}")
        
        print()
        
        # Check if this matches the API response
        print("🔍 Verification:")
        print(f"   Backend connects to: {db_name}")
        print(f"   Collections found: {len(collections)}")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    print()
    print("✅ Database connection analysis completed")

if __name__ == "__main__":
    # Load environment variables from backend .env
    try:
        with open('/app/backend/.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")
    
    asyncio.run(check_database_connections())