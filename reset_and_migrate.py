import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

# 🌍 Charger les variables d'environnement
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔌 Connexions
sqlite_conn = sqlite3.connect("scanbillet.db")
sqlite_cursor = sqlite_conn.cursor()
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

# 🧨 Supprimer les tables existantes
tables = ["scans", "agents", "billets", "roles", "users"]
for table in tables:
    pg_cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
print("🧨 Tables supprimées")

# 🏗️ Recréer les tables PostgreSQL
pg_cursor.execute("""
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);
""")

pg_cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);
""")

pg_cursor.execute("""
CREATE TABLE billets (
    id INTEGER PRIMARY KEY,
    code VARCHAR,
    nom_passager VARCHAR,
    trajet VARCHAR,
    date_depart TIMESTAMP,
    date_arrivee TIMESTAMP
);
""")

pg_cursor.execute("""
CREATE TABLE agents (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE,
    hashed_password VARCHAR,
    role_id INTEGER REFERENCES roles(id),
    code_id INTEGER
);
""")

pg_cursor.execute("""
CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    code_billet VARCHAR,
    agent_id INTEGER REFERENCES agents(id),
    timestamp TIMESTAMP,
    status VARCHAR
);
""")

pg_conn.commit()
print("✅ Tables recréées")

# 🔁 Fonction de migration
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

# 📋 Colonnes à migrer
tables_to_migrate = {
    "roles": ["id", "name"],
    "users": ["id", "name"],
    "billets": ["id", "code", "nom_passager", "trajet", "date_depart", "date_arrivee"],
    "agents": ["id", "username", "hashed_password", "role_id", "code_id"],
    "scans": ["id", "code_billet", "agent_id", "timestamp", "status"]
}

# 🚀 Migration
for table, columns in tables_to_migrate.items():
    migrate_table(table, columns)

# ✅ Commit et fermeture
pg_conn.commit()
pg_conn.close()
sqlite_conn.close()
print("🎉 Migration terminée avec succès")
