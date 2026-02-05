import flet as ft


class HistoryDrawer(ft.Container):
    def __init__(self, on_select_chat, on_new_chat, on_close):
        super().__init__()

        self.on_select_chat = on_select_chat
        self.on_new_chat = on_new_chat
        self.on_close = on_close

        self.width = 280
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_300))
        self.visible = False

        self.history_list = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.empty_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.HISTORY, size=32, color=ft.Colors.GREY_400),
                    ft.Text("No conversations yet", size=12, color=ft.Colors.GREY_600)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            ),
            alignment=ft.alignment.center,
            expand=True,
            visible=True
        )

        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Chat History", size=16, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=18,
                                on_click=lambda e: self.close()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=12,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300))
                ),

                ft.Container(
                    content=ft.ElevatedButton(
                        "New Chat",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: self._handle_new_chat(),
                        expand=True
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8)
                ),

                ft.Container(
                    content=self.history_list,
                    expand=True,
                    padding=12
                ),

                self.empty_state
            ],
            spacing=0,
            expand=True
        )

    def add_chat_item(self, chat_id, title, timestamp="", preview=""):
        self.empty_state.visible = False

        chat_item = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(title or "Untitled Chat",
                                    weight=ft.FontWeight.BOLD,
                                    size=12,
                                    expand=True),
                            ft.Text(timestamp, size=10, color=ft.Colors.GREY_500)
                        ]
                    ),
                    ft.Text(
                        preview[:40] + "..." if len(preview) > 40 else preview,
                        size=11,
                        color=ft.Colors.GREY_600
                    )
                ],
                spacing=3
            ),
            padding=8,
            border_radius=6,
            bgcolor=ft.Colors.GREY_50,
            ink=True,
            on_click=lambda e, cid=chat_id: self._handle_select_chat(cid)
        )

        self.history_list.controls.append(chat_item)
        self.update()

    def clear_history(self):
        self.history_list.controls.clear()
        self.empty_state.visible = True
    
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
        if self.on_close:
            self.on_close()
        self.update()

