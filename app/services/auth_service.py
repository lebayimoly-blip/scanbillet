from sqlalchemy.orm import Session
from app.models.agent import Agent
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_agent(db: Session, username: str, password: str):
    agent = db.query(Agent).filter(Agent.username == username).first()
    if agent and verify_password(password, agent.hashed_password):
        return agent
    return None
