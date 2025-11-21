from groq import Groq, AuthenticationError
from tkinter import Tk, filedialog
import subprocess

root = Tk()
root.withdraw()

class Key:
    def __init__(self):
        self.value = ""
    
    def read(self):
        print("Accessing to your API key...\n")
        sources = {"1": self.read_from_file, "2": self.read_from_keyboard}
        choice = input("Choose a valid option :\n1. from .txt file   2. from keyboard")
        while choice != "1" and choice != "2":
            choice = input("Choose a valid option :\n1. from .txt file   2. from keyboard")
        source = sources.get(choice)
        source()
    
    def read_from_file(self):
        try:
            key_file_path = filedialog.askopenfilename(title = "files", filetypes=[("files", "*.txt")])
            result = subprocess.run(
                ["cat", key_file_path],
                check=True,
                text=True,
                capture_output=True
            )
            key = result.stdout.strip()
            self.value = key
        except subprocess.CalledProcessError as e:
            raise RuntimeError("API key not readed") from e
    
    def read_from_keyboard(self):
        self.value = input("\nEnter you valid key: ")
        
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

def response(messages):
    key = Key().read()
    while True:
        try:
            completion = Completion(key.get_value())
            return completion.create(messages)
        except AuthenticationError:
            print("\nInvalid key!")
