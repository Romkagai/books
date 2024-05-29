from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QScrollArea, QLabel, QComboBox
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

        # Добавление групп для различных дополнительных опций
        other_group = QGroupBox("Другие настройки")
        other_layout = QVBoxLayout(other_group)
        theme_label = QLabel("Выбор темы:")
        self.theme_combo_box = QComboBox()
        self.theme_combo_box.addItem("Темная тема")
        self.theme_combo_box.addItem("Светлая тема")
        other_layout.addWidget(theme_label)
        other_layout.addWidget(self.theme_combo_box)
        other_layout.addStretch()
        scroll_layout.addWidget(other_group)

        # Добавление скроллируемой области в основной layout
        self.layout.addWidget(scroll_area)

        # Кнопка сохранения
        self.saveSettingsButton = QPushButton("Сохранить настройки")
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
