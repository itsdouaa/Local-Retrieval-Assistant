import os
from tkinter import Tk, filedialog
import text_extractor

root = Tk()
root.withdraw()

def recognize_type(file_path):
    return os.path.splitext(file_path)[1].lower()

def extract_text(file_path):
    extension = recognize_type(file_path)
    if extension = ".txt":
        title = os.path.splitext(os.path.basename(file_path))[0] + "\n"
        content = open(file_path, "r", encoding="utf-8").read()
        text = title + content
    else
        handlers = {
            ".pdf": text_extractor.from_pdf,
            ".docx": text_extractor.from_docx,
            **{ext: text_extractor.from_image for ext in [".jpg", ".jpeg", ".png"]}
        }
        handler = handlers.get(extension)
        try:
            text = handler(file_path)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
    return text

def load():
    file_path = filedialog.askopenfilename(
        title = "files",
        filetypes=[("files", "*.txt *.docx *.pdf *.jpeg *.jpg *.png")]
    )
    if file_path:
        treat(file_path)

def request():
    add_file = {"yes": load}
    add = add_file.get(input("do you want to add some context/files ?\n").lower())
    while add:
        add()
        add = add_file.get(input("do you want to add some context/files ?\n").lower())

