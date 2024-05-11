from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        aboutText = QLabel("Каталогизатор аудиокниг v1.0")
        layout.addWidget(aboutText)
