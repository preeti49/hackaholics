"""
field_extractor.py

Extract structured healthcare information
from OCR text using Regular Expressions.

Author: Healthcare AI Engine
"""

from __future__ import annotations

import re
from typing import Dict, Optional


class FieldExtractor:

    def __init__(self):

        self.patterns = {

            "patient_name":
                r"(?:patient\s*name)\s*[:\-]?\s*(.+)",

            "dob":
                r"(?:dob|date\s*of\s*birth)\s*[:\-]?\s*([0-9/\-]+)",

            "gender":
                r"(?:gender)\s*[:\-]?\s*(male|female|other)",

            "phone":
                r"(?:phone|mobile|contact)\s*[:\-]?\s*([\d\-\+\(\)\s]+)",

            "email":
                r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",

            "insurance_provider":
                r"(?:insurance\s*provider)\s*[:\-]?\s*(.+)",

            "member_id":
                r"(?:member\s*id)\s*[:\-]?\s*([A-Za-z0-9\-]+)",

            "policy_number":
                r"(?:policy\s*number)\s*[:\-]?\s*([A-Za-z0-9\-]+)",

            "diagnosis":
                r"(?:diagnosis)\s*[:\-]?\s*(.+)",

            "procedure":
                r"(?:procedure)\s*[:\-]?\s*(.+)",

            "physician":
                r"(?:physician|doctor|provider)\s*[:\-]?\s*(.+)",

            "hospital":
                r"(?:hospital)\s*[:\-]?\s*(.+)",

            "cpt_code":
                r"(?:cpt(?:\s*code)?)\s*[:\-]?\s*([A-Za-z0-9]+)",

            "icd10":
                r"(?:icd(?:-10)?(?:\s*code)?)\s*[:\-]?\s*([A-Za-z0-9.\-]+)",

            "allergies":
                r"(?:allergies)\s*[:\-]?\s*(.+)",

            "medications":
                r"(?:current\s*medications|medications?)\s*[:\-]?\s*(.+)"
        }

    ####################################################

    def clean_value(self, value: str) -> str:

        value = value.strip()

        value = value.replace("\n", " ")

        value = re.sub(r"\s+", " ", value)

        return value

    ####################################################

    def extract_field(
        self,
        text: str,
        pattern: str
    ) -> Optional[str]:

        match = re.search(

            pattern,

            text,

            flags=re.IGNORECASE

        )

        if not match:

            return None

        return self.clean_value(

            match.group(1)

        )

    ####################################################

    def extract_all(
        self,
        text: str
    ) -> Dict:

        extracted = {}

        for field, pattern in self.patterns.items():

            extracted[field] = self.extract_field(

                text,

                pattern

            )

        return extracted

    ####################################################

    def available_fields(
        self,
        extracted: Dict
    ):

        return [

            key

            for key, value in extracted.items()

            if value is not None

        ]

    ####################################################

    def missing_fields(
        self,
        extracted: Dict
    ):

        return [

            key

            for key, value in extracted.items()

            if value is None

        ]

    ####################################################

    def pretty_print(
        self,
        extracted: Dict
    ):

        print("=" * 50)

        for key, value in extracted.items():

            print(

                f"{key:25} : {value}"

            )

        print("=" * 50)


########################################################

if __name__ == "__main__":

    sample_text = """

    Patient Name : John Smith

    Date of Birth : 12/05/1994

    Gender : Male

    Phone : +91 9876543210

    Insurance Provider : Blue Cross

    Member ID : BX-892731

    Policy Number : P-11111

    Physician : Dr. Robert Brown

    Diagnosis : Migraine

    Procedure : MRI Brain

    CPT Code : 70553

    ICD-10 : G43.909

    Allergies : Penicillin

    Current Medications : Aspirin

    """

    extractor = FieldExtractor()

    data = extractor.extract_all(sample_text)

    extractor.pretty_print(data)

    print()

    print("Available Fields")

    print(extractor.available_fields(data))

    print()

    print("Missing Fields")

    print(extractor.missing_fields(data))