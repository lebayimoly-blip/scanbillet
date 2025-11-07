# scanbillet/routers/agents.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from scanbillet.database import SessionLocal
from scanbillet.models import Agent

router = APIRouter()

# 🔌 Dépendance pour session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📥 Schéma Pydantic pour validation des entrées
class AgentCreate(BaseModel):
    nom: str
    role: str

# 📤 GET /agents → liste des agents
@router.get("/", response_model=list[dict])
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return [{"id": a.id, "nom": a.nom, "role": a.role} for a in agents]

# 🆕 POST /agents → ajout d’un agent
@router.post("/", response_model=dict)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(nom=agent.nom, role=agent.role)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return {"id": db_agent.id, "nom": db_agent.nom, "role": db_agent.role}
