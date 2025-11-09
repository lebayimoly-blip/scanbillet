import psycopg2
import bcrypt
from dotenv import load_dotenv
import os

# 🌍 Charger les variables d'environnement
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 🧱 Connexion à PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 🧱 Créer la table roles si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
)
""")
conn.commit()
print("✅ Table roles vérifiée ou créée")

# 🔑 Hachage du mot de passe
mot_de_passe = "Google99."
hashed_password = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()

# 🔍 Vérifier si le rôle super_admin existe
cursor.execute("SELECT id FROM roles WHERE name = %s", ("super_admin",))
role = cursor.fetchone()

if not role:
    cursor.execute("INSERT INTO roles (name) VALUES (%s) RETURNING id", ("super_admin",))
    role_id = cursor.fetchone()[0]
    print("✅ Rôle super_admin créé")
else:
    role_id = role[0]
    print("✅ Rôle super_admin déjà présent")

# 🧨 Supprimer et recréer proprement la table agents
cursor.execute("DROP TABLE IF EXISTS agents CASCADE")
print("🧨 Table agents supprimée")

cursor.execute("""
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    code_id INTEGER
)
""")
conn.commit()
print("✅ Table agents recréée avec structure correcte")

# 👤 Insérer l’agent
cursor.execute("""
INSERT INTO agents (username, hashed_password, role_id, code_id)
VALUES (%s, %s, %s, %s)
""", ("lebayi moly", hashed_password, role_id, None))

conn.commit()
conn.close()
print("✅ Agent 'lebayi moly' inséré avec succès")
