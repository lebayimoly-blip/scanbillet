from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_agent
from app.core.security import create_access_token, get_current_agent
from app.models.agent import Agent

router = APIRouter()

# 🔄 Dépendance locale pour la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 Endpoint de connexion avec SQLAlchemy + JWT
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

# 🧪 Alternative brute avec psycopg2 (optionnelle pour test direct)
"""
from pydantic import BaseModel
import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class RawLoginRequest(BaseModel):
    username: str
    password: str

@router.post("/raw-login")
def raw_login(data: RawLoginRequest):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM agents WHERE username = %s", (data.username,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        hashed_password = result[0]
        if bcrypt.checkpw(data.password.encode(), hashed_password.encode()):
            return {"message": "Connexion réussie"}
        else:
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
