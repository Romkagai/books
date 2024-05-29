from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

class SettingsController(QObject):
    update_sort_settings = pyqtSignal(object)
    update_display_settings = pyqtSignal(object)
    update_book_info_settings = pyqtSignal(object)
    update_theme = pyqtSignal(object)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_ui_state()
        self.setup_connections()

    def setup_ui_state(self):
        self.load_initial_settings()
        self.emit_settings_to_view()
        self.load_theme()

    def setup_connections(self):
        self.view.saveSettingsButton.clicked.connect(self.save_settings)

    def load_initial_settings(self):
        sort_options = self.model.get_sorting_options()
        display_options = self.model.get_display_options()
        book_info_options = self.model.get_book_info_options()

        for option, checkbox in self.view.sort_checkboxes.items():
            checkbox.setChecked(sort_options.get(option, False))

        for option, checkbox in self.view.table_display_checkboxes.items():
            checkbox.setChecked(display_options.get(option, False))

        for option, checkbox in self.view.book_info_checkboxes.items():
            checkbox.setChecked(book_info_options.get(option, False))

    def emit_settings_to_view(self):
        self.update_sort_settings.emit(self.model.get_enabled_sorting_options())
        self.update_display_settings.emit(self.model.get_enabled_display_options())
        self.update_book_info_settings.emit(self.model.get_enabled_book_info_options())

    def load_theme(self):
        theme = self.model.get_theme()
        self.view.theme_combo_box.setCurrentText(theme)
        self.change_theme()

    def save_settings(self):
        sort_options = {option: checkbox.isChecked() for option, checkbox in self.view.sort_checkboxes.items()}
        display_options = {option: checkbox.isChecked() for option, checkbox in self.view.table_display_checkboxes.items()}
        book_info_options = {option: checkbox.isChecked() for option, checkbox in self.view.book_info_checkboxes.items()}
        theme = self.view.theme_combo_box.currentText()

        self.change_theme()

        # Проверяем, что хотя бы одна опция в каждом разделе включена
        if not any(sort_options.values()):
            first_sort_option = next(iter(self.view.sort_checkboxes))
            self.view.sort_checkboxes[first_sort_option].setChecked(True)
            sort_options[first_sort_option] = True
            QMessageBox.warning(self.view, "Настройки сортировки", "Должна быть выбрана хотя бы одна опция сортировки!")

        if not any(display_options.values()):
            first_display_option = next(iter(self.view.table_display_checkboxes))
            self.view.table_display_checkboxes[first_display_option].setChecked(True)
            display_options[first_display_option] = True
            QMessageBox.warning(self.view, "Настройки отображения", "Должна быть выбрана хотя бы одна опция отображения!")

        if not any(book_info_options.values()):
            first_book_info_option = next(iter(self.view.book_info_checkboxes))
            self.view.book_info_checkboxes[first_book_info_option].setChecked(True)
            book_info_options[first_book_info_option] = True
            QMessageBox.warning(self.view, "Настройки отображения", "Должна быть выбрана хотя бы одна опция отображения!")

        self.model.save_settings(sort_options, display_options, book_info_options, theme)
        self.emit_settings_to_view()

    def change_theme(self):
        theme = self.view.theme_combo_box.currentText()
        if theme == "Светлая тема":
            self.update_theme.emit("light_theme.css")
        elif theme == "Темная тема":
            self.update_theme.emit("dark_theme.css")
