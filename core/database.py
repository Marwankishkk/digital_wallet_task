# app/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URL)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]
    print("Connected to MongoDB! 🚀")

async def close_mongo_connection():
    db_instance.client.close()
    print("MongoDB connection closed.")