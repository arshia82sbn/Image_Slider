import logging
from threading import Lock


class LogManager:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is ever created (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, name="AppLogger"):
        """Initialize logging only once."""
        if LogManager._initialized:
            return

        with LogManager._lock:
            if LogManager._initialized:
                return

            # Create logger using string name
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)

            # Add handler only once
            if not self.logger.handlers:
                self.logger.addHandler(console_handler)

            LogManager._initialized = True

    def get_logger(self):
        return self.logger


# ✅ Global shortcut
def get_logger(name="AppLogger"):
    """
    Returns a global logger instance with custom name support.
    """
    manager = LogManager(name)
    return manager.get_logger()
