import json


class SettingsModel:
    def __init__(self, filename='settings.json'):
        self.filename = filename

    def load_settings(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Файл настроек не найден. Возвращаем значения по умолчанию.")
            return {}

    def save_settings(self, settings):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def get_enabled_sorting_options(self):
        settings = self.load_settings()
        return [option for option, enabled in settings['sorting'].items() if enabled]
