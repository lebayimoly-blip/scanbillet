from database import SessionLocal
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

hashed_pw = pwd_context.hash("Google99")

user = User(
    username="lebayi moly",
    hashed_password=hashed_pw,
    is_superuser=True
)

db.add(user)
db.commit()
db.refresh(user)
print("✅ Super utilisateur créé : lebayi moly")
