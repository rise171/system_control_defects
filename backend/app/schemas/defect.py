from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class DefectStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class DefectPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DefectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: DefectStatus = DefectStatus.NEW
    priority: DefectPriority = DefectPriority.MEDIUM
    project_id: int
    assigned_to_id: Optional[int] = None

class DefectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[DefectStatus] = None
    priority: Optional[DefectPriority] = None
    assigned_to_id: Optional[int] = None
    project_id: Optional[int] = None

class DefectDelete(BaseModel):
    id: int

class DefectGetting(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: DefectStatus
    priority: DefectPriority
    project_id: int
    created_by_id: int
    assigned_to_id: Optional[int]

    class Config:
        from_attributes = True