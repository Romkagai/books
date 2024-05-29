from database.database import Database
from helpers.metadata_extractor import extract_metadata, get_audio_files, format_size, format_bitrate, format_duration
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
        if directory:
            total_bitrate = 0
            total_duration = 0
            total_size = 0
            file_count = 0

            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        file_path = os.path.join(root, file)
                        metadata = extract_metadata(file_path)
                        total_bitrate += metadata["bitrate"]
                        total_duration += metadata["duration"]
                        total_size += metadata["size"]
                        file_count += 1

            if file_count > 0:
                avg_bitrate = total_bitrate / file_count  # Средний битрейт

                # Применение форматирования к метаданным
                formatted_metadata = {
                    "title": os.path.basename(directory),
                    "author": metadata["author"],  # Берем автора из последнего файла
                    "genre": metadata["genre"],  # Берем жанр из последнего файла
                    "year": metadata["year"],  # Берем год из последнего файла
                    "narrator": metadata["narrator"],  # Берем рассказчика из последнего файла
                    "description": metadata["description"],  # Берем описание из последнего файла
                    "bitrate": format_bitrate(avg_bitrate),
                    "duration": format_duration(total_duration),
                    "size": format_size(total_size),
                    "path": directory
                }

                self.db.add_audiobook_to_db(formatted_metadata)
        else:
            metadata = extract_metadata(file_path)

            # Форматирование отдельных метаданных
            metadata["bitrate"] = format_bitrate(metadata["bitrate"])
            metadata["duration"] = format_duration(metadata["duration"])
            metadata["size"] = format_size(metadata["size"])

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
