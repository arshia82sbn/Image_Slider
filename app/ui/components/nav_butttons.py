from customtkinter import CTkButton
from app.utils.log_manager import get_logger 
from app.utils.exceptions import ConfigError

logger = get_logger("Button creator")

class ButtonFactory:
    @staticmethod
    def create_nav_button(master, image, command):
        try:
            logger.info("button created")
            return CTkButton(master, image=image, text="", command=command,corner_radius=20)
        except ConfigError as e:
            logger.error("Cann't load the button:",e.details)