#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append('/app/backend')

from database import database
from datetime import datetime, timedelta
import uuid

async def create_sample_jobs():
    """Create sample jobs for Francis to test the completed jobs tab"""
    
    # Francis's user ID (homeowner)
    francis_id = "a6630cd9-1a03-435d-93fa-8d73e64775f6"
    francis_email = "francisdaniel4jb@gmail.com"
    
    # Sample jobs data
    sample_jobs = [
        {
            "id": str(uuid.uuid4()),
            "title": "Kitchen Plumbing Repair - COMPLETED",
            "description": "Fixed leaky faucet and improved water pressure. Job completed successfully with excellent results.",
            "category": "Plumbing",
            "location": "Lagos",
            "state": "Lagos",
            "lga": "Lagos Island", 
            "town": "Victoria Island",
            "zip_code": "101241",
            "home_address": "15 Ahmadu Bello Way, Victoria Island, Lagos",
            "budget_min": 15000,
            "budget_max": 25000,
            "timeline": "Within 1 week",
            "status": "completed",
            "homeowner": {
                "id": francis_id,
                "name": "Francis ekpemi daniel",
                "email": francis_email,
                "phone": "+2348058030079"
            },
            "homeowner_id": francis_id,
            "completed_at": datetime.utcnow() - timedelta(days=5),
            "final_cost": 20000,
            "hired_tradesperson": {
                "id": "b8ee65e9-100b-487e-b308-cc3256234c13",
                "name": "John Plumber",
                "rating": 4.5
            },
            "created_at": datetime.utcnow() - timedelta(days=7),
            "updated_at": datetime.utcnow() - timedelta(days=5),
            "expires_at": datetime.utcnow() + timedelta(days=23),
            "interests_count": 5,
            "quotes_count": 3
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Bathroom Tile Installation - COMPLETED",
            "description": "Installed new ceramic tiles in master bathroom. Work completed to high standards.",
            "category": "Tiling",
            "location": "Lagos",
            "state": "Lagos",
            "lga": "Lagos Island",
            "town": "Victoria Island", 
            "zip_code": "101241",
            "home_address": "15 Ahmadu Bello Way, Victoria Island, Lagos",
            "budget_min": 50000,
            "budget_max": 80000,
            "timeline": "Within 2 weeks",
            "status": "completed",
            "homeowner": {
                "id": francis_id,
                "name": "Francis ekpemi daniel",
                "email": francis_email,
                "phone": "+2348058030079"
            },
            "homeowner_id": francis_id,
            "completed_at": datetime.utcnow() - timedelta(days=10),
            "final_cost": 65000,
            "hired_tradesperson": {
                "id": "tradesperson-2-id",
                "name": "Mike Tiler", 
                "rating": 4.8
            },
            "created_at": datetime.utcnow() - timedelta(days=15),
            "updated_at": datetime.utcnow() - timedelta(days=10),
            "expires_at": datetime.utcnow() + timedelta(days=15),
            "interests_count": 8,
            "quotes_count": 5
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Electrical Wiring Upgrade - ACTIVE",
            "description": "Need to upgrade electrical wiring in living room for new appliances.",
            "category": "Electrical",
            "location": "Lagos", 
            "state": "Lagos",
            "lga": "Lagos Island",
            "town": "Victoria Island",
            "zip_code": "101241",
            "home_address": "15 Ahmadu Bello Way, Victoria Island, Lagos",
            "budget_min": 30000,
            "budget_max": 50000,
            "timeline": "Within 1 week",
            "status": "active",
            "homeowner": {
                "id": francis_id,
                "name": "Francis ekpemi daniel", 
                "email": francis_email,
                "phone": "+2348058030079"
            },
            "homeowner_id": francis_id,
            "created_at": datetime.utcnow() - timedelta(days=2),
            "updated_at": datetime.utcnow() - timedelta(days=2),
            "expires_at": datetime.utcnow() + timedelta(days=28),
            "interests_count": 3,
            "quotes_count": 1
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Painting and Wall Repair - IN PROGRESS",
            "description": "Painting exterior walls and fixing cracks. Work currently in progress.",
            "category": "Painting",
            "location": "Lagos",
            "state": "Lagos", 
            "lga": "Lagos Island",
            "town": "Victoria Island",
            "zip_code": "101241",
            "home_address": "15 Ahmadu Bello Way, Victoria Island, Lagos",
            "budget_min": 25000,
            "budget_max": 40000, 
            "timeline": "Within 2 weeks",
            "status": "in_progress",
            "homeowner": {
                "id": francis_id,
                "name": "Francis ekpemi daniel",
                "email": francis_email,
                "phone": "+2348058030079"
            },
            "homeowner_id": francis_id,
            "created_at": datetime.utcnow() - timedelta(days=5),
            "updated_at": datetime.utcnow() - timedelta(days=1),
            "expires_at": datetime.utcnow() + timedelta(days=25),
            "interests_count": 4,
            "quotes_count": 2
        }
    ]
    
    try:
        print("🔧 Creating sample jobs for Francis...")
        
        # Insert sample jobs
        for job in sample_jobs:
            # Convert datetime objects to strings for MongoDB
            if 'completed_at' in job and job['completed_at']:
                job['completed_at'] = job['completed_at'].isoformat()
            if 'created_at' in job:
                job['created_at'] = job['created_at'].isoformat()
            if 'updated_at' in job:
                job['updated_at'] = job['updated_at'].isoformat()
            if 'expires_at' in job:
                job['expires_at'] = job['expires_at'].isoformat()
            
            result = await database.database.jobs.insert_one(job)
            print(f"✅ Created job: {job['title']} (Status: {job['status']})")
        
        print(f"\n🎉 Successfully created {len(sample_jobs)} sample jobs for Francis!")
        print("👤 User can now login and see the completed jobs tab with sample data.")
        
    except Exception as e:
        print(f"❌ Error creating sample jobs: {str(e)}")

if __name__ == "__main__":
    asyncio.run(create_sample_jobs())