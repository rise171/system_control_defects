from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.settings import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    defect_id = Column(Integer, ForeignKey("defects.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    defect = relationship("Defect", back_populates="comments")
    author = relationship("User", back_populates="comments")
    attachments = relationship("DefectAttachment", back_populates="comment", cascade="all, delete-orphan")