from pathlib import Path
import threading
from typing import Optional, Callable
from PIL import Image
from app.core.image_loader import ImageLoader
from app.core.ocr_engine import OCREngineFactory, OCRExtractionError
from app.utils.log_manager import get_logger

logger = get_logger("AppController")


class AppController:
    """
    Simple, practical controller (Mediator).
    Responsibilities:
      - load images from folder (via ImageLoader)
      - navigate next/prev
      - run OCR in background and notify callbacks
    Callbacks that UI can set:
      - on_images_loaded(count: int)
      - on_image_changed(path: Path)
      - on_ocr_complete(text: str)
      - on_error(exc: Exception)
    """

    def __init__(self, ocr_engine_name: str = "tesseract"):
        self.image_loader = ImageLoader()
        self.iterator = None
        self._ocr_thread: Optional[threading.Thread] = None

        # Create OCR engine (factory) — if it fails we keep None but report via on_error
        try:
            self.ocr_engine = OCREngineFactory.create_engine(ocr_engine_name)
            logger.info("OCR engine initialized: %s", ocr_engine_name)
        except Exception as e:
            self.ocr_engine = None
            logger.exception("Failed to initialize OCR engine: %s", e)

        # Callbacks (set by UI)
        self.on_images_loaded: Optional[Callable[[int], None]] = None
        self.on_image_changed: Optional[Callable[[Path], None]] = None
        self.on_ocr_complete: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None

    # -------- Loading & Navigation --------
    def load_folder(self, folder_path: Path) -> int:
        """Load images synchronously from folder_path. Returns number loaded."""
        try:
            self.iterator = self.image_loader.load_from_folder(folder_path)
            count = len(self.iterator) if self.iterator else 0
            logger.info("Loaded %d images from %s", count, folder_path)
            if self.on_images_loaded:
                try:
                    self.on_images_loaded(count)
                except Exception as cb_e:
                    logger.exception("on_images_loaded callback failed: %s", cb_e)

            # notify about current image
            if self.iterator and self.iterator.current() and self.on_image_changed:
                try:
                    self.on_image_changed(self.iterator.current())
                except Exception as cb_e:
                    logger.exception("on_image_changed callback failed: %s", cb_e)
            return count
        except Exception as e:
            logger.exception("Error loading folder: %s", e)
            if self.on_error:
                self.on_error(e)
            raise

    def next_image(self) -> Optional[Path]:
        if not self.iterator:
            return None
        nxt = self.iterator.next()
        if nxt and self.on_image_changed:
            try:
                self.on_image_changed(nxt)
            except Exception as cb_e:
                logger.exception("on_image_changed callback failed: %s", cb_e)
        return nxt

    def prev_image(self) -> Optional[Path]:
        if not self.iterator:
            return None
        prev = self.iterator.prev()
        if prev and self.on_image_changed:
            try:
                self.on_image_changed(prev)
            except Exception as cb_e:
                logger.exception("on_image_changed callback failed: %s", cb_e)
        return prev

    def current_image(self) -> Optional[Path]:
        return self.iterator.current() if self.iterator else None

    # -------- OCR (async) --------
    def extract_text_async(self, path: Path, callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Start OCR in background. Returns True if started.
        Calls `callback(text)` and `self.on_ocr_complete(text)` when finished.
        If ocr_engine is not available, reports on_error and returns False.
        """

        if self.ocr_engine is None:
            err = RuntimeError("OCR engine not initialized")
            logger.error(err)
            if self.on_error:
                self.on_error(err)
            return False

        def worker(p: Path):
            try:
                logger.info("Starting OCR for %s", p)
                # Use engine.extract(Image) — engine expects PIL.Image
                image = Image.open(p)
                text = self.ocr_engine.extract(image)
                logger.info("OCR finished for %s", p)
                if callback:
                    try:
                        callback(text)
                    except Exception as cb_e:
                        logger.exception("OCR callback failed: %s", cb_e)
                if self.on_ocr_complete:
                    try:
                        self.on_ocr_complete(text)
                    except Exception as cb_e:
                        logger.exception("on_ocr_complete callback failed: %s", cb_e)
            except OCRExtractionError as e:
                logger.exception("OCRExtractionError: %s", e)
                if self.on_error:
                    self.on_error(e)
            except Exception as e:
                logger.exception("Unexpected OCR failure: %s", e)
                if self.on_error:
                    self.on_error(e)

        # Prevent concurrent OCR runs
        if self._ocr_thread and self._ocr_thread.is_alive():
            logger.warning("OCR already running")
            return False

        self._ocr_thread = threading.Thread(target=worker, args=(path,), daemon=True)
        self._ocr_thread.start()
        return True
