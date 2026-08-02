"""
priority_flag.py

Healthcare AI Priority Engine

Determines the processing priority of a document
based on:
    - Document Type
    - Completeness Score
    - Missing Critical Fields

Output Example
--------------
{
    "priority": "Critical",
    "color": "red",
    "reason": "...",
    "queue_order": 1
}
"""

from __future__ import annotations

from typing import Dict


class PriorityFlag:

    def __init__(self):

        # Higher number = higher business priority
        self.document_priority = {

            "Prior Authorization": 100,
            "Insurance Card": 90,
            "Medical Record": 80,
            "Lab Report": 70,
            "Prescription": 60,
            "Patient Intake Form": 50,
            "Unknown": 20
        }

    ###########################################################

    def evaluate(
        self,
        document_type: str,
        completeness_result: Dict
    ) -> Dict:

        score = completeness_result["score"]

        critical_missing = completeness_result["critical_missing"]

        ###############################################

        if critical_missing:

            return {

                "priority": "Critical",

                "color": "red",

                "queue_order": 1,

                "reason":
                    f"Critical fields missing: "
                    f"{', '.join(critical_missing)}"

            }

        ###############################################

        if score < 60:

            return {

                "priority": "High",

                "color": "orange",

                "queue_order": 2,

                "reason":
                    "Low completeness score"

            }

        ###############################################

        if score < 85:

            return {

                "priority": "Medium",

                "color": "yellow",

                "queue_order": 3,

                "reason":
                    "Needs manual verification"

            }

        ###############################################

        return {

            "priority": "Low",

            "color": "green",

            "queue_order": 4,

            "reason":
                "Ready for submission"

        }

    ###########################################################

    def business_priority(
        self,
        document_type: str
    ) -> int:

        return self.document_priority.get(

            document_type,

            0

        )

    ###########################################################

    def sort_documents(
        self,
        documents: list
    ):

        """
        Sort documents by business importance.

        documents = [
            {
                "document_type":"Lab Report"
            },
            ...
        ]
        """

        return sorted(

            documents,

            key=lambda x:

            self.business_priority(

                x["document_type"]

            ),

            reverse=True

        )


###############################################################

if __name__ == "__main__":

    completeness = {

        "score": 73,

        "critical_missing": [

            "diagnosis",

            "cpt_code"

        ]

    }

    priority = PriorityFlag()

    result = priority.evaluate(

        "Prior Authorization",

        completeness

    )

    print(result)

    print()

    documents = [

        {

            "document_type":

            "Lab Report"

        },

        {

            "document_type":

            "Insurance Card"

        },

        {

            "document_type":

            "Prior Authorization"

        }

    ]

    print(

        priority.sort_documents(

            documents

        )

    )