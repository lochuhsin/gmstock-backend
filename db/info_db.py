from dto.db_object import Script
from sqlalchemy import select, insert
from utils.util import backend_db
from typing import Generator

backend_session = backend_db()


def get_scripts() -> Generator:
    query = select(Script)
    return backend_session.scalars(query).all()


def insert_script() -> None:
    ...