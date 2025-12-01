import flet as ft

class MessageInput(ft.Row):
    def __init__(self, on_send, on_attach, placeholder="Ask AI..."):
        super().__init__()
        self.on_send = on_send
        self.on_attach = on_attach
        
        self.text_field = ft.TextField(
            hint_text=placeholder,
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=10,
        )
        
        self.controls = [
            self.text_field,
            ft.IconButton(
                icon=ft.Icons.ATTACH_FILE,
                on_click=on_attach,
                tooltip="Attach files"
            ),
            ft.IconButton(
                icon=ft.Icons.SEND,
                on_click=lambda e: self._handle_send(),
                tooltip="Send message"
            )
        ]
        self.vertical_alignment = ft.CrossAxisAlignment.END
    
    def _handle_send(self):
        if self.text_field.value.strip():
            self.on_send(self.text_field.value.strip())
            self.text_field.value = ""
