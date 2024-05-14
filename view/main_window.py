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
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                border-radius: 4px;
                background: #3e3e3e;
            }
            QTabBar::tab {
                background: #4e4e4e;
                padding: 10px;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2e2e2e;
                border-bottom: 2px solid #0078d7;
            }
            QHBoxLayout {
                margin: 10px;
            }
            QToolBar {
                background: #3e3e3e;
                border: none;
            }
            QToolBar::separator {
                background: #6e6e6e;
                width: 1px;
                height: 20px;
            }
            QAction {
                font-size: 14px;
                color: #f0f0f0;
            }
        """)
        self.main_layout = QHBoxLayout()
        self.setup_catalog_panel()
        self.setup_tabs()
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
        self.settings_controller.update_book_info_settings.connect(self.audiobook_info_controller.update_book_info_options)

    def load_app_settings(self):
        """
        Загрузка настроек приложения и обновление интерфейса.
        """
        self.settings_controller.setup_ui_state()
        self.catalog_panel_controller.update_audiobook_table()
