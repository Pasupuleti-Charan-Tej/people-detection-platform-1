from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, cameras, detections, alerts, stream, analytics
from app.core.config import settings
from app.core.database import engine, Base

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VisionAI People Detection API",
    description="Enterprise AI-powered people detection platform",
    version="2.0.0"
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST routes
app.include_router(auth.router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(cameras.router,    prefix="/api/cameras",    tags=["Cameras"])
app.include_router(detections.router, prefix="/api/detections", tags=["Detections"])
app.include_router(alerts.router,     prefix="/api/alerts",     tags=["Alerts"])
app.include_router(analytics.router,  prefix="/api/v1/analytics", tags=["Analytics"])

# WebSocket stream route
app.include_router(stream.router, tags=["Stream"])

@app.get("/")
def root():
    return {"status": "VisionAI API running 🚀", "version": "2.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected", "redis": "connected"}