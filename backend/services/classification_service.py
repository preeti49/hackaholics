import re

def classify_document(raw_text: str) -> str:
    """
    Classifies raw document text into one of 5 standard categories:
    - Blood Test
    - MRI Report
    - X-Ray Report
    - Prescription
    - Insurance Form
    """
    text_lower = raw_text.lower()

    if any(k in text_lower for k in ["blood test", "hemoglobin", "wbc", "platelet", "lipid", "cholesterol", "cbc", "cbc report", "glucose"]):
        return "Blood Test"
    elif any(k in text_lower for k in ["mri", "magnetic resonance", "brain mri", "spine mri", "t1-weighted", "t2-weighted", "contrast"]):
        return "MRI Report"
    elif any(k in text_lower for k in ["x-ray", "xray", "radiograph", "radiology", "chest pa", "fracture", "lung fields"]):
        return "X-Ray Report"
    elif any(k in text_lower for k in ["prescription", "rx", "tab.", "cap.", "mg", "syrup", "dosage", "once daily", "bid", "tid"]):
        return "Prescription"
    elif any(k in text_lower for k in ["insurance", "policy", "claim", "tpa", "cashless", "pre-authorization", "coverage", "sum insured"]):
        return "Insurance Form"
    else:
        return "Medical Report"
