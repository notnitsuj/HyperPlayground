import os

from sqlmodel import SQLModel, create_engine, Session

from . import models


sqlite_dir_name = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(sqlite_dir_name, "hp_database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def instantiate_db():
    if not os.path.exists(sqlite_file_name):
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
