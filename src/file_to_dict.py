import os
import Tags
import fitz
import docx
import mammoth
from PIL import Image
import pytesseract

def txt(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0]
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    tags = Tags.get(text)
    return {"title": title, "content": text, "tags": tags}

def docx(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0]
    document = docx.Document(file_path)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    tags = Tags.get(text)
    return {"title": title, "content": text, "tags": tags}

def doc(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0]
    with open(file_path, "rb") as document:
        text = mammoth.convert_to_text(document).value
    tags = Tags.get(text)
    return {"title": title, "content": text, "tags": tags}

def pdf(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0]
    document = fitz.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()
    tags = Tags.get(text)
    return {"title": title, "content": text, "tags": tags}

def image(file_path):
    title = os.path.splitext(os.path.basename(file_path))[0]
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang="eng+fra+ara")
    tags = Tags.get(text)
    return {"title": title, "content": text, "tags": tags}
