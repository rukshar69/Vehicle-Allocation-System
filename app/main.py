from fastapi import FastAPI, HTTPException, Depends
from models import AllocationCreate, AllocationUpdate, AllocationFilter, AllocationResponse
from crud import create_allocation, update_allocation, delete_allocation, get_all_allocations
from database import allocations_collection
app = FastAPI()

@app.post("/allocations/", response_model=AllocationResponse)
async def create_new_allocation(allocation: AllocationCreate):
    allocation_id = await create_allocation(allocation)
    '''
    Example response:
    {
        "id": "6717d73cf441c9bd03c0f158",
        "employee_id": 101,
        "vehicle_id": 10,
        "driver_id": 10,
        "date": "2024-10-22"
    }
    '''
    return {**allocation.dict(), "id": allocation_id, "driver_id": allocation.vehicle_id}

@app.put("/allocations/{allocation_id}", response_model=dict)
async def update_existing_allocation(allocation_id: str, update_data: AllocationUpdate):
    await update_allocation(allocation_id, update_data)
    return {"status": "Allocation updated successfully."}

@app.delete("/allocations/{allocation_id}", response_model=dict)
async def delete_existing_allocation(allocation_id: str):
    await delete_allocation(allocation_id)
    return {"status": "Allocation deleted successfully."}

@app.get("/allocations/", response_model=list[AllocationResponse])
async def get_allocations(filters: AllocationFilter = Depends()):
    allocations = await get_all_allocations(filters)
    return [{"id": str(a["_id"]), **a} for a in allocations]

@app.get("/ping-db")
async def ping_db():
    try:
        await allocations_collection.database.command("ping")
        return {"status": "MongoDB connected."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
