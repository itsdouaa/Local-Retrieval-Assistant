# pages/login_page.py
import flet as ft
from components.header import Header
from components.input_field import StyledTextField
from components.loading import LoadingSpinner

class LoginPage(ft.Container):
    def __init__(self, router):
        super().__init__()
        self.router = router
        
        self.header = Header(
            title="Login",
            show_menu_button=False,
            show_logout_button=False
        )
        
        self.username_field = StyledTextField(
            label="Username",
            icon=ft.Icons.ACCOUNT_CIRCLE
        )
        
        self.password_field = StyledTextField(
            label="Password",
            icon=ft.Icons.LOCK,
            is_password=True
        )
        
        self.error_text = ft.Text(
            color=ft.colors.RED,
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
                        color=ft.colors.GREY_600,
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
                            on_click=router.navigate_to_register
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                border_radius=15,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=15),
                width=400
            ),
            self.loading
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        self.bgcolor = ft.colors.BLUE_50
        self.padding = 20
        self.expand = True
    
    def _handle_login(self, e):
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()
        
        if username and password:
            self.router.handle_login(username, password)
    
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
        self.update()
