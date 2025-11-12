from customtkinter import set_appearance_mode , set_default_color_theme

class StyleConfig:
    """Centralized theme , and color , and font management for the entire app"""
    THEME = "dark-blue"
    
    COLORS = {
        "bg":"#1e1e1e",
        "fg": "#ffffff",
        "accent": "#4ecca3",
        "button": "#333333",
        "button_hover": "#4ecca3",
    }
    
    FONTS = {
        "title":("Roboto",24,"bold"),
        "subtitle":("Roboto",16),
        "button":("Roboto",14,"bold"),
        "text":("consolas",12),
    }
    
    @staticmethod
    def apply_theme():
        """Apply them globaly to Window"""
        set_appearance_mode("dark")
        set_default_color_theme(StyleConfig.THEME)