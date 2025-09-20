from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.settings import Base

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)  # Path in S3/MinIO
    content_type = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys (nullable for flexibility)
    defect_id = Column(Integer, ForeignKey("defects.id"))
    comment_id = Column(Integer, ForeignKey("comments.id"))

    # Relationships
    defect = relationship("Defect", back_populates="attachments")
    comment = relationship("Comment", back_populates="attachments")