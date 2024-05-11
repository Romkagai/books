import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        # Создание таблиц
        self.create_table(table_name="audiobooks",
                          columns=['book_id INTEGER PRIMARY KEY AUTOINCREMENT',
                                   'title TEXT NOT NULL DEFAULT "Без названия"',
                                   'author TEXT NOT NULL DEFAULT "Неизвестен"',
                                   'genre TEXT NOT NULL DEFAULT "Неизвестен"',
                                   'year INTEGER NOT NULL DEFAULT 0',
                                   'narrator TEXT NOT NULL DEFAULT "Неизвестен"',
                                   'date_added TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP',
                                   'description TEXT NOT NULL DEFAULT "Без описания"',
                                   'is_completed BOOL DEFAULT FALSE',
                                   'is_favorite BOOL DEFAULT FALSE',
                                   'bitrate INTEGER NOT NULL DEFAULT 0',
                                   'duration INTEGER NOT NULL DEFAULT 0',
                                   'size INTEGER NOT NULL DEFAULT 0',
                                   'path TEXT NOT NULL UNIQUE'])

        self.create_table(table_name="audiobooks_files",
                          columns=['file_id INTEGER PRIMARY KEY AUTOINCREMENT',
                                   'is_listened BOOL DEFAULT FALSE',
                                   'file_path TEXT NOT NULL UNIQUE',
                                   'book_id INTEGER NOT NULL',
                                   'FOREIGN KEY (book_id) REFERENCES audiobooks(book_id) ON DELETE CASCADE'])

    def add_audiobook_to_db(self, metadata):
        self.connect()
        try:
            title = metadata["title"]
            author = metadata["author"]
            genre = metadata["genre"]
            year = metadata["year"]
            narrator = metadata["narrator"]
            description = metadata["description"]
            bitrate = metadata["bitrate"]
            duration = metadata["duration"]
            size = metadata["size"]
            file_path = metadata["path"]

            self.cursor.execute("INSERT INTO audiobooks (title, author, genre, year, narrator, description, bitrate, "
                                "duration, size, path) VALUES ("
                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (
                                title, author, genre, year, narrator, description, bitrate, duration, size, file_path,))
            self.connection.commit()

            print("Книга добавлена в базу(database)", file_path)

        except sqlite3.IntegrityError as e:
            print("Error", e)

        self.close()

    def add_audiobook_file_to_db(self, file_path, book_id):
        self.connect()
        self.cursor.execute("INSERT INTO audiobooks_files (file_path, book_id) VALUES (?, ?)", (file_path, book_id))
        self.connection.commit()
        self.close()

    def check_audiobook_in_db(self, file_path):
        self.connect()
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM audiobooks WHERE path = ? LIMIT 1)", (file_path,))
        exists = self.cursor.fetchone()[0]
        self.close()
        return exists

    def get_audiobooks_list(self, sort_by, ascending, search_query, fields):
        self.connect()
        direction = "ASC" if ascending else "DESC"
        self.cursor.execute(f"SELECT {fields} FROM audiobooks "
                            f"WHERE {search_query} "
                            f"ORDER BY {sort_by} {direction}")
        records = self.cursor.fetchall()
        self.close()
        return records

    def get_book_info_by_name(self, title):
        self.connect()
        self.cursor.execute("SELECT * FROM audiobooks WHERE title = (?)", (title,))
        book_info = self.cursor.fetchall()
        self.close()
        return book_info

    def get_book_id_from_db(self, file_path):
        self.connect()
        self.cursor.execute("SELECT book_id FROM audiobooks WHERE path = (?)", (file_path,))
        book_id = self.cursor.fetchone()[0]
        self.close()
        return book_id

    def get_book_info_by_id(self, book_id):
        self.connect()
        self.cursor.execute("SELECT * FROM audiobooks WHERE book_id = (?)", (book_id,))
        book_info = self.cursor.fetchone()
        self.close()
        return book_info

    def get_audiobook_files(self, book_id):
        self.connect()
        self.cursor.execute("SELECT file_path, is_listened FROM audiobooks_files WHERE book_id = (?)", (book_id,))
        files = self.cursor.fetchall()
        self.close()
        return files

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def create_table(self, table_name, columns):
        self.connect()
        try:
            column_str = ', '.join(columns)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created (existed) successfully:", table_name)
        except sqlite3.Error as e:
            print("Error creating table:", e)
        self.close()

    def delete_audiobook(self, book_id):
        self.connect()
        self.cursor.execute("DELETE FROM audiobooks WHERE book_id = (?)", (book_id,))
        self.connection.commit()
        self.close()

    def add_audiobook_to_favorite(self, book_id):
        self.connect()
        self.cursor.execute("UPDATE audiobooks SET is_favorite = 1 WHERE book_id = (?)", (book_id,))
        self.connection.commit()
        self.close()

    def is_favorite(self, book_id):
        self.connect()
        self.cursor.execute("SELECT is_favorite FROM audiobooks WHERE book_id = (?)", (book_id,))
        is_favorite = self.cursor.fetchone()[0]
        self.close()
        return is_favorite

    def remove_audiobook_from_favorite(self, book_id):
        self.connect()
        self.cursor.execute("UPDATE audiobooks SET is_favorite = 0 WHERE book_id = (?)", (book_id,))
        self.connection.commit()
        self.close()

    def is_completed(self, book_id):
        self.connect()
        self.cursor.execute("SELECT is_completed FROM audiobooks WHERE book_id = (?)", (book_id,))
        is_completed = self.cursor.fetchone()[0]
        self.close()
        return is_completed

    def mark_as_completed(self, book_id):
        self.connect()
        self.cursor.execute("UPDATE audiobooks SET is_completed = 1 WHERE book_id = (?)", (book_id,))
        self.connection.commit()
        self.close()

    def mark_as_incompleted(self, book_id):
        self.connect()
        self.cursor.execute("UPDATE audiobooks SET is_completed = 0 WHERE book_id = (?)", (book_id,))
        self.connection.commit()
        self.close()

    def update_book_info(self, book_id, metadata):
        self.connect()
        try:
            # Создаем строку с перечислением полей и их новых значений
            update_parts = ', '.join([f"{key} = ?" for key in metadata.keys()])
            values = list(metadata.values()) + [book_id]

            query = f"UPDATE audiobooks SET {update_parts} WHERE book_id = ?"
            self.cursor.execute(query, values)
            self.connection.commit()

            print(f"Информация по книге с ID {book_id} обновлена в базе.")

        except Exception as e:
            print(f"Ошибка при обновлении аудиокниги: {e}")
        finally:
            self.close()