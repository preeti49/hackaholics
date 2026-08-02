"""
workflow_reasoning.py

Healthcare AI Workflow Reasoning Engine

Responsibilities
----------------
1. Decide the next workflow step.
2. Analyze document completeness.
3. Handle missing critical fields.
4. Decide when human review is required.
5. Recommend follow-up actions.

Author: Healthcare AI Engine
"""

from __future__ import annotations

import logging
from typing import Dict, Any

from ai_engine.llm.gemini_client import GeminiClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowReasoning:

    def __init__(self, gemini_client: GeminiClient = None):

        self.client = gemini_client or GeminiClient()

    ############################################################

    def build_prompt(

        self,

        document_type: str,

        extracted_fields: Dict[str, Any],

        validation_result: Dict[str, Any],

        completeness_result: Dict[str, Any],

        priority_result: Dict[str, Any]

    ) -> str:

        return f"""

You are an expert healthcare administrative workflow engine.

Your responsibility is to determine the NEXT ACTION.

Document Type

{document_type}

Extracted Fields

{extracted_fields}

Validation Result

{validation_result}

Completeness Result

{completeness_result}

Priority

{priority_result}

Available Actions

AUTO_SUBMIT

REQUEST_PATIENT_INFORMATION

REQUEST_PROVIDER_INFORMATION

REQUEST_INSURANCE_INFORMATION

MANUAL_REVIEW

ESCALATE

RERUN_OCR

REJECT_DOCUMENT

Rules

1. If OCR quality is poor -> RERUN_OCR

2. If patient information is missing ->
REQUEST_PATIENT_INFORMATION

3. If provider information is missing ->
REQUEST_PROVIDER_INFORMATION

4. If insurance information is missing ->
REQUEST_INSURANCE_INFORMATION

5. If critical fields are missing ->
MANUAL_REVIEW

6. If document is complete ->
AUTO_SUBMIT

7. If urgent and incomplete ->
ESCALATE

Return ONLY JSON

{
    "next_action":"",
    "reason":"",
    "confidence":95,
    "human_review":false,
    "estimated_completion":"5 minutes"
}

"""

    ############################################################

    def reason(

        self,

        document_type,

        extracted_fields,

        validation_result,

        completeness_result,

        priority_result

    ) -> Dict:

        prompt = self.build_prompt(

            document_type,

            extracted_fields,

            validation_result,

            completeness_result,

            priority_result

        )

        logger.info(

            "Running workflow reasoning..."

        )

        return self.client.generate_json(

            prompt

        )

    ############################################################

    def local_reasoning(

        self,

        validation_result,

        completeness_result,

        priority_result

    ) -> Dict:

        score = completeness_result.get(

            "score",

            0

        )

        critical = completeness_result.get(

            "critical_missing",

            []

        )

        priority = priority_result.get(

            "priority",

            "Low"

        )

        if critical:

            return {

                "next_action": "MANUAL_REVIEW",

                "reason": "Critical healthcare fields are missing.",

                "confidence": 98,

                "human_review": True

            }

        if priority == "Critical":

            return {

                "next_action": "ESCALATE",

                "reason": "Urgent administrative processing required.",

                "confidence": 96,

                "human_review": True

            }

        if score >= 95:

            return {

                "next_action": "AUTO_SUBMIT",

                "reason": "Document is complete.",

                "confidence": 99,

                "human_review": False

            }

        if score >= 75:

            return {

                "next_action": "REQUEST_PATIENT_INFORMATION",

                "reason": "Minor information is missing.",

                "confidence": 94,

                "human_review": False

            }

        return {

            "next_action": "RERUN_OCR",

            "reason": "Document quality appears insufficient.",

            "confidence": 88,

            "human_review": False

        }

    ############################################################

    def process(

        self,

        document_type,

        extracted_fields,

        validation_result,

        completeness_result,

        priority_result,

        use_ai=True

    ):

        if use_ai:

            try:

                return self.reason(

                    document_type,

                    extracted_fields,

                    validation_result,

                    completeness_result,

                    priority_result

                )

            except Exception as e:

                logger.warning(

                    f"Gemini unavailable: {e}"

                )

        return self.local_reasoning(

            validation_result,

            completeness_result,

            priority_result

        )


############################################################

if __name__ == "__main__":

    extracted = {

        "patient_name": "John Smith",

        "member_id": "ABC123",

        "diagnosis": "Migraine"

    }

    validation = {

        "missing_fields": [

            {

                "label": "Provider NPI",

                "reason": "Missing"

            }

        ]

    }

    completeness = {

        "score": 82,

        "critical_missing": []

    }

    priority = {

        "priority": "Medium"

    }

    workflow = WorkflowReasoning()

    result = workflow.process(

        document_type="Prior Authorization",

        extracted_fields=extracted,

        validation_result=validation,

        completeness_result=completeness,

        priority_result=priority,

        use_ai=False

    )

    print(result)