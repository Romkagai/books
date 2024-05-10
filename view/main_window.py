from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget
from view.book_info_tab import BookInfoTab
from view.settings_tab import SettingsTab
from view.about_tab import AboutTab
from view.catalog_panel import CatalogPanel


class AudioBookCataloguer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setup_model()
        self.setup_connections()

    def setupUI(self):
        self.setWindowTitle("Каталогизатор аудиокниг")
        self.mainLayout = QHBoxLayout()
        self.setup_catalog_panel()
        self.setup_tabs()
        self.setLayout(self.mainLayout)

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

    def setup_model(self):
        from controllers.audiobook_handler import AudiobookCataloguerLogic
        self.model = AudiobookCataloguerLogic(self)

    def setup_connections(self):
        self.CatalogPanel.addButton.clicked.connect(self.model.add_audiobook)
        self.CatalogPanel.audiobookTable.cellClicked.connect(self.model.update_current_book_id)
        self.BookInfoTab.findBookInfoButton.clicked.connect(self.model.do_nothing)
        self.BookInfoTab.deleteButton.clicked.connect(self.model.delete_audiobook)
        self.BookInfoTab.addFavoriteButton.clicked.connect(self.model.do_nothing)
        self.BookInfoTab.addCompletedButton.clicked.connect(self.model.do_nothing)
        self.BookInfoTab.editButton.clicked.connect(self.model.edit_book)
        self.CatalogPanel.sortOptions.currentIndexChanged.connect(self.model.sort_changed)
        self.CatalogPanel.sortDirectionButton.clicked.connect(self.model.toggle_sort_direction)
        self.CatalogPanel.searchPanel.textChanged.connect(self.CatalogPanel.searchTimer.start)
        self.CatalogPanel.searchTimer.timeout.connect(self.model.do_search)
        self.SettingsTab.saveSettingsButton.clicked.connect(self.model.update_sort_panel)

        self.model.update_audiobook_table()