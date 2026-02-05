import flet as ft
import os
import json
import time
import threading
import logging
import tkinter as tk
from tkinter import filedialog

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Imports de la logique métier (core)
from core import System, Session, Key, Database
from core import from_pdf, from_docx, from_image
from core import history, context

# Imports des composants UI
from ui import ChatPage, LoginPage, RegisterPage, LogoutPage, ProfilePage, ConfigPage

class RAGAssistant:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        
        self.system = System()
        self.current_user = None
        self.current_db = None
        self._session = None
        
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.config_page = ConfigPage()
        self.chat_page = ChatPage()
        self.logout_page = LogoutPage()
        self.profile_page = ProfilePage()
        
        self.config_page.set_page(page)
        
        self.setup_callbacks()
        
        self.show_login_page()
    
    def _setup_page(self):
        self.page.title = "RAG Assistant"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 800
        self.page.window.min_height = 600
        self.page.window.center()
    
    def setup_callbacks(self):
        self.login_page.set_callbacks({
            "on_login": self.handle_login,
            "on_register_click": self.show_register_page
        })
        
        self.register_page.set_callbacks({
            "on_register": self.handle_register,
            "on_login_click": self.show_login_page
        })
        
        self.config_page.set_callbacks({
            "on_submit": self.handle_config_submit,
            "on_back": self.show_login_page,
            "on_create_db": self._create_new_database,
            "on_open_db": self._open_existing_database,
            "on_load_key": self.handle_load_key
        })
        
        self.chat_page.set_callbacks({
            "on_send_message": self.handle_send_message,
            "on_attach_file": self.handle_attach_file,
            "on_menu_click": self.handle_menu_click,
            "on_profile_click": self.show_profile_page,
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
    
    def show_login_page(self, back: bool=False):
        logger.info("Showing login page")
        self.clear_page()
        if not back:
            self.login_page.clear_form()
        self.page.add(self.login_page)
        self.page.update()
    
    def show_register_page(self):
        logger.info("Showing register page")
        self.clear_page()
        self.register_page.clear_form()
        self.page.add(self.register_page)
        self.page.update()
    
    def show_config_page(self):
        logger.info("Showing config page")
        self.clear_page()
        self.config_page.clear_form()
        
        if self.current_user:
            config_data = self.system.load_user_config(self.current_user)
            if config_data:
                if 'db_path' in config_data:
                    self.config_page.set_db_path(config_data['db_path'])
                if 'api_key' in config_data:
                    self.config_page.set_api_key(config_data['api_key'])
        
        self.page.add(self.config_page)
        self.page.update()
    
    def show_chat_page(self):
        logger.info("Showing chat page")
        self.clear_page()
        if self.current_user:
            self.chat_page.set_user(self.current_user)
        self.page.add(self.chat_page)
        self.page.update()
    
    def show_logout_page(self):
        logger.info("Showing logout page")
        self.clear_page()
        if self.current_user:
            self.logout_page.set_user_info(self.current_user)
        self.page.add(self.logout_page)
        self.page.update()
    
    def show_profile_page(self):
        logger.info("Showing profile page")
        self.clear_page()
        if self.current_user:
            self.profile_page.set_user_info(self.current_user)
            self.profile_page.set_form_data(self.current_user, "")
            self.profile_page.clear_metadata()
            self.profile_page.add_metadata("Database", os.path.basename(self.current_db.path) if self.current_db else "None")
        self.page.add(self.profile_page)
        self.page.update()

    def _open_native_dialog(self, mode="open", title="Sélectionner", filetypes=None):
        """Ouvre une boîte de dialogue native selon le mode."""
        if filetypes is None:
            filetypes = [("Tous les fichiers", "*.*")]
        
        if mode == "open":
            return filedialog.askopenfilename(title=title, filetypes=filetypes)
        elif mode == "save":
            return filedialog.asksaveasfilename(title=title, filetypes=filetypes, defaultextension=".db")
        return None
    
    def clear_page(self):
        self.page.controls.clear()
    
    def handle_login(self, username, password):
        logger.info(f"Login attempt for user: {username}")
        self.login_page.show_loading(True, "Logging in...")
        
        success, message, config_path = self.system.login(username, password)
        
        if success:
            logger.info(f"Login successful for user: {username}")
            self.current_user = username
            
            config_data = self.system.load_user_config(username)
            
            if config_data and 'db_path' in config_data and 'api_key' in config_data:
                db_path = config_data['db_path']
                api_key = config_data['api_key']
                
                if os.path.exists(db_path):
                    logger.info(f"Opening existing database: {db_path}")
                    self._open_database_for_login(db_path, api_key)
                else:
                    logger.warning(f"Database not found: {db_path}")
                    self.login_page.show_loading(False)
                    self.show_config_page()
            else:
                logger.info("No configuration found, showing config page")
                self.login_page.show_loading(False)
                self.show_config_page()
                
        else:
            logger.warning(f"Login failed: {message}")
            self.login_page.show_loading(False)
            self.login_page.show_error(message)
    
    def _open_database_for_login(self, db_path, api_key):
        def on_db_opened(db):
            if db:
                logger.info("Database opened successfully")
                self.current_db = db
                
                self._session = Session(api_key=api_key)
                self._session.open(on_response=self.handle_session_response)
                
                self.login_page.show_loading(False)
                self.show_chat_page()
                self.load_chat_history()
            else:
                logger.error("Failed to open database")
                self.login_page.show_loading(False)
                self.login_page.show_error("Failed to open database. Please reconfigure.")
                self.show_config_page()
        
        if self.current_db:
            self.current_db.close_connection()
        
        self.current_db = Database()
        self.current_db.open_existing(path=db_path, page=self.page, on_opened=on_db_opened)
    
    def handle_register(self, username, password, confirm_password):
        logger.info(f"Registration attempt for user: {username}")
        self.register_page.show_loading(True, "Creating account...")
        
        success, message = self.system.register(username, password, confirm_password, self.page)
        if success:
            logger.info(f"Registration successful for user: {username}")
            self.current_user = username
            self.register_page.show_loading(False)
            self.show_config_page()
        else:
            logger.warning(f"Registration failed: {message}")
            self.register_page.show_loading(False)
            self.register_page.show_error(message)
            
    def handle_config_submit(self, db_path, api_key):
        if not db_path or not api_key:
            self.config_page.show_error("Veuillez fournir le chemin de la base et la clé API !")
            return
        
        self.config_page.show_loading(True, "Configuration en cours...")
        self._save_config_and_redirect(db_path, api_key)
        
    def _create_new_database(self, e=None):
        path = self._open_native_dialog(
            mode="save",
            title="Créer une nouvelle base de données RAG",
            filetypes=[("SQLite Database", "*.db")]
        )
        if path:
            self.config_page.set_db_path(path)
            self.page.update()
            logger.info(f"Nouvelle base créée : {path}")
    
    def _open_existing_database(self, e=None):
        path = self._open_native_dialog(
            title="Ouvrir une base de données existante",
            filetypes=[("SQLite Database", "*.db")]
        )
        if path:
            self.config_page.set_db_path(path)
            self.page.update()
            logger.info(f"Base de données sélectionnée : {path}")

    
    def _save_config_and_redirect(self, db_path, api_key):
        logger.info("Saving configuration and redirecting...")
        
        config_data = {
            "db_path": db_path,
            "api_key": api_key
        }
        
        success = self.system.save_user_config(self.current_user, config_data)
        
        if success:
            logger.info("Configuration saved successfully")
            self._session = Session(api_key=api_key)
            self._session.open(on_response=self.handle_session_response)
            
            self.config_page.show_success("Configuration saved! Redirecting to chat...")
            self._redirect_to_chat_after_delay()
        else:
            logger.error("Failed to save configuration")
            self.config_page.show_error("Failed to save configuration")
    
    def handle_load_key(self, e=None):
        path = self._open_native_dialog(
            title="Charger votre clé API Groq",
            filetypes=[("Fichier texte", "*.txt")]
        )
        if path:
            try:
                with open(path, 'r') as f:
                    key_val = f.read().strip()
                    self.config_page.set_api_key(key_val)
                    self.page.update()
            except Exception as err:
                logger.error(f"Erreur lors de la lecture de la clé : {err}")
    
    def _redirect_to_chat_after_delay(self):
        def redirect():
            time.sleep(2)
            self.page.run_task(self._async_redirect_to_chat)
        
        threading.Thread(target=redirect, daemon=True).start()
    
    async def _async_redirect_to_chat(self):
        self.show_chat_page()
    
    def handle_logout(self):
        logger.info(f"Logging out user: {self.current_user}")
        self.logout_page.show_loading(True, "Logging out...")
        
        if self._session:
            self._session.close()
        
        if self.current_db:
            self.current_db.close_connection()
        
        self.chat_page.reset()
        
        self.current_user = None
        self.current_db = None
        self._session = None
        self._pending_api_key = None
        
        self.logout_page.show_loading(False)
        self.show_login_page()
    
    def handle_send_message(self, text, context, chat_id=None):
        if not text.strip() or not self._session:
            return
        
        file_content = ""
        if context and os.path.exists(context):
            file_content = self.extract_file_content(context)
        
        self.chat_page.enable_input(False)
        
        self._session.send_message(text, file_content, self.current_db)
    
    def handle_session_response(self, role, content):
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
        self.page.update()
            
    def handle_attach_file(self, e):
        pass
    
    def handle_menu_click(self):
        self.chat_page._toggle_sidebar()
        
    def handle_load_chat(self, chat_id):
        pass
    
    def handle_new_chat(self):
        self.save_current_conversation()
        
        if self._session:
            self._session.messages.clear()
            
        self.chat_page.clear_messages()
        self.chat_page.message_input.clear_input()
        self.page.update()
        
    def handle_save_profile(self, display_username, bio):
        self.profile_page.show_success("Profile updated successfully!")
    
    def extract_file_content(self, file_path):
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
            logger.error(f"Error extracting file content: {e}")
            return ""
    
    def load_chat_history(self):
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
            logger.error(f"Error loading chat history: {e}")
    
    def save_current_conversation(self):
        if not self.current_db or not self._session:
            return
        
        messages_to_save = self._session.messages.get_all()
        
        if not messages_to_save:
            return
    
        try:
            history.save(self.current_db, messages_to_save)
            logger.info(f"Sauvegarde de {len(messages_to_save)} messages réussie.")
            
            self.chat_page.clear_history()
            self.load_chat_history()
            self.page.update()
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde via session : {e}")

def main(page: ft.Page):
    logger.info("Starting RAG Assistant...")
    app = RAGAssistant(page)

if __name__ == "__main__":
    ft.app(target=main)
