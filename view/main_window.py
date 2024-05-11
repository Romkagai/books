from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget
from view.book_info_view import BookInfoTab
from view.settings_tab_view import SettingsTab
from view.about_tab_view import AboutTab
from view.catalog_panel_view import CatalogPanel


class AudioBookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setup_models()
        self.setup_controllers()
        self.setup_connections()
        self.load_app_settings()

    def setupUI(self):
        self.setWindowTitle("Каталогизатор аудиокниг")
        self.mainLayout = QHBoxLayout()
        self.setup_catalog_panel()
        self.setup_tabs()
        self.setLayout(self.mainLayout)

    def setup_models(self):
        from models.audiobookinfo_model import AudioBookInfoModel
        from models.settings_model import SettingsModel
        from models.catalog_panel_model import CatalogPanelModel
        self.audiobook_info_model = AudioBookInfoModel()
        self.settings_model = SettingsModel()
        self.catalog_panel_model = CatalogPanelModel()

    def setup_controllers(self):
        from controllers.settings_controller import SettingsController
        from controllers.book_info_controller import BookInfoController
        from controllers.catalog_panel_controller import CatalogPanelController
        self.audiobook_info_controller = BookInfoController(self.BookInfoTab, self.audiobook_info_model)
        self.settings_controller = SettingsController(self.SettingsTab, self.settings_model)
        self.catalog_panel_controller = CatalogPanelController(self.CatalogPanel, self.catalog_panel_model)

    def setup_catalog_panel(self):
        self.CatalogPanel = CatalogPanel()
        self.mainLayout.addWidget(self.CatalogPanel)

    def setup_tabs(self):
        self.TabWidget = QTabWidget()
        self.BookInfoTab = BookInfoTab()
        self.SettingsTab = SettingsTab()
        self.AboutTab = AboutTab()

        self.TabWidget.addTab(self.BookInfoTab, "Информация о книге")
        self.TabWidget.addTab(self.SettingsTab, "Настройки")
        self.TabWidget.addTab(self.AboutTab, "О программе")

        self.mainLayout.addWidget(self.TabWidget)

    def setup_connections(self):
        self.catalog_panel_controller.book_selected.connect(self.audiobook_info_controller.update_selected_book_id)
        self.audiobook_info_controller.update_table.connect(self.catalog_panel_controller.update_audiobook_table)
        self.settings_controller.update_sort_settings.connect(self.catalog_panel_controller.update_sort_panel)
        self.settings_controller.update_display_settings.connect(self.catalog_panel_controller.update_display_options)

    def load_app_settings(self):
        self.settings_controller.setup_ui_state()
        self.catalog_panel_controller.update_audiobook_table()
