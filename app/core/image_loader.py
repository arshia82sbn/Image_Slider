from pathlib import Path
from typing import List, Iterator, Optional
from PIL import Image
from functools import lru_cache
from app.core.file_operations import FileHelper
from app.utils.exceptions import FileLoadError
from app.utils.log_manager import get_logger

logger = get_logger()

class ImageIterator:
    """
    Iterator over a list of image paths, Encapsulation navigation lagic
    Use next() , prev() , current() , has_next() , has_prev()
    """
    def __init__(self,paths:List[Path]):
        self._path = list(paths)
        self._index = 0 if self._path else -1
        
    def __len__(self)->int:
        return len(self._path)
    
    def current(self)-> Optional[Path]:
        if 0 <= self._index < len(self._path):
            return self._path[self._index]
        return None
    
    def next(self) -> Optional[Path]:
        if self.has_next():
            self._index += 1
        return self.current()
    
    def prev(self) -> Optional[Path]:
        if self.has_prev():
            self._index -= 1
        return self.current()
    
    def has_next(self) -> bool:
        return self._index < len(self._path) -1
    
    def has_prev(self) -> bool:
        return self._index > 0
    
    def goto(self,idx: int) -> Optional[Path]:
        if 0 <= idx < len(self._path):
            self._index = idx
            return self.current()
        return IndexError("Index out of bounds")
    
    def all(self) -> List[Path]:
        return list(self._path)
    
class ImageLoader:
    """
    Facade for loading, recizing, caching images. uses FileHelper for FS operations
    """
    def __init__(self,max_cache: int = 64):
        self._file_helper = FileHelper()
        self._iterator: Optional[ImageIterator] = None
        self._max_cache = max_cache
        
    def load_from_folder(self, folder: Path, recursive: bool = False) -> ImageIterator:
        folder = self._file_helper.resolve_path(folder)
        files = self._file_helper.list_files(folder,recursive=recursive)
        image_files = [p for p in files if self._file_helper.is_image_file(p)]
        logger.info("loading %d images from %s",len(image_files),folder)
        self._iterator = ImageIterator(image_files)
        return self._iterator
    
    @staticmethod
    @lru_cache
    def load_pil_image(path:str)-> Image.Image:
        """
        Load image via PIL and cache it (path must be string for lru_cache hashing)
        """
        logger.debug("Loading image to memory: %s",path)
        img = Image.open(path)
        # Convert to RGB to avoid mode issues when displaying
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img
    
    def get_resized(self,path:Path,size=(500,400)) -> Image.Image:
        img = ImageLoader.load_pil_image(str(path))
        return img.resize(size,Image.LANCZOS)
    
    def iterator(self) -> Optional[ImageIterator]:
        return self._iterator