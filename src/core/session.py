from . import groq_API
from . import context
from .database import Database

class Session:
    def __init__(self):
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
        
        context_text = ""
        if db:
            context_text = context.retrieve(question, db)
        
        prompt = Prompt.create(question, context_text, file_content)
        self.messages.add("user", prompt.format)
        
        key = groq_API.Key().get_value()
        if not key:
            if self.on_response:
                self.on_response("assistant", "Error: No API key configured")
            return
        
        if self.on_response:
            self.on_response("user", question)
        
        try:
            completion = groq_API.response(self.messages.get_last_three(), key)
            full_reply = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_reply += content
                if self.on_response:
                    self.on_response("assistant_chunk", content)
            
            self.messages.add("assistant", full_reply)
            if self.on_response:
                self.on_response("assistant_complete", full_reply)
            
            return full_reply
        except Exception:
            if self.on_response:
                self.on_response("assistant", "Error connecting to API")
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
