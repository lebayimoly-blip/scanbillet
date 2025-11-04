from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class Billet(Base):
    __tablename__ = "billets"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    nom_passager = Column(String)
    trajet = Column(String)
    date_depart = Column(DateTime)
    classe = Column(String)
