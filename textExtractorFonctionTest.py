from PIL import image
from pytesseract import pytesseract




tesseractPath = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
imagePath = r"C:\Users\khidma\Desktop\FIREBASE\TestExtractorImage.jpg"
pytesseract.tesseract_cmd = tesseractPath
image = Image.open(imagePath)
extractedText = pytesseract.image_to_string(image)
print(extractedText)
    