from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QFont

from ui.main_menu import MainMenu


class Application(QApplication):
    def __init__(self):
        super().__init__([])
        self.setFont(QFont('Helvetica', 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle('Przejazdy Wrocławskiego Roweru Miejskiego 2021')
        
        self.resize(1400, 700)
        # self.showFullScreen()
        self.showMaximized()
        # self.showNormal()

        # self.setFixedSize(self.size())
        # self.setStyleSheet('background-color: #072227;')

        self.initialize_central_widget()

    def initialize_central_widget(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.main_menu = MainMenu()

        self.central_widget.addWidget(self.main_menu)