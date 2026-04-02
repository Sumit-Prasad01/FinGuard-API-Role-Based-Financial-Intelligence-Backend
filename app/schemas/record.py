from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecordBase(BaseModel):
    amount: float
    type: str  
    category: str
    date: datetime
    notes: Optional[str] = None


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class RecordResponse(RecordBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True