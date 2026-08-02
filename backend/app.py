from flask import Flask, jsonify, send_file
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

CORS(
    app,
    resources={r"/api/*": {"origins": "*"}}
)

app.config.from_pyfile("config.py")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

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

    migrations = [
        "ALTER TABLE notifications ADD COLUMN patient_name TEXT",
        "ALTER TABLE notifications ADD COLUMN title TEXT",
        "ALTER TABLE notifications ADD COLUMN missing_fields TEXT",
        "ALTER TABLE documents ADD COLUMN document_type TEXT DEFAULT 'Medical Report'",
        "ALTER TABLE users ADD COLUMN insurance_provider TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN insurance_policy TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN insurance_status TEXT DEFAULT 'Not added'"
    ]

    for query in migrations:
        try:
            c.execute(query)
        except:
            pass

    from werkzeug.security import generate_password_hash

    demo_users = [
        (
            "Rahul Sharma",
            "patient@mamacare.org",
            "9876543210",
            generate_password_hash("password123"),
            "patient",
        ),
        (
            "Dr. Arvind Sharma",
            "doctor@mamacare.org",
            "9876543211",
            generate_password_hash("password123"),
            "doctor",
        ),
        (
            "Receptionist Desk #1",
            "reception@mamacare.org",
            "9876543212",
            generate_password_hash("password123"),
            "receptionist",
        ),
    ]

    for user in demo_users:
        try:
            c.execute(
                """
                INSERT INTO users
                (name,email,phone,password_hash,role)
                VALUES (?,?,?,?,?)
                """,
                user,
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


init_db()

app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(extract_bp, url_prefix="/api")
app.register_blueprint(validate_bp, url_prefix="/api")
app.register_blueprint(generate_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(appointment_bp, url_prefix="/api")
app.register_blueprint(notification_bp, url_prefix="/api")


@app.route("/")
def index():
    return jsonify({
        "status": "Backend Running",
        "message": "MamaCare API is Live 🚀"
    })


@app.route("/preview")
def preview():
    return send_file("../frontend/dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)