from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import User

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    manager_id: int

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True
        
class ProjectList(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    manager_id: int

    class Config:
        from_attributes = True

# Delete response
class ProjectDelete(BaseModel):
    message: str = "Project deleted successfully"
    project_id: int

class Project(ProjectBase):
    id: int
    created_at: datetime
    manager: User

    class Config:
        from_attributes = True