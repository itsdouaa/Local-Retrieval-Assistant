import flet as ft
from ..components import Header
from ..components import StyledTextField
from ..components import LoadingSpinner

class ConfigPage(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.on_back = None
        self.on_submit = None
        self.on_create_db = None
        self.on_open_db = None
        self.on_load_key = None
        
        self.db_path = ""
        self.api_key = ""
        
        self.header = Header(
            title="Database & API",
            show_menu_button=False,
            show_logout_button=False
        )
        
        self.db_link_field = ft.TextField(
            label="Database Path",
            hint_text="Enter path or click buttons below",
            icon=ft.Icons.STORAGE,
            on_change=self._handle_db_path_change
        )
        
        self.create_db_btn = ft.TextButton(
            content=ft.Text(
                "➕ Create a new database",
                color=ft.Colors.BLUE_200,
                size=14
            ),
            on_click=self._handle_create_db,
        )
        
        self.open_db_btn = ft.TextButton(
            content=ft.Text(
                "📂 Open existing database",
                color=ft.Colors.BLUE_200,
                size=14
            ),
            on_click=self._handle_open_db,
        )
        
        self.db_actions_row = ft.Row(
            [self.create_db_btn, self.open_db_btn],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.API_key_field = ft.TextField(
            label="API key",
            hint_text="Enter your API key or load from file",
            icon=ft.Icons.LOCK,
            password=True,
            on_change=self._handle_api_key_change
        )
        
        self.load_key_btn = ft.TextButton(
            content=ft.Text(
                "📄 Choose from .txt file",
                color=ft.Colors.BLUE_200,
                size=14
            ),
            on_click=self._handle_load_key,
        )
        
        self.api_actions_row = ft.Row(
            [self.load_key_btn],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.error_text = ft.Text(
            color=ft.Colors.RED,
            size=12,
            visible=False
        )
        
        self.success_text = ft.Text(
            color=ft.Colors.GREEN,
            size=12,
            visible=False
        )
        
        self.loading = LoadingSpinner("Configuration of account...")
        
        self.content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Configure Account",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Set your database and API key",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    self.db_link_field,
                    ft.Container(height=10),
                    self.db_actions_row,
                    ft.Container(height=10),
                    self.API_key_field,
                    ft.Container(height=10),
                    self.api_actions_row,
                    ft.Container(height=5),
                    self.error_text,
                    self.success_text,
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton(
                            "Back",
                            on_click=self._handle_back,
                            expand=True,
                            height=30
                        ),
                        ft.ElevatedButton(
                            "Submit",
                            on_click=self._handle_submit,
                            expand=True,
                            height=30
                        ),
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
        self.page = None  # Ajouté pour référence à la page
    
    def _handle_db_path_change(self, e):
        self.db_path = self.db_link_field.value.strip()
        print(f"DB path changed to: {self.db_path}")
    
    def _handle_api_key_change(self, e):
        self.api_key = self.API_key_field.value.strip()
        print(f"API key changed to: {self.api_key}")
    
    def _handle_create_db(self, e):
        print("Create DB button clicked")
        if self.on_create_db:
            self.on_create_db()
    
    def _handle_open_db(self, e):
        print("Open DB button clicked")
        if self.on_open_db:
            self.on_open_db()
    
    def _handle_load_key(self, e):
        print("Load key button clicked")
        if self.on_load_key:
            self.on_load_key()
    
    def _handle_back(self, e):
        print("Back button clicked")
        if self.on_back:
            self.on_back(True)
    
    def _handle_submit(self, e):
        print(f"Submit button clicked with db_path={self.db_path}, api_key={'*' * len(self.api_key) if self.api_key else 'None'}")
        if self.on_submit and self.db_path and self.api_key:
            self.on_submit(self.db_path, self.api_key)
        else:
            if not self.db_path:
                self.show_error("Please select or create a database first!")
            if not self.api_key:
                self.show_error("Please enter an API key!")
    
    def set_callbacks(self, callbacks):
        """Set all callbacks for this page"""
        self.on_back = callbacks.get("on_back")
        self.on_submit = callbacks.get("on_submit")
        self.on_create_db = callbacks.get("on_create_db")
        self.on_open_db = callbacks.get("on_open_db")
        self.on_load_key = callbacks.get("on_load_key")
    
    def show_error(self, message):
        """Show error message"""
        print(f"ConfigPage error: {message}")
        self.error_text.value = message
        self.error_text.visible = True
        self.success_text.visible = False
        if self.page:
            self.page.update()
    
    def show_success(self, message):
        """Show success message"""
        print(f"ConfigPage success: {message}")
        self.success_text.value = message
        self.success_text.visible = True
        self.error_text.visible = False
        if self.page:
            self.page.update()
    
    def show_loading(self, show=True, message=""):
        """Show or hide loading spinner"""
        self.loading.visible = show
        if message and hasattr(self.loading, 'content'):
            if len(self.loading.content.controls) > 1:
                text_control = self.loading.content.controls[1]
                if hasattr(text_control, 'value'):
                    text_control.value = message
        if self.page:
            self.page.update()
    
    def clear_form(self):
        """Clear all form fields"""
        self.db_link_field.value = ""
        self.API_key_field.value = ""
        self.db_path = ""
        self.api_key = ""
        self.error_text.visible = False
        self.success_text.visible = False
        self.loading.visible = False
        
    def set_db_path(self, path):
        """Set database path in the text field"""
        print(f"Setting DB path to: {path}")
        
        # Si c'est un objet Database, obtenir le chemin
        if hasattr(path, 'get_path'):
            path_str = path.get_path()
        else:
            path_str = str(path)
        
        self.db_path = path_str
        self.db_link_field.value = path_str
        self._handle_db_path_change(None)
        
    def set_api_key(self, key):
        """Set API key in the text field"""
        print(f"Setting API key to: {'*' * len(str(key)) if key else 'None'}")
        
        key_str = str(key) if key else ""
        self.api_key = key_str
        self.API_key_field.value = key_str
        # Déclencher manuellement le changement
        self._handle_api_key_change(None)
    
    def update(self):
        """Force update of the page"""
        if self.page:
            self.page.update()
    
    def set_page(self, page):
        """Set reference to the main page"""
        self.page = page
