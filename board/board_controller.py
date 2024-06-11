import re

from PyQt6.QtWidgets import QWidget

from .pieces import *
from logic import PuzzleManager


class BoardController:
    def __init__(self, board):
        self.board = board
        self.puzzle_manager = PuzzleManager()
    
    def initialize_puzzle(self, rating: int = None, theme: str = None):
        self.clear_data()
        self.get_puzzle_data(rating, theme)
        self.parsed_fen = self.parse_fen(self.puzzle_moves.fen)
        self.player_color = 'w' if self.parsed_fen['active_color'] == 'b' else 'b'
        self.moves = self.puzzle_moves.moves.split()
        self.current_move = 0
        self.setup_board()

    def clear_data(self):
        self.puzzle_info = None
        self.puzzle_moves = None
        self.parsed_fen = None
        self.player_color = None
        self.moves = None
        self.current_move = None

    def get_puzzle_data(self, rating: int = None, theme: str = None):
        result = self.puzzle_manager.get_puzzle(rating, theme)
        self.puzzle_info, self.puzzle_moves = result if result else (None, None)
        print(self.puzzle_info)
        print(self.puzzle_moves)

    def parse_fen(self, fen: str):
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
    
    def setup_board(self):
        piece_placement = self.parsed_fen['piece_placement'].split('/')
        for row, row_placement in enumerate(piece_placement):
            col = 0
            for char in row_placement:
                if char.isdigit():
                    col += int(char)
                else:
                    piece = self.create_piece(char, self.board.theme, self.board)
                    curr_row = row if self.player_color == 'w' else 7 - row
                    curr_col = col if self.player_color == 'w' else 7 - col
                    self.board.grid_layout.addWidget(piece, curr_row, curr_col)
                    col += 1

    def create_piece(self, char: str, theme: str, parent: QWidget = None):
        color = 'white' if char.isupper() else 'black'
        if char in 'Kk':
            return King(color, theme, parent)
        elif char in 'Qq':
            return Queen(color, theme, parent)
        elif char in 'Rr':
            return Rook(color, theme, parent)
        elif char in 'Bb':
            return Bishop(color, theme, parent)
        elif char in 'Nn':
            return Knight(color, theme, parent)
        elif char in 'Pp':
            return Pawn(color, theme, parent)
        
    def make_next_move(self):
        if self.current_move < len(self.moves):
            move = self.moves[self.current_move]
            self.board.move_piece(move)
            self.current_move += 1