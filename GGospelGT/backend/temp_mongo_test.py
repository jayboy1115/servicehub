import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://servicehub_data:servicehub123@servicehub.fh5tlnn.mongodb.net/?appName=ServiceHub"

async def main():
    try:
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=15000)
        await asyncio.wait_for(client.admin.command('ping'), timeout=15)
        print("✅ MongoDB ping succeeded")
        db = client["ServiceHub"]
        names = await db.list_collection_names()
        print(f"Collections: {names[:5]}")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
    finally:
        try:
            client.close()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())