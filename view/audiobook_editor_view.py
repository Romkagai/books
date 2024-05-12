from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox

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
        row = QHBoxLayout()
        lbl = QLabel(f"{label}:")
        le = QLineEdit(self)
        le.setText(str(value))  # Устанавливаем начальное значение поля из book_info
        row.addWidget(lbl)
        row.addWidget(le)
        self.layout().addLayout(row)
        self.inputs[label] = le  # Используем человекочитаемый label как ключ

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
            for label, le in self.inputs.items():
                updated_info[label] = le.text()
            self.book_info.update(updated_info)  # Обновляем book_info новыми значениями
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")

