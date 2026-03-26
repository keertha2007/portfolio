import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__, static_folder=".")
CORS(app)

# ── Database connection ──────────────────────────────────────────────────────

def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"], cursor_factory=RealDictCursor)
    return conn


def init_db():
    """Create the messages table if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         SERIAL PRIMARY KEY,
            name       VARCHAR(100) NOT NULL,
            email      VARCHAR(150) NOT NULL,
            message    TEXT        NOT NULL,
            created_at TIMESTAMP   NOT NULL DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅  Database initialised.")


# ── Routes ───────────────────────────────────────────────────────────────────

# Serve index.html at the root
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# Handle contact form submissions
@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    # Basic validation
    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "Message sent successfully! I'll get back to you soon."}), 201
    except Exception as e:
        print("DB error:", e)
        return jsonify({"success": False, "message": "Something went wrong. Please try again."}), 500


# ── Start ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
