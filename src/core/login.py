import logging
import hashlib
import json
import os
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
    def __init__(self, username: str = "", password: str = "", config_path: str = ""):
        self.username = username
        self.password = self.hash_password(password)
        self.config_path = config_path
        self.config_data = {}
        
        # Load config if path exists
        if config_path and os.path.exists(config_path):
            self.load_config()
    
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
    
    def set_config_path(self, config_path: str = ""):
        self.config_path = config_path
        if config_path and os.path.exists(config_path):
            return self.load_config()
        return True
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_path and os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def save_config(self, db_path="", api_key=""):
        """Save configuration to file"""
        try:
            if db_path:
                self.config_data["db_path"] = db_path
            if api_key:
                self.config_data["api_key"] = api_key
            
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_db_path(self):
        """Get database path from config"""
        return self.config_data.get("db_path", "")
    
    def get_api_key(self):
        """Get API key from config"""
        return self.config_data.get("api_key", "")
    
    def set_database_open(self, db_path: str = "", page=None):
        """Open database using path from config or parameter"""
        try:
            # Use provided path or get from config
            path_to_open = db_path or self.get_db_path()
            if not path_to_open:
                return False
            
            self.db = Database()
            self.db.open_existing(path=path_to_open, page=page)
            
            # Update config if new path provided
            if db_path:
                self.save_config(db_path=db_path)
            
            return True
        except Exception:
            return False
    
    def set_database_create(self, page=None, db_path=""):
        """Create new database"""
        try:
            self.db = Database()
            self.db.create(page=page)
            
            # Save the new database path to config
            if self.db.get_path():
                self.save_config(db_path=self.db.get_path())
                return True
            return False
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
            
            # Get config_path if it exists (index 1)
            config_path = self.users[username][1] if len(self.users[username]) > 1 else None
            
            self.logger.info(f"Login successful with: {username}")
            return True, "Login successful!", config_path
            
        except Exception as e:
            self.logger.error(f"Login error for {username}: {e}")
            return False, f"Login failed: {str(e)}", None
    
    def register(self, username, password, confirm_password, page=None):
        try:
            if not username or not username.strip():
                return False, "Username is required"
            
            if not password:
                return False, "Password is required"
            
            if password != confirm_password:
                return False, "Passwords do not match"
            
            if username in self.users:
                self.logger.warning(f"Registration attempt with existing username: {username}")
                return False, "Username already exists"
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = [hashed_password]
            
            if self.save_users():
                self.logger.info(f"New user registered: {username}")
                return True, "Registration successful!"
            else:
                if username in self.users:
                    del self.users[username]
                return False, "Failed to save user data"    
        except Exception as e:
            self.logger.error(f"Registration error for {username}: {e}")
            return False, f"Registration failed: {str(e)}"
    
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
    
    def user_exists(self, username):
        return username in self.users
    
    def set_user_config_path(self, username, config_path):
        """
        Set the configuration file path for a user
        config_path: Path to the JSON file containing db_path and api_key
        """
        try:
            if username not in self.users:
                self.logger.warning(f"Attempt to set config for non-existent user: {username}")
                return False
            
            # Ensure the users[username] list has at least one element (password)
            if len(self.users[username]) == 0:
                self.users[username] = [self.users[username]]
            
            # If we already have a config_path (index 1), update it
            if len(self.users[username]) > 1:
                self.users[username][1] = config_path
            else:
                # Add config_path as second element
                self.users[username].append(config_path)
            
            # Save changes
            if self.save_users():
                self.logger.info(f"Updated config path for {username}: {config_path}")
                return True
            else:
                self.logger.error(f"Failed to save config path for {username}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to set config path for {username}: {e}")
            return False
    
    def get_user_config_path(self, username):
        """
        Get the configuration file path for a user
        Returns: config_path if exists, None otherwise
        """
        try:
            if username not in self.users:
                return None
            
            if len(self.users[username]) > 1:
                config_path = self.users[username][1]
                if os.path.exists(config_path):
                    return config_path
                else:
                    self.logger.warning(f"Config file doesn't exist: {config_path}")
                    return None
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting config path for {username}: {e}")
            return None
    
    def load_user_config(self, username):
        """
        Load user configuration from config file
        Returns: dictionary with config data, None if error
        """
        try:
            config_path = self.get_user_config_path(username)
            if not config_path:
                return None
            
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            return config_data
            
        except Exception as e:
            self.logger.error(f"Error loading config for {username}: {e}")
            return None
    
    def save_user_config(self, username, config_data):
        """
        Save user configuration to config file
        config_data: dictionary containing db_path and api_key
        Returns: True if successful, False otherwise
        """
        try:
            config_dir = os.path.dirname(self.get_default_config_path(username))
            os.makedirs(config_dir, exist_ok=True)
            
            config_path = self.get_user_config_path(username)
            if not config_path:
                config_path = self.get_default_config_path(username)
                self.set_user_config_path(username, config_path)
            
            # Save config data
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            self.logger.info(f"Saved config for {username} to {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving config for {username}: {e}")
            return False
    
    def get_default_config_path(self, username):
        """
        Get default configuration file path for a user
        """
        config_dir = os.path.join(os.path.expanduser("~"), ".rag_assistant", "users")
        return os.path.join(config_dir, f"{username}_config.json")
    
    def create_user_config(self, username, db_path, api_key):
        """
        Create and save user configuration
        """
        config_data = {
            "db_path": db_path,
            "api_key": api_key,
            "created_at": datetime.datetime.now().isoformat()
        }
        return self.save_user_config(username, config_data)
