"""
orchestrator.py

Healthcare AI Pipeline Orchestrator

Coordinates the complete AI workflow:

PDF/Image
    ↓
OCR
    ↓
Document Classification
    ↓
Field Extraction
    ↓
Validation
    ↓
Completeness Score
    ↓
Priority Detection
    ↓
AI Follow-up Generation
    ↓
Document Draft Generation
    ↓
Workflow Reasoning

Author:
Healthcare AI Engine
"""

from pathlib import Path
import tempfile
import shutil
import logging

from ai_engine.ocr.easyocr_engine import EasyOCREngine
from ai_engine.ocr.pdf_parser import PDFParser

from ai_engine.extraction.document_classifier import DocumentClassifier
from ai_engine.extraction.field_extractor import FieldExtractor

from ai_engine.validation.missing_field_detector import MissingFieldDetector
from ai_engine.validation.completeness_score import CompletenessScore
from ai_engine.validation.priority_flag import PriorityFlag

from ai_engine.llm.followup_generator import FollowupGenerator
from ai_engine.llm.document_draft_generator import DocumentDraftGenerator
from ai_engine.llm.workflow_reasoning import WorkflowReasoning


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class HealthcareAIOrchestrator:

    def __init__(self):

        self.pdf_parser = PDFParser()

        self.ocr = EasyOCREngine()

        self.classifier = DocumentClassifier()

        self.extractor = FieldExtractor()

        self.detector = MissingFieldDetector()

        self.scorer = CompletenessScore()

        self.priority = PriorityFlag()

        self.followup = FollowupGenerator()

        self.drafts = DocumentDraftGenerator()

        self.workflow = WorkflowReasoning()

    ##########################################################

    def _ocr_pdf(self, pdf_path):

        temp_dir = tempfile.mkdtemp()

        pages = self.pdf_parser.convert_to_images(

            pdf_path,

            temp_dir

        )

        text = ""

        for page in pages:

            logger.info(f"OCR : {page}")

            text += self.ocr.extract_text(page)

            text += "\n"

        shutil.rmtree(temp_dir)

        return text

    ##########################################################

    def _ocr_image(self, image_path):

        return self.ocr.extract_text(image_path)

    ##########################################################

    def process_document(

        self,

        file_path,

        use_ai=True

    ):

        extension = Path(file_path).suffix.lower()

        ######################################################

        if extension == ".pdf":

            logger.info("Processing PDF")

            text = self._ocr_pdf(file_path)

        else:

            logger.info("Processing Image")

            text = self._ocr_image(file_path)

        ######################################################

        classification = self.classifier.classify(text)

        document_type = classification["document_type"]

        ######################################################

        extracted = self.extractor.extract_all(text)

        ######################################################

        validation = self.detector.detect_missing_fields(

            document_type,

            extracted

        )

        ######################################################

        completeness = self.scorer.calculate(

            extracted

        )

        ######################################################

        priority = self.priority.evaluate(

            document_type,

            completeness

        )

        ######################################################

        followups = self.followup.generate_followup_questions(

            extracted,

            validation,

            document_type

        )

        ######################################################

        drafts = self.drafts.generate_drafts(

            extracted,

            validation,

            document_type

        )

        ######################################################

        workflow = self.workflow.process(

            document_type,

            extracted,

            validation,

            completeness,

            priority,

            use_ai

        )

        ######################################################

        return {

            "document_type":

                document_type,

            "classification":

                classification,

            "ocr_text":

                text,

            "extracted_fields":

                extracted,

            "validation":

                validation,

            "completeness":

                completeness,

            "priority":

                priority,

            "followup_questions":

                followups,

            "generated_documents":

                drafts,

            "workflow":

                workflow

        }


##############################################################

if __name__ == "__main__":

    orchestrator = HealthcareAIOrchestrator()

    result = orchestrator.process_document(

        "uploads/sample_prior_auth.pdf",

        use_ai=False

    )

    from pprint import pprint

    pprint(result)