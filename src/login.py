import logging
import hashlib
import json
import os
import sys
import subprocess
from attempts import Attempt

class Logger:
    def __init__(self, log_file='log_file.log'):
        self.log_file = log_file
        if os.path.splitext(self.log_file)[1] != ".log":
            self.log_file = os.path.splitext(self.log_file)[0] + ".log"
        if not os.path.exists(self.log_file):
            try:
                subprocess.run(["touch", os.path.basename(log_file)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"log file not created: {e}")
    
    def setup_logger(self):
        self.logger = logging.getLogger('logger')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(self.log_file, encoding='utf-8')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
    
    def view_logs(self):
        print("\n=== RECENT LOGS ===\n")
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-10:]
                for log in logs:
                    print(log.strip())
        except FileNotFoundError:
            print("No logs found..")
        except Exception as e:
            print(f"Error reading logs: {e}")
    

class User:
    def __init__(self, username: str = "", password: str = ""):
        self.username = username
        self.password = self.hash_password(password)
        self.attempt = Attempt()
    
    def set_username(self, username: str = ""):
        if not username:
            username = self.attempt.safe_input("Username: ").strip()
            self.attempt.reset()
            while not username and self.attempt.should_retry():
                self.attempt.increment()
                print("Invalid username! Please retry.")
                username = self.attempt.safe_input("Username: ").strip()
            if self.attempt.attempts == 3:
                return False
        self.username = username
        return True
    
    def get_username(self):
        return self.username
    
    def set_password(self, password: str = ""):
        if not password:
            password = self.attempt.safe_input("Password: ")
            self.attempt.reset()
            while not password and self.attempt.should_retry():
                self.attempt.increment()
                print("Password cannot be empty!")
                password = self.attempt.safe_input("Password: ")
            if self.attempt.attempts == 3:
                return False
            confirm_password = self.attempt.safe_input("Confirm Password: ")
            self.attempt.reset()
            while password != confirm_password  and self.attempt.should_retry():
                self.attempt.increment()
                print("Passwords do not match! Please try again.")
                confirm_password = self.attempt.safe_input("Confirm Password: ")
            if self.attempt.attempts == 3:
                return False
        self.password = self.hash_password(password)
        return True
    
    def get_password(self):
        return self.password
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    

class System:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.logger = Logger()
        self.logger.setup_logger()
        self.load_users()
        self.attempt = Attempt()
    
    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                try:
                    subprocess.run(["touch", os.path.basename(self.users_file)], check=True)
                    self.users = {}
                except subprocess.CalledProcessError as e:
                    print(f"log file not created: {e}")
        except Exception as e:
            try:
                self.logger.error(f"Error when loading the users: {e}")
            except Exception:
                print(f"Error when loading the users: {e}")
            self.users = {}
    
    def save_users(self):
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error when saving the users: {e}")
    
    def register(self):
        new_user = User()
        new_user.set_username()
        username = new_user.get_username()
        self.attempt.reset()
        while username in self.users and self.attempt.should_retry():
            self.attempt.increment()
            self.logger.warning(f"Registration attempt with existing username: {username}")
            print("Username already exists")
            new_user.set_username()
            username = new_user.get_username()
        if self.attempt.attempts == 3:
            return False
        
        new_user.set_password()
        password = new_user.get_password()
        if password:
            self.users[username] = password
            self.logger.info(f"New user registered: {username}")
            self.save_users()
            print("Registration successful! You can now log in.")
            return True
        else:
            return False
        
    def login(self, username: str = ""):
        user = User()
        if username:
            user.set_username(username)
        else:
            user.set_username()
            username = user.get_username()
        self.attempt.reset()
        while username not in self.users and self.attempt.should_retry():
            self.attempt.increment()
            self.logger.warning(f"Login attempt with non-existent user: {username}")
            print("User not found!")
            user.set_username()
            username = user.get_username()
        if self.attempt.attempts == 3:
            return False
        
        password = self.attempt.safe_input("Password: ").strip()
        hashed_password = user.hash_password(password)
        self.attempt.reset()
        while self.users[username] != hashed_password and self.attempt.should_retry():
            self.attempt.increment()
            self.logger.warning(f"Failed login attempt for: {username}")
            print("Wrong password! Please retry.")
            password = self.attempt.safe_input("Password: ").strip()
            hashed_password = user.hash_password(password)
        if self.attempt.attempts == 3:
            return False
        self.logger.info(f"Login successful with: {username}")
        print("Login successful!")
        return True
    
    def change_password(self, username: str = ""):
        user = User()
        if username:
            user.set_username(username)
        else:
            user.set_username()
            username = user.get_username()
        if self.login(username):
            user.set_password()
            new_password = user.get_password()
            self.users[username] = new_password
            self.save_users()
            self.logger.info(f"Password changed successfully for: {username}")
            print("Password changed successfully!")
        else:
            print("Password not changed! Too many wrong attempts.")
    

