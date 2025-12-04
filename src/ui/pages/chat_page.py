# pages/chat_page.py
import flet as ft
from components.header import Header
from components.message_input import MessageInput
from components.history_drawer import HistoryDrawer

class ChatPage(ft.Container):
    def __init__(self, router):
        super().__init__()
        self.router = router
        
        self.current_chat_id = None
        
        self.header = Header(
            title="RAG Assistant",
            user_info=router.get_current_user(),
            on_menu_click=self._toggle_sidebar,
            on_logout_click=router.navigate_to_logout
        )
        
        self.sidebar = HistoryDrawer(
            on_select_chat=self._load_chat,
            on_new_chat=self._new_chat,
            on_close=self._toggle_sidebar
        )
        
        self.chat_history = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True
        )
        
        self.message_input = MessageInput(
            on_send=self._send_message,
            on_attach=self._attach_file,
            placeholder="Ask AI..."
        )
        
        self.content = ft.Stack([
            ft.Column([
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
            ], expand=True),
            self.sidebar
        ])
        
        self.expand = True
        self.bgcolor = ft.colors.WHITE
    
    def _toggle_sidebar(self):
        if self.sidebar.visible:
            self.sidebar.close()
        else:
            self.sidebar.open()
    
    def _send_message(self, text, context):
        if text.strip():
            self._add_message("user", text)
            self.router.handle_send_message(text, context, self.current_chat_id)
    
    def _attach_file(self, e):
        self.router.handle_attach_file(e)
    
    def _load_chat(self, chat_id):
        self.current_chat_id = chat_id
        self.router.handle_load_chat(chat_id)
    
    def _new_chat(self):
        self.current_chat_id = None
        self.clear_messages()
        self.message_input.clear_input()
        self.router.handle_new_chat()
    
    def _add_message(self, role, content):
        from components.message_bubble import MessageBubble
        message = {"role": role, "content": content}
        self.chat_history.controls.append(MessageBubble(message))
        self.chat_history.update()
    
    def add_message(self, role, content):
        self._add_message(role, content)
    
    def clear_messages(self):
        self.chat_history.controls.clear()
        self.chat_history.update()
    
    def set_user(self, user_info):
        self.header.update_user_info(user_info)
    
    def add_history_item(self, chat_id, title, timestamp, preview):
        self.sidebar.add_chat_item(chat_id, title, timestamp, preview)
    
    def clear_history(self):
        self.sidebar.clear_history()
    
    def set_context(self, context_data, label):
        self.message_input.set_context(context_data, label)
