class AppError(Exception):
    """
    Base exception for all application-level errors.
    Extends Python's built-in Exception.

    Attributes:
        message (str): Human-readable error message.
        details  (dict): Optional metadata for debugging.
    """
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self):
        if not self.details:
            return self.message
        return f"{self.message} | Details: {self.details}"


class InvalidFolderError(AppError):
    """Raised when selected folder does not exist or is inaccessible."""
    pass


class NoImageFilesFoundError(AppError):
    """Raised when no images are found in a selected directory."""
    pass


class FileLoadError(AppError):
    """Raised when file reading/loading fails (corrupt or unsupported)."""
    pass


class OCREngineNotFoundError(AppError):
    """Raised when Tesseract engine is not detected or path is invalid."""
    pass


class OCRExtractionError(AppError):
    """Raised when OCR fails to extract text from image."""
    pass


class OCRLanguageNotSupportedError(AppError):
    """Raised when Tesseract does not support requested language."""
    pass

class ConfigError(AppError):
    """Raised when configuration settings are missing or invalid."""
    pass
