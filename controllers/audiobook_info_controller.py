import os
import subprocess

from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QLabel, QCheckBox, QWidget, QHBoxLayout, QMessageBox

from view.audiobook_editor_view import EditBookDialog
from helpers.metadata_extractor import find_books, parse_book_details
from view.audiobook_selector_view import SelectBookDialog


class AudiobookInfoController(QObject):
    update_table = pyqtSignal()

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_connections()

        self.current_row = None
        self.current_book_id = None
        self.current_is_favorite = None
        self.current_is_completed = None

        self.current_book_info_options = None
        self.current_book_info = None

        self.init_info_labels()

    def init_info_labels(self):
        """
        Создаем список всех лейблов
        """
        all_options = self.model.get_all_book_info_options()
        for row, option in enumerate(all_options):
            label_key = QLabel(f"{option}:")
            label_value = QLabel()
            label_key.setStyleSheet("font-weight: bold;")
            label_value.setWordWrap(True)
            label_value.setMinimumHeight(20)  # Установим минимальную высоту для лейблов
            self.view.info_labels[option] = (label_key, label_value)
            self.view.info_labels_layout.addWidget(label_key, row, 0)
            self.view.info_labels_layout.addWidget(label_value, row, 1)
            self.view.info_labels_layout.setRowStretch(row, 1)  # Добавим растягивание строк

    def update_book_info_options(self, options):
        """
        Пришел сигнал об обновлении настроек отображаемых лейблов
        """
        self.current_book_info_options = options
        self.update_info_labels()

    def update_info_labels(self):
        """
        Обновление отображаемых лейблов
        """
        all_labels = set(self.view.info_labels.keys())
        visible_labels = set(self.current_book_info_options)

        # Сделаем видимыми только нужные лейблы и скроем остальные
        for label in all_labels:
            key_label, value_label = self.view.info_labels[label]
            if label in visible_labels:
                key_label.setVisible(True)
                value_label.setVisible(True)
            else:
                key_label.setVisible(False)
                value_label.setVisible(False)

        if self.current_book_id is not None:
            self.update_current_book_info()

    def update_selected_book_id(self, row, book_id):
        """
        Выбрана книга в таблице
        """
        self.current_row = row
        if self.current_book_id != book_id:
            self.current_book_id = book_id
            self.current_book_info = self.model.get_book_info_by_id(book_id)  # Cache book info
            self.display_audiobook_info()

    def display_audiobook_info(self, book_exists=True):
        if book_exists:
            book_id = self.current_book_id
            is_fav = self.model.is_favorite(book_id)
            is_completed = self.model.is_completed(book_id)

            self.update_current_book_info()

            if self.current_is_favorite != is_fav:
                self.current_is_favorite = is_fav
                self.update_favorite_button()

            if self.current_is_completed != is_completed:
                self.current_is_completed = is_completed
                self.update_completed_button()
        else:
            self.clear_info_labels()
            self.deactivate_buttons()

    def update_current_book_info(self):
        book_info = self.current_book_info

        for key, (key_label, value_label) in self.view.info_labels.items():
            if key in self.current_book_info_options and key in book_info:
                key_label.setVisible(True)
                value_label.setVisible(True)
                value_label.setText(f"{book_info[key]}")
            else:
                key_label.setVisible(False)
                value_label.setVisible(False)
                value_label.setText("")

        if 'Путь' in book_info and os.path.isdir(book_info['Путь']):
            self.view.file_table.setVisible(True)
            self.update_file_table(self.current_book_id)
        else:
            self.view.file_table.setVisible(False)

        for button in self.view.action_buttons.values():
            button.setEnabled(True)

        self.update_cover(self.current_book_id)

    def clear_info_labels(self):
        for key, (key_label, value_label) in self.view.info_labels.items():
            key_label.setVisible(False)
            value_label.setVisible(False)
            value_label.setText("")
        self.view.file_table.setVisible(False)
        self.view.image_scene.clear()
        self.view.image_scene.addText("Выберите книгу")

    def update_cover(self, book_id):
        try:
            cover_data = self.model.find_audiobook_cover(book_id)
            if cover_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(cover_data):
                    self.view.image_scene.clear()
                    self.view.image_scene.addPixmap(
                        pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.view.image_scene.clear()
                self.view.image_scene.addText("Ошибка загрузки изображения")
        except Exception as e:
            self.view.image_scene.clear()
            self.view.image_scene.addText("Обложка не найдена")
            print(f"Ошибка при загрузке обложки: {e}")

    def update_file_table(self, book_id):
        files = self.model.get_audiobook_files(book_id)
        self.view.file_table.setRowCount(len(files))
        for index, (file_path, is_listened) in enumerate(files):
            self.view.file_table.setItem(index, 0, QTableWidgetItem(os.path.basename(file_path)))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            chk_box = QCheckBox()
            chk_box.setChecked(is_listened)
            chk_box.stateChanged.connect(lambda state, path=file_path: self.toggle_listened(state, path))

            layout.addWidget(chk_box)
            widget.setLayout(layout)
            self.view.file_table.setCellWidget(index, 1, widget)

    def toggle_listened(self, state, file_path):
        is_listened = state == Qt.CheckState.Checked
        self.model.update_listened_status(is_listened, file_path)

    def delete_audiobook(self):
        self.model.delete_audiobook(self.current_book_id)
        self.current_book_id = None
        self.update_table.emit()
        self.clear_info_labels()
        self.deactivate_buttons()

    def deactivate_buttons(self):
        for button in self.view.action_buttons.values():
            button.setEnabled(False)

    def update_completed_button(self):
        if self.current_is_completed:
            text = "Пометить как незавершенное"
            new_handler = self.mark_as_incomplete
        else:
            text = "Пометить как завершенное"
            new_handler = self.mark_as_complete

        self.view.action_buttons["mark_completed"].setText(text)

        self.view.action_buttons["mark_completed"].clicked.disconnect()
        self.view.action_buttons["mark_completed"].clicked.connect(new_handler)

        self.update_table.emit()

    def mark_as_complete(self):
        self.model.mark_as_completed(self.current_book_id)
        self.current_is_completed = True
        self.update_completed_button()

    def mark_as_incomplete(self):
        self.model.mark_as_incompleted(self.current_book_id)
        self.current_is_completed = False
        self.update_completed_button()

    def update_favorite_button(self):
        if self.current_is_favorite:
            text = "Удалить из избранного"
            new_handler = self.remove_from_favorites
        else:
            text = "Добавить в избранное"
            new_handler = self.add_to_favorites

        self.view.action_buttons["add_favorite"].setText(text)

        self.view.action_buttons["add_favorite"].clicked.disconnect()
        self.view.action_buttons["add_favorite"].clicked.connect(new_handler)

        self.update_table.emit()

    def add_to_favorites(self):
        self.model.add_audiobook_to_favorite(self.current_book_id)
        self.current_is_favorite = True
        self.update_favorite_button()

    def remove_from_favorites(self):
        self.model.remove_audiobook_from_favorite(self.current_book_id)
        self.current_is_favorite = False
        self.update_favorite_button()

    def edit_book(self, book_info=None):
        if book_info is None or not isinstance(book_info, dict):
            book_info = self.current_book_info

        book_info.pop('Путь', None)
        dialog = EditBookDialog(self.view, book_info)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.model.update_book_info(self.current_book_id, dialog.book_info)
            self.current_book_info = self.model.get_book_info_by_id(self.current_book_id)
            self.update_table.emit()
            self.update_current_book_info()

    def open_audiobook_folder(self):
        book_path = self.current_book_info.get('Путь')
        if book_path:
            directory_path = os.path.dirname(book_path)
            if os.path.isdir(directory_path):
                if os.name == 'nt':
                    subprocess.run(['explorer', '/select,', os.path.normpath(book_path)])
                else:
                    subprocess.run(['open', directory_path])

    def find_audiobook_info(self):
        book_title = self.current_book_info.get('Название')
        if book_title:
            books = find_books(book_title)
            if books:
                select_dialog = SelectBookDialog(self.view, books)
                if select_dialog.exec() == QDialog.DialogCode.Accepted:
                    selected_book = select_dialog.selected_book
                    if selected_book:
                        book_details = parse_book_details(selected_book['URL'])
                        if book_details:
                            self.edit_book(book_details)
                    else:
                        QMessageBox.warning(self.view, "Ошибка",
                                            "Не удалось обнаружить информацию для данной аудиокниги")
            else:
                QMessageBox.warning(self.view, "Ошибка", "Не удалось обнаружить информацию для данной аудиокниги")

    def setup_connections(self):
        self.view.action_buttons["find_info"].clicked.connect(self.find_audiobook_info)
        self.view.action_buttons["add_favorite"].clicked.connect(lambda: None)
        self.view.action_buttons["mark_completed"].clicked.connect(lambda: None)
        self.view.action_buttons["delete"].clicked.connect(self.delete_audiobook)
        self.view.action_buttons["edit"].clicked.connect(self.edit_book)
        self.view.action_buttons["open_folder"].clicked.connect(self.open_audiobook_folder)