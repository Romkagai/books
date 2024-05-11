from database.database import Database
import os
from helpers.metadata_extractor import extract_cover_from_file
from config import DATABASE_AUDIOBOOKS_COLUMNS


class AudioBookInfoModel:
    def __init__(self):
        self.db = Database("database.db")

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
