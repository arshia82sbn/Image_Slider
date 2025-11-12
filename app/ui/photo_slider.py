import customtkinter as ctk
from PIL import Image, UnidentifiedImageError , ImageTk
import threading
from typing import List,Optional,Callable
from tkinter import filedialog
from app.core.ocr_engine import OCREngine
from app.core.image_loader import ImageLoader
from app.utils.log_manager import get_logger
from app.ui.components.text_display import TextDisplayFactory
from app.ui.style import styleConfig

logger = get_logger("Photo slider")

class ImageCache:
    "Algorithm for caching the data"
    _instance = None
    _lock = threading.Lock()
    _cache : dict[str , Image.Image] = {}
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ImageCache , cls).__new__(cls)
        return cls._instance
    def get(self,path: str) -> Optional[Image.Image]:
        return self._cache.get(path)
    
    def set(self,path:str,image:Image.Image) -> None:
        self._cache[path] = image

class TransitionStrategy:
    """Base class for defining transition effects."""
    def apply(self, label: ctk.CTkLabel, new_image: ctk.CTkImage) -> None:
        raise NotImplementedError


class FadeTransition(TransitionStrategy):
    """Fade in/out effect for image transitions."""
    def apply(self, label: ctk.CTkLabel, new_image: ctk.CTkImage) -> None:
        try:
            label.configure(image=new_image)
            # Simple fade simulation — could be extended with actual alpha animation
            label.update()
        except Exception as e:
            logger.error(f"Fade transition failed: {e}")


class InstantTransition(TransitionStrategy):
    """Instant image swap without effects."""
    def apply(self, label: ctk.CTkLabel, new_image: ctk.CTkImage) -> None:
        label.configure(image=new_image)


class Command:
    """Command interface for navigation actions."""
    def execute(self) -> None:
        raise NotImplementedError


class NextImageCommand(Command):
    def __init__(self, slider: "PhotoSlider"):
        self.slider = slider

    def execute(self) -> None:
        self.slider.next_image()


class PrevImageCommand(Command):
    def __init__(self, slider: "PhotoSlider"):
        self.slider = slider

    def execute(self) -> None:
        self.slider.prev_image()

class SliderObserver:
    """Observer for listening to slider updates."""
    def update(self, current_index: int, total: int) -> None:
        raise NotImplementedError

class PhotoSlider:
    """
    A robust, extensible image slider with transition effects and error handling.
    """
    def __init__(
        self,
        parent: ctk.CTkFrame,
        image_paths: List[str],
        transition: Optional[TransitionStrategy] = None,
        observer: Optional[SliderObserver] = None,
        refresh_interval: int = 4000
    ):
        self.parent = parent
        self.image_paths = image_paths
        self.transition = transition or InstantTransition()
        self.observer = observer
        self.refresh_interval = refresh_interval

        self.label = ctk.CTkLabel(parent, text="")
        self.label.pack(padx=10, pady=10)

        self.cache = ImageCache()
        self.index = 0
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # Commands
        self.next_command = NextImageCommand(self)
        self.prev_command = PrevImageCommand(self)

        self._notify_observer()

        logger.info("PhotoSlider initialized with %d images.", len(image_paths))
    def start(self) -> None:
        """Start automatic image cycling in a background thread."""
        if not self.image_paths:
            logger.warning("No images provided for the slider.")
            return

        self.running = True
        self.thread = threading.Thread(target=self._cycle_images, daemon=True)
        self.thread.start()
        logger.info("PhotoSlider started cycling images.")

    def stop(self) -> None:
        """Stop the automatic slideshow."""
        self.running = False
        logger.info("PhotoSlider stopped.")

    def next_image(self) -> None:
        """Display the next image manually."""
        self.index = (self.index + 1) % len(self.image_paths)
        self._update_image()

    def prev_image(self) -> None:
        """Display the previous image manually."""
        self.index = (self.index - 1) % len(self.image_paths)
        self._update_image()

    def _cycle_images(self) -> None:
        while self.running:
            try:
                self._update_image()
                threading.Event().wait(self.refresh_interval / 1000)
            except Exception as e:
                logger.error(f"Image cycling failed: {e}")

    def _update_image(self) -> None:
        """Load, cache, and display the current image with transitions."""
        try:
            path = self.image_paths[self.index]
            image = self._load_image(path)
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 300))
            self.transition.apply(self.label, ctk_image)
            self._notify_observer()
        except (FileNotFoundError, UnidentifiedImageError) as e:
            logger.error(f"Image load failed ({path}): {e}")
        except Exception as e:
            logger.exception(f"Unexpected error updating image: {e}")

    def _load_image(self, path: str) -> Image.Image:
        """Load an image from cache or disk."""
        cached = self.cache.get(path)
        if cached:
            return cached

        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        image = Image.open(path)
        self.cache.set(path, image)
        return image

    def _notify_observer(self) -> None:
        if self.observer:
            try:
                self.observer.update(self.index + 1, len(self.image_paths))
            except Exception as e:
                logger.error(f"Observer update failed: {e}")

