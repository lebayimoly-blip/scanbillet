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

# Lecture des scans depuis SQLite (avec le bon nom de colonne)
sqlite_cursor.execute("SELECT id, code_billet, agent_id, timestamp, position, status FROM scans")
scans = sqlite_cursor.fetchall()

# Insertion dans PostgreSQL (adaptation du nom de colonne cible)
for scan in scans:
    try:
        pg_cursor.execute(
            """
            INSERT INTO scans (id, code_billet, id_agent, timestamp, position, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            scan
        )
    except Exception as e:
        print(f"Erreur lors de l'insertion du scan {scan}: {e}")

# Finalisation
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("✅ Migration des scans terminée avec succès.")
