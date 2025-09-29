from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database.settings import Base

class DefectAttachment(Base):
    __tablename__ = "defect_attachments"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False) # Путь к файлу на сервере
    upload_date = Column(DateTime, default=datetime.utcnow)

    defect_id = Column(Integer, ForeignKey("defects.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"))

    defect = relationship("Defect", back_populates="attachments")
    comment = relationship("Comment", back_populates="attachments")