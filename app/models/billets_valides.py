# app/models/billets_valides.py
from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base  # ← fonctionne maintenant
from datetime import datetime

class BilletValide(Base):
    __tablename__ = "billets_valides"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # identifiant ou hash du billet
    source = Column(String)  # "scan" ou "pdf"
    date_ajout = Column(DateTime, default=datetime.utcnow)
