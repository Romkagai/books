import sys

from PyQt6.QtWidgets import QApplication
from ui.ui import AudiobookCataloguer


app = QApplication(sys.argv)
ex = AudiobookCataloguer()
ex.show()

sys.exit(app.exec())