# app/db/seed_billet.py
from app.db.session import SessionLocal, engine, Base
from app.models.billet import Billet

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# 🎫 Ajout d’un billet de test
billet = Billet(code="BILLET-123", nom="Test", valide=True)
db.add(billet)
db.commit()

print("✅ Billet BILLET-123 ajouté à la base.")
