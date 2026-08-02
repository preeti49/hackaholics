"""
missing_field_detector.py

Detect missing required fields based on
the classified document type.

Input:
    document_type
    extracted_fields

Output:
{
    "status": "Incomplete",
    "missing_fields": [...],
    "filled_fields": [...],
    "completion": 72.5
}
"""

from __future__ import annotations

from typing import Dict, List


class MissingFieldDetector:

    def __init__(self):

        # Required fields for each document

        self.required_fields = {

            "Insurance Card": [

                "patient_name",
                "insurance_provider",
                "member_id",
                "policy_number"

            ],

            "Prior Authorization": [

                "patient_name",
                "physician",
                "diagnosis",
                "procedure",
                "cpt_code",
                "icd10"

            ],

            "Patient Intake Form": [

                "patient_name",
                "dob",
                "gender",
                "phone",
                "allergies",
                "medications"

            ],

            "Prescription": [

                "patient_name",
                "physician",
                "medications"

            ],

            "Lab Report": [

                "patient_name",
                "dob",
                "diagnosis"

            ],

            "Medical Record": [

                "patient_name",
                "dob",
                "physician",
                "diagnosis"

            ]

        }

    ###########################################################

    def detect_missing_fields(
        self,
        document_type: str,
        extracted_fields: Dict
    ) -> Dict:

        required = self.required_fields.get(

            document_type,

            []

        )

        missing = []

        filled = []

        for field in required:

            value = extracted_fields.get(field)

            if value is None:

                missing.append(field)

            elif str(value).strip() == "":

                missing.append(field)

            else:

                filled.append(field)

        total = len(required)

        if total == 0:

            completion = 0

        else:

            completion = round(

                (len(filled) / total) * 100,

                2

            )

        status = (

            "Complete"

            if len(missing) == 0

            else "Incomplete"

        )

        return {

            "document_type": document_type,

            "status": status,

            "required_fields": required,

            "filled_fields": filled,

            "missing_fields": missing,

            "completion": completion

        }

    ###########################################################

    def is_complete(

        self,

        document_type: str,

        extracted_fields: Dict

    ) -> bool:

        result = self.detect_missing_fields(

            document_type,

            extracted_fields

        )

        return result["status"] == "Complete"


###############################################################

if __name__ == "__main__":

    sample_document = "Prior Authorization"

    extracted = {

        "patient_name": "John Smith",

        "physician": "Dr Brown",

        "diagnosis": None,

        "procedure": "MRI Brain",

        "cpt_code": None,

        "icd10": "G43.909"

    }

    detector = MissingFieldDetector()

    result = detector.detect_missing_fields(

        sample_document,

        extracted

    )

    print(result)