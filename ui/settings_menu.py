from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.main_menu import MainMenu, MenuButton, MenuHeading, AppNameLabel


class SettingsMenu(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_layout()

    def initialize_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_window_name_container()
        self.create_board_settings_container()
        self.create_pieces_settings_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.window_name_container)
        self.main_layout.addWidget(self.board_settings_container)
        self.main_layout.addWidget(self.pieces_settings_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_window_name_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.window_name_container, self.window_name_container_layout = container
        self.window_name_label = AppNameLabel('Settings')
        self.window_name_container_layout.addWidget(self.window_name_label)

    def create_board_settings_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.board_settings_container, self.board_settings_container_layout = container
        self.board_settings_heading = MenuHeading('Board style')
        self.board_settings_container_layout.addWidget(self.board_settings_heading)

    def create_pieces_settings_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.pieces_settings_container, self.pieces_settings_container_layout = container
        self.pieces_settings_heading = MenuHeading('Pieces style')
        self.pieces_settings_container_layout.addWidget(self.pieces_settings_heading)

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container
        self.save_button = MenuButton('Save settings')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.save_button)
        self.buttons_container_layout.addWidget(self.return_button)