from database.database import Database
from helpers.metadata_extractor import extract_metadata, get_audio_files
from config import DATABASE_FIELD_MAP
import os

class CatalogPanelModel:
    def __init__(self):
        self.db = Database("database.db")

    def import_audiobook(self, file_path, directory=None):
        """
        Импортирует аудиокнигу в базу данных.
        :param file_path: Путь к аудиофайлу или директории.
        :param directory: Директория, если файл_path является директорией.
        """
        metadata = extract_metadata(file_path)
        if directory:
            metadata["title"] = os.path.basename(directory)
            metadata["path"] = directory
        self.db.add_audiobook_to_db(metadata)

    def import_file(self, file_path, book_id):
        """
        Импортирует файл аудиокниги в базу данных.
        :param file_path: Путь к аудиофайлу.
        :param book_id: Идентификатор книги в базе данных.
        """
        self.db.add_audiobook_file_to_db(file_path, book_id)

    def get_audiobooks_list(self, sort_by, ascending, search_text, display_options):
        """
        Получает список аудиокниг из базы данных.
        :param sort_by: Поле для сортировки.
        :param ascending: Порядок сортировки.
        :param search_text: Текст для поиска.
        :param display_options: Поля для отображения.
        :return: Список аудиокниг.
        """
        field_names = ['book_id', 'is_favorite', 'is_completed']  # Добавляем поля для состояния
        search_fields = []

        for option in display_options:
            if option.lower() in DATABASE_FIELD_MAP:
                db_field = DATABASE_FIELD_MAP[option.lower()]
                field_names.append(db_field)
                search_fields.append(f"{db_field} LIKE '%{search_text}%'")

        fields = ", ".join(field_names)
        search_query = " OR ".join(search_fields) if search_fields else "1=1"

        return self.db.get_audiobooks_list(sort_by, ascending, search_query, fields)

    def get_audio_files(self, file_path):
        """
        Получает аудиофайлы из директории.
        :param file_path: Путь к директории.
        :return: Список аудиофайлов.
        """
        return get_audio_files(file_path)

    def get_book_id(self, file_path):
        """
        Получает идентификатор книги из базы данных.
        :param file_path: Путь к аудиофайлу или директории.
        :return: Идентификатор книги.
        """
        return self.db.get_book_id_from_db(file_path)

    def audiobook_exists(self, file_path):
        """
        Проверяет существование аудиокниги в базе данных.
        :param file_path: Путь к аудиофайлу или директории.
        :return: True, если аудиокнига существует, иначе False.
        """
        return self.db.check_audiobook_in_db(file_path)

    def get_option_by_name(self, option):
        """
        Получает поле базы данных по имени опции.
        :param option: Имя опции.
        :return: Поле базы данных.
        """
        return DATABASE_FIELD_MAP.get(option.lower())
