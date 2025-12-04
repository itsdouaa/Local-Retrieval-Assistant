import flet as ft
from components.header import Header
from components.input_field import StyledTextField

class ProfilePage(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.on_save_profile = None
        self.on_back_click = None
        
        self.header = Header(
            title="Profile",
            show_menu_button=True,
            on_menu_click=lambda: self._handle_back_click()
        )
        
        self.display_username_field = StyledTextField(
            label="Display Username",
            icon=ft.icons.PERSON
        )
        
        self.bio_field = ft.TextField(
            label="About Me",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=10,
            border_color=ft.colors.BLUE,
            prefix_icon=ft.icons.SHORT_TEXT
        )
        
        self.metadata_section = ft.Column(spacing=10)
        
        self.success_text = ft.Text(
            color=ft.colors.GREEN,
            size=12,
            visible=False
        )
        
        self.error_text = ft.Text(
            color=ft.colors.RED,
            size=12,
            visible=False
        )
        
        self.content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Profile Settings",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Personal Information", size=16, bold=True),
                                self.display_username_field,
                                ft.Container(height=10),
                                ft.Text("Bio", size=14, bold=True),
                                self.bio_field,
                                ft.Container(height=5),
                                self.success_text,
                                self.error_text,
                                ft.Container(height=20),
                                ft.ElevatedButton(
                                    "Save Changes",
                                    on_click=self._handle_save,
                                    width=200,
                                    height=45
                                )
                            ]),
                            padding=25
                        )
                    ),
                    ft.Container(height=20),
                    ft.Card(
                        content=ft.Container(
                            content=self.metadata_section,
                            padding=25
                        )
                    )
                ]),
                padding=30,
                border_radius=15,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=15),
                expand=True
            )
        ], expand=True)
        
        self.bgcolor = ft.colors.BLUE_50
        self.padding = 20
        self.expand = True
    
    def _handle_save(self, e):
        display_username = self.display_username_field.value.strip()
        bio = self.bio_field.value.strip()
        
        if self.on_save_profile:
            self.on_save_profile(display_username, bio)
    
    def _handle_back_click(self):
        if self.on_back_click:
            self.on_back_click()
    
    def set_callbacks(self, callbacks):
        self.on_save_profile = callbacks.get("on_save_profile")
        self.on_back_click = callbacks.get("on_back_click")
    
    def set_user_info(self, user_info):
        if user_info:
            self.header.update_user_info(user_info)
    
    def set_form_data(self, display_username, bio):
        self.display_username_field.value = display_username
        self.bio_field.value = bio
        self.update()
    
    def add_metadata(self, label, value):
        item = ft.Container(
            content=ft.Row([
                ft.Text(f"{label}:", weight=ft.FontWeight.BOLD, width=150),
                ft.Text(value, color=ft.colors.GREY_700, expand=True)
            ]),
            padding=ft.padding.symmetric(vertical=5)
        )
        self.metadata_section.controls.append(item)
        self.update()
    
    def clear_metadata(self):
        self.metadata_section.controls.clear()
        self.update()
    
    def show_success(self, message):
        self.success_text.value = message
        self.success_text.visible = True
        self.error_text.visible = False
        self.update()
    
    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self.success_text.visible = False
        self.update()
