import flet as ft

def create_auth_header(page, on_login, on_register, show_back=False, user_info=None):
    if user_info:
        return ft.Container(
            content=ft.Row([
                ft.Text("RAG Assistant", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"👤 {user_info}", color=ft.colors.GREY_600),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor=ft.colors.BLUE_50
        )
    else:
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.ElevatedButton("Log in", on_click=on_login, style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE)),
                    ft.OutlinedButton("Sign up", on_click=on_register),
                ], spacing=10),
                ft.Text("RAG Assistant", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(width=100)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15
        )
