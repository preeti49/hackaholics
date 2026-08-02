"""
followup_generator.py

AI-powered Follow-up Question Generator

Responsibilities
----------------
1. Analyze missing fields.
2. Generate patient-friendly follow-up questions.
3. Suggest proper input type.
4. Return structured JSON.

Author: Healthcare AI Engine
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any

from ai_engine.llm.gemini_client import GeminiClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FollowupGenerator:

    def __init__(self, gemini_client: GeminiClient = None):

        self.client = gemini_client or GeminiClient()

    #########################################################

    def build_prompt(

        self,

        extracted_fields: Dict[str, Any],

        validation_result: Dict[str, Any],

        doc_type: str

    ) -> str:

        missing_fields = validation_result.get(

            "missing_fields",

            []

        )

        return f"""

You are an experienced healthcare administrative assistant.

Your responsibility is to help patients complete healthcare paperwork.

Document Type

{doc_type}

Already Extracted Information

{extracted_fields}

Missing Fields

{missing_fields}

Instructions

1. Generate one question for each missing field.

2. Questions must be easy to understand.

3. Never ask for information already available.

4. If the missing field requires a document,
   ask the patient to upload it.

5. Return ONLY valid JSON.

Return Format

{{
    "questions":[

        {{
            "field":"",
            "question":"",
            "input_type":"text"
        }}

    ]
}}

Allowed input_type

text

date

number

email

phone

file

textarea

"""

    #########################################################

    def generate_followup_questions(

        self,

        extracted_fields: Dict[str, Any],

        validation_result: Dict[str, Any],

        doc_type: str

    ) -> Dict:

        missing = validation_result.get(

            "missing_fields",

            []

        )

        if not missing:

            return {

                "questions": [],

                "message": "No follow-up required."

            }

        prompt = self.build_prompt(

            extracted_fields,

            validation_result,

            doc_type

        )

        logger.info(

            "Generating follow-up questions..."

        )

        return self.client.generate_json(

            prompt

        )

    #########################################################

    def generate_as_list(

        self,

        extracted_fields,

        validation_result,

        doc_type

    ) -> List[str]:

        result = self.generate_followup_questions(

            extracted_fields,

            validation_result,

            doc_type

        )

        questions = []

        for item in result.get(

            "questions",

            []

        ):

            questions.append(

                item["question"]

            )

        return questions

    #########################################################

    def print_questions(

        self,

        extracted_fields,

        validation_result,

        doc_type

    ):

        result = self.generate_followup_questions(

            extracted_fields,

            validation_result,

            doc_type

        )

        print("=" * 60)

        print("FOLLOW-UP QUESTIONS")

        print("=" * 60)

        for i, q in enumerate(

            result.get(

                "questions",

                []

            ),

            start=1

        ):

            print(

                f"{i}. {q['question']}"

            )

            print(

                f"   Field : {q['field']}"

            )

            print(

                f"   Input : {q['input_type']}"

            )

            print()

    #########################################################

    def has_followups(

        self,

        validation_result

    ) -> bool:

        return len(

            validation_result.get(

                "missing_fields",

                []

            )

        ) > 0


###############################################################

if __name__ == "__main__":

    extracted = {

        "patient_name": "John Smith",

        "dob": "12/04/1994",

        "procedure": "MRI Brain"

    }

    validation = {

        "missing_fields": [

            {

                "label": "Diagnosis",

                "reason": "Not detected"

            },

            {

                "label": "Member ID",

                "reason": "Missing"

            },

            {

                "label": "Insurance Card",

                "reason": "Document not uploaded"

            }

        ]

    }

    generator = FollowupGenerator()

    generator.print_questions(

        extracted,

        validation,

        "Prior Authorization"

    )