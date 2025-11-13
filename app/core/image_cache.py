import threading
from PIL import Image
from typing import Optional

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
