from app.db.session import engine, Base
from app.models.agent import Agent
from app.models.role import Role
from app.models.scan import Scan

def init_db():
    print("🔄 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base SQLite initialisée.")

if __name__ == "__main__":
    init_db()
