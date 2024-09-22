from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.db.base import Base

class JobStatus(Base):
    __tablename__ = 'job_status'
    
    job_id = Column(String, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
