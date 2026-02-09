import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Tesseract version:", pytesseract.get_tesseract_version())

# Test with any image you have
img_path = r"images\train\test\test3.txt.jpg"  # change to your actual image
text = pytesseract.image_to_string(Image.open(img_path))
print("Extracted text sample:")
print(text[:200])  # first 200 characters