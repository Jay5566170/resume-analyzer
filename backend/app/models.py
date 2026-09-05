from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # Extracted data from AI
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    skills = Column(Text, nullable=True)      # JSON string
    experience = Column(Text, nullable=True)  # JSON string
    education = Column(Text, nullable=True)   # JSON string
    summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)