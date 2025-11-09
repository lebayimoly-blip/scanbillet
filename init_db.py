from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Connexion à PostgreSQL Render
DATABASE_URL = "postgresql://scanbillet_db_user:WCh851qa4kRBnMlB1ScmkFqPkoubdn4J@dpg-d46sv6je5dus73djfkf0-a.oregon-postgres.render.com:5432/scanbillet_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Table Roles
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Table Agents
class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")

# Table Billets
class Billet(Base):
    __tablename__ = "billets"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    nom_passager = Column(String)
    trajet = Column(String)
    date_depart = Column(DateTime)
    classe = Column(String)

# Table Scans
class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True)
    code_billet = Column(String)
    id_agent = Column(Integer)
    timestamp = Column(DateTime)
    position = Column(String)
    status = Column(String)

# Création des tables
Base.metadata.create_all(bind=engine)

print("✅ Toutes les tables ont été créées avec succès dans PostgreSQL Render.")
