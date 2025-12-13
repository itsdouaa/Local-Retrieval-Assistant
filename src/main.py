import flet as ft
import os
from system.login import System
from system.session import Session
from ui.pages.chat_page import ChatPage
from ui.pages.login_page import LoginPage
from ui.pages.register_page import RegisterPage
from ui.pages.logout_page import LogoutPage
from ui.pages.profile_page import ProfilePage
from database import Database
from text_extractor import from_pdf, from_docx, from_image

class RAGAssistant(ft.Page):
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "RAG Assistant"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 800
        self.page.window.min_height = 600
        self.page.window.center()
        
        self.system = System()
        self.current_user = None
        self.current_db = None
        self.session = None
        
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.chat_page = ChatPage()
        self.logout_page = LogoutPage()
        self.profile_page = ProfilePage()
        
        self._setup_callbacks()
        
        self.show_login_page()
    
    def _setup_callbacks(self):
        """Setup all page callbacks"""
        self.login_page.set_callbacks({
            "on_login": self.handle_login,
            "on_register_click": self.show_register_page
        })
        
        self.register_page.set_callbacks({
            "on_register": self.handle_register,
            "on_login_click": self.show_login_page
        })
        
        self.chat_page.set_callbacks({
            "on_send_message": self.handle_send_message,
            "on_attach_file": self.handle_attach_file,
            "on_menu_click": self.handle_menu_click,
            "on_logout_click": self.show_logout_page,
            "on_load_chat": self.handle_load_chat,
            "on_new_chat": self.handle_new_chat
        })
        
        self.logout_page.set_callbacks({
            "on_logout": self.handle_logout,
            "on_cancel": self.show_chat_page
        })
        
        self.profile_page.set_callbacks({
            "on_save_profile": self.handle_save_profile,
            "on_back_click": self.show_chat_page
        })
    
    def show_login_page(self):
        """Show login page"""
        self.clear_page()
        self.login_page.clear_form()
        self.page.add(self.login_page)
        self.page.update()
    
    def show_register_page(self):
        """Show registration page"""
        self.clear_page()
        self.register_page.clear_form()
        self.page.add(self.register_page)
        self.page.update()
    
    def show_chat_page(self):
        """Show main chat page"""
        self.clear_page()
        if self.current_user:
            self.chat_page.set_user(self.current_user)
        self.page.add(self.chat_page)
        self.page.update()
    
    def show_logout_page(self):
        """Show logout confirmation page"""
        self.clear_page()
        if self.current_user:
            self.logout_page.set_user_info(self.current_user)
        self.page.add(self.logout_page)
        self.page.update()
    
    def show_profile_page(self):
        """Show profile page"""
        self.clear_page()
        if self.current_user:
            self.profile_page.set_user_info(self.current_user)
            self.profile_page.set_form_data(self.current_user, "")
            self.profile_page.clear_metadata()
            self.profile_page.add_metadata("Database", os.path.basename(self.current_db.path) if self.current_db else "None")
        self.page.add(self.profile_page)
        self.page.update()
    
    def clear_page(self):
        """Clear current page content"""
        self.page.controls.clear()
    
    def handle_login(self, username, password):
        """Handle login attempt"""
        self.login_page.show_loading(True, "Logging in...")
        
        success, message, db_path = self.system.login(username, password)
        
        if success:
            self.current_user = username
            
            if db_path and os.path.exists(db_path):
                self.current_db = Database()
                self.current_db.open_existing(db_path, self.page, lambda db: None)
            else:
                db_path = self.system.create_user_database(username, self.page)
                if db_path:
                    self.current_db = Database()
                    self.current_db.open_existing(db_path, self.page, lambda db: None)
            
            self.session = Session()
            self.session.open(on_response=self.handle_session_response)
            
            self.login_page.show_loading(False)
            self.show_chat_page()
            
            self.load_chat_history()
        else:
            self.login_page.show_loading(False)
            self.login_page.show_error(message)
    
    def handle_register(self, username, password, confirm_password, terms_accepted):
        """Handle user registration"""
        if not terms_accepted:
            self.register_page.show_error("You must agree to the Terms and Privacy Policy")
            return
        
        self.register_page.show_loading(True, "Creating account...")
        
        success, message, db_path = self.system.register(
            username, password, confirm_password, None, self.page
        )
        
        if success:
            self.current_user = username
            
            if db_path:
                self.current_db = Database()
                self.current_db.open_existing(db_path, self.page, lambda db: None)
            
            self.session = Session()
            self.session.open(on_response=self.handle_session_response)
            
            self.register_page.show_loading(False)
            self.show_chat_page()
        else:
            self.register_page.show_loading(False)
            self.register_page.show_error(message)
    
    def handle_logout(self):
        """Handle user logout"""
        self.logout_page.show_loading(True, "Logging out...")
        
        if self.session:
            self.session.close()
        
        self.current_user = None
        self.current_db = None
        self.session = None
        
        self.logout_page.show_loading(False)
        self.show_login_page()
    
    def handle_send_message(self, text, context, chat_id=None):
        """Handle sending a message to the AI"""
        if not text.strip() or not self.session:
            return
        
        file_content = ""
        if context and os.path.exists(context):
            file_content = self.extract_file_content(context)
        
        self.chat_page.enable_input(False)
        
        self.session.send_message(text, file_content, self.current_db)
    
    def handle_session_response(self, role, content):
        """Handle responses from the session"""
        if role == "user":
            self.chat_page.add_message("user", content)
        elif role == "assistant_chunk":
            pass
        elif role == "assistant_complete":
            self.chat_page.add_message("assistant", content)
            self.chat_page.enable_input(True)
            
            if self.current_db:
                self.save_current_conversation()
        elif role == "assistant":
            self.chat_page.add_message("assistant", content)
            self.chat_page.enable_input(True)
    
    def handle_attach_file(self, e):
        """Handle file attachment"""
        pass
    
    def handle_menu_click(self):
        """Handle menu button click"""
        self.show_profile_page()
    
    def handle_load_chat(self, chat_id):
        """Load a specific chat from history"""
        pass
    
    def handle_new_chat(self):
        """Start a new chat"""
        self.chat_page.clear_messages()
        self.chat_page.message_input.clear_input()
    
    def handle_save_profile(self, display_username, bio):
        """Handle profile updates"""
        self.profile_page.show_success("Profile updated successfully!")
    
    def extract_file_content(self, file_path):
        """Extract text content from various file types"""
        try:
            if file_path.endswith('.pdf'):
                return from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return from_docx(file_path)
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                return from_image(file_path)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            print(f"Error extracting file content: {e}")
            return ""
    
    def load_chat_history(self):
        """Load user's chat history"""
        if not self.current_db:
            return
        
        try:
            history_table = self.current_db.get_table("history")
            chats = history_table.select(["id", "content", "timestamp"], "role = 'user'")
            
            for chat_id, content, timestamp in chats:
                preview = content[:50] + "..." if len(content) > 50 else content
                self.chat_page.add_history_item(
                    chat_id, 
                    f"Chat {chat_id}", 
                    timestamp, 
                    preview
                )
        except Exception as e:
            print(f"Error loading chat history: {e}")
    
    def save_current_conversation(self):
        """Save current conversation to database"""
        if not self.current_db:
            return
        
        pass

def main(page: ft.Page):
    """Main entry point"""
    app = RAGAssistant(page)

if __name__ == "__main__":
    ft.app(target=main)
