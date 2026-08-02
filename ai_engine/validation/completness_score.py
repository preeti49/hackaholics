"""
completeness_score.py

Calculates a weighted completeness score for healthcare documents.

This module uses centralized field weights from:
    ai_engine/config/field_weights.py

Author: Healthcare AI Engine
"""

from __future__ import annotations

from typing import Dict, Any

from ai_engine.config.field_weights import (
    FIELD_WEIGHTS,
    CRITICAL_FIELDS
)


class CompletenessScore:
    """
    Calculates the completeness score of an extracted document.
    """

    def __init__(self):

        self.field_weights = FIELD_WEIGHTS
        self.critical_fields = CRITICAL_FIELDS

    # =========================================================

    def calculate(
        self,
        extracted_fields: Dict[str, Any]
    ) -> Dict[str, Any]:

        total_weight = sum(self.field_weights.values())

        obtained_weight = 0

        filled_fields = []

        missing_fields = []

        critical_missing = []

        for field, weight in self.field_weights.items():

            value = extracted_fields.get(field)

            if self._is_valid(value):

                obtained_weight += weight
                filled_fields.append(field)

            else:

                missing_fields.append(field)

                if field in self.critical_fields:
                    critical_missing.append(field)

        score = round(
            (obtained_weight / total_weight) * 100,
            2
        )

        return {

            "score": score,

            "grade": self.grade(score),

            "filled_fields": filled_fields,

            "missing_fields": missing_fields,

            "critical_missing": critical_missing,

            "ready_for_submission": (
                score >= 90 and
                len(critical_missing) == 0
            )
        }

    # =========================================================

    @staticmethod
    def _is_valid(value) -> bool:

        if value is None:
            return False

        if isinstance(value, str):

            return value.strip() != ""

        if isinstance(value, list):

            return len(value) > 0

        return True

    # =========================================================

    @staticmethod
    def grade(score: float) -> str:

        if score >= 95:
            return "Excellent"

        elif score >= 85:
            return "Very Good"

        elif score >= 70:
            return "Good"

        elif score >= 50:
            return "Fair"

        return "Poor"

    # =========================================================

    def ready_for_submission(
        self,
        extracted_fields: Dict[str, Any]
    ) -> bool:

        result = self.calculate(extracted_fields)

        return result["ready_for_submission"]


# =============================================================
# Testing
# =============================================================

if __name__ == "__main__":

    sample = {

        "patient_name": "John Smith",

        "dob": "10/12/1994",

        "diagnosis": None,

        "procedure": "MRI Brain",

        "physician": "Dr Robert Brown",

        "member_id": "BX9281",

        "insurance_provider": "Blue Cross",

        "policy_number": None,

        "provider_npi": "1234567890",

        "cpt_code": None,

        "icd10": "G43.909",

        "allergies": "Penicillin"

    }

    scorer = CompletenessScore()

    result = scorer.calculate(sample)

    print("=" * 60)
    print("Completeness Result")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key:20}: {value}")

    print("=" * 60)

    print(
        "Ready For Submission :",
        scorer.ready_for_submission(sample)
    )