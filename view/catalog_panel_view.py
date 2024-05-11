from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, \
    QHeaderView
from PyQt6.QtCore import QTimer


class CatalogPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()


    def setupUI(self):
        layout = QVBoxLayout()
        self.setupSearchPanel(layout)
        self.setupSortingControls(layout)
        self.setupAudiobookTable(layout)
        self.setLayout(layout)

    def setupSearchPanel(self, layout):
        self.searchPanel = QLineEdit()
        self.searchPanel.setPlaceholderText("Введите текст для поиска...")

        # Динамический поиск
        self.searchTimer = QTimer()
        self.searchTimer.setInterval(300)
        self.searchTimer.setSingleShot(True)

        layout.addWidget(self.searchPanel)

    def setupSortingControls(self, layout):
        sortLabel = QLabel("Сортировать по:")
        self.sortOptions = QComboBox()
        self.sortDirectionButton = QPushButton("⬆️")

        sortLayout = QHBoxLayout()
        sortLayout.addWidget(sortLabel)
        sortLayout.addWidget(self.sortOptions)
        sortLayout.addWidget(self.sortDirectionButton)
        layout.addLayout(sortLayout)

        self.addButton = QPushButton("Добавить аудиокнигу")
        layout.addWidget(self.addButton)

    def setupAudiobookTable(self, layout):
        self.audiobookTable = QTableWidget()
        self.audiobookTable.verticalHeader().setVisible(False)

        header = self.audiobookTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Отключение редактирования
        self.audiobookTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.audiobookTable)
