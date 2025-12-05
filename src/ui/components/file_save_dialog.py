import flet as ft
import os

class FileSaveDialog(ft.Container):
    def __init__(self, on_file_selected, dialog_title="Save File", default_filename="", file_types=None, **kwargs):
        super().__init__(**kwargs)
        
        self.on_file_selected = on_file_selected
        self.dialog_title = dialog_title
        self.default_filename = default_filename
        self.file_types = file_types or [("All files", "*.*")]
        
        self.allowed_extensions = []
        for desc, ext in self.file_types:
            if ext.startswith("*."):
                self.allowed_extensions.append(ext[1:])
        
        self.file_picker = ft.FilePicker(
            on_result=self._handle_save_result
        )
        
        self.page = None
        self._build_ui()
    
    def _build_ui(self):
        self.content = ft.Container()
    
    def open_dialog(self, page: ft.Page):
        self.page = page
        
        if self.file_picker not in page.overlay:
            page.overlay.append(self.file_picker)
            page.update()
        
        self.file_picker.save_file(
            dialog_title=self.dialog_title,
            file_name=self.default_filename,
            allowed_extensions=self.allowed_extensions
        )
    
    def _handle_save_result(self, e: ft.FilePickerResultEvent):
        selected_path = e.path
        
        if self.page and self.file_picker in self.page.overlay:
            self.page.overlay.remove(self.file_picker)
            self.page.update()
        
        if self.on_file_selected:
            self.on_file_selected(selected_path)
    
    @staticmethod
    def ask_saveas_filename(page: ft.Page, **kwargs):
        dialog = FileSaveDialog(**kwargs)
        dialog.open_dialog(page)
        return dialog
    
    def as_button(self, button_text="Save File", icon=ft.Icons.SAVE):
        return ft.ElevatedButton(
            button_text,
            icon=icon,
            on_click=lambda e: self.open_dialog(e.page)
        )
