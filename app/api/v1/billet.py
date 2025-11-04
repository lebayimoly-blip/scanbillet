from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.billets_valides import BilletValide
from app.schemas.billet import BilletResponse
from app.services.billet_service import get_billet_by_code

router = APIRouter()

# 🔧 Session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📄 Lecture d’un billet par son code
@router.get("/{code}", response_model=BilletResponse)
def read_billet(code: str, db: Session = Depends(get_db)):
    billet = get_billet_by_code(db, code)
    if not billet:
        raise HTTPException(status_code=404, detail="Billet non trouvé")
    return billet

# 📥 Import groupé via PDF
@router.post("/import-pdf")
def import_billets_pdf(codes: list[str], db: Session = Depends(get_db)):
    ajoutés = 0
    doublons = 0
    for code in codes:
        if db.query(BilletValide).filter(BilletValide.code == code).first():
            doublons += 1
        else:
            db.add(BilletValide(code=code, source="pdf"))
            ajoutés += 1
    db.commit()
    return {"ajoutés": ajoutés, "doublons": doublons}

# 📷 Validation d’un billet scanné
@router.post("/valider-scan")
def valider_billet_scanné(code: str, db: Session = Depends(get_db)):
    billet = db.query(BilletValide).filter(BilletValide.code == code).first()
    if billet:
        return {"status": "valide", "source": billet.source, "code": billet.code}
    else:
        return {"status": "invalide", "code": code}
