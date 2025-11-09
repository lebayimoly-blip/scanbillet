import sqlite3
import psycopg2
from datetime import datetime

# Connexion à SQLite
sqlite_conn = sqlite3.connect("scanbillet.db")
sqlite_cursor = sqlite_conn.cursor()

# Connexion à PostgreSQL Render
pg_conn = psycopg2.connect(
    dbname="scanbillet_db",
    user="scanbillet_db_user",
    password="WCh851qa4kRBnMlB1ScmkFqPkoubdn4J",
    host="dpg-d46sv6je5dus73djfkf0-a.oregon-postgres.render.com",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Lecture des billets depuis SQLite
sqlite_cursor.execute("SELECT id, code, nom_passager, trajet, date_depart, classe FROM billets")
billets = sqlite_cursor.fetchall()

# Insertion dans PostgreSQL
for billet in billets:
    try:
        pg_cursor.execute(
            """
            INSERT INTO billets (id, code, nom_passager, trajet, date_depart, classe)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            billet
        )
    except Exception as e:
        print(f"Erreur lors de l'insertion du billet {billet}: {e}")

# Finalisation
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("✅ Migration des billets terminée avec succès.")
