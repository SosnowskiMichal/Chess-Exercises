from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class SettingsMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_main_layout()

    def initialize_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.container = QWidget()
        self.container.setStyleSheet('background-color: blue;')
        self.container.setContentsMargins(50, 50, 50, 50)
        self.main_layout.addWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.test = QLabel('Settings Menu')
        self.container_layout.addWidget(self.test)

        # TODO: create settings