from sqlalchemy.orm import Session
from app.models.scan import Scan
from app.schemas.sync import ScanSyncItem

def sync_scans(db: Session, scans: list[ScanSyncItem]):
    for item in scans:
        db_scan = Scan(
            code_billet=item.code_billet,
            agent_id=item.agent_id,
            timestamp=item.timestamp,
            position=item.position,
            status=item.status
        )
        db.add(db_scan)
    db.commit()
