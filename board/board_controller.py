import re
import chess
import threading

from typing import Dict, List, Tuple, Optional
from PyQt6.QtWidgets import QWidget, QDialog, QDialogButtonBox, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

from .pieces import *
from logic import PuzzleManager


class BoardController:
    def __init__(self, board) -> None:
        self.board = board
        self.puzzle_manager = PuzzleManager()
    
    def initialize_puzzle(self, rating: int = None, theme: str = None) -> None:
        self.clear_data()
        self.get_puzzle_data(rating, theme)
        self.initialize_data()
        self.setup_board()
        # threading.Timer(1, self.make_next_computer_move).start()
        self.make_next_computer_move()

    def clear_data(self) -> None:
        self.puzzle_info = None
        self.puzzle_moves = None
        self.parsed_fen = None
        self.player_color = None
        self.moves = None
        self.current_move = None

    def get_puzzle_data(self, rating: int = None, theme: str = None) -> None:
        result = self.puzzle_manager.get_puzzle(rating, theme)
        # result = self.puzzle_manager.get_puzzle_by_id('007fJ')
        self.puzzle_info, self.puzzle_moves = result if result else (None, None)
        # TODO: remove later
        print(self.puzzle_info)
        print(self.puzzle_moves)

    def initialize_data(self) -> None:
        self.pieces = []
        self.is_board_active = True
        self.board_controller = chess.Board(self.puzzle_moves.fen)
        self.legal_moves = self.generate_legal_moves()
        self.parsed_fen = self.parse_fen(self.puzzle_moves.fen)
        self.player_color = 'w' if self.parsed_fen['active_color'] == 'b' else 'b'
        self.moves = self.puzzle_moves.moves.split()
        self.current_move = 0

    def parse_fen(self, fen: str) -> Optional[Dict[str, str]]:
        fen_pattern = (
            r'(?P<piece_placement>[^ ]+) '
            r'(?P<active_color>[wb]) '
            r'(?P<castling_availability>[KQkq-]+) '
            r'(?P<en_passant_target_square>[a-h][3-6]|-) '
            r'(?P<halfmove_clock>\d+) '
            r'(?P<fullmove_number>\d+)'
        )
        fen_match = re.match(fen_pattern, fen)
        return fen_match.groupdict() if fen_match else None
    
    def setup_board(self) -> None:
        piece_placement = self.parsed_fen['piece_placement'].split('/')
        for row, row_placement in enumerate(piece_placement):
            col = 0
            for char in row_placement:
                if char.isdigit():
                    col += int(char)
                else:
                    curr_row = row if self.player_color == 'w' else 7 - row
                    curr_col = col if self.player_color == 'w' else 7 - col
                    square = f'{chr(col + ord('a'))}{8 - row}'
                    piece = self.create_piece(char, square, self.board.theme, self.board)
                    self.pieces.append(piece)
                    self.board.grid_layout.addWidget(piece, curr_row, curr_col)
                    col += 1

    def create_piece(
        self, char: str, square: str, theme: str, parent: QWidget = None
    ) -> ChessPiece:
        color = 'white' if char.isupper() else 'black'
        is_active = color[0] == self.player_color
        if char in 'Kk':
            return King(square, color, theme, is_active, parent)
        elif char in 'Qq':
            return Queen(square, color, theme, is_active, parent)
        elif char in 'Rr':
            return Rook(square, color, theme, is_active, parent)
        elif char in 'Bb':
            return Bishop(square, color, theme, is_active, parent)
        elif char in 'Nn':
            return Knight(square, color, theme, is_active, parent)
        elif char in 'Pp':
            return Pawn(square, color, theme, is_active, parent)
        
    def generate_legal_moves(self) -> List[str]:
        generator = self.board_controller.generate_legal_moves()
        return [move.uci() for move in generator]
    
    def handle_player_move(
        self, piece: ChessPiece, row: int = None, col: int = None, square: str = None
    ) -> None:
        if not self.is_board_active:
            return
        target_square = square if square is not None else self.get_board_square_name(row, col)
        if self.check_for_promotion(piece, target_square):
            promotion_piece = self.select_promotion_piece(piece.color, piece.theme)
            target_square_with_promotion = f'{target_square}{promotion_piece}'
            if self.validate_puzzle_move(piece, target_square_with_promotion):
                self.handle_promotion_move(piece, target_square, promotion_piece)
                # threading.Timer(1, self.make_next_computer_move).start()
                self.make_next_computer_move()
            else:
                self.signal_incorrect_move()
        elif self.validate_puzzle_move(piece, target_square):
            self.handle_standard_move(piece, target_square)
            # threading.Timer(1, self.make_next_computer_move).start()
            self.make_next_computer_move()
        else:
            self.signal_incorrect_move()

    def handle_standard_move(self, piece: ChessPiece, target_square: str) -> None:
        self.current_move += 1
        move = f'{piece.square}{target_square}'
        self.board_controller.push(chess.Move.from_uci(move))
        self.move_piece(piece, target_square)
        is_piece_captured, target_piece = self.validate_capture(piece, target_square)
        if is_piece_captured:
            self.capture_piece(target_piece)
        self.signal_correct_move()

    def handle_promotion_move(self, piece: ChessPiece, target_square: str, promotion_piece: str) -> None:
        self.current_move += 1
        move = f'{piece.square}{target_square}{promotion_piece}'
        self.board_controller.push(chess.Move.from_uci(move))
        promotion_piece = promotion_piece.upper() if piece.color == 'white' else promotion_piece
        pr_piece = self.create_piece(promotion_piece, target_square, self.board.theme, self.board)
        self.pieces.append(pr_piece)
        self.capture_piece(piece)
        self.board.grid_layout.addWidget(pr_piece, *self.get_board_square_indexes(target_square))
        # check if piece is captured
        is_piece_captured, target_piece = self.validate_capture(pr_piece, target_square)
        if is_piece_captured:
            self.capture_piece(target_piece)
        self.signal_correct_move()
        print(f'Promotion to {target_square}!')

    def select_promotion_piece(self, color: str, theme: str) -> Optional[str]:
        dialog = PromotionChoiceWindow(color, theme)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            promotion_piece = dialog.result
            print(f'Button {dialog.result} clicked')
            return promotion_piece
        return None

    def validate_move(self, piece: ChessPiece, target_square: str) -> bool:
        move = f'{piece.square}{target_square}'
        promotion_moves = [f'{move}{promotion}' for promotion in 'qrbn']
        return (
            move in self.legal_moves or
            any(pr_move in self.legal_moves for pr_move in promotion_moves)
        )

    def validate_puzzle_move(self, piece: ChessPiece, target_square: str) -> bool:
        expected_move = self.moves[self.current_move]
        move = f'{piece.square}{target_square}'
        return move == expected_move

    def validate_capture(self, piece: ChessPiece, target_square: str) -> Tuple[bool, ChessPiece]:
        piece_color = piece.color
        for other_piece in self.pieces:
            if other_piece.square == target_square and other_piece.color != piece_color:
                return True, other_piece
        return False, None
    
    def capture_piece(self, piece: ChessPiece) -> None:
        self.pieces.remove(piece)
        self.board.grid_layout.removeWidget(piece)

    def make_next_computer_move(self) -> None:
        if self.current_move >= len(self.moves):
            self.complete_puzzle()
        else:
            move = self.moves[self.current_move]
            piece = self.get_piece_at(move[:2])
            if len(move) == 4:
                self.handle_standard_move(piece, move[2:])
            else:
                self.handle_promotion_move(piece, move[2:4], move[4])
            self.legal_moves = self.generate_legal_moves()
            print(self.legal_moves)
    
    def move_piece(self, piece: ChessPiece, target_square: str) -> None:
        is_castling, castling_side = self.check_for_castling(piece, target_square)
        if is_castling:
            self.handle_castling(piece, castling_side)
        target_indexes = self.get_board_square_indexes(target_square)
        self.board.grid_layout.removeWidget(piece)
        self.board.grid_layout.addWidget(piece, *target_indexes)
        piece.square = target_square

    def check_for_castling(self, piece: ChessPiece, target_square: str) -> Tuple[bool, str]:
        move = f'{piece.square}{target_square}'
        if move in ('e1c1', 'e1g1', 'e8c8', 'e8g8'):
            return True, 'kingside' if move[2] == 'g' else 'queenside'
        return False, None
    
    def handle_castling(self, piece: ChessPiece, castling_side: str) -> None:
        rook_initial_square = (
            ('a1' if piece.color == 'white' else 'a8') if castling_side == 'queenside' 
            else ('h1' if piece.color == 'white' else 'h8')
        )
        rook_target_square = (
            ('d1' if piece.color == 'white' else 'd8') if castling_side == 'queenside' 
            else ('f1' if piece.color == 'white' else 'f8')
        )
        rook_target_indexes = self.get_board_square_indexes(rook_target_square)
        rook = self.get_piece_at(rook_initial_square)
        self.board.grid_layout.removeWidget(rook)
        self.board.grid_layout.addWidget(rook, *rook_target_indexes)
        rook.square = rook_target_square

    def check_for_promotion(self, piece: ChessPiece, target_square: str) -> None:
        return isinstance(piece, Pawn) and target_square[1] in ('1', '8')

    def get_piece_at(self, square: str) -> Optional[ChessPiece]:
        for piece in self.pieces:
            if piece.square == square:
                return piece
        return None

    def get_board_square_indexes(self, square: str) -> Tuple[int, int]:
        player_color = self.player_color
        column = ord(square[0]) - ord('a')
        row = 7 - (int(square[1]) - 1)
        if player_color == 'b':
            column = 7 - column
            row = 7 - row
        return row, column
    
    def get_board_square_name(self, row: int, col: int) -> str:
        player_color = self.player_color
        if player_color == 'w':
            col_name = chr(col + ord('a'))
            row_num = 8 - row
        else:
            col_name = chr(7 - col + ord('a'))
            row_num = row + 1
        return f'{col_name}{row_num}'
    
    def signal_correct_move(self) -> None:
        print('Correct move!')

    def signal_incorrect_move(self) -> None:
        print('Incorrect move!')

    def complete_puzzle(self) -> None:
        # TODO: implement puzzle completion logic
        if self.current_move >= len(self.moves):
            self.is_board_active = False
            print('Puzzle completed!')
        pass


