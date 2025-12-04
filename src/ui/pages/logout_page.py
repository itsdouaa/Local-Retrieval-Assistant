import flet as ft
from components.header import Header
from components.loading import LoadingSpinner

class LogoutPage(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.on_logout = None
        self.on_cancel = None
        
        self.header = Header(
            title="Logout",
            show_menu_button=False,
            show_logout_button=False
        )
        
        self.loading = LoadingSpinner("Logging out...")
        
        self.content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.icons.LOGOUT,
                        size=80,
                        color=ft.colors.BLUE_400
                    ),
                    ft.Text(
                        "Are you sure you want to log out?",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    ft.Text(
                        "You will need to log in again to continue.",
                        size=14,
                        color=ft.colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=40),
                    ft.Row([
                        ft.OutlinedButton(
                            "Cancel",
                            on_click=self._handle_cancel,
                            width=150,
                            height=45
                        ),
                        ft.ElevatedButton(
                            "Log Out",
                            on_click=self._handle_logout,
                            width=150,
                            height=45,
                            bgcolor=ft.colors.RED_400,
                            color=ft.colors.WHITE
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                border_radius=15,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=15),
                width=500
            ),
            self.loading
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        self.bgcolor = ft.colors.BLUE_50
        self.padding = 20
        self.expand = True
    
    def _handle_logout(self, e):
        if self.on_logout:
            self.on_logout()
    
    def _handle_cancel(self, e):
        if self.on_cancel:
            self.on_cancel()
    
    def set_callbacks(self, callbacks):
        self.on_logout = callbacks.get("on_logout")
        self.on_cancel = callbacks.get("on_cancel")
    
    def set_user_info(self, user_info):
        if user_info:
            self.header.update_user_info(user_info)
    
    def show_loading(self, show=True):
        self.loading.visible = show
        self.update()
