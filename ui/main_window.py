import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QFont, QFontDatabase
from matplotlib import style

from .main_menu import MainMenu
from .practice_window import PracticeWindow
from .custom_practice_settings import CustomPracticeSettings
from .time_modes_menu import TimeModesMenu
from .statistics_window import StatisticsWindow
from .settings_menu import SettingsMenu
from .ui_controller import UIController

from models import Board


class Application(QApplication):
    def __init__(self):
        super().__init__([])
        self.load_fonts()
        self.load_stylesheet()

    def load_stylesheet(self):
        stylesheet_path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'styles', 'styles.css'))
        with open(stylesheet_path, 'r') as file:
            self.setStyleSheet(file.read())
    
    def load_fonts(self):
        fonts_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts'))
        for filename in os.listdir(fonts_path):
            if filename.endswith(('.ttf', '.otf')):
                fontpath = os.path.join(fonts_path, filename)
                QFontDatabase.addApplicationFont(fontpath)
        self.setFont(QFont('Rubik', 16))
            

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess Puzzles')
        self.setContentsMargins(20, 20, 20, 20)
        self.setMinimumSize(1300, 800)
        
        # self.resize(1300, 800)
        # self.showMaximized()
        # self.showFullScreen()
        # self.showNormal()
        # self.setFixedSize(self.size())

        self.initialize_central_widget()
        self.ui_controller = UIController(self)

    def initialize_central_widget(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.main_menu = MainMenu()
        self.practice_window = PracticeWindow()
        self.custom_practice_settings = CustomPracticeSettings()
        self.time_modes_menu = TimeModesMenu()
        self.statistics_window = StatisticsWindow()
        self.settings_menu = SettingsMenu()

        # self.central_widget.addWidget(self.main_menu)
        # self.central_widget.addWidget(self.practice_window)
        # self.central_widget.addWidget(self.custom_practice_settings)
        # self.central_widget.addWidget(self.time_modes_menu)
        # self.central_widget.addWidget(self.statistics_window)
        # self.central_widget.addWidget(self.settings_menu)

        self.board = Board()
        self.central_widget.addWidget(self.board)