from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import date
from models import AllocationCreate, AllocationUpdate, AllocationFilter, AllocationResponse
from crud import create_allocation, update_allocation, delete_allocation, get_all_allocations
from database import allocations_collection

app = FastAPI(
    title="Vehicle Allocation System",
    description="A FastAPI app to manage vehicle allocations for employees with MongoDB as the backend.",
    version="1.0.0"
)

@app.post("/allocations/", response_model=AllocationResponse, status_code=201, tags=["Allocations"])
async def create_new_allocation(allocation: AllocationCreate):
    """
    Create a new vehicle allocation for an employee.

    - **employee_id**: ID of the employee (1-1000)
    - **vehicle_id**: ID of the vehicle (1-1000)
    - **date**: Date of the allocation (YYYY-MM-DD)

    Raises:
        - 400: If the vehicle is already allocated on the specified date.

    Returns:
        - **201**: A JSON object with the created allocation details.
    """
    allocation_id = await create_allocation(allocation)
    return {**allocation.dict(), "id": allocation_id, "driver_id": allocation.vehicle_id}

@app.put("/allocations/{allocation_id}", response_model=dict, tags=["Allocations"])
async def update_existing_allocation(allocation_id: str, update_data: AllocationUpdate):
    """
    Update an existing allocation.

    - **allocation_id**: ID of the allocation to update.
    - **date**: New allocation date (YYYY-MM-DD).

    Raises:
        - 404: If the allocation is not found.
        - 400: If the allocation date is in the past.

    Returns:
        - **200**: Status message indicating successful update.
    """
    await update_allocation(allocation_id, update_data)
    return {"status": "Allocation updated successfully."}

@app.delete("/allocations/{allocation_id}", response_model=dict, tags=["Allocations"])
async def delete_existing_allocation(allocation_id: str):
    """
    Delete an existing allocation.

    - **allocation_id**: ID of the allocation to delete.

    Raises:
        - 404: If the allocation is not found.
        - 400: If trying to delete an allocation in the past.

    Returns:
        - **200**: Status message indicating successful deletion.
    """
    await delete_allocation(allocation_id)
    return {"status": "Allocation deleted successfully."}

@app.get("/allocations/", response_model=list[AllocationResponse], tags=["Allocations"])
async def get_allocations(
    employee_id: Optional[int] = Query(None, ge=1, le=1000, description="Filter by employee ID"),
    vehicle_id: Optional[int] = Query(None, ge=1, le=1000, description="Filter by vehicle ID"),
    date: Optional[date] = Query(None, description="Filter by allocation date (YYYY-MM-DD)")
):
    """
    Get a list of vehicle allocations with optional filters.

    - **employee_id**: Filter allocations by employee ID (1-1000).
    - **vehicle_id**: Filter allocations by vehicle ID (1-1000).
    - **date**: Filter allocations by a specific date.

    Returns:
        - **200**: A list of allocations matching the filters.
    """
    filters = AllocationFilter(employee_id=employee_id, vehicle_id=vehicle_id, date=date)
    allocations = await get_all_allocations(filters)
    return [{"id": str(a["_id"]), **a} for a in allocations]

@app.get("/ping-db", response_model=dict, tags=["Utility"])
async def ping_db():
    """
    Test the connection to MongoDB.

    Returns:
        - **200**: If the connection is successful.
        - **500**: If there is an error connecting to MongoDB.
    """
    try:
        await allocations_collection.database.command("ping")
        return {"status": "MongoDB connected."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
