from pathlib import Path
import threading
from PIL import Image
from typing import Optional , Callable
from app.core import ImageLoader , FileHelper
from app.utils.log_manager import get_logger
from app.core.ocr_engine import OCREngine , OCREngineFactory , OCRExtractionError
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
        it = self.image_loader.iterator()
        if not it:
            logger.error("images are empty")
            return None
        prev = it.prev()
        if self.on_images_changed and prev:
            self.on_images_changed(prev)
        return prev
    
    def current_image(self)-> Optional[Path]:
        it = self.image_loader.iterator()
        return it.current() if it else None
    
    # OCR async code 
    def extract_text_async(self,path:Path ,callback:Optional[Callable[[str],None]]=None):
        """
        Run OCR in backgroound and trigger on_ocr_complete
        """
        def worker(p:Path):
            try:
                logger.info("Starting OCR for %s",p)
                image = Image.open(p)
                text = self.ocr_engine.extract(image=image)
                logger.info("OCR finished for %s", p)
                if callback:
                    callback(text)
                if self.on_ocr_complete:
                    self.on_ocr_complete(text)
            except OCRExtractionError as e:
                logger.warning(f"OCR extraction error:{e.details}")
                if self.on_error:
                    self.on_error(e)
            except Exception as e:
                logger.error("OCR failed : ",e)
                if self.on_error:
                    self.on_error(e)
        
        # ensure only onew OCR thread at a time
        if self._ocr_thread and self._ocr_thread.is_alive():
            logger.warning("OCR already in progress")
            return False
        
        self._ocr_thread = threading.Thread(target=worker,args=(path,),daemon=True)
        self._ocr_thread.start()
        return True