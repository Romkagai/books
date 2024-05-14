import sys
from PyQt6.QtWidgets import QApplication
from view.main_window import AudioBookCataloguer


def main():
    """
    Основная функция для запуска приложения.
    """
    # Создание приложения
    app = QApplication(sys.argv)

    # Создание главного окна
    main_window = AudioBookCataloguer()

    # Показ главного окна
    main_window.show()

    # Запуск основного цикла приложения
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
