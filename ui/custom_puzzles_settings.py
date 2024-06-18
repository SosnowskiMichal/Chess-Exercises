from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QComboBox
from PyQt6.QtCore import Qt

from .main_menu import MainMenu, MenuButton, AppNameLabel, MenuHeading


class CustomPuzzlesSettings(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_layout()

    def initialize_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_window_name_container()
        self.create_customization_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.window_name_container)
        self.main_layout.addWidget(self.customization_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_window_name_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.window_name_container, self.window_name_container_layout = container
        self.window_name_label = AppNameLabel('Customize puzzles')
        self.window_name_container_layout.addWidget(self.window_name_label)

    def create_customization_container(self) -> None:
        container = MainMenu.create_menu_container(type='g')
        self.customization_container, self.customization_container_layout = container
        self.customization_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.customization_container_layout.setHorizontalSpacing(20)
        self.customization_container_layout.setColumnStretch(1, 1)

        min_rating_label = MenuHeading(
            'Min rating:', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        max_rating_label = MenuHeading(
            'Max rating:', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        theme_label = MenuHeading(
            'Theme:', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        
        self.min_rating_value = RatingSelector()
        self.max_rating_value = RatingSelector()
        self.theme_value = ThemeSelector()

        self.customization_container_layout.addWidget(min_rating_label, 0, 0)
        self.customization_container_layout.addWidget(self.min_rating_value, 0, 1)
        self.customization_container_layout.addWidget(max_rating_label, 1, 0)
        self.customization_container_layout.addWidget(self.max_rating_value, 1, 1)
        self.customization_container_layout.addWidget(theme_label, 2, 0)
        self.customization_container_layout.addWidget(self.theme_value, 2, 1)

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container
        self.start_button = MenuButton('Start custom practice')
        self.reset_choice_button = MenuButton('Reset choice')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.start_button)
        self.buttons_container_layout.addWidget(self.reset_choice_button)
        self.buttons_container_layout.addWidget(self.return_button)


class RatingSelector(QSpinBox):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(40)


class ThemeSelector(QComboBox):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(40)
        self.setStyleSheet('background-color: #2a2b2e;')