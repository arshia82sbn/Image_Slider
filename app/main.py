import sys
from app.controller.app_controller import AppController
from app.ui.photo_slider import PhotoSlider
from app.utils.log_manager import get_logger

def main() -> None:
    """
    Entry point for the Photo Slider application.
    Uses an MVC-like structure:
      - Controller: business logic and state management
      - UI (PhotoSlider): visual presentation layer
    """
    logger = get_logger("Main")

    try:
        # Initialize core controller
        controller = AppController()
        logger.info("AppController initialized successfully.")

        # Initialize main UI window
        app = PhotoSlider(controller)
        logger.info("PhotoSlider UI created successfully.")

        # Start mainloop
        app.mainloop()

    except ImportError as e:
        logger.critical(f"Module import failed: {e}")
        sys.exit(1)

    except Exception as e:
        logger.exception(f"Unhandled exception in main application: {e}")
        sys.exit(2)

    finally:
        logger.info("Application terminated gracefully.")



if __name__ == "__main__":
    main()