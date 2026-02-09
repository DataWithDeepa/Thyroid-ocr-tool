# src/ocr_engine.py

import pytesseract
from .preprocess import preprocess_for_ocr

# Set Tesseract path - use the one that works on your computer
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# or if it's in (x86):
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def extract_text_from_crop(crop):
    if crop.size == 0:
        return ""
    
    processed = preprocess_for_ocr(crop)
    
    config = r'--oem 3 --psm 6 -l eng'
    
    text = pytesseract.image_to_string(processed, config=config)
    
    return text.strip()