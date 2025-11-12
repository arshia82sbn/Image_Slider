class Config:
    ENGINE_CONFIG = "--psm 6 --oem 3",
    APP_TITLE = "Photo Slider with OCR"
    WINDOW_SIZE = "800x600"
    TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSDATA_DIR = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
    
config = Config()