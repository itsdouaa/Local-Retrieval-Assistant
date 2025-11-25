from groq import Groq
from tkinter import Tk, filedialog
import subprocess
import attempt

attempt = attempt.Attempt()

root = Tk()
root.withdraw()

class NonLoadedKeyError(Exception):
    pass

class Key:
    def __init__(self):
        self.value = self.read()
        print("Accessing to your API key...\n")
    
    def read(self):
        sources = {"1": self.read_from_file, "2": self.read_from_keyboard}
        choice = attempt.safe_input("Choose a valid option :\n1. from .txt file   2. from keyboard").strip()
        while choice != "1" and choice != "2":
            choice = attempt.safe_input("Choose a valid option :\n1. from .txt file   2. from keyboard").strip()
        source = sources.get(choice)
        while True:
            try:
                key = source()
                if key:
                    return key  
                else:
                    raise NonLoadedKeyError("Operation canceled: key not loaded!")
            except Exception as e:
                print(e, "\nRetry loading a key:\n")
    
    def read_from_file(self):
        try:
            key_file_path = filedialog.askopenfilename(title = "files", filetypes=[("files", "*.txt")])
            if key_file_path:
                result = subprocess.run(
                    ["cat", key_file_path],
                    check=True,
                    text=True,
                    capture_output=True
                )
                key = result.stdout.strip()
            else:
                raise NonLoadedKeyError("Operation canceled: key not loaded!")
            return key
        except subprocess.CalledProcessError as e:
            raise RuntimeError("API key not readed") from e
    
    def read_from_keyboard(self):
        key = attempt.safe_input("\nEnter your valid key: ").strip()
        
    def get_value(self):
        return self.value

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
    while True:
        try:
            completion = Completion(key.get_value())
            return completion.create(messages)
        except Exception as e:
            print(e)
            return None
