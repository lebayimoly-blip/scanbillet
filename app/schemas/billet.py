from pydantic import BaseModel
from datetime import datetime

# 🎫 Détails du billet pour affichage ou réponse enrichie
class BilletInfo(BaseModel):
    code: str
    nom_passager: str
    trajet: str
    date_depart: datetime
    classe: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2

# 📦 Structure complète du billet en base
class BilletResponse(BaseModel):
    id: int
    code_billet: str
    agent_id: int
    timestamp: datetime
    position: str
    status: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2
