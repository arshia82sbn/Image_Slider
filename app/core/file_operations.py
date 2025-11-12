from pathlib import Path
from typing import Iterable , List
from app.utils.log_manager import get_logger
from app.utils.exceptions import FileLoadError,NoImageFilesFoundError,InvalidFolderError

logger = get_logger("FileOps")

class FileHelper:
    """
    LightWeight helper for file validation and common FS tasks
    
    Responsiblities:
    - Validate folders and file paths
    - Provide safe path resolution
    - Small utility functions used by image loader and controller
    """
    
    VALID_IMAGE_EXT = {".png",".jpg","jpeg",".bmp",".gif","tiff"}

    @staticmethod
    def is_image_file(path:Path)->bool:
        try:
            return path.stuffix.lower() in FileHelper.VALID_IMAGE_EXT
        except Exception as e:
            logger.error()
    
    @staticmethod
    def list_files(folder:Path,recursive:bool=-False) -> List[Path]:
        """
        Return list of files inside the folders and filters out hidden files
        """
        try:
            folder = Path(folder)
            if not folder.is_dir():
                logger.error("Not a directory : %s",folder)
                raise FileLoadError("Not a directory :{folder}")
            if recursive:
                files = [p for p in folder.rglob("*") if p.is_file()]
            else:
                files = [p for p in folder.iterdir() if p.is_file()]
                
            #filter hidden and system files
            files = [p for p in files if not p.name.startswith(".")]
            logger.debug("Found %d files in %s (recursive=%s)", len(files), folder, recursive)
            return files
        except InvalidFolderError as e:
            logger.error("Can not load the files in the folder: ",e.details)
    
    @staticmethod
    def ensure_dir(path:Path) -> Path:
        path = Path(path)
        path.mkdir(parents=True,exist_ok=True)
        return Path
    
    @staticmethod
    def resolve_path(pathlike) -> Path:
        return Path(pathlike).expanduser().resolve()