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
        for label, value in self.book_info.items():
            self.add_input_field(label, value)

    def add_input_field(self, label, value):
        # Преобразование пользовательского ключа к ключу в базе данных
        key = DATABASE_FIELD_MAP.get(label.lower(), label.lower())  # используем в качестве ключа оригинальный ключ, если он отсутствует в карте
        row = QHBoxLayout()
        lbl = QLabel(f"{label}:")
        le = QLineEdit(self)
        le.setText(str(value))  # значение из словаря напрямую, предполагается что оно уже правильное
        row.addWidget(lbl)
        row.addWidget(le)
        self.layout().addLayout(row)
        self.inputs[key] = le

    def create_action_buttons(self):
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)

        self.layout().addWidget(save_button)
        self.layout().addWidget(cancel_button)

    def save(self):
        try:
            updated_info = {}
            for key, le in self.inputs.items():
                updated_info[DATABASE_FIELD_MAP.get(key, key)] = le.text()
            self.book_info = updated_info
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
