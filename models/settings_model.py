import json

class SettingsModel:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Файл настроек не найден. Возвращаем значения по умолчанию.")
            return {}

    def save_settings(self, sort_options, display_options, book_info_options, theme):
        settings = {
            'sort_options': sort_options,
            'display_options': display_options,
            'book_info_options': book_info_options,
            'theme': theme
        }
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def get_enabled_sorting_options(self):
        settings = self.load_settings()
        return [option for option, enabled in settings['sort_options'].items() if enabled]

    def get_enabled_display_options(self):
        settings = self.load_settings()
        return [option for option, enabled in settings['display_options'].items() if enabled]

    def get_enabled_book_info_options(self):
        settings = self.load_settings()
        return [option for option, enabled in settings['book_info_options'].items() if enabled]

    def get_sorting_options(self):
        settings = self.load_settings()
        return settings['sort_options']

    def get_display_options(self):
        settings = self.load_settings()
        return settings['display_options']

    def get_book_info_options(self):
        settings = self.load_settings()
        return settings['book_info_options']

    def get_theme(self):
        settings = self.load_settings()
        return settings.get('theme')
