import os

from typing import List, Optional, Tuple
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from sqlalchemy import ForeignKey, create_engine, select, func, Row


class Base(DeclarativeBase):
    pass


class PuzzleInfo(Base):
    __tablename__: str = 'puzzle_info'

    puzzle_id: Mapped[str] = mapped_column(primary_key=True)
    rating: Mapped[int]
    rating_deviation: Mapped[int]
    themes: Mapped[str]

    def __repr__(self) -> str:
        return (
            f'<PuzzleInfo(puzzle_id={self.puzzle_id}, '
            f'rating={self.rating}, '
            f'rating_deviation={self.rating_deviation}, '
            f'themes={self.themes})>'
        )


class PuzzleMoves(Base):
    __tablename__: str = 'puzzle_moves'

    puzzle_id: Mapped[str] = mapped_column(
        ForeignKey('puzzle_info.puzzle_id'), primary_key=True
    )
    fen: Mapped[str]
    moves: Mapped[str]

    def __repr__(self) -> str:
        return (
            f'<PuzzleMoves(puzzle_id={self.puzzle_id}, '
            f'fen={self.fen}, '
            f'moves={self.moves})>'
        )


class PuzzleManager:
    def __init__(self) -> None:
        self.db_path = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), '..', 'data', 'puzzles_db.db'
            )
        )
        self.engine = None
        self.session = None
        self.rating_range = (None, None)
        self.puzzle_themes = None
        self.initialize_session()

    def initialize_session(self) -> None:
        if self.session:
            self.session.close()
            self.session = None
        if self.engine:
            self.engine.dispose()
            self.engine = None

        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.session = Session(self.engine)

    def get_puzzle(
        self,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        theme: Optional[str] = None
    ) -> Optional[Row[Tuple[PuzzleInfo, PuzzleMoves]]]:
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
    
    def get_puzzle_themes(self) -> List[str]:
        if self.puzzle_themes is not None:
            return self.puzzle_themes
        
        query = select(PuzzleInfo.themes).distinct()
        themes = self.session.execute(query).scalars().all()
        unique = set([t for theme in themes for t in theme.split()])
        self.puzzle_themes = sorted(unique)
        return self.puzzle_themes
    
    def get_rating_range(self) -> Tuple[Optional[int], Optional[int]]:
        if self.rating_range != (None, None):
            return self.rating_range
        
        query = select(func.min(PuzzleInfo.rating), func.max(PuzzleInfo.rating))
        result = self.session.execute(query).one_or_none()
        self.rating_range = result
        return self.rating_range