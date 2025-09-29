from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.settings import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    ENGINEER = "engineer"
    READER = "reader"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Relationships
    managed_projects = relationship("Project", back_populates="manager")
    created_defects = relationship("Defect", back_populates="creator", foreign_keys="Defect.created_by_id")
    assigned_defects = relationship("Defect", back_populates="assignee", foreign_keys="Defect.assigned_to_id")
    comments = relationship("Comment", back_populates="author")