from fastapi import APIRouter
from datetime import datetime
router = APIRouter()

@router.get("/")
def get_detections():
    return {
        "detections": [
            {"id": 1, "camera_id": 1, "track_id": "P#001", "confidence": 0.97, "timestamp": str(datetime.now())},
            {"id": 2, "camera_id": 2, "track_id": "P#002", "confidence": 0.94, "timestamp": str(datetime.now())},
        ],
        "total": 2
    }
