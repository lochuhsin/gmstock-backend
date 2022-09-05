from typing import Generator

from sqlalchemy import select

from dto.db_object import Script
from utils.util import backend_db

backend_session = backend_db()


def get_scripts() -> Generator:
    query = select(Script)
    return backend_session.scalars(query).all()


def insert_script(script: Script) -> None:
    backend_session.add(script)
    backend_session.commit()
