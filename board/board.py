from optparse import Option
import os

from typing import Tuple, Optional
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QSizePolicy, QGraphicsColorizeEffect
)
from PyQt6.QtGui import QPixmap, QColor, QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal

from .pieces import *
from .board_controller import BoardController


class ChessBoard(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.board_style = 'dark_wood'
        self.piece_style = 'dark_wood'
        self.set_assets_dir()
        self.board_controller = BoardController(self)
        self.initialize_board()

    board_status_signal = pyqtSignal(int)

    def initialize_board(self) -> None:
        self.setMinimumSize(720, 720)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.setAcceptDrops(True)
        self.initialize_layout()
        self.initialize_squares()
        self.board_controller.setup_board_coordinates(init=True)

    def set_assets_dir(self) -> None:
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..',
            'assets', 'boards', self.board_style
        )
        self.assets_dir = os.path.normpath(assets_dir)

    def initialize_layout(self) -> None:
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid_layout)

    def initialize_squares(self) -> None:
        for widget in self.findChildren(ChessBoardSquare):
            widget.deleteLater()

        for row in range(8):
            for col in range(8):
                square = ChessBoardSquare(row, col, self)
                self.grid_layout.addWidget(square, row, col)

    def initialize_puzzle(self) -> None:
        self.clear_board()
        self.board_controller.initialize_puzzle()

    def get_current_puzzle_info(self) -> Tuple[Optional[int], Optional[str]]:
        return self.board_controller.get_current_puzzle_info()

    def clear_board(self) -> None:
        for widget in self.findChildren(ChessPiece):
            widget.deleteLater()
        self.board_controller.setup_board_coordinates(init=True)
        self.board_controller.is_board_active = False

    def update_status(self, status: int) -> None:
        self.board_status_signal.emit(status)

    def set_style(self, board_style: str, piece_style: str) -> None:
        self.board_style = board_style
        self.piece_style = piece_style
        self.set_assets_dir()
        self.initialize_squares()


class ChessBoardSquare(QLabel):
    def __init__(self, row: int, col: int, board: ChessBoard) -> None:
        super().__init__(board)
        self.board = board
        self.row = row
        self.col = col
        self.initialize_square()

    def initialize_square(self) -> None:
        self.setMaximumSize(90, 90)
        self.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
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

    def dragEnterEvent(self, event: QMouseEvent) -> None:
        widget = event.source()
        if widget:
            board: ChessBoard = self.parentWidget()
            square_name = board.board_controller.get_board_square_name(
                self.row, self.col
            )
            if board.board_controller.validate_move(widget, square_name):
                effect = QGraphicsColorizeEffect()
                effect.setColor(QColor('gray'))
                self.setGraphicsEffect(effect)
                event.accept()

    def dragLeaveEvent(self, event: QMouseEvent) -> None:
        self.setGraphicsEffect(None)
        event.accept()

    def dropEvent(self, event: QMouseEvent) -> None:
        self.setGraphicsEffect(None)
        widget = event.source()
        if widget:
            board: ChessBoard = self.parentWidget()
            board.board_controller.handle_player_move(
                widget, row=self.row, col=self.col
            )
            event.accept()