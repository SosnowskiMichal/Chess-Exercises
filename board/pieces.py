import os

from typing import Optional
from PyQt6.QtWidgets import QLabel, QWidget, QSizePolicy, QGraphicsColorizeEffect
from PyQt6.QtGui import QPixmap, QDrag, QColor, QMouseEvent
from PyQt6.QtCore import Qt, QMimeData


class ChessPiece(QLabel):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(parent)
        self.square = square
        self.color = color
        self.piece_style = piece_style
        self.is_active = is_active
        self.set_assets_dir()
        self.initialize_piece()

    def initialize_piece(self) -> None:
        self.setMaximumSize(90, 90)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(True)
        if self.is_active:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setAcceptDrops(True)

    def set_assets_dir(self) -> None:
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'pieces', self.piece_style
        )
        self.assets_dir = os.path.normpath(assets_dir)

    def __str__(self) -> str:
        return f'{self.square} {self.color} {self.__class__.__name__}'
    
    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if not self.is_active or not self.parentWidget().board_controller.is_board_active:
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            drag = QDrag(self)
            mimeData = QMimeData()
            drag.setMimeData(mimeData)
            drag.setHotSpot(event.pos() - self.rect().topLeft())

            path = os.path.join(
                os.path.dirname(__file__), '..', 'assets', 'other', 'closedhand.png'
            )
            closed_hand_pixmap = QPixmap(path).scaled(15, 15)
            drag.setDragCursor(closed_hand_pixmap, Qt.DropAction.MoveAction)

            drag.exec(Qt.DropAction.MoveAction)
            self.setCursor(Qt.CursorShape.OpenHandCursor)

    def dragEnterEvent(self, event: QMouseEvent) -> None:
        widget = event.source()
        if widget:
            board = self.parentWidget()
            if board.board_controller.validate_move(widget, self.square):
                effect = QGraphicsColorizeEffect()
                effect.setColor(QColor('red'))
                self.setGraphicsEffect(effect)
                event.accept()

    def dragLeaveEvent(self, event: QMouseEvent) -> None:
        self.setGraphicsEffect(None)
        event.accept()

    def dropEvent(self, event: QMouseEvent) -> None:
        self.setGraphicsEffect(None)
        widget = event.source()
        if widget:
            board = self.parentWidget()
            board.board_controller.handle_player_move(
                widget, square=self.square
            )
            event.accept()
    

class King(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'king-{color}.png'))
        )


class Queen(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'queen-{color}.png'))
        )


class Rook(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'rook-{color}.png'))
        )


class Bishop(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'bishop-{color}.png'))
        )


class Knight(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'knight-{color}.png'))
        )


class Pawn(ChessPiece):
    def __init__(
        self,
        square: str,
        color: str,
        piece_style: str,
        is_active: bool,
        parent: QWidget
    ) -> None:
        super().__init__(square, color, piece_style, is_active, parent)
        self.setPixmap(
            QPixmap(os.path.join(self.assets_dir, f'pawn-{color}.png'))
        )