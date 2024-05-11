import sys

from PyQt6.QtWidgets import QApplication
from view.main_window import AudioBookCataloguer


# Создание приложения
app = QApplication(sys.argv)

# Создание моделей


# Создание главного окна
mainWindow = AudioBookCataloguer()

# Создание контроллеров и связывание представления с моделями

mainWindow.show()
sys.exit(app.exec())