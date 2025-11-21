import os
from tkinter import Tk, filedialog
import text_extractor

root = Tk()
root.withdraw()

def recognize_type(file_path):
    return os.path.splitext(file_path)[1].lower()

def extract_text(file_path):
    extension = recognize_type(file_path)
    if extension == ".txt":
        try:
            title = os.path.splitext(os.path.basename(file_path))[0] + "\n"
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            text = title + content
            if text and text.strip():
                print(f"File loaded successfully ({len(text)} characters).")
                return text
            else:
                print("No text extracted!")
                return ""
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
    else:
        handlers = {
            ".pdf": text_extractor.from_pdf,
            ".docx": text_extractor.from_docx,
            **{ext: text_extractor.from_image for ext in [".jpg", ".jpeg", ".png"]}
        }
        handler = handlers.get(extension)
        try:
            text = handler(file_path)
            if text and text.strip():
                print(f"File loaded successfully ({len(text)} characters).")
                return text
            else:
                print("No text extracted!")
                return ""
        except Exception as e:
            print(f"Error opening file: {e}")
            return ""
    

def load():
    try:
        file_path = filedialog.askopenfilename(
            title = "files",
            filetypes=[("files", "*.txt *.docx *.pdf *.jpeg *.jpg *.png")]
        )
        text = extract_text(file_path)
        return text if text else ""
    except Exception as e:
        print(e)
        return ""

