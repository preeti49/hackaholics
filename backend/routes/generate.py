from flask import Blueprint, request, jsonify
from utils.llm_utils import generate_followup_message

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-followup", methods=["POST"])
def generate_followup():
    data = request.get_json()
    patient_name = data.get("patient_name", "Patient")
    missing_fields = data.get("missing_fields", [])

    if not missing_fields:
        return jsonify({"message": "No missing fields — form is complete"}), 200

    followup = generate_followup_message(patient_name, missing_fields)
    return jsonify({"followup_message": followup}), 200

@generate_bp.route("/generate-paperwork", methods=["POST"])
def generate_paperwork():
    data = request.get_json() or {}
    workflow = data.get("workflow_type", "Prior Authorization")
    patient_name = data.get("patient_name", "Patient")
    fields = data.get("fields", {}) or {}
    missing = data.get("missing_fields", []) or []
    insurance = fields.get("insurance_number") or fields.get("policy_document") or "Pending verification"
    draft = f"""{workflow} — Administrative Draft

Patient: {patient_name}
Insurance / Member ID: {insurance}
Request purpose: Administrative review and benefits processing.

Attached records have been received and indexed. This draft is for staff review only; it does not make a clinical recommendation or treatment decision.

Required follow-up: {', '.join(missing) if missing else 'No missing fields identified. Please verify all details before submission.'}

Prepared by: Mama Care Administrative Automation
"""
    return jsonify({"draft": draft, "status": "Draft ready for staff review"}), 200
