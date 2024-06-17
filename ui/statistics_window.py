from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ui.main_menu import MainMenu, MenuButton, MenuHeading, AppNameLabel

class StatisticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_layout()

    def initialize_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

        self.create_window_name_container()
        self.create_puzzle_statistics_container()
        self.create_theme_statistics_container()
        self.create_buttons_container()

        self.main_layout.addWidget(self.window_name_container)
        self.main_layout.addWidget(self.puzzle_statistics_container)
        self.main_layout.addWidget(self.theme_statistics_container)
        self.main_layout.addWidget(self.buttons_container)

    def create_window_name_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.window_name_container, self.window_name_container_layout = container
        self.window_name_container_layout.addWidget(AppNameLabel('Statistics'))

    def create_puzzle_statistics_container(self) -> None:
        container = MainMenu.create_menu_container(type='g')
        self.puzzle_statistics_container, self.puzzle_statistics_container_layout = container
        self.puzzle_statistics_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.puzzle_statistics_container_layout.setHorizontalSpacing(20)
        self.puzzle_statistics_container_layout.setColumnStretch(1, 1)

        puzzles_played_label = MenuHeading('Puzzles played:', Qt.AlignmentFlag.AlignLeft)
        puzzles_solved_label = MenuHeading('Puzzles solved:', Qt.AlignmentFlag.AlignLeft)
        percent_solved_label = MenuHeading('Solve %:', Qt.AlignmentFlag.AlignLeft)
        self.puzzles_played_value = QLabel()
        self.puzzles_solved_value = QLabel()
        self.percent_solved_value = QLabel()

        self.puzzle_statistics_container_layout.addWidget(puzzles_played_label, 1, 0)
        self.puzzle_statistics_container_layout.addWidget(self.puzzles_played_value, 1, 1)
        self.puzzle_statistics_container_layout.addWidget(puzzles_solved_label, 2, 0)
        self.puzzle_statistics_container_layout.addWidget(self.puzzles_solved_value, 2, 1)
        self.puzzle_statistics_container_layout.addWidget(percent_solved_label, 3, 0)
        self.puzzle_statistics_container_layout.addWidget(self.percent_solved_value, 3, 1)

    def create_theme_statistics_container(self) -> None:
        container = MainMenu.create_menu_container(type='g')
        self.theme_statistics_container, self.theme_statistics_container_layout = container
        self.theme_statistics_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.theme_statistics_container_layout.setHorizontalSpacing(20)
        self.theme_statistics_container_layout.setColumnStretch(1, 1)

        most_popular_label = MenuHeading('Most popular:', Qt.AlignmentFlag.AlignLeft)
        best_percentage_label = MenuHeading('Best solve %:', Qt.AlignmentFlag.AlignLeft)
        worst_percentage_label = MenuHeading('Worst solve %:', Qt.AlignmentFlag.AlignLeft)
        self.most_popular_value = QLabel()
        self.best_percentage_value = QLabel()
        self.worst_percentage_value = QLabel()

        self.theme_statistics_container_layout.addWidget(most_popular_label, 0, 0)
        self.theme_statistics_container_layout.addWidget(self.most_popular_value, 0, 1)
        self.theme_statistics_container_layout.addWidget(best_percentage_label, 1, 0)
        self.theme_statistics_container_layout.addWidget(self.best_percentage_value, 1, 1)
        self.theme_statistics_container_layout.addWidget(worst_percentage_label, 2, 0)
        self.theme_statistics_container_layout.addWidget(self.worst_percentage_value, 2, 1)

    def create_buttons_container(self) -> None:
        container = MainMenu.create_menu_container()
        self.buttons_container, self.buttons_container_layout = container
        self.reset_progress_button = MenuButton('Reset progress', 'red_button')
        self.return_button = MenuButton('Return to menu')
        self.buttons_container_layout.addWidget(self.reset_progress_button)
        self.buttons_container_layout.addWidget(self.return_button)