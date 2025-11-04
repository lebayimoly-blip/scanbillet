from sqlalchemy.orm import Session
from app.models.scan import Scan
from app.schemas.scan import ScanRequest

def create_scan(db: Session, data: ScanRequest, status: str) -> Scan:
    scan = Scan(
        code_billet=data.code_billet,
        agent_id=data.agent_id,
        timestamp=data.timestamp,
        position=data.position,
        status=status
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan
