import flet as ft

class Header(ft.Container):
    def __init__(
        self,
        title="RAG Assistant",
        user_info=None,
        show_menu_button=True,
        on_menu_click=None,
        on_profile_click=None,
        show_back_button=True,
        on_back_click=None,
        show_logout_button=True,
        on_logout_click=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.title = title
        self.user_info = user_info
        self.on_menu_click = on_menu_click
        self.on_profile_click = on_profile_click
        self.on_back_click = on_back_click
        self.on_logout_click = on_logout_click
        
        if 'bgcolor' not in kwargs:
            self.bgcolor = ft.Colors.BLUE_50
        if 'height' not in kwargs:
            self.height = 60
        if 'padding' not in kwargs:
            self.padding = ft.padding.symmetric(horizontal=15, vertical=0)
        
        self._build_content(show_menu_button, show_back_button, show_logout_button)
        
    def _build_content(self, show_menu_button, show_back_button, show_logout_button):
        left_controls = []
        
        if show_menu_button:
            self.menu_button = ft.IconButton(
                icon=ft.Icons.MENU,
                icon_size=24,
                tooltip="Menu",
                on_click=self._handle_menu_click
            )
            left_controls.append(self.menu_button)
        
        if show_back_button:
            self.back_button = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="back",
                on_click=self._handle_back_click
            )
            left_controls.append(self.back_button)
        
        self.title_text = ft.Text(
            self.title,
            size=20,
            weight=ft.FontWeight.BOLD,
            expand=True
        )
        left_controls.append(self.title_text)
        
        left_row = ft.Row(
            left_controls,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        
        self.right_controls = ft.Row(
            [],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.content = ft.Row(
            [
                left_row,
                self.right_controls
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        
        if self.user_info:
            self._update_user_display()
    
    def _update_user_display(self):
        self.right_controls.controls.clear()
        
        if self.user_info:
            user_button = ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.GREY_600),
                    ft.Text(
                        f"{self.user_info}",
                        size=14,
                        color=ft.Colors.GREY_600,
                    )
                ], spacing=5),
                tooltip="Voir le profil",
                on_click=self._handle_profile_click
            )
            self.right_controls.controls.append(user_button)
            
            if self.on_logout_click:
                logout_button = ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_size=20,
                    tooltip="Déconnexion",
                    on_click=self._handle_logout_click
                )
                self.right_controls.controls.append(logout_button)
    
    def _handle_menu_click(self, e):
        if self.on_menu_click:
            self.on_menu_click()

    def _handle_back_click(self, e):
        if self.on_back_click:
            self.on_back_click()
    
    def _handle_logout_click(self, e):
        if self.on_logout_click:
            self.on_logout_click()
    
    def _handle_profile_click(self, e):
        if self.on_profile_click:
            self.on_profile_click()
        else:
            print(f"Redirection vers le profil de {self.user_info}")
    
    def update_user_info(self, user_info):
        self.user_info = user_info
        self._update_user_display()
    
    def update_title(self, new_title):
        self.title = new_title
        self.title_text.value = new_title
