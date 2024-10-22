from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AllocationCreate(BaseModel):
    employee_id: int = Field(..., ge=1, le=1000)
    vehicle_id: int = Field(..., ge=1, le=1000)
    date: date

class AllocationUpdate(BaseModel):
    date: date

class AllocationResponse(BaseModel):
    id: str
    employee_id: int
    vehicle_id: int
    driver_id: int
    date: date

class AllocationFilter(BaseModel):
    employee_id: Optional[int]
    vehicle_id: Optional[int]
    date: Optional[date]
