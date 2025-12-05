import flet as ft

class HistoryDrawer(ft.Container):
    def __init__(self, on_select_chat, on_new_chat, on_close):
        super().__init__()
        
        self.on_select_chat = on_select_chat
        self.on_new_chat = on_new_chat
        self.on_close = on_close
        
        self.width = 300
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_300))
        self.visible = False
        
        self.history_list = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Text("Chat History", size=18, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=20,
                            on_click=lambda e: self.close()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=15,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300))
                ),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        "New Chat",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: self._handle_new_chat(),
                        expand=True
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10)
                ),
                
                ft.Container(
                    content=self.history_list,
                    expand=True,
                    padding=15
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.HISTORY, size=40, color=ft.Colors.GREY_400),
                        ft.Text("No conversations yet", color=ft.Colors.GREY_600)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    expand=True,
                    visible=True
                )
            ],
            spacing=0,
            expand=True
        )
        
        self.empty_state = self.content.controls[3]
    
    def add_chat_item(self, chat_id, title, timestamp="", preview=""):
        self.empty_state.visible = False
        
        chat_item = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(title or "Untitled Chat", 
                           weight=ft.FontWeight.BOLD, 
                           size=14,
                           expand=True),
                    ft.Text(timestamp, size=12, color=ft.Colors.GREY_500)
                ]),
                ft.Text(preview[:50] + "..." if len(preview) > 50 else preview,
                       size=12, 
                       color=ft.Colors.GREY_600)
            ]),
            padding=10,
            border_radius=5,
            bgcolor=ft.Colors.GREY_50,
            on_click=lambda e, cid=chat_id: self._handle_select_chat(cid),
            ink=True
        )
        
        self.history_list.controls.append(chat_item)
        self.update()
    
    def clear_history(self):
        self.history_list.controls.clear()
        self.empty_state.visible = True
        self.update()
    
    def _handle_select_chat(self, chat_id):
        self.close()
        self.on_select_chat(chat_id)
    
    def _handle_new_chat(self):
        self.close()
        self.on_new_chat()
    
    def open(self):
        self.visible = True
        self.update()
    
    def close(self):
        self.visible = False
        self.on_close()
        self.update()
