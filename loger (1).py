import logging
import hashlib
import json
import os
import sys

class AuthLogger:
    def __init__(self, log_file='auth.log', users_file='users.json'):
        self.log_file = log_file
        self.users_file = users_file
        self.setup_logger()
        self.load_users()
    
    def setup_logger(self):
        """Configuration du système de logging"""
        self.logger = logging.getLogger('auth_logger')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(self.log_file, encoding='utf-8')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
    
    def load_users(self):
        """Chargement des utilisateurs depuis le fichier JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {
                    "admin": self.hash_password("admin123"),
                    "user": self.hash_password("user123")
                }
                self.save_users()
        except Exception as e:
            try:
                self.logger.error(f"Erreur lors du chargement des utilisateurs: {e}")
            except Exception:
                print(f"Erreur lors du chargement des utilisateurs: {e}")
            self.users = {}
    
    def save_users(self):
        """Sauvegarde des utilisateurs dans le fichier JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des utilisateurs: {e}")
    
    def hash_password(self, password):
        """Hash le mot de passe avec SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def safe_input(self, prompt):
        """Méthode sécurisée pour la saisie utilisateur"""
        try:
            # Essayer d'abord avec input normal
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            # Gérer les erreurs de saisie
            print("\nOpération annulée.")
            return ""
    
    def register(self):
        """Enregistrement d'un nouvel utilisateur"""
        print("\n=== INSCRIPTION ===")
        username = self.safe_input("Nom d'utilisateur: ").strip()
        
        if not username:
            print("❌ Nom d'utilisateur invalide.")
            return False
        
        if username in self.users:
            self.logger.warning(f"Tentative d'inscription avec un nom d'utilisateur existant: {username}")
            print("❌ Ce nom d'utilisateur existe déjà!")
            return False
        
        print("Mot de passe (sera visible): ", end="", flush=True)
        password = self.safe_input("")
        
        print("Confirmer le mot de passe: ", end="", flush=True)
        confirm_password = self.safe_input("")
        
        if password != confirm_password:
            self.logger.warning(f"Mot de passe de confirmation incorrect pour: {username}")
            print("❌ Les mots de passe ne correspondent pas!")
            return False
        
        if not password:
            print("❌ Le mot de passe ne peut pas être vide!")
            return False
        
        self.users[username] = self.hash_password(password)
        self.save_users()
        
        self.logger.info(f"Nouvel utilisateur inscrit: {username}")
        print("✅ Inscription réussie!")
        return True
    
    def login(self):
        """Authentification d'un utilisateur"""
        print("\n=== CONNEXION ===")
        username = self.safe_input("Nom d'utilisateur: ").strip()
        
        if username not in self.users:
            self.logger.warning(f"Tentative de connexion avec un utilisateur inexistant: {username}")
            print("❌ Utilisateur non trouvé!")
            return False
        
        print("Mot de passe: ", end="", flush=True)
        password = self.safe_input("")
        
        hashed_password = self.hash_password(password)
        
        if self.users[username] == hashed_password:
            self.logger.info(f"Connexion réussie pour: {username}")
            print("✅ Connexion réussie!")
            return True
        else:
            self.logger.warning(f"Tentative de connexion échouée pour: {username}")
            print("❌ Mot de passe incorrect!")
            return False
    
    def change_password(self):
        """Changement de mot de passe"""
        print("\n=== CHANGEMENT DE MOT DE PASSE ===")
        username = self.safe_input("Nom d'utilisateur: ").strip()
        
        if username not in self.users:
            self.logger.warning(f"Tentative de changement de mot de passe pour utilisateur inexistant: {username}")
            print("❌ Utilisateur non trouvé!")
            return False
        
        print("Mot de passe actuel: ", end="", flush=True)
        current_password = self.safe_input("")
        
        if self.users[username] != self.hash_password(current_password):
            self.logger.warning(f"Mot de passe actuel incorrect pour: {username}")
            print("❌ Mot de passe actuel incorrect!")
            return False
        
        print("Nouveau mot de passe: ", end="", flush=True)
        new_password = self.safe_input("")
        
        print("Confirmer le nouveau mot de passe: ", end="", flush=True)
        confirm_password = self.safe_input("")
        
        if new_password != confirm_password:
            self.logger.warning(f"Confirmation du nouveau mot de passe échouée pour: {username}")
            print("❌ Les mots de passe ne correspondent pas!")
            return False
        
        if not new_password:
            print("❌ Le mot de passe ne peut pas être vide!")
            return False
        
        self.users[username] = self.hash_password(new_password)
        self.save_users()
        
        self.logger.info(f"Mot de passe changé avec succès pour: {username}")
        print("✅ Mot de passe changé avec succès!")
        return True
    
    def view_logs(self):
        """Affichage des logs récents"""
        print("\n=== DERNIERS LOGS ===")
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-10:]
                for log in logs:
                    print(log.strip())
        except FileNotFoundError:
            print("Aucun log trouvé.")
        except Exception as e:
            print(f"Erreur lors de la lecture des logs: {e}")

def main():
    """Fonction principale"""
    auth_system = AuthLogger()
    
    while True:
        print("\n" + "="*40)
        print("SYSTÈME D'AUTHENTIFICATION AVEC LOGGING")
        print("="*40)
        print("1. S'inscrire")
        print("2. Se connecter")
        print("3. Changer le mot de passe")
        print("4. Voir les logs")
        print("5. Quitter")
        
        try:
            choice = input("\nChoisissez une option (1-5): ").strip()
            
            if choice == '1':
                auth_system.register()
            elif choice == '2':
                auth_system.login()
            elif choice == '3':
                auth_system.change_password()
            elif choice == '4':
                auth_system.view_logs()
            elif choice == '5':
                auth_system.logger.info("Arrêt du système d'authentification")
                print("👋 Au revoir!")
                break
            else:
                print("❌ Option invalide!")
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Au revoir!")
            break

if __name__ == "__main__":
    main()