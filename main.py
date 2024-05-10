import sys

from PyQt6.QtWidgets import QApplication
from view.main_window import AudioBookCataloguer


app = QApplication(sys.argv)
mainWindow = AudioBookCataloguer()
mainWindow.show()
sys.exit(app.exec())