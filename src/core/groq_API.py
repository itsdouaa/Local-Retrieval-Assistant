from groq import Groq
import flet as ft
import os

class NonLoadedKeyError(Exception):
    pass

class Key:
    def __init__(self, key_value=None):
        self.value = key_value
    
    def get_value(self):
        return self.value
    
    @staticmethod
    def from_text_field(text_field: ft.TextField):
        if text_field and text_field.value:
            return Key(text_field.value.strip())
        return None
    
    @staticmethod
    def from_file_picker(page: ft.Page, on_key_loaded):
        from ui.components.file_open_dialog import FileOpenDialog
        
        def handle_file_selected(file_path):
            if file_path and file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r') as f:
                        key_content = f.read().strip()
                        key = Key(key_content)
                        on_key_loaded(key)
                except:
                    on_key_loaded(None)
            else:
                on_key_loaded(None)
        
        FileOpenDialog.askopenfilename(
            page=page,
            on_file_selected=handle_file_selected,
            dialog_title="Select API Key File",
            file_types=[("Text files", "*.txt")]
        )

class Completion:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.parameters = {
            "model": "llama-3.3-70b-versatile",
            "temperature": 1,
            "max_completion_tokens": 4096,
            "top_p": 1,
            "stream": True,
            "stop": None,
        }    
    def create(self, messages):
        parameters = {**self.parameters}
        parameters["messages"] = messages
        return self.client.chat.completions.create(**parameters)

def response(messages, key: Key):
    try:
        if not key or not key.get_value():
            return None
        completion = Completion(key.get_value())
        return completion.create(messages)
    except Exception:
        return None
