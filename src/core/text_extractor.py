import os
import fitz
import docx
from PIL import Image
import pytesseract

def from_docx(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0] + "\n"
    document = docx.Document(file_path)
    text = title
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

def from_pdf(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0] + "\n"
    document = fitz.open(file_path)
    text = title
    for page in document:
        text += page.get_text()
    return text

def from_image(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0] + "\n"
    image = Image.open(file_path)
    text = title + pytesseract.image_to_string(image, lang="eng+fra+ara")
    return text
