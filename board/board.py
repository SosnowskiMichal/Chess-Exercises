import os

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap

from .pieces import *
from .board_controller import BoardController


class ChessBoard(QWidget):
    def __init__(self, theme='dark_wood'):
        super().__init__()
        self.theme = theme
        self.assets_dir = self.get_assets_dir(self.theme)
        self.board_controller = BoardController(self)
        self.initialize_board()

    def initialize_board(self):
        self.setAcceptDrops(True)
        self.setMaximumSize(800, 800)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.initialize_layout()
        self.initialize_squares()
        self.initialize_puzzle()

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

    # self.setup_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    # self.setup_board('r6k/pp2r2p/4Rp1Q/3p4/8/1N1P2R1/PqP2bPP/7K b - - 0 24')

    def initialize_puzzle(self, rating: int = None, theme: str = None):
        self.board_controller.initialize_puzzle(rating, theme)
        self.board_controller.make_next_move()

    def move_piece(self, move: str):
        piece_indexes = self.get_square_indexes(move[:2])
        target_indexes = self.get_square_indexes(move[2:])
        piece = self.get_widget_at(*piece_indexes)
        self.grid_layout.removeWidget(piece)
        self.grid_layout.addWidget(piece, *target_indexes)

    def get_square_indexes(self, square: str):
        player_color = self.board_controller.player_color
        column = ord(square[0]) - ord('a')
        row = 7 - (int(square[1]) - 1)
        if player_color == 'b':
            column = 7 - column
            row = 7 - row
        return row, column
    
    # TODO: rework (not working properly)
    def get_widget_at(self, row, column):
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and isinstance(item, QGridLayout):
                _, r, c, _ = self.grid_layout.getItemPosition(i)
                if r == row and c == column:
                    return item.widget()
        return None
    

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