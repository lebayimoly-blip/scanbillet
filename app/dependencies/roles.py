from fastapi import Depends, HTTPException
from app.models.agent import Agent
from app.core.security import get_current_agent  # ou get_current_user selon ton système

def require_roles(*allowed_roles):
    def checker(agent: Agent = Depends(get_current_agent)):
        if agent.role.name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Accès interdit")
        return agent
    return checker
