from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

appointment_bp = Blueprint("appointment", __name__)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@appointment_bp.route("/appointments/create", methods=["POST"])
def create_appointment():
    data = request.get_json() or {}
    patient_name = data.get("patient_name", "Unknown Patient").strip()
    doctor_name = data.get("doctor_name", "Dr. Arvind Sharma").strip()
    appointment_date = data.get("appointment_date", "").strip()
    appointment_time = data.get("appointment_time", "10:00 AM").strip()
    reason = data.get("reason", "General Consultation").strip()

    conn = get_db()
    c = conn.cursor()
    
    # Check if patient already has an active token (Waiting or In Consultation) under this doctor
    existing = c.execute(
        "SELECT * FROM appointments WHERE patient_name LIKE ? AND doctor_name LIKE ? AND status IN ('Waiting', 'In Consultation')",
        (f"%{patient_name}%", f"%{doctor_name}%")
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({
            "error": f"Active Token ({existing['token_no']}) already exists for '{patient_name}' with {doctor_name} (Status: {existing['status']}). Duplicate tokens cannot be generated until consultation is completed."
        }), 400

    # Calculate next token number for the day
    count = c.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    token_no = f"TOKEN #{count + 1:02d}"

    c.execute(
        "INSERT INTO appointments (token_no, patient_name, doctor_name, appointment_date, appointment_time, reason) VALUES (?, ?, ?, ?, ?, ?)",
        (token_no, patient_name, doctor_name, appointment_date, appointment_time, reason)
    )
    appointment_id = c.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Appointment Token Generated Successfully!",
        "appointment": {
            "id": appointment_id,
            "token_no": token_no,
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "reason": reason,
            "status": "Waiting"
        }
    }), 201

@appointment_bp.route("/appointments", methods=["GET"])
def get_appointments():
    doctor = request.args.get("doctor", "").strip()
    patient = request.args.get("patient", "").strip()
    conn = get_db()
    c = conn.cursor()
    where, args = [], []
    if doctor:
        where.append("doctor_name LIKE ?"); args.append(f"%{doctor}%")
    if patient:
        where.append("patient_name LIKE ?"); args.append(f"%{patient}%")
    query = "SELECT * FROM appointments" + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY id DESC"
    rows = c.execute(query, args).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

@appointment_bp.route("/appointments/<int:app_id>/status", methods=["PUT"])
def update_appointment_status(app_id):
    data = request.get_json() or {}
    new_status = data.get("status", "In Consultation")
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Token #{app_id} status updated to {new_status}"}), 200

@appointment_bp.route("/appointments/available-doctors", methods=["GET"])
def available_doctors():
    specialty = request.args.get("specialty", "General Medicine")
    doctors = [
        {"name": "Dr. Arvind Sharma", "specialty": "General Medicine", "available": True, "next_slot": "10:30 AM"},
        {"name": "Dr. Meera Iyer", "specialty": "Cardiology", "available": True, "next_slot": "11:15 AM"},
        {"name": "Dr. Nisha Patel", "specialty": "Gynecology", "available": True, "next_slot": "12:00 PM"},
        {"name": "Dr. Kabir Khan", "specialty": "Orthopedics", "available": False, "next_slot": "2:30 PM"},
    ]
    ranked = sorted(doctors, key=lambda d: (d["specialty"] != specialty, not d["available"]))
    return jsonify(ranked), 200

@appointment_bp.route("/prescriptions", methods=["GET", "POST"])
def prescriptions():
    conn = get_db(); c = conn.cursor()
    if request.method == "POST":
        data = request.get_json() or {}
        required = ["patient_name", "doctor_name", "diagnosis"]
        if any(not str(data.get(key, "")).strip() for key in required):
            conn.close(); return jsonify({"error": "Patient, doctor and diagnosis are required."}), 400
        import json
        c.execute("INSERT INTO prescriptions (patient_name, doctor_name, diagnosis, symptoms, advice, medicines) VALUES (?, ?, ?, ?, ?, ?)",
                  (data["patient_name"].strip(), data["doctor_name"].strip(), data["diagnosis"].strip(), data.get("symptoms", "").strip(), data.get("advice", "").strip(), json.dumps(data.get("medicines", []))))
        prescription_id = c.lastrowid; conn.commit()
        appointment_id = data.get("appointment_id")
        if appointment_id:
            c.execute("UPDATE appointments SET status = 'Completed' WHERE id = ?", (appointment_id,)); conn.commit()
        row = c.execute("SELECT * FROM prescriptions WHERE id = ?", (prescription_id,)).fetchone(); conn.close()
        return jsonify({"message": "Prescription saved and shared with the patient.", "prescription": dict(row)}), 201
    patient = request.args.get("patient", "").strip()
    rows = c.execute("SELECT * FROM prescriptions" + (" WHERE patient_name LIKE ?" if patient else "") + " ORDER BY id DESC", ([f"%{patient}%"] if patient else [])).fetchall()
    conn.close(); return jsonify([dict(r) for r in rows]), 200
