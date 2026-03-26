import os
import pg8000
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_db():
    url = urlparse(os.environ["DATABASE_URL"])
    params = dict(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path.lstrip("/"),
        port=url.port or 5432
    )
    try:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return pg8000.connect(**params, ssl_context=ctx)
    except Exception:
        return pg8000.connect(**params)

def init_db():
    conn = get_db()
    conn.run("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    conn.close()
    print("Database ready.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    try:
        conn = get_db()
        conn.run(
            "INSERT INTO contacts (name, email, message) VALUES (:name, :email, :message)",
            name=name, email=email, message=message
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Message saved!"}), 201
    except Exception as e:
        print("DB error:", e)
        return jsonify({"success": False, "error": "Failed to save. Try again."}), 500

@app.route("/contacts")
def get_contacts():
    try:
        conn = get_db()
        rows = conn.run("SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC")
        conn.close()
        keys = ["id", "name", "email", "message", "created_at"]
        return jsonify([dict(zip(keys, r)) for r in rows])
    except Exception as e:
        print("DB error:", e)
        return jsonify({"error": "Could not fetch contacts."}), 500

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
