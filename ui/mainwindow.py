import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
                             QGridLayout, QGraphicsView, QGraphicsScene, QLabel, QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from controllers.audiobook_manager import AudiobookManager


class AudiobookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        self.audiobook_manager = AudiobookManager(self)
        self.initUI()

    def initUI(self):
        # Главный layout
        mainLayout = QHBoxLayout()

        # Левая часть
        leftLayout = QVBoxLayout()
        searchPanel = QLineEdit()
        leftLayout.addWidget(searchPanel)

        # Элементы сортировки
        sortLabel = QLabel("Сортировать по:")
        sortOptions = QComboBox()
        sortOptions.addItems(["Название", "Автор", "Битрейт"])
        sortDirectionButton = QPushButton("⬆️⬇️")

        # Расположение элементов сортировки в горизонтальном layout
        sortLayout = QHBoxLayout()
        sortLayout.addWidget(sortLabel)
        sortLayout.addWidget(sortOptions)
        sortLayout.addWidget(sortDirectionButton)
        leftLayout.addLayout(sortLayout)

        addButton = QPushButton("Добавить аудиокнигу")
        self.audiobookTable = QTableWidget()
        self.audiobookTable.setColumnCount(3)  # ID, Автор, Название
        self.audiobookTable.setHorizontalHeaderLabels(["ID", "Автор", "Название"])
        self.audiobookTable.verticalHeader().setVisible(False)
        self.audiobookTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        leftLayout.addWidget(addButton)
        leftLayout.addWidget(self.audiobookTable)

        # Правая часть
        rightLayout = QVBoxLayout()
        self.imageScene = QGraphicsScene()
        self.imageView = QGraphicsView(self.imageScene)
        self.imageView.setFixedHeight(200)
        self.imageView.setFixedWidth(200)

        # Таблица файлов, изначально скрыта
        self.fileTable = QTableWidget()
        self.fileTable.setColumnCount(2)  # Файл, Проигран
        self.fileTable.setHorizontalHeaderLabels(["Файл", "Проигран"])
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fileTable.setVisible(False)  # Скрываем таблицу до нужного момента

        infoLayout = QGridLayout()
        labels = ["Название", "Автор", "Жанр", "Год", "Чтец", "Дата добавления"]
        self.infoLabels = [QLabel(label) for label in labels]
        for i, label in enumerate(self.infoLabels):
            infoLayout.addWidget(label, i, 0)

        actionButtons = [QPushButton("Найти информацию в интернете"),
                         QPushButton("Удалить"),
                         QPushButton("Добавить в избранное"),
                         QPushButton("Пометить как завершенное")]

        rightLayout.addWidget(self.imageView)
        rightLayout.addLayout(infoLayout)
        for button in actionButtons:
            rightLayout.addWidget(button)

        # Добавление левой и правой части в главный layout
        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addLayout(rightLayout, 1)
        mainLayout.addWidget(self.fileTable)
        self.setLayout(mainLayout)
        self.setWindowTitle("Каталогизатор аудиокниг")

        # Установка соединений
        addButton.clicked.connect(self.add_audiobook)
        self.audiobookTable.cellClicked.connect(self.display_audiobook_info)

        # Обновление таблицы при запуске
        self.update_audiobook_table()

    def add_audiobook(self):
        # Диалоговое окно с выбором добавления файла или папки
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Добавление аудиокниги")
        msg_box.setText("Выберите, что хотите добавить:")
        msg_box.addButton("Файл", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Папку", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        choice = msg_box.exec()

        print(choice)

        if choice == 0:  # Выбор файла
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "",
                                                       "Audio Files (*.mp3 *.aac *.wav)")
            if file_path:
                self.audiobook_manager.import_audiobook(file_path, directory=None)
                book_id = self.audiobook_manager.get_book_id(file_path)
                self.audiobook_manager.import_file(file_path, book_id)
                self.update_audiobook_table()

        elif choice == 1:  # Выбор папки
            directory = QFileDialog.getExistingDirectory(self, "Выберите папку с аудиофайлами")
            if directory:
                # Получаем список всех подходящих аудиофайлов в папке
                files_to_add = [os.path.join(directory, f) for f in os.listdir(directory)
                                if f.endswith(('.mp3', '.aac', '.wav', '.ogg')) and os.path.isfile(
                        os.path.join(directory, f))]

                if files_to_add:
                    print("Найдены файлы:", files_to_add)
                    self.audiobook_manager.import_audiobook(files_to_add[0], directory)
                    book_id = self.audiobook_manager.get_book_id(directory)
                    for file_path in files_to_add:
                        self.audiobook_manager.import_file(file_path, book_id)
                        self.update_audiobook_table()

    def update_audiobook_table(self):
        records = self.audiobook_manager.get_audiobooks_list()
        self.audiobookTable.setRowCount(len(records))  # Обновление количества строк

        print(records)

        for index, (book_id, author, title) in enumerate(records):
            self.audiobookTable.setItem(index, 0, QTableWidgetItem(str(book_id)))
            self.audiobookTable.setItem(index, 1, QTableWidgetItem(author))
            self.audiobookTable.setItem(index, 2, QTableWidgetItem(title))

    def display_audiobook_info(self, row):
        book_id = self.audiobookTable.item(row, 0).text()
        book_info = self.audiobook_manager.get_book_info_by_id(book_id)
        self.infoLabels[0].setText(f"Название: {book_info[1]}")  # Обновление лейблов
        self.infoLabels[1].setText(f"Автор: {book_info[2]}")
        self.infoLabels[2].setText(f"Жанр: {book_info[3]}")
        self.infoLabels[3].setText(f"Год: {book_info[4]}")
        self.infoLabels[4].setText(f"Чтец: {book_info[5]}")
        self.infoLabels[5].setText(f"Дата добавления: {book_info[6]}")

        if os.path.isdir(book_info[13]):
            self.fileTable.setVisible(True)
            self.update_file_table(book_id)
        else:
            self.fileTable.setVisible(False)

        self.update_cover(book_id)

    def update_file_table(self, book_id):
        files = self.audiobook_manager.get_audiobook_files(book_id)
        print(files)
        self.fileTable.setRowCount(len(files))  # Установка количества строк
        for index, (file_path, is_listened) in enumerate(files):
            self.fileTable.setItem(index, 0, QTableWidgetItem(file_path))
            self.fileTable.setItem(index, 1, QTableWidgetItem("Да" if is_listened else "Нет"))

    def update_cover(self, book_id):
        try:
            cover_data = self.audiobook_manager.find_audiobook_cover(book_id)
            if cover_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(cover_data):
                    self.imageScene.clear()  # Очистка предыдущих изображений
                    self.imageScene.addPixmap(pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    self.imageScene.addText("Ошибка загрузки изображения")
        except:
            self.imageScene.clear()
            self.imageScene.addText("Обложка не найдена")
