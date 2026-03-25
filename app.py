"""
Portfolio Backend - Flask Python Server
Handles serving the portfolio page and saving contact form submissions to PostgreSQL.
"""

import os
from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)


def get_db_connection():
    """Create and return a database connection using DATABASE_URL env variable."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL environment variable is not set.")
    return psycopg2.connect(database_url)


def init_db():
    """Create the contacts table if it doesn't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully.")


@app.route("/")
def home():
    """Serve the main portfolio page."""
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    """Save a contact form submission to the database."""
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided."}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Basic validation
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    if len(name) > 100:
        return jsonify({"success": False, "error": "Name is too long (max 100 chars)."}), 400

    if len(email) > 255 or "@" not in email:
        return jsonify({"success": False, "error": "Invalid email address."}), 400

    if len(message) > 2000:
        return jsonify({"success": False, "error": "Message is too long (max 2000 chars)."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s) RETURNING id, created_at",
            (name, email, message)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({
            "success": True,
            "message": "Thank you! Your message has been saved.",
            "id": result["id"]
        }), 201
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "error": "Failed to save message. Please try again."}), 500


@app.route("/contacts", methods=["GET"])
def get_contacts():
    """Get all contact form submissions (for admin review)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        contacts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(row) for row in contacts])
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Failed to fetch contacts."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    print(f"Starting portfolio server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
