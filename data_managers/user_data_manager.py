import os

from typing import Optional, Tuple, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from sqlalchemy import ForeignKey, create_engine, select, update, delete


class Base(DeclarativeBase):
    pass


class UserData(Base):
    __tablename__: str = 'user_data'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str]


class UserSettings(Base):
    __tablename__: str = 'user_settings'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_data.user_id'), primary_key=True
    )
    board_style: Mapped[str]
    piece_style: Mapped[str]


class UserPuzzleStatistics(Base):
    __tablename__: str = 'user_statistics'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_data.user_id'), primary_key=True
    )
    puzzles_played: Mapped[int]
    puzzles_solved: Mapped[int]


class UserThemeStatistics(Base):
    __tablename__: str = 'user_theme_statistics'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_data.user_id'), primary_key=True
    )
    theme: Mapped[str] = mapped_column(primary_key=True)
    puzzles_played: Mapped[int]
    puzzles_solved: Mapped[int]


class UserDataManager:
    def __init__(self) -> None:
        self.db_path = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), '..', 'data', 'users_db.db'
            )
        )
        self.engine = None
        self.session = None
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
        
    def create_database(self) -> None:
        Base.metadata.create_all(self.engine)

    def add_user(self, user_name: str) -> None:
        user_data = UserData(user_name=user_name)
        self.session.add(user_data)
        user_id = self.get_user_id(user_name)
        
        user_settings = UserSettings(
            user_id=user_id,board_style='dark_wood', piece_style='dark_wood'
        )
        user_puzzle_statistics = UserPuzzleStatistics(
            user_id=user_id, puzzles_played=0, puzzles_solved=0
        )
        self.session.add(user_settings)
        self.session.add(user_puzzle_statistics)
        self.session.commit()

    def get_user_id(self, user_name: str) -> Optional[int]:
        query = select(UserData.user_id).filter(UserData.user_name == user_name)
        user_id = self.session.execute(query).scalar()
        return user_id
    
    def get_user_settings(self, user_id: int) -> Optional[UserSettings]:
        query = select(UserSettings).filter(UserSettings.user_id == user_id)
        user_settings = self.session.execute(query).scalar()
        return user_settings
    
    def get_user_puzzle_statistics(self, user_id: int) -> Optional[UserPuzzleStatistics]:
        query = (
            select(UserPuzzleStatistics)
            .filter(UserPuzzleStatistics.user_id == user_id)
        )
        user_puzzle_statistics = self.session.execute(query).scalar()
        return user_puzzle_statistics
    
    def get_user_theme_statistics(
        self, user_id: int
    ) -> Tuple[Optional[Sequence], Optional[Sequence], Optional[Sequence]]:
        query_1 = (
            select(UserThemeStatistics)
            .where(UserThemeStatistics.user_id == user_id)
            .order_by(UserThemeStatistics.puzzles_played.desc())
            .limit(3)
        )
        query_2 = (
            select(
                UserThemeStatistics,
                (UserThemeStatistics.puzzles_solved / UserThemeStatistics.puzzles_played)
                .label('percentage')
            )
            .where(UserThemeStatistics.user_id == user_id)
            .order_by(
                (UserThemeStatistics.puzzles_solved / UserThemeStatistics.puzzles_played)
                .desc()
            )
            .limit(3)
        )
        query_3 = (
            select(
                UserThemeStatistics,
                (UserThemeStatistics.puzzles_solved / UserThemeStatistics.puzzles_played)
                .label('percentage')
            )
            .where(UserThemeStatistics.user_id == user_id)
            .order_by(
                (UserThemeStatistics.puzzles_solved / UserThemeStatistics.puzzles_played)
                .asc()
            )
            .limit(3)
        )

        most_popular = self.session.execute(query_1).all()
        best_percentage = self.session.execute(query_2).all()
        worst_percentage = self.session.execute(query_3).all()

        return most_popular, best_percentage, worst_percentage
    
    def reset_user_progress(self, user_id: int) -> None:
        try:
            query = (
                update(UserPuzzleStatistics)
                .where(UserPuzzleStatistics.user_id == user_id)
                .values(puzzles_played=0, puzzles_solved=0)
            )
            self.session.execute(query)
            
            query = (
                delete(UserThemeStatistics)
                .where(UserThemeStatistics.user_id == user_id)
            )
            self.session.execute(query)
            self.session.commit()
        except Exception as e:
            self.session.rollback()

    def update_user_settings(
        self, user_id: int, board_style: str, piece_style: str
    ) -> None:
        try:
            query = (
                update(UserSettings)
                .where(UserSettings.user_id == user_id)
                .values(board_style=board_style, piece_style=piece_style)
            )
            self.session.execute(query)
            self.session.commit()
        except Exception as e:
            self.session.rollback()

    def update_user_puzzle_statistics(
        self, user_id: int, themes: str, solved: bool
    ) -> None:
        try:
            query = (
                update(UserPuzzleStatistics)
                .where(UserPuzzleStatistics.user_id == user_id)
                .values(
                    puzzles_played=UserPuzzleStatistics.puzzles_played + 1,
                    puzzles_solved=UserPuzzleStatistics.puzzles_solved + int(solved)
                )
            )
            self.session.execute(query)

            themes = themes.split()
            for theme in themes:
                query = (
                    select(UserThemeStatistics)
                    .filter(
                        UserThemeStatistics.user_id == user_id,
                        UserThemeStatistics.theme == theme
                    )
                )
                record = self.session.execute(query).scalar()
                if record:
                    query = (
                        update(UserThemeStatistics)
                        .where(
                            UserThemeStatistics.user_id == user_id,
                            UserThemeStatistics.theme == theme
                        )
                        .values(
                            puzzles_played=UserThemeStatistics.puzzles_played + 1,
                            puzzles_solved=UserThemeStatistics.puzzles_solved + int(solved)
                        )
                    )
                    self.session.execute(query)
                else:
                    user_theme_statistics = UserThemeStatistics(
                        user_id=user_id,
                        theme=theme,
                        puzzles_played=1,
                        puzzles_solved=int(solved)
                    )
                    self.session.add(user_theme_statistics)
            self.session.commit()
        except Exception as e:
            self.session.rollback()