class PromotionChoiceWindow(QDialog):
    def __init__(self, color: str, theme: str) -> None:
        super().__init__()
        self.color = color
        self.theme = theme
        self.setWindowTitle('Promotion')
        self.set_assets_dir()
        self.initialize_layout()
        self.initialize_promotion_choices()
        self.connect_signals()
    
    def set_assets_dir(self) -> None:
        self.assets_dir = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'pieces', self.theme))

    def initialize_layout(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.button_box = QDialogButtonBox()
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.button_box)

    def initialize_promotion_choices(self) -> None:
        self.queen_button = self.button_box.addButton('', QDialogButtonBox.ButtonRole.AcceptRole)
        self.queen_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.queen_button.setIcon(QIcon(os.path.join(self.assets_dir, f'queen-{self.color}.png')))
        self.queen_button.setIconSize(QSize(90, 90))

        self.rook_button = self.button_box.addButton('', QDialogButtonBox.ButtonRole.AcceptRole)
        self.rook_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rook_button.setIcon(QIcon(os.path.join(self.assets_dir, f'rook-{self.color}.png')))
        self.rook_button.setIconSize(QSize(90, 90))

        self.bishop_button = self.button_box.addButton('', QDialogButtonBox.ButtonRole.AcceptRole)
        self.bishop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bishop_button.setIcon(QIcon(os.path.join(self.assets_dir, f'bishop-{self.color}.png')))
        self.bishop_button.setIconSize(QSize(90, 90))

        self.knight_button = self.button_box.addButton('', QDialogButtonBox.ButtonRole.AcceptRole)
        self.knight_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.knight_button.setIcon(QIcon(os.path.join(self.assets_dir, f'knight-{self.color}.png')))
        self.knight_button.setIconSize(QSize(90, 90))

    def connect_signals(self) -> None:
        self.queen_button.clicked.connect(self.queen_button_clicked)
        self.rook_button.clicked.connect(self.rook_button_clicked)
        self.bishop_button.clicked.connect(self.bishop_button_clicked)
        self.knight_button.clicked.connect(self.knight_button_clicked)

    def queen_button_clicked(self) -> None:
        self.result = 'q'
        self.accept()

    def rook_button_clicked(self) -> None:
        self.result = 'r'
        self.accept()

    def bishop_button_clicked(self) -> None:
        self.result = 'b'
        self.accept()

    def knight_button_clicked(self) -> None:
        self.result = 'n'
        self.accept()