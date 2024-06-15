import re

from PyQt6.QtWidgets import QStackedWidget

from logic import DataManager, PuzzleManager


class UIController:
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.central_widget: QStackedWidget = main_window.central_widget
        self.database_manager = DataManager()
        self.connect_main_menu_signals()
        self.connect_settings_menu_signals()
        self.connect_practice_window_signals()

    def connect_main_menu_signals(self) -> None:
        main_menu = self.main_window.main_menu
        main_menu.free_practice_button.clicked.connect(self.show_practice_window)
        main_menu.custom_practice_button.clicked.connect(self.show_custom_practice_settings)
        main_menu.time_modes_button.clicked.connect(self.show_time_modes_menu)
        main_menu.statistics_button.clicked.connect(self.show_statistics_window)
        main_menu.settings_button.clicked.connect(self.show_settings_menu)
        main_menu.quit_button.clicked.connect(self.main_window.close)

    def connect_settings_menu_signals(self) -> None:
        settings_menu = self.main_window.settings_menu
        settings_menu.return_button.clicked.connect(self.show_main_menu)

    def connect_practice_window_signals(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.new_puzzle_button.clicked.connect(self.initialize_puzzle)
        practice_window.return_button.clicked.connect(self.close_practice_window)

    def show_main_menu(self) -> None:
        widget = self.main_window.main_menu
        self.central_widget.setCurrentWidget(widget)
    
    def show_practice_window(self) -> None:
        widget = self.main_window.practice_window
        self.central_widget.setCurrentWidget(widget)

    def show_custom_practice_settings(self) -> None:
        widget = self.main_window.custom_practice_settings
        self.central_widget.setCurrentWidget(widget)

    def show_time_modes_menu(self) -> None:
        widget = self.main_window.time_modes_menu
        self.central_widget.setCurrentWidget(widget)

    def show_statistics_window(self) -> None:
        widget = self.main_window.statistics_window
        self.central_widget.setCurrentWidget(widget)

    def show_settings_menu(self) -> None:
        widget = self.main_window.settings_menu
        self.central_widget.setCurrentWidget(widget)

    def initialize_puzzle(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.board_widget.initialize_puzzle()
        puzzle_rating, puzzle_themes = practice_window.board_widget.get_current_puzzle_info()
        practice_window.rating_value.setText(str(puzzle_rating))
        practice_window.themes_value.setText(self.parse_themes(puzzle_themes))

    def parse_themes(self, themes: str) -> str:
        result = []
        themes = themes.split()
        for theme in themes:
            theme = re.sub(r'([A-Z0-9])', r' \1', theme)
            theme = ' '.join(word.capitalize() for word in theme.split())
            result.append(theme)
        return '\n'.join(result)

    def close_practice_window(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.board_widget.clear_board()
        practice_window.rating_value.clear()
        practice_window.themes_value.clear()
        practice_window.status_label.clear()
        self.show_main_menu()