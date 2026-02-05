from . import groq_API
from .groq_API import Key
from . import context
from .database import Database

class Session:
    def __init__(self, api_key=None):
        self.api_key = Key(api_key)
        self.messages = Messages()
        self._is_active = False
    
    def close(self):
        self.messages.clear()
        self._is_active = False
    
    def open(self, on_response=None):
        self._is_active = True
        self.on_response = on_response
        return self
    
    def send_message(self, question, file_content="", db=None):
        if not self._is_active:
            return
        
        if not self.api_key:
            raise ValueError("API key not set")
        
        context_text = ""
        if db:
            context_text = context.retrieve(question, db)
        
        prompt = Prompt.create(question, context_text, file_content)
        self.messages.add("user", prompt.format)
        
        try:
            completion = groq_API.response(self.messages.get_last_three(), self.api_key)
            
            if completion is None:
                error_msg = "Failed to get response from API. Please check your API key and connection."
                self.messages.add("assistant", error_msg)
                if self.on_response:
                    self.on_response("assistant", error_msg)
                return None
            
            if not hasattr(completion, '__iter__'):
                error_msg = f"Invalid response from API. Expected iterable, got {type(completion)}"
                self.messages.add("assistant", error_msg)
                if self.on_response:
                    self.on_response("assistant", error_msg)
                return None
            
            full_reply = ""
            try:
                for chunk in completion:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        content = chunk.choices[0].delta.content or ""
                        full_reply += content
                        if self.on_response:
                            self.on_response("assistant_chunk", content)
            except StopIteration:
                pass
            except Exception as e:
                print(f"Error processing stream: {e}")
            
            self.messages.add("assistant", full_reply)
            if self.on_response:
                self.on_response("assistant_complete", full_reply)
            
            return full_reply
            
        except Exception as e:
            error_msg = f"Error connecting to API: {str(e)}"
            print(f"Session error: {error_msg}")
            self.messages.add("assistant", error_msg)
            if self.on_response:
                self.on_response("assistant", error_msg)
            return None
    
class Messages:
    def __init__(self):
        self._messages = []
    
    def add(self, role, content):
        self._messages.append({"role": role, "content": content})
    
    def get_last_three(self):
        return self._messages[-3:] if len(self._messages) >= 3 else self._messages
    
    def get_all(self):
        return self._messages.copy() if self._messages else []
    
    def clear(self):
        self._messages.clear()

class Prompt:
    def __init__(self, question, context_text, file_content: str = ""):
        self.question = question
        self.context = context_text
        self.file = file_content
        if self.context and self.file:
            self.format = f"""### Context: \n{self.context + self.file}\n### Question: {self.question}\n### Answer:"""
        elif self.context and not self.file:
            self.format = f"""### Context: \n{self.context}\n### Question: {self.question}\n### Answer:"""
        elif not self.context and self.file:
            self.format = f"""### Context: \n{self.file}\n### Question: {self.question}\n### Answer:"""
        else:
            self.format = f"""### Question: {self.question}\n### Answer:"""
    
    @classmethod
    def create(cls, question, context_text="", file_content=""):
        return cls(question, context_text, file_content)
