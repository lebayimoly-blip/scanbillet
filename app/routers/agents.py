from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.agent import Agent
from app.models.role import Role
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AgentCreate(BaseModel):
    username: str
    password: str
    role: str

@router.get("/agents")
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

@router.post("/agents")
def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    if db.query(Agent).filter_by(username=agent_data.username).first():
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé.")

    role = db.query(Role).filter_by(name=agent_data.role).first()
    if not role:
        raise HTTPException(status_code=400, detail="Rôle invalide.")

    hashed_pw = pwd_context.hash(agent_data.password)
    agent = Agent(
        username=agent_data.username,
        hashed_password=hashed_pw,
        role_id=role.id
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent introuvable.")
    db.delete(agent)
    db.commit()
    return {"message": "Supprimé"}
