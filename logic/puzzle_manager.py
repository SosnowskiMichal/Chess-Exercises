import os
import csv

from typing import List, Iterator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from sqlalchemy import ForeignKey, create_engine, func, select


class Base(DeclarativeBase):
    pass


class PuzzleInfo(Base):
    __tablename__: str = 'puzzle_info'

    puzzle_id: Mapped[str] = mapped_column(primary_key=True)
    rating: Mapped[int]
    rating_deviation: Mapped[int]
    themes: Mapped[str]


class PuzzleMoves(Base):
    __tablename__: str = 'puzzle_moves'

    puzzle_id: Mapped[str] = mapped_column(
        ForeignKey('puzzle_info.puzzle_id'), primary_key=True)
    fen: Mapped[str]
    moves: Mapped[str]


class PuzzleManager:
    def __init__(self):
        self.db_path: str = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'puzzles.db'))
        self.engine: Engine = None
        self.session: Session = None
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

    # def create_database(self):
    #     Base.metadata.create_all(self.engine)

    # def load_data(self):
    #     filepath: str = os.path.normpath(
    #         os.path.join(os.path.dirname(__file__), '..', 'data', 'db_puzzle.csv'))
    #     index: int = 1
    #     try:
    #         with open(filepath, 'r', encoding='utf-8', newline='') as file:
    #             file_reader: Iterator[List[str]] = csv.reader(file)
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