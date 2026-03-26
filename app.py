"""
Portfolio Backend - Flask Python Server
Production-ready for Render + Neon PostgreSQL
"""

import os
from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse

app = Flask(__name__)


# ✅ Better DB connection (Neon requires SSL)
def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL environment variable is not set.")

    return psycopg2.connect(database_url, sslmode="require")


# ✅ Initialize DB safely
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database initialized successfully.")

    except Exception as e:
        print(f"❌ DB Init Error: {e}")


# ✅ Run DB init only once on startup (Render safe)
@app.before_first_request
def initialize():
    init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided."}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # ✅ Validation
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    if len(name) > 100:
        return jsonify({"success": False, "error": "Name too long"}), 400

    if len(email) > 255 or "@" not in email:
        return jsonify({"success": False, "error": "Invalid email"}), 400

    if len(message) > 2000:
        return jsonify({"success": False, "error": "Message too long"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            INSERT INTO contacts (name, email, message)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, email, message))

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Message saved successfully!",
            "id": result["id"]
        }), 201

    except Exception as e:
        print(f"❌ DB Error: {e}")
        return jsonify({"success": False, "error": "Server error"}), 500


@app.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY created_at DESC
        """)

        contacts = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([dict(row) for row in contacts])

    except Exception as e:
        print(f"❌ Fetch Error: {e}")
        return jsonify({"error": "Failed to fetch contacts"}), 500


# ✅ IMPORTANT for Render (Gunicorn handles this)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)
