import flet as ft
import sys
import os
import asyncio
from session import Session
from login import System
from database import Database

class ChatMessage(ft.Row):
    def __init__(self, message: dict):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.END
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message["role"])),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message["role"]),
            ),
            ft.Column(
                controls=[
                    ft.Text(message["role"].title(), weight=ft.FontWeight.BOLD),
                    ft.Text(message["content"], selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, role: str):
        return "U" if role == "user" else "AI"

    def get_avatar_color(self, role: str):
        return ft.Colors.BLUE if role == "user" else ft.Colors.GREEN
    

class RAG_Assistant:
    def __init__(self):
        self.page = None
        self.session = None
        self.system = System()
        self.current_user = None
        self.db = None
        
    def main(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.show_login_screen()

    def setup_page(self):
        self.page.title = "RAG Assistant"
        self.page.padding = 0
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_login_screen(self):
        """Affiche l'écran de connexion/inscription"""
        login_content = ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("ChatGPT", size=28, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    controls=[
                                        ft.TextButton("Log in", on_click=lambda _: self.show_login_form()),
                                        ft.FilledButton("Sign up for free", on_click=lambda _: self.show_register_form())
                                    ],
                                    spacing=20
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=20,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
                    ),
                    
                    # Main content
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "What can I help with?",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "Ask anything",
                                    size=18,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                
                                # Options grid
                                ft.ResponsiveRow(
                                    controls=[
                                        self.create_option_card("Attach", ft.Icons.ATTACH_FILE, self.attach_file),
                                        self.create_option_card("Search", ft.Icons.SEARCH, self.show_search),
                                        self.create_option_card("Study", ft.Icons.SCHOOL, self.show_study),
                                        self.create_option_card("+", ft.Icons.ADD, self.show_more_options),
                                    ],
                                    spacing=20,
                                    run_spacing=20
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=40
                        ),
                        padding=40,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            ),
            expand=True
        )
        
        self.page.clean()
        self.page.add(login_content)

    def create_option_card(self, title: str, icon: str, on_click):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=20, color=ft.Colors.BLUE),
                    ft.Text(title, weight=ft.FontWeight.W_500)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            on_click=on_click,
            col={"sm": 6, "md": 3}
        )

    def show_login_form(self):
        """Affiche le formulaire de connexion"""
        username_field = ft.TextField(label="Username", expand=True)
        password_field = ft.TextField(label="Password", password=True, expand=True)
        
        login_dialog = ft.AlertDialog(
            title=ft.Text("Log in"),
            content=ft.Column(
                controls=[username_field, password_field],
                tight=True
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                ft.FilledButton("Log in", on_click=lambda _: self.handle_login(
                    username_field.value, password_field.value
                )),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = login_dialog
        login_dialog.open = True
        self.page.update()

    def show_register_form(self):
        """Affiche le formulaire d'inscription"""
        username_field = ft.TextField(label="Username", expand=True)
        password_field = ft.TextField(label="Password", password=True, expand=True)
        confirm_password_field = ft.TextField(label="Confirm Password", password=True, expand=True)
        
        register_dialog = ft.AlertDialog(
            title=ft.Text("Sign up"),
            content=ft.Column(
                controls=[username_field, password_field, confirm_password_field],
                tight=True
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                ft.FilledButton("Sign up", on_click=lambda _: self.handle_register(
                    username_field.value, password_field.value, confirm_password_field.value
                )),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = register_dialog
        register_dialog.open = True
        self.page.update()

    async def handle_login(self, username: str, password: str):
        """Gère la connexion"""
        if not username or not password:
            self.show_snackbar("Please fill all fields!")
            return
            
        try:
            self.system.load_users()
            if self.system.login(username):
                self.current_user = username
                self.db = Database()
                self.db.open_existing(self.system.users[username][1])
                self.close_dialog()
                self.show_chat_interface()
            else:
                self.show_snackbar("Login failed!")
        except Exception as e:
            self.show_snackbar(f"Login error: {str(e)}")

    async def handle_register(self, username: str, password: str, confirm_password: str):
        """Gère l'inscription"""
        if not username or not password:
            self.show_snackbar("Please fill all fields!")
            return
            
        if password != confirm_password:
            self.show_snackbar("Passwords don't match!")
            return
            
        try:
            self.system.load_users()
            if self.system.register():
                self.show_snackbar("Registration successful! Please log in.")
                self.close_dialog()
            else:
                self.show_snackbar("Registration failed!")
        except Exception as e:
            self.show_snackbar(f"Registration error: {str(e)}")

    def show_chat_interface(self):
        """Affiche l'interface de chat principale"""
        self.chat_messages = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )
        
        self.message_field = ft.TextField(
            hint_text="Message ChatGPT...",
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=5,
        )
        
        chat_content = ft.Column(
            controls=[
                # Header avec bouton de déconnexion
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("ChatGPT", size=24, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Text(f"User: {self.current_user}", color=ft.Colors.GREY_600),
                                    ft.IconButton(
                                        icon=ft.icons.LOGOUT,
                                        on_click=lambda _: self.logout(),
                                        tooltip="Logout"
                                    )
                                ],
                                spacing=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_50
                ),
                
                # Zone des messages
                ft.Container(
                    content=self.chat_messages,
                    padding=20,
                    expand=True,
                ),
                
                # Zone de saisie
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ATTACH_FILE,
                                on_click=self.attach_file,
                                tooltip="Attach file"
                            ),
                            self.message_field,
                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                on_click=self.send_message,
                                tooltip="Send message"
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.END
                    ),
                    padding=20,
                    bgcolor=ft.Colors.GREY_50
                )
            ],
            expand=True
        )
        
        self.page.clean()
        self.page.add(chat_content)
        self.session = Session()

    async def send_message(self, e):
        """Envoie un message et gère la réponse"""
        if not self.message_field.value.strip():
            return
            
        message_text = self.message_field.value.strip()
        self.message_field.value = ""
        self.page.update()
        
        # Ajouter le message utilisateur
        user_message = {"role": "user", "content": message_text}
        self.chat_messages.controls.append(ChatMessage(user_message))
        self.page.update()
        
        # Simuler une réponse (à intégrer avec votre session)
        try:
            # Utiliser votre système de session existant
            if self.session:
                self.session.messages.add("user", message_text)
                
                # Ici vous intégrerez la vraie réponse Groq
                # Pour l'instant, simulation
                assistant_message = {"role": "assistant", "content": "This is a simulated response. Integrate with your Groq API."}
                self.chat_messages.controls.append(ChatMessage(assistant_message))
                
        except Exception as ex:
            error_message = {"role": "assistant", "content": f"Error: {str(ex)}"}
            self.chat_messages.controls.append(ChatMessage(error_message))
        
        self.page.update()

    def attach_file(self, e=None):
        """Gère l'attachement de fichiers"""
        self.show_snackbar("File attachment feature - integrate with your file.py")

    def show_search(self, e=None):
        self.show_snackbar("Search feature - integrate with your database search")

    def show_study(self, e=None):
        self.show_snackbar("Study mode - integrate with your context system")

    def show_more_options(self, e=None):
        self.show_snackbar("Additional options")

    def logout(self):
        """Déconnecte l'utilisateur"""
        self.current_user = None
        self.session = None
        self.db = None
        self.show_login_screen()

    def close_dialog(self):
        """Ferme la boîte de dialogue"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def show_snackbar(self, message: str):
        """Affiche un message snackbar"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

def main():
    app = RAG_Assistant()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
