from database.database import Database
import os
from controllers.data_extractor import extract_metadata, extract_cover_from_file
from config import DATABASE_AUDIOBOOKS_COLUMNS

class AudiobookManager:
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

    def get_book_id(self, file_path):
        return self.db.get_book_id_from_db(file_path)

    def get_audiobooks_list(self):
        return self.db.get_audiobooks_list()

    def get_book_info_by_id(self, book_id):
        book_info = self.db.get_book_info_by_id(book_id)
        if book_info:
            return dict(zip(DATABASE_AUDIOBOOKS_COLUMNS, book_info))
        return None

    def get_audiobook_files(self, book_id):
        return self.db.get_audiobook_files(book_id)

    def find_audiobook_cover(self, book_id):
        file_path = self.db.get_audiobook_files(book_id)[0][0]
        return extract_cover_from_file(file_path)

    def delete_audiobook(self, book_id):
        self.db.delete_audiobook(book_id)

    def add_audiobook_to_favorite(self, book_id):
        self.db.add_audiobook_to_favorite(book_id)

    def is_favorite(self, book_id):
        return self.db.is_favorite(book_id)

    def remove_audiobook_from_favorite(self, book_id):
        self.db.remove_audiobook_from_favorite(book_id)

    def is_completed(self, book_id):
        return self.db.is_completed(book_id)

    def mark_as_completed(self, book_id):
        self.db.mark_as_completed(book_id)

    def mark_as_incompleted(self, book_id):
        self.db.mark_as_incompleted(book_id)

    def update_book_info(self, book_id, book_info):
        self.db.update_book_info(book_id, book_info)

