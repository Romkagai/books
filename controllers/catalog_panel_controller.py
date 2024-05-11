from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
from config import DATABASE_FIELD_MAP


class CatalogPanelController(QObject):
    # Сигналы для изоляции контроллеров
    book_selected = pyqtSignal(object, object)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.setup_connections()
        # Текущая опция сортировки
        self.current_sort_option = None
        self.sortAscending = True
        # Текущая книга
        self.last_selected_item = None
        # Текущие опции отображения колонок
        self.current_display_options = None

    def new_item_clicked(self, row):
        book_id = self.view.audiobookTable.item(row, 0).text()
        if self.last_selected_item != book_id:
            self.last_selected_item = self.view.audiobookTable.item(row, 0).text()
            self.book_selected.emit(row, book_id)

    def update_sort_panel(self, options):
        self.current_sort_option = self.model.get_option_by_name(options[0])
        self.view.sortOptions.blockSignals(True)
        self.view.sortOptions.clear()
        self.view.sortOptions.addItems(options)
        self.view.sortOptions.blockSignals(False)

    def update_display_options(self, options):
        self.current_display_options = options
        self.update_audiobook_table()
        self.view.searchPanel.clear()

    def do_search(self):
        search_text = self.view.searchPanel.text()
        self.update_audiobook_table(self.current_sort_option, self.sortAscending, search_text)

    def toggle_sort_direction(self):
        self.sortAscending = not self.sortAscending
        if self.sortAscending:
            self.view.sortDirectionButton.setText("⬆️")
        else:
            self.view.sortDirectionButton.setText("⬇️")
        self.sort_changed()

    def sort_changed(self):
        currentText = self.view.sortOptions.currentText()
        self.current_sort_option = self.model.get_option_by_name(currentText)
        self.update_audiobook_table(self.current_sort_option, self.sortAscending)

    def update_audiobook_table(self, sort_by=None, ascending=None, search_text="", display_options=None):
        if display_options is None:
            display_options = self.current_display_options
        if sort_by is None:
            sort_by = self.current_sort_option
        if ascending is None:
            ascending = self.sortAscending

        records = self.model.get_audiobooks_list(sort_by, ascending, search_text, display_options)

        self.view.audiobookTable.setColumnCount(len(display_options) + 1)
        self.view.audiobookTable.setHorizontalHeaderLabels(['ID'] + display_options)
        self.view.audiobookTable.setRowCount(len(records))

        # header = self.view.audiobookTable.horizontalHeader()
        # for col in range(len(display_options)):
        #     header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        for row_idx, record in enumerate(records):
            for col_idx, field in enumerate(record):
                self.view.audiobookTable.setItem(row_idx, col_idx, QTableWidgetItem(str(field)))

        # Скрываем столбец с book_id
        self.view.audiobookTable.setColumnHidden(0, True)

    def add_audiobook(self):
        choice = self.prompt_audiobook_choice()
        if choice == 0:  # Выбран файл
            self.add_file()
        elif choice == 1:  # Выбрана директория
            self.add_directory()

    @staticmethod
    def prompt_audiobook_choice():
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Добавление аудиокниги")
        msg_box.setText("Выберите, что хотите добавить:")
        msg_box.addButton("Файл", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Папку", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        return msg_box.exec()

    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Выберите аудиофайл", "",
                                                   "Audio Files (*.mp3 *.aac *.wav)")
        if file_path:
            if not self.model.audiobook_exists(file_path):
                self.model.import_audiobook(file_path, directory=None)
                book_id = self.model.get_book_id(file_path)
                self.model.import_file(file_path, book_id)
                self.update_audiobook_table(self.current_sort_option)
            else:
                QMessageBox.information(self.view, "Внимание!", "Данная аудиокнига уже есть библиотеке")

    def add_directory(self):
        directory = QFileDialog.getExistingDirectory(self.view, "Выберите папку с аудиофайлами")
        if directory:
            if not self.model.audiobook_exists(directory):
                files_to_add = self.model.get_audio_files(directory)
                print(files_to_add)
                if files_to_add:
                    self.model.import_audiobook(files_to_add[0], directory)
                    book_id = self.model.get_book_id(directory)
                    for file_path in files_to_add:
                        self.model.import_file(file_path, book_id)
                        self.update_audiobook_table(self.current_sort_option)
            else:
                QMessageBox.information(self.view, "Внимание!", "Данная аудиокнига уже есть библиотеке")

    def setup_connections(self):
        self.view.addButton.clicked.connect(self.add_audiobook)
        self.view.audiobookTable.cellClicked.connect(self.new_item_clicked)
        self.view.sortOptions.currentIndexChanged.connect(self.sort_changed)
        self.view.sortDirectionButton.clicked.connect(self.toggle_sort_direction)
        self.view.searchPanel.textChanged.connect(self.view.searchTimer.start)
        self.view.searchTimer.timeout.connect(self.do_search)
