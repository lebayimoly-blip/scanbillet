# scanbillet/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 🔐 Connexion à PostgreSQL cloud via variable d’environnement
DATABASE_URL = os.getenv("DATABASE_URL")  # à définir dans Render

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
