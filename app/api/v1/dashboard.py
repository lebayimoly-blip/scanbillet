from fastapi import APIRouter, Depends
from app.dependencies.roles import require_role
from app.models.user import User

router = APIRouter()

@router.get("/dashboard")
def dashboard(user: User = Depends(require_role("super_admin"))):
    return {"message": "Bienvenue super admin"}
