from flask import Flask, request, jsonify
import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

# 🔐 Charger les variables d'environnement
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 🚀 Initialiser l'application Flask
app = Flask(__name__)

# 🔌 Connexion à PostgreSQL
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# 🔐 Route /login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Champs manquants"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM agents WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"error": "Utilisateur introuvable"}), 404

        hashed_password = result[0]
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return jsonify({"message": "Connexion réussie"}), 200
        else:
            return jsonify({"error": "Mot de passe incorrect"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🧭 Lancer le serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
