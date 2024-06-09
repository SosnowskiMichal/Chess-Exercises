import os

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class UserSettings(Base):
    __tablename__: str = 'user_settings'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    board_style: Mapped[str]
    piece_style: Mapped[str]


class UserStatistics(Base):
    __tablename__: str = 'user_statistics'
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add user statistics columns


class DataManager:
    def __init__(self):
        self.db_path: str = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db'))
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
        
    def create_database(self):
        Base.metadata.create_all(self.engine)