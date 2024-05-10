from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
from models.audiobook_manager import AudiobookManager
from view.book_editor import EditBookDialog
from config import DATABASE_FIELD_MAP as field_map, SORT_OPTIONS


class AudiobookCataloguerLogic:
    def __init__(self, ui):
        self.ui = ui
        self.audiobook_manager = AudiobookManager()
        # Текущая книга
        self.current_book_id = None
        self.current_is_favorite = None
        self.current_is_completed = None
        # Текущая опция сортировки
        self.current_sort_option = field_map[SORT_OPTIONS[0].lower()]
        self.sortAscending = True

    def add_audiobook(self):
        choice = self.prompt_audiobook_choice()
        if choice == 0:  # File selected
            self.add_file()
        elif choice == 1:  # Directory selected
            self.add_directory()

    def prompt_audiobook_choice(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Добавление аудиокниги")
        msg_box.setText("Выберите, что хотите добавить:")
        msg_box.addButton("Файл", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Папку", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        return msg_box.exec()

    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "Выберите аудиофайл", "", "Audio Files (*.mp3 *.aac *.wav)")
        if file_path:
            self.audiobook_manager.import_audiobook(file_path, directory=None)
            book_id = self.audiobook_manager.get_book_id(file_path)
            print(file_path, book_id)
            self.audiobook_manager.import_file(file_path, book_id)
            self.update_audiobook_table(self.current_sort_option)

    def add_directory(self):
        directory = QFileDialog.getExistingDirectory(self.ui, "Выберите папку с аудиофайлами")
        if directory:
            files_to_add = self.audiobook_manager.get_audio_files(directory)
            print(files_to_add)
            if files_to_add:
                self.audiobook_manager.import_audiobook(files_to_add[0], directory)
                book_id = self.audiobook_manager.get_book_id(directory)
                for file_path in files_to_add:
                    self.audiobook_manager.import_file(file_path, book_id)
                    self.update_audiobook_table(self.current_sort_option)

    def update_audiobook_table(self, sort_by=None, ascending=None, search_text=""):
        if sort_by is None:
            sort_by = self.current_sort_option
        if ascending is None:
            ascending = self.sortAscending
        records = self.audiobook_manager.get_audiobooks_list(sort_by, ascending, search_text)
        self.ui.CatalogPanel.audiobookTable.setRowCount(len(records))

        for index, (book_id, author, title) in enumerate(records):
            self.ui.CatalogPanel.audiobookTable.setItem(index, 0, QTableWidgetItem(str(book_id)))
            self.ui.CatalogPanel.audiobookTable.setItem(index, 1, QTableWidgetItem(author))
            self.ui.CatalogPanel.audiobookTable.setItem(index, 2, QTableWidgetItem(title))

    def display_audiobook_info(self, row):
        if row >= 0:
            book_id = self.ui.CatalogPanel.audiobookTable.item(row, 0).text()
            is_fav = self.audiobook_manager.is_favorite(book_id)
            is_completed = self.audiobook_manager.is_completed(book_id)

            print(book_id, is_fav, is_completed)  # Debug print, возможно, стоит убрать после тестирования.

            # Обновляем информацию о текущей книге.
            if self.current_book_id != book_id:
                self.current_book_id = book_id
                self.update_current_book_info()

            # Обновляем состояние кнопки "Избранное".
            if self.current_is_favorite != is_fav:
                self.current_is_favorite = is_fav
                self.update_favourite_button()

            # Обновляем состояние кнопки "Завершено".
            if self.current_is_completed != is_completed:
                self.current_is_completed = is_completed
                self.update_completed_button()
        else:
            # Очищаем информацию и деактивируем кнопки.
            self.clear_info_labels()
            for button in self.ui.BookInfoTab.actionButtons:
                button.setEnabled(False)

    def update_current_book_info(self):
        book_info = self.audiobook_manager.get_book_info_by_id(self.current_book_id)
        if book_info is None:
            print("Ошибка: информация о книге не найдена")
            return

        # Обновление информационных лейблов
        self.ui.BookInfoTab.infoLabels[0].setText(f"Название: {book_info['title']}")
        self.ui.BookInfoTab.infoLabels[1].setText(f"Автор: {book_info['author']}")
        self.ui.BookInfoTab.infoLabels[2].setText(f"Жанр: {book_info['genre']}")
        self.ui.BookInfoTab.infoLabels[3].setText(f"Год: {book_info['year']}")
        self.ui.BookInfoTab.infoLabels[4].setText(f"Чтец: {book_info['narrator']}")
        self.ui.BookInfoTab.infoLabels[5].setText(f"Дата добавления: {book_info['date_added']}")
        self.ui.BookInfoTab.infoLabels[6].setText(f"Описание: {book_info['description']}")

        # Проверка наличия и отображение таблицы файлов, если путь является директорией
        if 'path' in book_info and os.path.isdir(book_info['path']):
            self.ui.BookInfoTab.fileTable.setVisible(True)
            self.update_file_table(self.current_book_id)
        else:
            self.ui.BookInfoTab.fileTable.setVisible(False)

        # Активация кнопок
        for button in self.ui.BookInfoTab.actionButtons:
            button.setEnabled(True)

        self.update_cover(self.current_book_id)

    def clear_info_labels(self):
        # Очистка лейблов
        self.ui.BookInfoTab.infoLabels[0].setText(f"Название:")
        self.ui.BookInfoTab.infoLabels[1].setText(f"Автор:")
        self.ui.BookInfoTab.infoLabels[2].setText(f"Жанр:")
        self.ui.BookInfoTab.infoLabels[3].setText(f"Год:")
        self.ui.BookInfoTab.infoLabels[4].setText(f"Чтец:")
        self.ui.BookInfoTab.infoLabels[5].setText(f"Дата добавления:")
        self.ui.BookInfoTab.infoLabels[6].setText(f"Описание:")
        self.ui.BookInfoTab.fileTable.setVisible(False)
        self.ui.BookInfoTab.imageScene.clear()
        self.ui.BookInfoTab.imageScene.addText("Обложка не найдена")

        # Деактивация кнопок
        for button in self.ui.BookInfoTab.actionButtons:
            button.setEnabled(False)

    def update_completed_button(self):
        # Обновление состояния выполненного
        if self.current_is_completed:
            self.ui.BookInfoTab.addCompletedButton.setText("Пометить как незавершенное")
            self.ui.BookInfoTab.addCompletedButton.setStyleSheet("background-color: red;")
            self.ui.BookInfoTab.addCompletedButton.clicked.disconnect()
            self.ui.BookInfoTab.addCompletedButton.clicked.connect(self.mark_as_incomplete)

        else:
            self.ui.BookInfoTab.addCompletedButton.setText("Пометить как завершенное")
            self.ui.BookInfoTab.addCompletedButton.setStyleSheet("background-color: green;")
            self.ui.BookInfoTab.addCompletedButton.clicked.disconnect()
            self.ui.BookInfoTab.addCompletedButton.clicked.connect(self.mark_as_complete)

    def mark_as_complete(self):
        # Изменение состояния выполненного в базе данных
        self.audiobook_manager.mark_as_completed(self.current_book_id)
        # Обновление текущего состояния выполненного
        self.current_is_completed = True
        # Обновление состояния выполненного
        self.update_completed_button()

    def mark_as_incomplete(self):
        # Изменение состояния выполненного в базе данных
        self.audiobook_manager.mark_as_incompleted(self.current_book_id)
        # Обновление текущего состояния выполненного
        self.current_is_completed = False
        # Обновление состояния выполненного
        self.update_completed_button()

    def update_favourite_button(self):
        # Обновление состояния избранного
        if self.current_is_favorite:
            self.ui.BookInfoTab.addFavoriteButton.setText("Удалить из избранного")
            self.ui.BookInfoTab.addFavoriteButton.setStyleSheet("background-color: red;")
            self.ui.BookInfoTab.addFavoriteButton.clicked.disconnect()
            self.ui.BookInfoTab.addFavoriteButton.clicked.connect(self.remove_from_favorites)

        else:
            self.ui.BookInfoTab.addFavoriteButton.setText("Добавить в избранное")
            self.ui.BookInfoTab.addFavoriteButton.setStyleSheet("background-color: green;")
            self.ui.BookInfoTab.addFavoriteButton.clicked.disconnect()
            self.ui.BookInfoTab.addFavoriteButton.clicked.connect(self.add_to_favorites)

    def add_to_favorites(self):
        # Изменение состояния избранного в базе данных
        self.audiobook_manager.add_audiobook_to_favorite(self.current_book_id)
        # Обновление текущего состояния избранного
        self.current_is_favorite = True
        # Явное обновление кнопки
        self.update_favourite_button()

    def remove_from_favorites(self):
        # Изменение состояния избранного в базе данных
        self.audiobook_manager.remove_audiobook_from_favorite(self.current_book_id)
        # Обновление текущего состояния избранного
        self.current_is_favorite = False
        # Явное обновление кнопки
        self.update_favourite_button()

    def update_file_table(self, book_id):
        files = self.audiobook_manager.get_audiobook_files(book_id)
        print(files)
        self.ui.BookInfoTab.fileTable.setRowCount(len(files))  # Установка количества строк
        for index, (file_path, is_listened) in enumerate(files):
            self.ui.BookInfoTab.fileTable.setItem(index, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.ui.BookInfoTab.fileTable.setItem(index, 1, QTableWidgetItem("Да" if is_listened else "Нет"))

    def update_cover(self, book_id):
        try:
            cover_data = self.audiobook_manager.find_audiobook_cover(book_id)
            if cover_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(cover_data):
                    self.ui.BookInfoTab.imageScene.clear()  # Очистка предыдущих изображений
                    self.ui.BookInfoTab.imageScene.addPixmap(pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.ui.BookInfoTab.imageScene.clear()
                self.ui.BookInfoTab.imageScene.addText("Ошибка загрузки изображения")
        except:
            self.ui.BookInfoTab.imageScene.clear()
            self.ui.BookInfoTab.imageScene.addText("Обложка не найдена")

    def delete_audiobook(self):
        # Удаляем аудиокнигу из базы данных.
        self.audiobook_manager.delete_audiobook(self.current_book_id)

        # Удаляем строку из таблицы.
        row = self.ui.CatalogPanel.audiobookTable.currentRow()
        self.ui.CatalogPanel.audiobookTable.removeRow(row)

        # Проверяем состояние таблицы после удаления.
        if row < self.ui.CatalogPanel.audiobookTable.rowCount():
            # Если удалили не последнюю строку, показываем информацию о новой строке на этом месте.
            self.display_audiobook_info(row)
        elif self.ui.CatalogPanel.audiobookTable.rowCount() > 0:
            # Если удалили последнюю строку, но в таблице ещё есть записи, показываем информацию о предыдущей строке.
            self.display_audiobook_info(self.ui.CatalogPanel.audiobookTable.rowCount() - 1)
        else:
            # Если строк больше нет, очищаем информацию о книге.
            self.display_audiobook_info(-1)

    def do_nothing(self):
        pass

    def edit_book(self):
        row = self.ui.CatalogPanel.audiobookTable.currentRow()
        if row == -1:
            QMessageBox.warning(self.ui, "Предупреждение", "Выберите книгу для редактирования")
            return

        book_info = self.audiobook_manager.get_book_info_by_id(self.current_book_id)

        dialog = EditBookDialog(self.ui, book_info)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.audiobook_manager.update_book_info(self.current_book_id, dialog.book_info)
            self.update_audiobook_table(self.current_sort_option)
            self.update_current_book_info()

    def sort_changed(self):
        currentText = self.ui.CatalogPanel.sortOptions.currentText()
        self.current_sort_option = field_map[currentText.lower()]
        self.update_audiobook_table(self.current_sort_option, self.sortAscending)

    def update_current_book_id(self, row):
        self.display_audiobook_info(row)
        self.current_book_id = self.ui.CatalogPanel.audiobookTable.item(row, 0).text()
        print(row, self.current_book_id)

    def toggle_sort_direction(self):
        self.sortAscending = not self.sortAscending
        if self.sortAscending:
            self.ui.CatalogPanel.sortDirectionButton.setText("⬆️")
        else:
            self.ui.CatalogPanel.sortDirectionButton.setText("⬇️")
        self.sort_changed()

    def do_search(self):
        search_text = self.ui.CatalogPanel.searchPanel.text()
        self.update_audiobook_table(self.current_sort_option, self.sortAscending, search_text)
