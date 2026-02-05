import flet as ft
import tkinter as tk
from tkinter import filedialog
import os

class MessageInput(ft.Container):
    def __init__(self, on_send=None, on_attach=None, placeholder="Ask AI...", show_attach_button=True, **kwargs):
        self.on_send = on_send
        self.on_attach = on_attach
        self.placeholder = placeholder
        self.show_attach_button = show_attach_button
        
        super().__init__(**kwargs)
        
        self.attached_file_path = None
        
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
        buttons = []
        
        if self.show_attach_button:
            buttons.append(ft.IconButton(
                icon=ft.Icons.ATTACH_FILE_ROUNDED,
                icon_color=ft.Colors.GREY_600,
                on_click=self._handle_attach_with_tkinter
            ))
            
        buttons.append(ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            icon_color=ft.Colors.BLUE_600,
            on_click=lambda e: self._handle_send()
        ))

        input_row = ft.Row(
            controls=[
                self.text_field,
                *buttons
            ],
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=5
        )

        self.content = ft.Column([
            self._build_context_display(),
            input_row
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
    
    def _handle_attach_with_tkinter(self, e):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier",
            filetypes=[
                ("Documents", "*.pdf *.docx *.txt"),
                ("Images", "*.png *.jpg *.jpeg"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        root.destroy()

        if file_path:
            self._handle_file_selected(file_path)
            if self.on_attach:
                self.on_attach(file_path)
    
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
        
        self.update()

    def _remove_file(self, e):
        self.attached_file_path = None
        self.context_container.visible = False
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
    
    def _handle_send(self):
        message = self.text_field.value.strip()
        if message:
            self.on_send(message, self.attached_file_path)
            self.clear_input()
    
    def clear_input(self):
        self.text_field.value = ""
        self._remove_file(None)
     
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
