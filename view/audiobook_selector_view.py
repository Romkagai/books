from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox


class SelectBookDialog(QDialog):
    def __init__(self, parent, books):
        super().__init__(parent)
        self.books = books
        self.selected_book = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Выберите книгу")
        self.resize(700, 300)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget(self)
        for book in self.books:
            self.list_widget.addItem(f"{book['Автор']} - {book['Название']} ({book['Чтец']})")
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()

        select_button = QPushButton("Выбрать", self)
        select_button.clicked.connect(self.select)
        button_layout.addWidget(select_button)

        cancel_button = QPushButton("Отмена", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def select(self):
        selected_index = self.list_widget.currentRow()
        if selected_index >= 0:
            self.selected_book = self.books[selected_index]
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите книгу из списка")
