from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from scanbillet.database import SessionLocal
from scanbillet.models import User
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "scanbillet-secret")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return user

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not bcrypt.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }
