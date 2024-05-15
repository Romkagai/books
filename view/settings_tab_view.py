from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QScrollArea
from config import SORT_OPTIONS, COLUMN_OPTIONS, BOOK_INFO_OPTIONS


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Создание скроллируемой области
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_layout = QVBoxLayout(scroll_widget)

        # Добавление групп для настроек сортировки
        sorting_group = QGroupBox("Опции сортировки:")
        sorting_layout = QVBoxLayout(sorting_group)
        self.sort_checkboxes = {}
        self.add_sort_checkboxes(SORT_OPTIONS, sorting_layout)
        scroll_layout.addWidget(sorting_group)

        # Добавление групп для настроек отображения столбцов
        display_group = QGroupBox("Настройки отображения столбцов")
        display_layout = QVBoxLayout(display_group)
        self.table_display_checkboxes = {}
        self.add_table_display_checkboxes(COLUMN_OPTIONS, display_layout)
        scroll_layout.addWidget(display_group)

        # Добавление групп для настроек отображаемой информации о книге
        book_info_group = QGroupBox("Настройки информации о книге")
        book_info_layout = QVBoxLayout(book_info_group)
        self.book_info_checkboxes = {}
        self.add_book_info_checkboxes(BOOK_INFO_OPTIONS, book_info_layout)
        scroll_layout.addWidget(book_info_group)

        # Добавление скроллируемой области в основной layout
        self.layout.addWidget(scroll_area)

        # Кнопка сохранения
        self.saveSettingsButton = QPushButton("Сохранить настройки")
        self.saveSettingsButton.setStyleSheet("""
                    QPushButton {
                        border: 2px solid #3e3e3e;
                        border-radius: 10px;
                        padding: 5px;
                        font-size: 14px;
                        background-color: #2e2e2e;
                        color: #f0f0f0;
                    }
                    QPushButton:hover {
                        background-color: #3e3e3e;
                    }
                """)
        self.layout.addWidget(self.saveSettingsButton)

    def add_sort_checkboxes(self, options, layout):
        for option in options:
            checkbox = QCheckBox(option)
            layout.addWidget(checkbox)
            self.sort_checkboxes[option] = checkbox

    def add_table_display_checkboxes(self, options, layout):
        for option in options:
            checkbox = QCheckBox(option)
            layout.addWidget(checkbox)
            self.table_display_checkboxes[option] = checkbox

    def add_book_info_checkboxes(self, options, layout):
        for option in options:
            checkbox = QCheckBox(option)
            layout.addWidget(checkbox)
            self.book_info_checkboxes[option] = checkbox
