from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox
from config import DATABASE_FIELD_MAP


class EditBookDialog(QDialog):
    def __init__(self, parent, book_info):
        super().__init__(parent)
        self.inputs = {}
        self.book_info = book_info
        self.init_ui()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.setWindowTitle("Редактирование книги")
        self.create_input_fields()
        self.create_action_buttons()

    def create_input_fields(self):
        labels = ['Название', 'Автор', 'Жанр', 'Год', 'Чтец', 'Дата добавления', 'Описание', 'Битрейт']
        for label in labels:
            self.add_input_field(label)

    def add_input_field(self, label):
        key = DATABASE_FIELD_MAP[label.lower()]
        row = QHBoxLayout()
        lbl = QLabel(f"{label}:")
        le = QLineEdit(self)
        le.setText(str(self.book_info.get(key, "")))
        row.addWidget(lbl)
        row.addWidget(le)
        self.layout().addLayout(row)
        self.inputs[label.lower()] = le

    def create_action_buttons(self):
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)

        self.layout().addWidget(save_button)
        self.layout().addWidget(cancel_button)

    def save(self):
        try:
            for key, le in self.inputs.items():
                field_name = DATABASE_FIELD_MAP[key]
                self.book_info[field_name] = le.text()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
