import os

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap

from .pieces import *


class ChessBoard(QWidget):
    def __init__(self, theme='dark_wood'):
        super().__init__()
        self.theme = theme
        self.assets_dir = self.get_assets_dir(self.theme)
        self.initialize_board()

    def initialize_board(self):
        self.setAcceptDrops(True)
        self.setMaximumSize(800, 800)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.initialize_layout()
        self.initialize_squares()

    def get_assets_dir(self, theme):
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'boards', theme)
        return os.path.normpath(assets_dir)

    def initialize_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid_layout)

    def initialize_squares(self):
        for row in range(8):
            for col in range(8):
                square = ChessBoardSquare(row, col, self)
                self.grid_layout.addWidget(square, row, col)
        self.update_board()

    # TODO: rework (currently for testing)
    def update_board(self, fen: str = None, move: str = None):
        king_white = King('white', self.theme, self)
        queen_white = Queen('white', self.theme, self)
        rook_1_white = Rook('white', self.theme, self)
        rook_2_white = Rook('white', self.theme, self)
        bishop_1_white = Bishop('white', self.theme, self)
        bishop_2_white = Bishop('white', self.theme, self)
        knight_1_white = Knight('white', self.theme, self)
        knight_2_white = Knight('white', self.theme, self)
        
        self.grid_layout.addWidget(king_white, 7, 4)
        self.grid_layout.addWidget(queen_white, 7, 3)
        self.grid_layout.addWidget(rook_1_white, 7, 0)
        self.grid_layout.addWidget(rook_2_white, 7, 7)
        self.grid_layout.addWidget(bishop_1_white, 7, 2)
        self.grid_layout.addWidget(bishop_2_white, 7, 5)
        self.grid_layout.addWidget(knight_1_white, 7, 1)
        self.grid_layout.addWidget(knight_2_white, 7, 6)

        for col in range(8):
            pawn_white = Pawn('white', self.theme, self)
            self.grid_layout.addWidget(pawn_white, 6, col)


class ChessBoardSquare(QLabel):
    def __init__(self, row, col, board: ChessBoard = None):
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
                os.path.join(assets_dir, 'white.png'))
            self.setPixmap(background_image)
        else:
            background_image = QPixmap(
                os.path.join(assets_dir, 'black.png'))
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