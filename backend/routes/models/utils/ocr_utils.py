import pdfplumber
import easyocr
from PIL import Image
import io

reader = easyocr.Reader(["en", "hi"])  # English + Hindi

def extract_text_from_pdf(filepath: str) -> str:
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    # If pdfplumber gets nothing (scanned PDF), fall back to OCR
    if not text.strip():
        text = extract_text_from_image(filepath)
    return text.strip()

def extract_text_from_image(filepath: str) -> str:
    results = reader.readtext(filepath, detail=0)
    return " ".join(results)

def extract_text(filepath: str, file_type: str) -> str:
    if file_type == "pdf":
        return extract_text_from_pdf(filepath)
    else:
        return extract_text_from_image(filepath)
    