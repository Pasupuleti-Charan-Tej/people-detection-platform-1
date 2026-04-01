from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertResponse

router = APIRouter()

@router.post("/", response_model=AlertResponse)
def create_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    # Simple spam-prevention: filter similar alerts in the last 15 seconds
    time_threshold = datetime.utcnow() - timedelta(seconds=15)
    recent = db.query(Alert).filter(
        Alert.message == alert_in.message,
        Alert.created_at > time_threshold
    ).first()
    
    if recent:
        return recent # Skip duplicating
        
    db_alert = Alert(**alert_in.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/")
def get_alerts(db: Session = Depends(get_db), limit: int = 50):
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(limit).all()
    return {
        "alerts": alerts,
        "total": len(alerts)
    }
