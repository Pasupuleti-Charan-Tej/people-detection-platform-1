from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    severity = Column(String, index=True)
    camera_name = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
