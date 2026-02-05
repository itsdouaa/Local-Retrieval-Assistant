import flet as ft
from ..components import Header
from ..components import MessageInput
from ..components import HistoryDrawer


class ChatPage(ft.Container):
    def __init__(self):
        super().__init__()

        # Callbacks externes
        self.on_send_message = None
        self.on_attach_file = None
        self.on_menu_click = None
        self.on_profile_click = None
        self.on_logout_click = None
        self.on_load_chat = None
        self.on_new_chat = None

        # Etat
        self.current_user = None
        self.current_chat_id = None

        # Header
        self.header = Header(
            title="RAG Assistant",
            user_info=None,
            on_menu_click=self._handle_menu_click,
            on_profile_click=self._handle_profile_click,
            show_back_button=False,
            on_logout_click=self._handle_logout_click
        )

        # Sidebar
        self.sidebar = HistoryDrawer(
            on_select_chat=self._handle_select_chat,
            on_new_chat=self._handle_new_chat,
            on_close=self._close_sidebar
        )

        # Historique messages
        self.chat_history = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        # Input
        self.message_input = MessageInput(
            on_send=self._handle_send,
            on_attach=self._handle_attach,
            placeholder="Ask AI..."
        )

        # Layout
        self.content = ft.Stack(
            [
                ft.Column(
                    [
                        self.header,
                        ft.Container(
                            content=self.chat_history,
                            padding=20,
                            expand=True
                        ),
                        ft.Container(
                            content=self.message_input,
                            padding=ft.padding.symmetric(horizontal=20, vertical=10)
                        )
                    ],
                    expand=True
                ),
                self.sidebar
            ]
        )

        self.expand = True
        self.bgcolor = ft.Colors.WHITE

    def _toggle_sidebar(self):
        if self.sidebar.visible:
            self.sidebar.close()
        else:
            self.sidebar.open()

    def _close_sidebar(self):
        self.sidebar.visible = False
        
    def _handle_menu_click(self):
        if self.on_menu_click:
            self.on_menu_click()
        else:
            self._toggle_sidebar()

    def _handle_profile_click(self):
        if self.on_profile_click:
            self.on_profile_click()

    def _handle_logout_click(self):
        if self.on_logout_click:
            self.on_logout_click()

    def _handle_send(self, text, context):
        if text.strip() and self.on_send_message:
            self._add_message("user", text)
            self.on_send_message(text, context, self.current_chat_id)

    def _handle_attach(self, e):
        if self.on_attach_file:
            self.on_attach_file(e)

    def _handle_select_chat(self, chat_id):
        self.current_chat_id = chat_id
        if self.on_load_chat:
            self.on_load_chat(chat_id)
        self._close_sidebar()

    def _handle_new_chat(self):
        self.current_chat_id = None
        self.clear_messages()
        self.message_input.clear_input()
        if self.on_new_chat:
            self.on_new_chat()
        self._close_sidebar()

    def _add_message(self, role, content):
        from ..components.message_bubble import MessageBubble
        message = {"role": role, "content": content}
        self.chat_history.controls.append(MessageBubble(message))

    def add_message(self, role, content):
        self._add_message(role, content)

    def clear_messages(self):
        self.chat_history.controls.clear()
        
    def add_history_item(self, chat_id, title, timestamp, preview):
        self.sidebar.add_chat_item(chat_id, title, timestamp, preview)

    def clear_history(self):
        self.sidebar.clear_history()

    def set_callbacks(self, callbacks):
        self.on_send_message = callbacks.get("on_send_message")
        self.on_attach_file = callbacks.get("on_attach_file")
        self.on_menu_click = callbacks.get("on_menu_click")
        self.on_profile_click = callbacks.get("on_profile_click")
        self.on_logout_click = callbacks.get("on_logout_click")
        self.on_load_chat = callbacks.get("on_load_chat")
        self.on_new_chat = callbacks.get("on_new_chat")

    def set_user(self, user_info):
        self.current_user = user_info
        self.header.update_user_info(user_info)

    def clear_user(self):
        self.current_user = None
        self.header.update_user_info(None)

    def set_context(self, context_data, label):
        self.message_input.set_context(context_data, label)

    def enable_input(self, enabled=True):
        self.message_input.disable(not enabled)

    def reset(self):
        self.clear_user()
        self.clear_messages()
        self.clear_history()
        self.message_input.clear_input()
        self.current_chat_id = None
        self._close_sidebar()

