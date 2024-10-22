from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

# Define the MongoDB connection URI
MONGO_URI = "mongodb://mongodb:27017"

# Create a new AsyncIOMotorClient instance using the connection URI
client = AsyncIOMotorClient(MONGO_URI)

# Select the database named "vehicle_db"
db = client["vehicle_db"]

# Select the collection named "allocations" from the database
allocations_collection: Collection = db["allocations"]
