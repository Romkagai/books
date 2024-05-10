from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QLabel, QPushButton, QTableWidget, \
    QHeaderView


class BookInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        self.setup_book_info_tab(layout)
        self.setLayout(layout)

    def setup_book_info_tab(self, layout):
        self.setupImageView(layout)
        self.setupInfoLabels(layout)
        self.setupActionButtons(layout)
        self.setupFileTable(layout)

    def setupImageView(self, layout):
        self.imageScene = QGraphicsScene()
        self.imageView = QGraphicsView(self.imageScene)
        self.imageView.setFixedHeight(200)
        self.imageView.setFixedWidth(200)
        layout.addWidget(self.imageView)

    # Настройка лэйблов (информации о книге)
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

    # Настройка кнопок
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

    # Настройка таблицы с файлами (файлы аудиокниги)
    def setupFileTable(self, layout):
        self.fileTable = QTableWidget()
        self.fileTable.setColumnCount(2)  # Файл, Проигран
        self.fileTable.setHorizontalHeaderLabels(["Файл", "Проигран"])
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fileTable.setVisible(False)  # Скрываем таблицу до нужного момента
        layout.addWidget(self.fileTable)