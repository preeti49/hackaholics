REQUIRED_FIELDS = [
    "patient_name", "age", "phone",
    "email", "address",
    "insurance_number", "policy_document",
    "emergency_contact"
]

def validate_fields(extracted: dict) -> dict:
    validation = {}
    for field in REQUIRED_FIELDS:
        val = extracted.get(field)
        is_missing = val is None or str(val).strip() == "" or str(val).lower() in ("none", "null", "n/a", "unknown")
        validation[field] = {
            "value": None if is_missing else val,
            "missing": is_missing
        }
    return validation

def calculate_completeness_score(validation: dict) -> int:
    if not validation:
        return 0
    total = len(validation)
    present = sum(1 for v in validation.values() if not v.get("missing"))
    return int((present / total) * 100)

def get_missing_fields(validation: dict) -> list:
    return [field for field, data in validation.items() if data.get("missing")]

def determine_status(score: int) -> str:
    if score == 100:
        return "Completed"
    elif score >= 60:
        return "Pending Review"
    else:
        return "Missing Info"
