import flet as ft

class LoadingSpinner(ft.Container):
    def __init__(self, message="Loading..."):
        super().__init__()
        self.content = ft.Column([
            ft.ProgressRing(),
            ft.Text(message)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        self.alignment = ft.alignment.center
        self.visible = False
