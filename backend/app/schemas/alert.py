from pydantic import BaseModel
from datetime import datetime

class AlertCreate(BaseModel):
    type: str
    severity: str
    camera_name: str
    message: str

class AlertResponse(AlertCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
