import flet as ft
from pages import ChatPage, LoginPage, LogoutPage, RegisterPage, ProfilePage

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.core = None
        
        self.current_user = None
        self.current_chat_id = None
        
        self.chat_page = ChatPage()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.logout_page = LogoutPage()
        self.profile_page = ProfilePage()
        
        self._setup_callbacks()
        
        self.navigate_to_login()
    
    def _setup_callbacks(self):
        self.chat_page.set_callbacks({
            "on_send_message": self._handle_send_message,
            "on_attach_file": self._handle_attach_file,
            "on_menu_click": self._handle_chat_menu_click,
            "on_logout_click": self.navigate_to_logout,
            "on_load_chat": self._handle_load_chat,
            "on_new_chat": self._handle_new_chat
        })
        
        self.login_page.set_callbacks({
            "on_login": self._handle_login,
            "on_register_click": self.navigate_to_register
        })
        
        self.register_page.set_callbacks({
            "on_register": self._handle_register,
            "on_login_click": self.navigate_to_login
        })
        
        self.logout_page.set_callbacks({
            "on_logout": self._handle_logout,
            "on_cancel": self.navigate_to_chat
        })
        
        self.profile_page.set_callbacks({
            "on_save_profile": self._handle_save_profile,
            "on_back_click": self.navigate_to_chat
        })
    
    def set_core(self, core):
        self.core = core
        if self.current_user:
            self._update_user_info(self.current_user)
    
    def _show_page(self, page):
        self.page.controls.clear()
        self.page.add(page)
        self.page.update()
    
    def _update_user_info(self, user_info):
        """Update user info across all relevant pages"""
        self.chat_page.set_user(user_info)
        self.logout_page.set_user_info(user_info)
        self.profile_page.set_user_info(user_info)
    
    def navigate_to_chat(self):
        if self.current_user:
            self._show_page(self.chat_page)
        else:
            self.navigate_to_login()
    
    def navigate_to_login(self):
        self._show_page(self.login_page)
        self.page.update()
        self.login_page.clear_form()
    
    def navigate_to_register(self):
        self._show_page(self.register_page)
        self.page.update()
        self.login_page.clear_form()
    
    def navigate_to_logout(self):
        if self.current_user:
            self.logout_page.set_user_info(self.current_user)
        self._show_page(self.logout_page)
    
    def navigate_to_profile(self):
        if self.current_user:
            self.profile_page.set_user_info(self.current_user)
            # Load profile data here
        self._show_page(self.profile_page)
    
    def _handle_chat_menu_click(self):
        if self.chat_page:
            self.chat_page._toggle_sidebar()
    
    def _handle_login(self, username, password):
        if self.core:
            self.core.handle_login(username, password)
    
    def _handle_register(self, username, password, confirm, terms):
        if self.core:
            self.core.handle_register(username, password, confirm, terms)
    
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
        self.current_chat_id = chat_id
        if self.core:
            self.core.handle_load_chat(chat_id)
    
    def _handle_new_chat(self):
        self.current_chat_id = None
        self.chat_page.clear_messages()
        self.chat_page.message_input.clear_input()
    
    def _handle_save_profile(self, display_name, bio):
        if self.core:
            self.core.handle_save_profile(display_name, bio)
    
    def update_user(self, user_info):
        self.current_user = user_info
        self._update_user_info(user_info)
    
    def update_chat_history(self, chat_id, title, timestamp, preview):
        if self.chat_page:
            self.chat_page.add_history_item(chat_id, title, timestamp, preview)
    
    def add_message(self, role, content):
        if self.chat_page:
            self.chat_page.add_message(role, content)
    
    def show_error(self, page_name, message):
        """Show error on specific page"""
        pages = {
            "login": self.login_page,
            "register": self.register_page,
            "profile": self.profile_page,
            "chat": self.chat_page
        }
        page = pages.get(page_name)
        if page and hasattr(page, "show_error"):
            page.show_error(message)
    
    def show_loading(self, page_name, show=True, message=""):
        """Show/hide loading on specific page"""
        pages = {
            "login": self.login_page,
            "register": self.register_page,
            "logout": self.logout_page
        }
        page = pages.get(page_name)
        if page and hasattr(page, "show_loading"):
            page.show_loading(show, message)
