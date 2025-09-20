from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.defects import DefectStatus, DefectPriority
from app.schemas.user import User
from app.schemas.projects import Project
from app.schemas.comment import Comment
from app.schemas.attachment import Attachment


class DefectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: DefectStatus = DefectStatus.NEW
    priority: DefectPriority = DefectPriority.MEDIUM
    due_date: Optional[datetime] = None

class DefectCreate(DefectBase):
    project_id: int
    created_by_id: int
    assigned_to_id: Optional[int] = None

    class Config:
        from_attributes = True

class DefectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DefectStatus] = None
    priority: Optional[DefectPriority] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

    class Config:
        from_attributes = True

class Defect(DefectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    project: Project
    creator: User
    assignee: Optional[User] = None
    comments: List[Comment] = []
    attachments: List[Attachment] = []

    class Config:
        from_attributes = True

class DefectList(BaseModel):
    id: int
    title: str
    status: DefectStatus
    priority: DefectPriority
    due_date: Optional[datetime] = None
    created_at: datetime
    project_id: int
    assigned_to_id: Optional[int] = None

    class Config:
        from_attributes = True

class DefectDelete(BaseModel):
    message: str = "Defect deleted successfully"
    defect_id: int

    class Config:
        from_attributes = True

class DefectFilter(BaseModel):
    project_id: Optional[int] = None
    status: Optional[DefectStatus] = None
    priority: Optional[DefectPriority] = None
    assigned_to_id: Optional[int] = None