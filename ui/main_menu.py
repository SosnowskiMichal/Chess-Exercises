from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_main_layout()

    def initialize_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_app_name_container()
        # self.create_user_selection_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.app_name_container)
        # self.main_layout.addWidget(self.user_selection_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_app_name_container(self):
        container = MainMenu.create_menu_container()
        self.app_name_container, self.app_name_container_layout = container

        self.app_name_label = AppNameLabel('CHESS PUZZLES')
        self.app_name_container_layout.addWidget(self.app_name_label)

    # def create_user_selection_container(self):
    #     container = self.create_menu_container(grid=True)
    #     self.user_selection_container, self.user_selection_container_layout = container
    #     self.user_selection_container_layout.setSpacing(10)

    #     self.selection_label = QLabel('Select user:')
    #     self.selection_list = QComboBox()
    #     self.creation_label = QLabel('Create new user:')
    #     self.creation_input = QLineEdit()
    #     self.creation_button = MainMenuButton('Create user')
    #     self.warning_label = QLabel()

    #     self.user_selection_container_layout.addWidget(self.selection_label, 0, 0)
    #     self.user_selection_container_layout.addWidget(self.selection_list, 0, 1)
    #     self.user_selection_container_layout.addWidget(self.creation_label, 1, 0)
    #     self.user_selection_container_layout.addWidget(self.creation_input, 1, 1)
    #     self.user_selection_container_layout.addWidget(self.creation_button, 2, 0, 1, 2)
    #     self.user_selection_container_layout.addWidget(self.warning_label, 3, 0, 1, 2)

    def create_buttons_container(self):
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container

        self.free_practice_button = MenuButton('Free Practice')
        self.custom_practice_button = MenuButton('Custom Practice')
        self.time_modes_button = MenuButton('Time Modes')
        self.settings_button = MenuButton('Settings')
        self.statistics_button = MenuButton('Statistics')
        self.quit_button = MenuButton('Quit', 'red_button')

        self.buttons_container_layout.addWidget(self.free_practice_button)
        self.buttons_container_layout.addWidget(self.custom_practice_button)
        self.buttons_container_layout.addWidget(self.time_modes_button)
        self.buttons_container_layout.addSpacing(20)
        self.buttons_container_layout.addWidget(self.statistics_button)
        self.buttons_container_layout.addWidget(self.settings_button)
        self.buttons_container_layout.addSpacing(20)
        self.buttons_container_layout.addWidget(self.quit_button)

    def create_menu_container(grid: bool = False):
        container = QWidget()
        container.setObjectName('menu-container')
        container.setFixedWidth(500)
        container.setContentsMargins(20, 20, 20, 20)
        container_layout = QGridLayout(container) if grid else QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return container, container_layout


class AppNameLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class MenuButton(QPushButton):
    def __init__(self, text: str, name: str = None):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if name:
            self.setObjectName(name)

class MenuHeading(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setContentsMargins(0, 0, 0, 20)