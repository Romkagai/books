import json

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QComboBox, QLineEdit, QListWidget, QPushButton, \
    QAbstractItemView, QMessageBox
from config import SORT_OPTIONS
from controllers.settings_handler import SettingsHandler


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.handler = SettingsHandler(self)
        self.setup_settings_tab(self.layout)

    def setup_settings_tab(self, layout):
        # Лейбл - название настройки
        label = QLabel("Настройки сортировки")
        self.layout.addWidget(label)
        # Список для выбора параметров сортировки
        self.create_sort_options(SORT_OPTIONS)

        # Кнопка для сохранения настроек
        self.saveSettingsButton = QPushButton("Сохранить настройки")
        self.saveSettingsButton.clicked.connect(lambda: self.handler.save_sorting_settings(self.checkboxes))
        self.layout.addWidget(self.saveSettingsButton)

    def create_sort_options(self, options):
        self.checkboxes = {}
        for option in options:
            checkbox = QCheckBox(option)
            self.layout.addWidget(checkbox)
            self.checkboxes[option] = checkbox

        self.handler.apply_sorting_settings(self.checkboxes)
