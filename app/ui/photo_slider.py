from customtkinter import CTk
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from app.core.ocr_engine import OCREngine
from app.core.image_loader import ImageLoader
from app.utils.log_manager import get_logger
from app.ui.components.text_display import TextDisplayFactory
from app.ui.style import styleConfig

class PhotoSlider(CTk):
    
    def __init__(self):
        pass