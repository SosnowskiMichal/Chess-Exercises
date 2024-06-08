import os

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap


class Board(QWidget):
    def __init__(self, style='dark_wood', config=None):
        super().__init__()
        self.pieces = []
        self.assets_dir = self.get_assets_dir(style)
        self.initialize_layout()
        self.initialize_board()
        self.initialize_pieces(config)

    def get_assets_dir(self, style):
        assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', style)
        return os.path.normpath(assets_dir)

    def initialize_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)

    def initialize_board(self):
        for row in range(8):
            for col in range(8):
                square = ChessBoardSquare(row, col, self)
                self.grid_layout.addWidget(square, row, col)

    def initialize_pieces(self, config):
        self.pieces.clear()
        # TODO: implement


class ChessBoardSquare(QLabel):
    def __init__(self, row, col, board: Board = None):
        super().__init__(board)
        self.board = board
        self.row = row
        self.col = col
        self.set_background()

    def set_background(self):
        self.setScaledContents(True)
        assets_dir = self.board.assets_dir
        if (self.row + self.col) % 2 == 0:
            background_image = QPixmap(
                os.path.join(assets_dir, 'board', 'black.png'))
            self.setPixmap(background_image)
        else:
            background_image = QPixmap(
                os.path.join(assets_dir, 'board', 'white.png'))
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


class ChessPiece(QLabel):
    def __init__(self, piece_image):
        super().__init__()
    #     self.setPixmap(QPixmap(piece_image))
    #     self.setScaledContents(True)
    #     self.setFixedSize(80, 80)
        
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