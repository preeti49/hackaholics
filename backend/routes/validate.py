from flask import Blueprint, request, jsonify
from models.document import get_all_documents, get_analytics

validate_bp = Blueprint("validate", __name__)

@validate_bp.route("/documents", methods=["GET"])
def get_documents():
    docs = get_all_documents()
    return jsonify(docs), 200

@validate_bp.route("/analytics", methods=["GET"])
def analytics():
    data = get_analytics()
    return jsonify(data), 200