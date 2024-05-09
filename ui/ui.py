import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
                             QGridLayout, QGraphicsView, QGraphicsScene, QLabel, QHeaderView, QFileDialog, QMessageBox)

from controllers.audiobook_controller import AudiobookCataloguerLogic


class AudiobookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        # Атрибуты сущности
        # Модель приложения
        self.model = AudiobookCataloguerLogic(self)
        # Изменяемые параметры приложения
        self.audiobookTable = QTableWidget()
        self.imageScene = QGraphicsScene()
        self.imageView = QGraphicsView(self.imageScene)
        self.fileTable = QTableWidget()
        self.infoLabels = None
        self.addFavoriteButton = None
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
        self.audiobookTable.setColumnCount(3)  # ID, Автор, Название
        self.audiobookTable.setHorizontalHeaderLabels(["ID", "Автор", "Название"])
        self.audiobookTable.verticalHeader().setVisible(False)
        self.audiobookTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        leftLayout.addWidget(addButton)
        leftLayout.addWidget(self.audiobookTable)

        # Правая часть
        rightLayout = QVBoxLayout()
        self.imageView.setFixedHeight(200)
        self.imageView.setFixedWidth(200)

        # Таблица файлов, изначально скрыта
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
        # Кнопка "Добавить аудиокнигу"
        addButton.clicked.connect(self.model.add_audiobook)

        # Вывод информации об аудиокниге при нажатии на ячейку таблицы
        self.audiobookTable.cellClicked.connect(self.model.display_audiobook_info)

        # Кнопка "Удалить аудиокнигу"
        deleteButton = actionButtons[1]
        deleteButton.clicked.connect(self.model.delete_audiobook)

        # Кнопка "Добавить в избранное"
        self.addFavoriteButton = actionButtons[2]
        self.addFavoriteButton.clicked.connect(self.model.do_nothing)

        # Кнопка "Пометить как завершенное"
        # finishButton = actionButtons[3]
        # finishButton.clicked.connect(self.model.mark_audiobook_as_finished)

        # Обновление таблицы при запуске
        self.model.update_audiobook_table()

