from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 🛠️ Configuration des logs pour le debug backend
logging.basicConfig(level=logging.DEBUG)

# 🚀 Initialisation de l'application FastAPI
app = FastAPI(
    title="ScanBillet API",
    debug=False
)

# 🌐 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.10:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route racine
@app.get("/")
def root():
    return {"status": "ScanBillet backend actif"}

# 📦 Importation des routeurs
from app.api.v1.scan import router as scan_router
from app.api.v1.billet import router as billet_router
from app.api.v1.stats import router as stats_router
from app.api.v1.auth import router as auth_router
from app.api.v1.sync import router as sync_router
from app.routers import agents

# 📌 Inclusion des routeurs
app.include_router(scan_router, prefix="/scan", tags=["Scan"])
app.include_router(billet_router, prefix="/billet", tags=["Billet"])
app.include_router(stats_router, prefix="/stats", tags=["Statistiques"])
app.include_router(auth_router, prefix="/auth", tags=["Authentification"])
app.include_router(sync_router, prefix="/sync", tags=["Synchronisation"])
app.include_router(agents.router, tags=["Utilisateurs"])
