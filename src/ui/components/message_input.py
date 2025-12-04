import flet as ft

class MessageInput(ft.Container):
    def __init__(
        self,
        on_send,
        on_attach=None,
        placeholder="Ask AI...",
        show_attach_button=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.on_send = on_send
        self.on_attach = on_attach
        self.placeholder = placeholder
        self.show_attach_button = show_attach_button
        
        self.attached_context = None
        self.context_tag = None
        
        self.text_field = ft.TextField(
            hint_text=placeholder,
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=5,
            on_submit=lambda e: self._handle_send(),
            border_radius=10,
            border_color=ft.colors.BLUE_200,
            focused_border_color=ft.colors.BLUE_400,
        )
        
        self._build_content()
    
    def _build_content(self):
        controls = [self.text_field]
        
        if self.show_attach_button and self.on_attach:
            controls.append(
                ft.IconButton(
                    icon=ft.icons.ATTACH_FILE,
                    on_click=self._handle_attach,
                    tooltip="Attach context file",
                    icon_size=24
                )
            )
        
        controls.append(
            ft.IconButton(
                icon=ft.icons.SEND,
                on_click=lambda e: self._handle_send(),
                tooltip="Send message",
                icon_size=24
            )
        )
        
        self.content = ft.Column([
            self._build_context_display(),
            ft.Row(
                controls,
                vertical_alignment=ft.CrossAxisAlignment.END,
                spacing=5
            )
        ], spacing=10)
    
    def _build_context_display(self):
        self.context_container = ft.Container(
            visible=False,
            padding=ft.padding.only(left=10, right=10, top=5),
            content=ft.Row([
                ft.Icon(ft.icons.ATTACHMENT, size=16, color=ft.colors.BLUE_600),
                ft.Text("", size=12, color=ft.colors.BLUE_700, expand=True),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_size=16,
                    on_click=self._remove_context,
                    tooltip="Remove context"
                )
            ], spacing=5)
        )
        return self.context_container
    
    def _handle_send(self):
        message = self.text_field.value.strip()
        if message:
            self.on_send(message, self.attached_context)
            self.clear_input()
    
    def _handle_attach(self, e):
        if self.on_attach:
            self.on_attach(e)
    
    def _remove_context(self, e):
        self.set_context(None)
    
    def set_context(self, context_data, label="Attached context"):
        self.attached_context = context_data
        
        if context_data:
            self.context_tag = ft.Text(
                f"Context: {label}",
                size=12,
                color=ft.colors.BLUE_700,
                expand=True
            )
            self.context_container.content.controls[1] = self.context_tag
            self.context_container.visible = True
            self.text_field.hint_text = f"Ask about {label}..."
        else:
            self.context_tag = None
            self.context_container.visible = False
            self.text_field.hint_text = self.placeholder
        
        self.update()
    
    def get_context(self):
        return self.attached_context
    
    def has_context(self):
        return self.attached_context is not None
    
    def clear_input(self):
        self.text_field.value = ""
        self.set_context(None)
        self.update()
    
    def focus(self):
        self.text_field.focus()
    
    def disable(self, disabled=True):
        self.text_field.disabled = disabled
        for control in self.content.controls[1].controls:
            if isinstance(control, ft.IconButton):
                control.disabled = disabled
        self.update()
    
    def set_placeholder(self, placeholder):
        if not self.has_context():
            self.text_field.hint_text = placeholder
            self.update()
