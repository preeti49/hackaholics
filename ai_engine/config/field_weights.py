FIELD_WEIGHTS = {

    "patient_name": 15,
    "dob": 10,
    "gender": 5,
    "phone": 5,
    "email": 5,

    "insurance_provider": 15,
    "member_id": 20,
    "policy_number": 15,
    "group_number": 10,

    "physician": 15,
    "provider_npi": 15,

    "diagnosis": 20,
    "procedure": 15,

    "cpt_code": 20,
    "cpt_codes": 20,

    "icd10": 20,
    "icd10_codes": 20,

    "hospital": 10,
    "facility_name": 10,

    "service_description": 10,
    "clinical_justification": 15,

    "allergies": 10,
    "medications": 10,

    "urgency": 10
}


CRITICAL_FIELDS = {

    "patient_name",

    "member_id",

    "insurance_provider",

    "physician",

    "provider_npi",

    "diagnosis",

    "procedure",

    "cpt_code",

    "cpt_codes",

    "icd10",

    "icd10_codes"

}