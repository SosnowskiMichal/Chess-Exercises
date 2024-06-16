import os
import csv

from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from sqlalchemy import ForeignKey, create_engine, select, func


class Base(DeclarativeBase):
    pass


class PuzzleInfo(Base):
    __tablename__: str = 'puzzle_info'

    puzzle_id: Mapped[str] = mapped_column(primary_key=True)
    rating: Mapped[int]
    rating_deviation: Mapped[int]
    themes: Mapped[str]

    def __repr__(self):
        return (
            f'<PuzzleInfo(puzzle_id={self.puzzle_id}, '
            f'rating={self.rating}, '
            f'rating_deviation={self.rating_deviation}, '
            f'themes={self.themes})>'
        )


class PuzzleMoves(Base):
    __tablename__: str = 'puzzle_moves'

    puzzle_id: Mapped[str] = mapped_column(ForeignKey('puzzle_info.puzzle_id'), primary_key=True)
    fen: Mapped[str]
    moves: Mapped[str]

    def __repr__(self):
        return (
            f'<PuzzleMoves(puzzle_id={self.puzzle_id}, '
            f'fen={self.fen}, '
            f'moves={self.moves})>'
        )


class PuzzleManager:
    def __init__(self):
        self.db_path: str = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'puzzles.db'))
        self.engine: Engine = None
        self.session: Session = None
        self.rating_range = (None, None)
        self.puzzle_themes = None
        self.initialize_session()

    def initialize_session(self):
        if self.session:
            self.session.close()
            self.session = None
        if self.engine:
            self.engine.dispose()
            self.engine = None
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.session = Session(self.engine)

    def get_puzzle(self, min_rating: int = None, max_rating: int = None, theme: str = None):
        query = (
            select(PuzzleInfo, PuzzleMoves)
            .join(PuzzleMoves, PuzzleInfo.puzzle_id == PuzzleMoves.puzzle_id)
        )
        if min_rating is not None and max_rating is not None:
            query = query.filter(
                PuzzleInfo.rating >= min_rating,
                PuzzleInfo.rating <= max_rating
            )
        if theme is not None:
            query = query.filter(PuzzleInfo.themes.contains(theme))
        query = query.order_by(func.random()).limit(1)

        puzzle = self.session.execute(query).one_or_none()
        return puzzle
    
    def get_puzzle_themes(self):
        if self.puzzle_themes is not None:
            return self.puzzle_themes
        query = select(PuzzleInfo.themes).distinct()
        themes = self.session.execute(query).scalars().all()
        unique = set([t for theme in themes for t in theme.split()])
        self.puzzle_themes = sorted(unique)
        return self.puzzle_themes
    
    def get_rating_range(self):
        if self.rating_range != (None, None):
            return self.rating_range
        query = select(func.min(PuzzleInfo.rating), func.max(PuzzleInfo.rating))
        result = self.session.execute(query).one_or_none()
        self.rating_range = result
        return self.rating_range

    # def create_database(self):
    #     Base.metadata.create_all(self.engine)

    # def load_data(self):
    #     filepath: str = os.path.normpath(
    #         os.path.join(os.path.dirname(__file__), '..', 'data', 'db_puzzle.csv'))
    #     index: int = 1
    #     try:
    #         with open(filepath, 'r', encoding='utf-8', newline='') as file:
    #             file_reader = csv.reader(file)
    #             next(file_reader)
    #             for row in file_reader:
    #                 self.add_puzzle(row)
    #                 index += 1
    #         self.session.commit()
    #     except Exception as e:
    #         print(f'ERROR: {index}')
    #         print(e.__class__.__name__)

    # def add_puzzle(self, row: List[str]):
    #     puzzle_info: PuzzleInfo = PuzzleInfo(
    #         puzzle_id=row[0],
    #         rating=int(row[3]),
    #         rating_deviation=int(row[4]),
    #         themes=row[7]
    #     )
    #     puzzle_moves: PuzzleMoves = PuzzleMoves(
    #         puzzle_id=row[0],
    #         fen=row[1],
    #         moves=row[2]
    #     )
    #     self.session.add(puzzle_info)
    #     self.session.add(puzzle_moves)