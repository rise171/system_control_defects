from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttachmentBase(BaseModel):
    filename: str
    content_type: Optional[str] = None

class AttachmentCreate(AttachmentBase):
    filepath: str
    defect_id: Optional[int] = None
    comment_id: Optional[int] = None

    class Config:
        from_attributes = True

class Attachment(AttachmentBase):
    id: int
    filepath: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class AttachmentDelete(BaseModel):
    message: str = "Attachment deleted successfully"
    attachment_id: int

    class Config:
        from_attributes = True