import os

from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QLabel

from view.audiobook_editor_view import EditBookDialog


class AudiobookInfoController(QObject):
    update_table = pyqtSignal()

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_connections()

        self.current_row = None
        self.current_is_favorite = None
        self.current_is_completed = None

        self.current_book_info_options = None

        self.init_info_labels()

    # Создаем список всех лейблов
    def init_info_labels(self):
        all_options = self.model.get_all_book_info_options()
        for option in all_options:
            label = QLabel(f"{option}")
            label.setWordWrap(True)
            label.setMaximumWidth(200)
            label.setVisible(False)  # Изначально все лейблы скрыты
            self.view.infoLabels[option] = label
            self.view.infoLabelsLayout.addWidget(label)

    # Пришел сигнал об обновлении настроек отображаемых лейблов
    def update_book_info_options(self, options):
        self.current_book_info_options = options
        self.update_info_labels()

    # Обновление отображаемых лейблов
    def update_info_labels(self):
        all_labels = set(self.view.infoLabels.keys())
        visible_labels = set(self.current_book_info_options)

        # Сделаем видимыми только нужные лейблы и скроем остальные
        for label in all_labels:
            if label in visible_labels:
                self.view.infoLabels[label].setVisible(True)
            else:
                self.view.infoLabels[label].setVisible(False)

    # Выбрана книга в таблице
    def update_selected_book_id(self, row, book_id):
        self.current_row = row
        self.current_book_id = book_id
        self.display_audiobook_info()

    def display_audiobook_info(self, bookExists=True):
        if bookExists:
            book_id = self.current_book_id
            is_fav = self.model.is_favorite(book_id)
            is_completed = self.model.is_completed(book_id)

            # Обновляем информацию о текущей книге.
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
            self.deactivate_buttons()

    def update_current_book_info(self):
        book_info = self.model.get_book_info_by_id(self.current_book_id)

        for key, label in self.view.infoLabels.items():
            if key in book_info:
                label.setText(f"{key}: {book_info[key]}")

        # Проверка наличия и отображение таблицы файлов, если путь является директорией
        if 'Путь' in book_info and os.path.isdir(book_info['Путь']):
            self.view.fileTable.setVisible(True)
            self.update_file_table(self.current_book_id)
        else:
            self.view.fileTable.setVisible(False)

        # Активация кнопок
        for button in self.view.actionButtons:
            button.setEnabled(True)

        self.update_cover(self.current_book_id)

    def clear_info_labels(self):
        for key, label in self.view.infoLabels.items():
            label.setText(f"{key}")
        self.view.fileTable.setVisible(False)
        self.view.imageScene.clear()
        self.view.imageScene.addText("Выберите книгу")


    def update_cover(self, book_id):
        try:
            cover_data = self.model.find_audiobook_cover(book_id)
            if cover_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(cover_data):
                    self.view.imageScene.clear()  # Очистка предыдущих изображений
                    self.view.imageScene.addPixmap(
                        pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.view.imageScene.clear()
                self.view.imageScene.addText("Ошибка загрузки изображения")
        except:
            self.view.imageScene.clear()
            self.view.imageScene.addText("Обложка не найдена")

    def update_file_table(self, book_id):
        files = self.model.get_audiobook_files(book_id)
        self.view.fileTable.setRowCount(len(files))  # Установка количества строк
        for index, (file_path, is_listened) in enumerate(files):
            self.view.fileTable.setItem(index, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.view.fileTable.setItem(index, 1, QTableWidgetItem("Да" if is_listened else "Нет"))

    def delete_audiobook(self):
        # Удаляем аудиокнигу из базы данных.
        self.model.delete_audiobook(self.current_book_id)

        # Удаляем аудиокнигу
        self.current_book_id = None

        # Попросим контроллер таблицы её обновить
        self.update_table.emit()

        # Обновляем информацию о текущей книге
        self.clear_info_labels()

        # Деактивируем кнопки
        self.deactivate_buttons()

    def deactivate_buttons(self):
        for button in self.view.actionButtons:
            button.setEnabled(False)

    def update_completed_button(self):
        # Устанавливаем текст и стиль кнопки в зависимости от состояния выполнения
        if self.current_is_completed:
            text = "Пометить как незавершенное"
            color = "red"
            new_handler = self.mark_as_incomplete
        else:
            text = "Пометить как завершенное"
            color = "green"
            new_handler = self.mark_as_complete

        # Обновляем свойства кнопки
        self.view.addCompletedButton.setText(text)
        self.view.addCompletedButton.setStyleSheet(f"background-color: {color};")

        # Переключаем обработчик событий
        self.view.addCompletedButton.clicked.disconnect()
        self.view.addCompletedButton.clicked.connect(new_handler)

    def mark_as_complete(self):
        # Изменение состояния выполненного в базе данных
        self.model.mark_as_completed(self.current_book_id)
        # Обновление текущего состояния выполненного
        self.current_is_completed = True
        # Обновление состояния выполненного
        self.update_completed_button()

    def mark_as_incomplete(self):
        # Изменение состояния выполненного в базе данных
        self.model.mark_as_incompleted(self.current_book_id)
        # Обновление текущего состояния выполненного
        self.current_is_completed = False
        # Обновление состояния выполненного
        self.update_completed_button()

    def update_favourite_button(self):
        # Обновление состояния избранного
        if self.current_is_favorite:
            text = "Удалить из избранного"
            color = "red"
            new_handler = self.remove_from_favorites
        else:
            text = "Добавить в избранное"
            color = "green"
            new_handler = self.add_to_favorites

            # Обновляем свойства кнопки
        self.view.addFavoriteButton.setText(text)
        self.view.addFavoriteButton.setStyleSheet(f"background-color: {color};")

        # Переключаем обработчик событий
        self.view.addFavoriteButton.clicked.disconnect()
        self.view.addFavoriteButton.clicked.connect(new_handler)

    def add_to_favorites(self):
        # Изменение состояния избранного в базе данных
        self.model.add_audiobook_to_favorite(self.current_book_id)
        # Обновление текущего состояния избранного
        self.current_is_favorite = True
        # Явное обновление кнопки
        self.update_favourite_button()

    def remove_from_favorites(self):
        # Изменение состояния избранного в базе данных
        self.model.remove_audiobook_from_favorite(self.current_book_id)
        # Обновление текущего состояния избранного
        self.current_is_favorite = False
        # Явное обновление кнопки
        self.update_favourite_button()

    def edit_book(self):
        book_info = self.model.get_book_info_by_id(self.current_book_id, self.model.get_all_book_info_options()[:-1])

        dialog = EditBookDialog(self.view, book_info)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.model.update_book_info(self.current_book_id, dialog.book_info)
            self.update_table.emit()
            self.update_current_book_info()

    def setup_connections(self):
        self.view.findBookInfoButton.clicked.connect(lambda: None)
        self.view.addFavoriteButton.clicked.connect(lambda: None)
        self.view.addCompletedButton.clicked.connect(lambda: None)
        self.view.deleteButton.clicked.connect(self.delete_audiobook)
        self.view.editButton.clicked.connect(self.edit_book)