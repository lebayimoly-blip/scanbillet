from pydantic import BaseModel
from datetime import datetime

class ScanRequest(BaseModel):
    code_billet: str
    agent_id: int
    timestamp: datetime
    position: str

    class Config:
        from_attributes = True  # Pydantic v2

class ScanResponse(BaseModel):
    code_billet: str
    agent_id: int
    timestamp: datetime
    position: str
    status: str

    class Config:
        from_attributes = True  # Pydantic v2


