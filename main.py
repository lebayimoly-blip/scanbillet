from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="ScanBillet API", debug=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://scanbillet-frontendb.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.10:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Routeurs API
from app.api.v1.scan import router as scan_router
from app.api.v1.billet import router as billet_router
from app.api.v1.stats import router as stats_router
from app.api.v1.auth import router as auth_router
from app.api.v1.sync import router as sync_router

# 📦 Routeurs internes
from routers import agents, users

# 📌 Inclusion des routeurs
app.include_router(scan_router, prefix="/scan", tags=["Scan"])
app.include_router(billet_router, prefix="/billet", tags=["Billet"])
app.include_router(stats_router, prefix="/stats", tags=["Statistiques"])
app.include_router(auth_router, prefix="/auth", tags=["Authentification"])
app.include_router(sync_router, prefix="/sync", tags=["Synchronisation"])

# 🧩 Compatibilité frontend
app.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
app.include_router(users.router, prefix="/agents", tags=["Utilisateurs"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])

# 🧱 DB
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)
