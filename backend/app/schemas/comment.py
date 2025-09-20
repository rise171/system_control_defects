from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import User
from app.schemas.attachment import Attachment

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    defect_id: int
    author_id: int

    class Config:
        from_attributes = True

class CommentDelete(BaseModel):
    message: str = "Comment deleted successfully"
    comment_id: int

    class Config:
        from_attributes = True        

class Comment(CommentBase):
    id: int
    created_at: datetime
    author: User
    attachments: List[Attachment] = []

    class Config:
        from_attributes = True