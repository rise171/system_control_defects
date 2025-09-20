from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.settings import Base

class DefectStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class DefectPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(DefectStatus), default=DefectStatus.NEW, nullable=False)
    priority = Column(Enum(DefectPriority), default=DefectPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    project = relationship("Project", back_populates="defects")
    creator = relationship("User", back_populates="created_defects", foreign_keys=[created_by_id])
    assignee = relationship("User", back_populates="assigned_defects", foreign_keys=[assigned_to_id])
    comments = relationship("Comment", back_populates="defect", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="defect", cascade="all, delete-orphan")