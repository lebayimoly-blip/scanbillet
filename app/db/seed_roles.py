from app.db.session import SessionLocal
from app.models.role import Role

db = SessionLocal()

for role_name in ["agent", "admin", "super_admin"]:
    if not db.query(Role).filter_by(name=role_name).first():
        db.add(Role(name=role_name))

db.commit()
print("✅ Rôles initialisés")
