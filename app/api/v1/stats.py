from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.stats import StatsResponse, StatsFilters
from app.services.stats_service import get_stats
from app.models.billet import Billet  # ✅ Import du modèle Billet

router = APIRouter()

# 🔄 Dépendance DB locale
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📊 Endpoint POST pour stats filtrées
@router.post("/", response_model=StatsResponse)
def stats(filters: StatsFilters, db: Session = Depends(get_db)):
    # ✅ Appel corrigé : 3 arguments
    data = get_stats(db, filters.date_debut, filters.date_fin)
    return StatsResponse(**data)

# 📊 Endpoint GET pour stats simples
@router.get("/stats")
def get_stats_range(start: str, end: str, db: Session = Depends(get_db)):
    from datetime import datetime

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    billets = db.query(Billet).filter(
        Billet.scanned_at >= start_dt,
        Billet.scanned_at < end_dt
    ).all()

    total = len(billets)
    valides = sum(1 for b in billets if b.valide)
    invalides = total - valides

    return {
        "total_scanned": total,
        "valid_count": valides,
        "invalid_count": invalides
    }
