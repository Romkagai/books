from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, \
    QHeaderView
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

        # Установка стиля для строки поиска
        self.search_panel.setStyleSheet("""
            QLineEdit {
                border: 2px solid #3e3e3e;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #3e3e3e;
                color: #f0f0f0;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;
                background-color: #2e2e2e;
            }
        """)

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

        # Установка стилей для панели сортировки
        sort_label.setStyleSheet("color: #f0f0f0; font-size: 14px;")
        self.sort_options.setStyleSheet("""
            QComboBox {
                border: 2px solid #3e3e3e;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
        """)
        self.sort_direction_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #3e3e3e;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
        """)

        sort_layout = QHBoxLayout()
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
        self.add_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #0078d7;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                background-color: #0078d7;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)

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

        layout.addWidget(self.audiobook_table)
