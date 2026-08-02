from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

notification_bp = Blueprint("notification", __name__)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@notification_bp.route("/notifications/<path:patient_name>", methods=["GET"])
def get_notifications(patient_name):
    conn = get_db()
    c = conn.cursor()
    rows = c.execute(
        "SELECT * FROM notifications WHERE patient_name LIKE ? ORDER BY sent_at DESC",
        (f"%{patient_name}%",)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

@notification_bp.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.get_json() or {}
    patient_name = data.get("patient_name", "").strip()
    document_id = data.get("document_id")
    title = data.get("title", "Missing Information Required").strip()
    message = data.get("message", "").strip()
    missing_fields = data.get("missing_fields", "")

    if isinstance(missing_fields, list):
        missing_fields = ", ".join(missing_fields)

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notifications (patient_name, document_id, title, message, missing_fields) VALUES (?, ?, ?, ?, ?)",
        (patient_name, document_id, title, message, missing_fields)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Notification sent to patient inbox!"}), 201
