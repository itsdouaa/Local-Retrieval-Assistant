import flet as ft

class MessageBubble(ft.Container):
    def __init__(self, message: dict):
        super().__init__()
        self.role = message["role"]
        self.content = message["content"]
        
        self.bgcolor = ft.Colors.BLUE_50 if self.role == "user" else ft.Colors.GREY_100
        self.border_radius = 15
        self.padding = 15
        self.margin = ft.margin.only(bottom=10)
        self.content = ft.Column([
            ft.Text(self.role.title(), weight=ft.FontWeight.BOLD, size=12),
            ft.Text(self.content, selectable=True)
        ], tight=True)
