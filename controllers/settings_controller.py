from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox


class SettingsController(QObject):
    update_sort_settings = pyqtSignal(object)
    update_display_settings = pyqtSignal(object)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_ui_state()
        self.setup_connections()

    def setup_ui_state(self):
        self.load_initial_settings()
        self.emit_settings_to_view()

    def setup_connections(self):
        self.view.saveSettingsButton.clicked.connect(self.save_settings)

    def load_initial_settings(self):
        sort_options = self.model.get_sorting_options()
        display_options = self.model.get_display_options()

        for option, checkbox in self.view.sort_checkboxes.items():
            checkbox.setChecked(sort_options.get(option, False))

        for option, checkbox in self.view.table_display_checkboxes.items():
            checkbox.setChecked(display_options.get(option, False))

    def emit_settings_to_view(self):
        print(self.model.get_enabled_sorting_options())
        self.update_sort_settings.emit(self.model.get_enabled_sorting_options())
        self.update_display_settings.emit(self.model.get_enabled_display_options())

    def save_settings(self):
        sort_options = {option: checkbox.isChecked() for option, checkbox in self.view.sort_checkboxes.items()}
        display_options = {option: checkbox.isChecked() for option, checkbox in self.view.table_display_checkboxes.items()}

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

        self.model.save_settings(sort_options, display_options)
        self.emit_settings_to_view()

