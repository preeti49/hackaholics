from flask import Blueprint, request, jsonify
import os
from uuid import uuid4
from werkzeug.utils import secure_filename
import sqlite3
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from models.document import save_document
from services.ocr_service import run_ocr
from services.classification_service import classify_document
from services.extraction_service import extract_important_info
from services.validation_service import validate_report
from config import DATABASE

upload_bp = Blueprint("upload", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    patient_name = request.form.get("patient_name", "Unknown")

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use PDF, PNG, JPG"}), 400

    original_filename = secure_filename(file.filename)
    filename = f"{uuid4().hex}_{original_filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    file_type = filename.rsplit(".", 1)[1].lower()
    doc_id = save_document(patient_name, filename, file_type)

    return jsonify({
        "message": "File uploaded successfully",
        "document_id": doc_id,
        "filename": filename,
        "original_filename": original_filename,
        "file_type": file_type,
        "filepath": filepath
    }), 200

@upload_bp.route("/administrative/process-batch", methods=["POST"])
def process_batch():
    files = request.files.getlist("files")
    patient_name = request.form.get("patient_name", "Unknown Patient").strip()
    workflow_type = request.form.get("workflow_type", "Intake Form").strip()
    if not files:
        return jsonify({"error": "Upload at least one supported document."}), 400
    results = []
    for file in files[:10]:
        if not file or not file.filename or not allowed_file(file.filename):
            results.append({"filename": getattr(file, "filename", "Unknown"), "status": "Skipped", "error": "Unsupported file type"})
            continue
        original = secure_filename(file.filename)
        filename = f"{uuid4().hex}_{original}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        file_type = original.rsplit(".", 1)[1].lower()
        doc_id = save_document(patient_name, filename, file_type)
        try:
            raw_text = run_ocr(filepath, file_type) or ""
            doc_type = workflow_type if workflow_type != "Auto classify" else classify_document(raw_text)
            fields = extract_important_info(raw_text)
            if not fields.get("patient_name") or fields.get("patient_name") == "N/A": fields["patient_name"] = patient_name
            validation = validate_report(fields, doc_type)
            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()
                c.execute("UPDATE documents SET document_type=?, status=?, completeness_score=? WHERE id=?", (doc_type, validation["status"], validation["completeness_score"], doc_id))
                for key, value in fields.items():
                    c.execute("INSERT INTO extracted_fields (document_id, field_name, field_value, is_missing) VALUES (?, ?, ?, ?)", (doc_id, key, str(value or ""), int(key in validation["missing_fields"])))
            results.append({"document_id": doc_id, "filename": original, "document_type": doc_type, "status": validation["status"], "completeness_score": validation["completeness_score"], "missing_fields": validation["missing_fields"], "extracted_fields": fields})
        except Exception as error:
            results.append({"document_id": doc_id, "filename": original, "status": "Needs Review", "error": "Could not fully extract this file. It is safely queued for manual review."})
    return jsonify({"workflow_type": workflow_type, "processed": len(results), "results": results}), 200
