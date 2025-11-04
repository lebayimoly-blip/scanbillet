from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_scans: int
    total_valid: int
    total_invalid: int
    taux_validation: float

class StatsFilters(BaseModel):
    date_debut: str  # Format YYYY-MM-DD
    date_fin: str
    agent_id: int | None = None

class Config:
    from_attributes = True
