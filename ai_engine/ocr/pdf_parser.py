"""
pdf_parser.py

Healthcare AI PDF Parser

Responsibilities
----------------
1. Read uploaded PDF documents.
2. Convert every page into a high-resolution image.
3. Save images for OCR processing.
4. Provide utility functions for page count and metadata.

Supported Documents
-------------------
- Medical Records
- Insurance Forms
- Prior Authorization
- Intake Forms
- Lab Reports
- Prescriptions
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Dict

import fitz  # PyMuPDF
from PIL import Image


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParser:
    """
    Converts PDF pages into images for OCR.
    """

    def __init__(
        self,
        dpi: int = 300,
        image_format: str = "png",
    ):
        self.dpi = dpi
        self.image_format = image_format.lower()

    #########################################################

    def page_count(self, pdf_path: str) -> int:
        """
        Return total number of pages.
        """

        pdf = fitz.open(pdf_path)

        count = len(pdf)

        pdf.close()

        return count

    #########################################################

    def metadata(self, pdf_path: str) -> Dict:
        """
        Return metadata.
        """

        pdf = fitz.open(pdf_path)

        data = pdf.metadata

        pdf.close()

        return data

    #########################################################

    def convert_to_images(
        self,
        pdf_path: str,
        output_folder: str,
    ) -> List[str]:
        """
        Convert every PDF page to PNG images.
        """

        pdf_path = Path(pdf_path)

        output_folder = Path(output_folder)

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf = fitz.open(pdf_path)

        image_paths = []

        zoom = self.dpi / 72

        matrix = fitz.Matrix(
            zoom,
            zoom
        )

        logger.info(
            f"Converting {len(pdf)} pages..."
        )

        for page_number in range(len(pdf)):

            page = pdf.load_page(page_number)

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_path = (
                output_folder
                / f"page_{page_number+1}.{self.image_format}"
            )

            pix.save(str(image_path))

            image_paths.append(str(image_path))

            logger.info(
                f"Saved {image_path}"
            )

        pdf.close()

        return image_paths

    #########################################################

    def convert_first_page(
        self,
        pdf_path: str,
        output_path: str,
    ) -> str:
        """
        Convert only the first page.
        """

        pdf = fitz.open(pdf_path)

        page = pdf.load_page(0)

        zoom = self.dpi / 72

        matrix = fitz.Matrix(
            zoom,
            zoom
        )

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        pix.save(output_path)

        pdf.close()

        logger.info(
            f"Saved first page -> {output_path}"
        )

        return output_path

    #########################################################

    def validate_pdf(
        self,
        pdf_path: str,
    ) -> bool:
        """
        Check if PDF is valid.
        """

        try:

            pdf = fitz.open(pdf_path)

            pdf.close()

            return True

        except Exception:

            return False

    #########################################################

    def pdf_size_mb(
        self,
        pdf_path: str,
    ) -> float:
        """
        Return PDF size in MB.
        """

        size = Path(pdf_path).stat().st_size

        return round(size / (1024 * 1024), 2)


#############################################################

if __name__ == "__main__":

    parser = PDFParser(dpi=300)

    pdf_file = "uploads/sample_medical_record.pdf"

    print("=" * 60)

    print("Valid PDF :", parser.validate_pdf(pdf_file))

    print("Pages :", parser.page_count(pdf_file))

    print("Size :", parser.pdf_size_mb(pdf_file), "MB")

    print("Metadata :")

    print(parser.metadata(pdf_file))

    print("=" * 60)

    images = parser.convert_to_images(
        pdf_file,
        "output/pages"
    )

    print(images)