from app.db.session import SessionLocal, engine, Base
from app.models.agent import Agent
from app.models.role import Role
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Crée le rôle
admin_role = Role(name="super_admin")
db.add(admin_role)
db.commit()
db.refresh(admin_role)

# Crée l'agent
admin = Agent(
    username="admin",
    hashed_password=get_password_hash("admin123"),
    role_id=admin_role.id
)
db.add(admin)
db.commit()

print("✅ Base initialisée avec rôle et agent.")
