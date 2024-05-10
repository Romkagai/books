from PyQt6.QtWidgets import QMessageBox
from models.settings_manager import SettingsManager


class SettingsHandler:
    def __init__(self, ui):
        self.manager = SettingsManager()
        self.ui = ui

    def apply_sorting_settings(self, checkboxes):
        settings = self.manager.load_settings()
        sorting_settings = settings.get('sorting', {})
        for option, checkbox in checkboxes.items():
            checkbox.setChecked(sorting_settings.get(option, False))

    def save_sorting_settings(self, checkboxes):
        settings = self.manager.load_settings()

        # Создаем словарь с текущими настройками чекбоксов
        current_settings = {option: checkbox.isChecked() for option, checkbox in checkboxes.items()}

        # Проверяем, включен ли хотя бы один чекбокс
        if not any(current_settings.values()):
            # Все чекбоксы выключены, показываем сообщение и включаем первый по умолчанию
            QMessageBox.warning(self.ui, "Настройки", "Должна быть выбрана хотя бы одна опция сортировки!")
            first_option = next(iter(checkboxes))
            checkboxes[first_option].setChecked(True)
            current_settings[first_option] = True
            settings['sorting'] = current_settings
            self.manager.save_settings(settings)

        else:
            # Хотя бы один чекбокс включен, сохраняем настройки
            # Сохраняем измененные настройки
            settings['sorting'] = current_settings
            self.manager.save_settings(settings)

            # Информируем пользователя о сохранении настроек
            QMessageBox.information(self.ui, "Настройки", "Настройки сохранены!")

    def get_enabled_sorting_options(self):
        settings = self.manager.load_settings()
        return [option for option, enabled in settings['sorting'].items() if enabled]