import os
import pytesseract
from PIL import Image
from app.utils.config import config
from app.utils.log_manager import get_logger
from app.utils.exceptions import (
    OCREngineNotFoundError,
    OCRExtractionError,
    OCRLanguageNotSupportedError
)

logger = get_logger("OCR Engine")

# Abstract Base Class (Template for OCR Engines)
class OCREngine:
    """Abstract base class defining OCR extraction behavior."""
    def extract(self, image: Image.Image) -> str:
        """Extract text from image. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement 'extract' method.")

# Concrete Implementation using Tesseract OCR
class TesseractOCR(OCREngine):
    """
    Tesseract OCR Engine wrapper.
    Implements exception handling and configuration setup.
    """

    def __init__(self):
        # Ensure Tesseract binary exists
        if not os.path.exists(config.TESSERACT_CMD):
            logger.error("Tesseract executable not found at configured path.")
            raise OCREngineNotFoundError(
                f"Tesseract not found at: {config.TESSERACT_CMD}"
            )

        # Assign path for pytesseract
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
        logger.debug(f"Tesseract command set to: {config.TESSERACT_CMD}")

    def extract(self, image: Image.Image) -> str:
        """
        Extract text from an image using Tesseract OCR.
        Handles all relevant OCR-specific exceptions.
        """
        try:
            text = pytesseract.image_to_string(
                image,
                lang="fas+eng",  # Persian + English
                config=config.TESSDATA_DIR
            )
            if not text.strip():
                logger.warning("No text found in the provided image.")
            logger.info("OCR extraction completed successfully.")
            return text

        except pytesseract.TesseractNotFoundError as e:
            logger.exception("Tesseract engine not found.")
            raise OCREngineNotFoundError(str(e))

        except pytesseract.TesseractError as e:
            # Handle extraction failure
            logger.exception("OCR extraction failed.")
            raise OCRExtractionError(f"OCR extraction error: {e}")

        except pytesseract.TesseractLanguageError as e:
            logger.exception("Unsupported OCR language requested.")
            raise OCRLanguageNotSupportedError(str(e))

        except Exception as e:
            # General fallback
            logger.exception("Unexpected error during OCR extraction.")
            raise OCRExtractionError(f"Unexpected error: {e}")

# Factory Method for Engine Creation
class OCREngineFactory:
    """Factory for creating OCR engine instances."""
    @staticmethod
    def create_engine(engine_type: str = "tesseract") -> OCREngine:
        engine_type = engine_type.lower().strip()

        if engine_type == "tesseract":
            logger.debug("Creating Tesseract OCR engine instance.")
            return TesseractOCR()
        else:
            logger.error(f"Unsupported OCR engine type requested: {engine_type}")
            raise ValueError(f"Unsupported OCR engine type: {engine_type}")
