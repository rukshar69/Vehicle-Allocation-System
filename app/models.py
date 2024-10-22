from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Define a data model for creating new allocations
class AllocationCreate(BaseModel):
    # The employee ID must be an integer between 1 and 1000 (inclusive)
    employee_id: int = Field(..., ge=1, le=1000)
    # The vehicle ID must be an integer between 1 and 1000 (inclusive)
    vehicle_id: int = Field(..., ge=1, le=1000)
    # The date of the allocation
    date: date

# Define a data model for updating existing allocations
class AllocationUpdate(BaseModel):
    # The new date of the allocation
    date: date

# Define a data model for representing allocation responses
class AllocationResponse(BaseModel):
    # The unique ID of the allocation
    id: str
    # The employee ID associated with the allocation
    employee_id: int
    # The vehicle ID associated with the allocation
    vehicle_id: int
    # The driver ID associated with the allocation (assumed to be the same as vehicle ID)
    driver_id: int
    # The date of the allocation
    date: date

# Define a data model for filtering allocations
class AllocationFilter(BaseModel):
    employee_id: Optional[int] = Field(None, ge=1, le=1000)
    vehicle_id: Optional[int] = Field(None, ge=1, le=1000)
    date: Optional[date] = None