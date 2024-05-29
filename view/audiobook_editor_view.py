from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont


class EditBookDialog(QDialog):
    def __init__(self, parent, book_info):
        super().__init__(parent)
        self.inputs = {}
        self.book_info = book_info
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Редактирование книги")
        self.resize(400, 300)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.create_input_fields(main_layout)
        self.create_action_buttons(main_layout)

    def create_input_fields(self, layout):
        for label, value in self.book_info.items():
            self.add_input_field(layout, label, value)

    def add_input_field(self, layout, label, value):
        row = QHBoxLayout()
        lbl = QLabel(f"{label}:")
        le = QLineEdit(self)
        le.setText(str(value))  # Устанавливаем начальное значение поля из book_info
        row.addWidget(lbl)
        row.addWidget(le)
        layout.addLayout(row)
        self.inputs[label] = le  # Используем человекочитаемый label как ключ

    def create_action_buttons(self, layout):
        button_layout = QHBoxLayout()

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def save(self):
        try:
            updated_info = {label: le.text() for label, le in self.inputs.items()}
            self.book_info.update(updated_info)  # Обновляем book_info новыми значениями
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
