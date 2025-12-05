import flet as ft
from .file_open_dialog import FileOpenDialog

class MessageInput(ft.Container):
    def __init__(self, on_send, on_file_selected=None, placeholder="Ask AI...", show_attach_button=True, **kwargs):
        super().__init__(**kwargs)
        
        self.on_send = on_send
        self.on_file_selected = on_file_selected
        self.placeholder = placeholder
        self.show_attach_button = show_attach_button
        
        self.attached_file_path = None
        self.context_tag = None
        
        self.text_field = ft.TextField(
            hint_text=placeholder,
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=5,
            on_submit=lambda e: self._handle_send(),
            border_radius=10,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_400,
        )
        
        self._build_content()
    
    def _build_content(self):
        controls = [self.text_field]
        
        if self.show_attach_button:
            controls.append(
                ft.IconButton(
                    icon=ft.Icons.ATTACH_FILE,
                    on_click=self._handle_attach,
                    tooltip="Attach file",
                    icon_size=24
                )
            )
        
        controls.append(
            ft.IconButton(
                icon=ft.Icons.SEND,
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
                ft.Icon(ft.Icons.ATTACHMENT, size=16, color=ft.Colors.BLUE_600),
                ft.Text("", size=12, color=ft.Colors.BLUE_700, expand=True),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    on_click=self._remove_file,
                    tooltip="Remove attached file"
                )
            ], spacing=5)
        )
        return self.context_container
    
    def _handle_send(self):
        message = self.text_field.value.strip()
        if message:
            self.on_send(message, self.attached_file_path)
            self.clear_input()
    
    def _handle_attach(self, e):
        if e.page:
            FileOpenDialog.askopenfilename(
                page=e.page,
                on_file_selected=self._handle_file_selected,
                dialog_title="Attach File",
                file_types=[
                    ("Text files", "*.txt"),
                    ("PDF files", "*.pdf"),
                    ("Word documents", "*.docx"),
                    ("Image files", "*.jpg *.jpeg *.png"),
                    ("All files", "*.*")
                ]
            )
    
    def _handle_file_selected(self, file_path):
        self.attached_file_path = file_path
        
        if file_path:
            import os
            file_name = os.path.basename(file_path)
            self.context_tag = ft.Text(
                f"📄 {file_name}",
                size=12,
                color=ft.Colors.BLUE_700,
                expand=True
            )
            self.context_container.content.controls[1] = self.context_tag
            self.context_container.visible = True
            self.text_field.hint_text = f"Ask about {file_name}..."
        else:
            self.context_tag = None
            self.context_container.visible = False
            self.text_field.hint_text = self.placeholder
        
        if self.on_file_selected:
            self.on_file_selected(file_path)
        
        self.update()
    
    def _remove_file(self, e):
        self.attached_file_path = None
        self.context_tag = None
        self.context_container.visible = False
        self.text_field.hint_text = self.placeholder
        self.update()
    
    def set_context(self, context_data, label="Attached context"):
        if context_data:
            self.context_tag = ft.Text(
                f"Context: {label}",
                size=12,
                color=ft.Colors.BLUE_700,
                expand=True
            )
            self.context_container.content.controls[1] = self.context_tag
            self.context_container.visible = True
            self.text_field.hint_text = f"Ask about {label}..."
        else:
            self._remove_file(None)
        
        self.update()
    
    def get_file_path(self):
        return self.attached_file_path
    
    def has_file(self):
        return self.attached_file_path is not None
    
    def clear_input(self):
        self.text_field.value = ""
        self._remove_file(None)
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
        if not self.has_file():
            self.text_field.hint_text = placeholder
            self.update()
