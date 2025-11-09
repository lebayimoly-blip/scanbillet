import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# 🌍 Charger les variables d'environnement
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 🧱 Connexion à SQLite
sqlite_conn = sqlite3.connect("scanbillet.db")
sqlite_cursor = sqlite_conn.cursor()

# 🧱 Connexion à PostgreSQL
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

# 🔁 Fonction de migration avec colonnes explicites
def migrate_table(table_name, columns):
    try:
        sqlite_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        if not rows:
            print(f"⚠️ Table {table_name} vide")
            return
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
        execute_values(pg_cursor, query, rows)
        print(f"✅ {len(rows)} lignes insérées dans {table_name}")
    except Exception as e:
        print(f"❌ Erreur dans {table_name} :", e)

# 📋 Définition des tables et colonnes à migrer
tables_to_migrate = {
    "agents": ["id", "username", "hashed_password", "role_id", "code_id"],
    "billets": ["id", "code", "nom_passager", "trajet", "date_depart", "date_arrivee"],
    "roles": ["id", "name"],
    "scans": ["id", "code_billet", "agent_id", "timestamp", "status"],
    "users": ["id", "name"]
}

# 🚀 Migration
for table, columns in tables_to_migrate.items():
    migrate_table(table, columns)

# ✅ Commit et fermeture
pg_conn.commit()
pg_conn.close()
sqlite_conn.close()
