import sqlite3
import psycopg2

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

# Lecture des agents depuis SQLite
sqlite_cursor.execute("SELECT id, username, hashed_password, role_id FROM agents")
agents = sqlite_cursor.fetchall()

# Insertion dans PostgreSQL
for agent in agents:
    try:
        pg_cursor.execute(
            """
            INSERT INTO agents (id, username, hashed_password, role_id)
            VALUES (%s, %s, %s, %s)
            """,
            agent
        )
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'agent {agent}: {e}")

# Finalisation
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("✅ Migration des agents terminée avec succès.")
