import flet as ft
from components.header import Header
from components.input_field import StyledTextField
from components.loading import LoadingSpinner

class LoginPage(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.on_login = None
        self.on_register_click = None
        
        self.header = Header(
            title="Login",
            show_menu_button=False,
            show_logout_button=False
        )
        
        self.username_field = StyledTextField(
            label="Username",
            icon=ft.Icons.EMAIL
        )
        
        self.password_field = StyledTextField(
            label="Password",
            icon=ft.Icons.LOCK,
            is_password=True
        )
        
        self.error_text = ft.Text(
            color=ft.Colors.RED,
            size=12,
            visible=False
        )
        
        self.loading = LoadingSpinner("Logging in...")
        
        self.content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Welcome Back",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Sign in to your account",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    self.username_field,
                    ft.Container(height=10),
                    self.password_field,
                    ft.Container(height=5),
                    self.error_text,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Sign In",
                        on_click=self._handle_login,
                        expand=True,
                        height=50
                    ),
                    ft.Container(height=15),
                    ft.Row([
                        ft.Text("Don't have an account?"),
                        ft.TextButton(
                            "Sign up",
                            on_click=lambda e: self._handle_register_click()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=15),
                width=400
            ),
            self.loading
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        self.bgcolor = ft.Colors.BLUE_50
        self.padding = 20
        self.expand = True
    
    def _handle_login(self, e):
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()
        
        if username and password and self.on_login:
            self.on_login(username, password)
    
    def _handle_register_click(self):
        if self.on_register_click:
            self.on_register_click()
    
    def set_callbacks(self, callbacks):
        self.on_login = callbacks.get("on_login")
        self.on_register_click = callbacks.get("on_register_click")
    
    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self.update()
    
    def show_loading(self, show=True):
        self.loading.visible = show
        self.update()
    
    def clear_form(self):
        self.username_field.value = ""
        self.password_field.value = ""
        self.error_text.visible = False
        self.loading.visible = False
