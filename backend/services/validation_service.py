from utils.validation_utils import validate_fields, calculate_completeness_score, get_missing_fields, determine_status

def validate_report(extracted_fields: dict, doc_type: str = "Medical Report") -> dict:
    """
    Validates report fields, checks for missing info, invalid values, and insurance form completeness.
    """
    validation = validate_fields(extracted_fields)
    score = calculate_completeness_score(validation)
    missing = get_missing_fields(validation)
    status = determine_status(score)

    is_insurance_incomplete = False
    if doc_type == "Insurance Form":
        ins_num = extracted_fields.get("insurance_number")
        policy_num = extracted_fields.get("policy_number")
        if not ins_num or not policy_num or ins_num == "N/A" or policy_num == "N/A":
            is_insurance_incomplete = True
            if "insurance_number" not in missing:
                missing.append("insurance_number")

    return {
        "validation": validation,
        "completeness_score": score,
        "missing_fields": missing,
        "status": status,
        "is_insurance_incomplete": is_insurance_incomplete
    }
