from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResumeBase(BaseModel):
    filename: str

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(BaseModel):
    id: int
    filename: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # ✅ FIXED (was orm_mode)