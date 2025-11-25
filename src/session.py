import groq_API
import context
import attempt

attempt = attempt.Attempt()

class Session:
    def __init__(self):
        self.messages = Messages()
        self._is_active = False
    
    def close(self):
        self.messages.clear()
        self._is_active = False
    
    def open(self):
        self._is_active = True
        key = groq_API.Key()
        prompt = Prompt.from_input()
        while not prompt.is_exit_command():
            self.messages.add("user", prompt.format)
            print("\n\n-------------------------response-------------------------\n\n")
            try:
                completion = groq_API.response(self.messages.get_last_three(), key)
                full_reply = ""
                for chunk in completion:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    full_reply += content
                self.messages.add("assistant", full_reply)
            except Exception as e:
                print(f"Error Connecting to API: {e}")
                key = groq_API.Key()
            
            print("\n\n-------------------------prompt-------------------------\n\n")
            prompt = Prompt.from_input()
        
        return None

class Messages:
    def __init__(self):
        self._messages = []
    
    def add(self,role, content):
        self._messages.append({"role": role, "content": content})
    
    def get_last_three(self):
        return self._messages[-3:]
    
    def get_all(self):
        return self._messages.copy() if self._messages else []
    
    def clear(self):
        self._messages.clear()
       
class Prompt:
    def __init__(self, question, context):
        self.question = question
        self.context = context
        if self.context:
            self.format = f"""### Context: \n{context}\n### Question: {question}\n### Answer:"""
        else:
            self.format = f"""### Question: {question}\n### Answer:"""
    
    def is_exit_command(self) -> bool:
        return self.question.lower() == "exit"
        
    @classmethod
    def from_input(cls):
        question = attempt.safe_input("Ask Your Question : ").strip()
        
        _context = context.retrieve(question) if question.lower() != "exit" else ""
        return cls(question, _context)
    
if __name__ == '__main__':
    session = Session().open()
