from database.database import Database
from helpers.metadata_extractor import extract_cover_from_file
from config import DATABASE_FIELD_MAP, BOOK_INFO_OPTIONS

class AudioBookInfoModel:
    def __init__(self):
        self.db = Database("database.db")

    def get_book_info_by_id(self, book_id, options=BOOK_INFO_OPTIONS):
        """
        Возвращает информацию о книге по ее ID.
        """
        column_options = [DATABASE_FIELD_MAP[option.lower()] for option in options if option.lower() in DATABASE_FIELD_MAP]

        book_info = self.db.get_book_optional_info_by_id(book_id, column_options)
        if book_info:
            return dict(zip(options, book_info))
        return None

    def get_audiobook_files(self, book_id):
        """
        Возвращает список файлов аудиокниги.
        """
        return self.db.get_audiobook_files(book_id)

    def find_audiobook_cover(self, book_id):
        """
        Находит обложку аудиокниги.
        """
        file_path = self.db.get_audiobook_files(book_id)[0][0]
        return extract_cover_from_file(file_path)

    def delete_audiobook(self, book_id):
        """
        Удаляет аудиокнигу.
        """
        self.db.delete_audiobook(book_id)

    def add_audiobook_to_favorite(self, book_id):
        """
        Добавляет аудиокнигу в избранное.
        """
        self.db.add_audiobook_to_favorite(book_id)

    def is_favorite(self, book_id):
        """
        Проверяет, является ли аудиокнига избранной.
        """
        return self.db.is_favorite(book_id)

    def remove_audiobook_from_favorite(self, book_id):
        """
        Удаляет аудиокнигу из избранного.
        """
        self.db.remove_audiobook_from_favorite(book_id)

    def is_completed(self, book_id):
        """
        Проверяет, завершена ли аудиокнига.
        """
        return self.db.is_completed(book_id)

    def mark_as_completed(self, book_id):
        """
        Помечает аудиокнигу как завершенную.
        """
        self.db.mark_as_completed(book_id)

    def mark_as_incompleted(self, book_id):
        """
        Помечает аудиокнигу как незавершенную.
        """
        self.db.mark_as_incompleted(book_id)

    def update_book_info(self, book_id, book_info):
        """
        Обновляет информацию о книге.
        """
        db_book_info = {DATABASE_FIELD_MAP.get(key.lower(), key): value for key, value in book_info.items()}
        self.db.update_book_info(book_id, db_book_info)

    def update_listened_status(self, state, file_path):
        """
        Обновляет статус прослушивания файла.
        """
        self.db.update_listened_status(state, file_path)

    def get_all_book_info_options(self):
        """
        Возвращает все возможные опции информации о книге.
        """
        return BOOK_INFO_OPTIONS
