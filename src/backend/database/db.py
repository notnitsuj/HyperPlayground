import os

from sqlmodel import SQLModel, create_engine

from . import models


sqlite_dir_name = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(sqlite_dir_name, "hp_database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def instantiate_db():
    if not os.path.exists(sqlite_file_name):
        SQLModel.metadata.create_all(engine)
