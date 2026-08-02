"""
document_classifier.py

Healthcare AI Document Classifier

Input:
    OCR Text

Output:
{
    "document_type": "Lab Report",
    "confidence": 94.2
}
"""

from collections import defaultdict
from typing import Dict


class DocumentClassifier:

    def __init__(self):

        # Keywords for every document

        self.document_keywords = {

            "Insurance Card": [

                "member id",
                "policy number",
                "insurance",
                "provider",
                "coverage",
                "subscriber",
                "copay",
                "deductible"

            ],

            "Prior Authorization": [

                "prior authorization",
                "authorization request",
                "requesting provider",
                "diagnosis",
                "cpt",
                "icd",
                "medical necessity",
                "procedure"

            ],

            "Patient Intake Form": [

                "patient name",
                "emergency contact",
                "medical history",
                "allergies",
                "current medications",
                "date of birth",
                "gender"

            ],

            "Prescription": [

                "rx",
                "take",
                "tablet",
                "capsule",
                "doctor",
                "physician",
                "dosage",
                "mg",
                "refill"

            ],

            "Lab Report": [

                "laboratory",
                "test result",
                "reference range",
                "hemoglobin",
                "glucose",
                "cholesterol",
                "blood",
                "specimen"

            ],

            "Medical Record": [

                "chief complaint",
                "assessment",
                "plan",
                "progress note",
                "clinical notes",
                "history of present illness",
                "vitals"

            ]

        }

    ###############################################################

    def preprocess(self, text: str) -> str:

        return text.lower()

    ###############################################################

    def keyword_score(self, text: str):

        text = self.preprocess(text)

        scores = defaultdict(int)

        for document_type, keywords in self.document_keywords.items():

            for keyword in keywords:

                if keyword in text:
                    scores[document_type] += 1

        return scores

    ###############################################################

    def classify(self, text: str) -> Dict:

        scores = self.keyword_score(text)

        if len(scores) == 0:

            return {

                "document_type": "Unknown",

                "confidence": 0

            }

        best_document = max(

            scores,

            key=scores.get

        )

        max_score = scores[best_document]

        total_keywords = len(

            self.document_keywords[best_document]

        )

        confidence = (

            max_score /

            total_keywords

        ) * 100

        confidence = round(confidence, 2)

        return {

            "document_type": best_document,

            "confidence": confidence

        }

    ###############################################################

    def top_matches(self, text: str):

        scores = self.keyword_score(text)

        ranked = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True

        )

        return ranked

    ###############################################################

    def add_document_type(

        self,

        document_name: str,

        keywords: list

    ):

        self.document_keywords[document_name] = keywords


##################################################################

if __name__ == "__main__":

    sample_text = """

    Patient Name : John Smith

    Date of Birth : 12/03/1990

    Diagnosis : Migraine

    Prior Authorization Request

    CPT Code : 70553

    ICD-10 : G43.909

    Requesting Provider

    """

    classifier = DocumentClassifier()

    result = classifier.classify(sample_text)

    print(result)

    print()

    print(classifier.top_matches(sample_text))