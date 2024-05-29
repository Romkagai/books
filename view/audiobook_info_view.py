from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QLabel, QPushButton, QTableWidget, QHeaderView, QScrollArea, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QSplitter

class BookInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Разделитель для распределения пространства
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Vertical)

        # Область прокрутки для информации о книге
        self.book_info_scroll_area = QScrollArea()
        self.book_info_scroll_area_widget_contents = QWidget()
        self.book_info_scroll_area.setWidgetResizable(True)
        self.book_info_scroll_area.setWidget(self.book_info_scroll_area_widget_contents)

        book_info_layout = QVBoxLayout(self.book_info_scroll_area_widget_contents)
        self.setup_book_info_tab(book_info_layout)

        # Область прокрутки для кнопок и таблицы файлов
        self.action_scroll_area = QScrollArea()
        self.action_scroll_area_widget_contents = QWidget()
        self.action_scroll_area.setWidgetResizable(True)
        self.action_scroll_area.setWidget(self.action_scroll_area_widget_contents)

        action_layout = QVBoxLayout(self.action_scroll_area_widget_contents)
        self.setup_action_buttons(action_layout)
        self.setup_file_table(action_layout)

        # Добавление областей прокрутки в разделитель
        splitter.addWidget(self.book_info_scroll_area)
        splitter.addWidget(self.action_scroll_area)

        # Установка начальных размеров областей
        splitter.setStretchFactor(0, 7)  # 70% для информации о книге
        splitter.setStretchFactor(1, 3)  # 30% для кнопок и таблицы файлов

        # Добавление разделителя в основной макет
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def setup_book_info_tab(self, layout):
        self.setup_image_view(layout)
        self.setup_info_labels(layout)

        # Добавим пружину в конец layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

    def setup_image_view(self, layout):
        self.image_scene = QGraphicsScene()
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.setFixedSize(200, 200)  # Фиксированный размер для обложки
        self.image_view.setObjectName("imageView")
        image_layout = QHBoxLayout()
        image_layout.addStretch()
        image_layout.addWidget(self.image_view)
        image_layout.addStretch()
        layout.addLayout(image_layout)

    def setup_info_labels(self, layout):
        self.info_labels = {}
        self.info_labels_layout = QGridLayout()

        # Создаем горизонтальный макет для обложки и лейблов
        info_layout = QVBoxLayout()
        info_layout.addLayout(self.info_labels_layout)
        layout.addLayout(info_layout)

    def setup_action_buttons(self, layout):
        self.action_buttons = {
            "find_info": QPushButton("Найти информацию в интернете"),
            "delete": QPushButton("Удалить"),
            "add_favorite": QPushButton("Добавить в избранное"),
            "mark_completed": QPushButton("Пометить как завершенное"),
            "edit": QPushButton("Редактировать"),
            "open_folder": QPushButton("Открыть папку с аудиокнигой")
        }

        for button in self.action_buttons.values():
            button.setObjectName("infoButton")
            layout.addWidget(button)
            button.setEnabled(False)

    def setup_file_table(self, layout):
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(2)  # Файл, Проигран
        self.file_table.setHorizontalHeaderLabels(["Файл", "Проигран"])
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.file_table.setVisible(False)  # Скрываем таблицу до нужного момента
        layout.addWidget(self.file_table)
