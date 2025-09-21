from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1)
    defect_id: int
    author_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1)

class CommentDelete(BaseModel):
    id: int

class CommentGetting(BaseModel):
    id: int
    text: str
    created_at: datetime
    defect_id: int
    author_id: int

    class Config:
        from_attributes = True