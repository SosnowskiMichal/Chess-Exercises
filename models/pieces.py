import os

from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap


class ChessPiece(QLabel):
    def __init__(self, color: str, theme: str):
        super().__init__()
        self.color = color
        self.theme = theme
        self.assets_dir = self.get_assets_dir(theme)
        self.initialize_piece()

    def initialize_piece(self):
        self.setMaximumSize(100, 80)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
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
    def __init___(self, color: str, theme: str = 'dark_wood'):
        super().__init__(color, theme)
        self.setPixmap(QPixmap(os.path.join(self.assets_dir, f'king-{color}.png')))
        self.setMaximumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)