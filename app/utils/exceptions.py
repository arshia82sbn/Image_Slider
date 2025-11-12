"""
Centralized custom exception classes for the PhotoSlider_OCR application.

This module defines high-level custom exceptions that encapsulate
OCR, file-system, image-processing, and configuration errors.

All exceptions inherit from the base AppError class, which
supports structured error messages and optional debug metadata.

These exceptions can be consumed by UI and core business layers
to provide consistent error handling, improved logging, and
clear user feedback.
"""


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


# --------------------------------------------------
# File / Directory Handling Exceptions
# --------------------------------------------------

class InvalidFolderError(AppError):
    """Raised when selected folder does not exist or is inaccessible."""
    pass


class NoImageFilesFoundError(AppError):
    """Raised when no images are found in a selected directory."""
    pass


class FileLoadError(AppError):
    """Raised when file reading/loading fails (corrupt or unsupported)."""
    pass


# --------------------------------------------------
# Image Processing Exceptions
# --------------------------------------------------

class ImageProcessingError(AppError):
    """Raised when resizing, loading, or converting an image fails."""
    pass


class UnsupportedImageFormatError(AppError):
    """Raised when an unsupported image format is encountered."""
    pass


# --------------------------------------------------
# OCR Exceptions
# --------------------------------------------------

class OCREngineNotFoundError(AppError):
    """Raised when Tesseract engine is not detected or path is invalid."""
    pass


class OCRExtractionError(AppError):
    """Raised when OCR fails to extract text from image."""
    pass


class OCRLanguageNotSupportedError(AppError):
    """Raised when Tesseract does not support requested language."""
    pass


# --------------------------------------------------
# Configuration / Application-Level Errors
# --------------------------------------------------

class ConfigError(AppError):
    """Raised when configuration settings are missing or invalid."""
    pass


class ResourceNotFoundError(AppError):
    """Raised when icons, assets, or resource paths are missing."""
    pass
