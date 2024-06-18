from typing import Tuple, Optional
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_main_layout()

    def initialize_main_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_app_name_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.app_name_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_app_name_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.app_name_container, self.app_name_container_layout = container

        self.app_name_label = AppNameLabel('Chess Puzzles')
        self.app_name_container_layout.addWidget(self.app_name_label)

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container

        self.puzzles_button = MenuButton('Random puzzles')
        self.custom_puzzles_button = MenuButton('Custom puzzles')
        self.settings_button = MenuButton('Settings')
        self.statistics_button = MenuButton('Statistics')
        self.quit_button = MenuButton('Quit', 'red_button')

        self.buttons_container_layout.addWidget(self.puzzles_button)
        self.buttons_container_layout.addWidget(self.custom_puzzles_button)
        self.buttons_container_layout.addSpacing(20)
        self.buttons_container_layout.addWidget(self.statistics_button)
        self.buttons_container_layout.addWidget(self.settings_button)
        self.buttons_container_layout.addSpacing(20)
        self.buttons_container_layout.addWidget(self.quit_button)

    def create_menu_container(
        type: str = 'v', width: int = 550
    ) -> Tuple[QWidget, QGridLayout | QVBoxLayout | QHBoxLayout]:
        container = QWidget()
        container.setObjectName('menu-container')
        container.setFixedWidth(width)
        container.setContentsMargins(20, 20, 20, 20)
        if type == 'g':
            container_layout = QGridLayout(container)
        elif type == 'h':
            container_layout = QHBoxLayout(container)
        else:
            container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return container, container_layout


class AppNameLabel(QLabel):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class MenuButton(QPushButton):
    def __init__(
        self, text: Optional[str] = None, name: Optional[str] = None
    ) -> None:
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if name:
            self.setObjectName(name)

class MenuHeading(QLabel):
    def __init__(
        self,
        text: Optional[str] = None,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ) -> None:
        super().__init__(text)
        self.setAlignment(alignment)