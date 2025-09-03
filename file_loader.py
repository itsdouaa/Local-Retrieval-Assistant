import os
from tkinter import Tk, filedialog
import file_to_dict
import db

def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
    title = "files",
    filetypes=[("files", "*.txt *.docx *.pdf *.jpeg *.jpg *.png")]
    )
    return file_path if file_path else None

def recognize_type(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == "":
        return None 
    return ext.lower()
    
def main():
    file_path = choose_file()
    if not file_path:
        return None
    
    ext = recognize_type(file_path)
    handlers = {
        ".pdf": file_to_dict.pdf,
        ".txt": file_to_dict.txt,
        ".docx": file_to_dict.docx,
        ".doc": file_to_dict.doc,
        ".jpg": file_to_dict.image,
        ".jpeg": file_to_dict.image,
        ".png": file_to_dict.image
    }
    handler = handlers.get(ext)
    if handler:
        try:
            data = handler(file_path)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
        try:
            db.save(data)
        except Exception as e:
            print(f"Error connecting to database: {e}")
        return data
        
if __name__ == '__main__':
    main()
