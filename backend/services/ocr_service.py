import os
from utils.ocr_utils import extract_text as base_extract_text

def run_ocr(filepath: str, file_type: str) -> str:
    """
    Extracts text from uploaded PDF, PNG, JPG, TXT, DOCX files.
    """
    if not os.path.exists(filepath):
        return ""
    return base_extract_text(filepath, file_type)
