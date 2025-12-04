import flet as ft
from components.header import Header
from components.input_field import StyledTextField
from components.loading import LoadingSpinner

class RegisterPage(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.on_register = None
        self.on_login_click = None
        
        self.header = Header(
            title="Sign Up",
            show_menu_button=False,
            show_logout_button=False
        )
        
        self.username_field = StyledTextField(
            label="Username",
            icon=ft.Icons.PERSON
        )
        
        self.password_field = StyledTextField(
            label="Password",
            icon=ft.Icons.LOCK,
            is_password=True
        )
        
        self.confirm_field = StyledTextField(
            label="Confirm Password",
            icon=ft.Icons.LOCK,
            is_password=True
        )
        
        self.terms_checkbox = ft.Checkbox(
            label="I agree to Terms and Privacy Policy",
            value=False
        )
        
        self.error_text = ft.Text(
            color=ft.Colors.RED,
            size=12,
            visible=False
        )
        
        self.loading = LoadingSpinner("Creating account...")
        
        self.content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Create Account",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Join RAG Assistant today",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    self.username_field,
                    ft.Container(height=10),
                    self.password_field,
                    ft.Container(height=10),
                    self.confirm_field,
                    ft.Container(height=10),
                    self.terms_checkbox,
                    ft.Container(height=5),
                    self.error_text,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Create Account",
                        on_click=self._handle_register,
                        expand=True,
                        height=50
                    ),
                    ft.Container(height=15),
                    ft.Row([
                        ft.Text("Already have an account?"),
                        ft.TextButton(
                            "Sign in",
                            on_click=lambda e: self._handle_login_click()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=15),
                width=450
            ),
            self.loading
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        self.bgcolor = ft.Colors.BLUE_50
        self.padding = 20
        self.expand = True
    
    def _handle_register(self, e):
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()
        confirm = self.confirm_field.value.strip()
        terms = self.terms_checkbox.value
        
        if self.on_register:
            self.on_register(name, password, confirm, terms)
    
    def _handle_login_click(self):
        if self.on_login_click:
            self.on_login_click()
    
    def set_callbacks(self, callbacks):
        self.on_register = callbacks.get("on_register")
        self.on_login_click = callbacks.get("on_login_click")
    
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
        self.confirm_field.value = ""
        self.terms_checkbox.value = False
        self.error_text.visible = False
        self.loading.visible = False
