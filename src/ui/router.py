import flet as ft
from pages import ChatPage, LoginPage, LogoutPage, RegisterPage, ProfilePage, HistoryPage

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.core = None
        
        self.current_user = None
        self.current_chat_id = None
        
        self.chat_page = None
        self.login_page = None
        self.register_page = None
        self.logout_page = None
        self.profile_page = None
        self.history_page = None
        
        self.navigate_to_chat()
    
    def set_core(self, core):
        self.core = core
    
    def _show_page(self, page):
        self.page.controls.clear()
        self.page.add(page)
        self.page.update()
    
    def navigate_to_chat(self):
        if not self.chat_page:
            self.chat_page = ChatPage()
            self.chat_page.set_callbacks({
                "on_send_message": self._handle_send_message,
                "on_attach_file": self._handle_attach_file,
                "on_menu_click": lambda: self._toggle_sidebar(),
                "on_logout_click": self.navigate_to_logout,
                "on_load_chat": self._handle_load_chat,
                "on_new_chat": self._handle_new_chat
            })
        
        if self.current_user:
            self.chat_page.set_user(self.current_user)
        
        self._show_page(self.chat_page)
    
    def _toggle_sidebar(self):
        if self.chat_page:
            if self.chat_page.sidebar.visible:
                self.chat_page.sidebar.close()
            else:
                self.chat_page.sidebar.open()
    
    def navigate_to_login(self):
        if not self.login_page:
            self.login_page = LoginPage()
            self.login_page.set_callbacks({
                "on_login": self._handle_login,
                "on_register_click": self.navigate_to_register
            })
        
        self._show_page(self.login_page)
    
    def navigate_to_register(self):
        if not self.register_page:
            self.register_page = RegisterPage()
            self.register_page.set_callbacks({
                "on_register": self._handle_register,
                "on_login_click": self.navigate_to_login
            })
        
        self._show_page(self.register_page)
    
    def navigate_to_logout(self):
        if not self.logout_page:
            self.logout_page = LogoutPage()
            self.logout_page.set_callbacks({
                "on_logout": self._handle_logout,
                "on_cancel": self.navigate_to_chat
            })
        
        if self.current_user:
            self.logout_page.set_user_info(self.current_user)
        
        self._show_page(self.logout_page)
    
    def navigate_to_profile(self):
        if not self.profile_page:
            self.profile_page = ProfilePage()
            self.profile_page.set_callbacks({
                "on_save_profile": self._handle_save_profile,
                "on_back_click": self.navigate_to_chat
            })
        
        if self.current_user:
            self.profile_page.set_user_info(self.current_user)
        
        self._show_page(self.profile_page)
    
    def navigate_to_history(self):
        if not self.history_page:
            self.history_page = HistoryPage()
            self.history_page.set_callbacks({
                "on_back_click": self.navigate_to_chat,
                "on_load_chat": self._handle_load_chat
            })
        
        if self.current_user:
            self.history_page.set_user_info(self.current_user)
        
        self._show_page(self.history_page)
    
    def _handle_login(self, email, password):
        if self.core:
            self.core.handle_login(email, password)
    
    def _handle_register(self, name, email, password, confirm, terms):
        if self.core:
            self.core.handle_register(name, email, password, confirm, terms)
    
    def _handle_logout(self):
        if self.core:
            self.core.handle_logout()
    
    def _handle_send_message(self, text, context, chat_id):
        if self.core:
            self.core.handle_send_message(text, context, chat_id)
    
    def _handle_attach_file(self, e):
        if self.core:
            self.core.handle_attach_file(e)
    
    def _handle_load_chat(self, chat_id):
        if self.core:
            self.core.handle_load_chat(chat_id)
    
    def _handle_new_chat(self):
        if self.core:
            self.core.handle_new_chat()
    
    def _handle_save_profile(self, display_name, bio):
        if self.core:
            self.core.handle_save_profile(display_name, bio)
