from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtCore import Qt

from ui.main_menu import MainMenu, MenuButton, MenuHeading


class SettingsMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_main_layout()

    def initialize_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_board_settings_container()
        self.create_pieces_settings_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.board_settings_container)
        self.main_layout.addWidget(self.pieces_settings_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_board_settings_container(self):
        container = MainMenu.create_menu_container()
        self.board_settings_container, self.board_settings_container_layout = container
        self.board_settings_heading = MenuHeading('Board settings')
        self.board_settings_container_layout.addWidget(self.board_settings_heading)

    def create_pieces_settings_container(self):
        container = MainMenu.create_menu_container()
        self.pieces_settings_container, self.pieces_settings_container_layout = container
        self.pieces_settings_heading = MenuHeading('Pieces settings')
        self.pieces_settings_container_layout.addWidget(self.pieces_settings_heading)

    def create_buttons_container(self):
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container
        self.reset_progress_button = MenuButton('Reset progress', 'red_button')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.reset_progress_button)
        self.buttons_container_layout.addSpacing(10)
        self.buttons_container_layout.addWidget(self.return_button)