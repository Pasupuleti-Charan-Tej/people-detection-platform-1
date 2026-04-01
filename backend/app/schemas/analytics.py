from pydantic import BaseModel
from datetime import datetime

class DetectionLogCreate(BaseModel):
    camera_id: str
    people_count: int

class DetectionLogResponse(DetectionLogCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
