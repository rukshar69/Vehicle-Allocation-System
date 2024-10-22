from database import allocations_collection
from models import AllocationCreate, AllocationUpdate
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId

async def create_allocation(allocation: AllocationCreate):
    """
    Create a new allocation in the database.

    Args:
        allocation (AllocationCreate): The allocation data to be created,
            which includes employee_id, vehicle_id, and date.

    Raises:
        HTTPException: If the vehicle is already allocated for the specified date.

    Returns:
        str: The ID of the newly created allocation.
    """
    if await allocations_collection.find_one({
        "vehicle_id": allocation.vehicle_id,
        "date": allocation.date.isoformat()
    }):
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date.")

    allocation_data = allocation.dict()
    allocation_data["driver_id"] = allocation.vehicle_id  # Assume driver_id is the same as vehicle_id
    allocation_data["date"] = allocation.date.isoformat()  # Convert to string
    result = await allocations_collection.insert_one(allocation_data)
    return str(result.inserted_id)

async def update_allocation(allocation_id: str, update_data: AllocationUpdate):
    """
    Update an existing allocation with the provided update data.

    Args:
        allocation_id (str): The ID of the allocation to update.
        update_data (AllocationUpdate): The data to update the allocation with.

    Raises:
        HTTPException: If the allocation is not found or if the allocation date is in the past.

    Returns:
        bool: True if the allocation was successfully updated.
    """
    existing = await allocations_collection.find_one({"_id": ObjectId(allocation_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Allocation not found.")
    
    if datetime.strptime(existing["date"], "%Y-%m-%d").date() < datetime.utcnow().date():
        raise HTTPException(status_code=400, detail="Cannot modify past allocations.")

    update_dict = update_data.dict()
    update_dict["date"] = update_data.date.isoformat()  # Convert to string
    await allocations_collection.update_one(
        {"_id": ObjectId(allocation_id)},
        {"$set": update_dict}
    )
    return True

async def delete_allocation(allocation_id: str):
    """
    Delete an existing allocation from the database.

    Args:
        allocation_id (str): The ID of the allocation to be deleted.

    Raises:
        HTTPException: If the allocation is not found or if the allocation date is in the past.

    Returns:
        bool: True if the allocation was successfully deleted.
    """
    allocation = await allocations_collection.find_one({"_id": ObjectId(allocation_id)})
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")

    if datetime.strptime(allocation["date"], "%Y-%m-%d").date() < datetime.utcnow().date():
        raise HTTPException(status_code=400, detail="Cannot delete past allocations.")

    await allocations_collection.delete_one({"_id": ObjectId(allocation_id)})
    return True

async def get_all_allocations(filters):
    """
    Retrieve a list of allocations based on the provided filters.

    Args:
        filters (AllocationFilter): The filters to apply to the query.

    Returns:
        list[dict]: A list of allocations, each represented as a dictionary.
    """
    query = {key: value for key, value in filters.dict(exclude_none=True).items()}
    allocations = await allocations_collection.find(query).to_list(1000)
    return allocations
