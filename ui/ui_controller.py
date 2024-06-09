from PyQt6.QtWidgets import QStackedWidget

from logic import DataManager, PuzzleManager


class UIController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.central_widget: QStackedWidget = main_window.central_widget
        self.database_manager = DataManager()
        self.connect_main_menu_signals()
        self.connect_settings_menu_signals()

    def connect_main_menu_signals(self):
        main_menu = self.main_window.main_menu
        main_menu.free_practice_button.clicked.connect(self.show_practice_window)
        main_menu.custom_practice_button.clicked.connect(self.show_custom_practice_settings)
        main_menu.time_modes_button.clicked.connect(self.show_time_modes_menu)
        main_menu.statistics_button.clicked.connect(self.show_statistics_window)
        main_menu.settings_button.clicked.connect(self.show_settings_menu)
        main_menu.quit_button.clicked.connect(self.main_window.close)

    def connect_settings_menu_signals(self):
        settings_menu = self.main_window.settings_menu
        settings_menu.return_button.clicked.connect(self.show_main_menu)

    def show_main_menu(self):
        widget = self.main_window.main_menu
        self.central_widget.setCurrentWidget(widget)
    
    def show_practice_window(self):
        widget = self.main_window.practice_window
        self.central_widget.setCurrentWidget(widget)

    def show_custom_practice_settings(self):
        widget = self.main_window.custom_practice_settings
        self.central_widget.setCurrentWidget(widget)

    def show_time_modes_menu(self):
        widget = self.main_window.time_modes_menu
        self.central_widget.setCurrentWidget(widget)

    def show_statistics_window(self):
        widget = self.main_window.statistics_window
        self.central_widget.setCurrentWidget(widget)

    def show_settings_menu(self):
        widget = self.main_window.settings_menu
        self.central_widget.setCurrentWidget(widget)