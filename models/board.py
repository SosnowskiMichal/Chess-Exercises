import os

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap

from .pieces import *


class Board(QWidget):
    def __init__(self, theme='dark_wood', config=None):
        super().__init__()
        self.theme = theme
        self.config = config
        self.assets_dir = self.get_assets_dir(self.theme)
        self.initialize_board()

    def initialize_board(self):
        self.setMaximumSize(800, 800)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.initialize_layout()
        self.initialize_squares()
        # self.update_board(self.config)

    def get_assets_dir(self, theme):
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'boards', theme)
        return os.path.normpath(assets_dir)

    def initialize_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)

    def initialize_squares(self):
        for row in range(8):
            for col in range(8):
                square = ChessBoardSquare(row, col, self)
                self.grid_layout.addWidget(square, row, col)

    # def update_board(self, config):
    #     self.king_white = King('white', self.theme)
    #     self.king_black = King('black', self.theme)

    #     square = self.grid_layout.itemAtPosition(0, 4).widget()
    #     self.king_white.setParent(square)
    #     self.king_white.move(0, 0)
    #     self.king_white.show()

        # self.grid_layout.addWidget(self.king_white, 0, 4)
        # self.grid_layout.addWidget(self.king_black, 7, 4)


class ChessBoardSquare(QLabel):
    def __init__(self, row, col, board: Board = None):
        super().__init__(board)
        self.board = board
        self.row = row
        self.col = col
        self.initialize_square()

    def initialize_square(self):
        self.setMaximumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.set_background()

    def set_background(self):
        self.setScaledContents(True)
        assets_dir = self.board.assets_dir
        if (self.row + self.col) % 2 == 0:
            background_image = QPixmap(
                os.path.join(assets_dir, 'black.png'))
            self.setPixmap(background_image)
        else:
            background_image = QPixmap(
                os.path.join(assets_dir, 'white.png'))
            self.setPixmap(background_image)

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasImage():
    #         event.acceptProposedAction()

    # def dropEvent(self, event):
    #     piece = event.source()
    #     piece.setParent(self)
    #     piece.move(0, 0)
    #     piece.show()
    #     event.acceptProposedAction()