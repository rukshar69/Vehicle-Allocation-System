from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

MONGO_URI = "mongodb://mongodb:27017"
client = AsyncIOMotorClient(MONGO_URI)

db = client["vehicle_db"]
allocations_collection: Collection = db["allocations"]
