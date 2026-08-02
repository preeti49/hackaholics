from flask import Blueprint, request, jsonify
import os
import sqlite3
from config import UPLOAD_FOLDER, DATABASE

from services.ocr_service import run_ocr
from services.classification_service import classify_document
from services.extraction_service import extract_important_info
from services.validation_service import validate_report
from services.ai_service import generate_medical_ai_summary

extract_bp = Blueprint("extract", __name__)

@extract_bp.route("/extract", methods=["POST"])
def extract():
    data = request.get_json() or {}
    document_id = data.get("document_id")
    filename = data.get("filename")
    file_type = data.get("file_type")
    language = data.get("language", "English")
    patient_name = data.get("patient_name", "Rahul Sharma")

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    # 1. OCR Text Extraction (ocr_service)
    raw_text = run_ocr(filepath, file_type)

    # 2. Document Classification (classification_service)
    doc_type = classify_document(raw_text)

    # 3. Important Information Extraction (extraction_service)
    extracted = extract_important_info(raw_text)
    if not extracted.get("patient_name") or extracted.get("patient_name") == "N/A":
        extracted["patient_name"] = patient_name

    # 4. Validation (validation_service)
    val_result = validate_report(extracted, doc_type)
    score = val_result["completeness_score"]
    missing = val_result["missing_fields"]
    status = val_result["status"]

    # 5. AI Summary & Multilingual Translation (ai_service)
    ai_result = generate_medical_ai_summary(raw_text, language)

    # 6. Save document classification & details to DB
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "UPDATE documents SET document_type = ?, status = ?, completeness_score = ? WHERE id = ?",
            (doc_type, status, score, document_id)
        )
        
        # Save extracted fields
        for field, value in extracted.items():
            is_miss = 1 if field in missing else 0
            c.execute(
                "INSERT INTO extracted_fields (document_id, field_name, field_value, is_missing) VALUES (?, ?, ?, ?)",
                (document_id, field, str(value), is_miss)
            )

        # 7. Auto Alerts & Notifications System
        # Alert 1: Report Uploaded Successfully
        c.execute(
            "INSERT INTO notifications (patient_name, document_id, title, message, missing_fields) VALUES (?, ?, ?, ?, ?)",
            (patient_name, document_id, "Report Uploaded Successfully", f"Your document '{filename}' has been processed and classified as '{doc_type}'.", "")
        )

        # Alert 2: AI Summary Ready
        c.execute(
            "INSERT INTO notifications (patient_name, document_id, title, message, missing_fields) VALUES (?, ?, ?, ?, ?)",
            (patient_name, document_id, "AI Medical Summary Ready", f"AI Summary & Recommendations generated in {language}.", "")
        )

        # Alert 3: Missing Documents Alert
        if missing:
            c.execute(
                "INSERT INTO notifications (patient_name, document_id, title, message, missing_fields) VALUES (?, ?, ?, ?, ?)",
                (
                    patient_name,
                    document_id,
                    f"Action Required: Missing Information in {doc_type}",
                    f"Dear {patient_name}, required fields are missing: {', '.join(missing)}. Please update.",
                    ", ".join(missing)
                )
            )

        # Alert 4: Insurance Pending Alert
        if val_result.get("is_insurance_incomplete") or doc_type == "Insurance Form":
            c.execute(
                "INSERT INTO notifications (patient_name, document_id, title, message, missing_fields) VALUES (?, ?, ?, ?, ?)",
                (patient_name, document_id, "Insurance Claim Pending Review", "Your insurance document has been logged and sent to Receptionist Desk for verification.", "")
            )

        conn.commit()
        conn.close()
    except Exception as e:
        print("Extract DB update error:", e)

    return jsonify({
        "document_id": document_id,
        "document_type": doc_type,
        "extracted_fields": extracted,
        "validation": val_result["validation"],
        "completeness_score": score,
        "missing_fields": missing,
        "status": status,
        "ai_summary": ai_result["summary"],
        "language": language,
        "raw_text": raw_text[:500]
    }), 200