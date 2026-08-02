import sqlite3
from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def save_document(patient_name, filename, file_type):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO documents (patient_name, filename, file_type) VALUES (?, ?, ?)",
        (patient_name, filename, file_type)
    )
    doc_id = c.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def save_extracted_fields(document_id, fields: dict):
    conn = get_db()
    c = conn.cursor()
    for field_name, field_value in fields.items():
        is_missing = 1 if not field_value else 0
        c.execute(
            "INSERT INTO extracted_fields (document_id, field_name, field_value, is_missing) VALUES (?, ?, ?, ?)",
            (document_id, field_name, str(field_value), is_missing)
        )
    conn.commit()
    conn.close()

def update_document_status(document_id, status, completeness_score):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE documents SET status=?, completeness_score=? WHERE id=?",
        (status, completeness_score, document_id)
    )
    conn.commit()
    conn.close()

def get_all_documents():
    conn = get_db()
    c = conn.cursor()
    docs = c.execute("SELECT * FROM documents ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return [dict(d) for d in docs]

def get_analytics():
    conn = get_db()
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    pending = c.execute("SELECT COUNT(*) FROM documents WHERE status='Pending Review'").fetchone()[0]
    missing = c.execute("SELECT COUNT(*) FROM documents WHERE status='Missing Info'").fetchone()[0]
    avg_score = c.execute("SELECT AVG(completeness_score) FROM documents").fetchone()[0] or 0
    conn.close()
    return {
        "total": total,
        "pending": pending,
        "missing": missing,
        "avg_completeness": round(avg_score)
    }