"""
easyocr_engine.py

OCR Engine for Healthcare AI

Responsibilities:
1. Read scanned medical forms
2. Extract text using EasyOCR
3. Return clean text
4. Support multiple languages
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

import cv2
import easyocr
import numpy as np

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EasyOCREngine:

    def __init__(
        self,
        languages: List[str] = ["en"],
        gpu: bool = False
    ):

        logger.info("Loading EasyOCR model...")

        self.reader = easyocr.Reader(
            languages,
            gpu=gpu
        )

        logger.info("EasyOCR Loaded Successfully")

    ######################################################

    def preprocess_image(
        self,
        image_path: str
    ) -> np.ndarray:

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Image not found : {image_path}"
            )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return gray

    ######################################################

    def extract_text(
        self,
        image_path: str
    ) -> str:

        processed = self.preprocess_image(image_path)

        results = self.reader.readtext(
            processed,
            detail=0,
            paragraph=True
        )

        return "\n".join(results)

    ######################################################

    def extract_with_confidence(
        self,
        image_path: str
    ):

        processed = self.preprocess_image(image_path)

        results = self.reader.readtext(
            processed,
            detail=1
        )

        output = []

        for item in results:

            bbox, text, confidence = item

            output.append(
                {
                    "text": text,
                    "confidence": round(confidence, 3),
                    "bbox": bbox,
                }
            )

        return output

    ######################################################

    def save_text(
        self,
        image_path: str,
        output_file: str
    ):

        text = self.extract_text(image_path)

        with open(
            output_file,
            "w",
            encoding="utf8"
        ) as f:

            f.write(text)

        logger.info(f"Saved OCR text -> {output_file}")

    ######################################################

    def supported_file(
        self,
        file_path: str
    ) -> bool:

        ext = Path(file_path).suffix.lower()

        return ext in [
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".tiff"
        ]


##############################################################

if __name__ == "__main__":

    engine = EasyOCREngine()

    image = "sample_form.png"

    if engine.supported_file(image):

        text = engine.extract_text(image)

        print("=" * 60)
        print(text)
        print("=" * 60)

        detailed = engine.extract_with_confidence(image)

        print(detailed)