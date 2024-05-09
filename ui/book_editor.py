from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox
from config import BOOK_INFO_EDITOR_FIELD_MAP as field_map

class EditBookDialog(QDialog):
    def __init__(self, parent, book_info):
        super().__init__(parent)
        self.inputs = None
        self.book_info = book_info
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.inputs = {}
        labels = ['Название', 'Автор', 'Жанр', 'Год', 'Чтец', 'Дата добавления', 'Описание']
        for label in labels:
            key = field_map[label.lower()]  # Получаем ключ словаря из русского названия
            row = QHBoxLayout()
            lbl = QLabel(label + ":")
            le = QLineEdit(self)
            le.setText(str(self.book_info.get(key, "")))  # Используем метод get для безопасного доступа к словарю
            row.addWidget(lbl)
            row.addWidget(le)
            layout.addLayout(row)
            self.inputs[label.lower()] = le  # Сохраняем QLineEdit, используя русское название как ключ

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)  # Закрывает диалог без сохранения изменений

        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
        self.setLayout(layout)

    def save(self):
        try:
            for key, le in self.inputs.items():
                field_name = field_map[key]  # Получаем английское название поля из русского названия
                self.book_info[field_name] = le.text()  # Обновляем значение в словаре
            self.accept()  # Закрывает диалог и возвращает статус успешного завершения
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")


