from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.scan import Scan

def get_stats(db: Session, date_debut: str, date_fin: str, agent_id: int | None = None):
    query = db.query(Scan).filter(Scan.timestamp.between(date_debut, date_fin))
    if agent_id:
        query = query.filter(Scan.agent_id == agent_id)

    total = query.count()
    valides = query.filter(Scan.status == "valid").count()
    invalides = query.filter(Scan.status == "invalid").count()
    taux = (valides / total * 100) if total > 0 else 0.0

    return {
        "total_scans": total,
        "total_valid": valides,
        "total_invalid": invalides,
        "taux_validation": round(taux, 2)
    }
