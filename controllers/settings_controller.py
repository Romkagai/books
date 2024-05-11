from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox


class SettingsController(QObject):
    update_sort_settings = pyqtSignal(object)
    save_requested = pyqtSignal(dict)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_connections()

    def setup_connections(self):
        # Подключаем сигналы view к слотам контроллера
        self.save_requested.connect(self.save_new_settings)
        self.view.saveSettingsButton.clicked.connect(self.emit_save_requested)
        self.set_checkboxes()

    def set_checkboxes(self):
        settings = self.model.load_settings()
        sorting_settings = settings.get('sorting', {})
        for option, checkbox in self.view.sort_checkboxes.items():
            checkbox.setChecked(sorting_settings.get(option, False))


    def save_new_settings(self, checkbox_states):
        settings = self.model.load_settings()

        if not any(checkbox_states.values()):
            QMessageBox.warning(self.view, "Настройки", "Должна быть выбрана хотя бы одна опция сортировки!")
            first_option = next(iter(checkbox_states))
            self.view.sort_checkboxes[first_option].setChecked(True)
            checkbox_states[first_option] = True
        settings['sorting'] = checkbox_states
        self.model.save_settings(settings)
        self.update_sort_settings.emit(self.model.get_enabled_sorting_options())
        QMessageBox.information(self.view, "Настройки", "Настройки сохранены!")

    def load_app_settings(self):
        self.update_sort_settings.emit(self.model.get_enabled_sorting_options())

    def emit_save_requested(self):
        # Испускаем сигнал с текущим состоянием чекбоксов
        checkbox_states = {option: checkbox.isChecked() for option, checkbox in self.view.sort_checkboxes.items()}
        self.save_requested.emit(checkbox_states)

