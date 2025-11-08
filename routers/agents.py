from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Agent

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AgentCreate(BaseModel):
    nom: str
    role: str

@router.get("/", response_model=list[dict])
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return [{"id": a.id, "nom": a.nom, "role": a.role} for a in agents]

@router.post("/", response_model=dict)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(nom=agent.nom, role=agent.role)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return {"id": db_agent.id, "nom": db_agent.nom, "role": db_agent.role}
