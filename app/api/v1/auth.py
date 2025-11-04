from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_agent
from app.core.security import create_access_token, get_current_agent
from app.models.agent import Agent

router = APIRouter()

# 🔄 Dépendance locale pour la DB (optionnelle si déjà définie globalement)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 Endpoint de connexion
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    agent = authenticate_agent(db, data.username, data.password)
    if not agent:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": agent.username})
    return TokenResponse(access_token=token)

# 👤 Endpoint pour récupérer l'agent connecté
@router.get("/me")
def read_current_agent(agent: Agent = Depends(get_current_agent)):
    return {
        "id": agent.id,
        "username": agent.username,
        "role": agent.role.name
    }
