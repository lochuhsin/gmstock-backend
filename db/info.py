from typing import Generator

from sqlalchemy import select

from dto.db_object import Script
from utils.singleton import PostgresDB


def get_scripts() -> Generator:
    query = select(Script)
    return PostgresDB().session.scalars(query).all()


def insert_script(script: Script) -> None:
    PostgresDB().session.add(script)
    PostgresDB().session.commit()
