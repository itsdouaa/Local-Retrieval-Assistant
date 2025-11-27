class Attempt:
    def __init__(self, max_attempts=3):
        self.attempts = 0
        self.max_attempts = max_attempts
    
    def reset(self):
        self.attempts = 1
    
    def increment(self):
        self.attempts += 1
    
    def should_retry(self):
        return self.attempts < self.max_attempts
       
    def safe_input(self, prompt: str):
        while True:
            try:
                result = input(prompt+"\n")
                return result
            except (EOFError, KeyboardInterrupt) as e:
                print(e, "\nRetype please!\n")
