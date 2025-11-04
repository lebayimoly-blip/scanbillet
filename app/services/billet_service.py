from sqlalchemy.orm import Session
from app.models.billet import Billet

def get_billet_by_code(db: Session, code: str):
    return db.query(Billet).filter(Billet.code == code).first()
