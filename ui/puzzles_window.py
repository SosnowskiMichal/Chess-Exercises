from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ui.main_menu import MainMenu, MenuButton, AppNameLabel, MenuHeading
from board import ChessBoard


class PuzzlesWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_layout()

    def initialize_layout(self) -> None:
        self.create_main_layout()

        self.create_mode_name_container()
        self.create_puzzle_info_container()
        self.create_status_container()
        self.create_buttons_container()

        self.side_layout.addWidget(self.mode_name_container)
        self.side_layout.addWidget(self.puzzle_info_container)
        self.side_layout.addWidget(self.status_container)
        self.side_layout.addWidget(self.buttons_container)

    def create_main_layout(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.board_widget = ChessBoard()
        self.main_layout.addWidget(self.board_widget)
        self.side_layout = QVBoxLayout()
        self.main_layout.addLayout(self.side_layout)
        self.side_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_layout.setSpacing(20)

    def create_mode_name_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.mode_name_container, self.mode_name_container_layout = container
        mode_name_label = AppNameLabel('Practice mode')
        self.mode_name_container_layout.addWidget(mode_name_label)

    def create_puzzle_info_container(self) -> None:
        container = MainMenu.create_menu_container(type='g')
        self.puzzle_info_container, self.puzzle_info_container_layout = container
        self.puzzle_info_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.puzzle_info_container_layout.setHorizontalSpacing(20)

        rating_label = MenuHeading('Rating:', Qt.AlignmentFlag.AlignLeft)
        themes_label = MenuHeading('Themes:', Qt.AlignmentFlag.AlignLeft)
        self.rating_value = QLabel()
        self.themes_value = QLabel()
        self.themes_value.setWordWrap(True)

        self.puzzle_info_container_layout.addWidget(rating_label, 0, 0)
        self.puzzle_info_container_layout.addWidget(self.rating_value, 0, 1)
        self.puzzle_info_container_layout.addWidget(themes_label, 1, 0)
        self.puzzle_info_container_layout.addWidget(self.themes_value, 1, 1)

    def create_status_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.status_container, self.status_container_layout = container
        self.status_label = MenuHeading()
        self.status_container_layout.addWidget(self.status_label)

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container
        self.new_puzzle_button = MenuButton('New puzzle')
        self.customize_puzzles_button = MenuButton('Customize puzzles')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.new_puzzle_button)
        self.buttons_container_layout.addWidget(self.customize_puzzles_button)
        self.buttons_container_layout.addWidget(self.return_button)