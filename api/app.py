from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnérabilité 1 : SQL Injection volontaire
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        # Vulnérabilité 2 : Pas de token, pas de session sécurisée
        return {"status": "success", "user": username}

    # Vulnérabilité 3 : Message d’erreur trop détaillé
    return {"status": "error", "message": "Invalid credentials"}

# Vulnérabilité 4 : Mode debug activé en production
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
