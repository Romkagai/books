from database.database import Database
from helpers.metadata_extractor import extract_metadata, get_audio_files
from config import DATABASE_FIELD_MAP
import os

class CatalogPanelModel:
    def __init__(self):
        self.db = Database("database.db")

    def import_audiobook(self, file_path, directory):
        # Проверка, является ли file_path файлом с расширением .mp3
        if directory is None and file_path.endswith(".mp3"):
            print("Выбран аудиофайл (менеджер)")

            metadata = extract_metadata(file_path)
            print(type(metadata))
            print(metadata)

            self.db.add_audiobook_to_db(metadata)
            print("Книга добавлена (менеджер)")

        elif directory:
            print("Выбрана папка (менеджер)")
            metadata = extract_metadata(file_path)
            metadata["title"] = os.path.basename(directory)
            metadata["path"] = directory
            print(metadata)

            self.db.add_audiobook_to_db(metadata)
            print("Книга добавлена (менеджер)")

    def import_file(self, file_path, book_id):
        self.db.add_audiobook_file_to_db(file_path, book_id)

    def get_audiobooks_list(self, sort_by, ascending, search_text, display_options):
        field_names = ['book_id']  # Всегда включаем book_id
        search_fields = []

        for option in display_options:
            if option.lower() in DATABASE_FIELD_MAP:
                db_field = DATABASE_FIELD_MAP[option.lower()]
                field_names.append(db_field)
                search_fields.append(f"{db_field} LIKE '%{search_text}%'")

        fields = ", ".join(field_names)
        search_query = " OR ".join(
            search_fields) if search_fields else "1=1"  # Если нет полей для поиска, возвращаем все записи

        return self.db.get_audiobooks_list(sort_by, ascending, search_query, fields)

    def get_audio_files(self, file_path):
        return get_audio_files(file_path)

    def get_book_id(self, file_path):
        return self.db.get_book_id_from_db(file_path)

    def audiobook_exists(self, file_path):
        return self.db.check_audiobook_in_db(file_path)

    def get_option_by_name(self, option):
        sort_option = DATABASE_FIELD_MAP[option.lower()]
        return sort_option
