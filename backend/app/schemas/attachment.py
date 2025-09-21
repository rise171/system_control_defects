from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DefectAttachmentCreate(BaseModel):
    file_path: str = Field(..., min_length=1)
    defect_id: int

class DefectAttachmentUpdate(BaseModel):
    file_path: Optional[str] = Field(None, min_length=1)

class DefectAttachmentDelete(BaseModel):
    id: int

class DefectAttachmentGetting(BaseModel):
    id: int
    file_path: str
    upload_date: datetime
    defect_id: int

    class Config:
        from_attributes = True