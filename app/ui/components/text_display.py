from customtkinter import CTkTextbox
from app.ui.style import StyleConfig
from app.utils.log_manager import get_logger

logger = get_logger("Text Display")

class TextDisplayFactory:
    """Factory for creating text display widgets with consistent styling"""
    
    @staticmethod
    def create_textbox(master,width=500,height=100):
        "Creates and returns a pre styled textbox"
        try:
            return CTkTextbox(
                master,
                width=width,
                height=height,
                font=StyleConfig.FONTS["text"],
                fg_color=StyleConfig.COLORS["fg"],
                text_color=StyleConfig.COLORS["bg"],
                corner_radius=20,
                border_width=1,
                border_color=StyleConfig.COLORS["accent"],
            )
        except Exception as e:
            logger.error("Text box not be able to load: ",e)
            
    @staticmethod
    def clear_textbox(text_widget):
        """Utility to clear text content"""
        try:
            text_widget.delete("1.0","end")
        except Exception as e:
            logger.error("Text not deleted: ",e)
    
    @staticmethod
    def set_text(text_widget,content:str):
        """Utility to set text safely"""
        try:
            TextDisplayFactory.clear_textbox(text_widget)
            text_widget.insert("0.1",content)
        except Exception as e:
            logger.error("Text not inserted: ",e , "\n",content)