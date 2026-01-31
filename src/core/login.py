import logging
import hashlib
import json
import os
from . import database
from .database import Database

class Logger:
    def __init__(self, log_file='log_file.log'):
        self.log_file = log_file
        if os.path.splitext(self.log_file)[1] != ".log":
            self.log_file = os.path.splitext(self.log_file)[0] + ".log"
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('')
        self.setup_logger()
    
    def setup_logger(self):
        self.logger = logging.getLogger('logger')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(self.log_file, encoding='utf-8')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
    
    def warning(self, message):
        if hasattr(self, 'logger'):
            self.logger.warning(message)
    
    def error(self, message):
        if hasattr(self, 'logger'):
            self.logger.error(message)
    
    def info(self, message):
        if hasattr(self, 'logger'):
            self.logger.info(message)
    
    def debug(self, message):
        if hasattr(self, 'logger'):
            self.logger.debug(message)

class User:
    def __init__(self, username: str = "", password: str = "", path: str = ""):
        self.username = username
        self.password = self.hash_password(password)
        self.db = Database(path)
    
    def set_username(self, username: str = ""):
        self.username = username.strip()
        return bool(self.username)
    
    def get_username(self):
        return self.username
    
    def set_password(self, password: str = "", confirm_password: str = ""):
        if not password:
            return False
        
        if confirm_password and password != confirm_password:
            return False
        
        self.password = self.hash_password(password)
        return True
    
    def get_password(self):
        return self.password
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_database_open(self, path: str = "", page=None):
        try:
            self.db.open_existing(path=path, page=page)
            return True
        except Exception:
            return False
    
    def set_database_create(self, page=None):
        try:
            self.db.create(page=page)
            return True
        except Exception:
            return False

class System:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.logger = Logger()
        self.load_users()
    
    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.users = json.loads(content)
                    else:
                        self.users = {}
            else:
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
                self.users = {}
        except Exception as e:
            self.logger.error(f"Error when loading the users: {e}")
            self.users = {}
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
    
    def save_users(self):
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error when saving the users: {e}")
            return False
    
    def register(self, username, password, confirm_password, db_path=None, page=None):
        try:
            if not username or not username.strip():
                return False, "Username is required", None
            
            if not password:
                return False, "Password is required", None
            
            if password != confirm_password:
                return False, "Passwords do not match", None
            
            if username in self.users:
                self.logger.warning(f"Registration attempt with existing username: {username}")
                return False, "Username already exists", None
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if not db_path:
                user_db = Database()
                user_db.create(page=page)
                db_path = user_db.get_path()
            
            self.users[username] = [hashed_password, db_path]
            if self.save_users():
                self.logger.info(f"New user registered: {username}")
                return True, "Registration successful!", db_path
            else:
                if username in self.users:
                    del self.users[username]
                return False, "Failed to save user data", None
                
        except Exception as e:
            self.logger.error(f"Registration error for {username}: {e}")
            return False, f"Registration failed: {str(e)}", None
    
    def login(self, username, password):
        try:
            if username not in self.users:
                self.logger.warning(f"Login attempt with non-existent user: {username}")
                return False, "User not found", None
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            stored_password = self.users[username][0]
            
            if hashed_password != stored_password:
                self.logger.warning(f"Failed login attempt for: {username}")
                return False, "Invalid password", None
            
            db_path = self.users[username][1] if len(self.users[username]) > 1 else None
            
            self.logger.info(f"Login successful with: {username}")
            return True, "Login successful!", db_path
            
        except Exception as e:
            self.logger.error(f"Login error for {username}: {e}")
            return False, f"Login failed: {str(e)}", None
    
    def change_password(self, username, current_password, new_password, confirm_password):
        try:
            login_success, message, _ = self.login(username, current_password)
            if not login_success:
                return False, f"Current password verification failed: {message}"
            
            if not new_password:
                return False, "New password is required"
            
            if new_password != confirm_password:
                return False, "New passwords do not match"
                
            new_hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.users[username][0] = new_hashed_password
            
            if self.save_users():
                self.logger.info(f"Password changed successfully for: {username}")
                return True, "Password changed successfully!"
            else:
                return False, "Failed to save password change"
        except Exception as e:
            self.logger.error(f"Password change error for {username}: {e}")
            return False, f"Password change failed: {str(e)}"
            
    def get_user_database_path(self, username):
        if username in self.users and len(self.users[username]) > 1:
            return self.users[username][1]
        return None
    
    def user_exists(self, username):
        return username in self.users
    
    def create_user_database(self, username, page=None):
        try:
            user_db = Database()
            user_db.create(page=page)
            db_path = user_db.get_path()
            if username in self.users:
                self.users[username].append(db_path)
                self.save_users()
            return db_path
        except Exception as e:
            self.logger.error(f"Failed to create database for {username}: {e}")
            return None
