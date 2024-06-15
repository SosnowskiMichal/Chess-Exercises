import re
import chess
import threading

from typing import Dict, List, Tuple, Optional
from PyQt6.QtWidgets import QWidget

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
        threading.Timer(1, self.make_next_computer_move).start()
        print(self.legal_moves)

    def clear_data(self) -> None:
        self.puzzle_info = None
        self.puzzle_moves = None
        self.parsed_fen = None
        self.player_color = None
        self.moves = None
        self.current_move = None

    def get_puzzle_data(self, rating: int = None, theme: str = None) -> None:
        result = self.puzzle_manager.get_puzzle(rating, theme)
        self.puzzle_info, self.puzzle_moves = result if result else (None, None)
        # TODO: remove later
        print(self.puzzle_info)
        print(self.puzzle_moves)

    def initialize_data(self) -> None:
        self.pieces = []
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
        target_square = square if square is not None else self.get_board_square_name(row, col)
        if self.validate_puzzle_move(piece, target_square):
            self.current_move += 1
            move = f'{piece.square}{target_square}'
            self.move_piece_on_board(piece, target_square)
            self.board_controller.push(chess.Move.from_uci(move))
            is_piece_captured, target_piece = self.validate_capture(piece, target_square)
            if is_piece_captured:
                self.capture_piece(target_piece)
            threading.Timer(1, self.make_next_computer_move).start()

    def validate_move(self, piece: ChessPiece, target_square: str) -> bool:
        move = f'{piece.square}{target_square}'
        return move in self.legal_moves

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
            is_piece_captured, target_piece = self.validate_capture(piece, move[2:])
            if is_piece_captured:
                self.capture_piece(target_piece)
            self.move_piece_on_board(piece, move[2:])
            self.board_controller.push(chess.Move.from_uci(move))
            self.current_move += 1
            self.legal_moves = self.generate_legal_moves()

    def get_piece_at(self, square: str) -> Optional[ChessPiece]:
        for piece in self.pieces:
            if piece.square == square:
                return piece
        return None
    
    def move_piece_on_board(self, piece: ChessPiece, target_square: str) -> None:
        # TODO: check for promotion and handle it
        target_indexes = self.get_board_square_indexes(target_square)
        self.board.grid_layout.removeWidget(piece)
        self.board.grid_layout.addWidget(piece, *target_indexes)
        piece.square = target_square

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
    
    def complete_puzzle(self) -> None:
        # TODO: implement puzzle completion logic
        if self.current_move >= len(self.moves):
            print('Puzzle completed!')
        pass