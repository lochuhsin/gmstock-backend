from typing import Generator

from sqlalchemy import select

from dto.db_object import Script
from utils.singleton import BackendDB


def get_scripts() -> Generator:
    query = select(Script)
    return BackendDB().session.scalars(query).all()


def insert_script(script: Script) -> None:
    BackendDB().session.add(script)
    BackendDB().session.commit()
