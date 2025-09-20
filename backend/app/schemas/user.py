from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

# Base
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserGet(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    message: str = "User deleted successfully"
    user_id: int

    class Config:
        from_attributes = True