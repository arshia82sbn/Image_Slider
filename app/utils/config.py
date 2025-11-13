import os

class Config:
    ENGINE_CONFIG = "--psm 6 --oem 3",
    APP_TITLE = "Photo Slider with OCR"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WINDOW_SIZE = "800x600"
    TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    TESSDATA_DIR = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
    
config = Config()