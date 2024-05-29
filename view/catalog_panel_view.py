from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, \
    QHeaderView, QSizePolicy
from PyQt6.QtCore import QTimer


class CatalogPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса для панели каталога.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.setup_searching_button(layout)
        self.setup_sorting_controls(layout)
        self.setup_search_panel(layout)
        self.setup_audiobook_table(layout)

        self.setLayout(layout)

    def setup_search_panel(self, layout):
        """
        Настройка панели поиска.
        """
        self.search_panel = QLineEdit()
        self.search_panel.setPlaceholderText("Введите текст для поиска...")

        # Динамический поиск
        self.search_timer = QTimer()
        self.search_timer.setInterval(300)
        self.search_timer.setSingleShot(True)

        layout.addWidget(self.search_panel)

    def setup_sorting_controls(self, layout):
        """
        Настройка элементов управления сортировкой.
        """
        sort_label = QLabel("Сортировать по:")
        self.sort_options = QComboBox()
        self.sort_direction_button = QPushButton("⬆️")

        sort_layout = QHBoxLayout()
        sort_layout.setContentsMargins(0, 0, 0, 0)
        sort_layout.setSpacing(5)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_options)
        sort_layout.addWidget(self.sort_direction_button)
        layout.addLayout(sort_layout)

    def setup_searching_button(self, layout):
        """
        Настройка кнопки добавления аудиокниги.
        """

        self.add_button = QPushButton("Добавить аудиокнигу")
        # Установка стиля для кнопки
        self.add_button.setObjectName("addButton")

        layout.addWidget(self.add_button)

    def setup_audiobook_table(self, layout):
        """
        Настройка таблицы для отображения аудиокниг.
        """
        self.audiobook_table = QTableWidget()
        self.audiobook_table.verticalHeader().setVisible(False)

        header = self.audiobook_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Отключение редактирования
        self.audiobook_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.audiobook_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.audiobook_table)
