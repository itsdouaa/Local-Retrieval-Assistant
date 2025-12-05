import flet as ft

class StyledTextField(ft.TextField):
    def __init__(self, label, icon=None, is_password=False):
        super().__init__(
            label=label,
            password=is_password,
            border_color=ft.Colors.BLUE,
            border_radius=10,
            prefix_icon=icon
        )
