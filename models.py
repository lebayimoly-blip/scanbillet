# scanbillet/models.py

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# 🧑‍💼 Modèle utilisateur
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

# 🕵️ Modèle agent
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    role = Column(String, nullable=False)
