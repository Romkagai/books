from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton

from config import SORT_OPTIONS, COLUMN_OPTIONS


class SettingsTab(QWidget):
    # Определяем сигналы


    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_settings_tab()

    def setup_settings_tab(self):
        sort_label = QLabel("Опции сортировки:")
        self.layout.addWidget(sort_label)
        self.create_sort_options()

        self.saveSettingsButton = QPushButton("Сохранить настройки")
        self.layout.addWidget(self.saveSettingsButton)

    def create_sort_options(self):
        self.sort_checkboxes = {}
        for option in SORT_OPTIONS:
            checkbox = QCheckBox(option)
            self.layout.addWidget(checkbox)
            self.sort_checkboxes[option] = checkbox


