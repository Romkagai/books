from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox

class EditBookDialog(QDialog):
    def __init__(self, parent, book_info):
        super().__init__(parent)
        self.inputs = None
        self.book_info = book_info
        self.field_map = {
            'название': 'title',
            'автор': 'author',
            'жанр': 'genre',
            'год': 'year',
            'чтец': 'narrator',
            'описание': 'description',
            'битрейт': 'bitrate',
            'длительность': 'duration',
            'размер': 'size',
            'путь': 'path',
            'дата добавления': 'date_added'
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.inputs = {}
        labels = ['Название', 'Автор', 'Жанр', 'Год', 'Чтец', 'Дата добавления', 'Описание']
        indices = {label.lower(): i+1 for i, label in enumerate(labels)}
        for label in labels:
            row = QHBoxLayout()
            lbl = QLabel(label + ":")
            le = QLineEdit(self)
            le.setText(str(self.book_info[indices[label.lower()]]))
            row.addWidget(lbl)
            row.addWidget(le)
            layout.addLayout(row)
            self.inputs[label.lower()] = le

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)  # Закрывает диалог без сохранения изменений

        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
        self.setLayout(layout)

        print(self.inputs)

    def save(self):
        try:
            for key, le in self.inputs.items():
                # Используем словарь сопоставления для получения английского названия поля
                field_name = self.field_map[key]
                print(field_name)
                self.book_info[field_name] = le.text()  # Записываем значение из QLineEdit
            self.accept()  # Закрывает диалог и возвращает статус успешного завершения
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")

