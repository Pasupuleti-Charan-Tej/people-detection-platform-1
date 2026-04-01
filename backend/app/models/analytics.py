from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String, index=True)
    people_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
