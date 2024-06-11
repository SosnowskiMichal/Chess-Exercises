import os

from PyQt6.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ChessPiece(QLabel):
    def __init__(self, color: str, theme: str, parent: QWidget):
        super().__init__(parent)
        self.color = color
        self.theme = theme
        self.assets_dir = self.get_assets_dir(theme)
        self.initialize_piece()

    def initialize_piece(self):
        self.setMaximumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(True)

    def get_assets_dir(self, theme):
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'pieces', theme)
        return os.path.normpath(assets_dir)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.drag_start_position = event.position().toPoint()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() & Qt.MouseButton.LeftButton:
    #         drag = QDrag(self)
    #         mime_data = QMimeData()
            
    #         drag.setMimeData(mime_data)
    #         drag.setPixmap(self.pixmap())
    #         drag.setHotSpot(event.position().toPoint() - self.rect().topLeft())
            
    #         drag.exec(Qt.DropAction.MoveAction)
    

class King(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'king-{color}.png')))


class Queen(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'queen-{color}.png')))


class Rook(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'rook-{color}.png')))


class Bishop(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'bishop-{color}.png')))


class Knight(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'knight-{color}.png')))


class Pawn(ChessPiece):
    def __init__(self, color: str, theme: str = 'dark_wood', parent: QWidget = None):
        super().__init__(color, theme, parent)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'pawn-{color}.png')))