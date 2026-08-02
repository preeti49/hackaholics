"""
Reusable Gemini Client

Every AI module should use this file instead
of directly calling Gemini.

Modules using this file:

followup_generator.py
workflow_reasoning.py
document_classifier.py (fallback)
"""

from __future__ import annotations

import json
import logging
import time
from typing import Dict, List, Optional

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = GEMINI_MODEL

    #######################################################

    def generate_text(

        self,

        prompt: str,

        retries: int = 3

    ) -> str:

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=prompt

                )

                return response.text

            except Exception as e:

                logger.error(e)

                time.sleep(2 ** attempt)

        raise Exception("Gemini API failed.")

    #######################################################

    def generate_json(

        self,

        prompt: str,

        retries: int = 3

    ) -> Dict:

        instruction = f"""

Return ONLY valid JSON.

No markdown.

No explanation.

{prompt}

"""

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=instruction

                )

                text = response.text.strip()

                text = text.replace(

                    "```json",

                    ""

                )

                text = text.replace(

                    "```",

                    ""

                )

                return json.loads(text)

            except Exception as e:

                logger.warning(e)

                time.sleep(

                    2 ** attempt

                )

        raise Exception(

            "Could not generate JSON."

        )

    #######################################################

    def summarize(

        self,

        text: str

    ) -> str:

        prompt = f"""

Summarize this healthcare document.

{text}

"""

        return self.generate_text(prompt)

    #######################################################

    def classify_document(

        self,

        text: str

    ) -> Dict:

        prompt = f"""

Identify document type.

Possible types:

Insurance Card

Prior Authorization

Prescription

Medical Record

Lab Report

Patient Intake Form

Return JSON:

{{
"document_type":"",
"confidence":0
}}

{text}

"""

        return self.generate_json(prompt)

    #######################################################

    def ask(

        self,

        system_prompt: str,

        user_prompt: str

    ) -> str:

        final_prompt = f"""

SYSTEM

{system_prompt}

-------------------

USER

{user_prompt}

"""

        return self.generate_text(

            final_prompt

        )


##########################################################

if __name__ == "__main__":

    gemini = GeminiClient()

    print(

        gemini.summarize(

            """

Patient Name : John

Diagnosis : Migraine

MRI Recommended

"""

        )

    )

    print()

    print(

        gemini.classify_document(

            """

Policy Number

Insurance Provider

Member ID

"""

        )

    )