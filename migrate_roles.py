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

# Lecture des rôles depuis SQLite
sqlite_cursor.execute("SELECT id, name FROM roles")
roles = sqlite_cursor.fetchall()

# Insertion dans PostgreSQL
for role in roles:
    try:
        pg_cursor.execute(
            "INSERT INTO roles (id, name) VALUES (%s, %s)",
            role
        )
    except Exception as e:
        print(f"Erreur lors de l'insertion du rôle {role}: {e}")

# Finalisation
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("✅ Migration des rôles terminée avec succès.")
