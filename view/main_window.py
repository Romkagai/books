import os

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QSizePolicy
from view.audiobook_info_view import BookInfoTab
from view.settings_tab_view import SettingsTab
from view.about_tab_view import AboutTab
from view.catalog_panel_view import CatalogPanel
from models.audiobook_info_model import AudioBookInfoModel
from models.settings_model import SettingsModel
from models.catalog_panel_model import CatalogPanelModel
from controllers.settings_controller import SettingsController
from controllers.audiobook_info_controller import AudiobookInfoController
from controllers.catalog_panel_controller import CatalogPanelController


class AudioBookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)  # Установим минимальный размер окна
        self.resize(1024, 768)  # Установим начальный размер окна
        self.setup_ui()
        self.setup_models()
        self.setup_controllers()
        self.setup_connections()
        self.load_app_settings()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        self.setWindowTitle("Каталогизатор аудиокниг")
        self.main_layout = QHBoxLayout()
        self.setup_catalog_panel()
        self.setup_tabs()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(self.main_layout)

    def setup_catalog_panel(self):
        """
        Создание и добавление панели каталога в основной макет.
        """
        self.catalog_panel = CatalogPanel()
        self.main_layout.addWidget(self.catalog_panel)

    def setup_tabs(self):
        """
        Создание и добавление вкладок в основной макет.
        """
        self.tab_widget = QTabWidget()
        self.book_info_tab = BookInfoTab()
        self.settings_tab = SettingsTab()
        self.about_tab = AboutTab()

        self.tab_widget.addTab(self.book_info_tab, "Информация о книге")
        self.tab_widget.addTab(self.settings_tab, "Настройки")
        self.tab_widget.addTab(self.about_tab, "О программе")

        self.tab_widget.tabBar().setDocumentMode(True)
        self.tab_widget.tabBar().setExpanding(True)

        self.main_layout.addWidget(self.tab_widget)

    def setup_models(self):
        """
        Импорт и инициализация моделей данных.
        """
        self.audiobook_info_model = AudioBookInfoModel()
        self.settings_model = SettingsModel()
        self.catalog_panel_model = CatalogPanelModel()

    def setup_controllers(self):
        """
        Импорт и инициализация контроллеров для управления взаимодействием между представлениями и моделями.
        """
        self.audiobook_info_controller = AudiobookInfoController(self.book_info_tab, self.audiobook_info_model)
        self.settings_controller = SettingsController(self.settings_tab, self.settings_model)
        self.catalog_panel_controller = CatalogPanelController(self.catalog_panel, self.catalog_panel_model)

    def setup_connections(self):
        """
        Настройка сигналов и слотов для взаимодействия между различными компонентами.
        """
        self.catalog_panel_controller.book_selected.connect(self.audiobook_info_controller.update_selected_book_id)
        self.audiobook_info_controller.update_table.connect(self.catalog_panel_controller.update_audiobook_table)
        self.settings_controller.update_sort_settings.connect(self.catalog_panel_controller.update_sort_panel)
        self.settings_controller.update_display_settings.connect(self.catalog_panel_controller.update_display_options)
        self.settings_controller.update_book_info_settings.connect(
            self.audiobook_info_controller.update_book_info_options)
        self.settings_controller.update_theme.connect(self.apply_stylesheet)

    def load_app_settings(self):
        """
        Загрузка настроек приложения и обновление интерфейса.
        """
        self.settings_controller.setup_ui_state()
        self.catalog_panel_controller.update_audiobook_table()

    def apply_stylesheet(self, stylesheet_name):
        """
        Применение стиля из указанного CSS файла.
        """
        stylesheet_path = os.path.join(os.path.dirname(__file__), 'themes', stylesheet_name)
        with open(stylesheet_path, "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())
