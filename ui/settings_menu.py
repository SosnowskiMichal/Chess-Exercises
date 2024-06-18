import os

from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel,
    QHBoxLayout, QRadioButton, QButtonGroup
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .main_menu import MainMenu, MenuButton, MenuHeading, AppNameLabel


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
        container = MainMenu.create_menu_container(width=650)
        self.window_name_container, self.window_name_container_layout = container
        self.window_name_label = AppNameLabel('Settings')
        self.window_name_container_layout.addWidget(self.window_name_label)

    def create_board_settings_container(self) -> None:
        container = MainMenu.create_menu_container(type='h', width=650)
        self.board_settings_container, self.board_settings_container_layout = container
        self.board_styles_buttons = QButtonGroup()

    def create_pieces_settings_container(self) -> None:
        container = MainMenu.create_menu_container(type='h', width=650)
        self.pieces_settings_container, self.pieces_settings_container_layout = container
        self.pieces_styles_buttons = QButtonGroup()

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container(width=650)
        self.buttons_container, self.buttons_container_layout = container
        self.save_button = MenuButton('Save settings')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.save_button)
        self.buttons_container_layout.addWidget(self.return_button)

    def initialize_board_styles(self, styles: List[str], user_style: str) -> None:
        for style in styles:
            style_option = StyleOption(style, 4, self.board_styles_buttons)
            if style == user_style:
                style_option.radio_button.setChecked(True)
            self.board_settings_container_layout.addWidget(style_option)

    def initialize_pieces_styles(self, styles: List[str], user_style: str) -> None:
        for style in styles:
            style_option = StyleOption(style, 2, self.pieces_styles_buttons)
            if style == user_style:
                style_option.radio_button.setChecked(True)
            self.pieces_settings_container_layout.addWidget(style_option)


class StyleOption(QWidget):
    def __init__(
        self,
        style_option: str,
        grid_size: int,
        button_group: QButtonGroup,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.style_option = style_option
        self.grid_size = grid_size
        self.set_assets_dir()
        self.setMinimumWidth(150)
        self.initialize_layout()
        button_group.addButton(self.radio_button)

    def set_assets_dir(self) -> None:
        element = 'boards' if self.grid_size == 4 else 'pieces'
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', element, self.style_option
        )
        self.assets_dir = os.path.normpath(assets_dir)

    def initialize_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.radio_button_layout = QHBoxLayout()
        self.radio_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.radio_button = QRadioButton(self)
        self.radio_button.setObjectName(self.style_option)
        self.radio_button_layout.addWidget(self.radio_button)
        self.main_layout.addLayout(self.radio_button_layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.grid_layout)
        self.initialize_images()

        self.name_label = MenuHeading(self.style_option.replace('_', ' '))
        self.main_layout.addWidget(self.name_label)
        
    def initialize_images(self) -> None:
        if self.grid_size == 4:
            white_square_pix = QPixmap(
                os.path.join(self.assets_dir, 'black.png')
            ).scaled(40, 40)
            black_square_pix = QPixmap(
                os.path.join(self.assets_dir, 'white.png')
            ).scaled(40, 40)
            for i in range(2):
                for j in range(2):
                    square = QLabel()
                    square.setPixmap(
                        white_square_pix if (i + j) % 2 != 0
                        else black_square_pix
                    )
                    square.setMaximumSize(40, 40)
                    self.grid_layout.addWidget(square, i, j)
        elif self.grid_size == 2:
            white_queen_pix = QPixmap(
                os.path.join(self.assets_dir, 'queen-white.png')
            ).scaled(60, 60)
            black_queen_pix = QPixmap(
                os.path.join(self.assets_dir, 'queen-black.png')
            ).scaled(60, 60)
            for i in range(2):
                piece = QLabel()
                piece.setPixmap(white_queen_pix if i == 0 else black_queen_pix)
                piece.setMaximumSize(60, 60)
                self.grid_layout.addWidget(piece, 0, i)