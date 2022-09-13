from typing import Generator

from fastapi import HTTPException
from sqlalchemy import select

from dto.db_object import Script
from utils.singleton import PostgresDB


def get_scripts() -> Generator:
    query = select(Script)
    return PostgresDB().session.scalars(query).all()


def insert_script(script: Script) -> int:

    try:
        PostgresDB().session.add(script)
        PostgresDB().session.flush()
        PostgresDB().session.commit()
    except Exception as e:
        raise HTTPException(400, f"error: {str(e)}")

    return script.id


def get_script_by_id(_id: int) -> Script:
    try:
        return PostgresDB().session.query(Script).get({"id": _id})
    except Exception as e:
        raise HTTPException(400, f"error: {str(e)}")


def remove_script_by_id(_id: int) -> None:
    try:
        PostgresDB().session.query(Script).filter(Script.id == _id).delete()
        PostgresDB().session.commit()
    except Exception as e:
        raise HTTPException(400, f"error: {str(e)}")
