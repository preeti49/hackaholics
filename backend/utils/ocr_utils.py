import pdfplumber
from PIL import Image
import io

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        try:
            import easyocr
            _reader = easyocr.Reader(["en", "hi"])  # English + Hindi
        except Exception:
            _reader = False
    return _reader

def extract_text_from_pdf(filepath: str) -> str:
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
        
    # If pdfplumber gets nothing (scanned PDF), fall back to OCR
    if not text.strip():
        text = extract_text_from_image(filepath)
    return text.strip()

def extract_text_from_image(filepath: str) -> str:
    reader = get_reader()
    if reader:
        try:
            results = reader.readtext(filepath, detail=0)
            return " ".join(results)
        except Exception:
            return ""
    return ""

def extract_text(filepath: str, file_type: str) -> str:
    if file_type == "txt":
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        except Exception:
            return ""
    elif file_type == "pdf":
        return extract_text_from_pdf(filepath)
    else:
        return extract_text_from_image(filepath)
