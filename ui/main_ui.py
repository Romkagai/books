from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QComboBox, QTableWidget, QLabel,
                             QHeaderView, QGraphicsView, QGraphicsScene)

from controllers.audiobook_handler import AudiobookCataloguerLogic


class AudiobookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupModel()
        self.setupUI()
        self.setupConnections()

    def setupModel(self):
        self.model = AudiobookCataloguerLogic(self)

    def setupUI(self):
        self.createMainLayout()
        self.setupLeftPanel()
        self.setupRightPanel()
        self.setWindowTitle("Каталогизатор аудиокниг")

    def createMainLayout(self):
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

    def setupLeftPanel(self):
        leftLayout = QVBoxLayout()
        self.setupSearchPanel(leftLayout)
        self.setupSortingControls(leftLayout)
        self.setupAudiobookTable(leftLayout)
        self.mainLayout.addLayout(leftLayout, 1)

    def setupRightPanel(self):
        rightLayout = QVBoxLayout()
        self.setupImageView(rightLayout)
        self.setupInfoLabels(rightLayout)

        self.setupActionButtons(rightLayout)
        self.mainLayout.addLayout(rightLayout, 1)
        self.setupFileTable(rightLayout)

    def setupConnections(self):
        self.addButton.clicked.connect(self.model.add_audiobook)
        self.audiobookTable.cellClicked.connect(self.model.display_audiobook_info)
        self.findBookInfoButton.clicked.connect(self.model.do_nothing)
        self.deleteButton.clicked.connect(self.model.delete_audiobook)
        self.addFavoriteButton.clicked.connect(self.model.do_nothing)
        self.addCompletedButton.clicked.connect(self.model.do_nothing)
        self.editButton.clicked.connect(self.model.edit_book)
        self.model.update_audiobook_table()

    def setupSearchPanel(self, layout):
        searchPanel = QLineEdit()
        layout.addWidget(searchPanel)

    def setupFileTable(self, layout):
        self.fileTable = QTableWidget()
        self.fileTable.setColumnCount(2)  # Файл, Проигран
        self.fileTable.setHorizontalHeaderLabels(["Файл", "Проигран"])
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fileTable.setVisible(False)  # Скрываем таблицу до нужного момента
        layout.addWidget(self.fileTable)

    def setupSortingControls(self, layout):
        sortLabel = QLabel("Сортировать по:")
        sortOptions = QComboBox()
        sortOptions.addItems(["Название", "Автор", "Битрейт"])
        sortDirectionButton = QPushButton("⬆️⬇️")

        sortLayout = QHBoxLayout()
        sortLayout.addWidget(sortLabel)
        sortLayout.addWidget(sortOptions)
        sortLayout.addWidget(sortDirectionButton)
        layout.addLayout(sortLayout)

        self.addButton = QPushButton("Добавить аудиокнигу")
        layout.addWidget(self.addButton)

    def setupAudiobookTable(self, layout):
        self.audiobookTable = QTableWidget()
        self.audiobookTable.setColumnCount(3)
        self.audiobookTable.setHorizontalHeaderLabels(["ID", "Автор", "Название"])
        self.audiobookTable.verticalHeader().setVisible(False)
        self.audiobookTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.audiobookTable)

    def setupImageView(self, layout):
        self.imageScene = QGraphicsScene()
        self.imageView = QGraphicsView(self.imageScene)
        self.imageView.setFixedHeight(200)
        self.imageView.setFixedWidth(200)
        layout.addWidget(self.imageView)

    def setupInfoLabels(self, layout):
        infoLayout = QVBoxLayout()
        labels = ["Название", "Автор", "Жанр", "Год", "Чтец", "Дата добавления", "Описание"]
        self.infoLabels = [QLabel(label) for label in labels]
        max_label_width = 200
        for label in self.infoLabels:
            label.setWordWrap(True)
            label.setMaximumWidth(max_label_width)
            infoLayout.addWidget(label)
        layout.addLayout(infoLayout)

    def setupActionButtons(self, layout):
        self.actionButtons = [QPushButton("Найти информацию в интернете"),
                              QPushButton("Удалить"),
                              QPushButton("Добавить в избранное"),
                              QPushButton("Пометить как завершенное"),
                              QPushButton("Редактировать")]
        for button in self.actionButtons:
            layout.addWidget(button)
            button.setEnabled(False)

        self.findBookInfoButton = self.actionButtons[0]
        self.deleteButton = self.actionButtons[1]
        self.addFavoriteButton = self.actionButtons[2]
        self.addCompletedButton = self.actionButtons[3]
        self.editButton = self.actionButtons[4]
