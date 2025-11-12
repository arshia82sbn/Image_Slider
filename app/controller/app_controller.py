from pathlib import Path
import threading
from typing import Optional , Callable
from app.core import ImageLoader , FileHelper
from app.utils.log_manager import get_logger
from app.core.ocr_engine import OCREngine
from app.utils.exceptions import FileLoadError

logger = get_logger("AppController")

class AppController:
    """
    Mediator / Controller between UI (View) and Core logic
    Responsibilities:
    - coordinate folder selection , image loading
    - Expose async OCR extraction API
    - Provide callbacks to the UI for events
    """
    def __init__(self):
        self.image_loader = ImageLoader()
        self.file_helper = FileHelper()
        self.ocr_engine = OCREngine()
        self._ocr_thread = Optional[threading.Thread] = None
    
        # Callbacks that UI can set
        self.on_images_loaded : Optional[Callable[[int],None]] = None
        self.on_images_changed: Optional[Callable[[Path],None]] = None
        self.on_ocr_complete: Optional[Callable[[str],None]] = None
        self.on_error: Optional[Callable[[Exception],None]] = None
    
    def load_folder(self,folder_path:Path,recursive:bool = False):
        """
        Load images from folder; synchronous 
        Notify UI via on_images_loaded callback
        """
        try:
            iterator = self.image_loader.load_from_folder(folder_path,recursive=recursive)
            count = int(iterator)
            logger.info("Loaded %d images",count)
            if self.on_images_loaded:
                self.on_images_loaded(count)
                #Notify change for current image
                current  = iterator.current()
                if current and self.on_images_changed:
                    self.on_images_changed(current)
                return iterator
        except FileLoadError as e:
            logger.exception("Failed loading folder: %s",folder_path)
            if self.on_error:
                self.on_error(e)
            raise
    
    # Navigate helpers used by UI
    def next_image(self) -> Optional[Path]:
        try:
            it = self.image_loader.iterator()
            if not it:
                return None
            perv = it.perv()
            if self.on_images_changed and perv:
                self.on_images_changed(perv)
            return perv
        except Exception as e:
            logger.error("Next imaeg can't load:",e)
    
    def prev_image(self) ->Optional[Path]:
        pass