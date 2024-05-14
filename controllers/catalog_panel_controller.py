from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
from config import DATABASE_FIELD_MAP


class CatalogPanelController(QObject):
    # Сигналы для изоляции контроллеров
    book_selected = pyqtSignal(object, object)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self._current_sort_option = None
        self._sort_ascending = True
        self._last_selected_item = None
        self._current_display_options = None
        self.setup_connections()

    def setup_connections(self):
        """
        Настраивает сигналы и слоты для элементов управления.
        """
        self.view.add_button.clicked.connect(self.add_audiobook)
        self.view.audiobook_table.cellClicked.connect(self.new_item_clicked)
        self.view.sort_options.currentIndexChanged.connect(self.sort_changed)
        self.view.sort_direction_button.clicked.connect(self.toggle_sort_direction)
        self.view.search_panel.textChanged.connect(self.view.search_timer.start)
        self.view.search_timer.timeout.connect(self.do_search)

    def new_item_clicked(self, row):
        """
        Обрабатывает событие клика по элементу в таблице.
        """
        book_id = self.view.audiobook_table.item(row, 0).text()
        if self._last_selected_item != book_id:
            self._last_selected_item = book_id
            self.book_selected.emit(row, book_id)

    def update_sort_panel(self, options):
        """
        Обновляет панель сортировки.
        """
        self._current_sort_option = self.model.get_option_by_name(options[0])
        self.view.sort_options.blockSignals(True)
        self.view.sort_options.clear()
        self.view.sort_options.addItems(options)
        self.view.sort_options.blockSignals(False)

    def update_display_options(self, options):
        """
        Обновляет параметры отображения.
        """
        self._current_display_options = options
        self.update_audiobook_table()
        self.view.search_panel.clear()

    def do_search(self):
        """
        Выполняет поиск по тексту в панели поиска.
        """
        search_text = self.view.search_panel.text()
        self.update_audiobook_table(search_text=search_text)

    def toggle_sort_direction(self):
        """
        Переключает направление сортировки.
        """
        self._sort_ascending = not self._sort_ascending
        self.view.sort_direction_button.setText("⬆️" if self._sort_ascending else "⬇️")
        self.sort_changed()

    def sort_changed(self):
        """
        Обрабатывает изменение параметра сортировки.
        """
        current_text = self.view.sort_options.currentText()
        self._current_sort_option = self.model.get_option_by_name(current_text)
        self.update_audiobook_table()

    def update_audiobook_table(self, sort_by=None, ascending=None, search_text="", display_options=None):
        """
        Обновляет таблицу аудиокниг.
        """
        sort_by = sort_by or self._current_sort_option
        ascending = ascending if ascending is not None else self._sort_ascending
        display_options = display_options or self._current_display_options

        records = self.model.get_audiobooks_list(sort_by, ascending, search_text, display_options)

        self.view.audiobook_table.setColumnCount(len(display_options) + 3)  # Добавляем два столбца для эмодзи
        self.view.audiobook_table.setHorizontalHeaderLabels(['ID'] + display_options + ['⭐', '🎧'])
        self.view.audiobook_table.setRowCount(len(records))

        header = self.view.audiobook_table.horizontalHeader()
        for col in range(len(display_options) + 3):
            if col < len(display_options) + 1:
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
                self.view.audiobook_table.setColumnWidth(col, 50)

        for row_idx, record in enumerate(records):
            book_id, is_favorite, is_completed, *data = record
            for col_idx, field in enumerate([book_id] + data):
                item = QTableWidgetItem(str(field))
                self.view.audiobook_table.setItem(row_idx, col_idx, item)

            # Установка эмодзи для состояния книги
            favorite_item = QTableWidgetItem('✔️' if is_favorite else '❌')
            completed_item = QTableWidgetItem('✔️' if is_completed else '❌')
            favorite_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            completed_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view.audiobook_table.setItem(row_idx, len(display_options) + 1, favorite_item)
            self.view.audiobook_table.setItem(row_idx, len(display_options) + 2, completed_item)

        # Скрываем столбец с book_id
        self.view.audiobook_table.setColumnHidden(0, True)

    def add_audiobook(self):
        """
        Обрабатывает добавление новой аудиокниги.
        """
        choice = self.prompt_audiobook_choice()
        if choice == 0:  # Выбран файл
            self.add_file()
        elif choice == 1:  # Выбрана директория
            self.add_directory()

    @staticmethod
    def prompt_audiobook_choice():
        """
        Показывает диалоговое окно для выбора типа добавляемой аудиокниги.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Добавление аудиокниги")
        msg_box.setText("Выберите, что хотите добавить:")
        msg_box.addButton("Файл", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Папку", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        return msg_box.exec()

    def add_file(self):
        """
        Добавляет аудиофайл в базу данных.
        """
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Выберите аудиофайл", "", "Audio Files (*.mp3 *.aac *.wav)")
        if file_path:
            if not self.model.audiobook_exists(file_path):
                self.model.import_audiobook(file_path)
                book_id = self.model.get_book_id(file_path)
                self.model.import_file(file_path, book_id)
                self.update_audiobook_table()
            else:
                QMessageBox.information(self.view, "Внимание!", "Данная аудиокнига уже есть в библиотеке")

    def add_directory(self):
        """
        Добавляет директорию с аудиофайлами в базу данных.
        """
        directory = QFileDialog.getExistingDirectory(self.view, "Выберите папку с аудиофайлами")
        if directory:
            if not self.model.audiobook_exists(directory):
                files_to_add = self.model.get_audio_files(directory)
                if files_to_add:
                    self.model.import_audiobook(files_to_add[0], directory)
                    book_id = self.model.get_book_id(directory)
                    for file_path in files_to_add:
                        self.model.import_file(file_path, book_id)
                    self.update_audiobook_table()
            else:
                QMessageBox.information(self.view, "Внимание!", "Данная аудиокнига уже есть в библиотеке")
