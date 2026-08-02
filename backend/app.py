from flask import Flask, jsonify, send_file,redirect,url_for
from flask_cors import CORS
import sqlite3
import os
import google.generativeai as genai
from config import UPLOAD_FOLDER, DATABASE

from routes.upload import upload_bp
from routes.extract import extract_bp
from routes.validate import validate_bp
from routes.generate import generate_bp
from routes.auth import auth_bp
from routes.appointment import appointment_bp
from routes.notification import notification_bp

app = Flask(__name__)
CORS(app)
app.config.from_pyfile("config.py")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # 1. Users Table (Encrypted Password Auth)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'patient',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Documents Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            filename TEXT,
            file_type TEXT,
            status TEXT DEFAULT 'Pending Review',
            completeness_score INTEGER DEFAULT 0,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Extracted Fields Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS extracted_fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            field_name TEXT,
            field_value TEXT,
            is_missing INTEGER DEFAULT 0,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    """)

    # 4. Appointments / Tokens Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_no TEXT,
            patient_name TEXT,
            doctor_name TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Waiting',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            diagnosis TEXT,
            symptoms TEXT,
            advice TEXT,
            medicines TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 5. Notifications Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            document_id INTEGER,
            title TEXT,
            message TEXT,
            missing_fields TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Column migrations if old schema exists
    try:
        c.execute("ALTER TABLE notifications ADD COLUMN patient_name TEXT")
    except Exception:
        pass

    try:
        c.execute("ALTER TABLE notifications ADD COLUMN title TEXT")
    except Exception:
        pass

    try:
        c.execute("ALTER TABLE notifications ADD COLUMN missing_fields TEXT")
    except Exception:
        pass

    try:
        c.execute("ALTER TABLE documents ADD COLUMN document_type TEXT DEFAULT 'Medical Report'")
    except Exception:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN insurance_provider TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN insurance_policy TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN insurance_status TEXT DEFAULT 'Not added'")
    except Exception:
        pass



    # Seed default demo users with encrypted passwords
    from werkzeug.security import generate_password_hash
    demo_users = [
        ("Rahul Sharma", "patient@mamacare.org", "9876543210", generate_password_hash("password123"), "patient"),
        ("Dr. Arvind Sharma", "doctor@mamacare.org", "9876543211", generate_password_hash("password123"), "doctor"),
        ("Receptionist Desk #1", "reception@mamacare.org", "9876543212", generate_password_hash("password123"), "receptionist")
    ]
    for u in demo_users:
        try:
            c.execute(
                "INSERT INTO users (name, email, phone, password_hash, role) VALUES (?, ?, ?, ?, ?)",
                u
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

init_db()

# Register API Blueprints
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(extract_bp, url_prefix="/api")
app.register_blueprint(validate_bp, url_prefix="/api")
app.register_blueprint(generate_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(appointment_bp, url_prefix="/api")
app.register_blueprint(notification_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def index():
    return  {
        "status": "Backend Running",
        "message": "MamaCare API is live 🚀"
    }

@app.route("/preview", methods=["GET"])
def preview():
    return send_file("../frontend/dashboard.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
