import logging
import shutil
from datetime import datetime

from config import settings
from db import info
from dto.db_object import Script


def get_scripts() -> list | None:
    return [script for script in info.get_scripts()]


def _savefile(filename: str, file) -> str:
    filepath = settings.file_storage + filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return filepath


def add_script(description: str | None, create_at: datetime, file) -> None:
    filename: str = file.filename
    filepath: str = _savefile(file.filename, file)
    logging.error(filepath)

    script: Script = Script(
        name=filename,
        description=description,
        filepath=filepath,
        created_at=create_at,
        updated_at=create_at,
    )
    info.insert_script(script)
