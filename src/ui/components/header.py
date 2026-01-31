import flet as ft

class Header(ft.Container):
    def __init__(
        self,
        title="RAG Assistant",
        user_info=None,
        show_menu_button=True,
        on_menu_click=None,
        show_logout_button=True,
        on_logout_click=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.title = title
        self.user_info = user_info
        self.on_menu_click = on_menu_click
        self.on_logout_click = on_logout_click
        
        if 'bgcolor' not in kwargs:
            self.bgcolor = ft.Colors.BLUE_50
        if 'height' not in kwargs:
            self.height = 60
        if 'padding' not in kwargs:
            self.padding = ft.padding.symmetric(horizontal=15, vertical=0)
        
        self._build_content(show_menu_button, show_logout_button)
        
    def _build_content(self, show_menu_button, show_logout_button):
        left_controls = []
        
        if show_menu_button:
            self.menu_button = ft.IconButton(
                icon=ft.Icons.MENU,
                icon_size=24,
                tooltip="Menu",
                on_click=self._handle_menu_click
            )
            left_controls.append(self.menu_button)
        
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
        
        right_controls = []
        
        if self.user_info:
            self.user_text = ft.Text(
                f"👤 {self.user_info}",
                size=14,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.RIGHT
            )
            right_controls.append(self.user_text)
        
        if show_logout_button and self.user_info:
            self.logout_button = ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_size=20,
                tooltip="Se déconnecter",
                on_click=self._handle_logout_click
            )
            right_controls.append(self.logout_button)
        
        right_row = ft.Row(
            right_controls,
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.content = ft.Row(
            [
                left_row,
                right_row
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
    def _handle_menu_click(self, e):
        if self.on_menu_click:
            self.on_menu_click()
    
    def _handle_logout_click(self, e):
        if self.on_logout_click:
            self.on_logout_click()
    
    def update_user_info(self, user_info):
        self.user_info = user_info
        
        right_row = self.content.controls[1]
        
        # Rechercher le bouton logout existant
        logout_btn = None
        for control in right_row.controls:
            if isinstance(control, ft.IconButton) and control.icon == ft.Icons.LOGOUT:
                logout_btn = control
                break
        
        if user_info:
            # Mettre à jour ou ajouter le texte utilisateur
            user_text_found = False
            for control in right_row.controls:
                if hasattr(control, 'text') and "👤" in str(control.text):
                    control.value = f"👤 {user_info}"
                    user_text_found = True
                    break
            
            if not user_text_found:
                self.user_text = ft.Text(
                    f"👤 {user_info}",
                    size=14,
                    color=ft.Colors.GREY_600
                )
                right_row.controls.insert(0, self.user_text)
            
            # Ajouter le bouton logout s'il n'existe pas
            if not logout_btn:
                self.logout_button = ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_size=20,
                    tooltip="Se déconnecter",
                    on_click=self._handle_logout_click
                )
                right_row.controls.append(self.logout_button)
        else:
            # Supprimer le texte utilisateur
            right_row.controls = [
                c for c in right_row.controls 
                if not (hasattr(c, 'text') and "👤" in str(c.text))
            ]
            
            # Supprimer le bouton logout s'il existe
            if logout_btn:
                right_row.controls = [
                    c for c in right_row.controls 
                    if c != logout_btn
                ]
                self.logout_button = None
           
    def update_title(self, new_title):
        self.title = new_title
        self.title_text.value = new_title
        self.update()
    
    def show_menu_button(self, show=True):
        left_row = self.content.controls[0]
        
        if show and self.menu_button not in left_row.controls:
            left_row.controls.insert(0, self.menu_button)
        elif not show and self.menu_button in left_row.controls:
            left_row.controls.remove(self.menu_button)
        
        self.update()
    
    def show_logout_button(self, show=True):
        right_row = self.content.controls[1]
        
        if show and self.user_info and self.logout_button and self.logout_button not in right_row.controls:
            right_row.controls.append(self.logout_button)
        elif not show and self.logout_button in right_row.controls:
            right_row.controls.remove(self.logout_button)
        
        self.update()
    
    def set_menu_callback(self, callback):
        self.on_menu_click = callback
    
    def set_logout_callback(self, callback):
        self.on_logout_click = callback
