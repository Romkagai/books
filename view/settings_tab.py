from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QComboBox, QLineEdit


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setup_settings_tab(layout)

    def setup_settings_tab(self, layout):
        # Чекбоксы для отображения/скрытия столбцов
        # self.columnCheckboxes = {name: QCheckBox(name) for name in ["ID", "Автор", "Название"]}
        # for name, checkbox in self.columnCheckboxes.items():
        #     checkbox.setChecked(True)
        #     checkbox.stateChanged.connect(self.toggleColumnVisibility)
        #     layout.addWidget(checkbox)

        # Сортировка
        sortLabel = QLabel("Сортировать по:")
        self.sortOptions = QComboBox()
        self.sortOptions.addItems(["ID", "Автор", "Название"])
        layout.addWidget(sortLabel)
        layout.addWidget(self.sortOptions)

        # Фильтрация
        filterLabel = QLabel("Фильтр:")
        self.filterOptions = QLineEdit()
        layout.addWidget(filterLabel)
        layout.addWidget(self.filterOptions)

    # def toggleColumnVisibility(self):
    #     columns = ["ID", "Автор", "Название"]
    #     for i, name in enumerate(columns):
    #         self.audiobookTable.setColumnHidden(i, not self.columnCheckboxes[name].isChecked())