#!/bin/bash
echo "🚀 Démarrage de ScanBillet API..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
