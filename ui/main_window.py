import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QFont, QFontDatabase

from .main_menu import MainMenu
from .puzzles_window import PuzzlesWindow
from .custom_puzzles_settings import CustomPuzzlesSettings
from .statistics_window import StatisticsWindow
from .settings_menu import SettingsMenu
from .ui_controller import UIController


class Application(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.load_fonts()
        self.load_stylesheet()

    def load_stylesheet(self) -> None:
        stylesheet_path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'styles', 'styles.css'))
        with open(stylesheet_path, 'r') as file:
            self.setStyleSheet(file.read())
    
    def load_fonts(self) -> None:
        fonts_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts'))
        for filename in os.listdir(fonts_path):
            if filename.endswith(('.ttf', '.otf')):
                fontpath = os.path.join(fonts_path, filename)
                QFontDatabase.addApplicationFont(fontpath)
        self.setFont(QFont('Rubik', 16))
            

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Chess Puzzles')
        self.setContentsMargins(10, 10, 10, 10)
        self.setMinimumSize(1400, 800)
        
        # self.resize(1300, 800)
        # self.showMaximized()
        # self.showFullScreen()
        # self.showNormal()
        # self.setFixedSize(self.size())

        self.initialize_central_widget()
        self.ui_controller = UIController(self)

    def initialize_central_widget(self) -> None:
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.main_menu = MainMenu()
        self.puzzles_window = PuzzlesWindow()
        self.custom_puzzles_settings = CustomPuzzlesSettings()
        self.statistics_window = StatisticsWindow()
        self.settings_menu = SettingsMenu()

        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.puzzles_window)
        self.central_widget.addWidget(self.custom_puzzles_settings)
        self.central_widget.addWidget(self.statistics_window)
        self.central_widget.addWidget(self.settings_menu)