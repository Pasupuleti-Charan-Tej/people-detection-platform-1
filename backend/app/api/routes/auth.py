from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str

DEMO_USERS = {
    "admin@visionai.com":    {"password": "admin123", "role": "admin",    "name": "Charan P."},
    "operator@visionai.com": {"password": "op456",    "role": "operator", "name": "Alex K."},
    "viewer@visionai.com":   {"password": "view789",  "role": "viewer",   "name": "Sam T."},
}

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = DEMO_USERS.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": request.email, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"], "name": user["name"]}

@router.get("/me")
def get_me():
    return {"message": "Auth working ✅"}
