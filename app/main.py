from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB connection string 
MONGO_URI = "mongodb://mongodb:27017"

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
# db = client["vehicle_db"]  # Database name

@app.get("/ping-db")
async def ping_db():
    """Ping MongoDB to verify connectivity."""
    try:
        # Attempt to retrieve server info to verify the connection
        await client.server_info()
        return {"status": "Connected to MongoDB! Yay222!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {e}")
