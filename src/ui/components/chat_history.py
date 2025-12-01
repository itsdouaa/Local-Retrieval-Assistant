import flet as ft

class ChatHistory(ft.ListView):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 10
        self.auto_scroll = True
    
    def add_message(self, message: dict):
        self.controls.append(MessageBubble(message))
        self.update()
