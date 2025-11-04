from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.sync import SyncRequest
from app.services.sync_service import sync_scans

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def sync_data(payload: SyncRequest, db: Session = Depends(get_db)):
    sync_scans(db, payload.scans)
    return {"message": f"{len(payload.scans)} scans synchronisés avec succès"}
