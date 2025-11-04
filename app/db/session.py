from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

# 📦 URL de la base de données (SQLite pour démarrer en local)
DATABASE_URL = "sqlite:///./scanbillet.db"
# Pour PostgreSQL : "postgresql://user:password@localhost/dbname"

# ⚙️ Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # requis pour SQLite en mode multi-thread
)

# 🧵 Session locale pour les dépendances FastAPI
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🧱 Base déclarative pour les modèles ORM
Base = declarative_base()

# 🔄 Dépendance FastAPI pour injecter une session DB
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
