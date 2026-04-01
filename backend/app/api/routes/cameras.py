from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_cameras():
    return [
        {"id": 1, "name": "CAM-01", "location": "Entrance A",  "status": "active",  "fps": 30, "resolution": "1080p"},
        {"id": 2, "name": "CAM-02", "location": "Main Hall",   "status": "active",  "fps": 25, "resolution": "720p"},
        {"id": 3, "name": "CAM-03", "location": "Parking Lot", "status": "active",  "fps": 15, "resolution": "1080p"},
        {"id": 4, "name": "CAM-04", "location": "Server Room", "status": "standby", "fps": 30, "resolution": "1080p"},
    ]

@router.get("/{camera_id}")
def get_camera(camera_id: int):
    return {"id": camera_id, "name": f"CAM-0{camera_id}", "status": "active"}
