from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_main_layout()

    def initialize_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # TODO: create custom classes with new design

        self.container = QWidget()
        self.container.setStyleSheet('background-color: blue;')
        self.container.setContentsMargins(50, 50, 50, 50)
        self.main_layout.addWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_name_label = MainMenuLabel('APP NAME')
        self.free_practice_button = MainMenuButton('Free Practice')
        self.custom_practice_button = MainMenuButton('Custom Practice')
        self.time_modes_button = MainMenuButton('Time Modes')

        self.container_layout.addWidget(self.app_name_label)
        self.container_layout.addWidget(self.free_practice_button)
        self.container_layout.addWidget(self.custom_practice_button)
        self.container_layout.addWidget(self.time_modes_button)


class MainMenuLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class MainMenuButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)