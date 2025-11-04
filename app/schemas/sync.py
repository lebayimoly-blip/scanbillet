from pydantic import BaseModel
from datetime import datetime

class ScanSyncItem(BaseModel):
    code_billet: str
    agent_id: int
    timestamp: datetime
    position: str
    status: str  # "valid" ou "invalid"

class SyncRequest(BaseModel):
    scans: list[ScanSyncItem]

class Config:
    from_attributes = True
