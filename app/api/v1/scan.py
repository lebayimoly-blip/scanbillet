from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.scan import ScanRequest, ScanResponse
from app.db.session import SessionLocal
from app.services.scan_service import create_scan  # Assure-toi que ce fichier existe

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ScanResponse)
def scan_billet(data: ScanRequest, db: Session = Depends(get_db)):
    is_valid = data.code_billet.startswith("BILLET")
    scan = create_scan(db, data, status="valid" if is_valid else "invalid")
    return ScanResponse(**data.dict(), status=scan.status)
