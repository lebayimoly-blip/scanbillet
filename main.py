# scanbillet/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 🛠️ Configuration des logs
logging.basicConfig(level=logging.DEBUG)

# 🚀 Initialisation de l'application FastAPI
app = FastAPI(
    title="ScanBillet API",
    debug=False
)

# 🌐 Middleware CORS : autorise le frontend React à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.10:3000",
        "https://scanbillet-frontendb.onrender.com",  # ✅ frontend Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Importation des routeurs API
from app.api.v1.scan import router as scan_router
from app.api.v1.billet import router as billet_router
from app.api.v1.stats import router as stats_router
from app.api.v1.auth import router as auth_router
from app.api.v1.sync import router as sync_router

# 📦 Importation des routeurs internes
from scanbillet.routers import agents, users, auth

# 📌 Inclusion des routeurs
app.include_router(scan_router, prefix="/scan", tags=["Scan"])
app.include_router(billet_router, prefix="/billet", tags=["Billet"])
app.include_router(stats_router, prefix="/stats", tags=["Statistiques"])
app.include_router(auth_router, prefix="/auth", tags=["Authentification"])
app.include_router(sync_router, prefix="/sync", tags=["Synchronisation"])

# 🧩 Compatibilité frontend et REST explicite
app.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
app.include_router(users.router, prefix="/agents", tags=["Utilisateurs"])  # ← pour compatibilité React
app.include_router(agents.router, prefix="/agents", tags=["Agents"])       # ← pour agents métier
app.include_router(auth.router, prefix="/auth", tags=["Authentification"]) # ← pour login + /me

# 🧱 Création des tables dans PostgreSQL
from scanbillet.database import engine, Base
from scanbillet import models

Base.metadata.create_all(bind=engine)
