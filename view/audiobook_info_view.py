from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QLabel, QPushButton, QTableWidget, QHeaderView, QScrollArea, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy

class BookInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        # Отдельный макет для содержимого scroll_area
        content_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.setup_book_info_tab(content_layout)

        # Добавление scroll_area в основной макет
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def setup_book_info_tab(self, layout):
        self.setup_image_view(layout)
        self.setup_info_labels(layout)
        self.setup_action_buttons(layout)
        self.setup_file_table(layout)

        # Добавим пружину в конец layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

    def setup_image_view(self, layout):
        self.image_scene = QGraphicsScene()
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.setFixedSize(200, 200)  # Фиксированный размер для обложки
        self.image_view.setStyleSheet("background: transparent; border: none;")
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

        # Базовый стиль для кнопок
        button_base_style = """
            QPushButton {
                border: 2px solid #3e3e3e;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                background-color: #3e3e3e;
                color: #f0f0f0;
            }
            QPushButton:disabled {
                background-color: #5e5e5e;
                border: 2px solid #5e5e5e;
            }
            QPushButton:hover:!disabled {
                background-color: #4e4e4e;
            }
            QPushButton:pressed:!disabled {
                background-color: #2e2e2e;
            }
        """

        for button in self.action_buttons.values():
            button.setStyleSheet(button_base_style)
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