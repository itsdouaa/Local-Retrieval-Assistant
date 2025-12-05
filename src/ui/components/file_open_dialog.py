import flet as ft
import os

class FileOpenDialog(ft.Container):
    def __init__(self, on_file_selected, dialog_title="Open File", file_types=None, allow_multiple=False, **kwargs):
        super().__init__(**kwargs)
        
        self.on_file_selected = on_file_selected
        self.dialog_title = dialog_title
        self.file_types = file_types or [("All files", "*.*")]
        self.allow_multiple = allow_multiple
        
        self.allowed_extensions = []
        for desc, ext in self.file_types:
            if ext.startswith("*."):
                self.allowed_extensions.append(ext[1:])
        
        self.file_picker = ft.FilePicker(
            on_result=self._handle_open_result
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
        
        self.file_picker.pick_files(
            dialog_title=self.dialog_title,
            allowed_extensions=self.allowed_extensions,
            allow_multiple=self.allow_multiple
        )
    
    def _handle_open_result(self, e: ft.FilePickerResultEvent):
        if self.page and self.file_picker in self.page.overlay:
            self.page.overlay.remove(self.file_picker)
            self.page.update()
        
        selected_paths = []
        if e.files:
            if self.allow_multiple:
                selected_paths = [file.path for file in e.files]
            else:
                selected_paths = [e.files[0].path] if e.files else []
        
        if self.on_file_selected:
            if self.allow_multiple:
                self.on_file_selected(selected_paths)
            else:
                self.on_file_selected(selected_paths[0] if selected_paths else None)
    
    @staticmethod
    def askopenfilename(page: ft.Page, **kwargs):
        dialog = FileOpenDialog(**kwargs)
        dialog.open_dialog(page)
        return dialog
    
    @staticmethod
    def askopenfilenames(page: ft.Page, **kwargs):
        kwargs['allow_multiple'] = True
        dialog = FileOpenDialog(**kwargs)
        dialog.open_dialog(page)
        return dialog
    
    def as_button(self, button_text="Open File", icon=ft.Icons.FOLDER_OPEN):
        return ft.ElevatedButton(
            button_text,
            icon=icon,
            on_click=lambda e: self.open_dialog(e.page)
        )
