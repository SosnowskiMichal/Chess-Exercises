import os

from typing import Tuple
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QGraphicsColorizeEffect
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, pyqtSignal

from .pieces import *
from .board_controller import BoardController


class ChessBoard(QWidget):
    def __init__(self, theme: str = 'dark_wood') -> None:
        super().__init__()
        self.theme = theme
        self.assets_dir = self.get_assets_dir(self.theme)
        self.board_controller = BoardController(self)
        self.initialize_board()

    board_status_signal = pyqtSignal(int)

    def initialize_board(self) -> None:
        self.setAcceptDrops(True)
        # self.setMinimumSize(800, 800)
        # self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.initialize_layout()
        self.initialize_squares()
        # self.initialize_puzzle()

    def get_assets_dir(self, theme: str) -> str:
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'boards', theme)
        return os.path.normpath(assets_dir)

    def initialize_layout(self) -> None:
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid_layout)

    def initialize_squares(self) -> None:
        for row in range(8):
            for col in range(8):
                square = ChessBoardSquare(row, col, self)
                self.grid_layout.addWidget(square, row, col)

    def initialize_puzzle(self, rating: int = None, theme: str = None) -> None:
        self.clear_board()
        self.board_controller.initialize_puzzle(rating, theme)

    def get_current_puzzle_info(self) -> Tuple[int, str]:
        return self.board_controller.get_current_puzzle_info()

    def clear_board(self) -> None:
        for widget in self.findChildren(ChessPiece):
            widget.deleteLater()

    def update_status(self, status: int) -> None:
        self.board_status_signal.emit(status)


class ChessBoardSquare(QLabel):
    def __init__(self, row: int, col: int, board: ChessBoard = None) -> None:
        super().__init__(board)
        self.board = board
        self.row = row
        self.col = col
        self.initialize_square()

    def initialize_square(self) -> None:
        self.setMaximumSize(90, 90)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setAcceptDrops(True)
        self.set_background()

    def set_background(self) -> None:
        self.setScaledContents(True)
        assets_dir = self.board.assets_dir
        if (self.row + self.col) % 2 == 0:
            background_image = QPixmap(os.path.join(assets_dir, 'white.png'))
            self.setPixmap(background_image)
        else:
            background_image = QPixmap(os.path.join(assets_dir, 'black.png'))
            self.setPixmap(background_image)

    def dragEnterEvent(self, event) -> None:
        # TODO: rework coloring
        widget = event.source()
        if widget:
            board: ChessBoard = self.parentWidget()
            square_name = board.board_controller.get_board_square_name(self.row, self.col)
            if board.board_controller.validate_move(widget, square_name):
                effect = QGraphicsColorizeEffect()
                effect.setColor(QColor('red'))
                self.setGraphicsEffect(effect)
                event.accept()

    def dragLeaveEvent(self, event) -> None:
        self.setGraphicsEffect(None)
        event.accept()

    def dropEvent(self, event) -> None:
        self.setGraphicsEffect(None)
        widget = event.source()
        if widget:
            board: ChessBoard = self.parentWidget()
            board.board_controller.handle_player_move(widget, row=self.row, col=self.col)
            event.accept()