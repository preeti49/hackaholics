from flask import Blueprint, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import DATABASE
import re

auth_bp = Blueprint("auth", __name__)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "patient").strip().lower()

    if not name or not email or not password:
        return jsonify({"error": "Name, Email, and Password are required."}), 400
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Please enter a valid email address."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    password_hash = generate_password_hash(password)

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, email, phone, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, password_hash, role)
        )
        user_id = c.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "An account with this email already exists. Please Sign In."}), 400
    
    conn.close()
    return jsonify({
        "message": "Registration successful!",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }
    }), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    expected_role = data.get("role", "").strip().lower()

    if not email or not password:
        return jsonify({"error": "Email and Password are required."}), 400

    conn = get_db()
    c = conn.cursor()
    user_row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user_row:
        return jsonify({"error": "Invalid Credentials! Account not registered. Please Sign Up as a New User first."}), 401

    if not check_password_hash(user_row["password_hash"], password):
        return jsonify({"error": "Invalid Credentials! Incorrect password."}), 401

    if expected_role and user_row["role"] != expected_role:
        return jsonify({"error": f"Invalid Credentials! This account is registered as '{user_row['role']}'. Please select the correct portal."}), 403

    return jsonify({
        "message": "Login successful!",
        "user": {
            "id": user_row["id"],
            "name": user_row["name"],
            "email": user_row["email"],
            "phone": user_row["phone"],
            "role": user_row["role"]
        }
    }), 200

@auth_bp.route("/auth/patient-history/<path:patient_name>", methods=["GET"])
def get_patient_history(patient_name):
    conn = get_db()
    c = conn.cursor()
    docs = c.execute(
        "SELECT * FROM documents WHERE patient_name LIKE ? ORDER BY uploaded_at DESC",
        (f"%{patient_name}%",)
    ).fetchall()
    
    history = []
    for doc in docs:
        d_dict = dict(doc)
        fields = c.execute(
            "SELECT field_name, field_value, is_missing FROM extracted_fields WHERE document_id = ?",
            (doc["id"],)
        ).fetchall()
        d_dict["fields"] = {f["field_name"]: f["field_value"] for f in fields}
        history.append(d_dict)

    conn.close()
    return jsonify(history), 200

@auth_bp.route("/patients/search", methods=["GET"])
def search_patients():
    query = request.args.get("q", "").strip()
    conn = get_db()
    c = conn.cursor()
    if query:
        users = c.execute(
            "SELECT id, name, email, phone, created_at FROM users WHERE role = 'patient' AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)",
            (f"%{query}%", f"%{query}%", f"%{query}%")
        ).fetchall()
    else:
        users = c.execute(
            "SELECT id, name, email, phone, created_at FROM users WHERE role = 'patient' LIMIT 20"
        ).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users]), 200

@auth_bp.route("/patients/<int:patient_id>", methods=["GET", "PUT"])
def patient_profile(patient_id):
    conn = get_db()
    c = conn.cursor()
    if request.method == "PUT":
        data = request.get_json() or {}
        allowed = {"name", "phone", "insurance_provider", "insurance_policy", "insurance_status"}
        updates = {k: str(v).strip() for k, v in data.items() if k in allowed}
        if updates:
            sets = ", ".join(f"{key} = ?" for key in updates)
            c.execute(f"UPDATE users SET {sets} WHERE id = ? AND role = 'patient'", (*updates.values(), patient_id))
            conn.commit()
    patient = c.execute("SELECT id, name, email, phone, insurance_provider, insurance_policy, insurance_status, created_at FROM users WHERE id = ? AND role = 'patient'", (patient_id,)).fetchone()
    if not patient:
        conn.close()
        return jsonify({"error": "Patient not found"}), 404
    patient_data = dict(patient)
    patient_data["documents"] = [dict(r) for r in c.execute("SELECT * FROM documents WHERE patient_name LIKE ? ORDER BY uploaded_at DESC", (f"%{patient['name']}%",)).fetchall()]
    patient_data["appointments"] = [dict(r) for r in c.execute("SELECT * FROM appointments WHERE patient_name LIKE ? ORDER BY id DESC", (f"%{patient['name']}%",)).fetchall()]
    patient_data["prescriptions"] = [dict(r) for r in c.execute("SELECT * FROM prescriptions WHERE patient_name LIKE ? ORDER BY id DESC", (f"%{patient['name']}%",)).fetchall()]
    conn.close()
    return jsonify(patient_data), 200
